from __future__ import annotations

import copy

import pytest

from anyang_loop.intake_control import (
    authorize_review,
    bootstrap_context,
    decide_context,
    intake_status,
    manifest_hash,
    persist_context,
    propose_context,
    render_intake_status,
    validate_manifest,
)
from anyang_loop.ops_db import connect, migrate
from anyang_loop.ops_render import audit_data
from anyang_loop.ops_service import OpsError, add_actor, grant_authority, init_tenant


def manifest(version: str = "CTX-001", base_version: str | None = None, readiness: str = "ready") -> dict:
    return {
        "business_reference": "example-business",
        "version": version,
        "base_version": base_version,
        "external_content_ref": f"tenant-private://example/context/{version}",
        "authority_receipt_ref": "operator-receipt://example/authority-001",
        "readiness": readiness,
        "created_by": "Owner",
        "evidence": [
            {
                "class": "confirmed",
                "kind": "storefront",
                "summary": "The public storefront is in the approved intake scope.",
                "source_ref": "https://example.test/store",
                "confidence": "high",
                "sensitivity": "public",
            },
            {
                "class": "estimate",
                "kind": "capacity_proxy",
                "summary": "A low-confidence public-sales proxy is available for planning only.",
                "source_ref": "public-estimate://example/capacity",
                "confidence": "low",
                "sensitivity": "internal",
            },
        ],
        "unresolved_gates": [] if readiness != "hold" else ["Confirm the exact effective base context."],
    }


@pytest.fixture()
def ledger(tmp_path):
    connection = connect(tmp_path / "ops.db", create_parent=True)
    migrate(connection, "2026-07-17T00:00:00Z")
    init_tenant(
        connection,
        slug="example",
        name="Example",
        policy_profile="test",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp="2026-07-17T00:00:00Z",
    )
    actor = add_actor(connection, "example", "Owner", "owner")
    grant_authority(connection, "example", actor.id, "business_context", None, None)
    try:
        yield connection, actor.id
    finally:
        connection.close()


def make_effective(connection, actor_id: str, value: dict) -> str:
    proposed = propose_context(connection, "example", value)
    digest = proposed.details["content_hash"]
    decide_context(connection, "example", value["version"], actor_id, "approved", digest)
    persist_context(
        connection,
        "example",
        value["version"],
        actor_id,
        digest,
        f"tenant-private://example/effective/{value['version']}",
    )
    return digest


def test_full_lifecycle_keeps_review_authorization_separate(ledger):
    connection, actor_id = ledger
    value = manifest()
    proposal = propose_context(connection, "example", value)
    digest = proposal.details["content_hash"]

    with pytest.raises(OpsError, match="does not match"):
        decide_context(connection, "example", "CTX-001", actor_id, "approved", "wrong")

    decided = decide_context(connection, "example", "CTX-001", actor_id, "approved", digest)
    assert decided.details["state"] == "awaiting_persistence"
    before = intake_status(connection, "example")
    assert before["effective_context"] is None
    assert before["operating_review_authorization"] is None
    assert "Confirm preservation" in before["next_action"]

    persisted = persist_context(
        connection,
        "example",
        "CTX-001",
        actor_id,
        digest,
        "tenant-private://example/effective/CTX-001",
    )
    assert persisted.details["state"] == "effective"
    effective = intake_status(connection, "example")
    assert effective["effective_context"]["version"] == "CTX-001"
    assert effective["evidence"]["estimate"][0]["confidence"] == "low"
    assert "authorizes the first operating review" in effective["next_action"]

    authorize_review(connection, "example", "CTX-001", actor_id, "approved", digest)
    final = intake_status(connection, "example")
    assert final["operating_review_authorization"]["decision"] == "approved"
    assert "separately authorized operating review" in final["next_action"]
    assert "Business Intake Status Receipt" in render_intake_status(final)
    assert audit_data(connection, "example")["ok"]


def test_replacement_requires_current_exact_base_and_supersedes_atomically(ledger):
    connection, actor_id = ledger
    first_hash = make_effective(connection, actor_id, manifest())
    assert first_hash

    with pytest.raises(OpsError, match="Stale or missing base version"):
        propose_context(connection, "example", manifest("CTX-002", "CTX-000"))

    replacement = manifest("CTX-002", "CTX-001")
    second_hash = manifest_hash(replacement)
    propose_context(connection, "example", replacement)
    decide_context(connection, "example", "CTX-002", actor_id, "approved", second_hash)
    persist_context(
        connection,
        "example",
        "CTX-002",
        actor_id,
        second_hash,
        "tenant-private://example/effective/CTX-002",
    )
    rows = connection.execute(
        "SELECT version_label, state FROM business_context_version ORDER BY version_label"
    ).fetchall()
    assert [(row["version_label"], row["state"]) for row in rows] == [
        ("CTX-001", "superseded"),
        ("CTX-002", "effective"),
    ]


def test_exact_legacy_bootstrap_requires_receipts_hash_and_empty_ledger(ledger):
    connection, actor_id = ledger
    existing = manifest("CTX-LEGACY")
    digest = manifest_hash(existing)
    with pytest.raises(OpsError, match="hash does not match"):
        bootstrap_context(
            connection,
            "example",
            existing,
            actor_id,
            "wrong",
            "tenant-private://example/approval/legacy",
            "tenant-private://example/persistence/legacy",
        )
    result = bootstrap_context(
        connection,
        "example",
        existing,
        actor_id,
        digest,
        "tenant-private://example/approval/legacy",
        "tenant-private://example/persistence/legacy",
    )
    assert result.details["state"] == "effective"
    assert audit_data(connection, "example")["ok"]
    with pytest.raises(OpsError, match="empty business-context ledger"):
        bootstrap_context(
            connection,
            "example",
            manifest("CTX-OTHER"),
            actor_id,
            manifest_hash(manifest("CTX-OTHER")),
            "tenant-private://example/approval/other",
            "tenant-private://example/persistence/other",
        )


def test_hold_and_missing_authority_fail_closed(ledger):
    connection, actor_id = ledger
    held = manifest(readiness="hold")
    digest = manifest_hash(held)
    propose_context(connection, "example", held)
    with pytest.raises(OpsError, match="Hold context cannot be approved"):
        decide_context(connection, "example", "CTX-001", actor_id, "approved", digest)

    outsider = add_actor(connection, "example", "Reviewer", "reviewer")
    with pytest.raises(OpsError, match="lacks current business_context authority"):
        decide_context(connection, "example", "CTX-001", outsider.id, "rejected", digest)


def test_status_reports_proposed_rejected_and_hold_next_actions(ledger):
    connection, actor_id = ledger
    proposed = manifest()
    digest = manifest_hash(proposed)
    propose_context(connection, "example", proposed)
    assert "owner's decision" in intake_status(connection, "example")["next_action"]
    decide_context(connection, "example", "CTX-001", actor_id, "rejected", digest)
    assert "bootstrap or propose" in intake_status(connection, "example")["next_action"]

    held = manifest("CTX-002", readiness="hold")
    propose_context(connection, "example", held)
    status = intake_status(connection, "example")
    assert status["active_proposal"]["state"] == "hold"
    assert "Resolve the recorded missing evidence" in status["next_action"]


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("summary", "Buyer email: [redacted]", "raw customer-message fields"),
        ("summary", "Private margin is $123.45", "private economics"),
        ("source_ref", r"C:\\private\\customer-support.docx", "opaque, public, or sanitized"),
    ],
)
def test_manifest_privacy_validation_rejects_private_bodies_and_paths(field, value, error):
    unsafe = copy.deepcopy(manifest())
    unsafe["evidence"][0][field] = value
    with pytest.raises(OpsError, match=error):
        validate_manifest(unsafe)


def test_evidence_is_version_bound_and_content_is_immutable(ledger):
    connection, actor_id = ledger
    digest = make_effective(connection, actor_id, manifest())
    context = connection.execute(
        "SELECT * FROM business_context_version WHERE version_label = 'CTX-001'"
    ).fetchone()
    evidence = connection.execute(
        "SELECT * FROM business_context_evidence WHERE context_version_id = ?", (context["id"],)
    ).fetchall()
    assert evidence and all(row["tenant_id"] == context["tenant_id"] for row in evidence)
    assert context["content_hash"] == digest
    with pytest.raises(Exception, match="immutable"):
        connection.execute(
            "UPDATE business_context_version SET content_hash = 'changed' WHERE id = ?", (context["id"],)
        )


def test_v4_authority_migration_preserves_existing_grants_and_adds_context_scope(tmp_path):
    connection = connect(tmp_path / "legacy.db", create_parent=True)
    connection.executescript(
        """
        CREATE TABLE tenant (
            id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
            policy_profile TEXT NOT NULL, retainer_cents INTEGER NOT NULL DEFAULT 0,
            contractor_budget_cents INTEGER NOT NULL DEFAULT 0,
            tool_budget_cents INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL
        );
        CREATE TABLE actor (
            id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL REFERENCES tenant(id),
            name TEXT NOT NULL, role TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL, UNIQUE (tenant_id, name)
        );
        CREATE TABLE authority_grant (
            id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL REFERENCES tenant(id),
            actor_id TEXT NOT NULL REFERENCES actor(id),
            scope TEXT NOT NULL CHECK (scope IN ('assign', 'claim_use', 'spend', 'delivery', 'publication')),
            effective_at TEXT NOT NULL, expires_at TEXT, revoked_at TEXT, created_at TEXT NOT NULL
        );
        INSERT INTO tenant VALUES ('t1', 'legacy', 'Legacy', 'test', 0, 0, 0, '2026-01-01T00:00:00Z');
        INSERT INTO actor VALUES ('a1', 't1', 'Owner', 'owner', 1, '2026-01-01T00:00:00Z');
        INSERT INTO authority_grant VALUES (
            'g1', 't1', 'a1', 'publication', '2026-01-01T00:00:00Z', NULL, NULL, '2026-01-01T00:00:00Z'
        );
        """
    )
    migrate(connection, "2026-07-17T00:00:00Z")
    assert connection.execute("SELECT scope FROM authority_grant WHERE id = 'g1'").fetchone()[0] == "publication"
    grant_authority(connection, "legacy", "a1", "business_context", None, None)
    assert connection.execute(
        "SELECT COUNT(*) FROM authority_grant WHERE actor_id = 'a1' AND scope = 'business_context'"
    ).fetchone()[0] == 1
    connection.close()
