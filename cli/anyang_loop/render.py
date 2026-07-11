from __future__ import annotations

import json
from typing import Any

import yaml

from .model import LoopDefinition


def render_loop(loop: LoopDefinition, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(loop.as_dict(), indent=2) + "\n"
    if output_format == "obsidian":
        return render_obsidian(loop)
    if output_format == "markdown":
        return render_markdown(loop)
    if output_format == "yaml":
        return yaml.safe_dump(loop.as_dict(), sort_keys=False, allow_unicode=True)
    raise ValueError(f"Unsupported export format: {output_format}")


def render_markdown(loop: LoopDefinition) -> str:
    tags = ", ".join(loop.tags)
    memory = "\n".join(f"- {item}" for item in loop.memory_objects)
    return f"""# {loop.name}

{loop.description}

| Field | Value |
| --- | --- |
| Loop type | {loop.loop_type} |
| Project lane | {loop.project_lane} |
| Authority | {loop.authority} |
| Tags | {tags} |

## Signal

{loop.signal}

## Memory Objects

{memory}

## Decision

{loop.decision}

## Action

{loop.action}

## Evidence

{loop.evidence}

## Cadence

{loop.cadence}

## Learning Update

{loop.learning_update}

## Governance Boundary

{loop.governance_boundary}
"""


def render_obsidian(loop: LoopDefinition) -> str:
    tags = ["anyang-loop", loop.loop_type, *loop.tags]
    clean_tags = " ".join(f"#{tag.replace(' ', '-')}" for tag in tags if tag)
    body = render_markdown(loop)
    return f"{clean_tags}\n\n> Loop authority: [[Governance]] remains human-led. Use [[Membranes]] before cross-lane transfer.\n\n{body}"


def template_loop(name: str, loop_type: str) -> LoopDefinition:
    return LoopDefinition(
        name=name,
        description="Starter loop definition. Replace bracketed text before treating this loop as operational.",
        loop_type=loop_type,
        project_lane="[project or shared]",
        authority="human approval required",
        tags=[loop_type],
        signal="[What starts this loop?]",
        memory_objects=[
            "[Fact, object, commitment, risk, or prior decision]",
            "[Open loop or source surface]",
        ],
        decision="[What judgment should the Executive OS prepare for a human?]",
        action="[What changes in the world after human approval?]",
        evidence="[What receipt, approval, artifact, metric, or record proves it happened?]",
        cadence="[Daily, weekly, monthly, seasonal, or event-driven review rhythm]",
        learning_update="[What lesson, memory object, template, skill, or guardrail changes next cycle?]",
        governance_boundary="[Who must approve? What may the system not do on its own?]",
    )


def loop_to_yaml_data(loop: LoopDefinition) -> dict[str, Any]:
    return loop.as_dict()
