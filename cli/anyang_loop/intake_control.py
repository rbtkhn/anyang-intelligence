from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import yaml

from .ops_service import MutationResult, OpsError, _event, new_id, now_utc, tenant_id


CONTEXT_AUTHORITY_SCOPE = "business_context"
READINESS_STATES = ("ready", "provisional", "hold")
EVIDENCE_CLASSES = ("confirmed", "estimate", "hypothesis", "missing")
CONFIDENCE_STATES = ("high", "medium", "low", "unknown")
SENSITIVITY_STATES = ("public", "internal", "private", "restricted")
MISSING_MARKERS = {"", "missing", "unknown", "not confirmed", "pending confirmation"}

_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE = re.compile(r"(?<!\w)(?:\+?\d[\s().-]*){7,}\d(?!\w)")
_CURRENCY = re.compile(r"(?:[$€£]\s*\d|\b\d+(?:\.\d+)?\s*(?:USD|EUR|GBP)\b)", re.IGNORECASE)
_PRIVATE_FILE = re.compile(r"\.(?:docx|xlsx|csv|db|sqlite|sqlite3|wal|shm)(?:$|[?#])", re.IGNORECASE)


def load_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise OpsError(f"Intake manifest does not exist: {manifest_path}")
    try:
        value = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise OpsError(f"Cannot read intake manifest: {manifest_path}") from exc
    if not isinstance(value, dict):
        raise OpsError("Intake manifest must be a mapping")
    validate_manifest(value)
    return value


def validate_manifest(manifest: dict[str, Any]) -> None:
    allowed = {
        "business_reference",
        "version",
        "base_version",
        "external_content_ref",
        "authority_receipt_ref",
        "readiness",
        "created_by",
        "evidence",
        "unresolved_gates",
    }
    unknown = sorted(set(manifest) - allowed)
    if unknown:
        raise OpsError(f"Unsupported intake manifest fields: {', '.join(unknown)}")
    for field in (
        "business_reference",
        "version",
        "external_content_ref",
        "authority_receipt_ref",
        "readiness",
        "created_by",
    ):
        _required_text(manifest, field)
    if manifest["readiness"] not in READINESS_STATES:
        raise OpsError(f"Invalid readiness: {manifest['readiness']}")
    base = manifest.get("base_version")
    if base is not None and not isinstance(base, str):
        raise OpsError("base_version must be a string or null")
    _safe_reference(str(manifest["external_content_ref"]), "external_content_ref", allow_repo=False)
    _safe_reference(str(manifest["authority_receipt_ref"]), "authority_receipt_ref", allow_repo=False)

    evidence = manifest.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise OpsError("Intake manifest requires at least one evidence binding")
    for index, item in enumerate(evidence, start=1):
        if not isinstance(item, dict):
            raise OpsError(f"Evidence binding {index} must be a mapping")
        _validate_evidence(item, index)

    gates = manifest.get("unresolved_gates", [])
    if not isinstance(gates, list) or any(not isinstance(gate, str) or not gate.strip() for gate in gates):
        raise OpsError("unresolved_gates must be a list of non-empty strings")
    for gate in gates:
        _safe_summary(gate, "unresolved gate")
    if manifest["readiness"] == "hold" and not gates:
        raise OpsError("Hold readiness requires at least one unresolved gate")


def manifest_hash(manifest: dict[str, Any]) -> str:
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def propose_context(connection: sqlite3.Connection, tenant: str, manifest: dict[str, Any]) -> MutationResult:
    validate_manifest(manifest)
    tid = tenant_id(connection, tenant)
    current = _effective_context(connection, tid)
    base_version = _normalized_optional(manifest.get("base_version"))
    if current:
        if not base_version or base_version != current["version_label"]:
            raise OpsError(
                f"Stale or missing base version: current effective version is {current['version_label']}"
            )
        base_id = current["id"]
    else:
        if base_version:
            raise OpsError("A base version was supplied but the tenant has no effective context")
        base_id = None
    if str(manifest["version"]).strip().lower() in MISSING_MARKERS:
        raise OpsError("Proposal version requires an exact non-placeholder value")
    if str(manifest["external_content_ref"]).strip().lower() in MISSING_MARKERS:
        raise OpsError("Proposal requires an exact external content reference")

    identifier, created = new_id(), now_utc()
    digest = manifest_hash(manifest)
    state = "hold" if manifest["readiness"] == "hold" else "proposed"
    try:
        connection.execute(
            """INSERT INTO business_context_version(
                id, tenant_id, business_reference, version_label, base_context_id,
                external_content_ref, content_hash, authority_receipt_ref,
                readiness, state, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                identifier,
                tid,
                manifest["business_reference"],
                manifest["version"],
                base_id,
                manifest["external_content_ref"],
                digest,
                manifest["authority_receipt_ref"],
                manifest["readiness"],
                state,
                manifest["created_by"],
                created,
            ),
        )
        _insert_manifest_evidence(connection, tid, identifier, manifest, created)
    except sqlite3.IntegrityError as exc:
        raise OpsError(f"Business-context proposal is invalid or already exists: {manifest['version']}") from exc
    _event(connection, tid, None, "business_context_proposed", manifest["created_by"], None, state, manifest["version"], created)
    connection.commit()
    return MutationResult(
        "business_context_proposed",
        identifier,
        {"version": manifest["version"], "content_hash": digest, "state": state},
    )


def bootstrap_context(
    connection: sqlite3.Connection,
    tenant: str,
    manifest: dict[str, Any],
    actor_id: str,
    subject_hash: str,
    approval_receipt_ref: str,
    persistence_ref: str,
) -> MutationResult:
    validate_manifest(manifest)
    _safe_reference(approval_receipt_ref, "approval_receipt_ref", allow_repo=False)
    _safe_reference(persistence_ref, "persistence_ref", allow_repo=False)
    if manifest["readiness"] == "hold" or manifest.get("unresolved_gates"):
        raise OpsError("Legacy bootstrap requires a non-Hold context with no unresolved gates")
    if _normalized_optional(manifest.get("base_version")):
        raise OpsError("Legacy bootstrap is only valid for the first recorded effective context")
    digest = manifest_hash(manifest)
    if subject_hash != digest:
        raise OpsError("Legacy bootstrap hash does not match the exact supplied context")
    tid = tenant_id(connection, tenant)
    _require_context_authority(connection, tid, actor_id)
    if connection.execute(
        "SELECT COUNT(*) FROM business_context_version WHERE tenant_id = ?", (tid,)
    ).fetchone()[0]:
        raise OpsError("Legacy bootstrap requires an empty business-context ledger")

    identifier, created = new_id(), now_utc()
    try:
        connection.execute(
            """INSERT INTO business_context_version(
                id, tenant_id, business_reference, version_label, base_context_id,
                external_content_ref, content_hash, authority_receipt_ref,
                readiness, state, created_by, created_at, effective_at
            ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?, 'effective', ?, ?, ?)""",
            (
                identifier,
                tid,
                manifest["business_reference"],
                manifest["version"],
                manifest["external_content_ref"],
                digest,
                manifest["authority_receipt_ref"],
                manifest["readiness"],
                manifest["created_by"],
                created,
                created,
            ),
        )
        context = connection.execute(
            "SELECT * FROM business_context_version WHERE id = ?", (identifier,)
        ).fetchone()
        _insert_manifest_evidence(connection, tid, identifier, manifest, created)
        _insert_decision(
            connection,
            tid,
            context,
            "context_approval",
            "approved",
            actor_id,
            digest,
            "Imported from an operator-confirmed legacy approval receipt.",
            approval_receipt_ref,
            created,
        )
        _insert_decision(
            connection,
            tid,
            context,
            "persistence_confirmation",
            "confirmed",
            actor_id,
            digest,
            "Imported from an operator-confirmed legacy persistence receipt.",
            persistence_ref,
            created,
        )
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError("Legacy business-context bootstrap failed validation") from exc
    _event(connection, tid, None, "business_context_bootstrapped", actor_id, None, "effective", manifest["version"], created)
    connection.commit()
    return MutationResult(
        "business_context_bootstrapped",
        identifier,
        {"version": manifest["version"], "content_hash": digest, "state": "effective"},
    )


def decide_context(
    connection: sqlite3.Connection,
    tenant: str,
    version: str,
    actor_id: str,
    decision: str,
    subject_hash: str,
    conditions: str = "",
) -> MutationResult:
    if decision not in {"approved", "rejected", "changes_requested"}:
        raise OpsError(f"Invalid context decision: {decision}")
    if conditions:
        _safe_summary(conditions, "decision conditions")
    tid = tenant_id(connection, tenant)
    context = _context_by_version(connection, tid, version)
    if context["state"] not in {"proposed", "hold"}:
        raise OpsError(f"Context decision is invalid from state: {context['state']}")
    if decision == "approved" and context["readiness"] == "hold":
        raise OpsError("A Hold context cannot be approved; resolve its gates and submit a new proposal")
    _require_context_authority(connection, tid, actor_id)
    if subject_hash != context["content_hash"]:
        raise OpsError("Context decision hash does not match the exact proposal")
    target = {
        "approved": "awaiting_persistence",
        "rejected": "rejected",
        "changes_requested": "changes_requested",
    }[decision]
    created = now_utc()
    _insert_decision(connection, tid, context, "context_approval", decision, actor_id, subject_hash, conditions, "", created)
    connection.execute("UPDATE business_context_version SET state = ? WHERE id = ?", (target, context["id"]))
    _event(connection, tid, None, "business_context_decided", actor_id, context["state"], target, version, created)
    connection.commit()
    return MutationResult("business_context_decided", context["id"], {"version": version, "decision": decision, "state": target})


def persist_context(
    connection: sqlite3.Connection,
    tenant: str,
    version: str,
    actor_id: str,
    subject_hash: str,
    external_ref: str,
) -> MutationResult:
    _safe_reference(external_ref, "external_ref", allow_repo=False)
    tid = tenant_id(connection, tenant)
    context = _context_by_version(connection, tid, version)
    if context["state"] != "awaiting_persistence":
        raise OpsError(f"Persistence confirmation is invalid from state: {context['state']}")
    _require_context_authority(connection, tid, actor_id)
    if subject_hash != context["content_hash"]:
        raise OpsError("Persistence hash does not match the approved proposal")
    approval = _latest_decision(connection, context["id"], "context_approval")
    if not approval or approval["decision"] != "approved" or approval["subject_hash"] != subject_hash:
        raise OpsError("Current exact context approval is required before persistence")
    current = _effective_context(connection, tid)
    expected_base = context["base_context_id"]
    if (current and current["id"] != expected_base) or (not current and expected_base is not None):
        raise OpsError("Effective context changed after proposal; persistence requires a new proposal")
    created = now_utc()
    try:
        if current:
            connection.execute(
                "UPDATE business_context_version SET state = 'superseded', superseded_at = ? WHERE id = ?",
                (created, current["id"]),
            )
        connection.execute(
            "UPDATE business_context_version SET state = 'effective', effective_at = ? WHERE id = ?",
            (created, context["id"]),
        )
        _insert_decision(
            connection, tid, context, "persistence_confirmation", "confirmed",
            actor_id, subject_hash, "", external_ref, created,
        )
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError("Could not establish exactly one effective business context") from exc
    _event(connection, tid, None, "business_context_effective", actor_id, "awaiting_persistence", "effective", version, created)
    connection.commit()
    return MutationResult("business_context_effective", context["id"], {"version": version, "state": "effective", "external_ref": external_ref})


def authorize_review(
    connection: sqlite3.Connection,
    tenant: str,
    version: str,
    actor_id: str,
    decision: str,
    subject_hash: str,
    conditions: str = "",
) -> MutationResult:
    if decision not in {"approved", "declined"}:
        raise OpsError(f"Invalid operating-review decision: {decision}")
    if conditions:
        _safe_summary(conditions, "operating-review conditions")
    tid = tenant_id(connection, tenant)
    context = _context_by_version(connection, tid, version)
    if context["state"] != "effective":
        raise OpsError("Operating-review authorization requires the effective context")
    _require_context_authority(connection, tid, actor_id)
    if subject_hash != context["content_hash"]:
        raise OpsError("Operating-review authorization hash does not match the effective context")
    created = now_utc()
    _insert_decision(
        connection, tid, context, "operating_review_authorization", decision,
        actor_id, subject_hash, conditions, "", created,
    )
    _event(connection, tid, None, "operating_review_authorized" if decision == "approved" else "operating_review_declined", actor_id, None, decision, version, created)
    connection.commit()
    return MutationResult("operating_review_authorization_recorded", context["id"], {"version": version, "decision": decision})


def intake_status(connection: sqlite3.Connection, tenant: str) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    effective = _effective_context(connection, tid)
    active = connection.execute(
        """SELECT * FROM business_context_version
        WHERE tenant_id = ? AND state IN ('proposed', 'hold', 'awaiting_persistence', 'changes_requested')
        ORDER BY created_at DESC, id DESC LIMIT 1""",
        (tid,),
    ).fetchone()
    focus = active or effective
    evidence: dict[str, list[dict[str, str]]] = {name: [] for name in EVIDENCE_CLASSES}
    if focus:
        rows = connection.execute(
            """SELECT evidence_class, evidence_kind, redacted_summary, source_ref, confidence, sensitivity
            FROM business_context_evidence WHERE context_version_id = ?
            ORDER BY evidence_class, evidence_kind, id""",
            (focus["id"],),
        ).fetchall()
        for row in rows:
            evidence[row["evidence_class"]].append(
                {
                    "kind": row["evidence_kind"],
                    "summary": row["redacted_summary"],
                    "source_ref": row["source_ref"],
                    "confidence": row["confidence"],
                    "sensitivity": row["sensitivity"],
                }
            )
    owner_decision = _decision_summary(connection, focus, "context_approval")
    persistence = _decision_summary(connection, focus, "persistence_confirmation")
    review = _decision_summary(connection, effective, "operating_review_authorization")
    return {
        "tenant": tenant,
        "business_reference": focus["business_reference"] if focus else tenant,
        "effective_context": _context_summary(effective),
        "active_proposal": _context_summary(active),
        "authority_receipt_ref": focus["authority_receipt_ref"] if focus else None,
        "storefronts": [item for item in evidence["confirmed"] if item["kind"] == "storefront"],
        "evidence": evidence,
        "readiness": focus["readiness"] if focus else "hold",
        "owner_decision": owner_decision,
        "persistence": persistence,
        "operating_review_authorization": review,
        "next_action": _next_action(effective, active, owner_decision, persistence, review),
    }


def render_intake_status(data: dict[str, Any]) -> str:
    effective = data["effective_context"]
    proposal = data["active_proposal"]
    lines = [
        "# Business Intake Status Receipt",
        "",
        f"- Tenant: {data['tenant']}",
        f"- Business reference: {data['business_reference']}",
        f"- Effective context: {_display_context(effective)}",
        f"- Active proposal: {_display_context(proposal)}",
        f"- Authority receipt: {data['authority_receipt_ref'] or 'Missing'}",
        f"- Readiness: {data['readiness']}",
        f"- Owner decision: {_display_decision(data['owner_decision'])}",
        f"- Persistence: {_display_decision(data['persistence'])}",
        f"- Operating-review authorization: {_display_decision(data['operating_review_authorization'])}",
        f"- Next action: {data['next_action']}",
        "",
        "## Evidence",
        "",
    ]
    for classification in EVIDENCE_CLASSES:
        lines.append(f"### {classification.title()}")
        lines.append("")
        items = data["evidence"][classification]
        if not items:
            lines.append("- None recorded.")
        else:
            for item in items:
                lines.append(
                    f"- [{item['kind']}; {item['confidence']}; {item['sensitivity']}] "
                    f"{item['summary']} (source: {item['source_ref']})"
                )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _validate_evidence(item: dict[str, Any], index: int) -> None:
    allowed = {"class", "kind", "summary", "source_ref", "confidence", "sensitivity"}
    unknown = sorted(set(item) - allowed)
    if unknown:
        raise OpsError(f"Unsupported fields in evidence binding {index}: {', '.join(unknown)}")
    for field in allowed:
        _required_text(item, field, label=f"evidence binding {index}")
    if item["class"] not in EVIDENCE_CLASSES:
        raise OpsError(f"Invalid evidence class in binding {index}: {item['class']}")
    if item["confidence"] not in CONFIDENCE_STATES:
        raise OpsError(f"Invalid confidence in binding {index}: {item['confidence']}")
    if item["sensitivity"] not in SENSITIVITY_STATES:
        raise OpsError(f"Invalid sensitivity in binding {index}: {item['sensitivity']}")
    _safe_summary(item["summary"], f"evidence binding {index}")
    _safe_reference(item["source_ref"], f"evidence binding {index} source_ref", allow_repo=True)


def _insert_manifest_evidence(
    connection: sqlite3.Connection,
    tid: str,
    context_id: str,
    manifest: dict[str, Any],
    created: str,
) -> None:
    for item in manifest["evidence"]:
        connection.execute(
            """INSERT INTO business_context_evidence(
                id, tenant_id, context_version_id, evidence_class, evidence_kind,
                redacted_summary, source_ref, confidence, sensitivity, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                new_id(),
                tid,
                context_id,
                item["class"],
                item["kind"],
                item["summary"],
                item["source_ref"],
                item["confidence"],
                item["sensitivity"],
                created,
            ),
        )
    for gate in manifest.get("unresolved_gates", []):
        connection.execute(
            """INSERT INTO business_context_evidence(
                id, tenant_id, context_version_id, evidence_class, evidence_kind,
                redacted_summary, source_ref, confidence, sensitivity, created_at
            ) VALUES (?, ?, ?, 'missing', 'unresolved_gate', ?, 'operator-intake', 'unknown', 'internal', ?)""",
            (new_id(), tid, context_id, gate, created),
        )


def _safe_summary(value: str, label: str) -> None:
    if len(value) > 500 or "\n" in value or "\r" in value:
        raise OpsError(f"{label} must be a single redacted summary of at most 500 characters")
    if _EMAIL.search(value) or _PHONE.search(value):
        raise OpsError(f"{label} appears to contain a customer identifier")
    if _CURRENCY.search(value):
        raise OpsError(f"{label} appears to contain exact private economics")
    if re.search(r"(?:buyer|customer)\s+(?:name|email|phone|address)\s*:", value, re.IGNORECASE):
        raise OpsError(f"{label} appears to contain raw customer-message fields")


def _safe_reference(value: str, label: str, *, allow_repo: bool) -> None:
    if not value.strip() or _EMAIL.search(value) or _PRIVATE_FILE.search(value):
        raise OpsError(f"{label} must be an opaque, public, or sanitized reference")
    candidate = Path(value)
    if candidate.is_absolute() or value.lower().startswith("file:"):
        raise OpsError(f"{label} must not contain a local absolute path")
    if not allow_repo and (value.startswith("projects/") or value.startswith("repo:")):
        raise OpsError(f"{label} must point to the external tenant-private control plane")


def _required_text(mapping: dict[str, Any], field: str, *, label: str = "manifest") -> None:
    value = mapping.get(field)
    if not isinstance(value, str) or not value.strip():
        raise OpsError(f"{label} requires non-empty text for {field}")


def _normalized_optional(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return None if text.lower() in MISSING_MARKERS else text


def _context_by_version(connection: sqlite3.Connection, tid: str, version: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM business_context_version WHERE tenant_id = ? AND version_label = ?",
        (tid, version),
    ).fetchone()
    if not row:
        raise OpsError(f"Unknown business-context version for tenant: {version}")
    return row


def _effective_context(connection: sqlite3.Connection, tid: str) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM business_context_version WHERE tenant_id = ? AND state = 'effective'",
        (tid,),
    ).fetchone()


def _require_context_authority(connection: sqlite3.Connection, tid: str, actor_id: str) -> sqlite3.Row:
    actor = connection.execute(
        "SELECT * FROM actor WHERE id = ? AND tenant_id = ? AND active = 1", (actor_id, tid)
    ).fetchone()
    if not actor:
        raise OpsError(f"Unknown active actor for tenant: {actor_id}")
    now = now_utc()
    grant = connection.execute(
        """SELECT * FROM authority_grant
        WHERE tenant_id = ? AND actor_id = ? AND scope = ? AND revoked_at IS NULL
          AND effective_at <= ? AND (expires_at IS NULL OR expires_at >= ?)
        ORDER BY effective_at DESC LIMIT 1""",
        (tid, actor_id, CONTEXT_AUTHORITY_SCOPE, now, now),
    ).fetchone()
    if not grant:
        raise OpsError(f"Actor lacks current {CONTEXT_AUTHORITY_SCOPE} authority")
    return actor


def _insert_decision(
    connection: sqlite3.Connection,
    tid: str,
    context: sqlite3.Row,
    decision_type: str,
    decision: str,
    actor_id: str,
    subject_hash: str,
    conditions: str,
    external_ref: str,
    created: str,
) -> None:
    connection.execute(
        """INSERT INTO business_context_decision(
            id, tenant_id, context_version_id, decision_type, decision,
            actor_id, subject_hash, conditions, external_ref, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (new_id(), tid, context["id"], decision_type, decision, actor_id, subject_hash, conditions, external_ref, created),
    )


def _latest_decision(connection: sqlite3.Connection, context_id: str, decision_type: str) -> sqlite3.Row | None:
    return connection.execute(
        """SELECT * FROM business_context_decision
        WHERE context_version_id = ? AND decision_type = ? AND revoked_at IS NULL
        ORDER BY created_at DESC, id DESC LIMIT 1""",
        (context_id, decision_type),
    ).fetchone()


def _decision_summary(connection: sqlite3.Connection, context: sqlite3.Row | None, decision_type: str) -> dict[str, Any] | None:
    if not context:
        return None
    row = _latest_decision(connection, context["id"], decision_type)
    if not row:
        return None
    return {
        "decision": row["decision"],
        "actor_id": row["actor_id"],
        "subject_hash": row["subject_hash"],
        "external_ref": row["external_ref"] or None,
        "created_at": row["created_at"],
    }


def _context_summary(context: sqlite3.Row | None) -> dict[str, Any] | None:
    if not context:
        return None
    return {
        "id": context["id"],
        "version": context["version_label"],
        "state": context["state"],
        "content_hash": context["content_hash"],
        "external_content_ref": context["external_content_ref"],
        "readiness": context["readiness"],
    }


def _next_action(
    effective: sqlite3.Row | None,
    active: sqlite3.Row | None,
    owner_decision: dict[str, Any] | None,
    persistence: dict[str, Any] | None,
    review: dict[str, Any] | None,
) -> str:
    if active:
        if active["state"] == "hold":
            return "Resolve the recorded missing evidence or base-context gate, then submit a new exact proposal."
        if active["state"] in {"changes_requested"}:
            return "Render and submit a revised exact proposal."
        if active["state"] == "proposed" and not owner_decision:
            return "Obtain the named owner's decision on the exact proposal hash."
        if active["state"] == "awaiting_persistence" and not persistence:
            return "Confirm preservation in the external tenant-private destination."
    if not effective:
        return "Confirm whether an effective context exists, then bootstrap or propose without inference."
    if not review:
        return "Ask separately whether the owner authorizes the first operating review."
    if review["decision"] == "declined":
        return "Keep operating-review work on Hold until a new explicit authorization is recorded."
    return "Use this effective context for the separately authorized operating review."


def _display_context(value: dict[str, Any] | None) -> str:
    if not value:
        return "Missing"
    return f"{value['version']} ({value['state']}; hash {value['content_hash']})"


def _display_decision(value: dict[str, Any] | None) -> str:
    if not value:
        return "Missing"
    return f"{value['decision']} by {value['actor_id']} at {value['created_at']}"
