import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_repo.py"
POWERSHELL = ROOT / "tools/validate.ps1"


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
    with pytest.raises(ValueError, match="outside the repository"):
        module.validation_cache_root(ROOT, {"ANYANG_VALIDATION_CACHE": str(ROOT / ".dependencies")})


def test_validation_environment_is_keyed_by_repo_python_and_dependencies(tmp_path: Path):
    module = load_bootstrap()
    first = module.validation_environment_path(ROOT, tmp_path, ["PyYAML>=6.0", "pytest>=8.0"])
    second = module.validation_environment_path(ROOT, tmp_path, ["PyYAML>=6.0", "pytest>=9.0"])
    assert first.parent == second.parent
    assert first != second
    assert first.name.startswith(f"py{module.sys.version_info.major}{module.sys.version_info.minor}-")


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
    assert str(ROOT / ".pytest_cache" / "validate-repo") in pytest_command[-1]


def test_windows_launcher_has_stable_overrides_and_codex_fallback():
    launcher = POWERSHELL.read_text(encoding="utf-8")
    assert "ANYANG_PYTHON" in launcher
    assert ".cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" in launcher
    assert "validate_repo.py" in launcher
    assert "[switch]$BootstrapOnly" in launcher
    assert "[switch]$Refresh" in launcher
    assert "-not $selected -and $env:USERPROFILE" in launcher
    assert "$pathPython.Source -and" in launcher


def test_readme_exposes_one_command_local_validation():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert ".\\tools\\validate.ps1" in readme
    assert "python3 tools/validate_repo.py" in readme
