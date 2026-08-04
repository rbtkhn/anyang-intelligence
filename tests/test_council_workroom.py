from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest
import yaml

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
    record_council_event,
    render_council_markdown,
    render_council_envelope_markdown,
    render_council_envelope_pilot_review_markdown,
    verify_council_envelope,
    verify_council_transaction,
)
from anyang_loop.ops_cli import main
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_service import OpsError, add_actor, init_tenant, tenant_id


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
    projection = council_projection(connection, "TX-3", as_of=NOW)
    assert "authority-expired" in {
        flag["code"] for flag in projection["attention_flags"]
    }
    expired_envelope = council_decision_envelope(connection, "TX-3", as_of=NOW)
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
        assert review["receipt_coverage"]["percent"] == 100.0
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
        inbox = council_inbox(connection, "anyang-internal", NOW)
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

    first = council_decision_envelope(connection, "TX-1", as_of=NOW)
    second = council_decision_envelope(connection, "TX-1", as_of=NOW)
    assert first == second
    assert first["contract_version"] == "council-decision-envelope/v1"
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

    stale = council_decision_envelope(connection, "TX-1", as_of=NOW)
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


def test_gated_execution_requires_exact_current_envelope_binding(tmp_path):
    _, connection, actors = _internal_ledger(tmp_path)
    try:
        with pytest.raises(OpsError, match="preceding shadow cohort"):
            create_council_transaction(
                connection,
                "anyang-internal",
                {
                    "id": "GATED-EARLY",
                    "title": "Premature gated transaction",
                    "council_scope": "Internal envelope pilot",
                    "decision_class": "Class 1",
                    "pilot_category": ENVELOPE_GATED_CATEGORY,
                    "created_at": NOW,
                },
            )
        _prepare_shadow_gate(connection, actors)
        with pytest.raises(OpsError, match="day-10-eligibility"):
            create_council_transaction(
                connection,
                "anyang-internal",
                {
                    "id": "GATED-BEFORE-DAY-11",
                    "title": "Too-early gated transaction",
                    "council_scope": "Internal envelope pilot",
                    "decision_class": "Class 1",
                    "pilot_category": ENVELOPE_GATED_CATEGORY,
                    "created_at": "2026-07-10T00:00:00Z",
                },
            )
        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": "GATED-1",
                "title": "Gated transaction",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 1",
                "pilot_category": ENVELOPE_GATED_CATEGORY,
                "created_at": NOW,
            },
        )
        _recommend(connection, actors["executive"], "GATED-1")
        _approve(connection, actors["engineer"], "GATED-1")
        envelope = council_decision_envelope(connection, "GATED-1", as_of=NOW)
        base_packet = {
            "event_key": "execution",
            "actor_id": actors["interface"],
            "action_summary": "Execute bounded gated work",
            "payload": {
                "executor_invoked": True,
                "named_executor": "Executive Assistant",
                "execution_state": "executing",
                "action_taken": "Created the internal artifact",
            },
        }
        with pytest.raises(OpsError, match="envelope binding"):
            record_council_event(connection, "GATED-1", "execution_recorded", base_packet)
        packet = json.loads(json.dumps(base_packet))
        packet["payload"].update(
            {
                "envelope_projection_hash": envelope["projection_hash"],
                "human_receipt_digest": envelope["human_receipt_digest"],
                "envelope_as_of": NOW,
            }
        )
        record_council_event(connection, "GATED-1", "execution_recorded", packet)
        assert council_projection(connection, "GATED-1")["current_state"] == "executing"

        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": "GATED-2",
                "title": "Stale gated transaction",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 2",
                "pilot_category": ENVELOPE_GATED_CATEGORY,
                "created_at": NOW,
            },
        )
        _recommend(connection, actors["executive"], "GATED-2")
        _approve(connection, actors["engineer"], "GATED-2")
        stale = council_decision_envelope(connection, "GATED-2", as_of=NOW)
        _record_envelope_metric(
            connection, actors["steward"], "GATED-2", "envelope_generation_seconds", 1
        )
        stale_packet = json.loads(json.dumps(base_packet))
        stale_packet["event_key"] = "stale-execution"
        stale_packet["payload"].update(
            {
                "envelope_projection_hash": stale["projection_hash"],
                "human_receipt_digest": stale["human_receipt_digest"],
                "envelope_as_of": NOW,
            }
        )
        with pytest.raises(OpsError, match="projection hash is stale or mismatched"):
            record_council_event(
                connection, "GATED-2", "execution_recorded", stale_packet
            )
    finally:
        connection.close()


def _record_envelope_metric(connection, actor_id, transaction_id, name, value):
    record_council_event(
        connection,
        transaction_id,
        "metric_recorded",
        {
            "event_key": f"metric-{name}",
            "actor_id": actor_id,
            "council_role": "steward",
            "action_summary": f"Record {name}",
            "payload": {
                "name": name,
                "observed_value": value,
                "observation_status": "observed",
            },
        },
    )


def _prepare_shadow_gate(connection, actors):
    for index in range(5):
        transaction_id = f"GATE-SHADOW-{index}"
        create_council_transaction(
            connection,
            "anyang-internal",
            {
                "id": transaction_id,
                "title": f"Shadow gate case {index}",
                "council_scope": "Internal envelope pilot",
                "decision_class": "Class 1",
                "pilot_category": ENVELOPE_SHADOW_CATEGORY,
                "created_at": f"2026-07-{index + 1:02d}T00:00:00Z",
            },
        )
        for name, value in (
            ("incremental_review_minutes", 1),
            ("critical_field_parity", True),
            ("receipt_ledger_mismatch", 0),
            ("authority_or_membrane_incident", 0),
        ):
            _record_envelope_metric(
                connection, actors["steward"], transaction_id, name, value
            )


def test_envelope_pilot_review_adopts_only_observed_adequate_sample(tmp_path):
    _, connection, actors = _internal_ledger(tmp_path)
    start = "2026-07-01T00:00:00Z"
    end = "2026-07-30T00:00:00Z"
    try:
        empty = council_envelope_pilot_review(
            connection, "anyang-internal", from_time=start, as_of=end
        )
        assert empty["disposition"] == "Extend shadow measurement"
        assert empty["shadow_gate"]["ready"] is False
        assert empty["guardrails"]["pass"] is False
        for index in range(10):
            transaction_id = f"PILOT-{index:02d}"
            category = ENVELOPE_SHADOW_CATEGORY
            create_council_transaction(
                connection,
                "anyang-internal",
                {
                    "id": transaction_id,
                    "title": f"Pilot transaction {index}",
                    "council_scope": "Internal envelope pilot",
                    "decision_class": "Class 1",
                    "pilot_category": category,
                    "created_at": f"2026-07-{index + 2:02d}T00:00:00Z",
                },
            )
            _recommend(connection, actors["executive"], transaction_id)
            _approve(connection, actors["engineer"], transaction_id)
            record_council_event(
                connection,
                transaction_id,
                "execution_recorded",
                {
                    "event_key": "execution",
                    "actor_id": actors["interface"],
                    "action_summary": "Execute internal pilot work",
                    "payload": {
                        "executor_invoked": True,
                        "named_executor": "Executive Assistant",
                        "execution_state": "executing",
                        "action_taken": "Created an internal result",
                    },
                },
            )
            for name, value in (
                ("baseline_reconstruction_minutes", 10),
                ("envelope_reconstruction_minutes", 6),
                ("baseline_reconstruction_correctness", 5),
                ("envelope_reconstruction_correctness", 5),
                ("envelope_generation_seconds", 0.5),
                ("incremental_review_minutes", 1),
                ("critical_field_parity", True),
                ("receipt_ledger_mismatch", 0),
                ("correction_or_rework_minutes", 0),
                ("authority_or_membrane_incident", 0),
            ):
                _record_envelope_metric(
                    connection, actors["steward"], transaction_id, name, value
                )
        review = council_envelope_pilot_review(
            connection,
            "anyang-internal",
            from_time=start,
            as_of=end,
            attention_value_per_hour=100,
        )
        assert review["primary_kpi"]["observed"] == 40.0
        assert review["shadow_gate"]["ready"] is True
        assert review["guardrails"]["pass"] is True
        assert review["disposition"] == "Adopt bounded operation"
        assert review["supporting_outcomes"]["observed_hours_saved"] == 0.67
        assert review["supporting_outcomes"]["observed_attention_value"] == 67.0
        rendered = render_council_envelope_pilot_review_markdown(review)
        assert "Adopt bounded operation" in rendered
        assert "Historical replays excluded from ROI: True" in rendered
    finally:
        connection.close()


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
    envelope = council_decision_envelope(connection, "CLI-ENVELOPE", as_of=NOW)
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
                NOW,
                "--format",
                "json",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["projection_hash"] == envelope["projection_hash"]
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
