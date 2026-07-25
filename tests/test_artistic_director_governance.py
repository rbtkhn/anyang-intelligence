from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/media-production"
HISTORICAL_OPERATOR_FILES = (
    "creative-production-operator-onboarding.md",
    "creative-production-operator-prerequisite-skills-test.md",
    "creative-production-operator-readiness-exercise.md",
    "creative-production-operator-readiness-sprint.md",
    "creative-production-operator-14-day-ramp.md",
    "creative-production-operator-training-review.md",
    "creative-production-operator-assignment-gate.md",
    "creative-production-operator-assignment-template.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split())


def test_media_production_remains_service_line_under_vacant_artistic_director():
    readme = read(PROJECT / "README.md")
    dashboard = read(ROOT / "projects/operating-portfolio-dashboard.md")

    assert "internal department and service line of Anyang Intelligence" in readme
    assert "Governing creative role: Artistic Director" in readme
    assert "vacant and inactive" in readme
    assert "Planned Artistic Director compensation: $500 per month" in readme
    assert "does not authorize engagement or payment" in dashboard
    assert "$1,000/month Grace Gems retainer" in dashboard


def test_artistic_production_gate_requires_activation_authority_and_evidence():
    gate = read(PROJECT / "artistic-production-gate.md")
    gate_normalized = " ".join(gate.split())

    for required in (
        "vacant and inactive",
        "Task ID and approved objective",
        "Lane and source boundary",
        "Three to five materially different directions",
        "Applicable client authority",
        "planned Artistic Director compensation as uncommitted",
        "transaction-record action ID",
        "Artistically review-ready",
    ):
        assert required in gate

    for prohibited in (
        "publication",
        "external delivery",
        "spending",
        "rights clearance",
        "client commitments",
        "claims",
    ):
        assert prohibited in gate_normalized


def test_artistic_brief_preserves_ideation_and_client_boundaries():
    brief = read(PROJECT / "artistic-production-brief-template.md")

    for field in (
        "Task ID:",
        "Approved by:",
        "Artistic Director activation receipt:",
        "Client authority:",
        "Required number of materially different directions: `3–5`",
        "Production time and material capacity:",
        "Transaction-record action ID:",
    ):
        assert field in brief
    assert "does not authorize external delivery" in brief
    assert "client adoption" in brief


def test_operator_artifact_family_is_retained_but_superseded():
    for name in HISTORICAL_OPERATOR_FILES:
        text = read(PROJECT / name)
        assert "superseded — historical contractor design" in text


def test_active_media_production_routes_to_artistic_director():
    active_files = (
        PROJECT / "README.md",
        PROJECT / "30-day-plan.md",
        PROJECT / "executive-os-install.md",
        PROJECT / "grace-gems-monthly-service-package.md",
        PROJECT / "harness-map.md",
        ROOT / "skills/media-production/media-production-brief/SKILL.md",
        ROOT / "skills/media-production/media-production-quality-gate/SKILL.md",
    )

    combined = "\n".join(read(path) for path in active_files)
    assert "Artistic Director" in combined
    assert "artistic-production-gate.md" in combined
    assert "source/onboard the outsourced Creative Production Operator" not in combined
    assert "production brief for the Creative Production Operator" not in combined


def test_compensation_is_planned_and_does_not_authorize_payment():
    install = read(PROJECT / "executive-os-install.md")
    service = read(PROJECT / "grace-gems-monthly-service-package.md")
    tax_skill = read(ROOT / "skills/tax-financial-governance/SKILL.md")

    assert "$500 per month; uncommitted" in install
    assert "compensation plan, not permission to engage or" in install
    assert "does not authorize engagement or payment" in service
    assert "does not establish employment, contractor classification" in tax_skill


def test_artistic_director_does_not_replace_external_interface_or_client():
    contract = normalized(ROOT / "docs/executive-council-role-contract.md")
    migration = read(
        ROOT / "docs/executive-council-artistic-director-migration-2026-07-24.md"
    )

    assert "cannot task the Executive Assistant directly" in contract
    assert "sole normal real-world interface" in contract
    assert "client CEO authority" in contract
    assert "does not" in migration and "contact clients" in migration
    assert "client creative authority" in migration


def test_receipt_chain_uses_named_executor_without_new_receipt_family():
    pilot = normalized(ROOT / "docs/executive-council-three-receipt-pilot.md")
    transaction = normalized(
        ROOT / "templates/executive-council-transaction-record.md"
    )
    migration = normalized(
        ROOT / "docs/executive-council-artistic-director-migration-2026-07-24.md"
    )

    assert "named-executor action and evidence return" in pilot
    assert "Artistic Director is the named executor" in pilot
    assert "Executive Assistant is the named executor" in pilot
    assert "repeat this section as C1, C2" in transaction
    assert "No new Artistic Director receipt family is created" in migration
