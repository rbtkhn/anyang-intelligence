from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .ops_service import MutationResult, OpsError, add_actor, init_tenant, now_utc, tenant_id


WORKROOM_SCHEMA_VERSION = 1
COUNCIL_ROLES = ("engineer", "executive", "artistic", "interface", "steward", "client")
EVENT_TYPES = (
    "recommendation_recorded",
    "authority_disposition_recorded",
    "execution_recorded",
    "evidence_returned",
    "reconciliation_recorded",
    "metric_recorded",
    "held",
    "blocked",
    "corrected",
    "superseded",
)
TERMINAL_STATES = ("complete", "held", "blocked", "corrected", "superseded")
BACKFILL_CATEGORIES = {
    1: "system-improvement",
    2: "research-to-primitive",
    3: "translation-integrity",
    4: "priority-decision",
    5: "blocked-or-escalated",
}
BACKFILL_STATES = {1: "complete", 2: "approved", 3: "complete", 4: "executing", 5: "held"}
COMMON_PACKET_FIELDS = {
    "id",
    "event_key",
    "actor_id",
    "actor_label",
    "council_role",
    "action_summary",
    "occurred_at",
    "recorded_at",
    "evidence_ref",
    "attribution_status",
    "payload",
}


def load_packet(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise OpsError(f"Council packet must be a YAML mapping: {source}")
    return data


def create_council_transaction(
    connection: sqlite3.Connection,
    tenant: str,
    packet: dict[str, Any],
) -> MutationResult:
    required = ("id", "title", "council_scope", "decision_class")
    _require_fields(packet, required, "Council transaction")
    tid = tenant_id(connection, tenant)
    work_id = _text(packet.get("work_id"))
    if work_id:
        row = connection.execute(
            "SELECT id FROM work_item WHERE id = ? AND tenant_id = ?", (work_id, tid)
        ).fetchone()
        if not row:
            raise OpsError(f"Unknown work item for tenant: {work_id}")
    values = {
        "id": _text(packet["id"]),
        "tenant_id": tid,
        "title": _text(packet["title"]),
        "council_scope": _text(packet["council_scope"]),
        "decision_class": _text(packet["decision_class"]),
        "pilot_category": _text(packet.get("pilot_category")),
        "work_id": work_id or None,
        "source_ref": _text(packet.get("source_ref")),
        "created_at": _text(packet.get("created_at")) or now_utc(),
    }
    existing = connection.execute(
        "SELECT * FROM council_transaction WHERE id = ?", (values["id"],)
    ).fetchone()
    if existing:
        comparable = (
            "tenant_id",
            "title",
            "council_scope",
            "decision_class",
            "pilot_category",
            "work_id",
            "source_ref",
        )
        if all(existing[key] == values[key] for key in comparable):
            return MutationResult("council_transaction_exists", values["id"], {"idempotent": True})
        raise OpsError(f"Council transaction conflicts with existing record: {values['id']}")
    connection.execute(
        """INSERT INTO council_transaction(
            id, tenant_id, title, council_scope, decision_class, pilot_category,
            work_id, source_ref, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(values[key] for key in values),
    )
    connection.commit()
    return MutationResult("council_transaction_created", values["id"], {"idempotent": False})


def record_council_event(
    connection: sqlite3.Connection,
    transaction_id: str,
    event_type: str,
    packet: dict[str, Any],
    *,
    historical: bool = False,
) -> MutationResult:
    if event_type not in EVENT_TYPES:
        raise OpsError(f"Unsupported Council event type: {event_type}")
    transaction = _transaction(connection, transaction_id)
    payload = packet.get("payload")
    if payload is None:
        payload = {key: value for key, value in packet.items() if key not in COMMON_PACKET_FIELDS}
    if not isinstance(payload, dict):
        raise OpsError("Council event payload must be a mapping")
    action_summary = _text(packet.get("action_summary"))
    if not action_summary:
        raise OpsError("Council event requires action_summary")
    attribution_status = _text(packet.get("attribution_status")) or "attributed"
    if attribution_status not in {"attributed", "historical-missing"}:
        raise OpsError(f"Invalid attribution status: {attribution_status}")
    actor_id, actor_label, council_role = _resolve_actor(
        connection, transaction, packet, attribution_status, historical
    )
    evidence_ref = _text(packet.get("evidence_ref"))
    if event_type == "evidence_returned" and not historical and not evidence_ref:
        raise OpsError("Live evidence returns require an evidence_ref")
    _validate_event_payload(
        connection, transaction, event_type, payload, historical=historical
    )
    payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    event_key = _text(packet.get("event_key")) or _text(packet.get("id")) or str(uuid.uuid4())
    existing = connection.execute(
        "SELECT * FROM council_event WHERE transaction_id = ? AND event_key = ?",
        (transaction_id, event_key),
    ).fetchone()
    semantic = {
        "event_type": event_type,
        "actor_id": actor_id,
        "actor_label": actor_label,
        "council_role": council_role,
        "action_summary": action_summary,
        "occurred_at": _nullable_text(packet.get("occurred_at")),
        "evidence_ref": evidence_ref,
        "attribution_status": attribution_status,
        "payload_json": payload_json,
    }
    if existing:
        if all(existing[key] == value for key, value in semantic.items()):
            return MutationResult("council_event_exists", existing["id"], {"idempotent": True})
        raise OpsError(
            f"Council event key conflicts with existing event: {transaction_id}/{event_key}"
        )
    prior = connection.execute(
        """SELECT sequence, event_hash FROM council_event
        WHERE transaction_id = ? ORDER BY sequence DESC LIMIT 1""",
        (transaction_id,),
    ).fetchone()
    sequence = int(prior["sequence"]) + 1 if prior else 1
    prior_hash = str(prior["event_hash"]) if prior else ""
    event_id = _text(packet.get("id")) or (
        str(uuid.uuid5(uuid.NAMESPACE_URL, f"anyang:council:{transaction_id}:{event_key}"))
        if historical
        else str(uuid.uuid4())
    )
    recorded_at = _text(packet.get("recorded_at")) or now_utc()
    hash_payload = {
        "id": event_id,
        "transaction_id": transaction_id,
        "tenant_id": transaction["tenant_id"],
        "event_key": event_key,
        "sequence": sequence,
        **semantic,
        "recorded_at": recorded_at,
        "prior_hash": prior_hash,
    }
    event_hash = _hash(hash_payload)
    connection.execute(
        """INSERT INTO council_event(
            id, transaction_id, tenant_id, event_key, sequence, event_type,
            actor_id, actor_label, council_role, action_summary, occurred_at,
            recorded_at, evidence_ref, attribution_status, payload_json,
            prior_hash, event_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            event_id,
            transaction_id,
            transaction["tenant_id"],
            event_key,
            sequence,
            event_type,
            actor_id,
            actor_label,
            council_role,
            action_summary,
            semantic["occurred_at"],
            recorded_at,
            evidence_ref,
            attribution_status,
            payload_json,
            prior_hash,
            event_hash,
        ),
    )
    connection.commit()
    return MutationResult(
        "council_event_recorded",
        event_id,
        {"transaction_id": transaction_id, "sequence": sequence, "event_hash": event_hash},
    )


def council_subject_hash(connection: sqlite3.Connection, transaction_id: str) -> str:
    transaction = _transaction(connection, transaction_id)
    recommendations = connection.execute(
        """SELECT event_hash FROM council_event
        WHERE transaction_id = ? AND event_type = 'recommendation_recorded'
        ORDER BY sequence""",
        (transaction_id,),
    ).fetchall()
    payload = {
        "transaction": {
            key: transaction[key]
            for key in (
                "id",
                "tenant_id",
                "title",
                "council_scope",
                "decision_class",
                "pilot_category",
                "work_id",
                "source_ref",
            )
        },
        "recommendation_event_hashes": [row["event_hash"] for row in recommendations],
    }
    return _hash(payload)


def verify_council_transaction(
    connection: sqlite3.Connection, transaction_id: str
) -> dict[str, Any]:
    transaction = _transaction(connection, transaction_id)
    events = connection.execute(
        "SELECT * FROM council_event WHERE transaction_id = ? ORDER BY sequence",
        (transaction_id,),
    ).fetchall()
    issues: list[dict[str, str]] = []
    prior_hash = ""
    for expected_sequence, row in enumerate(events, start=1):
        if row["tenant_id"] != transaction["tenant_id"]:
            issues.append(
                {"code": "tenant-mismatch", "message": f"Event {row['id']} crosses tenant boundary."}
            )
        if row["sequence"] != expected_sequence:
            issues.append(
                {"code": "sequence-gap", "message": f"Expected sequence {expected_sequence}."}
            )
        if row["prior_hash"] != prior_hash:
            issues.append(
                {"code": "prior-hash-mismatch", "message": f"Event {row['id']} has a broken link."}
            )
        semantic = {
            "event_type": row["event_type"],
            "actor_id": row["actor_id"],
            "actor_label": row["actor_label"],
            "council_role": row["council_role"],
            "action_summary": row["action_summary"],
            "occurred_at": row["occurred_at"],
            "evidence_ref": row["evidence_ref"],
            "attribution_status": row["attribution_status"],
            "payload_json": row["payload_json"],
        }
        expected_hash = _hash(
            {
                "id": row["id"],
                "transaction_id": row["transaction_id"],
                "tenant_id": row["tenant_id"],
                "event_key": row["event_key"],
                "sequence": row["sequence"],
                **semantic,
                "recorded_at": row["recorded_at"],
                "prior_hash": row["prior_hash"],
            }
        )
        if expected_hash != row["event_hash"]:
            issues.append(
                {"code": "event-hash-mismatch", "message": f"Event {row['id']} failed hashing."}
            )
        prior_hash = row["event_hash"]
    return {
        "transaction_id": transaction_id,
        "ok": not issues,
        "event_count": len(events),
        "head_hash": prior_hash,
        "issues": issues,
    }


def council_projection(
    connection: sqlite3.Connection,
    transaction_id: str,
    *,
    as_of: str | None = None,
) -> dict[str, Any]:
    transaction = _transaction(connection, transaction_id)
    rows = connection.execute(
        "SELECT * FROM council_event WHERE transaction_id = ? ORDER BY sequence",
        (transaction_id,),
    ).fetchall()
    events = [_event_dict(row) for row in rows]
    sections: dict[str, list[dict[str, Any]]] = {"A": [], "B": [], "C": [], "D": []}
    metrics: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    authority_bindings: list[dict[str, Any]] = []
    current_state = "proposed"
    current_subject_hash = council_subject_hash(connection, transaction_id)
    for event in events:
        payload = event["payload"]
        event_type = event["event_type"]
        if event_type == "recommendation_recorded":
            sections["A"].append(event)
            current_state = "recommended"
        elif event_type == "authority_disposition_recorded":
            sections["B"].append(event)
            authority_bindings.append(
                {
                    "event_id": event["id"],
                    "decision": payload.get("decision"),
                    "subject_hash": payload.get("subject_hash"),
                    "anyang_authority_ref": payload.get("anyang_authority_ref", ""),
                    "client_authority_ref": payload.get("client_authority_ref", ""),
                }
            )
            decision = str(payload.get("decision", "")).lower()
            current_state = "approved" if decision in {"approved", "approved_with_changes"} else decision or "awaiting_approval"
        elif event_type == "execution_recorded":
            sections["C"].append(event)
            if payload.get("executor_invoked"):
                current_state = "executing"
        elif event_type == "evidence_returned":
            sections["C"].append(event)
            evidence.append(event)
            current_state = "evidence_returned"
        elif event_type == "reconciliation_recorded":
            sections["D"].append(event)
            terminal = str(payload.get("terminal_state", "")).lower()
            if terminal:
                current_state = terminal
        elif event_type == "metric_recorded":
            metrics.append(event)
        elif event_type in {"held", "blocked", "corrected", "superseded"}:
            current_state = event_type
    verification = verify_council_transaction(connection, transaction_id)
    flags = _attention_flags(
        connection,
        transaction,
        events,
        current_state,
        current_subject_hash,
        verification,
        as_of or now_utc(),
    )
    return {
        "schema_version": WORKROOM_SCHEMA_VERSION,
        "transaction": {
            key: transaction[key]
            for key in (
                "id",
                "tenant_id",
                "title",
                "council_scope",
                "decision_class",
                "pilot_category",
                "work_id",
                "source_ref",
                "created_at",
            )
        },
        "current_state": current_state,
        "subject_hash": current_subject_hash,
        "sections": sections,
        "events": events,
        "authority_bindings": authority_bindings,
        "evidence": evidence,
        "metrics": metrics,
        "attention_flags": flags,
        "lineage": {
            "source_ref": transaction["source_ref"],
            "event_count": verification["event_count"],
            "head_hash": verification["head_hash"],
            "chain_verified": verification["ok"],
        },
    }


def council_inbox(
    connection: sqlite3.Connection, tenant: str, as_of: str | None = None
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    rows = connection.execute(
        "SELECT id FROM council_transaction WHERE tenant_id = ? ORDER BY created_at, id", (tid,)
    ).fetchall()
    entries: list[dict[str, Any]] = []
    for row in rows:
        projection = council_projection(connection, row["id"], as_of=as_of)
        flags = projection["attention_flags"]
        priority = min((flag["priority"] for flag in flags), default="P3")
        latest = projection["events"][-1] if projection["events"] else None
        verb = latest["action_summary"] if latest else "Opened transaction"
        entries.append(
            {
                "transaction_id": row["id"],
                "title": projection["transaction"]["title"],
                "priority": priority,
                "current_state": projection["current_state"],
                "headline": f"{verb} → {projection['transaction']['title']} → {projection['current_state']}",
                "attention_needed": [flag["message"] for flag in flags],
                "next_evidence_or_approval": [flag["needed"] for flag in flags if flag.get("needed")],
            }
        )
    entries.sort(key=lambda item: (item["priority"], item["transaction_id"]))
    return {
        "schema_version": WORKROOM_SCHEMA_VERSION,
        "tenant": tenant,
        "as_of": as_of or now_utc(),
        "counts": {
            priority: sum(1 for item in entries if item["priority"] == priority)
            for priority in ("P0", "P1", "P2", "P3")
        },
        "entries": entries,
        "human_authority": "This inbox prepares attention. It grants no approval or execution authority.",
    }


def render_council_markdown(data: dict[str, Any]) -> str:
    transaction = data["transaction"]
    lines = [
        f"# {transaction['title']}",
        "",
        f"Transaction: `{transaction['id']}`",
        f"State: `{data['current_state']}`",
        f"Decision class: `{transaction['decision_class']}`",
        f"Scope: {transaction['council_scope']}",
        f"Subject hash: `{data['subject_hash']}`",
        "",
    ]
    for key, title in (
        ("A", "Recommendation"),
        ("B", "Authority Disposition"),
        ("C", "Execution And Evidence"),
        ("D", "Reconciliation"),
    ):
        lines.extend([f"## {key}. {title}", ""])
        events = data["sections"][key]
        if not events:
            lines.append("- Missing")
        for event in events:
            lines.append(f"- {event['action_summary']} — {event['actor_label']}")
            source_markdown = str(event["payload"].get("source_markdown", "")).strip()
            if source_markdown:
                lines.extend(["", source_markdown, ""])
        lines.append("")
    lines.extend(["## Metrics", ""])
    if not data["metrics"]:
        lines.append("- Missing")
    for event in data["metrics"]:
        payload = event["payload"]
        lines.append(
            f"- {payload.get('name', 'metric')}: {payload.get('observed_value', 'Missing')} "
            f"(`{payload.get('observation_status', 'missing')}`)"
        )
    lines.extend(["", "## Attention", ""])
    if not data["attention_flags"]:
        lines.append("- No structural attention flags.")
    for flag in data["attention_flags"]:
        suffix = f" Needed: {flag['needed']}" if flag.get("needed") else ""
        lines.append(f"- {flag['priority']} `{flag['code']}`: {flag['message']}.{suffix}")
    lines.extend(
        [
            "",
            "## Lineage",
            "",
            f"- Source: {data['lineage']['source_ref'] or 'Missing'}",
            f"- Event count: {data['lineage']['event_count']}",
            f"- Chain verified: {data['lineage']['chain_verified']}",
            f"- Head hash: `{data['lineage']['head_hash']}`",
            "",
            "## Human Authority Boundary",
            "",
            "- This projection records and prepares judgment. It does not grant execution authority.",
            "",
        ]
    )
    return "\n".join(lines)


def render_council_inbox_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Executive Council Attention Inbox",
        "",
        f"Tenant: `{data['tenant']}`",
        f"As of: {data['as_of']}",
        "",
        "## Attention",
        "",
    ]
    for entry in data["entries"]:
        lines.append(
            f"- **{entry['priority']}** {entry['headline']} (`{entry['transaction_id']}`)"
        )
        for needed in entry["next_evidence_or_approval"]:
            lines.append(f"  - Needed: {needed}")
    if not data["entries"]:
        lines.append("- No Council transactions.")
    lines.extend(["", "## Human Authority Boundary", "", f"- {data['human_authority']}", ""])
    return "\n".join(lines)


def council_pilot_review(
    connection: sqlite3.Connection,
    tenant: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    rows = connection.execute(
        "SELECT id FROM council_transaction WHERE tenant_id = ? ORDER BY id",
        (tid,),
    ).fetchall()
    projections = [
        council_projection(connection, row["id"], as_of=as_of) for row in rows
    ]
    consequential = [
        projection
        for projection in projections
        if _decision_class_number(projection["transaction"]["decision_class"]) > 0
    ]
    covered = [
        projection
        for projection in consequential
        if _has_complete_receipt(projection)
    ]
    unsupported = [
        projection["transaction"]["id"]
        for projection in projections
        if any(
            flag["code"] == "unsupported-execution"
            for flag in projection["attention_flags"]
        )
    ]
    burden_metrics = []
    for projection in projections:
        for event in projection["metrics"]:
            name = _text(event["payload"].get("name"))
            if re.search(r"time|burden|rework|interruption|aging|correction", name, re.I):
                burden_metrics.append(
                    {
                        "transaction_id": projection["transaction"]["id"],
                        "name": name,
                        "value": event["payload"].get("observed_value", "Missing"),
                        "status": event["payload"].get("observation_status", "missing"),
                        "evidence_ref": event["evidence_ref"],
                    }
                )
    denominator = len(consequential)
    return {
        "schema_version": WORKROOM_SCHEMA_VERSION,
        "tenant": tenant,
        "as_of": as_of or now_utc(),
        "transaction_count": len(projections),
        "consequential_transaction_count": denominator,
        "receipt_coverage": {
            "covered": len(covered),
            "total": denominator,
            "percent": round(100 * len(covered) / denominator, 2) if denominator else 0.0,
            "missing_transaction_ids": sorted(
                set(item["transaction"]["id"] for item in consequential)
                - set(item["transaction"]["id"] for item in covered)
            ),
        },
        "unauthorized_progression": {
            "count": len(unsupported),
            "transaction_ids": unsupported,
        },
        "operator_burden_measurements": burden_metrics,
        "missing_operator_burden_measurements": sum(
            1 for metric in burden_metrics if metric["status"] == "missing"
        ),
        "states": {
            projection["transaction"]["id"]: projection["current_state"]
            for projection in projections
        },
        "human_authority": (
            "This review measures the ledger. A continuation, expansion, or authority "
            "decision still requires an exact human disposition."
        ),
    }


def render_council_pilot_review_markdown(data: dict[str, Any]) -> str:
    coverage = data["receipt_coverage"]
    unsupported = data["unauthorized_progression"]
    lines = [
        "# Chief Executive–Executive Assistant Pilot Metrics Review",
        "",
        f"- Pilot tenant: `{data['tenant']}`",
        f"- Review date: {data['as_of']}",
        f"- Transactions: {data['transaction_count']}",
        "",
        "## Measures",
        "",
        "| Measure | Pilot result | Evidence | Interpretation |",
        "| --- | --- | --- | --- |",
        (
            f"| Receipt coverage | {coverage['percent']:.2f}% "
            f"({coverage['covered']}/{coverage['total']}) | Council event chains | "
            "Consequential transactions with recommendation, exact authority, and "
            "execution/evidence or explicit no-action receipt |"
        ),
        (
            f"| Unauthorized progression | {unsupported['count']} | "
            f"{', '.join(unsupported['transaction_ids']) or 'No flagged transactions'} | "
            "Execution without authority bound to the current subject |"
        ),
        (
            f"| Missing operator-burden measurements | "
            f"{data['missing_operator_burden_measurements']} | Metric events | "
            "Missing remains explicit until observed |"
        ),
    ]
    for metric in data["operator_burden_measurements"]:
        lines.append(
            f"| {metric['name']} | {metric['value']} | "
            f"{metric['evidence_ref'] or metric['transaction_id']} | "
            f"{metric['status']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- Net cognitive load reduced: `Unclear — human review required`",
            "- Records reliable: `Unclear — human review required`",
            "- Next stage: `Human decision required`",
            f"- Authority boundary: {data['human_authority']}",
            "",
        ]
    )
    return "\n".join(lines)


def friction_backfill_plan(cohort_path: str | Path, tracker_path: str | Path) -> dict[str, Any]:
    cohort = Path(cohort_path)
    tracker = Path(tracker_path)
    cases = _parse_friction_cases(cohort.read_text(encoding="utf-8"))
    tracker_text = tracker.read_text(encoding="utf-8")
    if len(cases) != 5:
        raise OpsError(f"Expected five friction cases, found {len(cases)}")
    for case in cases:
        if f"#case-{case['number']}" not in tracker_text.lower():
            raise OpsError(f"Tracker does not link friction case {case['number']}")
    return {
        "cohort": str(cohort),
        "tracker": str(tracker),
        "case_count": len(cases),
        "transactions": [
            {
                "id": case["transaction_id"],
                "title": case["title"],
                "source_state": case["source_state"],
                "normalized_state": BACKFILL_STATES[case["number"]],
                "metric_count": len(case["metrics"]),
            }
            for case in cases
        ],
    }


def backfill_friction_pilot(
    connection: sqlite3.Connection,
    tenant: str,
    cohort_path: str | Path,
    tracker_path: str | Path,
) -> MutationResult:
    plan = friction_backfill_plan(cohort_path, tracker_path)
    cases = _parse_friction_cases(Path(cohort_path).read_text(encoding="utf-8"))
    actors = _ensure_internal_council(connection, tenant)
    source_ref_base = Path(cohort_path).as_posix()
    tracker_ref = Path(tracker_path).as_posix()
    event_total = 0
    for case in cases:
        anchor = f"{source_ref_base}#case-{case['number']}"
        create_council_transaction(
            connection,
            tenant,
            {
                "id": case["transaction_id"],
                "title": case["title"],
                "council_scope": "Internal Executive Council friction pilot",
                "decision_class": case["decision_class"],
                "pilot_category": BACKFILL_CATEGORIES[case["number"]],
                "source_ref": anchor,
            },
        )
        recommendation_payload = {
            "decision": _bullet(case["sections"]["A"], "Decision") or "Missing",
            "evidence": _bullet(case["sections"]["A"], "Evidence")
            or _bullet(case["sections"]["A"], "Source")
            or "Missing",
            "recommendation": _bullet(case["sections"]["A"], "Recommendation") or "Missing",
            "success_condition": "Missing",
            "source_markdown": case["sections"]["A"],
            "source_state": case["source_state"],
            "tracker_ref": tracker_ref,
        }
        record_council_event(
            connection,
            case["transaction_id"],
            "recommendation_recorded",
            _backfill_packet(
                "A",
                actors["executive"],
                "executive",
                "Chief Executive recorded recommendation",
                anchor,
                recommendation_payload,
            ),
            historical=True,
        )
        subject_hash = council_subject_hash(connection, case["transaction_id"])
        authority_decision = "held" if case["number"] == 5 else "approved"
        authority_payload = {
            "decision": authority_decision,
            "decision_state": authority_decision,
            "no_action_taken": case["number"] == 5,
            "approved_scope": _bullet(case["sections"]["B"], "Approved scope") or "Missing",
            "limits_exclusions": _bullet(case["sections"]["B"], "Exclusion")
            or _bullet(case["sections"]["B"], "Exclusions")
            or _bullet(case["sections"]["B"], "Gap")
            or "Missing",
            "required_evidence": "Missing",
            "anyang_authority_ref": anchor,
            "client_authority_ref": "Missing" if case["number"] == 5 else "",
            "subject_hash": subject_hash,
            "source_markdown": case["sections"]["B"],
        }
        record_council_event(
            connection,
            case["transaction_id"],
            "authority_disposition_recorded",
            _backfill_packet(
                "B",
                actors["engineer"],
                "engineer",
                "System Engineer authority disposition recorded",
                anchor,
                authority_payload,
            ),
            historical=True,
        )
        no_action = bool(
            re.search(
                r"(?:no action taken|executor invoked:\s*no|executive assistant invoked:\s*not recorded)",
                case["sections"]["C"],
                re.I,
            )
        )
        action_taken = _bullet(case["sections"]["C"], "Action taken") or (
            "No action taken" if no_action else "Historical action recorded"
        )
        executor_known = False
        execution_payload = {
            "executor_invoked": not no_action,
            "named_executor": "Missing" if not executor_known else "",
            "execution_state": "not_invoked"
            if no_action
            else ("executing" if case["number"] == 4 else "evidence_returned"),
            "action_taken": action_taken,
            "no_action_taken": no_action,
            "source_markdown": case["sections"]["C"],
        }
        record_council_event(
            connection,
            case["transaction_id"],
            "execution_recorded",
            _backfill_packet(
                "C",
                None,
                "missing",
                "Historical execution state recorded",
                anchor,
                execution_payload,
                missing=True,
            ),
            historical=True,
        )
        returned = _bullet(case["sections"]["C"], "Evidence returned") or _bullet(
            case["sections"]["C"], "Current evidence"
        )
        if returned and returned.lower() not in {"none", "missing"}:
            record_council_event(
                connection,
                case["transaction_id"],
                "evidence_returned",
                _backfill_packet(
                    "C-evidence",
                    None,
                    "missing",
                    "Historical evidence return recorded",
                    anchor,
                    {"evidence": returned, "source_markdown": case["sections"]["C"]},
                    missing=True,
                ),
                historical=True,
            )
        reconciliation_actor = None
        reconciliation_role = "missing"
        if re.search(r"Chief Executive reconciliation", case["sections"]["D"], re.I):
            reconciliation_actor = actors["executive"]
            reconciliation_role = "executive"
        elif re.search(r"Engineer disposition", case["sections"]["D"], re.I):
            reconciliation_actor = actors["engineer"]
            reconciliation_role = "engineer"
        reconciliation_payload = {
            "reconciliation_state": "supported",
            "final_supported_state": _bullet(case["sections"]["D"], "Final supported state")
            or case["source_state"],
            "terminal_state": BACKFILL_STATES[case["number"]],
            "source_markdown": case["sections"]["D"],
        }
        record_council_event(
            connection,
            case["transaction_id"],
            "reconciliation_recorded",
            _backfill_packet(
                "D",
                reconciliation_actor,
                reconciliation_role,
                "Historical reconciliation recorded",
                anchor,
                reconciliation_payload,
                missing=not bool(reconciliation_actor),
            ),
            historical=True,
        )
        for metric in case["metrics"]:
            metric_key = f"metric-{_slug(metric['name'])}"
            record_council_event(
                connection,
                case["transaction_id"],
                "metric_recorded",
                _backfill_packet(
                    metric_key,
                    None,
                    "missing",
                    f"Historical metric recorded: {metric['name']}",
                    anchor,
                    {
                        "name": metric["name"],
                        "observed_value": metric["value"],
                        "observation_status": metric["status"],
                        "source_markdown": metric["row"],
                    },
                    missing=True,
                ),
                historical=True,
            )
        if case["number"] == 5:
            record_council_event(
                connection,
                case["transaction_id"],
                "held",
                _backfill_packet(
                    "held",
                    actors["engineer"],
                    "engineer",
                    "System Engineer held transaction",
                    anchor,
                    {"reason": case["source_state"], "no_action_taken": True},
                ),
                historical=True,
            )
        event_total += connection.execute(
            "SELECT COUNT(*) FROM council_event WHERE transaction_id = ?",
            (case["transaction_id"],),
        ).fetchone()[0]
    return MutationResult(
        "council_friction_pilot_backfilled",
        "EC-FRICTION-PILOT-2026-07-24-01",
        {"transactions": plan["case_count"], "events": event_total},
    )


def _resolve_actor(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    packet: dict[str, Any],
    attribution_status: str,
    historical: bool,
) -> tuple[str | None, str, str]:
    actor_id = _text(packet.get("actor_id"))
    council_role = _text(packet.get("council_role"))
    if attribution_status == "historical-missing":
        if not historical:
            raise OpsError("historical-missing attribution is allowed only during governed backfill")
        if actor_id:
            raise OpsError("historical-missing attribution cannot name an actor_id")
        return None, _text(packet.get("actor_label")) or "Missing", council_role or "missing"
    if not actor_id:
        raise OpsError("Live Council events require actor_id")
    actor = connection.execute(
        "SELECT * FROM actor WHERE id = ? AND tenant_id = ? AND active = 1",
        (actor_id, transaction["tenant_id"]),
    ).fetchone()
    if not actor:
        raise OpsError(f"Unknown or inactive Council actor: {actor_id}")
    council_role = council_role or str(actor["role"])
    if council_role not in COUNCIL_ROLES:
        raise OpsError(f"Unsupported Council role: {council_role}")
    return actor_id, str(actor["name"]), council_role


def _validate_event_payload(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    event_type: str,
    payload: dict[str, Any],
    *,
    historical: bool,
) -> None:
    required: dict[str, tuple[str, ...]] = {
        "recommendation_recorded": ("decision", "evidence", "recommendation", "success_condition"),
        "authority_disposition_recorded": (
            "decision",
            "approved_scope",
            "limits_exclusions",
            "required_evidence",
            "subject_hash",
        ),
        "execution_recorded": (
            "executor_invoked",
            "named_executor",
            "execution_state",
            "action_taken",
        ),
        "evidence_returned": ("evidence",),
        "reconciliation_recorded": (
            "reconciliation_state",
            "final_supported_state",
            "terminal_state",
        ),
        "metric_recorded": ("name", "observed_value", "observation_status"),
        "held": ("reason", "no_action_taken"),
        "blocked": ("reason",),
        "corrected": ("reason",),
        "superseded": ("reason",),
    }
    _require_fields(payload, required[event_type], f"{event_type} payload", allow_false=True)
    _validate_privacy_boundary(connection, transaction, payload)
    if event_type == "authority_disposition_recorded" and not historical:
        recommendation_count = connection.execute(
            """SELECT COUNT(*) FROM council_event
            WHERE transaction_id = ? AND event_type = 'recommendation_recorded'""",
            (transaction["id"],),
        ).fetchone()[0]
        if not recommendation_count:
            raise OpsError("Authority disposition requires a recorded recommendation")
    if event_type == "authority_disposition_recorded":
        current_hash = council_subject_hash(connection, transaction["id"])
        if payload["subject_hash"] != current_hash and not historical:
            raise OpsError("Authority disposition does not bind the current transaction subject hash")
        decision = str(payload["decision"]).lower()
        if decision in {"held", "rejected"} and payload.get("no_action_taken") is not True:
            raise OpsError("Held or rejected authority must record No action taken")
        if decision in {"approved", "approved_with_changes"}:
            class_number = _decision_class_number(transaction["decision_class"])
            if class_number in {1, 2, 3} and not _text(payload.get("anyang_authority_ref")):
                raise OpsError("Approved consequential work requires an exact Anyang authority reference")
            if class_number == 3 and not _text(payload.get("client_authority_ref")):
                raise OpsError("Class 3 approval requires a separate client authority reference")
    if event_type == "execution_recorded" and payload.get("executor_invoked"):
        if not _text(payload.get("named_executor")) and not historical:
            raise OpsError("Invoked execution requires a named executor")
        class_number = _decision_class_number(transaction["decision_class"])
        if class_number == 0 and not historical:
            raise OpsError("Class 0 may not record invoked execution")
        if class_number in {1, 2, 3} and not historical:
            subject_hash = council_subject_hash(connection, transaction["id"])
            approvals = connection.execute(
                """SELECT payload_json FROM council_event
                WHERE transaction_id = ? AND event_type = 'authority_disposition_recorded'
                ORDER BY sequence DESC""",
                (transaction["id"],),
            ).fetchall()
            if not any(
                _authority_is_current(
                    json.loads(row["payload_json"]), subject_hash, now_utc()
                )
                for row in approvals
            ):
                raise OpsError("Execution requires a current authority disposition")
    if event_type == "evidence_returned" and not historical:
        execution = connection.execute(
            """SELECT payload_json FROM council_event
            WHERE transaction_id = ? AND event_type = 'execution_recorded'
            ORDER BY sequence DESC LIMIT 1""",
            (transaction["id"],),
        ).fetchone()
        if not execution or not json.loads(execution["payload_json"]).get("executor_invoked"):
            raise OpsError("Returned evidence requires prior invoked execution")
    if event_type == "held" and not historical:
        execution = connection.execute(
            """SELECT payload_json FROM council_event
            WHERE transaction_id = ? AND event_type = 'execution_recorded'
            ORDER BY sequence DESC LIMIT 1""",
            (transaction["id"],),
        ).fetchone()
        if (
            not execution
            or json.loads(execution["payload_json"]).get("no_action_taken") is not True
        ):
            raise OpsError("Held transactions require an explicit No action taken execution receipt")
    if event_type == "reconciliation_recorded":
        terminal = str(payload.get("terminal_state", "")).lower()
        if terminal and terminal not in (*TERMINAL_STATES, "approved", "executing", "evidence_returned"):
            raise OpsError(f"Invalid terminal_state: {terminal}")
        if terminal == "complete" and not historical:
            execution = connection.execute(
                """SELECT payload_json FROM council_event
                WHERE transaction_id = ? AND event_type = 'execution_recorded'
                ORDER BY sequence DESC LIMIT 1""",
                (transaction["id"],),
            ).fetchone()
            evidence_count = connection.execute(
                """SELECT COUNT(*) FROM council_event
                WHERE transaction_id = ? AND event_type = 'evidence_returned'""",
                (transaction["id"],),
            ).fetchone()[0]
            if not execution or not json.loads(execution["payload_json"]).get("executor_invoked"):
                raise OpsError("Complete reconciliation requires invoked execution")
            if not evidence_count:
                raise OpsError("Complete reconciliation requires returned evidence")


def _attention_flags(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    events: list[dict[str, Any]],
    current_state: str,
    subject_hash: str,
    verification: dict[str, Any],
    as_of: str,
) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    if not verification["ok"]:
        flags.append(_flag("P0", "invalid-event-chain", "Council event history failed verification", "Repair through reviewed recovery"))
    emergency = connection.execute(
        "SELECT id FROM emergency_stop WHERE status = 'active' ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    if emergency:
        flags.append(_flag("P0", "emergency-stop-active", "Repository emergency stop is active", "System Engineer restart receipt"))
    conflict = connection.execute(
        """SELECT id FROM authority_conflict
        WHERE tenant_id = ? AND status = 'open'
          AND target IN (?, ?, '*')
        ORDER BY created_at DESC LIMIT 1""",
        (
            transaction["tenant_id"],
            transaction["id"],
            transaction["council_scope"],
        ),
    ).fetchone()
    if conflict:
        flags.append(
            _flag(
                "P0",
                "authority-conflict",
                "An unresolved authority conflict exists for this tenant",
                "Controlling authority resolution",
            )
        )
    recommendations = [event for event in events if event["event_type"] == "recommendation_recorded"]
    approvals = [event for event in events if event["event_type"] == "authority_disposition_recorded"]
    matching_approvals = [
        event
        for event in approvals
        if event["payload"].get("decision") in {"approved", "approved_with_changes"}
        and event["payload"].get("subject_hash") == subject_hash
    ]
    current_approvals = [
        event
        for event in matching_approvals
        if not _is_expired(event["payload"].get("expires_at"), as_of)
    ]
    invoked = [
        event
        for event in events
        if event["event_type"] == "execution_recorded" and event["payload"].get("executor_invoked")
    ]
    evidence = [event for event in events if event["event_type"] == "evidence_returned"]
    if recommendations and not current_approvals and current_state not in {"held", "blocked", "superseded"}:
        code = (
            "authority-expired"
            if matching_approvals
            else "authority-stale"
            if approvals
            else "awaiting-approval"
        )
        message = "Recommendation lacks authority bound to its current subject hash"
        flags.append(_flag("P1", code, message, "Exact System Engineer authority disposition"))
    if invoked and not current_approvals and _decision_class_number(transaction["decision_class"]) > 0:
        flags.append(_flag("P0", "unsupported-execution", "Execution is not supported by current authority", "Stop and reconcile authority"))
    if any(
        event["attribution_status"] == "historical-missing"
        and event["event_type"] in {"execution_recorded", "reconciliation_recorded"}
        for event in events
    ):
        flags.append(_flag("P1", "missing-attribution", "Historical execution or reconciliation attribution is missing", "Preserve as Missing unless new evidence appears"))
    if invoked and not evidence and current_state in {"executing", "complete"}:
        flags.append(_flag("P1", "missing-execution-evidence", "Invoked execution lacks a returned evidence event", "Named evidence return"))
    if current_state == "blocked":
        flags.append(_flag("P1", "blocked", "Transaction is blocked", "Responsible human and resolution evidence"))
    if current_state == "held":
        flags.append(_flag("P1", "held", "Transaction is held", "Exact authority or evidence named by the hold"))
    missing_metrics = [
        event
        for event in events
        if event["event_type"] == "metric_recorded"
        and event["payload"].get("observation_status") == "missing"
    ]
    if missing_metrics:
        flags.append(_flag("P2", "missing-pilot-metrics", f"{len(missing_metrics)} pilot measurements remain Missing", "Observed timing or outcome evidence"))
    if current_state in {"executing", "evidence_returned"}:
        flags.append(_flag("P2", "reconciliation-pending", "Transaction has not reached supported reconciliation", "Chief Executive reconciliation"))
    return flags


def _event_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "event_key": row["event_key"],
        "sequence": row["sequence"],
        "event_type": row["event_type"],
        "actor_id": row["actor_id"],
        "actor_label": row["actor_label"],
        "council_role": row["council_role"],
        "action_summary": row["action_summary"],
        "occurred_at": row["occurred_at"],
        "recorded_at": row["recorded_at"],
        "evidence_ref": row["evidence_ref"],
        "attribution_status": row["attribution_status"],
        "payload": json.loads(row["payload_json"]),
        "prior_hash": row["prior_hash"],
        "event_hash": row["event_hash"],
    }


def _transaction(connection: sqlite3.Connection, transaction_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM council_transaction WHERE id = ?", (transaction_id,)
    ).fetchone()
    if not row:
        raise OpsError(f"Unknown Council transaction: {transaction_id}")
    return row


def _ensure_internal_council(
    connection: sqlite3.Connection, tenant: str
) -> dict[str, str]:
    try:
        tid = tenant_id(connection, tenant)
    except OpsError:
        if tenant != "anyang-internal":
            raise
        init_tenant(
            connection,
            slug=tenant,
            name="Anyang Intelligence Internal Council",
            policy_profile="executive-council-internal-pilot-v1",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
        )
        tid = tenant_id(connection, tenant)
    names = {
        "engineer": "System Engineer",
        "executive": "Chief Executive",
        "artistic": "Artistic Director",
        "interface": "Executive Assistant",
        "steward": "Council Steward",
    }
    actors: dict[str, str] = {}
    for role, name in names.items():
        row = connection.execute(
            "SELECT id, role FROM actor WHERE tenant_id = ? AND name = ?", (tid, name)
        ).fetchone()
        if row:
            if row["role"] != role:
                raise OpsError(f"Council actor role conflict for {name}")
            actors[role] = row["id"]
        else:
            actors[role] = add_actor(connection, tenant, name, role).id
    return actors


def _parse_friction_cases(text: str) -> list[dict[str, Any]]:
    matches = list(re.finditer(r"^## Case (\d+)\s+[—-]\s+(.+)$", text, re.M))
    cases: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## Cohort status", match.end())
        if end < 0:
            end = len(text)
        body = text[match.end() : end]
        transaction_match = re.search(r"\*\*Transaction ID:\*\*\s*`([^`]+)`", body)
        class_match = re.search(r"\*\*Decision class:\*\*\s*`([^`]+)`", body)
        state_match = re.search(r"\*\*State:\*\*\s*`([^`]+)`", body)
        if not transaction_match or not class_match or not state_match:
            raise OpsError(f"Friction case {number} lacks required metadata")
        sections: dict[str, str] = {}
        section_matches = list(re.finditer(r"^### ([A-D])\.\s+.+$", body, re.M))
        measures_start = body.find("\n### Measures")
        for section_index, section_match in enumerate(section_matches):
            section_end = (
                section_matches[section_index + 1].start()
                if section_index + 1 < len(section_matches)
                else measures_start if measures_start >= 0 else len(body)
            )
            sections[section_match.group(1)] = body[section_match.end() : section_end].strip()
        if set(sections) != {"A", "B", "C", "D"}:
            raise OpsError(f"Friction case {number} does not contain sections A-D")
        metrics = _parse_metrics(body[measures_start:] if measures_start >= 0 else "")
        cases.append(
            {
                "number": number,
                "title": match.group(2).strip(),
                "transaction_id": transaction_match.group(1).strip(),
                "decision_class": class_match.group(1).strip(),
                "source_state": state_match.group(1).strip(),
                "sections": sections,
                "metrics": metrics,
            }
        )
    return cases


def _parse_metrics(text: str) -> list[dict[str, str]]:
    metrics: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*(?:Measure|[-: ]+)\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        value = cells[1].strip("`")
        lowered = value.lower()
        status = "missing" if "missing" in lowered else "not_applicable" if "not applicable" in lowered else "observed"
        metrics.append({"name": cells[0], "value": value, "status": status, "row": line})
    return metrics


def _backfill_packet(
    event_key: str,
    actor_id: str | None,
    role: str,
    summary: str,
    evidence_ref: str,
    payload: dict[str, Any],
    *,
    missing: bool = False,
) -> dict[str, Any]:
    return {
        "event_key": event_key,
        "actor_id": actor_id,
        "actor_label": "Missing" if missing else "",
        "council_role": role,
        "action_summary": summary,
        "occurred_at": "Missing",
        "evidence_ref": evidence_ref,
        "attribution_status": "historical-missing" if missing else "attributed",
        "payload": payload,
    }


def _bullet(section: str, label: str) -> str:
    match = re.search(
        rf"^\s*-\s+\*\*{re.escape(label)}:\*\*\s*(.+?)(?=^\s*-\s+\*\*|\Z)",
        section,
        re.M | re.S | re.I,
    )
    if not match:
        return ""
    return " ".join(line.strip() for line in match.group(1).strip().splitlines())


def _decision_class_number(value: str) -> int:
    match = re.search(r"class\s*([0-3])", value, re.I)
    if not match:
        raise OpsError(f"Decision class must name Class 0-3: {value}")
    return int(match.group(1))


def _require_fields(
    values: dict[str, Any],
    names: tuple[str, ...],
    context: str,
    *,
    allow_false: bool = False,
) -> None:
    missing = []
    for name in names:
        if name not in values or values[name] is None:
            missing.append(name)
            continue
        value = values[name]
        if isinstance(value, str) and not value.strip():
            missing.append(name)
        elif value is False and not allow_false:
            missing.append(name)
    if missing:
        raise OpsError(f"{context} is missing required fields: {', '.join(missing)}")


def _flag(priority: str, code: str, message: str, needed: str) -> dict[str, str]:
    return {"priority": priority, "code": code, "message": message, "needed": needed}


def _hash(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _authority_is_current(
    payload: dict[str, Any], subject_hash: str, as_of: str
) -> bool:
    return (
        str(payload.get("decision", "")).lower()
        in {"approved", "approved_with_changes"}
        and payload.get("subject_hash") == subject_hash
        and not _is_expired(payload.get("expires_at"), as_of)
    )


def _is_expired(expires_at: Any, as_of: str) -> bool:
    if not _text(expires_at):
        return False
    try:
        expiry = datetime.fromisoformat(_text(expires_at).replace("Z", "+00:00"))
        reference = datetime.fromisoformat(_text(as_of).replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if reference.tzinfo is None:
            reference = reference.replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise OpsError(f"Invalid authority expiry timestamp: {expires_at}") from exc
    return expiry < reference


def _has_complete_receipt(projection: dict[str, Any]) -> bool:
    sections = projection["sections"]
    if not sections["A"] or not sections["B"] or not sections["C"]:
        return False
    authority = sections["B"][-1]["payload"]
    decision = _text(authority.get("decision")).lower()
    if decision in {"held", "rejected"}:
        return any(
            event["event_type"] == "execution_recorded"
            and event["payload"].get("no_action_taken") is True
            for event in sections["C"]
        )
    return any(
        event["event_type"] == "execution_recorded"
        for event in sections["C"]
    )


def _validate_privacy_boundary(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    payload: dict[str, Any],
) -> None:
    tenant = connection.execute(
        "SELECT slug FROM tenant WHERE id = ?", (transaction["tenant_id"],)
    ).fetchone()
    if not tenant or tenant["slug"] != "anyang-internal":
        return
    classification = _text(
        payload.get("privacy_classification") or payload.get("sensitivity")
    ).lower()
    if classification in {"private", "restricted", "customer-private", "client-private"}:
        raise OpsError("Customer-private or restricted evidence may not enter the internal Council ledger")
    forbidden = {
        "evidence_body",
        "raw_evidence",
        "raw_content",
        "customer_private_body",
        "client_private_body",
    }
    present = sorted(key for key in forbidden if _text(payload.get(key)))
    if present:
        raise OpsError(
            "Internal Council events may link evidence but may not store private evidence bodies: "
            + ", ".join(present)
        )


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _nullable_text(value: Any) -> str | None:
    text = _text(value)
    return text or None


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "metric"
