#!/usr/bin/env python3
"""Run a governed repository CLI through the external dependency environment."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "cli"))

from anyang_loop.runtime_bootstrap import RuntimeBootstrapError, resolve_validation_python  # noqa: E402


SURFACES = {
    "project": "anyang_loop.project_cli",
    "loop": "anyang_loop.cli",
    "ops": "anyang_loop.ops_cli",
    "coffee": "anyang_loop.coffee_cli",
    "dream": "anyang_loop.dream_cli",
}


def runtime_environment(repo_root: Path, environ: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if environ is None else environ)
    cli_path = str(repo_root / "cli")
    env["PYTHONPATH"] = cli_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def surface_command(python: Path, surface: str, arguments: list[str]) -> list[str]:
    try:
        module = SURFACES[surface]
    except KeyError as exc:
        raise ValueError(f"Unknown repo command surface: {surface}") from exc
    return [str(python), "-m", module, *arguments]


def run_surface(
    python: Path,
    surface: str,
    arguments: list[str],
    *,
    repo_root: Path = REPO_ROOT,
    environ: dict[str, str] | None = None,
    executor: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> int:
    result = executor(
        surface_command(python, surface, arguments),
        cwd=repo_root,
        env=runtime_environment(repo_root, environ),
        check=False,
    )
    return int(result.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an Anyang repository command with bootstrapped dependencies.")
    parser.add_argument("--refresh", action="store_true", help="Rebuild the current dependency-keyed environment")
    parser.add_argument("--cache-dir", type=Path, help="Override the external validation cache directory")
    parser.add_argument("surface", choices=tuple(SURFACES))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    try:
        local_python = REPO_ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
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
    return run_surface(python, args.surface, args.arguments)


if __name__ == "__main__":
    raise SystemExit(main())
