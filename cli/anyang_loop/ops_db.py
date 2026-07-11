from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_VERSION = 3


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
    scope TEXT NOT NULL CHECK (scope IN ('assign', 'claim_use', 'spend', 'delivery', 'publication')),
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
    connection.execute(
        "INSERT OR IGNORE INTO schema_migration(version, applied_at) VALUES (?, ?)",
        (SCHEMA_VERSION, applied_at),
    )
    connection.commit()


def schema_version(connection: sqlite3.Connection) -> int:
    try:
        row = connection.execute("SELECT MAX(version) AS version FROM schema_migration").fetchone()
    except sqlite3.OperationalError:
        return 0
    return int(row["version"] or 0)
