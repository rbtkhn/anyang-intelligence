from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/media-production"
SPRINT = PROJECT / "creative-production-operator-readiness-sprint.md"
EXERCISE = PROJECT / "creative-production-operator-readiness-exercise.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_readiness_sprint_is_discoverable_and_precedes_onboarding():
    readme = read(PROJECT / "README.md")
    onboarding = read(PROJECT / "creative-production-operator-onboarding.md")

    assert "internal department and service line of Anyang Intelligence" in readme
    assert "Anyang Intelligence owns the department's client relationships" in readme
    assert "creative-production-operator-readiness-sprint.md" in readme
    assert "creative-production-operator-readiness-exercise.md" in readme
    assert "Advance to bounded onboarding" in onboarding
    assert "Grace Gems work remains unavailable" in onboarding


def test_sprint_has_bounded_sequence_evidence_and_decision_states():
    sprint = read(SPRINT)

    for day in range(1, 8):
        assert f"### Day {day}:" in sprint
    for decision in (
        "`Advance to bounded onboarding`",
        "`Conditional advance`",
        "`Do not advance`",
        "`Hold`",
    ):
        assert decision in sprint
    for evidence in (
        "authority and data-handling gate",
        "capacity receipt",
        "AI/tool disclosure",
        "Critical failures",
        "Record storage location (outside Git)",
    ):
        assert evidence in sprint


def test_sprint_does_not_imply_candidate_or_operating_authority():
    sprint = read(SPRINT)

    assert "Candidate sourcing, outreach, contracting, compensation, hiring, and assignment are not authorized" in sprint
    assert "The $500 monthly contractor allocation is a planning constraint, not permission to spend" in sprint
    assert "Grace Gems work remains `Hold`" in sprint
    assert "Do not commit completed candidate records to Git" in sprint
    for prohibited in (
        "client information",
        "publication",
        "customer contact",
        "live backlog",
    ):
        assert prohibited in sprint


def test_exercise_is_synthetic_claim_neutral_and_no_spend():
    exercise = read(EXERCISE)

    assert "Synthetic — not for publication or sale" in exercise
    assert "Time box: 120 minutes" in exercise
    assert "Spend: none" in exercise
    assert "use only the facts in this packet" in exercise
    assert "Mark anything else `Missing`" in exercise
    assert "do not publish, send, upload to public services, contact anyone, or create an account" in exercise
    assert "AI/tool disclosure" in exercise
    assert "one bounded revision containing no more than three exact changes" in exercise
    assert "does not test" in exercise and "willingness to work without compensation" in exercise


def test_plan_keeps_execution_behind_separate_authorization():
    plan = read(PROJECT / "30-day-plan.md")
    decisions = read(PROJECT / "decision-log.md")

    assert "Prepare the Creative Production Operator readiness sprint" in plan
    assert "If candidate interaction has been separately authorized" in plan
    assert "record an evidence-backed decision outside Git" in plan
    assert "A synthetic readiness sprint must precede Creative Production Operator onboarding" in decisions


def test_onboarding_distinguishes_internal_department_from_outsourced_role():
    onboarding = read(PROJECT / "creative-production-operator-onboarding.md")

    assert "Media Production is an internal Anyang Intelligence department" in onboarding
    assert "outsourced contract role engaged by Anyang Intelligence" in onboarding
    assert "completed submissions must use the sprint owner's approved private storage outside Git" in onboarding


def test_quality_gate_owns_readiness_and_routes_authority_questions():
    quality_gate = read(PROJECT / "creative-abundance-quality-gate.md")

    assert "owns asset quality and review readiness" in quality_gate
    assert "does not grant publication, client-delivery, rights-clearance, spending, contractor, or claim authority" in quality_gate
    assert "permissions-and-authority-review.md" in quality_gate


def test_permissions_review_owns_authority_boundaries():
    permissions = read(PROJECT / "permissions-and-authority-review.md")
    harness_map = read(PROJECT / "harness-map.md")

    assert "This review owns whether the workflow is permitted to cross an authority boundary" in permissions
    assert "not permission to publish, deliver, spend, clear rights, or commit a contractor" in permissions
    assert "sole owner for publication, delivery, rights clearance, spend, client commitment, claim approval, and contractor-authority boundaries" in harness_map
