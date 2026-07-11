# Parent Intake To Draft Runbook

This is the operator front door for the paid Learning Core 30-day plan workflow.

Use it when a real parent intake response arrives for the **30-Day Personalized Learning Plan** for new students, including onboarding.

The goal is to move from parent response to one of three safe states:

- `Ready`: draft the plan from parent-approved inputs.
- `Provisional`: draft a clearly labeled starter plan with visible assumptions.
- `Hold`: do not draft; request missing authority, safety, privacy, schedule, or learner-context inputs first.

## Governing Rule

Do not draft from vibes.

The plan may use:

- parent-approved intake answers
- parent-approved learner observations or student voice
- parent-approved privacy, save, share, and approval rules
- neutral template defaults that do not claim learner-specific truth
- clearly labeled provisional assumptions when the case is safe enough for `Provisional`

The plan may not use:

- guessed learner facts
- diagnosis-like language
- app activity as proof of mastery
- unapproved child-facing prompts
- unapproved save/share rules
- pricing, subscription, or internal retainer language
- embodied AI, robot, kiosk, or child-facing agent use unless separately cleared by the hold policy

## First 15-Minute Triage

When the parent response arrives:

1. Save or paste the parent response into the working notes for the case.
2. Mark whether the parent explicitly approves drafting from the current response.
3. Check authority:
   - Who approves the plan before use?
   - Who approves child-facing language?
   - Who approves what information may be saved or shared?
4. Check the minimum learner context:
   - age or grade band
   - first-month goal
   - current rhythm or starting point
   - at least some interests, strengths, friction, or support signals
5. Check schedule reality:
   - learning days
   - parent time
   - screen-time budget, if any
   - major household constraints
6. Check starter resources:
   - Khan Academy Kids approval, hold, or undecided status
   - reading basket status
   - portfolio evidence approach
7. Check support and safety:
   - high-stakes concerns
   - outside-support context
   - topics, tools, or activities to avoid
8. Assign one status only: `Ready`, `Provisional`, or `Hold`.

If the operator cannot assign one status after this pass, choose `Hold`.

## Status Rules

### Ready

Use `Ready` only when:

- parent authority is explicit
- drafting approval is explicit
- privacy and sharing boundaries are clear
- basic learner context is sufficient to avoid invention
- schedule and parent-time reality are clear enough to plan
- starter resources are approved, declined, or clearly marked undecided
- parent approval before plan use is explicit

Next action:

1. Fill [plan-draft-evidence-map.md](plan-draft-evidence-map.md).
2. Draft from [30-day-plan-template.md](30-day-plan-template.md).
3. Return the draft for parent approval.
4. Record approval state in [parent-approval-record.md](parent-approval-record.md).

### Provisional

Use `Provisional` when:

- parent authority and safety are clear
- drafting approval is clear
- some details are thin, but a safe starter plan can be useful
- every missing fact can remain visible as a missing input or provisional assumption

Next action:

1. List all missing inputs before drafting.
2. List all provisional assumptions before drafting.
3. Fill [plan-draft-evidence-map.md](plan-draft-evidence-map.md).
4. Draft from [30-day-plan-template.md](30-day-plan-template.md) with `Plan status: Provisional`.
5. Return the draft for parent review before use.
6. Record approval or required changes in [parent-approval-record.md](parent-approval-record.md).

### Hold

Use `Hold` when:

- parent approval authority is unclear
- drafting approval is missing
- privacy or sharing boundaries are unclear
- learner context is too thin to avoid invention
- schedule or parent-time reality is too unclear to plan
- high-stakes support, safety, legal, accountability, health, developmental, or emotional concerns need clarification
- the parent names an ambiguous boundary around a tool, activity, app, prompt, or support context
- embodied AI, robot, kiosk, or child-facing agent use is requested without explicit safety and override clearance

Next action:

1. Do not draft the plan.
2. Use [hold-response-template.md](hold-response-template.md).
3. Ask only for the missing decisions or facts needed to move safely.
4. Re-run this runbook when the parent replies.

## Required Evidence Bundle

Before any plan draft is sent for review, the operator should have:

- parent response or parent-approved notes
- readiness status: `Ready` or `Provisional`
- missing-input list, if any
- provisional-assumption list, if any
- evidence map linking draft sections to inputs
- draft plan
- parent approval record shell

The evidence bundle is what prevents the plan from becoming a polished guess.

## Handoff Checklist

Before leaving the intake stage, answer:

- What did the parent explicitly approve?
- What did the parent explicitly prohibit or pause?
- What is still unknown?
- What learner-specific claims are supported by parent input?
- What assumptions, if any, are labeled?
- What must the parent approve before use?
- Is the plan safe to draft, or should it remain `Hold`?

## Related Docs

- [parent-intake-message.md](parent-intake-message.md)
- [30-day-plan-inputs.md](30-day-plan-inputs.md)
- [onboarding-readiness-checklist.md](onboarding-readiness-checklist.md)
- [plan-drafting-gate.md](plan-drafting-gate.md)
- [plan-draft-evidence-map.md](plan-draft-evidence-map.md)
- [30-day-plan-template.md](30-day-plan-template.md)
- [parent-approval-record.md](parent-approval-record.md)
- [hold-response-template.md](hold-response-template.md)
- [embodied-ai-hold-policy.md](embodied-ai-hold-policy.md)
