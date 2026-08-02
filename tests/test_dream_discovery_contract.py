from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
CANONICAL = ROOT / "skills/dream/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split())


def test_dream_is_canonically_packaged_and_discoverable():
    _, raw, _ = read(CANONICAL).split("---", 2)
    metadata = yaml.safe_load(raw)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "dream"
    for trigger in ("dream", "day close", "closeout", "night review"):
        assert trigger in metadata["description"]
    assert "[dream](dream/SKILL.md)" in read(ROOT / "skills/README.md")

    expected_interface = {
        "display_name": "Dream",
        "short_description": "Settle the work cycle and preserve tomorrow",
        "default_prompt": "Use $dream to verify what landed, preserve boundaries, and name what tomorrow inherits.",
    }
    routes = (
        ROOT / "skills/dream/agents/openai.yaml",
        ROOT / ".agents/skills/dream/agents/openai.yaml",
        WORKSPACE / ".codex/skills/dream/agents/openai.yaml",
    )
    for path in routes:
        route = yaml.safe_load(read(path))
        assert route["interface"] == expected_interface
        assert route["policy"]["allow_implicit_invocation"] is True

    assert "../../../skills/dream/SKILL.md" in read(
        ROOT / ".agents/skills/dream/SKILL.md"
    )
    assert "../../../operating-substrate/skills/dream/SKILL.md" in read(
        WORKSPACE / ".codex/skills/dream/SKILL.md"
    )


def test_dream_discovery_preserves_read_only_closeout_boundaries():
    skill = normalized(CANONICAL).lower()
    for phrase in (
        "it remains read-only unless the operator explicitly passes `--record`",
        "do not edit, stage, commit, or push by default",
        "without creating autonomous merge authority",
        "cadence handoffs are repository-level coordination records",
    ):
        assert phrase in skill

    for adapter in (
        ROOT / ".agents/skills/dream/SKILL.md",
        WORKSPACE / ".codex/skills/dream/SKILL.md",
    ):
        text = normalized(adapter).lower()
        assert "discovery-only" in text
        assert "adds no behavior" in text
        assert "execution authority" in text
