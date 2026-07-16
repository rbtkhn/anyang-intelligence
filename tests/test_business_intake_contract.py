from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/business-intake/SKILL.md"
QUESTION_STRATEGY = ROOT / "skills/business-intake/references/question-strategy.md"
OUTPUT_CONTRACTS = ROOT / "skills/business-intake/references/output-contracts.md"
ROUTE = ROOT / "skills/business-intake/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/business-intake/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/business-intake/agents/openai.yaml"
GRACE_GEMS = ROOT / "projects/grace-gems/business-intake-survey.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def frontmatter(path: Path) -> dict:
    _, raw, _ = read(path).split("---", 2)
    return yaml.safe_load(raw)


def test_business_intake_is_cataloged_and_explicit_only():
    metadata = frontmatter(CANONICAL)
    assert metadata["name"] == "business-intake"
    assert "$business-intake create" in metadata["description"]
    assert "$business-intake change" in metadata["description"]

    catalog = read(ROOT / "skills/README.md")
    assert "[business-intake](business-intake/SKILL.md)" in catalog

    for route_path in (ROUTE, ADAPTER_ROUTE):
        route = yaml.safe_load(read(route_path))
        assert route["interface"]["display_name"] == "Business Intake"
        assert route["interface"]["short_description"] == "Govern owner-approved business intake"
        assert "$business-intake create" in route["interface"]["default_prompt"]
        assert route["policy"]["allow_implicit_invocation"] is False


def test_discovery_adapter_routes_to_the_complete_canonical_contract():
    adapter = read(ADAPTER)
    canonical = read(CANONICAL)

    assert "skills/business-intake/SKILL.md" in adapter
    assert "Do not conduct intake from this adapter alone" in adapter
    assert "references/question-strategy.md" in canonical
    assert "references/output-contracts.md" in canonical
    assert "projects/grace-gems/business-intake-survey.md" in canonical
    assert QUESTION_STRATEGY.is_file()
    assert OUTPUT_CONTRACTS.is_file()


def test_modes_states_and_persistence_are_fail_closed():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = canonical + contracts

    assert "Support exactly these explicit modes" in canonical
    assert "`Ready`, `Provisional`, or `Hold`" in canonical
    for outcome in ("`No Change`", "`Open Question`", "`Context Change Proposal`", "`Hold`"):
        assert outcome in canonical
    assert "Awaiting Persistence" in combined
    assert "prior version effective" in combined
    assert "partial approval" in combined
    assert "Do not reconstruct them from memory" in canonical
    assert "Use `Missing` instead of" in canonical


def test_private_data_and_external_authority_remain_separate():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = canonical + contracts

    for phrase in (
        "exact private economics",
        "customer messages",
        "supplier details",
        "private operating strategy",
        "Never write the tenant store",
        "raw customer-support transcripts outside Git",
        "does not authorize an operating review",
        "publication, pricing, spending, hiring, promotion, customer communication",
        "skills/tax-financial-governance/SKILL.md",
        "skills/project-state-update/SKILL.md",
    ):
        assert phrase in combined


def test_question_strategy_covers_six_evidence_groups_in_small_batches():
    strategy = read(QUESTION_STRATEGY)
    assert "no more than three questions at once" in strategy
    for heading in (
        "Goals And Scope",
        "Offer And Channels",
        "Economics And Evidence",
        "Customer And Operating Signals",
        "Capacity And Constraints",
        "Authority Boundaries",
    ):
        assert heading in strategy


def test_grace_gems_route_has_all_required_inputs_and_separate_authorizations():
    survey = read(GRACE_GEMS)
    assert "$business-intake create" in survey
    for numbered_heading in (
        "1. **Current goal:**",
        "2. **Top listings:**",
        "3. **Basic cost/pricing info:**",
        "4. **Customer support patterns:**",
        "5. **Owner decision rules:**",
        "6. **Fulfillment and production capacity:**",
    ):
        assert numbered_heading in survey
    assert "redact buyer names" in survey
    assert "first operating review and the week-one Media Production backlog each require separate owner authorization" in survey
    assert "no intake answer authorizes publication, pricing, spending, hiring, promotion, customer communication, or source changes" in survey
