from __future__ import annotations

import json
import sqlite3

import pytest
import yaml

from anyang_loop.choice_learning import (
    choice_context,
    choice_projection,
    choice_review,
    record_choice_event,
    record_choice_selection,
    render_choice_review_markdown,
    verify_choice,
)
from anyang_loop.ops_cli import main
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_service import OpsError, add_actor, init_tenant


NOW = "2026-07-29T12:00:00Z"


@pytest.fixture()
def ledger(tmp_path):
    connection = connect(tmp_path / "choices.db", create_parent=True)
    migrate(connection, NOW)
    init_tenant(
        connection,
        slug="anyang-internal",
        name="Anyang Internal",
        policy_profile="choice-learning-v1",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    actor = add_actor(
        connection, "anyang-internal", "Council Steward", "steward"
    ).id
    try:
        yield connection, actor
    finally:
        connection.close()


def selection(identifier: str, actor: str, selected: str = "small-proof") -> dict:
    return {
        "id": identifier,
        "workspace_id": "anyang-intelligence",
        "lane": "repository",
        "choice_kind": "next-action",
        "consequence_level": "ordinary",
        "decision_summary": "Choose the next bounded proof",
        "options": [
            {
                "key": "small-proof",
                "role": "recommended",
                "label": "Test the smallest proof",
                "tradeoff": "Fast evidence with narrow scope",
                "expected_outcome": "One verified receipt",
                "risk": "May miss broader effects",
                "learning_refs": ["RL-SYNTHETIC-1"],
            },
            {
                "key": "deep-audit",
                "role": "alternative",
                "label": "Run a deeper audit",
                "tradeoff": "More confidence with more time",
                "expected_outcome": "Broader evidence",
                "risk": "Higher operator burden",
                "learning_refs": [],
            },
            {
                "key": "counterexample",
                "role": "overlooked",
                "label": "Search for a counterexample",
                "tradeoff": "Tests the framing itself",
                "expected_outcome": "A stronger or rejected premise",
                "risk": "May not advance delivery",
                "learning_refs": [],
            },
            {
                "key": "pause",
                "role": "pause-or-deepen",
                "label": "Pause and preserve optionality",
                "tradeoff": "No immediate progress",
                "expected_outcome": "Decision remains reversible",
                "risk": "Momentum may stall",
                "learning_refs": [],
            },
        ],
        "recommendation_key": "small-proof",
        "selected_option_key": selected,
        "learning_refs": ["RL-SYNTHETIC-1"],
        "learning_context": {"basis": "current synthetic evidence"},
        "success_signal": "The receipt answers the decision",
        "risk_signal": "The proof expands beyond its boundary",
        "selected_by": "Council Steward",
        "actor_id": actor,
        "presented_at": NOW,
        "selected_at": NOW,
        "review_after": "2026-07-30T12:00:00Z",
        "recorded_at": NOW,
        "source_ref": "fictional://thread/choice",
    }


def outcome(
    key: str,
    result: str = "successful",
    *,
    authority_issue: bool = False,
) -> dict:
    return {
        "event_key": key,
        "event_type": "outcome_recorded",
        "recorded_by": "Council Steward",
        "action_summary": "Record the observed synthetic result",
        "evidence_ref": f"fictional://outcome/{key}",
        "occurred_at": "2026-07-30T12:00:00Z",
        "recorded_at": "2026-07-30T12:00:00Z",
        "payload": {
            "result": result,
            "cognitive_load": "lower",
            "momentum": "advanced",
            "discovery_value": "new-useful-path",
            "observation": "Synthetic evidence supported the result",
            "rework_minutes": 2,
            "authority_issue": authority_issue,
            "membrane_issue": False,
        },
    }


def test_schema_v7_to_v8_migration_is_idempotent_and_preserves_data(tmp_path):
    path = tmp_path / "migration.db"
    with connect(path, create_parent=True) as connection:
        migrate(connection, NOW)
        init_tenant(
            connection,
            slug="preserved",
            name="Preserved",
            policy_profile="v7",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp=NOW,
        )
        connection.executescript(
            """
            DROP TRIGGER choice_prompt_immutable_update;
            DROP TRIGGER choice_prompt_immutable_delete;
            DROP TRIGGER choice_event_append_only_update;
            DROP TRIGGER choice_event_append_only_delete;
            DROP TABLE choice_event;
            DROP TABLE choice_prompt;
            DELETE FROM schema_migration WHERE version = 8;
            INSERT OR IGNORE INTO schema_migration(version, applied_at)
            VALUES (7, '2026-07-28T00:00:00Z');
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


def test_selection_is_atomic_immutable_idempotent_and_exact(ledger):
    connection, actor = ledger
    assert connection.execute("SELECT COUNT(*) FROM choice_prompt").fetchone()[0] == 0
    packet = selection("CHOICE-1", actor)
    first = record_choice_selection(connection, "anyang-internal", packet)
    second = record_choice_selection(connection, "anyang-internal", packet)
    assert first.details["idempotent"] is False
    assert second.details["idempotent"] is True
    projection = choice_projection(connection, "CHOICE-1")
    assert projection["options"] == packet["options"]
    assert projection["selection"]["payload"]["selected_option_key"] == "small-proof"
    assert projection["lineage"]["authority_effect"] == "none"
    assert verify_choice(connection, "CHOICE-1")["ok"] is True
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        connection.execute(
            "UPDATE choice_prompt SET decision_summary = 'changed' WHERE id = 'CHOICE-1'"
        )
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        connection.execute(
            "DELETE FROM choice_event WHERE choice_id = 'CHOICE-1'"
        )
    changed = selection("CHOICE-1", actor, selected="deep-audit")
    with pytest.raises(OpsError, match="conflicts"):
        record_choice_selection(connection, "anyang-internal", changed)


def test_selected_choice_survives_sqlite_backup_recovery(tmp_path):
    source_path = tmp_path / "source.db"
    backup_path = tmp_path / "backup.db"
    with connect(source_path, create_parent=True) as source:
        migrate(source, NOW)
        init_tenant(
            source,
            slug="anyang-internal",
            name="Anyang Internal",
            policy_profile="choice-learning-v1",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp=NOW,
        )
        actor = add_actor(source, "anyang-internal", "Steward", "operator").id
        record_choice_selection(
            source, "anyang-internal", selection("CHOICE-BACKUP", actor)
        )
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
    with connect(backup_path) as restored:
        assert restored.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert schema_version(restored) == SCHEMA_VERSION
        projection = choice_projection(restored, "CHOICE-BACKUP")
        assert projection["selection"]["payload"]["selected_option_key"] == "small-proof"
        assert projection["lineage"]["chain_verified"] is True


def test_validation_privacy_tenant_and_hash_tampering(ledger):
    connection, actor = ledger
    malformed = selection("BAD-1", actor)
    malformed["options"][2]["role"] = "alternative"
    with pytest.raises(OpsError, match="Duplicate choice option role"):
        record_choice_selection(connection, "anyang-internal", malformed)
    no_discovery_or_pause = selection("BAD-SHAPE", actor)
    no_discovery_or_pause["options"] = no_discovery_or_pause["options"][:2] + [
        {
            **no_discovery_or_pause["options"][2],
            "role": "pause-or-deepen",
        }
    ]
    record_choice_selection(
        connection, "anyang-internal", no_discovery_or_pause
    )
    private = selection("BAD-2", actor)
    private["learning_context"] = {"customer_private_body": "forbidden"}
    with pytest.raises(OpsError, match="may not store"):
        record_choice_selection(connection, "anyang-internal", private)

    init_tenant(
        connection,
        slug="other",
        name="Other",
        policy_profile="test",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    other_actor = add_actor(connection, "other", "Other Actor", "operator").id
    cross_tenant = selection("BAD-3", other_actor)
    with pytest.raises(OpsError, match="cross-tenant"):
        record_choice_selection(connection, "anyang-internal", cross_tenant)

    record_choice_selection(
        connection, "anyang-internal", selection("CHOICE-TAMPER", actor)
    )
    connection.execute("DROP TRIGGER choice_event_append_only_update")
    connection.execute(
        "UPDATE choice_event SET action_summary = 'tampered' "
        "WHERE choice_id = 'CHOICE-TAMPER'"
    )
    assert verify_choice(connection, "CHOICE-TAMPER")["ok"] is False


def test_outcome_learning_thresholds_guardrails_and_review_order(ledger):
    connection, actor = ledger
    for index in range(1, 4):
        identifier = f"CHOICE-{index}"
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
        record_choice_event(
            connection,
            identifier,
            outcome(
                f"result-{index}",
                "successful" if index < 3 else "mixed",
                authority_issue=index == 1,
            ),
        )
    context = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-01T12:00:00Z",
    )
    pattern = context["outcome_patterns"][0]
    assert pattern["resolved"] == 3
    assert pattern["evidence_tier"] == "pattern"
    assert context["recommendation_guidance"]["selection_frequency_used"] is False
    assert context["recommendation_guidance"]["preserve_overlooked_possibility"] is True
    assert context["guardrails"][0]["choice_id"] == "CHOICE-1"

    pending = selection("PENDING-ORDINARY", actor)
    record_choice_selection(connection, "anyang-internal", pending)
    sensitive = selection("PENDING-SENSITIVE", actor)
    sensitive["consequence_level"] = "authority-sensitive"
    record_choice_selection(connection, "anyang-internal", sensitive)
    review = choice_review(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "2026-08-01T12:00:00Z",
    )
    assert review["choices"][0]["choice_id"] == "PENDING-SENSITIVE"
    assert review["coffee_limit"] == 1
    assert review["five_selection_review"]["assessment"] == "pending"


def test_five_selection_scorecard_continues_without_using_frequency(ledger):
    connection, actor = ledger
    for index in range(1, 6):
        identifier = f"COHORT-CONTINUE-{index}"
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
        record_choice_event(
            connection, identifier, outcome(f"cohort-continue-{index}")
        )
    review = choice_review(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "2026-08-01T12:00:00Z",
    )
    scorecard = review["five_selection_review"]
    assert scorecard["sample_ready"] is True
    assert scorecard["assessment"] == "continue"
    assert scorecard["primary_metrics"]["lower_cognitive_load"] == {
        "favorable_value": "lower",
        "favorable": 5,
        "observed": 5,
        "rate_percent": 100.0,
        "pilot_target": 3,
        "signal_met": True,
    }
    assert scorecard["primary_metrics"]["new_useful_path"]["pilot_target"] == 1
    assert scorecard["selection_frequency_used"] is False
    assert scorecard["guardrails"]["selection_frequency_used"] is False
    assert scorecard["supporting_evidence"]["rework_minutes"]["median"] == 2.0
    markdown = render_choice_review_markdown(review)
    assert "## Five-Selection Navigation Review" in markdown
    assert "Assessment: `continue`" in markdown


def test_five_selection_scorecard_extends_when_observations_are_missing(ledger):
    connection, actor = ledger
    for index in range(1, 6):
        identifier = f"COHORT-MISSING-{index}"
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
        packet = outcome(f"cohort-missing-{index}")
        packet["payload"]["cognitive_load"] = "Missing"
        packet["payload"]["momentum"] = "Missing"
        packet["payload"]["discovery_value"] = "Missing"
        record_choice_event(connection, identifier, packet)
    scorecard = choice_review(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "2026-08-01T12:00:00Z",
    )["five_selection_review"]
    assert scorecard["assessment"] == "extend-to-ten"
    assert scorecard["primary_metrics"]["lower_cognitive_load"]["observed"] == 0
    assert scorecard["primary_metrics"]["lower_cognitive_load"]["rate_percent"] is None


def test_five_selection_scorecard_adjusts_for_repeated_negative_experience(ledger):
    connection, actor = ledger
    for index in range(1, 6):
        identifier = f"COHORT-ADJUST-{index}"
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
        packet = outcome(f"cohort-adjust-{index}")
        if index <= 2:
            packet["payload"]["cognitive_load"] = "higher"
            packet["payload"]["momentum"] = "stalled"
            packet["payload"]["discovery_value"] = "not-useful"
        record_choice_event(connection, identifier, packet)
    scorecard = choice_review(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "2026-08-01T12:00:00Z",
    )["five_selection_review"]
    assert scorecard["assessment"] == "adjust"
    assert scorecard["supporting_evidence"]["negative_experience_count"] == 2
    assert scorecard["supporting_evidence"]["negative_experience_choice_ids"] == [
        "COHORT-ADJUST-1",
        "COHORT-ADJUST-2",
    ]


def test_five_selection_scorecard_holds_on_boundary_incident(ledger):
    connection, actor = ledger
    for index in range(1, 6):
        identifier = f"COHORT-HOLD-{index}"
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
        record_choice_event(
            connection,
            identifier,
            outcome(
                f"cohort-hold-{index}",
                authority_issue=index == 3,
            ),
        )
    scorecard = choice_review(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "2026-08-01T12:00:00Z",
    )["five_selection_review"]
    assert scorecard["assessment"] == "hold"
    assert scorecard["guardrails"]["authority_or_membrane_incidents"] == 1
    assert scorecard["guardrails"]["incident_choice_ids"] == ["COHORT-HOLD-3"]


def test_not_observable_correction_and_supersession(ledger):
    connection, actor = ledger
    record_choice_selection(
        connection, "anyang-internal", selection("CHOICE-CORRECT", actor)
    )
    record_choice_event(
        connection, "CHOICE-CORRECT", outcome("not-observable", "not_observable")
    )
    assert choice_projection(connection, "CHOICE-CORRECT")["current_state"] == "outcome_observed"
    record_choice_event(
        connection,
        "CHOICE-CORRECT",
        {
            "event_key": "correction",
            "event_type": "corrected",
            "recorded_by": "Council Steward",
            "action_summary": "Correct the bounded outcome",
            "payload": {
                "reason": "Later synthetic evidence arrived",
                "replacement_outcome": {
                    "result": "mixed",
                    "observation": "The path partly worked",
                },
            },
        },
    )
    assert choice_projection(connection, "CHOICE-CORRECT")["outcome"]["payload"][
        "result"
    ] == "mixed"
    record_choice_event(
        connection,
        "CHOICE-CORRECT",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Supersede the old choice",
            "payload": {
                "reason": "The decision changed",
                "superseding_choice_id": "CHOICE-NEXT",
            },
        },
    )
    assert choice_projection(connection, "CHOICE-CORRECT")["current_state"] == "superseded"


def test_choice_cli_dry_run_show_context_review_and_verify(tmp_path, capsys):
    db = tmp_path / "cli.db"
    with connect(db, create_parent=True) as connection:
        migrate(connection, NOW)
        init_tenant(
            connection,
            slug="anyang-internal",
            name="Internal",
            policy_profile="test",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
            timestamp=NOW,
        )
        actor = add_actor(connection, "anyang-internal", "Steward", "operator").id
    packet_path = tmp_path / "selection.yaml"
    packet_path.write_text(
        yaml.safe_dump(selection("CLI-CHOICE", actor), sort_keys=False),
        encoding="utf-8",
    )
    base = ["--db", str(db), "choice"]
    assert main(base + ["select", "--tenant", "anyang-internal", "--packet", str(packet_path), "--dry-run"]) == 0
    assert json.loads(capsys.readouterr().out)["dry_run"] is True
    assert main(base + ["select", "--tenant", "anyang-internal", "--packet", str(packet_path)]) == 0
    capsys.readouterr()
    assert main(base + ["show", "CLI-CHOICE", "--format", "json"]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["choice"]["id"] == "CLI-CHOICE"
    assert main(base + ["verify", "CLI-CHOICE"]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert main(base + ["context", "--tenant", "anyang-internal", "--workspace", "anyang-intelligence", "--lane", "repository", "--kind", "next-action", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["recommendation_guidance"][
        "selection_frequency_used"
    ] is False
    assert main(base + ["review", "--tenant", "anyang-internal", "--workspace", "anyang-intelligence", "--as-of", "2026-08-01T00:00:00Z", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["due_count"] == 1
