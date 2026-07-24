from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


DISPOSITIONS = {"primitive-candidate", "needs-verification", "lane-test-ready", "worldview-only", "preserved"}
REQUIRED_PACKET_FIELDS = (
    ("Source episode:", "Source interview:"),
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
LINK_RE = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
DISPOSITION_RE = re.compile(r"(?:ROI disposition|Disposition)\s*:\s*`?([a-z-]+)`?", re.I)


@dataclass(frozen=True)
class IntakeDiagnostic:
    code: str
    path: str
    message: str
    severity: str = "error"


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


def validate_lane(lane: str | Path) -> list[IntakeDiagnostic]:
    root = Path(lane).resolve()
    diagnostics: list[IntakeDiagnostic] = []
    required_dirs = ("transcripts", "source-notes", "analyses")
    for name in required_dirs:
        if not (root / name).is_dir():
            diagnostics.append(IntakeDiagnostic("intake-directory-missing", str(root / name), "required intake directory is missing"))
    if diagnostics:
        return diagnostics

    transcripts = {p.stem: p for p in (root / "transcripts").glob("*.md")}
    notes = {p.name.removesuffix(".source-note.md"): p for p in (root / "source-notes").glob("*.source-note.md")}
    analyses = {p.name.removesuffix(".analysis.md"): p for p in (root / "analyses").glob("*.analysis.md")}
    for stem, path in sorted(transcripts.items()):
        if stem not in notes:
            diagnostics.append(IntakeDiagnostic("intake-source-note-missing", str(path), f"no matching source note for {stem}"))
        if stem not in analyses:
            diagnostics.append(IntakeDiagnostic("intake-analysis-missing", str(path), f"no matching analysis for {stem}"))
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        if "rights" not in text or "internal" not in text:
            diagnostics.append(IntakeDiagnostic("intake-rights-metadata-missing", str(path), "transcript must state rights status and internal handling"))
        diagnostics.extend(_local_links(path))
    for stem, path in sorted(notes.items()):
        if stem not in transcripts:
            diagnostics.append(IntakeDiagnostic("intake-transcript-missing", str(path), f"no matching transcript for {stem}"))
        if "rights status" not in path.read_text(encoding="utf-8", errors="replace").lower():
            diagnostics.append(IntakeDiagnostic("intake-source-note-rights-missing", str(path), "source note must include Rights status"))
        diagnostics.extend(_local_links(path))
    ledger_candidates = list(root.glob("*ledger.md")) + list(root.glob("research-ledger.md"))
    ledger_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in ledger_candidates)
    for stem, path in sorted(analyses.items()):
        if stem not in transcripts:
            diagnostics.append(IntakeDiagnostic("intake-transcript-missing", str(path), f"no matching transcript for {stem}"))
        text = path.read_text(encoding="utf-8", errors="replace")
        if not all(field in text for field in DECISION_COMPRESSION_FIELDS):
            diagnostics.append(IntakeDiagnostic("intake-decision-compression-incomplete", str(path), "analysis is missing one or more Decision Compression fields"))
        dispositions = [item.lower() for item in DISPOSITION_RE.findall(text)]
        invalid = [item for item in dispositions if item not in DISPOSITIONS]
        if invalid:
            diagnostics.append(IntakeDiagnostic("intake-disposition-invalid", str(path), f"unsupported ROI disposition(s): {', '.join(invalid)}"))
        if "lane-test-ready" in dispositions and not all(any(field in text for field in aliases) for aliases in REQUIRED_PACKET_FIELDS):
            diagnostics.append(IntakeDiagnostic("intake-routing-packet-incomplete", str(path), "lane-test-ready analysis is missing one or more routing-packet fields"))
        if stem not in ledger_text:
            diagnostics.append(IntakeDiagnostic("intake-ledger-link-missing", str(path), "analysis stem is not present in the lane ledger"))
        diagnostics.extend(_local_links(path))
    return sorted(diagnostics, key=lambda item: (item.path, item.code, item.message))
