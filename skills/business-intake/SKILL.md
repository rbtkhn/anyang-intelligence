---
name: business-intake
description: Governed owner-facing intake for creating an initial business context or changing an existing approved context. Use only when the operator explicitly invokes $business-intake create or $business-intake change to gather business goals, operating evidence, economics, capacity constraints, owner authority, and data-handling boundaries before an operating review.
---

# Business Intake

Use this skill as the owner-facing entry point for commercial business installations. Conduct the conversation and produce copy-ready packets; never write a private business record or change repository state.

## Required Reads

Read before either mode:

1. `references/question-strategy.md`
2. `references/output-contracts.md`
3. `docs/data-handling-policy.md`
4. `docs/governance.md`
5. `docs/membranes.md`

For Grace Gems, also read `projects/grace-gems/business-intake-survey.md`. For Mountain Villa, also read `projects/mountain-villa/business-intake-survey.md`. Treat each as a project-specific question set under this skill, not as a separate authority or persistence workflow.

## Select The Mode

Support exactly these explicit modes:

- `$business-intake create`: establish an initial owner-approved business context.
- `$business-intake change`: review new evidence against the latest effective context and govern a possible revision.

If the explicit invocation does not name one mode, ask whether the operator intends to establish the first context or reconsider an effective one. Do not begin private questions until the mode is clear.

## Authority And Data Gate

Before business-specific questions:

1. Confirm an operator-supplied business reference.
2. Identify the owner authorized to approve the context.
3. Confirm the intake purpose and permission.
4. Confirm what evidence may be discussed, handled temporarily, preserved, deleted, and shared.
5. Confirm exclusions, reuse restrictions, and pause conditions.
6. Confirm the requested mode.

Return `Hold` when identity, authority, purpose, privacy, preservation, sharing, deletion, exclusions, or mode remains unclear. Request only the missing decision; do not pressure the owner to disclose private information.

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
10. Ask separately whether the owner authorizes preparation of the first operating review.

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
- Context approval authorizes only the exact displayed context and approved preservation scope.
- Context effectiveness requires separate operator-confirmed tenant-private persistence.
- Context approval does not authorize an operating review.
- Operating-review authorization does not authorize publication, pricing, spending, hiring, promotion, customer communication, source changes, or external claims.

Route money and financial classification through `skills/tax-financial-governance/SKILL.md`. Route durable sanitized repository facts through `skills/project-state-update/SKILL.md` only in a separate, explicitly authorized repository task.

## Data And Repository Boundary

- Treat completed packets, exact private economics, customer messages, supplier details, and private operating strategy as tenant-private.
- Produce copy-ready Markdown only. Never write the tenant store, a customer system, or project state.
- Keep raw customer-support transcripts outside Git; use owner-approved redacted patterns or external opaque references.
- Never claim a context changed, an operating review occurred, or an external action happened without the corresponding human confirmation.
- Emit reusable learning only as a de-identified doctrine candidate. Require a separate operator-authorized repository task before changing shared doctrine.

## Completion

Complete only with one explicit state:

- `Hold`, naming the missing decision and human authority;
- `No Change`, `Open Question`, `Rejected`, or `Deferred`;
- an approved packet in `Awaiting Persistence`;
- one operator-confirmed `Effective` version.

For `create`, record the separate operating-review decision. Never treat intake, context approval, persistence, operating-review authorization, or external-action approval as interchangeable.
