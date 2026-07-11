---
name: friction
preferred_activation: friction
description: Native Anyang Intelligence dissatisfaction and miss-capture ritual. Use for friction, not quite, that missed, wrong direction, too generic, too much, too little, weak, this is not working, or operator dissatisfaction with an answer, artifact, workflow, skill, decision, or repo change to classify what failed, choose a repair path, and decide whether the lesson should become a durable repo-visible improvement.
category: operator-coherence
status: active
scope_class: repo-governed
---

# Friction

**Preferred activation:** say `friction`.

`friction` is the native Anyang Intelligence dissatisfaction-signal capture ritual. It converts a miss, weak output, wrong direction, or operator dissatisfaction into a precise repair signal without turning the moment into apology theater, self-critique, or broad overcorrection.

Use `friction` when the operator says or implies:

- `friction`
- `not quite`
- `that missed`
- `wrong direction`
- `too generic`
- `too much`
- `too little`
- `weak`
- `I don't like this`
- `this is not working`

## Purpose

`friction` helps Anyang Intelligence learn from dissatisfaction as cleanly as `bravo` learns from satisfaction.

The key question is:

```text
What did not work, why did it miss, and what should change next time without overcorrecting?
```

## Inputs

Read or infer from the current thread first:

1. The answer, artifact, workflow, decision, or repo change that missed.
2. The immediate context: project lane, skill, doc, CLI, template, governance surface, or operator cadence.
3. Any explicit reason the operator gave for dissatisfaction.
4. The expected direction from the previous prompt or menu choice.
5. `git status --short --branch` only if the miss appears tied to repo state or a file change.

Optional, only when directly relevant:

- `docs/recursive-self-enhancement.md`
- `docs/operating-substrate.md`
- `skills/coffee/SKILL.md`
- `skills/bravo/SKILL.md`
- `skills/dream/SKILL.md`
- the customer, skill, CLI, or doc artifact that missed

## Procedure

1. Identify the missed object. If unclear, name the most likely object from the immediate context.
2. State the miss concretely. Avoid vague language like "I failed" or "quality was bad."
3. Classify the likely failure mode using the taxonomy below.
4. Choose the smallest repair path:
   - immediate revision
   - ask one clarifying question
   - update a skill
   - add a checklist
   - add a validator or lint rule
   - leave as one-off context
5. Name the reusable lesson, if one exists.
6. Name the boundary: what should not be generalized, automated, or overcorrected from this single miss.
7. Do not edit files unless the operator asks to preserve the lesson or the requested repair clearly requires implementation.

## Failure Mode Taxonomy

Use one or more:

- `Too generic`: failed to use repo, customer, or artifact context.
- `Too verbose`: buried the useful move.
- `Too thin`: lacked enough detail to act.
- `Wrong object`: optimized the wrong artifact, question, or decision.
- `Authority miss`: blurred human approval, customer commitment, child-safety, legal/tax, publication, or spending authority.
- `Membrane leak`: risked transferring private or customer-local facts into shared doctrine.
- `Stale context`: used old names, paths, or assumptions.
- `Overbuilt`: created process when a lighter move was enough.
- `Underbuilt`: skipped necessary guardrail, evidence, or validation.
- `Tone miss`: sounded salesy, anxious, flat, mechanical, or misaligned.
- `Validation gap`: made a confident claim without checking.

## Output Shape

Use this structure:

```text
Friction captured:
<one sentence naming what missed.>

Likely failure mode:
- <classification>

Repair path:
- Immediate revision / ask one clarifying question / update skill / add checklist / add validator / leave as one-off

Reusable lesson:
- <what future agents should do differently>

Boundary:
- <what not to overgeneralize from this miss>

Recommended next step:
- <smallest useful next action>
```

Keep it short unless the operator asks for deeper analysis.

## Relationship To Coffee, Bravo, And Dream

`coffee`, `bravo`, `friction`, and `dream` form the native Anyang Intelligence cadence loop:

- `coffee` detects entropy and chooses the next improvement candidate.
- `bravo` reinforces what worked.
- `friction` repairs what missed.
- `dream` confirms what landed and what tomorrow inherits.

The loop is:

```text
coffee detects
work changes
bravo reinforces
friction repairs
dream consolidates
coffee inherits
```

`friction` should strengthen the next cycle, not punish the current one.

## Guardrails

- Do not apologize performatively.
- Do not turn dissatisfaction into self-critique.
- Do not ask the operator to explain what is obvious from context.
- Do not convert every complaint into doctrine.
- Do not overcorrect from one miss.
- Do not weaken human authority or membrane boundaries to satisfy the moment.
- Do not preserve private, sensitive, or customer-local context as shared product doctrine.
- Prefer one precise repair over a broad rewrite.

## Done When

The operator sees:

- what missed
- why it likely missed
- the smallest repair path
- whether there is a reusable lesson
- what boundary prevents overgeneralization
