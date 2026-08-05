# Skill Adoption Receipt

Use under [External Skill Adoption Preserves Capability Lineage](../../docs/skill-adoption-governance.md).

- Receipt ID: `SAR-PATTERN-MEMORY-2026-08-05-01`
- Skill: `pattern-memory`
- Canonical local path: `skills/pattern-memory/SKILL.md`
- Status: `Probation`
- Receipt date: `2026-08-05`

## Purpose

- Bounded job this skill serves: Query and inspect deterministic,
  evidence-linked reusable patterns from eligible governed learning and
  allowlisted sanitized project documents without creating memory authority.
- Why existing capabilities are insufficient: Canonical ledgers and project
  documents preserve durable state but do not provide a bounded, ranked,
  cross-project retrieval projection with reconstructable provenance.
- Intended users or workflows: Internal Query, Inspect, and Evaluate work under
  the Governed Pattern Memory v1 shadow pilot.
- Out of scope: Conversation capture, automatic extraction, embeddings, model
  inference, prompt injection, tenant-private retrieval, automatic Skill or
  learning promotion, canonical-state mutation, and external action.

## Origin

- Upstream author or organization: Tencent Cloud Database team.
- Source URL or repository:
  [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory).
- Reviewed version, release, commit, or source date: Upstream `v0.3.6`, its
  public README, and package manifest were reviewed on `2026-08-05`. The exact
  immutable upstream commit inspected during the original evaluation is
  `Missing`. The operator-supplied research brief incorrectly described an
  unsupported `v2.0.0` Memory Hub architecture and is not treated as reliable
  upstream evidence.
- License or rights status: The upstream repository and package manifest
  declare MIT. No upstream source code, dependency, installer, plugin, gateway,
  or service was copied, installed, imported, or executed by the Anyang
  implementation.
- Source inspected by: Codex reviewed the operator-supplied brief, the live
  public upstream repository and package metadata, and the local implementation
  and Git lineage. Live source inspection established capability lineage, not
  benchmark validity or independent product quality.

## Capability And Authority

- Activation: `Explicit` operator invocation or model routing from requests to
  find, inspect, or evaluate governed reusable patterns.
- Tools or scripts: The repository-local `project pattern-memory query` command,
  implemented by `cli/anyang_loop/pattern_memory.py` and routed through the
  canonical repository launcher. No upstream executable is used.
- Network access: Not required. V1 reads only local tracked repository sources.
- Files, write surfaces, or data classes: Reads eligible `RL-*` rows and tracked
  allowlisted sanitized project documents. It may write only a derived report
  beneath ignored `generated-patterns/` or an explicitly named external path.
  Existing output requires separate `--force` authority for that exact file.
- Permitted effects: Produce a deterministic Markdown or JSON review projection
  with ranked candidates, evidence references, content hashes, exclusions,
  truncation, membranes, and generation provenance.
- Prohibited effects: Tenant-private retrieval; archive, transcript, source-note,
  or analysis ingestion; conversation capture; embeddings; model inference;
  prompt injection; canonical ledger, project, template, or Skill mutation;
  automatic promotion; and execution authority.
- Additional authority required: Replacing an existing report, retaining a
  candidate, changing an `RL-*` entry, modifying a Skill or project surface,
  adding embeddings, crossing a membrane, or implementing a retrieved pattern
  requires its own explicit governing decision.

## Lineage

- Mechanism or judgment inherited: The external evaluation materially informed
  the decision to treat prior agent work as selectively reusable, use local
  lexical BM25-style retrieval, constrain recall count and context volume, and
  preserve inspectable provenance back to source material.
- Local changes: Replaced automatic capture and layered persona memory with
  approved-or-later `RL-*` learning plus an allowlisted project-document tier;
  added stable candidate IDs and hashes, state eligibility, repository
  containment, tracking and privacy checks, Anyang membrane classifications,
  transactional report compilation, `authority_effect: none`, `review-only`
  disposition, deterministic tie-breaking, explicit output-collision control,
  shadow evaluation, and a separate human promotion boundary. V1 deliberately
  excludes databases, vectors, RRF, model distillation, proxies, dashboards,
  loadouts, automatic recall, and automatic Skill creation.
- Reason for each material change: Preserve Anyang's existing authoritative
  ledgers and membranes, prevent retrieval from becoming authority or durable
  memory, keep results reproducible without a model or external service, and
  measure usefulness before broadening capability.
- Reviewed local version or content hash: Kernel and RFC introduced by
  `de7e255`; canonical skill and adapters introduced by `bac84b6`. Canonical
  `SKILL.md` SHA-256 at review:
  `A415E515323C5C9AD5D6B9685B6CAFB9B348B8EEFD006914284F4D07205CD24F`.
- Canonical home and adapter relationship: The complete operating contract
  lives at `skills/pattern-memory/SKILL.md`. Repository and parent-workspace
  adapters are discovery-only and add no behavior, tool access, persistence,
  memory-promotion, or execution authority.

## Evidence

- Files inspected: Canonical skill and route metadata; repository and
  parent-workspace discovery adapters; `docs/governed-pattern-memory-v1.md`;
  `cli/anyang_loop/pattern_memory.py`; CLI routing; artifact-state registration;
  focused tests and ten-query replay fixture; implementation commits `de7e255`
  and `bac84b6`; operator-supplied TencentDB research brief; and the live public
  upstream README and package manifest.
- Representative tests and results: The implementation and skill package passed
  focused tests and the repository's exact-tree Full validation on `2026-08-04`
  with `519` passed and `3` skipped. The controlled ten-query replay placed the
  expected source in the top five for `9` of `10` queries. A fresh-task forward
  test reconstructed all five candidate IDs, source references, evidence paths,
  and hashes with no canonical mutation, but three provisional project snippets
  ranked above two stronger governed audit learnings. The current working tree
  contains an unrelated modification to `tests/test_pattern_memory.py`, so this
  receipt does not represent that modified tree as revalidated.
- Portfolio interaction review: The skill preserves the recursive-learning
  ledger and project documents as authoritative, keeps the existing
  `extract-patterns` baseline unchanged, routes final decisions through
  `learn-from-choices`, and stops before the existing RL or Skill promotion
  workflows. No fresh `$review-ai-harness` report was generated for this
  receipt.
- Known conflicts or overlap: Retrieval overlaps conceptually with recursive
  learning, project-document search, the legacy `extract-patterns` command, and
  Skill improvement. The canonical contract separates them by making reports
  derived and review-only and by prohibiting automatic retention or promotion.
- Untested behavior and coverage gaps: Exact immutable upstream commit from the
  original evaluation; independent upstream benchmark verification; broad human
  usefulness; cross-lane false positives and missed patterns; review burden;
  recall under paraphrased or low-overlap queries; long-running corpus change;
  and portfolio behavior after any future scoring or schema revision.
- Evidence classification: `Source-backed` for current upstream identity,
  declared MIT license, confirmed upstream capability themes, local Git
  lineage, implementation differences, structural tests, and the forward-test
  receipt; `Provisional-assumption` for behavioral value, general retrieval
  quality, portfolio non-conflict, and the exact historical upstream baseline.

## Decision

- Decision owner: Repository operator.
- Decision and rationale: The repository operator explicitly selected creation
  of this `Probation` receipt on `2026-08-05`. The causal development sequence
  and specific transfer of lexical retrieval, bounded recall, and inspectable
  provenance make `pattern-memory` materially externally derived even though
  its code, state model, governance, and runtime are Anyang-native. Provenance,
  rights, local boundaries, and structural evidence are reviewable; immutable
  historical upstream identity and broader behavioral evidence remain
  incomplete.
- Exact probation scope, if applicable: Internal
  `anyang-internal / repository / internal-sanitized` Query, Inspect, and
  Evaluate use under Governed Pattern Memory v1. Reports remain derived,
  review-only, and non-authoritative. No tenant-private sources, automatic
  capture, embeddings, model inference, injection, promotion, or canonical
  mutation.
- Review or expiry date: `2026-10-01`, after three additional human-reviewed
  query cohorts, or earlier after a material privacy, membrane, provenance,
  authority, recall, upstream-license, or portfolio-conflict incident.
- Rollback method: Prepare a separate operator-reviewed reversal covering the
  RFC, artifact-state registration, CLI kernel and route, skill, discovery
  adapters, tests, replay fixture, and ignored report family introduced by
  `de7e255` and `bac84b6`; preserve this receipt and Git lineage. Do not remove
  or revert those surfaces from this receipt alone.
- Supersedes or retires: The prior provisional classification of
  `pattern-memory` as repo-native by current file evidence; no skill or
  capability is retired.

## Boundary

This receipt records provenance, capability transfer, review evidence, and the
repository operator's bounded `Probation` decision. It authorizes only the
internal shadow-evaluation scope above. It does not authorize publication,
deployment, spending, customer contact, private-data access, installation
elsewhere, execution of upstream scripts or services, report promotion,
canonical-state mutation, or any broader action.
