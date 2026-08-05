# Council Steward Entropy-Reduction Cadence

**Status:** `advisory operating cadence - no execution authority`

**Owner:** System Engineer

**Applies to:** Executive Council portfolio reconciliation

**Default cadence:** monthly review with weekly focus areas

## Purpose

The Council Steward uses this cadence to reduce operating entropy before state
drift becomes expensive to reconstruct. It tests whether repository-visible
state claims are supported by receipts, authority, execution evidence,
completion gates, artifact lineage, and membrane checks.

This cadence does not authorize the Steward to approve findings, change state,
gather private evidence, communicate externally, purchase, publish, execute
corrections, or expand its own access. A finding may propose an exact
correction. The System Engineer must approve any persistent correction before
it changes authoritative state.

## Monthly rhythm

Week 1 - dashboard reconciliation:

- Compare [operating portfolio dashboard](../projects/operating-portfolio-dashboard.md)
  claims with controlling project documents, role contracts, authority receipts,
  and current state records.
- Prefer one finding per claim that materially affects priority, obligation,
  revenue, spending, client authority, runtime state, or completion status.

Week 2 - completion and state-label audit:

- Sample claims labeled `approved`, `active`, `evidence returned`, `complete`,
  `corrected`, or `superseded`.
- Check whether returned evidence supports the label and whether scope,
  executor, evidence, expiry, and exclusions match the authority record.

Week 3 - aging obligation review:

- Review pending decisions, held items, expired or stale approvals, review
  dates, follow-up owners, unresolved placeholders, and open commitments.
- Preserve `Missing` rather than reconstructing authority from narrative,
  continuity, silence, or prior practice.

Week 4 - high-risk membrane sample:

- Sample one boundary involving spending, client authority, privacy,
  child-safety, external claims, publication, rights, property, financial
  evidence, or cross-project transfer.
- Use only repository-visible receipts, sanitized derived facts, and opaque
  protected-evidence references unless a separate System Engineer approval
  permits wider Steward access.

## Review input order

Use the smallest evidence surface that can support or challenge the claim:

1. Current [authority envelope](../authority-envelope.yaml).
2. Current System Engineer approval, activation, pause, revocation, release,
   or reconciliation receipt.
3. Durable role contracts, including the
   [Council Steward role contract](council-steward-role-contract.md).
4. Current project authority, routing card, decision log, or README.
5. Current dashboard, operating review, derived view, or brief.
6. Historical, draft, compatibility, or superseded artifacts.
7. Existing Council workroom transaction events when available through the
   append-only ledger described in [CLI tools](../cli/README.md).

Lower-priority artifacts may supply context but must not silently override a
higher-priority source.

## Finding vocabulary

Use the vocabulary from the Council Steward role contract:

- `State Support` - receipts support the claimed state.
- `Reconciliation Required` - the current claim conflicts with or exceeds the
  evidence.
- `Insufficient Evidence` - the state cannot be adjudicated.
- `Contradiction Notice` - authoritative sources disagree.
- `Supersession Proposal` - overlapping artifacts require one controlling
  version.
- `Aging Obligation Notice` - an approval, commitment, exception, or review
  date is stale.
- `Completion Gate Finding` - returned evidence does or does not support
  `complete`.

One concise finding is preferred over a new report for every artifact. A
finding is advisory until accepted by the appropriate authority.

## Monthly scorecard metrics

Track the following counts and measures from repository-visible evidence or an
explicitly recorded Council event:

| Metric | Count or measure | Entropy reduced |
| --- | --- | --- |
| Unsupported state claims caught | Count of dashboard or document claims whose receipts do not support the displayed state | Unsupported summary drift |
| Completion-gate failures | Count of `complete` claims that should be `evidence returned`, `reconciliation pending`, `held`, or `blocked` | False closure |
| Authority gaps intercepted | Count of actions missing approval, named executor, scope, evidence requirement, expiry, or exclusions | Authority drift |
| Aging obligations surfaced | Count of stale reviews, expired approvals, unresolved follow-ups, or pending decisions without current owner/date | Open-loop decay |
| Supersession reductions | Count of overlapping artifacts consolidated or clearly marked historical/superseded after approval | Duplicate truth surfaces |
| Reconstruction time | Minutes required to identify controlling artifact, authority receipt, execution evidence, and current supported state | Review burden |
| Membrane holds | Count of cross-lane or private-context transfers correctly held pending review | Boundary leakage |
| False-positive burden | Count of Steward findings later rejected because evidence was sufficient or the issue was immaterial | Control cost |

Monthly success is not more findings. Success is lower reconstruction time,
fewer repeat contradictions, fewer stale obligations, fewer unsupported state
labels, and a false-positive burden low enough that the review still reduces
net cognitive load.

Structural validation, deterministic hash checks, complete fields, and command
success may support reconstruction. They do not by themselves prove operational
entropy was reduced. Entropy reduction requires an observed correction,
prevented rework, shorter reconstruction, resolved contradiction, clearer
authority chain, or preserved hold at a material boundary.

## First monthly pilot sample

The first monthly review uses exactly five items:

1. One portfolio dashboard claim.
2. One spending or purchase-related artifact.
3. One client-authority claim.
4. One runtime or source-boundary claim.
5. One stale, pending, expired, or held obligation.

Each sample must be reconstructable without private evidence bodies. If a
sample requires private evidence, use the approved opaque reference or mark the
review `Insufficient Evidence`.

## Monthly summary shape

```text
Council Steward Monthly Entropy Review
- Review month:
- Steward instance:
- Source boundary:
- Items sampled:
- Findings by type:
- Corrections proposed:
- Approvals required:
- Reconstruction-time notes:
- Entropy reduced:
- False positives or burden:
- What remains authoritative pending decision:
- Next review date:
```

When the review uses the Council workroom, align each material item to the
[Executive Council Transaction Record](../templates/executive-council-transaction-record.md)
sections:

- A. Recommendation;
- B. Authority disposition;
- C. Execution and evidence;
- D. Reconciliation.

Rendered Markdown is a review view, not a second writable record. The
append-only Council ledger remains the canonical operating state where it is
used.

## Escalation triggers

Escalate to the System Engineer when:

- an authoritative state claim exceeds its receipts;
- role runtime state, source release, access, or persistence is ambiguous;
- an approval, exception, or review date has expired;
- a correction would change governance, permissions, membranes, or current
  project state;
- a client-company decision may be missing;
- a claim touches spending, publication, external representation, rights,
  legal, tax, medical, educational, safety, child-related, privacy, property,
  or other regulated judgment;
- protected evidence appears necessary to resolve the finding; or
- the Steward's independence, source boundary, or false-positive burden
  compromises the value of the review.

## Done when

The monthly review is complete when the operator can see which claims were
sampled, which finding category applies, what evidence was reviewed, what
correction is proposed, who must approve it, what remains authoritative until
then, and whether the review reduced entropy rather than merely adding process.
