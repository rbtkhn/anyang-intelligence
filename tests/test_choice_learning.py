from __future__ import annotations

import json
import sqlite3

import pytest
import yaml

import anyang_loop.choice_learning as choice_learning_module
from anyang_loop.choice_learning import (
    choice_context,
    choice_projection,
    choice_review,
    load_choice_packet,
    record_choice_event,
    record_retained_choice_outcome,
    record_choice_selection,
    render_choice_context_markdown,
    render_choice_markdown,
    render_choice_review_markdown,
    validate_choice_event_packet,
    validate_retained_outcome_packet,
    validate_choice_selection_packet,
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


def classified_selection(
    identifier: str,
    actor: str,
    *,
    selected_key: str,
    comparability_key: str | None = "repository-authorized-push-v1",
) -> dict:
    packet = selection(identifier, actor)
    selected = packet["options"][0]
    selected["key"] = selected_key
    selected["label"] = f"Push authorized change {selected_key}"
    selected["classification_version"] = "LFC-CONTINUITY-v0.2"
    selected["pattern_key"] = "execute-bounded"
    selected["action_boundary"] = "external-action"
    if comparability_key:
        selected["comparability_key"] = comparability_key
    packet["recommendation_key"] = selected_key
    packet["selected_option_key"] = selected_key
    return packet


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


def retained_preflight_packet(identifier: str, actor: str, *, result: str = "successful") -> dict:
    packet = selection(identifier, actor, selected="small-proof")
    packet["schema"] = "anyang-choice-retained-outcome/v1"
    packet["consequence_level"] = "consequential"
    packet["comparison_context"] = {
        "decision_seam": "pre-mutation-evidence-depth",
        "work_class": "governed-operating-surface",
        "risk_class": "consequential",
    }
    packet["retention"] = {
        "provenance_mode": "same-task-reviewed-reconstruction",
        "original_menu_visible": True,
        "retention_authority_ref": f"fictional://authority/{identifier}",
        "reviewed_by": "Council Steward",
    }
    selected = packet["options"][0]
    selected["classification_version"] = "LFC-CONTINUITY-v0.3"
    selected["pattern_key"] = "gather-evidence"
    selected["action_boundary"] = "read-only"
    selected["comparability_key"] = "repository-governance-preflight-v1"
    packet["outcome"] = {
        "event_key": "retained-outcome",
        "action_summary": "Retain the reviewed preflight outcome",
        "evidence_ref": f"fictional://preflight/{identifier}",
        "occurred_at": "2026-08-07T12:00:00Z",
        "recorded_at": "2026-08-07T12:00:00Z",
        "result": result,
        "cognitive_load": "lower",
        "momentum": "advanced",
        "discovery_value": "new-useful-path",
        "observation": "The preflight exposed a material mismatch",
        "rework_minutes": 0,
        "authority_issue": False,
        "membrane_issue": False,
        "policy_measurements": {
            "preflight_minutes": 5,
            "useful_effect": "material-finding",
            "harm_effect": "none",
            "downstream_validation": "passed",
        },
    }
    return packet


def rehash_choice_events(connection: sqlite3.Connection, choice_id: str) -> None:
    prior_hash = ""
    rows = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence",
        (choice_id,),
    ).fetchall()
    for row in rows:
        values = dict(row)
        values["prior_hash"] = prior_hash
        event_hash = choice_learning_module._event_hash(values)
        connection.execute(
            """UPDATE choice_event SET prior_hash = ?, event_hash = ?
            WHERE id = ?""",
            (prior_hash, event_hash, row["id"]),
        )
        prior_hash = event_hash


def test_retained_outcome_is_reviewed_atomic_and_idempotent(ledger):
    connection, actor = ledger
    packet = retained_preflight_packet("RETAINED-ATOMIC", actor)
    dry_run = validate_retained_outcome_packet(packet, "anyang-internal")
    assert len(dry_run["packet_hash"]) == 64
    assert connection.execute(
        "SELECT COUNT(*) AS count FROM choice_prompt"
    ).fetchone()["count"] == 0

    result = record_retained_choice_outcome(
        connection, "anyang-internal", packet, dry_run["packet_hash"]
    )
    assert result.details["chain_verified"] is True
    projection = choice_projection(connection, "RETAINED-ATOMIC")
    assert projection["learning_eligibility"]["eligible"] is True
    assert projection["learning_eligibility"]["outcome_direction"] == "favorable"
    assert projection["retention"]["reviewed_packet_hash"] == dry_run["packet_hash"]
    assert verify_choice(connection, "RETAINED-ATOMIC")["ok"] is True

    repeated = record_retained_choice_outcome(
        connection, "anyang-internal", packet, dry_run["packet_hash"]
    )
    assert repeated.details["selection_result"] == "choice_selection_exists"
    assert repeated.details["outcome_result"] == "choice_event_exists"
    assert connection.execute(
        "SELECT COUNT(*) AS count FROM choice_event WHERE choice_id = 'RETAINED-ATOMIC'"
    ).fetchone()["count"] == 2


def test_retained_outcome_hash_and_validation_fail_without_partial_write(ledger):
    connection, actor = ledger
    packet = retained_preflight_packet("RETAINED-FAIL", actor)
    dry_run = validate_retained_outcome_packet(packet, "anyang-internal")
    with pytest.raises(OpsError, match="does not match"):
        record_retained_choice_outcome(
            connection, "anyang-internal", packet, "0" * 64
        )
    assert connection.execute(
        "SELECT COUNT(*) AS count FROM choice_prompt WHERE id = 'RETAINED-FAIL'"
    ).fetchone()["count"] == 0

    packet["outcome"]["policy_measurements"]["preflight_minutes"] = -1
    with pytest.raises(OpsError, match="non-negative"):
        validate_retained_outcome_packet(packet, "anyang-internal")
    assert dry_run["packet_hash"]
    assert connection.execute(
        "SELECT COUNT(*) AS count FROM choice_prompt WHERE id = 'RETAINED-FAIL'"
    ).fetchone()["count"] == 0


def test_active_preflight_policy_threshold_contradiction_and_staleness(ledger):
    connection, actor = ledger
    for index, result in enumerate(("successful", "successful", "mixed"), start=1):
        packet = retained_preflight_packet(f"ACTIVE-PREFLIGHT-{index}", actor, result=result)
        if result == "mixed":
            packet["outcome"]["policy_measurements"]["useful_effect"] = "no-material-effect"
        dry_run = validate_retained_outcome_packet(packet, "anyang-internal")
        record_retained_choice_outcome(
            connection, "anyang-internal", packet, dry_run["packet_hash"]
        )
    context = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-08T12:00:00Z",
    )
    assert context["recommendation_guidance"]["favored_comparability_keys"] == [
        "repository-governance-preflight-v1"
    ]
    cohort = next(
        item
        for item in context["comparability_cohorts"]
        if item["comparability_key"] == "repository-governance-preflight-v1"
    )
    assert cohort["favorable"] == 2
    assert cohort["neutral"] == 1

    contradiction = retained_preflight_packet(
        "ACTIVE-PREFLIGHT-CONTRADICTION", actor, result="unsuccessful"
    )
    contradiction["outcome"]["policy_measurements"].update(
        {
            "preflight_minutes": 20,
            "useful_effect": "no-material-effect",
            "harm_effect": "false-hold",
            "downstream_validation": "failed",
        }
    )
    dry_run = validate_retained_outcome_packet(contradiction, "anyang-internal")
    record_retained_choice_outcome(
        connection, "anyang-internal", contradiction, dry_run["packet_hash"]
    )
    contradicted = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-08T12:00:00Z",
    )
    assert contradicted["recommendation_guidance"]["favored_comparability_keys"] == []
    assert contradicted["recommendation_guidance"]["demoted_comparability_keys"] == []

    stale = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2027-01-08T12:00:00Z",
    )
    stale_cohort = next(
        item
        for item in stale["comparability_cohorts"]
        if item["comparability_key"] == "repository-governance-preflight-v1"
    )
    assert stale_cohort["resolved"] == 0
    assert stale_cohort["excluded_stale"] == 4


def test_active_preflight_policy_rejects_scope_and_provenance_drift(ledger):
    _connection, actor = ledger
    packet = retained_preflight_packet("RETAINED-SCOPE", actor)
    packet["lane"] = "learning-core"
    with pytest.raises(OpsError, match="scope mismatch"):
        validate_retained_outcome_packet(packet, "anyang-internal")
    packet = retained_preflight_packet("RETAINED-PROVENANCE", actor)
    packet["retention"]["provenance_mode"] = "cross-task-reconstruction"
    with pytest.raises(OpsError, match="same-task"):
        validate_retained_outcome_packet(packet, "anyang-internal")


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
    assert projection["schema_version"] == 2
    assert projection["options"] == packet["options"]
    assert projection["selection"]["payload"]["selected_option_key"] == "small-proof"
    assert projection["lineage"]["authority_effect"] == "none"
    assert projection["effective_classification"] == {
        "classification_version": "legacy-unclassified",
        "pattern_key": "unclassified",
        "action_boundary": "unclassified",
        "comparability_key": "Missing",
    }
    assert projection["learning_eligibility"]["eligible"] is False
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


def test_hash_consistent_semantic_tampering_fails_verification(ledger):
    connection, actor = ledger
    record_choice_selection(
        connection, "anyang-internal", selection("SEMANTIC-ROLE", actor)
    )
    connection.execute("DROP TRIGGER choice_event_append_only_update")
    selection_event = connection.execute(
        "SELECT payload_json FROM choice_event WHERE choice_id = 'SEMANTIC-ROLE'"
    ).fetchone()
    payload = json.loads(selection_event["payload_json"])
    payload["selected_option_role"] = "alternative"
    connection.execute(
        """UPDATE choice_event SET payload_json = ?
        WHERE choice_id = 'SEMANTIC-ROLE'""",
        (
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ),
        ),
    )
    rehash_choice_events(connection, "SEMANTIC-ROLE")
    verification = verify_choice(connection, "SEMANTIC-ROLE")
    assert verification["integrity_ok"] is True
    assert verification["semantics_ok"] is False
    assert {issue["code"] for issue in verification["issues"]} == {
        "selection-role-mismatch"
    }

    record_choice_selection(
        connection, "anyang-internal", selection("SEMANTIC-OPTIONS", actor)
    )
    connection.execute("DROP TRIGGER choice_prompt_immutable_update")
    options = json.loads(
        connection.execute(
            "SELECT options_json FROM choice_prompt WHERE id = 'SEMANTIC-OPTIONS'"
        ).fetchone()["options_json"]
    )
    options[0]["label"] = "Changed after selection"
    connection.execute(
        "UPDATE choice_prompt SET options_json = ? WHERE id = 'SEMANTIC-OPTIONS'",
        (
            json.dumps(
                options,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ),
        ),
    )
    verification = verify_choice(connection, "SEMANTIC-OPTIONS")
    assert verification["integrity_ok"] is True
    assert verification["semantics_ok"] is False
    assert "option-set-hash-mismatch" in {
        issue["code"] for issue in verification["issues"]
    }

    record_choice_selection(
        connection, "anyang-internal", selection("SEMANTIC-DUPLICATE", actor)
    )
    first = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = 'SEMANTIC-DUPLICATE'"
    ).fetchone()
    duplicate = dict(first)
    duplicate.update(
        {
            "id": "semantic-duplicate-selection",
            "event_key": "selection-duplicate",
            "sequence": 2,
            "prior_hash": first["event_hash"],
            "recorded_at": "2026-07-29T12:00:01Z",
        }
    )
    duplicate["event_hash"] = choice_learning_module._event_hash(duplicate)
    connection.execute(
        """INSERT INTO choice_event(
            id, choice_id, tenant_id, event_key, sequence, event_type,
            actor_id, actor_label, action_summary, occurred_at, recorded_at,
            evidence_ref, payload_json, prior_hash, event_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(
            duplicate[key]
            for key in (
                "id",
                "choice_id",
                "tenant_id",
                "event_key",
                "sequence",
                "event_type",
                "actor_id",
                "actor_label",
                "action_summary",
                "occurred_at",
                "recorded_at",
                "evidence_ref",
                "payload_json",
                "prior_hash",
                "event_hash",
            )
        ),
    )
    verification = verify_choice(connection, "SEMANTIC-DUPLICATE")
    assert verification["integrity_ok"] is True
    assert verification["semantics_ok"] is False
    assert "selection-count-invalid" in {
        issue["code"] for issue in verification["issues"]
    }


def test_supersession_requires_existing_same_scope_acyclic_choice(ledger):
    connection, actor = ledger
    for identifier in ("SUPER-A", "SUPER-B", "SUPER-MISSING", "SUPER-SELF"):
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )

    record_choice_event(
        connection,
        "SUPER-A",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Supersede with a valid same-scope choice",
            "payload": {
                "reason": "A newer bounded choice exists",
                "superseding_choice_id": "SUPER-B",
            },
        },
    )
    assert verify_choice(connection, "SUPER-A")["ok"] is True

    record_choice_event(
        connection,
        "SUPER-MISSING",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Reference a missing choice",
            "payload": {
                "reason": "Synthetic invalid lineage",
                "superseding_choice_id": "DOES-NOT-EXIST",
            },
        },
    )
    assert "superseding-choice-missing" in {
        issue["code"]
        for issue in verify_choice(connection, "SUPER-MISSING")["issues"]
    }

    record_choice_event(
        connection,
        "SUPER-SELF",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Reference the same choice",
            "payload": {
                "reason": "Synthetic cycle",
                "superseding_choice_id": "SUPER-SELF",
            },
        },
    )
    assert "supersession-cycle" in {
        issue["code"] for issue in verify_choice(connection, "SUPER-SELF")["issues"]
    }

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
    other_actor = add_actor(connection, "other", "Other Steward", "operator").id
    record_choice_selection(
        connection, "other", selection("SUPER-OTHER", other_actor)
    )
    record_choice_selection(
        connection, "anyang-internal", selection("SUPER-CROSS", actor)
    )
    record_choice_event(
        connection,
        "SUPER-CROSS",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Reference another tenant",
            "payload": {
                "reason": "Synthetic cross-scope lineage",
                "superseding_choice_id": "SUPER-OTHER",
            },
        },
    )
    assert "superseding-choice-scope-mismatch" in {
        issue["code"] for issue in verify_choice(connection, "SUPER-CROSS")["issues"]
    }

    for identifier in ("SUPER-CYCLE-A", "SUPER-CYCLE-B"):
        record_choice_selection(
            connection, "anyang-internal", selection(identifier, actor)
        )
    for origin, target in (
        ("SUPER-CYCLE-A", "SUPER-CYCLE-B"),
        ("SUPER-CYCLE-B", "SUPER-CYCLE-A"),
    ):
        record_choice_event(
            connection,
            origin,
            {
                "event_key": "superseded",
                "event_type": "superseded",
                "recorded_by": "Council Steward",
                "action_summary": "Create a synthetic supersession cycle",
                "payload": {
                    "reason": "Synthetic cyclic lineage",
                    "superseding_choice_id": target,
                },
            },
        )
    assert "supersession-cycle" in {
        issue["code"]
        for issue in verify_choice(connection, "SUPER-CYCLE-A")["issues"]
    }


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
    assert pattern["evidence_tier"] == "descriptive-only"
    assert pattern["recommendation_effect"] == "none"
    assert context["comparability_cohorts"] == []
    assert context["guidance_policy"]["id"] == "LFC-CAL-2026-07-30-01"
    assert context["guidance_policy"]["phase"] == "calibration"
    assert context["recommendation_guidance"]["ordering_frozen"] is True
    assert context["recommendation_guidance"]["favored_option_keys"] == []
    assert context["recommendation_guidance"][
        "diagnostic_favored_comparability_keys"
    ] == []
    assert context["recommendation_guidance"]["option_key_learning_used"] is False
    assert context["recommendation_guidance"]["selection_frequency_used"] is False
    assert context["recommendation_guidance"]["preserve_overlooked_possibility"] is True
    assert context["guardrails"][0]["choice_id"] == "CHOICE-1"

    after_window = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-07T12:00:00Z",
    )
    assert after_window["guidance_policy"]["id"] == "LFC-ACTIVE-v1.0"
    assert after_window["guidance_policy"]["phase"] == "calibration"
    assert after_window["recommendation_guidance"]["ordering_frozen"] is False
    assert after_window["recommendation_guidance"]["favored_option_keys"] == []

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


def test_classification_validation_scope_and_legacy_hash_compatibility(
    ledger, monkeypatch
):
    connection, actor = ledger
    legacy = selection("LEGACY-COMPAT", actor)
    record_choice_selection(connection, "anyang-internal", legacy)
    assert record_choice_selection(
        connection, "anyang-internal", legacy
    ).details["idempotent"] is True
    stored = json.loads(
        connection.execute(
            "SELECT options_json FROM choice_prompt WHERE id = 'LEGACY-COMPAT'"
        ).fetchone()["options_json"]
    )
    assert stored == legacy["options"]
    assert all("pattern_key" not in option for option in stored)

    valid = classified_selection(
        "CLASSIFIED-VALID", actor, selected_key="push-classified-valid"
    )
    normalized = validate_choice_selection_packet(valid, "anyang-internal")
    assert normalized["options"][0]["pattern_key"] == "execute-bounded"
    record_choice_selection(connection, "anyang-internal", valid)
    projection = choice_projection(connection, "CLASSIFIED-VALID")
    assert projection["original_classification"]["action_boundary"] == "external-action"
    assert projection["comparability_policy"]["status"] == "diagnostic-only"

    partial = classified_selection(
        "CLASSIFIED-PARTIAL", actor, selected_key="push-partial"
    )
    del partial["options"][0]["action_boundary"]
    with pytest.raises(OpsError, match="missing required fields"):
        validate_choice_selection_packet(partial, "anyang-internal")

    invalid_pattern = classified_selection(
        "CLASSIFIED-PATTERN", actor, selected_key="push-pattern"
    )
    invalid_pattern["options"][0]["pattern_key"] = "always-do-this"
    with pytest.raises(OpsError, match="pattern_key"):
        validate_choice_selection_packet(invalid_pattern, "anyang-internal")

    invalid_boundary = classified_selection(
        "CLASSIFIED-BOUNDARY", actor, selected_key="push-boundary"
    )
    invalid_boundary["options"][0]["action_boundary"] = "silent-execution"
    with pytest.raises(OpsError, match="action_boundary"):
        validate_choice_selection_packet(invalid_boundary, "anyang-internal")

    unknown_policy = classified_selection(
        "CLASSIFIED-POLICY", actor, selected_key="push-policy"
    )
    unknown_policy["options"][0]["comparability_key"] = "model-invented-v1"
    with pytest.raises(OpsError, match="Unknown choice comparability policy"):
        validate_choice_selection_packet(unknown_policy, "anyang-internal")

    wrong_workspace = classified_selection(
        "CLASSIFIED-WORKSPACE", actor, selected_key="push-workspace"
    )
    wrong_workspace["workspace_id"] = "another-workspace"
    with pytest.raises(OpsError, match="scope mismatch"):
        validate_choice_selection_packet(wrong_workspace, "anyang-internal")
    with pytest.raises(OpsError, match="scope mismatch"):
        validate_choice_selection_packet(valid, "other")

    oversized = classified_selection(
        "CLASSIFIED-OVERSIZED", actor, selected_key="push-oversized"
    )
    oversized["options"][0]["comparability_key"] = "x" * 121
    with pytest.raises(OpsError, match="exceeds"):
        validate_choice_selection_packet(oversized, "anyang-internal")

    private = classified_selection(
        "CLASSIFIED-PRIVATE", actor, selected_key="push-private"
    )
    private["options"][0]["classification_version"] = "operator" + "@" + "example.com"
    with pytest.raises(OpsError, match="privacy"):
        validate_choice_selection_packet(private, "anyang-internal")

    disabled_policy = {
        **choice_learning_module.CHOICE_COMPARABILITY_POLICIES[0],
        "status": "disabled",
    }
    monkeypatch.setattr(
        choice_learning_module,
        "CHOICE_COMPARABILITY_POLICIES",
        (disabled_policy,),
    )
    with pytest.raises(OpsError, match="disabled"):
        validate_choice_selection_packet(valid, "anyang-internal")


def test_explicit_comparability_cohort_is_diagnostic_and_ignores_option_keys(
    ledger,
):
    connection, actor = ledger
    for index, result in enumerate(("successful", "successful", "mixed"), start=1):
        identifier = f"EXPLICIT-COHORT-{index}"
        packet = classified_selection(
            identifier,
            actor,
            selected_key=f"unique-authorized-push-{index}",
        )
        record_choice_selection(connection, "anyang-internal", packet)
        record_choice_event(connection, identifier, outcome(f"explicit-{index}", result))
    missing_evidence = classified_selection(
        "EXPLICIT-MISSING-EVIDENCE",
        actor,
        selected_key="unique-authorized-push-missing-evidence",
    )
    record_choice_selection(
        connection, "anyang-internal", missing_evidence
    )
    missing_outcome = outcome("explicit-missing-evidence")
    missing_outcome["evidence_ref"] = ""
    record_choice_event(
        connection, "EXPLICIT-MISSING-EVIDENCE", missing_outcome
    )
    superseded = classified_selection(
        "EXPLICIT-SUPERSEDED",
        actor,
        selected_key="unique-authorized-push-superseded",
    )
    record_choice_selection(connection, "anyang-internal", superseded)
    record_choice_event(
        connection, "EXPLICIT-SUPERSEDED", outcome("explicit-superseded")
    )
    record_choice_selection(
        connection,
        "anyang-internal",
        selection("EXPLICIT-SUPERSEDING", actor),
    )
    record_choice_event(
        connection,
        "EXPLICIT-SUPERSEDED",
        {
            "event_key": "superseded",
            "event_type": "superseded",
            "recorded_by": "Council Steward",
            "action_summary": "Supersede the synthetic push choice",
            "payload": {
                "reason": "A replacement choice exists",
                "superseding_choice_id": "EXPLICIT-SUPERSEDING",
            },
        },
    )
    context = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-01T12:00:00Z",
    )
    assert len(context["outcome_patterns"]) == 5
    assert all(
        item["recommendation_effect"] == "none"
        for item in context["outcome_patterns"]
    )
    cohort = context["comparability_cohorts"][0]
    assert cohort["comparability_key"] == "repository-authorized-push-v1"
    assert cohort["resolved"] == 3
    assert cohort["evidence_tier"] == "pattern"
    assert cohort["diagnostic_direction"] == "favored"
    assert cohort["recommendation_effect"] == "none"
    guidance = context["recommendation_guidance"]
    assert guidance["favored_option_keys"] == []
    assert guidance["favored_comparability_keys"] == []
    assert guidance["diagnostic_favored_comparability_keys"] == [
        "repository-authorized-push-v1"
    ]
    assert guidance["selection_frequency_used"] is False
    assert guidance["option_key_learning_used"] is False
    assert context["diversity_diagnostics"]["pattern_counts"][
        "execute-bounded"
    ] == 5
    excluded = choice_projection(connection, "EXPLICIT-MISSING-EVIDENCE")
    assert excluded["learning_eligibility"]["eligible"] is False
    assert "outcome-evidence-missing" in excluded["learning_eligibility"][
        "exclusion_reasons"
    ]
    superseded_projection = choice_projection(
        connection, "EXPLICIT-SUPERSEDED"
    )
    assert "choice-superseded" in superseded_projection[
        "learning_eligibility"
    ]["exclusion_reasons"]


def test_active_comparability_policy_threshold_contradiction_and_freeze(
    ledger, monkeypatch
):
    connection, actor = ledger
    active_policy = {
        **choice_learning_module.CHOICE_COMPARABILITY_POLICIES[0],
        "status": "active",
    }
    monkeypatch.setattr(
        choice_learning_module,
        "CHOICE_COMPARABILITY_POLICIES",
        (active_policy,),
    )
    for index, result in enumerate(("successful", "successful", "mixed"), start=1):
        identifier = f"ACTIVE-COHORT-{index}"
        record_choice_selection(
            connection,
            "anyang-internal",
            classified_selection(
                identifier,
                actor,
                selected_key=f"active-authorized-push-{index}",
            ),
        )
        record_choice_event(connection, identifier, outcome(f"active-{index}", result))
    before_calibration = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-07-29T12:00:00Z",
    )
    assert before_calibration["recommendation_guidance"][
        "favored_comparability_keys"
    ] == ["repository-authorized-push-v1"]
    during_calibration = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-01T12:00:00Z",
    )
    assert during_calibration["recommendation_guidance"][
        "favored_comparability_keys"
    ] == []
    assert during_calibration["recommendation_guidance"][
        "diagnostic_favored_comparability_keys"
    ] == ["repository-authorized-push-v1"]

    record_choice_selection(
        connection,
        "anyang-internal",
        classified_selection(
            "ACTIVE-CONTRADICTION",
            actor,
            selected_key="active-authorized-push-contradiction",
        ),
    )
    record_choice_event(
        connection,
        "ACTIVE-CONTRADICTION",
        outcome("active-contradiction", "unsuccessful"),
    )
    contradicted = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-07-29T12:00:00Z",
    )
    assert contradicted["recommendation_guidance"][
        "favored_comparability_keys"
    ] == []
    assert contradicted["recommendation_guidance"][
        "demoted_comparability_keys"
    ] == []


def test_append_only_classification_corrections_and_learning_eligibility(ledger):
    connection, actor = ledger
    packet = classified_selection(
        "CLASSIFICATION-CORRECT",
        actor,
        selected_key="corrected-authorized-push",
        comparability_key=None,
    )
    record_choice_selection(connection, "anyang-internal", packet)
    record_choice_event(
        connection,
        "CLASSIFICATION-CORRECT",
        outcome("classification-result"),
    )
    record_choice_event(
        connection,
        "CLASSIFICATION-CORRECT",
        {
            "event_key": "classification-correction",
            "event_type": "corrected",
            "recorded_by": "Council Steward",
            "action_summary": "Attach the governed comparability policy",
            "payload": {
                "reason": "The exact push policy now applies",
                "classification_correction": {
                    "option_key": "corrected-authorized-push",
                    "field": "comparability_key",
                    "prior_value": "Missing",
                    "replacement_value": "repository-authorized-push-v1",
                    "policy_ref": "repository-authorized-push-v1",
                },
            },
        },
    )
    projection = choice_projection(connection, "CLASSIFICATION-CORRECT")
    assert projection["current_state"] == "outcome_observed"
    assert projection["original_classification"]["comparability_key"] == "Missing"
    assert (
        projection["effective_classification"]["comparability_key"]
        == "repository-authorized-push-v1"
    )
    assert projection["classification_corrections"][0]["valid"] is True
    assert projection["classification_verified"] is True
    assert projection["learning_eligibility"]["eligible"] is True
    assert verify_choice(connection, "CLASSIFICATION-CORRECT")["ok"] is True

    stale = {
        "event_key": "classification-stale",
        "event_type": "corrected",
        "recorded_by": "Council Steward",
        "action_summary": "Attempt a stale classification correction",
        "payload": {
            "reason": "Synthetic stale prior value",
            "classification_correction": {
                "option_key": "corrected-authorized-push",
                "field": "comparability_key",
                "prior_value": "Missing",
                "replacement_value": "repository-authorized-push-v1",
                "policy_ref": "repository-authorized-push-v1",
            },
        },
    }
    with pytest.raises(OpsError, match="prior_value is stale"):
        record_choice_event(connection, "CLASSIFICATION-CORRECT", stale)

    invalid_target = {
        **stale,
        "event_key": "classification-invalid-target",
        "payload": {
            **stale["payload"],
            "classification_correction": {
                **stale["payload"]["classification_correction"],
                "option_key": "missing-option",
            },
        },
    }
    with pytest.raises(OpsError, match="unknown option"):
        record_choice_event(
            connection, "CLASSIFICATION-CORRECT", invalid_target
        )

    record_choice_event(
        connection,
        "CLASSIFICATION-CORRECT",
        {
            "event_key": "classification-policy-removed",
            "event_type": "corrected",
            "recorded_by": "Council Steward",
            "action_summary": "Remove the comparability policy",
            "payload": {
                "reason": "The cohort no longer applies",
                "classification_correction": {
                    "option_key": "corrected-authorized-push",
                    "field": "comparability_key",
                    "prior_value": "repository-authorized-push-v1",
                    "replacement_value": "Missing",
                    "policy_ref": "repository-authorized-push-v1",
                },
            },
        },
    )
    removed = choice_projection(connection, "CLASSIFICATION-CORRECT")
    assert removed["effective_classification"]["comparability_key"] == "Missing"
    assert removed["learning_eligibility"]["eligible"] is False
    assert len(removed["classification_corrections"]) == 2

    invalid_removal_policy = {
        "event_type": "corrected",
        "payload": {
            "reason": "Invalid removal policy reference",
            "classification_correction": {
                "option_key": "corrected-authorized-push",
                "field": "comparability_key",
                "prior_value": "repository-authorized-push-v1",
                "replacement_value": "Missing",
                "policy_ref": "LFC-CONTINUITY-v0.2",
            },
        },
    }
    with pytest.raises(OpsError, match="Unknown choice comparability policy"):
        validate_choice_event_packet(invalid_removal_policy)

    no_change = {
        "event_type": "corrected",
        "payload": {
            "reason": "Invalid no-op correction",
            "classification_correction": {
                "option_key": "corrected-authorized-push",
                "field": "comparability_key",
                "prior_value": "Missing",
                "replacement_value": "Missing",
                "policy_ref": "repository-authorized-push-v1",
            },
        },
    }
    with pytest.raises(OpsError, match="must change"):
        validate_choice_event_packet(no_change)

    combined = {
        "event_type": "corrected",
        "payload": {
            "reason": "Invalid combined correction",
            "replacement_outcome": {
                "result": "mixed",
                "observation": "Synthetic replacement",
            },
            "classification_correction": {
                "option_key": "corrected-authorized-push",
                "field": "comparability_key",
                "prior_value": "repository-authorized-push-v1",
                "replacement_value": "Missing",
                "policy_ref": "LFC-CONTINUITY-v0.2",
            },
        },
    }
    with pytest.raises(OpsError, match="cannot replace"):
        validate_choice_event_packet(combined)


def test_pattern_correction_updates_effective_diversity_without_rewriting_options(
    ledger,
):
    connection, actor = ledger
    packet = classified_selection(
        "CLASSIFICATION-DIVERSITY",
        actor,
        selected_key="diversity-authorized-push",
        comparability_key=None,
    )
    record_choice_selection(connection, "anyang-internal", packet)
    original_options = connection.execute(
        "SELECT options_json FROM choice_prompt WHERE id = ?",
        ("CLASSIFICATION-DIVERSITY",),
    ).fetchone()["options_json"]
    record_choice_event(
        connection,
        "CLASSIFICATION-DIVERSITY",
        {
            "event_key": "pattern-correction",
            "event_type": "corrected",
            "recorded_by": "Council Steward",
            "action_summary": "Correct the selected strategy pattern",
            "payload": {
                "reason": "The branch gathered evidence rather than executing",
                "classification_correction": {
                    "option_key": "diversity-authorized-push",
                    "field": "pattern_key",
                    "prior_value": "execute-bounded",
                    "replacement_value": "gather-evidence",
                    "policy_ref": "LFC-CONTINUITY-v0.2",
                },
            },
        },
    )
    context = choice_context(
        connection,
        "anyang-internal",
        "anyang-intelligence",
        "repository",
        "next-action",
        "2026-08-01T12:00:00Z",
    )
    assert context["diversity_diagnostics"]["pattern_counts"]["execute-bounded"] == 0
    assert context["diversity_diagnostics"]["pattern_counts"]["gather-evidence"] == 1
    projection = choice_projection(connection, "CLASSIFICATION-DIVERSITY")
    assert projection["original_classification"]["pattern_key"] == "execute-bounded"
    assert projection["effective_classification"]["pattern_key"] == "gather-evidence"
    stored_options = connection.execute(
        "SELECT options_json FROM choice_prompt WHERE id = ?",
        ("CLASSIFICATION-DIVERSITY",),
    ).fetchone()["options_json"]
    assert stored_options == original_options


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
    record_choice_selection(
        connection, "anyang-internal", selection("CHOICE-NEXT", actor)
    )
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


def test_choice_packet_normalizes_unquoted_yaml_dates(tmp_path):
    packet_path = tmp_path / "unquoted-dates.yaml"
    packet_path.write_text(
        """id: DATE-DRY-RUN
presented_at: 2026-07-29T18:08:00Z
calendar_day: 2026-07-29
enabled: true
count: 2
nested:
  - occurred_at: 2026-07-30T12:00:00Z
""",
        encoding="utf-8",
    )
    loaded = load_choice_packet(packet_path)
    assert loaded == {
        "id": "DATE-DRY-RUN",
        "presented_at": "2026-07-29T18:08:00Z",
        "calendar_day": "2026-07-29",
        "enabled": True,
        "count": 2,
        "nested": [{"occurred_at": "2026-07-30T12:00:00Z"}],
    }


def test_choice_outcome_dry_run_validates_correction_shape(tmp_path, capsys):
    packet_path = tmp_path / "correction.yaml"
    packet_path.write_text(
        yaml.safe_dump(
            {
                "event_key": "classification-correction",
                "event_type": "corrected",
                "recorded_by": "Council Steward",
                "action_summary": "Correct the classification",
                "payload": {
                    "reason": "Synthetic correction",
                    "classification_correction": {
                        "option_key": "small-proof",
                        "field": "action_boundary",
                        "prior_value": "read-only",
                        "replacement_value": "workspace-mutation",
                        "policy_ref": "LFC-CONTINUITY-v0.2",
                    },
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "--db",
                str(tmp_path / "unused.db"),
                "choice",
                "outcome",
                "MISSING-BY-DESIGN",
                "--packet",
                str(packet_path),
                "--dry-run",
            ]
        )
        == 0
    )
    preview = json.loads(capsys.readouterr().out)
    assert preview["packet"]["payload"]["classification_correction"]["field"] == (
        "action_boundary"
    )
    assert "classification-prior-value" in preview["deferred_checks"]


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
    packet_path = tmp_path / "selection.yaml"
    packet_path.write_text(
        yaml.safe_dump(selection("CLI-CHOICE", actor), sort_keys=False),
        encoding="utf-8",
    )
    base = ["--db", str(db), "choice"]
    assert main(base + ["select", "--tenant", "anyang-internal", "--packet", str(packet_path), "--dry-run"]) == 0
    dry_run = json.loads(capsys.readouterr().out)
    assert dry_run["dry_run"] is True
    assert dry_run["deferred_checks"] == [
        "actor-exists-in-tenant",
        "idempotency-conflict",
    ]
    assert main(base + ["select", "--tenant", "anyang-internal", "--packet", str(packet_path)]) == 0
    capsys.readouterr()
    scope = [
        "--tenant",
        "anyang-internal",
        "--workspace",
        "anyang-intelligence",
        "--lane",
        "repository",
    ]
    assert main(base + ["show", "CLI-CHOICE", *scope, "--format", "json"]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["choice"]["id"] == "CLI-CHOICE"
    assert shown["schema_version"] == 2
    assert shown["effective_classification"]["pattern_key"] == "unclassified"
    assert "## Continuity Classification" in render_choice_markdown(shown)
    assert main(base + ["verify", "CLI-CHOICE", *scope]) == 0
    verified = json.loads(capsys.readouterr().out)
    assert verified["ok"] is True
    assert verified["integrity_ok"] is True
    assert verified["semantics_ok"] is True
    assert verified["verification_profile"] == "choice-semantic-v2"
    for mismatched_scope in (
        [
            "--tenant",
            "other",
            "--workspace",
            "anyang-intelligence",
            "--lane",
            "repository",
        ],
        [
            "--tenant",
            "anyang-internal",
            "--workspace",
            "another-workspace",
            "--lane",
            "repository",
        ],
        [
            "--tenant",
            "anyang-internal",
            "--workspace",
            "anyang-intelligence",
            "--lane",
            "customer",
        ],
    ):
        assert main(base + ["show", "CLI-CHOICE", *mismatched_scope]) == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err.strip() == (
            "ERROR: Choice was not found in the requested scope."
        )
    with pytest.raises(SystemExit):
        main(base + ["verify", "CLI-CHOICE"])
    capsys.readouterr()
    assert main(base + ["context", "--tenant", "anyang-internal", "--workspace", "anyang-intelligence", "--lane", "repository", "--kind", "next-action", "--format", "json"]) == 0
    context = json.loads(capsys.readouterr().out)
    assert context["schema_version"] == 2
    assert context["recommendation_guidance"]["selection_frequency_used"] is False
    assert context["recommendation_guidance"]["option_key_learning_used"] is False
    assert "## Diversity Diagnostics" in render_choice_context_markdown(context)
    assert main(base + ["review", "--tenant", "anyang-internal", "--workspace", "anyang-intelligence", "--as-of", "2026-08-01T00:00:00Z", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["due_count"] == 1


def test_choice_cli_retained_outcome_requires_reviewed_hash(tmp_path, capsys):
    db = tmp_path / "retained-cli.db"
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
        actor = add_actor(connection, "anyang-internal", "Council Steward", "steward").id
    packet_path = tmp_path / "retained.yaml"
    packet_path.write_text(
        yaml.safe_dump(retained_preflight_packet("CLI-RETAINED", actor), sort_keys=False),
        encoding="utf-8",
    )
    base = [
        "--db",
        str(db),
        "choice",
        "retain-outcome",
        "--tenant",
        "anyang-internal",
        "--packet",
        str(packet_path),
    ]
    assert main(base + ["--dry-run"]) == 0
    dry_run = json.loads(capsys.readouterr().out)
    assert dry_run["dry_run"] is True
    assert len(dry_run["packet_hash"]) == 64
    assert main(base) == 1
    assert "--approved-packet-hash is required" in capsys.readouterr().err
    assert main(base + ["--approved-packet-hash", dry_run["packet_hash"]]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["action"] == "choice_retained_outcome_recorded"
    assert result["chain_verified"] is True
