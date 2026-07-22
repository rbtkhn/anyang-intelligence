from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .model import coerce_list, coerce_text


class ProjectInputError(ValueError):
    """Raised when installer input is missing required structure."""


@dataclass
class ProjectInput:
    name: str
    domain_description: str
    context_map: dict[str, str]
    slug: str = ""
    memory_objects: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    cadence: str = ""
    risks: list[str] = field(default_factory=list)
    governance_boundary: str = ""
    success_criteria: list[str] = field(default_factory=list)
    source_projects: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "ProjectInput":
        required = ("name", "domain_description", "context_map")
        missing = [key for key in required if key not in data or not data[key]]
        if missing:
            raise ProjectInputError(f"Missing required install input fields: {', '.join(missing)}")
        context = data["context_map"]
        if not isinstance(context, dict):
            raise ProjectInputError("context_map must be a mapping.")
        name = coerce_text(data["name"])
        return cls(
            name=name,
            slug=coerce_text(data.get("slug")) or slugify(name),
            domain_description=coerce_text(data["domain_description"]),
            context_map={coerce_text(key): coerce_text(value) for key, value in context.items()},
            memory_objects=coerce_list(data.get("memory_objects")),
            decisions=coerce_list(data.get("decisions")),
            cadence=coerce_text(data.get("cadence")),
            risks=coerce_list(data.get("risks")),
            governance_boundary=coerce_text(data.get("governance_boundary")),
            success_criteria=coerce_list(data.get("success_criteria")),
            source_projects=coerce_list(data.get("source_projects")),
        )

    @property
    def primary_cadence(self) -> str:
        return self.cadence or self.context_map.get("Primary cadence", "Weekly operating review")

    @property
    def primary_risk(self) -> str:
        if self.risks:
            return self.risks[0]
        return self.context_map.get("Primary operating risk", "Operating drift")

    @property
    def executive_os_job(self) -> str:
        return self.context_map.get(
            "Executive Council job",
            self.context_map.get("Executive OS job", "Make context, decisions, risks, and learning easier to reconstruct"),
        )


def load_project_input(path: str | Path) -> ProjectInput:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ProjectInputError("Install input must be a YAML mapping.")
    return ProjectInput.from_mapping(data)


def slugify(value: str) -> str:
    chars: list[str] = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True
    return "".join(chars).strip("-") or "project"
