# Business Loop Contract

Define every field. Use `Missing` rather than invention. A loop is not ready for approval when a required field is missing.

## Identity And Linkage

- Loop name and stable reference.
- Business reference and effective context version.
- Effective plan priority and plan version with approval and persistence
  receipts, or standalone design authority.
- Specification version and state.
- One recurring decision.
- Loop owner and decision owner.

## Loop Grammar

- `Signal`: event, threshold, cadence, or exception that starts one cycle.
- `Memory objects`: versioned facts, commitments, prior decisions, risks, and open loops needed for judgment.
- `Decision prepared`: exact choice, options, and escalation threshold.
- `Authorized action path`: who may do what after which approval.
- `Evidence and receipts`: proof that decisions, actions, results, and approvals occurred.
- `Cadence and service expectation`: frequency, response window, and aging rule.
- `Metrics and burden guardrails`: outcomes, leading indicators, quality, risk, and human load.
- `Exceptions and escalation`: detectable exception classes, owner, route, and response expectation.
- `Pause and stop conditions`: thresholds that prevent or halt a cycle.
- `Learning update`: what evidence may revise loop mechanics, plan choices, or durable context.
- `Governance and data membrane`: permitted data, storage, sharing, retention, prohibited uses, and human/professional approvals.

## Smallest-Viable-Loop Rules

1. Support exactly one recurring decision.
2. Use the fewest stages, handoffs, memory objects, and metrics needed for trustworthy judgment.
3. Reuse existing approved evidence before requesting new evidence.
4. State what remains manual and why.
5. Preserve human review before consequential actions.
6. Reject automation that merely accelerates ambiguity or governance risk.
7. Include an aging rule so signals and open decisions cannot drift indefinitely.
8. Include a burden threshold; a loop whose review load exceeds its value must pause or change.

## Evidence And Review Rules

Classify statements as confirmed facts, estimates, hypotheses, interpretations, anomalies, or missing evidence.

For each metric, define:

- calculation and unit;
- source and evidence owner;
- baseline or `Missing`;
- success or decision threshold;
- review cadence;
- burden and quality guardrails.

For each exception, define:

- detection signal;
- prohibited automated response;
- responsible human;
- escalation route and deadline;
- evidence required to close it.

Do not treat activity counts as outcomes, missing receipts as successful actions, or silence as approval.

## Version And State Rules

- `Draft`: specification is incomplete or awaiting decision.
- `Awaiting Persistence`: exact specification approved but preservation is
  pending.
- `Approved - pilot pending`: exact approved specification has a
  version-matched persistence receipt; pilot scope is not approved.
- `Approved for pilot`: persisted specification and bounded pilot scope
  received separate explicit approvals; pilot not yet run.
- `Hold`: required authority, evidence, safety, ownership, or boundary is unresolved.
- `Active`: operator-confirmed activation receipt exists for this exact version.
- `Paused`: new cycles are stopped while obligations, evidence, and restart
  conditions remain governed; reactivation requires a pause receipt,
  satisfied restart conditions, authority, and a new Activation Receipt.
- `Retired`: owner confirmed terminal closure, transfers, evidence
  preservation, and access changes; it cannot be resumed.
- `Change proposed`: current version remains authoritative while an exact revision awaits decision.

Never silently edit an approved or active loop. Preserve the prior version
until replacement approval and persistence exist, plus any required
activation receipt.

Persistence and activation receipts are version-bound and cannot transfer to
a replacement specification. A review recommendation is advisory and does not
itself change the current authoritative state. Use `Paused` or `Retired` only
after the decision and required operational steps are both operator-confirmed.
