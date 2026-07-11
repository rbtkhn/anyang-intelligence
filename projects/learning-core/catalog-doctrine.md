# Dual Khan Catalogue Doctrine

Elementary School should treat Khan-related directory knowledge as **two parallel catalogue surfaces**, not one blended source of truth.

The catalogue layer is a **scaffold inside the Student Operating System**.

It is not the recommendation engine, curriculum authority, learner-placement system, or proof layer. Its job is to make resource awareness structured enough that the parent, operator, adapter layer, and review loops can make better governed decisions.

Use this mental model:

```text
catalogue layer
  -> resource awareness
  -> recommendation options
  -> parent-reviewed fit decision
  -> learner-use signal
  -> plan update
```

## The Two Catalogue Surfaces

### 1. `khan_academy_main_catalog`

This is the public-web-backed catalogue for the main Khan Academy product.

Use it when Elementary School needs:

- a durable external course tree
- a structured source for enrichment or reinforcement ideas
- provenance that points to official public web pages

Trust profile:

- stronger public provenance
- broader subject coverage
- more appropriate for directory and recommendation lookup than for behavioral learner inference

### 2. `khan_kids_curated_catalog`

This is the governed, manually curated catalogue for Khan Academy Kids.

Use it when Elementary School needs:

- a truthful starter-tool directory for early-learning recommendations
- a parent-facing explanation of what kinds of Khan Kids content exist
- a bridge between official public descriptions now and richer in-app capture later

Trust profile:

- truthful but coarse at first
- curated from official public descriptions and operator review
- must not pretend to represent hidden app-internal completeness unless explicitly verified

## Why The Surfaces Must Stay Separate

The two products are related, but they are not interchangeable:

- the main Khan Academy site is more publicly inspectable
- Khan Academy Kids is app-centered and exposes much of its real scope inside the app library
- Elementary School recommendation logic needs both, but with different evidence claims

If the surfaces are blended carelessly, the system will overstate certainty about Khan Kids and understate the different role of the main Khan Academy catalogue.

## Shared Catalogue Schema

Each catalog entry should carry:

- stable id
- source product
- title
- subject/domain
- age/grade band
- standards tags if known
- content type
- source URL or source note
- evidence status
- import method
- operator notes

See [catalog/catalog-schema.md](catalog/catalog-schema.md) for the operating schema.

## Governance Boundary

Catalogue knowledge may improve the option set available to recommendations.

The catalogue may answer:

- what resource categories exist
- where the source evidence came from
- which product surface the entry belongs to
- what kind of recommendation option the entry may support

The catalogue may not decide:

- whether the learner should use the resource
- whether the resource fits the household rhythm
- whether the learner is ready for a topic
- whether the resource should be used more, less, or paused
- whether a plan is approved for use

Catalogue knowledge may not:

- prove mastery
- diagnose the learner
- overrule parent authority
- overrule screen-time posture
- bypass save/share permissions
- imply that all Khan Kids content is publicly catalogued when it is not

## Track-Specific Update Logic

For `khan_academy_main_catalog`:

- prefer structured manifest import
- preserve official source URLs
- reject rows with missing provenance

For `khan_kids_curated_catalog`:

- start with truthful category-level entries
- expand only through governed manual curation or future in-app capture
- label entries by evidence strength rather than pretending to full coverage

## Student Operating System Role

The catalogue layer is **content directory scaffolding**.

It supports the Student Operating System the way a bookshelf, supply shelf, or course directory supports a teacher: it helps the adult see what is available, but it does not decide what the child needs.

Keep these layers separate:

- **Catalogue layer:** what resources and content categories exist, with provenance.
- **Adapter layer:** how a resource should fit the family, child, schedule, and parent boundary.
- **Signal pipeline:** what actually happened when the child used it.
- **Learning plan:** what parent-approved next step follows.

These should stay connected but distinct:

```text
catalogue knowledge
  -> resource awareness
  -> recommendation options

student behavior during actual use
  -> learner-fit signal
  -> weekly review
  -> learner profile update
  -> next-step recommendation
```
