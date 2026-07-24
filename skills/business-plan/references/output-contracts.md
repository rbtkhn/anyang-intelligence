# Business Plan Output Contracts

Produce only the packets needed by the selected mode. Use `Missing` instead of invention. Keep completed real-business packets outside Git.

## Plan Authority And Data Receipt

```text
Plan Authority And Data Receipt
- Business reference:
- Requested mode: [create / resume / change]
- Effective context and version:
- Context approval receipt:
- Context persistence receipt:
- Named decision owner:
- Planning authority and scope:
- Planning purpose:
- Decision supported:
- Time horizon:
- Evidence permitted:
- Evidence prohibited:
- Privacy, retention, and sharing boundary:
- Constraints and non-negotiables:
- Success measures:
- Review date:
- Receipt status: [Confirmed / Hold]
```

## Plan Continuation Receipt

```text
Plan Continuation Receipt
- Business reference:
- Plan case reference:
- Requested mode: resume
- Prior checkpoint or packet reference:
- Effective context and version:
- Context approval and persistence receipts:
- Proposed or approved plan and version: [reference / none]
- Current plan state: [Proposed / Awaiting Persistence / Hold]
- Current continuation status: [Awaiting Evidence / Awaiting Owner Decision / Awaiting Persistence / Hold]
- Checkpoint matches business, context, and plan case: [yes / no]
- Named decision owner:
- Planning authority current: [yes / no / Missing]
- Evidence and privacy boundary current: [yes / no / Missing]
- Evidence added since checkpoint:
- Contradictions or corrections:
- Unresolved decision:
- Next bounded artifact:
- Next human authority:
- Resume requirements:
- Loop, pilot, activation, or external-action authorization: no
```

## Business Plan Readiness

```text
Business Plan Readiness
- Business reference:
- Effective-context check: [confirmed / failed / Missing]
- Planning-authority check: [confirmed / failed / Missing]
- Objective and named decision:
- Economics required and status:
- Capacity boundary and status:
- Evidence path and status:
- Success measure and review date:
- Readiness: [Ready / Provisional / Hold]
- Readiness reason:
- Next human decision:
```

`Provisional` supports bounded scenario or learning work only. It does not support final plan approval when decision-critical evidence is missing.

## Proposed Business Plan

```text
Proposed Business Plan
- Business reference:
- Proposed plan version:
- Effective context and version:
- Authority receipt reference:
- Decision summary:
- Planning horizon and exclusions:
- Current state and evidence quality:
- Confirmed facts:
- Estimates:
- Assumptions:
- Hypotheses and interpretations:
- Missing evidence:
- Strategic choices and tradeoffs:
- Explicit exclusions and non-choices:
- Customer and value proposition:
- Segments and channels:
- Capabilities and capacity constraints:
- Economics assumptions and scenarios:
- Objectives:
- Leading indicators:
- Outcome metrics:
- Guardrails and burden measures:
- Risks and dependencies:
- 30-day learning agenda:
- 90-day learning agenda:
- Proposed operating loops:
- Owner decisions required:
- Review date:
- Authority and data boundary:
- State: Proposed
- External-action authorization: no
```

## Owner Plan Decision

```text
Owner Plan Decision
- Business reference:
- Exact proposed plan and version displayed: [yes / no]
- Named decision owner:
- Decision: [Approved / Rejected / Deferred / Changes Requested]
- Decision date:
- Approved scope:
- Exclusions retained:
- Separate loop-design authority: [not requested / approved / declined / pending]
- Separate pilot or execution authority: [not requested / approved / declined / pending]
- Approved preservation scope:
- Resulting state: [Awaiting Persistence / Rejected / Deferred / Proposed]
```

## Approved Business Plan Packet

```text
Approved Business Plan Packet
- Business reference:
- Effective context and version:
- Approved plan and version:
- Named owner:
- Approval receipt:
- Exact approved choices and exclusions:
- Objectives, metrics, and guardrails:
- Approved learning agenda:
- Approved priority for possible loop design:
- Loop-design authority: [approved / declined / pending / not requested]
- Review date:
- State: Awaiting Persistence
- Plan effectiveness: pending
- Loop, pilot, or activation authorization: no
- External-action authorization: no
```

## Plan Persistence Handoff

```text
Plan Persistence Handoff
- Business reference:
- Effective context and version:
- Approved plan packet and version:
- Plan approval receipt:
- Prior effective plan and version: [none / reference]
- Authorized operator:
- External tenant-private destination reference:
- Preservation confirmation: [pending / confirmed / failed]
- Confirmed effective plan version:
- Prior plan no longer effective: [yes / no / not applicable]
- Final state: [Awaiting Persistence / Effective - not activated / Hold]
- Loop, pilot, activation, or external-action authorization: no
```

A failed or ambiguous preservation attempt leaves the prior effective plan
authoritative and produces `Hold`.

## Plan Change Proposal

```text
Plan Change Proposal
- Business reference:
- Current approved plan and version:
- Current effective context and version:
- Change authority:
- Reason for review:
- New evidence or owner direction:
- Evidence class and quality:
- Context-change dependency: [none / $business-intake change required]
- Strategic effect:

Exact change set:
1. Field:
   Before:
   After:
   Evidence and uncertainty:

- Complete proposed resulting plan attached: [yes / no]
- Named decision owner:
- Owner decision: [Approved / Rejected / Deferred / Changes Requested / Pending]
- Intended resulting version:
- Approved preservation scope:
- State: [Change proposed / Awaiting Persistence / Rejected / Deferred / Hold]
```

Rerender any smaller exact change set before accepting partial approval. Keep
the prior effective plan authoritative until persistence of the approved
replacement is confirmed.

## Operating-Loop Design Handoff

```text
Operating-Loop Design Handoff
- Business reference:
- Effective context and version:
- Effective plan and version:
- Plan approval receipt:
- Plan persistence receipt:
- Plan state: Effective - not activated
- Approved priority:
- Objective and decision:
- Outcome metric and leading indicator:
- Guardrails and burden limits:
- Named plan owner:
- Proposed loop owner:
- Evidence and privacy boundary:
- Explicit loop-design authority: [yes / no]
- Pilot or activation authority: no
- Status: [Ready for loop design / Hold]
```

## Other Outcomes

- `Hold`: name the missing condition, deciding human, and minimum evidence needed.
- `No Change`: explain why the approved plan remains better supported.
- `Open Question`: state the uncertainty and bounded evidence that could resolve it.
- `Rejected`: preserve the rejected version and owner decision.
- `Deferred`: preserve the deferral reason, owner, and review date.

When authority is absent, include:

> **No action taken; plan remains proposed or held pending owner decision.**
