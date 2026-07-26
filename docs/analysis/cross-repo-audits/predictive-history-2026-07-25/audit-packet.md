# Sealed Initial Council Steward Ledger

**Transaction:** `EC-XRA-PREDICTIVE-HISTORY-2026-07-25-01`  
**Assurance action:** `EC-XRA-PH-STEWARD-2026-07-25-01`  
**Review date:** 2026-07-25 (America/Denver)  
**Target:** `C:\tmp\predictive-history-preflight-20260725-01`  
**Sealed commit:** `266c3e5af765541e1b1b8c88f835adf179e1a502`  
**Sealed tree:** `06e1d306c2954c97735f4663248d3d5954397448`  
**Collector receipt:** `C:\dev\anyang-intelligence\operating-substrate\docs\analysis\cross-repo-audits\predictive-history-2026-07-25\collector-receipt.json`  
**Receipt fingerprint:** `c3186fa25f41c366ab31b87b1694b6506620a24ee77723bca073255a2b608e78`  
**Steward review time:** approximately 10 minutes of active review and synthesis. This is the Steward portion of the combined-review-burden KPI, not an end-to-end transaction duration.

## Independence disclosure

The Council Steward reviewed the authorization record and primary repository evidence before receiving any Chief Executive hypotheses or interpretation. The runtime may share a model family with the Chief Executive, but this was a separate runtime, a separately bounded evidence pass, and a separately sealed ledger. The collector receipt was treated as mechanical evidence, not as a semantic finding set. No Chief Executive framing was used.

The review was read-only except for this expressly authorized ledger. No target or Council artifact was modified. No network, live site, analytics, private system, legacy workshop, or external source was accessed. Git verification used a per-command `safe.directory` override only; no persistent Git configuration was changed.

## Executive assurance result

The sealed repository has a strong, internally testable 206-card catalog core, and all ten first-tour seed IDs reconstruct through the active card, chapter, commentary, hub, and lecture-slice surfaces. The native test result is supported: 91 tests passed in 50.98 seconds in the collector's disposable snapshot.

That passing result does not establish publication readiness. The active study-edition build is still bound to the retired `book/volume-ii` namespace, the workflow does not trigger on canonical `lectures/` changes, two Great Books packets are outside the declared card SSOT, generated slice indexes contain hundreds of broken local links, six orientation YAML files are invalid, the nominal public card schema cannot represent 59 of the 206 active cards, and the public-boundary validator omits repository areas that contain machine-local/private-workspace references.

Proposed overall disposition: **materially contested**. Preserve the supported catalog controls; separately adjudicate the accepted defects below. This is a finding disposition, not a remediation or adoption recommendation.

## Exact coverage

### Authority and target state

- Read the transaction record and collector receipt.
- Verified target `HEAD` equals `266c3e5af765541e1b1b8c88f835adf179e1a502`.
- Verified target tree equals `06e1d306c2954c97735f4663248d3d5954397448`.
- Verified target Git status was empty at the beginning and end of review.
- Reviewed collector command evidence, mutation proof, deterministic samples, inventory, diagnostics, and declared gaps.

### Governing and controlling surfaces

Reviewed all controlling paths named by the collector configuration:

1. `.github/workflows/study-edition-pages.yml`
2. `AGENTS.md`
3. `README.md`
4. `START-HERE.md`
5. `data/cards.jsonl`
6. `data/llm-experience.json`
7. `data/routes/seed.json`
8. `docs/contracts/export-contract.md`
9. `docs/contracts/public-repo-contract.md`
10. `docs/onboarding/root-directory-map.md`
11. `docs/predictive-history-index.json`
12. `docs/predictive-history-index.md`
13. `essays/predictive-history-essay-index.json`
14. `interviews/predictive-history-interview-index.json`
15. `lectures/predictive-history-lecture-index.json`
16. `pyproject.toml`
17. `schemas/pattern.schema.json`
18. `schemas/ph-civ-card.schema.json`
19. `scripts/build_study_edition.py`
20. `scripts/validate_study_edition.py`
21. `src/civ_ph/cli.py`

Also reviewed `llms.txt`, `book/README.md`, the generated slice Markdown indexes, relevant migration and onboarding references, all selected card files and their declared dependencies, and the exact files implicated by non-link diagnostics.

### Thirty deterministic chapter-card traces

Trace definition: card Markdown -> `data/cards.jsonl` SSOT entry -> declared body/transcript -> declared commentary -> full catalog -> applicable namespace slice -> route membership where declared -> visible review/public-use gate.

**Lecture sample, 15/15 inspected; 14/15 complete:**

- Complete: `civ-01`, `civ-02`, `civ-12`, `civ-18`, `civ-24`, `civ-29`, `civ-35`, `civ-53`, `geo-04`, `geo-09`, `geo-13`, `gt-06`, `sh-02`, `sh-23`.
- Incomplete: `gb-11`. Card, transcript, commentary, doorway, and orientation files exist, but `gb-11` is absent from `data/cards.jsonl`, the 206-chapter hub, and the lecture slice.

**Essay sample, 8/8 complete:**

- `essay-2025-08-26-the-secret-history-of-the-world-3`
- `essay-2025-10-01-war-machine-usa`
- `essay-2026-01-10-minnesota-burning`
- `essay-2026-03-14-vietnam-redux`
- `essay-2026-04-18-the-us-iran-war-round-two`
- `essay-2026-04-25-the-trump-new-deal`
- `essay-2026-05-16-chinas-third-center-strategy`
- `essay-2026-06-13-welcome-to-boomer-hell`

**Interview sample, 7/7 complete:**

- `interview-2026-01-05-glenn-diesen`
- `interview-2026-03-07-dialogue-works`
- `interview-2026-03-20-tucker-carlson`
- `interview-2026-04-01-jay-shapiro`
- `interview-2026-04-13-glenn-diesen`
- `interview-2026-04-13-sneako-dugin`
- `interview-2026-05-07-diary-of-a-ceo`

For the 29 SSOT-backed sampled cards, declared body and commentary files existed, source IDs matched, full-hub and applicable-slice entries existed, and the card carried an explicit review status and limits section. Route membership was not required for every catalog chapter; absence from a route was recorded as no declared route dependency, not as a defect.

### Ten first-tour seed IDs

All 10/10 were independently traced through SSOT card, card Markdown, body/transcript, commentary, full hub, lecture slice, and route seed:

`civ-07`, `civ-17`, `civ-29`, `civ-51`, `gb-02`, `gb-09`, `geo-14`, `gt-16`, `sh-16`, `sh-28`.

Nine carry `in_review`; `gt-16` carries `provisional`. Each has a visible limits statement. No scholarly or present-day claim truth was adjudicated.

### Tests, schemas, and publication path

Reviewed all 10 test modules:

- `tests/test_book_namespace_guard.py`
- `tests/test_cli.py`
- `tests/test_docs_paths.py`
- `tests/test_interview_transcript_sections.py`
- `tests/test_lecture_transcript_rails.py`
- `tests/test_patterns.py`
- `tests/test_public_surface.py`
- `tests/test_reader_namespace_guard.py`
- `tests/test_repo_identity.py`
- `tests/test_volume_i_parts.py`

Reviewed both schemas:

- `schemas/pattern.schema.json`
- `schemas/ph-civ-card.schema.json`

Reviewed the complete three-file study-edition path:

- `.github/workflows/study-edition-pages.yml`
- `scripts/build_study_edition.py`
- `scripts/validate_study_edition.py`

The collector's approved native execution returned exit 0 with 91 tests passed. The Steward did not execute additional commands beyond read-only repository and evidence inspection.

## Trace reconstruction rate

- Selected chapter-card trace instances: 29/30 complete = **96.7%**.
- First-tour seed trace instances: 10/10 complete = **100%**.
- Combined required trace instances: 39/40 complete = **97.5%**.
- Unique IDs across both sets: 39; 38/39 fully reconstructible = **97.4%** because `civ-29` appears in both sets and `gb-11` is the sole incomplete unique trace.

This rate measures repository path/state reconstruction, not truth, scholarly quality, publication readiness, or live availability.

## Accepted findings

### PH-STW-01 - Study-edition publication source path is structurally stale

**Class:** verified defect  
**Consequence:** critical for the declared GitHub Pages study edition  
**Proposed disposition:** accept as material; adjudicate separately

Evidence:

- `docs/contracts/public-repo-contract.md:10-13` declares `lectures/`, `essays/`, and `interviews/` canonical and `book/` tombstone-only.
- `book/README.md:3-5,23` states that `book/` is no longer active and forbids new canonical chapter content there.
- `scripts/build_study_edition.py:22` binds `VOL2` to `book/volume-ii`.
- `scripts/build_study_edition.py:183-189` resolves every supported study chapter under that retired directory and raises when it is absent.
- `.github/workflows/study-edition-pages.yml:31-45` runs `build_study_edition.py --all-parts` and then validates all ten parts.
- `.github/workflows/study-edition-pages.yml:6-11` watches `site/**`, study scripts, and `book/volume-ii/**`, but not the canonical `lectures/**` chapter source.

At the sealed tree, `book/volume-ii` does not exist. Therefore the declared build code cannot resolve its chapter source at this snapshot. The actual live workflow and live Pages state were outside authority and remain inaccessible; this finding is about the sealed source path, not a claim about a particular remote run.

### PH-STW-02 - A governing export contract contradicts the current namespace contract

**Class:** verified contradiction  
**Consequence:** high for operator/agent interpretation  
**Proposed disposition:** accept as material; reconcile without silently rewriting lineage

Evidence:

- `AGENTS.md:7,13-15`, `START-HERE.md:7-24`, and `docs/contracts/public-repo-contract.md:3,10-13` define the namespace catalog hub as primary and two-volume/book surfaces as deprecated or tombstone-only.
- `docs/contracts/export-contract.md:5-13` still declares the public artifact as a "two-volume public ph-civ artifact" and names `ph-civ` and `ph-apo` as the public namespaces.
- `docs/contracts/export-contract.md:17,33` continues to frame exported cards primarily as `ph-civ` cards.

The newer contract and the export contract cannot both be controlling descriptions of the current public architecture.

### PH-STW-03 - Two chapter packets are outside the declared 206-card SSOT

**Class:** verified defect  
**Consequence:** high for inventory completeness and traceability  
**Proposed disposition:** accept `gb-11` as a sampled trace failure and `gb-12` as a corroborating global parity defect

Evidence:

- `AGENTS.md:7`, `START-HERE.md:15`, and `docs/onboarding/root-directory-map.md` declare `data/cards.jsonl` the SSOT for 206 public chapters.
- `data/cards/gb-11.md:2` and `data/cards/gb-12.md:2` identify two additional card files.
- Corresponding chapter packets exist under `lectures/great-books/gb-11/` and `lectures/great-books/gb-12/`.
- Neither ID occurs in `data/cards.jsonl`, `docs/predictive-history-index.json`, or `lectures/predictive-history-lecture-index.json`.
- Repository counts are 208 card Markdown files versus 206 JSONL SSOT entries.
- `tests/test_cli.py:22,26-39` proves internal completeness only for the 206 JSONL-loaded cards; it does not compare the card directory to the SSOT.

This does not establish whether the two packets should be activated or retired. It establishes that their present state is not represented by the declared SSOT.

### PH-STW-04 - Generated slice indexes have 532 broken local navigation links

**Class:** verified defect  
**Consequence:** high for reader navigation; low effect on JSON consumers  
**Proposed disposition:** accept as one generator/path-root cause, not 532 independent design failures

Evidence:

- `lectures/predictive-history-lecture-index.md:17-22` emits targets such as `lectures/civilization/...` from a file already inside `lectures/`, which resolves as `lectures/lectures/...`.
- `essays/predictive-history-essay-index.md:16-20` emits `essays/...` from inside `essays/`.
- `interviews/predictive-history-interview-index.md:18-21` emits `interviews/...` from inside `interviews/`.
- The corresponding repository-root targets exist for all 532 exact-unique candidates in this class.
- The full hub correctly uses `../lectures/...`, `../essays/...`, and `../interviews/...`; the defect is specific to slice Markdown rendering.

Collector aggregation: 441 lecture-slice candidates, 43 essay-slice candidates, and 48 interview-slice candidates.

### PH-STW-05 - Link debt extends beyond generated slices

**Class:** verified defect set with mixed consequence  
**Consequence:** medium overall; higher where controlling/onboarding documents are affected  
**Proposed disposition:** accept as consolidated link-debt groups; do not equate the raw candidate count with independent material findings

Of 1,105 exact-unique broken-link candidates:

- 532 are the generated-slice root-path defect in PH-STW-04.
- 447 are concentrated in legacy/archive or migrated part documents.
- 126 occur elsewhere, including methodology, onboarding, route, contract, commentary, migration, skill, and individual-card surfaces.

Examples:

- `START-HERE.md:21` links to `../book/` from repository root, which leaves the repository.
- `docs/contracts/public-repo-contract.md` contains two broken links: `../data/public-surface-triage.json` and `public-surface-status.md`.
- `docs/onboarding/study-edition.md` contains six broken relative links to current data, methodology, contract, and archive surfaces.
- `data/cards/gt-29.md` links to a missing methodology target.

Raw broken-link count is 1,110; exact-unique count is 1,105. Five rows are exact duplicates, so raw volume is inflated by 0.45%. All sampled candidates were real non-resolving links as written, but consequence varies substantially.

### PH-STW-06 - Six Great Books orientation files are invalid YAML

**Class:** verified defect  
**Consequence:** medium for orientation consumers; currently missed by native tests  
**Proposed disposition:** accept as one serialization/root-cause family with six affected files

Affected files:

- `lectures/great-books/gb-01/gb-01-orientation.yaml`
- `lectures/great-books/gb-05/gb-05-orientation.yaml`
- `lectures/great-books/gb-07/gb-07-orientation.yaml`
- `lectures/great-books/gb-09/gb-09-orientation.yaml`
- `lectures/great-books/gb-10/gb-10-orientation.yaml`
- `lectures/great-books/gb-11/gb-11-orientation.yaml`

Each contains an unquoted plain scalar with an embedded `: ` sequence; for example, `gb-11-orientation.yaml:3`. The collector's YAML parser rejected all six. The tests check selected orientation-file existence in places but do not parse these six YAML payloads.

### PH-STW-07 - The nominal public card schema cannot represent the full active catalog

**Class:** verified contract mismatch; runtime consequence inferred  
**Consequence:** medium for downstream schema consumers  
**Proposed disposition:** accept mismatch; actual downstream breakage remains unobserved

Evidence:

- `schemas/ph-civ-card.schema.json:16-18` permits only lecture-style IDs: `civ|gb|geo|gt|sh`.
- `schemas/ph-civ-card.schema.json:22-45` permits only lecture series and only `civilization|world-war` parts.
- The active 206-card SSOT includes 43 essay IDs and 16 interview IDs; interview cards use `part: provenance`.
- `llms-full.txt` presents `schemas/` as public card, route, and validation schemas.
- Repository search found no native schema-validation invocation; `src/civ_ph/cli.py:719-780` implements hand-written card checks instead.

The schema is internally valid JSON but is not a schema for all active public cards despite its generic title "Public orientation card."

### PH-STW-08 - Public-boundary validation omits surfaces containing machine-local/private-workspace references

**Class:** verified control gap with environment-only subcases  
**Consequence:** medium for portability and public-boundary confidence  
**Proposed disposition:** accept the scan-coverage gap; distinguish exposed corpus references from operational examples

Evidence:

- `src/civ_ph/cli.py:111-125` scans entrypoints, `book`, `data`, `docs`, `lectures`, compatibility namespaces, prompts, and schemas, but omits `corpus/`, `interviews/`, `essays/`, `commentaries/`, `artifacts/`, `scripts/`, `site/`, and tests.
- `src/civ_ph/cli.py:137-152` explicitly forbids `strategy-codex`, `C:\`, and `C:/` where the scan runs.
- `corpus/cross-volume/consciousness-attention-continuity.md:62` and `corpus/cross-volume/sacred-order-to-eschatological-mobilization.md:55` link to `/C:/dev/strategy-codex/...`.
- `artifacts/gt-29-asr-verify.md:26` contains `cd C:/dev/predictive-history`.
- `scripts/verify_gt29_youtube_asr.py:195` emits the same machine-local command.

The two corpus references are public-portability and source-boundary defects because they point outside the repository to a machine-local strategy workspace. The artifact and script references are classified **environment-only** examples unless invoked on another machine. The private target content was not accessed.

### PH-STW-09 - Seed status vocabulary is not fully aligned in prose

**Class:** inferred risk, not accepted as a material defect  
**Consequence:** low  
**Proposed disposition:** monitor or reconcile only if the System Engineer considers status-language exactness material

Evidence:

- `data/cards/gt-16.md:7` declares `review_status: provisional`.
- `data/cards/gt-16.md:26-28` says "This entry is in review."
- The first-tour seed includes `gt-16`.

The limits paragraph remains cautionary, so no unsupported readiness claim was found. The risk is vocabulary ambiguity, not an observed authorization or publication failure.

## Mechanical candidate review and precision

### Candidate accounting

Collector candidates reviewed at category/root-cause level:

| Category | Raw | Exact-unique | Steward classification |
| --- | ---: | ---: | --- |
| broken-relative-link | 1,110 | 1,105 | 532 generated slice/root-path defects; 447 legacy/migrated-document links; 126 other current or mixed links |
| invalid-yaml | 6 | 6 | six verified parse defects, one serialization family |
| machine-local-path | 4 | 4 | two corpus boundary defects; two environment-only examples |
| link-outside-repository | 3 | 3 | one root entrypoint error; two machine-local corpus links also represented in the prior category |
| **Total** | **1,123** | **1,118** | candidates are not independent material findings |

The two corpus links are cross-category manifestations and must not be double-counted as four separate semantic findings.

### Deterministic broken-link precision sample

Population: 1,105 exact-unique broken-relative-link candidates after grouping on `category|path|evidence`.

Selection method:

1. For every exact-unique candidate, calculate SHA-256 of  
   `266c3e5af765541e1b1b8c88f835adf179e1a502|diagnostic_id`.
2. Sort ascending by the hexadecimal hash.
3. Inspect the first 40 candidates.
4. Resolve each target exactly as Markdown would from its source file, remove only a fragment for filesystem existence testing, and separately test whether the same text identifies an existing repository-root target.

Results:

- 40/40 did not resolve as written: **100% point precision** for the collector's broken-link label.
- Approximate 95% Wilson interval: **91.2% to 100%**.
- 22/40 (55.0%) pointed to existing repository-root targets but were emitted as local relative paths.
- 17/40 (42.5%) were stale/moved documentation targets.
- 1/40 (2.5%) was another missing target.
- 0/40 were false positives.

All 13 non-link candidates were directly inspected rather than sampled. Detection precision was 13/13: all six YAML files failed for the stated syntax condition, all four files contained a machine-local path pattern, and all three links left the repository. Semantic consequence was then classified separately.

## Supported controls

1. **Sealed-state reproducibility:** commit, tree, clean status, tracked inventory, and receipt fingerprint are explicit and consistent.
2. **Native test baseline:** the collector executed only the approved `python -m pytest` command in a disposable snapshot; 91 tests passed, with no target mutation.
3. **SSOT-backed catalog integrity:** all 206 JSONL cards have unique declared transcript and commentary paths, and the generated hub and namespace JSON slices agree with that 206-card set.
4. **Required seed traceability:** all ten first-tour seed IDs resolve through active repository evidence.
5. **Visible epistemic gates:** card `review_status`, limits sections, commentary open-canvas status, and repeated "not final scholarly review" language constrain interpretation.
6. **Tombstone guards:** tests expressly prevent `book/` from regaining canonical content and reject deprecated reader namespaces as active surfaces.
7. **Human judgment boundary:** `docs/contracts/public-repo-contract.md` reserves selection, rights prudence, cultural balance, emotional calibration, and final public responsibility to human curators.
8. **Least-privilege workflow declaration:** the Pages workflow requests read access to contents and only the Pages/id-token permissions needed for deployment. This is source inspection, not verification of live GitHub enforcement.

## Root-cause consolidation

| Root cause | Manifestations |
| --- | --- |
| RC-01 incomplete namespace migration | stale study build source, stale workflow triggers, conflicting export contract, substantial archived/migrated link debt |
| RC-02 slice-index path-base error | 532 links point to existing repo-root targets but are emitted relative to slice files |
| RC-03 dual card inventories without parity guard | `cards/*.md` has 208 files while `cards.jsonl` has 206; `gb-11` and `gb-12` are unrepresented |
| RC-04 unsafe YAML scalar serialization | six Great Books orientation files fail on unquoted embedded colons |
| RC-05 accumulated documentation relocation debt | 447 legacy/migrated and 126 other broken-link candidates; five exact duplicate rows inflate raw count slightly |
| RC-06 incomplete public-boundary scan surface | machine-local/private-workspace references survive in omitted `corpus/`, `artifacts/`, and `scripts/` areas |
| RC-07 legacy, unwired schema ontology | public card schema covers lecture IDs only and is not invoked by native validation |

## Portable controls versus repository-specific ontology

**Portable audit-control kernel:**

- seal commit/tree and compare pre/post status;
- retain deterministic collector fingerprint and command evidence;
- distinguish candidates from findings and collapse shared root causes;
- deterministic hash-ranked precision samples with an explicit population;
- reconstruct declared SSOT-to-artifact-to-index-to-route traces;
- inspect status/publication gates;
- separate verified defects, inferred risks, inaccessible evidence, environment-only failures, and supported controls;
- disclose runtime/model-family independence limits;
- seal initial review before reconciliation.

**Predictive History adapter required:**

- `source_id` families and the 206-card `cards.jsonl` ontology;
- lecture/essay/interview namespace classification;
- card -> transcript/body -> commentary -> hub/slice mappings;
- first-tour seed and route semantics;
- review-status and commentary-canvas vocabulary;
- legacy `ph-civ`, `ph-apo`, `book`, Volume I/II, and Homer-to-Tolstoy compatibility rules;
- study-edition part/chapter layout;
- pattern and public-card schema expectations.

These repository-specific terms are not portable merely because the assurance method is.

## Inaccessible evidence and coverage gaps

- No live GitHub Pages state, workflow-run history, branch protection, analytics, audience behavior, or external availability was inspected.
- No legacy `rbtkhn/ph-workshop`, private strategy workspace, source media, or external source URL was accessed.
- Transcript, essay, interview, historical, geopolitical, theological, and scholarly truth was not adjudicated.
- Rights, consent, licensing, quotation accuracy, and human-curator approvals were not independently evidenced.
- Ignored and untracked files were outside the collector's tracked snapshot; the target itself was observed clean.
- The 30-card sample is deterministic and useful for trace controls but is not a content-quality sample of all 206 active cards.
- Broken-link semantic precision is estimated from 40 deterministic exact-unique candidates; category-level counts for unsampled links are root-cause classifications, not individual severity adjudications.
- Actual downstream use of the two schemas was not visible; schema consumer failures remain inferred.
- The study-edition build was source-inspected but not separately executed by the Steward because the authorization named only the collector's native pytest command.

## Seal statement

This is the Council Steward's **sealed initial ledger** for `EC-XRA-PREDICTIVE-HISTORY-2026-07-25-01`. It records the first independent interpretation of the authorized evidence boundary. Later evidence, Chief Executive interpretation, System Engineer adjudication, or remediation may be appended as separately attributable reconciliation records, but must not silently rewrite this initial ledger or represent its findings as broader than the sealed commit, tree, and stated coverage.

---

# Chief Executive Reconciliation

**Prepared after Steward seal:** yes

**Sealed Steward-ledger prefix length:** 25,205 bytes

**Sealed Steward-ledger SHA-256:**
`3B72DC42549B32A8F215AAAA275124DE7E84D84FDCEDD0307AC3AD43032CF58B`

The preceding 25,205-byte prefix is the independently produced Council
Steward ledger. This reconciliation is an appended Chief Executive judgment
layer and does not modify or replace that ledger.

## Structural conclusion

The third benchmark validates the audit kernel's central value proposition:
native tests can pass while material repository-operability and publication
claims remain contradicted by controlling evidence. The portable controls
worked across governance, research-archive, and public-distribution
repositories without importing a shared domain ontology.

The correct kernel disposition remains `revise`, not `adopt`. Predictive
History is technically different from the first two repositories, but it
shares intellectual and source lineage with Narrative Systems. System
Engineer finding acceptance, fully instrumented review burden, clean
environment-variable support, and an unrelated owner-controlled benchmark
remain incomplete.

## Operating implications

| Finding | Chief Executive classification | Operating implication | Authority state |
| --- | --- | --- | --- |
| `PH-STW-01` stale study-edition source path | `fix` | Treat sealed-source publication readiness as contested; repair only under later target authority | held |
| `PH-STW-02` conflicting export contract | `fix` | Reconcile the public namespace contract while preserving migration lineage | held |
| `PH-STW-03` two packets outside SSOT | `investigate` | Decide whether `gb-11` and `gb-12` should be activated, retired, or explicitly excluded before changing indexes | held |
| `PH-STW-04` 532 generated slice links | `fix` | Correct the slice-index path-base generator as one root cause, not hundreds of independent decisions | held |
| `PH-STW-05` remaining link debt | `narrow` | Prioritize controlling and reader-facing surfaces; do not turn all legacy debt into one remediation backlog | held |
| `PH-STW-06` invalid orientation YAML | `fix` | Repair the six serialized files and add structural parsing coverage | held |
| `PH-STW-07` incomplete public-card schema | `narrow` | Either rename the schema as lecture-only or expand and wire it for all active card types | held |
| `PH-STW-08` incomplete public-boundary scan | `fix` | Expand coverage to public corpus and tooling surfaces while retaining environment-only distinctions | held |
| `PH-STW-09` status-language ambiguity | `retain` | Monitor; do not elevate cautious wording variance into material remediation | no action recommended |

No classification above approves a target change.

## Cross-repository comparison

| Boundary | Operating substrate | Narrative Systems | Predictive History | Portable decision |
| --- | --- | --- | --- | --- |
| Repository role | Council governance and project portfolio | Research archive and forecasting system | Public catalog, CLI, and study distribution | retain repository-specific adapters |
| Native checks | broad governance validator | native validator and strict harness failed | 91 tests passed | native success and failure both require semantic review |
| Highest-value defect pattern | contradictory state and missing receipts | one malformed controlling manifest caused a cascade | passing tests omitted stale publication and SSOT boundaries | retain controlling-source trace review |
| Source-of-truth trace | authority and receipt lineage | source manifest to synthesis/forecast/verification | cards SSOT to chapter, indexes, routes, and publication gate | retain abstract SSOT-to-output tracing |
| Diagnostic compression | artifact groups and unsupported claims | 510 candidates consolidated into root causes | 1,123 candidates consolidated into nine findings and seven roots | retain candidate/finding separation |
| Independence | separate Steward pilot | separate sealed Steward ledger | separate sealed Steward ledger before executive framing | retain |
| Context membrane | project-labeled Council state | no geopolitical truth adjudication | no scholarly, live-site, or private-workshop adjudication | retain |
| Domain ontology | Council roles and receipts | forecast and verification vocabulary | chapter, route, catalog, and compatibility vocabulary | never merge automatically |

## Kernel value-proof scorecard

| Adoption gate | Target | Predictive History result | Status |
| --- | ---: | --- | --- |
| Decision-useful audit yield | `>=70%` | `PH-STW-01` through `PH-STW-08` accepted as material; `PH-STW-09` retained as a monitored low-risk inference | pass |
| Marginal setup and review cost reduction | `>=40%` | collector 52.8 seconds; Steward approximately 10 minutes; proposal/preflight, Chief Executive, System Engineer, and normalized first-pilot durations: `Missing` | not measurable |
| Unchanged portable high-consequence controls | `>=75%` | sealed identity, disposable collection, deterministic sampling, candidate/finding separation, trace reconstruction, evidence classes, root-cause consolidation, and independent seal all transferred | pass |
| Mechanical collection coverage | `>=90%` | 1,332/1,332 tracked files inventoried; command and all six sample groups completed | pass |
| Trace reconstruction | `>=90%` | 39/40 required trace instances, or 97.5% | pass |
| First-pass finding precision | `>=80%` | 40/40 sampled unique broken links genuine as written; all 13 non-link candidates directly confirmed | pass |
| Combined System Engineer and Chief Executive burden | `<=2 hours` | Steward approximately 10 minutes; Chief Executive review time: `Missing`; System Engineer review time: `Missing` | pending |
| False positives | `<=20%` | 0/40 in deterministic broken-link sample; semantic consequence still varied | pass |
| Unauthorized events | `0` | zero target writes, private access, live-site access, external action, or protected-context transfer observed | pass |

## Skill performance

The `executive-council-audit` skill successfully:

- stopped at proposal mode until a repository and bounded preflight were
  selected;
- separated preflight authority from full-audit authority;
- required an exact commit, tree, command, timeout, sample, executor,
  persistence path, expiry, and held-action list;
- invoked the versioned collector rather than duplicating it;
- preserved Council Steward independence and the sealed-ledger prefix;
- kept mechanical diagnostics separate from semantic findings;
- constrained the output to the three-artifact chain;
- prevented remediation or adoption from being inferred.

The skill remains `pilot`. One improvement is indicated: its configuration
reference should eventually support a bounded, explicit command-environment
contract so repositories that declare `PYTHONPATH`, locale, or similar
read-only runtime requirements do not require shell indirection. No skill or
collector change is authorized by this audit.

## Chief Executive recommendation

Recommend `revise`:

1. accept or revise each material Steward finding;
2. retain the skill and portable assurance envelope as a pilot;
3. instrument Chief Executive and System Engineer review minutes in the next
   benchmark;
4. prepare, but do not yet implement, a bounded collector environment-field
   design;
5. require one unrelated owner-controlled repository before commercial or
   universal-portability claims;
6. authorize Predictive History remediation only through a later, separate
   target-specific decision.

## System Engineer disposition

**Decision ID:** `EC-XRA-PH-DISPOSITION-2026-07-25-01`

**Decision source:** explicit selection `A. Accept the findings and classify
the kernel as revise` in the active Codex task on 2026-07-25

**Material findings:** accepted for the sealed commit and stated evidence
boundary:

- `PH-STW-01` through `PH-STW-08` are accepted as material findings;
- their Chief Executive classifications remain operating recommendations, not
  repair authority;
- `PH-STW-09` is retained as a monitored low-risk inference with no action
  authorized.

**Kernel:** `revise`. Retain the audit skill and portable assurance envelope
as a pilot. Do not represent the kernel as adopted, commercially proven, or
universally portable.

**Target remediation:** not authorized

**Still held:** target writes, fixes, issues, pull requests, commits, pushes,
publication, external communication, private or live-system access, further
Council Steward source expansion, and kernel adoption

**Audit state:** `adjudicated — findings accepted; kernel revise`
