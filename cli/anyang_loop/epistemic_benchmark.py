from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .epistemic_state import epistemic_report, load_epistemic_manifest, validate_epistemic_manifest


RETRIEVAL_CHECKS = (
    "controlling_claim",
    "state_and_scope",
    "upstream_support",
    "latest_transition_cause",
    "downstream_and_next_evidence",
)
BENCHMARK_VERSION = 1
TIME_LIMIT_SECONDS = 120.0


class EpistemicBenchmarkError(ValueError):
    pass


def score_epistemic_benchmark(
    manifest_path: str | Path | None,
    responses_path: str | Path,
) -> dict[str, Any]:
    resolved_manifest, manifest = load_epistemic_manifest(manifest_path)
    diagnostics = validate_epistemic_manifest(resolved_manifest)
    if diagnostics:
        codes = ", ".join(sorted({item.code for item in diagnostics}))
        raise EpistemicBenchmarkError(f"Benchmark requires a valid epistemic manifest; diagnostics: {codes}")
    responses_target = Path(responses_path).resolve()
    try:
        responses = yaml.safe_load(responses_target.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise EpistemicBenchmarkError(f"Unable to load benchmark responses: {exc}") from exc
    if not isinstance(responses, dict) or responses.get("version") != BENCHMARK_VERSION:
        raise EpistemicBenchmarkError(f"Benchmark responses require version: {BENCHMARK_VERSION}")
    if not responses.get("reviewed_at") or not responses.get("reviewer_alias"):
        raise EpistemicBenchmarkError("Benchmark responses require reviewed_at and a sanitized reviewer_alias")
    override_count = responses.get("overrides", 0)
    if not isinstance(override_count, int) or override_count < 0:
        raise EpistemicBenchmarkError("Benchmark overrides must be a non-negative integer")
    cohort = manifest.get("human_outcome_cohort", [])
    surfaces = manifest.get("surfaces", {})
    if len(cohort) != 12 or len(set(cohort)) != 12:
        raise EpistemicBenchmarkError("Benchmark requires exactly twelve unique manifest cohort surfaces")
    submitted = responses.get("surfaces")
    if not isinstance(submitted, dict):
        raise EpistemicBenchmarkError("Benchmark responses require a surfaces mapping")
    missing = [surface_id for surface_id in cohort if surface_id not in submitted]
    extra = [surface_id for surface_id in submitted if surface_id not in cohort]
    if missing or extra:
        raise EpistemicBenchmarkError(
            f"Benchmark responses must match the fixed cohort; missing={missing or []}, extra={extra or []}"
        )

    retrieval_correct = 0
    retrieval_maximum = len(cohort) * len(RETRIEVAL_CHECKS)
    true_positive = false_positive = false_negative = 0
    total_seconds = 0.0
    surface_results = []
    for surface_id in cohort:
        response = submitted[surface_id]
        if not isinstance(response, dict):
            raise EpistemicBenchmarkError(f"Surface response must be a mapping: {surface_id}")
        elapsed = response.get("elapsed_seconds")
        if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
            raise EpistemicBenchmarkError(f"Surface {surface_id} requires non-negative elapsed_seconds")
        total_seconds += float(elapsed)
        checks = response.get("retrieval_checks")
        if not isinstance(checks, dict) or set(checks) != set(RETRIEVAL_CHECKS):
            raise EpistemicBenchmarkError(
                f"Surface {surface_id} requires exactly these retrieval checks: {', '.join(RETRIEVAL_CHECKS)}"
            )
        if any(not isinstance(checks[name], bool) for name in RETRIEVAL_CHECKS):
            raise EpistemicBenchmarkError(f"Surface {surface_id} retrieval checks must be boolean")
        within_limit = float(elapsed) <= TIME_LIMIT_SECONDS
        surface_retrieval = sum(bool(checks[name]) for name in RETRIEVAL_CHECKS) if within_limit else 0
        retrieval_correct += surface_retrieval
        predicted_values = response.get("predicted_dependencies")
        if not isinstance(predicted_values, list) or any(not isinstance(value, str) for value in predicted_values):
            raise EpistemicBenchmarkError(f"Surface {surface_id} predicted_dependencies must be a list of claim IDs")
        if len(predicted_values) != len(set(predicted_values)):
            raise EpistemicBenchmarkError(f"Surface {surface_id} predicted_dependencies must be unique")
        predicted = set(predicted_values)
        expected = set(surfaces[surface_id].get("dependencies", []))
        surface_tp = len(predicted & expected)
        surface_fp = len(predicted - expected)
        surface_fn = len(expected - predicted)
        true_positive += surface_tp
        false_positive += surface_fp
        false_negative += surface_fn
        surface_results.append(
            {
                "id": surface_id,
                "elapsed_seconds": float(elapsed),
                "within_time_limit": within_limit,
                "retrieval_correct": surface_retrieval,
                "retrieval_maximum": len(RETRIEVAL_CHECKS),
                "expected_dependencies": sorted(expected),
                "predicted_dependencies": sorted(predicted),
                "true_positive": surface_tp,
                "false_positive": surface_fp,
                "false_negative": surface_fn,
            }
        )
    retrieval_success = retrieval_correct / retrieval_maximum if retrieval_maximum else 0.0
    f1_denominator = 2 * true_positive + false_positive + false_negative
    revision_accuracy = (2 * true_positive / f1_denominator) if f1_denominator else 1.0
    report = epistemic_report(
        resolved_manifest,
        retrieval_success=retrieval_success,
        revision_impact_accuracy=revision_accuracy,
    )
    review_minutes = round(total_seconds / 60.0, 2)
    ready_to_paste = {
        "retrieval_success": round(retrieval_success, 4),
        "revision_impact_accuracy": round(revision_accuracy, 4),
        "review_minutes": review_minutes,
        "false_positives": false_positive,
        "overrides": override_count,
    }
    return {
        "version": BENCHMARK_VERSION,
        "manifest": str(resolved_manifest),
        "responses": str(responses_target),
        "reviewed_at": responses["reviewed_at"],
        "reviewer_alias": responses["reviewer_alias"],
        "cohort_size": len(cohort),
        "time_limit_seconds": TIME_LIMIT_SECONDS,
        "retrieval": {
            "correct": retrieval_correct,
            "maximum": retrieval_maximum,
            "success": round(retrieval_success, 4),
        },
        "revision_impact": {
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "micro_f1": round(revision_accuracy, 4),
        },
        "human_burden": report["human"]["burden"],
        "composite_entropy": report["composite_entropy"],
        "relative_reduction": report["relative_reduction"],
        "acceptance": report["acceptance"],
        "ready_to_paste": {"human_measurement": ready_to_paste},
        "surfaces": surface_results,
        "recording_boundary": "Scoring is read-only; a human must review and deliberately land any aggregate measurement.",
    }


def render_epistemic_benchmark_markdown(result: dict[str, Any]) -> str:
    acceptance = result["acceptance"]
    lines = [
        "# Epistemic Human-Outcome Benchmark",
        "",
        f"Reviewed: {result['reviewed_at']}",
        f"Reviewer alias: `{result['reviewer_alias']}`",
        f"Cohort: {result['cohort_size']} surfaces",
        "",
        "## Results",
        f"- Retrieval success: {result['retrieval']['success']:.4f} ({result['retrieval']['correct']} / {result['retrieval']['maximum']})",
        f"- Revision-impact micro-F1: {result['revision_impact']['micro_f1']:.4f}",
        f"- Human burden: {result['human_burden']}",
        f"- Composite entropy: {result['composite_entropy']}",
        f"- Relative reduction: {result['relative_reduction'] if result['relative_reduction'] is not None else 'pending comparable baseline'}",
        f"- Critical gaps: {acceptance['critical_gap_count']}",
        f"- Acceptance: {'met' if acceptance['met'] else acceptance['status']}",
        "",
        "## Ready-To-Paste Measurement",
        "```yaml",
        yaml.safe_dump(result["ready_to_paste"], sort_keys=False).rstrip(),
        "```",
        "",
        "## Recording Boundary",
        f"- {result['recording_boundary']}",
        "",
    ]
    return "\n".join(lines)
