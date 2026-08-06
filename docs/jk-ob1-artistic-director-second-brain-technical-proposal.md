# Technical Proposal: Extending OB1 with a Reusable Second-Brain Substrate

**Audience:** JK and the Claude Code agent operating in the personal second-brain repository  
**Repository context:** The repository currently named `OB1`  
**Scope:** Analyze first; implement only after explicit human approval  
**Relationship:** `artistic-director/` remains a project within the broader personal second-brain system

## Pasteable agent instruction

Paste this proposal into Claude Code from the root of the repository. The agent
must perform an analysis and proposed implementation plan first. It must not
edit files, install dependencies, use secrets, commit, push, deploy, or contact
external services until the human explicitly approves a bounded implementation
plan.

---

You are analyzing a proposal to make this repository a more reliable personal
AI second-brain system. The existing `artistic-director/` folder is the first
substantive project using the proposed patterns. Your job is to inspect the
repository, compare the proposal with what already exists, identify conflicts
or duplication, and produce an implementation plan for human approval.

Do not implement anything yet.

## 1. Design objective

Improve the repository's ability to:

1. recover intent from compressed or ambiguous human instructions;
2. keep project, personal, private, and public information separated;
3. distinguish ideas, drafts, recommendations, approvals, publications, and
   completed actions;
4. turn human-approved corrections into durable lessons without automatic
   overgeneralization; and
5. improve the human-AI working relationship through repeatable calibration.

The system should remain lightweight, local-first, human-controlled, and useful
for a personal second brain. Do not recreate a large organizational governance
system.

## 2. Current project to inspect

Inspect these existing surfaces before proposing changes:

```text
CLAUDE.md
.claude/
docs/
schemas/
resources/
skills/
artistic-director/
```

Within `artistic-director/`, inspect at minimum:

```text
README.md
charter/role.md
charter/boundaries.md
charter/working-agreement.md
ai/system-instructions.md
ai/collaboration-loop.md
ai/critique-rubric.md
ai/prompt-patterns.md
ai/calibration-set.md
memory/accepted-lessons.md
memory/rejected-lessons.md
memory/open-questions.md
memory/role-principles.md
decisions/creative-decisions.md
decisions/holds-and-rejections.md
decisions/review-receipts.md
practice/
evaluations/
references/rights-and-attribution.md
```

Also inspect the Grace Gems project area, if present:

```text
artistic-director/practice/grace-gems-phase2/
```

Report existing conventions, duplicated concepts, machine-readable formats,
and any instructions that would conflict with this proposal.

## 3. Proposed architecture

Use existing repository conventions where possible. Do not create parallel
systems merely because this proposal names a possible path.

### 3.1 Global agent behavior

Candidate location: `CLAUDE.md` and/or `.claude/`.

The global agent guidance should point to five reusable capabilities:

- intent recovery;
- project membranes;
- decision and state receipts;
- lesson promotion; and
- calibration loops.

The global guidance should state that:

- recovered intent is an inference, not a fact;
- a draft or recommendation is not approval;
- project-local information does not become global memory automatically;
- lessons require explicit human acceptance;
- external action requires explicit permission; and
- the agent must preserve uncertainty instead of filling missing facts.

Do not put large workflow details into `CLAUDE.md` if a linked procedure or
skill is clearer.

### 3.2 Intent recovery

Candidate locations:

```text
.claude/intent-recovery.md
skills/intent-recovery/
artistic-director/ai/collaboration-loop.md
artistic-director/ai/prompt-patterns.md
```

Prefer one canonical procedure with project-specific adaptations rather than
separate incompatible versions.

Minimum receipt:

```text
What was said:
What I think it means:
Clearer articulation:
Practical implication:
Uncertainty:
Next question or action:
```

Required behavior:

1. preserve the literal human wording;
2. state the inferred meaning separately;
3. distinguish creative intent from factual or business claims;
4. preserve a material alternative interpretation;
5. ask for correction when ambiguity changes the next action; and
6. never treat recovery as authorization.

The Artistic Director may add creative distinctions such as warmth versus
sterility or intimacy versus scale, but those adaptations must not replace the
canonical procedure.

### 3.3 Project membranes

Candidate locations:

```text
docs/second-brain/project-membranes.md
projects/_template/manifest.md
artistic-director/charter/boundaries.md
references/rights-and-attribution.md
```

If a top-level `projects/` system does not exist, propose whether to create it
or use an existing OB1 convention. Do not assume a new top-level directory is
correct without inspecting the repository.

Every project manifest should be able to state:

```text
Project:
Owner:
Purpose:
Privacy level:
Allowed sources:
Prohibited sources:
What may become reusable memory:
What must remain project-local:
External-action rule:
Review owner:
```

The Artistic Director project should remain a distinct membrane. Grace Gems
facts, customer information, rights questions, campaign decisions, and client
materials must not become general OB1 memory merely because the AI encountered
them.

### 3.4 Decision and state receipts

Candidate locations:

```text
docs/second-brain/decision-states.md
schemas/decision-receipt.schema.json
resources/templates/decision-receipt.md
artistic-director/decisions/
```

Use a consistent state vocabulary, adapting existing terms rather than
creating a second incompatible vocabulary:

```text
idea
explore
draft
shortlist
recommendation
awaiting approval
approved
executing
published
complete
held
rejected
superseded
```

Minimum receipt:

```text
Decision ID:
Project:
Status:
Source:
Decision owner:
Evidence:
Alternatives considered:
Uncertainty:
Authority or approval:
Reversible: yes / no
Next action:
```

The agent must not infer approval from a polished artifact, previous practice,
silence, urgency, or a recommendation.

Map this standard onto the existing Artistic Director files:

- `decisions/creative-decisions.md` for creative choices;
- `decisions/holds-and-rejections.md` for blocked or declined directions;
- `decisions/review-receipts.md` for review and state evidence; and
- project-local receipts such as `practice/grace-gems-phase2/04-review-receipt.md`.

Do not erase useful historical records merely to make them fit the new format.
Propose a migration or compatibility approach.

### 3.5 Lesson promotion

Candidate locations:

```text
docs/second-brain/lesson-promotion.md
resources/templates/lesson.md
artistic-director/memory/
```

Maintain the distinction between:

- accepted lessons: human-approved reusable rules;
- rejected lessons: approaches explicitly not to repeat;
- held lessons: plausible but unresolved patterns;
- project-specific observations: useful only within one project; and
- open questions: areas where the AI must not pretend confidence.

Minimum lesson format:

```text
Lesson:
Evidence:
Applies when:
Does not apply when:
Accepted by:
Date:
Scope: project-specific / reusable
```

No automatic promotion is allowed. The agent may propose a lesson, but only the
human may accept it into reusable memory.

The existing Artistic Director files are the reference implementation:

```text
memory/accepted-lessons.md
memory/rejected-lessons.md
memory/open-questions.md
memory/role-principles.md
```

### 3.6 Calibration loop

Candidate locations:

```text
docs/second-brain/calibration-loop.md
resources/templates/calibration-exercise.md
artistic-director/ai/calibration-set.md
artistic-director/ai/collaboration-loop.md
artistic-director/evaluations/
```

Canonical loop:

```text
Brief
  -> AI questions and restatement
  -> distinct options
  -> human critique
  -> AI revision
  -> human accepts, rejects, or holds lesson
  -> remaining misunderstanding recorded
```

Each exercise should preserve the human's original critique, not only the AI's
summary of it.

The Rootmind exercise should remain historical evidence, not be rewritten as a
generic rule without preserving its original project context.

## 4. Proposed machine-readable schemas

Determine whether JSON Schema is already used consistently. If so, propose
schemas compatible with the existing conventions. If not, recommend whether
Markdown templates alone are sufficient for the first implementation.

Candidate schemas:

```text
schemas/intent-receipt.schema.json
schemas/project-manifest.schema.json
schemas/decision-receipt.schema.json
schemas/lesson.schema.json
schemas/calibration-exercise.schema.json
```

Do not create schemas merely for appearance. Each schema must have a concrete
consumer, validation path, or future migration benefit.

## 5. Proposed implementation stages

The agent should propose a staged plan rather than implementing everything at
once.

### Stage 0 — Analysis only

- inspect current files and conventions;
- identify overlap and conflicts;
- identify which paths already provide the needed capability;
- propose the smallest change set;
- identify files that must not change; and
- produce an approval request.

### Stage 1 — Canonical guidance

Implement only the smallest human-readable procedures for intent recovery,
membranes, state receipts, lesson promotion, and calibration.

### Stage 2 — Templates and compatibility

Add templates and, only if justified, schemas. Preserve existing Artistic
Director history and avoid unnecessary migration.

### Stage 3 — Artistic Director pilot

Apply the patterns to one new harmless exercise or one existing project-local
receipt. Do not rewrite all historical work automatically.

### Stage 4 — Evaluation

Evaluate whether the additions reduce confusion, improve source attribution,
protect project boundaries, and make human-AI collaboration easier. Only then
consider broader OB1 adoption.

## 6. Non-goals

This proposal does not authorize:

- a new cloud service or database;
- automatic memory promotion;
- automatic publishing or external communication;
- website construction or deployment;
- changes to repository ownership;
- importing Anyang Intelligence governance as a personal-system requirement;
- exact synchronization with another repository;
- deletion of existing Artistic Director history; or
- a large framework before a small pilot proves useful.

## 7. Required analysis output

Before implementation, return a report containing:

```text
Repository conventions found:
Existing capabilities that already solve part of the problem:
Duplications or conflicts:
Recommended canonical locations:
Files proposed for creation:
Files proposed for modification:
Files explicitly protected from change:
Migration and compatibility plan:
Schema recommendation:
Pilot exercise:
Validation method:
Risks:
Open questions:
Estimated effort:
Implementation sequence:
Approval requested:
```

The report must clearly separate facts discovered in the repository from the
agent's recommendations.

## 8. Acceptance criteria for later implementation

An implementation plan is ready for approval when:

- every proposed file has a reason and owner;
- the agent has identified existing files that should be reused;
- no new system duplicates an existing capability without justification;
- project-local and reusable memory are distinct;
- intent recovery cannot create authority;
- decision receipts distinguish recommendation from approval;
- lesson promotion requires human acceptance;
- historical Artistic Director work remains intact;
- the pilot is reversible; and
- the plan can be implemented without secrets, external services, or broad
  repository restructuring.

## 9. Approval gate

Stop after the analysis report. Ask the human this exact question:

> I have completed the repository analysis and implementation proposal. Do you
> approve Stage 1 only, approve a different bounded stage, request revisions,
> or reject the proposal?

Do not edit files until the human responds with an explicit implementation
approval.

---

## End of pasteable agent instruction

### Human note

This proposal is deliberately analysis-first. JK remains the owner of the
second-brain system and decides which general features, if any, should be
adopted. The Artistic Director project is the first test case, not the source of
automatic global rules.
