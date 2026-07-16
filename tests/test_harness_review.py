from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from anyang_loop.harness_review import (
    HarnessReviewError,
    SEMANTIC_LIMIT,
    _included,
    _metadata,
    _portable_path,
    record_decisions,
    render_harness,
    scan_harness,
)
from anyang_loop.project_cli import main

from cadence_helpers import make_git_repo, run, write


def build_repo(root: Path) -> None:
    make_git_repo(root)
    write(root / ".gitignore", "generated-reviews/\n")
    write(root / "README.md", "# Fixture harness\n")
    write(root / "pyproject.toml", "[project]\nname='fixture'\n")
    write(root / "bounded-agency.yaml", "version: 1\n")
    write(
        root / "skills" / "fixture-skill" / "SKILL.md",
        "---\nname: fixture-skill\ndescription: Use for fixture work.\n---\n\n# Fixture\n",
    )
    write(
        root / "skills" / "fixture-skill" / "agents" / "openai.yaml",
        'interface:\n  display_name: "Fixture Skill"\npolicy:\n  allow_implicit_invocation: false\n',
    )
    write(root / "projects" / "customer" / "README.md", "# Customer setup\n")
    write(root / "projects" / "customer" / "executive-os-install.md", "# Install\n")
    write(root / "projects" / "customer" / "archive" / "transcript.md", "private body\n")
    write(root / "tests" / "test_fixture.py", "def test_fixture():\n    assert True\n")
    write(root / ".github" / "workflows" / "validate.yml", "name: validate\n")
    run(root, "git", "add", ".")
    run(root, "git", "commit", "-m", "add harness fixture")


def load_packet(packet: Path) -> tuple[dict, dict]:
    evidence = packet / ".harness-review"
    scope = json.loads((evidence / "00-scope.json").read_text(encoding="utf-8"))
    inventory = json.loads((evidence / "01-inventory.json").read_text(encoding="utf-8"))
    return scope, inventory


def review_for(packet: Path, *, action: str = "ONE_HOME", proposal: str = "Consolidate the fixture route.") -> Path:
    scope, inventory = load_packet(packet)
    first = inventory["controls"][0]
    review = {
        "schema_version": 1,
        "scan_id": scope["scan_id"],
        "baseline_fingerprint": scope["baseline_fingerprint"],
        "run_context": {
            "surface": {"value": "codex", "evidence": "VERIFIED"},
            "model": {"value": "unknown", "evidence": "INACCESSIBLE"},
            "sandbox": {"value": "workspace-write", "evidence": "VERIFIED"},
            "approval_mode": {"value": "managed", "evidence": "VERIFIED"},
        },
        "summary": {
            "headline": "The fixture is governed but has one route to simplify.",
            "what_helps": ["Tracked controls have deterministic checks."],
            "what_gets_in_way": ["One route has unclear ownership."],
        },
        "decisions": [
            {
                "action": action,
                "control_ids": [first["control_id"]],
                "finding": "The first control owns a visible route.",
                "user_impact": "The operator may see overlapping guidance.",
                "proposal": proposal,
                "evidence_paths": [first["path"]],
                "risk": "A useful protection could be lost.",
                "approver": "repository-operator",
                "rollback": "Restore the reviewed Git baseline.",
                "protections": ["Preserve the original authority boundary."],
                "confidence": "high",
            }
        ],
        "unreviewed_control_ids": [item["control_id"] for item in inventory["controls"][1:]],
        "coverage_gaps": list(scope["coverage_gaps"]),
    }
    path = packet / ".harness-review" / "semantic-review.input.json"
    path.write_text(json.dumps(review), encoding="utf-8")
    return path


def test_scan_uses_tracked_allowlist_and_portable_metadata(tmp_path: Path):
    build_repo(tmp_path)
    write(tmp_path / "skills" / "untracked" / "SKILL.md", "untracked secret\n")

    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/run-one")
    scope, inventory = load_packet(packet)
    paths = {item["path"] for item in inventory["controls"]}

    assert "skills/fixture-skill/SKILL.md" in paths
    assert "skills/fixture-skill/agents/openai.yaml" in paths
    assert "projects/customer/README.md" in paths
    assert "projects/customer/archive/transcript.md" not in paths
    assert "skills/untracked/SKILL.md" not in paths
    assert all(not Path(path).is_absolute() for path in paths)
    assert all("content" not in item for item in inventory["controls"])
    assert scope["tracked_only"] is True
    assert any("untracked" in gap.lower() for gap in scope["coverage_gaps"])


def test_scan_semantic_selection_is_bounded_and_deterministic(tmp_path: Path):
    build_repo(tmp_path)
    for index in range(SEMANTIC_LIMIT + 8):
        write(tmp_path / "tests" / f"test_many_{index:02d}.py", f"def test_{index}():\n    assert True\n")
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "many controls")

    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/bounded")
    scope, inventory = load_packet(packet)

    assert scope["semantic_selected_count"] == SEMANTIC_LIMIT
    assert sum(item["semantic_selected"] for item in inventory["controls"]) == SEMANTIC_LIMIT


def test_render_escapes_hostile_text_and_keeps_paths_portable(tmp_path: Path):
    build_repo(tmp_path)
    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/render")
    review = review_for(packet, proposal="Consolidate <script>alert('x')</script> safely.")

    report = render_harness(packet, review)
    output = report.read_text(encoding="utf-8")

    assert "&lt;script&gt;" in output
    assert "<script>" not in output
    assert str(tmp_path) not in output
    assert (packet / ".harness-review" / "03-proposal-manifest.json").exists()
    assert run(tmp_path, "git", "status", "--short") == ""


def test_render_rejects_stale_or_incomplete_review(tmp_path: Path):
    build_repo(tmp_path)
    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/stale")
    review_path = review_for(packet)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["unreviewed_control_ids"] = []
    review_path.write_text(json.dumps(review), encoding="utf-8")
    with pytest.raises(HarnessReviewError, match="does not account"):
        render_harness(packet, review_path)

    review_for(packet)
    write(tmp_path / "README.md", "# Changed after scan\n")
    with pytest.raises(HarnessReviewError, match="changed after scan"):
        render_harness(packet, review_path)


def test_review_rejects_invented_ids_and_evidence_paths(tmp_path: Path):
    build_repo(tmp_path)
    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/invalid")
    review_path = review_for(packet)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["decisions"][0]["control_ids"] = ["ctl-invented"]
    review["decisions"][0]["evidence_paths"] = ["outside/private.txt"]
    review_path.write_text(json.dumps(review), encoding="utf-8")

    with pytest.raises(HarnessReviewError, match="outside the inventory"):
        render_harness(packet, review_path)


def test_decide_fails_closed_and_never_mutates_source(tmp_path: Path):
    build_repo(tmp_path)
    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/decide")
    render_harness(packet, review_for(packet))
    baseline = (tmp_path / "README.md").read_bytes()

    with pytest.raises(HarnessReviewError, match="Duplicate"):
        record_decisions(packet, [1, 1], [])
    with pytest.raises(HarnessReviewError, match="Unknown"):
        record_decisions(packet, [99], [])

    approval = record_decisions(packet, [1], [])
    result = json.loads(approval.read_text(encoding="utf-8"))
    assert result["items"][0]["decision"] == "APPROVED"
    assert (tmp_path / "README.md").read_bytes() == baseline
    assert run(tmp_path, "git", "status", "--short") == ""
    with pytest.raises(HarnessReviewError, match="overwrite"):
        record_decisions(packet, [], [1])


def test_cli_scan_render_and_decide(tmp_path: Path, capsys):
    build_repo(tmp_path)
    packet = tmp_path / "generated-reviews" / "ai-harness" / "cli"
    assert main(["harness", "scan", "--repo", str(tmp_path), "--output", str(packet)]) == 0
    review = review_for(packet)
    assert main(["harness", "render", "--packet", str(packet), "--review", str(review)]) == 0
    assert main(["harness", "decide", "--packet", str(packet), "--approve", "1"]) == 0
    output = capsys.readouterr().out
    assert "No source changes were applied" in output


def test_output_and_path_boundaries_fail_closed(tmp_path: Path):
    build_repo(tmp_path)
    with pytest.raises(HarnessReviewError, match="outside"):
        scan_harness(tmp_path, tmp_path / "outside")
    with pytest.raises(HarnessReviewError, match="Unsafe"):
        _portable_path("../escape")
    assert _included("projects/customer/README.md") is True
    assert _included("projects/customer/archive/README.md") is False


def test_skill_metadata_accepts_windows_line_endings():
    raw = b"---\r\nname: windows-skill\r\ndescription: Windows metadata.\r\n---\r\n# Skill\r\n"
    metadata = _metadata("skills/windows/SKILL.md", raw)
    assert metadata["label"] == "windows-skill"
    assert metadata["description"] == "Windows metadata."


def test_scan_does_not_follow_tracked_symlink_when_supported(tmp_path: Path):
    build_repo(tmp_path)
    link = tmp_path / "skills" / "linked" / "SKILL.md"
    link.parent.mkdir(parents=True)
    try:
        os.symlink(tmp_path / "README.md", link)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are not available in this environment")
    run(tmp_path, "git", "add", "skills/linked/SKILL.md")
    run(tmp_path, "git", "commit", "-m", "tracked symlink")

    packet = scan_harness(tmp_path, "generated-reviews/ai-harness/symlink")
    scope, inventory = load_packet(packet)
    assert "skills/linked/SKILL.md" not in {item["path"] for item in inventory["controls"]}
    assert any("symlink" in gap.lower() for gap in scope["coverage_gaps"])
