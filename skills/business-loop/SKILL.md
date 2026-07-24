---
name: business-loop
description: Governed design and review of one repeatable business operating loop. Use only when the operator explicitly invokes $business-loop design, $business-loop resume, $business-loop change, $business-loop review, $business-loop pause, or $business-loop retire to define, continue, revise, assess, pause, reactivate, or retire a loop tied to an effective plan priority or explicit standalone loop-design authority without implying pilot, activation, deployment, or external-action approval.
---

# Business Loop

Use [docs/loops.md](../../docs/loops.md) as canonical loop doctrine and [docs/executive-interface-protocol.md](../../docs/executive-interface-protocol.md) for Executive–Interface dispatch and receipts.

Design and review one repeatable decision loop. Do not execute the workflow, run a pilot, activate the loop, deploy automation, or grant external-action authority.

## Required Reads

Read before every mode:

1. `docs/loops.md`
2. `references/loop-contract.md`
3. `references/output-contracts.md`
4. `docs/data-handling-policy.md`
5. `docs/governance.md`
6. `docs/membranes.md`

Read `skills/automation-value-proof/SKILL.md` when the loop contains an automation candidate. Read `skills/bounded-workflow-pilot/SKILL.md` before recommending that pilot route. Use domain skills for domain evidence and `skills/tax-financial-governance/SKILL.md` for money classification or tax-sensitive decisions.

## Select The Mode

Support exactly these explicit modes:

- `$business-loop design`: prepare the first specification for one loop.
- `$business-loop resume`: continue an incomplete specification from a
  version-bound checkpoint or prepare reactivation of a `Paused` loop.
- `$business-loop change`: propose an exact change to a specified loop.
- `$business-loop review`: assess evidence from a pilot or active loop.
- `$business-loop pause`: prepare a reversible stop to new cycles.
- `$business-loop retire`: prepare terminal loop closure.

If no mode is named, ask which mode the operator intends. Do not collect private loop evidence until the mode is clear.

## Authority And Linkage Gate

Require operator-supplied:

- business reference and effective context version;
- effective plan priority, plan version, approval receipt, and persistence
  receipt, or explicit standalone loop-design authority;
- named loop owner and decision owner;
- one signal and one decision the loop supports;
- permitted and prohibited actions;
- evidence source and private-data location;
- cadence and service expectation;
- success metric, burden guardrail, and stop conditions.

For `change`, `review`, `pause`, or `retire`, also require the current loop
specification and version plus the latest applicable approval, persistence,
activation, or pause receipt.

For `resume`, require the latest Loop Continuation Receipt or Pause Receipt and
use its exact version-bound fields. Reconfirm only fields that are missing,
expired, contradicted, or changed.

Return `Hold` if context, priority linkage, design authority, owner, decision, action boundary, evidence path, cadence, metric, burden guardrail, or stop condition is missing, stale, contradictory, or bound to a different version. Do not reconstruct authority, approvals, or private facts from memory, access, discussion, interest, silence, or continuity.

## Design

1. Confirm context, approved-priority linkage or standalone authority, and loop-design scope.
2. Name exactly one recurring decision, one loop owner, and one decision owner.
3. Map the current workflow, evidence gaps, delays, exceptions, and burden without claiming execution occurred.
4. Design the smallest viable loop using every field in `references/loop-contract.md`.
5. Define human approval points, authorized actions, prohibited actions, escalation, pause, and stop conditions.
6. Define evidence, receipts, metrics, burden limits, cadence, and learning routes.
7. Produce a complete Proposed Operating Loop Specification and pilot recommendation.
8. Ask the named decision owner to approve, revise, defer, reject, or hold the exact specification.
9. After exact specification approval, produce an Approved Loop Specification
   Packet in `Awaiting Persistence`.
10. Mark the specification `Approved - pilot pending` only after an authorized
    operator confirms external tenant-private preservation.
11. Use `Approved for pilot` only when the specification is persisted and its
    exact bounded pilot scope has separate explicit approval.

## Resume

Require the operator-supplied business reference, loop case reference, latest
Loop Continuation Receipt or Pause Receipt, current specification and state,
effective context and plan receipts or standalone authority, owners, evidence
boundary, unresolved decision, and evidence added since the checkpoint. Do
not reconstruct them from memory.

Then:

1. Verify that the checkpoint, context, plan, and specification refer to the
   same business and loop case.
2. Continue only `Draft`, `Awaiting Persistence`, `Approved - pilot pending`,
   `Hold`, or `Paused`. Route `Active` to `review`, `change`, or `pause`.
   Never resume `Retired`; require a new design authorization.
3. For `Awaiting Persistence`, accept only a version-matched operator
   persistence confirmation or return `Hold`; do not redraft the approved
   specification.
4. For `Approved - pilot pending`, prepare only the bounded pilot decision or
   handoff; do not infer pilot approval.
5. For `Paused`, verify the pause receipt, open obligations, restart
   conditions, current specification, and reactivation authority. Require a
   new version-matched Activation Receipt before returning `Active`.
6. Otherwise produce only the next artifact required by design, approval,
   persistence, or pilot readiness.
7. Preserve the checkpoint, open decision, next human authority, and evidence
   required for another continuation.

## Change

1. Confirm the effective context, approved plan, current loop version, change authority, and new evidence.
2. Determine whether the evidence changes the loop, a strategic choice, or a durable business fact.
3. Route changed durable facts, authority, economics, capacity, or data boundaries to `$business-intake change`.
4. Route changed priorities, objectives, allocations, or strategic risks to `$business-plan change`.
5. For a loop-level change, show exact before-and-after wording and the complete resulting specification.
6. Ask the decision owner to approve, revise, defer, reject, or hold the exact change.
7. Put an approved replacement specification in `Awaiting Persistence` and
   track it separately from the current
   authoritative loop state.
8. Preserve the current approved or active version until replacement
   persistence is confirmed and, for activation changes, a replacement
   activation receipt exists. Never silently transfer an old persistence or
   activation receipt to a new version.

## Review

1. Confirm the loop version and whether the evidence comes from an approved pilot or an active loop.
2. Compare observed decisions, actions, evidence, exceptions, quality, outcomes, burden, and governance against the specification.
3. Separate measured facts, estimates, interpretations, anomalies, and missing evidence.
4. Inspect failures for open-loop drift, memory decay, cadence mismatch, governance bypass, evidence gaps, overbuilding, underbuilding, and missing learning updates.
5. Produce exactly one recommendation: `Adopt`, `Revise`, `Hold`, or `Retire`.
6. `Adopt` after a pilot means recommend activation; it does not create `Active`.
7. For an already active loop, require a current activation receipt for the
   exact reviewed version before retaining `Active`.
8. Preserve the current authoritative state until the recommendation receives
   its separate change, activation, pause, or retirement decision and receipt.

## Pause

1. Confirm pause authority, current version and state, new-cycle cutoff, open
   obligations, dependent workflows, evidence retention, and restart
   conditions.
2. Show the complete Pause Packet for the named decision owner.
3. Preserve the current authoritative state while approval or operational
   confirmation is pending.
4. Use `Paused` only after the owner approves and the operator confirms the
   reversible stop steps. Preserve the persisted specification for possible
   reactivation.

## Retire

1. Confirm terminal retirement authority, current version and state, open
   obligations, data-retention rules, and dependent workflows.
2. Route a temporary stop or intended restart to `pause`.
3. Define ownership transfers, open-loop closure, preserved evidence, access
   changes, and permanent schedule removal.
4. Show the complete Retirement Packet for the named decision owner.
5. Do not claim the loop retired until the operator confirms the decision and
   required terminal steps.
6. If approval exists but operational confirmation is pending, return `Hold`
   and preserve the current authoritative state.

## Pilot And Activation Boundaries

- A loop specification is a design artifact, not a running workflow.
- `Approved - pilot pending` means the exact approved specification has a
  version-matched persistence receipt but no approved pilot scope.
- `Approved for pilot` means the persisted specification and exact bounded
  pilot scope have separate explicit approval; it does not mean the pilot ran.
- A manual workflow pilot may proceed from a complete persisted Business Loop
  Pilot Handoff Packet with `Pilot route: manual workflow`.
- An automation pilot additionally requires one complete, human-approved
  `automation-value-proof` packet. Never waive value proof because an
  automation is embedded in an approved loop.
- Before invoking `bounded-workflow-pilot`, satisfy the prerequisites for the
  selected route.
- A pilot approval covers only its exact tools, paths, data classes, run limit, reviewer, evidence, and stop conditions.
- Pilot completion produces evidence and a recommendation, not activation.
- Use `Active` only with an operator-confirmed activation receipt naming the exact loop version, effective date, owner, permitted actions, and review date.
- Activation never expands the specified external-action authority.

## Learning And Routing

- Route evidence that changes a durable business fact to `$business-intake change`.
- Route evidence that changes a strategic choice, objective, allocation, or risk to `$business-plan change`.
- Route loop mechanics, cadence, ownership, evidence, burden, or exception changes to `$business-loop change`.
- Preserve `No Change` when evidence does not justify revision.

## Data And Repository Boundary

- Keep private customer, order, supplier, employee, financial, workflow, and performance records outside Git.
- Produce copy-ready Markdown only; use opaque external references or owner-approved redacted summaries.
- Do not deploy, schedule, publish, contact customers, spend, change policy, alter fulfillment commitments, or mutate source or project state.
- Route sanitized durable repository updates through `skills/project-state-update/SKILL.md` only in a separate, explicitly authorized task.

## Completion

End with exactly one state:

- `Draft`;
- `Awaiting Persistence`;
- `Approved - pilot pending`;
- `Approved for pilot`;
- `Hold`;
- `Active`, only with an operator-confirmed activation receipt;
- `Paused`;
- `Retired`;
- `Change proposed`;
- `No Change`.

Name the next human decision and authority. When authority is absent, include:

> **No action taken; loop remains draft, paused, or held pending owner decision.**
