from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

import yaml

from .ops_service import MutationResult, OpsError, now_utc, tenant_id
from .privacy_scan import scan_text


CHOICE_ROLES = ("recommended", "alternative", "overlooked", "pause-or-deepen")
CONSEQUENCE_LEVELS = ("ordinary", "consequential", "authority-sensitive")
EVENT_TYPES = (
    "outcome_recorded",
    "review_deferred",
    "corrected",
    "superseded",
)
OUTCOME_RESULTS = (
    "successful",
    "mixed",
    "unsuccessful",
    "no_action",
    "not_observable",
)
COGNITIVE_LOAD = ("lower", "same", "higher", "Missing")
MOMENTUM = ("advanced", "neutral", "stalled", "Missing")
DISCOVERY_VALUE = (
    "new-useful-path",
    "confirmed-known-path",
    "not-useful",
    "Missing",
)
TERMINAL_RESULTS = set(OUTCOME_RESULTS)
MAX_TEXT = 500
MAX_JSON = 24000


def load_choice_packet(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    value = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OpsError(f"Choice packet must be a YAML mapping: {source}")
    return value


def record_choice_selection(
    connection: sqlite3.Connection,
    tenant: str,
    packet: dict[str, Any],
) -> MutationResult:
    normalized = _validate_selection_packet(packet)
    tid = tenant_id(connection, tenant)
    _validate_actor(connection, tid, normalized["actor_id"])
    prompt_values = {
        "id": normalized["id"],
        "tenant_id": tid,
        "workspace_id": normalized["workspace_id"],
        "lane": normalized["lane"],
        "choice_kind": normalized["choice_kind"],
        "consequence_level": normalized["consequence_level"],
        "decision_summary": normalized["decision_summary"],
        "options_json": _canonical_json(normalized["options"]),
        "recommendation_key": normalized["recommendation_key"],
        "learning_refs_json": _canonical_json(normalized["learning_refs"]),
        "success_signal": normalized["success_signal"],
        "risk_signal": normalized["risk_signal"],
        "source_ref": normalized["source_ref"],
        "presented_at": normalized["presented_at"],
        "option_set_hash": _hash(normalized["options"]),
        "learning_context_hash": _hash(normalized["learning_context"]),
        "created_at": normalized["recorded_at"],
    }
    selection_payload = {
        "selected_option_key": normalized["selected_option_key"],
        "selected_option_role": normalized["option_by_key"][
            normalized["selected_option_key"]
        ]["role"],
        "review_after": normalized["review_after"],
        "authority_effect": "none",
    }
    event_id = str(
        uuid.uuid5(uuid.NAMESPACE_URL, f"anyang:choice:{normalized['id']}:selection")
    )
    event_values = {
        "id": event_id,
        "choice_id": normalized["id"],
        "tenant_id": tid,
        "event_key": "selection",
        "sequence": 1,
        "event_type": "branch_selected",
        "actor_id": normalized["actor_id"],
        "actor_label": normalized["selected_by"],
        "action_summary": f"Navigate into {normalized['selected_option_key']}",
        "occurred_at": normalized["selected_at"],
        "recorded_at": normalized["recorded_at"],
        "evidence_ref": normalized["evidence_ref"],
        "payload_json": _canonical_json(selection_payload),
        "prior_hash": "",
    }
    event_values["event_hash"] = _event_hash(event_values)

    existing = connection.execute(
        "SELECT * FROM choice_prompt WHERE id = ?", (normalized["id"],)
    ).fetchone()
    if existing:
        comparable = tuple(key for key in prompt_values if key != "created_at")
        if not all(existing[key] == prompt_values[key] for key in comparable):
            raise OpsError(f"Choice prompt conflicts with existing record: {normalized['id']}")
        event = connection.execute(
            "SELECT * FROM choice_event WHERE choice_id = ? AND event_key = 'selection'",
            (normalized["id"],),
        ).fetchone()
        if event and all(event[key] == value for key, value in event_values.items()):
            return MutationResult(
                "choice_selection_exists",
                normalized["id"],
                {"idempotent": True, "selected_option_key": normalized["selected_option_key"]},
            )
        raise OpsError(f"Choice selection conflicts with existing record: {normalized['id']}")

    try:
        connection.execute(
            """INSERT INTO choice_prompt(
                id, tenant_id, workspace_id, lane, choice_kind, consequence_level,
                decision_summary, options_json, recommendation_key, learning_refs_json,
                success_signal, risk_signal, source_ref, presented_at, option_set_hash,
                learning_context_hash, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(prompt_values.values()),
        )
        connection.execute(
            """INSERT INTO choice_event(
                id, choice_id, tenant_id, event_key, sequence, event_type,
                actor_id, actor_label, action_summary, occurred_at, recorded_at,
                evidence_ref, payload_json, prior_hash, event_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(event_values.values()),
        )
        connection.commit()
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError(f"Choice selection is invalid: {exc}") from exc
    return MutationResult(
        "choice_branch_selected",
        normalized["id"],
        {
            "idempotent": False,
            "selected_option_key": normalized["selected_option_key"],
            "authority_effect": "none",
        },
    )


def record_choice_event(
    connection: sqlite3.Connection,
    choice_id: str,
    packet: dict[str, Any],
) -> MutationResult:
    prompt = _prompt(connection, choice_id)
    event_type = _text(packet.get("event_type"))
    if event_type not in EVENT_TYPES:
        raise OpsError(f"Unsupported choice event type: {event_type}")
    event_key = _bounded(packet.get("event_key"), "event_key", required=True, maximum=200)
    actor_label = _bounded(packet.get("recorded_by"), "recorded_by", required=True)
    actor_id = _nullable_bounded(packet.get("actor_id"), "actor_id", maximum=200)
    _validate_actor(connection, prompt["tenant_id"], actor_id)
    summary = _bounded(packet.get("action_summary"), "action_summary", required=True)
    evidence_ref = _nullable_bounded(packet.get("evidence_ref"), "evidence_ref") or ""
    occurred_at = _nullable_bounded(packet.get("occurred_at"), "occurred_at", maximum=100)
    recorded_at = _nullable_bounded(packet.get("recorded_at"), "recorded_at", maximum=100) or now_utc()
    payload = packet.get("payload")
    if not isinstance(payload, dict):
        raise OpsError("Choice event payload must be a mapping")
    payload = _validate_event_payload(event_type, payload)
    _privacy_safe(payload, "choice event payload")
    payload_json = _canonical_json(payload)

    existing = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? AND event_key = ?",
        (choice_id, event_key),
    ).fetchone()
    semantic = {
        "event_type": event_type,
        "actor_id": actor_id,
        "actor_label": actor_label,
        "action_summary": summary,
        "occurred_at": occurred_at,
        "evidence_ref": evidence_ref,
        "payload_json": payload_json,
    }
    if existing:
        if all(existing[key] == value for key, value in semantic.items()):
            return MutationResult(
                "choice_event_exists", existing["id"], {"idempotent": True}
            )
        raise OpsError(f"Choice event key conflicts: {choice_id}/{event_key}")

    prior = connection.execute(
        """SELECT sequence, event_hash FROM choice_event
        WHERE choice_id = ? ORDER BY sequence DESC LIMIT 1""",
        (choice_id,),
    ).fetchone()
    sequence = int(prior["sequence"]) + 1 if prior else 1
    prior_hash = str(prior["event_hash"]) if prior else ""
    event_id = _nullable_bounded(packet.get("id"), "id", maximum=200) or str(uuid.uuid4())
    values = {
        "id": event_id,
        "choice_id": choice_id,
        "tenant_id": prompt["tenant_id"],
        "event_key": event_key,
        "sequence": sequence,
        **semantic,
        "recorded_at": recorded_at,
        "prior_hash": prior_hash,
    }
    values["event_hash"] = _event_hash(values)
    try:
        connection.execute(
            """INSERT INTO choice_event(
                id, choice_id, tenant_id, event_key, sequence, event_type,
                actor_id, actor_label, action_summary, occurred_at, evidence_ref,
                payload_json, recorded_at, prior_hash, event_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(values.values()),
        )
        connection.commit()
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError(f"Choice event is invalid: {exc}") from exc
    return MutationResult(
        "choice_event_recorded",
        event_id,
        {"choice_id": choice_id, "event_type": event_type, "sequence": sequence},
    )


def verify_choice(connection: sqlite3.Connection, choice_id: str) -> dict[str, Any]:
    prompt = _prompt(connection, choice_id)
    events = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence", (choice_id,)
    ).fetchall()
    issues: list[dict[str, str]] = []
    prior_hash = ""
    for expected, event in enumerate(events, start=1):
        if event["sequence"] != expected:
            issues.append({"code": "sequence-gap", "message": f"Expected event {expected}."})
        if event["tenant_id"] != prompt["tenant_id"]:
            issues.append({"code": "tenant-mismatch", "message": f"Event {event['id']} crosses tenant."})
        if event["prior_hash"] != prior_hash:
            issues.append({"code": "prior-hash-mismatch", "message": f"Event {event['id']} has a broken link."})
        values = {key: event[key] for key in _event_hash_fields()}
        if _event_hash(values) != event["event_hash"]:
            issues.append({"code": "event-hash-mismatch", "message": f"Event {event['id']} failed hashing."})
        prior_hash = event["event_hash"]
    return {
        "choice_id": choice_id,
        "ok": not issues,
        "event_count": len(events),
        "head_hash": prior_hash,
        "issues": issues,
    }


def choice_projection(connection: sqlite3.Connection, choice_id: str) -> dict[str, Any]:
    prompt = _prompt(connection, choice_id)
    rows = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence", (choice_id,)
    ).fetchall()
    events = [_event_dict(row) for row in rows]
    selected = next(
        (event for event in events if event["event_type"] == "branch_selected"), None
    )
    outcome = None
    state = "selected" if selected else "invalid"
    review_after = selected["payload"].get("review_after") if selected else None
    for event in events:
        if event["event_type"] == "outcome_recorded":
            outcome = event
            state = (
                "outcome_observed"
                if event["payload"].get("result") in TERMINAL_RESULTS
                else "outcome_pending"
            )
        elif event["event_type"] == "review_deferred":
            review_after = event["payload"]["review_after"]
            state = "review_deferred"
        elif event["event_type"] == "corrected":
            state = "corrected"
            if isinstance(event["payload"].get("replacement_outcome"), dict):
                outcome = {**event, "payload": event["payload"]["replacement_outcome"]}
        elif event["event_type"] == "superseded":
            state = "superseded"
    verification = verify_choice(connection, choice_id)
    options = json.loads(prompt["options_json"])
    return {
        "schema_version": 1,
        "choice": {
            key: prompt[key]
            for key in (
                "id",
                "tenant_id",
                "workspace_id",
                "lane",
                "choice_kind",
                "consequence_level",
                "decision_summary",
                "recommendation_key",
                "success_signal",
                "risk_signal",
                "source_ref",
                "presented_at",
                "created_at",
            )
        },
        "options": options,
        "learning_refs": json.loads(prompt["learning_refs_json"]),
        "selection": selected,
        "outcome": outcome,
        "current_state": state,
        "review_after": review_after,
        "attention_flags": _attention_flags(prompt, state, outcome, verification),
        "events": events,
        "lineage": {
            "option_set_hash": prompt["option_set_hash"],
            "learning_context_hash": prompt["learning_context_hash"],
            "event_count": verification["event_count"],
            "head_hash": verification["head_hash"],
            "chain_verified": verification["ok"],
            "authority_effect": "none",
        },
    }


def choice_context(
    connection: sqlite3.Connection,
    tenant: str,
    workspace_id: str,
    lane: str,
    choice_kind: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    rows = connection.execute(
        """SELECT id FROM choice_prompt
        WHERE tenant_id = ? AND workspace_id = ? AND lane = ? AND choice_kind = ?
        ORDER BY created_at, id""",
        (tid, workspace_id, lane, choice_kind),
    ).fetchall()
    projections = [choice_projection(connection, row["id"]) for row in rows]
    resolved = [
        projection
        for projection in projections
        if projection["outcome"]
        and projection["outcome"]["payload"].get("result") in TERMINAL_RESULTS
    ]
    patterns: dict[str, dict[str, Any]] = {}
    guardrails: list[dict[str, str]] = []
    learning_refs: set[str] = set()
    for projection in projections:
        learning_refs.update(projection["learning_refs"])
    for projection in resolved:
        selected_key = projection["selection"]["payload"]["selected_option_key"]
        result = projection["outcome"]["payload"]["result"]
        bucket = patterns.setdefault(
            selected_key,
            {
                "option_key": selected_key,
                "resolved": 0,
                "successful": 0,
                "mixed": 0,
                "unsuccessful": 0,
                "no_action": 0,
            },
        )
        bucket["resolved"] += 1
        bucket[result] += 1
        payload = projection["outcome"]["payload"]
        if payload.get("authority_issue") or payload.get("membrane_issue"):
            guardrails.append(
                {
                    "choice_id": projection["choice"]["id"],
                    "option_key": selected_key,
                    "reason": "Prior outcome recorded an authority or membrane incident.",
                    "evidence_ref": projection["outcome"]["evidence_ref"],
                }
            )
    pattern_rows = []
    favored: list[str] = []
    demoted: list[str] = []
    for key in sorted(patterns):
        bucket = patterns[key]
        bucket["evidence_tier"] = "thin"
        if bucket["resolved"] >= 3:
            if bucket["successful"] >= 2 and bucket["unsuccessful"] == 0:
                bucket["evidence_tier"] = "pattern"
                favored.append(key)
            elif bucket["unsuccessful"] >= 2 and bucket["successful"] == 0:
                bucket["evidence_tier"] = "pattern"
                demoted.append(key)
        pattern_rows.append(bucket)
    due_review = choice_review(connection, tenant, workspace_id, as_of)
    return {
        "schema_version": 1,
        "tenant": tenant,
        "workspace_id": workspace_id,
        "lane": lane,
        "choice_kind": choice_kind,
        "as_of": as_of or now_utc(),
        "resolved_outcome_count": len(resolved),
        "outcome_patterns": pattern_rows,
        "guardrails": guardrails,
        "learning_refs": sorted(learning_refs),
        "recommendation_guidance": {
            "favored_option_keys": favored,
            "demoted_option_keys": demoted,
            "selection_frequency_used": False,
            "preserve_overlooked_possibility": True,
            "rationale": _guidance_rationale(len(resolved), guardrails, favored, demoted),
        },
        "due_outcome_review": due_review["choices"][:1],
        "ledger_fallback": False,
    }


def choice_review(
    connection: sqlite3.Connection,
    tenant: str,
    workspace_id: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    reference = as_of or now_utc()
    rows = connection.execute(
        """SELECT id FROM choice_prompt
        WHERE tenant_id = ? AND workspace_id = ? ORDER BY created_at, id""",
        (tid, workspace_id),
    ).fetchall()
    due: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    for row in rows:
        projection = choice_projection(connection, row["id"])
        if projection["current_state"] == "superseded":
            continue
        outcome = projection["outcome"]
        if outcome and outcome["payload"].get("result") in TERMINAL_RESULTS:
            resolved.append(projection)
            continue
        review_after = projection["review_after"]
        if review_after and _timestamp(review_after) > _timestamp(reference):
            continue
        due.append(
            {
                "choice_id": projection["choice"]["id"],
                "decision_summary": projection["choice"]["decision_summary"],
                "consequence_level": projection["choice"]["consequence_level"],
                "selected_option_key": projection["selection"]["payload"][
                    "selected_option_key"
                ],
                "selected_option_label": _selected_label(projection),
                "review_after": review_after,
                "current_state": projection["current_state"],
            }
        )
    rank = {"authority-sensitive": 0, "consequential": 1, "ordinary": 2}
    due.sort(
        key=lambda item: (
            rank[item["consequence_level"]],
            item["review_after"] or "",
            item["choice_id"],
        )
    )
    return {
        "schema_version": 1,
        "tenant": tenant,
        "workspace_id": workspace_id,
        "as_of": reference,
        "due_count": len(due),
        "choices": due,
        "resolved_count": len(resolved),
        "reflection_sample_ready": len(resolved) >= 5,
        "five_selection_review": _five_selection_scorecard(resolved),
        "coffee_limit": 1,
        "human_authority": "Outcome review informs future navigation and grants no action authority.",
    }


def render_choice_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['choice']['decision_summary']}",
        "",
        f"Choice: `{data['choice']['id']}`",
        f"State: `{data['current_state']}`",
        f"Lane: `{data['choice']['lane']}`",
        "",
        "## Possibilities",
        "",
    ]
    selected_key = (
        data["selection"]["payload"]["selected_option_key"] if data["selection"] else ""
    )
    for option in data["options"]:
        marker = " — selected" if option["key"] == selected_key else ""
        lines.append(
            f"- **{option['label']}** (`{option['role']}`){marker}: {option['tradeoff']}"
        )
    lines.extend(["", "## Outcome", ""])
    if data["outcome"]:
        payload = data["outcome"]["payload"]
        lines.append(f"- Result: `{payload.get('result', 'Missing')}`")
        lines.append(f"- Cognitive load: `{payload.get('cognitive_load', 'Missing')}`")
        lines.append(f"- Momentum: `{payload.get('momentum', 'Missing')}`")
        lines.append(f"- Discovery value: `{payload.get('discovery_value', 'Missing')}`")
    else:
        lines.append("- Missing")
    lines.extend(
        [
            "",
            "## Lineage",
            "",
            f"- Chain verified: {data['lineage']['chain_verified']}",
            f"- Head hash: `{data['lineage']['head_hash']}`",
            "- Authority effect: `none`",
            "",
        ]
    )
    return "\n".join(lines)


def render_choice_context_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Choice Learning Context",
        "",
        f"Lane: `{data['lane']}`",
        f"Kind: `{data['choice_kind']}`",
        f"Resolved outcomes: {data['resolved_outcome_count']}",
        "",
        f"Recommendation rationale: {data['recommendation_guidance']['rationale']}",
        "",
        "## Outcome Patterns",
        "",
    ]
    if not data["outcome_patterns"]:
        lines.append("- No comparable resolved outcomes.")
    for pattern in data["outcome_patterns"]:
        lines.append(
            f"- `{pattern['option_key']}`: {pattern['evidence_tier']} evidence "
            f"across {pattern['resolved']} outcome(s)."
        )
    lines.extend(["", "## Guardrails", ""])
    if not data["guardrails"]:
        lines.append("- No outcome-derived authority or membrane guardrails.")
    for guardrail in data["guardrails"]:
        lines.append(f"- `{guardrail['option_key']}`: {guardrail['reason']}")
    lines.append("")
    return "\n".join(lines)


def render_choice_review_markdown(data: dict[str, Any]) -> str:
    scorecard = data["five_selection_review"]
    lines = [
        "# Choice Outcome Review",
        "",
        f"Due outcomes: {data['due_count']}",
        f"Resolved outcomes: {data['resolved_count']}",
        "",
    ]
    for item in data["choices"]:
        lines.append(
            f"- **{item['decision_summary']}** → {item['selected_option_label']} "
            f"(`{item['choice_id']}`)"
        )
    if not data["choices"]:
        lines.append("- No outcome review is due.")
    lines.extend(
        [
            "",
            "## Five-Selection Navigation Review",
            "",
            f"Cohort: {scorecard['cohort_size']} / {scorecard['required_size']} resolved selections",
        ]
    )
    if not scorecard["sample_ready"]:
        lines.append(
            f"- Pending: {scorecard['remaining']} more resolved selection(s) required."
        )
    else:
        metrics = scorecard["primary_metrics"]
        lines.extend(
            [
                (
                    f"- Lower cognitive load: "
                    f"{metrics['lower_cognitive_load']['favorable']} / "
                    f"{metrics['lower_cognitive_load']['observed']} observed"
                ),
                (
                    f"- Advanced momentum: "
                    f"{metrics['advanced_momentum']['favorable']} / "
                    f"{metrics['advanced_momentum']['observed']} observed"
                ),
                (
                    f"- New useful paths: "
                    f"{metrics['new_useful_path']['favorable']} / "
                    f"{metrics['new_useful_path']['observed']} observed"
                ),
                (
                    "- Authority or membrane incidents: "
                    f"{scorecard['guardrails']['authority_or_membrane_incidents']}"
                ),
                "- Selection frequency used: no",
                f"- Assessment: `{scorecard['assessment']}`",
                f"- Rationale: {scorecard['rationale']}",
            ]
        )
    lines.extend(["", f"Authority boundary: {data['human_authority']}", ""])
    return "\n".join(lines)


def _five_selection_scorecard(
    resolved: list[dict[str, Any]],
) -> dict[str, Any]:
    required_size = 5
    cohort = resolved[:required_size]
    base = {
        "cohort_rule": "earliest-five-resolved-non-superseded",
        "required_size": required_size,
        "cohort_size": len(cohort),
        "remaining": max(0, required_size - len(cohort)),
        "sample_ready": len(cohort) == required_size,
        "choice_ids": [item["choice"]["id"] for item in cohort],
        "selection_frequency_used": False,
        "recommendation_effect": (
            "Descriptive pilot evidence only; comparable-outcome thresholds remain controlling."
        ),
    }
    if len(cohort) < required_size:
        return {
            **base,
            "primary_metrics": {},
            "supporting_evidence": {},
            "guardrails": {
                "authority_or_membrane_incidents": 0,
                "incident_choice_ids": [],
                "selection_frequency_used": False,
            },
            "assessment": "pending",
            "rationale": "Five resolved, non-superseded selections are required.",
        }

    payloads = [item["outcome"]["payload"] for item in cohort]
    cognitive = _pilot_metric(
        payloads,
        field="cognitive_load",
        favorable="lower",
        target=3,
    )
    momentum = _pilot_metric(
        payloads,
        field="momentum",
        favorable="advanced",
        target=3,
    )
    discovery = _pilot_metric(
        payloads,
        field="discovery_value",
        favorable="new-useful-path",
        target=1,
    )
    primary = {
        "lower_cognitive_load": cognitive,
        "advanced_momentum": momentum,
        "new_useful_path": discovery,
    }
    incidents = [
        item["choice"]["id"]
        for item in cohort
        if item["outcome"]["payload"].get("authority_issue")
        or item["outcome"]["payload"].get("membrane_issue")
    ]
    negative_choices = [
        item["choice"]["id"]
        for item in cohort
        if item["outcome"]["payload"].get("cognitive_load") == "higher"
        or item["outcome"]["payload"].get("momentum") == "stalled"
        or item["outcome"]["payload"].get("discovery_value") == "not-useful"
    ]
    result_counts = {result: 0 for result in OUTCOME_RESULTS}
    for payload in payloads:
        result_counts[payload["result"]] += 1
    rework_values = [
        float(payload["rework_minutes"])
        for payload in payloads
        if payload.get("rework_minutes") is not None
    ]
    observed_dimensions = [metric["observed"] for metric in primary.values()]
    positive_signals = sum(metric["signal_met"] for metric in primary.values())

    if incidents:
        assessment = "hold"
        rationale = "An authority or membrane incident overrides positive outcome signals."
    elif any(observed < 3 for observed in observed_dimensions):
        assessment = "extend-to-ten"
        rationale = "At least one primary dimension has fewer than three observations."
    elif len(negative_choices) >= 2:
        assessment = "adjust"
        rationale = "At least two selections recorded higher load, stalled momentum, or not-useful discovery."
    elif positive_signals >= 2:
        assessment = "continue"
        rationale = "At least two primary measures met their pilot signal with no guardrail incident."
    else:
        assessment = "adjust"
        rationale = "Observable evidence did not meet the two-measure continuation threshold."

    return {
        **base,
        "primary_metrics": primary,
        "supporting_evidence": {
            "result_counts": result_counts,
            "negative_experience_count": len(negative_choices),
            "negative_experience_choice_ids": negative_choices,
            "rework_minutes": {
                "observed": len(rework_values),
                "total": round(sum(rework_values), 2),
                "median": round(float(median(rework_values)), 2)
                if rework_values
                else None,
            },
        },
        "guardrails": {
            "authority_or_membrane_incidents": len(incidents),
            "incident_choice_ids": incidents,
            "selection_frequency_used": False,
        },
        "assessment": assessment,
        "rationale": rationale,
    }


def _pilot_metric(
    payloads: list[dict[str, Any]],
    *,
    field: str,
    favorable: str,
    target: int,
) -> dict[str, Any]:
    observed = [payload[field] for payload in payloads if payload[field] != "Missing"]
    favorable_count = sum(value == favorable for value in observed)
    return {
        "favorable_value": favorable,
        "favorable": favorable_count,
        "observed": len(observed),
        "rate_percent": (
            round(favorable_count * 100 / len(observed), 1) if observed else None
        ),
        "pilot_target": target,
        "signal_met": favorable_count >= target,
    }


def _validate_selection_packet(packet: dict[str, Any]) -> dict[str, Any]:
    required = (
        "id",
        "workspace_id",
        "lane",
        "choice_kind",
        "consequence_level",
        "decision_summary",
        "options",
        "recommendation_key",
        "selected_option_key",
        "success_signal",
        "risk_signal",
        "selected_by",
    )
    missing = [name for name in required if name not in packet or packet[name] is None]
    if missing:
        raise OpsError(f"Choice selection is missing required fields: {', '.join(missing)}")
    consequence = _text(packet["consequence_level"])
    if consequence not in CONSEQUENCE_LEVELS:
        raise OpsError(f"Invalid consequence_level: {consequence}")
    options = packet["options"]
    if not isinstance(options, list) or not 3 <= len(options) <= 4:
        raise OpsError("Choice selection requires 3-4 possibilities")
    normalized_options = []
    seen_keys: set[str] = set()
    seen_roles: set[str] = set()
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            raise OpsError(f"Choice option {index} must be a mapping")
        normalized = {
            "key": _bounded(option.get("key"), f"option {index} key", required=True, maximum=120),
            "role": _bounded(option.get("role"), f"option {index} role", required=True, maximum=40),
            "label": _bounded(option.get("label"), f"option {index} label", required=True),
            "tradeoff": _bounded(option.get("tradeoff"), f"option {index} tradeoff", required=True),
            "expected_outcome": _bounded(
                option.get("expected_outcome"), f"option {index} expected_outcome", required=True
            ),
            "risk": _bounded(option.get("risk"), f"option {index} risk", required=True),
            "learning_refs": _string_list(
                option.get("learning_refs", []), f"option {index} learning_refs"
            ),
        }
        if normalized["key"] in seen_keys:
            raise OpsError(f"Duplicate choice option key: {normalized['key']}")
        if normalized["role"] not in CHOICE_ROLES:
            raise OpsError(f"Invalid choice option role: {normalized['role']}")
        if normalized["role"] in seen_roles:
            raise OpsError(f"Duplicate choice option role: {normalized['role']}")
        seen_keys.add(normalized["key"])
        seen_roles.add(normalized["role"])
        normalized_options.append(normalized)
    for required_role in ("recommended", "alternative"):
        if required_role not in seen_roles:
            raise OpsError(f"Choice options require the {required_role} role")
    if not ({"overlooked", "pause-or-deepen"} & seen_roles):
        raise OpsError(
            "Choice options require an overlooked or pause-or-deepen possibility"
        )
    recommendation_key = _text(packet["recommendation_key"])
    selected_key = _text(packet["selected_option_key"])
    option_by_key = {option["key"]: option for option in normalized_options}
    if recommendation_key not in option_by_key:
        raise OpsError("recommendation_key must name a presented option")
    if option_by_key[recommendation_key]["role"] != "recommended":
        raise OpsError("recommendation_key must bind the recommended option")
    if selected_key not in option_by_key:
        raise OpsError("selected_option_key must name a presented option")
    learning_refs = _string_list(packet.get("learning_refs", []), "learning_refs")
    normalized = {
        "id": _bounded(packet["id"], "id", required=True, maximum=200),
        "workspace_id": _bounded(packet["workspace_id"], "workspace_id", required=True),
        "lane": _bounded(packet["lane"], "lane", required=True),
        "choice_kind": _bounded(packet["choice_kind"], "choice_kind", required=True),
        "consequence_level": consequence,
        "decision_summary": _bounded(packet["decision_summary"], "decision_summary", required=True),
        "options": normalized_options,
        "recommendation_key": recommendation_key,
        "selected_option_key": selected_key,
        "learning_refs": learning_refs,
        "learning_context": packet.get("learning_context", {"learning_refs": learning_refs}),
        "success_signal": _bounded(packet["success_signal"], "success_signal", required=True),
        "risk_signal": _bounded(packet["risk_signal"], "risk_signal", required=True),
        "source_ref": _nullable_bounded(packet.get("source_ref"), "source_ref") or "",
        "presented_at": _nullable_bounded(packet.get("presented_at"), "presented_at", maximum=100),
        "selected_at": _nullable_bounded(packet.get("selected_at"), "selected_at", maximum=100)
        or now_utc(),
        "review_after": _nullable_bounded(packet.get("review_after"), "review_after", maximum=100)
        or now_utc(),
        "selected_by": _bounded(packet["selected_by"], "selected_by", required=True),
        "actor_id": _nullable_bounded(packet.get("actor_id"), "actor_id", maximum=200),
        "evidence_ref": _nullable_bounded(packet.get("evidence_ref"), "evidence_ref") or "",
        "recorded_at": _nullable_bounded(packet.get("recorded_at"), "recorded_at", maximum=100)
        or now_utc(),
        "option_by_key": option_by_key,
    }
    _privacy_safe(
        {key: value for key, value in normalized.items() if key != "option_by_key"},
        "choice selection",
    )
    for timestamp_name in (
        "presented_at",
        "selected_at",
        "review_after",
        "recorded_at",
    ):
        if normalized[timestamp_name]:
            _timestamp(normalized[timestamp_name])
    if len(_canonical_json(normalized_options)) > MAX_JSON:
        raise OpsError("Choice option set is too large")
    return normalized


def _validate_event_payload(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    value = dict(payload)
    if event_type == "outcome_recorded":
        result = _text(value.get("result"))
        if result not in OUTCOME_RESULTS:
            raise OpsError(f"Invalid choice outcome result: {result}")
        value["result"] = result
        value["cognitive_load"] = _enum_or_missing(
            value.get("cognitive_load"), COGNITIVE_LOAD, "cognitive_load"
        )
        value["momentum"] = _enum_or_missing(value.get("momentum"), MOMENTUM, "momentum")
        value["discovery_value"] = _enum_or_missing(
            value.get("discovery_value"), DISCOVERY_VALUE, "discovery_value"
        )
        value["observation"] = _bounded(
            value.get("observation", "Missing"), "observation", required=True
        )
        rework = value.get("rework_minutes")
        if rework is not None:
            rework = float(rework)
            if rework < 0:
                raise OpsError("rework_minutes must be non-negative")
        value["rework_minutes"] = rework
        value["authority_issue"] = bool(value.get("authority_issue", False))
        value["membrane_issue"] = bool(value.get("membrane_issue", False))
    elif event_type == "review_deferred":
        value = {
            "review_after": _bounded(
                value.get("review_after"), "review_after", required=True, maximum=100
            ),
            "reason": _bounded(value.get("reason"), "reason", required=True),
        }
        _timestamp(value["review_after"])
    elif event_type == "corrected":
        value["reason"] = _bounded(value.get("reason"), "reason", required=True)
        replacement = value.get("replacement_outcome")
        if replacement is not None:
            if not isinstance(replacement, dict):
                raise OpsError("replacement_outcome must be a mapping")
            value["replacement_outcome"] = _validate_event_payload(
                "outcome_recorded", replacement
            )
    elif event_type == "superseded":
        value = {
            "reason": _bounded(value.get("reason"), "reason", required=True),
            "superseding_choice_id": _bounded(
                value.get("superseding_choice_id"),
                "superseding_choice_id",
                required=True,
                maximum=200,
            ),
        }
    return value


def _attention_flags(
    prompt: sqlite3.Row,
    state: str,
    outcome: dict[str, Any] | None,
    verification: dict[str, Any],
) -> list[dict[str, str]]:
    flags = []
    if not verification["ok"]:
        flags.append({"priority": "P0", "code": "invalid-chain", "message": "Choice event chain failed verification."})
    if outcome and (
        outcome["payload"].get("authority_issue")
        or outcome["payload"].get("membrane_issue")
    ):
        flags.append({"priority": "P0", "code": "authority-or-membrane-incident", "message": "Outcome recorded a controlling boundary incident."})
    if state in {"selected", "review_deferred", "outcome_pending"}:
        flags.append({"priority": "P2", "code": "outcome-unresolved", "message": "Selected branch lacks a resolved outcome."})
    if prompt["consequence_level"] != "ordinary":
        flags.append({"priority": "P1", "code": "authority-separate", "message": "Choice receipt grants no consequential action authority."})
    return flags


def _event_hash(values: dict[str, Any]) -> str:
    payload = {key: values[key] for key in _event_hash_fields()}
    return _hash(payload)


def _event_hash_fields() -> tuple[str, ...]:
    return (
        "id",
        "choice_id",
        "tenant_id",
        "event_key",
        "sequence",
        "event_type",
        "actor_id",
        "actor_label",
        "action_summary",
        "occurred_at",
        "evidence_ref",
        "payload_json",
        "recorded_at",
        "prior_hash",
    )


def _event_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "event_key": row["event_key"],
        "sequence": row["sequence"],
        "event_type": row["event_type"],
        "actor_id": row["actor_id"],
        "actor_label": row["actor_label"],
        "action_summary": row["action_summary"],
        "occurred_at": row["occurred_at"],
        "recorded_at": row["recorded_at"],
        "evidence_ref": row["evidence_ref"],
        "payload": json.loads(row["payload_json"]),
        "prior_hash": row["prior_hash"],
        "event_hash": row["event_hash"],
    }


def _prompt(connection: sqlite3.Connection, choice_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM choice_prompt WHERE id = ?", (choice_id,)
    ).fetchone()
    if not row:
        raise OpsError(f"Unknown choice: {choice_id}")
    return row


def _validate_actor(
    connection: sqlite3.Connection, tid: str, actor_id: str | None
) -> None:
    if not actor_id:
        return
    actor = connection.execute(
        "SELECT id FROM actor WHERE id = ? AND tenant_id = ? AND active = 1",
        (actor_id, tid),
    ).fetchone()
    if not actor:
        raise OpsError(f"Unknown or cross-tenant choice actor: {actor_id}")


def _selected_label(projection: dict[str, Any]) -> str:
    selected_key = projection["selection"]["payload"]["selected_option_key"]
    return next(
        option["label"] for option in projection["options"] if option["key"] == selected_key
    )


def _guidance_rationale(
    resolved_count: int,
    guardrails: list[dict[str, str]],
    favored: list[str],
    demoted: list[str],
) -> str:
    if guardrails:
        return "Prior outcomes contain an authority or membrane guardrail; surface it immediately."
    if favored or demoted:
        return "At least one comparable option has pattern-level outcome evidence; preserve an overlooked path while using it."
    if resolved_count:
        return "Comparable outcomes remain thin; cite them without changing option order."
    return "No comparable outcome evidence is available; use current evidence and repository learning."


def _bounded(
    value: Any,
    name: str,
    *,
    required: bool,
    maximum: int = MAX_TEXT,
) -> str:
    text = _text(value)
    if required and not text:
        raise OpsError(f"{name} is required")
    if len(text) > maximum:
        raise OpsError(f"{name} exceeds {maximum} characters")
    if scan_text(text):
        raise OpsError(f"{name} failed privacy scanning")
    return text


def _nullable_bounded(
    value: Any, name: str, *, maximum: int = MAX_TEXT
) -> str | None:
    text = _text(value)
    return _bounded(text, name, required=False, maximum=maximum) or None


def _string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list):
        raise OpsError(f"{name} must be a list")
    if len(value) > 20:
        raise OpsError(f"{name} contains too many values")
    return [_bounded(item, name, required=True, maximum=300) for item in value]


def _enum_or_missing(value: Any, allowed: tuple[str, ...], name: str) -> str:
    text = _text(value) or "Missing"
    if text not in allowed:
        raise OpsError(f"Invalid {name}: {text}")
    return text


def _privacy_safe(value: Any, context: str) -> None:
    serialized = _canonical_json(value)
    if len(serialized) > MAX_JSON:
        raise OpsError(f"{context} is too large")
    if scan_text(serialized):
        raise OpsError(f"{context} failed privacy scanning")
    lowered = serialized.lower()
    for key in (
        "evidence_body",
        "raw_evidence",
        "raw_content",
        "customer_private_body",
        "client_private_body",
    ):
        if f'"{key}"' in lowered:
            raise OpsError(f"{context} may link evidence but may not store {key}")


def _timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(_text(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise OpsError(f"Invalid timestamp: {value}") from exc
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()
