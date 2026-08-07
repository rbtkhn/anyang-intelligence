from __future__ import annotations

import json
import hashlib
import sqlite3
from pathlib import Path

import pytest
import yaml

from anyang_loop import council_workroom as cw
from anyang_loop.council_workroom import (
    ENVELOPE_GATED_CATEGORY,
    ENVELOPE_SHADOW_CATEGORY,
    backfill_friction_pilot,
    compare_council_envelope,
    council_decision_envelope,
    council_envelope_pilot_review,
    council_inbox,
    council_pilot_review,
    council_projection,
    council_subject_hash,
    create_council_transaction,
    load_envelope_packet,
    open_envelope_review_session,
    record_council_event,
    render_council_markdown,
    render_council_envelope_markdown,
    render_council_envelope_pilot_review_markdown,
    start_envelope_pilot,
    submit_envelope_review_session,
    verify_council_envelope,
    verify_council_transaction,
)
from anyang_loop.ops_cli import main
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_service import OpsError, add_actor, init_tenant, now_utc, tenant_id


NOW = "2026-07-28T12:00:00Z"
ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "docs" / "executive-council-friction-pilot-cohort-2026-07-24.md"
TRACKER = ROOT / "docs" / "executive-council-pilot-tracker.md"


@pytest.fixture()
def ledger(tmp_path):
    connection = connect(tmp_path / "council.db", create_parent=True)
    migrate(connection, NOW)
    init_tenant(
        connection,
        slug="synthetic",
        name="Synthetic Council",
        policy_profile="test-only",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    actors = {
        role: add_actor(connection, "synthetic", name, role).id
        for role, name in (
            ("engineer", "System Engineer"),
            ("executive", "Chief Executive"),
            ("interface", "Executive Assistant"),
        )
    }
    try:
        yield connection, actors
    finally:
        connection.close()


def _create(connection, identifier="TX-1", decision_class="Class 1"):
    return create_council_transaction(
        connection,
        "synthetic",
        {
            "id": identifier,
            "title": f"Synthetic {identifier}",
            "council_scope": "Synthetic internal decision",
            "decision_class": decision_class,
            "pilot_category": "test",
            "source_ref": "fictional://council/source",
            "created_at": NOW,
        },
    )


def _internal_ledger(tmp_path):
    path = tmp_path / "internal-council.db"
    connection = connect(path, create_parent=True)
    migrate(connection, NOW)
    init_tenant(
        connection,
        slug="anyang-internal",
        name="Anyang Internal",
        policy_profile="test-only",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    actors = {
        role: add_actor(connection, "anyang-internal", name, role).id
        for role, name in (
            ("engineer", "System Engineer"),
            ("executive", "Chief Executive"),
            ("interface", "Executive Assistant"),
            ("steward", "Council Steward"),
        )
    }
    return path, connection, actors


def _recommend(connection, actor_id, identifier="TX-1", key="recommendation"):
    return record_council_event(
        connection,
        identifier,
        "recommendation_recorded",
        {
            "event_key": key,
            "actor_id": actor_id,
            "council_role": "executive",
            "action_summary": "Recommend bounded synthetic work",
            "payload": {
                "decision": "Choose the bounded option",
                "evidence": "fictional://evidence",
                "recommendation": "Proceed only inside the synthetic scope",
                "success_condition": "A synthetic receipt returns",
                "uncertainty": "Synthetic evidence may be incomplete",
            },
        },
    )


def _approve(
    connection,
    actor_id,
    identifier="TX-1",
    *,
    key="authority",
    expires_at=None,
    client_ref="",
):
    return record_council_event(
        connection,
        identifier,
        "authority_disposition_recorded",
        {
            "event_key": key,
            "actor_id": actor_id,
            "council_role": "engineer",
            "action_summary": "Approve the exact synthetic subject",
            "payload": {
                "decision": "approved",
                "approved_scope": "Bounded synthetic work",
                "limits_exclusions": "No external action",
                "required_evidence": "A synthetic receipt",
                "anyang_authority_ref": "fictional://authority/anyang",
                "client_authority_ref": client_ref,
                "subject_hash": council_subject_hash(connection, identifier),
                "expires_at": expires_at,
            },
        },
    )


def _complete(connection, actors, identifier="TX-1"):
    record_council_event(
        connection,
        identifier,
        "execution_recorded",
        {
            "event_key": "execution",
            "actor_id": actors["interface"],
            "council_role": "interface",
            "action_summary": "Execute bounded synthetic work",
            "payload": {
                "executor_invoked": True,
                "named_executor": "Executive Assistant",
                "execution_state": "executing",
                "action_taken": "Created the synthetic artifact",
            },
        },
    )
    record_council_event(
        connection,
        identifier,
        "evidence_returned",
        {
            "event_key": "evidence",
            "actor_id": actors["interface"],
            "council_role": "interface",
            "action_summary": "Return synthetic evidence",
            "evidence_ref": "fictional://receipt",
            "payload": {"evidence": "fictional://receipt"},
        },
    )
    record_council_event(
        connection,
        identifier,
        "reconciliation_recorded",
        {
            "event_key": "reconciliation",
            "actor_id": actors["executive"],
            "council_role": "executive",
            "action_summary": "Reconcile the synthetic outcome",
            "payload": {
                "reconciliation_state": "supported",
                "final_supported_state": "Synthetic receipt verified",
                "terminal_state": "complete",
            },
        },
    )


def test_schema_v6_to_current_migration_preserves_existing_data_and_is_idempotent(tmp_path):
    path = tmp_path / "migration.db"
    with connect(path, create_parent=True) as connection:
        migrate(connection, "2026-07-01T00:00:00Z")
        init_tenant(
            connection,
            slug="preserved",
            name="Preserved",
            policy_profile="v6",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp="2026-07-01T00:00:00Z",
        )
        connection.executescript(
            """
            DROP TRIGGER council_transaction_immutable_update;
            DROP TRIGGER council_transaction_immutable_delete;
            DROP TRIGGER council_event_append_only_update;
            DROP TRIGGER council_event_append_only_delete;
            DROP TABLE council_event;
            DROP TABLE council_transaction;
            DELETE FROM schema_migration WHERE version = 7;
            INSERT OR IGNORE INTO schema_migration(version, applied_at)
            VALUES (6, '2026-07-01T00:00:00Z');
            """
        )
        migrate(connection, NOW)
        migrate(connection, NOW)
        assert schema_version(connection) == SCHEMA_VERSION == 8
        assert connection.execute(
            "SELECT name FROM tenant WHERE slug = 'preserved'"
        ).fetchone()[0] == "Preserved"
        assert connection.execute(
            "SELECT COUNT(*) FROM schema_migration WHERE version = 8"
        ).fetchone()[0] == 1


def test_live_sequence_binds_authority_requires_executor_and_evidence(ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    first_subject = council_subject_hash(connection, "TX-1")
    _approve(connection, actors["engineer"])

    _recommend(connection, actors["executive"], key="recommendation-change")
    assert council_subject_hash(connection, "TX-1") != first_subject
    with pytest.raises(OpsError, match="current authority"):
        record_council_event(
            connection,
            "TX-1",
            "execution_recorded",
            {
                "actor_id": actors["interface"],
                "action_summary": "Attempt stale-authority execution",
                "payload": {
                    "executor_invoked": True,
                    "named_executor": "Executive Assistant",
                    "execution_state": "executing",
                    "action_taken": "Synthetic step",
                },
            },
        )

    _approve(connection, actors["engineer"], key="authority-2")
    with pytest.raises(OpsError, match="named_executor|named executor"):
        record_council_event(
            connection,
            "TX-1",
            "execution_recorded",
            {
                "actor_id": actors["interface"],
                "action_summary": "Attempt anonymous execution",
                "payload": {
                    "executor_invoked": True,
                    "named_executor": "",
                    "execution_state": "executing",
                    "action_taken": "Synthetic step",
                },
            },
        )
    record_council_event(
        connection,
        "TX-1",
        "execution_recorded",
        {
            "event_key": "execution",
            "actor_id": actors["interface"],
            "action_summary": "Execute the bounded synthetic step",
            "evidence_ref": "fictional://execution",
            "payload": {
                "executor_invoked": True,
                "named_executor": "Executive Assistant",
                "execution_state": "executing",
                "action_taken": "Produced a synthetic artifact",
            },
        },
    )
    with pytest.raises(OpsError, match="returned evidence"):
        record_council_event(
            connection,
            "TX-1",
            "reconciliation_recorded",
            {
                "actor_id": actors["executive"],
                "action_summary": "Attempt premature close",
                "payload": {
                    "reconciliation_state": "supported",
                    "final_supported_state": "Complete",
                    "terminal_state": "complete",
                },
            },
        )
    record_council_event(
        connection,
        "TX-1",
        "evidence_returned",
        {
            "event_key": "evidence",
            "actor_id": actors["interface"],
            "action_summary": "Return execution evidence",
            "evidence_ref": "fictional://receipt",
            "payload": {"evidence": "fictional://receipt"},
        },
    )
    record_council_event(
        connection,
        "TX-1",
        "reconciliation_recorded",
        {
            "event_key": "reconciliation",
            "actor_id": actors["executive"],
            "action_summary": "Reconcile the supported outcome",
            "payload": {
                "reconciliation_state": "supported",
                "final_supported_state": "Synthetic receipt verified",
                "terminal_state": "complete",
            },
        },
    )
    projection = council_projection(connection, "TX-1")
    assert projection["current_state"] == "complete"
    assert {key for key in projection["sections"]} == {"A", "B", "C", "D"}
    assert projection["lineage"]["chain_verified"] is True
    assert "# Synthetic TX-1" in render_council_markdown(projection)


def test_engineer_authority_event_remains_compatible_without_council_membership(ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    _approve(connection, actors["engineer"])

    row = connection.execute(
        "SELECT council_role FROM council_event WHERE transaction_id = ? AND event_type = ?",
        ("TX-1", "authority_disposition_recorded"),
    ).fetchone()
    envelope = yaml.safe_load((ROOT / "authority-envelope.yaml").read_text(encoding="utf-8"))

    assert row["council_role"] == "engineer"
    assert "engineer" in cw.AUTHORIZED_ACTOR_ROLES
    assert "engineer" not in envelope["governance"]["council_roles"]
    assert envelope["roles"]["engineer"]["classification"] == "authority-principal"


def test_class3_dual_authority_expiry_privacy_and_live_attribution(ledger):
    connection, actors = ledger
    _create(connection, "TX-3", "Class 3")
    _recommend(connection, actors["executive"], "TX-3")
    with pytest.raises(OpsError, match="client authority"):
        _approve(connection, actors["engineer"], "TX-3")
    _approve(
        connection,
        actors["engineer"],
        "TX-3",
        client_ref="fictional://authority/client",
        expires_at="2026-07-27T00:00:00Z",
    )
    projection = council_projection(connection, "TX-3", as_of=now_utc())
    assert "authority-expired" in {
        flag["code"] for flag in projection["attention_flags"]
    }
    expired_envelope = council_decision_envelope(connection, "TX-3", as_of=now_utc())
    assert expired_envelope["freshness"]["status"] == "expired"
    assert verify_council_envelope(expired_envelope)["disposition"] == "Hold"
    with pytest.raises(OpsError, match="historical-missing"):
        record_council_event(
            connection,
            "TX-3",
            "blocked",
            {
                "attribution_status": "historical-missing",
                "actor_label": "Missing",
                "action_summary": "Invalid live missing attribution",
                "payload": {"reason": "Synthetic"},
            },
        )

    init_tenant(
        connection,
        slug="anyang-internal",
        name="Internal",
        policy_profile="pilot",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    internal_actor = add_actor(
        connection, "anyang-internal", "Chief Executive", "executive"
    ).id
    create_council_transaction(
        connection,
        "anyang-internal",
        {
            "id": "PRIVATE-1",
            "title": "Privacy boundary",
            "council_scope": "Internal only",
            "decision_class": "Class 0",
        },
    )
    with pytest.raises(OpsError, match="private evidence bodies"):
        record_council_event(
            connection,
            "PRIVATE-1",
            "recommendation_recorded",
            {
                "actor_id": internal_actor,
                "action_summary": "Attempt private body storage",
                "payload": {
                    "decision": "Hold",
                    "evidence": "linked elsewhere",
                    "recommendation": "Do not store the body",
                    "success_condition": "Privacy preserved",
                    "evidence_body": "synthetic forbidden body",
                },
            },
        )


def test_event_stream_is_append_only_and_verification_detects_tampering(ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    event_id = connection.execute(
        "SELECT id FROM council_event WHERE transaction_id = 'TX-1'"
    ).fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        connection.execute(
            "UPDATE council_event SET action_summary = 'tampered' WHERE id = ?",
            (event_id,),
        )
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        connection.execute("DELETE FROM council_event WHERE id = ?", (event_id,))

    connection.execute("DROP TRIGGER council_event_append_only_update")
    connection.execute(
        "UPDATE council_event SET action_summary = 'tampered' WHERE id = ?",
        (event_id,),
    )
    verification = verify_council_transaction(connection, "TX-1")
    assert verification["ok"] is False
    assert "event-hash-mismatch" in {
        issue["code"] for issue in verification["issues"]
    }


def test_full_friction_backfill_is_deterministic_idempotent_and_preserves_missing(tmp_path):
    with connect(tmp_path / "backfill.db", create_parent=True) as connection:
        migrate(connection, NOW)
        first = backfill_friction_pilot(
            connection, "anyang-internal", COHORT, TRACKER
        )
        ids_before = [
            row[0]
            for row in connection.execute(
                "SELECT id FROM council_event ORDER BY transaction_id, sequence"
            )
        ]
        second = backfill_friction_pilot(
            connection, "anyang-internal", COHORT, TRACKER
        )
        ids_after = [
            row[0]
            for row in connection.execute(
                "SELECT id FROM council_event ORDER BY transaction_id, sequence"
            )
        ]
        assert first.details == second.details
        assert ids_before == ids_after
        assert connection.execute(
            "SELECT COUNT(*) FROM council_transaction"
        ).fetchone()[0] == 5
        assert {
            identifier: council_projection(connection, identifier)["current_state"]
            for identifier in (
                "EC-FRICTION-01",
                "EC-FRICTION-02",
                "EC-FRICTION-03",
                "EC-FRICTION-04",
                "EC-FRICTION-05",
            )
        } == {
            "EC-FRICTION-01": "complete",
            "EC-FRICTION-02": "approved",
            "EC-FRICTION-03": "complete",
            "EC-FRICTION-04": "executing",
            "EC-FRICTION-05": "held",
        }
        case_one = council_projection(connection, "EC-FRICTION-01")
        assert all(event["occurred_at"] == "Missing" for event in case_one["events"])
        assert any(
            event["payload"].get("observed_value", "").startswith("Missing")
            for event in case_one["metrics"]
        )
        assert "source_markdown" in case_one["sections"]["A"][0]["payload"]
        assert all(
            verify_council_transaction(connection, identifier)["ok"]
            for identifier in (
                "EC-FRICTION-01",
                "EC-FRICTION-02",
                "EC-FRICTION-03",
                "EC-FRICTION-04",
                "EC-FRICTION-05",
            )
        )
        for identifier in (
            "EC-FRICTION-01",
            "EC-FRICTION-02",
            "EC-FRICTION-03",
            "EC-FRICTION-04",
            "EC-FRICTION-05",
        ):
            envelope = council_decision_envelope(
                connection, identifier, as_of="2026-08-21T23:59:59Z"
            )
            assert envelope == council_decision_envelope(
                connection, identifier, as_of="2026-08-21T23:59:59Z"
            )
            issue_codes = {
                issue["code"] for issue in verify_council_envelope(envelope)["issues"]
            }
            assert not issue_codes.intersection(
                {
                    "projection-hash-mismatch",
                    "payload-digest-mismatch",
                    "receipt-digest-mismatch",
                    "event-hash-mismatch",
                }
            )
        review = council_pilot_review(
            connection, "anyang-internal", "2026-08-21T23:59:59Z"
        )
        assert review["receipt_coverage"]["percent"] == 0.0
        assert review["unauthorized_progression"]["count"] == 0
        assert review["operator_burden_measurements"]


def test_conflicting_rerun_fails_and_inbox_prioritizes_authority_conflict(tmp_path):
    cohort_copy = tmp_path / "cohort.md"
    cohort_copy.write_text(COHORT.read_text(encoding="utf-8"), encoding="utf-8")
    tracker_copy = tmp_path / "tracker.md"
    tracker_copy.write_text(
        TRACKER.read_text(encoding="utf-8").replace(
            "executive-council-friction-pilot-cohort-2026-07-24.md",
            "cohort.md",
        ),
        encoding="utf-8",
    )
    with connect(tmp_path / "conflict.db", create_parent=True) as connection:
        migrate(connection, NOW)
        backfill_friction_pilot(
            connection, "anyang-internal", cohort_copy, tracker_copy
        )
        changed = cohort_copy.read_text(encoding="utf-8").replace(
            "System improvement retrospective",
            "Changed retrospective",
            1,
        )
        cohort_copy.write_text(changed, encoding="utf-8")
        with pytest.raises(OpsError, match="conflicts with existing"):
            backfill_friction_pilot(
                connection, "anyang-internal", cohort_copy, tracker_copy
            )

        tid = tenant_id(connection, "anyang-internal")
        connection.execute(
            """INSERT INTO authority_conflict(
                id, tenant_id, target, instructions_json, resolution_owner,
                status, resolution, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "conflict-1",
                tid,
                "EC-FRICTION-04",
                "[]",
                "engineer",
                "open",
                "",
                NOW,
            ),
        )
        inbox = council_inbox(connection, "anyang-internal", now_utc())
        assert inbox["entries"][0]["transaction_id"] == "EC-FRICTION-04"
        assert inbox["entries"][0]["priority"] == "P0"


def test_council_cli_dry_run_and_projection_json(tmp_path, capsys):
    db = tmp_path / "cli.db"
    with connect(db, create_parent=True) as connection:
        migrate(connection, NOW)
        init_tenant(
            connection,
            slug="synthetic",
            name="Synthetic",
            policy_profile="test",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp=NOW,
        )
    packet = tmp_path / "transaction.yaml"
    packet.write_text(
        yaml.safe_dump(
            {
                "id": "CLI-1",
                "title": "CLI transaction",
                "council_scope": "Synthetic CLI test",
                "decision_class": "Class 0",
            }
        ),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "create",
                "--tenant",
                "synthetic",
                "--packet",
                str(packet),
                "--dry-run",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["dry_run"] is True
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "create",
                "--tenant",
                "synthetic",
                "--packet",
                str(packet),
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "show",
                "CLI-1",
                "--format",
                "json",
            ]
        )
        == 0
    )
    projection = json.loads(capsys.readouterr().out)
    assert projection["transaction"]["id"] == "CLI-1"
    assert set(
        (
            "transaction",
            "current_state",
            "sections",
            "events",
            "authority_bindings",
            "evidence",
            "metrics",
            "attention_flags",
            "lineage",
        )
    ).issubset(projection)


def test_decision_envelope_is_deterministic_verifiable_and_ledger_bound(ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    _approve(connection, actors["engineer"])
    _complete(connection, actors)

    as_of = now_utc()
    first = council_decision_envelope(connection, "TX-1", as_of=as_of)
    second = council_decision_envelope(connection, "TX-1", as_of=as_of)
    assert first == second
    assert first["contract_version"] == "council-decision-envelope/v1.1"
    assert first["authority_effect"] == "none"
    assert first["critical_field_coverage"]["complete"] is True
    assert verify_council_envelope(first)["ok"] is True
    assert compare_council_envelope(connection, first)["ok"] is True

    rendered = render_council_envelope_markdown(first)
    assert "What changed:" in rendered
    assert "Authority effect: `none`" in rendered
    assert verify_council_envelope(first, receipt=rendered.replace("\n", "\r\n"))["ok"] is True

    tampered = json.loads(json.dumps(first))
    tampered["payload"]["transaction"]["title"] = "Tampered"
    result = verify_council_envelope(tampered)
    assert result["ok"] is False
    assert result["disposition"] == "Hold"
    assert "projection-hash-mismatch" in {issue["code"] for issue in result["issues"]}

    malformed = json.loads(json.dumps(first))
    malformed["payload"]["transaction"] = []
    malformed_result = verify_council_envelope(malformed)
    assert malformed_result["ok"] is False
    assert "invalid-projection" in {issue["code"] for issue in malformed_result["issues"]}


def test_decision_envelope_holds_stale_authority_and_rejects_unknown_contract(ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    _approve(connection, actors["engineer"])
    _recommend(connection, actors["executive"], key="changed-recommendation")

    stale = council_decision_envelope(connection, "TX-1", as_of=now_utc())
    assert stale["freshness"]["status"] == "stale"
    assert verify_council_envelope(stale)["disposition"] == "Hold"

    stale["contract_version"] = "council-decision-envelope/v99"
    result = verify_council_envelope(stale)
    assert "unknown-contract-version" in {issue["code"] for issue in result["issues"]}


def test_envelope_pilot_categories_are_internal_and_class_bounded(tmp_path):
    path, connection, _ = _internal_ledger(tmp_path)
    try:
        for decision_class in ("Class 0", "Class 3"):
            with pytest.raises(OpsError, match="only Class 1 or Class 2"):
                create_council_transaction(
                    connection,
                    "anyang-internal",
                    {
                        "id": f"BAD-{decision_class[-1]}",
                        "title": "Invalid envelope pilot transaction",
                        "council_scope": "Internal",
                        "decision_class": decision_class,
                        "pilot_category": ENVELOPE_SHADOW_CATEGORY,
                    },
                )
        init_tenant(
            connection,
            slug="external",
            name="External",
            policy_profile="test",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp=NOW,
        )
        with pytest.raises(OpsError, match="internal-only"):
            create_council_transaction(
                connection,
                "external",
                {
                    "id": "BAD-EXTERNAL",
                    "title": "External envelope pilot transaction",
                    "council_scope": "External",
                    "decision_class": "Class 1",
                    "pilot_category": ENVELOPE_SHADOW_CATEGORY,
                },
            )
    finally:
        connection.close()
    assert path.exists()


def test_gated_operation_is_fail_closed_and_reserved_metrics_are_protected(tmp_path):
    _, connection, actors = _internal_ledger(tmp_path)
    try:
        with pytest.raises(OpsError, match="Gated envelope operation is held"):
            create_council_transaction(
                connection,
                "anyang-internal",
                {
                    "id": "GATED-HELD",
                    "title": "Held gated transaction",
                    "council_scope": "Internal envelope pilot",
                    "decision_class": "Class 1",
                    "pilot_category": ENVELOPE_GATED_CATEGORY,
                },
            )
        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": "CONTROL",
                "title": "Authorize shadow calibration",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 1",
                "created_at": NOW,
            },
        )
        _recommend(connection, actors["executive"], "CONTROL")
        _approve(connection, actors["engineer"], "CONTROL")
        with pytest.raises(OpsError, match="dedicated Council interface"):
            record_council_event(
                connection,
                "CONTROL",
                "metric_recorded",
                {
                    "actor_id": actors["steward"],
                    "council_role": "steward",
                    "action_summary": "Attempt a self-reported metric",
                    "payload": {
                        "name": "baseline_reconstruction_minutes",
                        "observed_value": 10,
                        "observation_status": "observed",
                    },
                },
            )
    finally:
        connection.close()


def test_protected_pilot_sessions_derive_measurement_and_never_open_gate(tmp_path):
    _, connection, actors = _internal_ledger(tmp_path)
    try:
        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": "CONTROL",
                "title": "Authorize shadow calibration",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 1",
                "created_at": NOW,
            },
        )
        _recommend(connection, actors["executive"], "CONTROL")
        _approve(connection, actors["engineer"], "CONTROL")
        activation = start_envelope_pilot(
            connection, "anyang-internal", "CONTROL", actors["engineer"]
        )
        pilot_id = activation.details["pilot_id"]
        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": "SHADOW-1",
                "title": "Measured shadow transaction",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 1",
                "pilot_category": ENVELOPE_SHADOW_CATEGORY,
                "source_ref": pilot_id,
            },
        )
        _recommend(connection, actors["executive"], "SHADOW-1")
        _approve(connection, actors["engineer"], "SHADOW-1")
        _complete(connection, actors, "SHADOW-1")

        projection = council_projection(connection, "SHADOW-1")
        material = [event for event in projection["events"] if event["event_type"] != "metric_recorded"]
        recommendation = projection["sections"]["A"][-1]
        authority = projection["sections"]["B"][-1]
        answers = {
            "what_changed_event_id": material[-1]["id"],
            "judgment_event_id": recommendation["id"],
            "authority_status_and_exclusion": "current|" + authority["payload"]["limits_exclusions"],
            "missing_evidence_codes": [],
            "next_action_code": "none",
        }
        even = int(hashlib.sha256(b"SHADOW-1").hexdigest()[:8], 16) % 2 == 0
        baseline_role = "steward" if even else "interface"
        reviewers = {
            "baseline": actors[baseline_role],
            "receipt": actors["interface" if baseline_role == "steward" else "steward"],
        }
        for surface in ("baseline", "receipt"):
            opened = open_envelope_review_session(
                connection, "SHADOW-1", pilot_id, surface, reviewers[surface]
            )
            submit_envelope_review_session(
                connection,
                opened.details["session_id"],
                {"actor_id": reviewers[surface], "answers": answers},
            )
        review = council_envelope_pilot_review(
            connection,
            "anyang-internal",
            from_time=None,
            as_of=now_utc(),
            pilot_id=pilot_id,
        )
        assert review["live_transaction_count"] == 1
        assert review["samples"][0]["protected_pair"] is not None, json.dumps(
            council_projection(connection, "SHADOW-1")["metrics"], indent=2
        )
        assert review["correct_paired_sample_count"] == 1, review
        assert review["shadow_gate"]["ready"] is False
        assert review["shadow_gate"]["calibration_hold"] is True
        assert review["disposition"] == "Extend shadow measurement"
    finally:
        connection.close()


def test_live_time_role_and_as_of_boundaries_are_fail_closed(ledger):
    connection, actors = ledger
    _create(connection)
    with pytest.raises(OpsError, match="stored role"):
        record_council_event(
            connection,
            "TX-1",
            "recommendation_recorded",
            {
                "actor_id": actors["executive"],
                "council_role": "engineer",
                "action_summary": "Spoof a role",
                "payload": {
                    "decision": "Choose",
                    "evidence": "fictional://evidence",
                    "recommendation": "Proceed",
                    "success_condition": "Receipt",
                },
            },
        )
    with pytest.raises(OpsError, match="server-owned"):
        record_council_event(
            connection,
            "TX-1",
            "recommendation_recorded",
            {
                "actor_id": actors["executive"],
                "council_role": "executive",
                "action_summary": "Supply a recording time",
                "recorded_at": NOW,
                "payload": {
                    "decision": "Choose",
                    "evidence": "fictional://evidence",
                    "recommendation": "Proceed",
                    "success_condition": "Receipt",
                },
            },
        )
    _recommend(connection, actors["executive"])
    assert council_projection(connection, "TX-1", as_of=NOW)["events"] == []


def test_envelope_parser_limits_sanitization_and_legacy_v1_compatibility(tmp_path, ledger):
    connection, actors = ledger
    _create(connection)
    _recommend(connection, actors["executive"])
    _approve(connection, actors["engineer"])
    _complete(connection, actors)
    as_of = now_utc()
    envelope = council_decision_envelope(connection, "TX-1", as_of=as_of)
    assert "source_markdown" not in json.dumps(envelope["payload"])
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"a":1,"a":2}', encoding="utf-8")
    with pytest.raises(OpsError, match="Duplicate JSON key"):
        load_envelope_packet(duplicate)
    nonfinite = tmp_path / "nonfinite.json"
    nonfinite.write_text('{"value":NaN}', encoding="utf-8")
    with pytest.raises(OpsError, match="Non-finite"):
        load_envelope_packet(nonfinite)

    projection = council_projection(connection, "TX-1", as_of=as_of)
    legacy = dict(envelope)
    legacy["contract_version"] = "council-decision-envelope/v1"
    legacy["payload"] = projection
    legacy["projection_hash"] = cw._hash(projection)
    legacy["payload_digest"] = cw._sha256_bytes(cw._canonical_json_bytes(projection))
    legacy["receipt_data"] = cw._human_receipt_data(projection)
    legacy["critical_field_coverage"] = cw._critical_field_coverage(legacy["receipt_data"])
    legacy["human_receipt"] = cw._render_human_receipt_body(legacy, legacy["receipt_data"])
    legacy["human_receipt_digest"] = cw._sha256_bytes(legacy["human_receipt"].encode("utf-8"))
    assert verify_council_envelope(legacy)["ok"] is True
    assert compare_council_envelope(connection, legacy)["ok"] is True
    record_council_event(
        connection,
        "TX-1",
        "corrected",
        {
            "actor_id": actors["engineer"],
            "council_role": "engineer",
            "action_summary": "# Injected\n| table |",
            "payload": {"reason": "Exercise Markdown escaping"},
        },
    )
    escaped = render_council_envelope_markdown(
        council_decision_envelope(connection, "TX-1", as_of=now_utc())
    )
    assert "\\# Injected \\| table \\|" in escaped


def test_envelope_cli_verify_is_offline_and_read_only(tmp_path, capsys):
    db, connection, actors = _internal_ledger(tmp_path)
    create_council_transaction(
        connection,
        "anyang-internal",
        {
            "id": "CLI-ENVELOPE",
            "title": "CLI envelope",
            "council_scope": "Internal",
            "decision_class": "Class 1",
            "created_at": NOW,
        },
    )
    _recommend(connection, actors["executive"], "CLI-ENVELOPE")
    _approve(connection, actors["engineer"], "CLI-ENVELOPE")
    _complete(connection, actors, "CLI-ENVELOPE")
    as_of = now_utc()
    envelope = council_decision_envelope(connection, "CLI-ENVELOPE", as_of=as_of)
    connection.close()
    packet = tmp_path / "envelope.json"
    packet.write_text(json.dumps(envelope, ensure_ascii=False), encoding="utf-8")
    before = db.read_bytes()
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "envelope",
                "CLI-ENVELOPE",
                "--as-of",
                    as_of,
                "--format",
                "json",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["projection_hash"] == envelope["projection_hash"]
    blocked_output = tmp_path / "blocked-in-repository.json"
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "envelope",
                "CLI-ENVELOPE",
                "--as-of",
                as_of,
                "--format",
                "json",
                "--output",
                str(blocked_output),
            ]
        )
        == 1
    )
    assert not blocked_output.exists()
    capsys.readouterr()
    assert main(["council", "envelope-verify", "--packet", str(packet)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["ok"] is True
    assert result["compared_to_ledger"] is False
    assert (
        main(
            [
                "--db",
                str(db),
                "council",
                "envelope-compare",
                "--packet",
                str(packet),
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["compared_to_ledger"] is True
    assert db.read_bytes() == before

    altered = json.loads(packet.read_text(encoding="utf-8"))
    altered["human_receipt"] = altered["human_receipt"].replace(
        "Authority effect: `none`", "Authority effect: `execute`"
    )
    packet.write_text(json.dumps(altered, ensure_ascii=False), encoding="utf-8")
    assert main(["council", "envelope-verify", "--packet", str(packet)]) == 1
    failed = json.loads(capsys.readouterr().out)
    assert failed["disposition"] == "Hold"
    assert "receipt-digest-mismatch" in {issue["code"] for issue in failed["issues"]}
    assert db.read_bytes() == before
