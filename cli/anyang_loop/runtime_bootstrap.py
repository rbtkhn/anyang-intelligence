"""Dependency-free runtime bootstrap for repository commands and validation."""

from __future__ import annotations

import ast
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import time
from typing import Callable, Iterator, Mapping
import uuid
import venv


MINIMUM_PYTHON = (3, 10)
BOOTSTRAP_VERSION = 1
Reporter = Callable[[str], None]


class RuntimeBootstrapError(RuntimeError):
    """Raised when the governed external runtime cannot be prepared."""


def ensure_supported_python(version: tuple[int, int] | None = None) -> None:
    current = version or tuple(sys.version_info[:2])
    if current < MINIMUM_PYTHON:
        raise RuntimeBootstrapError("Python 3.10 or newer is required")


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
        raise RuntimeBootstrapError(f"Missing TOML string array: [{section}] {key}")
    try:
        value = ast.literal_eval("\n".join(buffer))
    except (SyntaxError, ValueError) as exc:
        raise RuntimeBootstrapError(f"Invalid TOML string array: [{section}] {key}") from exc
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RuntimeBootstrapError(f"Expected a string array: [{section}] {key}")
    return value


def validation_requirements(pyproject: Path) -> list[str]:
    text = pyproject.read_text(encoding="utf-8")
    runtime = _toml_string_array(text, "project", "dependencies")
    development = _toml_string_array(text, "project.optional-dependencies", "dev")
    return list(dict.fromkeys(runtime + development))


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validation_cache_root(
    repo_root: Path,
    environ: Mapping[str, str] | None = None,
) -> Path:
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
    if is_within(resolved, repo_root.resolve()):
        raise RuntimeBootstrapError("Validation cache must remain outside the repository")
    return resolved


def validation_environment_path(repo_root: Path, cache_root: Path, requirements: list[str]) -> Path:
    repo_key = hashlib.sha256(str(repo_root.resolve()).encode("utf-8")).hexdigest()[:12]
    payload = {
        "bootstrap": BOOTSTRAP_VERSION,
        "runtime": environment_fingerprint(),
        "platform": sys.platform,
        "requirements": requirements,
    }
    dependency_key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    version = f"py{sys.version_info.major}{sys.version_info.minor}"
    return cache_root / repo_key / f"{version}-{dependency_key}"


def environment_fingerprint() -> dict[str, object]:
    """Return stable interpreter traits that determine virtualenv compatibility."""
    base_executable = getattr(sys, "_base_executable", None) or sys.executable
    return {
        "implementation": sys.implementation.name,
        "cache_tag": sys.implementation.cache_tag,
        "version": list(sys.version_info[:3]),
        "platform": sysconfig.get_platform(),
        "base_executable": str(Path(base_executable).resolve()),
    }


def environment_python(environment: Path) -> Path:
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _marker_matches(marker: Path, requirements: list[str]) -> bool:
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return False
    return data.get("requirements") == requirements and data.get("source") == "pyproject.toml"


def _environment_is_valid(environment: Path, requirements: list[str]) -> bool:
    return environment_python(environment).is_file() and _marker_matches(
        environment / ".anyang-validation.json",
        requirements,
    )


@contextmanager
def environment_lock(
    environment: Path,
    *,
    timeout_seconds: float = 180.0,
    poll_seconds: float = 0.1,
    stale_after_seconds: float = 900.0,
) -> Iterator[None]:
    lock = environment.with_name(environment.name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    descriptor: int | None = None

    while descriptor is None:
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(descriptor, f"pid={os.getpid()} created={time.time()}\n".encode("utf-8"))
        except FileExistsError:
            try:
                age = time.time() - lock.stat().st_mtime
                if age > stale_after_seconds:
                    lock.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() - started >= timeout_seconds:
                raise RuntimeBootstrapError(f"Timed out waiting for runtime lock: {lock}")
            time.sleep(poll_seconds)

    try:
        yield
    finally:
        os.close(descriptor)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def _create_venv(path: Path) -> None:
    venv.EnvBuilder(with_pip=True).create(path)


def _install_requirements(python: Path, requirements: list[str], repo_root: Path) -> None:
    result = subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            *requirements,
        ],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-20:])
        raise RuntimeBootstrapError(f"Dependency installation failed.\n{tail}".rstrip())


def ensure_validation_environment(
    repo_root: Path,
    cache_root: Path,
    requirements: list[str],
    *,
    refresh: bool = False,
    reporter: Reporter | None = None,
    create_environment: Callable[[Path], None] | None = None,
    install_requirements: Callable[[Path, list[str], Path], None] | None = None,
    lock_timeout_seconds: float = 180.0,
) -> Path:
    environment = validation_environment_path(repo_root, cache_root, requirements)
    if not refresh and _environment_is_valid(environment, requirements):
        return environment_python(environment)

    report = reporter or (lambda _message: None)
    create = create_environment or _create_venv
    install = install_requirements or _install_requirements

    with environment_lock(environment, timeout_seconds=lock_timeout_seconds):
        if not refresh and _environment_is_valid(environment, requirements):
            return environment_python(environment)
        if environment.exists():
            shutil.rmtree(environment)

        temporary = environment.with_name(f"{environment.name}.tmp-{os.getpid()}-{uuid.uuid4().hex[:8]}")
        try:
            report(f"Bootstrapping validation environment: {environment}")
            create(temporary)
            temporary_python = environment_python(temporary)
            install(temporary_python, requirements, repo_root)
            (temporary / ".anyang-validation.json").write_text(
                json.dumps({"requirements": requirements, "source": "pyproject.toml"}, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary.replace(environment)
        except Exception as exc:
            if temporary.exists():
                shutil.rmtree(temporary, ignore_errors=True)
            if isinstance(exc, RuntimeBootstrapError):
                raise
            raise RuntimeBootstrapError(f"Unable to bootstrap validation environment: {exc}") from exc
    return environment_python(environment)


def resolve_validation_python(
    repo_root: Path,
    *,
    cache_dir: Path | None = None,
    refresh: bool = False,
    reporter: Reporter | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    ensure_supported_python()
    root = repo_root.resolve()
    requirements = validation_requirements(root / "pyproject.toml")
    cache_root = cache_dir.expanduser().resolve() if cache_dir else validation_cache_root(root, environ)
    if is_within(cache_root, root):
        raise RuntimeBootstrapError("Validation cache must remain outside the repository")
    return ensure_validation_environment(
        root,
        cache_root,
        requirements,
        refresh=refresh,
        reporter=reporter,
    )
