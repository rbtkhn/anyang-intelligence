---
name: learn-from-choices
description: Outcome-aware possibility navigation for every final response. Use implicitly to offer 3-4 meaningful adjacent paths, interpret a letter as navigation rather than execution authority, and learn from observed usefulness without creating a preference bubble.
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

A letter means “enter and develop this branch.” It authorizes read-only
investigation that is already in scope. It does not authorize mutation,
execution, spending, publication, communication, customer action, commit, or
push.

When a branch reaches an action boundary, offer an explicitly labeled later
option such as `Execute`, `Commit`, `Push`, or `Send`. Existing authority and
approval rules remain controlling. A later explicit command supersedes any
pending menu.

## Private Choice Memory

Do not store an unselected footer. After the operator selects a branch, and
only when a private ledger is configured, record the exact sanitized option set
and selection atomically:

```text
.\tools\run.ps1 ops --db <private-db> choice select --tenant <tenant> --packet selection.yaml --dry-run
```

Review the dry run before mutation. The selection receipt grants no execution
authority. Link evidence by reference; never place private evidence bodies in
the ledger.

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
