from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml


ALLOWED_SOURCE_PRODUCTS = {"khan_academy_main_catalog", "khan_kids_curated_catalog"}
ALLOWED_EVIDENCE_STATUSES = {"official-public-web", "manual-curated", "manual-in-app-capture", "operator-note"}
ALLOWED_IMPORT_METHODS = {"public-web-manifest", "manual-curated", "manual-in-app-capture"}
LEDGER_STATUSES = {
    "imported",
    "duplicate",
    "missing-source",
    "invalid-manifest",
}
REQUIRED_FIELDS = (
    "stable_id",
    "source_product",
    "title",
    "subject_domain",
    "age_grade_band",
    "content_type",
    "evidence_status",
    "import_method",
)


class CatalogImportError(Exception):
    pass


@dataclass
class CatalogManifestRow:
    index: int
    stable_id: str
    source_product: str
    title: str
    subject_domain: str
    age_grade_band: str
    standards_tags: list[str]
    content_type: str
    source_url: str
    source_note: str
    evidence_status: str
    import_method: str
    operator_notes: str = ""


@dataclass
class CatalogRowResult:
    row: CatalogManifestRow
    status: str
    message: str
    destination: Path


@dataclass
class CatalogImportSummary:
    manifest_path: Path
    catalog_root: Path
    results: list[CatalogRowResult]
    dry_run: bool = False

    def count(self, *statuses: str) -> int:
        return sum(1 for result in self.results if result.status in statuses)


def load_catalog_manifest(path: str | Path) -> list[CatalogManifestRow]:
    manifest_path = Path(path)
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogImportError(f"Manifest not found: {manifest_path}") from exc
    except yaml.YAMLError as exc:
        raise CatalogImportError(f"Manifest YAML parse error in {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CatalogImportError("Manifest must be a mapping with a top-level 'catalog_entries' list.")
    rows = payload.get("catalog_entries")
    if not isinstance(rows, list):
        raise CatalogImportError("Manifest must include a top-level 'catalog_entries' list.")
    parsed: list[CatalogManifestRow] = []
    for index, raw in enumerate(rows, start=1):
        if not isinstance(raw, dict):
            raise CatalogImportError(f"Manifest row {index} must be a mapping.")
        values: dict[str, str] = {}
        for field in REQUIRED_FIELDS:
            values[field] = coerce_text(raw.get(field))
        for field in ("source_url", "source_note", "operator_notes"):
            values[field] = coerce_text(raw.get(field))
        standards = raw.get("standards_tags", [])
        if standards is None:
            standards = []
        if not isinstance(standards, list):
            raise CatalogImportError(f"Manifest row {index} standards_tags must be a list.")
        parsed.append(
            CatalogManifestRow(
                index=index,
                stable_id=values["stable_id"],
                source_product=values["source_product"],
                title=values["title"],
                subject_domain=values["subject_domain"],
                age_grade_band=values["age_grade_band"],
                standards_tags=[coerce_text(item) for item in standards if coerce_text(item)],
                content_type=values["content_type"],
                source_url=values["source_url"],
                source_note=values["source_note"],
                evidence_status=values["evidence_status"],
                import_method=values["import_method"],
                operator_notes=values["operator_notes"],
            )
        )
    return parsed


def find_catalog_root(manifest_path: str | Path) -> Path:
    path = Path(manifest_path).resolve()
    for candidate in [path.parent, *path.parents]:
        parts = candidate.parts[-3:]
        if parts == ("customers", "elementary-school", "catalog"):
            return candidate
    raise CatalogImportError(
        "Manifest must live under customers/elementary-school/catalog so catalogue assets stay inside the Elementary School membrane."
    )


def import_catalog(manifest_path: str | Path, *, dry_run: bool = False) -> CatalogImportSummary:
    manifest_file = Path(manifest_path).resolve()
    rows = load_catalog_manifest(manifest_file)
    catalog_root = find_catalog_root(manifest_file)
    results: list[CatalogRowResult] = []
    seen_destinations: set[Path] = set()
    for row in rows:
        destination = build_destination_path(catalog_root, row)
        result = evaluate_row(row, destination, seen_destinations)
        results.append(result)
        if result.status == "imported" and not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render_catalog_entry(row), encoding="utf-8")
        seen_destinations.add(destination)
    summary = CatalogImportSummary(manifest_path=manifest_file, catalog_root=catalog_root, results=results, dry_run=dry_run)
    if not dry_run:
        write_catalog_ledger(summary)
    return summary


def build_destination_path(catalog_root: Path, row: CatalogManifestRow) -> Path:
    return catalog_root / "imported" / row.source_product / f"{row.stable_id}.md"


def evaluate_row(
    row: CatalogManifestRow,
    destination: Path,
    seen_destinations: set[Path],
) -> CatalogRowResult:
    validation_error = validate_row(row)
    if validation_error:
        return CatalogRowResult(row=row, status="invalid-manifest", message=validation_error, destination=destination)
    if destination in seen_destinations:
        return CatalogRowResult(row=row, status="duplicate", message="Duplicate destination path inside manifest.", destination=destination)
    if destination.exists():
        return CatalogRowResult(row=row, status="duplicate", message="Destination catalog entry already exists.", destination=destination)
    if not row.source_url and not row.source_note:
        return CatalogRowResult(
            row=row,
            status="missing-source",
            message="At least one provenance field is required: source_url or source_note.",
            destination=destination,
        )
    return CatalogRowResult(row=row, status="imported", message="Imported catalog entry.", destination=destination)


def validate_row(row: CatalogManifestRow) -> str | None:
    missing = [field for field in REQUIRED_FIELDS if not getattr(row, field)]
    if missing:
        return f"Missing required fields: {', '.join(missing)}."
    if row.source_product not in ALLOWED_SOURCE_PRODUCTS:
        return f"Invalid source_product: {row.source_product}."
    if row.evidence_status not in ALLOWED_EVIDENCE_STATUSES:
        return f"Invalid evidence_status: {row.evidence_status}."
    if row.import_method not in ALLOWED_IMPORT_METHODS:
        return f"Invalid import_method: {row.import_method}."
    if row.source_product == "khan_academy_main_catalog":
        if row.import_method != "public-web-manifest":
            return "khan_academy_main_catalog rows must use import_method public-web-manifest."
        if row.evidence_status != "official-public-web":
            return "khan_academy_main_catalog rows must use evidence_status official-public-web."
    if row.source_product == "khan_kids_curated_catalog":
        if row.import_method == "public-web-manifest":
            return "khan_kids_curated_catalog rows may not use import_method public-web-manifest."
        if row.evidence_status == "official-public-web" and not row.source_url:
            return "khan_kids_curated_catalog rows using official-public-web evidence must include a source_url."
    return None


def render_catalog_entry(row: CatalogManifestRow) -> str:
    lines = [
        "---",
        f"stable_id: {yaml_scalar(row.stable_id)}",
        f"source_product: {row.source_product}",
        f"title: {yaml_scalar(row.title)}",
        f"subject_domain: {yaml_scalar(row.subject_domain)}",
        f"age_grade_band: {yaml_scalar(row.age_grade_band)}",
        f"standards_tags: {json.dumps(row.standards_tags, ensure_ascii=False)}",
        f"content_type: {yaml_scalar(row.content_type)}",
        f"source_url: {yaml_scalar(row.source_url)}",
        f"source_note: {yaml_scalar(row.source_note)}",
        f"evidence_status: {row.evidence_status}",
        f"import_method: {row.import_method}",
        f"operator_notes: {yaml_scalar(row.operator_notes)}",
        "---",
        "",
        f"# {row.title}",
        "",
        "## Catalog Metadata",
        "",
        f"- Stable ID: `{row.stable_id}`",
        f"- Source product: `{row.source_product}`",
        f"- Subject/domain: {row.subject_domain}",
        f"- Age/grade band: {row.age_grade_band}",
        f"- Content type: {row.content_type}",
        f"- Evidence status: `{row.evidence_status}`",
        f"- Import method: `{row.import_method}`",
    ]
    if row.standards_tags:
        lines.append(f"- Standards tags: {', '.join(f'`{tag}`' for tag in row.standards_tags)}")
    if row.source_url:
        lines.append(f"- Source URL: {row.source_url}")
    if row.source_note:
        lines.append(f"- Source note: {row.source_note}")
    if row.operator_notes:
        lines.extend(["", "## Operator Notes", "", row.operator_notes])
    lines.extend(
        [
            "",
            "## Recommendation Boundary",
            "",
            "This catalog entry may inform recommendation logic, but it does not prove mastery, diagnose the learner, or override parent authority.",
            "",
        ]
    )
    return "\n".join(lines)


def write_catalog_ledger(summary: CatalogImportSummary) -> None:
    ledger_path = summary.catalog_root / "catalog-import-ledger.md"
    lines = [
        "# Catalog Import Ledger",
        "",
        "This ledger tracks structured catalog-entry imports for Elementary School.",
        "",
        "Statuses:",
        "",
        "- `imported`: entry landed in the structured catalog area",
        "- `duplicate`: destination path already exists or collides inside the manifest",
        "- `missing-source`: manifest row lacks required provenance fields",
        "- `invalid-manifest`: metadata is incomplete or violates catalog rules",
        "",
        f"Manifest: `{summary.manifest_path.as_posix()}`",
        "",
        "| Source product | Title | Destination | Evidence status | Import status | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result in summary.results:
        lines.append(
            f"| {result.row.source_product} | {escape_cell(result.row.title)} | "
            f"`{result.destination.relative_to(summary.catalog_root).as_posix()}` | "
            f"`{result.row.evidence_status or 'missing'}` | `{result.status}` | {escape_cell(result.message)} |"
        )
    ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_catalog_import_summary(summary: CatalogImportSummary) -> str:
    staged = len(summary.results)
    imported = summary.count("imported")
    duplicates = summary.count("duplicate")
    missing = summary.count("missing-source")
    invalid = summary.count("invalid-manifest")
    lines = [
        "DRY RUN catalog import summary" if summary.dry_run else "Catalog import summary",
        f"- Manifest: {summary.manifest_path}",
        f"- Staged rows: {staged}",
        f"- Imported: {imported}",
        f"- Duplicates: {duplicates}",
        f"- Missing provenance rows: {missing}",
        f"- Invalid manifest rows: {invalid}",
        "",
        "Row results:",
    ]
    for result in summary.results:
        lines.append(
            f"- row {result.row.index}: {result.status} | {result.row.source_product} | {result.row.title} | {result.destination.name} | {result.message}"
        )
    return "\n".join(lines)


def render_catalog_completion_report(summary: CatalogImportSummary) -> str:
    product_totals = {product: 0 for product in ALLOWED_SOURCE_PRODUCTS}
    product_imported = {product: 0 for product in ALLOWED_SOURCE_PRODUCTS}
    product_missing = {product: 0 for product in ALLOWED_SOURCE_PRODUCTS}
    for result in summary.results:
        product = result.row.source_product if result.row.source_product in ALLOWED_SOURCE_PRODUCTS else None
        if product is None:
            continue
        product_totals[product] += 1
        already_landed = result.destination.exists()
        if result.status == "imported" or already_landed:
            product_imported[product] += 1
        if result.status == "missing-source" and not already_landed:
            product_missing[product] += 1
    lines = [
        "Catalog import completeness report",
        f"- Manifest: {summary.manifest_path}",
        f"- Total staged entries: {len(summary.results)}",
        f"- Total imported entries: {sum(product_imported.values())}",
        f"- Missing provenance rows: {summary.count('missing-source')}",
        f"- Invalid manifest rows: {summary.count('invalid-manifest')}",
        "",
        "| Source product | Staged | Imported | Missing provenance | Percent imported |",
        "| --- | --- | --- | --- | --- |",
    ]
    for product in sorted(ALLOWED_SOURCE_PRODUCTS):
        total = product_totals[product]
        percent = "0%" if total == 0 else f"{round((product_imported[product] / total) * 100)}%"
        lines.append(
            f"| {product} | {total} | {product_imported[product]} | {product_missing[product]} | {percent} |"
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


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|")
