from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from anyang_loop.cross_repo_audit import (
    MAX_SUMMARY_EXAMPLE_CHARS,
    CrossRepoAuditError,
    _write_receipt_atomic,
    collect_cross_repo_audit,
)

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
    assert receipt["adapter"]["sample_match_semantics"] == "repository-rooted-segment-glob-v1"
    assert receipt["collector"]["version"]
    assert receipt["collector"]["version"] == "1.2.0"
    assert len(receipt["collector"]["source_sha256"]) == 64
    assert receipt["collection_status"] == "complete"
    assert receipt["commands"][0]["execution_status"] == "completed"
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


def test_sampling_is_repository_rooted_recursive_and_excludable(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    write(repo / "content" / "civilizations" / "ROME" / "MEM-primary.md", "# Primary\n")
    write(repo / ".skeleton" / "content" / "civilizations" / "ROME" / "MEM-derived.md", "# Derived\n")
    write(repo / ".skeleton" / "root.md", "# Root skeleton\n")
    write(repo / ".skeleton" / "deep" / "nested" / "node.md", "# Deep skeleton\n")
    write(repo / "sources" / "excluded.md", "# Excluded\n")
    run(repo, "git", "add", ".")
    run(repo, "git", "commit", "-m", "sampling shapes")
    head = run(repo, "git", "rev-parse", "HEAD")
    value = json.loads(config(tmp_path / "config.json", head).read_text(encoding="utf-8"))
    value["sample_groups"] = [
        {
            "id": "canonical",
            "globs": ["content/civilizations/*/MEM*.md"],
            "count": 1,
        },
        {
            "id": "skeleton",
            "globs": [".skeleton/**/*.md"],
            "count": 3,
        },
        {
            "id": "sources",
            "globs": ["sources/*.md"],
            "exclude_globs": ["sources/excluded.md"],
            "count": 2,
        },
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")
    samples = {item["id"]: item for item in receipt["samples"]}

    assert samples["canonical"]["selected"] == ["content/civilizations/ROME/MEM-primary.md"]
    assert samples["canonical"]["include_match_counts"] == {"content/civilizations/*/MEM*.md": 1}
    assert samples["skeleton"]["eligible"] == 3
    assert ".skeleton/root.md" in samples["skeleton"]["selected"]
    assert ".skeleton/deep/nested/node.md" in samples["skeleton"]["selected"]
    assert samples["sources"]["included_before_exclusions"] == 3
    assert samples["sources"]["excluded"] == 1
    assert "sources/excluded.md" not in samples["sources"]["selected"]


@pytest.mark.parametrize("pattern", ["/absolute/*.md", "../outside/*.md", "C:/private/*.md"])
def test_sampling_rejects_unsafe_globs(tmp_path: Path, pattern: str):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    value = json.loads(config(tmp_path / "config.json", head).read_text(encoding="utf-8"))
    value["sample_groups"][0]["globs"] = [pattern]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    with pytest.raises(CrossRepoAuditError, match="Unsafe sample glob"):
        collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")


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
        if name == "nonzero":
            assert result["execution_status"] == "completed"
            assert receipt["collection_status"] == "complete"
            assert not any("command completion" in gap for gap in receipt["coverage_gaps"])
        else:
            assert result["execution_status"] in {"launch_failed", "timed_out"}
            assert receipt["collection_status"] == "partial"
            assert any("command completion" in gap for gap in receipt["coverage_gaps"])


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
    assert result["stdout_capture"]["truncated"] is False
    assert result["stdout_sha256"] == result["stdout_complete_minimized_sha256"]


def test_long_output_preserves_head_tail_hashes_and_structured_summary(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        (
            "import sys;"
            "sys.stdout.write('OPENING\\r\\n' + ('middle-line\\r\\n' * 3000)"
            " + 'Validation failed: 918 issues ' + 'to' + 'ken='"
            " + 'gh' + 'p_123456789012345678901234567890\\r\\n')"
        ),
    ]
    value = json.loads(config(tmp_path / "config.json", head, command).read_text(encoding="utf-8"))
    value["commands"][0]["summary_rules"] = [
        {
            "id": "validation-result",
            "stream": "stdout",
            "line_prefix": "Validation failed:",
            "minimum_matches": 1,
            "max_examples": 2,
        }
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")
    result = receipt["commands"][0]
    summary = result["summaries"][0]

    assert result["stdout"].startswith("OPENING\n")
    assert "[truncated]" in result["stdout"]
    assert "Validation failed: 918 issues" in result["stdout"]
    assert "\r" not in result["stdout"]
    assert "ghp_" not in result["stdout"]
    assert result["stdout_capture"]["truncated"] is True
    assert result["stdout_capture"]["omitted_chars"] > 0
    assert result["stdout_sha256"] != result["stdout_complete_minimized_sha256"]
    assert summary["match_count"] == 1
    assert summary["coverage_complete"] is True
    assert summary["examples"][0]["line"].endswith("[REDACTED]")
    assert receipt["collection_status"] == "complete"


def test_missing_required_summary_marks_collection_partial(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    value = json.loads(config(tmp_path / "config.json", head).read_text(encoding="utf-8"))
    value["commands"][0]["summary_rules"] = [
        {
            "id": "required-total",
            "line_prefix": "Validation complete:",
            "minimum_matches": 1,
        }
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")

    assert receipt["commands"][0]["execution_status"] == "completed"
    assert receipt["commands"][0]["summary_coverage_complete"] is False
    assert receipt["collection_status"] == "partial"
    assert any("Required command summaries" in gap for gap in receipt["coverage_gaps"])


def test_summary_examples_are_individually_bounded_and_hashed(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        "print('SUMMARY: ' + ('x' * 50000))",
    ]
    value = json.loads(config(tmp_path / "config.json", head, command).read_text(encoding="utf-8"))
    value["commands"][0]["summary_rules"] = [
        {
            "id": "large-summary",
            "line_prefix": "SUMMARY:",
            "minimum_matches": 1,
        }
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")
    summary = receipt["commands"][0]["summaries"][0]
    example = summary["examples"][0]

    assert summary["match_count"] == 1
    assert summary["truncated_example_count"] == 1
    assert example["line_truncated"] is True
    assert len(example["line"]) <= MAX_SUMMARY_EXAMPLE_CHARS
    assert example["original_chars"] == 50009
    assert example["omitted_chars"] > 0
    assert len(example["complete_minimized_line_sha256"]) == 64


def test_optional_incomplete_sample_does_not_make_collection_partial(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    value = json.loads(config(tmp_path / "config.json", head).read_text(encoding="utf-8"))
    value["sample_groups"] = [
        {
            "id": "optional-missing",
            "globs": ["does-not-exist/**/*.md"],
            "count": 2,
            "required": False,
        }
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")

    assert receipt["samples"][0]["selection_complete"] is False
    assert receipt["collection_status"] == "complete"
    assert not any("Requested sample size" in gap for gap in receipt["coverage_gaps"])


def test_required_incomplete_sample_marks_collection_partial(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    value = json.loads(config(tmp_path / "config.json", head).read_text(encoding="utf-8"))
    value["sample_groups"] = [
        {
            "id": "required-missing",
            "globs": ["does-not-exist/**/*.md"],
            "count": 2,
        }
    ]
    (tmp_path / "config.json").write_text(json.dumps(value), encoding="utf-8")

    receipt = collect_cross_repo_audit(repo, tmp_path / "config.json", tmp_path / "receipt.json")

    assert receipt["samples"][0]["required"] is True
    assert receipt["collection_status"] == "partial"
    assert any("Requested sample size" in gap for gap in receipt["coverage_gaps"])


def test_root_cause_uses_complete_minimized_output_not_preview(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    command = [
        sys.executable,
        "-c",
        "print('a' * 12000); print('controls.json'); print('z' * 12000)",
    ]

    receipt = collect_cross_repo_audit(
        repo,
        config(tmp_path / "config.json", head, command, []),
        tmp_path / "receipt.json",
    )

    assert "controls.json" not in receipt["commands"][0]["stdout"]
    assert receipt["root_cause_groups"][0]["affected_command_ids"] == ["native"]


def test_receipt_atomic_promotion_preserves_existing_output(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    head = build_repo(repo)
    output = tmp_path / "receipt.json"
    output.write_text("existing\n", encoding="utf-8")

    with pytest.raises(CrossRepoAuditError, match="Refusing to overwrite"):
        collect_cross_repo_audit(repo, config(tmp_path / "config.json", head), output)

    assert output.read_text(encoding="utf-8") == "existing\n"
    assert not list(tmp_path.glob(".receipt.json.*.tmp"))

    with pytest.raises(CrossRepoAuditError, match="Refusing to overwrite"):
        _write_receipt_atomic(output, b"replacement\n")

    assert output.read_text(encoding="utf-8") == "existing\n"
    assert not list(tmp_path.glob(".receipt.json.*.tmp"))
