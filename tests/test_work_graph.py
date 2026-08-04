from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from anyang_loop.graph_evidence import collect_graph_evidence
from anyang_loop.council_workroom import create_council_transaction
from anyang_loop.ops_db import connect, migrate
from anyang_loop.ops_service import init_tenant
from anyang_loop.project_cli import main
from anyang_loop.validation_evidence import read_full_validation_evidence
from anyang_loop.work_graph import (
    WorkGraphError,
    evaluate_work_graph,
    render_graph_json,
    render_graph_markdown,
    validate_work_graph,
    verify_graph_status,
)


AS_OF = "2026-08-04T18:00:00Z"


def graph_packet() -> dict:
    return {
        "contract_version": "anyang-work-graph/v1",
        "graph_id": "synthetic-graph",
        "objective": "Inspect one bounded repository graph",
        "objective_ref": "docs/work-graph-status-v1.md",
        "scope": {
            "repository": "synthetic-repo",
            "tenant": "anyang-internal",
            "permitted_paths": ["src", "docs/work.md"],
            "excluded_paths": ["docs/private-draft.md"],
        },
        "nodes": [
            {
                "id": "inspect",
                "kind": "inspection",
                "summary": "Inspect the declared artifact",
                "completion": [{"type": "file-exists", "path": "docs/work.md"}],
            },
            {
                "id": "commit",
                "kind": "action",
                "summary": "Commit the bounded change",
                "depends_on": ["inspect"],
                "completion": [{"type": "git-commit", "commit": "a" * 40}],
                "action_boundary": "commit",
                "human_gate": "required",
            },
        ],
    }


def synthetic_evidence(*, inspect: str = "satisfied", commit: str = "missing") -> dict:
    return {
        "source_snapshot": {
            "repository": "synthetic-repo",
            "head": "b" * 40,
            "branch": "main",
            "staged": [],
            "unstaged": [],
            "untracked": ["docs/private-draft.md"],
            "changed_paths": ["docs/private-draft.md"],
            "snapshot_digest": "c" * 64,
        },
        "nodes": {
            "inspect": [{"type": "file-exists", "status": inspect, "summary": "file", "refs": ["docs/work.md"]}],
            "commit": [{"type": "git-commit", "status": commit, "summary": "commit", "refs": ["a" * 40]}],
        },
    }


def init_repo(path: Path) -> None:
    path.mkdir()
    run_git(path, "init")
    run_git(path, "config", "user.email", "synthetic" + chr(64) + "example.invalid")
    run_git(path, "config", "user.name", "Synthetic Operator")
    (path / "src").mkdir()
    (path / "docs").mkdir()
    (path / "docs" / "work.md").write_text("work\n", encoding="utf-8")
    (path / "pyproject.toml").write_text(
        "[project]\nname='synthetic'\nversion='0.0.0'\ndependencies=[]\n"
        "[project.optional-dependencies]\ndev=[]\n",
        encoding="utf-8",
    )
    run_git(path, "add", "docs/work.md", "pyproject.toml")
    run_git(path, "commit", "-m", "seed")


def run_git(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=path, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.stdout.strip()


def test_validation_accepts_bounded_dag_and_rejects_cycles_and_unknowns(tmp_path):
    packet = graph_packet()
    validate_work_graph(packet, tmp_path)

    cycle = copy.deepcopy(packet)
    cycle["nodes"][0]["depends_on"] = ["commit"]
    with pytest.raises(WorkGraphError, match="cycle"):
        validate_work_graph(cycle)

    unknown = copy.deepcopy(packet)
    unknown["nodes"][0]["unexpected"] = True
    with pytest.raises(WorkGraphError, match="unknown fields"):
        validate_work_graph(unknown)

    adapter = copy.deepcopy(packet)
    adapter["nodes"][0]["completion"][0]["type"] = "shell-command"
    with pytest.raises(WorkGraphError, match="unsupported"):
        validate_work_graph(adapter)


@pytest.mark.parametrize(
    "mutation, message",
    [
        (lambda value: value.update(contract_version="anyang-work-graph/v2"), "contract_version"),
        (lambda value: value["scope"].update(permitted_paths=["../escape"]), "repository-relative"),
        (lambda value: value["nodes"][1].update(action_boundary="push", human_gate="none"), "human_gate"),
        (lambda value: value["nodes"][0]["completion"][0].update(path="C:/private/file"), "repository-relative"),
        (lambda value: value.update(objective="operator" + chr(64) + "example.com"), "privacy scan"),
    ],
)
def test_invalid_or_unsafe_declarations_fail_closed(mutation, message):
    packet = graph_packet()
    mutation(packet)
    with pytest.raises(WorkGraphError, match=message):
        validate_work_graph(packet)


def test_projection_derives_judgment_and_excluded_dirty_context():
    projection = evaluate_work_graph(graph_packet(), synthetic_evidence(), as_of=AS_OF)
    assert projection["authority_effect"] == "none"
    assert projection["disposition"] == "needs-judgment"
    assert [node["state"] for node in projection["nodes"]] == ["needs-judgment", "satisfied"]
    assert projection["scope_exclusions"] == [{"path": "docs/private-draft.md", "changed": True}]
    assert projection["next_permissible_actions"][0]["requires_explicit_authority"] is True
    assert render_graph_json(projection) == render_graph_json(projection)
    assert "Authority effect: `none`" in render_graph_markdown(projection)


def test_missing_authority_lineage_remains_visible_after_observed_action():
    projection = evaluate_work_graph(
        graph_packet(), synthetic_evidence(commit="satisfied"), as_of=AS_OF
    )
    assert projection["disposition"] == "complete"
    assert "authority-lineage-missing" in {item["code"] for item in projection["attention_flags"]}


def test_stale_and_held_evidence_propagate_without_claiming_completion():
    stale = evaluate_work_graph(graph_packet(), synthetic_evidence(inspect="stale"), as_of=AS_OF)
    held = evaluate_work_graph(graph_packet(), synthetic_evidence(inspect="held"), as_of=AS_OF)
    assert stale["disposition"] == "blocked"
    assert {node["id"]: node["state"] for node in stale["nodes"]} == {
        "commit": "blocked",
        "inspect": "stale",
    }
    assert held["disposition"] == "hold"


def test_projection_hash_detects_tampering():
    projection = evaluate_work_graph(graph_packet(), synthetic_evidence(), as_of=AS_OF)
    assert verify_graph_status(projection)["ok"] is True
    projection["nodes"][0]["state"] = "satisfied"
    verification = verify_graph_status(projection)
    assert verification["ok"] is False
    assert "projection-hash-mismatch" in {item["code"] for item in verification["issues"]}


def test_explicit_reference_is_lineage_not_completion_or_authority():
    packet = graph_packet()
    packet["nodes"] = [
        {
            "id": "reference",
            "kind": "decision",
            "summary": "Inspect a supplied decision reference",
            "completion": [{"type": "explicit-reference", "source_ref": "thread:synthetic#decision"}],
        }
    ]
    evidence = {
        "source_snapshot": synthetic_evidence()["source_snapshot"],
        "nodes": {
            "reference": [
                {"type": "explicit-reference", "status": "present", "summary": "reference", "refs": []}
            ]
        },
    }
    projection = evaluate_work_graph(packet, evidence, as_of=AS_OF)
    assert projection["nodes"][0]["state"] == "in-progress"
    assert projection["authority_effect"] == "none"


def test_git_and_file_evidence_are_read_only_and_scope_aware(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    packet = graph_packet()
    packet["nodes"] = [
        {
            "id": "inspect",
            "kind": "inspection",
            "summary": "Inspect files and changes",
            "completion": [
                {"type": "file-exists", "path": "docs/work.md"},
                {"type": "git-changes-within-scope"},
            ],
        }
    ]
    (repo / "src" / "change.py").write_text("value = 1\n", encoding="utf-8")
    (repo / "docs" / "private-draft.md").write_text("excluded\n", encoding="utf-8")
    validate_work_graph(packet, repo)
    index = repo / ".git" / "index"
    before_index = (index.read_bytes(), index.stat().st_mtime_ns)
    before_files = {path.relative_to(repo).as_posix(): path.read_bytes() for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts}
    evidence = collect_graph_evidence(packet, repo, as_of=AS_OF)
    after_index = (index.read_bytes(), index.stat().st_mtime_ns)
    after_files = {path.relative_to(repo).as_posix(): path.read_bytes() for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts}
    assert before_index == after_index
    assert before_files == after_files
    results = evidence["nodes"]["inspect"]
    assert [item["status"] for item in results] == ["satisfied", "satisfied"]
    assert "docs/private-draft.md" in evidence["source_snapshot"]["changed_paths"]


def test_scope_prefixes_do_not_accept_similarly_named_siblings(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    packet = graph_packet()
    packet["nodes"] = [
        {
            "id": "scope",
            "kind": "inspection",
            "summary": "Inspect exact path boundaries",
            "completion": [{"type": "git-changes-within-scope"}],
        }
    ]
    (repo / "src-escape").mkdir()
    (repo / "src-escape" / "change.py").write_text("value = 1\n", encoding="utf-8")
    evidence = collect_graph_evidence(packet, repo, as_of=AS_OF)
    assert evidence["nodes"]["scope"][0]["status"] == "held"
    assert evidence["nodes"]["scope"][0]["refs"] == ["src-escape/change.py"]


def test_remote_tracking_check_never_fetches(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    head = run_git(repo, "rev-parse", "HEAD")
    run_git(repo, "update-ref", "refs/remotes/origin/main", head)
    packet = graph_packet()
    packet["nodes"] = [
        {
            "id": "push",
            "kind": "action",
            "summary": "Observe local remote-tracking containment",
            "completion": [{"type": "git-remote-tracking-contains", "ref": "origin/main", "commit": head}],
            "action_boundary": "push",
            "human_gate": "required",
            "authority_ref": "thread:synthetic#push",
        }
    ]
    calls: list[list[str]] = []
    original = subprocess.run

    def observe(command, *args, **kwargs):
        calls.append(list(command))
        assert kwargs["env"]["GIT_OPTIONAL_LOCKS"] == "0"
        return original(command, *args, **kwargs)

    monkeypatch.setattr("anyang_loop.graph_evidence.subprocess.run", observe)
    evidence = collect_graph_evidence(packet, repo, as_of=AS_OF)
    assert evidence["nodes"]["push"][0]["status"] == "satisfied"
    assert all("fetch" not in command for command in calls)


def test_cli_status_and_offline_verify_write_no_artifact(tmp_path, capsys):
    repo = tmp_path / "repo"
    init_repo(repo)
    packet = graph_packet()
    packet["nodes"] = [packet["nodes"][0]]
    packet_path = tmp_path / "graph.yaml"
    packet_path.write_text(yaml.safe_dump(packet, sort_keys=False), encoding="utf-8")
    before = packet_path.read_bytes()
    assert main(["graph", "status", "--repo", str(repo), "--packet", str(packet_path), "--as-of", AS_OF, "--format", "json"]) == 0
    projection = json.loads(capsys.readouterr().out)
    assert projection["disposition"] == "complete"
    assert packet_path.read_bytes() == before
    status_path = tmp_path / "status.json"
    status_path.write_text(json.dumps(projection), encoding="utf-8")
    status_before = status_path.read_bytes()
    assert main(["graph", "verify", "--packet", str(status_path)]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert status_path.read_bytes() == status_before


def test_file_digest_evidence_reports_stale_without_echoing_content(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    packet = graph_packet()
    packet["nodes"] = [
        {
            "id": "digest",
            "kind": "inspection",
            "summary": "Verify the artifact digest",
            "completion": [{"type": "file-sha256", "path": "docs/work.md", "sha256": "0" * 64}],
        }
    ]
    evidence = collect_graph_evidence(packet, repo, as_of=AS_OF)
    result = evidence["nodes"]["digest"][0]
    assert result["status"] == "stale"
    assert result["details"]["observed_sha256"] == hashlib.sha256(
        (repo / "docs" / "work.md").read_bytes()
    ).hexdigest()
    assert "content" not in result
    assert set(result["details"]) == {"observed_sha256"}


def test_validation_evidence_requires_exact_current_fingerprint(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    cache = repo / ".pytest_cache" / "validation-results.json"
    cache.parent.mkdir()
    cache.write_text(
        json.dumps(
            {
                "version": 1,
                "full": {
                    "fingerprint": "f" * 64,
                    "completed_at": AS_OF,
                    "timings_seconds": {},
                },
            }
        ),
        encoding="utf-8",
    )
    before = cache.read_bytes()
    monkeypatch.setattr("anyang_loop.validation_evidence.existing_validation_python", lambda *args, **kwargs: Path(sys.executable))
    monkeypatch.setattr("anyang_loop.validation_evidence.repository_fingerprint", lambda *args, **kwargs: "f" * 64)
    assert read_full_validation_evidence(repo)["status"] == "passed"
    monkeypatch.setattr("anyang_loop.validation_evidence.repository_fingerprint", lambda *args, **kwargs: "e" * 64)
    assert read_full_validation_evidence(repo)["status"] == "stale"
    assert cache.read_bytes() == before


def test_council_evidence_is_tenant_isolated_and_database_bytes_do_not_change(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    database = tmp_path / "council.db"
    connection = connect(database, create_parent=True)
    migrate(connection, AS_OF)
    init_tenant(
        connection,
        slug="synthetic",
        name="Synthetic Council",
        policy_profile="test-only",
        retainer_cents=0,
        contractor_budget_cents=0,
        tool_budget_cents=0,
        timestamp=AS_OF,
    )
    create_council_transaction(
        connection,
        "synthetic",
        {
            "id": "TX-GRAPH",
            "title": "Synthetic graph evidence",
            "council_scope": "Internal test",
            "decision_class": "Class 1",
            "pilot_category": "test",
            "source_ref": "fictional://graph/source",
            "created_at": AS_OF,
        },
    )
    connection.close()
    packet = graph_packet()
    packet["scope"]["tenant"] = "synthetic"
    packet["nodes"] = [
        {
            "id": "council",
            "kind": "inspection",
            "summary": "Verify Council projection",
            "completion": [
                {"type": "council-projection", "transaction_id": "TX-GRAPH", "current_state": "proposed"},
                {"type": "council-event-chain", "transaction_id": "TX-GRAPH"},
            ],
        }
    ]
    before = database.read_bytes()
    evidence = collect_graph_evidence(packet, repo, as_of=AS_OF, db_path=database)
    assert [item["status"] for item in evidence["nodes"]["council"]] == ["satisfied", "satisfied"]
    assert database.read_bytes() == before

    packet["scope"]["tenant"] = "another-tenant"
    isolated = collect_graph_evidence(packet, repo, as_of=AS_OF, db_path=database)
    assert [item["status"] for item in isolated["nodes"]["council"]] == ["held", "held"]
