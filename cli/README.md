# Anyang CLI Tools

`anyang-loop` validates and renders Executive OS loop definitions for Anyang Intelligence.

`anyang-install` scaffolds and validates customer Executive OS installation folders from deterministic templates.

It also provides Singularity Science archive intake commands for transcript manifests.

Loops follow the 8-element grammar from [`docs/loops.md`](../docs/loops.md):

- signal
- memory objects
- decision
- action
- evidence
- cadence
- learning update
- governance boundary

The engine is advisory infrastructure. It prepares and checks operating loops; it does not execute customer work, approve commitments, send communications, or override human authority.

## Install

From the repo root:

```bash
python -m pip install -e .[dev]
```

Then run:

```bash
anyang-loop --help
anyang-install --help
```

If your shell does not have Python on `PATH`, install or activate a Python 3.10+ environment first.

## Loop Schema

YAML:

```yaml
name: weekly-executive-review
description: Weekly operating loop for leadership review.
loop_type: operating
customer_lane: shared
authority: human leadership
tags:
  - weekly
  - review
signal: Weekly review window or material operating change.
memory_objects:
  - priorities
  - risks
  - decisions
decision: Prepare tradeoffs and recommended next actions for leadership.
action: Convert approved decisions into owners, deadlines, and follow-ups.
evidence: Operating review, decision log update, owner approval, or metric.
cadence: Weekly.
learning_update: Preserve lessons and update memory for the next review.
governance_boundary: Humans approve priorities, commitments, spending, and external claims.
```

Markdown can use YAML front matter or headings:

```markdown
# Weekly Executive Review

## Signal

Weekly review window.

## Memory Objects

- priorities
- risks
- decisions

## Decision

Prepare tradeoffs for leadership.

## Action

Coordinate approved next actions.

## Evidence

Operating review and decision log.

## Cadence

Weekly.

## Learning Update

Update memory with lessons learned.

## Governance Boundary

Human leadership approves commitments and external claims.
```

## Commands

```bash
anyang-loop validate customers/grace-gems/loop-examples
anyang-loop new weekly-review --format markdown --type operating
anyang-loop list customers --include-builtins
anyang-loop simulate canonical-executive-loop
anyang-loop export recursive-improvement-loop --format obsidian
anyang-loop export customers/grace-gems/loop-examples/listing-gate.yaml --format json
```

`validate` exits nonzero when required grammar fields are missing. Warnings are advisory and should be reviewed before treating a loop as operational.

## Built-In Loops

- `canonical-executive-loop`: the inherited Executive OS loop from memory to updated memory.
- `recursive-improvement-loop`: the Anyang Intelligence self-improvement loop that turns friction into better docs, skills, templates, or guardrails.

## Lint Warnings

- `open-loop-drift`: no owner, responsibility, authority, or approval language is visible.
- `evidence-gap`: evidence is vague or lacks receipts, approvals, artifacts, metrics, or records.
- `cadence-mismatch`: cadence does not name a clear rhythm.
- `governance-bypass`: boundary does not name human authority or approval.
- `memory-decay`: learning does not update or preserve memory.
- `overbuilt-loop`: the loop is likely too large for one cycle.
- `underbuilt-loop`: high-trust content lacks a strong approval boundary.
- `no-recursive-update`: friction is named without a durable improvement path.

## Human Authority And Membranes

Use [`docs/membranes.md`](../docs/membranes.md) before moving lessons across customers. Transfer primitives, not private context. A valid loop may still be unsafe to reuse if it leaks customer facts, bypasses authority, or turns an impression into doctrine without evidence.

## Installer Generator

Create a customer install input YAML:

```yaml
name: Example Customer
domain_description: Founder-led services business with recurring delivery and owner approval needs.
context_map:
  Operating context: Founder-led services company
  Core work: Deliver client services and preserve operating memory
  Primary cadence: Weekly operating review
  Primary constraint: Owner time and scattered context
  Primary operating risk: Follow-ups and claims drift without evidence
  Executive OS job: Make decisions, risks, owners, and lessons easy to reconstruct
memory_objects:
  - clients
  - projects
  - decisions
  - risks
decisions:
  - Which client commitment needs owner review
  - Which follow-up should lead the next operating cycle
risks:
  - Unreviewed client claims
governance_boundary: Humans approve commitments, external communications, spending, and client-facing claims.
```

Generate a Markdown customer folder:

```bash
anyang-install new templates/customer-install/input-example.yaml --output customers/example-customer
```

Validate a generated folder or the whole customer portfolio:

```bash
anyang-install validate customers/example-customer
anyang-install validate customers
```

Render without placing under `customers/`:

```bash
anyang-install render templates/customer-install/input-example.yaml --format markdown --output tmp/example-markdown
anyang-install render templates/customer-install/input-example.yaml --format obsidian --output tmp/example-vault
anyang-install render templates/customer-install/input-example.yaml --format html --output tmp/example-dashboard
```

Extract membrane-aware pattern candidates:

```bash
anyang-install extract-patterns customers --output customers/pattern-candidates.md
```

Pattern extraction is review-only. It never updates templates or customer folders automatically.

## Transcript Intake

Singularity Science transcript intake is archive-only infrastructure. It normalizes internal transcript files into:

- `customers/singularity-science/archive/innermost-loop/transcripts/`
- `customers/singularity-science/archive/moonshots/transcripts/`

The manifest must live under `customers/singularity-science/archive/`.

Dry run an import:

```bash
anyang-install import-transcripts --manifest customers/singularity-science/archive/transcript-intake-manifest.json --dry-run
```

Run the import:

```bash
anyang-install import-transcripts --manifest customers/singularity-science/archive/transcript-intake-manifest.json
```

Report completeness:

```bash
anyang-install report-transcript-import --manifest customers/singularity-science/archive/transcript-intake-manifest.json
```

Manifest rows require:

- `lane`
- `title`
- `slug`
- `date_captured`
- `source_ref`
- `rights_status`
- `capture_method`
- `local_input_path`

Allowed `rights_status` values:

- `internal-commit-approved`
- `uncertain-review-needed`
- `do-not-commit`

## Verification

```bash
python -m pip install -e .[dev]
python -m pytest
```
