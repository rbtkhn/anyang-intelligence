from __future__ import annotations

import sqlite3

import pytest

from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_render import audit_data
from anyang_loop.ops_service import (
    OpsError,
    add_actor,
    add_claim,
    add_claim_dependency,
    add_source,
    create_work,
    grant_authority,
    init_tenant,
    list_epistemic_impacts,
    record_approval,
    transition_claim,
    update_epistemic_impact,
)


NOW = "2026-07-15T12:00:00Z"


def _ledger(tmp_path):
    connection = connect(tmp_path / "epistemic.db", create_parent=True)
    migrate(connection, NOW)
    init_tenant(
        connection,
        slug="synthetic",
        name="Synthetic Epistemic Tenant",
        policy_profile="test-only",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )
    return connection


def _source(connection, *, independence="independent", title="Synthetic source"):
    return add_source(
        connection,
        "synthetic",
        title=title,
        source_type="synthetic-test",
        provenance="fictional://epistemic-test",
        sensitivity="public",
        rights_status="test-only",
        evidence_ref=f"fictional://{title}",
        origin_group="synthetic-origin",
        independence_status=independence,
    ).id


def _claim(connection, source_ids, *, state="supported", status="active", strength="medium"):
    return add_claim(
        connection,
        "synthetic",
        source_ids,
        text="A fictional governed assertion.",
        classification="source-backed",
        evidence_strength=strength,
        scope="Synthetic tests only.",
        status=status,
        epistemic_state=state,
        actor="test-operator",
    ).id


def test_v3_to_v4_migration_preserves_claim_and_marks_history_unresolved(tmp_path):
    path = tmp_path / "legacy-v3.db"
    raw = sqlite3.connect(path)
    raw.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE schema_migration(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
        CREATE TABLE tenant(
          id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
          policy_profile TEXT NOT NULL, retainer_cents INTEGER NOT NULL DEFAULT 0,
          contractor_budget_cents INTEGER NOT NULL DEFAULT 0, tool_budget_cents INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL
        );
        CREATE TABLE source(
          id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL REFERENCES tenant(id), title TEXT NOT NULL,
          source_type TEXT NOT NULL, provenance TEXT NOT NULL, sensitivity TEXT NOT NULL,
          rights_status TEXT NOT NULL, evidence_ref TEXT NOT NULL, fresh_until TEXT,
          redacted_summary TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL
        );
        CREATE TABLE claim(
          id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL REFERENCES tenant(id), text TEXT NOT NULL,
          classification TEXT NOT NULL, evidence_strength TEXT NOT NULL, scope TEXT NOT NULL,
          status TEXT NOT NULL, expires_at TEXT, created_at TEXT NOT NULL
        );
        INSERT INTO schema_migration VALUES (3, '2026-07-01T00:00:00Z');
        INSERT INTO tenant VALUES ('t1', 'legacy', 'Legacy', 'test', 0, 0, 0, '2026-07-01T00:00:00Z');
        INSERT INTO claim VALUES (
          'c1', 't1', 'Preserved legacy text', 'provisional-assumption', 'thin',
          'Preserved scope', 'active', NULL, '2026-07-01T00:00:00Z'
        );
        """
    )
    raw.commit()
    raw.close()

    with connect(path) as connection:
        migrate(connection, NOW)
        claim = connection.execute("SELECT * FROM claim WHERE id = 'c1'").fetchone()
        transition = connection.execute("SELECT * FROM claim_transition WHERE claim_id = 'c1'").fetchone()
        assert schema_version(connection) == SCHEMA_VERSION == 4
        assert (claim["text"], claim["scope"], claim["status"]) == (
            "Preserved legacy text",
            "Preserved scope",
            "active",
        )
        assert (claim["epistemic_state"], claim["epistemic_version"]) == ("unresolved", 1)
        assert (transition["cause_type"], transition["actor"], transition["from_state"]) == (
            "legacy-migration",
            "system",
            None,
        )
        assert audit_data(connection, "legacy")["epistemic"]["transition_count"] == 1


def test_transitions_require_cause_follow_allowed_graph_and_are_append_only(tmp_path):
    with _ledger(tmp_path) as connection:
        claim_id = _claim(connection, [_source(connection)])
        with pytest.raises(OpsError, match="Invalid epistemic transition"):
            transition_claim(connection, claim_id, "attributed", "review", "r-1", "operator", "Rewind")
        with pytest.raises(OpsError, match="requires cause reference"):
            transition_claim(connection, claim_id, "contested", "review", "", "operator", "New conflict")

        result = transition_claim(
            connection, claim_id, "contested", "contradictory-source", "fictional://counter", "operator", "Conflict needs review."
        )
        row = connection.execute("SELECT * FROM claim WHERE id = ?", (claim_id,)).fetchone()
        transitions = connection.execute(
            "SELECT * FROM claim_transition WHERE claim_id = ? ORDER BY version", (claim_id,)
        ).fetchall()
        assert (row["epistemic_state"], row["epistemic_version"]) == ("contested", 2)
        assert transitions[1]["prior_transition_hash"] == transitions[0]["transition_hash"]
        assert result.details["epistemic_version"] == 2
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            connection.execute("UPDATE claim_transition SET rationale = 'tampered' WHERE claim_id = ?", (claim_id,))
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            connection.execute("DELETE FROM claim_transition WHERE claim_id = ?", (claim_id,))
        assert not [issue for issue in audit_data(connection, "synthetic")["issues"] if issue["code"] == "invalid-claim-transition-chain"]


def test_unknown_or_dependent_sources_never_count_as_independent_support(tmp_path):
    with _ledger(tmp_path) as connection:
        claim_id = _claim(
            connection,
            [_source(connection, independence="independent", title="one"), _source(connection, independence="dependent", title="repeat")],
            strength="strong",
        )
        add_claim_dependency(connection, "synthetic", claim_id, "artifact", "synthetic-note", "support", "operator")
        epistemic = audit_data(connection, "synthetic")["epistemic"]
        assert claim_id in epistemic["independence_gap_claim_ids"]
        assert epistemic["independent_support_counts"][claim_id] == 1
        assert epistemic["structural_points"] >= 4


def test_upstream_contestation_creates_impacts_without_upgrading_downstream(tmp_path):
    with _ledger(tmp_path) as connection:
        source_id = _source(connection)
        upstream = _claim(connection, [source_id], state="supported")
        downstream = _claim(connection, [source_id], state="interpreted", status="provisional")
        for downstream_type, downstream_ref in (
            ("claim", downstream),
            ("forecast", "synthetic-forecast-v1"),
            ("publication", "synthetic-publication-v1"),
        ):
            add_claim_dependency(connection, "synthetic", upstream, downstream_type, downstream_ref, "assumption", "operator")

        transition_claim(
            connection, upstream, "contested", "new-evidence", "fictional://counter", "human-reviewer", "Synthetic conflict."
        )
        impacts = list_epistemic_impacts(connection, "synthetic", "open")
        assert len(impacts) == 3
        assert {item["impact_type"] for item in impacts} == {"review-required"}
        assert connection.execute("SELECT epistemic_state FROM claim WHERE id = ?", (downstream,)).fetchone()[0] == "interpreted"
        assert connection.execute("SELECT COUNT(*) FROM claim_source WHERE claim_id = ?", (upstream,)).fetchone()[0] == 1
        audit = audit_data(connection, "synthetic")
        assert len(audit["epistemic"]["critical_gaps"]) == 2

        for impact in impacts:
            update_epistemic_impact(connection, impact["id"], "resolved", "human-reviewer", "Reviewed synthetic dependency.")
        assert not list_epistemic_impacts(connection, "synthetic", "open")
        assert not audit_data(connection, "synthetic")["epistemic"]["critical_gaps"]


def test_open_publication_impact_blocks_publication_approval(tmp_path):
    with _ledger(tmp_path) as connection:
        source_id = _source(connection)
        claim_id = _claim(connection, [source_id], state="supported", status="provisional")
        work_id = create_work(
            connection,
            "synthetic",
            [source_id],
            [claim_id],
            title="Synthetic publication",
            asset_job="Test the publication gate.",
            owner="owner",
            reviewer="reviewer",
            deliverable="fictional://publication",
            capacity_hours=1,
            actor="operator",
        ).id
        actor_id = add_actor(connection, "synthetic", "Human Approver", "owner").id
        grant_authority(connection, "synthetic", actor_id, "publication", NOW, None)
        add_claim_dependency(
            connection, "synthetic", claim_id, "publication", "synthetic-publication-v1", "support", "operator"
        )
        transition_claim(
            connection, claim_id, "contested", "new-evidence", "fictional://counter", "reviewer", "Material conflict."
        )
        with pytest.raises(OpsError, match="unresolved publication impact"):
            record_approval(
                connection,
                "synthetic",
                work_id=work_id,
                approver_actor_id=actor_id,
                scope="publication",
                decision="approved",
            )
