---
name: bounded-workflow-pilot
description: Run one human-approved, low-risk manual or automation workflow experiment within named tools, paths, data, run, review, and authority limits, recording sanitized results, exceptions, and receipts without implying deployment.
---

# Bounded Workflow Pilot

Run one sequential, bounded, and reversible experiment. Never convert a pilot
into production operation, automation, deployment, or external-action
authority by implication.

## Select The Authorization Route

Accept exactly one route:

- `manual workflow`: require one complete Business Loop Pilot Handoff Packet
  with a persisted specification in `Approved for pilot`, `Automation
  involved: no`, and separately approved exact pilot scope.
- `automation`: require one complete human-approved
  `automation-value-proof` packet with status `Approved for pilot`. When the
  automation belongs to a business loop, also require its complete persisted
  Business Loop Pilot Handoff Packet.

Return `Hold` when the route is missing, mixed, stale, contradictory, bound to
another context or version, or uses the manual route to avoid automation value
proof.

## Required Inputs

Require:

- exactly one named workflow and authorization route;
- exact context and, when applicable, plan and loop versions;
- version-matched approval and persistence receipts required by the route;
- approved tool set, path set, data class, and representative run limit;
- baseline, target, quality threshold, and burden guardrail;
- human owner, reviewer, approval boundary, and stop conditions;
- required receipt fields and evidence references;
- prohibited actions and exception route.

For an automation route, additionally require every input mandated by
`skills/automation-value-proof/SKILL.md`. Validator or packet success never
waives human approval.

## Execution Rules

1. Confirm the route, packets, versions, receipts, approval, and exact scope.
2. Run only the named workflow against approved inputs and within the run
   limit.
3. Preserve human review before any consequential output.
4. Record each representative run, duration, result, quality check, exception,
   manual intervention, and reviewer decision.
5. Stop immediately on privacy, rights, authority, quality, scope,
   persistence, version, or tool-policy violations.
6. Do not deploy, schedule, publish, contact customers, spend, change policy,
   alter fulfillment commitments, or mutate authority state.
7. Produce sanitized pilot results, run receipts, an exception report,
   before/after evidence, and a decision packet.

## Decision Output

Return exactly one status:

`Complete`, `Too thin`, `Revised`, `Blocked`, or `Rejected`.

Include:

- authorization route and version-bound source packets;
- baseline and post-pilot result;
- representative run count;
- exception rate;
- quality and revision comparison;
- human review minutes;
- maintenance estimate, using `not applicable` for a fully manual workflow
  when appropriate;
- authority, privacy, and persistence findings;
- evidence of prevented rework, privacy, rights, or missed-commitment events;
- reviewer decision: `Adopt`, `Revise`, `Hold`, or `Reject`.

`Complete` requires at least one accepted performance threshold and no
governance regression. Use `Too thin` when the baseline is incomplete,
evidence is sparse, review burden consumes the value, or no threshold is met.

## Boundary

The pilot produces evidence and a recommendation. It cannot create an
effective deployment, activation, recurring schedule, or external-action
decision. Human owners retain value, editorial, legal, financial, customer,
operating, and deployment authority.
