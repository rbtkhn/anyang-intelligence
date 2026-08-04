from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
from typing import Any, Mapping

from .runtime_bootstrap import (
    RuntimeBootstrapError,
    environment_python,
    validation_cache_root,
    validation_environment_path,
    validation_requirements,
)


VALIDATION_POLICY_VERSION = 1


def repository_validation_python(repo_root: Path) -> Path:
    """Return the repository-local runtime path used by the canonical launcher."""

    return repo_root.resolve() / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def repository_fingerprint(repo_root: Path, python: Path) -> str:
    """Return the exact tree/runtime fingerprint used by Full validation."""

    root = repo_root.resolve()
    digest = hashlib.sha256()
    digest.update(f"validation-policy:{VALIDATION_POLICY_VERSION}\n".encode())
    digest.update(f"python:{platform.python_implementation()}:{platform.python_version()}\n".encode())
    digest.update(f"platform:{platform.system()}:{platform.machine()}\n".encode())
    for args in (("rev-parse", "HEAD"), ("diff", "--binary", "--no-ext-diff", "HEAD", "--", ".")):
        output = _git(root, *args)
        digest.update(output)
    untracked = _git(root, "ls-files", "--others", "--exclude-standard", "-z")
    for encoded_path in sorted(item for item in untracked.split(b"\0") if item):
        relative = encoded_path.decode("utf-8", errors="surrogateescape")
        path = root / relative
        digest.update(b"untracked\0" + encoded_path + b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
    digest.update(str(python.resolve()).encode("utf-8", errors="surrogateescape"))
    return digest.hexdigest()


def existing_validation_python(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
) -> Path | None:
    """Locate an already-provisioned validation runtime without creating it."""

    root = repo_root.resolve()
    local_python = repository_validation_python(root)
    if local_python.is_file():
        return local_python
    requirements = validation_requirements(root / "pyproject.toml")
    cache_root = validation_cache_root(root, environ)
    environment = validation_environment_path(root, cache_root, requirements)
    python = environment_python(environment)
    marker = environment / ".anyang-validation.json"
    try:
        metadata = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    if not python.is_file():
        return None
    if metadata.get("source") != "pyproject.toml" or metadata.get("requirements") != requirements:
        return None
    return python


def read_full_validation_evidence(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Inspect the cached Full result without bootstrapping or updating it."""

    root = repo_root.resolve()
    cache_path = root / ".pytest_cache" / "validation-results.json"
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "missing", "cache_ref": ".pytest_cache/validation-results.json"}
    except (OSError, ValueError, TypeError):
        return {"status": "invalid", "cache_ref": ".pytest_cache/validation-results.json"}
    result = payload.get("full") if isinstance(payload, dict) else None
    if payload.get("version") != VALIDATION_POLICY_VERSION or not isinstance(result, dict):
        return {"status": "incompatible", "cache_ref": ".pytest_cache/validation-results.json"}
    try:
        python = existing_validation_python(root, environ=environ)
    except RuntimeBootstrapError:
        python = None
    evidence: dict[str, Any] = {
        "status": "runtime-unavailable" if python is None else "stale",
        "cache_ref": ".pytest_cache/validation-results.json",
        "recorded_fingerprint": str(result.get("fingerprint", "")),
        "completed_at": str(result.get("completed_at", "")),
        "policy_version": payload["version"],
    }
    if python is None:
        return evidence
    current = repository_fingerprint(root, python)
    evidence["current_fingerprint"] = current
    evidence["runtime_ref"] = (
        "repository-validation-runtime"
        if python.resolve() == repository_validation_python(root).resolve()
        else "external-validation-runtime"
    )
    evidence["status"] = "passed" if result.get("fingerprint") == current else "stale"
    return evidence


def _git(repo_root: Path, *args: str) -> bytes:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout
