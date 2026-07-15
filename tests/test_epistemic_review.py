from __future__ import annotations

import json

import pytest

from anyang_loop.epistemic_review import (
    claim_explanation_data,
    epistemic_review_data,
    impact_packet_data,
    render_claim_explanation_markdown,
    render_epistemic_review_markdown,
    render_impact_packet_markdown,
)
from anyang_loop.ops_db import connect, migrate
from anyang_loop.ops_cli import main
from anyang_loop.ops_render import audit_data, render_json, render_weekly_markdown, weekly_review_data
from anyang_loop.ops_service import (
    OpsError,
    add_claim,
    add_claim_dependency,
    add_source,
    init_tenant,
    transition_claim,
    update_epistemic_impact,
)


NOW = "2026-07-15T12:00:00Z"


def _tenant(connection, slug="synthetic"):
    init_tenant(
        connection,
        slug=slug,
        name=f"{slug.title()} Tenant",
        policy_profile="test-only",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=NOW,
    )


def _source(connection, title, independence, origin):
    return add_source(
        connection,
        "synthetic",
        title=title,
        source_type="synthetic",
        provenance=f"fictional://{title}",
        sensitivity="public",
        rights_status="test-only",
        evidence_ref=f"fictional://{title}/evidence",
        origin_group=origin,
        independence_status=independence,
    ).id


def _claim(connection, sources, *, text="Synthetic controlling claim", state="supported", status="active", classification="source-backed", strength="strong"):
    return add_claim(
        connection,
        "synthetic",
        sources,
        text=text,
        classification=classification,
        evidence_strength=strength,
        scope="Synthetic review tests only.",
        status=status,
        epistemic_state=state,
        actor="human-reviewer",
    ).id


def _scenario(tmp_path):
    connection = connect(tmp_path / "epistemic-review.db", create_parent=True)
    migrate(connection, NOW)
    _tenant(connection)
    first = _source(connection, "independent", "independent", "origin-a")
    repeated = _source(connection, "dependent-repeat", "dependent", "origin-a")
    claim_id = _claim(connection, [first, repeated])
    downstream_claim = _claim(
        connection,
        [first],
        text="Synthetic downstream claim",
        state="interpreted",
        status="provisional",
        strength="medium",
    )
    for downstream_type, downstream_ref in (
        ("publication", "publication-v1"),
        ("artifact", "artifact-v1"),
        ("forecast", "forecast-v1"),
        ("claim", downstream_claim),
    ):
        add_claim_dependency(
            connection,
            "synthetic",
            claim_id,
            downstream_type,
            downstream_ref,
            "support",
            "human-reviewer",
        )
    transition_claim(
        connection,
        claim_id,
        "contested",
        "contradictory-source",
        "fictional://counter",
        "human-reviewer",
        "Material synthetic conflict.",
    )
    impacts = {
        row["downstream_type"]: row
        for row in connection.execute(
            "SELECT * FROM epistemic_impact WHERE upstream_claim_id = ? AND impact_type = 'review-required'",
            (claim_id,),
        )
    }
    update_epistemic_impact(connection, impacts["claim"]["id"], "acknowledged", "human-reviewer")
    update_epistemic_impact(
        connection,
        impacts["forecast"]["id"],
        "resolved",
        "human-reviewer",
        "Forecast reviewed and bounded.",
    )
    transition_claim(
        connection,
        claim_id,
        "supported",
        "review-complete",
        "fictional://review",
        "human-reviewer",
        "Support restored for the bounded scope.",
    )
    _claim(
        connection,
        [],
        text="Synthetic unsupported hold",
        state="unresolved",
        status="hold",
        classification="unsupported-hold",
        strength="none",
    )
    return connection, claim_id, downstream_claim, impacts


def test_review_prioritizes_actionable_items_and_excludes_resolved_and_no_action(tmp_path):
    with _scenario(tmp_path)[0] as connection:
        data = epistemic_review_data(connection, "synthetic", NOW)
        assert data["counts"] == {"P0": 1, "P1": 1, "P2": 1, "actionable": 3}
        assert [item["priority"] for item in data["items"]] == ["P0", "P1", "P2"]
        assert [item["downstream_type"] for item in data["items"]] == ["publication", "artifact", "claim"]
        assert all(item["impact_type"] != "no-action" for item in data["items"])
        assert data["unsafe_claims"][0]["reasons"] == ["unsupported hold", "operational status hold"]
        assert len(data["independence_gaps"]) == 1
        rendered = render_epistemic_review_markdown(data)
        assert "P0 1, P1 1, P2 1" in rendered
        assert "publication-v1" in rendered
        assert json.loads(render_json(data)) == data


def test_claim_explanation_and_packet_reconstruct_lineage_without_mutation(tmp_path):
    connection, claim_id, downstream_claim, impacts = _scenario(tmp_path)
    with connection:
        before = connection.total_changes
        explanation = claim_explanation_data(connection, "synthetic", claim_id)
        packet = impact_packet_data(connection, "synthetic", impacts["publication"]["id"])
        assert connection.total_changes == before
        assert explanation["claim"]["epistemic_state"] == "supported"
        assert explanation["independent_support_count"] == 1
        assert len(explanation["transition_history"]) == 3
        assert explanation["latest_transition"]["cause_type"] == "review-complete"
        assert {item["downstream_type"] for item in explanation["dependencies"]} == {
            "publication", "artifact", "forecast", "claim"
        }
        assert {item["downstream_type"] for item in explanation["open_impacts"]} == {
            "publication", "artifact", "claim"
        }
        assert packet["priority"] == "P0"
        assert packet["triggering_transition"]["to_state"] == "contested"
        assert packet["dependency"]["downstream_ref"] == "publication-v1"
        assert {item["downstream_type"] for item in packet["related_open_impacts"]} == {
            "publication", "artifact", "claim"
        }
        assert "does not change" in packet["prohibited_automation"]
        assert "Latest Transition" in render_claim_explanation_markdown(explanation)
        assert "Permitted Human Actions" in render_impact_packet_markdown(packet)
        assert connection.execute(
            "SELECT epistemic_state FROM claim WHERE id = ?", (downstream_claim,)
        ).fetchone()[0] == "interpreted"


def test_claim_and_packet_reads_enforce_tenant_isolation(tmp_path):
    connection, claim_id, _, impacts = _scenario(tmp_path)
    with connection:
        _tenant(connection, "other")
        with pytest.raises(OpsError, match="Unknown claim for tenant"):
            claim_explanation_data(connection, "other", claim_id)
        with pytest.raises(OpsError, match="Unknown epistemic impact for tenant"):
            impact_packet_data(connection, "other", impacts["publication"]["id"])


def test_weekly_review_adds_the_same_epistemic_model_before_approvals(tmp_path):
    with _scenario(tmp_path)[0] as connection:
        data = weekly_review_data(connection, "synthetic", "2026-07-13", NOW)
        assert data["epistemic_review"]["counts"]["actionable"] == 3
        assert data["epistemic_review"]["items"] == epistemic_review_data(
            connection, "synthetic", NOW
        )["items"][:5]
        markdown = render_weekly_markdown(data)
        assert markdown.index("## Epistemic Review Required") < markdown.index("## Approvals Required")
        assert "P0 - review-required - publication:publication-v1" in markdown
        assert any(
            issue["code"] == "open-critical-epistemic-impact"
            for issue in audit_data(connection, "synthetic", NOW)["issues"]
        )


def test_resolving_the_publication_impact_removes_it_from_actionable_review(tmp_path):
    connection, _, _, impacts = _scenario(tmp_path)
    with connection:
        assert epistemic_review_data(connection, "synthetic", NOW)["counts"]["P0"] == 1
        update_epistemic_impact(
            connection,
            impacts["publication"]["id"],
            "resolved",
            "human-reviewer",
            "Publication reviewed against the restored claim.",
        )
        data = epistemic_review_data(connection, "synthetic", NOW)
        assert data["counts"]["P0"] == 0
        assert impacts["publication"]["id"] not in {item["impact_id"] for item in data["items"]}


def test_epistemic_cli_supports_review_explain_and_packet_formats(tmp_path, capsys):
    connection, claim_id, _, impacts = _scenario(tmp_path)
    path = tmp_path / "epistemic-review.db"
    connection.close()
    assert main([
        "--db", str(path), "epistemic", "review", "--tenant", "synthetic", "--format", "json"
    ]) == 0
    assert '"P0": 1' in capsys.readouterr().out
    assert main([
        "--db", str(path), "epistemic", "explain", "--tenant", "synthetic",
        "--claim-id", claim_id,
    ]) == 0
    assert "## Latest Transition" in capsys.readouterr().out
    assert main([
        "--db", str(path), "epistemic", "packet", "--tenant", "synthetic",
        "--impact-id", impacts["publication"]["id"],
    ]) == 0
    assert "## Permitted Human Actions" in capsys.readouterr().out
