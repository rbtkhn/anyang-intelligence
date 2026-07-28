# Cross-repository collector configuration

Use this reference only after the audit has exact System Engineer authority.
The configuration records mechanical collection; it does not grant authority.

> **Current execution hold:** Collector `1.4.0` is a Git-aware
> execution-surface candidate. Collector 1.3.1 qualified its bounded Windows
> containment paths, but archive-only execution caused Anyang's Git-dependent
> privacy scan to return a native failure. Version 1.4.0 attaches verified,
> detached, depth-one Git metadata for only the sealed commit before releasing
> native execution. It has not been approved for another audit. Do not start
> another exact-commit audit without accepted delta and qualification reviews
> plus a new System Engineer execution decision.

## Schema

```json
{
  "schema_version": 1,
  "audit_id": "EC-XRA-TARGET-YYYY-MM-DD-01",
  "expected_head": "40-character-commit-sha",
  "timeout_seconds": 180,
  "controlling_paths": [
    "README.md",
    "manifest.json"
  ],
  "commands": [
    {
      "id": "native-validation",
      "argv": [
        "powershell",
        "-NoProfile",
        "-File",
        "tools/validate.ps1"
      ],
      "depends_on": [
        "manifest.json"
      ],
      "summary_rules": [
        {
          "id": "validation-result",
          "stream": "stdout",
          "line_prefix": "Validation ",
          "minimum_matches": 1,
          "max_examples": 5
        }
      ]
    }
  ],
  "sample_groups": [
    {
      "id": "archive-sources",
      "globs": [
        "archive/**/*.md"
      ],
      "exclude_globs": [
        "archive/generated/**/*.md"
      ],
      "count": 30,
      "required": true
    }
  ]
}
```

## Field rules

- `schema_version`: use the version accepted by the canonical collector.
- `audit_id`: use the authorized transaction identifier.
- `expected_head`: require the exact sealed commit; never use a branch name.
- `timeout_seconds`: use `1–900` and record the approved value.
- `controlling_paths`: list repository-relative tracked control surfaces.
- `commands`: include only explicitly approved argv arrays.
- `commands[].id`: use a unique stable identifier.
- `commands[].argv`: avoid shell interpolation, redirection, pipelines, and
  compound command strings.
- schema v1 has no `commands[].env` field. If a native command requires an
  environment override, hold execution and request a separately reviewed
  collector/schema revision. Do not encode environment setup in a shell
  wrapper or depend on an undeclared ambient value.
- `commands[].depends_on`: list exact repository-relative controls whose
  failure may explain the command result. Do not declare speculative
  dependencies.
- `commands[].summary_rules`: optionally identify required output evidence
  using literal line prefixes. Each rule has a unique `id`, a `stream`
  (`stdout`, `stderr`, or `both`), a single-line `line_prefix`, a non-negative
  `minimum_matches` (default `1`), and `max_examples` from `1–20` (default
  `5`). Matching occurs after line-ending normalization and output
  minimization. Rules classify coverage only; they do not interpret native
  outcomes. Each persisted example is independently bounded and includes its
  complete minimized-line hash and size metadata.
- `sample_groups[].id`: use a unique stable identifier.
- `sample_groups[].globs`: use repository-rooted, case-sensitive POSIX glob
  patterns. `*` and `?` stay within one path segment; `**` spans zero or more
  directory segments. Absolute paths and parent traversal are rejected.
- `sample_groups[].exclude_globs`: optionally remove repository-rooted matches
  from the included population.
- `sample_groups[].count`: use the approved positive sample count.
- `sample_groups[].required`: defaults to `true`. An unavailable required
  sample makes collection status partial; an unavailable optional sample
  remains visible without making collection partial.

## Configuration review

Before execution, verify:

1. target `HEAD` equals `expected_head`;
2. every path is repository-relative and membrane-safe;
3. every command and timeout appears in the authority receipt;
4. every declared dependency is evidence-based;
5. samples are deterministic and sufficient for the stated depth; inspect
   include, exclusion, and final eligible counts rather than assuming a glob
   expresses the intended evidence class;
6. the output path is outside the target repository;
7. the configuration contains no credentials, private paths, or shell-expanded
   secrets;
8. the collector source identity will be recorded in the receipt.
9. no command depends on an undeclared environment override.

## Collector guarantees and limits

The current collector:

- inventories the sealed tracked snapshot;
- executes configured commands in a disposable, detached, depth-one Git
  snapshot containing only the sealed commit;
- retains safe archive extraction for worktree materialization, then attaches
  a clean index without performing a checkout or invoking smudge filters;
- verifies exact HEAD and tree, clean index, one reachable commit, and absence
  of remotes, refs, alternates, `FETCH_HEAD`, hooks, reflogs, and persisted
  source paths before native command release;
- records the preparation result in top-level `execution_snapshot`; preparation
  failure prevents native start and seals `launch_failed` command evidence plus
  a partial receipt;
- captures stdout and stderr through temporary files so descendant-held pipe
  handles cannot block receipt sealing;
- starts a gated command worker, establishes a managed Windows Job Object or
  POSIX session, and only then releases native execution so descendants cannot
  predate the collector's isolation boundary;
- applies bounded process-tree termination after timeout and records the
  result in `commands[].process_tree`; Windows pre-captures the descendant set,
  attempts `taskkill /T /F` while the gated root still exists, then terminates
  the managed Job and verifies that the pre-captured processes ended;
- records version, source hash, timeout, dependencies, and coverage gaps;
- records rooted sample accounting, command execution state, structured
  summary coverage, and complete-versus-partial collection status;
- treats a normally terminated nonzero command as completed evidence, not as
  an incomplete collection;
- keeps bounded head/tail previews while hashing complete minimized command
  output; full unbounded output is not persisted;
- minimizes captured machine paths and common secret patterns;
- validates JSON, YAML, and TOML structures;
- refuses to overwrite an existing receipt;
- verifies the target's Git-visible state before and after collection.

`commands[].process_tree` records `isolation_strategy`,
`isolation_ready_before_command`, `start_gate_status`,
`termination_attempted`, `termination_status`, `termination_duration_ms`,
`termination_sequence`, and `descendant_cleanup_status`. Termination status is
`not-required`, `terminated`, or `failed`; descendant cleanup is
`not-required`, `verified`, or `unverified`. A Windows isolation failure keeps
the gate closed and prevents the native command from starting. Timeout or
launch failure makes collection partial. Failed or unverified process-tree
cleanup adds a coverage gap but does not suppress a partial receipt after the
bounded worker returns.

`execution_snapshot` records strategy, readiness, HEAD/tree/index checks,
detached state, reachable commit count, remote and ref counts, and bounded
booleans for alternates, `FETCH_HEAD`, hooks, reflogs, and source-path
persistence. Do not accept command evidence when its snapshot status is not
`ready`.

It does not:

- provide an operating-system security sandbox;
- inspect ignored or untracked files;
- expose target remotes, local Git configuration, refs, reflogs, hooks,
  worktrees, stashes, or history before the sealed commit;
- prove external source truth;
- access private systems;
- assign semantic severity;
- establish Council Steward independence;
- authorize persistence, remediation, or publication.

The receipt preserves raw objective diagnostics. Reconciliation must report
raw observations, exact-unique observations, cross-category overlaps, and
supported root-cause groups separately; those classifications are not a
license to discard the raw evidence.

Treat any command capable of network or absolute-path action as requiring an
explicit boundary and separate risk review even though its working directory
is disposable.
