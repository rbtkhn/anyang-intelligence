from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from anyang_loop.contradiction_preflight import (
    ContradictionPacketError,
    evaluate_contradictions,
    load_contradiction_packet,
    render_contradiction_json,
    render_contradiction_markdown,
)
from anyang_loop.project_cli import main


NOW = "2026-07-30T18:00:00Z"


def packet(
    *,
    consequence: str = "consequential",
    request_value: object = "main",
    provisional: bool = False,
    controls: list[dict] | None = None,
) -> dict:
    if controls is None:
        controls = [
            control("control-1", request_value),
        ]
    return {
        "schema_version": 1,
        "request_ref": "thread:synthetic-request",
        "scope": "repository",
        "consequence_level": consequence,
        "as_of": NOW,
        "request_assertions": [
            {
                "id": "assertion-1",
                "field": "git.branch",
                "value": request_value,
                "scope": "repository",
                "source_ref": "thread:synthetic-request#branch",
                "provisional": provisional,
            }
        ],
        "controlling_facts": controls,
    }


def control(
    identifier: str,
    value: object,
    *,
    field: str = "git.branch",
    scope: str = "repository",
    role: str = "canonical",
    fresh_until: str = "2026-08-01T00:00:00Z",
) -> dict:
    result = {
        "id": identifier,
        "field": field,
        "value": value,
        "scope": scope,
        "authority_role": role,
        "source_ref": f"repo:synthetic/{identifier}.yaml",
        "as_of": "2026-07-30T17:00:00Z",
    }
    if fresh_until:
        result["fresh_until"] = fresh_until
    return result


def codes(result: dict) -> list[str]:
    return [item["code"] for item in result["diagnostics"]]


def test_aligned_request_continues_without_authority_effect():
    result = evaluate_contradictions(packet())
    assert result["disposition"] == "continue"
    assert result["recommended_interaction"] == "none"
    assert result["interaction_required"] is False
    assert codes(result) == ["aligned"]
    assert result["authority_effect"] == "none"
    assert result["capability_token"] is False
    assert "never grants authority" in result["enforcement"]


def test_direct_conflict_clarifies_through_decision_navigation():
    result = evaluate_contradictions(
        packet(request_value="feature", controls=[control("control-1", "main")])
    )
    assert result["disposition"] == "clarify"
    assert result["recommended_interaction"] == "decision-navigation"
    assert result["interaction_required"] is True
    assert codes(result) == ["request-control-conflict"]
    assert "session-local" in result["required_evidence_or_resolution"][0]


def test_conflicting_controlling_sources_hold_for_authority_resolution():
    result = evaluate_contradictions(
        packet(
            controls=[
                control("control-1", "main", role="canonical"),
                control("control-2", "release", role="authoritative"),
            ]
        )
    )
    assert result["disposition"] == "hold"
    assert result["recommended_interaction"] == "authority-resolution"
    assert codes(result) == ["controlling-source-conflict"]
    assert result["diagnostics"][0]["control_refs"] == [
        "repo:synthetic/control-1.yaml",
        "repo:synthetic/control-2.yaml",
    ]


def test_stale_missing_scope_and_non_authoritative_controls_are_distinct():
    stale = evaluate_contradictions(
        packet(
            controls=[
                control(
                    "stale",
                    "main",
                    fresh_until="2026-07-29T00:00:00Z",
                )
            ]
        )
    )
    missing = evaluate_contradictions(packet(controls=[]))
    scope = evaluate_contradictions(
        packet(controls=[control("other", "main", scope="customer")])
    )
    advisory = evaluate_contradictions(
        packet(controls=[control("advice", "main", role="advisory")])
    )
    assert codes(stale) == ["control-stale"]
    assert codes(missing) == ["control-missing"]
    assert codes(scope) == ["control-scope-mismatch"]
    assert codes(advisory) == ["control-non-authoritative"]
    for result in (stale, missing, scope, advisory):
        assert result["disposition"] == "clarify"
        assert result["recommended_interaction"] == "neutral-evidence"


def test_stale_and_advisory_facts_never_become_controlling():
    stale_conflict = evaluate_contradictions(
        packet(
            request_value="feature",
            controls=[
                control(
                    "stale",
                    "main",
                    fresh_until="2026-07-29T00:00:00Z",
                )
            ],
        )
    )
    advisory_conflict = evaluate_contradictions(
        packet(
            request_value="feature",
            controls=[control("advice", "main", role="derived")],
        )
    )
    assert "request-control-conflict" not in codes(stale_conflict)
    assert "request-control-conflict" not in codes(advisory_conflict)
    assert codes(stale_conflict) == ["control-stale"]
    assert codes(advisory_conflict) == ["control-non-authoritative"]


def test_consequence_level_and_visible_provisional_status_control_disposition():
    provisional = evaluate_contradictions(
        packet(consequence="ordinary", provisional=True, controls=[])
    )
    unmarked = evaluate_contradictions(
        packet(consequence="ordinary", provisional=False, controls=[])
    )
    sensitive = evaluate_contradictions(
        packet(consequence="authority-sensitive", provisional=True, controls=[])
    )
    assert provisional["disposition"] == "continue-provisional"
    assert provisional["interaction_required"] is False
    assert unmarked["disposition"] == "clarify"
    assert sensitive["disposition"] == "hold"


def test_projection_order_is_deterministic_and_values_are_not_echoed():
    candidate = packet()
    candidate["request_assertions"] = [
        {
            "id": "assertion-z",
            "field": "git.branch",
            "value": "main",
            "scope": "repository",
            "source_ref": "thread:synthetic-request#z",
            "provisional": False,
        },
        {
            "id": "assertion-a",
            "field": "schema.version",
            "value": 8,
            "scope": "repository",
            "source_ref": "thread:synthetic-request#a",
            "provisional": False,
        },
    ]
    candidate["controlling_facts"].append(
        control("control-schema", 8, field="schema.version")
    )
    result = evaluate_contradictions(candidate)
    assert [item["assertion_id"] for item in result["diagnostics"]] == [
        "assertion-a",
        "assertion-z",
    ]
    rendered_json = render_contradiction_json(result)
    rendered_markdown = render_contradiction_markdown(result)
    assert '"value"' not in rendered_json
    assert "| 8 |" not in rendered_markdown
    assert rendered_json == render_contradiction_json(result)
    assert rendered_markdown == render_contradiction_markdown(result)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda value: value.update(schema_version=2),
            "schema_version",
        ),
        (
            lambda value: value["request_assertions"].append(
                copy.deepcopy(value["request_assertions"][0])
            ),
            "IDs must be unique",
        ),
        (
            lambda value: value["controlling_facts"][0].update(
                authority_role="preferred"
            ),
            "authority_role",
        ),
        (
            lambda value: value.update(as_of="2026-07-30"),
            "timezone",
        ),
        (
            lambda value: value["request_assertions"][0].update(value={"x": 1}),
            "scalar",
        ),
        (
            lambda value: value["controlling_facts"][0].update(value=8),
            "mixes scalar value types",
        ),
        (
            lambda value: value["request_assertions"][0].update(
                value="operator" + chr(64) + "example.com"
            ),
            "privacy scan",
        ),
        (
            lambda value: value["request_assertions"][0].update(value="x" * 501),
            "exceeds",
        ),
        (
            lambda value: value["request_assertions"][0].update(scope="customer"),
            "scope must match",
        ),
        (
            lambda value: value.update(unexpected=True),
            "unknown fields",
        ),
        (
            lambda value: value["controlling_facts"][0].pop("source_ref"),
            "source_ref",
        ),
    ],
)
def test_invalid_packets_fail_closed(mutate, message):
    candidate = packet()
    mutate(candidate)
    with pytest.raises(ContradictionPacketError, match=message):
        evaluate_contradictions(candidate)


def test_oversized_packet_is_rejected_before_comparison():
    candidate = packet(controls=[])
    candidate["request_assertions"] = [
        {
            "id": f"assertion-{index}",
            "field": f"field.{index}",
            "value": "x" * 450,
            "scope": "repository",
            "source_ref": f"thread:synthetic-request#{index}",
            "provisional": True,
        }
        for index in range(60)
    ]
    with pytest.raises(ContradictionPacketError, match="oversized"):
        evaluate_contradictions(candidate)


def test_yaml_loader_normalizes_dates_but_requires_timestamp_timezone(tmp_path):
    valid = packet()
    path = tmp_path / "valid.yaml"
    path.write_text(yaml.safe_dump(valid, sort_keys=False), encoding="utf-8")
    loaded = load_contradiction_packet(path)
    assert evaluate_contradictions(loaded)["disposition"] == "continue"

    path.write_text(
        yaml.safe_dump({**valid, "as_of": "not-a-time"}, sort_keys=False),
        encoding="utf-8",
    )
    with pytest.raises(ContradictionPacketError, match="Invalid as_of"):
        evaluate_contradictions(load_contradiction_packet(path))


def test_cli_is_read_only_and_uses_disposition_exit_codes(tmp_path, capsys):
    aligned_path = tmp_path / "aligned.yaml"
    aligned_path.write_text(
        yaml.safe_dump(packet(), sort_keys=False), encoding="utf-8"
    )
    before = {
        path.name: path.read_bytes() for path in sorted(tmp_path.iterdir())
    }
    assert (
        main(
            [
                "contradiction-check",
                "--packet",
                str(aligned_path),
                "--format",
                "json",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["disposition"] == "continue"
    after = {
        path.name: path.read_bytes() for path in sorted(tmp_path.iterdir())
    }
    assert after == before

    conflict_path = tmp_path / "conflict.yaml"
    conflict_path.write_text(
        yaml.safe_dump(
            packet(
                request_value="feature",
                controls=[control("control-1", "main")],
            ),
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "contradiction-check",
                "--packet",
                str(conflict_path),
                "--format",
                "markdown",
            ]
        )
        == 1
    )
    assert "Disposition: `clarify`" in capsys.readouterr().out


def test_cli_rejects_invalid_packet_without_opening_a_database(tmp_path, capsys):
    path = tmp_path / "invalid.yaml"
    path.write_text("schema_version: 2\n", encoding="utf-8")
    assert main(["contradiction-check", "--packet", str(path)]) == 1
    assert "schema_version" in capsys.readouterr().out
    assert not list(tmp_path.glob("*.db"))
