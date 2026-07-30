"""Destination-repository policy adapter for the contradiction kernel."""

from __future__ import annotations

import re

from contradiction_kernel import ContradictionPolicy


HOST_POLICY = ContradictionPolicy(
    ordinary_consequence="ordinary",
    consequential_consequence="consequential",
    authority_sensitive_consequence="authority-sensitive",
    authority_roles=("canonical", "authoritative", "advisory", "derived"),
    controlling_roles=frozenset({"canonical", "authoritative"}),
)

_PRIVACY_RULES = {
    "email-address": re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        re.IGNORECASE,
    ),
    "private-key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "credential-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|password|token)\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9_\-/+=]{12,}"
    ),
}


def scan_packet_privacy(text: str) -> list[str]:
    """Return rule names only; never echo matched sensitive values."""

    return [
        rule
        for rule, pattern in _PRIVACY_RULES.items()
        if pattern.search(text)
    ]
