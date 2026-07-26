from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from anyang_loop.cross_repo_audit import CrossRepoAuditError, collect_cross_repo_audit

from cadence_helpers import make_git_repo, run, write


def build_repo(root: Path) -> str:
    make_git_repo(root)
    write(root / "README.md", "# Fixture\n\n[missing](missing.md)\n")
    write(root / "controls.json", '{"items": [1,]}\n')
    write(root / "settings.yaml", "items:\n  - valid\n")
    write(root / "settings.toml", 'mode = "valid"\n')
    write(root / "docs" / "local.md", "Source: C:/dev/private/source.md\n")
    write(root / "sources" / "a.md", "# A\n")
    write(root / "sources" / "b.md", "# B\n")
    run(root, "git", "add", ".")
    run(root, "git", "commit", "-m", "fixture")
    return run(root, "git", "rev-parse", "HEAD")


def config(
    path: Path,
    head: str,
    command: list[str] | None = None,
    depends_on: list[str] | None = None,
) -> Path:
    value = {
        "schema_version": 1,
        "audit_id": "fixture-audit",
        "expected_head": head,
        "timeout_seconds": 10,
        "controlling_paths": ["README.md", "missing-control.md"],
        "commands": [
            {
                "id": "native",
                "argv": command or [sys.executable, "-c", "print('ok')"],
                "depends_on": depends_on or [],
            }
        ],
        "sample_groups": [{"id": "sources", "globs": ["sources/*.md"], "count": 2}],
    }
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_collector_reports_objective_diagnostics_and_preserves_target(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    output = tmp_path / "receipt.json"

    receipt = collect_cross_repo_audit(repo, config(tmp_path / "config.json", head), output)

    categories = {item["category"] for item in receipt["diagnostics"]}
    assert {"invalid-json", "broken-relative-link", "machine-local-path", "declared-control-gap"} <= categories
    assert receipt["mutation_proof"]["git_status_unchanged"] is True
    assert receipt["mutation_proof"]["tracked_content_unchanged"] is True
    assert receipt["collector_boundary"]["assigns_semantic_severity"] is False
    assert receipt["collector_boundary"]["commands_execute_in_target_checkout"] is False
    assert receipt["collector_boundary"]["commands_execute_in_disposable_snapshot"] is True
    assert receipt["adapter"]["execution_surface"] == "disposable-git-archive"
    assert receipt["adapter"]["timeout_seconds"] == 10
    assert receipt["collector"]["version"]
    assert len(receipt["collector"]["source_sha256"]) == 64
    assert all(item["semantic_severity"] is None for item in receipt["diagnostics"])
    assert run(repo, "git", "status", "--short") == ""


def test_sampling_and_stable_fingerprint_are_deterministic(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    cfg = config(tmp_path / "config.json", head)

    first = collect_cross_repo_audit(repo, cfg, tmp_path / "first.json")
    second = collect_cross_repo_audit(repo, cfg, tmp_path / "second.json")

    assert first["samples"] == second["samples"]
    assert first["deterministic_fingerprint"] == second["deterministic_fingerprint"]


def test_invalid_controlling_json_collapses_dependent_command_failures(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        "import json; json.load(open('controls.json', encoding='utf-8'))",
    ]

    receipt = collect_cross_repo_audit(
        repo,
        config(tmp_path / "config.json", head, command, ["controls.json"]),
        tmp_path / "receipt.json",
    )

    groups = receipt["root_cause_groups"]
    assert len(groups) == 1
    assert groups[0]["root_cause_id"] == "invalid-json:controls.json"
    assert groups[0]["affected_command_ids"] == ["native"]
    assert groups[0]["collapsed_component_count"] == 2
    assert groups[0]["independent_finding_count"] == 1


def test_root_cause_requires_path_specific_command_evidence(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    write(repo / "other.json", '{"other": [1,]}\n')
    run(repo, "git", "add", ".")
    run(repo, "git", "commit", "-m", "second invalid json")
    head = run(repo, "git", "rev-parse", "HEAD")
    command = [
        sys.executable,
        "-c",
        "import json; json.load(open('controls.json', encoding='utf-8'))",
    ]

    receipt = collect_cross_repo_audit(
        repo,
        config(tmp_path / "config.json", head, command, ["controls.json"]),
        tmp_path / "receipt.json",
    )

    groups = {item["root_cause_id"]: item for item in receipt["root_cause_groups"]}
    assert groups["invalid-json:controls.json"]["affected_command_ids"] == ["native"]
    assert groups["invalid-json:other.json"]["affected_command_ids"] == []


def test_yaml_and_toml_are_structurally_validated(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    write(repo / "settings.yaml", "items:\n  - valid\n bad-indent: true\n")
    write(repo / "settings.toml", 'mode = "unterminated\n')
    run(repo, "git", "add", ".")
    run(repo, "git", "commit", "-m", "invalid structured files")
    head = run(repo, "git", "rev-parse", "HEAD")

    receipt = collect_cross_repo_audit(
        repo,
        config(tmp_path / "config.json", head),
        tmp_path / "receipt.json",
    )

    categories = {item["category"] for item in receipt["diagnostics"]}
    assert {"invalid-yaml", "invalid-toml"} <= categories


def test_nonzero_missing_and_timeout_commands_are_receipted(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    cases = [
        ("nonzero", [sys.executable, "-c", "raise SystemExit(7)"]),
        ("missing", ["definitely-not-a-command"]),
        ("timeout", [sys.executable, "-c", "import time; time.sleep(2)"]),
    ]
    for name, command in cases:
        cfg = json.loads(config(tmp_path / f"{name}.json", head, command).read_text(encoding="utf-8"))
        cfg["timeout_seconds"] = 1
        (tmp_path / f"{name}.json").write_text(json.dumps(cfg), encoding="utf-8")
        receipt = collect_cross_repo_audit(repo, tmp_path / f"{name}.json", tmp_path / f"{name}-receipt.json")
        result = receipt["commands"][0]
        assert result["exit_code"] != 0 or result["timed_out"] or result["stderr"]


def test_collector_fails_closed_on_head_mismatch_output_inside_target_and_mutating_token(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    cfg = config(tmp_path / "config.json", "0" * 40)
    with pytest.raises(CrossRepoAuditError, match="sealed commit"):
        collect_cross_repo_audit(repo, cfg, tmp_path / "receipt.json")

    cfg = config(tmp_path / "inside-config.json", head)
    with pytest.raises(CrossRepoAuditError, match="outside"):
        collect_cross_repo_audit(repo, cfg, repo / "receipt.json")

    bad = json.loads(cfg.read_text(encoding="utf-8"))
    bad["commands"][0]["argv"] = ["tool", "--write"]
    cfg.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(CrossRepoAuditError, match="prohibited"):
        collect_cross_repo_audit(repo, cfg, tmp_path / "receipt.json")


def test_mutating_command_changes_only_disposable_snapshot(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        "from pathlib import Path; Path('README.md').write_text('changed', encoding='utf-8')",
    ]
    cfg = config(tmp_path / "config.json", head, command)
    output = tmp_path / "receipt.json"

    receipt = collect_cross_repo_audit(repo, cfg, output)

    assert output.exists()
    assert (repo / "README.md").read_text(encoding="utf-8").startswith("# Fixture")
    assert run(repo, "git", "status", "--short") == ""
    assert receipt["collector_boundary"]["commands_execute_in_disposable_snapshot"] is True


def test_command_output_is_minimized_before_receipting(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        "print('to' + 'ken=' + 'gh' + 'p_' + '123456789012345678901234567890 C:' + '/Users/example/private.txt')",
    ]

    receipt = collect_cross_repo_audit(
        repo,
        config(tmp_path / "config.json", head, command),
        tmp_path / "receipt.json",
    )

    result = receipt["commands"][0]
    assert "ghp_" not in result["stdout"]
    assert "C:/Users/" not in result["stdout"]
    assert result["stdout_redaction_count"] == 2
    assert result["stdout"].count("[REDACTED]") == 2
