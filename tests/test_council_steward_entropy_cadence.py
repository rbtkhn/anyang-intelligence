from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/council-steward-entropy-reduction-cadence.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_council_steward_entropy_cadence_defines_monthly_review():
    text = normalized(DOC)
    lower = text.lower()
    for phrase in (
        "Default cadence:",
        "monthly review with weekly focus areas",
        "Week 1 - dashboard reconciliation",
        "Week 2 - completion and state-label audit",
        "Week 3 - aging obligation review",
        "Week 4 - high-risk membrane sample",
    ):
        assert phrase in text

    for phrase in (
        "one portfolio dashboard claim",
        "one spending or purchase-related artifact",
        "one client-authority claim",
        "one runtime or source-boundary claim",
        "one stale, pending, expired, or held obligation",
    ):
        assert phrase in lower


def test_council_steward_entropy_cadence_preserves_authority_boundary():
    text = normalized(DOC)
    for phrase in (
        "advisory operating cadence - no execution authority",
        "does not authorize the Steward to approve findings",
        "change state",
        "gather private evidence",
        "communicate externally",
        "purchase",
        "publish",
        "execute corrections",
        "System Engineer must approve any persistent correction",
        "A finding is advisory until accepted by the appropriate authority",
    ):
        assert phrase in text


def test_council_steward_entropy_metrics_are_countable_and_not_activity_volume():
    text = normalized(DOC)
    for metric in (
        "Unsupported state claims caught",
        "Completion-gate failures",
        "Authority gaps intercepted",
        "Aging obligations surfaced",
        "Supersession reductions",
        "Reconstruction time",
        "Membrane holds",
        "False-positive burden",
    ):
        assert metric in text

    for phrase in (
        "Track the following counts and measures from repository-visible evidence",
        "Monthly success is not more findings",
        "Structural validation",
        "do not by themselves prove operational entropy was reduced",
        "observed correction",
        "prevented rework",
        "shorter reconstruction",
    ):
        assert phrase in text


def test_council_steward_entropy_cadence_aligns_with_existing_council_surfaces():
    text = normalized(DOC)
    for phrase in (
        "authority envelope",
        "Council Steward role contract",
        "Executive Council Transaction Record",
        "A. Recommendation",
        "B. Authority disposition",
        "C. Execution and evidence",
        "D. Reconciliation",
        "append-only Council ledger remains the canonical operating state",
    ):
        assert phrase in text
