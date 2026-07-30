from __future__ import annotations

from pathlib import Path

import pytest

from anyang_loop.contradiction_kernel import (
    ContradictionPacketError,
    ContradictionPolicy,
    evaluate_contradictions,
)


PORTABLE_POLICY = ContradictionPolicy(
    ordinary_consequence="routine",
    consequential_consequence="material",
    authority_sensitive_consequence="permission-bound",
    authority_roles=("governing", "reference"),
    controlling_roles=frozenset({"governing"}),
)


def portable_packet(
    *,
    consequence: str = "material",
    request_value: str = "main",
    control_value: str = "main",
) -> dict:
    return {
        "schema_version": 1,
        "request_ref": "request:synthetic",
        "scope": "repository",
        "consequence_level": consequence,
        "as_of": "2026-07-30T18:00:00Z",
        "request_assertions": [
            {
                "id": "requested-branch",
                "field": "git.branch",
                "value": request_value,
                "scope": "repository",
                "source_ref": "request:synthetic#branch",
                "provisional": False,
            }
        ],
        "controlling_facts": [
            {
                "id": "current-branch",
                "field": "git.branch",
                "value": control_value,
                "scope": "repository",
                "authority_role": "governing",
                "source_ref": "repo:git",
                "as_of": "2026-07-30T17:59:00Z",
                "fresh_until": "2026-07-30T18:05:00Z",
            }
        ],
    }


def test_kernel_accepts_host_vocabulary_without_anyang_imports() -> None:
    scanned: list[str] = []

    def scanner(text: str) -> list[str]:
        scanned.append(text)
        return []

    aligned = evaluate_contradictions(
        portable_packet(),
        policy=PORTABLE_POLICY,
        privacy_scanner=scanner,
    )
    conflict = evaluate_contradictions(
        portable_packet(request_value="feature"),
        policy=PORTABLE_POLICY,
        privacy_scanner=scanner,
    )
    sensitive = evaluate_contradictions(
        portable_packet(
            consequence="permission-bound",
            request_value="feature",
        ),
        policy=PORTABLE_POLICY,
        privacy_scanner=scanner,
    )

    assert aligned["disposition"] == "continue"
    assert conflict["disposition"] == "clarify"
    assert sensitive["disposition"] == "hold"
    assert len(scanned) == 6

    core = (
        Path(__file__).resolve().parents[1]
        / "cli"
        / "anyang_loop"
        / "contradiction_kernel"
        / "core.py"
    ).read_text(encoding="utf-8")
    assert "from .privacy_scan import" not in core
    assert "from anyang_loop" not in core
    assert "anyang" not in core.lower()


def test_host_privacy_scanner_can_fail_closed() -> None:
    with pytest.raises(ContradictionPacketError, match="host-private"):
        evaluate_contradictions(
            portable_packet(),
            policy=PORTABLE_POLICY,
            privacy_scanner=lambda _text: ["host-private"],
        )


def test_policy_rejects_ambiguous_semantics() -> None:
    with pytest.raises(ValueError, match="distinct"):
        ContradictionPolicy(
            ordinary_consequence="material",
            consequential_consequence="material",
            authority_sensitive_consequence="permission-bound",
            authority_roles=("governing",),
            controlling_roles=frozenset({"governing"}),
        )

    with pytest.raises(ValueError, match="declared authority roles"):
        ContradictionPolicy(
            ordinary_consequence="routine",
            consequential_consequence="material",
            authority_sensitive_consequence="permission-bound",
            authority_roles=("reference",),
            controlling_roles=frozenset({"governing"}),
        )
