# Operating Substrate Migration Plan

This plan defines how the former `repo_probe` implementation root moved toward the clearer `operating-substrate` identity.

Status: completed in the local workspace.

## Decision

The previous physical path was:

```text
C:\dev\anyang-intelligence\repo_probe
```

The target architectural identity is:

```text
operating-substrate
```

The current physical path is:

```text
C:\dev\anyang-intelligence\operating-substrate
```

Do not attempt another root rename while there is uncommitted work, active branch drift, unresolved validation failure, or an open push/sync ambiguity.

## Why Rename

`repo_probe` is now misleading.

It suggests:

- prototype
- disposable experiment
- temporary scratch root
- uncertain authority

The folder now actually contains:

- operating doctrine
- customer memory
- install and loop CLIs
- native skills
- tests
- templates
- recursive self-enhancement surfaces

`operating-substrate` better names the role this folder now plays.

## Do Not Change

The migration should not reorganize internal architecture yet.

Keep:

- `docs/`
- `cli/`
- `customers/`
- `skills/`
- `templates/`
- `tests/`
- `os/`
- `playbooks/`

The current layer architecture is working. The problem is the implementation-root name, not the internal folder model.

## Pre-Migration Preconditions

Before any future filesystem rename:

- `git status --short --branch` shows a clean worktree.
- Local commits are intentionally pushed, exported, or otherwise preserved.
- The operator confirms the target physical path.
- Global Codex skill overrides for `coffee` and `dream` are updated or intentionally left compatible.
- Any hard-coded `repo_probe` references are found and classified.

Run:

```powershell
rg -n "repo_probe|operating-substrate|anyang-intelligence\\repo_probe|anyang-intelligence/repo_probe" -S C:\dev\anyang-intelligence
```

Classify each reference as:

- path that must change
- historical note that should remain
- migration note that should mention both names
- external/global Codex routing reference

## Validation Before Rename

From the current root before a future rename, run:

```powershell
$env:PYTHONPATH='C:\dev\anyang-intelligence\operating-substrate\cli'
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest -q
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.cli validate customers
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.install_cli validate customers
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.coffee_cli --repo .
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.dream_cli --repo .
```

Expected result:

- tests pass
- loop validation passes
- install validation passes, allowing only known Book Club generated-folder warnings
- coffee and dream render native Anyang Intelligence briefs

## Migration Sequence

This is the sequence used for the `repo_probe` -> `operating-substrate` rename. Reuse it only after the preconditions pass.

1. Close all shells, editors, and Codex sessions using the old implementation root as the working directory.
2. Rename the folder at the filesystem level from `repo_probe` to `operating-substrate`.
3. Open a fresh shell in `C:\dev\anyang-intelligence\operating-substrate`.
4. Update path references that must change.
5. Update global Codex skill routing overrides:

```text
C:\Users\rober\.codex\skills\coffee\SKILL.md
C:\Users\rober\.codex\skills\dream\SKILL.md
```

6. Re-run validation from the new path.
7. Commit only repo-tracked changes caused by the rename/path update.

## Post-Migration Validation

From `operating-substrate`, run:

```powershell
$env:PYTHONPATH='C:\dev\anyang-intelligence\operating-substrate\cli'
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest -q
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.cli validate customers
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.install_cli validate customers
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.coffee_cli --repo .
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m anyang_loop.dream_cli --repo .
```

Also verify:

```powershell
git status --short --branch
rg -n "repo_probe" -S
```

Any remaining `repo_probe` reference should be intentional and historical.

## Rollback

If validation fails immediately after the filesystem rename:

1. Do not edit further.
2. Rename `operating-substrate` back to `repo_probe`.
3. Reopen the original path.
4. Run the pre-migration validation again.
5. Investigate path assumptions before retrying.

Do not use destructive git resets as the first rollback tool. The rename is primarily a filesystem/path operation.

## Authority Boundary

The migration changes the implementation-root name only.

It does not authorize:

- publishing customer material
- moving private archive material
- changing customer commitments
- altering pricing hypotheses
- changing the authority model
- reorganizing customer folders
- merging global Codex skill behavior beyond the explicit routing override

Human approval is required before the actual rename.

## Current Convention

Use this convention now:

- `operating-substrate` = current physical path
- `operating substrate` = architectural identity
- `repo_probe` = historical name or rollback target only

## Recommended Timing For Future Root Moves

Do any future root move only after:

- the current local commit stack is preserved outside the agent-blocked push path
- the tree is clean
- no customer delivery work is mid-edit
- the operator is ready to reopen Codex sessions against the new path
