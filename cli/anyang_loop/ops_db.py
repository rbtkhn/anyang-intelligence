from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path


SCHEMA_VERSION = 6


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migration (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tenant (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    policy_profile TEXT NOT NULL,
    retainer_cents INTEGER NOT NULL DEFAULT 0 CHECK (retainer_cents >= 0),
    contractor_budget_cents INTEGER NOT NULL DEFAULT 0 CHECK (contractor_budget_cents >= 0),
    tool_budget_cents INTEGER NOT NULL DEFAULT 0 CHECK (tool_budget_cents >= 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actor (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL,
    UNIQUE (tenant_id, name)
);

CREATE TABLE IF NOT EXISTS authority_grant (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    actor_id TEXT NOT NULL REFERENCES actor(id),
    scope TEXT NOT NULL CHECK (scope IN ('assign', 'claim_use', 'spend', 'delivery', 'publication', 'business_context')),
    effective_at TEXT NOT NULL,
    expires_at TEXT,
    revoked_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    provenance TEXT NOT NULL,
    sensitivity TEXT NOT NULL CHECK (sensitivity IN ('public', 'internal', 'private', 'restricted')),
    rights_status TEXT NOT NULL,
    evidence_ref TEXT NOT NULL,
    fresh_until TEXT,
    origin_group TEXT,
    independence_status TEXT NOT NULL DEFAULT 'unknown' CHECK (
        independence_status IN ('unknown', 'independent', 'dependent')
    ),
    redacted_summary TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    text TEXT NOT NULL,
    classification TEXT NOT NULL CHECK (classification IN (
        'source-backed', 'customer-approved', 'template-default',
        'provisional-assumption', 'speculative-scenario', 'unsupported-hold'
    )),
    evidence_strength TEXT NOT NULL CHECK (evidence_strength IN ('strong', 'medium', 'thin', 'none')),
    scope TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'provisional', 'hold', 'retired')),
    epistemic_state TEXT NOT NULL DEFAULT 'unresolved' CHECK (epistemic_state IN (
        'attributed', 'interpreted', 'contested', 'supported',
        'disconfirmed', 'unresolved', 'adopted', 'retired'
    )),
    epistemic_version INTEGER NOT NULL DEFAULT 1 CHECK (epistemic_version > 0),
    expires_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim_source (
    claim_id TEXT NOT NULL REFERENCES claim(id),
    source_id TEXT NOT NULL REFERENCES source(id),
    PRIMARY KEY (claim_id, source_id)
);

CREATE TABLE IF NOT EXISTS work_item (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    title TEXT NOT NULL,
    asset_job TEXT NOT NULL,
    owner TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    deliverable TEXT NOT NULL,
    assignee TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    due_at TEXT,
    capacity_hours REAL NOT NULL CHECK (capacity_hours >= 0),
    budget_cents INTEGER NOT NULL DEFAULT 0 CHECK (budget_cents >= 0),
    blocker TEXT NOT NULL DEFAULT '',
    responsible_human TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS work_source (
    work_id TEXT NOT NULL REFERENCES work_item(id),
    source_id TEXT NOT NULL REFERENCES source(id),
    PRIMARY KEY (work_id, source_id)
);

CREATE TABLE IF NOT EXISTS work_claim (
    work_id TEXT NOT NULL REFERENCES work_item(id),
    claim_id TEXT NOT NULL REFERENCES claim(id),
    PRIMARY KEY (work_id, claim_id)
);

CREATE TABLE IF NOT EXISTS claim_transition (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    claim_id TEXT NOT NULL REFERENCES claim(id),
    version INTEGER NOT NULL CHECK (version > 0),
    from_state TEXT,
    to_state TEXT NOT NULL CHECK (to_state IN (
        'attributed', 'interpreted', 'contested', 'supported',
        'disconfirmed', 'unresolved', 'adopted', 'retired'
    )),
    cause_type TEXT NOT NULL,
    cause_ref TEXT NOT NULL,
    actor TEXT NOT NULL,
    rationale TEXT NOT NULL,
    prior_transition_hash TEXT NOT NULL DEFAULT '',
    transition_hash TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    UNIQUE (claim_id, version)
);

CREATE TABLE IF NOT EXISTS claim_dependency (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    upstream_claim_id TEXT NOT NULL REFERENCES claim(id),
    downstream_type TEXT NOT NULL CHECK (
        downstream_type IN ('claim', 'work', 'artifact', 'forecast', 'publication')
    ),
    downstream_ref TEXT NOT NULL,
    dependency_role TEXT NOT NULL CHECK (
        dependency_role IN ('support', 'assumption', 'context', 'alternative', 'authorization')
    ),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL,
    retired_at TEXT
);

CREATE TABLE IF NOT EXISTS epistemic_impact (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    transition_id TEXT NOT NULL REFERENCES claim_transition(id),
    upstream_claim_id TEXT NOT NULL REFERENCES claim(id),
    dependency_id TEXT NOT NULL REFERENCES claim_dependency(id),
    downstream_type TEXT NOT NULL,
    downstream_ref TEXT NOT NULL,
    impact_type TEXT NOT NULL CHECK (
        impact_type IN ('review-required', 'conditional', 'unresolved', 'stale', 'no-action')
    ),
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'acknowledged', 'resolved')),
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    acknowledged_at TEXT,
    resolved_at TEXT,
    resolved_by TEXT,
    resolution TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    work_id TEXT REFERENCES work_item(id),
    evidence_type TEXT NOT NULL,
    reference TEXT NOT NULL,
    creator TEXT NOT NULL,
    integrity_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approval (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    work_id TEXT NOT NULL REFERENCES work_item(id),
    approver_actor_id TEXT NOT NULL REFERENCES actor(id),
    scope TEXT NOT NULL CHECK (scope IN ('assign', 'claim_use', 'spend', 'delivery', 'publication')),
    subject_version INTEGER NOT NULL,
    subject_hash TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('approved', 'approved_with_changes', 'rejected')),
    conditions TEXT NOT NULL DEFAULT '',
    expires_at TEXT,
    revoked_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS outcome (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    work_id TEXT NOT NULL REFERENCES work_item(id),
    expected_result TEXT NOT NULL,
    observed_result TEXT NOT NULL DEFAULT 'pending',
    metric TEXT NOT NULL,
    metric_value REAL,
    observation_window TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'pending')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    work_id TEXT REFERENCES work_item(id),
    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT,
    details TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS authority_receipt (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    actor TEXT NOT NULL CHECK (actor IN ('engineer', 'executive', 'interface', 'client')),
    domain TEXT NOT NULL,
    lane TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    limits TEXT NOT NULL DEFAULT '',
    evidence_ref TEXT NOT NULL,
    approver TEXT NOT NULL CHECK (approver IN ('engineer', 'client')),
    effective_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    review_cadence TEXT NOT NULL DEFAULT '',
    audit_ref TEXT NOT NULL,
    recovery_ref TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('proposed', 'approved', 'revoked', 'expired')),
    revoked_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS authority_conflict (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    target TEXT NOT NULL,
    instructions_json TEXT NOT NULL,
    resolution_owner TEXT NOT NULL CHECK (resolution_owner IN ('engineer', 'client')),
    status TEXT NOT NULL CHECK (status IN ('open', 'resolved')),
    resolution TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS emergency_stop (
    id TEXT PRIMARY KEY,
    repo_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'cleared')),
    activated_by TEXT NOT NULL CHECK (activated_by = 'engineer'),
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    cleared_at TEXT,
    restart_receipt_ref TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS authority_observation (
    id TEXT PRIMARY KEY,
    tenant_id TEXT REFERENCES tenant(id),
    actor TEXT NOT NULL,
    domain TEXT NOT NULL,
    lane TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    outcome TEXT NOT NULL,
    receipt_id TEXT REFERENCES authority_receipt(id),
    evidence_ref TEXT NOT NULL DEFAULT '',
    minutes REAL NOT NULL DEFAULT 0 CHECK (minutes >= 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS business_context_version (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    business_reference TEXT NOT NULL,
    version_label TEXT NOT NULL,
    base_context_id TEXT REFERENCES business_context_version(id),
    external_content_ref TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    authority_receipt_ref TEXT NOT NULL,
    readiness TEXT NOT NULL CHECK (readiness IN ('ready', 'provisional', 'hold')),
    state TEXT NOT NULL CHECK (state IN (
        'proposed', 'awaiting_persistence', 'effective', 'superseded',
        'rejected', 'changes_requested', 'hold'
    )),
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    effective_at TEXT,
    superseded_at TEXT,
    UNIQUE (tenant_id, version_label)
);

CREATE TABLE IF NOT EXISTS business_context_evidence (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    context_version_id TEXT NOT NULL REFERENCES business_context_version(id),
    evidence_class TEXT NOT NULL CHECK (evidence_class IN ('confirmed', 'estimate', 'hypothesis', 'missing')),
    evidence_kind TEXT NOT NULL,
    redacted_summary TEXT NOT NULL,
    source_ref TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    sensitivity TEXT NOT NULL CHECK (sensitivity IN ('public', 'internal', 'private', 'restricted')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS business_context_decision (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    context_version_id TEXT NOT NULL REFERENCES business_context_version(id),
    decision_type TEXT NOT NULL CHECK (decision_type IN (
        'context_approval', 'persistence_confirmation', 'operating_review_authorization'
    )),
    decision TEXT NOT NULL CHECK (decision IN (
        'approved', 'rejected', 'changes_requested', 'confirmed', 'failed', 'declined'
    )),
    actor_id TEXT NOT NULL REFERENCES actor(id),
    subject_hash TEXT NOT NULL,
    conditions TEXT NOT NULL DEFAULT '',
    external_ref TEXT NOT NULL DEFAULT '',
    revoked_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS learning_event (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenant(id),
    signal_type TEXT NOT NULL CHECK (signal_type IN ('success', 'friction', 'review', 'closeout')),
    scope TEXT NOT NULL,
    observation TEXT NOT NULL,
    evidence_ref TEXT NOT NULL,
    bounded_lesson TEXT NOT NULL,
    disposition TEXT NOT NULL CHECK (disposition IN ('note', 'test', 'adopt', 'reject')),
    validation TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cadence_handoff (
    id TEXT PRIMARY KEY,
    repo_id TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    recorded_by TEXT NOT NULL,
    git_head TEXT NOT NULL,
    branch TEXT NOT NULL,
    worktree_state TEXT NOT NULL CHECK (worktree_state IN ('clean', 'dirty')),
    snapshot_fingerprint TEXT NOT NULL,
    validation_json TEXT NOT NULL,
    touched_surfaces_json TEXT NOT NULL,
    fresh_issue_codes_json TEXT NOT NULL,
    legacy_warning_codes_json TEXT NOT NULL,
    tomorrow_inherits TEXT NOT NULL,
    explicit_record INTEGER NOT NULL CHECK (explicit_record = 1)
);

CREATE TABLE IF NOT EXISTS cadence_measurement (
    id TEXT PRIMARY KEY,
    repo_id TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('coffee', 'dream', 'operating_review', 'other')),
    scheduled INTEGER NOT NULL CHECK (scheduled IN (0, 1)),
    completion_status TEXT NOT NULL CHECK (completion_status IN ('completed', 'partial', 'abandoned')),
    state_source TEXT NOT NULL CHECK (state_source IN ('recorded_handoff', 'git_fallback', 'manual_reconstruction')),
    manual_reconstruction INTEGER NOT NULL CHECK (manual_reconstruction IN (0, 1)),
    reconstruction_minutes REAL NOT NULL CHECK (reconstruction_minutes >= 0),
    evidence_check_passed INTEGER NOT NULL CHECK (evidence_check_passed IN (0, 1)),
    privacy_check_passed INTEGER NOT NULL CHECK (privacy_check_passed IN (0, 1)),
    authority_check_passed INTEGER NOT NULL CHECK (authority_check_passed IN (0, 1)),
    recorded_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    CHECK (manual_reconstruction = 1 OR reconstruction_minutes = 0),
    CHECK (state_source != 'manual_reconstruction' OR manual_reconstruction = 1)
);

CREATE INDEX IF NOT EXISTS idx_work_tenant_state ON work_item(tenant_id, state);
CREATE INDEX IF NOT EXISTS idx_event_tenant_created ON event(tenant_id, created_at);
CREATE INDEX IF NOT EXISTS idx_approval_work_scope ON approval(work_id, scope);
CREATE INDEX IF NOT EXISTS idx_cadence_repo_recorded ON cadence_handoff(repo_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_cadence_measurement_repo_occurred ON cadence_measurement(repo_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_claim_transition_claim_version ON claim_transition(claim_id, version);
CREATE INDEX IF NOT EXISTS idx_claim_dependency_upstream ON claim_dependency(upstream_claim_id, active);
CREATE INDEX IF NOT EXISTS idx_epistemic_impact_status ON epistemic_impact(tenant_id, status, impact_type);
CREATE INDEX IF NOT EXISTS idx_business_context_tenant_state ON business_context_version(tenant_id, state);
CREATE INDEX IF NOT EXISTS idx_business_context_evidence_version ON business_context_evidence(context_version_id, evidence_class);
CREATE INDEX IF NOT EXISTS idx_business_context_decision_version ON business_context_decision(context_version_id, decision_type, created_at);

CREATE UNIQUE INDEX IF NOT EXISTS idx_business_context_one_effective
ON business_context_version(tenant_id) WHERE state = 'effective';

CREATE TRIGGER IF NOT EXISTS business_context_content_immutable
BEFORE UPDATE OF business_reference, version_label, base_context_id, external_content_ref,
    content_hash, authority_receipt_ref, readiness, created_by, created_at
ON business_context_version
BEGIN
    SELECT RAISE(ABORT, 'business context version content is immutable');
END;

CREATE TRIGGER IF NOT EXISTS business_context_evidence_immutable_update
BEFORE UPDATE ON business_context_evidence
BEGIN
    SELECT RAISE(ABORT, 'business context evidence is immutable');
END;

CREATE TRIGGER IF NOT EXISTS business_context_evidence_immutable_delete
BEFORE DELETE ON business_context_evidence
BEGIN
    SELECT RAISE(ABORT, 'business context evidence is immutable');
END;

CREATE TRIGGER IF NOT EXISTS business_context_decision_immutable_update
BEFORE UPDATE ON business_context_decision
BEGIN
    SELECT RAISE(ABORT, 'business context decisions are immutable');
END;

CREATE TRIGGER IF NOT EXISTS business_context_decision_immutable_delete
BEFORE DELETE ON business_context_decision
BEGIN
    SELECT RAISE(ABORT, 'business context decisions are immutable');
END;

CREATE TRIGGER IF NOT EXISTS claim_transition_append_only_update
BEFORE UPDATE ON claim_transition
BEGIN
    SELECT RAISE(ABORT, 'claim_transition is append-only');
END;

CREATE TRIGGER IF NOT EXISTS claim_transition_append_only_delete
BEFORE DELETE ON claim_transition
BEGIN
    SELECT RAISE(ABORT, 'claim_transition is append-only');
END;
"""


def connect(path: str | Path, *, create_parent: bool = False) -> sqlite3.Connection:
    target = Path(path).expanduser().resolve()
    if create_parent:
        target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def migrate(connection: sqlite3.Connection, applied_at: str) -> None:
    connection.executescript(SCHEMA)
    _ensure_business_context_authority_scope(connection)
    _ensure_column(connection, "source", "origin_group", "TEXT")
    _ensure_column(
        connection,
        "source",
        "independence_status",
        "TEXT NOT NULL DEFAULT 'unknown' CHECK (independence_status IN ('unknown', 'independent', 'dependent'))",
    )
    _ensure_column(
        connection,
        "claim",
        "epistemic_state",
        "TEXT NOT NULL DEFAULT 'unresolved' CHECK (epistemic_state IN ('attributed', 'interpreted', 'contested', 'supported', 'disconfirmed', 'unresolved', 'adopted', 'retired'))",
    )
    _ensure_column(connection, "claim", "epistemic_version", "INTEGER NOT NULL DEFAULT 1 CHECK (epistemic_version > 0)")
    _backfill_legacy_claim_transitions(connection, applied_at)
    connection.execute(
        "INSERT OR IGNORE INTO schema_migration(version, applied_at) VALUES (?, ?)",
        (SCHEMA_VERSION, applied_at),
    )
    connection.commit()


def _ensure_business_context_authority_scope(connection: sqlite3.Connection) -> None:
    row = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'authority_grant'"
    ).fetchone()
    if row and "business_context" in str(row[0]):
        return
    connection.execute("PRAGMA foreign_keys = OFF")
    try:
        connection.executescript(
            """
            ALTER TABLE authority_grant RENAME TO authority_grant_v4;
            CREATE TABLE authority_grant (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL REFERENCES tenant(id),
                actor_id TEXT NOT NULL REFERENCES actor(id),
                scope TEXT NOT NULL CHECK (scope IN (
                    'assign', 'claim_use', 'spend', 'delivery', 'publication', 'business_context'
                )),
                effective_at TEXT NOT NULL,
                expires_at TEXT,
                revoked_at TEXT,
                created_at TEXT NOT NULL
            );
            INSERT INTO authority_grant(
                id, tenant_id, actor_id, scope, effective_at, expires_at, revoked_at, created_at
            )
            SELECT id, tenant_id, actor_id, scope, effective_at, expires_at, revoked_at, created_at
            FROM authority_grant_v4;
            DROP TABLE authority_grant_v4;
            """
        )
    finally:
        connection.execute("PRAGMA foreign_keys = ON")


def _ensure_column(connection: sqlite3.Connection, table: str, column: str, declaration: str) -> None:
    columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
    if column not in columns:
        connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")


def _backfill_legacy_claim_transitions(connection: sqlite3.Connection, applied_at: str) -> None:
    rows = connection.execute(
        """SELECT c.* FROM claim c
        WHERE NOT EXISTS (SELECT 1 FROM claim_transition t WHERE t.claim_id = c.id)
        ORDER BY c.id"""
    ).fetchall()
    for claim in rows:
        transition_id = f"legacy-migration-{claim['id']}"
        payload = {
            "id": transition_id,
            "claim_id": claim["id"],
            "version": 1,
            "from_state": None,
            "to_state": "unresolved",
            "cause_type": "legacy-migration",
            "cause_ref": "schema-v4",
            "actor": "system",
            "rationale": "Pre-v4 epistemic history was not reconstructed.",
            "prior_transition_hash": "",
            "created_at": applied_at,
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        connection.execute(
            """INSERT INTO claim_transition(
                id, tenant_id, claim_id, version, from_state, to_state, cause_type,
                cause_ref, actor, rationale, prior_transition_hash, transition_hash, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                transition_id,
                claim["tenant_id"],
                claim["id"],
                1,
                None,
                "unresolved",
                "legacy-migration",
                "schema-v4",
                "system",
                "Pre-v4 epistemic history was not reconstructed.",
                "",
                digest,
                applied_at,
            ),
        )
        connection.execute(
            "UPDATE claim SET epistemic_state = 'unresolved', epistemic_version = 1 WHERE id = ?",
            (claim["id"],),
        )


def schema_version(connection: sqlite3.Connection) -> int:
    try:
        row = connection.execute("SELECT MAX(version) AS version FROM schema_migration").fetchone()
    except sqlite3.OperationalError:
        return 0
    return int(row["version"] or 0)
