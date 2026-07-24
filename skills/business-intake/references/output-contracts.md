# Business Intake Output Contracts

Produce only the packets required by the selected mode. Use `Missing` instead of invention. Keep completed real-business packets outside Git.

## Owner Authority And Data Receipt

```text
Owner Authority And Data Receipt
- Business reference:
- Named owner approver:
- Requested mode: [create / resume / change]
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

## Intake Continuation Receipt

```text
Intake Continuation Receipt
- Business reference:
- Intake case reference:
- Requested mode: resume
- Prior checkpoint reference:
- Prior phase and status:
- Checkpoint matches business and intake case: [yes / no]
- Named owner:
- Authority boundary current: [yes / no / Missing]
- Data boundary current: [yes / no / Missing]
- Evidence added since checkpoint:
- Contradictions or corrections:
- Unresolved owner decision:
- Next bounded artifact:
- Resulting phase and status:
- Resume requirements:
```

## Verified Meeting Capture

```text
Verified Meeting Capture
- Business reference:
- Intake case reference:
- Meeting date:
- Source reference:
- CEO-confirmed priority:
- CEO correction to current understanding:
- Primary constraint:
- Highest-cost operational friction:
- Highest-risk customer promise:
- Approved first-review scope:
- Evidence authorized for review:
- Privacy and membrane limits:
- Approval authority:
- Success metric:
- Review date:
- Confirmed owner statements:
- Preparation hypotheses kept separate:
- Missing evidence:
- Intake phase:
- Context state:
- Operating-review authorization: [not requested / approved / declined / pending]
- External-action authorization: no
- Status:
```

If the meeting did not authorize action, include:

> **No action taken; intake remains proposed or held pending owner decision.**

## First Review Decision Receipt

```text
First Review Decision Receipt
- Business reference:
- Decision the review should support:
- Review scope:
- Evidence allowed:
- Evidence prohibited:
- Privacy and storage boundary:
- Actions permitted:
- Actions prohibited:
- Named approver:
- Decision: [approved / declined / pending / revise]
- Success metric:
- Review date:
- First-review brief required before execution: yes
- Implementation authorization: no
- Status:
```

## Intake Handoff Packet

```text
Intake Handoff Packet
- Business reference:
- Intake case reference:
- Current phase:
- Current status:
- Effective context and version: [reference / none / Missing]
- Context approval receipt: [reference / Missing]
- Context persistence receipt: [reference / Missing]
- Named owner:
- Confirmed owner statements:
- Preparation hypotheses:
- Authority boundary:
- Evidence and privacy boundary:
- Requested downstream route: [first operating review / business plan / other / none]
- Downstream preparation authority: [approved / declined / pending / Missing]
- Named downstream decision owner:
- Downstream evidence boundary:
- Completed artifacts:
- Open decisions:
- Missing evidence:
- Pause condition:
- Exact next action:
- Required human authority:
- Resume requirements:
- Downstream approval or execution authority: no
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

## Sanitized Intake-Control Manifest

Render this as fenced YAML only after the human-readable packet is complete. The manifest is an import candidate for the separately invoked external control plane; producing it does not authorize or perform persistence.

```yaml
business_reference: <stable tenant-safe reference>
version: <exact proposed version>
base_version: <exact effective version or null for a confirmed initial context>
external_content_ref: <opaque external proposal reference>
authority_receipt_ref: <opaque authority receipt reference>
readiness: <ready | provisional | hold>
created_by: <named operator>
evidence:
  - class: <confirmed | estimate | hypothesis | missing>
    kind: <bounded evidence kind>
    summary: <single-line redacted summary>
    source_ref: <opaque, public, or sanitized repository reference>
    confidence: <high | medium | low | unknown>
    sensitivity: <public | internal | private | restricted>
unresolved_gates:
  - <required missing decision or evidence>
```

Do not include raw messages, customer identifiers, exact private economics, local absolute paths, database files, or private attachment filenames. `hold` requires at least one unresolved gate. A missing effective base version must remain `hold`; do not substitute a conversational or repository-inferred version.
