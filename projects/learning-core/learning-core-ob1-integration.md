# Learning Core OB1 Integration

This document defines how the family's `Learning Core` could interface with [`OB1 / Open Brain`](https://github.com/JK3303/OB1).

OB1 integration is optional. `Learning Core` does not require OB1 to function, and no automatic integration is assumed.

The goal is not to replace Learning Core with OB1.

The goal is to let OB1 serve as the **memory substrate** while Learning Core remains the **governed education layer**.

## Core Position

Treat the two layers like this:

```text
OB1 / Open Brain
  -> memory store
  -> vector search
  -> retrieval layer
  -> shared AI-tool access

Learning Core
  -> education-specific schema
  -> parent authority rules
  -> child-safety boundaries
  -> review workflows
  -> recommendation and interpretation logic
```

OB1 should store and retrieve.

Learning Core should decide what records mean, what may be stored, what may be surfaced, and what may become a recommendation.

## Why The Fit Is Plausible

OB1 appears to be:

- one database
- one AI gateway
- one retrieval layer
- one chat-access surface
- one shared memory layer across multiple AI tools

That matches a real need in Learning Core:

- observations should not live in one chat only
- portfolio signals should be retrievable across tools
- weekly and monthly review should build on the same memory
- multiple AI surfaces may need governed access to the same learner context

So the interface is plausible if Learning Core stays the policy and workflow layer on top.

## The Most Important Distinction

OB1 wants broad persistent memory.

Learning Core needs **selective, parent-governed, child-safe memory**.

That means the hardest part is not database plumbing.

The hardest part is governance.

## Minimum Learning Core Objects

An OB1-backed Learning Core should define at least these objects:

- `family_profile`
- `learner_profile`
- `parent_preferences`
- `household_constraints`
- `resource_inventory`
- `reading_basket`
- `khan_usage_rule`
- `observation`
- `portfolio_artifact`
- `weekly_review`
- `monthly_review`
- `recommendation`
- `transition_readiness_check`
- `approval_record`

These are the minimum memory surfaces that let the system stay coherent across sessions and tools.

## Example Object Fields

### `learner_profile`

- learner_id
- preferred_name
- age_band
- schooling_context
- interests
- strengths
- friction_patterns
- support_level
- reading_posture
- current_stage

### `household_constraints`

- screen_time_budget
- supervision_budget
- prep_budget
- cleanup_tolerance
- rhythm_notes
- save_share_rules

### `observation`

- learner_id
- date
- source
- category
- note
- tags
- confidence
- parent_reviewed
- safe_to_reuse

### `portfolio_artifact`

- learner_id
- artifact_type
- title
- date
- summary
- pride_signal
- saved_by_parent
- share_status

### `transition_readiness_check`

- learner_id
- reading_capacity
- attention_capacity
- navigation_capacity
- correction_tolerance
- follow_through
- parent_fit
- threshold_status
- notes

## Workflow Mapping

### 1. Intake

Learning Core should:

- store parent intake or onboarding survey responses
- create learner and family records
- preserve approval boundaries and save/share rules

### 2. Phase 2 Gap Closing

Learning Core should:

- fill missing authority, learner, rhythm, or resource fields
- update readiness state
- avoid repeating already-known context

### 3. Weekly Review

Learning Core should:

- retrieve observations
- group patterns
- connect signals to likely next moves
- create a parent-readable weekly summary

### 4. Monthly Review

Learning Core should:

- retrieve observations, artifacts, and recommendations
- summarize what repeated
- clarify what changed
- name what next month should do differently

### 5. Khan Transition Review

Learning Core should:

- retrieve capability signals
- evaluate transition-readiness fields
- output `not yet`, `trial`, or `ready for limited extension`

### 6. Continuity Invitation

Learning Core should:

- retrieve month-one evidence
- identify whether real continuity demand exists
- generate an invitation only from actual patterns, not generic sales copy

## Governance Requirements

Every Learning Core record that touches child/family context should support policy fields such as:

- `visibility`
- `approval_scope`
- `sensitivity_level`
- `parent_reviewed`
- `shareable_transform`

Recommended posture:

- no child-linked record should be treated as broadly reusable by default
- every save/share boundary should come from parent authority
- every recommendation should stay subordinate to parent review

## What Must Never Be Inferred From OB1 Alone

Even with a strong memory substrate, Learning Core may not infer:

- diagnosis
- proof of mastery
- grade placement
- hidden child-facing authority
- permission to share sensitive records

OB1 retrieval is memory access, not educational authority.

## What “Seamless” Should Mean

In this context, seamless should mean:

- parent notes enter memory once
- observations stay retrievable across tools
- weekly and monthly review can reuse stored context
- Khan, reading-basket, and portfolio signals live in one governed memory graph
- multiple AI tools can work on the same approved learner context without re-eliciting everything

Seamless should not mean:

- automatic storage of everything
- unrestricted agent access
- disappearance of parent approval boundaries

## MVP Integration Path

### Phase 1

Start with:

- `learner_profile`
- `household_constraints`
- `observation`
- `portfolio_artifact`
- `weekly_review`

This is enough to make the Learning Core feel real in memory.

### Phase 2

Add:

- `reading_basket`
- `khan_usage_rule`
- `monthly_review`
- `recommendation`

This is enough to support continuity and adaptation.

### Phase 3

Add:

- `transition_readiness_check`
- `approval_record`
- continuity invitation logic

This is enough to support the more advanced Learning Core workflows.

## Best First Build

If Learning Core ever integrates with OB1, the strongest first build is:

1. learner profile
2. observations
3. weekly review
4. portfolio artifacts

That sequence gives the highest value with the least governance complexity.

## Boundary

Use OB1 as substrate, not authority.

Learning Core should remain the layer that protects:

- parent review
- child privacy
- save/share boundaries
- interpretation discipline
- no-diagnosis and no-mastery overreach

The interface is promising only if that governed layer stays explicit.
