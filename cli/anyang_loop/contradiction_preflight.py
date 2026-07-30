"""Backward-compatible Anyang facade for contradiction preflight."""

from __future__ import annotations

from typing import Any

from .contradiction_kernel import (
    ContradictionPacketError,
    evaluate_contradictions as _evaluate_contradictions,
    load_contradiction_packet,
    render_contradiction_json,
    render_contradiction_markdown,
)
from .contradiction_policy import (
    ANYANG_CONTRADICTION_POLICY,
    scan_contradiction_packet,
)


def evaluate_contradictions(packet: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a packet using Anyang's vocabulary, bounds, and privacy rules."""

    return _evaluate_contradictions(
        packet,
        policy=ANYANG_CONTRADICTION_POLICY,
        privacy_scanner=scan_contradiction_packet,
    )


__all__ = [
    "ContradictionPacketError",
    "evaluate_contradictions",
    "load_contradiction_packet",
    "render_contradiction_json",
    "render_contradiction_markdown",
]
