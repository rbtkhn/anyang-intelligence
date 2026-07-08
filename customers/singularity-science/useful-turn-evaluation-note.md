# Useful Turn Evaluation Note

This note captures a Singularity Science evaluation lens: the real competitive unit may be the useful turn, not the model in isolation.

Its purpose is to help Anyang Intelligence evaluate AI systems based on completed work and governed delegation, not only benchmark rank or model branding.

Use with:

- [ambient-agency-use-case-map.md](ambient-agency-use-case-map.md)
- [primitives/ambient-agency-review-gate.md](primitives/ambient-agency-review-gate.md)
- [research-operating-model.md](research-operating-model.md)

## Core Claim

Users do not buy a model in the abstract. They buy a completed chunk of useful work.

That means the practical competitive unit may be:

- how much work a single turn can do
- how much orchestration happens inside one interaction
- how cheaply that work can be delivered
- how continuously the system can stay engaged

The more important question is often not "which model is smartest?" but "how much real task progress happens before the human has to step back in?"

## What Is A Useful Turn

A useful turn is one bounded interaction cycle that produces meaningful forward motion.

Examples:

- a draft that is actually ready for review
- a research pass that surfaces the right sources and tensions
- a coding pass that implements and validates a coherent slice
- a coordination pass that reduces follow-up load
- a planning pass that cleanly identifies next decisions, not just ideas

A turn is more useful when it reduces the need for re-prompting, correction, context rebuilding, and hidden supervision.

## Why This Matters

### 1. Model rank is not the whole product

Two models can look close on benchmarks but perform very differently in real work because the experienced product includes:

- orchestration
- memory
- tool use
- review logic
- interface design
- fallback behavior
- stopping behavior

Users experience the stack, not only the base model.

### 2. Cost should be measured per accepted work unit

A more expensive model may still be cheaper if it:

- requires fewer retries
- reduces review time
- avoids downstream mistakes
- compresses several steps into one pass

A cheaper model may be more expensive in practice if it creates supervision drag.

### 3. Persistence increases useful-turn value

When a system remembers goals, constraints, prior outputs, and known boundaries, each turn starts further along.

That means the useful payload of one interaction can grow even when the underlying model changes only slightly.

### 4. Delegation density becomes a real moat

Delegation density means how much task surface can safely be handed to the system before human intervention.

The key word is safely.

A high-value system is not the one that acts most aggressively. It is the one that completes the most useful work before meaningful human review is needed, without creating hidden authority leak.

## Evaluation Questions

When comparing systems, ask:

1. How many human interventions are needed per completed task?
2. How much correction is required after the first pass?
3. How much context must be rebuilt each time?
4. How much hidden supervision is still required?
5. How often does the system choose the right next subtask?
6. How much approved work emerges from one engagement?
7. What is the cost of being wrong quietly rather than obviously?
8. Where does approval still happen, and is it meaningful?

## Example Contrast

Low useful-turn value:

- fluent output
- frequent reframing needed
- weak constraint retention
- weak handoff quality
- hidden cleanup burden

High useful-turn value:

- strong first-pass structure
- good constraint retention
- correct task routing
- lower correction burden
- clear review boundary
- output close to approval-ready

## Product Implication

If this lens is right, product advantage will often come less from raw intelligence gains and more from:

- orchestration quality
- memory design
- cost per accepted outcome
- review and approval structure
- continuity across turns
- visibility into what was actually delegated

In that world, the question shifts from "who has the best model?" to "who has the best governed work unit?"

## Boundary

Do not use this note to imply that benchmark performance no longer matters.

It matters, but often as one component inside a larger system whose practical value is determined by useful-turn completion and governed delegation.
