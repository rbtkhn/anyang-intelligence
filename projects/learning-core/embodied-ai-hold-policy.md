# Learning Core Embodied AI Hold Policy

This policy is a review gate for any child-facing robot, kiosk, tutoring device, or embodied AI interface considered inside the Learning Core lane.

Its purpose is to prevent premature adoption, preserve parent and adult authority, and stop novelty pressure from turning into child-facing operating change before the safety case is clear.

Use with:

- [README.md](README.md)
- [executive-os-install.md](executive-os-install.md)
- [onboarding-readiness-checklist.md](onboarding-readiness-checklist.md)
- [plan-drafting-gate.md](plan-drafting-gate.md)
- [../singularity-science/primitives/embodied-ai-exposure-scan.md](../singularity-science/primitives/embodied-ai-exposure-scan.md)

## Operating Rule

Default state: `Hold`.

No child-facing embodied AI should be treated as approved, normal, or implied by default in Learning Core.

The operator may review an embodied AI proposal, but use must remain paused until parent authority, supervision, safety posture, and human override are explicit.

## What Counts As Embodied AI Here

This policy covers:

- child-facing robots
- classroom or homeschool kiosks
- smart tutors with physical presence
- voice-first devices positioned as guides, companions, or teachers
- mobile sensing or monitoring devices that interact directly with a child
- physical systems that appear to instruct, watch, coach, redirect, or evaluate the learner

This policy does not automatically approve software-only learning tools. Those still require the ordinary Learning Core authority and safety gates.

## Why The Default Is Hold

Embodied AI raises sharper risks than ordinary software because the interface can:

- blur parent or adult authority
- create false confidence in supervision
- increase attachment or compliance pressure
- normalize surveillance or evaluation
- make children believe the system understands more than it does
- make adults underweight maintenance, failure, or override needs

In this lane, the cost of a bad default is too high. The burden is on the proposal to justify movement out of `Hold`.

## Immediate Hold Triggers

Stay at `Hold` if any of these are true:

- The device speaks or acts as if it is a teacher, parent, guide, or authority figure.
- The child could reasonably confuse the system's role or capability.
- Parent approval is missing, partial, or not specific to the embodied use.
- Adult supervision expectations are vague or unrealistic.
- There is no immediate adult override or shutdown path.
- The system collects, records, or transmits child information without explicit parent clarity.
- The proposal implies diagnosis, grading, mastery proof, behavior judgment, or developmental interpretation.
- Safety, privacy, maintenance, charging, connectivity, or failure behavior is not clearly understood.
- The main argument for use is hype, novelty, peer pressure, or "the future is here."

## Required Review Questions

Do not move out of `Hold` until these questions are answered in plain language:

1. What exact problem is this meant to solve for the household or learner?
2. Why is embodiment necessary here instead of a software-only or human-led alternative?
3. What adult remains visibly and practically in charge during use?
4. What would the child think this device is allowed to do?
5. How is the device stopped, redirected, or removed if it behaves badly or creates discomfort?
6. What information does it sense, store, infer, or share?
7. What failure mode matters most: safety, trust, privacy, overstimulation, dependence, or false instructional authority?
8. What maintenance or supervision burden falls on the parent?
9. What evidence, if any, suggests the device helps without weakening authority or safety?
10. What would make the answer "not now" even if the device seems impressive?

## Approval Conditions For Limited Testing

Movement from `Hold` to a narrow supervised test requires all of the following:

- explicit parent approval for this exact device/use case
- explicit statement that the device does not replace the parent, teacher, tutor, clinician, or legal authority
- clear adult supervision during every meaningful interaction
- immediate human override and shutdown path
- no diagnosis, grading, mastery proof, or hidden evaluation role
- clear privacy and recording rules
- reversible use with no dependence on the device for household continuity
- a short test window with a review date

If any one of these conditions is missing, remain at `Hold`.

## Safe Test Shape

If a parent explicitly wants a small test, the default safe shape is:

- short duration
- parent-supervised
- no unsupervised child-facing authority
- no high-stakes learning claims
- no sensitive data sharing
- no assumption that enthusiasm equals suitability

The goal of a test is not to prove adoption. The goal is to learn whether the device adds value without weakening trust, safety, or adult authority.

## Not Allowed

Do not use an embodied AI system in this lane to:

- replace parent review
- act as teacher of record
- evaluate the child as if it were a clinician or diagnostician
- create hidden monitoring or behavior scoring
- pressure the child into compliance through anthropomorphic authority
- imply educational accountability or mastery proof
- bypass parent knowledge of what the child is being told or shown

## Output Shape

When this gate is applied, record the result in this shape:

```text
Device or system:
Use case:
Why embodiment is being considered:
Parent approval status:
Adult accountable:
Main hold trigger or concern:
Override path:
Privacy / sensing rule:
Decision:
What would need to be true to move out of Hold:
```

## Boundary

This policy is a child-safety and authority guardrail, not a recommendation to buy or adopt embodied AI.

Route only the review discipline. Do not route Singularity Science source rhetoric, robotics pricing claims, or deployment timelines into Learning Core as operating pressure.
