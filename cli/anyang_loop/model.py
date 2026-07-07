from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "signal",
    "memory_objects",
    "decision",
    "action",
    "evidence",
    "cadence",
    "learning_update",
    "governance_boundary",
)

FIELD_ALIASES = {
    "signal": "signal",
    "memory object": "memory_objects",
    "memory objects": "memory_objects",
    "memory_objects": "memory_objects",
    "decision": "decision",
    "decision prepared": "decision",
    "action": "action",
    "action path": "action",
    "evidence": "evidence",
    "evidence required": "evidence",
    "cadence": "cadence",
    "review cadence": "cadence",
    "learning update": "learning_update",
    "learning_update": "learning_update",
    "governance boundary": "governance_boundary",
    "governance_boundary": "governance_boundary",
}

VALID_LOOP_TYPES = {"operating", "governance", "learning", "recursive"}


@dataclass
class Diagnostic:
    code: str
    message: str
    level: str = "warning"


@dataclass
class LoopDefinition:
    name: str
    signal: str
    memory_objects: list[str]
    decision: str
    action: str
    evidence: str
    cadence: str
    learning_update: str
    governance_boundary: str
    description: str = ""
    loop_type: str = "operating"
    customer_lane: str = ""
    authority: str = "human"
    source_path: str = ""
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, data: dict[str, Any], source_path: str = "") -> "LoopDefinition":
        normalized: dict[str, Any] = {}
        for key, value in data.items():
            canonical = normalize_field_name(str(key))
            normalized[canonical] = value

        name = str(normalized.get("name") or infer_name_from_source(source_path)).strip()
        loop_type = str(normalized.get("loop_type") or normalized.get("type") or "operating").strip().lower()
        if loop_type not in VALID_LOOP_TYPES:
            loop_type = "operating"

        return cls(
            name=name,
            description=coerce_text(normalized.get("description", "")),
            loop_type=loop_type,
            customer_lane=coerce_text(normalized.get("customer_lane", "")),
            authority=coerce_text(normalized.get("authority", "human")) or "human",
            source_path=source_path,
            tags=coerce_list(normalized.get("tags", [])),
            signal=coerce_text(normalized.get("signal", "")),
            memory_objects=coerce_list(normalized.get("memory_objects", [])),
            decision=coerce_text(normalized.get("decision", "")),
            action=coerce_text(normalized.get("action", "")),
            evidence=coerce_text(normalized.get("evidence", "")),
            cadence=coerce_text(normalized.get("cadence", "")),
            learning_update=coerce_text(normalized.get("learning_update", "")),
            governance_boundary=coerce_text(normalized.get("governance_boundary", "")),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "loop_type": self.loop_type,
            "customer_lane": self.customer_lane,
            "authority": self.authority,
            "source_path": self.source_path,
            "tags": self.tags,
            "signal": self.signal,
            "memory_objects": self.memory_objects,
            "decision": self.decision,
            "action": self.action,
            "evidence": self.evidence,
            "cadence": self.cadence,
            "learning_update": self.learning_update,
            "governance_boundary": self.governance_boundary,
        }


def normalize_field_name(name: str) -> str:
    compact = name.strip().lower().replace("-", " ").replace("_", " ")
    compact = " ".join(compact.split())
    return FIELD_ALIASES.get(compact, compact.replace(" ", "_"))


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(coerce_text(item) for item in value if coerce_text(item))
    if isinstance(value, dict):
        return "; ".join(f"{key}: {coerce_text(item)}" for key, item in value.items())
    return str(value).strip()


def coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [coerce_text(item) for item in value if coerce_text(item)]
    text = coerce_text(value)
    if not text:
        return []
    lines = [line.strip(" -\t") for line in text.splitlines()]
    return [line for line in lines if line]


def infer_name_from_source(source_path: str) -> str:
    if not source_path:
        return "untitled-loop"
    return Path(source_path).stem.replace("_", "-")

