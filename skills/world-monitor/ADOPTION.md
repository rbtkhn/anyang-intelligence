# Skill Adoption Receipt

Use under [External Skill Adoption Preserves Capability Lineage](../../docs/skill-adoption-governance.md).

- Receipt ID: `SAR-WORLD-MONITOR-2026-08-04-01`
- Skill: `world-monitor`
- Canonical local path: `skills/world-monitor/SKILL.md`
- Status: `Probation`
- Receipt date: `2026-08-04`

## Purpose

- Bounded job this skill serves: Convert one World Monitor REST signal into a
  provenance-bearing, read-only external-signal receipt and optionally prepare
  a human-gated Singularity Science review or promotion recommendation.
- Why existing capabilities are insufficient: General source intake does not
  normalize provider identity, signal freshness, observation/inference
  separation, adapter version, integrity hash, and explicit
  `no_authority_created` status at the external-monitor boundary.
- Intended users or workflows: Internal Singularity Science capture, review,
  comparison, routing proposals, and post-test closeout for World Monitor
  signals.
- Out of scope: Autonomous alerting or action, customer routing, direct archive
  writes, public claims, doctrine, MCP use, source-code reuse, and treating
  World Monitor output as ground truth.

## Origin

- Upstream author or organization: World Monitor project, led by Elie Habib
  (`koala73`).
- Source URL or repository:
  [koala73/worldmonitor](https://github.com/koala73/worldmonitor).
- Reviewed version, release, commit, or source date: Public `main` repository
  and documented programmatic-access surface reviewed on `2026-08-04`; the
  exact upstream commit used when the local adapter was created is `Missing`.
- License or rights status: The upstream project declares its source code
  [AGPL-3.0-only](https://github.com/koala73/worldmonitor/blob/main/LICENSE).
  The Anyang implementation consumes the external interface and states that it
  does not copy World Monitor source code. Commercial, combined-service, and
  trademark obligations remain unadjudicated.
- Source inspected by: Codex reviewed the public repository description,
  programmatic-access statement, and license boundary as read-only source
  material on `2026-08-04`. No upstream installer, package, MCP server, or
  source code was executed.

## Capability And Authority

- Activation: Model-routed or explicit `$world-monitor` use is described by
  the canonical skill. Its `agents/openai.yaml` route has no explicit
  `allow_implicit_invocation` policy, and no catalog entry or repository or
  workspace discovery adapter was found during this review.
- Tools or scripts: Local Python normalization and promotion-gate modules. The
  adapter can perform an HTTP GET against an operator-supplied URL and can add
  an operator-supplied API key to the request header. Normalization and
  promotion evaluation otherwise operate on supplied data without mutation.
- Network access: Optional outbound read to the operator-supplied REST URL with
  a default ten-second timeout. MCP is explicitly deferred.
- Files, write surfaces, or data classes: No file-write surface is implemented
  by the adapter or promotion gate. Returned signal data may contain external
  source content and must remain inside the Singularity Science membrane until
  separately reviewed.
- Permitted effects: Fetch or normalize a signal, return an
  `ExternalSignalReceipt`, prepare a bounded review packet, and recommend one
  promotion disposition without writing an archive artifact.
- Prohibited effects: Claims, approvals, work items, permissions, customer
  obligations, archive writes, customer routing, publication authority,
  doctrine, autonomous action, and automatic inference at intake.
- Additional authority required: Network retrieval, use of credentials,
  archive promotion, cross-lane transfer, customer use, publication,
  deployment, commercial use, or any persistent write requires the applicable
  explicit operator and human approval.

## Lineage

- Mechanism or judgment inherited: World Monitor's externally documented REST
  signal surface and provider/source metadata conventions.
- Local changes: Added an Anyang-native immutable receipt, required provenance
  and freshness fields, observation/inference separation, deterministic
  integrity hashing, `no_authority_created`, Singularity-only routing, a
  human-gated promotion decision, and explicit rights and corroboration holds.
- Reason for each material change: Prevent a dashboard or provider summary
  from becoming an Anyang claim, decision, customer action, or doctrine without
  independent evidence and human authority.
- Reviewed local version or content hash: Adapter introduced by local commit
  `b708e72`; skill and first promotion gate introduced by `a88a8e5`; explicit
  archive approval receipt requirement added by `0340b50`. Canonical
  `SKILL.md` SHA-256 at review:
  `C166D8AC94A644F4B79F2320F6F840593CD3E9BCA7FEE78D42D7E78007914406`.
- Canonical home and adapter relationship: The complete skill contract lives
  at `skills/world-monitor/SKILL.md`, with a load-later review-packet reference
  and local Python capability modules. No repository or workspace discovery
  adapter was found; the skill is also absent from `skills/README.md`.

## Evidence

- Files inspected: Canonical skill, route, review-packet reference, adapter and
  promotion-gate modules, adapter and promotion-gate tests, integration
  doctrine, pilot receipt, archive-promotion contract, local introduction and
  refinement commits, public upstream repository, and public upstream license.
- Representative tests and results: `python -m pytest -q -p no:cacheprovider
  tests/test_worldmonitor_adapter.py tests/test_worldmonitor_promotion_gate.py`
  passed `18` tests on `2026-08-04`. The suite covers required lineage,
  timestamps, authority rejection, idempotence, stale signals,
  observation/inference separation, corroboration, duplicate handling,
  Singularity-only promotion, explicit archive approval, and non-writing
  recommendations.
- Portfolio interaction review: The skill routes first into Singularity
  Science and distinguishes its receipt and promotion surfaces from source-note
  intake. No fresh generated `$review-ai-harness` packet was created, and the
  missing catalog and discovery routes limit portfolio visibility.
- Known conflicts or overlap: Potential overlap exists with Singularity Science
  source intake, recurrence review, and source-note promotion. The local gate
  stops before archive mutation and requires explicit archive approval, which
  structurally separates these responsibilities.
- Untested behavior and coverage gaps: Exact upstream source commit at initial
  integration; live REST compatibility; URL allowlisting and credential
  handling; source accuracy and independence; commercial-license sufficiency;
  false or missed activation; operator usefulness; MCP; and full portfolio
  interaction under competing triggers.
- Evidence classification: `Source-backed` for current upstream identity,
  public interface, declared license, local lineage, and structural test
  results; `Provisional-assumption` for live compatibility, operational value,
  source quality, and portfolio non-conflict.

## Decision

- Decision owner: Repository operator.
- Decision and rationale: The repository operator explicitly selected the
  bounded `Probation` disposition on `2026-08-04`. Structural controls and
  focused tests pass, while discovery routing, live-signal evidence, exact
  upstream version lineage, and behavioral portfolio evidence remain
  incomplete.
- Exact probation scope, if applicable: One operator-selected,
  public, non-sensitive REST signal may be fetched or supplied, normalized, and
  reviewed inside Singularity Science. No MCP, customer routing, archive write,
  publication, doctrine, deployment, or credential persistence.
- Review or expiry date: `2026-10-01`, or immediately after the first approved
  live-signal trial, upstream license or API change, credential-handling issue,
  or material activation or conflict failure.
- Rollback method: Disable invocation and prepare a separate operator-reviewed
  retirement or reversal covering the canonical skill, route, reference,
  adapter, promotion gate, tests, and project integration artifacts identified
  by commits `b708e72`, `a88a8e5`, and `0340b50`; preserve this receipt and Git
  lineage. Do not remove or revert those surfaces from this receipt alone.
- Supersedes or retires: None.

## Boundary

This receipt records provenance, review evidence, and the operator's bounded
`Probation` decision. It authorizes only the exact probation evaluation scope
recorded above. It does not authorize broader network access, persistent
credential use, archive promotion, publication, deployment, spending, customer
contact, private-data access, installation elsewhere, or commercial use.
