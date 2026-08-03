from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
CANONICAL = ROOT / "skills/game-design/SKILL.md"
REFERENCES = ROOT / "skills/game-design/references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split())


def test_game_design_is_canonical_cataloged_and_discoverable():
    _, raw, _ = read(CANONICAL).split("---", 2)
    metadata = yaml.safe_load(raw)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "game-design"
    assert "apprenticeship" in metadata["description"]
    assert "[game-design](game-design/SKILL.md)" in read(ROOT / "skills/README.md")

    routes = (
        ROOT / "skills/game-design/agents/openai.yaml",
        ROOT / ".agents/skills/game-design/agents/openai.yaml",
        WORKSPACE / ".codex/skills/game-design/agents/openai.yaml",
    )
    for path in routes:
        route = yaml.safe_load(read(path))
        assert route["interface"] == {
            "display_name": "Game Design",
            "short_description": "Learn, design, prototype, and critique games",
            "default_prompt": "Use $game-design to teach one useful design concept and help me test it through the smallest meaningful exercise.",
        }
        assert route["policy"]["allow_implicit_invocation"] is True

    assert "../../../skills/game-design/SKILL.md" in read(
        ROOT / ".agents/skills/game-design/SKILL.md"
    )
    assert "../../../operating-substrate/skills/game-design/SKILL.md" in read(
        WORKSPACE / ".codex/skills/game-design/SKILL.md"
    )


def test_game_design_preserves_apprentice_authorship_and_action_boundaries():
    skill = normalized(CANONICAL)
    for phrase in (
        "Robert is the aspiring designer and creative authority",
        "Lack of prior training does not reduce his creative authority",
        "strengthen Robert's judgment rather than substitute for it",
        "Do not reward agreement",
        "Do not claim that a design is fun",
        "Do not turn conceptual clarity into implementation authority",
        "Retain no lesson without an explicit, separately authorized action",
    ):
        assert phrase.lower() in skill.lower()


def test_game_design_uses_bounded_modes_and_evidence_states():
    skill = read(CANONICAL)
    for mode in ("learn", "explore", "design", "critique", "prototype", "playtest", "reflect"):
        assert f"`{mode}`" in skill
    for state in (
        "principle",
        "hypothesis",
        "Robert preference",
        "prototype observation",
        "playtest pattern",
        "candidate lesson",
        "accepted lesson",
        "hold",
    ):
        assert f"`{state}`" in skill
    assert "smallest useful prototype" in skill
    assert "One play session is a case" in skill


def test_game_design_references_are_complete_and_selective():
    skill = read(CANONICAL)
    names = (
        "design-foundations.md",
        "exercise-patterns.md",
        "critique-method.md",
        "systems-design.md",
        "evaluation-rubric.md",
    )
    for name in names:
        path = REFERENCES / name
        assert path.is_file()
        assert f"references/{name}" in skill

    foundations = read(REFERENCES / "design-foundations.md")
    exercises = read(REFERENCES / "exercise-patterns.md")
    critique = read(REFERENCES / "critique-method.md")
    systems = read(REFERENCES / "systems-design.md")
    systems_normalized = normalized(REFERENCES / "systems-design.md")
    rubric = read(REFERENCES / "evaluation-rubric.md")
    assert "meaningful choice" in foundations.lower()
    assert "Three mechanic alternatives" in exercises
    assert "Causal system sketch" in exercises
    assert "Trace the causal chain" in critique
    assert "two or more mechanics interact" in systems
    assert "intended player experience in Robert's words" in systems
    assert "manual turns" in systems
    assert "hypothesis" in systems
    assert "prototype observation" in systems
    assert "playtest pattern" in systems
    assert "does not select the intended player experience" in systems_normalized
    assert "authorize implementation" in systems_normalized
    assert "Evaluate the agent, not Robert" in rubric
    assert "Do not collapse the dimensions" in rubric
    assert "selection frequency is not evidence" in rubric.lower()


def test_game_design_routes_systems_reasoning_without_a_new_mode_or_skill():
    skill = read(CANONICAL)
    skill_normalized = normalized(CANONICAL)
    systems = read(REFERENCES / "systems-design.md")
    exercises = read(REFERENCES / "exercise-patterns.md")
    exercises_normalized = normalized(REFERENCES / "exercise-patterns.md")

    assert "references/systems-design.md" in skill
    for trigger in (
        "persistent state",
        "emergence",
        "economies",
        "social networks",
        "institutions",
        "populations",
        "simulation granularity",
    ):
        assert trigger in skill_normalized
    assert "- `systems`:" not in skill
    assert "name: systems-design" not in systems
    assert "Game Design decides whether" in systems
    assert "System Engineering action" in systems
    for outcome in (
        "reinforcing loop",
        "balancing force",
        "failure risk",
        "unknown",
    ):
        assert outcome in exercises
    for player_decision_guardrail in (
        "player-facing manual run",
        "what the player knows",
        "materially different alternatives",
        "the selected action",
        "why no alternative universally dominates",
    ):
        assert player_decision_guardrail in exercises_normalized


def test_game_design_privacy_and_integrity_fail_closed():
    skill = normalized(CANONICAL)
    rubric = normalized(REFERENCES / "evaluation-rubric.md")
    for phrase in (
        "Do not automatically retain recordings",
        "Child-facing work remains on hold",
        "Persist it only through a separately selected action",
        "customer, family, learner, property, community, and other lane-specific facts do not cross",
    ):
        assert phrase.lower() in skill.lower()
    assert "failure produces `hold` regardless of other ratings" in rubric.lower()
