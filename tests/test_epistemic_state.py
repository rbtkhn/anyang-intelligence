from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml

from anyang_loop.epistemic_state import epistemic_report, load_epistemic_manifest, validate_epistemic_manifest
from anyang_loop.project_cli import main


def test_repository_epistemic_manifest_is_valid_and_structurally_deterministic():
    diagnostics = validate_epistemic_manifest()
    report = epistemic_report()
    assert diagnostics == []
    assert report["structural"] == {
        "points": 0,
        "maximum": 186,
        "entropy_rate": 0.0,
        "baseline_rate": 100.0,
        "relative_reduction": 1.0,
    }
    assert report["acceptance"]["critical_gap_count"] == 0
    assert report["acceptance"]["status"] == "pending-human-measurement"
    assert not report["acceptance"]["met"]
    assert report["human_measurement_check"] == {
        "status": "pending",
        "visibility": "ci-report",
        "blocking": False,
        "required_for_composite_acceptance": True,
        "message": "Human outcomes are not recorded; composite acceptance remains pending.",
    }


def test_ci_surfaces_pending_human_measurement_without_blocking(capsys):
    assert main(["epistemic-report"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["human_measurement_check"]["status"] == "pending"
    assert output["human_measurement_check"]["blocking"] is False
    workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "python-version: ['3.10', '3.12', '3.13']" in workflow
    assert "run: anyang-project epistemic-report" in workflow


def test_human_burden_and_composite_acceptance_use_declared_formula(tmp_path):
    _, manifest = load_epistemic_manifest()
    candidate = copy.deepcopy(manifest)
    candidate["baseline"]["composite_entropy"] = 100.0
    path = tmp_path / "epistemic-state.yaml"
    path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
    # The copied paths remain relative to the repository manifest, so use the real
    # manifest for path validation and the copied one only for metric calculation.
    report = epistemic_report(path, retrieval_success=0.75, revision_impact_accuracy=0.50)
    assert report["human"]["burden"] == 35.0
    assert report["composite_entropy"] == 7.0
    assert report["relative_reduction"] == 0.93
    # Missing copied surface files are critical, proving acceptance cannot be
    # manufactured by favorable human inputs alone.
    assert not report["acceptance"]["met"]


def test_critical_gaps_and_applicable_denominator_are_detected(tmp_path):
    _, manifest = load_epistemic_manifest()
    candidate = copy.deepcopy(manifest)
    candidate["surfaces"] = {
        "broken-publication": {
            "path": "missing.md",
            "kind": "publication",
            "criticality": "critical",
            "claim_id": "",
            "epistemic_state": "unresolved",
            "scope": "",
            "provenance": {},
            "dependencies": [],
            "as_of": "",
            "review_trigger": "",
            "transition": {},
            "corroboration_asserted": True,
            "source_independence": "unknown",
            "downstream_repetition_as_evidence": True,
            "open_impacts": ["stale"],
        }
    }
    candidate["human_outcome_cohort"] = ["broken-publication"]
    path = tmp_path / "broken.yaml"
    path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
    report = epistemic_report(path)
    codes = {item["code"] for item in report["diagnostics"]}
    assert {
        "epistemic-surface-missing",
        "source-version-binding-missing",
        "approval-binding-missing",
        "critical-impact-open",
        "synthetic-corroboration",
    } <= codes
    assert report["structural"]["points"] == 20
    assert report["structural"]["maximum"] == 20
    assert report["acceptance"]["critical_gap_count"] > 0


def test_human_measurement_check_contract_is_required(tmp_path):
    _, manifest = load_epistemic_manifest()
    candidate = copy.deepcopy(manifest)
    candidate["human_measurement"].pop("check")
    path = tmp_path / "missing-human-check.yaml"
    path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
    codes = {item.code for item in validate_epistemic_manifest(path)}
    assert "human-measurement-check-invalid" in codes
