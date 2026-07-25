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
    assert "Artistic Director monthly operating envelope: $1,000" in readme
    assert "included in the Media Production package" in readme
    assert "not a separately billed or client-owned position" in readme
    assert "Current spend authority: $0" in readme
    assert "current spend authority `$0`" in dashboard
    assert "$1,000/month Grace Gems service-package retainer" in dashboard


def test_artistic_production_gate_requires_activation_authority_and_evidence():
    gate = read(PROJECT / "artistic-production-gate.md")
    gate_normalized = " ".join(gate.split())

    for required in (
        "vacant and inactive",
        "Task ID and approved objective",
        "Lane and source boundary",
        "Three to five materially different directions",
        "Applicable client authority",
        "`$1,000/month` Artistic Director operating envelope as a ceiling",
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
        ROOT / "skills/media-production/media-production-ledger/SKILL.md",
        ROOT / "skills/media-production/media-production-package/SKILL.md",
        ROOT / "skills/media-production/media-production-quality-gate/SKILL.md",
    )

    combined = "\n".join(read(path) for path in active_files)
    assert "Artistic Director" in combined
    assert "artistic-production-gate.md" in combined
    assert "creative-production-operator-onboarding.md" not in combined
    assert "source/onboard the outsourced Creative Production Operator" not in combined
    assert "production brief for the Creative Production Operator" not in combined
    assert "Planned Artistic Director compensation: $500" not in combined


def test_steward_contract_uses_five_position_governing_rule():
    contract = read(ROOT / "docs/council-steward-role-contract.md")
    normalized_contract = " ".join(contract.split())

    assert "## Five-position governing rule" in contract
    assert "## Four-role governing rule" not in contract
    for position in (
        "System Engineer",
        "Chief Executive",
        "Artistic Director",
        "Executive Assistant",
        "Council Steward",
    ):
        assert position in normalized_contract


def test_structural_migration_receipt_preserves_decision_lineage():
    migration = read(
        ROOT / "docs/executive-council-artistic-director-migration-2026-07-24.md"
    )

    for field in (
        "**Approval source:**",
        "**Decision timestamp:**",
        "**Effective timestamp:**",
        "**Executed by:**",
        "**Implementation evidence:**",
        "**Review or expiry:**",
        "**Revocation and rollback path:**",
    ):
        assert field in migration
    assert "fc060bb4b6ed59f3bfa41a627a798df52a24b364" in migration


def test_operating_ceiling_does_not_authorize_allocation_or_payment():
    install = read(PROJECT / "executive-os-install.md")
    service = read(PROJECT / "grace-gems-monthly-service-package.md")
    tax_skill = read(ROOT / "skills/tax-financial-governance/SKILL.md")
    tax_skill_normalized = " ".join(tax_skill.split())

    assert "`$1,000/month` amount is a total operating ceiling" in install
    assert "No portion is pre-classified as compensation" in install
    assert "does not pre-classify any portion as compensation" in service
    assert "No portion is pre-allocated to compensation" in tax_skill_normalized
    assert (
        "does not establish employment, contractor classification"
        in tax_skill_normalized
    )


def test_grace_gems_activation_proposal_remains_inactive_and_unfunded():
    proposal = read(
        ROOT
        / "docs/"
        "executive-council-artistic-director-grace-gems-activation-proposal-2026-07-25.md"
    )
    brief = read(PROJECT / "grace-gems-owned-channel-visual-design-brief-2026-07-25.md")

    assert "**State:** `prepared — not activated`" in proposal
    assert "Human holder: `Missing`" in proposal
    assert "AI runtime: `Missing`" in proposal
    assert "Spend authorized by this proposal: `$0`" in proposal
    assert "Separate Artistic Director charge to Grace Gems: none" in proposal
    assert "internal Anyang Intelligence delivery function" in proposal
    assert "not allocated specifically" in proposal
    assert "does not task the Artistic Director directly" in proposal
    assert "Any unchecked item keeps the Artistic Director inactive" in proposal
    assert "does not staff or activate" in proposal

    assert "held pending Artistic Director activation" in brief
    assert "Artistic Director monthly operating ceiling: `$1,000`" in brief
    assert "Task-level tool, asset, or production allocation: `$0" in brief
    assert "No ideation, production, delivery, publication, spend" in brief


def test_anyang_operating_cost_baseline_preserves_planning_and_spend_boundaries():
    baseline = read(
        ROOT
        / "docs/"
        "anyang-intelligence-monthly-operating-cost-baseline-2026-07-25.md"
    )
    dashboard = read(ROOT / "projects/operating-portfolio-dashboard.md")

    for line in (
        "| Office rent | `$5,000` |",
        "| Utilities | `$1,000` |",
        "| Transportation | `$1,000` |",
        "| Artistic Director | `$1,000` |",
        "| Executive Assistant | `$5,000` |",
        "| Chief Executive | `$1,000` |",
        "| **Total** | **`$14,000`** |",
        "baseline is `$168,000`",
        "Current spend authorized by this record: `$0`",
        "not separately billed to Grace Gems",
    ):
        assert line in baseline

    assert "planning baseline of `$14,000`" in dashboard
    assert "funding source and allocation remain unapproved" in dashboard


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
