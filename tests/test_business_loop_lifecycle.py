from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: str) -> str:
    return " ".join(read(path).split())


def test_change_preserves_current_active_version_until_replacement_receipt():
    skill = normalized("skills/business-loop/SKILL.md")
    contracts = normalized("skills/business-loop/references/output-contracts.md")
    combined = skill + " " + contracts

    for phrase in (
        "track it separately from the current authoritative loop state",
        "Never silently transfer an old persistence or activation receipt to a new version",
        "Replacement persistence receipt",
        "Replacement activation receipt",
        "Proposed-version state",
        "Current authoritative version and state after decision",
        "Preserve the prior active version until replacement persistence and activation receipts are confirmed",
    ):
        assert phrase in combined


def test_review_requires_version_matched_activation_and_is_non_mutating():
    skill = normalized("skills/business-loop/SKILL.md")
    contracts = normalized("skills/business-loop/references/output-contracts.md")
    combined = skill + " " + contracts

    for phrase in (
        "Activation receipt reference",
        "Activation receipt current and version-matched",
        "require a current activation receipt for the exact reviewed version",
        "preserves the current authoritative state",
        "it does not create `Active`",
    ):
        assert phrase in combined


def test_pause_and_retirement_require_operational_confirmation():
    skill = normalized("skills/business-loop/SKILL.md")
    contracts = normalized("skills/business-loop/references/output-contracts.md")
    combined = skill + " " + contracts

    for phrase in (
        "Operator confirmation of operational steps:",
        "Operator confirmation of terminal steps:",
        "State transition effective:",
        "reversible stop steps",
        "terminal decision and operational steps",
        "preserve the prior authoritative state",
    ):
        assert phrase in combined


def test_resume_from_pause_requires_new_activation_and_retired_cannot_resume():
    skill = normalized("skills/business-loop/SKILL.md")
    contract = normalized("skills/business-loop/references/loop-contract.md")
    outputs = normalized("skills/business-loop/references/output-contracts.md")
    combined = skill + " " + contract + " " + outputs

    for phrase in (
        "Loop Continuation Receipt",
        "Route `Active` to `review`, `change`, or `pause`",
        "Never resume `Retired`; require a new design authorization",
        "Require a new version-matched Activation Receipt before returning `Active`",
        "retired loop cannot be resumed",
    ):
        assert phrase in combined


def test_lifecycle_simulation_covers_all_requested_modes_and_boundaries():
    simulation = normalized("docs/business-loop-lifecycle-simulation-2026-07-24.md")
    for phrase in (
        "`$business-loop change`",
        "`$business-loop review`",
        "`$business-loop pause`",
        "`$business-loop resume`",
        "`$business-loop retire`",
        "The v1 persistence and activation receipts do not transfer to v2",
        "A recommendation does not silently modify the loop",
        "resulting state: `Paused`",
        "transition: `resume from pause`",
        "resulting state: `Retired`",
        "new loop-design authority",
        "No action taken",
    ):
        assert phrase in simulation
