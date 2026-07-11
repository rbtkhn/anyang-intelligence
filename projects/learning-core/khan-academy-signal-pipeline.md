# Khan Academy Signal Pipeline

This document explains how **Khan Academy Kids** signals should flow into the **Student Operating System**.

The goal is not to treat app activity as proof of mastery.

The goal is to turn parent-reviewed app observations into better next-step recommendations.

This signal document is about **student behavior during actual use**.

It should be kept distinct from catalogue doctrine and content-directory knowledge. See [catalog-doctrine.md](catalog-doctrine.md) and [catalog/catalog-schema.md](catalog/catalog-schema.md) for the catalogue layer.

## Core Principle

Khan Academy Kids should enter the system as a **behavioral signal surface**, not as an academic verdict surface.

Do not pipeline:

- score -> mastery claim
- completion -> grade judgment
- app progress -> diagnosis

Do pipeline:

- choice -> interest signal
- repetition -> confidence or preference signal
- avoidance -> friction signal
- frustration -> support signal
- transfer -> next-step recommendation

## Pipeline Overview

The pipeline should look like this:

```text
Khan Academy Kids use
  -> parent observes signals
  -> signals are translated into short structured notes
  -> notes enter learner profile, weekly review, and portfolio when useful
  -> Student Operating System updates next recommendations
```

The parent remains the authority layer at every step.

## Catalog Knowledge Versus Use Signals

Elementary School should keep these two lanes separate:

```text
catalogue knowledge
  -> what kinds of content exist
  -> what recommendation options are available

actual student use
  -> what the learner chose
  -> what created ease or friction
  -> what should change next
```

The catalogue can improve recommendations before the student uses a tool.

Only actual parent-observed use should update learner-fit judgments.

## Signal Types

Elementary School should pay attention to these specific signal types:

### 1. Choice Signal

What the child chooses first inside the app.

Why it matters:

- shows attraction
- shows initiative
- helps identify where engagement starts most easily

### 2. Repeat Signal

What the child returns to voluntarily.

Why it matters:

- often reveals confidence
- may show preference or curiosity
- is stronger than one-time novelty

### 3. Avoidance Signal

What the child skips, quits, or resists.

Why it matters:

- reveals friction faster than success screens do
- helps the parent see what is not fitting

### 4. Frustration Signal

What triggers visible frustration.

Examples:

- too much text
- too much speed
- too much correction
- too much sitting
- too much repetition

Why it matters:

- should shape the next plan's activity mix, timing, and support level

### 5. Ease Signal

What feels immediately comfortable or intuitive.

Why it matters:

- helps identify confidence-building material
- gives the first month early wins

### 6. Stamina Signal

How long the child stays engaged before attention drops.

Why it matters:

- helps set realistic time limits
- helps fit the app inside the family's screen-time and energy budget

### 7. Prompt-Dependence Signal

How much adult support is needed to start, continue, or recover.

Why it matters:

- connects directly to the learner-support posture
- helps decide whether the app is helping or creating extra activation burden

### 8. Transfer Signal

Whether app use leads to off-app curiosity or output.

Examples:

- asking a follow-up question
- drawing something afterward
- wanting a related book
- wanting to try something physically

Why it matters:

- shows the app is feeding real learning energy, not just consuming time

### 9. Screen-Time Fit Signal

Whether the app stays inside the household screen-time posture without conflict or spillover.

Why it matters:

- keeps the app aligned with family reality
- prevents a useful tool from becoming a household burden

### 10. Evidence-Worthiness Signal

Whether anything from the session is worth saving.

Examples:

- a short parent note
- a screenshot, if approved
- an observed question
- an off-app artifact created after the session

Why it matters:

- keeps evidence light and meaningful
- prevents the app from flooding the portfolio with low-value noise

## Structured Note Shape

Translate meaningful app observations into short notes like:

```text
Date:
Time used:
What the child chose first:
What the child repeated or avoided:
What seemed easy:
What caused frustration:
Any off-app question, drawing, or follow-up:
Parent note:
Save to portfolio? [yes / no]
```

Most sessions should produce no formal note or only one short observation.

The system should preserve signal, not paperwork.

## Where The Signals Go

### Learner Profile

Persistent signals should update the learner profile:

- likely interests
- likely confidence zones
- likely friction triggers
- startup support needs
- preferred activity types

### Weekly Parent Review

Short-cycle signals should feed the weekly review:

- what the child chose
- what the child resisted
- what should be repeated
- what should be reduced
- what should be replaced

### Student Portfolio

Only meaningful evidence should enter the portfolio:

- approved screenshot
- short parent note
- off-app artifact or reflection
- milestone created from transfer or breakthrough

App activity by itself should not clutter the portfolio.

### Monthly Portfolio Review

Khan Academy Kids notes should help the monthly review answer:

- what patterns kept repeating
- what engagement improved
- what friction stayed persistent
- whether the app supported confidence, curiosity, or follow-through
- what next-month adjustment is now clearer

### Next-Step Recommendation Layer

This is the most important destination.

The system should use app signals to improve:

- reading-basket recommendations
- project ideas
- practice format choices
- time-block length
- support posture
- whether Khan Academy Kids should expand, stay limited, or be removed

## Recommendation Examples

Examples:

- `Student repeated animal activities and asked follow-up questions. Recommend more animal nonfiction and one related drawing or nature activity.`
- `Student lost focus after 8 minutes and resisted text-heavy sections. Reduce time block and avoid dense worksheet follow-ups.`
- `Student used the app willingly but did not transfer interest off-app. Keep the app as a small practice block, not the center of the day.`
- `Student needed help starting but stayed engaged once inside a familiar activity. Keep startup support high and transition gently into off-app work.`

## Governance Boundary

Khan Academy Kids may inform planning.

It may not overrule:

- parent judgment
- child safety boundaries
- save / share permissions
- outside-support escalation rules
- evidence standards

The app is one observation surface among several.

It is not the curriculum, the teacher of record, or the verdict on the child.

## Success Criteria

The pipeline is working when:

- parents can name what the child chose, repeated, avoided, or questioned
- app use produces better next recommendations
- screen-time stays bounded and intentional
- the portfolio captures only meaningful app-related evidence
- the app helps the first month become more legible rather than more noisy

## Failure Modes

The pipeline is failing when:

- app progress is mistaken for mastery
- too many screenshots or low-value notes enter the portfolio
- the app becomes random screen time
- recommendations are based on app data alone
- the family loses sight of off-app learning and real-world evidence

## Relationship To Other Docs

Use this with:

- [startup-bundle.md](startup-bundle.md)
- [30-day-plan-inputs.md](30-day-plan-inputs.md)
- [student-portfolio.md](student-portfolio.md)
- [monthly-portfolio-review.md](monthly-portfolio-review.md)
- [reading-basket.md](reading-basket.md)

Khan Academy Kids should behave like the reading basket: a governed observation-and-recommendation loop grounded in real student behavior.
