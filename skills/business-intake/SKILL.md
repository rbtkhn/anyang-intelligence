---
name: business-intake
description: Governed owner-facing intake for creating, resuming, or changing a business context. Use only when the operator explicitly invokes $business-intake create, $business-intake resume, or $business-intake change for initial intake, a verified meeting capture or handoff continuation, phased intake, owner-response capture, or review of new evidence against an effective context.
---

# Business Intake

Use [docs/executive-interface-protocol.md](../../docs/executive-interface-protocol.md) for Executive–Interface task dispatch, structured responses, escalations, and receipts. Intake permission and context approval do not create external-action authority.

Use this skill as the owner-facing entry point for commercial business installations. Conduct the conversation and produce copy-ready packets, including a sanitized intake-control manifest when requested; never write a private business record, invoke the persistence CLI, or change repository state.

## Required Reads

Read before any mode:

1. `references/question-strategy.md`
2. `references/output-contracts.md`
3. `docs/data-handling-policy.md`
4. `docs/governance.md`
5. `docs/membranes.md`

For Grace Gems, also read `projects/grace-gems/business-intake-survey.md`. For Mountain Villa, also read `projects/mountain-villa/business-intake-survey.md`. Treat each as a project-specific question set under this skill, not as a separate authority or persistence workflow.

## Select The Mode

Support exactly these explicit modes:

- `$business-intake create`: establish an initial owner-approved business context.
- `$business-intake resume`: continue an incomplete intake from a verified checkpoint, meeting capture, or handoff.
- `$business-intake change`: review new evidence against the latest effective context and govern a possible revision.

If the explicit invocation does not name one mode, ask whether the operator intends to establish the first context, continue an incomplete intake, or reconsider an effective one. Do not begin private questions until the mode is clear.

## Authority And Data Gate

Before business-specific questions:

1. Confirm an operator-supplied business reference.
2. Identify the owner authorized to approve the context.
3. Confirm the intake purpose and permission.
4. Confirm what evidence may be discussed, handled temporarily, preserved, deleted, and shared.
5. Confirm exclusions, reuse restrictions, and pause conditions.
6. Confirm the requested mode.

Return `Hold` when identity, authority, purpose, privacy, preservation, sharing, deletion, exclusions, or mode remains unclear. Request only the missing decision; do not pressure the owner to disclose private information.

When an operator supplies an `ops intake status` receipt, treat its exact version-bound fields as the continuation checkpoint. Ask again only when a required field is absent, expired, contradicted, or bound to a different context version. Never treat the receipt as authority for a new decision.

A supplied handoff may support read-only orientation before private questions.
Treat it as a checkpoint only after matching the business reference, intake
case, phase, status, authority boundary, and evidence boundary. Never infer
approval from a meeting, interest, access, discussion, continuity, or the
existence of a handoff.

## Intent Recovery For Owner Language

When an owner expresses a goal or constraint informally, metaphorically, or with acknowledged difficulty articulating it, automatically read and follow `skills/intent-recovery/SKILL.md` in `Business intake` mode before asking follow-up questions. Show the full intent-recovery output and ask the owner to confirm or correct the articulation before including it in a Proposed Business Context.

Skip recovery for factual receipts, exact economics, explicit approvals, clear answers, and genuinely missing evidence. Never use recovered intent to supply economics, capacity, customer facts, private strategy, approval, or authority. Keep unconfirmed articulations out of completed packets and use `Missing` for unsupported facts.

## Create

1. Require operator confirmation that no effective business context exists for the reference.
2. Route an existing context to `change`; route possible duplication or an unchecked state to `Hold`.
3. Gather only evidence that can change the first operating review or its readiness.
4. Produce an Owner Authority and Data Receipt plus a Business Intake and Readiness Packet.
5. Classify readiness as `Ready`, `Provisional`, or `Hold`. Readiness does not approve a context or authorize an operating review.
6. For `Ready` or `Provisional`, prepare a separate Proposed Business Context. End `Hold` with only the blocker and deciding human.
7. Show the complete proposed context and ask the named owner to approve, reject, or request changes.
8. After exact approval, produce an Approved Business Context Packet in `Awaiting Persistence`.
9. Mark the context `Effective` only after an authorized operator confirms external tenant-private preservation.
10. Ask separately whether the owner authorizes one downstream preparation
    route: the first operating review, business planning, or neither.
11. For a business-planning route, produce an Intake Handoff Packet carrying
    the exact context approval and persistence receipts, planning-preparation
    authority, named decision owner, and evidence boundary. Do not infer plan
    approval or execution authority.

## Resume

Require the operator-supplied business reference, latest intake checkpoint or
handoff, current phase and status, named owner, authority and data boundaries,
unresolved decision, and evidence added since the checkpoint. Do not
reconstruct them from memory.

Then:

1. Verify that the checkpoint belongs to the same business and intake case.
2. Reconfirm authority or data fields only when missing, expired,
   contradicted, or changed.
3. Separate confirmed owner statements from preparation hypotheses, public
   observations, interpretations, and missing evidence.
4. For a post-meeting continuation, produce a Verified Meeting Capture before
   recommending work.
5. Record the current intake phase without treating phase progression as
   context approval, persistence, operating-review authority, or external
   action authority.
6. Request only evidence tied to the next approved intake or review question;
   never request a broad data dump.
7. Produce only the next required packet: an Intake Continuation Receipt,
   Verified Meeting Capture, bounded evidence request, First Review Decision
   Receipt, or Intake Handoff Packet.
8. If a first review is authorized, complete its brief before execution and
   route the evidence review to the appropriate domain skill or separate
   authorized task.
9. Return `Paused`, `Awaiting Owner Response`, or `Hold` when the next decision
   belongs to the owner. Preserve the exact checkpoint and resume requirements.

## Change

Require the operator-supplied business reference, latest confirmed-effective context and version, corresponding approval receipt, current authority and data boundaries, and new evidence. Do not reconstruct them from memory.

Then:

1. Ask what prompted review, which sections may be stale, what evidence changed, and whether authority or data boundaries changed.
2. Inspect only affected sections.
3. Separate confirmed facts, estimates, hypotheses, interpretations, and missing evidence.
4. Produce exactly one outcome: `No Change`, `Open Question`, `Context Change Proposal`, or `Hold`.
5. For a proposal, show exact before-and-after wording and the complete proposed resulting context.
6. Ask the named owner to approve, reject, defer, or request changes to that exact change set.
7. Rerender a smaller exact change set before accepting partial approval.
8. After approval, produce an Approved Business Context Packet in `Awaiting Persistence`.
9. Keep the prior version effective until the operator confirms preservation of the replacement.

## Readiness Rules

- `Ready`: authority and data boundaries are confirmed, all evidence required for the intended first review is sufficiently clear, and drafting would not require invention.
- `Provisional`: required boundaries and core operating evidence are clear, while optional or refinable evidence remains thin and can stay labeled.
- `Hold`: a required authority, privacy, identity, purpose, economics, capacity, approval, or evidence boundary is unresolved.

Never use `Provisional` to route around a required condition. Use `Missing` instead of supplying a fact the owner did not provide.

## Approval Boundaries

Keep these decisions separate:

- Intake permission authorizes only the bounded intake.
- A meeting, handoff, phase transition, evidence access, or owner interest does
  not authorize a review or action.
- Context approval authorizes only the exact displayed context and approved preservation scope.
- Context effectiveness requires separate operator-confirmed tenant-private persistence.
- Context approval does not authorize an operating review.
- Context approval does not authorize business-plan preparation, plan
  approval, loop design, or execution.
- Operating-review authorization does not authorize publication, pricing, spending, hiring, promotion, customer communication, source changes, or external claims.

Route money and financial classification through `skills/tax-financial-governance/SKILL.md`. Route durable sanitized repository facts through `skills/project-state-update/SKILL.md` only in a separate, explicitly authorized repository task.

## Data And Repository Boundary

- Treat completed packets, exact private economics, customer messages, supplier details, and private operating strategy as tenant-private.
- Produce copy-ready Markdown only. Never write the tenant store, a customer system, or project state.
- A sanitized intake-control manifest is a copy-ready fenced YAML packet, not a mutation. Only a separately invoked `ops intake` command may validate or persist it.
- Keep raw customer-support transcripts outside Git; use owner-approved redacted patterns or external opaque references.
- Never claim a context changed, an operating review occurred, or an external action happened without the corresponding human confirmation.
- Emit reusable learning only as a de-identified doctrine candidate. Require a separate operator-authorized repository task before changing shared doctrine.

## Completion

Complete only with one explicit state:

- `Hold`, naming the missing decision and human authority;
- `Paused` or `Awaiting Owner Response`, naming the checkpoint, open decision,
  and evidence needed to resume;
- `No Change`, `Open Question`, `Rejected`, or `Deferred`;
- an approved packet in `Awaiting Persistence`;
- one operator-confirmed `Effective` version.

For `create` or `resume`, record the separate downstream preparation decision.
Never treat intake, phase progression, meeting capture, context approval,
persistence, operating-review authorization, planning-preparation authority,
plan approval, or external-action approval as interchangeable.
