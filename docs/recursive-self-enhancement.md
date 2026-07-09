# Recursive Self-Enhancement

Recursive self-enhancement, as defined in this repo, is:

A work cycle produces friction or learning, and Anyang Intelligence improves the operating system that will handle the next similar cycle.

In practical terms:

```text
work happens
  -> friction or pattern appears
  -> we name the learning
  -> we choose one durable improvement
  -> we update a doc, skill, template, checklist, loop, or guardrail
  -> the next cycle starts smarter
```

The key distinction is that the system does not merely remember what happened. It changes its own operating surface so a future agent, operator, or customer lane does not need to rediscover the same lesson from chat memory.

This is not autonomous self-modification in the loose sci-fi sense. It is governed improvement: human-approved, repo-visible, evidence-backed changes to the procedures Anyang Intelligence uses to do future work.

## Core Rule

The output of a work cycle should improve the next similar cycle when, and only when, there is a durable lesson worth preserving.

That preservation should happen in repo-visible operating surfaces such as:

- docs
- skills
- templates
- checklists
- loops
- validators
- guardrails

Do not treat chat recall alone as system improvement.

## Why It Matters

Anyang Intelligence compounds when real work becomes better infrastructure.

The point is not to accumulate anecdotes. The point is to reduce repeated confusion, prevent known failure modes, and raise the baseline quality of future work across agents, operators, and customer lanes.

This means the system should not simply say:

- we learned something

It should also answer:

- where is that learning now encoded?
- what future work is safer, faster, or clearer because of it?

## Standard Cycle

Use this default sequence:

1. Work happens.
2. Friction, failure, ambiguity, or a reusable pattern appears.
3. Name the learning in plain language.
4. Choose one durable improvement.
5. Update the relevant operating surface.
6. Validate the change when possible.
7. Let the next cycle inherit the improvement.

The improvement should be small enough to stay grounded and large enough to matter.

## Relation To Loops

[Loops](loops.md) are the operating grammar for recursive self-enhancement.

Every durable improvement should be expressible as a loop update:

- **Signal:** What friction, failure, ambiguity, or repeated move started the improvement?
- **Memory objects:** What facts, artifacts, decisions, or patterns need to be preserved?
- **Decision:** What improvement should be made, and why this one instead of another?
- **Action:** Which doc, skill, template, checklist, loop, validator, or guardrail changes?
- **Evidence:** What proves the improvement landed?
- **Cadence:** When should this be revisited?
- **Learning update:** What changes for the next similar cycle?
- **Governance boundary:** Who approves the change, and what authority does the system not have?

If the loop cannot name its learning update, the system noticed friction but did not yet enhance itself.

## Relation To Coffee

Native [coffee](../skills/coffee/SKILL.md) is the lightweight cadence that notices recursive self-enhancement opportunities.

Coffee should not improve everything at once. It should name:

- the current picture
- the entropy or friction
- one learning
- one improvement candidate
- a bounded next action

That makes coffee the detection and selection ritual. The enhancement itself is complete only when the chosen improvement is preserved in a repo-visible surface and, when possible, validated.

## Relation To Dream

Native [dream](../skills/dream/SKILL.md) is the closeout cadence that confirms what actually landed.

Dream should not choose a new improvement by default. It should settle the work cycle by naming:

- what was preserved in durable repo surfaces
- what validation passed, failed, or was skipped
- what warnings are known legacy noise versus fresh issues
- which authority or membrane boundaries still matter
- what tomorrow inherits

That makes dream the consolidation ritual. If coffee asks what should improve next, dream asks what the repo can safely carry forward.

## Relation To Bravo

Native [bravo](../skills/bravo/SKILL.md) is the positive-signal cadence that captures what the operator found especially good.

Recursive self-enhancement should learn from excellence as well as friction. Bravo names:

- what was praised
- which property made it valuable
- where the pattern might repeat
- what boundary prevents overgeneralization
- whether the signal is a note, candidate, or preservation request

That makes bravo the reinforcement ritual. If coffee notices what may need improvement and dream confirms what landed, bravo notices what should be repeated.

## Relation To Friction

Native [friction](../skills/friction/SKILL.md) is the dissatisfaction-signal cadence that captures what missed.

Friction names:

- what did not work
- the likely failure mode
- the smallest repair path
- what future agents should do differently
- what boundary prevents overcorrection

That makes friction the repair ritual. If bravo notices what should be repeated, friction notices what should be revised, guarded, or tested before it recurs.

## Durable Improvement Test

A change qualifies as recursive self-enhancement when it is:

- human-approved
- repo-visible
- grounded in actual work
- specific enough to reuse
- narrow enough not to overfit one conversation
- safe within the relevant governance membrane

If the lesson remains only in chat, it is not complete.

If the change crosses authority, privacy, customer-scope, or safety boundaries, it is not governed improvement.

For an end-of-cycle operating gate, use [recursive-self-enhancement-checklist.md](recursive-self-enhancement-checklist.md).

## Elementary School Example

The Elementary School lane provides a clean example:

```text
parent intake idea
  -> mock intake simulations
  -> Hold failure mode appears
  -> Hold response template added
  -> intake readiness loop formalized
  -> future intake work now has a safer path
```

The important point is not that the system discussed a failure mode. The important point is that the failure mode was converted into a reusable operating surface.

That is the difference between memory and enhancement.

The formal loop version lives in [customers/elementary-school/loop-examples/parent-intake-readiness.yaml](../customers/elementary-school/loop-examples/parent-intake-readiness.yaml). Its learning update requires real or simulated intake outcomes to improve the intake message, readiness checklist, Hold response, or plan template when a recurring failure mode appears.

## Boundaries

Recursive self-enhancement does not mean:

- unrestricted self-modification
- hidden prompt drift
- silent policy change
- autonomous authority expansion
- replacing human review with agent momentum

The governing constraints still apply:

- humans remain the authority layer
- the strictest applicable membrane wins
- high-trust lanes require stronger safety discipline
- private customer facts do not automatically become general product doctrine

## Preferred Output Shapes

When a cycle reveals a durable lesson, prefer one of these output shapes:

- a clarified doctrine doc
- a new skill step or guardrail
- a checklist that prevents a known miss
- a template that removes repeated ambiguity
- a validator or lint rule
- a README link that makes the improvement discoverable

Choose the lightest artifact that prevents the problem from recurring.

## Completion Question

At the end of a work cycle, ask:

`What changed in the operating surface so the next similar cycle starts smarter?`

If there is no answer, the work may be finished, but recursive self-enhancement has not yet occurred.
