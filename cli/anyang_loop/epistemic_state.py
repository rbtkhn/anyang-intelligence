from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_MANIFEST = "epistemic-state.yaml"
EPISTEMIC_STATES = {
    "attributed",
    "interpreted",
    "contested",
    "supported",
    "disconfirmed",
    "unresolved",
    "adopted",
    "retired",
}
EXCLUDED_SEGMENTS = {"archive", "tenant-private", "migration-backups", "strategy_codex_probe"}


@dataclass(frozen=True)
class EpistemicDiagnostic:
    code: str
    path: Path
    message: str
    critical: bool = False


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_epistemic_manifest(path: str | Path | None = None) -> tuple[Path, dict[str, Any]]:
    manifest_path = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Epistemic manifest root must be a mapping")
    return manifest_path, data


def validate_epistemic_manifest(path: str | Path | None = None) -> list[EpistemicDiagnostic]:
    try:
        manifest_path, data = load_epistemic_manifest(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        target = Path(path) if path else repository_root() / DEFAULT_MANIFEST
        return [EpistemicDiagnostic("epistemic-manifest-invalid", target, str(exc), True)]
    root = manifest_path.parent
    diagnostics: list[EpistemicDiagnostic] = []
    governance = data.get("governance")
    if not isinstance(governance, dict) or not all(governance.get(key) for key in ("owner", "review_cadence", "enforcement")):
        diagnostics.append(EpistemicDiagnostic("epistemic-governance-incomplete", manifest_path, "Governance requires owner, review cadence, and enforcement mode."))
    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        return [EpistemicDiagnostic("epistemic-surfaces-empty", manifest_path, "Declare at least one governed surface.", True)]
    claim_ids = {
        str(surface.get("claim_id"))
        for surface in surfaces.values()
        if isinstance(surface, dict) and surface.get("claim_id")
    }
    for surface_id, surface in surfaces.items():
        if not isinstance(surface, dict):
            diagnostics.append(EpistemicDiagnostic("epistemic-surface-invalid", manifest_path, f"Surface {surface_id} must be a mapping.", True))
            continue
        relative = str(surface.get("path", "")).replace("\\", "/")
        target = (root / relative).resolve()
        if not relative or any(part in EXCLUDED_SEGMENTS for part in Path(relative).parts):
            diagnostics.append(EpistemicDiagnostic("epistemic-surface-excluded", target, f"Surface {surface_id} is missing or enters an excluded tree.", True))
        elif not target.is_file():
            diagnostics.append(EpistemicDiagnostic("epistemic-surface-missing", target, f"Surface {surface_id} does not exist.", True))
        _required(surface, surface_id, target, diagnostics)
        for dependency in surface.get("dependencies", []):
            if dependency not in claim_ids:
                diagnostics.append(EpistemicDiagnostic("dependency-unbound", target, f"Surface {surface_id} depends on unknown claim {dependency}.", True))
        state = surface.get("epistemic_state")
        if state not in EPISTEMIC_STATES:
            diagnostics.append(EpistemicDiagnostic("epistemic-state-invalid", target, f"Surface {surface_id} has invalid state: {state}", True))
        if surface.get("corroboration_asserted") and surface.get("source_independence") != "independent":
            diagnostics.append(EpistemicDiagnostic("independence-unproven", target, f"Surface {surface_id} asserts corroboration without independent sources.", True))
        if surface.get("downstream_repetition_as_evidence"):
            diagnostics.append(EpistemicDiagnostic("synthetic-corroboration", target, f"Surface {surface_id} credits downstream repetition as evidence.", True))
        criticality = surface.get("criticality")
        kind = surface.get("kind")
        if criticality == "critical" and state in {"disconfirmed", "unresolved", "retired"} and not surface.get("permitted_boundary"):
            diagnostics.append(EpistemicDiagnostic("critical-state-unbounded", target, f"Critical surface {surface_id} requires a permitted boundary for state {state}.", True))
        if kind in {"publication", "decision", "approval"}:
            if not surface.get("source_version"):
                diagnostics.append(EpistemicDiagnostic("source-version-binding-missing", target, f"Surface {surface_id} requires a source-version binding.", True))
            if not surface.get("approval_binding"):
                diagnostics.append(EpistemicDiagnostic("approval-binding-missing", target, f"Surface {surface_id} requires an approval binding.", True))
        for impact in surface.get("open_impacts", []):
            if criticality == "critical" and impact in {"review-required", "unresolved", "stale"}:
                diagnostics.append(EpistemicDiagnostic("critical-impact-open", target, f"Surface {surface_id} has an open critical impact: {impact}", True))
    cohort = data.get("human_outcome_cohort", [])
    if not isinstance(cohort, list) or len(cohort) != 12 or len(set(cohort)) != 12:
        diagnostics.append(EpistemicDiagnostic("human-cohort-invalid", manifest_path, "Human outcome cohort must contain exactly twelve unique surface IDs."))
    elif any(item not in surfaces for item in cohort):
        diagnostics.append(EpistemicDiagnostic("human-cohort-unknown", manifest_path, "Human outcome cohort references an unknown surface."))
    human = data.get("human_measurement")
    required_measurements = ("retrieval_success", "revision_impact_accuracy", "review_minutes", "false_positives", "overrides")
    if not isinstance(human, dict) or any(key not in human for key in required_measurements):
        diagnostics.append(EpistemicDiagnostic("human-measurement-contract-incomplete", manifest_path, "Human measurement must declare every aggregate field, even while values remain pending."))
    else:
        check = human.get("check")
        if not isinstance(check, dict) or check != {
            "visibility": "ci-report",
            "blocking": False,
            "required_for_composite_acceptance": True,
        }:
            diagnostics.append(EpistemicDiagnostic("human-measurement-check-invalid", manifest_path, "Human measurement check must remain visible in CI, nonblocking while pending, and required for composite acceptance."))
    return diagnostics


def epistemic_report(
    path: str | Path | None = None,
    *,
    retrieval_success: float | None = None,
    revision_impact_accuracy: float | None = None,
) -> dict[str, Any]:
    manifest_path, data = load_epistemic_manifest(path)
    diagnostics = validate_epistemic_manifest(manifest_path)
    points = maximum = 0
    per_surface: list[dict[str, Any]] = []
    for surface_id, surface in data.get("surfaces", {}).items():
        result = _surface_entropy(surface_id, surface)
        points += result["points"]
        maximum += result["maximum"]
        per_surface.append(result)
    structural_rate = round(100.0 * points / maximum, 2) if maximum else 0.0
    human = data.get("human_measurement", {})
    human_check = human.get("check", {}) if isinstance(human, dict) else {}
    retrieval = retrieval_success if retrieval_success is not None else human.get("retrieval_success")
    revision = revision_impact_accuracy if revision_impact_accuracy is not None else human.get("revision_impact_accuracy")
    human_burden = composite = reduction = None
    baseline = data.get("baseline", {})
    if retrieval is not None and revision is not None:
        _rate("retrieval_success", retrieval)
        _rate("revision_impact_accuracy", revision)
        human_burden = round(100.0 - (60.0 * retrieval + 40.0 * revision), 2)
        composite = round(0.8 * structural_rate + 0.2 * human_burden, 2)
        baseline_composite = baseline.get("composite_entropy")
        if baseline_composite not in (None, 0):
            reduction = round((baseline_composite - composite) / baseline_composite, 4)
    baseline_structural = baseline.get("structural_entropy_rate")
    structural_reduction = None
    if baseline_structural not in (None, 0):
        structural_reduction = round((baseline_structural - structural_rate) / baseline_structural, 4)
    critical = [item for item in diagnostics if item.critical]
    return {
        "manifest": str(manifest_path),
        "structural": {
            "points": points,
            "maximum": maximum,
            "entropy_rate": structural_rate,
            "baseline_rate": baseline_structural,
            "relative_reduction": structural_reduction,
        },
        "human": {
            "retrieval_success": retrieval,
            "revision_impact_accuracy": revision,
            "burden": human_burden,
            "status": "measured" if human_burden is not None else "pending-human-measurement",
        },
        "human_measurement_check": {
            "status": "recorded" if human_burden is not None else "pending",
            "visibility": human_check.get("visibility", "ci-report"),
            "blocking": bool(human_check.get("blocking", False)),
            "required_for_composite_acceptance": bool(human_check.get("required_for_composite_acceptance", True)),
            "message": (
                "Human outcomes are recorded and included in the composite calculation."
                if human_burden is not None
                else "Human outcomes are not recorded; composite acceptance remains pending."
            ),
        },
        "composite_entropy": composite,
        "relative_reduction": reduction,
        "acceptance": {
            "target_reduction": 0.40,
            "critical_gap_count": len(critical),
            "zero_critical_gaps": not critical,
            "met": reduction is not None and reduction >= 0.40 and not critical,
            "status": "measured" if reduction is not None else "pending-human-measurement",
        },
        "surfaces": per_surface,
        "diagnostics": [
            {"code": item.code, "path": str(item.path), "message": item.message, "critical": item.critical}
            for item in diagnostics
        ],
    }


def _required(surface: dict[str, Any], surface_id: str, target: Path, diagnostics: list[EpistemicDiagnostic]) -> None:
    for field in ("claim_id", "epistemic_state", "scope", "provenance", "dependencies", "as_of", "review_trigger", "next_evidence", "transition"):
        value = surface.get(field)
        if value in (None, "", [], {}):
            diagnostics.append(EpistemicDiagnostic("epistemic-field-missing", target, f"Surface {surface_id} requires {field}.", field in {"claim_id", "provenance"}))
    transition = surface.get("transition")
    if isinstance(transition, dict) and not all(transition.get(key) for key in ("cause", "actor", "history_ref")):
        diagnostics.append(EpistemicDiagnostic("transition-lineage-incomplete", target, f"Surface {surface_id} transition requires cause, actor, and history_ref."))


def _surface_entropy(surface_id: str, surface: dict[str, Any]) -> dict[str, Any]:
    points = 0
    maximum = 10
    gaps: list[str] = []
    checks = (
        (2, bool(surface.get("claim_id") and surface.get("epistemic_state")), "claim-state"),
        (2, bool(surface.get("provenance")), "provenance"),
        (1, bool(str(surface.get("scope", "")).strip()), "scope"),
        (2, bool(surface.get("dependencies")), "dependencies"),
        (1, bool(surface.get("as_of") and surface.get("review_trigger")), "review-trigger"),
        (2, isinstance(surface.get("transition"), dict) and all(surface["transition"].get(key) for key in ("cause", "actor", "history_ref")), "transition-history"),
    )
    for weight, passed, label in checks:
        if not passed:
            points += weight
            gaps.append(label)
    if surface.get("corroboration_asserted"):
        maximum += 4
        if surface.get("source_independence") != "independent":
            points += 1
            gaps.append("source-independence")
        if surface.get("downstream_repetition_as_evidence"):
            points += 3
            gaps.append("synthetic-corroboration")
    if surface.get("criticality") == "critical":
        maximum += 3
        if any(item in {"review-required", "unresolved", "stale"} for item in surface.get("open_impacts", [])):
            points += 3
            gaps.append("open-critical-impact")
    if surface.get("kind") in {"publication", "decision", "approval"}:
        maximum += 3
        if not (surface.get("source_version") and surface.get("approval_binding")):
            points += 3
            gaps.append("source-version-approval-binding")
    return {"id": surface_id, "points": points, "maximum": maximum, "entropy_rate": round(100.0 * points / maximum, 2), "gaps": gaps}


def _rate(label: str, value: float) -> None:
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{label} must be between 0.0 and 1.0")
