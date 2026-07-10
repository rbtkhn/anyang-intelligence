from __future__ import annotations

import subprocess
from pathlib import Path


def run(root: Path, *args: str) -> str:
    result = subprocess.run(args, cwd=root, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_git_repo(root: Path, dashboard: str = "# Operating Portfolio Dashboard\n") -> None:
    run(root, "git", "init")
    run(root, "git", "config", "user.email", "cadence" + chr(64) + "example.invalid")
    run(root, "git", "config", "user.name", "Cadence Test")
    write(root / "customers" / "operating-portfolio-dashboard.md", dashboard)
    write(root / "customers" / "comparison-matrix.md", "# Customer Comparison Matrix\n")
    write(root / "customers" / "commercial-hypotheses.md", "# Commercial Hypotheses\n")
    write(root / "skills" / "README.md", "# Skills\n\n- coffee\n- dream\n")
    write(root / "docs" / "membranes.md", "# Membranes\n")
    run(root, "git", "add", ".")
    run(root, "git", "commit", "-m", "fixture")
