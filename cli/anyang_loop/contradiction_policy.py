"""Anyang host policy for the portable contradiction kernel."""

from __future__ import annotations

from .contradiction_kernel import ContradictionPolicy
from .privacy_scan import scan_text


ANYANG_CONTRADICTION_POLICY = ContradictionPolicy(
    ordinary_consequence="ordinary",
    consequential_consequence="consequential",
    authority_sensitive_consequence="authority-sensitive",
    authority_roles=("canonical", "authoritative", "advisory", "derived"),
    controlling_roles=frozenset({"canonical", "authoritative"}),
)


def scan_contradiction_packet(text: str) -> list[str]:
    """Apply the repository's existing privacy rules without exposing values."""

    return scan_text(text)
