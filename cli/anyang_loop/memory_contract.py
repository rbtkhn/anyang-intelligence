from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

import yaml

from .privacy_scan import scan_text


DEFAULT_MANIFEST = "memory-constitution.yaml"
SCHEMA = "anyang-agent-memory-constitution/v1"
VERSION = "0.2"
RULE_ID = re.compile(r"^AMC-[A-Z]{2,3}-\d{3}$")
REQUIRED_FAMILIES = {
    "AMC-ID", "AMC-COL", "AMC-CLS", "AMC-PRO", "AMC-EVI", "AMC-AUT",
    "AMC-RET", "AMC-REL", "AMC-RGT", "AMC-DEL", "AMC-EVL", "AMC-EMG", "AMC-AMD",
}
REQUIRED_RUNTIME_FLAGS = {
    "enabled", "collection_enabled", "ingestion_enabled", "promotion_enabled",
    "retrieval_enabled", "automatic_injection_enabled",
}
REQUIRED_PROHIBITIONS = {
    "read-session-bodies", "create-private-database", "ingest-source-events",
    "generate-memory-candidates", "promote-memory", "retrieve-memory",
    "inject-self-model-packet", "infer-operator-preferences",
}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
ALLOWED_DISPOSITIONS = {"hold", "reject", "exclude", "quarantine"}
FORBIDDEN_KEYS = {"raw_content", "session_body", "transcript_body"}
FORBIDDEN_VALUE_MARKERS = ("c:/private/", "/private/", ".codex/sessions")


@dataclass(frozen=True)
class MemoryContractDiagnostic:
    code: str
    path: Path
    message: str
    critical: bool = True


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_memory_constitution(path: str | Path | None = None) -> tuple[Path, dict[str, Any]]:
    manifest = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Memory constitution root must be a mapping")
    return manifest, data


def validate_memory_constitution(path: str | Path | None = None) -> list[MemoryContractDiagnostic]:
    try:
        manifest, data = load_memory_constitution(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        target = Path(path) if path else repository_root() / DEFAULT_MANIFEST
        return [MemoryContractDiagnostic("memory-contract-invalid", target, str(exc))]

    diagnostics: list[MemoryContractDiagnostic] = []
    if data.get("schema") != SCHEMA or str(data.get("version")) != VERSION:
        diagnostics.append(MemoryContractDiagnostic("memory-contract-version", manifest, f"Expected {SCHEMA} version {VERSION}."))
    if data.get("status") != "advisory" or data.get("authority_effect") != "none":
        diagnostics.append(MemoryContractDiagnostic("memory-contract-authority", manifest, "Phase 1 must remain advisory with authority_effect none."))

    runtime = data.get("runtime")
    if (
        not isinstance(runtime, dict)
        or set(runtime) != REQUIRED_RUNTIME_FLAGS
        or any(value is not False for value in runtime.values())
    ):
        diagnostics.append(MemoryContractDiagnostic("memory-runtime-enabled", manifest, "Every Phase 1 runtime capability must be declared and false."))

    storage = data.get("storage")
    if (
        not isinstance(storage, dict)
        or set(storage) != {"canonical_store", "private_write_root", "repository_database_allowed"}
        or storage.get("canonical_store") != "not-configured"
        or storage.get("private_write_root") != "not-authorized"
        or storage.get("repository_database_allowed") is not False
    ):
        diagnostics.append(MemoryContractDiagnostic("memory-storage-configured", manifest, "Phase 1 storage must remain unconfigured and unauthorized."))

    governance = data.get("governance")
    if not isinstance(governance, dict) or governance != {
        "constitutional_authority": "human-operator",
        "collection_authority": "none",
        "promotion_authority": "none",
        "amendment_authority": "human-operator",
    }:
        diagnostics.append(MemoryContractDiagnostic("memory-governance-invalid", manifest, "Phase 1 requires human constitutional authority and no collection or promotion authority."))

    _validate_documents(manifest, data.get("documents"), diagnostics)
    _validate_rules(manifest, data.get("rules"), diagnostics)

    prohibitions = data.get("prohibited_phase_1_actions")
    if not isinstance(prohibitions, list) or set(prohibitions) != REQUIRED_PROHIBITIONS:
        diagnostics.append(MemoryContractDiagnostic("memory-prohibitions-incomplete", manifest, "Phase 1 prohibited actions must match the canonical disabled set."))

    for key, value in _walk(data):
        if key in FORBIDDEN_KEYS:
            diagnostics.append(MemoryContractDiagnostic("memory-raw-content-prohibited", manifest, f"Phase 1 manifest contains prohibited field {key}."))
        if isinstance(value, str) and _contains_forbidden_path(value):
            diagnostics.append(MemoryContractDiagnostic("memory-private-path-prohibited", manifest, "Phase 1 manifest contains a private or session-store path."))
    return diagnostics


def render_memory_contract_report(path: str | Path | None = None) -> dict[str, Any]:
    diagnostics = validate_memory_constitution(path)
    try:
        manifest, data = load_memory_constitution(path)
    except (OSError, ValueError, yaml.YAMLError):
        manifest = (Path(path) if path else repository_root() / DEFAULT_MANIFEST).resolve()
        data = {}
    rules = data.get("rules", []) if isinstance(data.get("rules"), list) else []
    return {
        "schema": "anyang-agent-memory-contract-report/v1",
        "manifest": manifest.name,
        "version": str(data.get("version", "")),
        "status": data.get("status"),
        "authority_effect": data.get("authority_effect"),
        "runtime_enabled": bool(data.get("runtime", {}).get("enabled")) if isinstance(data.get("runtime"), dict) else None,
        "rule_count": len(rules),
        "ok": not diagnostics,
        "diagnostics": [
            {"code": item.code, "path": item.path.as_posix(), "message": item.message, "critical": item.critical}
            for item in diagnostics
        ],
    }


def render_memory_contract_json(path: str | Path | None = None) -> str:
    return json.dumps(render_memory_contract_report(path), indent=2, sort_keys=True) + "\n"


def _validate_documents(manifest: Path, documents: Any, diagnostics: list[MemoryContractDiagnostic]) -> None:
    if not isinstance(documents, dict) or set(documents) != {"constitution", "conformance", "kernel", "acceptance"}:
        diagnostics.append(MemoryContractDiagnostic("memory-documents-incomplete", manifest, "Declare exactly the four Phase 1 documents."))
        return
    root = manifest.parent.resolve()
    for name, record in documents.items():
        if not isinstance(record, dict) or set(record) != {"path", "version"}:
            diagnostics.append(MemoryContractDiagnostic("memory-document-invalid", manifest, f"Document {name} requires path and version."))
            continue
        target = (root / str(record["path"])).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            diagnostics.append(MemoryContractDiagnostic("memory-document-escape", target, f"Document {name} escapes the manifest root."))
            continue
        if not target.is_file():
            diagnostics.append(MemoryContractDiagnostic("memory-document-missing", target, f"Document {name} does not exist."))
            continue
        content = target.read_text(encoding="utf-8")
        marker = f"**Version:** {record['version']}"
        if marker not in content:
            diagnostics.append(MemoryContractDiagnostic("memory-document-version", target, f"Document {name} is missing version marker {marker}."))
        privacy_findings = sorted(set(scan_text(content)))
        if privacy_findings:
            diagnostics.append(MemoryContractDiagnostic("memory-document-privacy", target, f"Document {name} failed privacy checks: {', '.join(privacy_findings)}."))
        if _contains_forbidden_path(content):
            diagnostics.append(MemoryContractDiagnostic("memory-document-private-path", target, f"Document {name} contains a private or session-store path."))


def _validate_rules(manifest: Path, rules: Any, diagnostics: list[MemoryContractDiagnostic]) -> None:
    if not isinstance(rules, list) or not rules:
        diagnostics.append(MemoryContractDiagnostic("memory-rules-empty", manifest, "Declare at least one constitutional rule."))
        return
    seen: set[str] = set()
    families: set[str] = set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            diagnostics.append(MemoryContractDiagnostic("memory-rule-invalid", manifest, f"Rule {index} must be a mapping."))
            continue
        if set(rule) != {"id", "article", "severity", "failure_disposition", "planned_test"}:
            diagnostics.append(MemoryContractDiagnostic("memory-rule-fields", manifest, f"Rule {index} has an invalid field set."))
            continue
        rule_id = str(rule["id"])
        if not RULE_ID.fullmatch(rule_id):
            diagnostics.append(MemoryContractDiagnostic("memory-rule-id-invalid", manifest, f"Invalid rule ID {rule_id}."))
        if rule_id in seen:
            diagnostics.append(MemoryContractDiagnostic("memory-rule-id-duplicate", manifest, f"Duplicate rule ID {rule_id}."))
        seen.add(rule_id)
        families.add(rule_id.rsplit("-", 1)[0])
        if not str(rule["article"]).strip():
            diagnostics.append(MemoryContractDiagnostic("memory-rule-article-missing", manifest, f"Rule {rule_id} has no article."))
        if rule["severity"] not in ALLOWED_SEVERITIES:
            diagnostics.append(MemoryContractDiagnostic("memory-rule-severity-invalid", manifest, f"Rule {rule_id} has an unknown severity."))
        if rule["failure_disposition"] not in ALLOWED_DISPOSITIONS:
            diagnostics.append(MemoryContractDiagnostic("memory-rule-disposition-invalid", manifest, f"Rule {rule_id} has an unknown disposition."))
        if not str(rule["planned_test"]).startswith("test_"):
            diagnostics.append(MemoryContractDiagnostic("memory-rule-test-invalid", manifest, f"Rule {rule_id} has no pytest-style planned test."))
    missing = sorted(REQUIRED_FAMILIES - families)
    if missing:
        diagnostics.append(MemoryContractDiagnostic("memory-rule-family-missing", manifest, "Missing rule families: " + ", ".join(missing)))


def _walk(value: Any, key: str = ""):
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            yield from _walk(child_value, str(child_key))
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child, key)
    else:
        yield key, value


def _contains_forbidden_path(value: str) -> bool:
    normalized = value.lower().replace("\\", "/")
    return any(marker in normalized for marker in FORBIDDEN_VALUE_MARKERS)
