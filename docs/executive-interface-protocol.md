# Executive–Interface Communication Protocol

## Purpose

This protocol standardizes communication between the Executive and the Interface without creating a new messaging system. It makes delegation, human-world context, uncertainty, escalation, and completion recoverable.

It applies first to Anyang internal work and the Grace Gems advisory boundary. It does not authorize external communication or Client-company action.

## Authority and roles

```text
Engineer authorization
  -> Chief Executive dispatch
  -> Executive Assistant action
  -> evidence return

Client CEO authority
  -> client decision or evidence authorization
  -> Executive Assistant action when compatible Anyang authority also exists
```

- The Chief Executive is the normal tasker of the Executive Assistant, but only
  within an exact Engineer approval or current standing mandate.
- The Interface observes, advises, drafts, coordinates, escalates, and executes only under a named approval.
- The Engineer retains highest authority and veto power.
- The Client retains authority over Client-company decisions.

No message type, status, receipt, or handoff creates authority by implication.

## Valid dispatch requirements

A dispatch is valid only when it identifies:

- task ID and objective;
- current Anyang authority;
- applicable client authority;
- permitted authority mode;
- recipients, systems, or evidence surface;
- limits and prohibited actions;
- required return evidence;
- expiration or review date;
- escalation and stop conditions.

A message type, priority, status, prior practice, or relationship does not cure
a missing authority field.

## Message types

The initial protocol uses `task`, `response`, `escalation`, and `receipt`. The vocabulary also reserves `question`, `challenge`, `correction`, `handoff`, `stop`, and `resume` for later pilot expansion.

## Shared vocabulary

Statuses: `Received`, `Clarifying`, `In progress`, `Waiting`, `Ready for review`, `Approved`, `Complete`, `Blocked`, `Declined`, `Escalated`, `Superseded`, `Withdrawn`.

Priorities: `FYI`, `Routine`, `Important`, `Urgent`, `Immediate stop`.

Authority modes: `Observe`, `Advise`, `Draft`, `Coordinate`, `Execute—approved`, `Escalate`, `Stop`.

## Lifecycle

```text
Chief Executive prepares bounded dispatch
  -> Executive Assistant validates authority
  -> Received / Clarifying / Declined / Escalated
  -> approved action when valid
  -> evidence returned
  -> Chief Executive reconciliation
  -> Steward review only at a scheduled or exception gate
  -> complete, corrected, blocked, or superseded
```

Batch routine work. Interrupt only for `Urgent`, `Immediate stop`, privacy, legal, safety, Client-authority, or deadline-critical events.

## Refusal and escalation

The Executive Assistant returns `Declined`, `Blocked`, or `Escalated` without
acting when:

- approval is missing, expired, contradictory, or broader than the task;
- Engineer authority is being treated as client-company authority;
- client approval is being treated as Anyang system authority;
- recipient or decision authority is unclear;
- scope, audience, channel, access, retention, or success condition is missing;
- the task introduces money, claims, commitments, privacy exposure, or business
  change outside the approved scope;
- the required evidence exceeds the approved minimum;
- real conditions materially differ from the approved handoff.

Stopping, requesting clarification, reporting deviation, and returning evidence
are safeguard actions. They do not create authority to originate new work.

## Queue and availability

Maintain a recoverable Executive Assistant queue containing task ID, priority,
authority state, owner, deadline, age, current status, and required evidence.

Batch routine work. Define acknowledgment and escalation targets during the
pilot. No task may silently move from `Waiting` to `Complete`.

If the Executive Assistant is unavailable, external action holds. The Engineer
may authorize a named, time-bounded exception; no automatic substitute
interface is created.

## Evidence discipline

The Interface must distinguish direct observations, explicit stakeholder statements, practical constraints, interpretation, unknowns, and unverified reports. A response is not approval, and a receipt confirms completion without creating authority.

## Pilot

Run a 2–4 week shadow-mode pilot using task, response, escalation, and receipt templates only. Track clarification requests, missing-scope returns, ambiguous-delegation rework, dispatch-to-response time, Interface burden, recommendation-changing escalations, stale receipts, authority violations, and Executive/Interface usefulness ratings.

Expand only after at least one success threshold is met: 25% less clarification or rework, 2+ hours/week saved, 90%+ receipt coverage, material escalation improvement, or zero authority/Client-boundary violations.
