from __future__ import annotations

from .lint import validate_loop
from .model import LoopDefinition


def simulate_loop(loop: LoopDefinition) -> str:
    diagnostics = validate_loop(loop)
    warnings = [item for item in diagnostics if item.level != "error"]
    errors = [item for item in diagnostics if item.level == "error"]
    lines = [
        f"Simulating loop: {loop.name}",
        "",
        f"1. Signal received: {loop.signal}",
        f"2. Memory loaded: {', '.join(loop.memory_objects) if loop.memory_objects else 'no memory objects defined'}",
        f"3. Decision prepared for human authority: {loop.decision}",
        f"4. Proposed action path: {loop.action}",
        f"5. Mock evidence check: {loop.evidence}",
        f"6. Cadence check: {loop.cadence}",
        f"7. Learning update proposed: {loop.learning_update}",
        f"8. Governance boundary enforced: {loop.governance_boundary}",
        "",
    ]
    if errors:
        lines.append("Simulation result: blocked by validation errors.")
    elif warnings:
        lines.append("Simulation result: cycle can proceed after reviewing lint warnings.")
    else:
        lines.append("Simulation result: cycle is operational with human authority preserved.")

    if diagnostics:
        lines.append("")
        lines.append("Diagnostics:")
        for item in diagnostics:
            lines.append(f"- {item.level.upper()} {item.code}: {item.message}")
    return "\n".join(lines) + "\n"

