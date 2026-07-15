from __future__ import annotations

import copy

import pytest
import yaml

from anyang_loop.epistemic_benchmark import EpistemicBenchmarkError, score_epistemic_benchmark
from anyang_loop.epistemic_state import load_epistemic_manifest
from anyang_loop.project_cli import main


CHECKS = {
    "controlling_claim": True,
    "state_and_scope": True,
    "upstream_support": True,
    "latest_transition_cause": True,
    "downstream_and_next_evidence": True,
}


def _responses():
    _, manifest = load_epistemic_manifest()
    return {
        "version": 1,
        "reviewed_at": "2026-07-15T12:00:00Z",
        "reviewer_alias": "reviewer-a",
        "overrides": 0,
        "surfaces": {
            surface_id: {
                "elapsed_seconds": 120,
                "retrieval_checks": dict(CHECKS),
                "predicted_dependencies": list(manifest["surfaces"][surface_id]["dependencies"]),
            }
            for surface_id in manifest["human_outcome_cohort"]
        },
    }


def _write(tmp_path, data, name="responses.yaml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_perfect_benchmark_scores_human_formula_but_keeps_baseline_pending(tmp_path):
    result = score_epistemic_benchmark(None, _write(tmp_path, _responses()))
    assert result["retrieval"] == {"correct": 60, "maximum": 60, "success": 1.0}
    assert result["revision_impact"]["micro_f1"] == 1.0
    assert result["human_burden"] == 0.0
    assert result["composite_entropy"] == 0.0
    assert result["relative_reduction"] is None
    assert result["acceptance"]["status"] == "pending-human-measurement"
    assert not result["acceptance"]["met"]
    assert result["ready_to_paste"]["human_measurement"] == {
        "retrieval_success": 1.0,
        "revision_impact_accuracy": 1.0,
        "review_minutes": 24.0,
        "false_positives": 0,
        "overrides": 0,
    }


def test_two_minute_boundary_and_micro_f1_penalize_late_missing_and_false_edges(tmp_path):
    responses = _responses()
    first = next(iter(responses["surfaces"]))
    responses["surfaces"][first]["elapsed_seconds"] = 120.01
    result = score_epistemic_benchmark(None, _write(tmp_path, responses, "late.yaml"))
    assert result["retrieval"]["correct"] == 55
    assert result["retrieval"]["success"] == 0.9167
    assert result["human_burden"] == 5.0

    inaccurate = _responses()
    for response in inaccurate["surfaces"].values():
        response["predicted_dependencies"] = []
    inaccurate["surfaces"][first]["predicted_dependencies"] = ["false-positive-claim"]
    result = score_epistemic_benchmark(None, _write(tmp_path, inaccurate, "inaccurate.yaml"))
    assert result["revision_impact"]["true_positive"] == 0
    assert result["revision_impact"]["false_positive"] == 1
    assert result["revision_impact"]["false_negative"] > 0
    assert result["revision_impact"]["micro_f1"] == 0.0
    assert result["human_burden"] == 40.0


def test_benchmark_rejects_non_cohort_or_ambiguous_responses(tmp_path):
    responses = _responses()
    responses["surfaces"].pop(next(iter(responses["surfaces"])))
    with pytest.raises(EpistemicBenchmarkError, match="must match the fixed cohort"):
        score_epistemic_benchmark(None, _write(tmp_path, responses, "missing.yaml"))

    responses = _responses()
    first = next(iter(responses["surfaces"]))
    responses["surfaces"][first]["predicted_dependencies"] *= 2
    with pytest.raises(EpistemicBenchmarkError, match="must be unique"):
        score_epistemic_benchmark(None, _write(tmp_path, responses, "duplicate.yaml"))


def test_project_cli_emits_json_without_rewriting_manifest(tmp_path, capsys):
    manifest_path, manifest_before = load_epistemic_manifest()
    response_path = _write(tmp_path, _responses())
    assert main([
        "epistemic-benchmark",
        "score",
        "--manifest",
        str(manifest_path),
        "--responses",
        str(response_path),
        "--format",
        "json",
    ]) == 0
    output = capsys.readouterr().out
    assert '"recording_boundary"' in output
    _, manifest_after = load_epistemic_manifest(manifest_path)
    assert manifest_after == copy.deepcopy(manifest_before)
