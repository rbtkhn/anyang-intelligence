---
name: learn-from-choices
description: Lightweight, outcome-aware possibility navigation for every final response. Use implicitly to offer 3-4 meaningful adjacent paths, bind a letter to the displayed option and its explicit action boundary, and retain only explicit operator-approved learning without creating a preference bubble.
---

# Learn From Choices

Use this skill in every final user-facing response. Its purpose is to reveal
valuable adjacent possibilities, lower the operator's cognitive load, and
maintain forward momentum. Do not apply the footer to intermediate commentary.

## Response Contract

End every final response with:

```text
Next best possibilities — reply A-D:
A. <recommended path>
B. <strong alternative>
C. <credible overlooked possibility>
D. <pause, deepen, or stop path>
```

Use three options when a fourth would be fake. Keep each option short and make
each change the path, objective, evidence sought, or commitment level. Explain
the recommended branch in one evidence-grounded sentence immediately before
the menu.

Bind displayed options to stable semantic roles independent of letters:

- `recommended`
- `alternative`
- `overlooked`
- `pause-or-deepen`

Preserve a credible overlooked possibility whenever one exists. Never invent
novelty merely to fill a slot.

## Navigation And Authority

A letter selects the displayed option. For an exploratory option, it means
“enter and develop this branch” and authorizes only read-only investigation
already in scope.

When a displayed option is explicitly action-labeled `Execute`, `Commit`,
`Push`, or `Send`, selecting its letter authorizes only that named bounded
action. Existing authority and approval rules remain controlling, and the
selection grants no broader or hidden authority. A later direct command
supersedes any pending menu.

Comma-separated letters select multiple branches in order. Retain each selected
branch as a separate schema-v8 receipt with the same option-set identity and
stop before later branches if an authorized action fails. A ranked response
such as `A>C>B` is preference evidence only: execute nothing, create no
branch-selection receipt, and use the first-ranked branch to shape the next
read-only exploration or menu. Reject duplicates, unknown letters, mixed
comma/ranking syntax, and a compound selection containing `pause-or-deepen`.

Elicitation may separately present 2-4 mutually exclusive neutral factual
answers. Do not force those answers into recommendation roles or treat them as
choice-memory selections.

## Private Choice Memory

Follow the versioned [Lite v1 contract](../../docs/learn-from-choices-lite-v1.md)
as the default. Do not store an unselected footer or an ordinary selected
branch. Do not inspect `choice status`, construct a selection packet, write
SQLite, or warn about missing retention merely because the operator selected a
letter.

Use `bravo` and `friction` only as candidate outcome signals when their
relationship to a branch is supported. Leave unknown cognitive load, momentum,
and discovery dimensions as `Missing`. Persist nothing automatically. Durable
learning requires a separately displayed and selected action such as `Execute
retain this learning`, plus the existing authority and privacy boundary.

Only sanitized, operator-approved repository `RL-*` learning may cross
sessions under Lite defaults. Never promote a repository learning
automatically. The schema-v8 choice ledger and CLI remain an advanced manual
audit surface available only through explicit invocation.

## Recursive Learning

Follow the versioned
[Continuity Contract v0.2](../../docs/learn-from-choices-continuity-contract-v0.2.md)
for option strategy classification, visible action boundaries, explicit
comparability cohorts, and append-only classification correction. Patterns are diagnostic;
action boundaries identify authority seams but retain
`authority_effect: none`. Only valid explicit comparability policy keys create
cohorts. Legacy options remain unclassified without backfill, and the initial
repository push policy is diagnostic-only, so it cannot reorder
recommendations.

Learn from observed outcomes, burden, momentum, and discovery—not selection
frequency.

- One or two comparable outcomes are thin evidence. Mention them without
  reordering possibilities.
- After at least three comparable resolved outcomes, two consistent results
  with no material contradiction may change the recommended branch.
- Repeated selection alone never changes ordering.
- Always keep a credible overlooked path even when another path has strong
  outcome evidence.
- Surface authority, privacy, safety, or membrane incidents immediately,
  regardless of sample size.
- Keep tenant outcomes in their lane. Cross membranes only with sanitized,
  operator-approved learning.

After at least five explicit, comparable, outcome-supported learnings, a
read-only review may recommend a contract change. The operator must separately
authorize that change.

## Held Calibration Pilot

For `anyang-internal / anyang-intelligence / repository`, the versioned
[Learn From Choices Calibration Pilot](../../docs/learn-from-choices-calibration-pilot-2026-07-30.md)
is held for continuity-provenance review. Do not tag or retain ordinary Lite
selections. Recommendation ordering remains frozen against pilot outcomes and
selection frequency until an explicit later disposition authorizes a change.
Continue to surface immediate authority or membrane guardrails.

## Composition

- `coffee` retains its four-option ritual but does not solicit unresolved choice
  outcomes under Lite defaults.
- `elicitation` uses this contract for low-load decision menus.
- `bravo` may supply positive or mixed outcome evidence.
- `friction` may supply mixed or unsuccessful outcome evidence.
- `dream` consolidates landed work but does not solicit unresolved choices.

## Done When

The final response offers a small, genuinely diverse map; the recommendation is
transparent; selecting a letter navigates without silently authorizing action;
and learning expands useful possibility space without forming a preference
bubble.
