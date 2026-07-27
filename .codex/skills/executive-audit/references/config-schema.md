# Cross-repository collector configuration

Use this reference only after the audit has exact System Engineer authority.
The configuration records mechanical collection; it does not grant authority.

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
- executes configured commands in a disposable Git archive;
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

It does not:

- provide an operating-system security sandbox;
- inspect ignored or untracked files;
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
