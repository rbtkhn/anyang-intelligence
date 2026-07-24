# Business Loop Output Contracts

Produce only the packets needed by the selected mode. Keep completed real-business packets and private evidence outside Git.

## Loop Authority And Linkage Receipt

```text
Loop Authority And Linkage Receipt
- Business reference:
- Effective context and version:
- Effective plan priority and plan version:
- Plan approval receipt:
- Plan persistence receipt:
- Plan state: [Effective - not activated / not applicable]
- Standalone loop-design authority, if applicable:
- Requested mode: [design / resume / change / review / pause / retire]
- Named loop owner:
- Named decision owner:
- One signal:
- One decision:
- Permitted actions:
- Prohibited actions:
- Evidence source:
- Private-data location:
- Cadence and service expectation:
- Success metric:
- Burden guardrail:
- Pause and stop conditions:
- Receipt status: [Confirmed / Hold]
```

## Loop Continuation Receipt

```text
Loop Continuation Receipt
- Business reference:
- Loop case reference:
- Requested mode: resume
- Prior checkpoint or pause receipt:
- Effective context and version:
- Effective plan and version: [reference / not applicable]
- Plan approval and persistence receipts: [references / not applicable]
- Loop specification and version:
- Current loop state: [Draft / Awaiting Persistence / Approved - pilot pending / Hold / Paused]
- Current continuation status: [Awaiting Evidence / Awaiting Specification Decision / Awaiting Persistence / Awaiting Pilot Decision / Awaiting Reactivation / Hold]
- Checkpoint matches business, context, plan, and loop case: [yes / no]
- Named loop owner and decision owner:
- Authority current: [yes / no / Missing]
- Evidence and privacy boundary current: [yes / no / Missing]
- Evidence added since checkpoint:
- Contradictions or corrections:
- Open obligations, if paused:
- Restart conditions satisfied: [yes / no / not applicable]
- Unresolved decision:
- Next bounded artifact:
- Next human authority:
- Resume requirements:
- Pilot run, activation, or external-action authorization: no
```

## Current Workflow Map

```text
Current Workflow Map
- Workflow boundary:
- Signal:
- Current stages and handoffs:
- Current memory objects:
- Current decision owner:
- Current action and approval path:
- Evidence currently produced:
- Delays and aging:
- Exceptions and escalation:
- Human burden:
- Evidence gaps:
- Confirmed facts:
- Estimates and interpretations:
- Missing evidence:
- Status: [Mapped / Hold]
```

Mapping does not establish that any action was authorized or completed.

## Proposed Operating Loop Specification

```text
Proposed Operating Loop Specification
- Loop name and stable reference:
- Business reference:
- Effective context and version:
- Approved plan priority and plan version:
- Proposed specification version:
- One recurring decision:
- Signal:
- Memory objects:
- Decision prepared:
- Loop owner:
- Decision owner and approval authority:
- Authorized action path:
- Prohibited actions:
- Evidence and receipts:
- Cadence and service expectation:
- Outcome metric:
- Leading indicator:
- Quality and risk guardrails:
- Human-burden guardrail:
- Exceptions and escalation:
- Pause and stop conditions:
- Learning update:
- Governance and data membrane:
- Pilot recommendation:
- Pilot prerequisites:
- Review date:
- State: Draft
- Pilot authorization: no
- Activation authorization: no
```

## Owner Loop Decision

```text
Owner Loop Decision
- Loop reference and exact specification version displayed:
- Named decision owner:
- Decision: [Approved / Changes Requested / Deferred / Rejected / Hold]
- Decision date:
- Approved scope and exclusions:
- Approved preservation scope:
- Separate pilot authorization: [not requested / approved / declined / pending]
- Separate activation authorization: [not requested / approved / declined / pending]
- Resulting state: [Awaiting Persistence / Draft / Hold]
```

Specification approval, persistence, and pilot authorization are distinct.
Approval produces `Awaiting Persistence`; persistence produces
`Approved - pilot pending`; only a separately approved exact pilot scope
produces `Approved for pilot`.

## Approved Loop Specification Packet

```text
Approved Loop Specification Packet
- Business reference:
- Effective context and version:
- Effective plan and version: [reference / not applicable]
- Loop reference and approved specification version:
- Named decision owner:
- Approval receipt:
- Exact approved specification:
- Approved preservation scope:
- Separate pilot authorization: [not requested / approved / declined / pending]
- State: Awaiting Persistence
- Pilot run or activation authorization: no
```

## Loop Specification Persistence Handoff

```text
Loop Specification Persistence Handoff
- Business reference:
- Approved loop specification packet and version:
- Specification approval receipt:
- Prior authoritative specification and version: [none / reference]
- Authorized operator:
- External tenant-private destination reference:
- Preservation confirmation: [pending / confirmed / failed]
- Confirmed persisted specification version:
- Prior specification superseded: [yes / no / not applicable]
- Pilot authorization: [approved / pending / declined / not requested]
- Final state: [Awaiting Persistence / Approved - pilot pending / Approved for pilot / Hold]
- Pilot run, activation, or external-action authorization: no
```

`Approved for pilot` requires confirmed persistence plus separate approval of
the exact bounded pilot scope. Failed or ambiguous persistence leaves the
prior authoritative specification in force and produces `Hold`.

## Pilot Handoff Packet

```text
Pilot Handoff Packet
- Loop reference and approved specification version:
- Specification approval receipt:
- Specification persistence receipt:
- Specification state: Approved for pilot
- Pilot route: [manual workflow / automation]
- Automation involved: [yes / no]
- Exact pilot question and scope:
- Approved tools, paths, and data classes:
- Run limit:
- Named owner and reviewer:
- Baseline and target:
- Quality and burden thresholds:
- Required evidence and receipts:
- Exceptions and stop conditions:
- Approved automation-value-proof reference: [required for automation / not applicable]
- bounded-workflow-pilot prerequisites satisfied: [yes / no]
- Pilot authorization: [approved / pending / declined]
- Deployment or activation authorization: no
- Status: [Ready for pilot / Hold]
```

For `manual workflow`, this complete persisted packet supplies the pilot
readiness and authorization route. For `automation`, also require a complete
human-approved `automation-value-proof` packet. Do not invoke
`bounded-workflow-pilot` unless every prerequisite for the selected route is
satisfied.

## Activation Receipt

```text
Activation Receipt
- Loop reference:
- Exact approved specification version:
- Transition: [initial activation / resume from pause]
- Prior pause receipt: [reference / not applicable]
- Pilot or readiness evidence:
- Named activating operator:
- Named loop owner and decision owner:
- Effective date:
- Permitted actions:
- Prohibited actions:
- Evidence destination:
- Cadence:
- Guardrails and stop conditions:
- Review date:
- Activation confirmed: [yes / no]
- State: [Active / Hold]
```

Only `Activation confirmed: yes` permits `Active`.

## Loop Review Packet

```text
Loop Review Packet
- Loop reference and version:
- Evidence period:
- Source state: [approved pilot / Active]
- Activation receipt reference: [required when source state is Active / not applicable]
- Activation receipt current and version-matched: [yes / no / not applicable]
- Expected decisions and cycles:
- Observed decisions and cycles:
- Authorized actions and receipts:
- Outcomes and leading indicators:
- Quality and risk findings:
- Exceptions and escalation performance:
- Human burden:
- Governance and membrane findings:
- Open-loop drift or memory decay:
- Cadence fit:
- Learning:
- Missing evidence:
- Recommendation: [Adopt / Revise / Hold / Retire]
- Route: [activation decision / $business-loop change / $business-plan change / $business-intake change / no change]
- Named decision owner:
- Review date:
- Current authoritative version and state:
- Resulting state: [Approved - pilot pending / Approved for pilot / Active / Change proposed / Hold / Paused / Retired / No Change]
```

`Adopt` after a pilot recommends activation; it does not create `Active`.
`Adopt` for an active loop retains `Active` only when the exact version's
activation receipt remains current. `Revise`, `Hold`, or `Retire` is a
recommendation and preserves the current authoritative state until its
separate decision and required receipt exist.

## Loop Change Proposal

```text
Loop Change Proposal
- Loop reference:
- Current specification version and state:
- Effective context and approved plan versions:
- Change authority:
- Evidence prompting change:
- Route check: [loop change / $business-plan change / $business-intake change]

Exact change set:
1. Field:
   Before:
   After:
   Evidence and uncertainty:

- Complete proposed resulting specification attached: [yes / no]
- Named decision owner:
- Decision: [Approved / Changes Requested / Deferred / Rejected / Pending]
- Intended resulting version:
- Activation impact:
- Replacement specification approval: [approved / pending / rejected / not applicable]
- Replacement persistence receipt: [confirmed / pending / not required]
- Replacement activation receipt: [confirmed / pending / not required]
- Proposed-version state: [Change proposed / Awaiting Persistence / Approved - pilot pending / Approved for pilot / Active / Hold / No Change]
- Current authoritative version and state after decision:
```

Existing persistence or activation receipts cannot govern the intended
replacement version. Preserve the prior active version until replacement
persistence and activation receipts are confirmed.

## Pause Packet

```text
Pause Packet
- Loop reference and current version:
- Current state:
- Pause authority:
- Reason and evidence:
- New-cycle cutoff:
- Open obligations and owner:
- Dependent workflows:
- Evidence preserved and retention rule:
- Access or schedule changes:
- Restart conditions:
- Named decision owner:
- Decision: [Approved / Rejected / Deferred / Pending]
- Operator confirmation of operational steps: [confirmed / pending]
- State transition effective: [yes / no]
- Current authoritative version and state:
- Resulting state: [Paused / Hold]
```

Use `Paused` only when the decision is approved and reversible stop steps are
confirmed. Otherwise use `Hold` and preserve the prior authoritative state.

## Retirement Packet

```text
Retirement Packet
- Loop reference and current version:
- Current state:
- Terminal retirement authority:
- Reason and evidence:
- New-cycle cutoff:
- Open obligations and owner:
- Dependent workflows:
- Ownership transfers:
- Evidence preserved and retention rule:
- Access and permanent schedule changes:
- Named decision owner:
- Decision: [Approved / Rejected / Deferred / Pending]
- Operator confirmation of terminal steps: [confirmed / pending]
- State transition effective: [yes / no]
- Current authoritative version and state:
- Resulting state: [Retired / Hold]
```

Use `Retired` only when the terminal decision and operational steps are
confirmed. A retired loop cannot be resumed; a future loop requires new design
authority.

When authority is absent, include:

> **No action taken; loop remains draft, paused, or held pending owner decision.**
