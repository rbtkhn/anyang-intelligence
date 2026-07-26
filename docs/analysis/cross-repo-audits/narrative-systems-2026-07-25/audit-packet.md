# Narrative Systems Cross-Repo Audit Kernel Pilot — Audit Packet

**Audit ID:** `EC-XRA-NARRATIVE-SYSTEMS-2026-07-25-01`  
**Audit date:** 2026-07-25  
**Target commit:** `5be49ca8765aa803ca7b90b085b0325066a008f0`  
**Target tree:** `c28644cb2c7cd0d84e143b7fd1e14fe938356ba4`  
**Depth:** `benchmark and trace`  
**Current disposition:** `Chief Executive recommends revise; System Engineer adjudication pending`

## Executive conclusion

The portable audit kernel is technically viable and materially useful, but it
does not yet qualify for adoption under its own gate. It transferred cleanly
from a governance-heavy operating repository to a source-heavy epistemic
archive, produced a 90% trace-reconstruction rate, preserved the target without
mutation, and exposed several decision-useful control failures without
adjudicating world claims.

Two adoption measures remain unavailable: the first pilot did not record a
normalized setup/review-time baseline, and this pilot's material findings have
not yet received System Engineer dispositions. The correct outcome is
`revise`, not `adopt`: retain the bounded collector and assurance protocol,
measure the two missing quantities in the next authorized audit, and keep
repository adapters distinct from the portable kernel.

## Council Steward initial finding ledger — sealed

**Review:** `EC-XRA-NARRATIVE-SYSTEMS-2026-07-25-01`  
**Runtime:** `/root/executive_council_steward_pilot_01`  
**Independence disclosure:** The Council Steward may share the Chief
Executive’s model family, but operated as a separate runtime, role contract,
evidence review, and reporting path. The Chief Executive narrative was not
used as evidence.  
**Mutation check:** target remained clean; HEAD and tree match the collector
receipt.

### Exact coverage

- Governing contracts: bounded-agency, epistemic constitution,
  reality-verification lattice, repository, and harness contracts.
- Archive sources: `30/1,895` (`1.58%`), all readable.
- Daily syntheses: `10/52` (`19.2%`).
- Voice records: `10/46` (`21.7%`); all 34 sampled local links resolved.
- Public briefs: `2/2`; all 11 local links resolved.
- Verification packets: `3/3` existing packet surfaces.
- Forecast hooks: `10/55`, ranked by SHA-256 of
  `sealed-commit|Hook-ID`; all ten linked to a daily forecast and
  accountability row.
- Predictive History: `1/2` eligible surfaces, selected
  `predictive-history/README.md`.
- Historical Entropy: `1/2`, selected
  `historical-entropy/reviews/he-01-specialist-review-brief.md`; all five local
  links resolved.
- Mechanical diagnostics: all `510` reviewed at category/root-cause level;
  deterministic sample of `30/272` unique broken-link diagnostics inspected in
  source context.

### Material findings

1. **`VERIFIED — critical`: authoritative archive membership is structurally
   unavailable.**

   `narrative-geopolitics/archive/source-manifest.json:27416-27417` contains a
   trailing comma before the closing array. The bounded-agency contract
   identifies this manifest as authoritative source membership and routing at
   `narrative-geopolitics/method/bounded-agency-contract.md:22`. Native
   validation and the strict AI harness both exit `1` on this parse error.

   **Steward proposed disposition:** hold repository-operability and
   manifest-backed completeness claims.

2. **`VERIFIED + INFERRED — high`: one root defect creates a large validation
   cascade.**

   The strict harness fails directly while loading the invalid manifest; the
   native test output shows repeated manifest-decoding failures across
   manifest-dependent tests. The bounded collector output does not preserve
   enough of the final test summary to prove that every test failure shares
   this cause.

   **Steward proposed disposition:** consolidate confirmed
   manifest-dependent failures under one root cause; keep unclassified test
   failures held rather than counting each as an independent defect.

3. **`VERIFIED — high`: sampled daily-state and forecast synchronization is
   incomplete.**

   - `narrative-geopolitics/work/daily/2026-07-23/synthesis.md:5` says
     `live-intake-first` while retaining template instructions, placeholder
     claim `OPC-YYYYMMDD-01`, placeholder story and forecast IDs, and incorrect
     method links.
   - `NG-20260720-F02` exists in the July 20 synthesis and forecast but is
     absent from `narrative-geopolitics/work/forecasts/forecast-ledger.md`.
   - Eight of ten sampled daily chains were reconstructible; July 20 was
     ledger-incomplete and July 23 was not a completed synthesis.

   **Steward proposed disposition:** support the eight complete sampled daily
   chains; hold the July 20 and July 23 chains.

4. **`VERIFIED — material`: “three completed verification packets” is
   unsupported.**

   - `VER-20260710-01`: `assessed`, `operationally_contested`, not closed.
   - `VER-20260714-01`: `requested`, `not_investigated`, zero evidence chains,
     placeholder assessment.
   - `VER-20260724-01`: `closed`, `operationally_supported` for a bounded
     public-language observable.

   Only one packet is closed; the second is a request shell.

   **Steward proposed disposition:** preserve all three states and reject their
   aggregation as three completed packets.

5. **`VERIFIED — material`: the 480-link headline is duplicate-inflated but
   not parser-noise dominated.**

   - Raw diagnostics: `480`.
   - Unique path/evidence diagnostics: `272`.
   - Exact duplicate inflation: `208` (`43.3%`).
   - Deterministic unique-diagnostic sample: `30/30` genuinely failed to
     resolve as written; first-pass accepted precision `100%` with an
     approximate 95% Wilson interval of `88.6–100%`.
   - Of those 30, `24` (`80%`) pointed to existing repository-root files using
     invalid nested-relative syntax or line-suffixed targets; `6` (`20%`)
     referenced genuinely absent targets.

   **Steward proposed disposition:** reject `480` as a unique-issue count;
   accept `272` unique diagnostics, separated into recoverable path-expression
   defects and absent-target defects.

6. **`ENVIRONMENT-ONLY — material`: portable execution remains partly coupled
   to machine-local provenance.**

   The collector found 29 machine-local-path diagnostics. The selected
   Predictive History surface says
   `Local source inspected: C:\dev\predictive-history`; several voice/source
   records cite external `strategy-codex` paths. These may be valid provenance
   notes, but their referenced environments were outside this authorization
   and were not verified.

   **Steward proposed disposition:** support them as disclosed provenance
   only; hold claims that those paths form portable or currently accessible
   dependencies.

### Supported controls

- Method contracts clearly separate source, synthesis, forecast, verification,
  publication, and authority transitions.
- The public Hormuz brief is honestly labeled `source-bounded`, distinguishes
  recurrence from independence, and links its forecast hook.
- The conceptual essay identifies itself as architecture rather than world
  reporting and states that downstream recurrence cannot upgrade evidence.
- The assessed bypass packet separates incident convergence from contested
  attribution and keeps `NG-20260708-F02` open.
- The closed transit-governance packet confines support to public framing and
  explicitly refuses inference to physical transit conditions.
- Forecast accountability triage preserves retrospective exclusion: the
  deterministic forecast sample contained nine `excluded_retrospective` hooks
  and one non-accountable falsifier, all with reconstructible source-run and
  accountability paths.
- The Historical Entropy review brief separates specialist source review from
  public release.
- Collector mutation proof, snapshot identity, deterministic selection, and
  severity-free diagnostics conform to the bounded assurance design.

### Trace reconstruction

**First-pass rate: `18/20` (`90%`)** across ten sampled daily chains plus ten
seeded forecast-hook chains:

- daily chains: `8/10` complete;
- forecast hooks: `10/10` traceable from ledger to daily
  forecast/synthesis and accountability classification.

This is a path-and-state reconstruction rate, not authoritative
source-membership validation. Manifest-backed confirmation is `INACCESSIBLE`
for all sampled chains until the authoritative JSON parses.

### Root-cause consolidation

- **RC-1:** one trailing comma disables the authoritative manifest, native
  validation, strict harness, and multiple dependent tests.
- **RC-2:** nested generated reports emit repository-root paths as
  Markdown-relative links, producing a large recoverable-path defect family.
- **RC-3:** repeated identical links inflate 272 unique link defects to 480
  rows.
- **RC-4:** daily artifact synchronization permits a template synthesis and a
  missing forecast-ledger hook to coexist with otherwise mature state
  contracts.
- **RC-5:** imported provenance retains machine-local paths that are meaningful
  locally but not independently portable.

### Portable-boundary assessment

The operating-substrate pilot’s control kernel is portable with exceptions:
sealed identity, no-write proof, deterministic sampling, raw-diagnostic
separation, independent semantic review, evidence-state labels, and root-cause
consolidation transferred cleanly.

Narrative Systems’ domain ontology, manifest schema, repository commands,
forecast vocabulary, and machine-local provenance do not transfer
automatically. The benchmark supports a portable assurance envelope plus
repository-specific adapter, not a shared ontology or proof of universal
operability.

### Coverage gaps

- External source truth and substantive geopolitical/historical correctness
  were not adjudicated.
- External URLs and private or machine-local repositories were not accessed.
- Ignored and untracked files were outside the collector snapshot.
- Bounded native-validation output prevents a complete independent partition
  of all test failures.
- The 30-source sample is small relative to the 1,895-source archive.
- The deterministic forecast sample contained no accountable open ex-ante
  hook; live-gate behavior was instead observed through the three verification
  packets.
- Invalid manifest state prevented authoritative membership and voice-routing
  confirmation.

> **Steward seal:** This initial Council Steward ledger is sealed against later
> rewriting. Later evidence, Chief Executive interpretation, or System
> Engineer adjudication may append a separately attributable reconciliation,
> but must not silently alter these findings, classifications, coverage
> statements, or disclosed limitations.

## Chief Executive operating implications

These implications are appended after the Steward seal and do not modify its
findings.

| Steward finding | Operating implication | Chief Executive disposition |
| --- | --- | --- |
| Invalid authoritative manifest | The repository cannot currently prove its own archive membership or pass its declared completion checks. A later remediation decision should repair and validate this single controlling source before broad cleanup. | `fix`, but remediation unapproved |
| Validation cascade | Finding-count inflation would distort priority and ROI. The kernel must preserve root-cause groups and hold unclassified failures. | `retain` the consolidation control |
| Two incomplete daily chains | Strong contracts are not sufficient without synchronization checks across generated artifacts and ledgers. | `investigate`, then bounded fix if authorized |
| Heterogeneous verification packets | Audit adapters must inventory state, not infer “completed” from directory membership. | `fix` the audit description; preserve target states |
| Duplicate-inflated link diagnostics | Collector candidates need exact deduplication before semantic review and separate classification of broken expression versus absent target. | `fix` in kernel; implemented and regression-tested after the sealed run |
| Machine-local provenance | Local provenance can remain evidence without being represented as portable dependency. | `narrow` portability claims |

The post-seal collector revision now deduplicates identical Markdown targets
within each source artifact and emits an explicit root-cause group connecting
an invalid controlling JSON file to dependent native-command failures. A
regression test proves that one invalid controlling file remains one
independent finding. The original collector receipt remains unchanged as the
evidence packet reviewed by the Steward.

That original schema-v1 receipt predates collector source-hash binding,
effective-timeout capture, disposable-snapshot execution, and output
minimization. Its deterministic fingerprint binds receipt content, not the
implementation that produced it. It remains valid as disclosed pilot history,
but it is not implementation-reproducible or customer-publication-ready and
must not be reused as the proof artifact for kernel adoption or commercial
delivery.

## Cross-repository comparison

| Boundary | Operating-substrate pilot | Narrative Systems pilot | Portable kernel decision |
| --- | --- | --- | --- |
| Snapshot | Individually sealed dirty working-tree sources | Clean public commit and tree | Retain sealed identity; adapter chooses sealing method |
| Primary risk | Authority, receipt, state, and artifact-lineage contradiction | Source, generated-state, forecast, verification, and publication lineage | Retain abstract state-support test |
| Inventory scale | 476 files in latest sealed manifest | 3,231 tracked files | Retain mechanical full inventory |
| Native checks | Anyang canonical validator and privacy scan | Repository validator and strict AI harness | Retain declared-command execution receipts |
| Semantic sampling | Portfolio and Grace Gems controlling artifacts | Deterministic stratified source and trace sample | Retain deterministic repository adapter |
| Independence | Separate Steward runtime and primary-source packet | Same standard, disclosed same-model-family possibility | Retain |
| Root-cause need | Contradictions and overlapping artifact groups | Manifest cascade and link-family inflation | Retain consolidation |
| Non-portable layer | Council roles, receipts, membranes | Forecast vocabulary, archive manifest, claim lattice | Keep repository-specific |

Seven of seven defined high-consequence assurance boundaries transferred
without changing their meaning: identity, no-write proof, full mechanical
inventory, deterministic sampling, raw/semantic separation, evidence labels,
and independent root-cause review. This is `100%` provisional portable-boundary
coverage for the two-repository cohort, above the `75%` gate. It is not
evidence of universal portability.

## Value-proof scorecard

| Measure | Gate | Observed | Status |
| --- | ---: | ---: | --- |
| Decision-useful audit yield | `≥70%` | Six material finding groups each support a proposed `fix`, `retain`, `narrow`, or `investigate` disposition; System Engineer acceptance is not yet recorded | `pending adjudication` |
| Marginal setup/review-cost reduction | `≥40%` | Collector execution took 67.3 seconds across both native commands plus bounded inventory work; the first pilot has no measured normalized setup/review baseline | `not measurable` |
| Portable boundary coverage | `≥75%` | `7/7`, or `100%`, for the defined two-repository kernel | `provisional pass` |
| Mechanical collection coverage | `≥90%` | `3,231/3,231` tracked files inventoried; all requested sample groups complete; both declared native commands executed | `pass` |
| Trace reconstruction | `≥90%` | `18/20`, or `90%` | `pass at threshold` |
| First-pass finding precision | `≥80%` | Broken-link unique-diagnostic sample `30/30`, or `100%`; System Engineer material-finding acceptance pending | `provisional pass` |
| Combined System Engineer and Chief Executive review burden | `≤2 hours` | Not instrumented | `not measurable` |
| False-positive rate | `≤20%` | `0/30` sampled unique link diagnostics were false; duplicates were count inflation, not false diagnostics | `provisional pass` |
| Unauthorized writes/actions/access/transfers | `0` | `0`; tracked content and Git status unchanged; no external or private action | `pass` |
| Single-repository ontology promoted into kernel | `0` | `0` | `pass` |

## Recommended disposition

**`Revise`**

Safety, collection coverage, trace reconstruction, sampled precision, and
two-repository portability pass. Adoption remains blocked because
decision-useful yield lacks System Engineer adjudication and marginal cost
reduction lacks a measured first-pilot baseline. The missing timing evidence
may be extended into one later authorized audit; it cannot excuse a safety or
precision failure.

For the next authorized use:

1. measure Chief Executive and System Engineer review minutes explicitly;
2. record System Engineer acceptance, revision, hold, or rejection for each
   material finding group;
3. use the deduplicated collector and root-cause-group receipt;
4. retain the portable protocol plus thin collector;
5. keep every repository ontology and command set in its adapter.

No Narrative Systems remediation, issue, pull request, publication, or kernel
adoption is authorized by this recommendation.
