---
name: elicitation
description: Native Anyang Intelligence elicitation procedure. Use when the operator asks for elicitation, multiple-choice questions, intake questions, discovery questions, clarification, decision support, requirements gathering, or when a customer/skill/doc task depends on missing human judgment, authority, preferences, constraints, or context before safe execution.
---

# Elicitation Skill

Use this skill to draw out the minimum human input needed for high-quality Anyang Intelligence work.

Elicitation is not interrogation. It is a structured way to help the operator or customer make hidden context explicit so the Executive OS can act safely and usefully.

## Purpose

Use elicitation to:

- Clarify goals, constraints, preferences, and authority.
- Convert fuzzy intent into usable operating inputs.
- Surface risks before execution.
- Preserve human judgment where the system lacks authority.
- Avoid invented facts.
- Make future work faster by turning answers into a clear next artifact or action.

## When To Ask

Ask questions when missing information materially affects:

- paid scope
- customer commitments
- parent, owner, board, or operator authority
- child-safety, legal, tax, financial, property, nonprofit, or health-sensitive boundaries
- public claims, publication, delivery, spending, hiring, or external communications
- personal preferences that cannot be inferred from repo state
- product direction where several plausible paths have different consequences

Do not ask when the answer is already in the repo, can be safely inferred, or the cost of delay is higher than the risk of a reasonable assumption.

## Procedure

### 1. Name The Unknowns

Before asking, identify what is actually missing:

- Goal: What outcome is wanted?
- Authority: Who can approve?
- Scope: What is included or excluded?
- Evidence: What facts or receipts exist?
- Constraints: Time, budget, capacity, tone, tools, safety, privacy.
- Preference: Which tradeoff should be optimized?
- Risk: What could go wrong if the system guesses?

Ask only for information that changes the next action.

### 2. Choose The Elicitation Shape

Use the lightest shape that works:

- **Single direct question:** when one answer blocks progress.
- **Multiple choice:** when the operator is choosing among known paths.
- **Ranked options:** when priority order matters.
- **10-question intake:** when building a new scope, offer, skill, customer intake, or strategy from sparse context.
- **Hold questions:** when authority, privacy, safety, or basic context is missing.

Prefer multiple choice when it lowers effort, but include an optional free-form escape hatch when nuance matters.

### 3. Write Good Multiple Choice Questions

Each question should:

- Ask one decision.
- Use plain language.
- Offer 3-5 distinct options.
- Make tradeoffs visible.
- Avoid leading the operator toward the answer the agent wants.
- Include "not sure yet" only when uncertainty is itself a useful state.

Use labels like `A`, `B`, `C`, `D` when the operator may answer compactly.

Good option text:

```text
A. Fast proof - prioritize the smallest artifact that can test demand this week.
B. Trust proof - prioritize safety, authority, and review boundaries before any outward motion.
C. Product proof - prioritize reusable templates and primitives even if delivery is slower.
D. Not sure yet - ask a narrower follow-up.
```

Avoid:

- fake choices
- overlapping options
- more questions than needed
- asking the user to restate context already in the repo
- asking open-ended questions when a structured choice would work

### 4. Preserve Authority

If the elicitation involves a high-trust lane, include authority checks:

- Who approves this?
- What may be saved or shared?
- What should not be assumed?
- What would require professional review?
- What should trigger a pause?

For Learning Core, parent or guardian authority controls child-facing decisions, saved/shared information, outside-support escalation, and plan use.

For Grace Gems, owner approval controls product, pricing, policy, authenticity, shipping, return, certificate, rush-order, promotion, and customer-message claims.

For Media Production, human approval controls creative direction, publication, client commitments, rights, spending, hiring, and external claims.

### 5. Turn Answers Into Action

After answers arrive:

1. Summarize the choice in plain language.
2. Name assumptions and unresolved unknowns.
3. Identify the next artifact or action.
4. Update repo memory only when the answer changes a durable fact, scope, template, skill, checklist, loop, or project state.
5. If the answers reveal a recurring pattern, consider [../../docs/recursive-self-enhancement-checklist.md](../../docs/recursive-self-enhancement-checklist.md).

Do not treat an answer as authority beyond the lane it belongs to.

## Output Templates

### Short Elicitation

```text
I need one choice before I can do this safely:

A. <option and tradeoff>
B. <option and tradeoff>
C. <option and tradeoff>
D. Not sure yet - I will narrow the question.
```

### 10-Question Intake

```text
Answer with the letter for each question, like `1A 2C 3B`.

1. <question>
A. <option>
B. <option>
C. <option>
D. <option>

...

10. <question>
A. <option>
B. <option>
C. <option>
D. <option>
```

### Answer Synthesis

```text
Elicitation summary:
- Direction chosen:
- Authority boundary:
- Constraints:
- Open unknowns:
- Next artifact/action:
- Repo update needed: yes/no
```

## Guardrails

Do not:

- Use elicitation to delay obvious work.
- Ask for private facts that are not needed.
- Convert preferences into customer facts without confirmation.
- Transfer answers across project lanes without membrane review.
- Treat operator answers as legal, tax, clinical, educational, accounting, or compliance conclusions.
- Ask children directly unless a parent-approved Student Operating System skill explicitly governs the interaction.
- Store sensitive answers in durable docs unless the authority and privacy boundary allow it.

## Done When

Elicitation is done when the missing human input has been converted into:

- a clear next action,
- a safe hold,
- a scoped artifact,
- or a durable repo update with authority boundaries intact.
