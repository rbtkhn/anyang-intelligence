# Operating Substrate

This document summarizes the system Anyang Intelligence has built so far.

The repo is no longer only a thesis about Executive Operating Systems. It now contains the first pieces of an operating substrate: docs that define the philosophy, command-line tools that make installations and loops repeatable, customer folders that preserve domain context, and skills that encode recurring procedures.

## Core Thesis

Anyang Intelligence compounds when real customer work produces reusable operating primitives.

The pattern is:

```text
customer work
  -> friction or repeated move
  -> loop, template, skill, or tool
  -> better next cycle
  -> stronger Executive OS
```

That compounding pattern is the repo's practical meaning of [recursive self-enhancement](recursive-self-enhancement.md): governed, repo-visible improvement to the operating surface after real work reveals a durable lesson.

The system should get smarter without taking authority away from humans. It prepares decisions, checks quality, preserves evidence, and improves memory; it does not publish, spend, commit customers, make legal/tax judgments, or cross privacy membranes by itself.

## System Layers

### 1. Philosophy And Governance

The foundation lives in `docs/`:

- `docs/thesis.md` defines the Executive OS idea.
- `docs/product.md` defines the product boundary.
- `docs/install-method.md` defines the repeatable 7-part installation method.
- `docs/loops.md` defines the loop grammar.
- `docs/membranes.md` defines cross-customer transfer rules.
- `docs/governance.md` defines authority boundaries.

These docs answer what the system is allowed to become.

### 2. Tooling Spine

The first installable Python tools now live under `cli/`:

- `anyang-loop` parses, validates, simulates, lists, and exports 8-element loop definitions.
- `anyang-install` scaffolds and validates customer installations from structured YAML input.

This matters because it turns the operating philosophy into repeatable infrastructure. A customer install no longer has to begin from a blank page, and a loop can be checked for signal, memory, decision, action, evidence, cadence, learning update, and governance boundary.

### 3. Customer Operating Memory

The `customers/` folder holds the live operating portfolio:

- Media Production is the clearest near-term commercial proof because it has a $1,000/month Grace Gems retainer, a defined production role, and measurable outputs.
- Grace Gems is both a direct operating case and the first paying client of Media Production.
- Elementary School is paid but high-trust; it should move through scope and safety discipline before delivery.
- Book Club, Mountain Home, and Non-Profit broaden the operating model across community, property, asset, donor, board, and mission contexts.

The portfolio is intentionally mixed. It teaches which primitives generalize and which facts must stay local.

### 4. Skills As Encoded Operating Procedures

The `skills/` folder converts repeated work into procedures future agents can reuse.

The most developed chain is Media Production:

```text
source signal
  -> media-production-brief
  -> media-production-quality-gate
  -> media-production-package
  -> media-production-ledger
  -> future review and learning
```

That chain now supports moving a Grace Gems or Predictive History signal from idea to brief, review, package, and evidence memory without confusing drafts with approval, packages with publication, or signals with proof.

The native `coffee` skill provides the repo's recursive improvement pulse. It reads the Anyang Intelligence portfolio, loops, membranes, skills, and git state, then names the current picture, entropy, one learning, one improvement candidate, and a bounded A-D next move.

The native `bravo` skill provides the repo's positive-signal capture pulse. It turns operator satisfaction into reusable design intelligence by naming what worked, why it worked, where it may apply again, and what boundary prevents overgeneralization.

The native `dream` skill provides the repo's closeout pulse. It checks git state, reviews the latest durable changes, runs Anyang-native validation when appropriate, separates known legacy warnings from fresh issues, and names what tomorrow inherits without creating autonomous merge authority.

See [cadence-loop-example.md](cadence-loop-example.md) for a short fixture showing `coffee -> bravo -> dream -> coffee` using the native cadence skill work itself.

### 5. Internal Research Archive

The `customers/singularity-science/` folder stores the Singularity Science research project.

Its [archive](../customers/singularity-science/archive/README.md) holds internal analysis source material for Innermost Loop and Moonshots. This keeps transcripts, source notes, analyses, and frontier ledgers separate from docs, skills, and customer deliverables while still placing the ongoing research project beside other Anyang Intelligence operating lanes.

Archive material can inform product judgment, governance warnings, and reusable primitive candidates. It should not be treated as public content, customer-facing copy, or reusable doctrine without source discipline, rights review, and membrane translation.

## What Is Valuable Now

The valuable thing is not any single file. The value is that the repo has begun to behave like the product it describes.

It can now:

- Install customer operating folders more consistently.
- Validate customer loops instead of relying on prose alone.
- Preserve governance boundaries as first-class structure.
- Turn repeated customer work into skills.
- Keep Media Production work moving through a human-approved pipeline.
- Use `coffee` to notice friction and choose the next durable improvement.
- Use `bravo` to notice excellence and reinforce repeatable patterns.
- Use `dream` to settle what landed, verify the repo can rest, and name what tomorrow inherits.

This is the first sign of compounding: the work improves the system that will perform the next work.

## Authority Model

Humans remain the authority layer.

Anyang Intelligence may:

- Draft.
- Structure.
- Validate.
- Simulate.
- Package.
- Prepare ledger entries.
- Recommend next actions.
- Surface risks and missing evidence.

Anyang Intelligence may not autonomously:

- Publish or deliver external work.
- Approve customer commitments.
- Approve spending or hiring.
- Make legal, tax, payroll, child-safety, board, or compliance conclusions.
- Treat private customer facts as reusable product doctrine.
- Treat a generated recommendation as human authority.

The strictest applicable membrane wins.

## Current Center Of Gravity

The strongest near-term product proof is Media Production serving Grace Gems.

Reasons:

- It has real monthly revenue.
- It has a concrete service package.
- It has visible production constraints.
- It has repeatable creative work.
- It has quality and evidence needs that can become software primitives.
- It is lower-risk than Elementary School while still commercially meaningful.

Elementary School remains important, but its trust boundary means scope and safety must lead. Non-Profit and Mountain Home are valuable governance proofs, but they should not displace paid operating obligations until the primary proof loop is stable.

## Next Leverage Points

The next valuable improvements are likely:

- A Media Production weekly operating review that uses brief, gate, package, and ledger outputs.
- A Grace Gems first-week deliverables plan tied to owner approval boundaries.
- A Creative Production Operator onboarding/sourcing gate before contractor work begins.
- Real Elementary School parent intake responses run through the readiness loop before any 30-day plan draft.
- A cross-customer primitive map that turns lessons into templates without leaking private context.

Each next step should follow the same rule: preserve one durable improvement only when it makes the next operating cycle smarter.

## Working Architecture

The system now has this shape:

```text
docs
  -> define philosophy, loops, membranes, governance

cli
  -> make loops and installs repeatable

customers
  -> preserve domain operating memory and research lanes

skills
  -> encode recurring procedures

coffee
  -> detects entropy and selects the next improvement

bravo
  -> captures positive signals and repeatable taste

dream
  -> confirms what landed and closes the cycle

human authority
  -> approves commitments, publication, spending, and boundary crossings
```

This is the operating substrate: not full software yet, not just documentation anymore, but a working bridge between manual installation and productized Executive OS infrastructure.
