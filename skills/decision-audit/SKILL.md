---
name: decision-audit
description: Read-only audit of consequential decisions the agent made during proposed or completed work. Use explicitly for decision audits, assumption reviews, pre-commit judgment checks, or questions about choices the agent is least confident in; use implicitly before handoff or closeout only when an agent-selected architecture, behavior, authority, data, scope, contract, or state-label decision remains materially contestable or weakly evidenced.
---

# Decision Audit

Surface the few consequential agent decisions that still deserve evidence or
human review. Keep the audit sparse. Do not manufacture uncertainty merely to
appear reflective.

## Inspect The Decision Surface

Read the smallest relevant surface in this order:

1. The operator's request, selected branch, and explicit decisions.
2. The current diff or proposed artifact and its controlling repository files.
3. Tests, validation, evidence, and attributable decision or authority records.
4. Recent commits only when the request is historical.

Treat Git-only reconstruction as incomplete. A commit may reveal a candidate
decision, but only contemporaneous context, an attributable receipt, or an
explicit rationale can establish that the agent made it.

## Apply The Eligibility Gate

Report a decision only when all are true:

1. The agent selected among plausible alternatives.
2. The selection materially affects architecture, behavior, authority, data
   retention, project scope, public contracts, state meaning, safety, privacy,
   membranes, or reversibility.
3. The choice remains weakly evidenced, inferred, materially contestable, or
   dependent on an unconfirmed assumption.

Always surface an applicable authority, privacy, safety, or membrane concern.
Also inspect state labels such as `validated`, `approved`, `complete`, or
`authorized` when the evidence may prove only implementation structure rather
than the outcome a reasonable reader could infer.

Exclude:

- mechanical or stylistic choices with negligible consequences;
- decisions explicitly made by the operator, unless the agent materially
  interpreted or expanded their scope;
- requirements established by controlling repository evidence;
- unselected possibilities;
- reversible implementation details already bounded by tests and a stronger
  authoritative gate; and
- generic uncertainty unsupported by a concrete decision.

## Classify Evidence Honestly

Use one evidence level:

- `Outcome-supported`: observed behavior or results support the decision.
- `Structurally supported`: tests or validation establish form, invariants, or
  routing, but not the claimed operational outcome.
- `Missing`: no adequate supporting source is available.

Do not use numeric confidence without a defined calibration basis. Do not call
validator success outcome evidence.

## Produce The Audit

Prioritize by consequence if wrong, evidence weakness, and irreversibility.
Return no more than three findings. For each use:

```text
Decision:
- <what the agent decided>

Why it is uncertain:
- <missing evidence, inference, ambiguity, or competing objective>

Evidence used:
- <Outcome-supported / Structurally supported / Missing; source>

Strongest alternative:
- <credible alternative>

If wrong:
- <likely consequence and reversibility>

Authority boundary:
- <who may decide or approve>

Recommended disposition:
- Accept provisionally / Review / Hold
```

Use `Hold` as read-only advice only. It changes no ledger, claim, transaction,
approval, or repository state. When nothing qualifies, say: `No material
uncertain agent decision found.`

## Compose With Dream

During `dream`, run this audit only when the eligibility gate is satisfied by
current-session evidence. Show at most the highest-priority finding in an
optional section between integrity and tomorrow inheritance:

```text
Decision uncertainty:
- Review - Chose <X> over <Y> because <reason>. Evidence: <level and source>.
  If wrong: <consequence>. Authority: <decision owner>.
```

Omit the section entirely when nothing qualifies. Do not print reassuring
filler, ask a question, invoke Elicitation, update a decision log, or record a
Council event during Dream.

Keep Dream's deterministic CLI and JSON unchanged. Keep decision uncertainty
out of the external cadence handoff. Existing privacy, safety, authority,
validation, dirty-worktree, synchronization, and paid-obligation priorities
remain controlling; an ordinary reversible uncertainty must not displace a
higher-priority closeout issue.

## Route Without Persisting

- Route a selected missing human judgment to `elicitation`.
- Route a possible request-versus-control conflict to Elicitation's structured
  contradiction preflight.
- Link an existing Council transaction rather than duplicating it.
- Recommend a project decision-log or Council update only as a separately
  authorized later action.
- Use `learn-from-choices` for resolution paths without changing action
  authority.
- Keep `review-ai-harness` separate: it reviews agent infrastructure, while
  this skill reviews decisions made during the work.

Persist nothing automatically. Do not expose customer-private evidence or
interpret silence, repeated selection, praise, or dissatisfaction as approval.

## Provenance

The core retrospective question is adapted from David Ondrej's `decisions`
skill. This Anyang-native version adds materiality, evidence, authority,
membrane, persistence, and closeout boundaries.

## Done When

The operator sees only material agent-selected decisions, the evidence level
and strongest alternative are visible, historical inference remains labeled,
and no review finding silently changes authority or durable state.
