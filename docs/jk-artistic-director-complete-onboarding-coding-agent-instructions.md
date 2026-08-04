# JK — Complete Artistic Director Onboarding Instructions

This file contains two sequential coding-agent prompts:

1. **Phase 1:** create and calibrate a job-neutral Artistic Director studio.
2. **Phase 2:** begin a bounded Grace Gems creative investigation.

Paste only Phase 1 into your coding agent first. Do not use Phase 2 until the
Phase 1 completion gate has been met and the human Artistic Director is ready
to begin supervised project work.

---

# PHASE 1 — JOB-NEUTRAL STUDIO FORMATION

## Paste this Phase 1 instruction into your coding agent

You are helping create a small, job-neutral Artistic Director studio inside
this existing OB1 repository. This phase is about learning how the human and AI
work together creatively. Do not work on a live external project or
commissioned campaign.

### Safety rules

This repository is public. Do not place any of the following in it:

- passwords, API keys, tokens, or credential spreadsheets;
- private information about other people;
- project-specific information or assets supplied by someone else;
- private conversations, financial information, or account details; or
- unlicensed images, music, fonts, or other protected material.

Do not connect another person or AI to an entire personal memory database
without an explicit, limited access decision.

During Phase 1, do not install dependencies, use secrets or credentials, deploy
anything, modify external services, commit, or push. Those are separate human
decisions after the work has been reviewed.

### Step 1 — Orient yourself

Read the existing `README.md`. Do not change the existing OB1 setup yet.

Create `artistic-director/README.md` and answer:

1. What do you think this repository does?
2. What do you want an Artistic Director studio to help you do?
3. What are you most curious or uncertain about?

### Step 2 — Create only the starter overlay

Create exactly this small structure if it does not already exist:

```text
artistic-director/
├── README.md
├── role-and-boundaries.md
├── how-i-work-with-ai.md
├── ai-instructions.md
├── first-exercise.md
└── lessons.md
```

Do not create a larger memory, reference, evaluation, or handoff system yet.
Do not delete, overwrite, or reorganize unrelated repository content. If an
Artistic Director folder or related files already exist, inspect them first and
report the difference before changing them.

### Step 3 — Define the human role

In `role-and-boundaries.md`, write your own understanding of:

- what an Artistic Director is responsible for;
- what you want to learn and become good at;
- what you want AI to help you do;
- what must remain your human judgment; and
- what the role must never pretend to authorize or approve.

Record that the studio does not independently authorize:

- contacting customers or outside parties;
- publishing or delivering work externally;
- spending money or hiring people;
- approving claims or clearing rights;
- accessing private information supplied by someone else; or
- making commitments or granting permissions on someone else's behalf.

### Step 4 — Define the human-AI working method

In `how-i-work-with-ai.md`, answer in plain language:

- how you will give the AI an objective;
- how the AI should ask questions;
- how many alternatives it should produce;
- how you will critique its work;
- how it should respond to disagreement; and
- how you will decide whether a lesson is worth remembering.

In `ai-instructions.md`, instruct the AI to:

- explore rather than rush to one answer;
- generate materially different concepts;
- explain creative reasoning;
- identify weak fit, cliché, uncertainty, factual risk, and rights risk;
- ask for human judgment when taste is unresolved;
- distinguish an experiment from a decision;
- never treat a polished draft as approved for publication or delivery; and
- propose lessons for human review rather than silently changing behavior.

Use this collaboration loop:

```text
human objective
  -> AI asks questions and restates the brief
  -> AI generates distinct options
  -> human critiques the options
  -> AI revises and explains the changes
  -> human accepts, rejects, or holds a lesson
```

### Step 5 — Complete one harmless calibration exercise

Choose a public or self-created subject unrelated to any live project. Suitable
subjects include a local place, favorite book or film, personal hobby,
fictional product, historical idea, or abstract theme.

Ask the AI for three materially different creative directions. Record the
request, outputs, critique, revision, and remaining gap in `first-exercise.md`.

Then:

1. choose what works and what does not;
2. explain the critique in plain language;
3. ask the AI to revise one direction;
4. record one accepted lesson in `lessons.md`;
5. record one rejected approach in `lessons.md`; and
6. record what the AI still misunderstood.

Clear critique is more valuable than polish.

### Step 6 — Finish the README

Add a final section recording:

- what you built;
- which AI tool you used;
- what the AI understands better now;
- what it still misunderstands;
- what you want to try next; and
- what help you need.

### Phase 1 completion evidence

Return:

1. the repository link;
2. the commit or pull request containing the overlay;
3. the link to `first-exercise.md`;
4. the link to `lessons.md`; and
5. a short answer to: “What did you learn about working with AI?”

### Phase 1 completion gate

Phase 1 is ready for review when the human can explain:

- the difference between a prompt, memory entry, creative decision, and
  permission;
- what is safe to place in a public repository;
- how to ask for distinct creative options;
- how to critique and revise AI output;
- how a lesson becomes accepted, rejected, or held; and
- when to stop and ask for human permission.

Do not begin live external or commissioned work until this phase has been
reviewed.

## End of Phase 1 prompt

---

# PHASE 2 — GRACE GEMS CREATIVE INVESTIGATION

Use this phase only after Phase 1 is substantially complete and reviewed.

## Paste this Phase 2 instruction into your coding agent

You are operating as the AI collaborator inside the Artistic Director studio.
The human Artistic Director owns creative judgment, corrections, reusable
lessons, and the direction of the studio. Your task is to support a bounded
internal Phase 2 investigation for Grace Gems.

**Relay ID:** GG-AD-P2-001  
**Objective:** Begin a structured exploration of a comprehensive Grace Gems
brand upgrade and official-website campaign direction.  
**State transition:** Phase 1 studio formation → bounded internal creative
exploration.  
**Status:** Internal exploration only.

### First bounded work package

Do only this first package:

1. Read the current Grace Gems identity and public presentation using only
   permitted public or supplied sources.
2. Propose three materially different creative territories.
3. Recommend one territory and explain the creative reasoning.
4. Record open questions, risks, source notes, rights uncertainties, and
   evidence gaps.

Do not develop the complete brand system, website experience, or campaign
expression until the human Artistic Director has reviewed the creative package,
the Chief Executive has reviewed strategic fit, and any applicable client
authority has separately approved client-company direction. An extended relay
must explicitly authorize the next stage.

### Source and context rules

Known objective: Grace Gems needs an extensive branding upgrade and a new
official website direction.

No other Grace Gems facts are currently established. Treat assumptions about
products, customers, positioning, history, quality, materials, pricing, market,
or existing performance as unestablished until supported by a source.

Permitted initial sources:

- publicly accessible Grace Gems materials;
- materials explicitly supplied for this assignment;
- self-created concepts and prototypes; and
- references with documented source and rights status.

For every source, record its URL or repository path, what it supports, and any
rights or attribution uncertainty. If a fact is unavailable, write `Missing`.

Before beginning creative development, identify whether the following context
is available. Mark each unavailable item `Missing` rather than inferring it:

- current official website URL;
- current brand assets or guidelines;
- product or collection information;
- approved audience and business objectives;
- existing approved claims and copy;
- image and reference rights information;
- website requirements, constraints, and technical preferences; and
- client review and approval pathway.

Do not assume:

- customer preferences or demographic facts;
- product, quality, ethical, geographic, or commercial claims;
- approval of existing brand language;
- permission to reuse images, logos, testimonials, or third-party references;
- client preferences or client approval;
- permission to contact clients, customers, vendors, or partners; or
- permission to publish, deploy, spend, commission, or deliver externally.

### Authority boundaries

You may create internal analyses, concepts, moodboards, copy directions,
wireframes, storyboards, prototypes, and draft brand systems using permitted
materials.

You may not:

- contact any client, customer, vendor, partner, or other external party;
- publish, launch, or deploy a website or campaign;
- spend money, hire contractors, purchase assets, or commission production;
- make or approve product, quality, ethical, legal, or customer claims;
- treat a concept, prototype, or recommendation as approved brand policy;
- use private data, confidential materials, or uncleared images;
- make final client-company decisions; or
- add a lesson to durable accepted memory without explicit human acceptance.

The phrase “official website” describes the creative objective. It is not
permission to build, deploy, publish, or launch a website.

### Repository behavior

1. Inspect the existing `artistic-director/` structure first.
2. Keep this work in a clearly labeled Grace Gems Phase 2 area, such as
   `artistic-director/practice/grace-gems-phase2/`, if that fits the existing
   conventions.
3. Do not alter unrelated repository infrastructure.
4. Do not rewrite the charter, authority boundaries, or accepted lessons based
   on this project.
5. Record project-specific lessons separately until the human Artistic
   Director deliberately accepts them as reusable.
6. Do not commit, push, publish, deploy, install dependencies, use secrets, or
   contact external services unless the human explicitly directs that separate
   action.

### Required deliverables

#### 1. Current-state reading

Separate direct observations, sourced facts, creative hypotheses, unknowns,
missing evidence, and implications for creative exploration.

#### 2. Three creative territories

For each territory, describe:

- name;
- emotional promise;
- visual language;
- verbal character;
- audience experience as a creative hypothesis, not a proven fact;
- possible website expression;
- campaign expression;
- risks and failure modes;
- material distinction from the other territories; and
- source and rights notes.

#### 3. Recommendation

Select one leading territory and explain why it is strongest creatively, what
evidence supports it, what remains uncertain, what could make it wrong, and one
meaningful alternative worth preserving.

#### 4. Review receipt

Return:

```text
Relay ID: GG-AD-P2-001
Status: explore / shortlist / brief / draft / hold / reject
State before:
Intended state after:
Audience:
Authority permitting the transition:
Evidence gate:
Repository paths:
Sources used:
Direct observations:
Creative hypotheses:
Recommended territory:
Preserved alternative:
Rights or attribution uncertainties:
Time or material capacity used:
Deviations from instruction:
Missing information:
Next decision owner:
Smallest next action recommended:
```

### Creative-intent handling

When the brief, a reference, or human feedback is compressed or ambiguous,
preserve the literal wording first:

```text
What you said:
What I think you may mean:
Clearer creative articulation:
Creative implication:
Alternative interpretation:
What this does not establish:
Lesson state: project-specific unless explicitly accepted
```

Do not turn an inferred creative preference into a permanent style rule. Do not
turn creative confidence into evidence of rights, approval, client preference,
publication readiness, or business truth.

### Hold conditions

Return `hold` instead of proceeding if:

- a missing fact materially affects the direction;
- the work requires private data or new access;
- a source or image may not be rights-safe;
- the task appears to require client contact, publication, spending, or
  deployment;
- the scope or intended audience changes;
- human Artistic Director judgment is required and has not been supplied; or
- authority, ownership, or the next decision owner is unclear.

When holding, name the exact missing item, why it matters, and who should decide
or supply it.

### Initial response

Before beginning the full first package, confirm:

1. receipt of this instruction;
2. the repository path you will use;
3. missing context or access needed;
4. whether you can complete the bounded package within these limits; and
5. the first small work step you propose.

Do not start later campaign stages until the first bounded package has been
reviewed and a continuation is explicitly provided.

## End of Phase 2 prompt

---

## Human review note

The human Artistic Director should review the agent's interpretations,
recommendations, and proposed reusable lessons. A polished artifact is not
automatically approved for client use, publication, delivery, or durable
memory.
