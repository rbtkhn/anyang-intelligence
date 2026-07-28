---
name: executive-audit
description: "Prepare, select, run, reconcile, compare, or follow up on bounded Executive Council repository audits using the Anyang cross-repository collector and Council assurance protocol. Use when the System Engineer asks for metadata-only benchmark discovery, an operability audit, evidence-lineage review, cross-repository benchmark, audit-kernel evaluation, remediation plan, delta review, customer-safe rehearsal, public-safe derivative, or a proposal for one. Treat invocation as a request, never as audit authorization, Council Steward activation, content access, private access, remediation, publication, customer delivery, or external action."
---

# Executive Audit

Use this repo-scoped pilot skill to produce decision-useful repository assurance
without turning mechanical diagnostics into semantic findings or silently
expanding Council authority.

## Controlling status

Procedural revision `v1.4` is a Git-aware execution-surface candidate, not an
executable audit procedure. Revision v1.3.1 qualified the gated Windows
containment and partial-receipt paths, but its archive-only command surface
could not run Git-dependent validators. Revision v1.4 retains safe archive
extraction and attaches detached, depth-one Git metadata containing only the
sealed commit. Native execution remains gated until exact HEAD/tree, clean
index, one-commit history, and absence of remotes, alternates, reflogs, hooks,
and persisted source paths are verified. Preparation failure prevents command
start and seals a bounded partial receipt. Lifecycle IPC and another audit
rerun remain outside this revision. Do not use v1.4 for a new exact-commit
audit until its delta and qualification receipts are accepted and the System
Engineer separately authorizes execution. Do not interpret any revision label
as kernel adoption.

Treat the portable kernel as `pilot — revise`, not adopted. Narrative Systems
and Predictive History are completed technical benchmarks after the
operating-substrate baseline. Require a later System Engineer decision and at
least one unrelated, owner-controlled benchmark before representing the kernel
as commercially validated, generally adopted, or universal.

The skill is procedural memory. It is not:

- a Council role or runtime;
- a standing mandate;
- a Council Steward activation;
- repository, private-system, or external access authority;
- permission to remediate, publish, create issues, open pull requests, spend,
  contact anyone, or transfer protected context.

## Read the authority surface

Before taking audit action, read the current versions of:

1. `operating-substrate/authority-envelope.yaml`
2. `operating-substrate/docs/authority-model.md`
3. `operating-substrate/docs/executive-council-role-contract.md`
4. `operating-substrate/docs/council-steward-role-contract.md`
5. the applicable Council Steward activation, pause, expiration, or revocation
   receipt;
6. any project membrane or target-specific contract named by the request.

Use current controlling sources over examples in this skill. Stop and expose
contradictions; do not silently reconcile them.

## Gate 1: classify authority depth

Classify the request before inspecting a new repository. Treat these as three
separate authority gates:

1. metadata-only candidate discovery;
2. selected-target preflight;
3. exact-commit audit execution.

Approval at one gate never authorizes the next.

### Metadata-only candidate discovery

Proceed only when the System Engineer names the provider or owner boundary,
candidate limit, and decision use. Retrieve only whitelisted repository
metadata: owner, name, visibility, fork/template/archive state, primary
language, size, timestamps, default branch, and current branch-head identity.
Do not inspect descriptions, topics, README files, trees, blobs, releases,
issues, pull requests, or other repository contents.

Use a connected repository metadata surface first. If it is unavailable or
returns no usable result, use the provider's official public metadata API with
the same field whitelist. Do not substitute generic web search or broaden
access. Record the fallback and any authentication or coverage limitation
without recording credentials.

Before shortlisting, test:

- ownership and permission fit;
- non-fork, non-template, and active/archive status;
- independence from prior benchmarks in code, domain, source, and operating
  lineage;
- likely structural richness based only on permitted metadata;
- whether the candidate tests `legacy resilience`, `commercial
  representativeness`, or another declared benchmark purpose.

Metadata supports screening, not outcome proof. Return no more than the
authorized candidate count, disclose uncertainty, and request a separate
selected-target preflight decision.

### Selected-target preflight

Proceed only when the System Engineer names one repository and a bounded
content, command, and time boundary. Use the preflight to:

- resolve target identity and proposed exact commit;
- identify the repository's declared outcome and likely controlling surfaces;
- test whether native commands are available without bypasses;
- propose sampling, exclusions, measurements, output paths, and stop rules;
- classify the benchmark purpose and remaining representativeness limits.

Do not run the full collector, complete semantic review, activate a Council
Steward runtime, or treat a discovered defect as a completed audit finding.
Return an exact audit-execution decision request.

### Proposal only

Use proposal mode whenever the requested gate lacks exact authority. Read only
already authorized Council sources and evidence permitted by an earlier gate.
Prepare:

- objective and decision use;
- candidate repository and commit boundary;
- proposed commands, sampling, exclusions, timebox, and artifacts;
- declared repository outcome to trace end to end;
- measurement method for collector and human review cost;
- required Council Steward activation or source-scope extension;
- risks, cost, and adoption gate;
- one explicit System Engineer decision request.

Do not inspect the target, run the collector, activate a runtime, or persist an
audit packet merely because the skill was invoked.

### Exact-commit audit execution

Proceed only when a current System Engineer receipt or explicit in-session
decision names:

- target repository and exact commit;
- public, repository-visible, or otherwise permitted evidence boundary;
- approved commands and timeout;
- sampling method and exclusions;
- named executor for mechanical collection;
- whether a separately identified Council Steward runtime may review;
- permitted artifact paths and persistence;
- expiration, stop, and revocation conditions;
- actions that remain held.

If any field is missing or materially ambiguous, return to proposal mode.
System Engineer approval does not create client-company authority. Client
approval does not create Anyang system authority.

## Gate 2: seal the target

Before collection:

1. resolve the canonical repository root;
2. record remote identity without embedding credentials;
3. record `HEAD` and `HEAD^{tree}`;
4. capture Git-visible status;
5. confirm the sealed commit matches the authorization;
6. identify controlling surfaces and deterministic sample groups;
7. confirm the receipt output is outside the target repository;
8. map evidence as included-current, included-historical, omitted,
   private, or unavailable;
9. disclose ignored, untracked, submodule, large-file, private, and
   environment coverage gaps.

Do not infer approval from public visibility, repository access, a clean
worktree, prior discussion, or an earlier audit.

Stop on commit mismatch, new private evidence, changed scope, unclear
ownership, credential exposure, or an unapproved command.

## Gate 3: configure mechanical collection

Read [references/config-schema.md](references/config-schema.md) before creating
or reviewing a collector configuration.

Use the canonical implementation:

- `operating-substrate/cli/anyang_loop/cross_repo_audit.py`
- invoke from `operating-substrate` with:

```powershell
.\tools\run.ps1 project cross-repo-audit `
  --repo <target-repository> `
  --config <approved-config.json> `
  --output <receipt-outside-target.json>
```

Do not copy the collector into this skill. Do not weaken its commit check,
disposable-snapshot execution, output minimization, source-hash binding, or
non-overwrite rule.

Declare each command's exact repository-relative `depends_on` controls. Root
cause grouping may use declared dependencies or path-specific command output;
never use generic error text alone.

Use repository-rooted sample globs and declare exclusions where a derived or
mirrored tree could otherwise enter a canonical evidence class. Treat `*` as
one path segment and `**` as recursive. For each decision-critical command,
declare literal-prefix `summary_rules` for the result or total lines the audit
must preserve. Review include, exclusion, final eligible, and selected counts
before accepting sample coverage.

Do not confuse native outcome with collection completion. A command that
terminates with a nonzero exit code produced completed evidence. A timeout,
launch failure, unavailable required sample, or missing required summary makes
collection partial. Never describe a red native validator as an
environment-only or incomplete collection merely because its exit code is
nonzero.

Account for diagnostics at four levels: raw observations, exact-unique
observations, cross-category overlaps, and supported root-cause groups. Keep
the raw evidence intact while preventing one controlling defect from being
reported as many independent findings.

Configuration schema v1 has no per-command environment field. If an approved
native command requires `PYTHONPATH`, locale, or another environment override,
stop and request a separately reviewed collector/schema change. Do not bypass
the schema with shell interpolation, a wrapper command, or an undeclared
ambient environment.

The collector returns objective candidates and execution evidence. It does not
assign semantic severity, establish claim truth, or recommend strategy. Its
disposable execution surface is not an operating-system security sandbox.
Commands see the exact sealed tree plus a detached, depth-one Git repository;
they do not see target remotes, refs, reflogs, hooks, configuration, ignored
files, untracked files, or broader history. Exact-commit authority must include
the sealed commit object's author, committer, message, parent hashes, and
signature metadata because native Git commands can inspect them.

Command output is captured through temporary files so descendant-held pipe
handles cannot block receipt sealing. Commands run in a managed Windows job
and process group or a POSIX session; after a timeout, tree termination is
bounded and reported in `commands[].process_tree`. Windows falls back to
`taskkill /T /F` and then root-process termination when job containment is
unavailable. A failed or uncertain cleanup remains visible as a coverage gap
and does not suppress the partial receipt. Command previews are bounded
head/tail views. Use `execution_snapshot`, capture metadata, complete
minimized-output hashes, summary counts, process-tree status, and collection
status when assessing whether evidence was preserved; do not mistake a preview
for the complete output.

## Gate 4: preserve independent review

Do not impersonate the Council Steward.

When an independently activated Council Steward runtime is authorized:

1. give it the sealed target evidence, authorization boundary, collector
   receipt, and sampling rule;
2. withhold Chief Executive hypotheses until its initial ledger is sealed;
3. require primary-source trace review for semantic findings;
4. disclose runtime identity and possible shared-model-family use;
5. preserve the sealed Steward ledger so Chief Executive interpretation cannot
   overwrite it;
6. record review start/end timestamps or an explicit active-duration estimate,
   and use `Missing` when defensible timing evidence is unavailable.

Minimum independence requires:

- a separate runtime or review instance;
- a separate role contract and prompt;
- primary evidence before executive framing;
- separately attributable output;
- preserved disagreement;
- direct System Engineer escalation;
- no shared mutable draft presented as an independent ledger.

If these conditions cannot be met, label the review `Chief Executive
preflight`, not `Council Steward finding`.

## Gate 5: trace without merging membranes

Review the approved governing contracts and deterministic samples. Trace:

`source -> synthesis or claim -> verification dependency -> decision,
forecast, or publication gate`

Native test success or failure never substitutes for this trace. Review at
least one declared repository outcome end to end. Where multiple inventories,
manifests, indexes, ledgers, or generated views claim the same state, test
controlling-source parity and label derived surfaces.

Keep every observation project-labeled. Cross-project comparison may cover
abstract controls such as:

- receipt completeness;
- approval-to-evidence linkage;
- artifact aging;
- lineage gaps;
- contradiction handling;
- validation coverage;
- recovery and revocation behavior.

Do not merge client facts, private economics, stakeholder messages, supplier
facts, raw creative material, credentials, or protected project context.

Classify evidence distinctly:

- `verified defect`;
- `inferred risk`;
- `inaccessible evidence`;
- `environment-only failure`;
- `collector candidate — not adjudicated`.

Collapse cascading symptoms only when a controlling dependency is evidenced.
Select a deterministic sample of reported candidates for first-pass precision
measurement, including at least one candidate from every material diagnostic
category when available.

## Gate 6: produce the minimum artifact chain

Use three consolidated organization-level artifacts under:

`operating-substrate/docs/analysis/cross-repo-audits/<target>-<date>/`

1. `transaction-record.md`
   - recommendation;
   - System Engineer authority;
   - named execution and evidence;
   - reconciliation;
   - final System Engineer disposition when received.
2. `collector-receipt.json`
   - sealed snapshot;
   - collector identity and configuration;
   - inventory, commands, diagnostics, samples, and coverage gaps;
   - observed target-state evidence.
3. `audit-packet.md`
   - sealed Council Steward ledger when independently produced;
   - Chief Executive implications;
   - cross-repository comparison;
   - value-proof scorecard;
   - open System Engineer decisions.

Do not create one receipt per finding. Do not create an empty Executive
Assistant receipt when no external action occurred. The Executive Assistant
and Artistic Director remain uninvolved unless separately tasked under their
own authority.

Preserve historical or sealed artifacts unchanged. If an old receipt lacks
current lineage or output-minimization fields, disclose the limitation and
require a new receipt for later adoption or customer delivery.

The sealed three-artifact chain ends with audit reconciliation. Any remediation
plan, delta review, or customer-safe rehearsal is a separately authorized,
explicitly linked follow-up artifact; it does not modify or silently extend the
sealed audit chain.

Before sealing, validate every prospective artifact by its explicit path,
including new and untracked files. Do not claim prospective files are clean
from `git diff --check` alone because it does not inspect untracked content.
Normalize accidental whitespace and formatting before sealing. After sealing,
preserve the ledger bytes; document harmless formatting exceptions rather than
rewriting the seal.

### Public-repository egress

Treat persistence inside a public repository, commit, push, publication, and
customer delivery as distinct actions. Before any public-repository commit or
push, classify:

- machine-local paths and usernames;
- runtime identities and internal infrastructure;
- internal deliberation and detailed evidence bodies;
- credentials and private-system indicators;
- client or unrelated portfolio context;
- information that is technically public but not approved for Anyang
  publication.

An internal audit artifact is not automatically public-safe. If egress review
occurs after sealing, either retain the sealed artifact internally or create a
separately linked, explicitly labeled public-safe derivative. Never silently
redact or rewrite the sealed Steward ledger. Public visibility of the target
does not authorize publication of Council artifacts.

## Gate 7: reconcile and stop

The Chief Executive may classify operating implications as:

- `retain`;
- `fix`;
- `narrow`;
- `retire`;
- `investigate`.

Only the System Engineer may accept, revise, hold, or reject material findings
for Anyang system action. A client CEO decides applicable client-company
actions. Findings do not authorize remediation.

At reconciliation, record:

- System Engineer disposition for every material finding;
- the expiration, revocation, or continuation state of any temporary Council
  Steward source extension;
- proposal/preflight, collector, Steward, Chief Executive, and System Engineer
  review timestamps or active-duration estimates, using `Missing` rather than
  inference;
- raw, exact-unique, overlap, root-cause-group, and adjudicated-finding counts;
- reviewed-candidate precision and coverage against the declared outcome.

Use this five-stage timing ledger in the transaction record:

| Stage | Started | Ended | Active duration | Evidence |
| --- | --- | --- | --- | --- |
| Proposal/preflight | value or `Missing` | value or `Missing` | value or `Missing` | source |
| Collector | value or `Missing` | value or `Missing` | value or `Missing` | source |
| Council Steward | value or `Missing` | value or `Missing` | value or `Missing` | source |
| Chief Executive | value or `Missing` | value or `Missing` | value or `Missing` | source |
| System Engineer | value or `Missing` | value or `Missing` | value or `Missing` | source |

Do not derive elapsed or active time without defensible timestamps.

End with:

- audit state and sealed commit;
- what evidence was and was not reviewed;
- material findings by evidence class;
- independence disclosure;
- target mutation observation;
- validation and coverage gaps;
- artifact paths;
- actions still held;
- explicit System Engineer choices.

## Post-audit follow-up

Treat every follow-up as a new authority gate.

- **Remediation plan:** may translate accepted findings into bounded proposed
  changes, but does not authorize target writes.
- **Delta review:** requires an exact before/after boundary and tests only the
  authorized change plus affected controls; it does not reopen the sealed
  ledger.
- **Customer-safe rehearsal:** is an internal redaction and usefulness test.
  Preserve finding meaning and evidence class while removing internal paths,
  runtime identifiers, credentials, and unrelated portfolio context. It does
  not authorize customer delivery, commercial claims, or publication.
- **Public-safe derivative:** requires a named source artifact, explicit egress
  review, preserved lineage, and separate publication authority. It is not a
  replacement for the sealed internal artifact.

Append later System Engineer dispositions with attribution and time. Never
rewrite a sealed Steward finding to match the disposition.

## Validation

For changes inside `operating-substrate`, run only its canonical validator:

```powershell
.\tools\validate.ps1
```

Also verify:

- every prospective new or untracked artifact was checked directly before
  persistence or sealing;
- the target Git-visible state is unchanged;
- collector output is outside the target;
- the receipt identifies collector source and effective configuration;
- the declared repository outcome has at least one end-to-end trace;
- duplicated state surfaces have an explicit parity result;
- diagnostic and timing accounting uses the required categories without
  invented values;
- privacy validation passes;
- public-repository egress is classified before any commit or push;
- the sealed Steward ledger remains byte-preserved after executive
  interpretation;
- no external action or protected-context transfer occurred.

## Hard stops

Stop and escalate rather than improvise when:

- audit authority or Steward activation is missing;
- the target commit or evidence boundary changes;
- a command or output path is outside approved scope;
- private or client evidence appears without exact authority;
- evidence minimization cannot protect sensitive output;
- independent review is compromised;
- a native command requires undeclared environment manipulation;
- diagnostic deduplication would discard raw evidence or lacks a supported
  dependency;
- a public-repository commit or push is requested without a completed egress
  classification and explicit authority;
- remediation, publication, outreach, spending, or client adoption is
  requested without separate approval;
- the collector or skill is being treated as self-authorizing.
