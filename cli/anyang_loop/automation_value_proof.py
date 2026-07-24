from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .privacy_scan import scan_text


REQUIRED_FIELDS = {
    "Recurring constraint": "missing-recurring-constraint",
    "Baseline measurement": "missing-baseline",
    "Target metric": "missing-target-metric",
    "Approved inputs and tools": "missing-approved-inputs",
    "Human owner": "missing-human-owner",
    "Approval boundary": "missing-approval-boundary",
    "Representative test cases": "missing-test-cases",
    "Exception behavior": "missing-exception-plan",
    "Before/after evidence": "missing-before-after-evidence",
    "Review burden": "missing-review-burden",
    "Unresolved uncertainty": "missing-uncertainty",
    "Completion receipt": "missing-completion-receipt",
}
PLACEHOLDER_RE = re.compile(r"(?i)(?:\[\s*(?:fill|describe|name|add|待填)\s*\]|<[^>]+>|TODO|TBD|unknown)$")
VALUE_CLAIM_RE = re.compile(r"(?i)\b(?:(?:\d+(?:\.\d+)?|zero|one|two|three|four|five|six|seven|eight|nine|ten)\s*(?:hours?|minutes?|%|percent)|\$\s*\d[\d,.]*|time saved|money made|cost saved|hours saved)\b")
PRIVATE_PATH_RE = re.compile(r"(?i)(?:tenant-private|customer-private|raw-customer-transcripts|migration-backups|\.codex-tmp)")


@dataclass(frozen=True)
class ValueProofDiagnostic:
    code: str
    line: int | None
    message: str


def _field_value(lines: list[str], field: str) -> tuple[str | None, int | None]:
    prefix = f"- {field}:"
    for index, line in enumerate(lines):
        if line.strip().lower().startswith(prefix.lower()):
            return line.split(":", 1)[1].strip(), index + 1
    return None, None


def _is_empty(value: str | None) -> bool:
    if value is None or not value.strip():
        return True
    return value.strip().lower() in {"none", "n/a", "not applicable"} or bool(PLACEHOLDER_RE.search(value.strip()))


def validate_value_proof_text(text: str) -> list[ValueProofDiagnostic]:
    lines = text.splitlines()
    diagnostics: list[ValueProofDiagnostic] = []
    for field, code in REQUIRED_FIELDS.items():
        value, line = _field_value(lines, field)
        if _is_empty(value):
            diagnostics.append(ValueProofDiagnostic(code, line, f"{field} must be completed."))

    claims = [index + 1 for index, line in enumerate(lines) if VALUE_CLAIM_RE.search(line)]
    baseline, baseline_line = _field_value(lines, "Baseline measurement")
    evidence, evidence_line = _field_value(lines, "Before/after evidence")
    if claims and (_is_empty(baseline) or _is_empty(evidence)):
        diagnostics.append(
            ValueProofDiagnostic(
                "unsupported-quantitative-claim",
                claims[0],
                "Quantitative value claims require a completed baseline measurement and before/after evidence.",
            )
        )

    private_lines = [index + 1 for index, line in enumerate(lines) if PRIVATE_PATH_RE.search(line)]
    if private_lines:
        diagnostics.append(
            ValueProofDiagnostic(
                "private-data-route",
                private_lines[0],
                "Private/customer source paths must remain outside the repo-tracked proof packet.",
            )
        )

    for rule in scan_text(text):
        diagnostics.append(
            ValueProofDiagnostic("privacy-rule", None, f"Proof packet triggers repository privacy rule: {rule}.")
        )
    return diagnostics


def validate_value_proof(path: str | Path) -> list[ValueProofDiagnostic]:
    source = Path(path)
    if not source.exists():
        return [ValueProofDiagnostic("missing-file", None, f"Proof packet does not exist: {source}")]
    return validate_value_proof_text(source.read_text(encoding="utf-8"))
