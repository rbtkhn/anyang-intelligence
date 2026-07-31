from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT
    / "projects"
    / "media-production"
    / "schemas"
    / "artistic-director-ai-factory.schema.json"
)
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def errors(record: dict) -> list:
    return sorted(VALIDATOR.iter_errors(record), key=lambda item: list(item.path))


def valid_records() -> list[dict]:
    return [
        {
            "record_type": "dashboard",
            "dashboard_id": "dashboard-1",
            "project_id": "media-production",
            "lane": "media-production",
            "canon_version": "v1",
            "status": "held",
            "owner": "System Engineer",
            "activation_state": "inactive",
            "capacity_state": "held",
            "spend_state": "none",
        },
        {
            "record_type": "thesis",
            "thesis_id": "thesis-1",
            "thesis_text": "A bounded synthetic creative thesis.",
            "intended_viewer_effect": "Curiosity",
            "source_boundary": "Synthetic internal material only",
            "do_not_invent": ["client facts"],
            "do_not_copy": ["named artists"],
            "status": "draft",
        },
        {
            "record_type": "batch",
            "batch_id": "batch-1",
            "task_id": "task-1",
            "brief_id": "brief-1",
            "thesis_id": "thesis-1",
            "stage": "prepared",
            "disposition": "brief",
            "reviewer": "Artistic Director",
            "stop_condition": "Stop before rendering or external action",
        },
        {
            "record_type": "canon_entry",
            "canon_entry_id": "canon-1",
            "asset_type": "style-rule",
            "asset_name": "Restrained palette",
            "asset_version": "v1",
            "provenance": "Synthetic batch",
            "owner": "Artistic Director",
            "review_status": "candidate",
            "reuse_boundary": "Internal candidate only",
            "decision_receipt_id": "decision-1",
        },
        {
            "record_type": "decision",
            "decision_receipt_id": "decision-1",
            "decision_date": "2026-07-31T12:00:00Z",
            "decision_type": "explore",
            "alternatives_considered": ["direction-a", "direction-b"],
            "reasoning": "Preserve alternatives during internal preparation.",
            "reviewer": "Artistic Director",
            "next_permitted_action": "Hold for activation",
            "stop_condition": "No production or publication",
        },
        {
            "record_type": "reference",
            "reference_id": "reference-1",
            "source_location": "internal:synthetic/reference-1",
            "rights_status": "unknown",
            "decision": "held",
            "reviewer": "Artistic Director",
        },
        {
            "record_type": "experiment",
            "experiment_id": "experiment-1",
            "hypothesis": "A compact canon reduces preparation burden.",
            "canon_rule_challenged": "No active canon",
            "expected_effect": "More consistent review packets",
            "result": "Not yet observed",
            "review_status": "draft",
            "next_action": "Hold for activation",
        },
        {
            "record_type": "review",
            "review_id": "review-1",
            "artifact_id": "artifact-1",
            "quality_status": "unknown",
            "rights_status": "unknown",
            "client_authority_status": "not_applicable",
            "publication_status": "not_approved",
            "spend_status": "none",
        },
        {
            "record_type": "compounding",
            "ledger_entry_id": "ledger-1",
            "source_signal": "Synthetic batch preparation",
            "assets_created": ["brief"],
            "reused_where": [],
            "outcome_signal": "Not yet observed",
            "evidence_location": "repo:synthetic/batch-1",
            "review_date": "2026-07-31",
        },
    ]


def test_schema_is_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(SCHEMA)
    assert "grant no publication" in SCHEMA["description"]


@pytest.mark.parametrize("record", valid_records(), ids=lambda item: item["record_type"])
def test_each_record_type_has_a_minimal_valid_shape(record: dict) -> None:
    assert errors(record) == []


def test_optional_batch_budget_does_not_require_authority_but_spend_does() -> None:
    record = valid_records()[2]
    assert errors(record) == []
    assert errors({**record, "budget_impact": 0}) == []
    assert errors({**record, "budget_impact": 1})
    assert errors({**record, "budget_impact": 1, "authority_reference": "approval-1"}) == []


def test_canon_requires_explicit_non_unknown_rights_status() -> None:
    record = {**valid_records()[3], "review_status": "canon"}
    assert errors(record)
    assert errors({**record, "rights_status": "internal"}) == []
    assert errors({**record, "rights_status": "unknown"})


def test_optional_publication_state_does_not_require_authority_but_approval_does() -> None:
    record = valid_records()[4]
    assert errors(record) == []
    assert errors({**record, "publication_state": "approved"})
    assert errors(
        {
            **record,
            "publication_state": "approved",
            "authority_reference": "approval-1",
        }
    ) == []


def test_optional_experiment_promotion_does_not_require_receipts() -> None:
    record = valid_records()[6]
    assert errors(record) == []
    assert errors({**record, "promotion_decision": "promote_to_canon"})
    assert errors(
        {
            **record,
            "promotion_decision": "promote_to_canon",
            "decision_receipt_id": "decision-1",
            "canon_entry_id": "canon-1",
        }
    ) == []
