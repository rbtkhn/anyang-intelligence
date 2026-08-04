# Anyang CLI Tools

The council-loop command validates and renders Executive Council loop definitions for Anyang Intelligence. The legacy anyang-loop command remains supported.

The council-project command scaffolds and validates Executive Council project folders from deterministic templates. The legacy anyang-project command remains supported.

It also provides Singularity Science archive intake commands for transcript manifests.

## Governed Operating Ledger

`anyang-ops` is the local-first SQLite control plane for customer work. It stores typed sources, claims, work, evidence, approvals, outcomes, and append-only events, then generates sanitized weekly Markdown or JSON reviews.

Repository workflows use `tools/run.ps1` (or `python3 tools/run_repo.py` on macOS/Linux). Customer commands require an explicit database path:

```powershell
$env:ANYANG_DATA_DIR = 'C:\path\outside\the\repository\grace-gems'
.\tools\run.ps1 ops init --tenant grace-gems --name "Grace Gems" --policy-profile governed-media-v1 --retainer-cents 100000 --contractor-budget-cents 50000 --tool-budget-cents 50000
```

Use `--dry-run` on every mutation command to inspect the intended operation. Use `.\tools\run.ps1 ops audit --tenant grace-gems` for ledger integrity and `.\tools\run.ps1 ops privacy-scan --repo .` before committing. Private evidence bodies and raw customer transcripts remain outside the database; use approved external references and redacted summaries.

Business intake uses a separate governed control path. The conversational `$business-intake` skill may prepare a sanitized manifest, but only these explicit commands can change tenant state:

```powershell
.\tools\run.ps1 ops authority grant --tenant grace-gems --actor-id OWNER_ID --scope business_context --dry-run
.\tools\run.ps1 ops intake bootstrap --tenant grace-gems --manifest EXACT_EXISTING_CONTEXT_MANIFEST --actor-id OWNER_ID --subject-hash EXACT_HASH --approval-receipt-ref EXACT_APPROVAL_RECEIPT --persistence-ref EXACT_PERSISTENCE_RECEIPT --dry-run
.\tools\run.ps1 ops intake propose --tenant grace-gems --manifest projects/grace-gems/intake-control-manifest-2026-07-17.yaml --dry-run
.\tools\run.ps1 ops intake decide --tenant grace-gems --version CONTEXT_VERSION --actor-id OWNER_ID --decision approved --subject-hash EXACT_HASH --dry-run
.\tools\run.ps1 ops intake persist --tenant grace-gems --version CONTEXT_VERSION --actor-id OWNER_ID --subject-hash EXACT_HASH --external-ref tenant-private://approved/context --dry-run
.\tools\run.ps1 ops intake authorize-review --tenant grace-gems --version CONTEXT_VERSION --actor-id OWNER_ID --decision approved --subject-hash EXACT_HASH --dry-run
.\tools\run.ps1 ops intake status --tenant grace-gems --format markdown
```

The one-time `bootstrap` path requires an empty context ledger, a non-`hold` exact manifest, the matching manifest hash, current `business_context` authority, and separate pre-existing approval and persistence receipt references. The status receipt names the effective context, active proposal, evidence classes, separate owner/persistence/review decisions, and one next action. A `hold` manifest cannot be approved; resolve its gates and submit a new exact version instead.

Schema v8 retains the separation between epistemic state and operational claim status. Human
operators can record a cause-bearing state change, bind downstream uses, and
clear the resulting review queue:

```bash
.\tools\run.ps1 ops dependency add --tenant grace-gems --upstream-claim-id CLAIM_ID --downstream-type publication --downstream-ref LISTING_VERSION --role support --actor REVIEWER
.\tools\run.ps1 ops claim transition CLAIM_ID contested --cause-type contradictory-source --cause-ref SOURCE_REF --actor REVIEWER --rationale "Material conflict requires review."
.\tools\run.ps1 ops impact list --tenant grace-gems --status open
.\tools\run.ps1 ops impact resolve IMPACT_ID --actor REVIEWER --resolution "Publication was reviewed against the changed warrant."
```

Claim transitions are hash-linked and append-only. Propagation creates review
obligations; it never upgrades evidence or silently rewrites downstream state.

Review the live queue, reconstruct one claim, or prepare a read-only impact
packet without changing ledger state:

```bash
.\tools\run.ps1 ops epistemic review --tenant grace-gems --format markdown
.\tools\run.ps1 ops epistemic explain --tenant grace-gems --claim-id CLAIM_ID --format json
.\tools\run.ps1 ops epistemic packet --tenant grace-gems --impact-id IMPACT_ID --format markdown
```

The review queue orders open critical forecast/publication impacts as P0, other
open actionable impacts as P1, and acknowledged or conditional impacts as P2.
Resolved and `no-action` records remain in ledger history but are excluded from
actionable totals. Weekly reviews include the same prioritized model.

### Executive Council ledger workroom

Schema v7 also provides an internal, local-first Council workroom. A transaction
is immutable metadata plus one append-only, per-transaction hash chain. Its
current state and A–D view are derived from recommendation, authority,
execution/evidence, reconciliation, and metric events; rendered Markdown is
never a second writable record.

Use YAML packets for transaction and event bodies:

```powershell
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council create --tenant anyang-internal --packet transaction.yaml --dry-run
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council record --transaction-id TX_ID --event recommendation_recorded --packet event.yaml --dry-run
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council show TX_ID --format markdown
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council inbox --tenant anyang-internal --as-of 2026-07-28T12:00:00Z --format json
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council pilot-review --tenant anyang-internal --as-of 2026-08-21T23:59:59Z --format markdown
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council verify TX_ID
```

Initialize and reconstruct the bounded five-case pilot in one idempotent
operation:

```powershell
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council backfill-friction-pilot `
  --tenant anyang-internal `
  --cohort docs/executive-council-friction-pilot-cohort-2026-07-24.md `
  --tracker docs/executive-council-pilot-tracker.md `
  --dry-run
```

Remove `--dry-run` only after reviewing the plan. The backfill creates the
sanitized internal tenant and five Council actors when absent, preserves every
source section and measure in event lineage, and retains unavailable actor,
time, and metric values as `Missing`. Repeating an identical backfill is a
no-op; a changed transaction or event under the same stable identity fails.

For live records, event packets require a known tenant actor. Approved Class 1
or Class 2 work requires an exact Anyang authority reference; Class 3 also
requires a separate client-authority reference. Approval binds to the current
recommendation subject hash, so a later recommendation invalidates it.
Completion requires named execution and returned evidence. Private evidence
bodies are prohibited in `anyang-internal`; store approved references instead.
An approval event documents authority but never grants tool access, permission,
or execution capability.

#### Dual-surface decision envelope pilot

The schema-v8 ledger can derive a deterministic
`council-decision-envelope/v1` machine packet and a matching human receipt.
Generation, offline verification, ledger comparison, and pilot review are
read-only and do not migrate SQLite. The rendering commands write an artifact
only when given an explicit `--output` path; private outputs stay outside Git:

```powershell
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council envelope TX_ID --as-of 2026-08-04T18:00:00Z --format json
.\tools\run.ps1 ops council envelope-verify --packet C:\private\envelope.json
.\tools\run.ps1 ops council envelope-verify --packet C:\private\envelope.json --receipt C:\private\receipt.md
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council envelope-compare --packet C:\private\envelope.json
.\tools\run.ps1 ops --db C:\private\anyang-ops.db council envelope-pilot-review `
  --tenant anyang-internal `
  --from 2026-08-05T00:00:00Z `
  --as-of 2026-09-04T00:00:00Z `
  --format markdown
```

The human receipt digest covers its exact UTF-8/LF body. Markdown adds a
self-referential verification trailer after that body; the trailer is not part
of the digest. Hashes establish packet consistency, not factual truth or
authorship. Use `envelope-compare` to establish parity with the current
canonical ledger.

New internal Class 1-2 transactions may use
`decision-envelope-v1-shadow` or `decision-envelope-v1-gated` as their
immutable `pilot_category`. Invoked execution in gated mode additionally
requires `envelope_projection_hash`, `human_receipt_digest`, and
`envelope_as_of` in the execution payload. The service recomputes the current
envelope before appending execution, so any intervening recommendation,
authority, or event change invalidates the binding. Class 0 remains optional;
Class 3, customer, and external work are excluded.
The service also rejects creation of a gated transaction before day 11 or
until the measured five-case shadow gate passes.

The full measurement protocol, stable metric names, phase gate, disposition
rules, and authority boundary are defined in
[`docs/dual-surface-decision-envelope-v1.md`](../docs/dual-surface-decision-envelope-v1.md).

### Learn-from-choices manual audit compatibility

Learn From Choices Lite does not call these interfaces for ordinary letter
navigation. The schema-v8 ledger remains available as an explicitly invoked,
advanced audit surface for existing receipts and deliberate manual workflows.
No selection or outcome is persisted automatically.

Schema v8 adds immutable selected-choice prompts and append-only, hash-chained
choice events. An unselected response footer creates no record. An ordinary
selected letter also creates no record under Lite defaults. A manually created
receipt records navigation and grants no execution authority.

Configure the external ledger pointer explicitly when continuity should survive
new shells and agent sessions. The command initializes only the sanitized
`anyang-internal / anyang-intelligence / repository` choice scope and writes a
versioned user-local pointer outside Git. Always inspect the dry run first:

```powershell
.\tools\run.ps1 ops choice configure --data-dir C:\private\anyang-intelligence --dry-run
.\tools\run.ps1 ops choice configure --data-dir C:\private\anyang-intelligence
.\tools\run.ps1 ops choice status --format json
```

Resolution precedence is explicit `--db`, `ANYANG_DATA_DIR`, then user-local
configuration. `choice status` and Coffee inspect SQLite read-only and never
migrate it. Clear only the pointerâ€”never the ledgerâ€”with `choice configure
--clear --dry-run` followed by the reviewed command without `--dry-run`.

```powershell
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice context --tenant anyang-internal --workspace anyang-intelligence --lane repository --kind next-action --format json
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice select --tenant anyang-internal --packet selection.yaml --dry-run
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice outcome CHOICE_ID --packet outcome.yaml --dry-run
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice review --tenant anyang-internal --workspace anyang-intelligence --as-of 2026-07-29T12:00:00Z
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice show CHOICE_ID --tenant anyang-internal --workspace anyang-intelligence --lane repository --format json
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice verify CHOICE_ID --tenant anyang-internal --workspace anyang-intelligence --lane repository
```

Direct `show` and `verify` reads require the expected tenant, workspace, and
lane. A mismatch returns a generic not-found error without disclosing the
record's actual scope. Verification checks both the hash chain and semantic
identity: immutable options and recommendation, exactly one initial selection,
selection role and no-authority binding, canonical event payloads, and
same-scope acyclic choice supersession.

Choice continuity classification is optional for legacy packet compatibility.
When supplied, it is all-or-nothing:

```yaml
options:
  - key: recommended
    role: recommended
    label: Push the authorized repository change
    description: Publish the already-authorized commit.
    classification_version: LFC-CONTINUITY-v0.2
    pattern_key: execute-bounded
    action_boundary: external-action
    comparability_key: repository-authorized-push-v1
```

SQLite remains schema v8; choice projections and contexts are schema v2.
Patterns and option-key outcome counts are diagnostic only. Comparability
cohorts form only through a registered explicit policy. The initial
`repository-authorized-push-v1` policy is diagnostic-only and cannot reorder
recommendations. Action boundaries expose permission seams and always retain
`authority_effect: none`.

A `corrected` event may append one `classification_correction` targeting
`pattern_key`, `action_boundary`, or `comparability_key`. Its `prior_value`
must match the effective value at that sequence; it never rewrites the
original option. Classification-only correction does not change operational
state and cannot be combined with outcome replacement.

Selection dry runs validate structure, classification, privacy, and policy
scope while deferring actor and database idempotency checks. Outcome dry runs
validate correction shape while deferring choice-specific actor, prior-value,
and idempotency checks. See
`docs/learn-from-choices-continuity-contract-v0.2.md` for the versioned
contract.

Recommendation guidance uses observed usefulness, burden, momentum, discovery,
and outcomes. Selection frequency is explicitly excluded. One or two outcomes
remain thin evidence; at least three comparable outcomes with two consistent
results and no material contradiction may influence the recommended branch.
Authority or membrane incidents surface immediately when the manual audit
surface is invoked. Ordinary navigation is independent of ledger availability,
and only operator-approved `RL-*` learning may enter Git.

When explicitly invoked after five resolved, non-superseded selections,
`choice review` renders a
stable initial-cohort scorecard. It reports lower cognitive load, advanced
momentum, new-useful-path discovery, result distribution, optional rework, and
authority or membrane incidents. Missing dimensions stay out of denominators.
The assessment is `continue`, `adjust`, `extend-to-ten`, or `hold`; an authority
or membrane incident always produces `hold`. This descriptive checkpoint never
uses selection frequency and does not replace the separate comparable-outcome
threshold for changing recommendations.

### Cadence reconstruction baseline

Record each real cadence event immediately after it completes or stops. Do not backfill simulated successes:

```bash
.\tools\run.ps1 ops --db C:\private\anyang-ops.db cadence record \
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
.\tools\run.ps1 ops --db C:\private\anyang-ops.db cadence report --repo-id anyang-intelligence --limit 10
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

Installed entry points remain available to package users:

```bash
anyang-loop --help
anyang-project --help
anyang-coffee --help
anyang-dream --help
```

If your shell does not have Python on `PATH`, install or activate a Python 3.10+ environment first.

For repository validation, no preinstalled development extras are required. From PowerShell use:

```powershell
.\tools\validate.ps1
```

The launcher locates Python, bootstraps dependencies declared in `pyproject.toml` into an external user cache, and runs pytest plus every CI validator and the privacy scan. On macOS or Linux use `python3 tools/validate_repo.py`.

Run an individual repo command through the same environment without installing entry points:

```powershell
.\tools\run.ps1 project validate projects
.\tools\run.ps1 loop validate projects
.\tools\run.ps1 ops privacy-scan --repo .
```

On macOS or Linux use `python3 tools/run_repo.py <surface> ...`. Supported surfaces are `project`, `loop`, `ops`, `coffee`, and `dream`.

## Coffee Re-Entry

`anyang-coffee` operationalizes the native [coffee skill](../skills/coffee/SKILL.md). It is read-only: it does not edit, stage, commit, push, publish, or approve anything.

Run it from the repo root through the canonical runtime:

```bash
.\tools\run.ps1 coffee
```

Or point it at a repo path:

```bash
.\tools\run.ps1 coffee --repo .
```

To consume the latest explicitly recorded dream handoff or emit machine-readable output:

```bash
.\tools\run.ps1 coffee --repo . --db C:\private\anyang-ops.db --format json
```

Coffee uses a complete Git snapshot, preserves portfolio subsection context, and follows a fixed priority order: failed verification, recorded handoff, dirty-worktree risk, paid obligation or external blocker, then stale portfolio state. It never writes. Without a configured database it reports a Git-only fallback.

## Dream Closeout

`anyang-dream` operationalizes the native [dream skill](../skills/dream/SKILL.md). It is read-only by default: it does not edit, stage, commit, push, publish, or approve anything.

Run it from the repo root through the canonical runtime:

```bash
.\tools\run.ps1 dream
```

Or point it at a repo path:

```bash
.\tools\run.ps1 dream --repo .
```

Fast verification is the default. Full verification adds pytest plus project-install and loop validation:

```bash
.\tools\run.ps1 dream --repo . --verify full
```

Dream remains read-only unless an external handoff is explicitly recorded:

```bash
.\tools\run.ps1 dream --repo . --verify fast --record --db C:\private\anyang-ops.db --recorded-by operator
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

```powershell
.\tools\run.ps1 loop validate projects/grace-gems/loop-examples
.\tools\run.ps1 loop new weekly-review --format markdown --type operating
.\tools\run.ps1 loop list customers --include-builtins
.\tools\run.ps1 loop simulate canonical-executive-loop
.\tools\run.ps1 loop export recursive-improvement-loop --format obsidian
.\tools\run.ps1 loop export projects/grace-gems/loop-examples/listing-gate.yaml --format json
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

```powershell
.\tools\run.ps1 project new templates/project-install/input-example.yaml --output projects/example-customer
```

Validate a generated folder or the whole project portfolio:

```powershell
.\tools\run.ps1 project validate projects/example-customer
.\tools\run.ps1 project validate projects
```

Validate the curated reader-facing analytical interfaces:

```powershell
.\tools\run.ps1 project validate-interfaces
.\tools\run.ps1 project validate-interfaces --manifest analytical-interfaces.yaml
.\tools\run.ps1 project validate-interfaces --path templates/operating-review.md
```

Validate a bounded automation value-proof packet before treating its result as evidence:

```powershell
.\tools\run.ps1 project validate-value-proof --path templates/automation-value-proof.md
```

The template is intentionally incomplete and should fail until a real pilot packet is populated. The validator checks objective structure, quantitative-evidence prerequisites, approval boundaries, exception plans, and repo privacy rules; it does not decide whether an automation is valuable or ready to deploy.

The manifest separates governed publication and decision surfaces from provenance-bearing archives and stable identifiers. Objective diagnostics are release gates; accountable human review still judges whether a title or distinction faithfully carries the evidence.

Validate the curated artifact-state contract:

```powershell
.\tools\run.ps1 project validate-artifacts
.\tools\run.ps1 project validate-artifacts --manifest artifact-state.yaml
```

The artifact manifest declares each consequential representation's operation, authority, provenance, permitted write path, and recovery procedure. It may name operator-controlled external paths, but validation reads only the declarations and never private artifact contents. Derived artifacts must name their sources, each domain may have only one canonical authority, and non-public authoritative state may not be tracked in Git.

Validate the phase-authority contract:

```powershell
.\tools\run.ps1 project validate-agency
.\tools\run.ps1 project validate-agency --manifest bounded-agency.yaml
```

`artifact-state.yaml` governs artifact authority, provenance, mutability, and recovery. `bounded-agency.yaml` separately governs what one temporary operating phase may read and write. See [Repository-Anchored Bounded Agency](../docs/repository-anchored-bounded-agency.md) for the composition rules and enforcement boundary.

Manifest governance metadata names an owner, review cadence, next review, expansion rule, and retirement rule. Any exception must name its control, scope, reason, approver, expiration, and review condition; expired exceptions fail validation. Use the quarterly [governance control review](../docs/governance-control-review.md) to keep, narrow, make advisory, or retire controls before adding new validator families.

Render without placing under `projects/`:

```powershell
.\tools\run.ps1 project render templates/project-install/input-example.yaml --format markdown --output tmp/example-markdown
.\tools\run.ps1 project render templates/project-install/input-example.yaml --format obsidian --output tmp/example-vault
.\tools\run.ps1 project render templates/project-install/input-example.yaml --format html --output tmp/example-dashboard
```

Extract membrane-aware pattern candidates:

```powershell
.\tools\run.ps1 project extract-patterns projects --output projects/pattern-candidates.md
```

Pattern extraction is review-only. It never updates templates or project folders automatically.

## Elicitation Contradiction Preflight

Compare normalized request assertions with explicitly supplied controlling
facts before asking a consequential clarification question:

```powershell
.\tools\run.ps1 project contradiction-check --packet contradiction-packet.yaml --format markdown
.\tools\run.ps1 project contradiction-check --packet contradiction-packet.yaml --format json
```

Packet schema v1 requires `request_ref`, `scope`, `consequence_level`, `as_of`,
one or more `request_assertions`, and a `controlling_facts` list. Assertions and
facts use normalized lowercase field keys and scalar string, number, or boolean
values. Each fact names its authority role, provenance, as-of time, and optional
freshness deadline. Set `provisional: true` only for an ordinary request
assertion that may safely continue without current control.

```yaml
schema_version: 1
request_ref: thread:current-request
scope: repository
consequence_level: consequential
as_of: 2026-07-30T18:00:00Z
request_assertions:
  - id: requested-branch
    field: git.branch
    value: main
    scope: repository
    source_ref: thread:current-request#branch
    provisional: false
controlling_facts:
  - id: current-branch
    field: git.branch
    value: main
    scope: repository
    authority_role: canonical
    source_ref: repo:git-preflight
    as_of: 2026-07-30T17:59:00Z
    fresh_until: 2026-07-30T18:05:00Z
```

The command performs exact field, scope, type, value, authority-role, and
freshness comparisons. It does not search prose, open SQLite, write files,
transition claims, or decide which source governs. Markdown and JSON output do
not echo compared values. Exit `0` means `continue` or
`continue-provisional`; exit `1` means the packet is invalid or its disposition
is `clarify` or `hold`. Every result has `authority_effect: none` and is
inspectable guidance, not a reusable capability token.

### Portable kernel

The comparison engine is isolated in
`cli/anyang_loop/contradiction_kernel/`. It has no Anyang privacy import and
accepts an explicit `ContradictionPolicy` plus a host-supplied privacy scanner.
The policy names the three consequence semantics, allowed authority roles,
controlling roles, and packet bounds.

`cli/anyang_loop/contradiction_policy.py` is the Anyang host adapter.
`cli/anyang_loop/contradiction_preflight.py` is the compatibility facade used
by the existing CLI and callers. A repository port should copy the kernel,
define its own host policy and privacy scanner, and keep authority declarations
outside the kernel. The kernel compares supplied facts; it does not discover
or rank controlling sources.

## Transcript Intake

Singularity Science transcript intake is archive-only infrastructure. It normalizes internal transcript files into:

- `projects/singularity-science/archive/innermost-loop/transcripts/`
- `projects/singularity-science/archive/moonshots/transcripts/`
- `projects/singularity-science/archive/nate-b-jones/transcripts/`
- `projects/singularity-science/archive/external-interviews/transcripts/`

The manifest must live under `projects/singularity-science/archive/`.

Dry run an import:

```powershell
.\tools\run.ps1 project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json --dry-run
```

Inspect the live phase state without writing:

```powershell
.\tools\run.ps1 project preflight --phase singularity-transcript-intake --manifest projects/singularity-science/archive/transcript-intake-manifest.json
.\tools\run.ps1 project preflight --phase singularity-transcript-intake --manifest projects/singularity-science/archive/transcript-intake-manifest.json --format json
```

Preflight exit `0` means the phase may begin, including when non-blocking warnings or row-level rights holds are visible. Exit `1` means the contract or invocation is blocked. Exit `2` means the request is valid but requires the operator to widen authority. Preflight is read-only and never grants authority; the mutation command reconstructs state again and postflight checks the resulting repository delta.

Run the import:

```powershell
.\tools\run.ps1 project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json
.\tools\run.ps1 project import-transcripts --manifest projects/singularity-science/archive/transcript-intake-manifest.json --format json
```

Report completeness:

```powershell
.\tools\run.ps1 project report-transcript-import --manifest projects/singularity-science/archive/transcript-intake-manifest.json
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

```powershell
.\tools\run.ps1 project import-catalog --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml --dry-run
```

Run the import:

```powershell
.\tools\run.ps1 project import-catalog --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml
```

Report completeness:

```powershell
.\tools\run.ps1 project report-catalog-import --manifest projects/learning-core/catalog/khan-catalog-manifest.sample.yaml
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

```powershell
.\tools\run.ps1 project validate-epistemics
.\tools\run.ps1 project epistemic-report
.\tools\run.ps1 project epistemic-report --retrieval-success 0.83 --revision-impact-accuracy 0.75
```

CI runs `epistemic-report` as a visible readiness check. Missing human
measurements keep composite acceptance pending but do not fail the build;
objective critical gaps still return a failing status.

Score the fixed twelve-surface human benchmark from a sanitized response file:

```powershell
.\tools\run.ps1 project epistemic-benchmark score --responses benchmark-responses.yaml --format markdown
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

For repository testing and validation, run `.\tools\validate.ps1` on Windows or `python3 tools/validate_repo.py` on macOS or Linux.
