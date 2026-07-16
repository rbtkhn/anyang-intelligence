from __future__ import annotations

import py_compile
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .privacy_scan import scan_repo
from .repo_snapshot import RepoSnapshot
from .runtime_bootstrap import RuntimeBootstrapError, resolve_validation_python


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    exit_code: int | None
    duration_ms: int
    summary: str

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "exit_code": self.exit_code,
            "duration_ms": self.duration_ms,
            "summary": self.summary,
        }


CommandRunner = Callable[[Path, list[str]], tuple[int, str, str]]
RuntimeResolver = Callable[[Path], Path]


def run_verification(
    snapshot: RepoSnapshot,
    mode: str,
    *,
    command_runner: CommandRunner | None = None,
    runtime_resolver: RuntimeResolver | None = None,
) -> list[CheckResult]:
    if mode not in {"fast", "full", "none"}:
        raise ValueError(f"Unknown verification mode: {mode}")
    if mode == "none":
        return [CheckResult("verification", "skipped", None, 0, "Verification intentionally skipped.")]
    runner = command_runner or _run_command
    results = [
        _command_check("git-diff-check", snapshot.root, ["git", "diff", "--check"], runner),
        _privacy_check(snapshot.root),
        _compile_check(snapshot),
    ]
    if mode == "full":
        resolver = runtime_resolver or _resolve_runtime_python
        started = time.perf_counter()
        try:
            validation_python = resolver(snapshot.root)
        except (OSError, RuntimeError, ValueError) as exc:
            results.append(
                CheckResult(
                    "validation-runtime",
                    "unavailable",
                    None,
                    _elapsed(started),
                    f"Validation runtime unavailable: {type(exc).__name__}: {exc}",
                )
            )
            return results
        results.extend(
            [
                _command_check(
                    "pytest",
                    snapshot.root,
                    [
                        str(validation_python),
                        "-m",
                        "pytest",
                        "-q",
                        "--basetemp",
                        str(snapshot.root / ".pytest_cache" / "dream-full"),
                    ],
                    runner,
                ),
                _command_check(
                    "install-validation",
                    snapshot.root,
                    [str(validation_python), "-m", "anyang_loop.project_cli", "validate", "projects"],
                    runner,
                ),
                _command_check(
                    "loop-validation",
                    snapshot.root,
                    [str(validation_python), "-m", "anyang_loop.cli", "validate", "projects"],
                    runner,
                ),
            ]
        )
    return results


def _resolve_runtime_python(root: Path) -> Path:
    return resolve_validation_python(
        root,
        reporter=lambda message: print(message, file=sys.stderr, flush=True),
    )


def validation_status(results: list[CheckResult]) -> str:
    statuses = {result.status for result in results}
    if "fail" in statuses:
        return "fail"
    if statuses == {"skipped"}:
        return "skipped"
    if "unavailable" in statuses:
        return "partial"
    return "pass"


def _command_check(name: str, root: Path, command: list[str], runner: CommandRunner) -> CheckResult:
    started = time.perf_counter()
    try:
        code, stdout, stderr = runner(root, command)
    except OSError as exc:
        return CheckResult(name, "unavailable", None, _elapsed(started), f"Command unavailable: {type(exc).__name__}")
    combined = "\n".join(part for part in (stdout.strip(), stderr.strip()) if part)
    if code == 0:
        summary = _bounded_summary(combined) or "Completed successfully."
        return CheckResult(name, "pass", 0, _elapsed(started), summary)
    if "No module named" in combined or "not recognized" in combined or "not found" in combined:
        return CheckResult(name, "unavailable", code, _elapsed(started), "Required command or dependency is unavailable.")
    return CheckResult(name, "fail", code, _elapsed(started), _bounded_summary(combined) or "Command failed.")


def _privacy_check(root: Path) -> CheckResult:
    started = time.perf_counter()
    try:
        findings = scan_repo(root)
    except (OSError, RuntimeError) as exc:
        return CheckResult("privacy-scan", "unavailable", None, _elapsed(started), f"Privacy scan unavailable: {type(exc).__name__}")
    if findings:
        rules = sorted({finding.rule for finding in findings})
        return CheckResult(
            "privacy-scan",
            "fail",
            1,
            _elapsed(started),
            f"{len(findings)} finding(s) across rule(s): {', '.join(rules)}.",
        )
    return CheckResult("privacy-scan", "pass", 0, _elapsed(started), "No prohibited tracked content found.")


def _compile_check(snapshot: RepoSnapshot) -> CheckResult:
    started = time.perf_counter()
    paths = [snapshot.root / path for path in snapshot.changed_paths if path.endswith(".py") and (snapshot.root / path).is_file()]
    if not paths:
        return CheckResult("python-compile", "pass", 0, _elapsed(started), "No changed Python files.")
    failures: list[str] = []
    for path in paths:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError:
            failures.append(path.relative_to(snapshot.root).as_posix())
    if failures:
        return CheckResult("python-compile", "fail", 1, _elapsed(started), f"Compilation failed for {len(failures)} changed file(s).")
    return CheckResult("python-compile", "pass", 0, _elapsed(started), f"Compiled {len(paths)} changed Python file(s).")


def _run_command(root: Path, command: list[str]) -> tuple[int, str, str]:
    env = os.environ.copy()
    cli_path = str(root / "cli")
    env["PYTHONPATH"] = cli_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    result = subprocess.run(
        command,
        cwd=root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode, result.stdout, result.stderr


def _elapsed(started: float) -> int:
    return max(0, round((time.perf_counter() - started) * 1000))


def _bounded_summary(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return ""
    summary = " | ".join(lines[:3])
    return summary[:400]
