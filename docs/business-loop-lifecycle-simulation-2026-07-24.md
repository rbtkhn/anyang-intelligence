# Business Loop Lifecycle Simulation

**Date:** 2026-07-24  
**Status:** Passed after lifecycle-state corrections  
**Data classification:** Synthetic fixture; every business, person, event,
amount, and observation below is fabricated.

## Purpose

Stress-test:

- `$business-loop change`;
- `$business-loop review`;
- `$business-loop pause`;
- `$business-loop resume`;
- `$business-loop retire`.

No workflow, pilot, activation, pause, retirement, customer contact, or other
external action was performed.

## Starting Fixture

- Business reference: `SYNTH-CUSTOM-STUDIO`
- Effective context: `SYNTH-CONTEXT-v1`
- Effective plan: `SYNTH-PLAN-v1`
- Plan persistence receipt: `SYNTH-PLAN-PERSISTENCE-001`
- Loop: `SYNTH-SPEC-COMPLETENESS-v1`
- Specification persistence receipt: `SYNTH-SPEC-PERSISTENCE-v1`
- State: `Active`
- Version-matched activation receipt: `SYNTH-ACTIVATE-v1`
- Synthetic evidence location: `synthetic-external-store://case-001`
- Loop owner: `Synthetic Operations Owner`
- Decision owner: `Synthetic Owner A`

## Change Path

Synthetic evidence shows weekly human review burden exceeded the 20-minute
guardrail in three consecutive cycles. The evidence changes loop cadence and
exception handling, not business capacity or plan priority.

Route: `$business-loop change`

Exact synthetic change:

```text
Field: cadence and burden escalation
Before: weekly rollup; escalate after one cycle above 20 minutes
After: event-driven decision plus biweekly burden rollup; pause after two
       consecutive rollups above 20 minutes
```

Decision sequence:

1. Replacement `SYNTH-SPEC-COMPLETENESS-v2` approved.
2. Replacement persistence receipt remains pending.
3. Proposed-version state is `Awaiting Persistence`.
4. Replacement persistence is separately confirmed.
5. Replacement activation receipt remains pending.
6. `SYNTH-SPEC-COMPLETENESS-v1` remains the authoritative `Active` version.
7. The v1 persistence and activation receipts do not transfer to v2.
8. After a separate synthetic activation confirmation, v2 becomes `Active`
   and v1 becomes superseded.

Result: passed after making proposed-version state and authoritative current
state separate fields.

## Review Paths

### Approved-Pilot Review

Synthetic pilot evidence meets the quality threshold and stays below the
burden guardrail.

- Recommendation: `Adopt`
- Route: activation decision
- Current state: `Approved for pilot`
- Resulting state: `Approved for pilot`
- `Active`: prohibited until a version-matched activation receipt exists

Result: passed.

### Active-Loop Review

Synthetic evidence for v2 shows expected decisions and receipts, no governance
regression, and a current version-matched activation receipt.

- Recommendation: `Adopt`
- Route: no change
- Resulting state: `Active`

When the activation receipt is missing, stale, or bound to v1, the same review
returns `Hold`; it cannot retain `Active` for v2.

Result: passed after adding the activation-receipt check to the review packet.

### Review Recommending Change

Synthetic evidence indicates burden is again approaching the guardrail.

- Recommendation: `Revise`
- Route: `$business-loop change`
- Current authoritative state: `Active`
- State transition caused by recommendation: none

Result: passed. A recommendation does not silently modify the loop.

## Pause Path

The decision owner approves a reversible pause, but the schedule disablement
and open-obligation transfer are initially unconfirmed.

- Decision: approved
- Operational confirmation: pending
- Resulting state: `Hold`
- Current authoritative state: `Active`

After separate synthetic operator confirmation:

- new cycles stopped;
- open obligations assigned;
- evidence retained;
- restart conditions recorded;
- resulting state: `Paused`.

Result: passed after making operational confirmation mandatory.

### Resume From Pause

After the synthetic pause receipt exists, the operator supplies the same
persisted specification, satisfied restart conditions, current authority, and
a new version-matched Activation Receipt.

- invocation: `$business-loop resume`;
- prior state: `Paused`;
- transition: `resume from pause`;
- resulting state: `Active`.

Without the pause receipt, satisfied restart conditions, reactivation
authority, or new Activation Receipt, the result is `Hold`.

Result: passed.

## Retirement Path

The decision owner approves terminal retirement with open obligations,
dependent workflow review, evidence retention, access removal, and ownership
transfer specified.

Before operational confirmation:

- resulting state: `Hold`;
- prior authoritative state preserved.

After synthetic operator confirmation:

- open obligations closed or transferred;
- evidence retention confirmed;
- access and schedule changes confirmed;
- resulting state: `Retired`.

Result: passed.

Attempting `$business-loop resume` after `Retired` returns `Hold` and requires
new loop-design authority.

## Routing Checks

| New evidence | Required route | Result |
| --- | --- | --- |
| Sustainable capacity changed | `$business-intake change` | Passed |
| Strategic priority changed | `$business-plan change` | Passed |
| Cadence, burden, or exception rule changed | `$business-loop change` | Passed |
| Evidence insufficient to justify change | `No Change` or `Hold` | Passed |

## Corrections Made

1. Added a version-matched activation receipt check to active-loop reviews.
2. Separated replacement proposal state from current authoritative loop state.
3. Prohibited transferring old persistence or activation receipts to a new
   specification.
4. Required confirmed operational steps before `Paused` or `Retired`.
5. Added checkpoint-bound continuation and governed reactivation from
   `Paused`; terminal `Retired` remains non-resumable.

No action taken; all lifecycle states and evidence in this document are
synthetic.
