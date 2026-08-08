from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/learn-from-choices/SKILL.md"
ROUTE = ROOT / "skills/learn-from-choices/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/learn-from-choices/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/learn-from-choices/agents/openai.yaml"
CALIBRATION = ROOT / "docs/learn-from-choices-calibration-pilot-2026-07-30.md"
CONTINUITY = ROOT / "docs/learn-from-choices-continuity-contract-v0.3.md"
ACTIVE = ROOT / "docs/learn-from-choices-active-v1.md"
LITE = ROOT / "docs/learn-from-choices-lite-v1.md"


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
    normalized = " ".join(skill.split())
    for phrase in (
        "every final user-facing response",
        "three or four",
        "credible overlooked path",
        "A letter selects the displayed option",
        "authorizes only that named bounded action",
        "no broader or hidden authority",
    ):
        assert phrase.lower() in (agents + skill).lower()
    assert "Do not store an unselected footer" in skill
    assert "Repeated selection alone never changes ordering" in skill
    assert "Never promote a repository learning automatically" in normalized
    assert "Do not inspect `choice status`" in skill
    assert "ordinary selected" in skill.lower()
    assert "Persist nothing automatically" in skill
    assert "Execute retain this learning" in normalized


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
    assert "does not solicit unresolved choice outcomes" in coffee
    assert "unresolved choice" not in dream.lower()
    assert "select the displayed option" in coffee
    assert "binds its selected letter to that named bounded action" in " ".join(
        coffee.split()
    )


def test_calibration_is_append_only_disposed_into_active_v1():
    skill = read(CANONICAL)
    calibration = read(CALIBRATION)
    active = read(ACTIVE)
    normalized_calibration = " ".join(calibration.split()).lower()
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
        "Do not silently extend it",
        "Lite transition hold",
        "initial readiness status exposed zeroed learning counters",
        "configured ledger was populated",
        "interim operational hold",
        "Pilot status: `Too thin`",
        "Reviewer decision: `Revise`",
        "Learn From Choices Active v1",
    ):
        assert phrase.lower() in normalized_calibration
    assert "../../docs/learn-from-choices-active-v1.md" in skill
    assert "repository-governance-preflight-v1" in skill
    assert "same-task packet" in active
    assert "Ordinary navigation remains ephemeral" in active
    assert "Authority effect: `none`" in active


def test_lite_default_has_zero_automatic_choice_persistence():
    agents = read(ROOT / "AGENTS.md")
    skill = read(CANONICAL)
    lite = read(LITE)
    cli = read(ROOT / "cli/README.md")
    coffee = read(ROOT / "skills/coffee/SKILL.md")
    normalized_lite = " ".join(lite.split()).lower()
    for phrase in (
        "ordinary selection causes zero choice-ledger calls",
        "creates no selection packet or ledger receipt",
        "causes no retention warning",
        "No outcome or repository learning is persisted automatically",
        "SQLite remains schema v8",
        "advanced manual audit surface",
        "does not compute or display unresolved, due, or resolved choice counts",
    ):
        assert phrase.lower() in normalized_lite
    assert "ordinary selections perform no choice-ledger" in agents
    assert "Follow the versioned [Lite v1 contract]" in skill
    assert "No selection or outcome is persisted automatically" in cli
    assert "does not solicit unresolved choice outcomes" in coffee


def test_continuity_v03_contract_is_explicit_and_canonical():
    skill = read(CANONICAL)
    contract = read(CONTINUITY)
    cli = read(ROOT / "cli/README.md")
    assert "../../docs/learn-from-choices-continuity-contract-v0.3.md" in skill
    for phrase in (
        "schema-v8",
        "retained episode",
        "comparison context",
        "repository-authorized-push-v1",
        "diagnostic-only",
        "authority_effect: none",
        "selection frequency",
        "append-only compatibility",
        "repository-governance-preflight-v1",
        "90-day",
    ):
        assert phrase.lower() in contract.lower()
    assert "patterns are diagnostic" in skill.lower()
    assert "only valid explicit comparability policy keys create" in skill.lower()
    assert "SQLite remains schema v8" in cli
    assert "Selection dry runs validate structure" in cli


def test_active_v1_template_and_skill_retention_boundary():
    skill = read(CANONICAL)
    bravo = read(ROOT / "skills/bravo/SKILL.md")
    friction = read(ROOT / "skills/friction/SKILL.md")
    template = yaml.safe_load(read(ROOT / "templates/choice-retained-outcome.yaml"))
    assert "Execute retain this reviewed episode" in " ".join(skill.split())
    assert "Execute retain this reviewed episode" in " ".join(bravo.split())
    assert "Execute retain this reviewed episode" in " ".join(friction.split())
    assert template["schema"] == "anyang-choice-retained-outcome/v1"
    assert template["comparison_context"]["decision_seam"] == "pre-mutation-evidence-depth"
    assert template["retention"]["provenance_mode"] == "same-task-reviewed-reconstruction"
