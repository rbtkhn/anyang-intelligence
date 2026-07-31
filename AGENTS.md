# Agent Runtime Contract

This repository owns its validation runtime. Do not invoke Pytest directly or use a bare `pytest` command as the repository validation path.

Use the canonical launcher instead:

- Windows: `.\tools\validate.ps1`
- macOS/Linux: `python3 tools/validate_repo.py`

For a focused test run, use the repository's selected validation environment or the bundled workspace Python when available. On Windows, repository launchers prefer the bundled dependency-aware runtime before PATH Python. Do not hard-code a user-specific Python path or commit environment files.

The canonical launcher derives dependencies from `pyproject.toml`, caches them outside Git, and runs the full test and validator inventory. If a direct interpreter lacks Pytest, repair the local environment or invoke the canonical launcher; do not change repository instructions to assume an arbitrary global installation.

## Possibility Navigation

Read and follow `skills/learn-from-choices/SKILL.md` implicitly. End every final
user-facing response, but not intermediate commentary, with three or four
meaningfully different next-best possibilities. State which branch is
recommended and why. Preserve a credible overlooked path when one exists;
never create fake diversity.

A letter selects the displayed option. An exploratory option enters a branch
for read-only development. When the displayed option is explicitly
action-labeled `Execute`, `Commit`, `Push`, or `Send`, selecting its letter
authorizes only that named bounded action, subject to the existing authority.
It grants no broader or hidden authority. A later direct command supersedes the
pending menu.

Comma-separated letters select displayed branches in order. Ranked letters
express preference only and execute nothing. Neutral factual elicitation follows
the canonical `skills/elicitation/SKILL.md` exception rather than recommendation
roles.

Under Learn From Choices Lite, ordinary selections perform no choice-ledger
lookup or write. Durable learning is exceptional: it requires supported outcome
evidence and a separately action-labeled, operator-selected retention step.
Selection frequency never supplies learning evidence.

When a consequential request assertion may conflict with repository state,
follow Elicitation's structured contradiction preflight before asking or
acting. The preflight compares only explicitly supplied controlling facts,
never grants authority, and never changes durable claim state.
