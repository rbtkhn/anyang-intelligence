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
  -> human Artistic Director works in the OB1 artistic-director/ folder
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

Executive Assistant observation, kept separate from the Artistic Director's
response:
- Transmission or receipt issue:
- New fact:
- Scope change:
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

