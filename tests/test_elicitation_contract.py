from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from anyang_loop.choice_learning import (
    choice_projection,
    interpret_elicitation_response,
    record_choice_event,
    record_choice_selection,
    validate_elicitation_surface,
)
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_service import OpsError, add_actor, init_tenant


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
NOW = "2026-07-30T12:00:00Z"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def decision_options() -> list[dict[str, str]]:
    return [
        {
            "key": "inspect",
            "role": "recommended",
            "label": "Inspect the focused diff",
        },
        {
            "key": "push",
            "role": "alternative",
            "label": "Push the focused commit",
        },
        {
            "key": "review-push",
            "role": "overlooked",
            "label": "Review and push after portability repair",
        },
        {
            "key": "pause",
            "role": "pause-or-deepen",
            "label": "Pause and preserve optionality",
        },
    ]


def ledger_packet(identifier: str, actor: str, selected: str) -> dict:
    options = [
        {
            **option,
            "tradeoff": f"Tradeoff for {option['key']}",
            "expected_outcome": f"Outcome for {option['key']}",
            "risk": f"Risk for {option['key']}",
            "learning_refs": ["LFC-CAL-2026-07-30-01"],
        }
        for option in decision_options()
    ]
    return {
        "id": identifier,
        "workspace_id": "anyang-intelligence",
        "lane": "repository",
        "choice_kind": "next-action",
        "consequence_level": "ordinary",
        "decision_summary": "Choose ordered Elicitation branches",
        "options": options,
        "recommendation_key": "inspect",
        "selected_option_key": selected,
        "learning_refs": ["LFC-CAL-2026-07-30-01"],
        "learning_context": {"contract": "elicitation-continuity-v1"},
        "success_signal": "Each branch has an independent receipt",
        "risk_signal": "One selection silently authorizes another",
        "selected_by": "Council Steward",
        "actor_id": actor,
        "presented_at": NOW,
        "selected_at": NOW,
        "review_after": "2026-08-01T12:00:00Z",
        "recorded_at": NOW,
        "source_ref": "repo:skills/elicitation/SKILL.md",
    }


def outcome_packet(event_key: str, result: str) -> dict:
    return {
        "event_key": event_key,
        "event_type": "outcome_recorded",
        "recorded_by": "Council Steward",
        "action_summary": "Record branch-specific result",
        "evidence_ref": f"repo:test/{event_key}",
        "occurred_at": NOW,
        "recorded_at": NOW,
        "payload": {
            "result": result,
            "cognitive_load": "Missing",
            "momentum": "Missing",
            "discovery_value": "Missing",
            "observation": "Synthetic contract evidence",
            "authority_issue": False,
            "membrane_issue": False,
        },
    }


def test_elicitation_is_discoverable_and_implicitly_bounded():
    canonical = ROOT / "skills/elicitation/SKILL.md"
    route = ROOT / "skills/elicitation/agents/openai.yaml"
    adapter = ROOT / ".agents/skills/elicitation/SKILL.md"
    adapter_route = ROOT / ".agents/skills/elicitation/agents/openai.yaml"
    workspace_adapter = WORKSPACE / ".codex/skills/elicitation/SKILL.md"
    workspace_route = WORKSPACE / ".codex/skills/elicitation/agents/openai.yaml"

    metadata = yaml.safe_load(read(canonical).split("---", 2)[1])
    assert metadata["name"] == "elicitation"
    assert "genuinely missing, materially consequential" in metadata["description"]
    assert "[elicitation](elicitation/SKILL.md)" in read(ROOT / "skills/README.md")

    for path in (route, adapter_route):
        value = yaml.safe_load(read(path))
        assert value["policy"]["allow_implicit_invocation"] is True
        assert value["interface"]["display_name"] == "Elicitation"
    assert "../../../skills/elicitation/SKILL.md" in read(adapter)
    if workspace_adapter.exists() and workspace_route.exists():
        value = yaml.safe_load(read(workspace_route))
        assert value["policy"]["allow_implicit_invocation"] is True
        assert value["interface"]["display_name"] == "Elicitation"
        assert "../../../operating-substrate/skills/elicitation/SKILL.md" in read(
            workspace_adapter
        )


def test_decision_and_neutral_surfaces_have_distinct_nonleading_shapes():
    decision = validate_elicitation_surface(
        {
            "interaction_type": "decision-navigation",
            "question": "What should happen next?",
            "options": decision_options(),
        }
    )
    assert len(decision["options"]) == 4
    assert decision["authority_effect"] == "none"

    neutral = validate_elicitation_surface(
        {
            "interaction_type": "neutral-evidence",
            "question": "Which environment produced the receipt?",
            "options": [
                {"key": "local", "label": "Local workspace"},
                {"key": "ci", "label": "Continuous integration"},
            ],
        }
    )
    assert all("role" not in option for option in neutral["options"])
    with pytest.raises(OpsError, match="requires 3-4"):
        validate_elicitation_surface(
            {
                "interaction_type": "decision-navigation",
                "question": "Too few branches?",
                "options": decision_options()[:2],
            }
        )
    with pytest.raises(OpsError, match="recommendation roles"):
        validate_elicitation_surface(
            {
                "interaction_type": "neutral-evidence",
                "question": "Which factual state?",
                "options": decision_options()[:2],
            }
        )


def test_single_compound_and_ranked_response_semantics():
    exploratory = interpret_elicitation_response(decision_options(), "a")
    assert exploratory["mode"] == "single"
    assert exploratory["receipt_count"] == 1
    assert exploratory["selected_branches"][0]["option_key"] == "inspect"
    assert (
        exploratory["selected_branches"][0]["action_authorization"]["authorized"]
        is False
    )

    action = interpret_elicitation_response(decision_options(), "B")
    assert action["selected_branches"][0]["action_authorization"] == {
        "authorized": True,
        "verb": "Push",
        "bounded_action": "Push the focused commit",
    }
    disguised_action = interpret_elicitation_response(decision_options(), "C")
    assert (
        disguised_action["selected_branches"][0]["action_authorization"]["authorized"]
        is False
    )

    compound = interpret_elicitation_response(decision_options(), "A,C")
    assert compound["mode"] == "compound"
    assert [branch["letter"] for branch in compound["selected_branches"]] == [
        "A",
        "C",
    ]
    assert compound["receipt_count"] == 2
    assert compound["shared_option_set_identity"] is True
    assert compound["stop_on_failure"] is True
    assert compound["authority_effect"] == "none"

    ranked = interpret_elicitation_response(decision_options(), "A>C>B")
    assert ranked["mode"] == "ranked"
    assert ranked["selected_branches"] == []
    assert ranked["receipt_count"] == 0
    assert ranked["execute_nothing"] is True
    assert ranked["top_preference"]["option_key"] == "inspect"


@pytest.mark.parametrize(
    ("label", "verb"),
    [
        ("execute the bounded repair", "Execute"),
        ("COMMIT: the focused files", "Commit"),
        ("push—the verified commit", "Push"),
        ("Send the approved message", "Send"),
    ],
)
def test_reserved_action_verbs_are_case_insensitive_first_tokens(label, verb):
    options = decision_options()
    options[0]["label"] = label
    result = interpret_elicitation_response(options, "A")
    assert result["selected_branches"][0]["action_authorization"]["verb"] == verb


@pytest.mark.parametrize("response", ["A,A", "A,Z", "A,D", "A,C>B"])
def test_invalid_compound_responses_fail_closed(response):
    with pytest.raises(OpsError):
        interpret_elicitation_response(decision_options(), response)


def test_compound_selection_uses_separate_schema_v8_receipts(tmp_path):
    connection = connect(tmp_path / "elicitation.db", create_parent=True)
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
        record_choice_selection(
            connection,
            "anyang-internal",
            ledger_packet("ELICITATION-COMPOUND-A", actor, "inspect"),
        )
        record_choice_selection(
            connection,
            "anyang-internal",
            ledger_packet("ELICITATION-COMPOUND-C", actor, "review-push"),
        )
        first = choice_projection(connection, "ELICITATION-COMPOUND-A")
        second = choice_projection(connection, "ELICITATION-COMPOUND-C")
        assert schema_version(connection) == SCHEMA_VERSION == 8
        assert (
            first["lineage"]["option_set_hash"]
            == second["lineage"]["option_set_hash"]
        )
        assert first["choice"]["presented_at"] == second["choice"]["presented_at"]
        assert first["lineage"]["authority_effect"] == "none"
        assert second["lineage"]["authority_effect"] == "none"

        record_choice_event(
            connection,
            "ELICITATION-COMPOUND-A",
            outcome_packet("branch-a", "successful"),
        )
        record_choice_event(
            connection,
            "ELICITATION-COMPOUND-C",
            outcome_packet("branch-c", "mixed"),
        )
        assert choice_projection(connection, "ELICITATION-COMPOUND-A")[
            "current_state"
        ] == "outcome_observed"
        assert choice_projection(connection, "ELICITATION-COMPOUND-C")[
            "current_state"
        ] == "outcome_observed"
    finally:
        connection.close()


def test_contract_removes_high_burden_and_authority_contradictions():
    skill = read(ROOT / "skills/elicitation/SKILL.md")
    for phrase in (
        "Present 3-4 genuinely different",
        "Present 2-4 mutually exclusive factual answers",
        "`A,C` selects both branches",
        "`A>C>B` records preference order only",
        "first token",
        "`Review and push the focused commit` remains exploratory",
        "`authority_effect: none`",
        "batches of 1-3 questions",
        "at most ten questions total",
        "ask one blocking question at a time",
        "Stop the current and remaining batches immediately",
        "Do not present a monolithic ten-question form",
    ):
        assert phrase.lower() in skill.lower()
    assert "Offer 3-5 distinct options" not in skill
    assert "10-Question Intake" not in skill


def test_contradiction_preflight_routes_before_consequential_questions():
    skill = read(ROOT / "skills/elicitation/SKILL.md")
    agents = read(ROOT / "AGENTS.md")
    cli = read(ROOT / "cli/README.md")
    normalized = " ".join(skill.split())

    assert normalized.index("After intent recovery and before asking") < normalized.index(
        "For decision menus and final-response possibility maps"
    )
    for phrase in (
        "smallest relevant controlling surface",
        "never ask the checker to search prose or decide which source governs",
        "Route missing or stale facts to neutral evidence intake",
        "Route one request-versus-control conflict to decision navigation",
        "Hold conflicting controlling sources for named authority resolution",
        "`authority_effect: none`",
        "never changes a repository fact",
        "exact menu selections",
        "ordinary missing preferences",
    ):
        assert phrase.lower() in normalized.lower()
    assert "structured contradiction preflight" in agents
    assert "project contradiction-check --packet" in cli
    assert "does not search prose, open SQLite, write files" in cli
