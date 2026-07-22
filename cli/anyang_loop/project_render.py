from __future__ import annotations

import html
from pathlib import Path

import yaml

from .project_model import ProjectInput
from .model import LoopDefinition
from .render import render_loop


def build_project_files(spec: ProjectInput) -> dict[str, str]:
    loops = build_loops(spec)
    files = {
        "README.md": render_readme(spec),
        "executive-os-install.md": render_project_doc(spec),
        "risk-register.md": render_risk_register(spec),
        "decision-log.md": render_decision_log(spec),
        "operating-review.md": render_operating_review(spec),
        "30-day-plan.md": render_30_day_plan(spec),
        "membrane-notes.md": render_membrane_notes(spec),
    }
    for loop in loops:
        files[f"loop-examples/{loop.name}.yaml"] = yaml.safe_dump(loop.as_dict(), sort_keys=False, allow_unicode=True)
    return files


def build_loops(spec: ProjectInput) -> list[LoopDefinition]:
    memory = spec.memory_objects or ["Context map", "Decisions", "Risks", "Follow-ups", "Lessons learned"]
    decisions = spec.decisions or ["Next-cycle priority decision", "Risk or escalation decision"]
    governance = spec.governance_boundary or "Humans approve commitments, external communications, spending, and domain-sensitive decisions."
    return [
        LoopDefinition(
            name=f"{spec.slug}-operating-loop",
            description=f"Primary operating loop for {spec.name}.",
            loop_type="operating",
            project_lane=spec.slug,
            authority="human leadership",
            tags=["generated", "operating"],
            signal=f"A meaningful change, open question, or review window appears in {spec.name}.",
            memory_objects=memory,
            decision=f"Prepare structured options for: {decisions[0]}.",
            action="After human approval, update owners, next actions, deadlines, and operating records.",
            evidence="Operating review, decision log update, owner approval, metric, artifact, or source note.",
            cadence=spec.primary_cadence,
            learning_update="Preserve what changed, what surprised the operator, and what should update next cycle memory.",
            governance_boundary=governance,
        ),
        LoopDefinition(
            name=f"{spec.slug}-governance-loop",
            description=f"Authority and risk boundary loop for {spec.name}.",
            loop_type="governance",
            project_lane=spec.slug,
            authority="human approval",
            tags=["generated", "governance"],
            signal=f"A decision touches {spec.primary_risk}, sensitive information, spending, external claims, or professional judgment.",
            memory_objects=["Governance boundary", "Risk register", "Approval record", "Evidence requirements"],
            decision="Decide whether the item can proceed, needs approval, needs professional review, or must stay local.",
            action="Hold, approve, revise, escalate, or prepare professional-review questions after human review.",
            evidence="Approval record, risk register update, source note, professional-review question, or hold decision.",
            cadence="Event-driven before high-stakes action, plus review during the operating cadence.",
            learning_update="Update governance notes and risk memory when a boundary prevents drift or needs tightening.",
            governance_boundary=governance,
        ),
        LoopDefinition(
            name=f"{spec.slug}-learning-loop",
            description=f"Learning loop for improving {spec.name} over time.",
            loop_type="learning",
            project_lane=spec.slug,
            authority="human leadership",
            tags=["generated", "learning"],
            signal="An operating review, outcome, surprise, mistake, or useful pattern appears.",
            memory_objects=["Expected outcome", "Actual outcome", "Surprises", "Lessons", "Changed risks"],
            decision="Decide what Executive Council should remember, change, preserve, or stop doing next cycle.",
            action="Update memory, templates, risk register, decision log, or review questions after human approval.",
            evidence="Lesson learned, review note, changed template, risk update, decision record, or artifact.",
            cadence=spec.primary_cadence,
            learning_update="Convert outcomes into updated memory and candidate reusable primitives after membrane review.",
            governance_boundary="Humans decide whether lessons become project state or reusable Executive Council primitives.",
        ),
    ]


def render_readme(spec: ProjectInput) -> str:
    return f"""# {spec.name}

{spec.name} is a project installation for the Anyang Intelligence Executive Council.

## Domain

{spec.domain_description}

## Executive Council Role

Executive Council acts as the governed operating layer for this context. Its job is to {spec.executive_os_job}.

Executive Council does not replace human authority. It prepares decisions, coordinates execution, preserves memory, and keeps the operating context learning.

## Operating Thesis

{spec.name} should be managed as a living loop of context, decision, action, evidence, review, and learning.

## Installation

See [executive-os-install.md](executive-os-install.md) for the generated Executive Council installation. The filename remains a compatibility alias.

Use [membrane-notes.md](membrane-notes.md) before transferring lessons from this project lane into another lane.
"""


def render_project_doc(spec: ProjectInput) -> str:
    memory = bullet_list(spec.memory_objects or ["Context map", "Decisions", "Risks", "Follow-ups", "Lessons learned"])
    decisions = bullet_list(spec.decisions or ["Recurring operating decisions", "High-consequence decisions", "Risk or escalation decisions"])
    success = bullet_list(spec.success_criteria or [
        "Context is easier to reconstruct.",
        "Decisions are clearer.",
        "Follow-ups are less likely to disappear.",
        "Risks are visible earlier.",
        "Reviews are useful enough to repeat.",
        "The operating context learns from its own outcomes.",
    ])
    return f"""# {spec.name} Executive Council Installation

## Purpose

Install Executive Council, developed by Anyang Intelligence, for {spec.name}.

The system should help leadership coordinate {spec.domain_description} while preserving human authority and domain-specific safeguards.

## Council Mandate

Executive Council should behave like the governed operating layer of the operating context:

- See the whole operating context.
- Maintain memory, risks, decisions, owners, and follow-ups.
- Clarify decisions and priorities.
- Coordinate owners, deadlines, workflows, communications, and reviews.
- Surface risks, blockers, gaps, and opportunities.
- Turn signals and outcomes into learning and next actions.

## Context Map

{context_table(spec.context_map)}

## Executive Memory Objects

{memory}

## Decision System

Executive Council should prepare structured decisions for:

{decisions}

## Operating Review Cadence

Primary cadence: **{spec.primary_cadence}**.

The review should answer:

- What changed?
- What is open?
- What is blocked?
- What risks are rising?
- What decisions are needed?
- What should happen next?

## Risk and Governance Boundary

{spec.governance_boundary or "Humans retain authority over commitments, external communication, spending, legal, financial, educational, safety-sensitive, and professional-review decisions."}

Executive Council may organize context, draft reviews, surface risks, recommend options, and preserve lessons.

Executive Council may not make binding commitments, send external communications, approve spending, replace professional judgment, or expose sensitive information beyond approved access rules.

## 30-Day Installation Plan

See [30-day-plan.md](30-day-plan.md).

## Success Criteria

{success}

## Human Authority

Executive Council recommends, organizes, and prepares. Humans retain final authority over domain-specific decisions, approvals, commitments, communications, and external claims.
"""


def render_risk_register(spec: ProjectInput) -> str:
    rows = "\n".join(f"| {risk} | Operating | TBD | TBD | Human owner | Define mitigation and evidence | {spec.primary_cadence} |" for risk in (spec.risks or [spec.primary_risk]))
    return f"""# {spec.name} Risk Register

| Risk | Area | Severity | Likelihood | Owner | Mitigation | Review date |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## Risk Areas

- Strategy.
- Finance.
- Project.
- Product.
- Operations.
- People.
- Legal or compliance.
- Security.
- Domain-specific safety or authority.
"""


def render_decision_log(spec: ProjectInput) -> str:
    return f"""# {spec.name} Decision Log

| Date | Decision | Owner | Status | Review date | Source memo |
| --- | --- | --- | --- | --- | --- |
|  |  |  | Proposed |  |  |

## Status Values

- Proposed.
- Approved.
- Rejected.
- Deferred.
- Reversed.
- Superseded.
"""


def render_operating_review(spec: ProjectInput) -> str:
    return f"""# {spec.name}: Where Changed Evidence Alters the Next Decision

Title rationale: This review makes the operating change and its decision consequence visible before the supporting detail.

## Review Date

Record the review date and evidence window.

## Lead Judgment

State what changed, why it matters, the mechanism producing the change, and the decision consequence.

## Controlling Object

Name the contested relationship or threshold this review is waiting to resolve.

## The Evidence That Changed the Operating Picture

- Record the strongest dated change and its evidence pointer.

## Metrics Narrative


## Active Priorities

| Priority | Owner | Status | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## Open Decisions

| Decision | Owner | Needed by | Status |
| --- | --- | --- | --- |
|  |  |  |  |

Decision question: Does the changed evidence justify revising the current priority without outrunning the authority or evidence boundary?

## Blockers

| Blocker | Owner | Dependency | Next action |
| --- | --- | --- | --- |
|  |  |  |  |

## Risks

| Risk | Owner | Change since last review | Next action |
| --- | --- | --- | --- |
| {spec.primary_risk} | Human owner | TBD | Define mitigation |

## Follow-Ups

| Action | Owner | Due date |
| --- | --- | --- |
|  |  |  |

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Unknown—required operating evidence has not yet been entered | Keep the next decision provisional | Name the receipt, metric, approval, or observation needed |
"""


def render_30_day_plan(spec: ProjectInput) -> str:
    return f"""# {spec.name} 30-Day Installation Plan

## Week 1: Context and Source Map

- Capture the operating context.
- Identify where truth currently lives.
- Define access rules and sensitive boundaries.
- Create the first context map.

## Week 2: Memory and Decisions

- Define executive memory objects.
- Create the initial decision log.
- Run one real decision through the system.

## Week 3: Review and Governance

- Install the operating review cadence.
- Define governance boundaries.
- Identify top risks, blockers, or open loops.

## Week 4: First Learning Loop

- Run the first operating review.
- Record what changed.
- Capture lessons learned.
- Set next-cycle priorities.
"""


def render_membrane_notes(spec: ProjectInput) -> str:
    sources = ", ".join(spec.source_projects) if spec.source_projects else "none declared"
    return f"""# {spec.name} Membrane Notes

Use [../../docs/membranes.md](../../docs/membranes.md) before transferring lessons, facts, templates, claims, or operating patterns from this project lane into another lane.

## Source Projects Considered

{sources}

## Shareable Primitives

- Loop structures.
- Review questions.
- Evidence standards.
- Risk patterns.
- Governance checklists.
- Cadence lessons.

## Keep Local Unless Approved

- Private facts.
- Sensitive records.
- Project identities or private messages.
- Financial details.
- Legal, tax, educational, safety, property, donor, contractor, or compliance-sensitive context.
- Draft claims not approved for external use.

## Required Transfer Filter

- Translate project-specific facts into generic primitives before reuse.
- Preserve human authority boundaries and evidence requirements.
- Use the strictest applicable membrane when sensitive content appears.
"""


def render_obsidian(spec: ProjectInput) -> dict[str, str]:
    files = build_project_files(spec)
    rendered: dict[str, str] = {}
    for path, content in files.items():
        obsidian_path = path.replace(".md", ".md").replace("loop-examples/", "Loops/")
        rendered[obsidian_path] = "#project-install #anyang-intelligence\n\n[[Membranes]] [[Governance]]\n\n" + content
    rendered["Index.md"] = f"# {spec.name} Vault Index\n\n- [[README]]\n- [[executive-os-install]]\n- [[30-day-plan]]\n- [[membrane-notes]]\n"
    return rendered


def render_html_dashboard(spec: ProjectInput) -> str:
    loops = build_loops(spec)
    risk_items = "".join(f"<li>{html.escape(risk)}</li>" for risk in (spec.risks or [spec.primary_risk]))
    loop_items = "".join(f"<li><strong>{html.escape(loop.name)}</strong>: {html.escape(loop.loop_type)} - {html.escape(loop.cadence)}</li>" for loop in loops)
    context_rows = "".join(f"<tr><th>{html.escape(key)}</th><td>{html.escape(value)}</td></tr>" for key, value in spec.context_map.items())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(spec.name)} Executive Council Dashboard</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 920px; margin: 40px auto; line-height: 1.5; color: #1f2a24; }}
    h1, h2 {{ color: #143d2b; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #c8d6ce; padding: 8px; text-align: left; }}
    .warning {{ background: #fff4d6; border-left: 4px solid #c58b13; padding: 12px; }}
  </style>
</head>
<body>
  <h1>{html.escape(spec.name)} Executive Council Dashboard</h1>
  <p>{html.escape(spec.domain_description)}</p>
  <div class="warning">Human authority remains final. Use membrane review before transferring project lessons.</div>
  <h2>Context Map</h2>
  <table>{context_rows}</table>
  <h2>Loops</h2>
  <ul>{loop_items}</ul>
  <h2>Risks</h2>
  <ul>{risk_items}</ul>
  <h2>Cadence</h2>
  <p>{html.escape(spec.primary_cadence)}</p>
</body>
</html>
"""


def write_files(files: dict[str, str], output_dir: Path, force: bool = False) -> None:
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise FileExistsError(f"Output directory already exists and is not empty: {output_dir}")
    for relative, content in files.items():
        target = output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def context_table(context: dict[str, str]) -> str:
    rows = "\n".join(f"| {key} | {value} |" for key, value in context.items())
    return f"| Field | Current starting point |\n| --- | --- |\n{rows}"


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
