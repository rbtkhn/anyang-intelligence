---
name: coffee
preferred_activation: coffee
description: Lightweight Anyang Intelligence re-entry ritual for restoring operating context, naming live obligations, and choosing the next best move.
category: operator-coherence
status: active
scope_class: repo-governed
---

# Coffee

**Preferred activation:** say `coffee`.

`coffee` is the Anyang Intelligence re-entry ritual. It should feel like a short sip of coherence: enough orientation to restore momentum, not a heavy maintenance pass.

Use `coffee` when the operator asks:

- `coffee`
- `where are we`
- `what next`
- `pause and reflect`
- `reentry`
- `current state`

## Purpose

`coffee` helps the operator quickly see:

- the current operating picture
- which customer obligations are live
- what is waiting on external input
- where repo memory may be thin, stale, or contradictory
- the highest-leverage next actions

## Inputs

Read these first, in order:

1. `customers/operating-portfolio-dashboard.md`
2. `customers/comparison-matrix.md`
3. `customers/commercial-hypotheses.md`
4. `git status --short --branch`
5. Recent commits when useful: `git log --oneline -5`

Optional, only when directly relevant:

- the specific customer `README.md`
- the customer install or scope document
- `skills/customer-state-update/SKILL.md` if new customer facts appeared

## Procedure

1. Read the portfolio dashboard first. Treat it as the freshest repo-level source of truth unless the operator has just corrected it.
2. Check git state so the operator knows whether the repo is clean, dirty, ahead, or behind.
3. Identify paid obligations first. Do not let unpaid complexity crowd out paid commitments.
4. Separate confirmed facts from hypotheses, donor-funded support, optional donations, revenue, expenses, asset values, and unplanned scope.
5. Scan for contradiction risk: customer status, money, paid/free access, employee-facing language, and outward-facing brand language.
6. Produce a concise re-entry brief with the sections below.
7. Do not edit, stage, commit, or push by default. `coffee` is read-only unless the operator chooses an action and asks to proceed.

## Output Shape

Use this structure:

```text
Current picture:
<2-4 sentences grounded in repo state.>

Live obligations:
- <confirmed obligation, especially paid or time-sensitive>

Waiting on:
- <external input, missing scope, or blocked decision>

Entropy flags:
- <thin, stale, or contradictory area>

Coffee menu - reply A-D:
A. Confirm - <specific repo-grounded verification or cleanup move>
B. Scope - <specific paid/customer obligation to define>
C. Deepen - <specific customer context to enrich>
D. Ship - <specific implementation/documentation move ready to execute>
```

## Menu Rules

- Always offer exactly four options: A through D.
- Each option must be a concrete action, not a bare label.
- Prefer actions that reduce uncertainty, clarify obligations, or convert a paid commitment into a defined operating plan.
- If one option is clearly best, mark it with `(recommended)`.
- Stop on the menu unless the operator already gave permission to proceed.

## Guardrails

- Keep it light. `coffee` is a re-entry ritual, not a full audit.
- Do not invent facts that are not in the repo or the current conversation.
- Do not refer to customer-facing or employee-facing documents as products of Anyang Intelligence unless that boundary is already approved.
- Use `Anyang Intelligence`, not shortened `Anyang`, in outward-facing language.
- Preserve the distinction between free participation and donor-funded support.
- Preserve the distinction between a one-time retainer and a recurring subscription.
- Preserve the distinction between Media Production's own operating system and the content it creates for Grace Gems or Predictive History.

## Done When

The operator has a clear current-state brief and a bounded A-D choice set for the next move.
