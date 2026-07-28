# SEALED INITIAL LEDGER

**Transaction:** `EC-XRA-CIVILIZATION-MEMORY-2026-07-26-01`  
**Steward runtime:** `/root/executive_council_steward_pilot_01`  
**Evidence boundary:** tracked public files at commit `ce8ac249cdf5a3d6a840926863ce59d9d3ecbe2e`, tree `a4e13027c074cf3deb5c103912dc46d4826e41a5`  
**Seal state:** initial, advisory, pending System Engineer adjudication

## Findings

**CS-01 — Governance command reports drift but exits green**

- **Classification:** verified defect
- **Significance:** High; exit status cannot support a governance-consistency claim.
- **Evidence:** receipt `commands[id=governance-consistency]` records exit `0` while stdout reports four stale AMERICA source-version rows and 25 missing mandatory connection sections. `tools/cmc-governance-checks.sh` prints `DRIFT`/`WARN` but never exits nonzero for them.
- **Scope:** 29 reported discrepancies in the authorized run. Independent table inspection found eight stale source-version rows across AMERICA, CHINA, and INDIA; the native command checks only AMERICA.
- **Confidence/limits:** High; repository structure and command behavior, not historical truth.
- **Disposition:** Accept; treat the green result as informational output only, not assurance.

**CS-02 — The tracked MEM corpus fails its declared minimum validator**

- **Classification:** verified defect
- **Significance:** High; the corpus does not satisfy the two structural claims actually enforced.
- **Evidence:** receipt `commands[id=full-mem-validation]`, exit `1`; `tools/cmc-validate-corpus.py`. An independent read-only application of its exact predicates found 859 missing exact `MEM CONNECTIONS (MANDATORY)` labels and 59 header/footer mismatches: 918 reportable issues over 1,282 `MEM*.md` inputs.
- **Confidence/limits:** High for those two predicates. Receipt stdout is truncated, so exact totals come from primary-file scanning, not the receipt’s captured tail. This does not assess deeper evidentiary or historical quality.
- **Disposition:** Accept; withhold corpus-compliance assurance.

**CS-03 — Native validation has vacuous and weak green paths**

- **Classification:** verified defect
- **Significance:** High; nominally green checks do not cover their advertised claims.
- **Evidence:**  
  - Exact chronicle command returns `Validation passed: 0 day(s)` and exit `0` for `IRAN–WAR–CHRONICLE.md`, which contains ten `## Day N · date` sections. CRLF line endings prevent `splitSections()` from matching its LF-only title expression in `scripts/validate-chronicle.mjs`.
  - `cmc-validate-corpus.py` compares versions only when both header and footer are present. Primary scan found 426 files missing at least one endpoint—11 missing headers, 417 missing footers, two missing both—without a corresponding parity failure.
  - In changed-only mode, a failed `git diff` becomes an empty selection and exits green.
- **Confidence/limits:** High. The full corpus command remains red for other reasons; the finding concerns uncovered failure modes.
- **Disposition:** Accept; do not infer chronicle or metadata health from current green paths.

**CS-04 — Canonical registries and centralized compliance truth are stale**

- **Classification:** verified defect
- **Significance:** High; discovery, parity, and compliance surfaces do not reliably represent tracked canon.
- **Evidence:** `CIV–INDEX–*.md`, `COMPLIANCE–REGISTRY.md`, `VERSION–MANIFEST.md`, and filesystem comparison.
- **Scope:** Active index comparison found nine existing MEMs absent from registers and nine active register entries without matching files across seven of ten indexes; Germany, India, and Persia were clean under the same test. The compliance registry declares 1,019 files across nine civilizations versus 1,163 current canonical MEMs in those civilizations, and omits AMERICA’s 113 entirely. All nine declared civilization counts are stale. Its header says v3.5 while its footer says v1.0.
- **Confidence/limits:** High after excluding `MEM–RELEVANCE` and historical-note-only references. Compliance statuses themselves were not recomputed against every substantive criterion.
- **Disposition:** Accept; withhold reliance on INDEX/compliance parity.

**CS-05 — Governance bundle is not a current canonical snapshot**

- **Classification:** verified defect
- **Significance:** High for downstream adopters and validators.
- **Evidence:** `docs/governance/GOVERNANCE–BUNDLE–SPEC.md` requires version bumps and as-is snapshots; `governance-bundle/v1.0/CIV–MEM–CORE.md` and `CIV–MEM–TEMPLATE.md` remain v3.4 while controlling sources are v3.5. Their SHA-256 hashes differ. The manifest lacks source commit/hashes and emits `template_sections_sample`, while the active contract names `template_sections`.
- **Scope:** Both copied governing files plus the machine-readable manifest.
- **Confidence/limits:** High; content-composition semantics were not exhaustively compared.
- **Disposition:** Accept; do not treat bundle v1.0 as current governing truth.

**CS-06 — Generated graph is stale and lacks freshness proof**

- **Classification:** verified defect
- **Significance:** Medium-high; graph-based discovery omits canonical nodes.
- **Evidence:** `.graph/graph.json` contains 1,261 unique nodes; `tools/cmc-graph-export.py` currently selects 1,281 `MEM–*.md` paths. Set comparison found 20 missing nodes and zero extraneous nodes. `.graph/.cache.json` is absent.
- **Confidence/limits:** High for node parity; edge semantics were not exhaustively recomputed.
- **Disposition:** Accept; withhold complete-graph assurance.

**CS-07 — Recovery beyond Git is partial and placeholder-only**

- **Classification:** inferred risk
- **Significance:** High if corpus-swap reconstruction is relied upon.
- **Evidence:** `.skeleton` contains 132 tracked Markdown files, all under ROME; its cache reports `written:132`, `skipped:78`, totaling ROME’s 210 inputs but does not record scope. `tools/cmc-regenerate.py` explicitly identifies itself as a stub, ignores corpus content, and copies skeleton placeholders while recording unimplemented retrieval/generation extension points.
- **Confidence/limits:** High about implementation state; no claim that the pinned Git snapshot itself is unrecoverable. Remote retention, backups, and an actual restore exercise were outside scope.
- **Disposition:** Hold any non-Git recoverability claim pending direct restore evidence.

**CS-08 — Collector MEM sampling is contaminated and skeleton sampling is absent**

- **Classification:** collector candidate — not adjudicated
- **Significance:** Medium; sample-derived rates would be biased.
- **Evidence:** receipt `samples[id=civilization-mems]`: seven of 60 selected paths are under `.skeleton`, and `eligible:1414` equals the mixed canonical/derived population. Among the 53 canonical selections, 40 lack the exact mandatory label and two have version mismatch; all seven derived files contain the mandatory label. Receipt `samples[id=generated-skeleton]` reports `eligible:0`, selected `0/20`, despite 132 tracked skeleton Markdown files.
- **Confidence/limits:** High for receipt/path facts; collector matching internals were not adjudicated. The authorized deterministic 20-file skeleton sample is unavailable.
- **Disposition:** Exclude the mixed MEM sample from quantitative assurance and record generated-skeleton evidence as unavailable.

**CS-09 — Console architecture link is broken**

- **Classification:** verified defect
- **Significance:** Low.
- **Evidence:** `tools/cmc-console/README.md:56` links to `../ARCHITECTURE.md`; neither that target nor a local console `ARCHITECTURE.md` exists.
- **Disposition:** Retain as a low-significance documentation defect.

## Non-findings and false positives

- Target commit/tree matched exactly; checkout status was clean. Receipt mutation fingerprints also match before/after.
- No authorized command timed out or produced stderr. The corpus failure is repository-content failure, not environment-only failure.
- A sampled lineage trace is observable: `MEM–CHINA–LIT–ROMANCE–THREE–KINGDOMS` appears in the MEM, CHINA index, CHINA SCHOLAR, CHINA STATE, and graph with three incident edges. This verifies one trace, not corpus-wide lineage.
- The collector’s `link-outside-repository` diagnostic for `SIMPLIFICATION_OPPORTUNITIES.md` is a false positive caused by a regex literal, not a repository link.
- Machine-local paths in three console documents are real but occur in setup/test examples; they are not elevated here into semantic defects.
- No environment-only failure was identified.

## Coverage and precision limits

- External historical/source truth, private systems, ignored/untracked files, live console behavior, dependencies, and deployment were not inspected.
- The receipt contains no declared-outcome trace field; the trace above was independently assembled from primary files.
- Full-validator stdout was truncated in the receipt, and `root_cause_groups` is empty.
- Governance documents were sampled 30/238; all indexes, cores, states, scholars, cursor rules, bundle files, and graph requested by the receipt were selected, except generated skeletons at 0/20.
- The deterministic MEM sample is effectively 53 canonical plus seven derived files, not 60 canonical MEMs.
- No broad claim is made about STATE files lacking the parsed source-version table format.

## Council conclusion

The pinned Git snapshot provides identifiable controlling files and demonstrates at least one functioning MEM→INDEX→SCHOLAR/STATE→graph lineage. It does not presently substantiate the stronger assurance claim that governance checks enforce their findings, canonical registries remain aligned, derived surfaces mirror canon, or corpus-swap recovery is implemented.

The initial Council position is therefore **assurance not established at this commit**, with findings remaining advisory until System Engineer adjudication.

**Independence disclosure:** this was a separately identified logical review runtime that did not solicit or adopt Chief Executive hypotheses. It remains within the same Codex/OpenAI provider and model family and shared tooling environment; independence is procedural and evidentiary, not provider-, model-, or infrastructure-independent.

---

# Chief Executive Interpretation

## Ledger seal

The Council Steward ledger above was sealed before this interpretation was
added:

- sealed ledger bytes: `10,321`;
- sealed ledger SHA-256:
  `803ef050c0f9e5401d6744d3591982db7aa298532261bc314aa5ecdeb1211136`;
- sealed ledger extent: lines 1–111 of the pre-interpretation artifact;
- seal time: `2026-07-26T22:44:55-06:00`.

The interpretation below does not alter the Steward's classifications.

## Executive answer

At a fundamental level, the audit tested whether Civilization Memory has a
trustworthy chain from canon to decision:

`governing source → corpus → registry/index → derived surface → green check`

That chain exists conceptually and is visible in at least one end-to-end
trace. It is not presently reliable as an assurance system. The decisive
failure is not that some files are old. It is that multiple controls can emit
green while observing drift, selecting zero records, or silently skipping
missing evidence.

The repository therefore remains valuable as a knowledge corpus and as a
governance design. At the sealed commit, it should not be represented as
having established corpus-wide compliance, complete graph parity, a current
portable governance bundle, or non-Git reconstruction capability.

## Recommended finding disposition

The Chief Executive recommends:

- **accept CS-01 through CS-07 and CS-09** on the evidence and limits stated
  by the Steward;
- **accept the factual basis of CS-08** and retain its
  `collector candidate — not adjudicated` classification until the collector
  is separately reviewed;
- **hold all remediation** until the System Engineer explicitly authorizes a
  remediation-planning transaction.

## Decision priority

If remediation planning is later authorized, sequence the decision work as:

1. **Restore fail-closed assurance.** A successful command must mean the
   asserted property was tested on a non-empty, valid population and passed.
2. **Reconcile controlling truth.** Bring registry, INDEX, bundle, and graph
   surfaces into declared parity with canon, with source commit and freshness
   evidence.
3. **Bound recovery claims.** Distinguish Git restoration from corpus-swap
   reconstruction, label partial artifacts by scope, and require a restore
   exercise before claiming recoverability.
4. **Repair audit instrumentation.** Correct the collector's canonical/derived
   sampling boundary and preserve complete command summaries.
5. **Clear low-risk documentation drift.** Repair the broken console
   architecture link after assurance-critical work.

## ROI judgment

The audit returned high decision value because it changed the meaning of the
repository's green signals. It found:

- a governance check that exits `0` while reporting 29 discrepancies;
- 918 minimum-validator issues across 1,282 selected corpus files;
- a chronicle check that passes after parsing zero of ten day sections;
- 426 files for which version parity can be silently untested because an
  endpoint is absent;
- a centralized registry that trails current canon and omits AMERICA;
- a governance bundle and graph that do not mirror current controlling
  sources;
- a reconstruction path explicitly implemented as a placeholder stub.

Without this audit, maintenance could optimize content while relying on
controls that cannot distinguish healthy state from unexamined or known-bad
state. The highest-return next investment is therefore not broad content
cleanup. It is a small assurance-hardening plan that makes every future green
signal decision-safe.

## System Engineer adjudication gate

No finding authorizes a repository change. The next authorized action must be
one of:

- **A — Accept and plan:** accept the recommended dispositions and authorize
  a separate, bounded remediation plan only;
- **B — Accept and hold:** accept the findings but authorize no further work;
- **C — Revise:** identify finding IDs whose classification or scope should be
  reconsidered;
- **D — Reject and close:** reject the recommendation and close the
  transaction without remediation.
