---
name: bounded-workflow-pilot
description: Run one human-approved, low-risk workflow experiment within named tools, paths, data, and authority limits, recording sanitized results, exceptions, and receipts.
---

# Bounded Workflow Pilot

Use this skill only when `automation-value-proof` has produced one complete packet with status `Approved for pilot` and a named human owner and reviewer.

The pilot is sequential, bounded, and reversible. It must not become production automation by implication.

## Required inputs

- Exactly one approved value-proof packet.
- One named workflow, tool set, path set, data class, and run limit.
- Human owner, reviewer, approval boundary, and stop conditions.
- Required receipt fields and evidence references.

Reject or return `Hold` for missing, stale, contradictory, or scope-broad approvals.

## Execution rules

1. Confirm the packet, context version, approval, and exact scope.
2. Run only the named workflow against approved inputs.
3. Preserve human review before any consequential output.
4. Record each representative run, duration, result, quality check, exception, manual intervention, and reviewer decision.
5. Stop immediately on privacy, rights, authority, quality, scope, or tool-policy violations.
6. Do not deploy, schedule, publish, contact customers, spend, change policy, or mutate authority state.
7. Produce sanitized pilot results, run receipts, an exception report, before/after evidence, and a decision packet.

## Decision output

Return exactly one status:

`Complete`, `Too thin`, `Revised`, `Blocked`, or `Rejected`.

The decision packet must include:

- baseline and post-pilot result;
- representative run count;
- exception rate;
- quality/revision comparison;
- human review minutes;
- maintenance estimate;
- authority and privacy findings;
- evidence of any prevented rework, privacy, rights, or missed-commitment event;
- reviewer decision: `Adopt`, `Revise`, `Hold`, or `Reject`.

`Complete` requires at least one accepted performance threshold and no governance regression. Use `Too thin` when the baseline is incomplete, evidence is too sparse, review burden consumes the saving, or no threshold is met.

## Boundary

The pilot produces evidence and a recommendation. It cannot produce an effective deployment decision automatically. Human owners retain value, editorial, legal, financial, customer, and deployment authority.

