from __future__ import annotations

import json
import os
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .ops_db import connect, migrate
from .ops_service import now_utc
from .privacy_scan import scan_text
from .repo_snapshot import RepoSnapshot


@dataclass(frozen=True)
class CadenceHandoff:
    id: str
    repo_id: str
    recorded_at: str
    recorded_by: str
    git_head: str
    branch: str
    worktree_state: str
    snapshot_fingerprint: str
    validation: tuple[dict[str, Any], ...]
    touched_surfaces: tuple[str, ...]
    fresh_issue_codes: tuple[str, ...]
    legacy_warning_codes: tuple[str, ...]
    tomorrow_inherits: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "repo_id": self.repo_id,
            "recorded_at": self.recorded_at,
            "recorded_by": self.recorded_by,
            "git_head": self.git_head,
            "branch": self.branch,
            "worktree_state": self.worktree_state,
            "snapshot_fingerprint": self.snapshot_fingerprint,
            "validation": list(self.validation),
            "touched_surfaces": list(self.touched_surfaces),
            "fresh_issue_codes": list(self.fresh_issue_codes),
            "legacy_warning_codes": list(self.legacy_warning_codes),
            "tomorrow_inherits": self.tomorrow_inherits,
        }


def resolve_cadence_db(explicit: str | None, *, for_record: bool) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not for_record and not path.exists():
            raise ValueError(f"Cadence database does not exist: {path}")
        return path
    data_dir = os.environ.get("ANYANG_DATA_DIR")
    if not data_dir:
        if for_record:
            raise ValueError("Dream --record requires --db or ANYANG_DATA_DIR")
        return None
    path = (Path(data_dir).expanduser().resolve() / "anyang-ops.db")
    if not for_record and not path.exists():
        return None
    return path


def record_handoff(
    path: str | Path,
    snapshot: RepoSnapshot,
    validation: list[dict[str, Any]],
    fresh_issue_codes: list[str],
    legacy_warning_codes: list[str],
    tomorrow_inherits: str,
    recorded_by: str,
    *,
    recorded_at: str | None = None,
) -> CadenceHandoff:
    _validate_safe(recorded_by, "recorded_by")
    _validate_safe(tomorrow_inherits, "tomorrow_inherits")
    for code in (*fresh_issue_codes, *legacy_warning_codes):
        _validate_code(code)
    for surface in snapshot.touched_surfaces:
        _validate_surface(surface)
    timestamp, identifier = recorded_at or now_utc(), str(uuid.uuid4())
    handoff = CadenceHandoff(
        id=identifier,
        repo_id=snapshot.repo_id,
        recorded_at=timestamp,
        recorded_by=recorded_by,
        git_head=snapshot.head,
        branch=snapshot.branch,
        worktree_state=snapshot.worktree_state,
        snapshot_fingerprint=snapshot.fingerprint,
        validation=tuple(_sanitize_validation(validation)),
        touched_surfaces=tuple(snapshot.touched_surfaces),
        fresh_issue_codes=tuple(fresh_issue_codes),
        legacy_warning_codes=tuple(legacy_warning_codes),
        tomorrow_inherits=tomorrow_inherits,
    )
    connection = connect(path, create_parent=True)
    try:
        migrate(connection, timestamp)
        connection.execute(
            """INSERT INTO cadence_handoff(
                id, repo_id, recorded_at, recorded_by, git_head, branch, worktree_state,
                snapshot_fingerprint, validation_json, touched_surfaces_json,
                fresh_issue_codes_json, legacy_warning_codes_json, tomorrow_inherits,
                explicit_record
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (
                handoff.id,
                handoff.repo_id,
                handoff.recorded_at,
                handoff.recorded_by,
                handoff.git_head,
                handoff.branch,
                handoff.worktree_state,
                handoff.snapshot_fingerprint,
                json.dumps(list(handoff.validation), sort_keys=True),
                json.dumps(list(handoff.touched_surfaces)),
                json.dumps(list(handoff.fresh_issue_codes)),
                json.dumps(list(handoff.legacy_warning_codes)),
                handoff.tomorrow_inherits,
            ),
        )
        connection.commit()
    finally:
        connection.close()
    return handoff


def latest_handoff(path: str | Path, repo_id: str) -> CadenceHandoff | None:
    connection = connect(path)
    try:
        try:
            row = connection.execute(
                """SELECT * FROM cadence_handoff
                WHERE repo_id = ? ORDER BY recorded_at DESC, id DESC LIMIT 1""",
                (repo_id,),
            ).fetchone()
        except sqlite3.OperationalError:
            return None
    finally:
        connection.close()
    if not row:
        return None
    return CadenceHandoff(
        id=row["id"],
        repo_id=row["repo_id"],
        recorded_at=row["recorded_at"],
        recorded_by=row["recorded_by"],
        git_head=row["git_head"],
        branch=row["branch"],
        worktree_state=row["worktree_state"],
        snapshot_fingerprint=row["snapshot_fingerprint"],
        validation=tuple(json.loads(row["validation_json"])),
        touched_surfaces=tuple(json.loads(row["touched_surfaces_json"])),
        fresh_issue_codes=tuple(json.loads(row["fresh_issue_codes_json"])),
        legacy_warning_codes=tuple(json.loads(row["legacy_warning_codes_json"])),
        tomorrow_inherits=row["tomorrow_inherits"],
    )


def _sanitize_validation(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    allowed = {"name", "status", "exit_code", "duration_ms", "summary"}
    result: list[dict[str, Any]] = []
    for item in items:
        clean = {key: item.get(key) for key in allowed}
        _validate_safe(str(clean.get("summary") or ""), "validation summary")
        result.append(clean)
    return result


def _validate_safe(value: str, label: str) -> None:
    if scan_text(value):
        raise ValueError(f"Unsafe {label}; cadence handoffs may not contain private identifiers or contact data")
    if len(value) > 500:
        raise ValueError(f"{label} is too long for a bounded cadence handoff")


def _validate_code(value: str) -> None:
    if not value or len(value) > 80 or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789:-_" for character in value.lower()):
        raise ValueError(f"Invalid cadence issue code: {value}")


def _validate_surface(value: str) -> None:
    if not value or "/" in value or "\\" in value or len(value) > 80:
        raise ValueError(f"Invalid touched surface: {value}")
