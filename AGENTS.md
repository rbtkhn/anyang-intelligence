# Agent Runtime Contract

This repository owns its validation runtime. Do not invoke Pytest directly or use a bare `pytest` command as the repository validation path.

Use the canonical launcher instead:

- Windows: `.\tools\validate.ps1`
- macOS/Linux: `python3 tools/validate_repo.py`

For a focused test run, use the repository's selected validation environment or the bundled workspace Python when available. On Windows, repository launchers prefer the bundled dependency-aware runtime before PATH Python. Do not hard-code a user-specific Python path or commit environment files.

The canonical launcher derives dependencies from `pyproject.toml`, caches them outside Git, and runs the full test and validator inventory. If a direct interpreter lacks Pytest, repair the local environment or invoke the canonical launcher; do not change repository instructions to assume an arbitrary global installation.
