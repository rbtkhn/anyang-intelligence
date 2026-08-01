from __future__ import annotations

from pathlib import Path

import yaml

from anyang_loop.choice_continuity import configure_choice_continuity
from anyang_loop.coffee import build_coffee_data, render_coffee_text
from anyang_loop.ops_db import connect
from anyang_loop.ops_service import tenant_id

from cadence_helpers import make_git_repo, write


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


DASHBOARD = """# Operating Portfolio Dashboard

## Active Obligations

### Media Production

- Operate the approved service package.

## Portfolio Rule

Current priority order:

1. Serve Media Production.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def selection(choice_id: str, actor_id: str) -> dict:
    options = [
        {
            "key": "inspect",
            "role": "recommended",
            "label": "Inspect the bounded continuity slice",
            "tradeoff": "Read-only investigation costs a small amount of time.",
            "expected_outcome": "The next branch is evidence-grounded.",
            "risk": "The inspection may reveal no new issue.",
            "learning_refs": ["LFC-CAL-2026-07-30-01"],
        },
        {
            "key": "alternate",
            "role": "alternative",
            "label": "Review a different operating objective",
            "tradeoff": "The continuity slice waits.",
            "expected_outcome": "A different objective receives attention.",
            "risk": "Current continuity evidence may become stale.",
            "learning_refs": ["LFC-CAL-2026-07-30-01"],
        },
        {
            "key": "overlooked",
            "role": "overlooked",
            "label": "Test an overlooked continuity seam",
            "tradeoff": "The path is less certain.",
            "expected_outcome": "A useful unseen path may emerge.",
            "risk": "The path may not be useful.",
            "learning_refs": ["LFC-CAL-2026-07-30-01"],
        },
        {
            "key": "pause",
            "role": "pause-or-deepen",
            "label": "Pause with state preserved",
            "tradeoff": "Momentum pauses.",
            "expected_outcome": "Optionality remains intact.",
            "risk": "The outcome remains unresolved.",
            "learning_refs": ["LFC-CAL-2026-07-30-01"],
        },
    ]
    return {
        "id": choice_id,
        "workspace_id": "anyang-intelligence",
        "lane": "repository",
        "choice_kind": "next-action",
        "consequence_level": "ordinary",
        "decision_summary": "Choose the next continuity branch",
        "options": options,
        "recommendation_key": "inspect",
        "selected_option_key": "inspect",
        "learning_refs": ["LFC-CAL-2026-07-30-01"],
        "learning_context": {"contract": "coffee-continuity"},
        "success_signal": "Continuity is easier to reconstruct.",
        "risk_signal": "Selection retention silently fails.",
        "selected_by": "Council Steward",
        "actor_id": actor_id,
        "presented_at": "2026-07-31T12:00:00Z",
        "selected_at": "2026-07-31T12:00:00Z",
        "review_after": "2026-07-31T12:00:00Z",
        "recorded_at": "2026-07-31T12:00:00Z",
        "source_ref": "repo:skills/coffee/SKILL.md",
    }


def boundary_outcome() -> dict:
    return {
        "event_key": "coffee-boundary-outcome",
        "event_type": "outcome_recorded",
        "recorded_by": "Council Steward",
        "action_summary": "Record the bounded continuity outcome",
        "evidence_ref": "repo:test/coffee-boundary-outcome",
        "occurred_at": "2026-07-31T13:00:00Z",
        "recorded_at": "2026-07-31T13:00:00Z",
        "payload": {
            "result": "mixed",
            "cognitive_load": "same",
            "momentum": "neutral",
            "discovery_value": "confirmed-known-path",
            "observation": "Synthetic boundary guardrail",
            "authority_issue": True,
            "membrane_issue": False,
        },
    }


def test_coffee_is_canonically_packaged_and_discoverable():
    canonical = ROOT / "skills/coffee/SKILL.md"
    route = ROOT / "skills/coffee/agents/openai.yaml"
    adapter = ROOT / ".agents/skills/coffee/SKILL.md"
    adapter_route = ROOT / ".agents/skills/coffee/agents/openai.yaml"
    workspace_adapter = WORKSPACE / ".codex/skills/coffee/SKILL.md"
    workspace_route = WORKSPACE / ".codex/skills/coffee/agents/openai.yaml"

    metadata = yaml.safe_load(read(canonical).split("---", 2)[1])
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "coffee"
    for path in (route, adapter_route, workspace_route):
        value = yaml.safe_load(read(path))
        assert value["interface"] == {
            "display_name": "Coffee",
            "short_description": "Restore context and choose the next move",
            "default_prompt": "Use $coffee to restore operating context and choose the next bounded move.",
        }
        assert value["policy"]["allow_implicit_invocation"] is True
    assert "../../../skills/coffee/SKILL.md" in read(adapter)
    assert "../../../operating-substrate/skills/coffee/SKILL.md" in read(workspace_adapter)


def test_ready_coffee_reads_only_guardrails_without_writing_database(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    make_git_repo(repo, DASHBOARD)
    write(repo / "skills" / "README.md", "# Skills\n\n- coffee\n")
    config_home = tmp_path / "config"
    monkeypatch.setenv("ANYANG_CONFIG_HOME", str(config_home))
    data_dir = tmp_path / "private"
    configure_choice_continuity(data_dir, repo)
    database = data_dir / "anyang-ops.db"

    from anyang_loop.choice_learning import record_choice_event, record_choice_selection

    with connect(database) as connection:
        tid = tenant_id(connection, "anyang-internal")
        actor = connection.execute(
            "SELECT id FROM actor WHERE tenant_id = ? AND name = 'Council Steward'", (tid,)
        ).fetchone()["id"]
        record_choice_selection(connection, "anyang-internal", selection("COFFEE-DUE", actor))

    before = database.read_bytes()
    modified = database.stat().st_mtime_ns

    def reject_learning_review(*args, **kwargs):
        raise AssertionError("Coffee must not inspect choice context or unresolved reviews")

    monkeypatch.setattr("anyang_loop.choice_continuity.choice_context", reject_learning_review)
    monkeypatch.setattr("anyang_loop.choice_continuity.choice_review", reject_learning_review)
    result = build_coffee_data(repo)
    assert result["schema_version"] == 2
    assert result["choice_continuity"]["status"] == "ready"
    assert result["choice_continuity"]["due_count"] == 0
    assert result["choice_continuity"]["ordering_frozen"] is True
    assert result["menu"][3].startswith("D. Pause")
    assert "outcome" not in result["menu"][3].lower()
    assert len(result["menu"]) == 4
    rendered = render_coffee_text(result)
    assert "Choice continuity:" in rendered
    assert "due outcome" not in rendered.lower()
    assert database.read_bytes() == before
    assert database.stat().st_mtime_ns == modified

    with connect(database) as connection:
        record_choice_event(connection, "COFFEE-DUE", boundary_outcome())
    after_outcome = database.read_bytes()
    outcome_modified = database.stat().st_mtime_ns
    guarded = build_coffee_data(repo)
    assert guarded["decision_reason"] == "choice-boundary-guardrail"
    assert len(guarded["choice_continuity"]["guardrails"]) == 1
    assert guarded["choice_continuity"]["due_count"] == 0
    assert database.read_bytes() == after_outcome
    assert database.stat().st_mtime_ns == outcome_modified


def test_unconfigured_coffee_has_honest_git_only_fallback(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    make_git_repo(repo, DASHBOARD)
    result = build_coffee_data(repo)
    assert result["choice_continuity"]["status"] == "unconfigured"
    assert result["choice_continuity"]["retention_available"] is False
    assert "git-only fallback" in result["current_picture"]
    assert len(result["menu"]) == 4
