from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from .ops_service import OpsError, tenant_id


CRITICAL_IMPACT_TYPES = {"stale", "unresolved", "review-required"}
ACTIONABLE_IMPACT_TYPES = CRITICAL_IMPACT_TYPES | {"conditional"}


def epistemic_review_data(
    connection: sqlite3.Connection,
    tenant: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    cutoff = as_of or _now()
    impacts = connection.execute(
        """SELECT i.*, c.text AS claim_text, c.epistemic_state, c.status AS claim_status
        FROM epistemic_impact i JOIN claim c ON c.id = i.upstream_claim_id
        WHERE i.tenant_id = ? AND i.status != 'resolved' AND i.impact_type != 'no-action'
        ORDER BY i.created_at, i.id""",
        (tid,),
    ).fetchall()
    items = [_impact_review_item(row) for row in impacts]
    items.sort(key=lambda row: (_priority_rank(row["priority"]), row["created_at"], row["impact_id"]))
    claims = connection.execute("SELECT * FROM claim WHERE tenant_id = ? ORDER BY id", (tid,)).fetchall()
    unsafe_claims = []
    independence_gaps = []
    for claim in claims:
        reasons = _unsafe_reasons(claim, cutoff)
        if reasons:
            unsafe_claims.append(
                {
                    "claim_id": claim["id"],
                    "text": claim["text"],
                    "epistemic_state": claim["epistemic_state"],
                    "operational_status": claim["status"],
                    "reasons": reasons,
                }
            )
        gap = _independence_gap(connection, claim)
        if gap:
            independence_gaps.append(gap)
    counts = {priority: sum(item["priority"] == priority for item in items) for priority in ("P0", "P1", "P2")}
    return {
        "tenant": tenant,
        "as_of": cutoff,
        "counts": {**counts, "actionable": len(items)},
        "items": items,
        "unsafe_claims": unsafe_claims,
        "independence_gaps": independence_gaps,
        "human_authority": "This review creates no transition, resolution, approval, or downstream state change.",
    }


def claim_explanation_data(
    connection: sqlite3.Connection,
    tenant: str,
    claim_id: str,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    claim = connection.execute(
        "SELECT * FROM claim WHERE id = ? AND tenant_id = ?", (claim_id, tid)
    ).fetchone()
    if not claim:
        raise OpsError(f"Unknown claim for tenant: {claim_id}")
    sources = connection.execute(
        """SELECT s.* FROM source s JOIN claim_source cs ON cs.source_id = s.id
        WHERE cs.claim_id = ? ORDER BY s.id""",
        (claim_id,),
    ).fetchall()
    transitions = connection.execute(
        "SELECT * FROM claim_transition WHERE claim_id = ? ORDER BY version", (claim_id,)
    ).fetchall()
    dependencies = connection.execute(
        "SELECT * FROM claim_dependency WHERE upstream_claim_id = ? ORDER BY active DESC, created_at, id",
        (claim_id,),
    ).fetchall()
    impacts = connection.execute(
        """SELECT * FROM epistemic_impact WHERE upstream_claim_id = ?
        AND status != 'resolved' AND impact_type != 'no-action' ORDER BY created_at, id""",
        (claim_id,),
    ).fetchall()
    latest = transitions[-1] if transitions else None
    return {
        "tenant": tenant,
        "claim": {
            "id": claim["id"],
            "text": claim["text"],
            "classification": claim["classification"],
            "evidence_strength": claim["evidence_strength"],
            "scope": claim["scope"],
            "operational_status": claim["status"],
            "epistemic_state": claim["epistemic_state"],
            "epistemic_version": claim["epistemic_version"],
            "expires_at": claim["expires_at"],
        },
        "sources": [_source_row(row) for row in sources],
        "independent_support_count": len(
            {
                str(row["origin_group"])
                for row in sources
                if row["independence_status"] == "independent" and row["origin_group"]
            }
        ),
        "latest_transition": _transition_row(latest) if latest else None,
        "transition_history": [_transition_row(row) for row in transitions],
        "dependencies": [_dependency_row(row) for row in dependencies],
        "open_impacts": [_impact_row(row) for row in impacts],
        "reconsideration_evidence": _reconsideration_evidence(claim),
        "human_authority": "Only a named human may change this claim's semantic state or resolve its impacts.",
    }


def impact_packet_data(
    connection: sqlite3.Connection,
    tenant: str,
    impact_id: str,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    impact = connection.execute(
        "SELECT * FROM epistemic_impact WHERE id = ? AND tenant_id = ?", (impact_id, tid)
    ).fetchone()
    if not impact:
        raise OpsError(f"Unknown epistemic impact for tenant: {impact_id}")
    transition = connection.execute(
        "SELECT * FROM claim_transition WHERE id = ? AND tenant_id = ?", (impact["transition_id"], tid)
    ).fetchone()
    dependency = connection.execute(
        "SELECT * FROM claim_dependency WHERE id = ? AND tenant_id = ?", (impact["dependency_id"], tid)
    ).fetchone()
    related = connection.execute(
        """SELECT * FROM epistemic_impact WHERE tenant_id = ? AND upstream_claim_id = ?
        AND transition_id = ? AND status != 'resolved' AND impact_type != 'no-action'
        ORDER BY created_at, id""",
        (tid, impact["upstream_claim_id"], impact["transition_id"]),
    ).fetchall()
    return {
        "tenant": tenant,
        "impact": _impact_row(impact),
        "priority": _impact_review_item(impact)["priority"],
        "downstream_posture": _downstream_posture(impact["impact_type"]),
        "triggering_transition": _transition_row(transition),
        "dependency": _dependency_row(dependency),
        "controlling_claim": claim_explanation_data(connection, tenant, impact["upstream_claim_id"]),
        "related_open_impacts": [_impact_row(row) for row in related],
        "permitted_human_actions": [
            "Acknowledge the impact after a named reviewer accepts responsibility.",
            "Review the cited cause and upstream evidence without treating downstream repetition as support.",
            "Record a separate cause-bearing claim transition if human judgment changes.",
            "Resolve the impact with a named actor and rationale after the downstream review is complete.",
        ],
        "prohibited_automation": "This packet does not change claim warrant, downstream state, approval, or impact status.",
    }


def render_epistemic_review_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['tenant']} Epistemic Review",
        "",
        f"As of: {data['as_of']}",
        f"Actionable: {data['counts']['actionable']} (P0 {data['counts']['P0']}, P1 {data['counts']['P1']}, P2 {data['counts']['P2']})",
        "",
        "## Review Queue",
    ]
    lines.extend(
        [
            f"- **{item['priority']}** `{item['impact_type']}` on {item['downstream_type']}:`{item['downstream_ref']}` "
            f"from claim `{item['claim_id']}` ({item['status']})"
            for item in data["items"]
        ]
        or ["- None."]
    )
    lines.extend(["", "## Unsafe Claims"])
    lines.extend(
        [f"- `{item['claim_id']}`: {', '.join(item['reasons'])}" for item in data["unsafe_claims"]]
        or ["- None."]
    )
    lines.extend(["", "## Independence Gaps"])
    lines.extend(
        [
            f"- `{item['claim_id']}`: {item['independent_support_count']} independent origin group(s); {item['reason']}"
            for item in data["independence_gaps"]
        ]
        or ["- None."]
    )
    lines.extend(["", "## Human Authority", f"- {data['human_authority']}", ""])
    return "\n".join(lines)


def render_claim_explanation_markdown(data: dict[str, Any]) -> str:
    claim = data["claim"]
    latest = data["latest_transition"]
    lines = [
        f"# Claim {claim['id']}",
        "",
        claim["text"],
        "",
        "## Current Posture",
        f"- Epistemic: `{claim['epistemic_state']}` v{claim['epistemic_version']}",
        f"- Operational: `{claim['operational_status']}`",
        f"- Evidence: `{claim['classification']}` / `{claim['evidence_strength']}`",
        f"- Scope: {claim['scope']}",
        f"- Expires: {claim['expires_at'] or 'not declared'}",
        "",
        "## Upstream Support",
    ]
    lines.extend(
        [
            f"- `{source['id']}` {source['title']} — {source['independence_status']} / origin `{source['origin_group'] or 'unknown'}`"
            for source in data["sources"]
        ]
        or ["- None."]
    )
    lines.extend(
        [
            "",
            "## Latest Transition",
            (
                f"- {latest['from_state'] or 'created'} → {latest['to_state']} because `{latest['cause_type']}` "
                f"({latest['cause_ref']}) by {latest['actor']}: {latest['rationale']}"
                if latest
                else "- Missing transition history."
            ),
            "",
            "## Downstream Dependencies",
        ]
    )
    lines.extend(
        [
            f"- {row['downstream_type']}:`{row['downstream_ref']}` — {row['dependency_role']} ({'active' if row['active'] else 'retired'})"
            for row in data["dependencies"]
        ]
        or ["- None."]
    )
    lines.extend(["", "## Open Impacts"])
    lines.extend(
        [f"- `{row['impact_type']}` on {row['downstream_type']}:`{row['downstream_ref']}` ({row['status']})" for row in data["open_impacts"]]
        or ["- None."]
    )
    lines.extend(
        [
            "",
            "## Evidence That Could Change It",
            f"- {data['reconsideration_evidence']}",
            "",
            "## Human Authority",
            f"- {data['human_authority']}",
            "",
        ]
    )
    return "\n".join(lines)


def render_impact_packet_markdown(data: dict[str, Any]) -> str:
    impact = data["impact"]
    transition = data["triggering_transition"]
    dependency = data["dependency"]
    lines = [
        f"# Epistemic Impact Packet {impact['id']}",
        "",
        f"Priority: **{data['priority']}**",
        f"Posture: {data['downstream_posture']}",
        "",
        "## Trigger",
        f"- Claim `{impact['upstream_claim_id']}` moved {transition['from_state']} → {transition['to_state']}.",
        f"- Cause: `{transition['cause_type']}` / {transition['cause_ref']} by {transition['actor']}.",
        f"- Rationale: {transition['rationale']}",
        "",
        "## Affected Dependency",
        f"- {dependency['downstream_type']}:`{dependency['downstream_ref']}` as `{dependency['dependency_role']}`.",
        "",
        "## Related Open Impacts",
    ]
    lines.extend(
        [f"- `{row['id']}` {row['impact_type']} ({row['status']})" for row in data["related_open_impacts"]]
        or ["- None."]
    )
    lines.extend(["", "## Permitted Human Actions"])
    lines.extend([f"- {action}" for action in data["permitted_human_actions"]])
    lines.extend(["", "## Automation Boundary", f"- {data['prohibited_automation']}", ""])
    return "\n".join(lines)


def _impact_review_item(row: sqlite3.Row) -> dict[str, Any]:
    if row["status"] == "acknowledged" or row["impact_type"] == "conditional":
        priority = "P2"
    elif row["status"] == "open" and row["downstream_type"] in {"forecast", "publication"} and row["impact_type"] in CRITICAL_IMPACT_TYPES:
        priority = "P0"
    else:
        priority = "P1"
    return {
        "priority": priority,
        "impact_id": row["id"],
        "claim_id": row["upstream_claim_id"],
        "claim_text": row["claim_text"] if "claim_text" in row.keys() else None,
        "claim_state": row["epistemic_state"] if "epistemic_state" in row.keys() else None,
        "downstream_type": row["downstream_type"],
        "downstream_ref": row["downstream_ref"],
        "impact_type": row["impact_type"],
        "status": row["status"],
        "reason": row["reason"],
        "created_at": row["created_at"],
    }


def _unsafe_reasons(claim: sqlite3.Row, cutoff: str) -> list[str]:
    reasons = []
    if claim["classification"] == "unsupported-hold":
        reasons.append("unsupported hold")
    if claim["status"] in {"hold", "retired"}:
        reasons.append(f"operational status {claim['status']}")
    if claim["epistemic_state"] in {"disconfirmed", "retired"}:
        reasons.append(f"epistemic state {claim['epistemic_state']}")
    if claim["expires_at"] and claim["expires_at"] < cutoff:
        reasons.append("expired")
    return reasons


def _independence_gap(connection: sqlite3.Connection, claim: sqlite3.Row) -> dict[str, Any] | None:
    if claim["evidence_strength"] != "strong":
        return None
    sources = connection.execute(
        """SELECT s.* FROM source s JOIN claim_source cs ON cs.source_id = s.id
        WHERE cs.claim_id = ? ORDER BY s.id""",
        (claim["id"],),
    ).fetchall()
    if len(sources) < 2:
        return None
    origins = [str(row["origin_group"]) for row in sources if row["origin_group"]]
    independent = {
        str(row["origin_group"])
        for row in sources
        if row["independence_status"] == "independent" and row["origin_group"]
    }
    if all(row["independence_status"] == "independent" and row["origin_group"] for row in sources) and len(origins) == len(set(origins)):
        return None
    return {
        "claim_id": claim["id"],
        "independent_support_count": len(independent),
        "reason": "one or more sources have unknown/dependent independence or repeat an origin group",
    }


def _source_row(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in (
        "id", "title", "source_type", "provenance", "rights_status", "evidence_ref",
        "fresh_until", "origin_group", "independence_status", "redacted_summary",
    )}


def _transition_row(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in (
        "id", "version", "from_state", "to_state", "cause_type", "cause_ref", "actor",
        "rationale", "prior_transition_hash", "transition_hash", "created_at",
    )}


def _dependency_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "downstream_type": row["downstream_type"],
        "downstream_ref": row["downstream_ref"],
        "dependency_role": row["dependency_role"],
        "active": bool(row["active"]),
        "created_at": row["created_at"],
        "retired_at": row["retired_at"],
    }


def _impact_row(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in (
        "id", "transition_id", "upstream_claim_id", "dependency_id", "downstream_type",
        "downstream_ref", "impact_type", "status", "reason", "created_at", "acknowledged_at",
        "resolved_at", "resolved_by", "resolution",
    )}


def _reconsideration_evidence(claim: sqlite3.Row) -> str:
    if claim["expires_at"]:
        return "A refreshed, reviewed source that restores the claim's declared time boundary and scope."
    if claim["epistemic_state"] in {"contested", "disconfirmed", "unresolved"}:
        return "Reviewed independent evidence that directly addresses the latest transition cause within the declared scope."
    return "A reviewed upstream source, scope change, or authority change material enough to justify a new cause-bearing transition."


def _downstream_posture(impact_type: str) -> str:
    return {
        "review-required": "Review the downstream surface before further use.",
        "stale": "Treat the downstream surface as stale until explicitly reviewed.",
        "unresolved": "Keep the downstream surface unresolved and non-authorizing.",
        "conditional": "Use only inside an explicit human-approved conditional boundary.",
        "no-action": "No downstream action is required by this transition.",
    }[impact_type]


def _priority_rank(priority: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2}[priority]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
