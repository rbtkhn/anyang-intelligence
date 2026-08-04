from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sqlite3
import subprocess
from typing import Any, Mapping

from .council_workroom import council_projection, verify_council_transaction
from .ops_db import connect_readonly
from .ops_service import OpsError
from .validation_evidence import read_full_validation_evidence


def collect_graph_evidence(
    packet: dict[str, Any],
    repo_root: str | Path,
    *,
    as_of: str,
    db_path: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Collect only the evidence explicitly requested by a validated graph."""

    root = Path(repo_root).resolve()
    from .work_graph import WorkGraphError, validate_work_graph

    validate_work_graph(packet, root)
    if db_path is not None:
        database = Path(db_path).expanduser().resolve()
        try:
            database.relative_to(root)
        except ValueError:
            pass
        else:
            raise WorkGraphError("Council database must remain outside the repository")
    snapshot = _repository_snapshot(root)
    results: dict[str, list[dict[str, Any]]] = {}
    council_connection: sqlite3.Connection | None = None
    try:
        for node in packet["nodes"]:
            node_results: list[dict[str, Any]] = []
            for rule in node.get("completion", []):
                kind = rule["type"]
                if kind.startswith("git-"):
                    result = _git_evidence(root, snapshot, packet["scope"], rule)
                elif kind.startswith("validation-"):
                    result = _validation_evidence(root, rule, environ=environ)
                elif kind.startswith("file-"):
                    result = _file_evidence(root, rule)
                elif kind.startswith("council-"):
                    if db_path is None:
                        result = _result(rule, "unknown", "council database was not supplied")
                    else:
                        if council_connection is None:
                            council_connection = connect_readonly(db_path)
                        result = _council_evidence(
                            council_connection,
                            packet["scope"].get("tenant"),
                            rule,
                            as_of=as_of,
                        )
                else:
                    result = _result(rule, "present", "explicit reference supplied")
                node_results.append(result)
            results[node["id"]] = node_results
    except (OSError, sqlite3.Error, OpsError, RuntimeError) as exc:
        raise RuntimeError(f"Unable to collect graph evidence: {exc}") from exc
    finally:
        if council_connection is not None:
            council_connection.close()
    return {"source_snapshot": snapshot, "nodes": results}


def _repository_snapshot(root: Path) -> dict[str, Any]:
    head = _git_text(root, "rev-parse", "HEAD")
    branch = _git_text(root, "branch", "--show-current") or "detached"
    staged = _git_paths(root, "diff", "--cached", "--name-only", "-z")
    unstaged = _git_paths(root, "diff", "--name-only", "-z")
    untracked = _git_paths(root, "ls-files", "--others", "--exclude-standard", "-z")
    changed = sorted(set(staged + unstaged + untracked))
    payload = "\n".join((head, branch, *changed)).encode("utf-8", errors="surrogateescape")
    return {
        "repository": root.name,
        "head": head,
        "branch": branch,
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
        "changed_paths": changed,
        "snapshot_digest": hashlib.sha256(payload).hexdigest(),
    }


def _git_evidence(
    root: Path,
    snapshot: dict[str, Any],
    scope: dict[str, Any],
    rule: dict[str, Any],
) -> dict[str, Any]:
    kind = rule["type"]
    if kind == "git-head":
        expected = rule["expected"]
        return _result(rule, "satisfied" if snapshot["head"] == expected else "missing", "HEAD comparison")
    if kind == "git-changes-within-scope":
        permitted = tuple(scope["permitted_paths"])
        excluded = tuple(scope.get("excluded_paths", []))
        relevant = [path for path in snapshot["changed_paths"] if not _matches_any(path, excluded)]
        outside = [path for path in relevant if not _matches_any(path, permitted)]
        if outside:
            return _result(rule, "held", "changed paths escape declared scope", refs=outside)
        return _result(
            rule,
            "satisfied" if relevant else "missing",
            "scoped changes inspected",
            refs=relevant,
        )
    if kind == "git-commit":
        commit = rule["commit"]
        exists = _git_returncode(root, "cat-file", "-e", f"{commit}^{{commit}}") == 0
        return _result(rule, "satisfied" if exists else "missing", "local commit lookup", refs=[commit])
    if kind == "git-remote-tracking-contains":
        ref = rule["ref"]
        commit = rule["commit"]
        exists = _git_returncode(root, "merge-base", "--is-ancestor", commit, ref) == 0
        return _result(
            rule,
            "satisfied" if exists else "missing",
            "local remote-tracking comparison; no fetch performed",
            refs=[ref, commit],
        )
    raise RuntimeError(f"Unsupported Git evidence type: {kind}")


def _validation_evidence(
    root: Path,
    rule: dict[str, Any],
    *,
    environ: Mapping[str, str] | None,
) -> dict[str, Any]:
    evidence = read_full_validation_evidence(root, environ=environ)
    status = evidence["status"]
    mapped = {
        "passed": "satisfied",
        "stale": "stale",
        "missing": "missing",
        "invalid": "held",
        "incompatible": "held",
        "runtime-unavailable": "unknown",
    }[status]
    refs = [evidence["cache_ref"]]
    return _result(rule, mapped, f"Full validation cache is {status}", refs=refs, details=evidence)


def _file_evidence(root: Path, rule: dict[str, Any]) -> dict[str, Any]:
    relative = rule["path"]
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"Evidence path escapes repository: {relative}") from exc
    if rule["type"] == "file-exists":
        return _result(rule, "satisfied" if path.is_file() else "missing", "file existence", refs=[relative])
    if not path.is_file():
        return _result(rule, "missing", "file missing", refs=[relative])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return _result(
        rule,
        "satisfied" if digest == rule["sha256"] else "stale",
        "file digest comparison",
        refs=[relative],
        details={"observed_sha256": digest},
    )


def _council_evidence(
    connection: sqlite3.Connection,
    tenant: str | None,
    rule: dict[str, Any],
    *,
    as_of: str,
) -> dict[str, Any]:
    transaction_id = rule["transaction_id"]
    projection = council_projection(connection, transaction_id, as_of=as_of)
    row = connection.execute(
        "SELECT slug FROM tenant WHERE id = ?", (projection["transaction"]["tenant_id"],)
    ).fetchone()
    if not row or row["slug"] != tenant:
        return _result(rule, "held", "Council evidence crosses the declared tenant boundary")
    if rule["type"] == "council-event-chain":
        verification = verify_council_transaction(connection, transaction_id, as_of=as_of)
        return _result(
            rule,
            "satisfied" if verification["ok"] else "held",
            "Council event chain verification",
            refs=[transaction_id, verification["head_hash"]],
        )
    expected_state = rule.get("current_state")
    expected_subject = rule.get("subject_hash")
    matches = (expected_state is None or projection["current_state"] == expected_state) and (
        expected_subject is None or projection["subject_hash"] == expected_subject
    )
    if not projection["lineage"]["chain_verified"]:
        return _result(
            rule,
            "held",
            "Council projection event chain failed verification",
            refs=[transaction_id, projection["lineage"]["head_hash"]],
        )
    return _result(
        rule,
        "satisfied" if matches else "stale",
        "tenant-isolated Council projection comparison",
        refs=[transaction_id, projection["lineage"]["head_hash"]],
        details={
            "current_state": projection["current_state"],
            "subject_hash": projection["subject_hash"],
            "chain_verified": projection["lineage"]["chain_verified"],
        },
    )


def _result(
    rule: dict[str, Any],
    status: str,
    summary: str,
    *,
    refs: list[str] | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": rule["type"],
        "status": status,
        "summary": summary,
        "refs": sorted(refs or []),
    }
    if details:
        result["details"] = details
    return result


def _matches_any(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(
        path == prefix.rstrip("/") or path.startswith(prefix.rstrip("/") + "/")
        for prefix in prefixes
    )


def _git_paths(root: Path, *args: str) -> list[str]:
    output = _git(root, *args)
    return sorted(
        item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for item in output.split(b"\0")
        if item
    )


def _git_text(root: Path, *args: str) -> str:
    return _git(root, *args).decode("utf-8", errors="replace").strip()


def _git_returncode(root: Path, *args: str) -> int:
    return _run_git(root, *args).returncode


def _git(root: Path, *args: str) -> bytes:
    result = _run_git(root, *args)
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(
        ["git", *args],
        cwd=root,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
