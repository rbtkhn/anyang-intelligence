from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n")


def test_plan_resume_uses_only_incomplete_version_bound_states():
    combined = " ".join(
        (
            read("skills/business-plan/SKILL.md")
            + read("skills/business-plan/references/output-contracts.md")
        ).split()
    )
    for phrase in (
        "$business-plan resume",
        "Plan Continuation Receipt",
        "[Proposed / Awaiting Persistence / Hold]",
        "Route an already-effective plan to `change`",
        "no effective plan exists",
        "next human authority",
    ):
        assert phrase in combined


def test_loop_resume_has_bounded_states_and_mode_routing():
    combined = read("skills/business-loop/SKILL.md") + read(
        "skills/business-loop/references/output-contracts.md"
    )
    for phrase in (
        "$business-loop resume",
        "Loop Continuation Receipt",
        "`Draft`, `Awaiting Persistence`, `Approved - pilot pending`,",
        "Route `Active` to `review`, `change`, or `pause`",
        "Never resume `Retired`",
        "prepare only the bounded pilot decision",
    ):
        assert phrase in combined


def test_pause_is_reversible_retirement_is_terminal():
    combined = " ".join(
        (
            read("skills/business-loop/SKILL.md")
            + read("skills/business-loop/references/output-contracts.md")
        ).split()
    )
    for phrase in (
        "$business-loop pause",
        "prepare a reversible stop",
        "Pause Packet",
        "Preserve the persisted specification for possible",
        "$business-loop retire",
        "prepare terminal loop closure",
        "Retirement Packet",
        "retired loop cannot be resumed",
    ):
        assert phrase in combined


def test_paused_reactivation_requires_new_version_matched_receipt():
    combined = (
        read("skills/business-loop/SKILL.md")
        + read("skills/business-loop/references/loop-contract.md")
        + read("skills/business-loop/references/output-contracts.md")
    )
    combined = " ".join(combined.split())
    for phrase in (
        "new version-matched Activation Receipt",
        "Transition: [initial activation / resume from pause]",
        "Prior pause receipt: [reference / not applicable]",
        "Restart conditions satisfied",
        "returning `Active`",
    ):
        assert phrase in combined


def test_catalog_and_adapters_expose_resume_and_pause_modes():
    catalog = read("skills/README.md")
    plan_adapter = read(".agents/skills/business-plan/SKILL.md")
    loop_adapter = read(".agents/skills/business-loop/SKILL.md")
    for phrase in (
        "`resume`, or `change`",
        "`resume`, `change`, `review`, `pause`, or `retire`",
    ):
        assert phrase in catalog
    assert "$business-plan resume" in plan_adapter
    assert "$business-loop resume" in loop_adapter
    assert "$business-loop pause" in loop_adapter
