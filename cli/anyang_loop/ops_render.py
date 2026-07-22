from __future__ import annotations

import json
import hashlib
import sqlite3
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from typing import Any

from .epistemic_review import epistemic_review_data
from .ops_service import WORK_STATES, tenant_id


def weekly_review_data(
    connection: sqlite3.Connection, tenant: str, week_start: str, as_of: str | None = None
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    start = date.fromisoformat(week_start)
    end = start + timedelta(days=7)
    cutoff = as_of or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    tenant_row = connection.execute("SELECT * FROM tenant WHERE id = ?", (tid,)).fetchone()
    work = connection.execute(
        "SELECT * FROM work_item WHERE tenant_id = ? ORDER BY state, due_at, id", (tid,)
    ).fetchall()
    counts = Counter(row["state"] for row in work)
    events = connection.execute(
        """SELECT * FROM event WHERE tenant_id = ? AND created_at >= ? AND created_at < ?
        ORDER BY created_at, id""",
        (tid, f"{start.isoformat()}T00:00:00Z", f"{end.isoformat()}T00:00:00Z"),
    ).fetchall()
    approvals = connection.execute(
        """SELECT a.*, ac.name AS approver_name, w.title AS work_title
        FROM approval a JOIN actor ac ON ac.id = a.approver_actor_id
        JOIN work_item w ON w.id = a.work_id
        WHERE a.tenant_id = ? ORDER BY a.created_at, a.id""",
        (tid,),
    ).fetchall()
    claims = connection.execute(
        "SELECT * FROM claim WHERE tenant_id = ? ORDER BY status, expires_at, id", (tid,)
    ).fetchall()
    outcomes = connection.execute(
        """SELECT o.*, w.title AS work_title FROM outcome o JOIN work_item w ON w.id = o.work_id
        WHERE o.tenant_id = ? ORDER BY o.created_at, o.id""",
        (tid,),
    ).fetchall()
    evidence_counts = {
        row["work_id"]: row["count"]
        for row in connection.execute(
            "SELECT work_id, COUNT(*) AS count FROM evidence WHERE tenant_id = ? GROUP BY work_id", (tid,)
        )
    }
    overdue = [
        _work_row(row, evidence_counts)
        for row in work
        if row["due_at"] and row["due_at"] < cutoff and row["state"] not in {"reviewed", "closed"}
    ]
    blocked = [_work_row(row, evidence_counts) for row in work if row["state"] == "blocked"]
    delivered = [_work_row(row, evidence_counts) for row in work if row["state"] in {"delivered", "outcome_pending", "reviewed", "closed"}]
    approval_required = []
    for row in work:
        if row["state"] in {"ready_to_assign", "ready_for_owner_approval"}:
            approval_required.append(
                {
                    "work_id": row["id"],
                    "title": row["title"],
                    "required": "assign" if row["state"] == "ready_to_assign" else "claim_use and delivery",
                }
            )
    unsafe_claims = [
        _dict(row)
        for row in claims
        if row["classification"] == "unsupported-hold"
        or row["status"] in {"hold", "retired"}
        or (row["expires_at"] and row["expires_at"] < cutoff)
    ]
    planned_budget = sum(int(row["budget_cents"]) for row in work if row["state"] != "closed")
    owner_scores = [
        float(row["metric_value"])
        for row in outcomes
        if row["metric"] == "owner_usefulness" and row["metric_value"] is not None
    ]
    epistemic = epistemic_review_data(connection, tenant, cutoff)
    return {
        "tenant": {"slug": tenant_row["slug"], "name": tenant_row["name"], "policy_profile": tenant_row["policy_profile"]},
        "period": {"week_start": start.isoformat(), "week_end": (end - timedelta(days=1)).isoformat(), "as_of": cutoff},
        "changes": [_event_row(row) for row in events],
        "backlog": {state: counts.get(state, 0) for state in WORK_STATES if counts.get(state, 0)},
        "blocked": blocked,
        "overdue": overdue,
        "unsafe_or_stale_claims": unsafe_claims,
        "epistemic_review": {
            "counts": epistemic["counts"],
            "items": epistemic["items"][:5],
            "unsafe_claims": epistemic["unsafe_claims"],
            "independence_gaps": epistemic["independence_gaps"],
            "human_authority": epistemic["human_authority"],
        },
        "approvals_required": approval_required,
        "approvals_recorded": [
            {
                "work_id": row["work_id"],
                "work_title": row["work_title"],
                "scope": row["scope"],
                "decision": row["decision"],
                "approver": row["approver_name"],
                "subject_version": row["subject_version"],
                "revoked": bool(row["revoked_at"]),
            }
            for row in approvals
        ],
        "delivered": delivered,
        "outcomes": [
            {
                "work_id": row["work_id"],
                "work_title": row["work_title"],
                "metric": row["metric"],
                "metric_value": row["metric_value"],
                "observed_result": row["observed_result"],
                "confidence": row["confidence"],
            }
            for row in outcomes
        ],
        "economics": {
            "retainer_cents": tenant_row["retainer_cents"],
            "contractor_budget_cents": tenant_row["contractor_budget_cents"],
            "tool_budget_cents": tenant_row["tool_budget_cents"],
            "active_work_budget_cents": planned_budget,
            "budget_remaining_cents": tenant_row["retainer_cents"] - planned_budget,
        },
        "proof_metrics": {
            "planned_work": len(work),
            "delivered_or_later": len(delivered),
            "visible_blockers": len(blocked),
            "owner_usefulness_average": round(sum(owner_scores) / len(owner_scores), 2) if owner_scores else None,
        },
        "decisions_required": approval_required + [
            {"work_id": row["id"], "title": row["title"], "required": f"resolve blocker: {row['blocker']}"}
            for row in work
            if row["state"] == "blocked"
        ],
        "proposed_next_priorities": [
            {"work_id": row["id"], "title": row["title"], "state": row["state"], "due_at": row["due_at"]}
            for row in sorted(work, key=lambda item: (item["due_at"] or "9999", item["id"]))
            if row["state"] not in {"closed", "reviewed"}
        ][:5],
    }


def render_weekly_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['tenant']['name']} Weekly Operating Review",
        "",
        f"Week: {data['period']['week_start']} through {data['period']['week_end']}",
        f"As of: {data['period']['as_of']}",
        f"Policy: `{data['tenant']['policy_profile']}`",
        "",
        "## Changes",
        *_bullets(data["changes"], lambda row: f"{row['created_at']} - {row['event_type']} - {row['details'] or 'no detail'}"),
        "",
        "## Backlog By State",
        *_bullets([{"state": key, "count": value} for key, value in data["backlog"].items()], lambda row: f"{row['state']}: {row['count']}"),
        "",
        "## Blocked Or Overdue",
        *_bullets(data["blocked"] + data["overdue"], lambda row: f"{row['title']} (`{row['state']}`) - {row['blocker'] or 'overdue'} - owner: {row['responsible_human'] or row['owner']}"),
        "",
        "## Unsafe Or Stale Claims",
        *_bullets(data["unsafe_or_stale_claims"], lambda row: f"{row['text']} - {row['classification']} / {row['status']}"),
        "",
        "## Epistemic Review Required",
        (
            f"- Actionable: {data['epistemic_review']['counts']['actionable']} "
            f"(P0 {data['epistemic_review']['counts']['P0']}, "
            f"P1 {data['epistemic_review']['counts']['P1']}, "
            f"P2 {data['epistemic_review']['counts']['P2']})"
        ),
        *_bullets(
            data["epistemic_review"]["items"],
            lambda row: (
                f"{row['priority']} - {row['impact_type']} - "
                f"{row['downstream_type']}:{row['downstream_ref']} - claim {row['claim_id']}"
            ),
        ),
        "",
        "## Approvals Required",
        *_bullets(data["approvals_required"], lambda row: f"{row['title']} - {row['required']}"),
        "",
        "## Approvals Recorded",
        *_bullets(data["approvals_recorded"], lambda row: f"{row['work_title']} - {row['scope']} - {row['decision']} by {row['approver']} for v{row['subject_version']}"),
        "",
        "## Delivered Work And Evidence",
        *_bullets(data["delivered"], lambda row: f"{row['title']} - {row['state']} - evidence anchors: {row['evidence_count']}"),
        "",
        "## Outcomes",
        *_bullets(data["outcomes"], lambda row: f"{row['work_title']} - {row['metric']}: {row['observed_result']} ({row['confidence']})"),
        "",
        "## Capacity And Economics",
        f"- Retainer: ${data['economics']['retainer_cents'] / 100:,.2f}",
        f"- Contractor allocation: ${data['economics']['contractor_budget_cents'] / 100:,.2f}",
        f"- Tool allocation: ${data['economics']['tool_budget_cents'] / 100:,.2f}",
        f"- Active work budget: ${data['economics']['active_work_budget_cents'] / 100:,.2f}",
        f"- Remaining against retainer: ${data['economics']['budget_remaining_cents'] / 100:,.2f}",
        "",
        "## Decisions Required",
        *_bullets(data["decisions_required"], lambda row: f"{row['title']} - {row['required']}"),
        "",
        "## Proposed Next-Week Priorities",
        *_bullets(data["proposed_next_priorities"], lambda row: f"{row['title']} - {row['state']} - due {row['due_at'] or 'unscheduled'}"),
        "",
        "## Human Authority Boundary",
        "- This review prepares decisions. It does not authorize claims, assignment, spend, delivery, or publication.",
        "",
    ]
    return "\n".join(lines)


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def audit_data(connection: sqlite3.Connection, tenant: str, as_of: str | None = None) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    cutoff = as_of or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    work = connection.execute("SELECT * FROM work_item WHERE tenant_id = ? ORDER BY id", (tid,)).fetchall()
    issues: list[dict[str, str]] = []
    for row in work:
        if row["state"] == "blocked" and (not row["blocker"] or not row["responsible_human"]):
            issues.append({"code": "incomplete-blocker", "work_id": row["id"], "message": "Blocked work lacks reason or responsible human."})
        if row["state"] in {"delivered", "outcome_pending", "reviewed", "closed"}:
            count = connection.execute("SELECT COUNT(*) FROM evidence WHERE work_id = ? AND evidence_type = 'delivery_receipt'", (row["id"],)).fetchone()[0]
            if not count:
                issues.append({"code": "missing-delivery-receipt", "work_id": row["id"], "message": "Delivered work lacks a delivery receipt."})
    for claim in connection.execute("SELECT * FROM claim WHERE tenant_id = ? ORDER BY id", (tid,)):
        if claim["classification"] in {"source-backed", "customer-approved"}:
            count = connection.execute("SELECT COUNT(*) FROM claim_source WHERE claim_id = ?", (claim["id"],)).fetchone()[0]
            if not count:
                issues.append({"code": "missing-source-lineage", "claim_id": claim["id"], "message": "Supported claim lacks source lineage."})
        if claim["expires_at"] and claim["expires_at"] < cutoff and claim["status"] == "active":
            issues.append({"code": "expired-active-claim", "claim_id": claim["id"], "message": "Expired claim remains active."})
        if claim["epistemic_state"] in {"disconfirmed", "retired"} and claim["status"] == "active":
            issues.append({"code": "epistemically-unusable-active-claim", "claim_id": claim["id"], "message": "Disconfirmed or retired claim remains operationally active."})
        if not _valid_transition_chain(connection, claim["id"]):
            issues.append({"code": "invalid-claim-transition-chain", "claim_id": claim["id"], "message": "Claim transition history is missing or fails hash-chain verification."})
    if _table_exists(connection, "business_context_version"):
        issues.extend(_business_context_issues(connection, tid))
    epistemic = _epistemic_entropy(connection, tid)
    issues.extend(epistemic["critical_gaps"])
    return {"tenant": tenant, "as_of": cutoff, "ok": not issues, "issues": issues, "epistemic": epistemic}


def _business_context_issues(connection: sqlite3.Connection, tid: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    contexts = connection.execute(
        "SELECT * FROM business_context_version WHERE tenant_id = ? ORDER BY created_at, id", (tid,)
    ).fetchall()
    if sum(1 for row in contexts if row["state"] == "effective") > 1:
        issues.append(
            {"code": "multiple-effective-contexts", "message": "Tenant has more than one effective business context."}
        )
    for context in contexts:
        if context["base_context_id"]:
            base = connection.execute(
                "SELECT tenant_id FROM business_context_version WHERE id = ?", (context["base_context_id"],)
            ).fetchone()
            if not base or base["tenant_id"] != tid:
                issues.append(
                    {
                        "code": "cross-tenant-context-base",
                        "context_id": context["id"],
                        "message": "Business context has a missing or cross-tenant base version.",
                    }
                )
        evidence_mismatch = connection.execute(
            """SELECT COUNT(*) FROM business_context_evidence
            WHERE context_version_id = ? AND tenant_id != ?""",
            (context["id"], tid),
        ).fetchone()[0]
        if evidence_mismatch:
            issues.append(
                {
                    "code": "cross-tenant-context-evidence",
                    "context_id": context["id"],
                    "message": "Business-context evidence crosses the tenant boundary.",
                }
            )
        decisions = connection.execute(
            """SELECT * FROM business_context_decision
            WHERE context_version_id = ? AND revoked_at IS NULL ORDER BY created_at, id""",
            (context["id"],),
        ).fetchall()
        if any(row["tenant_id"] != tid or row["subject_hash"] != context["content_hash"] for row in decisions):
            issues.append(
                {
                    "code": "invalid-context-decision-binding",
                    "context_id": context["id"],
                    "message": "Business-context decision has a tenant or subject-hash mismatch.",
                }
            )
        approvals = [row for row in decisions if row["decision_type"] == "context_approval" and row["decision"] == "approved"]
        persistence = [
            row for row in decisions
            if row["decision_type"] == "persistence_confirmation" and row["decision"] == "confirmed"
        ]
        if context["state"] == "awaiting_persistence" and not approvals:
            issues.append(
                {
                    "code": "context-awaiting-without-approval",
                    "context_id": context["id"],
                    "message": "Context awaits persistence without exact owner approval.",
                }
            )
        if context["state"] in {"effective", "superseded"} and (not approvals or not persistence):
            issues.append(
                {
                    "code": "effective-context-receipt-gap",
                    "context_id": context["id"],
                    "message": "Effective context history lacks approval or persistence confirmation.",
                }
            )
    return issues


def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    return connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
    ).fetchone() is not None


def _epistemic_entropy(connection: sqlite3.Connection, tenant_id_value: str) -> dict[str, Any]:
    points = maximum = 0
    independence_gaps: list[str] = []
    independent_support_counts: dict[str, int] = {}
    claims = connection.execute("SELECT * FROM claim WHERE tenant_id = ? ORDER BY id", (tenant_id_value,)).fetchall()
    for claim in claims:
        maximum += 9
        points += 0 if claim["epistemic_state"] and claim["id"] else 2
        sources = connection.execute(
            """SELECT s.* FROM source s JOIN claim_source cs ON cs.source_id = s.id
            WHERE cs.claim_id = ? ORDER BY s.id""",
            (claim["id"],),
        ).fetchall()
        if claim["classification"] != "template-default" and not sources:
            points += 2
        if not str(claim["scope"]).strip():
            points += 1
        dependencies = connection.execute(
            "SELECT * FROM claim_dependency WHERE upstream_claim_id = ? AND active = 1",
            (claim["id"],),
        ).fetchall()
        if claim["status"] == "active" and not dependencies:
            points += 2
        if not _valid_transition_chain(connection, claim["id"]):
            points += 2
        if claim["evidence_strength"] == "strong" and len(sources) > 1:
            maximum += 4
            independent_origins = {
                str(source["origin_group"])
                for source in sources
                if source["independence_status"] == "independent" and source["origin_group"]
            }
            independent_support_counts[claim["id"]] = len(independent_origins)
            origin_groups = [str(source["origin_group"]) for source in sources if source["origin_group"]]
            independence_unproven = any(
                source["independence_status"] != "independent" or not source["origin_group"] for source in sources
            )
            derived_repetition = len(set(origin_groups)) < len(origin_groups)
            if independence_unproven:
                points += 1
                independence_gaps.append(claim["id"])
            if any(source["independence_status"] == "dependent" for source in sources) or derived_repetition:
                points += 3
        open_impacts = connection.execute(
            """SELECT * FROM epistemic_impact WHERE upstream_claim_id = ?
            AND status != 'resolved' AND impact_type != 'no-action'""",
            (claim["id"],),
        ).fetchall()
        if open_impacts:
            maximum += 3
            points += 3
    critical_gaps = [
        {
            "code": "open-critical-epistemic-impact",
            "claim_id": row["upstream_claim_id"],
            "message": f"Open {row['impact_type']} impact remains on {row['downstream_type']}:{row['downstream_ref']}.",
        }
        for row in connection.execute(
            """SELECT * FROM epistemic_impact WHERE tenant_id = ? AND status != 'resolved'
            AND impact_type IN ('review-required', 'unresolved', 'stale')
            AND downstream_type IN ('forecast', 'publication') ORDER BY id""",
            (tenant_id_value,),
        )
    ]
    rate = round((100.0 * points / maximum), 2) if maximum else 0.0
    return {
        "structural_points": points,
        "structural_maximum": maximum,
        "structural_entropy_rate": rate,
        "claim_count": len(claims),
        "transition_count": connection.execute(
            "SELECT COUNT(*) FROM claim_transition WHERE tenant_id = ?", (tenant_id_value,)
        ).fetchone()[0],
        "open_impact_count": connection.execute(
            "SELECT COUNT(*) FROM epistemic_impact WHERE tenant_id = ? AND status != 'resolved'", (tenant_id_value,)
        ).fetchone()[0],
        "independent_support_counts": independent_support_counts,
        "independence_gap_claim_ids": independence_gaps,
        "critical_gaps": critical_gaps,
    }


def _valid_transition_chain(connection: sqlite3.Connection, claim_id: str) -> bool:
    rows = connection.execute(
        "SELECT * FROM claim_transition WHERE claim_id = ? ORDER BY version", (claim_id,)
    ).fetchall()
    if not rows:
        return False
    prior = ""
    for expected_version, row in enumerate(rows, start=1):
        if row["version"] != expected_version or row["prior_transition_hash"] != prior:
            return False
        payload = {
            "id": row["id"],
            "claim_id": row["claim_id"],
            "version": row["version"],
            "from_state": row["from_state"],
            "to_state": row["to_state"],
            "cause_type": row["cause_type"],
            "cause_ref": row["cause_ref"],
            "actor": row["actor"],
            "rationale": row["rationale"],
            "prior_transition_hash": row["prior_transition_hash"],
            "created_at": row["created_at"],
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        if digest != row["transition_hash"]:
            return False
        prior = digest
    return True


def _dict(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def _work_row(row: sqlite3.Row, evidence_counts: dict[str, int]) -> dict[str, Any]:
    return {
        "id": row["id"], "title": row["title"], "state": row["state"], "version": row["version"],
        "owner": row["owner"], "reviewer": row["reviewer"], "due_at": row["due_at"],
        "blocker": row["blocker"], "responsible_human": row["responsible_human"],
        "capacity_hours": row["capacity_hours"], "budget_cents": row["budget_cents"],
        "evidence_count": evidence_counts.get(row["id"], 0),
    }


def _event_row(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in ("id", "work_id", "event_type", "actor", "from_state", "to_state", "details", "created_at")}


def _bullets(values: list[dict[str, Any]], formatter) -> list[str]:
    return [f"- {formatter(value)}" for value in values] or ["- None."]
