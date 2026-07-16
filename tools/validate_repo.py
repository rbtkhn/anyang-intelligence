#!/usr/bin/env python3
"""Bootstrap an external validation environment and run repo checks."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv


REPO_ROOT = Path(__file__).resolve().parents[1]
MINIMUM_PYTHON = (3, 10)
BOOTSTRAP_VERSION = 1


def _toml_string_array(text: str, section: str, key: str) -> list[str]:
    current_section = ""
    collecting = False
    buffer: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]") and not collecting:
            current_section = line[1:-1]
            continue
        if current_section != section:
            continue
        if not collecting:
            prefix = f"{key} ="
            if not line.startswith(prefix):
                continue
            line = line[len(prefix) :].strip()
            collecting = True
        buffer.append(line)
        if "]" in line:
            break

    if not buffer or "]" not in buffer[-1]:
        raise ValueError(f"Missing TOML string array: [{section}] {key}")
    value = ast.literal_eval("\n".join(buffer))
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Expected a string array: [{section}] {key}")
    return value


def validation_requirements(pyproject: Path) -> list[str]:
    text = pyproject.read_text(encoding="utf-8")
    runtime = _toml_string_array(text, "project", "dependencies")
    development = _toml_string_array(text, "project.optional-dependencies", "dev")
    return list(dict.fromkeys(runtime + development))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validation_cache_root(repo_root: Path, environ: dict[str, str] | None = None) -> Path:
    env = os.environ if environ is None else environ
    if env.get("ANYANG_VALIDATION_CACHE"):
        root = Path(env["ANYANG_VALIDATION_CACHE"]).expanduser()
    elif env.get("LOCALAPPDATA"):
        root = Path(env["LOCALAPPDATA"]) / "AnyangIntelligence" / "validation"
    elif env.get("XDG_CACHE_HOME"):
        root = Path(env["XDG_CACHE_HOME"]) / "anyang-intelligence" / "validation"
    else:
        root = Path.home() / ".cache" / "anyang-intelligence" / "validation"

    resolved = root.resolve()
    if _is_within(resolved, repo_root.resolve()):
        raise ValueError("Validation cache must remain outside the repository")
    return resolved


def validation_environment_path(repo_root: Path, cache_root: Path, requirements: list[str]) -> Path:
    repo_key = hashlib.sha256(str(repo_root.resolve()).encode("utf-8")).hexdigest()[:12]
    payload = {
        "bootstrap": BOOTSTRAP_VERSION,
        "python": list(sys.version_info[:2]),
        "platform": sys.platform,
        "requirements": requirements,
    }
    dependency_key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    version = f"py{sys.version_info.major}{sys.version_info.minor}"
    return cache_root / repo_key / f"{version}-{dependency_key}"


def environment_python(environment: Path) -> Path:
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_validation_environment(
    repo_root: Path,
    cache_root: Path,
    requirements: list[str],
    *,
    refresh: bool = False,
) -> Path:
    environment = validation_environment_path(repo_root, cache_root, requirements)
    python = environment_python(environment)
    marker = environment / ".anyang-validation.json"

    if refresh and environment.exists():
        shutil.rmtree(environment)
    if python.is_file() and marker.is_file():
        return python
    if environment.exists():
        shutil.rmtree(environment)

    environment.parent.mkdir(parents=True, exist_ok=True)
    print(f"Bootstrapping validation environment: {environment}", flush=True)
    venv.EnvBuilder(with_pip=True).create(environment)
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            *requirements,
        ],
        cwd=repo_root,
        check=True,
    )
    marker.write_text(
        json.dumps({"requirements": requirements, "source": "pyproject.toml"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return python


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


def run_validation(python: Path, repo_root: Path) -> None:
    env = os.environ.copy()
    cli_path = str(repo_root / "cli")
    env["PYTHONPATH"] = cli_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")

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

    if sys.version_info < MINIMUM_PYTHON:
        parser.error("Python 3.10 or newer is required")

    requirements = validation_requirements(REPO_ROOT / "pyproject.toml")
    cache_root = (
        args.cache_dir.expanduser().resolve()
        if args.cache_dir
        else validation_cache_root(REPO_ROOT)
    )
    if _is_within(cache_root, REPO_ROOT.resolve()):
        parser.error("Validation cache must remain outside the repository")

    python = ensure_validation_environment(
        REPO_ROOT,
        cache_root,
        requirements,
        refresh=args.refresh,
    )
    print(f"Validation Python: {python}")
    print(f"Dependency source: {REPO_ROOT / 'pyproject.toml'}")
    if not args.bootstrap_only:
        run_validation(python, REPO_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
