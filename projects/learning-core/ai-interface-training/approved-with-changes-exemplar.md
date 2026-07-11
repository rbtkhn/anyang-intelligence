# Approved With Changes Exemplar

This is a fictional end-to-end example showing how the Elementary School lane should behave when a parent reviews a draft, approves the direction, and requests changes before use.

It is not a real family, student record, or delivery artifact.

Treat this as the canonical revision exemplar for the `parent reviews -> system updates` part of the Elementary School loop.

## Purpose

This exemplar exists to show that approval is not binary.

A useful parent review may say:

- yes to the direction
- no to one part of the plan
- yes, but shorter
- yes, but change what gets saved
- yes, but remove one activity type

The system should be able to absorb those changes cleanly without losing authority clarity.

## Loop Position

This exemplar sits after the first draft:

```text
observe
  -> gather insight
  -> recommend next move
  -> parent reviews
  -> system updates
```

Its job is to show what `system updates` actually looks like.

## Fictional Starting Point

Start from the same fictional `Ready` scenario used in [ready-plan-exemplar.md](ready-plan-exemplar.md).

Assume the first draft included:

- Monday-Thursday mid-morning rhythm
- 15 minutes of Khan Academy Kids on learning days
- animal/nature/drawing/building emphasis
- physical folder plus phone-photo portfolio
- weekly proud-work choice

## Parent Review Response

Fictional parent feedback:

- The overall rhythm feels good.
- Keep the animal and nature emphasis.
- Reduce Khan Academy Kids from 15 minutes to 10 minutes.
- Keep app use inside a strict household screen-time budget.
- Use the physical folder, but save fewer phone photos.
- Keep weekly proud-work choice.
- Replace one Week 2 counting game suggestion with more outdoor observation because the child responds better outside.
- Do not save screenshots from apps.

## What Changed

This is the key discipline point:

The system should not merely note the feedback. It should update the actual plan and approval record so the new approved state becomes visible.

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
- Daily rhythm: Monday-Thursday mid-morning
- Screen-time budget / no-budget decision: strict household screen-time budget in place
- Khan Academy Kids rule: allowed for 10 minutes on learning days, parent-supervised, inside household screen-time budget
- Reading basket direction: keep animal, nature, and easy-reader emphasis
- Portfolio evidence plan: physical folder plus limited phone photos
- Week 1 focus: approved
- Child-facing prompts or survey language: approved
- Watch items / support framing: reading avoidance and worksheet frustration phrased calmly
- What information may be saved: parent notes, proud work, selected photos of physical work
- What information may be shared: no sharing outside household without parent approval
- First monthly portfolio review shape: approved

Changed by parent:
- Reduce Khan Academy Kids from 15 minutes to 10 minutes.
- Keep app time inside strict household screen-time budget.
- Save fewer phone photos.
- Replace one Week 2 counting-game emphasis with more outdoor observation.
- Do not save app screenshots.

Not approved yet / still provisional:
- None.

Assumptions still visible:
- None required for use.

Parent questions or concerns:
- Keep the plan light and avoid drifting into too much documentation.

Next update required:
- Update app rule in draft.
- Update portfolio evidence wording in draft.
- Update Week 2 activity emphasis in draft.

Safe-to-use status:
- only after listed updates
```

## Example Draft Revision

Below is a shortened example of what should change in the actual plan after review.

### Before Parent Review

```text
Khan Academy Kids use rule:
- Use for 15 minutes on learning days.
- Parent-supervised.
- Treat as practice and observation, not as a grade, diagnosis, curriculum replacement, or proof of mastery.

Portfolio evidence plan:
- Use the physical folder plus phone photos.
- Save proud work, useful photos, and short notes only when they help reveal the learning arc.

Week 2 focus:
- Goal: increase confidence through easy wins and hands-on math.
- Activities:
  - dice or card counting games
  - easy-reader time with parent support
  - building or sorting activity tied to interests
```

### After Parent Review

```text
Khan Academy Kids use rule:
- Use for 10 minutes on learning days.
- Parent-supervised.
- Keep use inside the household screen-time budget.
- Treat as practice and observation, not as a grade, diagnosis, curriculum replacement, or proof of mastery.

Portfolio evidence plan:
- Use the physical folder as the main record.
- Save proud work, selected photos of physical work, and short parent notes only when they help reveal the learning arc.
- Do not save app screenshots.

Week 2 focus:
- Goal: increase confidence through easy wins and supported outdoor observation.
- Activities:
  - easy-reader time with parent support
  - outdoor nature observation tied to current interests
  - one light math or counting moment only if it stays low-pressure
```

## Why This Matters

This is the real authority test.

A good system does not merely produce a strong first draft. It also:

- receives parent review without confusion
- records what changed
- updates the draft to match the approved state
- keeps unsupported old wording from lingering

## Failure Modes To Avoid

Do not:

- keep the old app rule in the plan after the parent changed it
- let the approval record and plan disagree
- describe the draft as approved when updates are still required
- save evidence types the parent declined
- treat parent edits as optional taste notes instead of authority

## Minimum Passing Standard

An approved-with-changes revision passes when:

- the parent's requested changes are visible
- the approval record and revised plan match
- the safe-to-use status is honest
- no removed or declined element remains active by accident

## Reusable Pattern

The reusable pattern is:

```text
draft sent
  -> parent changes named
  -> approval record updated
  -> plan revised
  -> safe-to-use status rechecked
```

That is the concrete behavior the Elementary School lane should preserve.
