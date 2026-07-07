from __future__ import annotations

from .model import LoopDefinition


BUILTINS = {
    "canonical-executive-loop": LoopDefinition(
        name="canonical-executive-loop",
        description="The inherited Executive OS loop: memory -> decision -> coordination -> review -> learning -> updated memory.",
        loop_type="operating",
        customer_lane="shared",
        authority="human leadership",
        tags=["builtin", "executive-os", "canonical"],
        source_path="docs/loops.md",
        signal="A meaningful operating change, ambiguity, risk, commitment, or review moment requires executive attention.",
        memory_objects=[
            "Facts",
            "Assumptions",
            "Commitments",
            "Risks",
            "Open loops",
            "Prior decisions",
        ],
        decision="Prepare options, tradeoffs, recommendations, and human approval points.",
        action="Coordinate approved decisions into owners, next actions, dependencies, deadlines, and status.",
        evidence="Decision memo, operating review, risk register update, owner approval, metric, artifact, or lesson learned.",
        cadence="Weekly by default; daily, monthly, seasonal, or event-driven when the domain requires it.",
        learning_update="Compare expected outcomes with actual outcomes and update memory so the organization does not relearn the same lesson from scratch.",
        governance_boundary="The engine prepares judgment; humans retain authority over decisions, commitments, approvals, spending, external claims, and professional review.",
    ),
    "recursive-improvement-loop": LoopDefinition(
        name="recursive-improvement-loop",
        description="The Anyang Intelligence self-improvement loop that turns friction into better docs, skills, templates, or guardrails.",
        loop_type="recursive",
        customer_lane="shared",
        authority="operator",
        tags=["builtin", "recursive", "coffee"],
        source_path="docs/loops.md; skills/coffee/SKILL.md",
        signal="A work cycle produces friction, learning, entropy, contradiction risk, or a reusable operating insight.",
        memory_objects=[
            "Recent work cycle",
            "Detected friction",
            "Learning",
            "Improvement candidate",
            "Affected skill, template, checklist, guardrail, or customer doc",
        ],
        decision="Decide which one durable improvement would make the next work cycle smarter without overbuilding the system.",
        action="Update the chosen repo surface only after operator approval: skill, template, checklist, guardrail, customer doc, or priority decision.",
        evidence="Diff, updated doc, changed template, new checklist, validation result, or operator-confirmed closeout.",
        cadence="Event-driven after meaningful work cycles; lightweight coffee re-entry when restoring operating context.",
        learning_update="Preserve the learning as a reusable primitive while filtering private customer context through membranes.",
        governance_boundary="The operator approves durable changes; customer facts, sensitive context, and authority boundaries do not cross lanes without membrane review.",
    ),
}


def get_builtin(name: str) -> LoopDefinition | None:
    return BUILTINS.get(name)


def all_builtins() -> list[LoopDefinition]:
    return list(BUILTINS.values())

