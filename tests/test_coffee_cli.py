from pathlib import Path

from anyang_loop.cadence_store import record_handoff
from anyang_loop.coffee import build_coffee_data
from anyang_loop.coffee_cli import main
from anyang_loop.repo_snapshot import collect_repo_snapshot

from cadence_helpers import make_git_repo, write


DASHBOARD = """# Operating Portfolio Dashboard

## Current Cash Picture

Unknown or pending:

- Grace Gems owner intake.
- Grace Gems margin evidence.

## Active Obligations

### Learning Core

- Explore an unpaid curriculum idea.

### Media Production

- Operate the Grace Gems $1,000/month service package.

## Portfolio Rule

Current priority order:

1. Serve Grace Gems through Media Production.
2. Deepen Learning Core later.
"""


def test_coffee_is_not_self_referential_and_preserves_priority(tmp_path: Path):
    make_git_repo(tmp_path, DASHBOARD)
    write(tmp_path / "skills" / "README.md", "# Skills\n\ncoffee\ndream\n")

    data = build_coffee_data(tmp_path)

    assert "native `anyang-coffee`" not in data["improvement_candidate"]
    assert data["waiting_on"][:2] == ["Grace Gems owner intake.", "Grace Gems margin evidence."]
    assert data["live_obligations"][0].startswith("Media Production:")
    assert "git-only fallback" in data["current_picture"]


def test_failed_recorded_dream_governs_next_coffee(tmp_path: Path):
    make_git_repo(tmp_path, DASHBOARD)
    snapshot = collect_repo_snapshot(tmp_path)
    database = tmp_path / "external" / "cadence.db"
    record_handoff(
        database,
        snapshot,
        [{"name": "privacy-scan", "status": "fail", "exit_code": 1, "duration_ms": 2, "summary": "2 findings."}],
        ["validation:privacy-scan"],
        [],
        "Resolve privacy findings before shipping.",
        "operator",
        recorded_at="2026-07-10T00:00:00Z",
    )

    data = build_coffee_data(tmp_path, str(database))

    assert data["decision_reason"] == "validation-failure"
    assert data["improvement_candidate"] == "Resolve privacy findings before shipping."
    assert data["menu"][0].startswith("A. Confirm (recommended)")


def test_coffee_cli_json(tmp_path: Path, capsys):
    make_git_repo(tmp_path, DASHBOARD)
    assert main(["--repo", str(tmp_path), "--format", "json"]) == 0
    assert '"decision_reason"' in capsys.readouterr().out


def test_coffee_explicit_missing_db_fails_but_implicit_missing_db_falls_back(tmp_path: Path, monkeypatch, capsys):
    make_git_repo(tmp_path, DASHBOARD)
    missing = tmp_path / "missing" / "cadence.db"

    assert main(["--repo", str(tmp_path), "--db", str(missing)]) == 1
    assert "does not exist" in capsys.readouterr().err

    monkeypatch.setenv("ANYANG_DATA_DIR", str(tmp_path / "empty-data-dir"))
    data = build_coffee_data(tmp_path)
    assert "git-only fallback" in data["current_picture"]
