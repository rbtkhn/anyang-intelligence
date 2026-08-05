from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
CANONICAL = ROOT / "skills/pattern-memory/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split()).lower()


def test_pattern_memory_is_canonical_cataloged_and_discoverable() -> None:
    _, raw, _ = read(CANONICAL).split("---", 2)
    metadata = yaml.safe_load(raw)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "pattern-memory"
    for trigger in ("pattern-memory", "what anyang has learned", "cross-project patterns"):
        assert trigger in metadata["description"].lower()
    assert "[pattern-memory](pattern-memory/SKILL.md)" in read(ROOT / "skills/README.md")

    expected_interface = {
        "display_name": "Governed Pattern Memory",
        "short_description": "Find reusable patterns with provenance",
        "default_prompt": "Use $pattern-memory to find governed reusable patterns for this task.",
    }
    routes = (
        ROOT / "skills/pattern-memory/agents/openai.yaml",
        ROOT / ".agents/skills/pattern-memory/agents/openai.yaml",
        WORKSPACE / ".codex/skills/pattern-memory/agents/openai.yaml",
    )
    for path in routes:
        route = yaml.safe_load(read(path))
        assert route["interface"] == expected_interface
        assert route["policy"]["allow_implicit_invocation"] is True

    assert "../../../skills/pattern-memory/SKILL.md" in read(
        ROOT / ".agents/skills/pattern-memory/SKILL.md"
    )
    assert "../../../operating-substrate/skills/pattern-memory/SKILL.md" in read(
        WORKSPACE / ".codex/skills/pattern-memory/SKILL.md"
    )


def test_pattern_memory_skill_preserves_shadow_and_promotion_boundaries() -> None:
    skill = normalized(CANONICAL)
    for phrase in (
        "retrieval is not retention",
        "authority_effect` is `none",
        "project-provisional",
        "do not create or update an `rl-*` entry",
        "do not represent structural or replay success as human usefulness",
        "do not use `--force` unless the operator explicitly authorizes",
        "no durable state or execution authority changed",
    ):
        assert phrase in skill

    for adapter in (
        ROOT / ".agents/skills/pattern-memory/SKILL.md",
        WORKSPACE / ".codex/skills/pattern-memory/SKILL.md",
    ):
        text = normalized(adapter)
        assert "discovery-only" in text
        assert "adds no behavior" in text
        assert "memory-promotion" in text
        assert "execution authority" in text


def test_pattern_memory_skill_reuses_canonical_cli_and_rfc() -> None:
    skill = read(CANONICAL)
    assert "../../docs/governed-pattern-memory-v1.md" in skill
    assert ".\\tools\\run.ps1 project pattern-memory query" in skill
    assert "generated-patterns/" in skill
    assert not (ROOT / "skills/pattern-memory/scripts").exists()
    assert not (ROOT / "skills/pattern-memory/references").exists()
