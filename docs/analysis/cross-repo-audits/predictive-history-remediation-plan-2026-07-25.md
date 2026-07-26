# Predictive History — Bounded Remediation Plan

**Plan ID:** `EC-XRA-PREDICTIVE-HISTORY-REMEDIATION-2026-07-25-01`  
**Prepared by:** Chief Executive  
**Authority source:** System Engineer selection `A. Prepare a bounded
Predictive History remediation proposal`  
**State:** `plan prepared — target execution, issue, pull request, commit,
push, deployment, and publication remain unapproved`  
**Target baseline:** commit
`266c3e5af765541e1b1b8c88f835adf179e1a502`, tree
`06e1d306c2954c97735f4663248d3d5954397448`  
**Accepted findings:** `PH-STW-01` through `PH-STW-08`; `PH-STW-09` remains
monitor-only  
**Controlling audit:** [transaction
record](predictive-history-2026-07-25/transaction-record.md) and [audit
packet](predictive-history-2026-07-25/audit-packet.md)

## Recommendation

Repair Predictive History in six ordered units. Start with the declared
publication path and controlling contracts, then resolve the dual-inventory
decision before regenerating indexes. Follow with YAML parsing, schema
coverage, and public-boundary portability.

Do not turn 1,105 unique broken links into an indiscriminate cleanup program.
Repair the 532-link generated family at its source, repair current controlling
and onboarding links, classify the remaining legacy debt, and preserve
historical material unless a link actively misrepresents current operation.

`gb-11` and `gb-12` require an explicit System Engineer content-state decision.
Their files demonstrate that packets exist; they do not prove whether the
chapters should be activated, retired, or excluded. No execution may silently
make that decision.

## Authority and execution boundary

This plan authorizes no Predictive History change. A later execution decision
must name:

- the exact repair units;
- the target branch or disposable worktree;
- the named executor;
- the `gb-11` and `gb-12` disposition if repair unit 2 is included;
- whether generated artifacts may be rewritten;
- required Council Steward re-review;
- whether a commit, push, issue, pull request, deployment, or publication is
  permitted.

Default proposed execution posture:

- local owner-controlled worktree at the sealed baseline;
- no private workspace, live-site, analytics, external research, or
  client-project evidence;
- no transcript, commentary, historical argument, rights, or scholarly-truth
  edits;
- no deletion of migration lineage or historical provenance;
- one reviewable diff per repair unit;
- stop on an unexpected source-of-truth disagreement;
- no commit or push without a later exact decision.

This plan is a post-audit proposal and is not part of the sealed three-artifact
audit chain.

## Repair unit 1 — Restore canonical study-edition publication controls

### Exact changes

1. In `scripts/build_study_edition.py`:
   - remove the hard-coded `book/volume-ii` source root;
   - load the canonical records from `data/cards.jsonl`;
   - resolve each supported `civ-*` transcript and commentary through its
     declared `source_paths`;
   - require resolved paths to remain inside the repository and under the
     canonical lecture surface;
   - fail once with the source ID and missing declared path when a required
     file is unavailable.
2. In `.github/workflows/study-edition-pages.yml`:
   - replace the retired `book/volume-ii/**` trigger with `lectures/**`;
   - include `data/cards.jsonl`, `data/parts/**`, and `data/spines/**`, because
     those inputs affect the rendered study edition;
   - preserve the existing least-privilege permissions and build/validation
     commands.
3. Reconcile `docs/contracts/export-contract.md` to the current
   `docs/contracts/public-repo-contract.md`:
   - identify the namespace catalog as the active public architecture;
   - identify `lectures/`, `essays/`, and `interviews/` as canonical corpora;
   - describe `ph-civ`, `ph-apo`, and `book` as compatibility or tombstone
     lineage;
   - preserve the `rbtkhn/ph-workshop` snapshot as import provenance.
4. Add focused regression coverage proving:
   - the study builder resolves `civ-*` chapters through the SSOT;
   - a declared path outside the repository is rejected;
   - missing source records fail clearly;
   - the workflow watches every declared build input and no retired source
     root.

### Acceptance

- `python scripts/build_study_edition.py --all-parts` succeeds in a disposable
  worktree.
- Every existing `scripts/validate_study_edition.py` invocation in the workflow
  succeeds.
- The active export and public-repository contracts describe one compatible
  architecture.
- No `book/` chapter becomes canonical.
- No study content, claims, or publication is changed merely to restore the
  build path.

## Repair unit 2 — Resolve chapter-inventory parity

### Required System Engineer decision

Select one disposition for both `gb-11` and `gb-12`, or decide them
individually:

1. **Activate:** add reviewed SSOT records linked to the existing public card,
   transcript, commentary, and orientation paths; then regenerate the hub and
   lecture slice.
2. **Retire:** preserve the packets and Git lineage, but mark them clearly as
   noncanonical historical material and remove current reader-routing claims.
3. **Exclude temporarily:** create one explicit machine-readable exclusion
   record with reason, authority, and review date; do not treat exclusion as
   retirement or activation.

### Exact control changes after disposition

1. Add a parity validator comparing `data/cards/*.md` with
   `data/cards.jsonl`.
2. Require every card Markdown file to be:
   - represented exactly once in the SSOT; or
   - named in the approved exclusion record.
3. Require every SSOT record to resolve its card, transcript/body, and
   commentary.
4. Remove hard-coded `206`, `147`, and related counts from tests where a
   source-derived assertion can express the same contract.
5. If activation is selected, regenerate only the full hub and namespace
   catalogs through `python scripts/generate_ph_civ_index.py`.
6. Do not manufacture publication dates, source snapshots, rights status,
   review evidence, or route membership. Missing required metadata is a stop
   condition.

### Acceptance

- Card Markdown, SSOT, full hub, and lecture-slice counts reconcile.
- `gb-11` and `gb-12` have one explicit, evidenced state each.
- The parity test fails on an unrepresented card fixture.
- No route membership or readiness state is inferred from packet existence.

## Repair unit 3 — Correct generated links and bound link debt

### Exact changes

1. In `src/civ_ph/ph_civ_index.py`, make link rendering destination-aware:
   - compute each target relative to the Markdown file being generated;
   - preserve repository-relative paths in JSON outputs;
   - emit portable forward slashes.
2. Add generator tests proving that every link emitted by the full hub and
   three namespace Markdown slices resolves from its containing directory.
3. Regenerate only the generated hub and namespace index family with
   `python scripts/generate_ph_civ_index.py`.
4. Repair current controlling and onboarding links, including the accepted
   examples in:
   - `START-HERE.md`;
   - `docs/contracts/public-repo-contract.md`;
   - `docs/onboarding/study-edition.md`;
   - `data/cards/gt-29.md`.
5. Produce a bounded internal classification during execution for the
   remaining broken links:
   - generated/current control;
   - current reader-facing;
   - historical/migrated;
   - genuinely unavailable.
6. Do not alter captured transcripts or fabricate targets. Historical links
   may remain broken when preserving provenance is more accurate than
   rewriting them.

### Acceptance

- All 532 generated slice-link failures disappear as one corrected generator
  family.
- Generated Markdown links resolve from their actual output directories.
- Current controlling and onboarding links resolve or explicitly state that
  the target is unavailable.
- Historical debt is reported separately and is not represented as current
  publication failure.

## Repair unit 4 — Restore YAML structural validity

### Exact changes

1. Quote only the unsafe scalar values in these files:
   - `lectures/great-books/gb-01/gb-01-orientation.yaml`;
   - `lectures/great-books/gb-05/gb-05-orientation.yaml`;
   - `lectures/great-books/gb-07/gb-07-orientation.yaml`;
   - `lectures/great-books/gb-09/gb-09-orientation.yaml`;
   - `lectures/great-books/gb-10/gb-10-orientation.yaml`;
   - `lectures/great-books/gb-11/gb-11-orientation.yaml`.
2. Preserve the scalar text exactly; do not rewrite or reinterpret the
   orientation content.
3. Add an explicit YAML parser dependency to the project’s validation
   environment and a test that parses every tracked orientation YAML file.
4. Validate required orientation keys separately from parse success; do not
   treat valid syntax as semantic approval.

### Acceptance

- Every tracked orientation YAML file parses.
- The six repaired scalar values are textually unchanged after parsing.
- A fixture containing an unsafe unquoted `: ` scalar fails.
- No transcript, commentary, or card-state change occurs.

## Repair unit 5 — Align and enforce public-card schemas

### Exact changes

1. Preserve `schemas/ph-civ-card.schema.json` as a compatibility surface, but
   retitle and document it as lecture-card-only.
2. Add one canonical `schemas/public-card.schema.json` capable of representing
   the active lecture, essay, and interview record families.
3. Model family-specific ID, series, part, and source-path constraints with
   explicit schema branches rather than weakening every field to unrestricted
   text.
4. Wire native validation to check every `data/cards.jsonl` row against the
   canonical public-card schema.
5. Add positive fixtures for one lecture, essay, and interview and negative
   fixtures for mixed-family IDs, invalid parts, missing sections, and
   repository-escaping source paths.
6. Update `llms-full.txt` and schema-facing documentation so downstream users
   can distinguish the generic schema from the compatibility schema.

### Acceptance

- All active SSOT records validate against the canonical public-card schema.
- The compatibility schema retains its narrower lecture meaning.
- Invalid mixed-family fixtures fail deterministically.
- Schema validation is invoked by `python -m pytest`; it is not merely a
  published but unwired artifact.

## Repair unit 6 — Complete the public-boundary and portability control

### Exact changes

1. Expand `PUBLIC_BOUNDARY_SCAN_PATHS` in `src/civ_ph/cli.py` to cover current
   public and executable surfaces omitted at the sealed commit, including:
   - `corpus`;
   - `essays`;
   - `interviews`;
   - `commentaries`;
   - `artifacts`;
   - `scripts`;
   - `site`;
   - `tests`.
2. Replace the two active `corpus/cross-volume/` machine-local links with
   repository-contained public references or an explicit statement that the
   private upstream is unavailable. Do not access or reconstruct the private
   target.
3. In `scripts/verify_gt29_youtube_asr.py`, emit a repository-relative launch
   instruction instead of `cd C:/dev/predictive-history`.
4. Preserve `artifacts/gt-29-asr-verify.md` unchanged if execution review
   confirms it is historical evidence. Classify any exclusion by exact path,
   reason, and evidence class; do not exempt the whole `artifacts/` tree.
5. Replace blanket historical exceptions with the narrowest path-specific
   exclusions necessary.
6. Add tests proving:
   - current executable and reader-facing surfaces reject machine-local and
     private-workspace markers;
   - historical provenance can be retained only through an explicit narrow
     exclusion;
   - omitted top-level public surfaces cannot silently fall outside the scan.

### Acceptance

- No active public or executable surface depends on a user-specific absolute
  path.
- Private-workspace content is neither accessed nor copied.
- Historical evidence remains intact and visibly classified.
- Boundary tests cover every declared current public surface.

## End-to-end execution order

If later authorized:

1. Reconfirm target `HEAD`, tree, remote, and clean Git-visible state.
2. Create a local disposable repair worktree from the sealed commit.
3. Execute repair unit 1 and run focused publication tests.
4. Stop for the `gb-11` and `gb-12` decision before repair unit 2.
5. Execute repair unit 2 only under that exact disposition.
6. Execute repair units 3 through 6 one at a time, validating after each.
7. Run:
   - `python -m pytest`;
   - `python scripts/build_study_edition.py --all-parts`;
   - every existing study-edition validator invocation;
   - the repaired public-boundary validation;
   - a read-only cross-repository collector against the repaired tree.
8. Obtain a separately authorized Council Steward delta review against
   `PH-STW-01` through `PH-STW-08`.
9. Return the complete diff, validation evidence, residual-link
   classification, and Steward reconciliation to the System Engineer.

No execution state becomes complete until the System Engineer accepts the
delta. A clean test run does not authorize publication or deployment.

## Completion criteria

- `PH-STW-01`, `PH-STW-02`, `PH-STW-04`, `PH-STW-06`, `PH-STW-07`, and
  `PH-STW-08` are corrected and independently rechecked.
- `PH-STW-03` has an explicit System Engineer disposition and parity is
  enforced.
- `PH-STW-05` is narrowed into corrected current controls and visible
  historical debt rather than hidden or broadly rewritten.
- `PH-STW-09` remains monitor-only unless separately elevated.
- Native tests, study build, study validators, schema validation, link
  validation, and public-boundary validation pass.
- No transcript, commentary argument, rights status, scholarly claim, private
  source, live site, external system, issue, pull request, commit, push,
  deployment, or publication is changed without separate authority.

## Stop and rollback rules

Stop immediately if:

- target HEAD or tree differs from the authorized baseline;
- `gb-11` or `gb-12` would need invented metadata or an unapproved state
  decision;
- a repair requires private-workspace access;
- generated catalogs change for reasons not attributable to the approved SSOT
  or generator repair;
- source content, review status, rights state, or historical argument would
  need substantive alteration;
- an unexpected build, schema, or boundary failure cannot be attributed to a
  named repair unit;
- publication, deployment, external communication, or a remote mutation
  becomes necessary.

Rollback by repair unit using the reviewed diff. Do not use a broad reset that
could discard unrelated work. Preserve the original audit packet and sealed
Council Steward ledger unchanged.

## Exact next System Engineer decision

- **A. Authorize mechanical phase 1 — recommended:** execute units 1, 3, 4, 5,
  and 6 locally in a disposable worktree; keep unit 2 held; return the diff,
  validation evidence, and residual-link classification without commit or
  push.
- **B. Authorize all six units and activate `gb-11` and `gb-12`:** execute the
  complete local remediation, add both packets to the SSOT, obtain a separately
  authorized Steward delta review, and return evidence without commit or push.
- **C. Hold execution:** preserve this proposal without changing Predictive
  History.
