---
name: learner-intake
description: Governed Learning Core intake for creating a first learner profile or changing an existing approved profile. Use when the operator invokes $learner-intake create, $learner-intake change, asks to onboard a new learner, prepare a parent-authorized intake, establish an initial learner profile, review new learner evidence, correct or remove profile content, or propose a guardian-approved profile revision.
---

# Learner Intake

Use this skill as Learning Core's family-facing entry point for learner profiles. Conduct the conversation and produce copy-ready packets; never write a private learner record.

## Required Reads

Read before either mode:

1. `projects/learning-core/parent-intake-to-draft-runbook.md`
2. `projects/learning-core/parent-intake-message.md`
3. `projects/learning-core/parent-intake-summary-template.md`
4. `projects/learning-core/initial-learner-profile-template.md`
5. `references/output-contracts.md`

Read `references/question-strategy.md` before asking family questions. Use `skills/student-operating-system/learner-profile/SKILL.md` as the internal evidence-analysis procedure; do not expose it as a competing family-facing entry point.

## Select The Mode

- `$learner-intake create`: establish a first profile from a parent-authorized intake.
- `$learner-intake change`: review new evidence against the latest effective profile and govern a possible revision.

Accept natural-language equivalents, but state the selected mode. If the mode is unclear, ask whether the operator wants to establish the first profile or reconsider an existing one.

## Shared Authority Gate

Before learner-specific questions:

1. Confirm an operator-supplied opaque learner reference. Treat a parent-approved display label as non-unique.
2. Identify the parent or guardian authorized to approve the profile.
3. Confirm permission for this intake or review.
4. Confirm what may be discussed, temporarily handled, preserved, deleted, and shared.
5. Confirm exclusions and the minimum planning implication of any caution or outside-support context.
6. Confirm whether the current request is `create` or `change`.

Return `Hold` when identity, authority, privacy, preservation, sharing, caution, or mode remains unclear. Do not pressure the family to resolve a boundary within the session.

## Create

1. Require operator confirmation that no effective profile exists for the opaque learner reference.
2. Route an existing profile to `change`; route uncertain identity or possible duplication to `Hold`.
3. Conduct the evidence-first parent conversation. Offer learner voice only after explicit parent approval.
4. Produce an authority receipt and intake/readiness packet.
5. Classify intake as `Ready`, `Provisional`, or `Hold`; classification does not approve a profile or authorize drafting.
6. End a `Hold` with only the missing decision and human authority. For `Ready` or `Provisional`, prepare the separate proposed initial profile.
7. Show the complete proposed profile and ask the named guardian to approve, reject, or request changes.
8. After exact approval, produce an `Approved Initial Profile Packet` with status `Awaiting Persistence`.
9. Mark the profile `Effective` only after the operator supplies tenant-private preservation confirmation.
10. Ask separately whether the guardian authorizes a 30-day draft.

## Change

Require all of these authoritative inputs:

- opaque learner reference;
- latest confirmed-effective profile and version reference;
- corresponding approval receipt;
- current authority and preservation boundaries.

Do not reconstruct them from memory. Return `Hold` when they are missing, stale, or conflicting.

If guardian authority has changed or is disputed, stop until a current authority receipt is established. Do not let profile review itself transfer approval authority.

Then:

1. Ask what prompted review, what may have changed, what recent evidence supports it, and whether boundaries changed.
2. Expand only into affected profile sections.
3. Separate observations, interpretations, hypotheses, and counterevidence.
4. Produce exactly one outcome: `No Change`, `Open Question`, `Profile Change Proposal`, or `Hold`.
5. Keep a single signal as an observation or open question. Require two aligned signals for an ordinary change proposal.
6. Show exact before-and-after wording and the complete proposed resulting profile.
7. Ask the named guardian to approve, reject, or defer the exact change set.
8. Rerender a smaller exact change set before accepting partial approval.
9. After approval, produce an `Approved Change Packet` with status `Awaiting Persistence`.
10. Keep the previous version effective until the operator confirms preservation of the new version.

## State And Approval Rules

```text
CREATE
No profile -> Proposed Initial Profile -> Guardian Approved
           -> Awaiting Persistence -> Effective

CHANGE
Effective Profile -> Evidence Review -> No Change / Proposed Change / Hold
                  -> Approved / Rejected / Deferred
                  -> Awaiting Persistence -> New Effective Version
```

- Allow only one effective version.
- Treat approval and persistence as separate transitions.
- Bind approval to the named guardian, base version, and exact displayed contents.
- Treat vague permission to "update" as insufficient until the exact revision is confirmed.
- Never infer approval from silence, continued participation, weekly review, intake verification, readiness, drafting authorization, or plan approval.
- Let a guardian request reconsideration, correction, or removal at any time; authorize only the exact stated and confirmed action.
- Stop use and enter `Hold` immediately for safety or privacy concerns without silently rewriting the profile.
- Do not reuse content named in a learner correction or removal request while guardian resolution is pending.

## Data And Persistence Boundary

- Treat conversation and draft packets as temporary working state.
- Keep real family information out of Git and repository project files.
- Produce copy-ready Markdown only. Do not write the tenant-private store.
- Treat the operator-controlled tenant-private store as authoritative for effective profiles.
- Keep authority and save/share rules canonical in the authority receipt; reference them from the profile instead of duplicating them.
- Preserve the minimum audit fact for an authorized removal without retaining the removed sensitive content.
- Never claim a profile changed until an authorized operator confirms persistence.

## Recursive Learning

Adapt later questions and next-signal recommendations to approved family evidence without changing the profile silently.

Emit a reusable improvement only as a `De-identified Doctrine Candidate`. Require repeated patterns, remove learner references, quotations, and distinctive family circumstances, and state that a separate operator-authorized repository task is required. Never mutate doctrine during intake.

## Completion

Complete only with one explicit terminal or handoff state:

- `Hold`, with the missing decision and human authority named;
- `No Change`, `Rejected`, or `Deferred`;
- approved packet in `Awaiting Persistence`;
- one operator-confirmed `Effective` version.

For `create`, record the separate 30-day drafting decision. Never treat profile approval as plan-drafting or plan-use approval.
