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
[Continuity Contract v0.3](../../docs/learn-from-choices-continuity-contract-v0.3.md)
for option strategy classification, visible action boundaries, explicit
comparability cohorts, and append-only classification correction. Patterns are diagnostic;
action boundaries identify authority seams but retain
`authority_effect: none`. Only valid explicit comparability policy keys create
cohorts. V0.2 receipts remain compatible, legacy options remain unclassified
without backfill, and the repository push policy remains diagnostic-only.

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

## Active Outcome Learning

For `anyang-internal / anyang-intelligence / repository`, follow
[Learn From Choices Active v1](../../docs/learn-from-choices-active-v1.md) and
[Continuity Contract v0.3](../../docs/learn-from-choices-continuity-contract-v0.3.md).
The prior calibration is disposed `Too thin / Revise` and its receipts remain
historical.

Ordinary Lite selections remain ephemeral. Only when the current decision seam
exactly matches `repository-governance-preflight-v1` may a read-only active
context lookup inform recommendation ordering. Treat its favored or demoted
direction as a rebuttable prior, explain any material effect briefly, yield to
current controlling evidence, and preserve a credible overlooked path.

Bravo, Friction, a completion receipt, or explicit operator feedback may
identify a candidate episode. Persist nothing until the exact same-task packet
is shown in dry run and the operator selects `Execute retain this reviewed
episode`. Missing or cross-task provenance routes to an `RL-*` candidate and is
ineligible for the active cohort. Active guidance never changes authority.

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
