# Skill Adoption Receipt

Use under [External Skill Adoption Preserves Capability Lineage](../../docs/skill-adoption-governance.md).

- Receipt ID: `SAR-DECISION-AUDIT-2026-08-04-01`
- Skill: `decision-audit`
- Canonical local path: `skills/decision-audit/SKILL.md`
- Status: `Probation`
- Receipt date: `2026-08-04`

## Purpose

- Bounded job this skill serves: Surface no more than three consequential,
  agent-selected decisions that remain materially contestable, weakly
  evidenced, or dependent on an unconfirmed assumption.
- Why existing capabilities are insufficient: General closeout, elicitation,
  and infrastructure review do not isolate uncertain decisions made by the
  agent during the current work.
- Intended users or workflows: Explicit decision and assumption audits, narrow
  pre-commit judgment checks, and conditional internal composition with Dream.
- Out of scope: Infrastructure review, automatic persistence, generic
  uncertainty lists, operator-made decisions, execution, and any change to
  approval or authority.

## Origin

- Upstream author or organization: David Ondrej.
- Source URL or repository:
  [davidondrej/skills — decisions](https://github.com/davidondrej/skills/blob/main/skills/thinking-and-docs/decisions/SKILL.md).
- Reviewed version, release, commit, or source date: Public `main` source
  reviewed on `2026-08-04`; the exact upstream commit used for the original
  local adaptation is `Missing`.
- License or rights status: The upstream repository publishes an
  [MIT License](https://github.com/davidondrej/skills/blob/main/LICENSE),
  copyright David Ondrej, 2026. Local attribution is retained in the canonical
  skill's Provenance section.
- Source inspected by: Codex reviewed the public upstream `decisions` skill and
  repository license as read-only source material on `2026-08-04`. No upstream
  code, hook, installer, or script was executed.

## Capability And Authority

- Activation: `Implicit`, only when the canonical eligibility gate is met;
  explicit `$decision-audit` use is also supported.
- Tools or scripts: No bundled script and no mandatory command. The skill may
  ask the active agent to inspect the operator request, current diff, governing
  repository files, tests, evidence, and recent commits.
- Network access: Not required by the skill.
- Files, write surfaces, or data classes: Read-only access to the smallest
  relevant repository and session evidence. Customer-private evidence must not
  be exposed. No write surface is granted.
- Permitted effects: Produce a sparse user-facing audit containing the
  uncertain decision, evidence level, strongest alternative, consequence,
  authority boundary, and advisory disposition.
- Prohibited effects: Automatic persistence; ledger, claim, transaction,
  approval, or repository mutation; invented uncertainty; exposure of private
  evidence; or treating a finding as execution authority.
- Additional authority required: Any decision-log update, Council update,
  source change, persistence, or downstream action requires separate explicit
  authorization through its governing workflow.

## Lineage

- Mechanism or judgment inherited: Ask the agent to identify only important
  choices it made and remains genuinely uncertain about, consider strong
  alternatives, and answer concisely.
- Local changes: Added materiality and eligibility gates; evidence
  classifications; authority, privacy, and membrane boundaries; a fixed sparse
  output contract; conditional Dream composition; explicit routing to
  elicitation, `learn-from-choices`, and `review-ai-harness`; and a prohibition
  on automatic persistence.
- Reason for each material change: Convert a broad retrospective prompt into an
  Anyang-native, evidence-aware, read-only review that cannot manufacture
  authority or durable state.
- Reviewed local version or content hash: Introduced by local commit
  `1af8c14ce3945b073292b7c7e43b3cbb4ebea291`; canonical `SKILL.md` SHA-256 at
  review: `42E370A0E6CFC9A4C2910A72A9938B4C13431B4BA4E8D6D43EE2E59EAE62AA12`.
- Canonical home and adapter relationship: The complete contract lives at
  `skills/decision-audit/SKILL.md`. Repository and workspace adapters are
  discovery-only and explicitly add no behavior, tool access, persistence, or
  execution authority.

## Evidence

- Files inspected: Canonical skill and route; repository and workspace
  discovery adapters and routes; `tests/test_decision_audit_contract.py`;
  `tests/test_dream_discovery_contract.py`; local introduction commit
  `1af8c14ce3945b073292b7c7e43b3cbb4ebea291`; public upstream skill; and public
  upstream license.
- Representative tests and results: Contract tests encode canonical packaging,
  routing parity, sparse read-only behavior, evidence labeling, historical
  limits, Dream composition, and adapter non-authority. A focused run on
  `2026-08-04` did not reach assertions because the ambient Python environment
  lacked `PyYAML` (`ModuleNotFoundError: yaml`). This is a test-environment gap,
  not a passing result or a demonstrated skill failure.
- Portfolio interaction review: The canonical skill explicitly separates
  infrastructure review into `$review-ai-harness`, routes missing human
  judgment to elicitation, uses `learn-from-choices` for resolution paths, and
  composes with Dream only under a current-session eligibility gate. No fresh
  generated harness-review packet was created for this receipt.
- Known conflicts or overlap: Adjacent responsibilities exist with Dream,
  elicitation, `learn-from-choices`, and `review-ai-harness`; current contracts
  state separate controlling objects and authority effects. Behavioral
  non-conflict has not been established by representative outcome fixtures.
- Untested behavior and coverage gaps: Exact upstream source commit at original
  adaptation; false or missed implicit activation; operator usefulness;
  false-positive burden; interaction under competing skill triggers; and a
  successful focused test run in the governed validation environment.
- Evidence classification: `Source-backed` for current upstream identity,
  license, local lineage, and structural contracts; `Provisional-assumption`
  for behavioral quality and portfolio non-conflict.

## Decision

- Decision owner: Repository operator.
- Decision and rationale: The repository operator explicitly selected the
  bounded `Probation` disposition on `2026-08-04`. Origin, license, local
  lineage, authority
  boundaries, and structural contracts are reviewable, while behavioral
  usefulness, false activation, portfolio non-conflict, the exact upstream
  commit, and a successful focused run in the governed validation environment
  remain incomplete. Existing repository presence and Git history are evidence
  of implementation, not outcome evidence.
- Exact probation scope, if applicable: Use for three internal,
  non-customer-private decision audits through explicit invocation or the
  existing conditional Dream eligibility gate. Record whether each audit found
  a material uncertainty, produced a false positive, displaced a higher-priority
  issue, or changed the operator's decision. No automatic persistence or
  downstream action.
- Review or expiry date: `2026-10-01`, after the third reviewed audit, or
  earlier if a material activation, conflict, rights, or outcome failure
  appears.
- Rollback method: Prepare a separate operator-reviewed reversal covering the
  canonical skill, catalog route, discovery adapters, Dream composition, and
  associated tests identified by local commit `1af8c14`; preserve this receipt
  and Git lineage. Do not remove or revert those surfaces from this receipt
  alone.
- Supersedes or retires: None.

## Boundary

This receipt records provenance, review evidence, and the operator's bounded
`Probation` decision. It authorizes only the exact probation evaluation scope
recorded above. It does not authorize publication, deployment, spending,
customer contact, private-data access, installation elsewhere, execution of
scripts and tools, automatic persistence, or downstream action.
