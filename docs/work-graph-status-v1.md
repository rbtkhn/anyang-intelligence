# Work Graph Status v1

## Purpose

Work Graph Status projects explicit work dependencies against bounded repository
evidence. It answers what is satisfied, ready, blocked, stale, held, or waiting
for human judgment without executing a node or creating another operating-state
store.

The declaration is intent. The status projection is derived evidence. Neither
is authority.

## Commands

```text
anyang-project graph status --repo PATH --packet GRAPH.yaml --as-of TIME --format markdown|json
anyang-project graph verify --packet GRAPH-STATUS.json
```

`status` writes only to standard output. `verify` operates offline. A successful
inspection exits `0` even when the graph is ordinarily blocked; invalid input,
integrity failure, unsupported versions, privacy failure, or scope escape exits
`1`.

## Declaration

```yaml
contract_version: anyang-work-graph/v1
graph_id: envelope-hardening
objective: Harden and publish the Council decision-envelope pilot
objective_ref: docs/dual-surface-decision-envelope-v1.1.md
scope:
  repository: operating-substrate
  tenant: anyang-internal
  permitted_paths:
    - cli/anyang_loop
    - tests
    - docs/dual-surface-decision-envelope-v1.1.md
  excluded_paths:
    - docs/jk-artistic-director-phase2-coding-agent-instructions.md
    - docs/macbook-pro-purchase-authorization-draft-2026-08-04.md
nodes:
  - id: implement
    kind: workspace-change
    summary: Implement the bounded contract
    completion:
      - type: git-changes-within-scope
    action_boundary: repository-write
    human_gate: required
  - id: full-validation
    kind: validation
    summary: Verify the exact tree and runtime
    depends_on: [implement]
    completion:
      - type: validation-full-pass
  - id: commit
    kind: action
    summary: Commit the validated patch
    depends_on: [full-validation]
    completion:
      - type: git-commit
        commit: 39926ee37fdc97b0b17ecbef6ff2dc1ab6805307
    action_boundary: commit
    human_gate: required
  - id: push
    kind: action
    summary: Publish the exact commit
    depends_on: [commit]
    completion:
      - type: git-remote-tracking-contains
        ref: origin/main
        commit: 39926ee37fdc97b0b17ecbef6ff2dc1ab6805307
    action_boundary: push
    human_gate: required
```

Dependencies exist only in `depends_on`; the status projection derives edges.
This avoids maintaining two competing graph definitions. Packets are bounded,
privacy-scanned, acyclic, and reject unknown fields or adapters.

## Evidence types

| Type | Observation |
| --- | --- |
| `git-head` | Exact local HEAD comparison |
| `git-changes-within-scope` | Non-excluded changes remain within declared paths |
| `git-commit` | A commit exists locally |
| `git-remote-tracking-contains` | A local remote-tracking ref contains a commit |
| `validation-full-pass` | Cached Full validation matches the exact tree and runtime |
| `file-exists` | A declared repository file exists |
| `file-sha256` | A declared file has an exact digest |
| `council-projection` | A tenant-isolated Council projection matches declared state or subject |
| `council-event-chain` | A tenant-isolated Council event chain verifies |
| `explicit-reference` | A bounded reference is present, without proving authority |

There is no arbitrary command adapter. Git runs with optional locks disabled.
Remote evidence never fetches. Validation evidence never bootstraps or refreshes
the runtime. Council evidence requires `--db`, opens SQLite read-only, performs
no migration, and emits no evidence bodies.

## Derived states

- `pending`: upstream work is not satisfied.
- `ready`: read-only work can produce its declared evidence.
- `needs-judgment`: a mutation or human boundary is ready.
- `in-progress`: partial evidence exists.
- `satisfied`: every completion condition verifies.
- `blocked`: upstream or required evidence prevents progress.
- `stale`: evidence no longer binds to the current subject, tree, or runtime.
- `held`: integrity, privacy, tenant, or membrane safety requires stopping.
- `superseded`: a declared successor is satisfied.
- `unknown`: the adapter cannot determine state safely.

The overall disposition is `complete`, `ready`, `needs-judgment`, `blocked`, or
`hold`. Observed completion of a mutation without an authority reference remains
visible as `authority-lineage-missing`; evidence that an action happened is not
evidence that it was authorized.

## Projection and verification

The `anyang-graph-status/v1` projection includes the graph declaration digest,
source snapshot, nodes, derived edges, human gates, attention flags, next
permissible actions, scope exclusions, lineage, `authority_effect: none`, and a
canonical SHA-256 projection hash. Canonical JSON uses sorted keys, compact
separators, and UTF-8. Identical evidence and explicit `as_of` produce identical
semantic bytes.

Offline verification detects structural changes, unsupported states or
versions, authority expansion, and projection tampering. It does not re-query
the repository and is not a reusable capability token.

## Boundaries

V1 does not orchestrate nodes, infer objectives from conversation, refresh
validation, fetch remotes, migrate SQLite, persist graph runs, retain choices,
change recommendation ordering, or authorize repository or external actions.
Existing direct-command, Council, authority, privacy, and membrane controls
remain controlling.
