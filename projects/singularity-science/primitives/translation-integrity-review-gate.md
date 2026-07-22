# Translation Integrity Review Gate

Use this internal gate when meaning crosses a consequential boundary:

```text
intent → system behavior → operational outcome → evidence → authority → learning
```

## When to invoke

Required for:

- promoting research into a primitive;
- routing a primitive into a customer or operating lane;
- approving consequential automation;
- publishing or treating an outcome as final;
- changing where authority, approval, or delegation lives.

Optional for source notes, descriptive archive maintenance, and low-stakes observations. Do not invoke it for purely clerical work unless the work changes meaning, authority, or downstream action.

## Review block

```text
Workflow:
Beneficiary:
Human intent:
System behavior:
Operational outcome:
Primary value metric:
Quality / risk guardrail:
Evidence of value:
New burden introduced:
Value gained:
Net operating judgment:
Artifact owner:
Workflow owner:
Evidence reviewer:
Approval authority:
Status:
Reason code:
Unresolved translation risk:
What remains outside the system:
Next learning cycle:
Next review trigger:
```

## Status

- `pass`: intent, behavior, outcome, evidence, and authority align.
- `concern`: the mechanism is plausible, but evidence, burden, quality, or authority is incomplete.
- `blocked`: intent is unclear, evidence contradicts the claim, authority is absent, or risk exceeds permission.

## Reason codes

- `intent-unclear`
- `behavior-mismatch`
- `outcome-unproven`
- `guardrail-failure`
- `burden-outweighs-value`
- `authority-ambiguous`
- `evidence-conflict`
- `rights-or-membrane-risk`
- `not-applicable`

## Evidence standard

Every value claim needs one primary outcome measure, at least one quality, safety, rights, privacy, or human-burden guardrail, representative evidence, and the cost or review burden introduced.

Do not treat speed, volume, completion rate, a single successful demo, or raw source material as sufficient value evidence.

## Learning loop

For `concern` or `blocked`, record the next action: clarify intent, change behavior, redefine the metric, improve evidence, add a guardrail, reduce burden, identify authority, or hold/stop.

When evidence fails:

```text
evidence failure → revise intent or outcome → revise behavior → retest
```

Every `pass` must include a next review trigger. A pass is not permanent doctrine.

## Boundary

This gate is an internal governance aid. It does not grant legal, rights, safety, professional, customer, or publication authority, and it does not automatically approve a workflow.
