from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/business-plan/SKILL.md"
EVIDENCE_RULES = ROOT / "skills/business-plan/references/evidence-and-scenario-rules.md"
OUTPUT_CONTRACTS = ROOT / "skills/business-plan/references/output-contracts.md"
ROUTE = ROOT / "skills/business-plan/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/business-plan/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/business-plan/agents/openai.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def frontmatter(path: Path) -> dict:
    _, raw, _ = read(path).split("---", 2)
    return yaml.safe_load(raw)


def test_business_plan_is_cataloged_and_explicit_only():
    metadata = frontmatter(CANONICAL)
    assert metadata["name"] == "business-plan"
    assert "$business-plan create" in metadata["description"]
    assert "$business-plan resume" in metadata["description"]
    assert "$business-plan change" in metadata["description"]
    assert "[business-plan](business-plan/SKILL.md)" in read(ROOT / "skills/README.md")

    for route_path in (ROUTE, ADAPTER_ROUTE):
        route = yaml.safe_load(read(route_path))
        assert route["interface"]["display_name"] == "Business Plan"
        assert 25 <= len(route["interface"]["short_description"]) <= 64
        assert "$business-plan create" in route["interface"]["default_prompt"]
        assert route["policy"]["allow_implicit_invocation"] is False


def test_adapter_routes_to_complete_canonical_contract():
    adapter = read(ADAPTER)
    canonical = read(CANONICAL)
    assert "skills/business-plan/SKILL.md" in adapter
    assert "$business-plan resume" in adapter
    assert "Do not prepare a plan from this adapter alone" in adapter
    assert "references/output-contracts.md" in canonical
    assert "references/evidence-and-scenario-rules.md" in canonical
    assert OUTPUT_CONTRACTS.is_file()
    assert EVIDENCE_RULES.is_file()


def test_resume_is_checkpoint_bound_and_cannot_replace_change():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = " ".join((canonical + contracts).split())
    for phrase in (
        "Plan Continuation Receipt",
        "version-bound checkpoint",
        "Route an already-effective plan to `change`",
        "version-matched operator",
        "do not redraft the approved",
        "Preserve the exact checkpoint",
    ):
        assert phrase in combined


def test_context_authority_and_decision_inputs_fail_closed():
    canonical = read(CANONICAL)
    combined = canonical + read(OUTPUT_CONTRACTS)
    for phrase in (
        "latest effective business context and exact version",
        "context approval and persistence receipts",
        "planning authority and named decision owner",
        "planning purpose, decision, and time horizon",
        "success measures and review date",
        "Do not reconstruct",
        "never request a broad data dump",
        "`Hold`",
    ):
        assert phrase in combined


def test_evidence_scenarios_economics_and_capacity_are_honest():
    canonical = read(CANONICAL)
    evidence = read(EVIDENCE_RULES)
    combined = canonical + evidence
    for phrase in (
        "`Confirmed fact`",
        "`Estimate`",
        "`Assumption`",
        "`Hypothesis`",
        "`Scenario`",
        "`Interpretation`",
        "`Missing`",
        "Do not invent margins, sustainable production capacity",
        "low/base/high",
        "base case into a forecast",
        "skills/tax-financial-governance/SKILL.md",
    ):
        assert phrase in combined


def test_required_plan_sections_and_learning_measures_are_present():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    evidence = read(EVIDENCE_RULES)
    combined = (canonical + contracts + evidence).lower()
    for phrase in (
        "decision summary",
        "strategic choices",
        "customer and value proposition",
        "capabilities and capacity constraints",
        "economics assumptions and scenarios",
        "leading indicators",
        "outcome metrics",
        "guardrails and burden measures",
        "30-day learning agenda",
        "90-day learning agenda",
        "proposed operating loops",
    ):
        assert phrase in combined


def test_plan_approval_does_not_leak_into_execution():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = canonical + contracts
    for phrase in (
        "`Awaiting Persistence`",
        "`Effective - not activated`",
        "Plan Persistence Handoff",
        "Plan effectiveness requires a separate operator-confirmed persistence",
        "External-action authorization: no",
        "Plan approval approves only the exact displayed plan",
        "does not authorize a loop, pilot, automation",
        "Pilot or activation authority: no",
        "No action taken; plan remains proposed or held pending owner decision.",
    ):
        assert phrase in combined


def test_change_routing_and_private_data_boundaries_are_explicit():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = canonical + contracts
    for phrase in (
        "$business-intake change",
        "durable business fact",
        "exact before-and-after wording",
        "Keep private records outside Git",
        "customer and order records",
        "supplier and employee details",
        "skills/project-state-update/SKILL.md",
        "automation-value-proof",
        "bounded-workflow-pilot",
    ):
        assert phrase in combined
