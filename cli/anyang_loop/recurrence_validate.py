from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DISPOSITIONS = {"watch", "verify", "preserve-candidate", "lane-test-ready", "drop"}
REQUIRED_FIELDS = ("Review ID:", "Review date:", "New source:", "Archive lane:", "Canonical ledger:", "Source identity and provenance:", "Rights status:", "## Seam review", "## Required next actions", "## Performance baseline")
SEAM_ROW_RE = re.compile(r"^\|\s*`?([^|`]+)`?\s*\|.*\|\s*(watch|verify|preserve-candidate|lane-test-ready|drop)\s*\|\s*$", re.I | re.M)

@dataclass(frozen=True)
class RecurrenceDiagnostic:
    code: str
    path: str
    message: str
    severity: str = "error"

def validate_packet(path: str | Path) -> list[RecurrenceDiagnostic]:
    packet = Path(path).resolve()
    if not packet.is_file():
        return [RecurrenceDiagnostic("recurrence-packet-missing", str(packet), "packet does not exist")]
    text = packet.read_text(encoding="utf-8", errors="replace")
    diagnostics = [RecurrenceDiagnostic("recurrence-field-missing", str(packet), f"required field missing: {field}") for field in REQUIRED_FIELDS if field not in text]
    rows = [(seam.strip(), disposition.lower()) for seam, disposition in SEAM_ROW_RE.findall(text) if seam.strip().lower() not in {"seam id", "---"}]
    if not rows:
        diagnostics.append(RecurrenceDiagnostic("recurrence-seams-missing", str(packet), "seam review contains no disposition rows"))
    seen: set[str] = set()
    for seam_id, disposition in rows:
        if seam_id in seen:
            diagnostics.append(RecurrenceDiagnostic("recurrence-seam-duplicate", str(packet), f"seam appears more than once: {seam_id}"))
        seen.add(seam_id)
        if disposition not in DISPOSITIONS:
            diagnostics.append(RecurrenceDiagnostic("recurrence-disposition-invalid", str(packet), f"unsupported disposition: {disposition}"))
    if "comparison minutes:" in text.lower() and "unavailable" not in text.lower():
        diagnostics.append(RecurrenceDiagnostic("recurrence-performance-unsubstantiated", str(packet), "performance fields must record measured values or unavailable"))
    diagnostics.extend(_local_links(packet))
    return sorted(diagnostics, key=lambda item: (item.path, item.code, item.message))

def _local_links(packet: Path) -> list[RecurrenceDiagnostic]:
    diagnostics = []
    for target in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", packet.read_text(encoding="utf-8", errors="replace")):
        target = target.split("#", 1)[0].strip().strip("<>")
        if target and not target.startswith(("http:", "https:", "mailto:")) and not (packet.parent / target).resolve().exists():
            diagnostics.append(RecurrenceDiagnostic("recurrence-link-missing", str(packet), f"local link target does not exist: {target}"))
    return diagnostics

def validate_directory(path: str | Path) -> list[RecurrenceDiagnostic]:
    root = Path(path).resolve()
    packets = sorted(root.glob("*.md"))
    if not packets:
        return [RecurrenceDiagnostic("recurrence-packets-missing", str(root), "no recurrence packets found")]
    return sorted((item for packet in packets for item in validate_packet(packet)), key=lambda item: (item.path, item.code, item.message))
