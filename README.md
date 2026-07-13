# Anyang Intelligence

Anyang Intelligence builds **Executive Operating Systems** for organizations: AI-assisted decision, memory, coordination, and learning infrastructure trained on how each business actually works.

The starting thesis is simple: leaders should not have to reconstruct the state of the business from scattered meetings, dashboards, docs, and memory every time they make a decision.

## Implementation Root

This folder is the Anyang Intelligence **operating substrate**: the executable working root where docs, customer memory, skills, CLIs, templates, tests, and recursive improvement live together.

The previous implementation-root name was `repo_probe`. That name is now historical. The current physical path and architectural identity are both `operating-substrate`.

See [docs/operating-substrate-migration-plan.md](docs/operating-substrate-migration-plan.md) for the completed rename plan and rollback notes.

## What This Is

An Executive Operating System is an organization-specific intelligence layer that helps leadership:

- Know the current state of the business.
- Clarify decisions before they become drift.
- Coordinate execution across owners, projects, and review cycles.
- Learn from outcomes and preserve institutional memory.

This is not an "AI CEO" that replaces leadership. It is an AI-native operating partner that makes leadership more coherent, better informed, and easier to compound over time.

## Strategic Direction: Embodied Agency

Anyang Intelligence builds governed intelligence systems that help people understand, coordinate, and eventually act in digital and physical worlds. The direction is not autonomous authority: every consequential action remains bounded by explicit human approval, evidence, safety, privacy, security, and accountability requirements.

Today, the work is primarily digital operating infrastructure. Over time, the same memory, decision, review, and escalation architecture may govern useful tools, workflow automation, and physical systems where a defined task, maintenance plan, and human override make their use responsible.

## First Wedge

The first version is service-led installation for founder-led teams and lean organizations with real complexity but limited executive infrastructure.

The deliverable is a working Executive OS installed inside the organization:

- Company context map.
- Executive memory model.
- Decision log and decision memo workflow.
- Weekly executive review cadence.
- Project and owner coordination loop.
- Risk register.
- Learning loop for assumptions, outcomes, and course correction.
- Loop grammar for turning memory, decision, coordination, review, and learning into repeatable operating cycles.

## Repository Structure

```text
anyang-intelligence/
  README.md
  docs/
    thesis.md
    product.md
    implementation-model.md
    install-method.md
    loops.md
    membranes.md
    governance.md
  os/
    executive-memory.md
    decision-system.md
    coordination-loop.md
    learning-loop.md
  skills/
    README.md
    customer-state-update/
      SKILL.md
  projects/
    README.md
    book-club/
      README.md
      executive-os-install.md
    learning-core/
      README.md
      executive-os-install.md
    grace-gems/
      README.md
      executive-os-install.md
    media-production/
      README.md
      executive-os-install.md
    mountain-villa/
      README.md
      executive-os-install.md
  playbooks/
    installation-sprint.md
    weekly-executive-review.md
    decision-memo.md
  templates/
    company-context-map.md
    decision-log.md
    risk-register.md
    operating-review.md
```

## Current Status

This repo is in concept and operating-design stage. The immediate goal is to define the Executive OS clearly enough to install it manually with early organizations before turning repeated patterns into software.

The current installations are tracked in [projects/](projects/README.md): Grace Gems proves marketplace execution governance, Mountain Villa proves property and asset-risk governance, Book Club proves lightweight community cadence governance, Media Production proves creative pipeline governance, and Learning Core proves high-trust educational operations.

The shared method is captured in [docs/install-method.md](docs/install-method.md). The loop grammar is captured in [docs/loops.md](docs/loops.md), the cross-lane filter judgment is captured in [docs/membranes.md](docs/membranes.md), material claim discipline is captured in [docs/evidence-awareness-checklist.md](docs/evidence-awareness-checklist.md), and reader-facing judgment is governed by [docs/analytical-interfaces.md](docs/analytical-interfaces.md). Each project should adapt that method to its own domain instead of inventing a new operating shape from scratch.

The current system-level buildout is summarized in [docs/operating-substrate.md](docs/operating-substrate.md).

The repo's north-star AI posture is defined in [docs/artificial-enlightened-intelligence.md](docs/artificial-enlightened-intelligence.md): more capability should produce more evidence discipline, stronger membranes, clearer authority boundaries, and safer recursive improvement.

Reusable maintenance procedures are tracked in [skills/](skills/README.md).
