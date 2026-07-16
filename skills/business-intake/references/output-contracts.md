# Business Intake Output Contracts

Produce only the packets required by the selected mode. Use `Missing` instead of invention. Keep completed real-business packets outside Git.

## Owner Authority And Data Receipt

```text
Owner Authority And Data Receipt
- Business reference:
- Named owner approver:
- Requested mode: [create / change]
- Effective-context check: [none confirmed / existing context found / possible duplicate / not checked]
- Check confirmed by operator: [yes / no]
- Intake purpose:
- Intake authorized: [yes / no]
- May discuss:
- May handle temporarily:
- May preserve:
- Must not preserve:
- May share:
- Deletion authority:
- Exclusions and reuse restrictions:
- Pause conditions:
- Receipt status: [Confirmed / Hold]
```

## Business Intake And Readiness Packet

```text
Business Intake And Readiness Packet
- Business reference:
- Intended operating-review decision:
- Goals and desired outcomes:
- Products, services, customers, and channels:
- Economics and evidence quality:
- Customer and operating signals:
- Fulfillment, staffing, budget, and capacity constraints:
- Owner approval boundaries:
- Confirmed facts:
- Estimates:
- Hypotheses:
- Missing inputs:
- Readiness: [Ready / Provisional / Hold]
- Readiness reason:
- Next action:
- Required human authority:
```

## Proposed Business Context

```text
Proposed Business Context
- Business reference:
- Proposed version:
- Authority receipt reference:
- Business purpose and current goal:
- Offer and customer:
- Channels and operating model:
- Economics and evidence status:
- Customer and operating signals:
- Capacity and constraints:
- Risks and unknowns:
- Owner decision rights:
- Local/private facts:
- Approved transferable primitives:
- State: Proposed Business Context
```

## Owner Decision

```text
Owner Decision
- Business reference:
- Proposed context reference and version:
- Exact context displayed: [yes / no]
- Named owner:
- Decision: [Approved / Rejected / Changes Requested]
- Decision date:
- Approved preservation scope:
- Resulting state: [Awaiting Persistence / Rejected / Proposed Business Context]
- Separate operating-review authorization: [not requested / approved / declined / pending]
```

## Context Change Proposal

```text
Context Change Proposal
- Business reference:
- Current effective context reference and version:
- Current approval receipt reference:
- Reason for review:
- Evidence quality: [strong / medium / thin / none]
- Supporting evidence:
- Counterevidence:
- Uncertainty retained:

Exact change set:
1. Field:
   Before:
   After:
   Preservation or deletion implication:

- Complete proposed resulting context attached: [yes / no]
- Owner decision: [Approved / Rejected / Deferred / Changes Requested]
- Named owner:
- Decision date:
- Intended resulting version:
```

If a requested partial approval changes the displayed set, render the smaller exact change set and ask again. Do not infer approval.

## Approved Business Context Packet

```text
Approved Business Context Packet
- Packet type: [Approved Initial Context / Approved Change / Approved Removal]
- Business reference:
- Base effective context and version: [none for initial context]
- Named owner:
- Approval date:
- Exact approved contents or removal scope:
- Approved preservation scope:
- Intended resulting version:
- State: Awaiting Persistence
```

## Persistence Handoff

```text
Persistence Handoff
- Business reference:
- Approved packet reference:
- Prior effective version:
- Intended resulting version:
- Authorized operator:
- External tenant-private destination reference:
- Preservation confirmation: [pending / confirmed / failed]
- Confirmed effective version:
- Prior version no longer effective: [yes / no / not applicable]
- Final state: [Awaiting Persistence / Effective / Hold]
```

A failed or ambiguous preservation attempt leaves the prior version effective and produces `Hold`.

## Change Review Outcomes

- `No Change`: explain why the effective context remains better supported.
- `Open Question`: state the signal and evidence that would resolve it.
- `Context Change Proposal`: use the exact contract above.
- `Hold`: name the unresolved boundary and deciding human.

## De-identified Doctrine Candidate

```text
De-identified Doctrine Candidate
- Repeated pattern:
- Number and diversity of de-identified contexts:
- Bounded proposed improvement:
- Evidence that would weaken it:
- Membrane review: [pass / hold]
- Operator decision required:
- Repository mutation authorized: no
```

Exclude customer identities, quotations, exact private economics, suppliers, proprietary strategy, distinctive chronology, and unapproved claims.
