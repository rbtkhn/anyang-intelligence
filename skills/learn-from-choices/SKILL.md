---
name: learn-from-choices
description: Outcome-aware possibility navigation for every final response. Use implicitly to offer 3-4 meaningful adjacent paths, bind a letter to the displayed option and its explicit action boundary, and learn from observed usefulness without creating a preference bubble.
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

Do not store an unselected footer. After the operator selects a branch, and
first inspect continuity without writing:

```text
.\tools\run.ps1 ops choice status --format json
```

Only when the result is `ready`, record the exact sanitized option set and
selection atomically. Run the existing dry run before the write:

```text
.\tools\run.ps1 ops choice select --tenant anyang-internal --packet selection.yaml --dry-run
```

Review the dry run before mutation. The selection receipt grants no execution
authority. Link evidence by reference; never place private evidence bodies in
the ledger. A retention failure does not block the selected branch: disclose it
once and exclude the selection from the calibration cohort.

Configure continuity only through the explicit, separately authorized command
`choice configure --data-dir <absolute-external-directory>`. Never create or
activate private operating state merely because a footer was selected.

Outcome events are optional during ordinary work:

```text
.\tools\run.ps1 ops --db <private-db> choice outcome <CHOICE_ID> --packet outcome.yaml --dry-run
```

Use `bravo` and `friction` as outcome signals when the relationship to a
selected branch is supported. Leave unknown cognitive load, momentum, and
discovery dimensions as `Missing`. Unresolved choices return only through
`coffee`; do not interrupt ordinary work or `dream` to solicit them.

If the private ledger is unavailable, continue navigation, say that the
selection was not retained when retention would otherwise be expected, and use
only operator-approved repository `RL-*` learning. Never promote a repository learning automatically.

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

After five resolved selections, `coffee` may offer one lightweight review
branch to assess cognitive load, momentum, and discovery value.

## Active Calibration Pilot

For `anyang-internal / anyang-intelligence / repository`, follow the versioned
[Learn From Choices Calibration Pilot](../../docs/learn-from-choices-calibration-pilot-2026-07-30.md)
from 2026-07-30 through 2026-08-05, America/Denver.

During this calibration window, recommendation ordering remains frozen against
pilot outcomes even if a three-outcome pattern appears. Treat outcome patterns
as diagnostic, continue to surface immediate authority or membrane guardrails,
and never infer missing subjective measurements. At expiry, do not silently
extend the pilot; outcome-informed reordering remains frozen until an explicit
review disposition authorizes a later state.

For every selection presented during the observation window in this exact
scope, include `LFC-CAL-2026-07-30-01` in `learning_refs`. If the tag cannot be
retained, disclose the gap and exclude that selection from the pilot cohort.
The `choice context` policy is controlling for machine-readable
`diagnostic-only` guidance; its favored and demoted patterns are evidence
diagnostics, not permission to reorder options.

## Composition

- `coffee` owns unresolved-outcome follow-up and retains its four-option ritual.
- `elicitation` uses this contract for low-load decision menus.
- `bravo` may supply positive or mixed outcome evidence.
- `friction` may supply mixed or unsuccessful outcome evidence.
- `dream` consolidates landed work but does not solicit unresolved choices.

## Done When

The final response offers a small, genuinely diverse map; the recommendation is
transparent; selecting a letter navigates without silently authorizing action;
and learning expands useful possibility space without forming a preference
bubble.
