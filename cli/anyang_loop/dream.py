from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cadence_store import record_handoff, resolve_cadence_db
from .cadence_verify import CheckResult, run_verification, validation_status
from .repo_snapshot import RepoSnapshot, collect_repo_snapshot


def build_dream_data(
    repo_root: str | Path = ".",
    *,
    db_path: str | None = None,
    verify: str = "fast",
    record: bool = False,
    recorded_by: str = "operator",
) -> dict[str, Any]:
    snapshot = collect_repo_snapshot(repo_root, recent_limit=8)
    checks = run_verification(snapshot, verify)
    overall = validation_status(checks)
    fresh_codes = [f"validation:{check.name}" for check in checks if check.status == "fail"]
    legacy_codes = [
        "legacy:install-validation-warning"
        for check in checks
        if check.name == "install-validation" and "WARNING" in check.summary
    ]
    tomorrow = _tomorrow_inherits(snapshot, checks)
    latest = snapshot.recent_commits[0] if snapshot.recent_commits else "no recent commit visible"
    recent_rhythm = (
        f"The repo is settled around `{latest}` with a {snapshot.worktree_state} worktree. "
        f"This closeout observed {len(snapshot.changed_paths)} changed path(s) across "
        f"{', '.join(snapshot.touched_surfaces) or 'no touched surfaces'} and verification status `{overall}`."
    )
    data: dict[str, Any] = {
        "recent_rhythm": recent_rhythm,
        "git": {
            "branch": snapshot.branch,
            "sync_status": snapshot.sync_status,
            "worktree_state": snapshot.worktree_state,
            "head": snapshot.head,
        },
        "validation_status": overall,
        "validation": [check.as_dict() for check in checks],
        "generated_artifacts": [],
        "touched_surfaces": list(snapshot.touched_surfaces),
        "integrity_and_governance": _governance_lines(snapshot, checks),
        "tomorrow_inherits": tomorrow,
        "fresh_issue_codes": fresh_codes,
        "legacy_warning_codes": legacy_codes,
        "snapshot": snapshot.as_dict(),
        "recorded_handoff": None,
    }
    if record:
        database = resolve_cadence_db(db_path, for_record=True)
        assert database is not None
        handoff = record_handoff(
            database,
            snapshot,
            data["validation"],
            fresh_codes,
            legacy_codes,
            tomorrow,
            recorded_by,
        )
        data["recorded_handoff"] = handoff.as_dict()
        data["generated_artifacts"] = [f"cadence handoff `{handoff.id}` in external SQLite"]
    return data


def build_dream_brief(repo_root: str | Path = ".") -> str:
    return render_dream_text(build_dream_data(repo_root))


def render_dream_text(data: dict[str, Any]) -> str:
    generated = ", ".join(data["generated_artifacts"]) if data["generated_artifacts"] else "none; dream remained read-only"
    validation = _validation_text(data["validation_status"], data["validation"])
    git = data["git"]
    return "\n".join(
        [
            "Dream:",
            "",
            "Recent rhythm:",
            data["recent_rhythm"],
            "",
            "Run status:",
            f"- Git: `{git['branch']}`; {git['worktree_state']} worktree; remote state `{git['sync_status']}`",
            f"- Validation: {validation}",
            f"- Generated artifacts: {generated}",
            f"- Touched surfaces: {', '.join(data['touched_surfaces']) or 'none'}",
            "",
            "Integrity and governance:",
            *[f"- {line}" for line in data["integrity_and_governance"]],
            "",
            "Tomorrow inherits:",
            f"- {data['tomorrow_inherits']}",
        ]
    )


def render_dream_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def _tomorrow_inherits(snapshot: RepoSnapshot, checks: list[CheckResult]) -> str:
    failed = [check for check in checks if check.status == "fail"]
    if any(check.name == "privacy-scan" for check in failed):
        return "Resolve the recorded privacy-scan findings before expanding or shipping the current slice."
    if failed:
        return "Resolve the failed verification checks before expanding or shipping the current slice."
    if snapshot.dirty:
        return "Validate and isolate one coherent dirty-worktree slice before shipping."
    if snapshot.sync_status in {"ahead", "behind", "diverged"}:
        return "Review remote synchronization state before assuming cross-session continuity."
    return "Begin the next cycle from the highest-priority paid obligation in the portfolio dashboard."


def _governance_lines(snapshot: RepoSnapshot, checks: list[CheckResult]) -> list[str]:
    lines: list[str] = []
    failures = [check for check in checks if check.status == "fail"]
    if failures:
        lines.append(f"{len(failures)} fresh verification failure(s) remain; no clean-pass claim is permitted.")
    if any(check.name == "install-validation" and "WARNING" in check.summary for check in checks):
        lines.append("Install validation completed with known legacy warnings; they are not reported as fresh cadence failures.")
    if "projects" in snapshot.touched_surfaces:
        lines.append("Project changes retain their local privacy, evidence, and human-authority boundaries.")
    if "cli" in snapshot.touched_surfaces or "tests" in snapshot.touched_surfaces:
        lines.append("CLI and test changes remain advisory and create no publication, spend, delivery, or merge authority.")
    if not lines:
        lines.append("No new boundary issue is supported by the snapshot; normal membrane rules remain in force.")
    return lines


def _validation_text(overall: str, checks: list[dict[str, Any]]) -> str:
    detail = ", ".join(f"{check['name']}={check['status']}" for check in checks)
    return f"{overall} ({detail})"
