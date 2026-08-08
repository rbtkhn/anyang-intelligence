from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml

from anyang_loop.memory_contract import (
    load_memory_constitution,
    render_memory_contract_report,
    validate_memory_constitution,
)
from anyang_loop.project_cli import main


ROOT = Path(__file__).resolve().parents[1]


def _candidate(tmp_path: Path, mutate=None) -> Path:
    _, manifest = load_memory_constitution()
    candidate = copy.deepcopy(manifest)
    for record in candidate["documents"].values():
        source = ROOT / record["path"]
        target = tmp_path / record["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    if mutate:
        mutate(candidate)
    path = tmp_path / "memory-constitution.yaml"
    path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
    return path


def _codes(path: Path) -> set[str]:
    return {item.code for item in validate_memory_constitution(path)}


def test_repository_memory_contract_is_valid_and_disabled(capsys):
    assert validate_memory_constitution() == []
    report = render_memory_contract_report()
    assert report["ok"] is True
    assert report["runtime_enabled"] is False
    assert report["authority_effect"] == "none"
    assert report["rule_count"] == 20
    assert main(["validate-memory-contract", "--format", "json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True


def test_required_rule_families_are_present_and_ids_are_unique():
    _, manifest = load_memory_constitution()
    ids = [rule["id"] for rule in manifest["rules"]]
    families = {rule_id.rsplit("-", 1)[0] for rule_id in ids}
    assert len(ids) == len(set(ids))
    assert {"AMC-ID", "AMC-COL", "AMC-CLS", "AMC-PRO", "AMC-EVI", "AMC-AUT", "AMC-RET", "AMC-REL", "AMC-RGT", "AMC-DEL", "AMC-EVL", "AMC-EMG", "AMC-AMD"} <= families
    assert all(rule["planned_test"].startswith("test_") for rule in manifest["rules"])


def test_activation_or_storage_configuration_fails_phase_1(tmp_path):
    enabled = _candidate(tmp_path / "enabled", lambda data: data["runtime"].update(enabled=True))
    configured = _candidate(tmp_path / "configured", lambda data: data["storage"].update(canonical_store="sqlite"))
    assert "memory-runtime-enabled" in _codes(enabled)
    assert "memory-storage-configured" in _codes(configured)


def test_falsy_non_boolean_runtime_and_storage_values_fail_phase_1(tmp_path):
    null_runtime = _candidate(tmp_path / "null-runtime", lambda data: data["runtime"].update(enabled=None))
    zero_storage = _candidate(tmp_path / "zero-storage", lambda data: data["storage"].update(repository_database_allowed=0))
    assert "memory-runtime-enabled" in _codes(null_runtime)
    assert "memory-storage-configured" in _codes(zero_storage)


def test_collection_authority_and_nonhuman_amendment_authority_fail(tmp_path):
    collection = _candidate(tmp_path / "collection", lambda data: data["governance"].update(collection_authority="agent"))
    amendment = _candidate(tmp_path / "amendment", lambda data: data["governance"].update(amendment_authority="agent"))
    assert "memory-governance-invalid" in _codes(collection)
    assert "memory-governance-invalid" in _codes(amendment)


def test_duplicate_rule_unknown_severity_and_missing_test_fail(tmp_path):
    def mutate(data):
        data["rules"][1]["id"] = data["rules"][0]["id"]
        data["rules"][2]["severity"] = "absolute"
        data["rules"][3]["planned_test"] = "missing"

    codes = _codes(_candidate(tmp_path, mutate))
    assert {"memory-rule-id-duplicate", "memory-rule-severity-invalid", "memory-rule-test-invalid"} <= codes


def test_missing_family_and_prohibition_fail(tmp_path):
    def mutate(data):
        data["rules"] = [rule for rule in data["rules"] if not rule["id"].startswith("AMC-DEL-")]
        data["prohibited_phase_1_actions"].remove("read-session-bodies")

    codes = _codes(_candidate(tmp_path, mutate))
    assert {"memory-rule-family-missing", "memory-prohibitions-incomplete"} <= codes


def test_private_source_path_and_raw_session_body_fail(tmp_path):
    def mutate(data):
        data["source_path"] = "C:/private/session.jsonl"
        data["session_body"] = "synthetic body that still must not be stored"

    codes = _codes(_candidate(tmp_path, mutate))
    assert {"memory-private-path-prohibited", "memory-raw-content-prohibited"} <= codes


def test_document_version_mismatch_and_escape_fail(tmp_path):
    mismatch = _candidate(tmp_path / "mismatch", lambda data: data["documents"]["kernel"].update(version="2"))
    escape = _candidate(tmp_path / "escape", lambda data: data["documents"]["kernel"].update(path="../outside.md"))
    assert "memory-document-version" in _codes(mismatch)
    assert "memory-document-escape" in _codes(escape)


def test_document_privacy_and_session_store_paths_fail(tmp_path):
    privacy = _candidate(tmp_path / "privacy")
    privacy_doc = privacy.parent / "docs" / "agent-memory-kernel-v1.md"
    privacy_doc.write_text(
        privacy_doc.read_text(encoding="utf-8") + "\nSynthetic contact: person" + chr(64) + "example.invalid\n",
        encoding="utf-8",
    )
    session_store = _candidate(tmp_path / "session-store")
    session_doc = session_store.parent / "docs" / "agent-memory-kernel-v1.md"
    session_doc.write_text(
        session_doc.read_text(encoding="utf-8") + "\nProhibited source: .codex" + "/sessions/raw.jsonl\n",
        encoding="utf-8",
    )
    assert "memory-document-privacy" in _codes(privacy)
    assert "memory-document-private-path" in _codes(session_store)


def test_invalid_manifest_json_is_structured_and_nonzero(tmp_path, capsys):
    path = tmp_path / "invalid.yaml"
    path.write_text("[unterminated", encoding="utf-8")
    assert main(["validate-memory-contract", "--manifest", str(path), "--format", "json"]) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is False
    assert output["diagnostics"][0]["code"] == "memory-contract-invalid"


def test_contract_report_is_deterministic_and_read_only():
    manifest_path, _ = load_memory_constitution()
    before = manifest_path.read_bytes()
    first = render_memory_contract_report()
    second = render_memory_contract_report()
    assert first == second
    assert manifest_path.read_bytes() == before
