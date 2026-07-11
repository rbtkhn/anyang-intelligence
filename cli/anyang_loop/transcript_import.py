from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

import yaml


ALLOWED_LANES = {"external-interviews", "innermost-loop", "moonshots", "nate-b-jones"}
ALLOWED_RIGHTS = {"internal-commit-approved", "uncertain-review-needed", "do-not-commit"}
LEDGER_STATUSES = {
    "imported",
    "blocked-rights",
    "duplicate",
    "missing-source",
    "needs-source-note",
    "skipped-do-not-commit",
    "invalid-manifest",
}
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
REDACTED_EMAIL = "[redacted-email]"


class TranscriptImportError(Exception):
    pass


@dataclass
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
        if self.episode_id:
            return f"{self.title} ({self.episode_id})"
        return self.title


@dataclass
class RowResult:
    row: TranscriptManifestRow
    status: str
    message: str
    destination: Path


@dataclass
class ImportSummary:
    manifest_path: Path
    archive_root: Path
    results: list[RowResult]
    dry_run: bool = False

    def count(self, *statuses: str) -> int:
        return sum(1 for result in self.results if result.status in statuses)


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
        values: dict[str, str] = {}
        for field in REQUIRED_FIELDS:
            values[field] = coerce_text(raw.get(field))
        for field in ("title_date", "date_published", "speaker", "episode_id", "notes"):
            values[field] = coerce_text(raw.get(field))
        parsed.append(
            TranscriptManifestRow(
                index=index,
                lane=values["lane"],
                title=values["title"],
                slug=values["slug"],
                date_captured=values["date_captured"],
                source_ref=values["source_ref"],
                rights_status=values["rights_status"],
                capture_method=values["capture_method"],
                local_input_path=values["local_input_path"],
                title_date=values["title_date"],
                date_published=values["date_published"],
                speaker=values["speaker"],
                episode_id=values["episode_id"],
                notes=values["notes"],
            )
        )
    return parsed


def find_archive_root(manifest_path: str | Path) -> Path:
    path = Path(manifest_path).resolve()
    for candidate in [path.parent, *path.parents]:
        parts = candidate.parts[-3:]
        if parts == ("projects", "singularity-science", "archive"):
            return candidate
    raise TranscriptImportError(
        "Manifest must live under projects/singularity-science/archive so imported transcripts stay inside the archive membrane."
    )


def import_transcripts(manifest_path: str | Path, *, dry_run: bool = False) -> ImportSummary:
    manifest_file = Path(manifest_path).resolve()
    rows = load_manifest(manifest_file)
    archive_root = find_archive_root(manifest_file)
    results: list[RowResult] = []
    seen_destinations: set[Path] = set()
    for row in rows:
        destination = build_destination_path(archive_root, row)
        result = evaluate_row(row, manifest_file, destination, seen_destinations)
        results.append(result)
        if result.status == "imported" and not dry_run:
            body = load_transcript_body(resolve_input_path(manifest_file, row.local_input_path))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render_transcript(row, body), encoding="utf-8")
        seen_destinations.add(destination)
    summary = ImportSummary(manifest_path=manifest_file, archive_root=archive_root, results=results, dry_run=dry_run)
    if not dry_run:
        write_import_ledger(summary)
    return summary


def build_destination_path(archive_root: Path, row: TranscriptManifestRow) -> Path:
    date_prefix = row.effective_date
    filename = f"{date_prefix}-{row.slug}.md"
    if not row.date_published:
        filename = f"{row.date_captured}-captured-{row.slug}.md"
    return archive_root / row.lane / "transcripts" / filename


def evaluate_row(
    row: TranscriptManifestRow,
    manifest_path: Path,
    destination: Path,
    seen_destinations: set[Path],
) -> RowResult:
    validation_error = validate_row(row)
    if validation_error:
        return RowResult(row=row, status="invalid-manifest", message=validation_error, destination=destination)
    if destination in seen_destinations:
        return RowResult(row=row, status="duplicate", message="Duplicate destination path inside manifest.", destination=destination)
    if destination.exists():
        return RowResult(row=row, status="duplicate", message="Destination transcript already exists.", destination=destination)
    if row.rights_status == "do-not-commit":
        return RowResult(row=row, status="skipped-do-not-commit", message="Rights status blocks commit.", destination=destination)
    if row.rights_status == "uncertain-review-needed":
        return RowResult(row=row, status="blocked-rights", message="Rights review required before commit.", destination=destination)
    source_path = resolve_input_path(manifest_path, row.local_input_path)
    if not source_path.exists():
        return RowResult(row=row, status="missing-source", message=f"Source file missing: {source_path}", destination=destination)
    try:
        load_transcript_body(source_path)
    except TranscriptImportError as exc:
        return RowResult(row=row, status="invalid-manifest", message=str(exc), destination=destination)
    return RowResult(row=row, status="imported", message="Imported transcript and marked source note follow-up.", destination=destination)


def validate_row(row: TranscriptManifestRow) -> str | None:
    missing = [field for field in REQUIRED_FIELDS if not getattr(row, field)]
    if missing:
        return f"Missing required fields: {', '.join(missing)}."
    if row.lane not in ALLOWED_LANES:
        return f"Invalid lane: {row.lane}."
    if row.rights_status not in ALLOWED_RIGHTS:
        return f"Invalid rights_status: {row.rights_status}."
    for value, label in (
        (row.date_captured, "date_captured"),
        (row.title_date, "title_date"),
        (row.date_published, "date_published"),
    ):
        if value and not is_iso_date(value):
            return f"{label} must use YYYY-MM-DD format."
    return None


def resolve_input_path(manifest_path: Path, local_input_path: str) -> Path:
    path = Path(local_input_path)
    if path.is_absolute():
        return path
    return (manifest_path.parent / path).resolve()


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
        "---",
        f"title: {yaml_scalar(row.title)}",
        f"lane: {row.lane}",
        f"source_ref: {yaml_scalar(row.source_ref)}",
        f"title_date: {row.title_date or ''}",
        f"date_published: {row.date_published or ''}",
        f"date_captured: {row.date_captured}",
        f"rights_status: {row.rights_status}",
        f"capture_method: {yaml_scalar(row.capture_method)}",
        f"speaker: {yaml_scalar(row.speaker)}",
        f"episode_id: {yaml_scalar(row.episode_id)}",
        f"notes: {yaml_scalar(row.notes)}",
        "---",
        "",
        f"# {row.title}",
        "",
        "## Source Metadata",
        "",
        f"- Lane: `{row.lane}`",
        f"- Source reference: {row.source_ref}",
        f"- Date published: {row.date_published or 'unknown'}",
        f"- Date captured: {row.date_captured}",
        f"- Rights status: `{row.rights_status}`",
        f"- Capture method: {row.capture_method}",
    ]
    if row.speaker:
        lines.append(f"- Speaker: {row.speaker}")
    if row.episode_id:
        lines.append(f"- Episode ID: {row.episode_id}")
    if row.notes:
        lines.extend(["", "## Intake Notes", "", row.notes])
    lines.extend(["", "## Transcript", "", body, ""])
    return "\n".join(lines)


def write_import_ledger(summary: ImportSummary) -> None:
    ledger_path = summary.archive_root / "transcript-import-ledger.md"
    lines = [
        "# Transcript Import Ledger",
        "",
        "This ledger tracks transcript-level import state across Singularity Science source lanes.",
        "",
        "Statuses:",
        "",
        "- `imported`: transcript landed in the archive and still needs source-note follow-up",
        "- `blocked-rights`: rights status requires review before commit",
        "- `duplicate`: destination path already exists or collides inside the manifest",
        "- `missing-source`: manifest row points to a source file that was not found",
        "- `needs-source-note`: imported transcript still needs a source note",
        "- `skipped-do-not-commit`: rights status explicitly prevents commit",
        "- `invalid-manifest`: manifest metadata is incomplete or malformed",
        "",
        f"Manifest: `{summary.manifest_path.as_posix()}`",
        "",
        "| Lane | Title | Destination | Rights status | Import status | Follow-up | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in summary.results:
        follow_up = "needs-source-note" if result.status == "imported" else "-"
        notes = escape_cell(result.message)
        lines.append(
            f"| {result.row.lane} | {escape_cell(result.row.source_label)} | `{result.destination.relative_to(summary.archive_root).as_posix()}` | "
            f"`{result.row.rights_status or 'missing'}` | `{result.status}` | `{follow_up}` | {notes} |"
        )
    ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_import_summary(summary: ImportSummary) -> str:
    staged = len(summary.results)
    imported = summary.count("imported")
    blocked = summary.count("blocked-rights")
    duplicates = summary.count("duplicate")
    missing = summary.count("missing-source")
    skipped = summary.count("skipped-do-not-commit")
    invalid = summary.count("invalid-manifest")
    lines = [
        "DRY RUN transcript import summary" if summary.dry_run else "Transcript import summary",
        f"- Manifest: {summary.manifest_path}",
        f"- Staged rows: {staged}",
        f"- Imported: {imported}",
        f"- Blocked rights-review items: {blocked}",
        f"- Duplicates: {duplicates}",
        f"- Missing source files: {missing}",
        f"- Skipped do-not-commit: {skipped}",
        f"- Invalid manifest rows: {invalid}",
        "",
        "Row results:",
    ]
    for result in summary.results:
        lines.append(
            f"- row {result.row.index}: {result.status} | {result.row.lane} | {result.row.title} | {result.destination.name} | {result.message}"
        )
    return "\n".join(lines)


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
        already_landed = result.destination.exists()
        if result.status == "imported" or already_landed:
            lane_imported[lane] += 1
        if result.status == "blocked-rights" and not already_landed:
            lane_blocked[lane] += 1
        if result.status == "missing-source" and not already_landed:
            lane_missing[lane] += 1
    staged = len(summary.results)
    total_imported = sum(lane_imported.values())
    lines = [
        "Transcript import completeness report",
        f"- Manifest: {summary.manifest_path}",
        f"- Total staged transcripts: {staged}",
        f"- Total imported transcripts: {total_imported}",
        f"- Blocked rights-review items: {summary.count('blocked-rights')}",
        f"- Missing source files: {summary.count('missing-source')}",
        "",
        "| Lane | Staged | Imported | Blocked rights | Missing source | Percent imported |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for lane in sorted(ALLOWED_LANES):
        total = lane_totals[lane]
        percent = "0%" if total == 0 else f"{round((lane_imported[lane] / total) * 100)}%"
        lines.append(
            f"| {lane} | {total} | {lane_imported[lane]} | {lane_blocked[lane]} | {lane_missing[lane]} | {percent} |"
        )
    return "\n".join(lines)


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def yaml_scalar(value: str) -> str:
    if not value:
        return '""'
    return json.dumps(value, ensure_ascii=False)


def is_iso_date(value: str) -> bool:
    if len(value) != 10:
        return False
    year, month, day = value.split("-", 2)
    return all(part.isdigit() for part in (year, month, day)) and len(month) == 2 and len(day) == 2


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|")
