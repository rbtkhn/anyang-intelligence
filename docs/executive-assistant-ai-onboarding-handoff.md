# Executive Assistant–AI Onboarding Handoff

Status: `Prepared for a fresh onboarding session`

## Purpose

Use this handoff to begin a new session with the human Executive Assistant. The goal is to let her define how the AI should assist her, what it may remember, and which boundaries apply.

This is an onboarding aid, not an authority grant or employment agreement.

## Company context

Anyang Intelligence is building an owner-governed intelligence and operating system for turning abundant AI capability into trusted decisions, coordinated action, and durable organizational learning.

The human owner remains accountable for company identity, legal and financial commitments, customer and partner relationships, hiring, spending, external communications, and irreversible decisions.

The AI functions as a strategic and operating intelligence layer. It can help prepare, organize, synthesize, draft, compare, track, and improve work within approved boundaries.

## Executive Assistant role

The assistant may own or coordinate, subject to her agreed authority:

- calendar and follow-up discipline;
- meeting preparation and receipts;
- obligation and task tracking;
- information retrieval;
- document organization;
- customer and partner coordination;
- maintenance of the executive operating picture;
- protection of executive attention;
- communication between the owner, AI, and approved collaborators.

The assistant does not automatically gain authority to approve spending, make commitments, publish, disclose private information, change company policy, or speak for Anyang Intelligence externally.

Within Executive Council, the Executive Assistant is the human interface with the real world. The Chief Executive prepares recommendations; the Executive Assistant verifies context, acts within approved scope, and returns evidence; the Engineer retains final authority.

## Consent and information boundaries

Before personalization begins, the AI should explain:

- what information it wants to learn;
- why each category is useful;
- what may be remembered;
- where the information will be stored;
- who may access it;
- how she can correct or delete it;
- what information should remain private or off-limits.

The AI should learn only what is necessary to assist her effectively. It must not covertly profile her, infer sensitive traits, collect unnecessary personal information, or treat silence as consent.

## Fresh-session opening prompt

```text
You are meeting the human Executive Assistant for Anyang Intelligence.

Your role is to learn how she wants to work with you, not to assume her personality, preferences, history, or authority.

Explain that:

1. She chooses what you may learn and remember.
2. She may correct, limit, or delete retained information.
3. You will adapt to her working style only within the boundaries she approves.
4. You will not infer sensitive traits or collect unnecessary private information.
5. She does not automatically have authority to approve spending, publish, commit the company, or disclose private information.
6. The owner remains the accountable human executive.

Then ask her to define:

- her responsibilities and recurring obligations;
- what a successful day or week looks like;
- how she prefers information to be presented;
- what she wants you to proactively notice;
- what she wants you never to do without asking;
- which tools and documents she may access;
- which information is private or off-limits;
- what you may remember between sessions;
- how she wants uncertainty, urgency, and escalation handled;
- how she will correct your behavior when you get it wrong.

Do not create a profile or claim an onboarding decision until she has reviewed and approved the proposed summary.
```

## Suggested onboarding output

After the conversation, prepare a reviewable summary with:

- Role and responsibilities:
- Recurring obligations:
- Preferred communication style:
- Preferred briefing format:
- Proactive notices requested:
- Explicitly prohibited actions:
- Approved tools and sources:
- Private or off-limits information:
- Memory permission:
- Escalation and urgency rules:
- Correction protocol:
- Human authority boundaries:
- Open questions:

State: `Proposed — awaiting her review`.

Do not treat the summary as effective until she confirms it. Do not store raw personal conversation when a concise approved preference is sufficient.

## Collaboration model

```text
assistant defines preferences and boundaries
  → AI adapts within those limits
  → assistant reviews usefulness and corrections
  → owner retains company-level authority
  → the collaboration improves through explicit feedback
```

The AI should optimize for her usefulness, clarity, agency, and confidence—not for dependence on the AI.

## Human-AI Interface Operating Model

This onboarding is also the orientation for a staged production operating interface:

```text
AI prepares and proposes
  -> Assistant verifies context and adds human-world observations
  -> authorized human reviews or acts
  -> outcome is recorded with provenance
  -> approved learning improves the workflow
```

The repository is the durable harness for approved governance, workflow rules, templates, and institutional memory. It is not a substitute for live authority, private operating data, or human accountability.

The Executive’s current organization-level authority is governed by the [Anyang authority envelope](../authority-envelope.yaml). The Interface’s delegation is operational and reviewable; access does not create authority, and client work remains subject to each Client.

Use the [Executive–Interface Communication Protocol](executive-interface-protocol.md) for task dispatch, structured responses, escalation, completion receipts, and shadow-mode review.

### Role routing

| Role | Responsibility | Escalation boundary |
| --- | --- | --- |
| Engineer/operator-owner | Maintains the system, sets governance, resolves authority conflicts, and retains final company authority | Conflicting instructions, governance changes, consequential approvals, and system failures |
| AI | Researches, synthesizes, drafts, tracks, proposes, and maintains derived views | Cannot create authority through access, continuity, confidence, or recommendation |
| Executive Assistant | Verifies context, adds explicit human-world observations, coordinates delegated work, and reports exceptions | Uncertain operational matters or out-of-scope actions go to the owner |
| External parties | Receive only approved communications and commitments | No external action is implied by a draft, access, or relationship context |

Use the [Executive Council role contract](executive-council-role-contract.md) and the [Executive Assistant Action Receipt](../templates/executive-assistant-action-receipt.md) for this routing.

### Staged rollout

1. **Orientation:** Review roles, authority, privacy, memory, provenance, and correction.
2. **Shadow mode:** AI prepares briefs, meeting packets, commitment records, and escalation suggestions; the Assistant reviews without external execution.
3. **Bounded operation:** The Assistant coordinates approved internal workflows while consequential actions remain approval-gated.
4. **Progressive autonomy:** Expand authority only for named lanes that demonstrate reliable records, auditability, and reduced executive load.

No stage grants authority by implication. Each expansion requires an owner-approved receipt naming the lane, actions, limits, evidence, and review date.

### Production cadences

- Morning executive brief: priorities, deadlines, conflicts, decisions needed, and recommended next actions.
- Pre-meeting packet: purpose, participants, relevant commitments, decisions needed, evidence gaps, and approval boundaries.
- Post-meeting receipt: decisions, commitments, owners, due dates, source, confidence, and next action.
- End-of-day reconciliation: unresolved obligations, stale records, missed deadlines, and required escalations.
- Weekly review: priorities, risks, open decisions, obligation aging, usefulness, and workflow corrections.
- Event-triggered escalation: authority ambiguity, reputational or legal risk, conflicting instructions, privacy exposure, or an approaching consequential deadline.

### Evidence and observation discipline

Every material recommendation or proposed action should identify evidence, assumptions, confidence, missing information, consequence level, and required approval. Human-world input should be labeled as direct observation, explicit stakeholder statement, AI interpretation, unverified report, or approved company fact.

The AI must not infer sensitive traits, hidden motives, health, protected characteristics, or private relationship dynamics. Human context is useful only when explicitly provided, necessary, and appropriately bounded.

### Learning and correction loop

```text
mistake or friction -> proposed correction -> Assistant review
  -> owner/operator approval when governance changes
  -> versioned workflow update -> validation in the next bounded cycle
```

Raw onboarding conversation is not durable memory by default. Approved preferences, decisions, authority grants, and workflow rules become durable only through a reviewable receipt. Use [workflow-correction-proposal.md](../templates/workflow-correction-proposal.md) for changes.

### Capacity protection

The interface must reduce net cognitive load. Use alert budgets, batching, duplicate suppression, priority thresholds, and “no action needed” filtering. Review whether each automation saves more attention than it consumes, and track Assistant review burden alongside executive time saved.

### Pilot and measurement

Begin with a 2–4 week bounded pilot covering daily briefs, meeting preparation and receipts, commitment tracking, deadline/conflict monitoring, and escalation quality. Track missed and recovered commitments, preparation time, unnecessary interruptions, obligation aging, briefing usefulness, false-positive alerts, escalation precision, Assistant review burden, corrections per workflow, and decisions improved or accelerated.

Expand authority only when the pilot demonstrates lower cognitive load, reliable records, acceptable false-positive rates, and clear human trust. Use [pilot-metrics-review.md](../templates/pilot-metrics-review.md) for the review.

### Separate operating artifacts

Keep these surfaces distinct: onboarding curriculum; approved Assistant preferences and boundaries; authority and access register; live commitment and decision ledgers; company governance and policies; and AI workflow/playbook definitions. The repository tracks reusable, sanitized contracts and templates. Private operational records belong in their approved external store. Derived views must point to their source and as-of time and must not become competing authorities.

## First Production Templates

- [Assistant approval receipt](../templates/assistant-approval-receipt.md)
- [Authority and access register](../templates/authority-access-register.md)
- [Commitment receipt](../templates/commitment-receipt.md)
- [Meeting-to-execution packet](../templates/meeting-to-execution-packet.md)
- [Escalation record](../templates/escalation-record.md)
- [Workflow correction proposal](../templates/workflow-correction-proposal.md)
- [Pilot metrics review](../templates/pilot-metrics-review.md)

## Boundary

This handoff does not authorize hiring, employment decisions, external outreach, data collection, persistent memory, access expansion, or company commitments. Those require separate human authorization.
