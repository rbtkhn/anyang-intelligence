from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import date

import yaml


DEFAULT_MANIFEST = "artifact-state.yaml"
AUTHORITY_LEVELS = {
    "canonical",
    "provisional",
    "derived",
    "evidentiary",
    "convenience",
    "operational-residue",
}
AUTHORITATIVE_LEVELS = {"canonical", "provisional"}


@dataclass(frozen=True)
class ArtifactDiagnostic:
    code: str
    path: Path
    message: str


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_artifact_manifest(path: str | Path | None = None) -> list[ArtifactDiagnostic]:
    manifest_path = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
    if not manifest_path.exists():
        return [ArtifactDiagnostic("artifact-manifest-missing", manifest_path, "Artifact-state manifest does not exist.")]
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [ArtifactDiagnostic("artifact-manifest-invalid", manifest_path, f"Cannot load artifact-state manifest: {exc}")]
    if not isinstance(data, dict):
        return [ArtifactDiagnostic("artifact-manifest-invalid", manifest_path, "Manifest root must be a mapping.")]

    diagnostics: list[ArtifactDiagnostic] = []
    governance = data.get("governance")
    if not isinstance(governance, dict):
        diagnostics.append(ArtifactDiagnostic("control-governance-missing", manifest_path, "Declare control owner, review cadence, next review, expansion rule, and retirement rule."))
    else:
        for field in ("owner", "review_cadence", "next_review", "expansion_rule", "retirement_rule"):
            if not _present(governance.get(field)):
                diagnostics.append(ArtifactDiagnostic("control-governance-incomplete", manifest_path, f"Governance metadata requires '{field}'."))

    exceptions = data.get("exceptions", [])
    if not isinstance(exceptions, list):
        diagnostics.append(ArtifactDiagnostic("control-exceptions-invalid", manifest_path, "Exceptions must be a list."))
    else:
        for index, exception in enumerate(exceptions):
            _validate_exception(exception, index, manifest_path, diagnostics)

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        return [ArtifactDiagnostic("artifact-set-empty", manifest_path, "Declare at least one governed artifact.")]

    canonical_by_domain: dict[str, list[str]] = {}
    for artifact_id, artifact in artifacts.items():
        label = str(artifact_id)
        if not isinstance(artifact, dict):
            diagnostics.append(_diagnostic("artifact-declaration-invalid", manifest_path, label, "Declaration must be a mapping."))
            continue
        for field in ("path", "operation", "domain", "authority", "provenance", "mutability", "recovery"):
            if not _present(artifact.get(field)):
                diagnostics.append(_diagnostic("artifact-field-missing", manifest_path, label, f"Add a non-empty '{field}' declaration."))

        authority = artifact.get("authority")
        if authority and authority not in AUTHORITY_LEVELS:
            diagnostics.append(_diagnostic("artifact-authority-invalid", manifest_path, label, f"Authority must be one of: {', '.join(sorted(AUTHORITY_LEVELS))}."))
        domain = artifact.get("domain")
        if authority == "canonical" and _present(domain):
            canonical_by_domain.setdefault(str(domain), []).append(label)

        provenance = artifact.get("provenance")
        if isinstance(provenance, dict):
            if not any(_present(provenance.get(key)) for key in ("sources", "schema", "origin")):
                diagnostics.append(_diagnostic("artifact-provenance-empty", manifest_path, label, "Provenance must name sources, schema, or origin."))
        elif provenance is not None:
            diagnostics.append(_diagnostic("artifact-provenance-invalid", manifest_path, label, "Provenance must be a mapping."))

        mutability = artifact.get("mutability")
        if isinstance(mutability, dict):
            if not _present(mutability.get("method")) or not _present(mutability.get("writers")):
                diagnostics.append(_diagnostic("artifact-mutability-incomplete", manifest_path, label, "Mutability must name a method and permitted writers."))
        elif mutability is not None:
            diagnostics.append(_diagnostic("artifact-mutability-invalid", manifest_path, label, "Mutability must be a mapping."))

        recovery = artifact.get("recovery")
        if isinstance(recovery, dict):
            if not _present(recovery.get("method")) or not _present(recovery.get("verification")):
                diagnostics.append(_diagnostic("artifact-recovery-incomplete", manifest_path, label, "Recovery must name a method and post-recovery verification."))
        elif recovery is not None:
            diagnostics.append(_diagnostic("artifact-recovery-invalid", manifest_path, label, "Recovery must be a mapping."))

        if authority == "derived":
            sources = provenance.get("sources") if isinstance(provenance, dict) else None
            if not _present(sources):
                diagnostics.append(_diagnostic("derived-source-missing", manifest_path, label, "Derived artifacts must name at least one source artifact."))
            elif isinstance(sources, list):
                for source in sources:
                    if source not in artifacts:
                        diagnostics.append(_diagnostic("artifact-source-unknown", manifest_path, label, f"Source artifact '{source}' is not declared."))

        git = artifact.get("git", {})
        if isinstance(git, dict) and git.get("tracked") is True and authority in AUTHORITATIVE_LEVELS and artifact.get("data_class") != "public":
            diagnostics.append(_diagnostic("private-authority-in-git", manifest_path, label, "Non-public authoritative state may not be tracked in Git."))

    for domain, artifact_ids in canonical_by_domain.items():
        if len(artifact_ids) > 1:
            diagnostics.append(ArtifactDiagnostic("duplicate-canonical-authority", manifest_path, f"Domain '{domain}' has multiple canonical artifacts: {', '.join(artifact_ids)}."))
    return diagnostics


def _present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) >= 3
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _diagnostic(code: str, path: Path, artifact_id: str, message: str) -> ArtifactDiagnostic:
    return ArtifactDiagnostic(code, path, f"Artifact '{artifact_id}': {message}")


def _validate_exception(
    exception: object, index: int, path: Path, diagnostics: list[ArtifactDiagnostic]
) -> None:
    label = f"Exception {index + 1}"
    if not isinstance(exception, dict):
        diagnostics.append(ArtifactDiagnostic("control-exception-invalid", path, f"{label} must be a mapping."))
        return
    for field in ("control", "scope", "reason", "approved_by", "expires", "review_condition"):
        if not _present(exception.get(field)):
            diagnostics.append(ArtifactDiagnostic("control-exception-incomplete", path, f"{label} requires '{field}'."))
    expires = exception.get("expires")
    if expires:
        try:
            expiry = expires if isinstance(expires, date) else date.fromisoformat(str(expires))
            if expiry < date.today():
                diagnostics.append(ArtifactDiagnostic("control-exception-expired", path, f"{label} expired on {expiry.isoformat()}."))
        except ValueError:
            diagnostics.append(ArtifactDiagnostic("control-exception-date-invalid", path, f"{label} expires must use YYYY-MM-DD."))
