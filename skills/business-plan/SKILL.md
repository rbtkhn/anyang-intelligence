---
name: business-plan
description: Governed planning from an effective owner-approved business context. Use only when the operator explicitly invokes $business-plan create, $business-plan resume, or $business-plan change to create, continue, revise, compare, or approve an evidence-backed business plan, strategic plan, 30/90-day plan, segment or channel strategy, or growth plan without inventing economics, capacity, priorities, or execution authority.
---

# Business Plan

Use [docs/executive-interface-protocol.md](../../docs/executive-interface-protocol.md) for Executive–Interface dispatch, structured responses, escalations, and receipts.

Prepare owner-decision artifacts only. Never treat planning permission, a recommendation, or plan approval as authority to activate a loop, run a pilot, spend, publish, change customer-facing material, or mutate repository state.

## Required Reads

Read before every mode:

1. `references/output-contracts.md`
2. `references/evidence-and-scenario-rules.md`
3. `docs/data-handling-policy.md`
4. `docs/governance.md`
5. `docs/membranes.md`

Read `skills/tax-financial-governance/SKILL.md` when the plan requires money classification or tax-sensitive judgment. Use domain skills for evidence review and domain-specific recommendations.

## Select The Mode

Support exactly these explicit modes:

- `$business-plan create`: prepare the first plan from an effective context.
- `$business-plan resume`: continue an incomplete plan from a version-bound
  checkpoint in `Proposed`, `Awaiting Persistence`, or `Hold`.
- `$business-plan change`: evaluate evidence or owner direction against the latest approved plan.

If the invocation does not name a mode, ask whether the operator intends to
create the first plan, continue an incomplete one, or revise an effective one.
Do not collect private planning evidence until the mode is clear.

## Authority And Context Gate

Require operator-supplied:

- business reference;
- latest effective business context and exact version;
- corresponding context approval and persistence receipts;
- planning authority and named decision owner;
- planning purpose, decision, and time horizon;
- approved evidence and privacy boundary;
- constraints and non-negotiables;
- success measures and review date.

Do not reconstruct missing receipts, versions, authority, economics, capacity, or priorities from memory, public storefronts, discussion, access, continuity, or owner interest.

Return `Hold` when the effective context, planning authority, objective, decision-relevant economics, capacity boundary, evidence path, success measure, or review date is missing. Request only evidence tied to the named planning decision; never request a broad data dump.

For `resume`, use the exact checkpoint-bound fields instead of asking again.
Reconfirm only fields that are missing, expired, contradicted, or changed.

## Create

1. Confirm that the effective context, receipts, and planning authority refer to the same business.
2. Define the exact plan question, time horizon, exclusions, and owner decision.
3. Separate confirmed facts, estimates, assumptions, hypotheses, scenarios, interpretations, and missing evidence.
4. Identify strategic choices, tradeoffs, and explicit non-choices.
5. Define customer, value proposition, segment, channel, capability, capacity, economics, and risk implications only to the evidence-supported depth.
6. Define objectives, leading indicators, outcome metrics, guardrails, and review cadence.
7. Build a bounded 30/90-day learning agenda for unresolved assumptions.
8. Produce a complete Proposed Business Plan for owner approval, revision, deferral, or rejection.
9. Record the owner decision exactly. An approval produces an Approved
   Business Plan Packet in `Awaiting Persistence`.
10. Mark the plan `Effective - not activated` only after an authorized
    operator confirms external tenant-private preservation of the exact
    approved version.
11. Produce an Operating-Loop Design Handoff only from an effective plan and
    include its approval and persistence receipts.

## Resume

Require the operator-supplied business reference, latest Plan Continuation
Receipt or plan packet, plan case reference, current state and status,
effective context and receipts, planning authority and evidence boundary,
unresolved decision, and evidence added since the checkpoint. Do not
reconstruct them from memory.

Then:

1. Verify that the checkpoint, context, and proposed plan belong to the same
   business and plan case.
2. Route an already-effective plan to `change`; use `resume` only when no
   effective plan exists or an approved replacement is awaiting persistence.
3. Reconfirm authority, privacy, or evidence fields only when missing,
   expired, contradicted, or changed.
4. Separate new confirmed facts, estimates, assumptions, hypotheses,
   interpretations, scenarios, and missing evidence.
5. For `Awaiting Persistence`, accept only a version-matched operator
   persistence confirmation or return `Hold`; do not redraft the approved
   plan.
6. Otherwise produce only the next artifact: Business Plan Readiness,
   Proposed Business Plan, Owner Plan Decision, Approved Business Plan Packet,
   Plan Persistence Handoff, or Operating-Loop Design Handoff.
7. Preserve the exact checkpoint, open decision, next human authority, and
   evidence needed for another continuation.

## Change

Require the latest approved plan and version, its approval receipt, current effective context, change authority, and the new evidence or owner direction.

Then:

1. Determine whether the signal changes a durable business fact, a strategic choice, or only a plan implementation detail.
2. Route a changed durable fact, authority, economics, capacity, or data boundary to `$business-intake change` before changing the plan.
3. Compare only affected plan sections while preserving the full resulting plan for decision.
4. Produce one outcome: `No Change`, `Open Question`, `Plan Change Proposal`, or `Hold`.
5. For a proposal, show exact before-and-after wording, evidence effects, and the complete proposed resulting plan.
6. Ask the named owner to approve, reject, defer, or request changes to the exact change set.
7. Rerender a smaller exact change set before accepting partial approval.
8. Record an approved change in `Awaiting Persistence`.
9. Keep the prior effective plan version authoritative until an authorized
   operator confirms preservation of the replacement.
10. Mark only the confirmed replacement version `Effective - not activated`.

## Required Plan Contents

Include:

- decision summary;
- effective-context reference and evidence quality;
- strategic choices, tradeoffs, exclusions, and non-choices;
- customer, value proposition, segment, and channel;
- capabilities and capacity constraints;
- economics with explicit assumptions and scenarios;
- objectives, metrics, guardrails, and cadence;
- risks, dependencies, and missing evidence;
- 30/90-day learning agenda;
- proposed operating loops;
- owner decisions and review date;
- authority and data boundary;
- one explicit status.

Use the exact packet contracts in `references/output-contracts.md`. Apply all evidence and scenario rules in `references/evidence-and-scenario-rules.md`.

## Approval And Handoff Boundaries

- Context effectiveness is a prerequisite, not planning authority.
- Planning authority permits preparation only within its stated scope.
- Plan approval approves only the exact displayed plan and authorized
  preservation scope; it does not make the plan effective.
- Plan effectiveness requires a separate operator-confirmed persistence
  receipt for the exact approved version.
- `Effective - not activated` does not authorize a loop, pilot, automation,
  publication, pricing, spending, hiring, customer communication, fulfillment
  commitment, or external claim.
- Hand an approved priority to operating-loop design only with the effective
  plan version, approval and persistence receipts, objective, metric,
  guardrails, named owner, and explicit loop-design authority.
- Route execution to `bounded-workflow-pilot` only after a separately approved loop or pilot specification.
- Route automation candidates to `automation-value-proof` before a pilot.

## Data And Repository Boundary

- Treat completed plans, exact private economics, customer and order records, supplier and employee details, capacity, and private strategy as tenant-private.
- Produce copy-ready Markdown only. Keep private records outside Git.
- Use opaque external references or owner-approved redacted summaries.
- Do not write project state. Route durable sanitized repository updates through `skills/project-state-update/SKILL.md` only in a separate, explicitly authorized task.
- Never claim a plan, loop, pilot, or external action occurred without its human-confirmed receipt.

## Completion

End with exactly one state:

- `Hold`;
- `Proposed`;
- `Awaiting Persistence`;
- `Effective - not activated`;
- `Rejected`;
- `Deferred`;
- `Change proposed`;
- `No Change`;
- `Open Question`.

Name the next human decision and its authority. When authority is absent, include:

> **No action taken; plan remains proposed or held pending owner decision.**
