#!/usr/bin/env python3
"""Bootstrap an external validation environment and run repo checks."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "cli"))

from anyang_loop.runtime_bootstrap import (  # noqa: E402
    MINIMUM_PYTHON,
    RuntimeBootstrapError,
    ensure_supported_python,
    ensure_validation_environment,
    environment_python,
    is_within as _is_within,
    resolve_validation_python,
    validation_cache_root,
    validation_environment_path,
    validation_requirements,
)
from anyang_loop.validation_evidence import (  # noqa: E402
    VALIDATION_POLICY_VERSION,
    repository_fingerprint,
    repository_validation_python,
)


FULL_ONLY_PREFIXES = ("cli/", "tools/", ".github/")
FULL_ONLY_PATHS = {
    "AGENTS.md",
    "pyproject.toml",
    "tests/conftest.py",
    "tests/test_cross_repo_audit.py",
    "tests/test_pytest_temp_config.py",
    "tests/test_runtime_guidance.py",
    "tests/test_validation_bootstrap.py",
}
PROJECT_TEST_ROUTES = {
    "book-club": ("tests/test_business_loop_contract.py",),
    "game-design": ("tests/test_game_design_contract.py", "tests/test_game_design_project_contract.py"),
    "grace-gems": ("tests/test_business_intake_contract.py", "tests/test_executive_interface_protocol.py"),
    "learning-core": ("tests/test_business_loop_contract.py",),
    "media-production": (
        "tests/test_artistic_director_ai_factory_schema.py",
        "tests/test_artistic_director_governance.py",
    ),
    "mountain-villa": ("tests/test_business_intake_contract.py",),
    "singularity-science": (
        "tests/test_singularity_intake_validate.py",
        "tests/test_singularity_science_skill.py",
    ),
}
PREFIX_TEST_ROUTES = (
    ("skills/coffee/", ("tests/test_coffee_continuity_contract.py",)),
    ("skills/decision-audit/", ("tests/test_decision_audit_contract.py",)),
    ("skills/dream/", ("tests/test_dream_discovery_contract.py",)),
    ("skills/elicitation/", ("tests/test_elicitation_contract.py",)),
    ("skills/game-design/", ("tests/test_game_design_contract.py",)),
    ("skills/learn-from-choices/", ("tests/test_learn_from_choices_contract.py",)),
    ("skills/singularity", ("tests/test_singularity_science_skill.py",)),
)
EXACT_TEST_ROUTES = {
    "memory-constitution.yaml": ("tests/test_memory_contract.py",),
    "os/recursive-learning-ledger.md": ("tests/test_recursive_learning_ledger.py",),
}
GOVERNED_FILE_ROUTES = {
    "analytical-interfaces.yaml": ("analytical interfaces", "tests/test_analytical_interfaces.py"),
    "artifact-state.yaml": ("artifact state", "tests/test_artifact_state.py"),
    "authority-envelope.yaml": ("bounded agency", "tests/test_authority.py"),
    "bounded-agency.yaml": ("bounded agency", "tests/test_bounded_agency.py"),
    "epistemic-state.yaml": ("epistemic state", "tests/test_epistemic_state.py"),
}
FAST_CONTENT_PREFIXES = ("archive/", "docs/", "playbooks/", "skills/", "templates/")


def validation_commands(python: Path, repo_root: Path) -> list[tuple[str, list[str]]]:
    project = [str(python), "-m", "anyang_loop.project_cli"]
    pytest_base = repo_root / ".pytest_cache" / f"validate-repo-{os.getpid()}"
    return [
        (
            "pytest",
            [
                str(python),
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                f"--basetemp={pytest_base}",
            ],
        ),
        ("project installs", project + ["validate", "projects"]),
        ("loop fixtures", [str(python), "-m", "anyang_loop.cli", "validate", "projects"]),
        ("analytical interfaces", project + ["validate-interfaces"]),
        ("artifact state", project + ["validate-artifacts"]),
        ("bounded agency", project + ["validate-agency"]),
        ("epistemic state", project + ["validate-epistemics"]),
        ("epistemic report", project + ["epistemic-report"]),
        ("privacy scan", [str(python), "-m", "anyang_loop.ops_cli", "privacy-scan", "--repo", "."]),
    ]


def _git(repo_root: Path, *args: str, text: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def repository_changes(repo_root: Path) -> list[dict[str, str]]:
    """Return tracked and untracked changes without losing spaces in paths."""
    output = _git(
        repo_root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    ).stdout
    assert isinstance(output, bytes)
    records = output.decode("utf-8", errors="surrogateescape").split("\0")
    changes: list[dict[str, str]] = []
    index = 0
    while index < len(records) and records[index]:
        record = records[index]
        if len(record) < 4:
            raise RuntimeError(f"Unexpected git status record: {record!r}")
        status = record[:2]
        path = record[3:].replace("\\", "/")
        change = {"status": status, "path": path}
        if "R" in status or "C" in status:
            index += 1
            if index >= len(records) or not records[index]:
                raise RuntimeError("Git rename/copy status omitted its source path")
            change["source_path"] = records[index].replace("\\", "/")
        changes.append(change)
        index += 1
    return changes


def plan_fast_validation(changes: list[dict[str, str]]) -> dict[str, Any]:
    tests: set[str] = set()
    validators: set[str] = set()
    reasons: list[str] = []

    if not changes:
        return {"effective_mode": "fast", "tests": [], "validators": [], "reasons": ["working tree is clean"]}

    for change in changes:
        status = change["status"]
        path = change["path"]
        if any(marker in status for marker in ("D", "R", "C", "U")):
            reasons.append(f"{path}: status {status!r} requires repository-wide validation")
            continue
        if path in FULL_ONLY_PATHS or path.startswith(FULL_ONLY_PREFIXES):
            reasons.append(f"{path}: validation-critical path")
            continue
        if path.startswith("tests/") and path.endswith(".py"):
            tests.add(path)
            continue
        if path in EXACT_TEST_ROUTES:
            tests.update(EXACT_TEST_ROUTES[path])
            continue
        if path.startswith("projects/"):
            parts = path.split("/")
            project = parts[1] if len(parts) > 1 else ""
            routed = PROJECT_TEST_ROUTES.get(project)
            if not routed:
                reasons.append(f"{path}: project has no explicit test route")
                continue
            tests.update(routed)
            validators.update(("project installs", "loop fixtures"))
            continue
        if path in GOVERNED_FILE_ROUTES:
            validator, test = GOVERNED_FILE_ROUTES[path]
            validators.add(validator)
            tests.add(test)
            continue
        if path == "README.md":
            tests.update(("tests/test_runtime_guidance.py", "tests/test_validation_bootstrap.py"))
            continue
        if path.startswith(FAST_CONTENT_PREFIXES):
            for prefix, routed in PREFIX_TEST_ROUTES:
                if path.startswith(prefix):
                    tests.update(routed)
            continue
        reasons.append(f"{path}: unclassified path")

    effective_mode = "full" if reasons and reasons != ["working tree is clean"] else "fast"
    return {
        "effective_mode": effective_mode,
        "tests": sorted(tests),
        "validators": sorted(validators),
        "reasons": reasons,
    }


def fast_validation_commands(
    python: Path,
    repo_root: Path,
    tests: list[str],
    validators: list[str],
) -> list[tuple[str, list[str]]]:
    full = dict(validation_commands(python, repo_root))
    commands: list[tuple[str, list[str]]] = [
        ("diff integrity", ["git", "diff", "--check", "HEAD", "--"]),
    ]
    if tests:
        pytest_base = repo_root / ".pytest_cache" / f"validate-fast-{os.getpid()}"
        commands.append(
            (
                "focused pytest",
                [
                    str(python),
                    "-m",
                    "pytest",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    f"--basetemp={pytest_base}",
                    *tests,
                ],
            )
        )
    for label in (
        "project installs",
        "loop fixtures",
        "analytical interfaces",
        "artifact state",
        "bounded agency",
        "epistemic state",
        "epistemic report",
    ):
        if label in validators:
            commands.append((label, full[label]))
    commands.append(("privacy scan", full["privacy scan"]))
    return commands


def runtime_environment(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    cli_path = str(repo_root / "cli")
    env["PYTHONPATH"] = cli_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def run_validation(
    python: Path,
    repo_root: Path,
    commands: list[tuple[str, list[str]]] | None = None,
) -> dict[str, float]:
    # Pytest accepts a missing --basetemp directory, but its parent must exist.
    # Fresh CI checkouts do not contain ignored .pytest_cache state.
    (repo_root / ".pytest_cache").mkdir(parents=True, exist_ok=True)
    env = runtime_environment(repo_root)
    timings: dict[str, float] = {}
    started = time.perf_counter()
    for label, command in commands or validation_commands(python, repo_root):
        print(f"\n== {label} ==", flush=True)
        phase_started = time.perf_counter()
        try:
            subprocess.run(command, cwd=repo_root, env=env, check=True)
        finally:
            duration = time.perf_counter() - phase_started
            timings[label] = duration
            print(f"Duration: {duration:.3f}s", flush=True)
    print(f"\nValidation duration: {time.perf_counter() - started:.3f}s", flush=True)
    return timings


def _cache_path(repo_root: Path) -> Path:
    return repo_root / ".pytest_cache" / "validation-results.json"


def cached_full_result(repo_root: Path, fingerprint: str) -> dict[str, Any] | None:
    path = _cache_path(repo_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    result = payload.get("full") if isinstance(payload, dict) else None
    if isinstance(result, dict) and result.get("fingerprint") == fingerprint:
        return result
    return None


def record_full_result(repo_root: Path, fingerprint: str, timings: dict[str, float]) -> None:
    path = _cache_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": VALIDATION_POLICY_VERSION,
        "full": {
            "fingerprint": fingerprint,
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "timings_seconds": {label: round(value, 6) for label, value in timings.items()},
        },
    }
    temporary = path.with_name(f"{path.name}.tmp-{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap external Python dependencies and run CI-equivalent repository validation."
    )
    parser.add_argument("--bootstrap-only", action="store_true", help="Prepare and report the environment only")
    parser.add_argument("--refresh", action="store_true", help="Rebuild the current dependency-keyed environment")
    parser.add_argument("--cache-dir", type=Path, help="Override the external validation cache directory")
    parser.add_argument(
        "--mode",
        choices=("full", "fast"),
        default="full",
        help="Run the full inventory (default) or a change-routed fast gate",
    )
    parser.add_argument("--force", action="store_true", help="Rerun Full even when this tree fingerprint passed")
    args = parser.parse_args(argv)

    try:
        ensure_supported_python()
        local_python = repository_validation_python(REPO_ROOT)
        if local_python.is_file() and not args.refresh and not args.cache_dir:
            python = local_python
        else:
            python = resolve_validation_python(
                REPO_ROOT,
                cache_dir=args.cache_dir,
                refresh=args.refresh,
                reporter=lambda message: print(message, file=sys.stderr, flush=True),
            )
    except (OSError, RuntimeBootstrapError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Validation Python: {python}")
    print(f"Dependency source: {REPO_ROOT / 'pyproject.toml'}")
    if not args.bootstrap_only:
        try:
            changes = repository_changes(REPO_ROOT)
            fingerprint = repository_fingerprint(REPO_ROOT, python)
            effective_mode = args.mode
            commands = None
            if args.mode == "fast":
                plan = plan_fast_validation(changes)
                effective_mode = plan["effective_mode"]
                print("Changed paths:")
                for change in changes:
                    print(f"  {change['status']} {change['path']}")
                if effective_mode == "full":
                    print("Fast gate escalated to Full:")
                    for reason in plan["reasons"]:
                        print(f"  - {reason}")
                else:
                    print("Fast gate selected tests:")
                    for test in plan["tests"]:
                        print(f"  - {test}")
                    print("Fast gate selected validators:")
                    for validator in plan["validators"]:
                        print(f"  - {validator}")
                    commands = fast_validation_commands(
                        python,
                        REPO_ROOT,
                        plan["tests"],
                        plan["validators"],
                    )

            print(f"Validation mode: {effective_mode.title()}")
            print(f"Tree fingerprint: {fingerprint}")
            if effective_mode == "full" and not args.force:
                cached = cached_full_result(REPO_ROOT, fingerprint)
                if cached:
                    print(
                        "Full validation already passed for this exact tree "
                        f"at {cached.get('completed_at', 'an unknown time')}. Use --force to rerun."
                    )
                    return 0

            timings = run_validation(python, REPO_ROOT, commands)
            if effective_mode == "full":
                record_full_result(REPO_ROOT, fingerprint, timings)
        except subprocess.CalledProcessError as exc:
            return exc.returncode or 1
        except (OSError, RuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
