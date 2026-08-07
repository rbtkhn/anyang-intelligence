# Executive Assistant–Artistic Director Relay Protocol

**Purpose:** Define how the Executive Assistant transmits Chief Executive
instructions to the human Artistic Director and returns the Artistic Director's
output for review.

**Status:** Operating design  
**Scope:** Internal Artistic Director development and approved creative work  
**External action:** Not authorized by this protocol

## Governing rule

The Executive Assistant is the relay and evidence-return interface. The
Executive Assistant carries the instruction faithfully, receives the response
faithfully, and reports what happened.

The Executive Assistant does not silently rewrite the objective, add creative
direction, approve the output, expand the scope, or convert a human Artistic
Director response into a client commitment.

The Chief Executive prepares the learning objective and decision context. The
System Engineer's approval or standing mandate must support any bounded
Artistic Director task that persists work or consumes material capacity. The
human Artistic Director owns creative execution within the approved boundary.

## Normal relay loop

```text
Chief Executive prepares bounded instruction
  -> required authority and scope fields are checked
  -> Executive Assistant transmits the instruction verbatim
  -> human Artistic Director works in the independent Second_Brain
     projects/artistic-director/ project
  -> human Artistic Director returns output and evidence
  -> Executive Assistant returns the response without silent alteration
  -> Chief Executive evaluates fit, risks, and next decision
```

The loop pauses when the Executive Assistant is unavailable, the instruction
changes, the response is incomplete, or a new authority question appears.

## Outbound instruction requirements

Before transmitting, the Chief Executive provides the Executive Assistant with
one complete instruction containing:

- Relay ID:
- Date:
- Human Artistic Director:
- Objective:
- Decision context:
- Approved task or standing mandate:
- Lane or subject:
- Permitted source material:
- Prohibited source material:
- Requested output state: `explore / shortlist / brief / draft / review-ready`;
- Exact deliverables:
- Material-capacity limit:
- Budget limit, if any:
- Claims, rights, privacy, and representation cautions:
- Required questions for the human Artistic Director:
- Creative-intent context, if applicable:
- Known interpretation or unresolved creative ambiguity:
- State before transmission: `proposed / internal exploration / draft /
  review-ready / awaiting approval / approved for external delivery`;
- Intended state after receipt:
- Audience and external-status boundary: `internal / client review /
  public / other`;
- Authority permitting any state transition:
- Evidence gate for the transition:
- Evidence to return:
- Expiry or response date:
- Stop conditions:
- Next decision owner:

The Executive Assistant should transmit the instruction as written, adding only
a short cover note that identifies the Relay ID and requests confirmation of
receipt.

## Executive Assistant transmission template

```text
Subject: Artistic Director instruction [Relay ID]

Hi [name],

I am transmitting the attached instruction from the Chief Executive.

Please treat the attached instruction as the complete task boundary. Do not
assume authority beyond what it states. Please confirm receipt, identify any
unclear or missing field, and return your work with the requested evidence.

Relay ID: [ID]
Response requested by: [date or no fixed date]

Executive Assistant transmission note:
- Transmitted without substantive changes: yes / no
- Changes or clarifications made: [none or exact description]
- Time transmitted:
```

If the Executive Assistant believes the instruction needs clarification, do
not rewrite it. Return it to the Chief Executive with the question.

## Human Artistic Director response requirements

The human Artistic Director should return:

- Relay ID;
- receipt confirmation;
- status: `explore / shortlist / brief / draft / review-ready / hold / reject`;
- work product or repository path;
- sources used;
- alternatives considered;
- creative reasoning;
- claims, rights, privacy, or representation uncertainties;
- time or material capacity used;
- deviations from the instruction;
- questions requiring a decision;
- reuse opportunities; and
- the next permitted action requested.

The human Artistic Director's output is not automatically approved for client
use, delivery, publication, spending, claims, or external representation.

## Intent-recovery fields

When a relay includes creative feedback, an aesthetic reaction, a reference
choice, or a revision request, preserve the following fields separately from
the ordinary task and output fields:

- **Human's exact words:** the original reaction or request;
- **Recovered creative intent:** the likely distinction beneath the words;
- **Clearer articulation:** a first-person statement the human could adopt or
  correct;
- **Creative implication:** what should change in the work if the articulation
  is correct;
- **Alternative interpretation:** another plausible reading when it would lead
  to a materially different revision;
- **What remains unestablished:** facts, rights, claims, budget, approval,
  publication, or client direction not supplied by the response; and
- **Lesson state:** `accepted / corrected / rejected / held / project-specific`.

For every material relay, also preserve the state-transition fields:

- **State before transmission:** what status the work or request currently has;
- **Intended state after receipt:** what status the instruction is meant to
  create, if any;
- **Audience and external-status boundary:** who may see or receive the work;
- **Authority permitting the transition:** the approval or standing mandate;
- **Evidence gate:** what must be verified before the transition is complete;
- **Transition result:** whether the state changed, remained unchanged, or is
  held; and
- **Next decision owner:** the person or authority who must decide the next
  state.

The Executive Assistant must hold the relay when the requested transition is
not explicit, when the authority is absent or incompatible, or when the
evidence gate is not satisfied.

The Executive Assistant may transmit these fields when they are already
explicitly supplied, but should not invent or finalize the recovered intent.
When the interpretation is newly inferred, the human Artistic Director must
confirm, correct, reject, or hold it before it becomes a reusable lesson.

## Executive Assistant return template

```text
Subject: Artistic Director response [Relay ID]

Relay ID: [ID]
Human Artistic Director response received: [time]
Response status: [status]
Repository or artifact path: [path or link]

Returned without substantive changes: yes / no
Changes or compression made: [none or exact description]

Output received:
- [file, link, or concise description]

Evidence received:
- [sources]
- [alternatives]
- [reasoning]
- [time/capacity]
- [deviations]
- [rights/claims/privacy uncertainties]
- [open questions]

Intent recovery, when applicable:
- Human's exact words:
- Recovered creative intent:
- Clearer articulation:
- Creative implication:
- Alternative interpretation:
- What remains unestablished:
- Lesson state: [accepted / corrected / rejected / held / project-specific]

Executive Assistant observation, kept separate from the Artistic Director's
response:
- Transmission or receipt issue:
- New fact:
- Scope change:
- State before transmission:
- Intended state after receipt:
- Audience and external-status boundary:
- Authority permitting transition:
- Evidence gate:
- Transition result: [changed / unchanged / held / escalated]
- Next decision owner:
- Escalation required: yes / no
```

The Executive Assistant should preserve the Artistic Director's original words
and links. A summary may be added, but it must be labeled as the Executive
Assistant's summary and must not replace the source response.

## Stop and escalate

The Executive Assistant must stop the relay and return the matter for review
when:

- the instruction is missing approval, scope, expiry, or evidence requirements;
- the human Artistic Director asks for private data, new tools, spending, or
  external access;
- the objective or client direction changes;
- claims, rights, privacy, likeness, or product accuracy is uncertain;
- the response implies approval, publication, delivery, or commitment;
- a client or third party attempts to task the Artistic Director directly;
- the Executive Assistant would need to choose between conflicting authorities;
  or
- the human Artistic Director is unavailable or declines the task.

No relay continuation is inferred from silence, a polished artifact, prior
practice, or urgency.

## Attribution and records

Each relay should preserve three distinct attributions:

1. **Chief Executive:** prepared the objective and decision context.
2. **Executive Assistant:** transmitted and returned the evidence.
3. **Artistic Director:** made the creative judgments and produced the work.

If the Executive Assistant adds interpretation, it belongs in a separately
labeled observation field. If the human Artistic Director changes the AI's
working method, that learning remains attributable to the human until it is
deliberately accepted into durable role memory.

## Minimal first use

For the first relay, use one small, job-neutral calibration task. Do not start
with a live client campaign. The first receipt should prove that:

- the instruction was understood;
- the relay preserved the instruction;
- the Artistic Director returned the requested evidence; and
- the Executive Assistant preserved the distinction between transmission,
  creative output, and evaluation.
