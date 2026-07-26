# Narrative Systems — Bounded Remediation Plan

**Plan ID:** `EC-XRA-NARRATIVE-SYSTEMS-REMEDIATION-2026-07-25-01`  
**Prepared by:** Chief Executive  
**Authority source:** System Engineer selection `B. Prepare remediation`  
**State:** `plan prepared; target execution, commit, push, issue, and publication remain unapproved`  
**Target baseline:** commit
`5be49ca8765aa803ca7b90b085b0325066a008f0`, tree
`c28644cb2c7cd0d84e143b7fd1e14fe938356ba4`

## Recommendation

Repair Narrative Systems in six ordered units. Begin with the authoritative
manifest and validator failure mode, then correct downstream state and
generated-link controls. Do not perform broad cleanup, rewrite captured source
bodies, investigate geopolitical claims, close verification requests, or
restore missing evidence by inference.

Each unit must remain separately reviewable and reversible. A failure in one
unit stops later units until the System Engineer accepts the changed state or
returns it for revision.

## Authority and execution boundary

This plan authorizes no target-repository change. A later execution receipt
must name:

- the target branch or worktree;
- the exact repair units authorized;
- the named executor;
- whether commits are permitted;
- required Council Steward re-review;
- whether any push or pull request is permitted.

Default execution posture:

- local target worktree only;
- no external research or private repositories;
- no source-body rewriting;
- no new verification evidence;
- no forecast resolution;
- no publication, issue, pull request, commit, or push;
- stop on unexpected source/manifest disagreement or substantive state
  ambiguity.

## Repair unit 1 — Restore the authoritative manifest gate

### Exact changes

1. Remove the trailing comma after the final source object in
   `narrative-geopolitics/archive/source-manifest.json`.
2. Preserve all 1,895 rows, their order, metadata, and hashes. Do not regenerate
   or re-sort the manifest merely to repair syntax.
3. Harden `scripts/validate_repository.py` so malformed controlling JSON
   produces one root diagnostic instead of a traceback and dependent cascade:
   - parse the manifest once before manifest-dependent checks;
   - on `JSONDecodeError`, report its repository-relative path, line, and
     column;
   - skip only `archive_manifest_failures`, `daily_run_failures`, and
     `voice_routing_failures`;
   - continue independent checks;
   - do not represent skipped checks as passes.
4. Add a regression fixture to `tests/test_entropy_reduction.py` proving:
   - malformed manifest JSON returns one controlling parse failure;
   - manifest-dependent checks are marked unavailable rather than repeated;
   - an independent broken-link failure is still reported;
   - no traceback escapes the validator.

### Known post-repair baseline

A read-only in-memory parse after removing only the trailing comma found:

- declared source count: 1,895;
- manifest rows: 1,895;
- duplicate local paths: 0;
- manifest rows missing files: 0;
- archive files missing rows: 0.

Any different result during execution is a stop condition.

### Acceptance

- `python -m json.tool narrative-geopolitics/archive/source-manifest.json`
  succeeds.
- The manifest/archive parity check returns the exact known baseline above.
- A deliberately malformed test fixture yields one root failure.
- No archive source body changes.

## Repair unit 2 — Correct daily-run state and generated path rebasing

### Exact changes

1. Treat the 2026-07-23 downstream packet as intake-only and unexecuted:
   - keep `sources.md` and its landed source accounting;
   - change `synthesis.md` and `forecast.md` from `live-intake-first` to an
     explicit template/unexecuted state;
   - retain `judgment.md` as `template`;
   - retain `daily-brief.md` as `not-promoted`;
   - add one plain state note: no synthesis, operational claim, story lineup,
     forecast, judgment, issue, or publication was adopted;
   - remove no historical files and manufacture no analytical content.
2. Correct daily-output method links under the affected July 20–23 daily
   directories from template-relative `../method/...` to daily-relative
   `../../../method/...`.
3. Update the daily bootstrap/render path so template links are rebased when
   copied into `work/daily/YYYY-MM-DD/`; do not change the template’s own
   correct `../method/...` links.
4. Extend daily validation:
   - a `live-intake-first` synthesis containing `delta-v1` placeholders fails;
   - a forecast containing `NG-YYYYMMDD-*` under a live status fails;
   - a reader brief containing title/story placeholders remains
     `not-promoted` and cannot satisfy completion;
   - template/unexecuted state remains permitted but cannot be called
     synthesized, forecast-ready, issued, or complete.
5. Add tests covering the July-23-shaped failure and correct rebasing for a
   newly bootstrapped daily directory.

### Acceptance

- The July 23 date reconstructs as `intake complete; downstream unexecuted`.
- No placeholder ID is counted as a real claim, story, or forecast.
- All affected daily method links resolve.
- The validator rejects the same live/template conflation in a fixture.

## Repair unit 3 — Reconcile July 20 forecast timing and ledger completeness

### Evidence controlling the correction

Git history shows `forecast.md`, including `NG-20260720-F01` and
`NG-20260720-F02`, first appears in commit `5be49ca…` on 2026-07-25. The
repository does not support its present “same-day live-intake-first” timing
claim for July 20.

### Exact changes

1. Preserve both forecast hypotheses and their original source-run date.
2. Correct `NG-20260720-F01` in the central ledger:
   - authored no later than: `2026-07-25`;
   - timing provenance: `git_commit_upper_bound`;
   - forecast type: `retrospective_hypothesis`;
   - resolution status: `excluded_retrospective`;
   - accountable: `no`;
   - review note: historical hypothesis retained; same-day authorship is not
     evidenced.
3. Add the missing `NG-20260720-F02` entry and matching triage row with the
   same conservative timing classification.
4. Update the entry-table statuses to match the triage statuses.
5. Do not score either hook, resolve either outcome, or create verification
   evidence.
6. Strengthen `scripts/validate_daily_run.py`:
   - a forecast hook absent from the central ledger is a failure at forecast,
     issue, and publication stages, not a warning;
   - intake and synthesis stages may report it as pending;
   - every inserted ledger hook requires one matching accountability row.
7. Add regression tests for missing-hook rejection and conservative
   retrospective registration.

### Acceptance

- Both hook IDs appear exactly once in the entry table and once in
  Accountability Triage.
- Entry and triage statuses match.
- Neither hook is calibration-eligible or accountable.
- No verification packet or world-state claim is created.

## Repair unit 4 — Repair generated Markdown lineage

### Exact changes

1. Fix generated source references in:
   - `scripts/thesis_track.py`;
   - `scripts/voice_comparison.py`.
2. Compute Markdown paths relative to the generated report’s destination
   directory. Do not emit repository-root paths as nested relative links.
3. Represent source line numbers as adjacent text such as `line 47`, not as a
   filesystem suffix `source.md:47`. Do not invent Markdown headings to mimic
   line anchors.
4. Add generator tests proving:
   - rendered source paths resolve from the output directory;
   - line metadata remains visible;
   - no generated link target ends with `:N` or `:N-N`;
   - Windows and POSIX path inputs render portable forward-slash links.
5. Regenerate only the derived artifacts owned by the corrected generators.
6. Regenerate the historical-reference comparison with its recorded cohort:
   `freeman,diesen,davis,crooke,mearsheimer`, including the five voice ledgers
   and review queue. This removes stale references to source paths no longer
   present in the current manifest.
7. Classify remaining link failures:
   - repair generated/internal links;
   - preserve links captured inside archive source bodies;
   - do not fabricate targets for genuinely absent evidence;
   - record absent targets as coverage gaps.

### Acceptance

- Native non-archive Markdown link validation returns zero failures.
- A cross-repo collector scan reports no duplicate-inflated generated-link
  family.
- Captured archive source text remains byte-identical.
- Generated counts and review states change only where current manifest
  membership or corrected link rendering requires it.

## Repair unit 5 — Preserve verification packet state accuracy

No verification packet content should change in this remediation.

The controlling inventory must continue to report:

- `VER-20260710-01`: `assessed`, `operationally_contested`, not closed;
- `VER-20260714-01`: `requested`, `not_investigated`, zero evidence chains;
- `VER-20260724-01`: `closed`, `operationally_supported` for its bounded
  public-language observable.

Replace only any discovered aggregate wording that calls all three
“completed.” Directory membership, an existing packet shell, assessment, and
closure remain distinct states.

### Acceptance

- Packet bodies and evidence records are unchanged.
- State inventory reports one requested, one assessed, and one closed packet.
- No packet is closed, promoted, or treated as supporting without independent
  evidence and its existing authority gate.

## Repair unit 6 — Separate portability from historical provenance

### Exact changes

1. Replace active machine-specific dependencies:
   - make the Predictive History external root an explicit runtime input and
     render its authority surface as an abstract external lane, not
     `C:\dev\predictive-history`;
   - require `scripts/prepare_statecraft_backfill.py` to receive an explicit
     upstream root rather than defaulting to
     `C:\dev\strategy-codex\source-archive\statecraft`;
   - replace the startup prompt’s absolute repository path with a
     repository-root instruction;
   - replace current demo commands that embed a user cache interpreter with
     repository launchers.
2. Preserve machine-local strings when they are historical provenance in:
   - archive source bodies;
   - migration receipts;
   - prior inventories;
   - verification source records.
3. Label preserved paths as historical or environment-specific; do not claim
   they are currently accessible.
4. Add a current-guidance portability test that scans executable scripts and
   active instructions while excluding sealed history, captured sources, and
   migration evidence.

### Acceptance

- No active command or runtime contract depends on a user-specific absolute
  path.
- Historical provenance remains intact.
- Missing external lanes fail as `unavailable`, not as absent evidence or
  repository corruption.

## End-to-end validation and reconciliation

Run in this order:

1. JSON syntax and manifest/archive parity.
2. Focused tests for manifest failure handling, daily-state validation,
   forecast registration, link rendering, and portability.
3. `.\tools\validate.ps1`.
4. `.\tools\run.ps1 harness --json --strict`.
5. Read-only cross-repo collector against the repaired commit.
6. Council Steward re-review of the six original findings and every newly
   exposed failure.

Completion requires:

- native validation and strict harness exit `0`;
- no target mutation outside authorized repair files and regenerated derived
  artifacts;
- zero unauthorized source-body, verification-evidence, forecast-resolution,
  or publication changes;
- manifest-backed trace reconstruction restored;
- every original finding classified as corrected, intentionally held, or
  unchanged with reason;
- System Engineer acceptance of the final diff and Steward reconciliation.

## Stop and rollback rules

Stop immediately if:

- manifest parity differs from the known 1,895/1,895 baseline;
- a repair would require inventing source, timing, verification, or claim
  evidence;
- regenerated analytical counts change for a reason other than current
  manifest membership or deterministic code correction;
- a captured archive source body would need alteration;
- new failures cannot be attributed to a named repair unit;
- external or private access becomes necessary.

Rollback by repair unit, never by broad repository reset. Preserve the original
audit receipt and Steward ledger as immutable pre-repair evidence.

## Exact next System Engineer decision

- **A. Authorize units 1–3 only:** restore controlling operability and honest
  daily/forecast state before generated-output cleanup.
- **B. Authorize all six units:** execute the complete bounded remediation
  locally, then return the diff and validation evidence without commit or push.
- **C. Hold execution:** preserve this plan without changing Narrative
  Systems.
