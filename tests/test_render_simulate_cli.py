from pathlib import Path
import tempfile

from anyang_loop.cli import main
from anyang_loop.builtins import get_builtin
from anyang_loop.render import render_loop
from anyang_loop.simulate import simulate_loop


def test_render_formats():
    loop = get_builtin("canonical-executive-loop")
    assert loop is not None
    assert "# canonical-executive-loop" in render_loop(loop, "markdown")
    assert "#anyang-loop" in render_loop(loop, "obsidian")
    assert '"name": "canonical-executive-loop"' in render_loop(loop, "json")


def test_simulate_mentions_governance():
    loop = get_builtin("recursive-improvement-loop")
    assert loop is not None
    output = simulate_loop(loop)
    assert "Governance boundary enforced" in output


def test_cli_new_and_validate():
    tmp_path = Path(tempfile.mkdtemp())
    output = tmp_path / "loop.yaml"
    assert main(["new", "tmp-loop", "--output", str(output)]) == 0
    assert output.exists()
    assert main(["validate", str(output)]) == 0


def test_cli_export_builtin(capsys):
    assert main(["export", "canonical-executive-loop", "--format", "json"]) == 0
    captured = capsys.readouterr()
    assert "canonical-executive-loop" in captured.out


def test_cli_list_examples(capsys):
    root = Path(__file__).resolve().parents[1]
    assert main(["list", str(root / "projects"), "--include-builtins"]) == 0
    captured = capsys.readouterr()
    assert "canonical-executive-loop" in captured.out
    assert "grace-gems-listing-gate" in captured.out
