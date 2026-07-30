from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/learn-from-choices/SKILL.md"
ROUTE = ROOT / "skills/learn-from-choices/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/learn-from-choices/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/learn-from-choices/agents/openai.yaml"
CALIBRATION = ROOT / "docs/learn-from-choices-calibration-pilot-2026-07-30.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_skill_is_implicit_cataloged_and_discoverable():
    _, raw, _ = read(CANONICAL).split("---", 2)
    metadata = yaml.safe_load(raw)
    assert metadata["name"] == "learn-from-choices"
    assert "every final response" in metadata["description"]
    assert "[learn-from-choices](learn-from-choices/SKILL.md)" in read(
        ROOT / "skills/README.md"
    )
    for path in (ROUTE, ADAPTER_ROUTE):
        route = yaml.safe_load(read(path))
        assert route["interface"]["display_name"] == "Learn From Choices"
        assert route["policy"]["allow_implicit_invocation"] is True
    assert "../../../skills/learn-from-choices/SKILL.md" in read(ADAPTER)


def test_universal_contract_separates_navigation_from_execution():
    agents = read(ROOT / "AGENTS.md")
    skill = read(CANONICAL)
    for phrase in (
        "every final user-facing response",
        "three or four",
        "credible overlooked path",
        "does not authorize mutation",
        "A later explicit command supersedes",
    ):
        assert phrase.lower() in (agents + skill).lower()
    assert "Do not store an unselected footer" in skill
    assert "Repeated selection alone never changes ordering" in skill
    assert "Never promote a repository learning automatically" in skill
    assert "If the private ledger is unavailable, continue navigation" in skill


def test_composition_and_coffee_only_followup_contract():
    coffee = read(ROOT / "skills/coffee/SKILL.md")
    elicitation = read(ROOT / "skills/elicitation/SKILL.md")
    bravo = read(ROOT / "skills/bravo/SKILL.md")
    friction = read(ROOT / "skills/friction/SKILL.md")
    dream = read(ROOT / "skills/dream/SKILL.md")
    assert "learn-from-choices" in coffee
    assert "learn-from-choices" in elicitation
    assert "outcome_recorded" in bravo
    assert "outcome_recorded" in friction
    assert "at most one lightweight outcome-review branch" in coffee
    assert "unresolved choice" not in dream.lower()
    assert "A bare letter does not authorize mutation" in coffee


def test_active_calibration_freezes_outcome_informed_reordering():
    skill = read(CANONICAL)
    calibration = read(CALIBRATION)
    assert "../../docs/learn-from-choices-calibration-pilot-2026-07-30.md" in skill
    assert "recommendation ordering remains frozen" in skill
    assert "2026-07-30 through 2026-08-05" in skill
    for phrase in (
        "Status: `Conditional lifecycle — see Activation state`",
        "Hold — repository persistence",
        "Approved for pilot — activation scheduled",
        "Active — Phase 1",
        "Pilot route: `manual workflow`",
        "Automation involved: `no`",
        "Activation confirmed: `yes` only after repository persistence",
        "Authority effect of every selection: `none`",
        "Do not reorder, favor, or demote options using pilot outcomes",
        "LFC-CAL-2026-07-30-01` to `learning_refs",
        "Exclude an untagged selection from the pilot cohort",
        "At most 1 per 5 resolved choices",
        "Do not silently extend it",
    ):
        assert phrase.lower() in calibration.lower()
    assert "LFC-CAL-2026-07-30-01` in `learning_refs" in skill
    assert "`diagnostic-only` guidance" in skill
