#!/usr/bin/env python3
"""Bootstrap an external validation environment and run repo checks."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


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


def validation_commands(python: Path, repo_root: Path) -> list[tuple[str, list[str]]]:
    project = [str(python), "-m", "anyang_loop.project_cli"]
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
                f"--basetemp={repo_root / '.pytest_cache' / 'validate-repo'}",
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


def runtime_environment(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    cli_path = str(repo_root / "cli")
    env["PYTHONPATH"] = cli_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def run_validation(python: Path, repo_root: Path) -> None:
    env = runtime_environment(repo_root)
    for label, command in validation_commands(python, repo_root):
        print(f"\n== {label} ==", flush=True)
        subprocess.run(command, cwd=repo_root, env=env, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap external Python dependencies and run CI-equivalent repository validation."
    )
    parser.add_argument("--bootstrap-only", action="store_true", help="Prepare and report the environment only")
    parser.add_argument("--refresh", action="store_true", help="Rebuild the current dependency-keyed environment")
    parser.add_argument("--cache-dir", type=Path, help="Override the external validation cache directory")
    args = parser.parse_args(argv)

    try:
        ensure_supported_python()
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
            run_validation(python, REPO_ROOT)
        except subprocess.CalledProcessError as exc:
            return exc.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
