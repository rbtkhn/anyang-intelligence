import importlib.util
import json
import os
from pathlib import Path
import time

import pytest

from anyang_loop.runtime_bootstrap import (
    RuntimeBootstrapError,
    ensure_supported_python,
    ensure_validation_environment,
    environment_fingerprint,
    environment_lock,
    environment_python,
    validation_environment_path,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_repo.py"
POWERSHELL = ROOT / "tools/validate.ps1"
PYTHON_LAUNCHER = ROOT / "tools/python_launcher.ps1"


def load_bootstrap():
    spec = importlib.util.spec_from_file_location("validate_repo", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_requirements_come_from_pyproject_without_third_party_toml_parser():
    module = load_bootstrap()
    requirements = module.validation_requirements(ROOT / "pyproject.toml")
    assert "PyYAML>=6.0" in requirements
    assert "pytest>=8.0" in requirements


def test_validation_cache_refuses_repo_local_dependencies():
    module = load_bootstrap()
    with pytest.raises(RuntimeBootstrapError, match="outside the repository"):
        module.validation_cache_root(ROOT, {"ANYANG_VALIDATION_CACHE": str(ROOT / ".dependencies")})


def test_validation_environment_is_keyed_by_repo_python_and_dependencies(tmp_path: Path):
    module = load_bootstrap()
    first = module.validation_environment_path(ROOT, tmp_path, ["PyYAML>=6.0", "pytest>=8.0"])
    second = module.validation_environment_path(ROOT, tmp_path, ["PyYAML>=6.0", "pytest>=9.0"])
    assert first.parent == second.parent
    assert first != second
    assert first.name.startswith(f"py{module.sys.version_info.major}{module.sys.version_info.minor}-")


def test_environment_fingerprint_captures_interpreter_compatibility():
    fingerprint = environment_fingerprint()
    assert fingerprint["implementation"]
    assert fingerprint["cache_tag"]
    assert fingerprint["version"][:2] == list(__import__("sys").version_info[:2])
    assert Path(str(fingerprint["base_executable"])).is_absolute()


def test_environment_fingerprint_is_stable_inside_a_virtual_environment(monkeypatch):
    import sys

    base = Path(sys.executable).resolve()
    monkeypatch.setattr(sys, "_base_executable", str(base), raising=False)
    first = environment_fingerprint()
    monkeypatch.setattr(sys, "executable", str(ROOT / "synthetic-venv" / "python"))
    second = environment_fingerprint()
    assert first == second


def test_validation_command_set_matches_ci_controls():
    module = load_bootstrap()
    commands = module.validation_commands(Path("python"), ROOT)
    labels = [label for label, _ in commands]
    assert labels == [
        "pytest",
        "project installs",
        "loop fixtures",
        "analytical interfaces",
        "artifact state",
        "bounded agency",
        "epistemic state",
        "epistemic report",
        "privacy scan",
    ]
    pytest_command = commands[0][1]
    assert "no:cacheprovider" in pytest_command
    assert pytest_command[-1] == f"--basetemp={ROOT / '.pytest_cache' / f'validate-repo-{os.getpid()}'}"


def test_fast_plan_routes_project_content_and_its_explicit_test():
    module = load_bootstrap()
    plan = module.plan_fast_validation(
        [
            {"status": " M", "path": "projects/media-production/artistic-production-gate.md"},
            {"status": " M", "path": "tests/test_artistic_director_governance.py"},
        ]
    )

    assert plan["effective_mode"] == "fast"
    assert plan["validators"] == ["loop fixtures", "project installs"]
    assert plan["tests"] == [
        "tests/test_artistic_director_ai_factory_schema.py",
        "tests/test_artistic_director_governance.py",
    ]
    assert plan["reasons"] == []


def test_fast_plan_routes_recursive_learning_ledger_to_its_contract_test():
    module = load_bootstrap()
    plan = module.plan_fast_validation(
        [{"status": " M", "path": "os/recursive-learning-ledger.md"}]
    )

    assert plan == {
        "effective_mode": "fast",
        "tests": ["tests/test_recursive_learning_ledger.py"],
        "validators": [],
        "reasons": [],
    }


def test_fast_plan_routes_decision_audit_to_its_contract_test():
    module = load_bootstrap()
    plan = module.plan_fast_validation(
        [{"status": " M", "path": "skills/decision-audit/SKILL.md"}]
    )

    assert plan == {
        "effective_mode": "fast",
        "tests": ["tests/test_decision_audit_contract.py"],
        "validators": [],
        "reasons": [],
    }


@pytest.mark.parametrize(
    ("status", "path", "reason"),
    [
        (" M", "tools/validate_repo.py", "validation-critical"),
        (" M", "unclassified.bin", "unclassified"),
        (" M", "os/learning-loop.md", "unclassified"),
        (" D", "docs/removed.md", "requires repository-wide"),
        (" D", "os/recursive-learning-ledger.md", "requires repository-wide"),
        ("R ", "docs/renamed.md", "requires repository-wide"),
    ],
)
def test_fast_plan_escalates_risky_or_unknown_changes(status, path, reason):
    module = load_bootstrap()
    plan = module.plan_fast_validation([{"status": status, "path": path}])

    assert plan["effective_mode"] == "full"
    assert reason in plan["reasons"][0]


def test_fast_commands_are_focused_and_retain_privacy_and_integrity():
    module = load_bootstrap()
    commands = module.fast_validation_commands(
        Path("python"),
        ROOT,
        ["tests/test_artistic_director_governance.py"],
        ["loop fixtures", "project installs"],
    )
    labels = [label for label, _ in commands]

    assert labels == [
        "diff integrity",
        "focused pytest",
        "project installs",
        "loop fixtures",
        "privacy scan",
    ]
    focused = commands[1][1]
    assert "tests/test_artistic_director_governance.py" in focused
    assert "tests/test_cross_repo_audit.py" not in focused


def test_full_result_cache_is_bound_to_exact_fingerprint(tmp_path: Path):
    module = load_bootstrap()
    module.record_full_result(tmp_path, "tree-a", {"pytest": 1.25})

    cached = module.cached_full_result(tmp_path, "tree-a")
    assert cached is not None
    assert cached["timings_seconds"] == {"pytest": 1.25}
    assert module.cached_full_result(tmp_path, "tree-b") is None
    payload = json.loads((tmp_path / ".pytest_cache" / "validation-results.json").read_text())
    assert payload["version"] == module.VALIDATION_POLICY_VERSION


def test_python_launcher_prefers_bundled_dependency_aware_runtime():
    launcher = PYTHON_LAUNCHER.read_text(encoding="utf-8")

    bundled_marker = "$codexPython = Join-Path $env:USERPROFILE"
    path_marker = "$pathPython = Get-Command python"
    assert bundled_marker in launcher
    assert path_marker in launcher
    assert launcher.index(bundled_marker) < launcher.index(path_marker)


def test_run_validation_prepares_pytest_parent_in_fresh_checkout(tmp_path: Path, monkeypatch):
    module = load_bootstrap()
    repo_root = tmp_path / "fresh-checkout"
    repo_root.mkdir()
    calls = []

    def fake_run(command, *, cwd, env, check):
        assert (repo_root / ".pytest_cache").is_dir()
        calls.append((command, cwd, env, check))

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module.run_validation(Path("python"), repo_root)

    assert len(calls) == len(module.validation_commands(Path("python"), repo_root))
    assert calls[0][0][-1] == (
        f"--basetemp={repo_root / '.pytest_cache' / f'validate-repo-{os.getpid()}'}"
    )


def test_windows_launcher_has_stable_overrides_and_codex_fallback():
    launcher = POWERSHELL.read_text(encoding="utf-8")
    resolver = PYTHON_LAUNCHER.read_text(encoding="utf-8")
    assert "ANYANG_PYTHON" in resolver
    assert ".cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" in resolver
    assert "validate_repo.py" in launcher
    assert "python_launcher.ps1" in launcher
    assert "[switch]$BootstrapOnly" in launcher
    assert "[switch]$Refresh" in launcher
    assert "[ValidateSet('Full', 'Fast')]" in launcher
    assert "[switch]$Force" in launcher
    assert "@('--mode', $Mode.ToLowerInvariant())" in launcher
    assert "$env:USERPROFILE" in resolver
    assert "$pathPython.Source -and" in resolver


def test_readme_exposes_one_command_local_validation():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert ".\\tools\\validate.ps1" in readme
    assert "python3 tools/validate_repo.py" in readme


def _fake_environment(path: Path) -> None:
    python = environment_python(path)
    python.parent.mkdir(parents=True, exist_ok=True)
    python.write_text("synthetic python\n", encoding="utf-8")


def _fake_install(_python: Path, _requirements: list[str], _repo_root: Path) -> None:
    return None


def test_python_version_is_enforced_before_bootstrap():
    with pytest.raises(RuntimeBootstrapError, match="3.10"):
        ensure_supported_python((3, 9))
    ensure_supported_python((3, 10))


def test_partial_environment_is_replaced_atomically(tmp_path: Path):
    requirements = ["PyYAML>=6.0", "pytest>=8.0"]
    environment = validation_environment_path(ROOT, tmp_path, requirements)
    environment.mkdir(parents=True)
    (environment / "partial.txt").write_text("partial\n", encoding="utf-8")

    python = ensure_validation_environment(
        ROOT,
        tmp_path,
        requirements,
        create_environment=_fake_environment,
        install_requirements=_fake_install,
    )

    assert python == environment_python(environment)
    assert python.is_file()
    assert not (environment / "partial.txt").exists()
    assert not list(environment.parent.glob(environment.name + ".tmp-*"))


def test_valid_environment_is_reused_without_installing(tmp_path: Path):
    requirements = ["PyYAML>=6.0", "pytest>=8.0"]
    first = ensure_validation_environment(
        ROOT,
        tmp_path,
        requirements,
        create_environment=_fake_environment,
        install_requirements=_fake_install,
    )

    def unexpected(*_args):
        raise AssertionError("cached environments must not reinstall")

    second = ensure_validation_environment(
        ROOT,
        tmp_path,
        requirements,
        create_environment=unexpected,
        install_requirements=unexpected,
    )
    assert second == first


def test_failed_bootstrap_leaves_no_partial_environment(tmp_path: Path):
    requirements = ["PyYAML>=6.0", "pytest>=8.0"]
    environment = validation_environment_path(ROOT, tmp_path, requirements)

    def fail_install(*_args):
        raise RuntimeBootstrapError("offline")

    with pytest.raises(RuntimeBootstrapError, match="offline"):
        ensure_validation_environment(
            ROOT,
            tmp_path,
            requirements,
            create_environment=_fake_environment,
            install_requirements=fail_install,
        )

    assert not environment.exists()
    assert not list(environment.parent.glob(environment.name + ".tmp-*"))


def test_environment_lock_is_exclusive_and_removes_stale_locks(tmp_path: Path):
    environment = tmp_path / "runtime"
    lock = environment.with_name(environment.name + ".lock")
    lock.write_text("stale\n", encoding="utf-8")
    stale = time.time() - 100
    os.utime(lock, (stale, stale))

    with environment_lock(environment, stale_after_seconds=1):
        assert lock.is_file()
        with pytest.raises(RuntimeBootstrapError, match="Timed out"):
            with environment_lock(environment, timeout_seconds=0.01, poll_seconds=0.005):
                pass
    assert not lock.exists()
