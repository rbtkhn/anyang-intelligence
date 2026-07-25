# Media Production Harness Map

Status: `Review note — no workflow change`

Purpose: identify where Media Production rules live, when they should load, how they are enforced, and where duplicate or drifting instructions create operator cleanup. This map does not authorize publication, client commitments, rights decisions, spending, hiring, or contractor assignment.

## Map

| Rule surface | Primary owner | Load phase | Enforcement type | Drift risk | Consolidation direction |
| --- | --- | --- | --- | --- | --- |
| `README.md` | Anyang Intelligence operator | Orientation and routing | Human-readable index | Medium | Keep identity, scope, budget, and front-door links; defer detailed rules elsewhere |
| `executive-os-install.md` | Anyang Intelligence operator | System setup and periodic review | Operating model and review prompts | Medium | Keep department model, authority boundaries, cadence, and risk posture; avoid repeating task instructions |
| `artistic-production-gate.md` | System Engineer and Chief Executive | Briefing and pre-production | Required decision gate | Low | Own activation, scope, source, capacity, budget, rights, claims, client authority, and evidence checks before persistent ideation or production |
| `artistic-production-brief-template.md` | Chief Executive | Briefing and production handoff | Required structured record | Low | Own the objective, source boundary, concept directions, selected production scope, risks, evidence, and disposition |
| `creative-abundance-quality-gate.md` | Human reviewer | Production review and pre-delivery | Required quality checklist | Low | Make this the owner for source fidelity, usefulness, readability, review readiness, and revision disposition; route unresolved authority questions onward |
| `permissions-and-authority-review.md` | Anyang Intelligence operator | Whenever authority is ambiguous | Explicit hold/escalation review | Medium | Make this the sole owner for publication, delivery, rights clearance, spend, client commitment, claim approval, and contractor-authority boundaries |
| `creative-production-operator-*.md` | Historical migration lineage | Never load for current work | Superseded contractor design | Low | Preserve explicit superseded status; do not use as Artistic Director activation, briefing, production, or review controls |
| `abundance-principle.md` | Anyang Intelligence operator | Orientation and creative framing | Principle and judgment prompts | Medium | Keep the purpose and reuse lens here; do not let it become a substitute for source, rights, or approval gates |
| `grace-gems-monthly-service-package.md` | Anyang Intelligence service owner | Client service planning | Service scope and budget record | Medium | Own the Grace Gems service promise, deliverable shape, and commercial constraints; link to task-level gates |
| `grace-gems-trust-architecture-kit.md` | Anyang Intelligence service owner | Grace Gems briefing and concept development | Client/lane-specific framework | Medium | Keep client-specific trust hypotheses and asset directions here; do not generalize private client evidence into shared guidance |
| `30-day-plan.md` | Anyang Intelligence operator | Planning and prioritization | Bounded plan and review triggers | Low | Keep time-boxed priorities and authorization dependencies; avoid duplicating operating procedures |
| `decision-log.md` | Anyang Intelligence operator | Decision review and governance changes | Decision receipt and review trigger | Low | Own durable operating-model decisions; link to the controlling document instead of restating it |
| `risk-register.md` | Anyang Intelligence operator | Weekly and event-driven review | Risk register | Medium | Track risks and mitigations; link to the controlling gate rather than restating procedures |
| `turn-usefulness-exemplar.md` | Anyang Intelligence operator | Orientation and response-quality calibration | Example and review heuristic | High | Keep as a calibration example; remove or update language when it conflicts with a controlling gate |
| `operating-review.md` | Anyang Intelligence operator | Weekly and event-driven review | Review agenda and learning loop | Medium | Use it to identify repeated failures and propose changes; do not duplicate gate criteria |
| `membrane-notes.md` | Anyang Intelligence operator | Context transfer and archive | Privacy and transfer boundary | Low | Keep private-client, contractor, and rights-sensitive boundary rules here |
| `loop-examples/creative-production-review.yaml` | Anyang Intelligence operator | Workflow implementation/reference | Structured loop example | Medium | Keep as an executable-shaped example; align authority language with the assignment and quality gates |

## Phase loading

### Orientation

Load `README.md`, the relevant section of `executive-os-install.md`, and the
Artistic Director section of the Executive Council role contract. These explain
what Media Production is and where work enters the system.

### Briefing and assignment

Load `artistic-production-gate.md` and
`artistic-production-brief-template.md`. Load client- or lane-specific source
notes only after the task has an approved source boundary. Do not load
superseded contractor materials.

### Production

Load the approved artistic-production brief, its source notes, and only the
production guidance needed for the asset type. Do not treat orientation
documents as a substitute for the approved brief.

### Review and pre-delivery

Load the quality gate. If publication, delivery, spend, rights, client commitment, or contractor authority is unclear, also load the permissions and authority review and choose `Hold` until resolved.

### Artistic Director activation

No current project artifact activates the position. Use a separate System
Engineer activation receipt naming the human holder, AI runtime, tools,
permissions, prohibited evidence, term, review date, persistence boundary, and
revocation path. Superseded contractor readiness materials do not qualify.

### Weekly learning

Use the operating review and risk register to identify drift, cleanup, repeated revisions, and missing checks. Changes to controlling gates require human review before adoption.

## Duplicate-rule candidates

These concepts appear across multiple surfaces and need one controlling owner:

- Source and claim discipline: quality gate; the artistic production gate and
  brief supply the source boundary.
- Rights and licensing: quality gate flags issues; permissions review owns unresolved clearance or approval authority.
- Publication and client delivery: quality gate verifies readiness; permissions review owns permission to cross the boundary.
- Artistic Director activation, scope, and capacity: Artistic Production Gate;
  the Council role contract defines the position.
- Department identity and budget: README and executive install; service-package
  docs apply them to the client lane.
- Historical contractor readiness: superseded files preserve lineage and do not
  govern current work.

## Review questions

1. Does a new rule belong in orientation, a phase-specific gate, or a structured record?
2. Is the rule enforceable as a check, decision field, or validator rather than prose alone?
3. Which document is the single owner when the same concept appears elsewhere?
4. Does the change alter publication, client commitments, rights review, spending, hiring, or contractor authority? If yes, obtain human approval before changing the workflow.
