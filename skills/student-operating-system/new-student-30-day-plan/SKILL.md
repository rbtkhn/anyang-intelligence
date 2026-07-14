---
name: new-student-30-day-plan
description: Student Operating System procedure for creating the scoped 30-Day Personalized Learning Plan for new students from a verified intake, confirmed-effective learner profile, and separate guardian drafting authorization. Use when drafting the Learning Core retainer deliverable, new-student onboarding plan, first-month learning plan, or 30-day parent-reviewed plan while preserving parent authority and child-safety boundaries.
---

# New Student 30-Day Plan Skill

Use this skill to create the scoped Learning Core retainer deliverable: a **30-Day Personalized Learning Plan** for new students, including onboarding.

This is a Student Operating System-level skill. It assembles approved inputs into the first-month plan. It does **not** define customer pricing, replace parent authority, create a full curriculum, diagnose, grade, prove mastery, or authorize unsupervised child-facing AI.

## Required Reads

Read these first:

1. `projects/learning-core/one-time-retainer-scope.md`
2. `projects/learning-core/executive-os-install.md`
3. `projects/learning-core/30-day-plan-inputs.md`
4. `projects/learning-core/30-day-plan-template.md`
5. `projects/learning-core/startup-bundle.md`
6. `projects/learning-core/reading-basket.md`
7. `projects/learning-core/student-portfolio.md`
8. `projects/learning-core/monthly-portfolio-review.md`

Also require the tenant-private, operator-supplied:

- parent-verified intake packet;
- latest confirmed-effective learner profile and version reference;
- current authority and preservation receipt;
- separate guardian authorization to draft the 30-day plan.

When available, also read:

- Parent goals and non-negotiable boundaries.
- Parent-approved learner voice, when available.
- Parent observations.
- Khan Academy Kids engagement notes.
- Reading basket status or book list.
- Student portfolio setup status.
- Existing curriculum/resources.
- Schedule constraints.
- Parent-approved outside-support notes.
- Applicable education accountability requirements the parent wants considered.

If key inputs are missing, produce a **plan hold** with missing inputs instead of inventing learner facts.

## Input Readiness

Classify readiness before drafting:

| Status | Use when | Action |
| --- | --- | --- |
| **Ready** | Verified intake, effective profile, current boundaries, and drafting authorization are available; required planning inputs are clear. | Draft the 30-day plan. |
| **Provisional** | Required authority is clear and the effective profile is available, but optional learner-fit evidence remains thin. | Draft with clear assumptions and missing inputs. |
| **Hold** | Intake, effective profile, drafting authority, safety boundary, schedule, or basic learner context is missing or stale. | Do not draft the plan; list required inputs. |

When in doubt, choose **Provisional** or **Hold**, not **Ready**.

## Required Output

Produce this exact structure:

```text
30-Day Personalized Learning Plan:
Plan status:
Learner:
Parent goal:
Inputs checked:
Missing inputs:

Authority and safety boundary:
- ...

New-student onboarding sequence:
Week 0 / Before start:
- ...
Week 1 setup:
- ...

Learner context summary:
- Interests:
- Strengths:
- Friction or support signals:
- Parent constraints:
- Evidence quality:

30-day rhythm:
- Daily anchor:
- Reading:
- Khan Academy Kids:
- Hands-on practice:
- Project / enrichment:
- Movement / play / outside time:
- Parent observation:
- Portfolio evidence:

Week 1 focus:
- Goal:
- Activities:
- Evidence to save:
- Parent review question:

Week 2 focus:
- Goal:
- Activities:
- Evidence to save:
- Parent review question:

Week 3 focus:
- Goal:
- Activities:
- Evidence to save:
- Parent review question:

Week 4 focus:
- Goal:
- Activities:
- Evidence to save:
- Parent review question:

Reading basket plan:
- ...

Khan Academy Kids use rule:
- ...

Portfolio evidence plan:
- ...

Weekly parent review prompts:
- ...

First monthly portfolio review shape:
- ...

Parent decisions needed:
- ...

Watch items / support signals:
- ...

Next-month decision options:
- ...
```

Do not include pricing or monetary-value language in the plan artifact.

## Procedure

### 1. Confirm Parent Authority

Name what the parent or guardian must approve before use:

- Daily rhythm.
- Resources and activities.
- Child-facing prompts.
- Portfolio evidence to save.
- Any support concern.
- Any outside-support escalation.
- Any accountability or legal requirement.

If parent approval rules are unclear, mark the plan **Hold**.

### 2. Build From Evidence

Use observed signals, not assumptions:

- Parent goals.
- Student voice.
- Reading basket signals.
- Khan Academy Kids parent observations.
- Portfolio artifacts.
- Proud work.
- Current resources.
- Existing schedule.

If evidence is thin, say so and make the plan provisional.

### 3. Keep The Month Humane

Prefer a simple, repeatable rhythm:

- Reading.
- Khan Academy Kids, parent-supervised.
- One focused practice area.
- One hands-on or creative activity.
- Movement, play, or outside time.
- Parent observation.
- Light portfolio evidence.

Avoid crowding all subjects into every day. The first month should reveal the learner, not exhaust the family.

### 4. Include Onboarding

The plan must include an onboarding sequence:

- Confirm parent goals and boundaries.
- Review the verified intake and latest confirmed-effective learner profile.
- Confirm Khan Academy Kids setup and use rule.
- Build or refresh the reading basket.
- Create or confirm the student portfolio.
- Establish the parent observation notebook.
- Agree on weekly review timing.

### 5. Close The Loop

Every week must define:

- What the parent should observe.
- What evidence to save.
- What question the weekly parent review should answer.
- What might change next week.

The month must end with a first monthly portfolio review shape and next-month decision options.

## Guardrails

Do not:

- Diagnose.
- Grade.
- Label the child.
- Present app progress as proof of mastery.
- Replace parent instruction.
- Imply legal homeschool compliance.
- Create a complete curriculum.
- Recommend unsupervised child-facing AI.
- Hide support concerns from the parent.
- Mention internal skill names in parent-facing output.
- Include customer pricing, subscription, or retainer language in the plan artifact.

If persistent reading, writing, attention, speech/language, math, behavior, health, or developmental concerns appear, the safe action is parent review and possible teacher, tutor, clinician, specialist, or other qualified human support.

## Related Skills

Use these when needed:

- `skills/student-operating-system/learner-intake/SKILL.md` in `create` mode when no effective learner profile exists, or `change` mode when the profile may be stale. Do not draft from a proposed or approved-but-unpreserved profile.
- `skills/student-operating-system/learner-profile/SKILL.md` only as the internal evidence-analysis subroutine behind learner intake.
- `skills/student-operating-system/parent-interface/SKILL.md` when parent approval, parent-facing language, or parent decision records are the main task.
- `skills/student-operating-system/learning-plan/SKILL.md` for shorter daily, weekly, reading, project, or next-cycle plans.
- `skills/student-operating-system/weekly-parent-review/SKILL.md` after a week of evidence exists.
- `skills/student-operating-system/student-experience/SKILL.md` for child-safe surveys, reflections, learner-interest artifacts, or proud-work choices.

## Done When

The operator has a parent-reviewed 30-day plan draft or a clear plan hold that:

- Names input readiness.
- Includes onboarding.
- Provides a humane 30-day rhythm and four weekly focus outlines.
- Connects reading basket, Khan Academy Kids, portfolio evidence, weekly review, and monthly review.
- Names parent decisions, watch items, and next-month options.
- Preserves parent authority, child safety, privacy, and evidence boundaries.
