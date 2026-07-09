from pathlib import Path

from anyang_loop.dream import build_dream_brief
from anyang_loop.dream_cli import main


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(root: Path) -> None:
    write(root / "customers" / "operating-portfolio-dashboard.md", "# Operating Portfolio Dashboard\n")
    write(root / "skills" / "README.md", "# Skills\n\n| [dream](dream/SKILL.md) | Native dream. |\n")
    write(root / "docs" / "membranes.md", "# Membranes\n")


def test_build_dream_brief_uses_native_shape(tmp_path):
    make_repo(tmp_path)
    output = build_dream_brief(tmp_path)
    assert "Dream:" in output
    assert "Recent rhythm:" in output
    assert "Run status:" in output
    assert "Integrity and governance:" in output
    assert "Tomorrow inherits:" in output


def test_dream_cli_prints_brief(tmp_path, capsys):
    make_repo(tmp_path)
    assert main(["--repo", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "Dream:" in captured.out
    assert "dream is read-only" in captured.out
