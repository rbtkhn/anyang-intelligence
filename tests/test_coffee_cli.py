from pathlib import Path

from anyang_loop.coffee import build_coffee_brief
from anyang_loop.coffee_cli import main


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(root: Path) -> None:
    write(
        root / "customers" / "operating-portfolio-dashboard.md",
        """# Operating Portfolio Dashboard

## Active Obligations

- Elementary School paid Anyang Intelligence a $1,000 one-time retainer for the scoped 30-day collaborative build.
- Await Grace Gems owner/operator intake response.

## Immediate Decision Queue

1. Elementary School: classify Ready / Provisional / Hold before drafting.

## Current Interpretation

Paid obligations lead.

Current priority order:

1. Serve Grace Gems through Media Production.
2. Collect Elementary School parent intake responses.
""",
    )
    write(root / "customers" / "comparison-matrix.md", "# Customer Comparison Matrix\n")
    write(root / "customers" / "commercial-hypotheses.md", "# Commercial Hypotheses\n")
    write(root / "skills" / "README.md", "# Skills\n\n| [coffee](coffee/SKILL.md) | Native coffee. |\n")


def test_build_coffee_brief_uses_native_shape(tmp_path):
    make_repo(tmp_path)
    output = build_coffee_brief(tmp_path)
    assert "Current picture:" in output
    assert "Live obligations:" in output
    assert "Elementary School paid Anyang Intelligence" in output
    assert "Coffee menu - reply A-D:" in output
    assert "A. Confirm" in output
    assert "D. Ship" in output


def test_coffee_cli_prints_brief(tmp_path, capsys):
    make_repo(tmp_path)
    assert main(["--repo", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "native `anyang-coffee`" in captured.out
    assert "Coffee menu - reply A-D:" in captured.out
