from __future__ import annotations

import json
import math
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from .privacy_scan import scan_text


PACKET_SCHEMA_VERSION = 1
CONSEQUENCE_LEVELS = ("ordinary", "consequential", "authority-sensitive")
AUTHORITY_ROLES = ("canonical", "authoritative", "advisory", "derived")
CONTROLLING_ROLES = {"canonical", "authoritative"}
DISPOSITIONS = ("continue", "continue-provisional", "clarify", "hold")
DIAGNOSTIC_CODES = (
    "aligned",
    "request-control-conflict",
    "controlling-source-conflict",
    "control-stale",
    "control-missing",
    "control-scope-mismatch",
    "control-non-authoritative",
)
MAX_TEXT = 500
MAX_PACKET_JSON = 24_000
TOKEN_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class ContradictionPacketError(ValueError):
    pass


def load_contradiction_packet(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        value = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ContradictionPacketError(
            f"Cannot load contradiction packet {source}: {exc}"
        ) from exc
    if not isinstance(value, dict):
        raise ContradictionPacketError("Contradiction packet must be a YAML mapping")
    return _normalize_yaml_dates(value)


def evaluate_contradictions(packet: dict[str, Any]) -> dict[str, Any]:
    normalized = _validate_packet(packet)
    as_of = _timestamp(normalized["as_of"], "as_of")
    controls_by_field: dict[str, list[dict[str, Any]]] = {}
    for control in normalized["controlling_facts"]:
        controls_by_field.setdefault(control["field"], []).append(control)

    diagnostics = [
        _evaluate_assertion(
            assertion,
            controls_by_field.get(assertion["field"], []),
            normalized["consequence_level"],
            as_of,
        )
        for assertion in normalized["request_assertions"]
    ]
    diagnostics.sort(key=lambda item: (item["assertion_id"], item["code"]))
    disposition = _overall_disposition(
        diagnostics, normalized["consequence_level"]
    )
    interaction = _overall_interaction(diagnostics)
    required = sorted(
        {
            item["required_evidence_or_resolution"]
            for item in diagnostics
            if item["required_evidence_or_resolution"]
        }
    )
    counts = {
        code: sum(item["code"] == code for item in diagnostics)
        for code in DIAGNOSTIC_CODES
    }
    return {
        "schema_version": PACKET_SCHEMA_VERSION,
        "request": {
            "request_ref": normalized["request_ref"],
            "scope": normalized["scope"],
            "consequence_level": normalized["consequence_level"],
            "as_of": normalized["as_of"],
        },
        "disposition": disposition,
        "recommended_interaction": interaction,
        "interaction_required": disposition in {"clarify", "hold"},
        "diagnostic_counts": counts,
        "diagnostics": diagnostics,
        "required_evidence_or_resolution": required,
        "authority_effect": "none",
        "capability_token": False,
        "enforcement": (
            "This inspectable preflight reports contradictions and never grants "
            "authority or becomes a reusable capability token."
        ),
    }


def render_contradiction_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def render_contradiction_markdown(data: dict[str, Any]) -> str:
    request = data["request"]
    lines = [
        "# Elicitation Contradiction Preflight",
        "",
        f"- Disposition: `{data['disposition']}`",
        f"- Request: `{_markdown_cell(request['request_ref'])}`",
        f"- Scope: `{_markdown_cell(request['scope'])}`",
        f"- Consequence: `{request['consequence_level']}`",
        f"- As of: {request['as_of']}",
        f"- Recommended interaction: `{data['recommended_interaction']}`",
        f"- Interaction required: `{str(data['interaction_required']).lower()}`",
        "",
        "## Diagnostics",
        "",
        "| Assertion | Diagnostic | Request reference | Control references | Needed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in data["diagnostics"]:
        controls = (
            ", ".join(f"`{_markdown_cell(value)}`" for value in item["control_refs"])
            or "Missing"
        )
        needed = item["required_evidence_or_resolution"] or "None"
        lines.append(
            f"| `{item['assertion_id']}` | `{item['code']}` | "
            f"`{_markdown_cell(item['request_ref'])}` | {controls} | {needed} |"
        )
    lines.extend(["", "## Authority Boundary", "", f"- {data['enforcement']}", ""])
    return "\n".join(lines)


def _evaluate_assertion(
    assertion: dict[str, Any],
    field_controls: list[dict[str, Any]],
    consequence_level: str,
    as_of: datetime,
) -> dict[str, Any]:
    same_scope = [
        control for control in field_controls if control["scope"] == assertion["scope"]
    ]
    authoritative = [
        control
        for control in same_scope
        if control["authority_role"] in CONTROLLING_ROLES
    ]
    fresh = [
        control
        for control in authoritative
        if not control["fresh_until"]
        or _timestamp(control["fresh_until"], "fresh_until") >= as_of
    ]

    code: str
    controls: list[dict[str, Any]]
    needed = ""
    interaction = "none"
    if fresh:
        controls = fresh
        values = {_typed_value_key(control["value"]) for control in fresh}
        if len(values) > 1:
            code = "controlling-source-conflict"
            needed = "Named authority resolution between controlling sources"
            interaction = "authority-resolution"
        elif assertion["value"] == fresh[0]["value"]:
            code = "aligned"
        else:
            code = "request-control-conflict"
            needed = (
                "Human disposition: keep session-local, propose durable correction, "
                "or hold"
            )
            interaction = "decision-navigation"
    elif authoritative:
        code = "control-stale"
        controls = authoritative
        needed = "Refreshed controlling evidence within the declared scope"
        interaction = "neutral-evidence"
    elif same_scope:
        code = "control-non-authoritative"
        controls = same_scope
        needed = "Canonical or authoritative evidence for the declared operation"
        interaction = "neutral-evidence"
    elif field_controls:
        code = "control-scope-mismatch"
        controls = field_controls
        needed = "Controlling evidence for the request scope"
        interaction = "neutral-evidence"
    else:
        code = "control-missing"
        controls = []
        needed = "Controlling evidence for the normalized assertion"
        interaction = "neutral-evidence"

    provisional = bool(assertion["provisional"])
    return {
        "assertion_id": assertion["id"],
        "field": assertion["field"],
        "scope": assertion["scope"],
        "consequence_level": consequence_level,
        "provisional": provisional,
        "code": code,
        "request_ref": assertion["source_ref"],
        "control_refs": sorted(control["source_ref"] for control in controls),
        "required_evidence_or_resolution": needed,
        "recommended_interaction": interaction,
    }


def _overall_disposition(
    diagnostics: list[dict[str, Any]], consequence_level: str
) -> str:
    codes = {item["code"] for item in diagnostics}
    if "controlling-source-conflict" in codes:
        return "hold"
    non_aligned = [item for item in diagnostics if item["code"] != "aligned"]
    if not non_aligned:
        return "continue"
    if consequence_level == "authority-sensitive":
        return "hold"
    if "request-control-conflict" in codes:
        return "clarify"
    if consequence_level == "consequential":
        return "clarify"
    if all(item["provisional"] for item in non_aligned):
        return "continue-provisional"
    return "clarify"


def _overall_interaction(diagnostics: list[dict[str, Any]]) -> str:
    interactions = {item["recommended_interaction"] for item in diagnostics}
    for value in (
        "authority-resolution",
        "decision-navigation",
        "neutral-evidence",
    ):
        if value in interactions:
            return value
    return "none"


def _validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise ContradictionPacketError("Contradiction packet must be a mapping")
    raw = json.dumps(_normalize_yaml_dates(packet), sort_keys=True, default=str)
    if len(raw) > MAX_PACKET_JSON:
        raise ContradictionPacketError("Contradiction packet is oversized")
    raw_findings = scan_text(raw)
    if raw_findings:
        raise ContradictionPacketError(
            "Contradiction packet failed privacy scan: "
            + ", ".join(raw_findings)
        )
    allowed_top = {
        "schema_version",
        "request_ref",
        "scope",
        "consequence_level",
        "as_of",
        "request_assertions",
        "controlling_facts",
    }
    unknown_top = set(packet) - allowed_top
    if unknown_top:
        raise ContradictionPacketError(
            "Contradiction packet has unknown fields: "
            + ", ".join(sorted(unknown_top))
        )
    if packet.get("schema_version") != PACKET_SCHEMA_VERSION:
        raise ContradictionPacketError(
            f"Contradiction packet schema_version must be {PACKET_SCHEMA_VERSION}"
        )
    request_ref = _text(packet.get("request_ref"), "request_ref")
    scope = _text(packet.get("scope"), "scope")
    consequence = _text(packet.get("consequence_level"), "consequence_level")
    if consequence not in CONSEQUENCE_LEVELS:
        raise ContradictionPacketError(
            f"Invalid consequence_level: {consequence}"
        )
    as_of = _text(packet.get("as_of"), "as_of", maximum=100)
    _timestamp(as_of, "as_of")

    assertions = packet.get("request_assertions")
    controls = packet.get("controlling_facts")
    if not isinstance(assertions, list) or not assertions:
        raise ContradictionPacketError(
            "Contradiction packet requires request_assertions"
        )
    if not isinstance(controls, list):
        raise ContradictionPacketError(
            "Contradiction packet controlling_facts must be a list"
        )
    normalized_assertions = [
        _validate_assertion(value, index) for index, value in enumerate(assertions, 1)
    ]
    normalized_controls = [
        _validate_control(value, index) for index, value in enumerate(controls, 1)
    ]
    if any(assertion["scope"] != scope for assertion in normalized_assertions):
        raise ContradictionPacketError(
            "Every request assertion scope must match the packet scope"
        )
    _unique_ids(normalized_assertions, normalized_controls)
    _validate_value_types(normalized_assertions, normalized_controls)

    normalized = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "request_ref": request_ref,
        "scope": scope,
        "consequence_level": consequence,
        "as_of": as_of,
        "request_assertions": normalized_assertions,
        "controlling_facts": normalized_controls,
    }
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    if len(serialized) > MAX_PACKET_JSON:
        raise ContradictionPacketError("Contradiction packet is oversized")
    findings = scan_text(serialized)
    if findings:
        raise ContradictionPacketError(
            "Contradiction packet failed privacy scan: " + ", ".join(findings)
        )
    return normalized


def _validate_assertion(value: Any, index: int) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContradictionPacketError(f"Request assertion {index} must be a mapping")
    unknown = set(value) - {"id", "field", "value", "scope", "source_ref", "provisional"}
    if unknown:
        raise ContradictionPacketError(
            f"Request assertion {index} has unknown fields: {', '.join(sorted(unknown))}"
        )
    provisional = value.get("provisional", False)
    if not isinstance(provisional, bool):
        raise ContradictionPacketError(
            f"Request assertion {index} provisional must be boolean"
        )
    return {
        "id": _token(value.get("id"), f"request assertion {index} id"),
        "field": _token(value.get("field"), f"request assertion {index} field"),
        "value": _scalar(value.get("value"), f"request assertion {index} value"),
        "scope": _text(value.get("scope"), f"request assertion {index} scope"),
        "source_ref": _text(
            value.get("source_ref"), f"request assertion {index} source_ref"
        ),
        "provisional": provisional,
    }


def _validate_control(value: Any, index: int) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContradictionPacketError(f"Controlling fact {index} must be a mapping")
    allowed = {
        "id",
        "field",
        "value",
        "scope",
        "authority_role",
        "source_ref",
        "as_of",
        "fresh_until",
    }
    unknown = set(value) - allowed
    if unknown:
        raise ContradictionPacketError(
            f"Controlling fact {index} has unknown fields: {', '.join(sorted(unknown))}"
        )
    role = _text(
        value.get("authority_role"),
        f"controlling fact {index} authority_role",
        maximum=40,
    )
    if role not in AUTHORITY_ROLES:
        raise ContradictionPacketError(
            f"Invalid controlling fact {index} authority_role: {role}"
        )
    fact_as_of = _text(
        value.get("as_of"), f"controlling fact {index} as_of", maximum=100
    )
    _timestamp(fact_as_of, f"controlling fact {index} as_of")
    fresh_until = value.get("fresh_until")
    normalized_fresh_until = (
        _text(
            fresh_until,
            f"controlling fact {index} fresh_until",
            maximum=100,
        )
        if fresh_until is not None
        else ""
    )
    if normalized_fresh_until:
        _timestamp(normalized_fresh_until, f"controlling fact {index} fresh_until")
    return {
        "id": _token(value.get("id"), f"controlling fact {index} id"),
        "field": _token(value.get("field"), f"controlling fact {index} field"),
        "value": _scalar(value.get("value"), f"controlling fact {index} value"),
        "scope": _text(value.get("scope"), f"controlling fact {index} scope"),
        "authority_role": role,
        "source_ref": _text(
            value.get("source_ref"), f"controlling fact {index} source_ref"
        ),
        "as_of": fact_as_of,
        "fresh_until": normalized_fresh_until,
    }


def _unique_ids(
    assertions: list[dict[str, Any]], controls: list[dict[str, Any]]
) -> None:
    identifiers = [value["id"] for value in (*assertions, *controls)]
    if len(identifiers) != len(set(identifiers)):
        raise ContradictionPacketError(
            "Contradiction packet IDs must be unique across assertions and controls"
        )


def _validate_value_types(
    assertions: list[dict[str, Any]], controls: list[dict[str, Any]]
) -> None:
    types_by_field_scope: dict[tuple[str, str], set[str]] = {}
    for value in (*assertions, *controls):
        key = (value["field"], value["scope"])
        types_by_field_scope.setdefault(key, set()).add(_scalar_kind(value["value"]))
    mixed = [
        f"{field}@{scope}"
        for (field, scope), kinds in sorted(types_by_field_scope.items())
        if len(kinds) > 1
    ]
    if mixed:
        raise ContradictionPacketError(
            "Contradiction packet mixes scalar value types for: " + ", ".join(mixed)
        )


def _scalar(value: Any, label: str) -> str | int | float | bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            raise ContradictionPacketError(f"{label} must be a finite number")
        return value
    if isinstance(value, str):
        return _text(value, label)
    raise ContradictionPacketError(
        f"{label} must be a scalar string, number, or boolean"
    )


def _scalar_kind(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    return "string"


def _typed_value_key(value: Any) -> tuple[str, Any]:
    return (_scalar_kind(value), value)


def _token(value: Any, label: str) -> str:
    text = _text(value, label, maximum=120)
    if not TOKEN_RE.fullmatch(text):
        raise ContradictionPacketError(
            f"{label} must use lowercase letters, digits, dots, underscores, or hyphens"
        )
    return text


def _text(value: Any, label: str, *, maximum: int = MAX_TEXT) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContradictionPacketError(f"{label} must be a non-empty string")
    text = value.strip()
    if len(text) > maximum:
        raise ContradictionPacketError(f"{label} exceeds {maximum} characters")
    if any(character in text for character in ("\n", "\r", "\x00")):
        raise ContradictionPacketError(f"{label} must be a single line")
    return text


def _timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContradictionPacketError(f"Invalid {label} timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ContradictionPacketError(f"{label} timestamp must include a timezone")
    return parsed


def _normalize_yaml_dates(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalize_yaml_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_yaml_dates(item) for item in value]
    return value


def _markdown_cell(value: str) -> str:
    return value.replace("`", "\\`").replace("|", "\\|")
