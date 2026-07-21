from pathlib import Path
import sqlite3
import tempfile

import pytest

from anyang_loop.cadence_metrics import measurement_report, record_measurement
from anyang_loop.ops_cli import main
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version


def database_path() -> Path:
    return Path(tempfile.mkdtemp()) / "anyang-ops.db"


def values(**overrides) -> dict:
    result = {
        "repo_id": "anyang-intelligence",
        "occurred_at": "2026-07-11T12:00:00Z",
        "event_type": "coffee",
        "scheduled": True,
        "completion_status": "completed",
        "state_source": "recorded_handoff",
        "manual_reconstruction": False,
        "reconstruction_minutes": 0,
        "evidence_check_passed": True,
        "privacy_check_passed": True,
        "authority_check_passed": True,
        "recorded_by": "operator",
    }
    result.update(overrides)
    return result


def test_schema_migrates_existing_database_to_cadence_measurements():
    path = database_path()
    raw = sqlite3.connect(path)
    raw.execute("CREATE TABLE schema_migration(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
    raw.execute("INSERT INTO schema_migration VALUES (2, '2026-07-10T00:00:00Z')")
    raw.commit()
    raw.close()

    with connect(path) as connection:
        migrate(connection, "2026-07-11T00:00:00Z")
        assert schema_version(connection) == SCHEMA_VERSION
        assert connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='cadence_measurement'"
        ).fetchone()


def test_record_measurement_rejects_inconsistent_manual_time():
    path = database_path()
    with connect(path, create_parent=True) as connection:
        migrate(connection, "2026-07-11T00:00:00Z")
        with pytest.raises(ValueError, match="minutes must be zero"):
            record_measurement(connection, **values(reconstruction_minutes=4))
        with pytest.raises(ValueError, match="requires manual_reconstruction"):
            record_measurement(
                connection,
                **values(state_source="manual_reconstruction", manual_reconstruction=False),
            )


def test_report_uses_completed_events_and_guardrails_for_rate():
    path = database_path()
    with connect(path, create_parent=True) as connection:
        migrate(connection, "2026-07-11T00:00:00Z")
        record_measurement(connection, **values(occurred_at="2026-07-11T10:00:00Z"))
        record_measurement(
            connection,
            **values(
                occurred_at="2026-07-11T11:00:00Z",
                state_source="git_fallback",
                privacy_check_passed=False,
            ),
        )
        record_measurement(
            connection,
            **values(
                occurred_at="2026-07-11T12:00:00Z",
                state_source="manual_reconstruction",
                manual_reconstruction=True,
                reconstruction_minutes=6,
            ),
        )
        record_measurement(
            connection,
            **values(
                occurred_at="2026-07-11T13:00:00Z",
                completion_status="partial",
                state_source="manual_reconstruction",
                manual_reconstruction=True,
                reconstruction_minutes=3,
            ),
        )
        report = measurement_report(connection, "anyang-intelligence", limit=4)

    assert report["recorded_events"] == 4
    assert report["completed_events"] == 3
    assert report["completed_without_manual_reconstruction"] == 1
    assert report["self_contained_completion_rate"] == 33.3
    assert report["median_reconstruction_minutes"] == 0
    assert report["total_reconstruction_minutes"] == 6
    assert report["sample_ready"] is True


def test_cli_dry_run_does_not_require_or_create_database(capsys):
    path = database_path()
    assert main(
        [
            "--db", str(path), "cadence", "record",
            "--repo-id", "anyang-intelligence", "--event-type", "coffee", "--scheduled",
            "--completion-status", "completed", "--state-source", "git_fallback",
            "--no-manual-reconstruction", "--reconstruction-minutes", "0",
            "--evidence-check-passed", "--privacy-check-passed", "--authority-check-passed",
            "--recorded-by", "operator", "--dry-run",
        ]
    ) == 0
    assert '"dry_run": true' in capsys.readouterr().out
    assert not path.exists()


def test_cli_records_and_reports_measurement(capsys):
    path = database_path()
    with connect(path, create_parent=True) as connection:
        migrate(connection, "2026-07-11T00:00:00Z")
    command = [
        "--db", str(path), "cadence", "record",
        "--repo-id", "anyang-intelligence", "--event-type", "dream", "--scheduled",
        "--completion-status", "completed", "--state-source", "recorded_handoff",
        "--no-manual-reconstruction", "--reconstruction-minutes", "0",
        "--evidence-check-passed", "--privacy-check-passed", "--authority-check-passed",
        "--recorded-by", "operator",
    ]
    assert main(command) == 0
    capsys.readouterr()
    assert main(["--db", str(path), "cadence", "report", "--repo-id", "anyang-intelligence"]) == 0
    output = capsys.readouterr().out
    assert '"self_contained_completion_rate": 100.0' in output
    assert '"sample_ready": false' in output
