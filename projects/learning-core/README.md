# Learning Core

Learning Core is an Anyang Intelligence build for the **Student Operating System**, a parent-guided learning operating system built on the Anyang Intelligence Executive OS method.

## Organization

The Student Operating System is a high-trust elementary learning operating context that can layer onto either public school or homeschool:

- Work: personalized elementary learning, parent-guided support, daily learning plans, enrichment, progress tracking, portfolio evidence, and family communication.
- Cadence: daily learning rhythm, weekly parent review, monthly portfolio review, seasonal learning goals, and school-year planning.
- Operating challenge: create a rich individualized learning experience without replacing parent authority, child safety, human care, or required education accountability.
- Paid retainer received: $1,000.
- Payer: Learning Core.
- Payee: Anyang Intelligence.
- Retainer type: one-time services.
- Service scope: 30-Day Personalized Learning Plan for new students, including onboarding, defined in [one-time-retainer-scope.md](one-time-retainer-scope.md).
- Starter iPad app: Khan Academy Kids, free, parent-supervised, age-appropriate for a 7-year-old, and part of the initial resource bundle.

## Executive OS Role

Anyang Intelligence acts as the Student Operating System layer for the parent and learner.

In practical terms, the Executive OS helps:

- Maintain the learner profile, interests, strengths, challenges, goals, and learning history.
- Prepare daily and weekly learning plans for parent review.
- Suggest lessons, projects, books, field trips, practice activities, and enrichment.
- Track progress, questions, portfolio artifacts, and follow-ups.
- Adapt future plans from observed engagement and learning evidence.
- Preserve parent decisions, curriculum choices, and learning reflections.

The system does not replace parents, teachers, tutors, clinicians, legal requirements, or child-facing human judgment. It supports a parent-guided personalized learning experience.

## Operating Thesis

A traditional education experience, whether public school or homeschool, should not become a pile of worksheets, apps, handoffs, and forgotten good intentions.

The Student Operating System should help the family create a coherent, humane, personalized layer of depth and continuity around the learner's actual education experience:

```text
learner interests and needs
  -> parent-reviewed learning plan
  -> lessons and experiences
  -> evidence and reflection
  -> progress review
  -> next learning decision
```

## Starter Resource Bundle

Khan Academy Kids should be included in the startup bundle as the first default iPad learning app.

Role in the system:

- Provide a free, low-friction, child-friendly daily practice and exploration app.
- Support early reading, writing, language, math, books, videos, creative activities, and social-emotional learning.
- Give the parent a safe starter tool that supports the scoped 30-Day Personalized Learning Plan.
- Generate parent-observed engagement signals for the first learner profile and daily rhythm.
- Reflect Learning Core's due diligence in sifting through crowded digital-learning options so the parent does not have to start from an app marketplace with no clear filter.

Boundary:

- Khan Academy Kids is a starter resource, not the full curriculum.
- App use remains parent-supervised.
- Any learning conclusions should come from parent review, observed engagement, and portfolio evidence, not app activity alone.

See [startup-bundle.md](startup-bundle.md) for the parent-facing Startup Bundle.

See [30-day-plan-inputs.md](30-day-plan-inputs.md) for the parent goals, learner context, onboarding, safety, and approval inputs needed before drafting the 30-Day Personalized Learning Plan.

See [parent-intake-message.md](parent-intake-message.md) for the adaptable parent message used to collect those inputs before drafting.

See [parent-onboarding-survey.md](parent-onboarding-survey.md) for the lighter 10-question multiple-choice registration and onboarding survey used when the parent needs a faster front door.

See [parent-guide-signals.md](parent-guide-signals.md) for the parent-set budgets and household-fit signals the Student Operating System can use to adapt plans to real family constraints.

See [parent-intake-to-draft-runbook.md](parent-intake-to-draft-runbook.md) for the operator front door used when a real parent response arrives and the case needs to be classified as `Ready`, `Provisional`, or `Hold`.

See [onboarding-readiness-checklist.md](onboarding-readiness-checklist.md) for the internal/operator checklist that converts parent intake into a `Ready`, `Provisional`, or `Hold` decision before drafting.

See [mock-intake-simulations.md](mock-intake-simulations.md) for three fictional intake tests that exercise the Ready, Provisional, and Hold gates.

See [hold-response-template.md](hold-response-template.md) for the parent-facing pause message used when intake is classified as `Hold`.

See [recursive-self-enhancement.md](recursive-self-enhancement.md) for the lane-specific note showing how Learning Core intake friction was converted into reusable onboarding infrastructure.

See [naming-architecture.md](naming-architecture.md) for the lane rule that keeps `Learning Core`, `Learning Core`, and `Student Operating System` distinct.

See [plan-drafting-gate.md](plan-drafting-gate.md) for the internal/operator checklist that controls how `Ready` and `Provisional` intake is safely converted into a 30-day plan draft.

See [plan-draft-evidence-map.md](plan-draft-evidence-map.md) for the internal/operator worksheet that traces each major draft section back to parent inputs, approved context, template defaults, or labeled assumptions.

See [embodied-ai-hold-policy.md](embodied-ai-hold-policy.md) for the child-safety and parent-authority review gate that keeps any child-facing robot, kiosk, or embodied tutoring device in `Hold` until a narrow supervised use case is explicitly approved.

See [embodied-ai-parent-review-worksheet.md](embodied-ai-parent-review-worksheet.md) for the parent-review surface that captures why a child-facing embodied device is being considered, what it records, who remains in charge, and why the default answer is still `Hold` until a narrow supervised case is explicit.

See [mock-ready-plan-evidence-map.md](mock-ready-plan-evidence-map.md) for a fictional `Ready` intake traceability test before any real parent-facing plan is drafted.

See [ai-interface-training/](ai-interface-training/) for Learning Core-specific AI interface training exemplars, including the canonical fictional `Ready` plan exemplar for intake review, drafting-gate use, evidence mapping, safe draft structure, and parent approval handoff.

The same training folder now also includes an `approved with changes` exemplar for showing how parent edits should update both the approval record and the plan before use.

It also now includes a `hold after review` exemplar for showing how parent review can pause plan use when boundaries, permissions, or higher-stakes concerns need clarification.

See [parent-approval-record.md](parent-approval-record.md) for the internal/operator artifact that records what the parent approved, what changed, what remains provisional, and whether a draft is safe to use.

See [parent-approval-checklist.md](parent-approval-checklist.md) for the parent-facing review surface that makes it easy to approve, change, or pause draft elements before use.

See [30-day-plan-template.md](30-day-plan-template.md) for the parent-facing plan shell used after inputs are approved.

See [loop-examples/parent-intake-readiness.yaml](loop-examples/parent-intake-readiness.yaml) for the formal loop definition behind parent intake, readiness classification, and recursive template improvement.

See [reading-basket.md](reading-basket.md) for the first physical literacy tool in the startup bundle.

See [student-portfolio.md](student-portfolio.md) for the place to store physical work, digital work, student output the learner is proud of, milestones, and reports.

See [monthly-portfolio-review.md](monthly-portfolio-review.md) for the first reporting layer built from the student portfolio.

See [catalog-doctrine.md](catalog-doctrine.md) for the dual-track doctrine that separates the public main Khan Academy catalogue from the governed Khan Kids curated catalogue.

The catalog layer is a resource-awareness scaffold inside the Student Operating System, not the recommendation engine, curriculum authority, or proof-of-mastery layer.

See [catalog/catalog-schema.md](catalog/catalog-schema.md) for the shared schema used by imported main-Khan entries and curated Khan Kids entries.

See [catalog/khan-kids-curated-catalog.yaml](catalog/khan-kids-curated-catalog.yaml) for the first governed Khan Kids catalog artifact.

See [catalog/khan-kids-in-app-capture-spec.md](catalog/khan-kids-in-app-capture-spec.md) for the future manual in-app capture path that can deepen the Khan Kids directory without overstating public coverage.

See [khan-adapter-layer.md](khan-adapter-layer.md) for the operating doctrine that says Khan should keep doing Khan-style in-product recommendation, while Learning Core governs how Khan fits into the broader Student Operating System.

See [khan-transition-point.md](khan-transition-point.md) for the handoff rule between Khan Academy Kids and the main Khan Academy environment, with specific capability signals and a narrow role for course completion.

See [khan-transition-readiness-target.md](khan-transition-readiness-target.md) for the deeper doctrine that turns that handoff threshold into a deliberate capability target Learning Core can build toward over time.

See [khan-academy-signal-pipeline.md](khan-academy-signal-pipeline.md) for the governed signal path that turns Khan Academy Kids observations into learner-profile updates, portfolio evidence, and better next-step recommendations.

See [subscription-boundary.md](subscription-boundary.md) for the commercial boundary between the free 30-day entry plan and the monthly continuity subscription.

See [subscription-experience.md](subscription-experience.md) for the recurring cadence, support boundaries, and monthly deliverables of the continuity subscription.

See [parent-journey-pressure-test.md](parent-journey-pressure-test.md) for the end-to-end pressure test of intake, free month, observation loop, subscription invitation, and first continuity month.

See [continuity-invitation-template.md](continuity-invitation-template.md) for the parent-facing message template that turns month-one evidence into a non-salesy continuity invitation.

See [learning-core-ob1-integration.md](learning-core-ob1-integration.md) for the architecture note that explains how the family's `Learning Core` could interface with `OB1 / Open Brain` as a governed memory substrate.

For repo-local Codex work, see [learning-core-lane skill](../../skills/student-operating-system/learning-core-lane/SKILL.md) for the lane-specific front door that ties together naming, onboarding, readiness, drafting, continuity, and Khan/reading-basket interpretation rules.

## Customer Offer

The current project-facing entry offer is a **free 30-day collaborative build** of the family's `Learning Core` for new students whose family wants more depth, continuity, and parent clarity around a public-school, homeschool, or hybrid education experience.

Part of that value proposition is curation. Learning Core does due diligence on starter tools, learning supports, and recommendation logic so the parent does not have to personally sift through countless competing apps, programs, and product claims alone.

The goal of that first 30 days is to collaborate with the customer until the family's `Learning Core` becomes usable enough that they can operate it independently if they choose.

After the first 30-day build, the continuity offer is a **monthly subscription** for families who want ongoing support through:

- Chat-group participation.
- Premium newsletters.
- Personalized ongoing consultation.
- Early access to new upgrades and features.

Learning Core now provides **$1,000 per month in confirmed recurring revenue** to Anyang Intelligence through this continuity service. The service remains subject to parent authority, child-safety boundaries, and the agreed scope.

## Paid Retainer

Learning Core has paid Anyang Intelligence a **$1,000 one-time retainer** for a scoped 30-day collaborative build of the family's `Learning Core`, including onboarding.

This should be treated as a paid discovery and service-design obligation. The one-time service package is defined in [one-time-retainer-scope.md](one-time-retainer-scope.md) before delivery begins.

The retainer is a separate historical cash event from the confirmed monthly continuity revenue and should remain scoped intentionally.

## Installation

See [executive-os-install.md](executive-os-install.md) for the first Student Operating System install design.
