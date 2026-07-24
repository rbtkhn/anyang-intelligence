# Business Capability Skill Architecture

**Status:** Core architecture implemented; synthetic end-to-end and lifecycle forward-tests passed  
**Date:** 2026-07-24  
**Scope:** `business-intake`, `business-plan`, and `business-loop`

## Purpose

Define three distinct skills that move a business from verified context to
chosen direction to repeatable learning without collapsing evidence, approval,
planning, and action into one workflow.

```text
business-intake
  -> effective business context
  -> business-plan
  -> approved plan priority
  -> business-loop
  -> approved loop specification
  -> bounded-workflow-pilot
  -> evidence and learning
  -> loop, plan, or context review
```

## Core separation

| Skill | Truth object | Primary question | Must not imply |
| --- | --- | --- | --- |
| `business-intake` | Business context | What is confirmed, missing, authorized, and safe to use? | That discussion, access, or context approval authorizes work |
| `business-plan` | Business plan | Given the effective context, what choices should the owner approve? | That a recommendation, forecast, or approved plan authorizes execution |
| `business-loop` | Operating-loop specification | How should one approved priority repeatedly produce decisions, evidence, and learning? | That loop design authorizes deployment, publication, spending, or customer impact |

## Shared doctrine

All three skills must:

- distinguish confirmed facts, estimates, hypotheses, interpretations, and
  missing evidence;
- preserve owner authority and data membranes;
- use bounded evidence requests tied to a named decision;
- keep private customer, order, supplier, employee, and financial records
  outside Git;
- separate preparation, approval, persistence, activation, and external action;
- treat silence, interest, access, discussion, and continuity as non-approval;
- end with an explicit state and next human decision;
- preserve `No action taken` when authority is absent.

## 1. Refine `business-intake`

### Proposed trigger contract

Use for initial business intake, changes to an effective business context,
verified meeting capture, intake handoffs, phased intake continuation, and
owner-response capture.

Support three explicit modes:

- `$business-intake create`: establish the first approved context.
- `$business-intake resume`: continue an incomplete intake from a verified,
  version-bound checkpoint.
- `$business-intake change`: evaluate new evidence against an effective
  context.

Allow read-only orientation from a clearly supplied intake handoff without
private questioning. Require an explicit mode before collecting private
business evidence or producing an approval packet.

### `resume` mode

Require:

- business reference;
- latest intake handoff or receipt;
- current phase and status;
- confirmed owner and authority boundary;
- current privacy and evidence limits;
- unresolved decision;
- evidence added since the checkpoint.

Then:

1. Verify that the checkpoint belongs to the same business and intake case.
2. Separate confirmed owner statements from preparation hypotheses.
3. Capture meeting corrections, priorities, constraints, authority, evidence
   permissions, success metric, review date, and status.
4. Preserve all unresolved fields as `Missing`, `Proposed`, or `Hold`.
5. Prepare only the next bounded intake artifact.
6. Do not infer operating-review or implementation authority.

### Phase model

| Phase | Purpose | Exit evidence |
| --- | --- | --- |
| Phase 1: orientation | Identify the business, owner, purpose, and safe intake boundary | Owner Authority and Data Receipt |
| Phase 2: deeper intake | Verify priorities, constraints, economics, capacity, customer promises, and evidence paths | Verified capture plus readiness packet |
| Context approval | Show the complete proposed context for exact owner decision | Approved Business Context Packet |
| Persistence | Preserve the approved context outside Git | Operator-confirmed persistence receipt |
| Review gate | Ask separately whether one bounded operating review is authorized | First-review decision and brief |

Phase progression does not imply context effectiveness or action authority.

### New or revised outputs

- verified meeting capture;
- intake continuation receipt;
- owner correction record;
- bounded evidence request;
- first-review decision receipt;
- handoff packet carrying phase, state, authority, evidence boundary, open
  decisions, and next gate;
- existing authority, readiness, proposed-context, approved-context, and
  persistence packets.

### Resource plan

Keep the existing `SKILL.md`, `references/question-strategy.md`, and
`references/output-contracts.md`. Add only if the existing output-contract
reference cannot absorb them cleanly:

- `references/continuation-contract.md` for checkpoint and handoff fields;
- `references/meeting-capture-contract.md` for verified post-meeting capture.

Do not add scripts unless repeated packet validation proves error-prone.

## 2. Create `business-plan`

### Proposed trigger contract

Use when an owner asks to create, revise, compare, or approve a business plan,
strategic plan, 30/90-day plan, segment strategy, channel strategy, or
evidence-backed growth plan from an effective business context.

Support:

- `$business-plan create`;
- `$business-plan resume`;
- `$business-plan change`.

Use `resume` only for a version-bound incomplete plan or approved replacement
awaiting persistence. Route an effective plan to `change`.

### Required inputs

- business reference;
- latest effective context and version;
- context approval and persistence receipt;
- planning authority and named decision owner;
- planning purpose and time horizon;
- decision the plan must support;
- approved evidence and privacy boundary;
- current constraints and non-negotiables;
- success measures and review date.

Return `Hold` when the effective context, planning authority, objective,
economics required for the decision, capacity boundary, or evidence path is
missing.

### Plan workflow

1. Confirm the effective context and plan authority.
2. Define the plan question, horizon, and exclusions.
3. Separate facts, assumptions, scenarios, and unknowns.
4. Identify strategic choices, tradeoffs, and explicit non-choices.
5. Define customer, value proposition, segment, channel, capability, capacity,
   economics, and risk implications only to the evidence-supported depth.
6. Define objectives, leading indicators, outcome metrics, guardrails, and
   review cadence.
7. Propose a bounded learning agenda rather than invented certainty.
8. Show the complete proposed plan for owner approval, revision, deferral, or
   rejection.
9. Preserve the exact approved plan outside Git and require a version-matched
   persistence receipt before it becomes effective.
10. Preserve plan approval and effectiveness separately from execution
    authority.

### Required plan sections

- decision summary;
- effective-context reference;
- current state and evidence quality;
- strategic choices and exclusions;
- customer, value proposition, segment, and channel;
- operating capabilities and capacity constraints;
- economics with explicit assumptions and scenarios;
- objectives, metrics, and guardrails;
- risks, dependencies, and missing evidence;
- 30/90-day learning agenda;
- proposed operating loops;
- owner decisions and review date;
- authority and data boundary;
- status.

### Output states

- `Hold`;
- `Proposed`;
- `Awaiting Persistence`;
- `Effective - not activated`;
- `Rejected`;
- `Deferred`;
- `Change proposed`.

An approved plan remains ineffective until persistence is confirmed and
non-operative until the owner separately authorizes the relevant loop, pilot,
or action.

### Resource plan

Initialize with:

```text
skills/business-plan/
  SKILL.md
  agents/openai.yaml
  references/
    output-contracts.md
    evidence-and-scenario-rules.md
```

Do not add a generic business-plan template asset unless repeated use shows the
output contract is insufficient.

## 3. Create `business-loop`

### Proposed trigger contract

Use when an owner wants to design, revise, review, pause, or retire one
repeatable business operating loop tied to an approved plan priority or an
explicit standalone loop-design authorization.

Use the operator-selected name `business-loop`. Preserve the business-specific
trigger and operating-loop contract so it remains distinct from software and
automation loops.

Support:

- `$business-loop design`;
- `$business-loop resume`;
- `$business-loop change`;
- `$business-loop review`;
- `$business-loop pause`;
- `$business-loop retire`.

Use `resume` for an incomplete version-bound specification or governed
reactivation of `Paused`. Use `pause` for a reversible stop and `retire` for
terminal closure; never resume `Retired`.

### Required inputs

- business reference and effective context version;
- approved plan priority or explicit loop-design authority;
- named loop owner and decision owner;
- signal and decision the loop supports;
- permitted actions and prohibited actions;
- evidence source and private-data location;
- cadence, success metric, burden guardrail, and stop conditions.

### Loop grammar

Each loop specification must define:

- signal;
- memory objects;
- decision prepared;
- owner and approval authority;
- authorized action path;
- evidence and receipts;
- cadence and service expectation;
- metrics and burden guardrails;
- exceptions and escalation;
- pause and stop conditions;
- learning update;
- governance and data membrane.

### Workflow

1. Confirm context, plan linkage, and loop-design authority.
2. Name one decision and one loop owner.
3. Map the current workflow and evidence gaps.
4. Design the smallest viable loop.
5. Define the human approval points and prohibited actions.
6. Define measurement, burden, exceptions, and review cadence.
7. Produce a loop specification and pilot recommendation.
8. Preserve the exact approved specification outside Git and require a
   version-matched persistence receipt.
9. Require separate approval of the exact pilot scope before invoking
   `bounded-workflow-pilot`.
10. Use pilot evidence to recommend `Adopt`, `Revise`, `Hold`, or `Retire`.
11. Route changed business facts to `$business-intake change`; route changed
    strategic choices to `$business-plan change`.

### Output states

- `Draft`;
- `Awaiting Persistence`;
- `Approved - pilot pending`;
- `Approved for pilot`;
- `Hold`;
- `Active` only with an operator-confirmed activation receipt;
- `Paused`;
- `Retired`.

The skill designs and reviews loops. It does not execute the workflow or grant
itself activation authority.

### Resource plan

Initialize with:

```text
skills/business-loop/
  SKILL.md
  agents/openai.yaml
  references/
    loop-contract.md
    output-contracts.md
```

Reuse `docs/loops.md` as canonical doctrine. Do not duplicate it in the skill.

## Handoff rules

| From | To | Required handoff |
| --- | --- | --- |
| `business-intake` | `business-plan` | Effective context version, approval and persistence receipts, planning authority, evidence boundary |
| `business-plan` | `business-loop` | Effective plan and version, approval and persistence receipts, approved priority, objective, metric, guardrails, owner, loop-design authority |
| `business-loop` | `bounded-workflow-pilot` | Persisted approved loop specification, specification approval and persistence receipts, route, exact pilot scope, run limit, reviewer, evidence, stop conditions |
| Pilot evidence | Loop review | Run receipts, exceptions, quality, burden, owner decision |
| Loop learning | Plan change | Evidence that changes a strategic choice, objective, allocation, or risk |
| Loop or plan learning | Intake change | Evidence that changes a durable business fact, authority, economics, capacity, or data boundary |

## Overlap boundaries

- Use `intent-recovery` only to clarify owner language; never to invent facts,
  economics, authority, or approval.
- Use `tax-financial-governance` for money classification and tax-sensitive
  decisions.
- Use domain skills for evidence review and domain-specific recommendations.
- Use `project-state-update` only for a separate authorized sanitized
  repository update.
- Use `bounded-workflow-pilot` for either a persisted, approved manual-loop
  pilot handoff or an approved automation pilot.
- Require `automation-value-proof` whenever the pilot contains automation;
  never use the manual route to bypass it.

## Validation plan

### Static validation

1. Run the skill-creator quick validator for each skill folder.
2. Run the repository's canonical validation launcher.
3. Verify frontmatter triggers are mutually distinguishable.
4. Verify every output has one explicit state and human decision.

### Forward-test scenarios

1. A CEO meeting handoff contains priorities but no action approval.
2. A public storefront review is authorized while private business context
   remains ineffective.
3. A user requests a business plan without verified margins or capacity.
4. An approved plan priority lacks a loop owner or cadence.
5. Pilot evidence contradicts the current plan.
6. New evidence changes a durable business fact and must return to intake
   change.

Success requires correct routing, bounded evidence requests, no invented facts,
and no approval leakage.

## Implementation sequence

1. Refine and validate `business-intake`, including `resume`.
2. Forward-test intake against the anonymized meeting-handoff scenario.
3. Create and validate `business-plan`.
4. Forward-test planning with missing economics and capacity.
5. Create and validate `business-loop`.
6. Forward-test loop design and pilot routing.
7. Run one end-to-end simulated handoff across all three skills.

No skill implementation is authorized by this architecture document alone.
