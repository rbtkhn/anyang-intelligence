# Anyang CLI Tools

`anyang-loop` validates and renders Executive OS loop definitions for Anyang Intelligence.

`anyang-project` scaffolds and validates project Executive OS folders from deterministic templates.

It also provides Singularity Science archive intake commands for transcript manifests.

## Governed Operating Ledger

`anyang-ops` is the local-first SQLite control plane for customer work. It stores typed sources, claims, work, evidence, approvals, outcomes, and append-only events, then generates sanitized weekly Markdown or JSON reviews.

Customer commands require an explicit database path:

```powershell
$env:ANYANG_DATA_DIR = 'C:\path\outside\the\repository\grace-gems'
anyang-ops init --tenant grace-gems --name "Grace Gems" --policy-profile governed-media-v1 --retainer-cents 100000 --contractor-budget-cents 50000 --tool-budget-cents 50000
```

Use `--dry-run` on every mutation command to inspect the intended operation. Use `anyang-ops audit --tenant grace-gems` for ledger integrity and `anyang-ops privacy-scan --repo .` before committing. Private evidence bodies and raw customer transcripts remain outside the database; use approved external references and redacted summaries.

Schema v4 keeps epistemic state distinct from operational claim status. Human
operators can record a cause-bearing state change, bind downstream uses, and
clear the resulting review queue:

```bash
anyang-ops dependency add --tenant grace-gems --upstream-claim-id CLAIM_ID --downstream-type publication --downstream-ref LISTING_VERSION --role support --actor REVIEWER
anyang-ops claim transition CLAIM_ID contested --cause-type contradictory-source --cause-ref SOURCE_REF --actor REVIEWER --rationale "Material conflict requires review."
anyang-ops impact list --tenant grace-gems --status open
anyang-ops impact resolve IMPACT_ID --actor REVIEWER --resolution "Publication was reviewed against the changed warrant."
```

Claim transitions are hash-linked and append-only. Propagation creates review
obligations; it never upgrades evidence or silently rewrites downstream state.

Review the live queue, reconstruct one claim, or prepare a read-only impact
packet without changing ledger state:

```bash
anyang-ops epistemic review --tenant grace-gems --format markdown
anyang-ops epistemic explain --tenant grace-gems --claim-id CLAIM_ID --format json
anyang-ops epistemic packet --tenant grace-gems --impact-id IMPACT_ID --format markdown
```

The review queue orders open critical forecast/publication impacts as P0, other
open actionable impacts as P1, and acknowledged or conditional impacts as P2.
Resolved and `no-action` records remain in ledger history but are excluded from
actionable totals. Weekly reviews include the same prioritized model.

### Cadence reconstruction baseline

Record each real cadence event immediately after it completes or stops. Do not backfill simulated successes:

```bash
anyang-ops --db C:\private\anyang-ops.db cadence record \
  --repo-id anyang-intelligence \
  --event-type coffee \
  --scheduled \
  --completion-status completed \
  --state-source git_fallback \
  --no-manual-reconstruction \
  --reconstruction-minutes 0 \
  --evidence-check-passed \
  --privacy-check-passed \
  --authority-check-passed \
  --recorded-by operator
```

Review the latest ten events:

```bash
anyang-ops --db C:\private\anyang-ops.db cadence report --repo-id anyang-intelligence --limit 10
```

The completion rate uses completed events as its denominator. An event enters the numerator only when it required no manual reconstruction and passed evidence, privacy, and authority checks. Partial and abandoned events remain visible but do not inflate the rate. `sample_ready` becomes true after the requested number of events has been recorded.

The ledger is canonical operating state. Generated Markdown is a review view, not a second writable source of truth.

It also provides Learning Core catalog intake commands for governed course-directory assets.

`anyang-coffee` renders the native Anyang Intelligence re-entry brief from repo state, portfolio docs, skills, and git status.

`anyang-dream` renders the native Anyang Intelligence closeout brief from repo state, recent commits, changed paths, and governance surfaces.

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
anyang-project --help
anyang-coffee --help
anyang-dream --help
```

If your shell does not have Python on `PATH`, install or activate a Python 3.10+ environment first.

## Coffee Re-Entry

`anyang-coffee` operationalizes the native [coffee skill](../skills/coffee/SKILL.md). It is read-only: it does not edit, stage, commit, push, publish, or approve anything.

Run it from the repo root:

```bash
anyang-coffee
```

Or point it at a repo path:

```bash
anyang-coffee --repo C:\dev\anyang-intelligence\operating-substrate
```

To consume the latest explicitly recorded dream handoff or emit machine-readable output:

```bash
anyang-coffee --repo . --db C:\private\anyang-ops.db --format json
```

Coffee uses a complete Git snapshot, preserves portfolio subsection context, and follows a fixed priority order: failed verification, recorded handoff, dirty-worktree risk, paid obligation or external blocker, then stale portfolio state. It never writes. Without a configured database it reports a Git-only fallback.

## Dream Closeout

`anyang-dream` operationalizes the native [dream skill](../skills/dream/SKILL.md). It is read-only by default: it does not edit, stage, commit, push, publish, or approve anything.

Run it from the repo root:

```bash
anyang-dream
```

Or point it at a repo path:

```bash
anyang-dream --repo C:\dev\anyang-intelligence\operating-substrate
```

Fast verification is the default. Full verification adds pytest plus project-install and loop validation:

```bash
anyang-dream --repo . --verify full
```

Dream remains read-only unless an external handoff is explicitly recorded:

```bash
anyang-dream --repo . --verify fast --record --db C:\private\anyang-ops.db --recorded-by operator
```

The repo-scoped handoff stores sanitized validation status, touched top-level surfaces, and one inheritance line. It is separate from customer tenants and creates no publication, delivery, spend, customer, or merge authority.

## Loop Schema

YAML:

```yaml
name: weekly-executive-review
description: Weekly operating loop for leadership review.
loop_type: operating
project_lane: shared
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
anyang-loop validate projects/grace-gems/loop-examples
anyang-loop new weekly-review --format markdown --type operating
anyang-loop list customers --include-builtins
anyang-loop simulate canonical-executive-loop
anyang-loop export recursive-improvement-loop --format obsidian
anyang-loop export projects/grace-gems/loop-examples/listing-gate.yaml --format json
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

Use [`docs/membranes.md`](../docs/membranes.md) before moving lessons across projects. Transfer primitives, not private context. A valid loop may still be unsafe to reuse if it leaks customer facts, bypasses authority, or turns an impression into doctrine without evidence.

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

Generate a Markdown project folder:

```bash
anyang-project new templates/project-install/input-example.yaml --output projects/example-customer
```

Validate a generated folder or the whole project portfolio:

```bash
anyang-project validate projects/example-customer
anyang-project validate projects
```

Validate the curated reader-facing analytical interfaces:

```bash
anyang-project validate-interfaces
anyang-project validate-interfaces --manifest analytical-interfaces.yaml
anyang-project validate-interfaces --path templates/operating-review.md
```

The manifest separates governed publication and decision surfaces from provenance-bearing archives and stable identifiers. Objective diagnostics are release gates; accountable human review still judges whether a title or distinction faithfully carries the evidence.

Validate the curated artifact-state contract:

```bash
anyang-project validate-artifacts
anyang-project validate-artifacts --manifest artifact-state.yaml
```

The artifact manifest declares each consequential representation's operation, authority, provenance, permitted write path, and recovery procedure. It may name operator-controlled external paths, but validation reads only the declarations and never private artifact contents. Derived artifacts must name their sources, each domain may have only one canonical authority, and non-public authoritative state may not be tracked in Git.

Validate the phase-authority contract:

```bash
anyang-project validate-agency
anyang-project validate-agency --manifest bounded-agency.yaml
```

`artifact-state.yaml` governs artifact authority, provenance, mutability, and recovery. `bounded-agency.yaml` separately governs what one temporary operating phase may read and write. See [Repository-Anchored Bounded Agency](../docs/repository-anchored-bounded-agency.md) for the composition rules and enforcement boundary.

Manifest governance metadata names an owner, review cadence, next review, expansion rule, and retirement rule. Any exception must name its control, scope, reason, approver, expiration, and review condition; expired exceptions fail validation. Use the quarterly [governance control review](../docs/governance-control-review.md) to keep, narrow, make advisory, or retire controls before adding new validator families.

Render without placing under `projects/`:

```bash
anyang-project render templates/project-install/input-example.yaml --format markdown --output tmp/example-markdown
anyang-project render templates/project-install/input-example.yaml --format obsidian --output tmp/example-vault
anyang-project render templates/project-install/input-example.yaml --format html --output tmp/example-dashboard
```

Extract membrane-aware pattern candidates:

```bash
anyang-project extract-patterns projects --output projects/pattern-candidates.md
```

Pattern extraction is review-only. It never updates templates or project folders automatically.

## Transcript Intake

Singularity Science transcript intake is archive-only infrastructure. It normalizes internal transcript files into:

- `projects/singularity-science/archive/innermost-loop/transcripts/`
- `projects/singularity-science/archive/moonshots/transcripts/`
- `projects/singularity-science/archive/nate-b-jones/transcripts/`
- `projects/singularity-science/archive/external-interviews/transcripts/`

The manifest must live under `projects/singularity-science/archive/`.

Dry run an import:

```bash
anyang-project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json --dry-run
```

Inspect the live phase state without writing:

```bash
anyang-project preflight --phase singularity-transcript-intake --manifest projects/singularity-science/archive/transcript-intake-manifest.json
anyang-project preflight --phase singularity-transcript-intake --manifest projects/singularity-science/archive/transcript-intake-manifest.json --format json
```

Preflight exit `0` means the phase may begin, including when non-blocking warnings or row-level rights holds are visible. Exit `1` means the contract or invocation is blocked. Exit `2` means the request is valid but requires the operator to widen authority. Preflight is read-only and never grants authority; the mutation command reconstructs state again and postflight checks the resulting repository delta.

Run the import:

```bash
anyang-project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json
anyang-project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json --format json
```

Report completeness:

```bash
anyang-project report-transcript-import --manifest projects/singularity-science/archive/transcript-intake-manifest.json
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

Optional manifest fields include:

- `title_date`
- `date_published`
- `speaker`
- `episode_id`
- `notes`

When `title_date` is present, transcript filenames use it ahead of `date_published` so issue-dated source streams like Innermost Loop preserve their visible source date.

## Learning Core Catalog Intake

Learning Core catalog intake is a governed content-directory import surface. It supports:

- public-web-backed main Khan Academy catalog entries
- curated Khan Academy Kids catalog entries

The manifest must live under `projects/learning-core/catalog/`.

Dry run an import:

```bash
anyang-project import-catalog --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml --dry-run
```

Run the import:

```bash
anyang-project import-catalog --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml
```

Report completeness:

```bash
anyang-project report-catalog-import --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml
```

Catalog manifest rows require:

- `stable_id`
- `source_product`
- `title`
- `subject_domain`
- `age_grade_band`
- `content_type`
- `evidence_status`
- `import_method`

Optional catalog fields include:

- `standards_tags`
- `source_url`
- `source_note`
- `operator_notes`

At least one provenance field is required: `source_url` or `source_note`.

## Verification

Validate the curated claim-to-surface nervous system and report its operational
entropy separately from the still-required human outcome measurement:

```bash
anyang-project validate-epistemics
anyang-project epistemic-report
anyang-project epistemic-report --retrieval-success 0.83 --revision-impact-accuracy 0.75
```

Score the fixed twelve-surface human benchmark from a sanitized response file:

```bash
anyang-project epistemic-benchmark score --responses benchmark-responses.yaml --format markdown
```

The version-1 response file requires `reviewed_at`, a pseudonymous
`reviewer_alias`, and one entry for every manifest cohort surface. Each surface
records `elapsed_seconds`, boolean checks for `controlling_claim`,
`state_and_scope`, `upstream_support`, `latest_transition_cause`, and
`downstream_and_next_evidence`, plus `predicted_dependencies`. Scoring is
read-only and emits a reviewed, ready-to-paste aggregate block; it never edits
the manifest.

The governing states, transition rules, and non-upgrade law are defined in
[`docs/epistemic-constitution.md`](../docs/epistemic-constitution.md). The
curated cohort and baseline are declared in [`epistemic-state.yaml`](../epistemic-state.yaml).

```bash
python -m pip install -e .[dev]
python -m pytest
```
