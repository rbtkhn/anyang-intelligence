# The Repository Defines Durable Authority; Preflight Reconstructs Live Permission

Repository-anchored bounded agency separates durable operating authority from temporary session state.

This is the permission model beneath the canonical [continuity intent](operating-substrate.md#core-thesis). Successive models and specialized agents can inherit durable purpose, evidence, obligations, and governance from the repository, but each session must reconstruct current permission rather than treating continuity as standing authority.

```text
repository contracts = durable memory
canonical data = authority for a declared operation
scripts = bounded capabilities
session mandate = temporary objective
preflight = live state reconstruction
validators = executable invariants
handoff = advisory, validated transition
operator = authority to widen scope
```

Do not copy mutable facts such as commit hashes, dirty-state claims, counts, test results, dates, or deployment status into durable startup prompts. A session names a phase and objective; the repository supplies durable rules; preflight inspects what is true now.

## Existing Contracts Remain Authoritative

This layer composes existing controls rather than replacing them:

- [Governance](governance.md) defines human authority.
- [Membranes](membranes.md) governs movement across projects and audiences.
- [The File Extension Does Not Decide Which Record Governs](data-store-roles.md) defines one authority per operation.
- [`artifact-state.yaml`](../artifact-state.yaml) declares consequential artifact authority, provenance, mutability, and recovery.
- [`bounded-agency.yaml`](../bounded-agency.yaml) declares phase-specific reads, writes, blockers, completion, and handoff ownership.
- Git and filesystem inspection reconstruct live repository state.

Artifact authority and phase permission are different. An artifact declaration says what a surface means and how it may be maintained. A phase envelope says which subset of those operations a temporary session may perform.

Model or agent succession does not widen that subset. Missing, stale, revoked, ambiguous, or out-of-scope approval remains unavailable until the operator or governing contract resolves it.

## State Roles

| Role | Meaning |
| --- | --- |
| Canonical input | Durable or invocation-selected source the phase may trust for its declared operation. |
| Derived projection | Regenerable view of canonical inputs; never a peer writable authority. |
| Working state | Temporary diagnostics, renderings, or implementation intermediates. |
| Public or external state | Published, deployed, released, messaged, or otherwise externally visible output. |
| Advisory state | Handoffs, caches, session memory, and recommendations that grant no authority. |
| Capability surface | Repository command allowed to perform declared mutations. |
| Protected surface | Anything outside the phase write plan or requiring additional operator authority. |

Every operational phase must answer its bounded objective, authoritative inputs, permitted reads and writes, protected surfaces, invariants, warnings, blockers, completion rule, recovery path, and next owner.

## Enforcement Levels

Repository commands enforce their own resolved inputs and outputs. Postflight compares the actual repository delta with the normalized execution plan. Arbitrary agent reads remain advisory unless the execution environment supplies a filesystem sandbox. Preflight reports required authorization but never grants it.

The mutation command repeats preflight immediately before writing. A standalone preflight result is inspectable guidance, not a reusable capability token. A successor phase runs a new preflight.

## Warnings, Holds, And Blockers

- A warning keeps a visible condition in the operator's view without blocking bounded work.
- A row hold prevents that item from mutating while allowing independently approved rows to proceed.
- A phase blocker prevents all mutation for the invocation.
- An authorization requirement identifies work outside the envelope and exits without mutation.

Unrelated dirty paths warn. Dirty paths that intersect intended writes block. Protected-surface requests require additional operator authority.

## First Phase: Singularity Science Transcript Intake

Transcript intake uses the manifest named on the command line as canonical for that invocation. The repository currently contains both a generic and a generated manifest, and the historical ledger contains stale absolute provenance. That ambiguity is documented rather than silently resolved: neither tracked manifest becomes a permanent universal authority merely because it exists.

The phase may read only its invoked manifest and the transcript bodies that manifest explicitly references. It may create non-conflicting transcript files and regenerate the derived import ledger. It may not create or modify source notes, analysis, customer implications, other project lanes, public claims, Git history, or external effects.

Rights-review rows remain row-level holds, and do-not-commit rows remain terminal non-write outcomes. Invalid rows, missing approved sources, dirty intended destinations, path escape, conflicting destinations, protected-surface intersections, or unexpected deltas block mutation.

## Transition And Recovery

Execution follows:

```text
temporary mandate
  -> read-only preflight
  -> mutation-time preflight
  -> bounded write plan
  -> actual-delta validation
  -> phase validation
  -> advisory handoff
  -> successor preflight
```

Transcript writes use bounded temporary files and never overwrite an existing destination. If execution is interrupted, rerun recovery through the same capability: remove only its named temporary files, reconcile existing destinations by content and provenance, and regenerate the derived ledger. A handoff records what passed and who owns the next action; it does not authorize that action.
