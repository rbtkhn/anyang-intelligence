---
name: executive-council-audit
description: "Prepare, run, reconcile, or compare bounded Executive Council repository audits using the Anyang cross-repository collector and Council assurance protocol. Use when the System Engineer asks for an operability audit, evidence-lineage review, cross-repository benchmark, audit-kernel evaluation, or a proposal for one. Treat invocation as a request, never as audit authorization, Council Steward activation, private access, remediation, publication, or external action."
---

# Executive Council Audit

Use this repo-scoped pilot skill to produce decision-useful repository assurance
without turning mechanical diagnostics into semantic findings or silently
expanding Council authority.

## Controlling status

Treat the portable kernel as `pilot — revise`, not adopted. Narrative Systems
is the second benchmark. Require a later System Engineer decision and at least
one materially different benchmark before representing the kernel as adopted.

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

## Gate 1: classify the request

Classify the request before inspecting a new repository.

### Proposal only

Use proposal mode when exact audit authority is absent. Read only already
authorized local Council sources. Prepare:

- objective and decision use;
- candidate repository and commit boundary;
- proposed commands, sampling, exclusions, timebox, and artifacts;
- required Council Steward activation or source-scope extension;
- risks, cost, and adoption gate;
- one explicit System Engineer decision request.

Do not inspect the target, run the collector, activate a runtime, or persist an
audit packet merely because the skill was invoked.

### Authorized execution

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
8. disclose ignored, untracked, submodule, large-file, private, and
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

The collector returns objective candidates and execution evidence. It does not
assign semantic severity, establish claim truth, or recommend strategy. Its
disposable execution surface is not an operating-system security sandbox.

## Gate 4: preserve independent review

Do not impersonate the Council Steward.

When an independently activated Council Steward runtime is authorized:

1. give it the sealed target evidence, authorization boundary, collector
   receipt, and sampling rule;
2. withhold Chief Executive hypotheses until its initial ledger is sealed;
3. require primary-source trace review for semantic findings;
4. disclose runtime identity and possible shared-model-family use;
5. preserve the sealed Steward ledger so Chief Executive interpretation cannot
   overwrite it.

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

## Validation

For changes inside `operating-substrate`, run only its canonical validator:

```powershell
.\tools\validate.ps1
```

Also verify:

- the target Git-visible state is unchanged;
- collector output is outside the target;
- the receipt identifies collector source and effective configuration;
- privacy validation passes;
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
- remediation, publication, outreach, spending, or client adoption is
  requested without separate approval;
- the collector or skill is being treated as self-authorizing.
