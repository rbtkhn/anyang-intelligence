from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n")


def test_intake_handoff_supplies_version_bound_plan_prerequisites():
    intake = read("skills/business-intake/SKILL.md")
    contracts = read("skills/business-intake/references/output-contracts.md")
    combined = intake + contracts

    for phrase in (
        "Context approval receipt",
        "Context persistence receipt",
        "Requested downstream route",
        "Downstream preparation authority",
        "Named downstream decision owner",
        "Downstream evidence boundary",
        "Downstream approval or execution authority: no",
        "business planning, or neither",
    ):
        assert phrase in combined


def test_plan_handoff_cannot_activate_a_loop_or_pilot():
    plan = read("skills/business-plan/SKILL.md")
    contracts = read("skills/business-plan/references/output-contracts.md")
    combined = plan + contracts

    for phrase in (
        "State: Awaiting Persistence",
        "Final state: [Awaiting Persistence / Effective - not activated / Hold]",
        "Plan persistence receipt",
        "Loop-design authority",
        "Pilot or activation authority: no",
        "External-action authorization: no",
    ):
        assert phrase in combined


def test_loop_specification_and_pilot_approvals_are_separate():
    loop = read("skills/business-loop/SKILL.md")
    contracts = read("skills/business-loop/references/output-contracts.md")
    combined = " ".join((loop + contracts).split())

    for phrase in (
        "specification is persisted and its exact bounded pilot scope",
        "Approval produces `Awaiting Persistence`",
        "persistence produces `Approved - pilot pending`",
        "only a separately approved exact pilot scope produces `Approved for pilot`",
        "Specification persistence receipt",
        "Pilot route: [manual workflow / automation]",
        "Approved automation-value-proof reference",
        "Deployment or activation authorization: no",
    ):
        assert phrase in combined


def test_learning_routes_to_the_correct_truth_object():
    loop = read("skills/business-loop/SKILL.md")
    assert "durable business fact to `$business-intake change`" in loop
    assert "strategic choice, objective, allocation, or risk to `$business-plan change`" in loop
    assert "mechanics, cadence, ownership, evidence, burden, or exception changes to `$business-loop change`" in loop


def test_synthetic_end_to_end_simulation_is_non_operational():
    simulation = read("docs/business-capability-end-to-end-simulation-2026-07-24.md")
    for phrase in (
        "Synthetic fixture",
        "State: `Effective`",
        "`Effective - not activated`",
        "specification persistence receipt",
        "pilot route: `manual workflow`",
        "state: `Approved for pilot`",
        "pilot run: no",
        "activation: no",
        "No action taken",
    ):
        assert phrase in simulation
