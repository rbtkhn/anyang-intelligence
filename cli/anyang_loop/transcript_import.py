from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any

import yaml


ALLOWED_LANES = {"external-interviews", "innermost-loop", "moonshots", "nate-b-jones"}
ALLOWED_RIGHTS = {"internal-commit-approved", "uncertain-review-needed", "do-not-commit"}
BLOCKING_STATUSES = {"invalid-manifest", "missing-source", "conflicting-destination", "path-escape"}
TERMINAL_STATUSES = {"imported", "already-present", "blocked-rights", "skipped-do-not-commit"}
LEDGER_STATUSES = TERMINAL_STATUSES | BLOCKING_STATUSES | {"needs-source-note"}
REQUIRED_FIELDS = (
    "lane",
    "title",
    "slug",
    "date_captured",
    "source_ref",
    "rights_status",
    "capture_method",
    "local_input_path",
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REDACTED_EMAIL = "[redacted-email]"
TEMP_SUFFIX = ".anyang-transcript-tmp"


class TranscriptImportError(Exception):
    pass


@dataclass(frozen=True)
class TranscriptManifestRow:
    index: int
    lane: str
    title: str
    slug: str
    date_captured: str
    source_ref: str
    rights_status: str
    capture_method: str
    local_input_path: str
    title_date: str = ""
    date_published: str = ""
    speaker: str = ""
    episode_id: str = ""
    notes: str = ""

    @property
    def effective_date(self) -> str:
        return self.title_date or self.date_published or self.date_captured

    @property
    def source_label(self) -> str:
        return f"{self.title} ({self.episode_id})" if self.episode_id else self.title


@dataclass(frozen=True)
class RowResult:
    row: TranscriptManifestRow
    status: str
    message: str
    destination: Path
    source_path: Path | None = None
    expected_content: str | None = None


@dataclass
class ImportSummary:
    manifest_path: Path
    archive_root: Path
    results: list[RowResult]
    dry_run: bool = False
    executed: bool = False

    def count(self, *statuses: str) -> int:
        return sum(1 for result in self.results if result.status in statuses)

    @property
    def blockers(self) -> list[RowResult]:
        return [result for result in self.results if result.status in BLOCKING_STATUSES]

    @property
    def planned_destinations(self) -> tuple[Path, ...]:
        return tuple(result.destination for result in self.results if result.status == "imported")

    @property
    def ledger_path(self) -> Path:
        return self.archive_root / "transcript-import-ledger.md"

    @property
    def complete(self) -> bool:
        return not self.blockers and all(result.status in TERMINAL_STATUSES for result in self.results)


def load_manifest(path: str | Path) -> list[TranscriptManifestRow]:
    manifest_path = Path(path)
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TranscriptImportError(f"Manifest not found: {manifest_path}") from exc
    except yaml.YAMLError as exc:
        raise TranscriptImportError(f"Manifest YAML parse error in {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise TranscriptImportError("Manifest must be a mapping with a top-level 'transcripts' list.")
    rows = payload.get("transcripts")
    if not isinstance(rows, list):
        raise TranscriptImportError("Manifest must include a top-level 'transcripts' list.")
    parsed: list[TranscriptManifestRow] = []
    for index, raw in enumerate(rows, start=1):
        if not isinstance(raw, dict):
            raise TranscriptImportError(f"Manifest row {index} must be a mapping.")
        values = {field: coerce_text(raw.get(field)) for field in REQUIRED_FIELDS}
        values.update({field: coerce_text(raw.get(field)) for field in ("title_date", "date_published", "speaker", "episode_id", "notes")})
        parsed.append(TranscriptManifestRow(index=index, **values))
    return parsed


def find_archive_root(manifest_path: str | Path) -> Path:
    path = Path(manifest_path).resolve()
    for candidate in [path.parent, *path.parents]:
        if tuple(part.casefold() for part in candidate.parts[-3:]) == ("projects", "singularity-science", "archive"):
            return candidate.resolve()
    raise TranscriptImportError(
        "Manifest must live under projects/singularity-science/archive so imported transcripts stay inside the archive membrane."
    )


def plan_transcript_import(manifest_path: str | Path) -> ImportSummary:
    manifest_file = Path(manifest_path).resolve()
    rows = load_manifest(manifest_file)
    archive_root = find_archive_root(manifest_file)
    results: list[RowResult] = []
    seen_destinations: set[str] = set()
    for row in rows:
        destination = build_destination_path(archive_root, row)
        result = evaluate_row(row, manifest_file, archive_root, destination, seen_destinations)
        results.append(result)
        seen_destinations.add(normalized_path(destination))
    return ImportSummary(manifest_path=manifest_file, archive_root=archive_root, results=results, dry_run=True)


def import_transcripts(manifest_path: str | Path, *, dry_run: bool = False) -> ImportSummary:
    summary = plan_transcript_import(manifest_path)
    summary.dry_run = dry_run
    if dry_run or summary.blockers:
        return summary
    recover_import(summary)
    execute_import_plan(summary)
    summary.executed = True
    return summary


def build_destination_path(archive_root: Path, row: TranscriptManifestRow) -> Path:
    filename = f"{row.effective_date}-{row.slug}.md"
    if not row.date_published:
        filename = f"{row.date_captured}-captured-{row.slug}.md"
    return archive_root / row.lane / "transcripts" / filename


def evaluate_row(
    row: TranscriptManifestRow,
    manifest_path: Path,
    archive_root: Path,
    destination: Path,
    seen_destinations: set[str],
) -> RowResult:
    validation_error = validate_row(row)
    if validation_error:
        return RowResult(row, "invalid-manifest", validation_error, destination)
    if not path_within(destination, archive_root):
        return RowResult(row, "path-escape", "Destination escapes the archive root.", destination)
    destination_key = normalized_path(destination)
    if destination_key in seen_destinations:
        return RowResult(row, "conflicting-destination", "Duplicate destination path inside manifest.", destination)
    source_path = resolve_input_path(manifest_path, row.local_input_path)
    if row.rights_status == "do-not-commit":
        return RowResult(row, "skipped-do-not-commit", "Rights status prevents an archive write.", destination, source_path)
    if row.rights_status == "uncertain-review-needed":
        return RowResult(row, "blocked-rights", "Rights review is required before this row may write.", destination, source_path)
    if not source_path.exists():
        return RowResult(row, "missing-source", f"Approved source file is missing: {source_path}", destination, source_path)
    try:
        body = load_transcript_body(source_path)
    except TranscriptImportError as exc:
        return RowResult(row, "invalid-manifest", str(exc), destination, source_path)
    expected = render_transcript(row, body)
    if destination.exists():
        try:
            current = destination.read_text(encoding="utf-8")
        except OSError as exc:
            return RowResult(row, "conflicting-destination", f"Cannot verify existing destination: {exc}", destination, source_path, expected)
        if current == expected:
            return RowResult(row, "already-present", "Destination already contains the normalized transcript.", destination, source_path, expected)
        return RowResult(row, "conflicting-destination", "Destination exists with different content; overwrite is prohibited.", destination, source_path, expected)
    return RowResult(row, "imported", "Ready to create normalized transcript and source-note follow-up.", destination, source_path, expected)


def validate_row(row: TranscriptManifestRow) -> str | None:
    missing = [field for field in REQUIRED_FIELDS if not getattr(row, field)]
    if missing:
        return f"Missing required fields: {', '.join(missing)}."
    if row.lane not in ALLOWED_LANES:
        return f"Invalid lane: {row.lane}."
    if row.rights_status not in ALLOWED_RIGHTS:
        return f"Invalid rights_status: {row.rights_status}."
    if not SLUG_PATTERN.fullmatch(row.slug):
        return "slug must use lowercase letters, numbers, and internal hyphens only."
    for value, label in ((row.date_captured, "date_captured"), (row.title_date, "title_date"), (row.date_published, "date_published")):
        if value and not is_iso_date(value):
            return f"{label} must use YYYY-MM-DD format."
    return None


def execute_import_plan(summary: ImportSummary) -> None:
    if summary.blockers:
        raise TranscriptImportError("Blocked transcript plan cannot execute.")
    writes: list[tuple[Path, str]] = []
    for result in summary.results:
        if result.status == "imported":
            if result.expected_content is None:
                raise TranscriptImportError(f"Missing rendered content for row {result.row.index}.")
            writes.append((result.destination, result.expected_content))
    ledger_text = render_import_ledger(summary)
    writes.append((summary.ledger_path, ledger_text))
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, content in writes:
            if destination != summary.ledger_path and destination.exists():
                raise TranscriptImportError(f"Destination appeared after planning; overwrite prohibited: {destination}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = temporary_path(destination)
            temporary.write_text(content, encoding="utf-8")
            staged.append((temporary, destination))
        for temporary, destination in staged:
            if destination != summary.ledger_path and destination.exists():
                raise TranscriptImportError(f"Destination appeared during execution; overwrite prohibited: {destination}")
            os.replace(temporary, destination)
    except Exception:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)
        raise


def recover_import(summary: ImportSummary) -> None:
    bounded = [*summary.planned_destinations, summary.ledger_path]
    for destination in bounded:
        temporary = temporary_path(destination)
        if path_within(temporary, summary.archive_root):
            temporary.unlink(missing_ok=True)


def temporary_path(destination: Path) -> Path:
    return destination.with_name(f".{destination.name}{TEMP_SUFFIX}")


def resolve_input_path(manifest_path: Path, local_input_path: str) -> Path:
    path = Path(local_input_path)
    return path.resolve() if path.is_absolute() else (manifest_path.parent / path).resolve()


def load_transcript_body(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError as exc:
        raise TranscriptImportError(f"Source file missing: {path}") from exc
    stripped = text.strip()
    if not stripped:
        raise TranscriptImportError(f"Transcript body is empty after normalization: {path}")
    return redact_transcript_body(stripped.replace("\r\n", "\n"))


def redact_transcript_body(text: str) -> str:
    return EMAIL_PATTERN.sub(REDACTED_EMAIL, text)


def render_transcript(row: TranscriptManifestRow, body: str) -> str:
    lines = [
        "---", f"title: {yaml_scalar(row.title)}", f"lane: {row.lane}", f"source_ref: {yaml_scalar(row.source_ref)}",
        f"title_date: {row.title_date or ''}", f"date_published: {row.date_published or ''}", f"date_captured: {row.date_captured}",
        f"rights_status: {row.rights_status}", f"capture_method: {yaml_scalar(row.capture_method)}", f"speaker: {yaml_scalar(row.speaker)}",
        f"episode_id: {yaml_scalar(row.episode_id)}", f"notes: {yaml_scalar(row.notes)}", "---", "", f"# {row.title}", "", "## Source Metadata", "",
        f"- Lane: `{row.lane}`", f"- Source reference: {row.source_ref}", f"- Date published: {row.date_published or 'unknown'}",
        f"- Date captured: {row.date_captured}", f"- Rights status: `{row.rights_status}`", f"- Capture method: {row.capture_method}",
    ]
    if row.speaker:
        lines.append(f"- Speaker: {row.speaker}")
    if row.episode_id:
        lines.append(f"- Episode ID: {row.episode_id}")
    if row.notes:
        lines.extend(["", "## Intake Notes", "", row.notes])
    lines.extend(["", "## Transcript", "", body, ""])
    return "\n".join(lines)


def render_import_ledger(summary: ImportSummary) -> str:
    lines = [
        "# Transcript Import Ledger", "", "This derived ledger reports the terminal state of the manifest named for this invocation.", "",
        "Statuses:", "", "- `imported`: transcript landed and still needs source-note follow-up",
        "- `already-present`: destination already matched the normalized transcript",
        "- `blocked-rights`: rights review holds this row without blocking independently approved rows",
        "- `skipped-do-not-commit`: rights status prevents an archive write",
        "- `missing-source`: approved manifest row points to a missing source",
        "- `conflicting-destination`: destination exists with different content or collides inside the manifest",
        "- `invalid-manifest`: manifest metadata is incomplete or malformed", "",
        f"Manifest: `{repo_display_path(summary.manifest_path)}`", "",
        "| Lane | Title | Destination | Rights status | Import status | Follow-up | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in summary.results:
        follow_up = "needs-source-note" if result.status in {"imported", "already-present"} else "-"
        lines.append(
            f"| {result.row.lane} | {escape_cell(result.row.source_label)} | `{safe_relative(result.destination, summary.archive_root)}` | "
            f"`{result.row.rights_status or 'missing'}` | `{result.status}` | `{follow_up}` | {escape_cell(result.message)} |"
        )
    return "\n".join(lines) + "\n"


def write_import_ledger(summary: ImportSummary) -> None:
    summary.ledger_path.write_text(render_import_ledger(summary), encoding="utf-8")


def render_import_summary(summary: ImportSummary) -> str:
    lines = [
        "DRY RUN transcript import summary" if summary.dry_run else "Transcript import summary",
        f"- Manifest: {repo_display_path(summary.manifest_path)}", f"- Staged rows: {len(summary.results)}",
        f"- Ready/imported: {summary.count('imported')}", f"- Already present: {summary.count('already-present')}",
        f"- Blocked rights-review items: {summary.count('blocked-rights')}", f"- Conflicting destinations: {summary.count('conflicting-destination')}",
        f"- Missing source files: {summary.count('missing-source')}", f"- Skipped do-not-commit: {summary.count('skipped-do-not-commit')}",
        f"- Invalid manifest rows: {summary.count('invalid-manifest')}", f"- Phase complete: {'yes' if summary.complete else 'no'}", "", "Row results:",
    ]
    lines.extend(
        f"- row {result.row.index}: {result.status} | {result.row.lane} | {result.row.title} | {result.destination.name} | {result.message}"
        for result in summary.results
    )
    return "\n".join(lines)


def import_summary_dict(summary: ImportSummary) -> dict[str, Any]:
    return {
        "manifest": repo_display_path(summary.manifest_path),
        "dry_run": summary.dry_run,
        "executed": summary.executed,
        "complete": summary.complete,
        "blockers": [result.status for result in summary.blockers],
        "planned_destinations": [repo_display_path(path) for path in summary.planned_destinations],
        "ledger": repo_display_path(summary.ledger_path),
        "rows": [
            {
                "index": result.row.index, "lane": result.row.lane, "title": result.row.title,
                "status": result.status, "destination": repo_display_path(result.destination), "message": result.message,
            }
            for result in summary.results
        ],
    }


def render_completion_report(summary: ImportSummary) -> str:
    lane_totals = {lane: 0 for lane in ALLOWED_LANES}
    lane_imported = {lane: 0 for lane in ALLOWED_LANES}
    lane_blocked = {lane: 0 for lane in ALLOWED_LANES}
    lane_missing = {lane: 0 for lane in ALLOWED_LANES}
    for result in summary.results:
        lane = result.row.lane if result.row.lane in ALLOWED_LANES else None
        if lane is None:
            continue
        lane_totals[lane] += 1
        if result.status in {"imported", "already-present"}:
            lane_imported[lane] += 1
        if result.status == "blocked-rights":
            lane_blocked[lane] += 1
        if result.status == "missing-source":
            lane_missing[lane] += 1
    total_imported = sum(lane_imported.values())
    lines = [
        "Transcript import completeness report", f"- Manifest: {repo_display_path(summary.manifest_path)}",
        f"- Total staged transcripts: {len(summary.results)}", f"- Total imported transcripts: {total_imported}",
        f"- Blocked rights-review items: {summary.count('blocked-rights')}", f"- Missing source files: {summary.count('missing-source')}", "",
        "| Lane | Staged | Imported | Blocked rights | Missing source | Percent imported |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for lane in sorted(ALLOWED_LANES):
        total = lane_totals[lane]
        percent = "0%" if total == 0 else f"{round((lane_imported[lane] / total) * 100)}%"
        lines.append(f"| {lane} | {total} | {lane_imported[lane]} | {lane_blocked[lane]} | {lane_missing[lane]} | {percent} |")
    return "\n".join(lines)


def path_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def normalized_path(path: Path) -> str:
    return str(path.resolve(strict=False)).replace("\\", "/").casefold()


def repository_root_for(path: Path) -> Path | None:
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def repo_display_path(path: Path) -> str:
    root = repository_root_for(path.resolve())
    if root:
        try:
            return path.resolve().relative_to(root).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def safe_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.name


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return value.strip() if isinstance(value, str) else str(value).strip()


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False) if value else '""'


def is_iso_date(value: str) -> bool:
    if len(value) != 10:
        return False
    try:
        year, month, day = value.split("-", 2)
    except ValueError:
        return False
    return all(part.isdigit() for part in (year, month, day)) and len(year) == 4 and len(month) == 2 and len(day) == 2


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|")
