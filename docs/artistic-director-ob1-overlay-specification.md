# Artistic Director Overlay for JK3303/OB1

**Target repository:** `JK3303/OB1`  
**Base system:** Open Brain  
**Phase:** Phase 1 studio formation  
**Status:** Design only; no remote repository changes made

## Purpose

Add an Artistic Director operating layer to the existing OB1 Open Brain
repository without replacing or restructuring its core infrastructure.

OB1 remains the single technical and GitHub repository. The overlay teaches the human
Artistic Director how to use AI creatively, gives the AI a reviewable working
method, and creates a place for the studio to evolve independently.

The overlay is job-neutral. It contains no Grace Gems strategy, client facts,
customer records, private evidence, campaign requirements, or assumed brand
direction.

## Design principles

- Preserve OB1's existing setup, extensions, recipes, schemas, and skills.
- Add a clearly named Artistic Director layer rather than scattering role files
  throughout the Open Brain infrastructure.
- Keep human preferences, AI behavior, role rules, and project facts distinct.
- Prefer plain Markdown before adding code, automations, or database schema.
- Make every AI lesson attributable, reviewable, and reversible.
- Keep this public repository free of credentials, private client data,
  confidential references, and unlicensed assets.
- Allow the human to change the overlay's creative direction after the initial
  seed is accepted.

## Exact overlay structure

Add this directory at the root of the existing OB1 repository. This is a folder
inside OB1, not a second repository:

```text
artistic-director/
├── README.md
├── charter/
│   ├── role.md
│   ├── working-agreement.md
│   └── boundaries.md
├── ai/
│   ├── system-instructions.md
│   ├── collaboration-loop.md
│   ├── critique-rubric.md
│   ├── calibration-set.md
│   ├── prompt-patterns.md
│   └── change-log.md
├── memory/
│   ├── role-principles.md
│   ├── creative-vocabulary.md
│   ├── accepted-lessons.md
│   ├── rejected-lessons.md
│   └── open-questions.md
├── references/
│   ├── README.md
│   ├── reference-log.md
│   ├── rights-and-attribution.md
│   └── generic-lessons.md
├── practice/
│   ├── briefs/
│   ├── concepts/
│   ├── critiques/
│   └── experiments/
├── decisions/
│   ├── creative-decisions.md
│   ├── holds-and-rejections.md
│   └── review-receipts.md
├── evaluations/
│   ├── human-reviews/
│   ├── ai-self-reviews/
│   └── cohort-reviews/
└── handoff/
    ├── current-state.md
    ├── successor-guide.md
    └── exit-record.md
```

## File purposes

### `artistic-director/README.md`

The front door for the human and any AI working in the overlay. It should
explain:

- this is an independent Artistic Director studio built on OB1;
- the overlay is not required to stay in exact sync with Anyang Intelligence;
- the human owns the creative evolution of the studio;
- Chief Executive observation is read-only and does not create task authority;
- job-specific material belongs in a later, separately bounded project area;
- where to find the role, AI, memory, practice, decisions, and handoff files.

### `charter/role.md`

Start from the governed Artistic Director role and let the human add his own
interpretation. Separate:

- durable role responsibilities;
- the current human holder's responsibilities;
- AI-assisted responsibilities;
- decisions reserved to Anyang Intelligence or a client owner; and
- the human's own artistic ambitions.

### `charter/working-agreement.md`

Define how the human and AI collaborate:

- how a request becomes a brief;
- how concepts are generated and compared;
- when the AI asks questions;
- how critique is recorded;
- how a lesson enters memory;
- how the human overrides the AI; and
- how disagreement is preserved rather than flattened.

### `charter/boundaries.md`

State that the overlay cannot independently authorize client contact,
publication, delivery, spending, hiring, contracting, rights clearance,
claims, private-data access, or changes to Executive Council authority.

### `ai/system-instructions.md`

Define the initial AI behavior. It should require the AI to:

- distinguish exploration, shortlist, brief, draft, review-ready, approved,
  delivered, and published states;
- show alternatives instead of prematurely converging;
- explain its creative reasoning;
- identify uncertainty, cliché, factual risk, rights risk, and weak fit;
- ask for human judgment where taste or authority is unresolved; and
- treat the human's corrections as candidate lessons, not automatic universal
  rules.

### `ai/collaboration-loop.md`

Use this first operating loop:

```text
human objective
  -> AI questions and restates the brief
  -> AI generates materially different options
  -> human critiques the options
  -> AI revises and explains the changes
  -> human records the lesson
  -> AI proposes a reusable rule
  -> human accepts, rejects, or holds the rule
```

### `ai/critique-rubric.md`

Score or describe work across:

- clarity;
- distinctiveness;
- emotional or audience effect;
- strategic fit;
- craft and coherence;
- originality versus imitation;
- factual and rights discipline;
- reuse potential;
- revision burden; and
- whether the work feels like the human's developing practice.

### `ai/calibration-set.md`

Contain a small, job-neutral test set. Each exercise should have:

- the brief;
- the AI output;
- the human's critique;
- the revised output;
- the accepted lesson;
- the rejected lesson; and
- a note on what the AI still misunderstood.

Use public or self-created material only. Do not use Grace Gems material in
Phase 1.

### `memory/`

Keep these categories separate:

- `role-principles.md`: role-level rules that should survive holder changes;
- `creative-vocabulary.md`: terms and distinctions the studio uses;
- `accepted-lessons.md`: human-approved reusable lessons;
- `rejected-lessons.md`: approaches the AI should avoid, with reasons; and
- `open-questions.md`: unresolved areas where the AI should not pretend
  confidence.

### `references/`

Record why a reference matters, not just a link to an image. Include rights
status, what generic principle may be learned, what must not be copied, and
whether the reference is safe to reuse. Private or licensed source material
should not be committed to this public repository.

### `practice/`

This is the human's creative laboratory. It should begin with job-neutral
exercises, then later receive a separate Grace Gems campaign area only after
Phase 1 completion and approval.

### `decisions/`

Record meaningful creative choices, alternatives, reasoning, reversals, holds,
and rejections. A creative decision receipt is not an approval to publish,
deliver, spend, or make a client commitment.

### `evaluations/`

Capture human review, AI self-review, and cohort-level assessment separately.
The AI may critique its own output, but the human remains the authority for
the human's creative standard.

### `handoff/`

Make the studio understandable to a successor without pretending that one
human's taste is universal. Attribute holder-specific preferences and preserve
the distinction between role memory and personal style.

## OB1-specific security requirements

Before using OB1's setup guide:

- do not commit the credential tracker spreadsheet;
- do not commit `.env` files, API keys, Supabase secrets, access keys, or
  tokens;
- do not use the public repo for raw Open Brain captures containing private
  personal, client, customer, financial, or account information;
- verify that database and MCP access are authenticated and scoped;
- do not connect the Chief Executive to the entire personal memory database by
  default; expose only an approved observation surface; and
- keep Grace Gems data in its governing private or approved project location.

The public GitHub repo and the external OB1 database are separate surfaces.
Protect both independently.

## Phase 1 file creation order

The human should create files in this order:

1. `artistic-director/README.md`;
2. `charter/role.md`;
3. `charter/boundaries.md`;
4. `charter/working-agreement.md`;
5. `ai/system-instructions.md`;
6. `ai/collaboration-loop.md`;
7. `ai/critique-rubric.md`;
8. one calibration exercise;
9. `memory/` files after the exercise, based on actual learning;
10. `handoff/current-state.md`.

Do not ask the human to fill every file with abstract policy before he has
used the AI. The initial files establish safety and orientation; the first
exercise should generate the material that makes the remaining files useful.

## Phase 1 completion condition

The OB1 overlay is ready for Phase 2 when:

- the human can explain the difference between an AI prompt, a memory entry,
  a creative decision, and an authority approval;
- the AI can produce and compare several distinct concepts;
- the human has critiqued and revised at least one AI output;
- at least one accepted lesson and one rejected lesson are recorded;
- the human can identify what must not enter the public repo or Open Brain;
- the Chief Executive can observe the overlay without write access; and
- the human can describe what would require escalation before client work.

Phase 2 may then add a separately bounded Grace Gems campaign area. It should
not be mixed into the job-neutral calibration history.
