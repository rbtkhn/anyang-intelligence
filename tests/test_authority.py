from datetime import date
from pathlib import Path

import yaml

from anyang_loop.authority import authority_preflight, approval_receipt_is_current, validate_authority_envelope
from anyang_loop.project_cli import main


ROOT = Path(__file__).resolve().parents[1]


def test_repository_authority_envelope_validates():
    assert validate_authority_envelope() == []
    assert main(["validate-authority"]) == 0


def test_authority_preflight_never_grants_authority():
    result = authority_preflight("internal-coordination", "assign-hannah-tasks")
    assert result.status == "approval-required"
    assert result.approval_required is True
    assert "explicit-approval-required" in result.blockers


def test_preflight_blocks_prohibited_client_mutation():
    result = authority_preflight("client-advisory", "change-client-listings")
    assert result.status == "blocked"
    assert "prohibited-action" in result.blockers


def test_council_steward_has_bounded_portfolio_reconciliation_lane():
    data = yaml.safe_load((ROOT / "authority-envelope.yaml").read_text(encoding="utf-8"))
    assert data["roles"]["steward"]["authority"] == "bounded-council-state-reconciliation"

    domain = data["domains"]["portfolio-reconciliation"]
    assert "read-repository-project-state" in domain["allowed_actions"]
    assert "access-private-system" in domain["prohibited_actions"]
    assert domain["approver"] == "engineer"

    allowed = authority_preflight(
        "portfolio-reconciliation", "read-repository-project-state"
    )
    assert allowed.status == "approval-required"
    assert allowed.approval_required is True

    blocked = authority_preflight("portfolio-reconciliation", "access-private-system")
    assert blocked.status == "blocked"
    assert "prohibited-action" in blocked.blockers


def test_council_contract_places_four_role_council_over_project_portfolio():
    contract = (ROOT / "docs/executive-council-role-contract.md").read_text(
        encoding="utf-8"
    )
    assert "4. Council Steward." in contract
    assert "It is not a component of Grace Gems" in contract
    assert "shared read surface across repository-visible artifacts under" in contract


def test_council_is_engineer_governed_advisory_execution_and_assurance_system():
    data = yaml.safe_load((ROOT / "authority-envelope.yaml").read_text(encoding="utf-8"))
    assert (
        data["governance"]["operating_character"]
        == "engineer-governed-advisory-execution-and-assurance-system"
    )
    assert "client_parallel_authority_rule" in data["governance"]


def test_internal_coordination_defines_read_only_executive_discretion():
    data = yaml.safe_load((ROOT / "authority-envelope.yaml").read_text(encoding="utf-8"))
    domain = data["domains"]["internal-coordination"]
    assert "choose-analysis-method" in domain["read_only_discretion"]
    assert "executive_assistant_dispatch_rule" in domain
    assert domain["approval_threshold"] == "explicit-operator-approval-before-mutation"


def test_client_action_uses_non_substituting_dual_authority():
    data = yaml.safe_load((ROOT / "authority-envelope.yaml").read_text(encoding="utf-8"))
    domain = data["domains"]["client-advisory"]
    assert domain["required_approvers"] == ["engineer", "client"]
    assert "dual_authority_rule" in domain
    assert "authority_non_substitution_rule" in domain


def test_client_advisory_preflight_reports_both_required_authorities():
    result = authority_preflight(
        "client-advisory", "coordinate-approved-client-work"
    )
    assert result.status == "approval-required"
    assert result.authority == "engineer+client"
    assert result.blockers == ("dual-approval-required",)


def test_authority_validator_requires_steward_role(tmp_path: Path):
    source = ROOT / "authority-envelope.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    del data["roles"]["steward"]
    path = tmp_path / "authority-envelope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    diagnostics = validate_authority_envelope(path)
    assert any(
        item.code == "authority-role-incomplete" and "steward" in item.message
        for item in diagnostics
    )


def test_dual_authority_requires_valid_approver_set(tmp_path: Path):
    source = ROOT / "authority-envelope.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    data["domains"]["client-advisory"]["required_approvers"] = ["client"]
    path = tmp_path / "authority-envelope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    codes = {item.code for item in validate_authority_envelope(path)}
    assert "authority-required-approvers-invalid" in codes


def test_council_contract_distinguishes_role_runtime_and_client_authority():
    contract = (ROOT / "docs/executive-council-role-contract.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(contract.split())
    assert "Council membership conveys responsibility, not sovereign authority" in normalized
    assert "Durable membership and runtime activation" in normalized
    assert "Engineer approval does not create client-company authority" in normalized
    assert "The Chief Executive is the normal tasker of the Executive Assistant" in normalized


def test_invalid_domains_require_all_authority_fields(tmp_path: Path):
    source = ROOT / "authority-envelope.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    del data["domains"]["internal-coordination"]["recovery"]
    path = tmp_path / "authority-envelope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    codes = {item.code for item in validate_authority_envelope(path)}
    assert "authority-field-missing" in codes


def test_approval_receipt_requires_approved_unrevoked_and_unexpired():
    receipt = {"status": "Approved", "revoked": False, "expires_on": "2026-12-31"}
    assert approval_receipt_is_current(receipt, as_of=date(2026, 7, 21))
    receipt["revoked"] = True
    assert not approval_receipt_is_current(receipt, as_of=date(2026, 7, 21))
    receipt["revoked"] = False
    assert not approval_receipt_is_current(receipt, as_of=date(2027, 1, 1))


def test_receipt_without_expiry_is_not_current():
    assert not approval_receipt_is_current({"status": "Approved", "revoked": False})
