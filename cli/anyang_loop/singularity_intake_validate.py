from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


DISPOSITIONS = {"primitive-candidate", "needs-verification", "lane-test-ready", "worldview-only", "preserved"}
RETENTION_STATUSES = {"watch", "needs-verification", "worldview-only"}
INTAKE_TIERS = {"light", "standard", "deep"}
FEEDBACK_OUTCOMES = {"accepted", "modified", "rejected", "held", "adopted", "caused-unintended-work"}
RIGHTS_MARKERS = ("internal", "public web capture", "operator-provided", "unknown", "provisional")
REQUIRED_PACKET_FIELDS = (
    ("Source episode:", "Source interview:", "Source episode or Source interview:"),
    ("Seam:",),
    ("Transferable question or checklist:",),
    ("Receiving lane:",),
    ("Membrane classification:",),
    ("Human authority required:",),
    ("Evidence still needed:",),
    ("What stays inside Singularity Science:",),
)
DECISION_COMPRESSION_FIELDS = (
    "What changed:",
    "Reusable mechanism:",
    "Decision implication:",
    "Evidence still missing:",
    "Recommended disposition:",
)
RECEIPT_FIELDS = (
    "Research question:",
    "Decision or risk affected:",
    "Baseline assumption:",
    "Human authority required:",
    "Downstream receipt reference:",
    "Outcome after review:",
    "Review date:",
    "Counterfactual:",
    "Attribution confidence:",
)
RETENTION_FIELDS = (
    "Retention reason:",
    "Current status:",
    "Evidence missing:",
    "Revisit trigger:",
    "Review owner:",
    "Next review date:",
    "Potential receiving lane:",
)
LINK_RE = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")
STRUCTURED_DISPOSITION_RE = re.compile(r"(?im)^\s*(?:ROI disposition|Disposition)\s*:\s*`?([a-z-]+)`?\s*$")
FIELD_RE = re.compile(r"(?im)^\s*([^:\n]+):\s*([^\n]*)$")


@dataclass(frozen=True)
class IntakeDiagnostic:
    code: str
    path: str
    message: str
    severity: str = "error"


def _fields(text: str) -> dict[str, str]:
    return {key.strip().lower(): value.strip() for key, value in FIELD_RE.findall(text)}


def _field_value(text: str, label: str) -> str:
    return _fields(text).get(label.removesuffix(":").lower(), "")


def _canonical_stem(stem: str) -> str:
    return re.sub(r"^(\d{4}-\d{2}-\d{2}-)?captured-", r"\1", stem, flags=re.I)


def _is_fixture(path: Path, text: str) -> bool:
    lowered = f"{path.name}\n{text}".lower()
    return "fixture" in lowered and ("gated" in lowered or "synthetic" in lowered)


def _local_links(path: Path) -> list[IntakeDiagnostic]:
    diagnostics: list[IntakeDiagnostic] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for target in LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip().strip("<>")
        if not target or target.startswith(("http:", "https:", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            diagnostics.append(IntakeDiagnostic("intake-link-missing", path.as_posix(), f"local link target does not exist: {target}"))
    return diagnostics


def _metadata_diagnostics(path: Path, text: str, *, require_receipt: bool = False) -> list[IntakeDiagnostic]:
    diagnostics: list[IntakeDiagnostic] = []
    fields = _fields(text)
    tier = fields.get("intake tier", "").lower()
    if tier and tier not in INTAKE_TIERS:
        diagnostics.append(IntakeDiagnostic("intake-tier-invalid", str(path), f"unsupported intake tier: {tier}"))
    status = fields.get("current status", "").lower().split()[0] if fields.get("current status") else ""
    if status and status not in RETENTION_STATUSES:
        diagnostics.append(IntakeDiagnostic("intake-retention-status-invalid", str(path), f"unsupported retention status: {status}"))
    if status in RETENTION_STATUSES:
        missing = [label for label in RETENTION_FIELDS if not fields.get(label.removesuffix(":").lower())]
        if missing:
            diagnostics.append(IntakeDiagnostic("intake-retention-fields-missing", str(path), f"retained source is missing: {', '.join(missing)}"))
    outcome = fields.get("outcome after review", "").lower()
    if outcome and outcome not in FEEDBACK_OUTCOMES:
        diagnostics.append(IntakeDiagnostic("intake-feedback-outcome-invalid", str(path), f"unsupported downstream outcome: {outcome}"))
    if require_receipt or fields.get("research question"):
        missing = [label for label in RECEIPT_FIELDS if not fields.get(label.removesuffix(":").lower())]
        if missing:
            diagnostics.append(IntakeDiagnostic("intake-receipt-fields-missing", str(path), f"material receipt is missing: {', '.join(missing)}"))
    return diagnostics


def validate_lane(lane: str | Path) -> list[IntakeDiagnostic]:
    root = Path(lane).resolve()
    diagnostics: list[IntakeDiagnostic] = []
    required_dirs = ("transcripts", "source-notes", "analyses")
    for name in required_dirs:
        if not (root / name).is_dir():
            diagnostics.append(IntakeDiagnostic("intake-directory-missing", str(root / name), "required intake directory is missing"))
    if diagnostics:
        return diagnostics

    transcript_paths = {p.stem: p for p in (root / "transcripts").glob("*.md")}
    note_paths = {p.name.removesuffix(".source-note.md"): p for p in (root / "source-notes").glob("*.source-note.md")}
    analysis_paths = {p.name.removesuffix(".analysis.md"): p for p in (root / "analyses").glob("*.analysis.md")}
    transcripts = {_canonical_stem(stem): (stem, path) for stem, path in transcript_paths.items()}
    notes = {_canonical_stem(stem): (stem, path) for stem, path in note_paths.items()}
    analyses = {_canonical_stem(stem): (stem, path) for stem, path in analysis_paths.items()}

    for source_id, (original_stem, path) in sorted(transcripts.items()):
        text = path.read_text(encoding="utf-8", errors="replace")
        fixture = _is_fixture(path, text)
        if source_id not in notes:
            diagnostics.append(IntakeDiagnostic("intake-source-note-missing", str(path), f"no matching source note for {source_id}"))
        if source_id not in analyses:
            diagnostics.append(IntakeDiagnostic("intake-analysis-missing", str(path), f"no matching analysis for {source_id}"))
        lowered = text.lower()
        if not fixture and (("rights status" not in lowered and "rights_status" not in lowered) or not any(marker in lowered for marker in RIGHTS_MARKERS)):
            diagnostics.append(IntakeDiagnostic("intake-rights-metadata-missing", str(path), "transcript must state controlled rights status and handling"))
        diagnostics.extend(_metadata_diagnostics(path, text))
        diagnostics.extend(_local_links(path))

    for source_id, (original_stem, path) in sorted(notes.items()):
        text = path.read_text(encoding="utf-8", errors="replace")
        if source_id not in transcripts:
            diagnostics.append(IntakeDiagnostic("intake-transcript-missing", str(path), f"no matching transcript for {source_id}"))
        if "rights status" not in text.lower() and "rights_status" not in text.lower():
            diagnostics.append(IntakeDiagnostic("intake-source-note-rights-missing", str(path), "source note must include Rights status"))
        diagnostics.extend(_metadata_diagnostics(path, text))
        diagnostics.extend(_local_links(path))

    ledger_paths = list(root.glob("*ledger.md")) + list(root.glob("research-ledger.md"))
    ledger_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in ledger_paths)
    for source_id, (original_stem, path) in sorted(analyses.items()):
        text = path.read_text(encoding="utf-8", errors="replace")
        fixture = _is_fixture(path, text)
        if source_id not in transcripts:
            diagnostics.append(IntakeDiagnostic("intake-transcript-missing", str(path), f"no matching transcript for {source_id}"))
        if not fixture and not all(field in text for field in DECISION_COMPRESSION_FIELDS):
            diagnostics.append(IntakeDiagnostic("intake-decision-compression-incomplete", str(path), "analysis is missing one or more Decision Compression fields"))
        dispositions = [item.lower() for item in STRUCTURED_DISPOSITION_RE.findall(text)]
        invalid = [item for item in dispositions if item not in DISPOSITIONS]
        if invalid:
            diagnostics.append(IntakeDiagnostic("intake-disposition-invalid", str(path), f"unsupported ROI disposition(s): {', '.join(invalid)}"))
        if "lane-test-ready" in dispositions and not all(any(field in text for field in aliases) for aliases in REQUIRED_PACKET_FIELDS):
            diagnostics.append(IntakeDiagnostic("intake-routing-packet-incomplete", str(path), "lane-test-ready analysis is missing one or more routing-packet fields"))
        if not fixture and not any(candidate in ledger_text for candidate in (source_id, original_stem)):
            diagnostics.append(IntakeDiagnostic("intake-ledger-link-missing", str(path), "canonical source ID is not present in the lane ledger"))
        diagnostics.extend(_metadata_diagnostics(path, text))
        diagnostics.extend(_local_links(path))
    return sorted(diagnostics, key=lambda item: (item.path, item.code, item.message))
