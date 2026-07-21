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
