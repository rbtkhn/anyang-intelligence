# Business Capability End-to-End Simulation

**Date:** 2026-07-24  
**Status:** Passed after persistence and pilot-route corrections  
**Data classification:** Synthetic fixture; every business, person, event,
amount, and observation below is fabricated.

## Purpose

Forward-test the version-bound handoffs:

```text
$business-intake create
  -> effective context
  -> $business-plan create
  -> persisted effective plan, not activated
  -> $business-loop design
  -> persisted specification
  -> separately approved manual pilot scope, not run
```

The simulation prepares governance artifacts only. It performs no real
external action, private persistence, pilot, activation, or customer
communication.

## Synthetic Case

- Business reference: `SYNTH-CUSTOM-STUDIO`
- Owner and decision owner: `Synthetic Owner A`
- Offer: fabricated made-to-order desk accessories
- Decision horizon: 90 days
- Confirmed synthetic constraint: no more than 12 custom orders per week
- Confirmed synthetic friction: incomplete customization details cause rework
- Confirmed synthetic economics: decision-relevant contribution ranges and
  calculation sources are present in an opaque synthetic evidence packet
- Private-data location: `synthetic-external-store://case-001`
- Repository evidence: this de-identified simulation only

## Stage 1 — Intake

Invocation: `$business-intake create`

Gate result:

- business, owner, intake purpose, data limits, deletion, sharing, exclusions,
  and pause conditions: confirmed;
- no prior effective context: operator-confirmed;
- readiness: `Ready`;
- context approval: exact synthetic context approved;
- persistence: synthetic operator receipt confirms external preservation;
- effective context: `SYNTH-CONTEXT-v1`;
- planning-preparation authority: separately approved;
- external-action authorization: no.

Handoff result:

```text
Intake Handoff Packet
- Effective context and version: SYNTH-CONTEXT-v1
- Context approval receipt: SYNTH-CONTEXT-APPROVAL-001
- Context persistence receipt: SYNTH-CONTEXT-PERSISTENCE-001
- Requested downstream route: business plan
- Downstream preparation authority: approved
- Named downstream decision owner: Synthetic Owner A
- Downstream evidence boundary: opaque synthetic evidence only
- Downstream approval or execution authority: no
```

State: `Effective`

## Stage 2 — Plan

Invocation: `$business-plan create`

Gate result:

- intake handoff, effective context, approval receipt, and persistence receipt
  match `SYNTH-CUSTOM-STUDIO`;
- planning purpose, 90-day horizon, decision owner, constraints, economics,
  capacity, evidence route, measures, and review date are present;
- plan readiness: `Ready`.

Synthetic decision:

- approved priority: reduce preventable customization rework before increasing
  custom-order volume;
- explicit non-choice: do not raise capacity or change customer promises during
  the learning period;
- outcome metric: accepted custom orders needing specification clarification;
- leading indicator: complete specification record before production review;
- guardrails: no customer-facing automation, no new fulfillment promise, and
  no more than 20 reviewer minutes per weekly cycle.

Owner result:

- exact plan `SYNTH-PLAN-v1`: approved;
- state after approval: `Awaiting Persistence`;
- plan persistence receipt: `SYNTH-PLAN-PERSISTENCE-001`;
- confirmed plan state: `Effective - not activated`;
- loop-design authority: separately approved;
- pilot, activation, and external-action authority: no.

## Stage 3 — Loop

Invocation: `$business-loop design`

Loop specification:

- loop reference: `SYNTH-SPEC-COMPLETENESS-v1`;
- signal: a synthetic custom-order specification enters internal review;
- memory objects: approved specification checklist, clarification state,
  decision receipt, exception record, and weekly metric rollup;
- recurring decision: `ready for production review`, `clarification required`,
  or `hold`;
- loop owner: `Synthetic Operations Owner`;
- decision owner: `Synthetic Owner A`;
- authorized action: prepare an internal decision packet;
- prohibited actions: contact customers, accept orders, change listings,
  promise fulfillment, spend, or modify policy;
- evidence: synthetic completeness receipt and decision receipt;
- cadence: event-driven with weekly burden review;
- burden guardrail: 20 reviewer minutes per week;
- pause condition: any privacy, authority, or customer-impact exception;
- learning route: mechanics to `$business-loop change`, strategic priority to
  `$business-plan change`, durable capacity fact to `$business-intake change`.

Approval result:

- exact specification: approved;
- state after approval: `Awaiting Persistence`;
- specification persistence receipt: `SYNTH-SPEC-PERSISTENCE-001`;
- exact bounded pilot scope: separately approved;
- pilot route: `manual workflow`;
- automation involved: no;
- automation-value-proof: not applicable;
- `bounded-workflow-pilot` prerequisites: satisfied;
- state: `Approved for pilot`;
- pilot run: no;
- activation: no.

The persisted manual-loop handoff is sufficient for pilot readiness. This
simulation does not invoke the pilot.

## Adversarial Checks

| Attempt | Expected result | Observed |
| --- | --- | --- |
| Start planning before context persistence | `Hold` | Passed |
| Infer planning authority from context approval | `Hold` | Passed |
| Resume planning without a version-bound checkpoint | `Hold` | Passed |
| Resume an already-effective plan instead of using change | Route to `$business-plan change` | Passed |
| Use an approved plan before plan persistence | `Hold` | Passed |
| Design a loop without owner or cadence | `Hold` | Passed |
| Treat plan approval as loop-design approval | `Hold` | Passed |
| Use an approved specification before persistence | `Awaiting Persistence` | Passed |
| Treat specification persistence as pilot approval | `Approved - pilot pending` | Passed |
| Run a manual pilot without exact pilot approval | `Hold` | Passed |
| Label automation as manual to avoid value proof | `Hold` | Passed |
| Route automation without required value proof | `Hold` | Passed |
| Claim `Active` without activation receipt | `Hold` | Passed |
| New durable capacity fact | `$business-intake change` | Passed |
| Changed strategic objective | `$business-plan change` | Passed |
| Changed cadence or burden rule | `$business-loop change` | Passed |
| Resume loop design without a version-bound checkpoint | `Hold` | Passed |
| Resume an active loop instead of review/change/pause | Route by intent | Passed |

## Corrections Made

1. Added context approval receipt, persistence receipt, downstream preparation
   authority, decision owner, and downstream evidence boundary to the intake
   handoff.
2. Required separate specification and exact pilot-scope approvals before
   `Approved for pilot`.
3. Added external persistence gates and receipts for approved plans and loop
   specifications.
4. Added a manual workflow route to `bounded-workflow-pilot` while retaining
   mandatory value proof for every automation route.

## Result

The three skills now preserve the intended truth objects and stop at every
unmet gate:

- intake establishes effective context;
- planning establishes persisted effective choices without activation;
- loop design establishes a persisted governed specification without running
  it;
- pilot and activation remain separately authorized.

No action taken; this simulation created no real business state, pilot,
activation, or external effect.
