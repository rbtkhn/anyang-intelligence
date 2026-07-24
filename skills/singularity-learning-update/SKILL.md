---
name: singularity-learning-update
description: Turn a reviewed Singularity recurrence packet and optional test receipt into one append-only, evidence-linked learning update while preserving human authority and explicit transition limits.
---

# Singularity Learning Update

Use after `singularity-recurrence-review` produces a complete recurrence packet. Use an optional verification or bounded-test receipt only when one exists; do not invent one.

This skill updates the research learning loop. It does not create doctrine, publish, mutate customer/project state, approve deployment, or edit canonical source interpretation automatically.

## Required inputs

- one recurrence packet;
- optional verification or bounded-test receipt;
- affected lane ledger, seam, or primitive candidate;
- named human reviewer when a shared artifact or receiving lane could be affected.

Reject the update when source references are missing, the transition is not allowed, or evidence is insufficient for the requested status.

## Allowed transitions

```text
watch → verify
watch → preserve-candidate
verify → lane-test-ready
verify → held
preserve-candidate → preserved
preserved → narrowed
preserved → retired
```

The transition must be justified by evidence, not by repetition alone. A source-specific or worldview-only seam may remain `watch` or `held` indefinitely.

## Workflow

1. Validate the recurrence packet and source references.
2. Confirm the prior status and requested new status are an allowed transition.
3. Check that the evidence supports the transition and that uncertainty remains visible.
4. Require human review for any status affecting a shared primitive, receiving lane, doctrine candidate, or customer boundary.
5. Write one append-only learning update; never rewrite historical updates.
6. Record the next watch condition and evidence required for the next transition.
7. State explicitly what remains inside Singularity Science.

## Required output

Each update must include:

- update ID and date;
- affected source, lane, seam, or candidate;
- prior status and new status;
- evidence references;
- reason for change;
- remaining uncertainty;
- reviewer and approval boundary;
- next recurrence or verification trigger;
- explicit non-authority and non-routing statement.

Use `held` when evidence conflicts, provenance is weak, the source is not independent, or the proposed transition would overgeneralize rhetoric. Use `retired` when a preserved candidate no longer survives its evidence or membrane boundary.

## Five-intake ROI decision

After five comparable recurrence reviews and learning updates, record one result:

- `Expand`: at least one threshold met and no governance regression;
- `Retain`: useful but no threshold yet;
- `Stop`: no threshold met or review burden exceeds measured benefit.

Thresholds are any one of:

- 25% lower recurrence-review time;
- 25% less duplicate or repeated analysis;
- 25% less ledger correction/rework;
- one avoided premature primitive or doctrine-routing decision;
- one hidden recurring seam identified through independent-source reasoning.

## Boundary

Learning is not authority. No update may publish doctrine, alter customer state, authorize deployment, approve external action, or silently create a new source lane.

