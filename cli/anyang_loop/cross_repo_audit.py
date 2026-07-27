from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from fnmatch import fnmatchcase
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import yaml

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib


SCHEMA_VERSION = 1
COLLECTOR_VERSION = "1.2.0"
MAX_CAPTURE_CHARS = 20_000
MAX_SUMMARY_EXAMPLES = 20
MAX_SUMMARY_EXAMPLE_CHARS = 2_000
MAX_TEXT_SCAN_BYTES = 2 * 1024 * 1024
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".ps1",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
MUTATING_TOKENS = {
    "--apply",
    "--fix",
    "--force-write",
    "--write",
    "--write-receipt",
    "commit",
    "push",
}
MACHINE_PATH = re.compile(r"(?i)(?:[a-z]:[\\/](?:dev|users|windows)[\\/]|/(?:home|root|users)/)")
MACHINE_PATH_VALUE = re.compile(
    r"(?i)(?:[a-z]:[\\/](?:dev|users|windows)[\\/]|/(?:home|root|users)/)[^\s\"'<>]*"
)
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(token|password|passwd|secret|api[_-]?key|authorization)"
    r"(\s*[:=]\s*)([^\s,;]+)"
)
SECRET_TOKEN = re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})\b")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class CrossRepoAuditError(RuntimeError):
    pass


def collect_cross_repo_audit(
    repo: str | Path,
    config_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    root = _repository_root(Path(repo))
    config = _read_config(Path(config_path))
    output = Path(output_path).resolve()
    _ensure_outside(output, root)
    if output.exists():
        raise CrossRepoAuditError(f"Refusing to overwrite existing collector receipt: {output}")

    head = _git(root, "rev-parse", "HEAD")
    expected = config["expected_head"]
    if head != expected:
        raise CrossRepoAuditError(f"Target HEAD {head} does not match sealed commit {expected}.")

    status_before = _git_bytes(root, "status", "--porcelain=v1", "-z")
    tracked = _tracked_inventory(root)
    tracked_fingerprint_before = _tracked_fingerprint(tracked)
    diagnostics = _objective_diagnostics(root, tracked, config)
    with _disposable_snapshot(root, expected) as execution_root:
        command_runs = [
            _run_command(execution_root, item, config["timeout_seconds"])
            for item in config["commands"]
        ]
    commands = [item["receipt"] for item in command_runs]
    command_outputs = {
        item["receipt"]["id"]: {
            "stdout": item["stdout_complete"],
            "stderr": item["stderr_complete"],
        }
        for item in command_runs
    }
    root_cause_groups = _root_cause_groups(diagnostics, commands, command_outputs)

    tracked_after = _tracked_inventory(root)
    status_after = _git_bytes(root, "status", "--porcelain=v1", "-z")
    tracked_fingerprint_after = _tracked_fingerprint(tracked_after)
    mutation_proof = {
        "status_before_sha256": _sha256(status_before),
        "status_after_sha256": _sha256(status_after),
        "tracked_fingerprint_before": tracked_fingerprint_before,
        "tracked_fingerprint_after": tracked_fingerprint_after,
        "git_status_unchanged": status_before == status_after,
        "tracked_content_unchanged": tracked_fingerprint_before == tracked_fingerprint_after,
    }
    if not mutation_proof["git_status_unchanged"] or not mutation_proof["tracked_content_unchanged"]:
        raise CrossRepoAuditError("Target repository changed during collection; no receipt was written.")

    samples = _select_samples(tracked, config["sample_groups"], expected)
    collection_status = _collection_status(commands, samples)
    inventory = {
        "tracked_file_count": len(tracked),
        "tracked_bytes": sum(item["bytes"] for item in tracked),
        "by_top_level": _count_by(tracked, lambda item: item["path"].split("/", 1)[0]),
        "by_suffix": _count_by(tracked, lambda item: PurePosixPath(item["path"]).suffix.lower() or "[none]"),
        "files": tracked,
    }
    stable = {
        "schema_version": SCHEMA_VERSION,
        "collector": _collector_identity(),
        "audit_id": config["audit_id"],
        "repository": _repository_identity(root),
        "head": head,
        "tree": _git(root, "rev-parse", "HEAD^{tree}"),
        "adapter": {
            "controlling_paths": config["controlling_paths"],
            "sample_groups": config["sample_groups"],
            "commands": [
                {
                    "id": item["id"],
                    "argv": item["argv"],
                    "depends_on": item["depends_on"],
                    "summary_rules": item["summary_rules"],
                }
                for item in config["commands"]
            ],
            "timeout_seconds": config["timeout_seconds"],
            "execution_surface": "disposable-git-archive",
            "sample_match_semantics": "repository-rooted-segment-glob-v1",
        },
        "inventory": inventory,
        "samples": samples,
        "diagnostics": diagnostics,
        "root_cause_groups": root_cause_groups,
        "coverage_gaps": _coverage_gaps(tracked, diagnostics, commands, samples),
        "collection_status": collection_status,
    }
    receipt = {
        **stable,
        "collected_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "commands": commands,
        "mutation_proof": mutation_proof,
        "deterministic_fingerprint": _sha256(_canonical_bytes(stable)),
        "collector_boundary": {
            "assigns_semantic_severity": False,
            "declares_claim_truth": False,
            "recommends_strategy": False,
            "commands_execute_in_target_checkout": False,
            "commands_execute_in_disposable_snapshot": True,
            "target_git_visible_state_observed_unchanged": (
                mutation_proof["git_status_unchanged"]
                and mutation_proof["tracked_content_unchanged"]
            ),
            "operating_system_security_sandbox_claimed": False,
        },
    }
    _write_receipt_atomic(
        output,
        (json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"),
    )
    return receipt


def _read_config(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CrossRepoAuditError(f"Cannot read collector configuration: {path}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise CrossRepoAuditError("Collector configuration requires schema_version 1.")
    for field in ("audit_id", "expected_head"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise CrossRepoAuditError(f"Collector configuration requires {field}.")
    timeout = value.get("timeout_seconds", 180)
    if not isinstance(timeout, int) or timeout < 1 or timeout > 900:
        raise CrossRepoAuditError("timeout_seconds must be an integer from 1 to 900.")
    value["timeout_seconds"] = timeout
    value["controlling_paths"] = _string_list(value.get("controlling_paths", []), "controlling_paths")
    commands = value.get("commands")
    if not isinstance(commands, list):
        raise CrossRepoAuditError("commands must be a list.")
    seen: set[str] = set()
    for command in commands:
        if not isinstance(command, dict) or not isinstance(command.get("id"), str):
            raise CrossRepoAuditError("Each command requires a string id.")
        if command["id"] in seen:
            raise CrossRepoAuditError(f"Duplicate command id: {command['id']}")
        seen.add(command["id"])
        argv = _string_list(command.get("argv"), f"commands.{command['id']}.argv")
        if not argv:
            raise CrossRepoAuditError(f"Command {command['id']} has no argv.")
        prohibited = {token.lower() for token in argv} & MUTATING_TOKENS
        if prohibited:
            raise CrossRepoAuditError(f"Command {command['id']} contains prohibited mutation token(s): {sorted(prohibited)}")
        command["argv"] = argv
        dependencies = _string_list(
            command.get("depends_on", []),
            f"commands.{command['id']}.depends_on",
        )
        command["depends_on"] = [_portable_path(item) for item in dependencies]
        rules = command.get("summary_rules", [])
        if not isinstance(rules, list):
            raise CrossRepoAuditError(f"commands.{command['id']}.summary_rules must be a list.")
        rule_ids: set[str] = set()
        for rule in rules:
            if not isinstance(rule, dict) or not isinstance(rule.get("id"), str) or not rule["id"].strip():
                raise CrossRepoAuditError(f"Each summary rule for command {command['id']} requires a string id.")
            if rule["id"] in rule_ids:
                raise CrossRepoAuditError(f"Duplicate summary rule id for command {command['id']}: {rule['id']}")
            rule_ids.add(rule["id"])
            stream = rule.get("stream", "stdout")
            if stream not in {"stdout", "stderr", "both"}:
                raise CrossRepoAuditError(
                    f"Summary rule {command['id']}.{rule['id']} stream must be stdout, stderr, or both."
                )
            prefix = rule.get("line_prefix")
            if not isinstance(prefix, str) or not prefix or "\n" in prefix or "\r" in prefix:
                raise CrossRepoAuditError(
                    f"Summary rule {command['id']}.{rule['id']} requires a single-line literal line_prefix."
                )
            minimum = rule.get("minimum_matches", 1)
            if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0:
                raise CrossRepoAuditError(
                    f"Summary rule {command['id']}.{rule['id']} minimum_matches must be a non-negative integer."
                )
            maximum = rule.get("max_examples", 5)
            if (
                not isinstance(maximum, int)
                or isinstance(maximum, bool)
                or maximum < 1
                or maximum > MAX_SUMMARY_EXAMPLES
            ):
                raise CrossRepoAuditError(
                    f"Summary rule {command['id']}.{rule['id']} max_examples must be from 1 to {MAX_SUMMARY_EXAMPLES}."
                )
            rule["stream"] = stream
            rule["minimum_matches"] = minimum
            rule["max_examples"] = maximum
        command["summary_rules"] = rules
    groups = value.get("sample_groups")
    if not isinstance(groups, list) or not groups:
        raise CrossRepoAuditError("sample_groups must be a non-empty list.")
    group_ids: set[str] = set()
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("id"), str):
            raise CrossRepoAuditError("Each sample group requires a string id.")
        if group["id"] in group_ids:
            raise CrossRepoAuditError(f"Duplicate sample group id: {group['id']}")
        group_ids.add(group["id"])
        group["globs"] = [
            _portable_glob(item)
            for item in _string_list(group.get("globs"), f"sample_groups.{group['id']}.globs")
        ]
        group["exclude_globs"] = [
            _portable_glob(item)
            for item in _string_list(
                group.get("exclude_globs", []),
                f"sample_groups.{group['id']}.exclude_globs",
            )
        ]
        required = group.get("required", True)
        if not isinstance(required, bool):
            raise CrossRepoAuditError(f"Sample group {group['id']} required must be a boolean.")
        group["required"] = required
        if not isinstance(group.get("count"), int) or group["count"] < 1:
            raise CrossRepoAuditError(f"Sample group {group['id']} requires a positive count.")
    return value


def _tracked_inventory(root: Path) -> list[dict[str, Any]]:
    paths = sorted(_git_paths(root, "ls-files", "-z"))
    inventory: list[dict[str, Any]] = []
    for relative in paths:
        normalized = _portable_path(relative)
        source = root / Path(normalized)
        if source.is_symlink():
            inventory.append({"path": normalized, "kind": "symlink", "bytes": 0, "sha256": None})
            continue
        try:
            resolved = source.resolve(strict=True)
        except FileNotFoundError:
            inventory.append({"path": normalized, "kind": "missing", "bytes": 0, "sha256": None})
            continue
        _ensure_within(resolved, root)
        raw = resolved.read_bytes()
        inventory.append({"path": normalized, "kind": "file", "bytes": len(raw), "sha256": _sha256(raw)})
    return inventory


def _objective_diagnostics(root: Path, tracked: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    known = {item["path"] for item in tracked}
    for relative in config["controlling_paths"]:
        if relative not in known:
            diagnostics.append(_diagnostic("declared-control-gap", relative, "Declared controlling path is not tracked."))
    for item in tracked:
        if item["kind"] != "file":
            diagnostics.append(_diagnostic(f"tracked-{item['kind']}", item["path"], f"Tracked path is {item['kind']}."))
            continue
        path = item["path"]
        suffix = PurePosixPath(path).suffix.lower()
        if suffix not in TEXT_SUFFIXES or item["bytes"] > MAX_TEXT_SCAN_BYTES:
            continue
        source = root / Path(path)
        text = source.read_text(encoding="utf-8", errors="replace")
        if suffix in {".json", ".yaml", ".yml", ".toml"}:
            try:
                _parse_structured_text(suffix, text)
            except (json.JSONDecodeError, yaml.YAMLError, tomllib.TOMLDecodeError) as exc:
                category = {
                    ".json": "invalid-json",
                    ".yaml": "invalid-yaml",
                    ".yml": "invalid-yaml",
                    ".toml": "invalid-toml",
                }[suffix]
                diagnostics.append(
                    _diagnostic(
                        category,
                        path,
                        _structured_error_evidence(exc),
                        root_cause_id=f"{category}:{path}",
                    )
                )
        matches = sorted({match.group(0) for match in MACHINE_PATH.finditer(text)})
        if matches:
            diagnostics.append(
                _diagnostic(
                    "machine-local-path",
                    path,
                    f"Contains {len(matches)} machine-local path pattern(s).",
                )
            )
        if suffix == ".md":
            diagnostics.extend(_broken_links(root, path, text))
    diagnostics.sort(key=lambda item: (item["category"], item["path"], item["evidence"]))
    return diagnostics


def _broken_links(root: Path, relative: str, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    base = (root / Path(relative)).parent
    for raw_target in sorted(set(MARKDOWN_LINK.findall(text))):
        target = raw_target.strip().split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        candidate = (base / target.replace("/", os.sep)).resolve()
        try:
            _ensure_within(candidate, root)
        except CrossRepoAuditError:
            findings.append(_diagnostic("link-outside-repository", relative, f"Link target leaves repository: {target}"))
            continue
        if not candidate.exists():
            findings.append(_diagnostic("broken-relative-link", relative, f"Missing relative link target: {target}"))
    return findings


def _root_cause_groups(
    diagnostics: list[dict[str, Any]],
    commands: list[dict[str, Any]],
    command_outputs: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for diagnostic in diagnostics:
        root_cause_id = diagnostic.get("root_cause_id")
        if not root_cause_id:
            continue
        path = diagnostic["path"]
        affected: list[str] = []
        for command in commands:
            complete = (command_outputs or {}).get(command["id"])
            output = (
                complete["stdout"] + "\n" + complete["stderr"]
                if complete is not None
                else command["stdout"] + "\n" + command["stderr"]
            )
            if path in command["declared_dependencies"] or path in output:
                affected.append(command["id"])
        groups.append(
            {
                "root_cause_id": root_cause_id,
                "primary_diagnostic_id": diagnostic["diagnostic_id"],
                "affected_command_ids": sorted(affected),
                "collapsed_component_count": 1 + len(affected),
                "independent_finding_count": 1,
            }
        )
    return sorted(groups, key=lambda item: item["root_cause_id"])


def _select_samples(
    tracked: list[dict[str, Any]], groups: list[dict[str, Any]], seed: str
) -> list[dict[str, Any]]:
    paths = [item["path"] for item in tracked if item["kind"] == "file"]
    result: list[dict[str, Any]] = []
    for group in groups:
        include_counts = {
            pattern: sum(1 for path in paths if _rooted_glob_match(path, pattern))
            for pattern in group["globs"]
        }
        included = {
            path
            for path in paths
            if any(_rooted_glob_match(path, pattern) for pattern in group["globs"])
        }
        exclude_counts = {
            pattern: sum(1 for path in included if _rooted_glob_match(path, pattern))
            for pattern in group["exclude_globs"]
        }
        excluded = {
            path
            for path in included
            if any(_rooted_glob_match(path, pattern) for pattern in group["exclude_globs"])
        }
        matches = sorted(included - excluded)
        ranked = sorted(matches, key=lambda path: (_sha256(f"{seed}:{group['id']}:{path}".encode("utf-8")), path))
        selected = sorted(ranked[: group["count"]])
        result.append(
            {
                "id": group["id"],
                "required": group["required"],
                "requested": group["count"],
                "include_match_counts": include_counts,
                "exclude_match_counts": exclude_counts,
                "included_before_exclusions": len(included),
                "excluded": len(excluded),
                "eligible": len(matches),
                "selected": selected,
                "selection_complete": len(selected) == group["count"],
            }
        )
    return result


def _run_command(root: Path, command: dict[str, Any], timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            command["argv"],
            cwd=root,
            check=False,
            text=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return _command_run_result(
            command,
            stdout_raw=result.stdout,
            stderr_raw=result.stderr,
            exit_code=result.returncode,
            execution_status="completed",
            timed_out=False,
            duration_ms=round((time.monotonic() - started) * 1000),
        )
    except subprocess.TimeoutExpired as exc:
        stdout_raw = exc.stdout or b""
        stderr_raw = exc.stderr or b""
        if isinstance(stdout_raw, str):
            stdout_raw = stdout_raw.encode("utf-8")
        if isinstance(stderr_raw, str):
            stderr_raw = stderr_raw.encode("utf-8")
        return _command_run_result(
            command,
            stdout_raw=stdout_raw,
            stderr_raw=stderr_raw,
            exit_code=None,
            execution_status="timed_out",
            timed_out=True,
            duration_ms=round((time.monotonic() - started) * 1000),
        )
    except OSError as exc:
        return _command_run_result(
            command,
            stdout_raw=b"",
            stderr_raw=str(exc).encode("utf-8"),
            exit_code=None,
            execution_status="launch_failed",
            timed_out=False,
            duration_ms=round((time.monotonic() - started) * 1000),
        )


def _command_run_result(
    command: dict[str, Any],
    *,
    stdout_raw: bytes,
    stderr_raw: bytes,
    exit_code: int | None,
    execution_status: str,
    timed_out: bool,
    duration_ms: int,
) -> dict[str, Any]:
    stdout = _capture_output(stdout_raw)
    stderr = _capture_output(stderr_raw)
    summaries = _command_summaries(command["summary_rules"], stdout["complete"], stderr["complete"])
    receipt = {
        "id": command["id"],
        "argv": command["argv"],
        "declared_dependencies": command["depends_on"],
        "exit_code": exit_code,
        "timed_out": timed_out,
        "execution_status": execution_status,
        "duration_ms": duration_ms,
        "stdout": stdout["preview"],
        "stderr": stderr["preview"],
        "stdout_sha256": stdout["preview_sha256"],
        "stderr_sha256": stderr["preview_sha256"],
        "stdout_complete_minimized_sha256": stdout["complete_minimized_sha256"],
        "stderr_complete_minimized_sha256": stderr["complete_minimized_sha256"],
        "stdout_redaction_count": stdout["redaction_count"],
        "stderr_redaction_count": stderr["redaction_count"],
        "stdout_capture": stdout["metadata"],
        "stderr_capture": stderr["metadata"],
        "summaries": summaries,
        "summary_coverage_complete": all(item["coverage_complete"] for item in summaries),
    }
    return {
        "receipt": receipt,
        "stdout_complete": stdout["complete"],
        "stderr_complete": stderr["complete"],
    }


def _coverage_gaps(
    tracked: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    commands: list[dict[str, Any]],
    samples: list[dict[str, Any]],
) -> list[str]:
    gaps = [
        "Collector reports objective repository evidence only; semantic support, consequence, and severity require independent review.",
        "Ignored and untracked files, private systems, runtime model selection, and external source truth are not inspected.",
    ]
    oversized = sum(1 for item in tracked if item["kind"] == "file" and item["bytes"] > MAX_TEXT_SCAN_BYTES)
    if oversized:
        gaps.append(f"{oversized} tracked file(s) exceeded the structured/text diagnostic size ceiling.")
    incomplete_commands = [item["id"] for item in commands if item["execution_status"] != "completed"]
    if incomplete_commands:
        gaps.append(f"Native command completion was not established for: {', '.join(incomplete_commands)}.")
    incomplete_summaries = [item["id"] for item in commands if not item["summary_coverage_complete"]]
    if incomplete_summaries:
        gaps.append(f"Required command summaries were unavailable for: {', '.join(incomplete_summaries)}.")
    incomplete = [item["id"] for item in samples if item["required"] and not item["selection_complete"]]
    if incomplete:
        gaps.append(f"Requested sample size was unavailable for: {', '.join(incomplete)}.")
    if any(item["category"].startswith("invalid-") for item in diagnostics):
        gaps.append("Invalid structured input may cause multiple dependent command failures; semantic review must avoid double-counting.")
    return gaps


@contextmanager
def _disposable_snapshot(root: Path, commit: str):
    archive = _git_bytes(root, "archive", "--format=tar", commit)
    with tempfile.TemporaryDirectory(prefix="anyang-cross-repo-audit-") as temporary:
        snapshot = Path(temporary) / "snapshot"
        snapshot.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
            members = bundle.getmembers()
            for member in members:
                path = PurePosixPath(member.name)
                if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
                    raise CrossRepoAuditError(f"Unsafe path in Git archive: {member.name}")
            try:
                bundle.extractall(snapshot, members=members, filter="data")
            except TypeError:
                if any(member.issym() or member.islnk() for member in members):
                    raise CrossRepoAuditError(
                        "This Python runtime cannot safely materialize archived symbolic links."
                    )
                bundle.extractall(snapshot, members=members)
        yield snapshot


def _collector_identity() -> dict[str, str]:
    source = Path(__file__).resolve()
    return {
        "name": "anyang-loop-cross-repo-audit",
        "version": COLLECTOR_VERSION,
        "source_sha256": _sha256(source.read_bytes()),
    }


def _parse_structured_text(suffix: str, text: str) -> None:
    normalized = text.lstrip("\ufeff")
    if suffix == ".json":
        json.loads(normalized)
    elif suffix in {".yaml", ".yml"}:
        yaml.safe_load(normalized)
    elif suffix == ".toml":
        tomllib.loads(normalized)


def _structured_error_evidence(
    exc: json.JSONDecodeError | yaml.YAMLError | tomllib.TOMLDecodeError,
) -> str:
    if isinstance(exc, json.JSONDecodeError):
        return f"{exc.msg} at line {exc.lineno}, column {exc.colno}."
    if isinstance(exc, tomllib.TOMLDecodeError):
        return str(exc)
    mark = getattr(exc, "problem_mark", None)
    problem = getattr(exc, "problem", None) or exc.__class__.__name__
    if mark is not None:
        return f"{problem} at line {mark.line + 1}, column {mark.column + 1}."
    return str(problem)


def _minimize_output(value: str) -> tuple[str, int]:
    redactions = 0

    def replace_assignment(match: re.Match[str]) -> str:
        nonlocal redactions
        redactions += 1
        return f"{match.group(1)}{match.group(2)}[REDACTED]"

    def replace_value(match: re.Match[str]) -> str:
        nonlocal redactions
        redactions += 1
        return "[REDACTED]"

    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = SECRET_ASSIGNMENT.sub(replace_assignment, value)
    value = SECRET_TOKEN.sub(replace_value, value)
    value = MACHINE_PATH_VALUE.sub(replace_value, value)
    return value, redactions


def _diagnostic(category: str, path: str, evidence: str, root_cause_id: str | None = None) -> dict[str, Any]:
    identity = f"{category}:{path}:{evidence}"
    return {
        "diagnostic_id": "diag-" + _sha256(identity.encode("utf-8"))[:12],
        "category": category,
        "path": path,
        "evidence": evidence,
        "root_cause_id": root_cause_id,
        "semantic_severity": None,
    }


def _tracked_fingerprint(inventory: list[dict[str, Any]]) -> str:
    return _sha256(_canonical_bytes(inventory))


def _count_by(items: list[dict[str, Any]], key: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        label = key(item)
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))


def _repository_root(path: Path) -> Path:
    candidate = path.resolve()
    result = subprocess.run(
        ["git", "-c", f"safe.directory={candidate}", "rev-parse", "--show-toplevel"],
        cwd=candidate,
        check=False,
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise CrossRepoAuditError(result.stderr.decode("utf-8", errors="replace").strip() or "Not a Git repository.")
    return Path(result.stdout.decode("utf-8", errors="replace").strip()).resolve()


def _git(root: Path, *args: str, allow_failure: bool = False) -> str:
    return _git_bytes(root, *args, allow_failure=allow_failure).decode("utf-8", errors="replace").strip("\0\r\n")


def _git_bytes(root: Path, *args: str, allow_failure: bool = False) -> bytes:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root}", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode and not allow_failure:
        raise CrossRepoAuditError(result.stderr.decode("utf-8", errors="replace").strip() or "Git command failed.")
    return result.stdout


def _repository_identity(root: Path) -> str:
    remote = _git(root, "config", "--get", "remote.origin.url", allow_failure=True).strip()
    if not remote:
        return root.name
    if "://" in remote:
        parsed = urlsplit(remote)
        host = parsed.hostname or ""
        port = f":{parsed.port}" if parsed.port else ""
        return urlunsplit((parsed.scheme.lower(), f"{host.lower()}{port}", parsed.path.rstrip("/"), "", ""))
    if "@" in remote and ":" in remote:
        remote = remote.split("@", 1)[1]
    return remote.rstrip("/")


def _git_paths(root: Path, *args: str) -> list[str]:
    return [part for part in _git(root, *args).split("\0") if part]


def _portable_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise CrossRepoAuditError(f"Unsafe tracked path: {path}")
    return pure.as_posix()


def _portable_glob(pattern: str) -> str:
    normalized = pattern.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized):
        raise CrossRepoAuditError(f"Unsafe sample glob: {pattern}")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise CrossRepoAuditError(f"Unsafe sample glob: {pattern}")
    return pure.as_posix()


def _rooted_glob_match(path: str, pattern: str) -> bool:
    path_parts = tuple(PurePosixPath(path).parts)
    pattern_parts = tuple(PurePosixPath(pattern).parts)

    @lru_cache(maxsize=None)
    def match(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        part = pattern_parts[pattern_index]
        if part == "**":
            return match(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and match(path_index + 1, pattern_index)
            )
        return (
            path_index < len(path_parts)
            and fnmatchcase(path_parts[path_index], part)
            and match(path_index + 1, pattern_index + 1)
        )

    return match(0, 0)


def _ensure_within(path: Path, root: Path) -> None:
    try:
        common = os.path.commonpath((str(path), str(root)))
    except ValueError as exc:
        raise CrossRepoAuditError("Path is outside the target repository.") from exc
    if common != str(root):
        raise CrossRepoAuditError("Path is outside the target repository.")


def _ensure_outside(path: Path, root: Path) -> None:
    try:
        common = os.path.commonpath((str(path), str(root)))
    except ValueError:
        return
    if common == str(root):
        raise CrossRepoAuditError("Collector output must be outside the target repository.")


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise CrossRepoAuditError(f"{field} must be a list of non-empty strings.")
    return value


def _capture_output(raw: bytes) -> dict[str, Any]:
    decoded = raw.decode("utf-8", errors="replace")
    minimized, redactions = _minimize_output(decoded)
    preview, omitted = _head_tail_preview(minimized)
    return {
        "complete": minimized,
        "preview": preview,
        "preview_sha256": _sha256(preview.encode("utf-8")),
        "complete_minimized_sha256": _sha256(minimized.encode("utf-8")),
        "redaction_count": redactions,
        "metadata": {
            "original_chars": len(decoded),
            "minimized_chars": len(minimized),
            "captured_chars": len(preview),
            "omitted_chars": omitted,
            "truncated": omitted > 0,
        },
    }


def _head_tail_preview(value: str) -> tuple[str, int]:
    return _bounded_head_tail_preview(value, MAX_CAPTURE_CHARS)


def _bounded_head_tail_preview(value: str, limit: int) -> tuple[str, int]:
    if len(value) <= limit:
        return value, 0
    marker = "\n[truncated]\n"
    content_budget = limit - len(marker)
    head_budget = content_budget // 2
    tail_budget = content_budget - head_budget
    head_end = value.rfind("\n", 0, head_budget + 1)
    if head_end < 1:
        head_end = head_budget
    else:
        head_end += 1
    tail_start = value.find("\n", len(value) - tail_budget)
    if tail_start < 0 or tail_start >= len(value) - 1:
        tail_start = len(value) - tail_budget
    else:
        tail_start += 1
    head = value[:head_end]
    tail = value[tail_start:]
    omitted = max(0, len(value) - len(head) - len(tail))
    return head + marker + tail, omitted


def _command_summaries(
    rules: list[dict[str, Any]],
    stdout: str,
    stderr: str,
) -> list[dict[str, Any]]:
    streams = {"stdout": stdout, "stderr": stderr}
    summaries: list[dict[str, Any]] = []
    for rule in rules:
        selected_streams = (
            ("stdout", "stderr")
            if rule["stream"] == "both"
            else (rule["stream"],)
        )
        match_count = 0
        examples: list[dict[str, Any]] = []
        truncated_example_count = 0
        for stream in selected_streams:
            for raw_line in io.StringIO(streams[stream]):
                line = raw_line.rstrip("\n")
                if not line.startswith(rule["line_prefix"]):
                    continue
                match_count += 1
                if len(examples) >= rule["max_examples"]:
                    continue
                preview, omitted = _bounded_head_tail_preview(
                    line,
                    MAX_SUMMARY_EXAMPLE_CHARS,
                )
                if omitted:
                    truncated_example_count += 1
                examples.append(
                    {
                        "stream": stream,
                        "line": preview,
                        "line_truncated": omitted > 0,
                        "original_chars": len(line),
                        "omitted_chars": omitted,
                        "complete_minimized_line_sha256": _sha256(line.encode("utf-8")),
                    }
                )
        summaries.append(
            {
                "id": rule["id"],
                "stream": rule["stream"],
                "line_prefix": rule["line_prefix"],
                "minimum_matches": rule["minimum_matches"],
                "match_count": match_count,
                "examples": examples,
                "examples_truncated": match_count > rule["max_examples"],
                "truncated_example_count": truncated_example_count,
                "coverage_complete": match_count >= rule["minimum_matches"],
            }
        )
    return summaries


def _collection_status(commands: list[dict[str, Any]], samples: list[dict[str, Any]]) -> str:
    commands_complete = all(
        item["execution_status"] == "completed" and item["summary_coverage_complete"]
        for item in commands
    )
    samples_complete = all(
        not item["required"] or item["selection_complete"]
        for item in samples
    )
    return "complete" if commands_complete and samples_complete else "partial"


def _write_receipt_atomic(output: Path, payload: bytes) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, output)
        except FileExistsError as exc:
            raise CrossRepoAuditError(f"Refusing to overwrite existing collector receipt: {output}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
