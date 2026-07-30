"""Portable, deterministic contradiction-preflight kernel."""

from .core import (
    ContradictionPacketError,
    ContradictionPolicy,
    evaluate_contradictions,
    load_contradiction_packet,
    render_contradiction_json,
    render_contradiction_markdown,
)

__all__ = [
    "ContradictionPacketError",
    "ContradictionPolicy",
    "evaluate_contradictions",
    "load_contradiction_packet",
    "render_contradiction_json",
    "render_contradiction_markdown",
]
