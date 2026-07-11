# Hold After Review Exemplar

This is a fictional end-to-end example showing how the Learning Core lane should behave when parent review reveals a boundary, concern, or missing clarity that pauses plan use.

It is not a real family, student record, or delivery artifact.

Treat this as the canonical pause exemplar for the `parent reviews -> system updates` part of the Learning Core loop when the correct outcome is **not proceed yet**.

## Purpose

This exemplar exists to show that parent review is not only for:

- approving a plan
- approving with changes

It is also a valid place for:

- stopping
- pausing
- clarifying boundaries
- refusing unsupported plan use

The system should be able to treat a pause as a clean, honest outcome rather than a failure to be hidden.

## Loop Position

This exemplar sits after a draft has already been sent for review:

```text
observe
  -> gather insight
  -> recommend next move
  -> parent reviews
  -> system updates
```

Here, `system updates` means the system records the pause, preserves the reason, and names the next safe requirement before any use.

## Fictional Starting Point

Start from a fictional draft that looked generally usable but still depended on one important unresolved boundary:

- a gentle first-month rhythm was proposed
- Khan Academy Kids was included as a small support block
- a portfolio plan was suggested
- the reading basket direction was set

## Parent Review Response

Fictional parent feedback:

- The overall direction seems helpful.
- Do not use Khan Academy Kids for now.
- Do not save any photos or digital evidence yet.
- I am still deciding what may be written down.
- I do not want child-facing prompts used until I review them more carefully.
- I am concerned that reading frustration may be more serious than I first thought, and I want to think about outside support before using the plan.

## Why This Triggers Hold

This is a `Hold after review` case because:

- the parent withdrew approval for one proposed tool
- save/share boundaries are now unclear again
- child-facing prompt approval is no longer in place
- the parent named a potentially higher-stakes reading concern that they want to consider before use

The system should not treat the original draft as safe to use.

## Example Parent Approval Record

```text
Parent Approval Record

Learner or label: Parent-approved learner label
Plan title: 30-Day Personalized Learning Plan
Plan date range: Month 1
Draft status sent for review: Ready
Parent approver: Parent
Review date: [fictional example date]

Approved now:
- General goal of a calm first-month rhythm
- Reading basket direction in broad terms

Changed by parent:
- Remove Khan Academy Kids from the current plan for now.
- Do not save photos or digital evidence yet.
- Delay child-facing prompts until further parent review.

Not approved yet / still provisional:
- What information may be written down
- What information may be saved
- What information may be shared
- Child-facing prompt language
- Whether outside-support context should be considered in planning

Assumptions still visible:
- Original draft assumed a small app support block.
- Original draft assumed a limited portfolio-photo routine.

Parent questions or concerns:
- Reading frustration may be more serious than first described.
- Parent wants more time before allowing child-facing prompt use.

Next update required:
- Remove app use from the current draft.
- Remove digital evidence suggestions from the current draft.
- Pause child-facing prompt use.
- Clarify save/share rules.
- Clarify whether outside-support context should be considered.

Safe-to-use status:
- no
```

## Example System Update

The system should not merely mark the plan `Hold` and stop thinking.

It should update the working state clearly:

### Original Draft Language

```text
Khan Academy Kids:
- Use for 10-15 minutes on learning days.
- Parent-supervised.

Portfolio evidence:
- Save selected photos of physical work and short parent notes.

Child-facing prompts:
- Use the starter prompts in week 1 after parent approval.
```

### Updated Hold State

```text
Current plan use status:
- Hold after review

Changes required before any plan use:
- Do not include Khan Academy Kids in the current version.
- Do not suggest photos or digital evidence saving yet.
- Do not use child-facing prompts until the parent explicitly approves them.
- Clarify what may be written down, saved, and shared.
- Clarify whether reading concerns should remain in normal plan scope or require outside-support context first.
```

## What The Operator Should Send Next

The next response should be calm and specific.

It should say, in substance:

- thank you for clarifying
- I will pause the plan for now
- I will not use the app block, digital evidence suggestions, or child-facing prompts
- before I revise the plan, I need clear guidance on what may be written down, saved, or shared
- if you want, we can also clarify whether the reading concern should stay in ordinary first-month planning or be considered alongside outside support

This is not a moment to push the draft forward. It is a moment to protect authority and reduce false momentum.

## Why This Matters

This is the final authority test.

A good system knows how to:

- draft
- revise
- pause

If it can only move forward, it is not actually parent-led.

## Failure Modes To Avoid

Do not:

- call the draft approved because some parts were liked
- keep app language active after the parent removed it
- preserve digital evidence suggestions after the parent withdrew permission
- treat a higher-stakes concern as ordinary drift
- keep child-facing prompt language live after approval was withheld

## Minimum Passing Standard

A hold-after-review response passes when:

- the pause reason is visible
- the approval record is updated
- the plan is not treated as safe to use
- the next clarification questions are specific
- the parent remains clearly in authority

## Reusable Pattern

The reusable pattern is:

```text
draft sent
  -> parent raises boundary or concern
  -> approval record updated
  -> safe-to-use status becomes no
  -> next clarification path is named
```

That is the concrete behavior the Learning Core lane should preserve when review stops the plan rather than refining it.
