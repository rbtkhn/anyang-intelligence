from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


EVIDENCE_CLASSIFICATIONS = (
    "source-backed",
    "customer-approved",
    "template-default",
    "provisional-assumption",
    "speculative-scenario",
    "unsupported-hold",
)
APPROVAL_SCOPES = ("assign", "claim_use", "spend", "delivery", "publication")
WORK_STATES = (
    "draft",
    "ready_to_assign",
    "assigned",
    "review_ready",
    "changes_requested",
    "blocked",
    "ready_for_owner_approval",
    "approved_for_delivery",
    "delivered",
    "outcome_pending",
    "reviewed",
    "closed",
)
TRANSITIONS = {
    "draft": {"ready_to_assign", "blocked"},
    "ready_to_assign": {"assigned", "blocked", "draft"},
    "assigned": {"review_ready", "blocked"},
    "review_ready": {"changes_requested", "blocked", "ready_for_owner_approval"},
    "changes_requested": {"ready_to_assign", "blocked"},
    "blocked": {"draft", "ready_to_assign", "assigned", "review_ready"},
    "ready_for_owner_approval": {"approved_for_delivery", "changes_requested", "blocked"},
    "approved_for_delivery": {"delivered", "changes_requested", "blocked"},
    "delivered": {"outcome_pending"},
    "outcome_pending": {"reviewed"},
    "reviewed": {"closed", "ready_to_assign"},
    "closed": set(),
}


class OpsError(ValueError):
    pass


@dataclass(frozen=True)
class MutationResult:
    action: str
    id: str
    details: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {"action": self.action, "id": self.id, **self.details}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id() -> str:
    return str(uuid.uuid4())


def tenant_id(connection: sqlite3.Connection, slug: str) -> str:
    row = connection.execute("SELECT id FROM tenant WHERE slug = ?", (slug,)).fetchone()
    if not row:
        raise OpsError(f"Unknown tenant: {slug}")
    return str(row["id"])


def init_tenant(
    connection: sqlite3.Connection,
    *,
    slug: str,
    name: str,
    policy_profile: str,
    retainer_cents: int,
    contractor_budget_cents: int,
    tool_budget_cents: int,
    timestamp: str | None = None,
) -> MutationResult:
    created = timestamp or now_utc()
    identifier = new_id()
    try:
        connection.execute(
            """INSERT INTO tenant(
                id, slug, name, policy_profile, retainer_cents,
                contractor_budget_cents, tool_budget_cents, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                identifier,
                slug,
                name,
                policy_profile,
                retainer_cents,
                contractor_budget_cents,
                tool_budget_cents,
                created,
            ),
        )
    except sqlite3.IntegrityError as exc:
        raise OpsError(f"Tenant already exists or configuration is invalid: {slug}") from exc
    _event(connection, identifier, None, "tenant_initialized", "operator", None, None, policy_profile, created)
    connection.commit()
    return MutationResult("tenant_initialized", identifier, {"slug": slug})


def add_actor(connection: sqlite3.Connection, tenant: str, name: str, role: str) -> MutationResult:
    tid = tenant_id(connection, tenant)
    identifier, created = new_id(), now_utc()
    try:
        connection.execute(
            "INSERT INTO actor(id, tenant_id, name, role, created_at) VALUES (?, ?, ?, ?, ?)",
            (identifier, tid, name, role, created),
        )
    except sqlite3.IntegrityError as exc:
        raise OpsError(f"Actor already exists or is invalid: {name}") from exc
    _event(connection, tid, None, "actor_added", name, None, None, role, created)
    connection.commit()
    return MutationResult("actor_added", identifier, {"name": name, "role": role})


def grant_authority(
    connection: sqlite3.Connection,
    tenant: str,
    actor_id: str,
    scope: str,
    effective_at: str | None,
    expires_at: str | None,
) -> MutationResult:
    if scope not in APPROVAL_SCOPES:
        raise OpsError(f"Invalid authority scope: {scope}")
    tid = tenant_id(connection, tenant)
    _require_actor(connection, tid, actor_id)
    identifier, created = new_id(), now_utc()
    connection.execute(
        """INSERT INTO authority_grant(
            id, tenant_id, actor_id, scope, effective_at, expires_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (identifier, tid, actor_id, scope, effective_at or created, expires_at, created),
    )
    _event(connection, tid, None, "authority_granted", actor_id, None, None, scope, created)
    connection.commit()
    return MutationResult("authority_granted", identifier, {"actor_id": actor_id, "scope": scope})


def revoke_authority(connection: sqlite3.Connection, grant_id: str, actor: str) -> MutationResult:
    row = connection.execute("SELECT * FROM authority_grant WHERE id = ?", (grant_id,)).fetchone()
    if not row:
        raise OpsError(f"Unknown authority grant: {grant_id}")
    revoked = now_utc()
    connection.execute("UPDATE authority_grant SET revoked_at = ? WHERE id = ?", (revoked, grant_id))
    _event(connection, row["tenant_id"], None, "authority_revoked", actor, None, None, row["scope"], revoked)
    connection.commit()
    return MutationResult("authority_revoked", grant_id, {"scope": row["scope"]})


def add_source(connection: sqlite3.Connection, tenant: str, **values: Any) -> MutationResult:
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    connection.execute(
        """INSERT INTO source(
            id, tenant_id, title, source_type, provenance, sensitivity,
            rights_status, evidence_ref, fresh_until, redacted_summary, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            identifier,
            tid,
            values["title"],
            values["source_type"],
            values["provenance"],
            values["sensitivity"],
            values["rights_status"],
            values["evidence_ref"],
            values.get("fresh_until"),
            values.get("redacted_summary", ""),
            created,
        ),
    )
    _event(connection, tid, None, "source_added", values.get("actor", "operator"), None, None, identifier, created)
    connection.commit()
    return MutationResult("source_added", identifier, {"title": values["title"]})


def add_claim(connection: sqlite3.Connection, tenant: str, source_ids: Iterable[str], **values: Any) -> MutationResult:
    if values["classification"] not in EVIDENCE_CLASSIFICATIONS:
        raise OpsError(f"Invalid evidence classification: {values['classification']}")
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    sources = list(source_ids)
    if values["classification"] in {"source-backed", "customer-approved"} and not sources:
        raise OpsError(f"{values['classification']} claims require at least one source")
    connection.execute(
        """INSERT INTO claim(
            id, tenant_id, text, classification, evidence_strength, scope,
            status, expires_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            identifier,
            tid,
            values["text"],
            values["classification"],
            values["evidence_strength"],
            values["scope"],
            values["status"],
            values.get("expires_at"),
            created,
        ),
    )
    for source_id in sources:
        _require_tenant_record(connection, "source", source_id, tid)
        connection.execute("INSERT INTO claim_source(claim_id, source_id) VALUES (?, ?)", (identifier, source_id))
    _event(connection, tid, None, "claim_added", values.get("actor", "operator"), None, None, identifier, created)
    connection.commit()
    return MutationResult("claim_added", identifier, {"classification": values["classification"]})


def create_work(
    connection: sqlite3.Connection,
    tenant: str,
    source_ids: Iterable[str],
    claim_ids: Iterable[str],
    **values: Any,
) -> MutationResult:
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    sources, claims = list(source_ids), list(claim_ids)
    for source_id in sources:
        _require_tenant_record(connection, "source", source_id, tid)
    for claim_id in claims:
        _require_tenant_record(connection, "claim", claim_id, tid)
    connection.execute(
        """INSERT INTO work_item(
            id, tenant_id, title, asset_job, owner, reviewer, deliverable,
            assignee, state, due_at, capacity_hours, budget_cents, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?, ?)""",
        (
            identifier,
            tid,
            values["title"],
            values["asset_job"],
            values["owner"],
            values["reviewer"],
            values["deliverable"],
            values.get("assignee", ""),
            values.get("due_at"),
            values["capacity_hours"],
            values.get("budget_cents", 0),
            created,
            created,
        ),
    )
    for source_id in sources:
        connection.execute("INSERT INTO work_source(work_id, source_id) VALUES (?, ?)", (identifier, source_id))
    for claim_id in claims:
        connection.execute("INSERT INTO work_claim(work_id, claim_id) VALUES (?, ?)", (identifier, claim_id))
    _event(connection, tid, identifier, "work_created", values.get("actor", "operator"), None, "draft", "", created)
    connection.commit()
    return MutationResult("work_created", identifier, {"state": "draft", "version": 1})


def add_evidence(connection: sqlite3.Connection, tenant: str, **values: Any) -> MutationResult:
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    work_id = values.get("work_id")
    if work_id:
        _require_tenant_record(connection, "work_item", work_id, tid)
    digest = values.get("integrity_hash") or hashlib.sha256(
        f"{values['evidence_type']}\0{values['reference']}".encode("utf-8")
    ).hexdigest()
    connection.execute(
        """INSERT INTO evidence(
            id, tenant_id, work_id, evidence_type, reference, creator, integrity_hash, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (identifier, tid, work_id, values["evidence_type"], values["reference"], values["creator"], digest, created),
    )
    _event(connection, tid, work_id, "evidence_added", values["creator"], None, None, values["evidence_type"], created)
    connection.commit()
    return MutationResult("evidence_added", identifier, {"integrity_hash": digest})


def record_approval(connection: sqlite3.Connection, tenant: str, **values: Any) -> MutationResult:
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    work = _require_tenant_record(connection, "work_item", values["work_id"], tid)
    actor = _require_actor(connection, tid, values["approver_actor_id"])
    _require_active_authority(connection, tid, actor["id"], values["scope"], created)
    subject_hash = work_subject_hash(connection, work["id"])
    connection.execute(
        """INSERT INTO approval(
            id, tenant_id, work_id, approver_actor_id, scope, subject_version,
            subject_hash, decision, conditions, expires_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            identifier,
            tid,
            work["id"],
            actor["id"],
            values["scope"],
            work["version"],
            subject_hash,
            values["decision"],
            values.get("conditions", ""),
            values.get("expires_at"),
            created,
        ),
    )
    _event(connection, tid, work["id"], "approval_recorded", actor["name"], None, None, values["scope"], created)
    connection.commit()
    return MutationResult(
        "approval_recorded",
        identifier,
        {"scope": values["scope"], "subject_version": work["version"], "subject_hash": subject_hash},
    )


def revoke_approval(connection: sqlite3.Connection, approval_id: str, actor: str) -> MutationResult:
    row = connection.execute("SELECT * FROM approval WHERE id = ?", (approval_id,)).fetchone()
    if not row:
        raise OpsError(f"Unknown approval: {approval_id}")
    revoked = now_utc()
    connection.execute("UPDATE approval SET revoked_at = ? WHERE id = ?", (revoked, approval_id))
    _event(connection, row["tenant_id"], row["work_id"], "approval_revoked", actor, None, None, row["scope"], revoked)
    connection.commit()
    return MutationResult("approval_revoked", approval_id, {"scope": row["scope"]})


def transition_work(
    connection: sqlite3.Connection,
    work_id: str,
    target: str,
    actor: str,
    reason: str,
    responsible_human: str,
) -> MutationResult:
    work = connection.execute("SELECT * FROM work_item WHERE id = ?", (work_id,)).fetchone()
    if not work:
        raise OpsError(f"Unknown work item: {work_id}")
    current = str(work["state"])
    if target not in TRANSITIONS.get(current, set()):
        raise OpsError(f"Invalid transition: {current} -> {target}")
    if target == "blocked" and (not reason.strip() or not responsible_human.strip()):
        raise OpsError("Blocked work requires a blocker reason and responsible human")
    _enforce_transition(connection, work, target)
    updated, version = now_utc(), int(work["version"])
    if target == "changes_requested":
        version += 1
    blocker = reason if target == "blocked" else ""
    responsible = responsible_human if target == "blocked" else ""
    connection.execute(
        """UPDATE work_item
        SET state = ?, version = ?, blocker = ?, responsible_human = ?, updated_at = ?
        WHERE id = ?""",
        (target, version, blocker, responsible, updated, work_id),
    )
    _event(connection, work["tenant_id"], work_id, "work_transitioned", actor, current, target, reason, updated)
    connection.commit()
    return MutationResult("work_transitioned", work_id, {"from": current, "to": target, "version": version})


def record_outcome(connection: sqlite3.Connection, tenant: str, **values: Any) -> MutationResult:
    tid, identifier, created = tenant_id(connection, tenant), new_id(), now_utc()
    _require_tenant_record(connection, "work_item", values["work_id"], tid)
    connection.execute(
        """INSERT INTO outcome(
            id, tenant_id, work_id, expected_result, observed_result, metric,
            metric_value, observation_window, confidence, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            identifier,
            tid,
            values["work_id"],
            values["expected_result"],
            values.get("observed_result", "pending"),
            values["metric"],
            values.get("metric_value"),
            values["observation_window"],
            values["confidence"],
            created,
        ),
    )
    _event(connection, tid, values["work_id"], "outcome_recorded", values.get("actor", "operator"), None, None, values["metric"], created)
    connection.commit()
    return MutationResult("outcome_recorded", identifier, {"confidence": values["confidence"]})


def work_subject_hash(connection: sqlite3.Connection, work_id: str) -> str:
    work = connection.execute("SELECT * FROM work_item WHERE id = ?", (work_id,)).fetchone()
    if not work:
        raise OpsError(f"Unknown work item: {work_id}")
    source_ids = [row[0] for row in connection.execute("SELECT source_id FROM work_source WHERE work_id = ? ORDER BY source_id", (work_id,))]
    claim_ids = [row[0] for row in connection.execute("SELECT claim_id FROM work_claim WHERE work_id = ? ORDER BY claim_id", (work_id,))]
    payload = {
        "id": work["id"],
        "title": work["title"],
        "asset_job": work["asset_job"],
        "owner": work["owner"],
        "reviewer": work["reviewer"],
        "deliverable": work["deliverable"],
        "assignee": work["assignee"],
        "version": work["version"],
        "capacity_hours": work["capacity_hours"],
        "budget_cents": work["budget_cents"],
        "sources": source_ids,
        "claims": claim_ids,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _enforce_transition(connection: sqlite3.Connection, work: sqlite3.Row, target: str) -> None:
    work_id, now = work["id"], now_utc()
    if target == "ready_to_assign":
        if not all(str(work[field]).strip() for field in ("asset_job", "owner", "reviewer", "deliverable")):
            raise OpsError("Assignment readiness requires asset job, owner, reviewer, and bounded deliverable")
        if connection.execute("SELECT COUNT(*) FROM work_source WHERE work_id = ?", (work_id,)).fetchone()[0] == 0:
            raise OpsError("Assignment readiness requires at least one source")
    if target == "assigned":
        _require_current_approval(connection, work, "assign", now)
        if int(work["budget_cents"]) > 0:
            _require_current_approval(connection, work, "spend", now)
    if target == "ready_for_owner_approval":
        claims = connection.execute(
            """SELECT c.* FROM claim c JOIN work_claim wc ON wc.claim_id = c.id
            WHERE wc.work_id = ? ORDER BY c.id""",
            (work_id,),
        ).fetchall()
        if claims:
            if connection.execute("SELECT COUNT(*) FROM evidence WHERE work_id = ?", (work_id,)).fetchone()[0] == 0:
                raise OpsError("Claim-bearing work requires evidence before owner approval")
            for claim in claims:
                if claim["status"] in {"hold", "retired"} or claim["classification"] == "unsupported-hold":
                    raise OpsError(f"Claim is not operationally usable: {claim['id']}")
                if claim["expires_at"] and claim["expires_at"] < now:
                    raise OpsError(f"Claim is expired: {claim['id']}")
                sources = connection.execute(
                    """SELECT s.* FROM source s JOIN claim_source cs ON cs.source_id = s.id
                    WHERE cs.claim_id = ?""",
                    (claim["id"],),
                ).fetchall()
                if not sources and claim["classification"] != "template-default":
                    raise OpsError(f"Claim lacks source lineage: {claim['id']}")
                if any(source["fresh_until"] and source["fresh_until"] < now for source in sources):
                    raise OpsError(f"Claim depends on a stale source: {claim['id']}")
    if target == "approved_for_delivery":
        if connection.execute("SELECT COUNT(*) FROM work_claim WHERE work_id = ?", (work_id,)).fetchone()[0]:
            _require_current_approval(connection, work, "claim_use", now)
        _require_current_approval(connection, work, "delivery", now)
    if target == "delivered":
        receipt = connection.execute(
            "SELECT id FROM evidence WHERE work_id = ? AND evidence_type = 'delivery_receipt' LIMIT 1",
            (work_id,),
        ).fetchone()
        if not receipt:
            raise OpsError("Delivered work requires a delivery_receipt evidence anchor")
        _require_current_approval(connection, work, "delivery", now)
    if target == "reviewed":
        if connection.execute("SELECT COUNT(*) FROM outcome WHERE work_id = ?", (work_id,)).fetchone()[0] == 0:
            raise OpsError("Reviewed work requires an outcome record; pending is allowed")


def _require_current_approval(connection: sqlite3.Connection, work: sqlite3.Row, scope: str, now: str) -> sqlite3.Row:
    expected_hash = work_subject_hash(connection, work["id"])
    rows = connection.execute(
        """SELECT * FROM approval
        WHERE work_id = ? AND scope = ? AND decision IN ('approved', 'approved_with_changes')
          AND revoked_at IS NULL AND subject_version = ? AND subject_hash = ?
        ORDER BY created_at DESC""",
        (work["id"], scope, work["version"], expected_hash),
    ).fetchall()
    for row in rows:
        if not row["expires_at"] or row["expires_at"] >= now:
            return row
    raise OpsError(f"Current {scope} approval is required for work version {work['version']}")


def _require_active_authority(
    connection: sqlite3.Connection, tenant: str, actor_id: str, scope: str, now: str
) -> sqlite3.Row:
    rows = connection.execute(
        """SELECT * FROM authority_grant
        WHERE tenant_id = ? AND actor_id = ? AND scope = ? AND revoked_at IS NULL
          AND effective_at <= ? ORDER BY effective_at DESC""",
        (tenant, actor_id, scope, now),
    ).fetchall()
    for row in rows:
        if not row["expires_at"] or row["expires_at"] >= now:
            return row
    raise OpsError(f"Actor lacks active authority for scope: {scope}")


def _require_actor(connection: sqlite3.Connection, tenant: str, actor_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM actor WHERE id = ? AND tenant_id = ? AND active = 1", (actor_id, tenant)
    ).fetchone()
    if not row:
        raise OpsError(f"Unknown or inactive actor: {actor_id}")
    return row


def _require_tenant_record(connection: sqlite3.Connection, table: str, identifier: str, tenant: str) -> sqlite3.Row:
    if table not in {"source", "claim", "work_item"}:
        raise OpsError(f"Unsafe table lookup: {table}")
    row = connection.execute(f"SELECT * FROM {table} WHERE id = ? AND tenant_id = ?", (identifier, tenant)).fetchone()
    if not row:
        raise OpsError(f"Unknown {table} record for tenant: {identifier}")
    return row


def _event(
    connection: sqlite3.Connection,
    tenant: str,
    work: str | None,
    event_type: str,
    actor: str,
    from_state: str | None,
    to_state: str | None,
    details: str,
    created_at: str,
) -> None:
    connection.execute(
        """INSERT INTO event(
            id, tenant_id, work_id, event_type, actor, from_state, to_state, details, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (new_id(), tenant, work, event_type, actor, from_state, to_state, details, created_at),
    )
