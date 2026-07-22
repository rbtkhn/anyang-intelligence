# Executive–Interface Communication Protocol

## Purpose

This protocol standardizes communication between the Executive and the Interface without creating a new messaging system. It makes delegation, human-world context, uncertainty, escalation, and completion recoverable.

It applies first to Anyang internal work and the Grace Gems advisory boundary. It does not authorize external communication or Client-company action.

## Authority and roles

```text
Engineer -> Executive -> Interface -> Client boundary
```

- The Executive sends organizational task direction.
- The Interface observes, advises, drafts, coordinates, escalates, and executes only under a named approval.
- The Engineer retains highest authority and veto power.
- The Client retains authority over Client-company decisions.

No message type, status, receipt, or handoff creates authority by implication.

## Message types

The initial protocol uses `task`, `response`, `escalation`, and `receipt`. The vocabulary also reserves `question`, `challenge`, `correction`, `handoff`, `stop`, and `resume` for later pilot expansion.

## Shared vocabulary

Statuses: `Received`, `Clarifying`, `In progress`, `Waiting`, `Ready for review`, `Approved`, `Complete`, `Blocked`, `Declined`, `Escalated`, `Superseded`, `Withdrawn`.

Priorities: `FYI`, `Routine`, `Important`, `Urgent`, `Immediate stop`.

Authority modes: `Observe`, `Advise`, `Draft`, `Coordinate`, `Execute—approved`, `Escalate`, `Stop`.

## Lifecycle

```text
Executive task dispatch
  -> Interface clarification only when necessary
  -> Interface structured response
  -> Executive decision, revision, or escalation
  -> completion receipt or explicit blocked/declined outcome
  -> weekly review of ambiguity, correction, stale receipts, and burden
```

Batch routine work. Interrupt only for `Urgent`, `Immediate stop`, privacy, legal, safety, Client-authority, or deadline-critical events.

## Evidence discipline

The Interface must distinguish direct observations, explicit stakeholder statements, practical constraints, interpretation, unknowns, and unverified reports. A response is not approval, and a receipt confirms completion without creating authority.

## Pilot

Run a 2–4 week shadow-mode pilot using task, response, escalation, and receipt templates only. Track clarification requests, missing-scope returns, ambiguous-delegation rework, dispatch-to-response time, Interface burden, recommendation-changing escalations, stale receipts, authority violations, and Executive/Interface usefulness ratings.

Expand only after at least one success threshold is met: 25% less clarification or rework, 2+ hours/week saved, 90%+ receipt coverage, material escalation improvement, or zero authority/Client-boundary violations.
