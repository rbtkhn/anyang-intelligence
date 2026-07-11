# Permissions and Authority Review Gate

This primitive is a review gate for agentic workflows that look capable in demos or bounded turns but still fail to create trustworthy value because permissions, approval logic, spending authority, signing authority, or workflow access remain unresolved.

Its purpose is to prevent false confidence when orchestration quality outruns real operating authority.

Use with:

- [README.md](README.md)
- [ambient-agency-review-gate.md](ambient-agency-review-gate.md)
- [acceleration-source-verification-gate.md](acceleration-source-verification-gate.md)
- [../turn-usefulness-scorecard.md](../turn-usefulness-scorecard.md)
- [../../../docs/membranes.md](../../../docs/membranes.md)

## Operating Rule

Default state: `watch` or `hold` until the workflow's real authority boundaries are visible.

This gate does not ask whether the model can do the work. It asks whether the workflow is actually allowed to finish the work safely.

## What Counts As A Permissions And Authority Problem

Apply this gate when a workflow can reason, draft, or plan well, but value still depends on unresolved questions such as:

- Can it access the needed data?
- Can it use the needed tools or APIs?
- Can it spend money?
- Can it sign, submit, or publish?
- Can it trigger a downstream workflow?
- Can it contact a human, customer, donor, parent, contractor, or board member?
- Can it complete the turn without quietly inventing authority it does not have?

Examples include:

- strong draft agents blocked by approval bottlenecks
- task runners that can plan but cannot execute safely
- copilots that imply commitment before owner review
- research-to-lane translations that outrun membrane review
- enterprise or lane workflows where permissions are more limiting than intelligence

## Core Questions

1. What real-world action is the workflow trying to finish?
2. Which step is blocked by missing permission or unclear authority?
3. Is the bottleneck data access, tool access, spend, sign-off, publication, outreach, or override?
4. If the agent were stronger, would the workflow still stall at the same point?
5. Is the current review step meaningful, or only symbolic after most decisions were already made?
6. What must always return to a human no matter how good the orchestration becomes?

## Review Dimensions

| Dimension | What to ask | Typical warning sign |
| --- | --- | --- |
| Data access | Can the workflow see the information it actually needs? | The system looks helpful but repeatedly asks for missing context or works from stale fragments |
| Tool authority | Can it use the systems that matter, not just describe them? | Outputs are polished but execution still requires manual copy-forward |
| Spend authority | Could it commit funds, purchases, or paid actions? | The workflow implies action while real money still sits outside review |
| Sign / send authority | Could it submit, publish, notify, or represent the lane externally? | Drafting is mistaken for approval-ready execution |
| Approval integrity | Does human review happen before the point of no return? | Review exists on paper but most practical decisions are already locked in |
| Override / fallback | Can a human stop, inspect, redirect, or take over cleanly? | When the workflow gets stuck, responsibility becomes ambiguous |

## Lane Review Prompts

### Singularity Science

- Is the workflow only extracting and translating, or is it starting to imply downstream commitments before membrane review?
- Could research artifacts silently harden into lane doctrine because authority boundaries are underspecified?
- Are we mistaking a strong memo for a safely routable operating change?

Recommended default: `watch`

### Media Production

- Can the workflow draft, or is it beginning to imply publish, rights, contractor, or client authority?
- Does polished asset review hide the fact that approval, rights clearance, or delivery still depends on manual choke points?
- Would stronger tool access reduce friction, or would the real bottleneck still be human review?

Recommended default: `watch`

### Grace Gems

- Is the system helping prepare owner review, or is it drifting toward pricing, customer promise, or listing authority?
- Could the workflow send, update, or commit something the owner has not meaningfully reviewed?
- Is the blocker really intelligence, or simply owner approval and marketplace trust?

Recommended default: `watch`

### Learning Core

- Does the workflow stay firmly inside parent and adult authority, or is it beginning to act as if child-facing permission already exists?
- Could a strong tutoring or intake workflow create pressure to skip adult approval because the output looks complete?
- Are approval and supervision still visible before any child-facing step?

Recommended default: `hold`

### retired Non-Profit project

- Can the workflow draft governance material without implying donor, board, grant, or stewardship authority?
- Are board review and donor review still meaningful, or are they becoming ceremonial after the packet is assembled?
- Does the workflow surface what evidence is still missing before a claim is shared externally?

Recommended default: `watch`

### Mountain Villa

- Is the workflow only surfacing risk, or is it drifting toward contractor, safety, access, or emergency authority?
- Would better automation help, or does the real bottleneck remain human judgment, property access, or fallback responsibility?
- If the system acts on a signal, who can stop or override it quickly?

Recommended default: `watch`, with `hold` for safety-critical use

## Status Guidance

- `watch`: recurring pressure exists, but authority boundaries are still mostly manual or unclear
- `candidate`: the pattern repeats enough to preserve as a reusable lane or cross-lane gate
- `test`: a narrow, reversible, clearly supervised workflow has explicit authority boundaries
- `hold`: execution pressure is outrunning approval integrity or membrane discipline
- `adopted`: a human has approved the gate as part of a lane's normal review sequence

## Output Shape

When this gate is applied, capture:

```text
Lane:
Workflow or turn:
Target action:
Blocked authority point:
Type of permission gap:
What the system can finish safely:
What must return to human approval:
Override path:
Main authority risk:
Default state:
What stays inside Singularity Science:
```

## Boundary

Do not use this gate to argue that more tool access is always the answer.

Sometimes the constraint is correctly human. The point is to distinguish:

- missing enablement that can be designed cleanly
- from authority that should remain visibly human

Route only the governance question: where does a workflow stop being useful because authority, not intelligence, is the real bottleneck?
