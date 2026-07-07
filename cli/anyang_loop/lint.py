from __future__ import annotations

from .model import REQUIRED_FIELDS, Diagnostic, LoopDefinition


CADENCE_WORDS = (
    "daily",
    "weekly",
    "monthly",
    "seasonal",
    "event",
    "review",
    "cadence",
    "when",
)
AUTHORITY_WORDS = (
    "human",
    "owner",
    "parent",
    "guardian",
    "board",
    "cpa",
    "bookkeeper",
    "attorney",
    "approval",
    "approve",
    "operator",
    "leadership",
)
HIGH_TRUST_WORDS = (
    "child",
    "learner",
    "family",
    "donor",
    "tax",
    "legal",
    "property",
    "customer",
    "pricing",
    "spending",
    "health",
    "safety",
    "nonprofit",
)


def validate_loop(loop: LoopDefinition) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    data = loop.as_dict()
    for field in REQUIRED_FIELDS:
        value = data[field]
        if isinstance(value, list):
            missing = not value
        else:
            missing = not str(value).strip()
        if missing:
            diagnostics.append(Diagnostic("missing-field", f"Missing required field: {field}", "error"))

    if loop.loop_type == "recursive" and "recursive" not in loop.learning_update.lower():
        diagnostics.append(Diagnostic("recursive-update", "Recursive loops should name how the system improves itself."))

    diagnostics.extend(lint_failure_modes(loop))
    return diagnostics


def lint_failure_modes(loop: LoopDefinition) -> list[Diagnostic]:
    text = " ".join(
        [
            loop.signal,
            " ".join(loop.memory_objects),
            loop.decision,
            loop.action,
            loop.evidence,
            loop.cadence,
            loop.learning_update,
            loop.governance_boundary,
        ]
    ).lower()
    diagnostics: list[Diagnostic] = []

    if "owner" not in text and "responsib" not in text and "authority" not in text:
        diagnostics.append(Diagnostic("open-loop-drift", "Loop may drift: no owner, responsibility, or authority language found."))

    if too_vague(loop.evidence) or not has_any(loop.evidence, ("receipt", "approval", "artifact", "metric", "memo", "review", "record", "evidence", "photo", "log")):
        diagnostics.append(Diagnostic("evidence-gap", "Evidence looks thin; name receipts, approvals, artifacts, metrics, or records."))

    if not has_any(loop.cadence, CADENCE_WORDS):
        diagnostics.append(Diagnostic("cadence-mismatch", "Cadence should name a rhythm such as daily, weekly, monthly, seasonal, or event-driven."))

    if not has_any(loop.governance_boundary, AUTHORITY_WORDS):
        diagnostics.append(Diagnostic("governance-bypass", "Governance boundary should name human authority or required approval."))

    if not has_any(loop.learning_update, ("memory", "record", "preserve", "update", "lesson", "learn", "template", "skill", "guardrail")):
        diagnostics.append(Diagnostic("memory-decay", "Learning update should say what gets preserved or updated in memory."))

    if len(loop.memory_objects) > 15 or len(text) > 5000:
        diagnostics.append(Diagnostic("overbuilt-loop", "Loop may be overbuilt; consider splitting or simplifying it."))

    if has_any(text, HIGH_TRUST_WORDS) and not has_any(loop.governance_boundary, AUTHORITY_WORDS):
        diagnostics.append(Diagnostic("underbuilt-loop", "High-trust context appears without a strong approval boundary."))

    if "friction" in text and not has_any(loop.learning_update, ("doc", "skill", "template", "guardrail", "checklist", "update")):
        diagnostics.append(Diagnostic("no-recursive-update", "Friction is named but no durable system update is specified."))

    return diagnostics


def has_errors(diagnostics: list[Diagnostic]) -> bool:
    return any(item.level == "error" for item in diagnostics)


def has_any(value: str, words: tuple[str, ...]) -> bool:
    value_lower = value.lower()
    return any(word in value_lower for word in words)


def too_vague(value: str) -> bool:
    compact = value.strip().lower()
    return len(compact) < 12 or compact in {"tbd", "none", "n/a", "unknown"}

