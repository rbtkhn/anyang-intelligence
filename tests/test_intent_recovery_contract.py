from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/intent-recovery/SKILL.md"
ROUTE = ROOT / "skills/intent-recovery/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/intent-recovery/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/intent-recovery/agents/openai.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def frontmatter(path: Path) -> dict:
    _, raw, _ = read(path).split("---", 2)
    return yaml.safe_load(raw)


def test_intent_recovery_is_cataloged_discoverable_and_explicit_only():
    metadata = frontmatter(CANONICAL)
    catalog = read(ROOT / "skills/README.md")

    assert metadata["name"] == "intent-recovery"
    assert "$intent-recovery" in metadata["description"]
    assert "[intent-recovery](intent-recovery/SKILL.md)" in catalog

    for route_path in (ROUTE, ADAPTER_ROUTE):
        route = yaml.safe_load(read(route_path))
        assert route["interface"]["display_name"] == "Intent Recovery"
        assert route["interface"]["short_description"] == "Recover and clarify the operator's underlying intent"
        assert "$intent-recovery" in route["interface"]["default_prompt"]
        assert route["policy"]["allow_implicit_invocation"] is False

    adapter = read(ADAPTER)
    assert "skills/intent-recovery/SKILL.md" in adapter
    assert "Do not recover intent from this adapter alone" in adapter


def test_intent_recovery_separates_interpretation_from_action():
    skill = read(CANONICAL)

    for output_field in (
        "What you said:",
        "What I think you mean:",
        "Clearer articulation:",
        "Practical implication:",
        "Uncertainty:",
    ):
        assert output_field in skill

    assert "Treat recovered intent as inference, not fact" in skill
    assert "Intent recovery is interpretive preparation. It is never approval to execute." in skill
    assert "Do not diagnose psychology" in skill
    assert "Do not inflate every short message into a grand philosophy" in skill
    assert "Do not infer publication, spending, hiring, customer-contact, persistence, or source-change authority" in skill


def test_consequential_ambiguity_routes_to_elicitation():
    recovery = read(CANONICAL)
    elicitation = read(ROOT / "skills/elicitation/SKILL.md")

    assert "Route consequential ambiguity to [elicitation](../elicitation/SKILL.md) before action" in recovery
    assert "Low confidence or consequential action" in recovery
    assert "automatically read and follow the complete canonical [intent recovery](../intent-recovery/SKILL.md) contract" in elicitation
    assert "genuinely missing" in elicitation


def test_bounded_automatic_composition_covers_five_workflows():
    recovery = read(CANONICAL)
    elicitation = read(ROOT / "skills/elicitation/SKILL.md")
    bravo = read(ROOT / "skills/bravo/SKILL.md")
    friction = read(ROOT / "skills/friction/SKILL.md")
    intake = read(ROOT / "skills/business-intake/SKILL.md")
    thesis = read(ROOT / "docs/thesis.md")
    product = read(ROOT / "docs/product.md")

    for mode in ("Elicitation", "Bravo", "Friction", "Product doctrine", "Business intake"):
        assert f"**{mode}:**" in recovery

    assert "skills/intent-recovery/SKILL.md" in bravo
    assert "skills/intent-recovery/SKILL.md" in friction
    assert "skills/intent-recovery/SKILL.md" in intake
    assert "[intent recovery](../skills/intent-recovery/SKILL.md)" in thesis
    assert "[intent recovery](../skills/intent-recovery/SKILL.md)" in product
    assert "Recovered intent:" in elicitation + bravo + friction


def test_automatic_recovery_has_adaptive_receipts_and_skip_conditions():
    recovery = read(CANONICAL)

    assert "Use an adaptive receipt for high-confidence recovery" in recovery
    assert "Recovered intent: <one concise, clearly labeled inference>" in recovery
    for skip_condition in (
        "exact menu selections",
        "clear commands",
        "factual receipts",
        "explicit approvals",
        "genuinely missing evidence",
    ):
        assert skip_condition in recovery


def test_doctrine_and_business_modes_fail_closed():
    recovery = read(CANONICAL)
    thesis = read(ROOT / "docs/thesis.md")
    product = read(ROOT / "docs/product.md")
    intake = read(ROOT / "skills/business-intake/SKILL.md")

    for classification in ("`Vision`", "`Product Hypothesis`", "`Doctrine Candidate`", "`Approved Direction`"):
        assert classification in recovery
    assert "Never assign `Approved Direction` from interpretation alone" in recovery
    assert "until the operator explicitly approves both the direction and any repository edit" in thesis
    assert "is not an approved direction or authorization to edit this surface" in product

    assert "ask the owner to confirm or correct the articulation" in intake
    assert "Keep unconfirmed articulations out of completed packets" in intake
    assert "Never use recovered intent to supply economics, capacity, customer facts, private strategy, approval, or authority" in intake
