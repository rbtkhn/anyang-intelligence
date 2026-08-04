from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
CANONICAL = ROOT / "skills/decision-audit/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split()).lower()


def test_decision_audit_is_canonically_packaged_and_discoverable():
    _, raw, _ = read(CANONICAL).split("---", 2)
    metadata = yaml.safe_load(raw)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "decision-audit"
    for trigger in ("decision audits", "assumption reviews", "pre-commit"):
        assert trigger in metadata["description"]
    assert "[decision-audit](decision-audit/SKILL.md)" in read(ROOT / "skills/README.md")

    expected_interface = {
        "display_name": "Decision Audit",
        "short_description": "Surface consequential uncertain agent decisions",
        "default_prompt": (
            "Use $decision-audit to surface consequential decisions the agent made "
            "that still need evidence or human review."
        ),
    }
    routes = (
        ROOT / "skills/decision-audit/agents/openai.yaml",
        ROOT / ".agents/skills/decision-audit/agents/openai.yaml",
        WORKSPACE / ".codex/skills/decision-audit/agents/openai.yaml",
    )
    for path in routes:
        route = yaml.safe_load(read(path))
        assert route["interface"] == expected_interface
        assert route["policy"]["allow_implicit_invocation"] is True

    assert "../../../skills/decision-audit/SKILL.md" in read(
        ROOT / ".agents/skills/decision-audit/SKILL.md"
    )
    assert "../../../operating-substrate/skills/decision-audit/SKILL.md" in read(
        WORKSPACE / ".codex/skills/decision-audit/SKILL.md"
    )


def test_decision_audit_is_sparse_evidence_aware_and_read_only():
    skill = normalized(CANONICAL)
    for phrase in (
        "the agent selected among plausible alternatives",
        "materially affects architecture",
        "outcome-supported",
        "structurally supported",
        "missing",
        "return no more than three findings",
        "no material uncertain agent decision found",
        "persist nothing automatically",
        "it changes no ledger, claim, transaction, approval, or repository state",
    ):
        assert phrase in skill

    for excluded in (
        "mechanical or stylistic choices",
        "decisions explicitly made by the operator",
        "unselected possibilities",
        "reversible implementation details already bounded by tests",
    ):
        assert excluded in skill


def test_historical_replay_and_state_labels_do_not_overclaim():
    skill = normalized(CANONICAL)
    for phrase in (
        "treat git-only reconstruction as incomplete",
        "reveal a candidate decision",
        "can establish that the agent made it",
        "validated`, `approved`, `complete`, or `authorized`",
        "do not call validator success outcome evidence",
    ):
        assert phrase in skill


def test_dream_composition_is_conditional_skill_layer_only():
    skill = normalized(CANONICAL)
    dream = normalized(ROOT / "skills/dream/SKILL.md")
    dream_runtime = normalized(ROOT / "cli/anyang_loop/dream.py")

    for phrase in (
        "show at most the highest-priority finding",
        "omit the section entirely",
        "keep dream's deterministic cli and json unchanged",
        "out of the external cadence handoff",
        "do not print a no-findings placeholder",
        "must not displace a higher-priority closeout issue",
    ):
        assert phrase in skill or phrase in dream

    assert "decision-audit" in dream
    assert "current-session evidence" in dream
    assert "decision uncertainty" in dream
    assert "decision_audit" not in dream_runtime


def test_discovery_adapters_add_no_authority_or_behavior():
    for adapter in (
        ROOT / ".agents/skills/decision-audit/SKILL.md",
        WORKSPACE / ".codex/skills/decision-audit/SKILL.md",
    ):
        text = normalized(adapter)
        assert "discovery-only" in text
        assert "adds no behavior" in text
        assert "persistence" in text
        assert "execution authority" in text
