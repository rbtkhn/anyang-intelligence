from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .bounded_agency import AgencyContractError, PhaseContract, load_phase
from .repo_snapshot import RepoSnapshot, collect_repo_snapshot
from .transcript_import import BLOCKING_STATUSES, EMAIL_PATTERN, ImportSummary, TranscriptImportError, plan_transcript_import


TRANSCRIPT_PHASE = "singularity-transcript-intake"


@dataclass(frozen=True)
class PhasePreflight:
    phase: PhaseContract
    snapshot: RepoSnapshot
    summary: ImportSummary | None
    authoritative_inputs: tuple[str, ...]
    creates: tuple[str, ...]
    modifies: tuple[str, ...]
    deletes: tuple[str, ...]
    unrelated_dirty: tuple[str, ...]
    dirty_write_paths: tuple[str, ...]
    protected_intersections: tuple[str, ...]
    warnings: tuple[dict[str, str], ...]
    row_holds: tuple[dict[str, Any], ...]
    blockers: tuple[dict[str, str], ...]
    authorization_required: tuple[dict[str, str], ...]

    @property
    def exit_code(self) -> int:
        if self.blockers:
            return 1
        if self.authorization_required:
            return 2
        return 0

    @property
    def expected_writes(self) -> tuple[str, ...]:
        return tuple(sorted(set((*self.creates, *self.modifies, *self.deletes))))

    def as_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase.phase_id,
            "objective": self.phase.objective,
            "capability": self.phase.capability,
            "status": "blocked" if self.blockers else "authorization-required" if self.authorization_required else "ready",
            "repository": {
                "id": self.snapshot.repo_id,
                "fingerprint": self.snapshot.fingerprint,
                "head": self.snapshot.head,
                "branch": self.snapshot.branch,
                "sync_status": self.snapshot.sync_status,
                "worktree_state": self.snapshot.worktree_state,
                "staged": list(self.snapshot.staged),
                "unstaged": list(self.snapshot.unstaged),
                "deleted": list(self.snapshot.deleted),
                "renamed": list(self.snapshot.renamed),
                "untracked": list(self.snapshot.untracked),
            },
            "authoritative_inputs": list(self.authoritative_inputs),
            "plan": {"create": list(self.creates), "modify": list(self.modifies), "delete": list(self.deletes)},
            "unrelated_dirty_paths": list(self.unrelated_dirty),
            "dirty_write_paths": list(self.dirty_write_paths),
            "protected_intersections": list(self.protected_intersections),
            "warnings": list(self.warnings),
            "row_holds": list(self.row_holds),
            "blockers": list(self.blockers),
            "authorization_required": list(self.authorization_required),
            "validators": list(self.phase.invariants),
            "complete_when": list(self.phase.complete_when),
            "next_phase": self.phase.next_phase,
            "enforcement": {
                "command_reads_and_writes": "enforced-by-capability",
                "repository_delta": "validated-postflight",
                "arbitrary_agent_reads": "advisory-unless-externally-sandboxed",
                "authority": "preflight-never-grants-authority",
            },
        }


def run_preflight(
    phase_id: str,
    manifest: str | Path,
    *,
    repo_root: str | Path | None = None,
    contract_path: str | Path | None = None,
) -> PhasePreflight:
    phase = load_phase(phase_id, contract_path)
    if phase_id != TRANSCRIPT_PHASE:
        raise AgencyContractError(f"No preflight adapter exists for phase: {phase_id}")
    root = Path(repo_root).resolve() if repo_root else find_repository_root(Path(manifest).resolve())
    snapshot = collect_repo_snapshot(root)
    blockers: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    holds: list[dict[str, Any]] = []
    summary: ImportSummary | None = None
    try:
        summary = plan_transcript_import(manifest)
    except TranscriptImportError as exc:
        blockers.append({"code": "invalid-manifest", "message": str(exc)})

    creates: list[str] = []
    modifies: list[str] = []
    authoritative_inputs = [repo_or_external(Path(manifest).resolve(), root)]
    if summary:
        creates = [relative_repo(path, root) for path in summary.planned_destinations]
        modifies = [relative_repo(summary.ledger_path, root)]
        for result in summary.results:
            if result.source_path:
                authoritative_inputs.append(repo_or_external(result.source_path, root))
            if result.status in BLOCKING_STATUSES:
                blockers.append({"code": result.status, "message": f"row {result.row.index}: {result.message}"})
            elif result.status in {"blocked-rights", "skipped-do-not-commit"}:
                holds.append({"row": result.row.index, "code": result.status, "message": result.message})

    expected = set((*creates, *modifies))
    dirty_write = tuple(sorted(path for path in snapshot.changed_paths if normalize_repo_path(path) in {normalize_repo_path(item) for item in expected}))
    if dirty_write:
        blockers.append({"code": "dirty-permitted-write-surface", "message": f"Intended write paths are already dirty: {', '.join(dirty_write)}"})
    unrelated = tuple(sorted(path for path in snapshot.changed_paths if path not in dirty_write))
    if unrelated:
        warnings.append({"code": "unrelated-dirty-worktree", "message": f"Unrelated dirty paths remain visible: {', '.join(unrelated)}"})

    protected: list[str] = []
    authorization: list[dict[str, str]] = []
    for path in expected:
        if not matches_any(path, phase.may_write):
            authorization.append({"code": "write-outside-envelope", "message": f"Requested write is outside may_write: {path}"})
        if matches_any(path, phase.protected):
            protected.append(path)
            authorization.append({"code": "protected-surface-intersection", "message": f"Requested write intersects a protected surface: {path}"})
    for path in creates:
        if not matches_any(path, phase.operations["create"]):
            authorization.append({"code": "create-not-authorized", "message": f"Create is outside phase operations: {path}"})
    for path in modifies:
        if not matches_any(path, phase.operations["modify"]):
            authorization.append({"code": "modify-not-authorized", "message": f"Modification is outside phase operations: {path}"})

    archive = root / "projects" / "singularity-science" / "archive"
    manifests = [archive / "transcript-intake-manifest.json", archive / "transcript-intake-manifest.generated.json"]
    if all(path.exists() for path in manifests):
        warnings.append({
            "code": "manifest-authority-ambiguity",
            "message": "Both generic and generated manifests exist; only the manifest named for this invocation is authoritative for this phase.",
        })
    return PhasePreflight(
        phase=phase,
        snapshot=snapshot,
        summary=summary,
        authoritative_inputs=tuple(dict.fromkeys(authoritative_inputs)),
        creates=tuple(sorted(creates)),
        modifies=tuple(sorted(modifies)),
        deletes=(),
        unrelated_dirty=unrelated,
        dirty_write_paths=dirty_write,
        protected_intersections=tuple(sorted(protected)),
        warnings=tuple(warnings),
        row_holds=tuple(holds),
        blockers=tuple(blockers),
        authorization_required=tuple(authorization),
    )


def verify_transition(before: RepoSnapshot, after: RepoSnapshot, expected_writes: tuple[str, ...]) -> dict[str, Any]:
    baseline = {normalize_repo_path(path) for path in before.changed_paths}
    current = {normalize_repo_path(path) for path in after.changed_paths}
    actual = tuple(sorted(current - baseline))
    expected = {normalize_repo_path(path) for path in expected_writes}
    unexpected = tuple(sorted(path for path in actual if path not in expected))
    missing = tuple(sorted(path for path in expected if path not in current))
    return {
        "status": "fail" if unexpected else "pass",
        "baseline_fingerprint": before.fingerprint,
        "result_fingerprint": after.fingerprint,
        "actual_delta": list(actual),
        "unexpected_delta": list(unexpected),
        "expected_paths_not_changed": list(missing),
    }


def validate_phase_result(
    preflight: PhasePreflight, summary: ImportSummary, transition: dict[str, Any]
) -> list[dict[str, str]]:
    statuses = {result.status for result in summary.results}
    output_paths = (*preflight.creates, *preflight.modifies, *preflight.deletes)
    checks = {
        "invoked-manifest-authoritative-for-phase": summary.manifest_path.resolve() == (preflight.snapshot.root / preflight.authoritative_inputs[0]).resolve()
        if not preflight.authoritative_inputs[0].startswith("external:")
        else True,
        "manifest-valid": "invalid-manifest" not in statuses,
        "source-present": "missing-source" not in statuses,
        "rights-governed": all(result.status in {*BLOCKING_STATUSES, "imported", "already-present", "blocked-rights", "skipped-do-not-commit"} for result in summary.results),
        "destination-contained": all(relative_repo(result.destination, preflight.snapshot.root) for result in summary.results),
        "destination-no-overwrite": "conflicting-destination" not in statuses,
        "contact-details-redacted": all(
            not EMAIL_PATTERN.search(result.expected_content or "") for result in summary.results
        ),
        "actual-delta-within-plan": transition["status"] == "pass",
        "no-cross-project-output": all(matches_any(path, preflight.phase.may_write) for path in output_paths),
    }
    return [
        {"code": invariant, "status": "pass" if checks.get(invariant, False) else "fail"}
        for invariant in preflight.phase.invariants
    ]


def render_preflight(preflight: PhasePreflight) -> str:
    data = preflight.as_dict()
    lines = [
        f"Bounded agency preflight: {data['phase']}",
        f"- Status: {data['status']}",
        f"- Capability: {data['capability']}",
        f"- Repository: {data['repository']['branch']} / {data['repository']['sync_status']} / {data['repository']['worktree_state']}",
        f"- Fingerprint: {data['repository']['fingerprint']}",
        f"- Planned creates: {len(preflight.creates)}",
        f"- Planned modifications: {len(preflight.modifies)}",
        f"- Row holds: {len(preflight.row_holds)}",
        f"- Warnings: {len(preflight.warnings)}",
        f"- Blockers: {len(preflight.blockers)}",
        f"- Authorization requirements: {len(preflight.authorization_required)}",
    ]
    for label, items in (("WARNING", preflight.warnings), ("HOLD", preflight.row_holds), ("BLOCK", preflight.blockers), ("AUTH", preflight.authorization_required)):
        for item in items:
            lines.append(f"- {label} {item['code']}: {item['message']}")
    lines.extend(["", "Planned writes:"])
    lines.extend(f"- create {path}" for path in preflight.creates)
    lines.extend(f"- modify {path}" for path in preflight.modifies)
    lines.extend(["", f"Next phase: {preflight.phase.next_phase['owner']} ({preflight.phase.next_phase['authority']})"])
    return "\n".join(lines)


def render_preflight_json(preflight: PhasePreflight) -> str:
    return json.dumps(preflight.as_dict(), indent=2, sort_keys=True)


def find_repository_root(path: Path) -> Path:
    for candidate in [path.parent, *path.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise TranscriptImportError(f"Cannot locate repository root from: {path}")


def relative_repo(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise TranscriptImportError(f"Planned output escapes repository root: {path}") from exc


def repo_or_external(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return f"external:{path.as_posix()}"


def normalize_repo_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./").casefold()


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    normalized = normalize_repo_path(path)
    return any(path_glob_match(normalized, normalize_repo_path(pattern)) for pattern in patterns if not pattern.startswith("external-"))


def path_glob_match(path: str, pattern: str) -> bool:
    marker = "__DOUBLE_STAR__"
    expression = re.escape(pattern.replace("**", marker))
    expression = expression.replace(re.escape(marker), ".*")
    expression = expression.replace(r"\*", "[^/]*").replace(r"\?", "[^/]")
    return re.fullmatch(expression, path) is not None
