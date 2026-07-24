import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/run_repo.py"
POWERSHELL = ROOT / "tools/run.ps1"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_repo", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_surface_allowlist_and_commands():
    module = load_runner()
    assert module.SURFACES == {
        "project": "anyang_loop.project_cli",
        "loop": "anyang_loop.cli",
        "ops": "anyang_loop.ops_cli",
        "coffee": "anyang_loop.coffee_cli",
        "dream": "anyang_loop.dream_cli",
    }
    assert module.surface_command(Path("python"), "project", ["harness", "scan"]) == [
        "python",
        "-m",
        "anyang_loop.project_cli",
        "harness",
        "scan",
    ]
    with pytest.raises(ValueError, match="Unknown"):
        module.surface_command(Path("python"), "unknown", [])


def test_runner_prepends_current_source_and_propagates_exit_code(tmp_path: Path):
    module = load_runner()
    observed = {}

    def executor(command, **kwargs):
        observed["command"] = command
        observed.update(kwargs)
        return SimpleNamespace(returncode=7)

    code = module.run_surface(
        Path("python"),
        "loop",
        ["validate", "projects"],
        repo_root=tmp_path,
        environ={"PYTHONPATH": "existing"},
        executor=executor,
    )

    assert code == 7
    assert observed["command"][-2:] == ["validate", "projects"]
    assert observed["cwd"] == tmp_path
    assert observed["check"] is False
    assert observed["env"]["PYTHONPATH"] == str(tmp_path / "cli") + os.pathsep + "existing"


def test_main_keeps_bootstrap_progress_off_stdout(monkeypatch, capsys):
    module = load_runner()
    # Isolate the resolver-path contract from any repository-local .venv.
    monkeypatch.setattr(module, "REPO_ROOT", Path("C:/nonexistent-anyang-repo"))

    def resolve(_root, **kwargs):
        kwargs["reporter"]("preparing external runtime")
        return Path("validated-python")

    def run(_python, _surface, _arguments):
        print('{"status":"pass"}')
        return 0

    monkeypatch.setattr(module, "resolve_validation_python", resolve)
    monkeypatch.setattr(module, "run_surface", run)

    assert module.main(["dream", "--format", "json"]) == 0
    captured = capsys.readouterr()
    assert captured.out == '{"status":"pass"}\n'
    assert captured.err == "preparing external runtime\n"


def test_powershell_runner_exposes_all_surfaces_and_forwards_arguments():
    launcher = POWERSHELL.read_text(encoding="utf-8")
    assert "python_launcher.ps1" in launcher
    assert "run_repo.py" in launcher
    assert "ValueFromRemainingArguments" in launcher
    for surface in ("project", "loop", "ops", "coffee", "dream"):
        assert f"'{surface}'" in launcher
