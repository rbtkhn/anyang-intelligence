# Learner Intake Output Contracts

Produce only the packets required by the selected mode. Use `Missing` instead of inventing content. Keep real completed packets outside Git.

## Authority And Privacy Receipt

```text
Authority And Privacy Receipt
- Opaque learner reference:
- Parent-approved display label:
- Named guardian approver:
- Intake or review authorized: [yes / no]
- May discuss:
- May handle temporarily:
- May preserve:
- Must not preserve:
- May share:
- Deletion authority:
- Exclusions:
- Minimum caution implication:
- Receipt status: [Confirmed / Hold]
```

This receipt is canonical for authority and save/share boundaries. Profiles reference it; they do not copy its rules.

## Intake And Readiness Packet

Use `projects/learning-core/parent-intake-summary-template.md`. Include `Ready`, `Provisional`, or `Hold`, evidence quality, missing inputs, assumptions, next action, and its human authority.

## Proposed Initial Learner Profile

Use `projects/learning-core/initial-learner-profile-template.md`. Set profile state to `Proposed Initial Profile`. Include only content the guardian permitted for review and possible preservation.

## Initial Profile Decision

```text
Initial Profile Decision
- Opaque learner reference:
- Proposed profile reference:
- Exact profile displayed: [yes / no]
- Named guardian:
- Decision: [Approved / Rejected / Changes Requested]
- Decision date:
- Approved preservation scope:
- Resulting state: [Awaiting Persistence / Rejected / Proposed Initial Profile]
- Separate drafting authorization: [not requested / approved / declined / pending]
```

If changes are requested, render the complete corrected profile and seek confirmation again.

## Change Review Outcome

Use one of these states:

- `No Change`: explain why the current profile remains better supported.
- `Open Question`: state the signal and evidence that would clarify it.
- `Profile Change Proposal`: use the contract below.
- `Hold`: name the unresolved boundary and deciding human.

## Profile Change Proposal

```text
Profile Change Proposal
- Opaque learner reference:
- Current effective profile reference:
- Current effective version:
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

- Complete proposed resulting profile attached: [yes / no]
- Guardian decision: [Approved / Rejected / Deferred / Changes Requested]
- Named guardian:
- Decision date:
- Intended resulting version:
```

Do not accept partial approval as an implicit edit. Rerender only the accepted changes as a new exact change set and ask for confirmation.

## Approved Profile Packet

Use for an approved initial profile or approved change:

```text
Approved Profile Packet
- Packet type: [Approved Initial Profile / Approved Change / Approved Removal]
- Opaque learner reference:
- Base effective profile and version: [none for initial profile]
- Named guardian:
- Approval date:
- Exact approved contents or removal scope:
- Approved preservation scope:
- Intended resulting version:
- State: Awaiting Persistence
```

For removal, preserve only the minimum audit fact and do not repeat removed sensitive content.

## Persistence Handoff

```text
Persistence Handoff
- Opaque learner reference:
- Approved packet reference:
- Prior effective version:
- Intended resulting version:
- Authorized operator:
- Tenant-private destination reference:
- Preservation confirmation: [pending / confirmed / failed]
- Confirmed effective version:
- Prior version no longer effective: [yes / no / not applicable]
- Final state: [Awaiting Persistence / Effective / Hold]
```

The skill prepares this handoff but does not write the store. Do not call a version `Effective` without operator confirmation. A failed or ambiguous preservation attempt leaves the prior version effective and produces `Hold`.

## De-identified Doctrine Candidate

```text
De-identified Doctrine Candidate
- Repeated pattern:
- Number and diversity of de-identified contexts:
- Bounded proposed improvement:
- Evidence that would weaken it:
- Privacy review: [pass / hold]
- Operator decision required:
- Repository mutation authorized: no
```

Exclude learner references, quotations, distinctive family facts, and real case chronology.
