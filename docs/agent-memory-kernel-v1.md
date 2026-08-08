# Agent Memory Kernel

**Version:** 1
**Status:** advisory implementation specification
**Authority effect:** `none`

## Lead judgment

The proposed kernel uses a separate private SQLite control plane. Git stores
only contracts, deterministic code, and synthetic fixtures. Raw transcripts
remain external evidence and do not become database bodies.

## Trust boundary

Untrusted importers and models may propose source events, summaries, and memory
candidates. A deterministic kernel checks structure, lineage, policy,
transitions, privacy, membranes, and authority effect. Humans decide
consequential meaning and promotion.

The trusted kernel contains no model calls.

## Proposed package

```text
cli/anyang_loop/memory_kernel/
  constants.py  errors.py  models.py  schema.py  store.py  policy.py
  collection.py  evidence.py  lifecycle.py  retrieval.py  neutralize.py
  deletion.py  evaluation.py  audit.py  render.py
```

A future `memory_cli.py` would expose dry-run-first collection declarations,
candidate review, lifecycle transitions, retrieval, audit, restriction, and
deletion. Phase 1 implements none of those operations.

## Proposed canonical tables

```text
memory_schema_migration
collection_declaration
source_record
source_event
episode
memory_object
memory_evidence_link
evidence_origin
memory_transition
memory_dependency
memory_restriction
retrieval_packet
retrieval_item
disposition_task
evaluation_cohort
evaluation_observation
memory_audit_event
```

`memory_object.authority_effect` is constrained to `none`. Independent support
counts distinct eligible causal origins rather than database rows. Every
transition is append-only and hash-linked. Every retrieval packet declares
historical content as quoted evidence and records neutralization, exclusions,
budgets, provenance, and contradictions.

## Proposed service boundaries

- `collection` registers governed declarations and source metadata.
- `evidence` resolves causal dependence and independent support.
- `lifecycle` exclusively mutates current memory state.
- `neutralize` prevents historical content from becoming instructions.
- `retrieval` compiles deterministic, bounded self-model packets.
- `deletion` propagates restriction and deletion dispositions.
- `evaluation` compares fixed baseline and assisted cohorts.
- `audit` reports integrity without changing state.

The existing governed pattern-memory implementation may later serve as a
sanitized source adapter. It does not become autobiographical memory merely by
being searchable.

## Delivery phases

1. Contracts and disabled validator only.
2. Deterministic kernel with synthetic data.
3. Retrieval firewall and adversarial replay.
4. Existing approved repository learning in shadow mode.
5. Separately authorized, bounded session-history pilot.
6. One narrow active task cohort after outcome evidence.

## No-go conditions

Activation is prohibited while any test permits historical instruction
execution, cross-lane retrieval, incomplete deletion, stale authority reuse,
hidden contradiction, personality inference, circular corroboration, private
state in Git, or effectiveness claims based only on passing tests.

## Status vocabulary

- `specified`: the contract describes it.
- `implemented`: deterministic code exists.
- `validated`: structural checks pass.
- `activated`: a separate decision permits runtime use.
- `observed`: a later cycle supplies outcome evidence.

Phase 1 may claim only `specified` and validated contract structure. It may not
claim that Anyang remembers.
