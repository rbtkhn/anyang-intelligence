# Dual-Surface Decision Envelope v1

Status: `legacy verification compatibility; generation superseded by v1.1`

New envelopes use `council-decision-envelope/v1.1`. Version 1 packets remain
accepted by offline verification and ledger comparison, but the original v1
pilot activation and gated-progression design is not operational. See
[`dual-surface-decision-envelope-v1.1.md`](dual-surface-decision-envelope-v1.1.md).

Authority owner: System Engineer  
Measurement owner: Council Steward

## Purpose

The envelope provides two deterministic views of one canonical Executive
Council transaction:

```text
append-only Council history -> machine envelope -> human receipt
```

The private schema-v8 SQLite ledger remains canonical operating state. The
machine envelope and human receipt are derived, transient views. Neither view
grants authority, invokes an executor, changes a transaction, or acts as a
reusable capability token.

## Contract

`council-decision-envelope/v1` contains the complete schema-v1 Council
projection, its canonical SHA-256 digest, the event-chain head, an explicit
RFC3339 `as_of`, authority freshness, membrane classification, attention
flags, critical human-field coverage, and the exact human receipt body.

JSON is canonicalized with sorted keys, compact separators, UTF-8, and no
ASCII escaping. The payload digest and projection hash cover the complete
projection. The human receipt digest covers the exact UTF-8 receipt body with
LF line endings. The Markdown renderer appends a verification trailer after
the body; that self-referential trailer is intentionally outside the receipt
digest.

The human receipt always exposes these fields, preserving `Missing` rather
than inventing facts:

- what changed and what judgment is required;
- recommendation, expected outcome, uncertainty, and evidence references;
- authority disposition, exact subject binding, scope, expiration, and
  exclusions;
- named executor, execution/evidence state, reconciliation, and outcome;
- required approval or evidence, next permissible action, and stop condition.

Hashes prove internal consistency, not truth or authorship. Offline
verification detects alteration relative to the packet. Ledger comparison is
required to establish parity with current canonical state.

## Interfaces

```text
anyang-ops council envelope TRANSACTION_ID --as-of TIME --format json|markdown
anyang-ops council envelope-verify --packet ENVELOPE.json
anyang-ops council envelope-verify --packet ENVELOPE.json --receipt RECEIPT.md
anyang-ops --db DB council envelope-compare --packet ENVELOPE.json
anyang-ops --db DB council envelope-pilot-review --tenant anyang-internal --from TIME --as-of TIME --format json|markdown
```

Envelope generation, verification, comparison, and pilot review are
read-only with respect to operating state. They do not migrate SQLite;
`envelope` and `envelope-pilot-review` write a file only when the operator
explicitly supplies the standard `--output` path, which must remain outside
the repository for private operating data. Unknown
contracts, invalid hashes, receipt/projection divergence, stale or expired
authority, missing critical human fields, and cross-tenant comparisons return
`Hold` and exit `1`.

## Historical gated-execution design

The remainder of this document records the original v1 design. It is not an
operating instruction: v1.1 fails closed on gated enrollment and execution.

New pilot transactions use one immutable category:

- `decision-envelope-v1-shadow`
- `decision-envelope-v1-gated`

Both categories are limited to `anyang-internal` Class 1 or Class 2 work.
Class 0 remains optional. Class 3, customer-lane, and external transactions
remain outside the pilot.

Shadow transactions retain existing execution behavior. An invoked execution
for a gated transaction additionally supplies:

```yaml
payload:
  envelope_projection_hash: SHA256
  human_receipt_digest: SHA256
  envelope_as_of: RFC3339_TIME
```

The service reconstructs the envelope before appending execution and rejects
missing, stale, or mismatched bindings. Existing approval, actor, evidence,
privacy, tenant, and subject-hash rules remain controlling.

## Thirty-day protocol

The pilot begins at the explicit activation timestamp supplied as `--from`;
the first shadow transaction must use that same `created_at` value so later
reviews can reconstruct the window without a second state store.
Historical friction cases may test rendering, tamper detection, privacy, and
reconstruction, but are excluded from ROI.

Days 1-10 are shadow-only. Each live Class 1-2 transaction receives two
independent timed reconstructions. One Council reviewer uses the existing
projection and one uses the human receipt; reviewer assignments alternate by
transaction ID parity. Before seeing the other surface, each reviewer answers:

1. What changed?
2. What judgment is required?
3. What authority exists and what remains excluded?
4. What evidence is missing?
5. What is the next permissible action or stop condition?

The day-10 gate requires at least five live transactions, complete critical
field parity and envelope/chain verification, zero unauthorized progression,
zero authority or membrane incidents, zero incorrect authority
representations, and median incremental review burden no greater than two
minutes. A failed gate leaves the remaining pilot in shadow mode.
Creation of a `decision-envelope-v1-gated` transaction reconstructs this gate
from the earliest shadow transaction through the proposed gated transaction's
`created_at`; the service rejects gated enrollment before day 11 or while any
gate check remains held.

The Council Steward records observations through existing append-only
`metric_recorded` events using these exact names:

- `baseline_reconstruction_minutes`
- `envelope_reconstruction_minutes`
- `baseline_reconstruction_correctness`
- `envelope_reconstruction_correctness`
- `envelope_generation_seconds`
- `incremental_review_minutes`
- `critical_field_parity`
- `receipt_ledger_mismatch`
- `correction_or_rework_minutes`
- `authority_or_membrane_incident`

Correctness is an integer from zero to five. Timing values are non-negative
active minutes or seconds. Boolean parity is `true` or `false`; mismatch and
incident values are observed counts. Missing observations remain absent or
use `observation_status: missing`; they never count as zero.

## Final disposition

The primary KPI is median reduction in reconstruction time among pairs where
both reviewers scored five of five. The adoption threshold is 30 percent and
the aspirational target is 40 percent.

- `Adopt bounded operation`: at least ten live correct pairs, primary
  threshold met, 100 percent receipt coverage, and every guardrail passes.
- `Extend shadow measurement`: the sample is too small or benefit remains
  inconclusive while safety holds.
- `Revise`: benefit is measurable but a non-safety burden, parity, or usability
  threshold fails.
- `Stop`: any authority/privacy incident, repeated receipt divergence, or less
  than 10 percent improvement with an adequate sample.

Only observed live measurements contribute to hours saved. An optional
attention-value rate may translate those observed hours into a scenario; it is
not revenue or realized cash ROI. System Engineer disposition is still
required to activate, continue, or expand gated operation.
