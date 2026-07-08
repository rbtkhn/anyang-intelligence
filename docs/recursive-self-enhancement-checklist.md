# Recursive Self-Enhancement Checklist

Use this checklist at the end of a meaningful work cycle to decide whether the cycle should improve Anyang Intelligence's operating surface.

This is a lightweight gate, not a mandate to create more process. If there is no durable lesson, stop.

## 1. Name The Work Cycle

- What work just happened?
- Which lane or surface did it affect: customer, skill, loop, template, CLI, governance doc, or portfolio doc?
- Was the work real enough to teach the system something, or was it only speculative?

## 2. Name The Friction Or Pattern

Look for one of these:

- repeated ambiguity
- missing authority boundary
- missing evidence standard
- unsafe or unclear handoff
- recurring template gap
- validation or lint warning
- customer-language confusion
- private-context transfer risk
- a useful move that future agents should not have to rediscover

If there is no friction or reusable pattern, do not force an improvement.

## 3. Decide Whether It Is Durable

A lesson is durable enough to preserve when it is:

- likely to recur
- grounded in actual work
- specific enough to help next time
- general enough not to overfit one conversation
- safe within the relevant membrane
- approved or clearly reviewable by the human operator

If the lesson depends on private customer facts, translate it into a primitive before preserving it.

## 4. Choose One Operating Surface

Pick the lightest surface that prevents recurrence:

- doctrine doc
- customer README or scope doc
- checklist
- template
- skill step
- loop definition
- validator or lint rule
- portfolio dashboard update
- README link for discoverability

Do not improve five surfaces when one will do.

## 5. Preserve The Improvement

Before calling the cycle enhanced, confirm:

- the improvement is repo-visible
- the next similar agent can find it
- it names the authority boundary
- it does not leak private context
- it does not turn a recommendation into human approval
- it does not add pricing, legal, tax, child-safety, or compliance claims without authority

## 6. Validate When Possible

Use the relevant check:

- loop change: `anyang-loop validate <path>`
- customer-folder change: `anyang-install validate customers`
- Python/tooling change: `python -m pytest`
- documentation change: read the diff and scan for boundary leaks

If validation is not available, state what was manually checked.

## 7. Completion Question

Ask:

```text
What changed in the operating surface so the next similar cycle starts smarter?
```

If the answer is only "we talked about it," recursive self-enhancement did not occur.

If the answer points to a specific doc, skill, template, checklist, loop, validator, guardrail, or linked artifact, the enhancement is real.

## Compact Closeout Format

Use this when summarizing a completed enhancement:

```text
Cycle:
<what work happened>

Friction:
<what would recur or create risk>

Improvement:
<what changed in the repo>

Evidence:
<diff, validation, link, commit, or artifact>

Next cycle starts smarter because:
<one sentence>
```
