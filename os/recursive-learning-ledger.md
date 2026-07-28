# Recursive Learning Ledger

## Purpose

This is the canonical repository-level index of material lessons that change how
Anyang Intelligence handles future work.

The ledger connects:

```text
signal -> learning -> human decision -> durable change -> validation -> observed outcome
```

It does not replace detailed audits, project ledgers, decision records, commits,
or operating reviews. Link to those sources instead of copying them here.

## Authority And Boundaries

- The operator approves durable changes and their disposition.
- A ledger entry records authority; it does not create authority.
- Private or lane-restricted evidence stays in its governing location. Use a
  bounded reference here.
- Do not claim effectiveness from implementation or validator success alone.
  Use `Unmeasured` until a later work cycle provides outcome evidence.
- Do not force an entry when work produced no durable, reusable learning.

## Inclusion Rule

Create one stable `RL-YYYY-NNN` entry when all of the following are true:

1. Actual work produced friction, a failure, a surprise, or a reusable success.
2. The learning is likely to matter in a future cycle.
3. A human decision approved, rejected, or deferred a durable response.
4. The evidence and affected operating surface can be referenced without
   crossing a privacy, customer, or authority membrane.

## States

- `candidate`: recorded for a human decision.
- `approved`: approved but not yet implemented.
- `implemented`: preserved in a durable operating surface.
- `validated`: the structural change passed its relevant checks.
- `observed`: a later cycle supplied outcome evidence.
- `deferred`: intentionally held with a revisit condition.
- `rejected`: reviewed and declined.
- `superseded`: replaced by another identified learning.

Implementation proves that the operating surface changed. Validation proves that
the change satisfies its stated structural checks. Only observation can support
a claim that behavior, burden, quality, or outcomes improved.

## Ledger

| ID | Opened | Signal | Learning | Decision and authority | Durable surface | Evidence and validation | Outcome or revisit | State |
|---|---|---|---|---|---|---|---|---|
| RL-2026-001 | 2026-07-28 | Repository inspection found recursive-learning doctrine, loops, and project-specific ledgers but no canonical cross-cycle index. | Distributed evidence needs one bounded index to make improvement history and outcome follow-up reconstructable. | Operator approved creation of `recursive-learning-ledger`. | `os/recursive-learning-ledger.md`; discoverability link in `docs/recursive-self-enhancement.md`. | Manual schema, authority-boundary, link, privacy-keyword, diff, and three-entry backfill-fit checks passed. | The three-entry review trigger was reached; the schema preserved different adjudication states without merging them. Reconstruction-time and behavior effects remain Unmeasured. | validated |
| RL-2026-002 | 2026-07-25 | The Narrative Systems pilot returned 510 mechanical diagnostics, including 480 relative-link candidates; independent review reconstructed 18 of 20 sampled traces, consolidated five root causes, and rejected the raw link headline as a unique-issue count. | Mechanical diagnostics must remain candidates until independent review removes duplication, tests trace meaning, and consolidates shared root causes. Audit receipts also need collector identity, effective timeout, and minimized-output provenance before reproducibility or publication claims. | System Engineer authorized the bounded audit and a separate remediation plan; material-finding adjudication, target remediation, and kernel adoption remained pending or unapproved. | [Narrative Systems transaction](../docs/analysis/cross-repo-audits/narrative-systems-2026-07-25/transaction-record.md), [audit packet](../docs/analysis/cross-repo-audits/narrative-systems-2026-07-25/audit-packet.md), and [remediation plan](../docs/analysis/cross-repo-audits/narrative-systems-2026-07-25/remediation-plan.md). | Sealed collection, no-mutation proof, independent review, and later Predictive History reuse of candidate-to-finding compression are repository-visible. Final Narrative Systems finding acceptance remains Missing. | Later Predictive History review compressed 1,123 candidates into nine findings and seven root causes, demonstrating transfer of the method; decision-useful yield and marginal-cost benefit remain Unmeasured. | observed |
| RL-2026-003 | 2026-07-25 | Predictive History passed 91 native tests while independent review still produced eight accepted material findings; 1,123 collector candidates compressed into nine findings and seven root causes, with 39 of 40 required traces complete and 40 of 40 sampled unique broken links confirmed as written. | A green native suite does not establish repository assurance. Generated/source parity, trace reconstruction, stale state, and semantic coverage require independent checks, while raw diagnostic volume must not be represented as material-finding count. | System Engineer accepted PH-STW-01 through PH-STW-08, retained PH-STW-09 as a monitored inference, and classified the kernel `revise`; remediation, adoption, publication, and commercial use remained held. | [Predictive History transaction](../docs/analysis/cross-repo-audits/predictive-history-2026-07-25/transaction-record.md), [audit packet](../docs/analysis/cross-repo-audits/predictive-history-2026-07-25/audit-packet.md), and [internal offer design](../docs/analysis/ai-repository-assurance-commercial-offer-2026-07-25.md). | System Engineer adjudication, sealed Steward ledger, no-mutation proof, 97.5% trace reconstruction, and sampled precision evidence validate the bounded learning. | Audit-method utility is structurally supported; delivery burden, unrelated-owner portability, customer outcome, and commercial ROI remain Unmeasured. | validated |
| RL-2026-004 | 2026-07-26 | Civilization Memory returned green governance output with 29 reported drift items and green chronicle health after selecting zero day sections; adjudication also identified seven verified target defects, one inferred target risk, and one verified Collector v1.1 sampling defect. | Command exit state, semantic assurance, and collection completeness are separate facts. Empty-population greens must not imply coverage, rooted sampling must exclude false matches while including intended deep paths, and collector defects must be separated from target defects. | System Engineer accepted the target findings with one targeted revision, reclassified CS-08 as a verified collector defect, and held target remediation, kernel adoption, and commercial-validation claims pending separate authority. | [Civilization Memory transaction](../docs/analysis/cross-repo-audits/civilization-memory-2026-07-26/transaction-record.md), [audit packet](../docs/analysis/cross-repo-audits/civilization-memory-2026-07-26/audit-packet.md), [Collector](../cli/anyang_loop/cross_repo_audit.py), and [focused tests](../tests/test_cross_repo_audit.py). | Sealed hashes and mutation proof support the audit; later Collector hardening was committed as `855943b` and passed the canonical suite with 331 tests passed and 3 skipped. | Structural containment, sampling, capture, and receipt controls were validated. Their effect on a later independent benchmark, reconstruction time, or commercial ROI remains Unmeasured. | validated |

## Update Rules

- Keep one row per stable learning ID and update its state as evidence matures.
  Git history preserves prior states.
- Prefer links and hashes over duplicated narrative.
- Record `Missing` when authority, validation, timing, or outcome evidence cannot
  be reconstructed.
- If the meaning of a learning changes materially, create a new ID and mark the
  prior entry `superseded`.
- Never rewrite a rejected or deferred learning as approved without recording
  the new human decision.

## Cadence

- `coffee` may identify a `candidate`.
- Approved implementation updates the durable-surface and evidence fields.
- `dream` may confirm that an entry reached `implemented` or `validated`.
- A later comparable work cycle supplies the evidence required for `observed`.
- Repository operating review should examine unresolved `candidate`, `approved`,
  `implemented`, and `deferred` entries without treating entry count as success.

## Success Standard

The ledger succeeds when it makes one consequential learning easier to
reconstruct, prevents a known failure from being rediscovered, or establishes
honest outcome evidence. More rows are not inherently better.
