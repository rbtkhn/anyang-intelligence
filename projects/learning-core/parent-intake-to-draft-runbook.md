# Evidence-First Intake To Draft-Decision Runbook

This is the operator front door for a real Learning Core parent intake. Its endpoint is a parent-verified intake summary, one readiness status, and a separately approved initial learner-profile packet—not an automatic 30-day plan draft.

Use `$learner-intake create` with [parent-intake-message.md](parent-intake-message.md) for the two guided conversations. Use `$learner-intake change` when a confirmed-effective profile already exists and new evidence may justify reconsideration. [parent-onboarding-survey.md](parent-onboarding-survey.md) remains only an optional pseudonymous preview.

## Authority And Data Boundary

- The parent or guardian controls intake, child-facing questions, preservation, sharing, drafting, and plan use.
- Use a parent-approved learner label. Do not collect identifiers in repository surfaces.
- Treat live answers as temporary working state until the parent verifies the summary.
- Keep real family information out of Git and `projects/learning-core/`.
- Store an approved case record only in the operator-controlled tenant-private store.
- Treat guardian approval and operator-confirmed persistence as separate transitions.
- Keep the prior profile effective until preservation of an approved replacement is confirmed.
- Do not contact schools, teachers, specialists, applications, or other systems.

The repository may hold reusable blank templates and synthetic fixtures, but never the real intake packet.

## Process

### 1. Authority And Privacy Gate

Target 8–10 minutes; stop at 12.

Confirm:

- parent or guardian authority;
- permission to conduct and classify the intake;
- parent-approved learner label;
- separate approvers for drafting, child-facing questions, plan use, and saved evidence;
- what may be discussed, preserved, deleted, or shared;
- excluded tools, topics, activities, or approaches;
- whether caution or outside-support context exists and what minimum planning implication may be considered.

If authority, privacy, save/share, or caution boundaries are unresolved, assign `Hold`. Do not move into learner-specific intake.

### 2. Evidence-First Learner Conversation

Target 15–20 minutes; stop at 25.

When the Success–Friction–Bridge pilot is selected, use the canonical [clickable create cards](../../skills/student-operating-system/learner-intake/references/clickable-create-cards.md) instead of asking the open-ended prompts below. Ask all short readiness cards and six core episode cards, then only conditional cards whose trigger applies. Do not run both versions.

Collect only inputs that could change a planning decision:

- what the parent wants to understand this month;
- useful success even without an academic-level change;
- explicit avoidances;
- what already works and should be preserved;
- one recent positive learning episode;
- one recent friction episode, its immediate context, and what helped;
- one concrete choice, question, connection, artifact, or repeated interest;
- where learning already crosses contexts;
- choices the learner can carry and support the parent still needs to provide;
- minimum viable and ordinary household capacity;
- pivot, pause, screen-time, and preparation boundaries;
- currently usable resources and first-week tool decisions;
- useful evidence, excessive capture, deletion authority, and outside-support triggers;
- the independence the family hopes the learner can increasingly carry forward.

Record observations separately from parent interpretations. Do not convert one episode into a fixed label or request an exhaustive resource inventory.

### 3. Optional Learner Voice

Target 5–7 minutes after explicit parent approval.

For the pilot, ask at most the three learner cards in the [clickable create cards](../../skills/student-operating-system/learner-intake/references/clickable-create-cards.md). Otherwise use the three questions in [parent-intake-message.md](parent-intake-message.md). The learner may skip any question. Stop when comfort, attention, or interest falls. Child participation is optional and cannot block an otherwise sufficient parent intake.

### 4. Offline Classification

Target 10–15 minutes.

Apply [onboarding-readiness-checklist.md](onboarding-readiness-checklist.md) and assign exactly one state:

- `Ready`: all required authority, privacy, learner-context, concrete-signal, household-rhythm, tool, and caution conditions are sufficiently clear.
- `Provisional`: required authority and safety conditions are clear, but optional learner-fit evidence remains thin and every gap can stay visible.
- `Hold`: any required authority, privacy, learner-context, rhythm, tool, overload, or outside-support boundary remains unresolved.

When uncertain between statuses, choose the safer status. Never use `Provisional` to route around a waiting condition.

### 5. Parent Verification

Target 5–8 minutes.

Prepare a packet from [parent-intake-summary-template.md](parent-intake-summary-template.md). Ask the parent to:

- correct the summary;
- confirm the permissions matrix;
- approve or remove each preserved learner signal;
- confirm the classification rationale;
- decide what may be retained in the tenant-private store.

Do not preserve the packet before this review unless the parent already approved that temporary handling.

### 6. Initial Learner Profile

Prepare a separate proposed profile using [initial-learner-profile-template.md](initial-learner-profile-template.md). Show the complete profile to the named guardian and request an exact decision.

- `Approved` produces an approved initial-profile packet in `Awaiting Persistence`.
- `Changes Requested` requires a complete corrected profile and a new exact confirmation.
- `Rejected` leaves no effective profile.

Only an authorized operator's confirmation that the approved packet was preserved in the tenant-private store makes the profile `Effective`. Do not place the real packet in Git.

### 7. Next-Action Gate

- For `Hold`, use [hold-response-template.md](hold-response-template.md) and request only missing decisions.
- For `Ready` or `Provisional`, require the confirmed-effective initial profile, then ask separately whether the parent authorizes an evidence-mapped 30-day draft.
- If drafting is approved, then use [plan-drafting-gate.md](plan-drafting-gate.md) and [plan-draft-evidence-map.md](plan-draft-evidence-map.md).

Classification does not grant drafting authority. A draft does not grant authority for use.

## Question Quality Rules

Prefer questions that:

- ask for a recent event rather than a general trait;
- distinguish observation from interpretation;
- reveal what should be preserved as well as what should change;
- alter readiness, rhythm, resources, evidence, safety, or the next decision;
- help the family become more independent rather than more dependent on the service.

Defer questions that merely make the profile look complete.

## Completion Test

The intake is complete only when:

- the parent has verified the pseudonymous summary;
- permissions and prohibited uses are explicit;
- one readiness status has an evidence-based rationale;
- any profile that was proposed has an explicit guardian decision;
- any effective profile has operator-confirmed tenant-private persistence;
- missing inputs and assumptions remain visible;
- the next action names its human authority;
- no real family record has entered Git.

## Existing Profile Changes

Use `$learner-intake change` rather than repeating full intake. Require the latest effective profile, its version and approval receipt, current authority boundaries, and the new evidence. Produce `No Change`, `Open Question`, an exact `Profile Change Proposal`, or `Hold`.

Evidence may justify a proposal but cannot modify the profile. The named guardian must approve the exact before-and-after change set, and the prior version remains effective until an authorized operator confirms persistence of the replacement.
