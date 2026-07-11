---
name: dream
preferred_activation: dream
description: Native Anyang Intelligence closeout ritual for operating-substrate. Use for dream, day close, closeout, settle the system, or night review to consolidate the session, verify repo integrity, name what was preserved, and identify what tomorrow inherits without creating autonomous merge authority.
category: operator-coherence
status: active
scope_class: repo-governed
---

# Dream

**Preferred activation:** say `dream`.

`dream` is the native Anyang Intelligence closeout ritual. It should feel like quiet integration: enough verification and compression to make tomorrow easier, without turning the end of a session into another build sprint.

The operator may type only `dream`. Do not require them to say `anyang-dream`, `native dream`, or a repo qualifier.

When working inside `anyang-intelligence/operating-substrate`, this skill is authoritative. Do not route `dream` through strategy-codex `auto_dream.py`, cadence logs, conductor rollups, Grace-Mar memory files, or external night-close rituals unless the operator explicitly leaves the Anyang Intelligence repo. Anyang Intelligence dream reads this repo, its project folders, its loop/install tooling, its skills, and git state.

When tools are available, prefer the native command:

```text
anyang-dream --repo .
```

Native dream runs fast verification by default. It remains read-only unless the operator explicitly passes `--record`, which stores one sanitized repo-level handoff in external SQLite without creating customer authority.

If the command is unavailable, perform the same read-only procedure manually from the inputs below.

Use `dream` when the operator asks:

- `dream`
- `day close`
- `closeout`
- `settle the system`
- `night review`
- `what did we preserve`

## Purpose

`dream` helps the operator end a work cycle with:

- a clean account of what changed
- current git sync state
- validation status for the operating substrate
- known warnings or unresolved loops
- customer and membrane boundaries still visible
- a single tomorrow inheritance line

The closeout question is:

```text
What did this cycle preserve in the repo, and what does tomorrow inherit?
```

## Inputs

Read these first, in order:

1. `git status --short --branch`
2. Recent commits: `git log --oneline --decorate -8`
3. `projects/operating-portfolio-dashboard.md`
4. `skills/README.md`
5. `docs/recursive-self-enhancement.md`
6. `docs/membranes.md`
7. The customer or skill folder touched during the session, when obvious from recent commits or dirty files

Optional, only when directly relevant:

- `git diff --stat` when the worktree is dirty
- `cli/README.md` when loop or install tooling changed
- `projects/README.md` when project folder structure changed
- `docs/operating-substrate.md` when the repo's meta-operating layer changed
- `pyproject.toml` and `tests/` when Python tooling changed

Do not require unavailable strategy-codex-only files such as `scripts/auto_dream.py`, `last-dream.json`, `docs/skill-work/work-cadence/`, Cici notebook generators, or Grace-Mar Record surfaces.

## Procedure

1. Check git state first. Say whether the repo is clean, dirty, ahead, behind, or synced.
2. Name the consolidation window from recent commits and current uncommitted work.
3. Identify what was preserved in durable repo surfaces: project docs, skills, templates, CLIs, tests, loop examples, or governance docs.
4. Run fast verification by default: `git diff --check`, privacy scanning when available, and compilation of changed Python files. Use `--verify full` for pytest plus install and loop validation, or `--verify none` only when intentionally skipping checks.
5. Separate fresh issues from known legacy warnings.
6. Check authority and membrane boundaries for the touched surfaces:
   - customer commitments
   - parent or owner authority
   - child-safety decisions
   - publication, spending, rights, external claims
   - cross-project pattern transfer
   - private or sensitive context
7. State what was not generated. A normal dream remains read-only. `--record` creates only one sanitized external SQLite handoff; it does not create `last-dream.json`, a tracked cadence log, notebook pages, or autonomous follow-up tasks.
8. Name one open loop or tomorrow inheritance. Prefer the most direct continuation of the preserved work.
9. Do not edit, stage, commit, or push by default. `dream` is maintenance and closeout, not autonomous shipping, unless the operator explicitly asks.

## Native Verification Hooks

Use these when available and relevant:

- `anyang-dream --repo .`
- `anyang-dream --repo . --verify fast`
- `anyang-dream --repo . --verify full`
- `anyang-dream --repo . --verify fast --record --db <external-db>`
- `git status --short --branch`
- `git log --oneline --decorate -8`
- `python -m anyang_loop.project_cli validate customers`
- `python -m anyang_loop.cli validate customers`
- `python -m pytest`
- `git diff --check`

In this repo, local `python`, `py`, or `pytest` may not be on `PATH`. If needed, use the Codex bundled Python runtime when available:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

If a verifier reaches visible completion but the process does not exit, report that caveat honestly. Do not call it a clean pass unless the command exits cleanly.

## Output Shape

Use this structure:

```text
Dream:

Recent rhythm:
<2-4 sentences about what settled and what the system learned, grounded in recent commits or touched files. No telemetry wall.>

Run status:
- Git: <clean/dirty/ahead/behind/synced>
- Validation: <pass/fail/skipped, with known legacy warnings separated>
- Generated artifacts: <none, or named files>
- Touched surfaces: <docs/projects/skills/cli/tests>

Integrity and governance:
- <one or more relevant boundary checks, or "No new boundary issue found.">

Tomorrow inherits:
- <one concrete continuation, blocker, or next seam>
```

Keep the default brief short. Expand only when a check fails, a warning is new, the repo is dirty, or the operator asks for a fuller closeout.

## Relationship To Coffee

`coffee`, `bravo`, `friction`, and `dream` form the native Anyang Intelligence cadence loop:

- `coffee` restores orientation and chooses the next A-D move.
- `bravo` reinforces what worked.
- `friction` repairs what missed.
- `dream` settles the work cycle and names what tomorrow inherits.

`coffee` may recommend durable improvements. `dream` confirms what actually landed and whether the repo is ready to rest.

## Guardrails

- Do not create a new memory surface by default.
- Record a cadence handoff only after explicit `--record`; failed verification may still be recorded so the next coffee inherits the blocker.
- Do not invent a cadence log if the repo does not have one.
- Do not pretend strategy-codex scripts exist in this repo.
- Do not turn `dream` into a broad planning sprint.
- Do not treat warnings from legacy hand-built project folders as new failures unless today's work caused them.
- Do not merge, stage, commit, push, publish, or transfer customer patterns across membranes without operator authority.
- Preserve the distinction between paid obligations, hypotheses, donations, revenue, expenses, and asset values.
- Preserve the distinction between one-time retainers and recurring subscription/customer pricing.
- Preserve parent, owner/operator, client, and human approval authority.
- Keep customer-owned AI interface training scoped to its project folder unless an explicit membrane review extracts a reusable primitive.
- Cadence handoffs are repository-level coordination records, not tenant learning, customer evidence, or approval receipts. Never store customer facts, raw paths with private identifiers, emails, transcripts, or evidence bodies in them.

## Done When

The operator knows:

- whether the repo is clean and synced
- what changed in the work cycle
- what validation passed or was skipped
- whether any boundary issue remains
- what tomorrow inherits
