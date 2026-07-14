from __future__ import annotations

from dataclasses import dataclass
import fnmatch
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .artifact_state import repository_root


DEFAULT_MANIFEST = "bounded-agency.yaml"
KNOWN_PHASES = {"singularity-transcript-intake"}
KNOWN_CAPABILITIES = {"anyang-project import-transcripts"}
KNOWN_INVARIANTS = {
    "invoked-manifest-authoritative-for-phase",
    "manifest-valid",
    "source-present",
    "rights-governed",
    "destination-contained",
    "destination-no-overwrite",
    "contact-details-redacted",
    "actual-delta-within-plan",
    "no-cross-project-output",
}


@dataclass(frozen=True)
class AgencyDiagnostic:
    code: str
    path: Path
    message: str


@dataclass(frozen=True)
class PhaseContract:
    phase_id: str
    objective: str
    capability: str
    canonical_inputs: tuple[str, ...]
    derived_outputs: tuple[str, ...]
    may_read: tuple[str, ...]
    may_write: tuple[str, ...]
    protected: tuple[str, ...]
    operations: dict[str, tuple[str, ...]]
    invariants: tuple[str, ...]
    warnings: tuple[str, ...]
    row_holds: tuple[str, ...]
    authorization_required: tuple[str, ...]
    blockers: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    recovery: dict[str, Any]
    complete_when: tuple[str, ...]
    next_phase: dict[str, str]


class AgencyContractError(Exception):
    pass


def load_agency_manifest(path: str | Path | None = None) -> tuple[Path, dict[str, Any]]:
    manifest_path = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError as exc:
        raise AgencyContractError(f"Agency manifest not found: {manifest_path}") from exc
    except (OSError, yaml.YAMLError) as exc:
        raise AgencyContractError(f"Cannot load agency manifest {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AgencyContractError("Agency manifest root must be a mapping.")
    return manifest_path, payload


def load_phase(phase_id: str, path: str | Path | None = None) -> PhaseContract:
    manifest_path, payload = load_agency_manifest(path)
    diagnostics = validate_agency_manifest(manifest_path)
    if diagnostics:
        raise AgencyContractError("; ".join(item.message for item in diagnostics))
    raw = payload["phases"].get(phase_id)
    if not isinstance(raw, dict):
        raise AgencyContractError(f"Unknown agency phase: {phase_id}")
    operations = raw.get("operations", {})
    return PhaseContract(
        phase_id=phase_id,
        objective=str(raw["objective"]),
        capability=str(raw["capability"]),
        canonical_inputs=tuple(raw["canonical_inputs"]),
        derived_outputs=tuple(raw["derived_outputs"]),
        may_read=tuple(raw["may_read"]),
        may_write=tuple(raw["may_write"]),
        protected=tuple(raw["must_not_write_without_explicit_authorization"]),
        operations={key: tuple(operations.get(key, [])) for key in ("create", "modify", "delete")},
        invariants=tuple(raw["invariants"]),
        warnings=tuple(raw["warnings"]),
        row_holds=tuple(raw["row_holds"]),
        authorization_required=tuple(raw["authorization_required"]),
        blockers=tuple(raw["blockers"]),
        stop_conditions=tuple(raw["stop_conditions"]),
        recovery=dict(raw["recovery"]),
        complete_when=tuple(raw["complete_when"]),
        next_phase={str(key): str(value) for key, value in raw["next_phase"].items()},
    )


def validate_agency_manifest(path: str | Path | None = None, artifact_path: str | Path | None = None) -> list[AgencyDiagnostic]:
    try:
        manifest_path, data = load_agency_manifest(path)
    except AgencyContractError as exc:
        target = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
        return [AgencyDiagnostic("agency-manifest-invalid", target, str(exc))]
    diagnostics: list[AgencyDiagnostic] = []
    if data.get("version") != 1:
        diagnostics.append(AgencyDiagnostic("agency-version-invalid", manifest_path, "Version must be 1."))
    governance = data.get("governance")
    if not isinstance(governance, dict):
        diagnostics.append(AgencyDiagnostic("agency-governance-missing", manifest_path, "Governance metadata is required."))
    else:
        for field in ("owner", "review_cadence", "expansion_rule", "retirement_rule"):
            if not _present(governance.get(field)):
                diagnostics.append(AgencyDiagnostic("agency-governance-incomplete", manifest_path, f"Governance requires '{field}'."))
    artifact_ids = _artifact_ids(artifact_path)
    phases = data.get("phases")
    if not isinstance(phases, dict) or not phases:
        return diagnostics + [AgencyDiagnostic("agency-phases-empty", manifest_path, "Declare at least one phase.")]
    for phase_id, phase in phases.items():
        label = str(phase_id)
        if label not in KNOWN_PHASES:
            diagnostics.append(_diag("agency-phase-unknown", manifest_path, label, "No registered phase adapter owns this phase."))
        if not isinstance(phase, dict):
            diagnostics.append(_diag("agency-phase-invalid", manifest_path, label, "Phase must be a mapping."))
            continue
        required = (
            "objective", "capability", "canonical_inputs", "derived_outputs", "may_read", "may_write",
            "operations", "must_not_write_without_explicit_authorization", "invariants", "warnings", "blockers",
            "working_state", "public_state", "advisory_state", "row_holds", "authorization_required",
            "stop_conditions", "recovery", "complete_when", "next_phase",
        )
        for field in required:
            if not _present(phase.get(field)):
                diagnostics.append(_diag("agency-field-missing", manifest_path, label, f"Add non-empty '{field}'."))
        capability = phase.get("capability")
        if capability and capability not in KNOWN_CAPABILITIES:
            diagnostics.append(_diag("agency-capability-unknown", manifest_path, label, f"Unknown capability '{capability}'."))
        for field in ("canonical_inputs", "derived_outputs"):
            values = phase.get(field, [])
            if isinstance(values, list):
                for artifact_id in values:
                    if artifact_id not in artifact_ids:
                        diagnostics.append(_diag("agency-artifact-unknown", manifest_path, label, f"Unknown artifact '{artifact_id}'."))
        invariants = phase.get("invariants", [])
        if isinstance(invariants, list):
            for invariant in invariants:
                if invariant not in KNOWN_INVARIANTS:
                    diagnostics.append(_diag("agency-invariant-unknown", manifest_path, label, f"Unknown invariant '{invariant}'."))
        operations = phase.get("operations")
        if isinstance(operations, dict):
            for operation in ("create", "modify", "delete"):
                if operation not in operations or not isinstance(operations.get(operation), list):
                    diagnostics.append(_diag("agency-operations-incomplete", manifest_path, label, f"Operations require list '{operation}'."))
        else:
            diagnostics.append(_diag("agency-operations-invalid", manifest_path, label, "Operations must be a mapping."))
        for field in ("may_read", "may_write", "must_not_write_without_explicit_authorization"):
            for pattern in phase.get(field, []) if isinstance(phase.get(field), list) else []:
                error = validate_pattern(str(pattern), allow_external=field != "may_write")
                if error:
                    diagnostics.append(_diag("agency-path-invalid", manifest_path, label, f"{field} pattern '{pattern}': {error}"))
        writes = phase.get("may_write", []) if isinstance(phase.get("may_write"), list) else []
        protected = phase.get("must_not_write_without_explicit_authorization", []) if isinstance(phase.get("must_not_write_without_explicit_authorization"), list) else []
        seen_writes: dict[str, str] = {}
        for allowed in writes:
            normalized = str(allowed).replace("\\", "/").casefold()
            if normalized in seen_writes and seen_writes[normalized] != str(allowed):
                diagnostics.append(
                    _diag(
                        "agency-path-case-collision",
                        manifest_path,
                        label,
                        f"Write patterns '{seen_writes[normalized]}' and '{allowed}' collide on case-insensitive filesystems.",
                    )
                )
            seen_writes[normalized] = str(allowed)
        for allowed in writes:
            for denied in protected:
                if patterns_overlap(str(allowed), str(denied)):
                    diagnostics.append(_diag("agency-write-protected-overlap", manifest_path, label, f"Write '{allowed}' overlaps protected '{denied}'."))
        recovery = phase.get("recovery")
        if not isinstance(recovery, dict) or not _present(recovery.get("method")) or not _present(recovery.get("verification")):
            diagnostics.append(_diag("agency-recovery-incomplete", manifest_path, label, "Recovery requires method and verification."))
        next_phase = phase.get("next_phase")
        if not isinstance(next_phase, dict) or not _present(next_phase.get("owner")) or next_phase.get("authority") != "advisory-handoff-only":
            diagnostics.append(_diag("agency-next-phase-invalid", manifest_path, label, "Next phase requires owner and advisory-handoff-only authority."))
    return diagnostics


def validate_pattern(pattern: str, *, allow_external: bool) -> str | None:
    normalized = pattern.replace("\\", "/")
    if allow_external and (
        normalized in {"invoked-manifest", "manifest-referenced-source-bodies"}
        or normalized.startswith("external-systems:")
    ):
        return None
    if not normalized or normalized.startswith(("/", "~")) or ":/" in normalized:
        return "absolute paths are not allowed"
    if ".." in PurePosixPath(normalized).parts:
        return "path traversal is not allowed"
    return None


def patterns_overlap(left: str, right: str) -> bool:
    a = left.replace("\\", "/").casefold().strip("/").split("/")
    b = right.replace("\\", "/").casefold().strip("/").split("/")

    def segment_overlap(x: str, y: str) -> bool:
        x_wild = any(char in x for char in "*?")
        y_wild = any(char in y for char in "*?")
        if not x_wild and not y_wild:
            return x == y
        if not x_wild:
            return fnmatch.fnmatchcase(x, y)
        if not y_wild:
            return fnmatch.fnmatchcase(y, x)
        x_example = x.replace("*", "x").replace("?", "x")
        y_example = y.replace("*", "x").replace("?", "x")
        return fnmatch.fnmatchcase(x_example, y) or fnmatch.fnmatchcase(y_example, x)

    seen: set[tuple[int, int]] = set()

    def intersects(i: int, j: int) -> bool:
        if (i, j) in seen:
            return False
        seen.add((i, j))
        if i == len(a) and j == len(b):
            return True
        if i < len(a) and a[i] == "**":
            return intersects(i + 1, j) or (j < len(b) and intersects(i, j + 1))
        if j < len(b) and b[j] == "**":
            return intersects(i, j + 1) or (i < len(a) and intersects(i + 1, j))
        return i < len(a) and j < len(b) and segment_overlap(a[i], b[j]) and intersects(i + 1, j + 1)

    return intersects(0, 0)


def _artifact_ids(path: str | Path | None) -> set[str]:
    target = (Path(path) if path else repository_root() / "artifact-state.yaml").resolve()
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return set()
    artifacts = data.get("artifacts", {})
    return set(artifacts) if isinstance(artifacts, dict) else set()


def _present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _diag(code: str, path: Path, phase_id: str, message: str) -> AgencyDiagnostic:
    return AgencyDiagnostic(code, path, f"Phase '{phase_id}': {message}")
