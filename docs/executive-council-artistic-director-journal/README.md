# Artistic Director Journal

## Purpose

This is the Anyang Intelligence journal of the Executive Council Artistic
Director role. It begins on **2026-08-01**, the official human-holder start
date of JK's tenure, and continues across future human holders.

The journal is a public-safe observational and continuity surface. It does not
replace the [Executive Council role contract](../executive-council-role-contract.md),
[milestone record](../executive-council-artistic-director-milestones.md),
authority receipts, or the [Recursive Learning Ledger](../../os/recursive-learning-ledger.md).
It creates no authority and does not automatically create durable learning.

July 24–25 role migration and interim appointment records are historical
prehistory. They remain in the milestone record and dated receipts, but the
journal's first entry is 2026-08-01.

## Ownership and continuity

The journal belongs to the Artistic Director position, not to an individual
holder. Each entry identifies the active holder and tenure state. When a holder
changes, the outgoing tenure is closed and the incoming tenure is opened in the
same role-level sequence.

JK's `Second_Brain` repository remains independent. Public repository
observation may supply evidence to an entry, but it does not create ownership,
synchronization, edit permission, or technical linkage.

The Chief Executive is the canonical journal recorder. Corrections are
append-only: a later entry may correct or supersede an earlier entry, but the
earlier record is not silently rewritten.

## Daily entry contract

Each calendar day beginning 2026-08-01 receives one entry. A day with no
attributable activity receives an explicit no-change entry. Each entry contains:

- `entry_id`
- `date`
- `holder`
- `tenure_state`
- `recorder`
- `observation_window`
- `sources`
- `observed_activity`
- `returned_outputs`
- `developmental_assessment`
- `council_interpretation`
- `uncertainties`
- `continuity_implications`
- `promoted_records`
- `recursive_learning`

Developmental assessment may describe the fullest role development supported by
public or explicitly transmitted evidence. It must not claim access to private
thoughts or unobserved activity. Sensitive analysis belongs in Anyang private
state under the same entry ID, not in the public journal.

## Journal-to-ledger interface

The journal is the signal and evidence layer. The Recursive Learning Ledger is
the canonical durable-learning layer.

Each entry's `recursive_learning` section contains:

- `learning_candidate`: `none`, `candidate`, or `linked`;
- `rl_id`: populated only after a ledger entry exists;
- `signal_type`: `friction`, `failure`, `surprise`, `reusable success`, or `pattern`;
- `learning_statement`;
- `affected_surface`: `role`, `onboarding`, `AI collaboration`, `review`, `handoff`, `observation`, or `governance`;
- `proposed_durable_response`;
- `disposition`: `none` when there is no candidate, otherwise `pending`, `approved`, `rejected`, `deferred`, `superseded`, or the linked ledger state;
- `validation_reference`; and
- `outcome_reference`.

A journal entry may propose a candidate, but only a separately authorized
ledger action may create or update an `RL-*` row. Do not create a ledger row
for every daily observation.

The governed loop is:

~~~text
daily journal signal
  -> weekly or event-driven learning review
  -> candidate learning
  -> explicit human disposition
  -> durable operating change
  -> validation
  -> later observed outcome
~~~

The ledger states remain authoritative:

~~~text
candidate -> approved -> implemented -> validated -> observed
~~~

`deferred`, `rejected`, and `superseded` states remain visible. Implementation
or validator success does not prove improved behavior; later comparable-cycle
evidence is required for `observed`.

## Review cadence

- Daily: record the observation and possible signal.
- Weekly: review recurring friction, reusable success, and developmental
  patterns using the [weekly review template](weekly-review-template.md).
- Event-driven: review after a major failure, surprise, holder transition,
  authority incident, or significant project milestone.
- Monthly: reconcile the journal, milestones, open learning candidates, ledger
  states, and unresolved outcomes.

## Learning scope

Eligible recursive learning concerns role and system behavior:

- human-holder onboarding;
- AI collaboration and training;
- creative review and decision quality;
- successor continuity;
- observation and relay quality;
- authority, privacy, and membrane controls; and
- reusable operating methods.

Individual Grace Gems aesthetic choices remain project-local unless later
evidence demonstrates transferable role or system learning.

## Authority boundary

The journal does not authorize runtime activation, task approval, production,
publication, deployment, spending, client contact, rights clearance, or
external delivery. Those states require their controlling receipts and gates.
