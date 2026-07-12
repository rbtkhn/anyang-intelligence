from pathlib import Path

import yaml

from anyang_loop.artifact_state import validate_artifact_manifest
from anyang_loop.project_cli import main


def artifact(**changes):
    value = {
        "path": "external/state.db",
        "operation": "Record accepted operating state.",
        "domain": "operating-state",
        "authority": "canonical",
        "data_class": "tenant-private",
        "provenance": {"schema": "schema.sql"},
        "mutability": {"method": "Governed transactional writes.", "writers": ["application"]},
        "recovery": {"method": "Restore a consistent backup.", "verification": ["integrity-check"]},
        "git": {"tracked": False},
    }
    value.update(changes)
    return value


def write_manifest(tmp_path: Path, artifacts: dict) -> Path:
    path = tmp_path / "artifacts.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "governance": {
                    "owner": "repository-operator",
                    "review_cadence": "quarterly",
                    "next_review": "2026-10-01",
                    "expansion_rule": "Add only for demonstrated recurring failures.",
                    "retirement_rule": "Retire when costs exceed demonstrated benefit.",
                },
                "exceptions": [],
                "artifacts": artifacts,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path


def codes(path: Path) -> set[str]:
    return {item.code for item in validate_artifact_manifest(path)}


def test_complete_contract_passes(tmp_path):
    assert codes(write_manifest(tmp_path, {"ledger": artifact()})) == set()


def test_requires_five_part_contract(tmp_path):
    broken = artifact()
    broken.pop("operation")
    broken.pop("recovery")
    assert codes(write_manifest(tmp_path, {"ledger": broken})) == {"artifact-field-missing"}


def test_rejects_duplicate_canonical_authority(tmp_path):
    path = write_manifest(tmp_path, {"first": artifact(), "second": artifact(path="external/other.db")})
    assert "duplicate-canonical-authority" in codes(path)


def test_derived_artifact_requires_known_source(tmp_path):
    derived = artifact(authority="derived", domain="review", provenance={"sources": ["missing"]})
    result = codes(write_manifest(tmp_path, {"review": derived}))
    assert "artifact-source-unknown" in result


def test_rejects_incomplete_mutability_and_recovery(tmp_path):
    broken = artifact(mutability={"method": "Regenerate only."}, recovery={"method": "Regenerate."})
    result = codes(write_manifest(tmp_path, {"ledger": broken}))
    assert {"artifact-mutability-incomplete", "artifact-recovery-incomplete"} <= result


def test_rejects_private_authoritative_state_in_git(tmp_path):
    path = write_manifest(tmp_path, {"ledger": artifact(git={"tracked": True})})
    assert "private-authority-in-git" in codes(path)


def test_exception_requires_approver_expiration_and_review_condition(tmp_path):
    path = write_manifest(tmp_path, {"ledger": artifact()})
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["exceptions"] = [{"control": "private-authority-in-git", "scope": "legacy-ledger"}]
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    assert "control-exception-incomplete" in codes(path)


def test_default_manifest_and_cli_pass():
    assert validate_artifact_manifest() == []
    assert main(["validate-artifacts"]) == 0
