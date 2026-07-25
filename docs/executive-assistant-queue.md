# Executive Assistant Queue

**Mode:** `shadow`

**Authority effect:** `none — this queue records state and does not approve,
dispatch, or execute work`

**Maintainer:** Chief Executive

**Scope:** Sanitized organization-level index of work actually dispatched to
the Executive Assistant.

## Queue rules

- Record one row per logical workflow, regardless of artifact count.
- Add a row only when a dispatch reaches the Executive Assistant or the
  Executive Assistant returns a blocked, declined, or escalated response to an
  attempted dispatch.
- Do not add recommendations, prepared-but-unsent drafts, or handoffs that have
  not reached the Executive Assistant.
- Link authority; do not infer it from a dispatch, status, relationship, or
  prior practice.
- Keep Anyang authority and client authority separate. Neither substitutes for
  the other.
- Use `capacity` only when Executive Assistant unavailability or deferral is
  explicitly reported. `Not sent` does not establish a capacity hold.
- A `Waiting` row must name a reason code and next owner.
- `Complete` requires linked returned evidence. No row may silently move from
  `Waiting` to `Complete`.
- Store no personal addresses, credentials, private-system locations, raw
  evidence, or protected client context here.
- Calculate age from the recorded timestamps at review time; do not maintain a
  manually aging value.

## Controlled values

**Authority:** `approved / held / missing / not applicable`

**State:** `Received / Clarifying / In progress / Waiting / Ready for review /
Approved / Complete / Blocked / Declined / Escalated / Superseded / Withdrawn`

**Reason code:** `authority / capacity / external-response / clarification /
dependency / none`

## Pilot service thresholds

These thresholds measure interface performance. They do not create action
authority, availability commitments, or a substitute interface.

| Priority | Acknowledgment threshold |
| --- | --- |
| `Immediate stop` | The stop is effective when issued; governed action holds immediately |
| `Urgent` | Within four known working hours |
| `Important` | Within one known working day |
| `Routine` | Within one known working day |
| `FYI` | Exclude unless a response or deliverable is requested |

When working availability is unknown, record the interval but do not label it a
threshold breach.

## Active queue

| Task and dispatch | Lane | Priority | Anyang authority | Client authority | State | Reason | Next owner | Dispatched at | Acknowledged at | Due | Last state change | Required evidence or receipt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EAQ-GG-2026-07-24-01` — [independent-channel strategic decision message](../projects/grace-gems/ceo-independent-channel-strategic-decision-message-2026-07-24.md) | Grace Gems | `Important` | `missing` — exact approval receipt not linked | `not applicable` to sending the request; client decision pending | `Waiting` | `external-response` | Grace Gems CEO | `Missing` — operator confirmed sent on 2026-07-24 | `Missing` | `Not set` | `Missing` — date only: 2026-07-24 | Technical delivery receipt and CEO response |

## Closed queue

Move a row here only after reconciliation. Preserve the same task ID and links.

| Task and dispatch | Final state | Closed at | Evidence or receipt | Reconciled by |
| --- | --- | --- | --- | --- |
