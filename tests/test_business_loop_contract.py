from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/business-loop/SKILL.md"
LOOP_CONTRACT = ROOT / "skills/business-loop/references/loop-contract.md"
OUTPUT_CONTRACTS = ROOT / "skills/business-loop/references/output-contracts.md"
ROUTE = ROOT / "skills/business-loop/agents/openai.yaml"
ADAPTER = ROOT / ".agents/skills/business-loop/SKILL.md"
ADAPTER_ROUTE = ROOT / ".agents/skills/business-loop/agents/openai.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def frontmatter(path: Path) -> dict:
    _, raw, _ = read(path).split("---", 2)
    return yaml.safe_load(raw)


def test_business_loop_is_cataloged_and_explicit_only():
    metadata = frontmatter(CANONICAL)
    assert metadata["name"] == "business-loop"
    for mode in ("design", "resume", "change", "review", "pause", "retire"):
        assert f"$business-loop {mode}" in metadata["description"]
    assert "[business-loop](business-loop/SKILL.md)" in read(
        ROOT / "skills/README.md"
    )

    for route_path in (ROUTE, ADAPTER_ROUTE):
        route = yaml.safe_load(read(route_path))
        assert route["interface"]["display_name"] == "Business Loop"
        assert 25 <= len(route["interface"]["short_description"]) <= 64
        assert "$business-loop design" in route["interface"]["default_prompt"]
        assert route["policy"]["allow_implicit_invocation"] is False


def test_adapter_routes_to_canonical_loop_doctrine_and_contracts():
    adapter = read(ADAPTER)
    canonical = read(CANONICAL)
    assert "skills/business-loop/SKILL.md" in adapter
    assert "$business-loop resume" in adapter
    assert "$business-loop pause" in adapter
    assert "Do not design or review a loop from this adapter alone" in adapter
    assert "docs/loops.md" in canonical
    assert "references/loop-contract.md" in canonical
    assert "references/output-contracts.md" in canonical
    assert LOOP_CONTRACT.is_file()
    assert OUTPUT_CONTRACTS.is_file()


def test_authority_linkage_and_one_decision_gate_fail_closed():
    combined = (read(CANONICAL) + read(OUTPUT_CONTRACTS)).lower()
    for phrase in (
        "business reference and effective context version",
        "effective plan priority",
        "plan approval receipt",
        "plan persistence receipt",
        "explicit standalone loop-design authority",
        "named loop owner and decision owner",
        "one signal and one decision",
        "success metric, burden guardrail, and stop conditions",
        "return `hold`",
        "do not reconstruct authority",
    ):
        assert phrase in combined


def test_loop_contract_contains_complete_canonical_grammar():
    combined = read(LOOP_CONTRACT) + read(OUTPUT_CONTRACTS)
    for phrase in (
        "`Signal`",
        "`Memory objects`",
        "`Decision prepared`",
        "`Authorized action path`",
        "`Evidence and receipts`",
        "`Cadence and service expectation`",
        "`Metrics and burden guardrails`",
        "`Exceptions and escalation`",
        "`Pause and stop conditions`",
        "`Learning update`",
        "`Governance and data membrane`",
    ):
        assert phrase in combined


def test_pilot_activation_and_execution_authority_do_not_leak():
    combined = read(CANONICAL) + read(OUTPUT_CONTRACTS) + read(LOOP_CONTRACT)
    for phrase in (
        "`Awaiting Persistence`",
        "`Approved - pilot pending`",
        "`Approved for pilot`",
        "Loop Specification Persistence Handoff",
        "Specification persistence receipt",
        "Pilot authorization: no",
        "Activation authorization: no",
        "Deployment or activation authorization: no",
        "Only `Activation confirmed: yes` permits `Active`",
        "Pilot completion produces evidence and a recommendation, not activation",
        "bounded-workflow-pilot",
        "automation-value-proof",
        "manual workflow",
        "does not create `Active`",
    ):
        assert phrase in combined


def test_review_detects_failure_modes_and_routes_learning():
    canonical = read(CANONICAL)
    contracts = read(OUTPUT_CONTRACTS)
    combined = canonical + contracts
    for phrase in (
        "open-loop drift",
        "memory decay",
        "cadence mismatch",
        "governance bypass",
        "evidence gaps",
        "overbuilding",
        "underbuilding",
        "`Adopt`, `Revise`, `Hold`, or `Retire`",
        "$business-intake change",
        "$business-plan change",
        "$business-loop change",
    ):
        assert phrase in combined


def test_pause_retirement_privacy_and_repo_boundaries_are_explicit():
    combined = (read(CANONICAL) + read(OUTPUT_CONTRACTS)).lower()
    for phrase in (
        "pause packet",
        "retirement packet",
        "reversible stop",
        "retirement packet",
        "open obligations",
        "ownership transfers",
        "restart conditions",
        "a retired loop cannot be resumed",
        "keep private customer, order, supplier, employee, financial",
        "outside git",
        "skills/project-state-update/skill.md",
        "no action taken; loop remains draft, paused, or held pending owner decision.",
    ):
        assert phrase in combined
