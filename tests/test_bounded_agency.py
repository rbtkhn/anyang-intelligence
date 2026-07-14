from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from anyang_loop.bounded_agency import validate_agency_manifest
from anyang_loop.phase_preflight import TRANSCRIPT_PHASE, render_preflight_json, run_preflight, verify_transition
from anyang_loop.project_cli import main
from anyang_loop.repo_snapshot import collect_repo_snapshot
from cadence_helpers import make_git_repo, run, write


def write_ready_manifest(root: Path) -> Path:
    source = root / "operator-input" / "episode.txt"
    write(source, "A bounded transcript source.")
    manifest = root / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    write(
        manifest,
        json.dumps(
            {
                "transcripts": [
                    {
                        "lane": "moonshots",
                        "title": "Bounded Episode",
                        "slug": "bounded-episode",
                        "date_captured": "2026-07-13",
                        "source_ref": "https://example.com/bounded",
                        "rights_status": "internal-commit-approved",
                        "capture_method": "manual export",
                        "local_input_path": source.as_posix(),
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    return manifest


def committed_repo(tmp_path: Path) -> tuple[Path, Path]:
    make_git_repo(tmp_path)
    manifest = write_ready_manifest(tmp_path)
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "transcript fixture")
    return tmp_path, manifest


def test_repository_agency_contract_validates():
    assert validate_agency_manifest() == []
    assert main(["validate-agency"]) == 0


def test_static_contract_rejects_unknown_capability_path_traversal_and_incomplete_recovery(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "bounded-agency.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    phase = data["phases"][TRANSCRIPT_PHASE]
    phase["capability"] = "unknown capability"
    phase["may_write"].append("../escape/**")
    phase["may_write"].append("C:/unsafe/**")
    phase["must_not_write_without_explicit_authorization"].append("C:/unsafe/**")
    phase["recovery"] = {"method": "Recover."}
    path = tmp_path / "bounded-agency.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    codes = {item.code for item in validate_agency_manifest(path)}

    assert "agency-capability-unknown" in codes
    assert "agency-path-invalid" in codes
    assert "agency-write-protected-overlap" in codes
    assert "agency-recovery-incomplete" in codes


def test_static_contract_rejects_unknown_artifact_invariant_and_windows_case_collision(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "bounded-agency.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    phase = data["phases"][TRANSCRIPT_PHASE]
    phase["canonical_inputs"].append("unknown-artifact")
    phase["invariants"].append("unknown-invariant")
    phase["may_write"].extend(["Case/Path/**", "case/path/**"])
    data["phases"]["invented-phase"] = dict(phase)
    path = tmp_path / "bounded-agency.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    codes = {item.code for item in validate_agency_manifest(path)}

    assert "agency-artifact-unknown" in codes
    assert "agency-invariant-unknown" in codes
    assert "agency-path-case-collision" in codes
    assert "agency-phase-unknown" in codes


def test_preflight_reconstructs_clean_live_state_and_json(tmp_path: Path):
    root, manifest = committed_repo(tmp_path)

    preflight = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=root)
    payload = json.loads(render_preflight_json(preflight))

    assert preflight.exit_code == 0
    assert payload["status"] == "ready"
    assert payload["repository"]["worktree_state"] == "clean"
    assert payload["plan"]["create"] == [
        "projects/singularity-science/archive/moonshots/transcripts/2026-07-13-captured-bounded-episode.md"
    ]
    assert payload["plan"]["modify"] == ["projects/singularity-science/archive/transcript-import-ledger.md"]
    assert payload["enforcement"]["authority"] == "preflight-never-grants-authority"


def test_preflight_accepts_only_manifest_referenced_external_source(tmp_path: Path):
    make_git_repo(tmp_path)
    external = tmp_path.parent / f"{tmp_path.name}-external-source.txt"
    external.write_text("Explicit external source.", encoding="utf-8")
    manifest = write_ready_manifest(tmp_path)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["transcripts"][0]["local_input_path"] = external.as_posix()
    manifest.write_text(json.dumps(data), encoding="utf-8")
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "external source fixture")

    preflight = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=tmp_path)

    assert preflight.exit_code == 0
    assert f"external:{external.as_posix()}" in preflight.authoritative_inputs


def test_output_symlink_escape_blocks_when_platform_supports_symlinks(tmp_path: Path):
    make_git_repo(tmp_path)
    manifest = write_ready_manifest(tmp_path)
    archive = manifest.parent
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    lane = archive / "moonshots"
    try:
        lane.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("Directory symlinks require platform permission.")
    run(tmp_path, "git", "add", str(manifest))
    run(tmp_path, "git", "commit", "-m", "symlink fixture")

    preflight = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=tmp_path)

    assert preflight.exit_code == 1
    assert any(item["code"] == "path-escape" for item in preflight.blockers)


def test_unrelated_dirty_warns_but_dirty_planned_ledger_blocks(tmp_path: Path):
    root, manifest = committed_repo(tmp_path)
    write(root / "notes.txt", "unrelated")

    warning = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=root)

    assert warning.exit_code == 0
    assert any(item["code"] == "unrelated-dirty-worktree" for item in warning.warnings)

    write(manifest.parent / "transcript-import-ledger.md", "dirty ledger")
    blocked = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=root)

    assert blocked.exit_code == 1
    assert any(item["code"] == "dirty-permitted-write-surface" for item in blocked.blockers)


def test_valid_request_outside_write_envelope_requires_operator_authorization(tmp_path: Path):
    root, manifest = committed_repo(tmp_path)
    source = Path(__file__).resolve().parents[1] / "bounded-agency.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    phase = data["phases"][TRANSCRIPT_PHASE]
    phase["may_write"] = ["projects/singularity-science/archive/transcript-import-ledger.md"]
    contract = tmp_path / "authority.yaml"
    contract.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    preflight = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=root, contract_path=contract)

    assert preflight.exit_code == 2
    assert any(item["code"] == "write-outside-envelope" for item in preflight.authorization_required)


def test_invalid_slug_path_escape_blocks_without_writes(tmp_path: Path):
    root, manifest = committed_repo(tmp_path)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["transcripts"][0]["slug"] = "../escape"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    run(root, "git", "add", str(manifest))
    run(root, "git", "commit", "-m", "invalid manifest fixture")

    preflight = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=root)

    assert preflight.exit_code == 1
    assert any(item["code"] == "invalid-manifest" for item in preflight.blockers)
    assert not (root / "projects" / "singularity-science" / "archive" / "escape.md").exists()


def test_transition_reports_unexpected_delta(tmp_path: Path):
    root, _ = committed_repo(tmp_path)
    before = collect_repo_snapshot(root)
    write(root / "expected.md", "expected")
    write(root / "unexpected.md", "unexpected")
    after = collect_repo_snapshot(root)

    transition = verify_transition(before, after, ("expected.md",))

    assert transition["status"] == "fail"
    assert transition["unexpected_delta"] == ["unexpected.md"]
