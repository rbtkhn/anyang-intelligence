import json
import sqlite3
from pathlib import Path

import pytest
import anyang_loop.dream_cli as dream_cli_module

from anyang_loop.cadence_store import latest_handoff, record_handoff
from anyang_loop.cadence_verify import run_verification
from anyang_loop.cadence_verify import CheckResult
from anyang_loop.coffee_cli import main as coffee_main
from anyang_loop.dream import build_dream_data
from anyang_loop.dream_cli import main as dream_main
from anyang_loop.repo_snapshot import collect_repo_snapshot
from anyang_loop.privacy_scan import scan_repo

from cadence_helpers import make_git_repo, write


def test_dream_none_is_read_only(tmp_path: Path):
    make_git_repo(tmp_path)
    database = tmp_path / "cadence.db"

    data = build_dream_data(tmp_path, db_path=str(database), verify="none", record=False)

    assert data["validation_status"] == "skipped"
    assert data["recorded_handoff"] is None
    assert not database.exists()


def test_fast_verification_reports_failure_and_unavailable(tmp_path: Path):
    make_git_repo(tmp_path)
    snapshot = collect_repo_snapshot(tmp_path)

    def runner(root, command):
        if command[:3] == ["git", "diff", "--check"]:
            return 1, "", "whitespace error"
        return 127, "", "not found"

    results = run_verification(
        snapshot,
        "full",
        command_runner=runner,
        runtime_resolver=lambda _root: Path("validated-python"),
    )

    assert results[0].status == "fail"
    assert any(result.status == "unavailable" for result in results)
    assert all(result.status in {"pass", "fail", "unavailable"} for result in results)


def test_full_verification_uses_an_isolated_repo_local_pytest_temp(tmp_path: Path):
    make_git_repo(tmp_path)
    snapshot = collect_repo_snapshot(tmp_path)
    commands = []

    def runner(root, command):
        commands.append((root, command))
        return 0, "", ""

    run_verification(
        snapshot,
        "full",
        command_runner=runner,
        runtime_resolver=lambda _root: Path("validated-python"),
    )

    pytest_command = next(command for _, command in commands if "pytest" in command)
    assert pytest_command[0] == "validated-python"
    basetemp_index = pytest_command.index("--basetemp")
    assert Path(pytest_command[basetemp_index + 1]) == tmp_path / ".pytest_cache" / "dream-full"


def test_full_verification_reports_runtime_bootstrap_failure(tmp_path: Path):
    make_git_repo(tmp_path)
    snapshot = collect_repo_snapshot(tmp_path)

    def unavailable(_root):
        raise RuntimeError("offline")

    results = run_verification(snapshot, "full", runtime_resolver=unavailable)

    assert results[-1].name == "validation-runtime"
    assert results[-1].status == "unavailable"


def test_unavailable_check_becomes_fresh_issue_and_tomorrow_inheritance(tmp_path: Path, monkeypatch):
    make_git_repo(tmp_path)
    unavailable = CheckResult("pytest", "unavailable", 1, 1, "missing")
    monkeypatch.setattr("anyang_loop.dream.run_verification", lambda *_args, **_kwargs: [unavailable])

    data = build_dream_data(tmp_path, verify="full")

    assert data["validation_status"] == "partial"
    assert data["fresh_issue_codes"] == ["validation:pytest"]
    assert "unavailable verification" in data["tomorrow_inherits"]
    assert "no clean-pass claim" in data["integrity_and_governance"][0]


@pytest.mark.parametrize(
    ("status", "expected"),
    [("pass", 0), ("skipped", 0), ("partial", 1), ("fail", 1)],
)
def test_dream_cli_exit_code_matches_validation_status(status, expected, monkeypatch, capsys):
    monkeypatch.setattr(
        dream_cli_module,
        "build_dream_data",
        lambda *_args, **_kwargs: {"validation_status": status, "recorded_handoff": {"id": "synthetic"}},
    )

    assert dream_cli_module.main(["--format", "json", "--verify", "none"]) == expected
    assert json.loads(capsys.readouterr().out)["validation_status"] == status


def test_dream_record_then_coffee_inherits(tmp_path: Path, capsys):
    make_git_repo(tmp_path)
    write(tmp_path / "untracked.txt", "work\n")
    database = tmp_path / "external" / "cadence.db"

    assert dream_main(
        ["--repo", str(tmp_path), "--db", str(database), "--verify", "none", "--record", "--format", "json"]
    ) == 0
    dream = json.loads(capsys.readouterr().out)
    assert coffee_main(["--repo", str(tmp_path), "--db", str(database), "--format", "json"]) == 0
    coffee = json.loads(capsys.readouterr().out)

    assert dream["recorded_handoff"] is not None
    assert coffee["improvement_candidate"] == dream["tomorrow_inherits"]


def test_existing_v1_database_migrates_for_handoff(tmp_path: Path):
    make_git_repo(tmp_path)
    database = tmp_path / "v1.db"
    connection = sqlite3.connect(database)
    connection.execute("CREATE TABLE schema_migration(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
    connection.execute("INSERT INTO schema_migration VALUES (1, '2026-07-09T00:00:00Z')")
    connection.commit()
    connection.close()

    snapshot = collect_repo_snapshot(tmp_path)
    handoff = record_handoff(database, snapshot, [], [], [], "Continue validation.", "operator")

    assert latest_handoff(database, snapshot.repo_id).id == handoff.id


def test_handoff_rejects_private_contact_text(tmp_path: Path):
    make_git_repo(tmp_path)
    snapshot = collect_repo_snapshot(tmp_path)
    unsafe_contact = "person" + chr(64) + "example.com"
    with pytest.raises(ValueError, match="Unsafe tomorrow_inherits"):
        record_handoff(tmp_path / "cadence.db", snapshot, [], [], [], f"Email {unsafe_contact} tomorrow.", "operator")


def test_dream_cli_requires_store_for_record(tmp_path: Path, monkeypatch, capsys):
    make_git_repo(tmp_path)
    monkeypatch.delenv("ANYANG_DATA_DIR", raising=False)
    assert dream_main(["--repo", str(tmp_path), "--verify", "none", "--record"]) == 1
    assert "requires --db" in capsys.readouterr().err


def test_privacy_scan_includes_untracked_candidate_files(tmp_path: Path):
    make_git_repo(tmp_path)
    unsafe_contact = "person" + chr(64) + "example.com"
    write(tmp_path / "untracked-private.txt", unsafe_contact)

    findings = scan_repo(tmp_path)

    assert any(finding.path == "untracked-private.txt" and finding.rule == "email-address" for finding in findings)


def test_privacy_scan_includes_csv_candidate_files(tmp_path: Path):
    make_git_repo(tmp_path)
    unsafe_contact = "person" + chr(64) + "example.com"
    write(tmp_path / "candidate-ledger.csv", f"record_id,counterparty\nFIN-0001,{unsafe_contact}\n")

    findings = scan_repo(tmp_path)

    assert any(finding.path == "candidate-ledger.csv" and finding.rule == "email-address" for finding in findings)


def test_privacy_scan_allows_marked_synthetic_pseudonym_fixture(tmp_path: Path):
    make_git_repo(tmp_path)
    pseudonym = "Abi" + "gail"
    write(
        tmp_path / "projects" / "learning-core" / f"{pseudonym.lower()}-fixture.md",
        f"---\nprivacy_class: synthetic-fixture\n---\n\n# {pseudonym} Fixture\n\n{pseudonym} is a pseudonym.\n",
    )

    findings = scan_repo(tmp_path)

    assert not any(finding.rule == "known-child-identifier" for finding in findings)
