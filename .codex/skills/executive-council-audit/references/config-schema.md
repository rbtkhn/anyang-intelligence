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
      ]
    }
  ],
  "sample_groups": [
    {
      "id": "archive-sources",
      "globs": [
        "archive/**/*.md"
      ],
      "count": 30
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
- `commands[].depends_on`: list exact repository-relative controls whose
  failure may explain the command result. Do not declare speculative
  dependencies.
- `sample_groups[].id`: use a unique stable identifier.
- `sample_groups[].globs`: use repository-relative deterministic glob patterns.
- `sample_groups[].count`: use the approved positive sample count.

## Configuration review

Before execution, verify:

1. target `HEAD` equals `expected_head`;
2. every path is repository-relative and membrane-safe;
3. every command and timeout appears in the authority receipt;
4. every declared dependency is evidence-based;
5. samples are deterministic and sufficient for the stated depth;
6. the output path is outside the target repository;
7. the configuration contains no credentials, private paths, or shell-expanded
   secrets;
8. the collector source identity will be recorded in the receipt.

## Collector guarantees and limits

The current collector:

- inventories the sealed tracked snapshot;
- executes configured commands in a disposable Git archive;
- records version, source hash, timeout, dependencies, and coverage gaps;
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

Treat any command capable of network or absolute-path action as requiring an
explicit boundary and separate risk review even though its working directory
is disposable.
