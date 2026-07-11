# Khan Adapter Layer

This document defines how **Elementary School** should use **Khan Academy** and **Khan Academy Kids** without trying to replace their internal recommendation logic.

## Core Idea

Khan already has its own recommendation and sequencing system inside the product.

Elementary School does **not** need to build a competing recommendation engine for Khan content.

Elementary School does need to build the **adapter layer around Khan** so the product fits the actual child, parent, and household.

In short:

```text
Khan recommends content inside Khan
  ->
Elementary School decides how Khan should fit inside the Student Operating System
```

## What Khan Should Be Trusted To Do

Khan can handle:

- in-product content sequencing
- in-product progression logic
- in-product next-content recommendation
- skill-path structure inside the app or site

Elementary School should treat this as product-native guidance, not as something it needs to reinvent.

## What Elementary School Should Not Delegate To Khan

Elementary School should not delegate:

- parent authority
- household screen-time posture
- supervision decisions
- save/share boundaries
- whether Khan should be central, small, paused, or removed
- whether app behavior is helping the learner overall
- whether app behavior is transferring into books, projects, questions, or real-world curiosity

Khan can recommend what is next **inside Khan**.

Elementary School must decide whether Khan itself is being used well **inside the family's Learning Core**.

## Adapter-Layer Questions

The adapter layer should answer questions like:

- Should Khan Academy Kids be used at all right now?
- Should it be 10 minutes, 15 minutes, or paused?
- Should Khan stay a small support block or expand?
- Is the learner showing healthy engagement or repeated friction?
- Is Khan producing useful transfer into reading, drawing, projects, or questions?
- Does Khan fit the parent's real supervision and screen-time posture?
- Should off-app recommendations change because of what Khan surfaced?

## Signals The Adapter Layer Needs

### Parent and Household Signals

- screen-time budget
- supervision budget
- parent energy budget
- prep tolerance
- household rhythm reality
- authority boundaries

These determine whether Khan fits the home at all.

### Learner-Use Signals

- what the learner chooses first
- what the learner repeats
- what the learner avoids
- what creates frustration
- what feels easy
- how long attention holds
- how much prompting is needed
- whether interest transfers off-app

These determine whether Khan is helping or merely consuming time.

### Recommendation Outcome Signals

- whether the parent kept or changed the Khan block
- whether the child used it willingly
- whether Khan led to useful next-step ideas
- whether Khan crowded out better activities

These determine whether Khan should expand, stay limited, or be reduced.

## Adapter-Layer Outputs

Elementary School should output decisions like:

- `use Khan Academy Kids as a 10-15 minute supervised starter block`
- `keep Khan small; use it mainly for confidence and observation`
- `reduce Khan time because attention drops after 8 minutes`
- `pair Khan animal-interest sessions with nonfiction books in the reading basket`
- `pause Khan for now because it is creating friction without useful transfer`
- `use main Khan Academy as optional extension for a visible spillover interest`

These are **usage and interpretation decisions**, not content-sequencing decisions.

## Relationship To Other Khan Artifacts

### Catalogue Doctrine

See [catalog-doctrine.md](catalog-doctrine.md).

The catalogue tells us:

- what kinds of Khan content exist
- what recommendation options are available

The catalogue does not tell us whether the current learner should use more or less Khan.

### Transition Point

See [khan-transition-point.md](khan-transition-point.md).

The transition note defines when the learner may be ready to move from Khan Academy Kids toward the main Khan Academy environment.

It gives priority to visible capabilities and parent-approved readiness over raw completion counts.

### Signal Pipeline

See [khan-academy-signal-pipeline.md](khan-academy-signal-pipeline.md).

The signal pipeline tells us:

- what actually happened during use
- what learner-fit evidence appeared

The signal pipeline is the main evidence source for adapter-layer decisions.

## Governance Boundary

The adapter layer may:

- decide how Khan fits into the broader plan
- decide whether Khan should expand, stay limited, or be removed
- turn Khan-linked behavior into off-app recommendations

The adapter layer may not:

- convert Khan progress into mastery claims
- convert Khan completion into grade placement
- convert Khan friction into diagnosis
- bypass parent authority

## Success Criteria

The adapter layer is working when:

- Khan remains useful without taking over the learning plan
- the parent understands why Khan is being used
- Khan time stays inside household reality
- strong in-app interest produces better off-app recommendations
- repeated friction causes adjustment rather than drift
- Elementary School leverages Khan's strengths without surrendering judgment to it
