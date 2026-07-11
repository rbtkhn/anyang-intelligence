from __future__ import annotations

from dataclasses import dataclass
from statistics import median
import sqlite3
import uuid

from .ops_service import now_utc
from .privacy_scan import scan_text


EVENT_TYPES = ("coffee", "dream", "operating_review", "other")
COMPLETION_STATUSES = ("completed", "partial", "abandoned")
STATE_SOURCES = ("recorded_handoff", "git_fallback", "manual_reconstruction")


@dataclass(frozen=True)
class CadenceMeasurement:
    id: str
    repo_id: str
    occurred_at: str
    event_type: str
    scheduled: bool
    completion_status: str
    state_source: str
    manual_reconstruction: bool
    reconstruction_minutes: float
    evidence_check_passed: bool
    privacy_check_passed: bool
    authority_check_passed: bool
    recorded_by: str
    created_at: str

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "repo_id": self.repo_id,
            "occurred_at": self.occurred_at,
            "event_type": self.event_type,
            "scheduled": self.scheduled,
            "completion_status": self.completion_status,
            "state_source": self.state_source,
            "manual_reconstruction": self.manual_reconstruction,
            "reconstruction_minutes": self.reconstruction_minutes,
            "evidence_check_passed": self.evidence_check_passed,
            "privacy_check_passed": self.privacy_check_passed,
            "authority_check_passed": self.authority_check_passed,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at,
        }


def record_measurement(connection: sqlite3.Connection, **values) -> CadenceMeasurement:
    _validate_values(values)
    measurement = CadenceMeasurement(
        id=str(uuid.uuid4()),
        repo_id=values["repo_id"],
        occurred_at=values.get("occurred_at") or now_utc(),
        event_type=values["event_type"],
        scheduled=bool(values["scheduled"]),
        completion_status=values["completion_status"],
        state_source=values["state_source"],
        manual_reconstruction=bool(values["manual_reconstruction"]),
        reconstruction_minutes=float(values["reconstruction_minutes"]),
        evidence_check_passed=bool(values["evidence_check_passed"]),
        privacy_check_passed=bool(values["privacy_check_passed"]),
        authority_check_passed=bool(values["authority_check_passed"]),
        recorded_by=values["recorded_by"],
        created_at=now_utc(),
    )
    connection.execute(
        """INSERT INTO cadence_measurement(
            id, repo_id, occurred_at, event_type, scheduled, completion_status,
            state_source, manual_reconstruction, reconstruction_minutes,
            evidence_check_passed, privacy_check_passed, authority_check_passed,
            recorded_by, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            measurement.id, measurement.repo_id, measurement.occurred_at,
            measurement.event_type, int(measurement.scheduled), measurement.completion_status,
            measurement.state_source, int(measurement.manual_reconstruction),
            measurement.reconstruction_minutes, int(measurement.evidence_check_passed),
            int(measurement.privacy_check_passed), int(measurement.authority_check_passed),
            measurement.recorded_by, measurement.created_at,
        ),
    )
    connection.commit()
    return measurement


def measurement_report(connection: sqlite3.Connection, repo_id: str, limit: int = 10) -> dict:
    if limit <= 0:
        raise ValueError("Cadence report limit must be positive")
    rows = connection.execute(
        """SELECT * FROM cadence_measurement
        WHERE repo_id = ? ORDER BY occurred_at DESC, id DESC LIMIT ?""",
        (repo_id, limit),
    ).fetchall()
    events = [_row_dict(row) for row in rows]
    completed = [event for event in events if event["completion_status"] == "completed"]
    self_contained = [
        event for event in completed
        if not event["manual_reconstruction"]
        and event["evidence_check_passed"]
        and event["privacy_check_passed"]
        and event["authority_check_passed"]
    ]
    minutes = [event["reconstruction_minutes"] for event in completed]
    return {
        "repo_id": repo_id,
        "requested_sample_size": limit,
        "recorded_events": len(events),
        "completed_events": len(completed),
        "completed_without_manual_reconstruction": len(self_contained),
        "self_contained_completion_rate": round(len(self_contained) / len(completed) * 100, 1) if completed else None,
        "median_reconstruction_minutes": median(minutes) if minutes else None,
        "total_reconstruction_minutes": round(sum(minutes), 2),
        "sample_ready": len(events) >= limit,
        "events": events,
    }


def _validate_values(values: dict) -> None:
    for name in ("repo_id", "recorded_by"):
        value = str(values.get(name) or "").strip()
        if not value or len(value) > 200 or scan_text(value):
            raise ValueError(f"Cadence measurement {name} must be bounded and privacy-safe")
    if values.get("event_type") not in EVENT_TYPES:
        raise ValueError("Invalid cadence event type")
    if values.get("completion_status") not in COMPLETION_STATUSES:
        raise ValueError("Invalid cadence completion status")
    if values.get("state_source") not in STATE_SOURCES:
        raise ValueError("Invalid cadence state source")
    minutes = float(values.get("reconstruction_minutes", 0))
    manual = bool(values.get("manual_reconstruction"))
    if minutes < 0 or (not manual and minutes != 0):
        raise ValueError("Reconstruction minutes must be zero when manual reconstruction is false")
    if values.get("state_source") == "manual_reconstruction" and not manual:
        raise ValueError("Manual reconstruction state source requires manual_reconstruction=true")


def _row_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "occurred_at": row["occurred_at"],
        "event_type": row["event_type"],
        "scheduled": bool(row["scheduled"]),
        "completion_status": row["completion_status"],
        "state_source": row["state_source"],
        "manual_reconstruction": bool(row["manual_reconstruction"]),
        "reconstruction_minutes": row["reconstruction_minutes"],
        "evidence_check_passed": bool(row["evidence_check_passed"]),
        "privacy_check_passed": bool(row["privacy_check_passed"]),
        "authority_check_passed": bool(row["authority_check_passed"]),
        "recorded_by": row["recorded_by"],
    }
