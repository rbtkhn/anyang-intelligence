---
name: elicitation
description: Low-load Anyang Intelligence elicitation for genuinely missing, materially consequential human input. Use implicitly only when safe execution is blocked by missing judgment, authority, preferences, constraints, or evidence; also use when the operator explicitly asks for elicitation, clarification, discovery questions, requirements gathering, structured intake, or multiple-choice decision support.
---

# Elicitation

Draw out the minimum human input needed to continue safely. Do not use
elicitation to delay work whose answer is already available, safely inferable,
or immaterial.

When meaning is likely present but compressed, automatically read and follow the complete canonical [intent recovery](../intent-recovery/SKILL.md) contract before asking. Use elicitation only when the missing input remains genuinely missing and materially consequential.

## Run Contradiction Preflight When Needed

After intent recovery and before asking, run the read-only contradiction
preflight when a material factual assertion conflicts with, or may supersede,
repository state. Inspect the smallest relevant controlling surface and create
a sanitized structured packet; never ask the checker to search prose or decide
which source governs.

Use:

```text
.\tools\run.ps1 project contradiction-check --packet <packet.yaml> --format markdown
```

- Continue when material assertions align.
- Keep an ordinary unsupported assertion provisional only when it is visibly
  marked provisional.
- Route missing or stale facts to neutral evidence intake.
- Route one request-versus-control conflict to decision navigation.
- Hold conflicting controlling sources for named authority resolution.

The preflight is inspectable guidance with `authority_effect: none`. It never
changes a repository fact, transitions a ledger claim, or becomes a reusable
capability token. Skip it for exact menu selections, clear commands without a
factual conflict, and ordinary missing preferences.

For decision menus and final-response possibility maps, read and follow the
complete canonical
[`learn-from-choices`](../learn-from-choices/SKILL.md) contract.

## Choose The Interaction Type

Keep these surfaces distinct:

### Decision Or Navigation Menu

Use when the human must choose a path. Present 3-4 genuinely different
possibilities with stable semantic roles:

- `recommended`
- `alternative`
- `overlooked`
- `pause-or-deepen`

Explain the recommendation from current evidence without making the choice
leading. Preserve a credible overlooked path and do not manufacture diversity.

### Neutral Evidence Intake

Use when the human is reporting a fact rather than choosing a direction.
Present 2-4 mutually exclusive factual answers. Do not assign recommendation
roles, recommend an answer, or use an action-authorizing label. A neutral
answer is evidence, not action authority and not a Learn From Choices branch
selection.

Allow free-form answers whenever the factual choices do not fit. Do not display
a fifth option merely to permit free-form input.

## Interpret Compact Responses

Map letters to the displayed options in presentation order.

- `A` selects one branch.
- `A,C` selects both branches and processes them left-to-right.
- `A>C>B` records preference order only. Execute nothing, create no
  branch-selection receipt, and use the first-ranked branch to shape the next
  read-only exploration or menu.

Reject duplicate or unknown letters, mixed comma/ranking syntax, and a compound
selection that combines `pause-or-deepen` with another option.

For a compound selection, retain each branch as a separate schema-v8 choice
receipt with the same immutable option set, presentation timestamp, and
option-set hash. Record outcomes independently. If an authorized action fails,
stop before later selections and report which branches remain unexecuted.

Selection frequency remains excluded from recommendation learning, and the
current Learn From Choices calibration freeze remains controlling.

## Apply Visible Action Boundaries

Exploratory selections authorize only read-only navigation already in scope.

A selected decision option authorizes a bounded action only when its visible
label begins with one of these reserved verbs:

- `Execute`
- `Commit`
- `Push`
- `Send`

Match reserved verbs case-insensitively as the label's first token. For example,
`Push the focused commit` authorizes exactly that push, while
`Review and push the focused commit` remains exploratory. Existing authority,
approval, privacy, and safety controls still apply.

Every ledger receipt retains `authority_effect: none`: it records the
operator's instruction but grants no tool access, different action, or broader
authority.

## Ask In Low-Load Batches

Use the lightest shape that resolves the blocker:

- Ask one direct question when one answer blocks progress.
- Deliver structured intake in batches of 1-3 questions through native
  controls, with at most ten questions total.
- In text fallback, ask one blocking question at a time.
- Stop the current and remaining batches immediately when a controlling
  `Hold` is selected or stated.

Do not present a monolithic ten-question form. Ask only questions whose answers
change the next action.

## Preserve Authority

Ask who approves, what may be retained or shared, what must not be assumed, and
what should trigger a hold when those facts materially affect the work.

Operator answers remain bounded to their lane. Parent or guardian authority
controls child-facing Learning Core decisions. The owner controls Grace Gems
commercial claims and customer messages. Human approval controls Media
Production direction, publication, commitments, rights, spending, and hiring.

Do not convert a preference into a customer fact, transfer answers across
project membranes without review, or treat an answer as professional legal,
tax, clinical, educational, accounting, or compliance advice.

## Continue After The Answer

After receiving the required input:

1. Summarize the answer and its authority boundary.
2. Name remaining assumptions or unknowns.
3. Continue the authorized next branch or hold.
4. Update durable repository memory only when the answer changes an approved
   fact, scope, contract, template, checklist, skill, loop, or project state.

Do not store sensitive answers unless the governing authority and privacy
boundary allow it.

## Done When

The minimum missing input has become a clear read-only branch, an exactly
authorized bounded action, a safe hold, a scoped artifact, or an approved
durable update.
