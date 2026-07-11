from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SENSITIVE_RULES = {
    "professional review required": (
        "tax",
        "legal",
        "payroll",
        "withholding",
        "attorney",
        "cpa",
        "insurance",
        "medical",
        "compliance",
    ),
    "approval required": (
        "child",
        "family",
        "donor",
        "project transcript",
        "project message",
        "pricing",
        "margin",
        "spending",
        "property access",
        "security",
        "external claim",
        "board",
    ),
    "keep local": (
        "identity",
        "private",
        "sensitive",
        "exact vulnerability",
        "personal information",
    ),
}

PRIMITIVE_WORDS = (
    "cadence",
    "review",
    "evidence",
    "gate",
    "checklist",
    "guardrail",
    "loop",
    "risk",
    "approval",
    "template",
    "quality",
)


@dataclass
class PatternCandidate:
    source_lane: str
    receiving_lane: str
    transfer_candidate: str
    classification: str
    reason: str
    safe_transformed_version: str
    required_approval: str


def classify_text(text: str) -> tuple[str, str, str]:
    lowered = text.lower()
    for classification, words in SENSITIVE_RULES.items():
        for word in words:
            if word in lowered:
                approval = "professional review" if classification == "professional review required" else "owner/operator"
                return classification, f"Matched sensitive membrane term: {word}", approval
    if any(word in lowered for word in PRIMITIVE_WORDS):
        return "translate first", "Looks like a reusable operating primitive, but project context should be stripped.", "none"
    return "translate first", "Candidate needs review before reuse.", "none"


def extract_patterns(projects_path: str | Path) -> list[PatternCandidate]:
    root = Path(projects_path)
    candidates: list[PatternCandidate] = []
    for readme in sorted(root.glob("*/README.md")):
        lane = readme.parent.name
        text = readme.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip(" -\t")
            if not stripped or len(stripped) < 18:
                continue
            if any(word in stripped.lower() for word in PRIMITIVE_WORDS):
                classification, reason, approval = classify_text(stripped)
                candidates.append(
                    PatternCandidate(
                        source_lane=lane,
                        receiving_lane="shared primitives",
                        transfer_candidate=stripped,
                        classification=classification,
                        reason=reason,
                        safe_transformed_version=make_safe_version(stripped),
                        required_approval=approval,
                    )
                )
    return candidates


def make_safe_version(text: str) -> str:
    replacements = {
        "Grace Gems": "the project",
        "Mountain Villa": "the project",
        "Book Club": "the project",
        "Learning Core": "the project",
        "Media Production": "the project",
    }
    safe = text
    for source, target in replacements.items():
        safe = safe.replace(source, target)
    return safe


def render_pattern_report(candidates: list[PatternCandidate]) -> str:
    lines = [
        "# Cross-Project Pattern Candidates",
        "",
        "Review-only report. Do not auto-promote these candidates into shared templates without human membrane review.",
        "",
    ]
    for candidate in candidates:
        lines.extend(
            [
                "## Candidate",
                "",
                f"Source lane: {candidate.source_lane}",
                "",
                f"Receiving lane: {candidate.receiving_lane}",
                "",
                f"Transfer candidate: {candidate.transfer_candidate}",
                "",
                f"Membrane classification: {candidate.classification}",
                "",
                f"Reason: {candidate.reason}",
                "",
                f"Safe transformed version: {candidate.safe_transformed_version}",
                "",
                f"Required approval: {candidate.required_approval}",
                "",
            ]
        )
    return "\n".join(lines)
