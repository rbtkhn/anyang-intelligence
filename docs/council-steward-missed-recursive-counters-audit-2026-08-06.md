# Council Steward Missed Recursive Counters Audit - 2026-08-06

**Status:** `advisory audit - no execution authority`

**Owner:** System Engineer

**Reviewer posture:** Council Steward, read-only

**Source boundary:** repository-visible files, validation output, and explicitly
recorded local ledger counts; no private evidence bodies reviewed

## Purpose

This audit identifies places where the repository already defines a recursive
improvement loop but does not yet count the outcome signal needed to improve
the loop. The issue is not missing process. The issue is missing evidence that
the process lowered reconstruction burden, reduced rework, improved decision
quality, or avoided false closure.

This document does not approve new governance policy, change any state label,
authorize new data collection, or convert structural validation into an
operational outcome claim. Any persistent instrumentation, ledger change, or
policy correction requires System Engineer approval.

## Steward finding vocabulary

- `State Support` - the counter exists and supports the improvement claim.
- `Reconciliation Required` - the repo claims or implies improvement before
  the outcome counter exists.
- `Insufficient Evidence` - the repo defines the loop but the outcome cannot
  be assessed from visible evidence.
- `Aging Obligation Notice` - a named baseline, review, or outcome remains
  pending without a current completed measurement.
- `Supersession Proposal` - overlapping metric surfaces should be consolidated
  after approval.

## Missed recursive counters

| Area | Current visible state | Missing counter | Finding | First countable event |
| --- | --- | --- | --- | --- |
| Epistemic state | Structural entropy reports clean, but composite acceptance remains `pending-human-measurement` | Human retrieval success, revision-impact accuracy, and reviewer burden minutes | `Aging Obligation Notice` | One fixed twelve-surface timed reviewer exercise |
| Choice navigation | Choice prompts and outcomes can be recorded, but ordinary selection and outcome are not persisted automatically | Comparable resolved outcomes with usefulness, rework, cognitive load, discovery, and authority incidents | `Insufficient Evidence` | Five explicitly outcome-recorded comparable selections |
| Council pilot | Pilot tracker lists friction and obligation measures while the pilot remains active | Baseline preparation time, recovered commitments, obligation aging, rework prevented, final outcome | `Aging Obligation Notice` | One completed pilot metrics review packet |
| Governance controls | Control review says false-positive and control-cost baselines do not yet exist | True positives, false positives, bypasses, exceptions, operator minutes, retire/narrow decisions | `Insufficient Evidence` | One quarterly control-cost review |
| Pattern Memory | Adoption notes need usefulness, missed patterns, false positives, review burden, and upstream baseline | Accepted suggestions, rejected suggestions, missed patterns later found, review minutes | `Insufficient Evidence` | One pattern-memory adoption review with human usefulness fields |
| Decision Audit | Adoption notes local adaptation and representative outcome evidence are missing | Material uncertainty caught, false positives, decision reversals avoided, audit burden | `Insufficient Evidence` | One decision-audit activation outcome review |
| Automation proof | Automation skills require baseline and proof before ROI claims | Candidates with measurable baseline, pilots passing threshold, review burden, `Too thin` rejects | `State Support` for rule; `Insufficient Evidence` for current portfolio outcomes | One automation candidate register with baseline completeness |
| Analytical interfaces | Interface guidance names reader-outcome measures but warns baselines do not yet exist | Retrieval success, delayed recall, title-predictability, editorial overrides, drafting time | `Aging Obligation Notice` | One timed reader-outcome test |

## Priority order

1. **Epistemic human outcome baseline.** This is the most direct recursive
   improvement opportunity because the CLI already exposes the acceptance gap.
   Without it, the repo can say the structure is complete but cannot say the
   structure made human review easier.
2. **Governance control cost and false positives.** Controls should be kept,
   narrowed, made advisory, or retired based on observed protection versus
   burden. Counting only pass rates can reward ceremony.
3. **Choice outcome quality.** The footer and choice system should learn from
   explicitly approved outcomes, not from selection frequency.
4. **Council pilot friction.** The Council operating model should prove lower
   reconstruction and fewer stale obligations before expansion.
5. **Pattern and decision skill usefulness.** Skill adoption should count
   human usefulness and false positives before claiming improved judgment.

## First twelve-surface epistemic measurement exercise

Use the twelve fixed surfaces listed in `epistemic-state.yaml`. The reviewer
must not inspect private evidence bodies. The exercise measures whether a
human can reconstruct claim state and revision consequences from the repository
surface itself.

### Inputs

- The current `epistemic-state.yaml` surface list.
- The controlling file for each surface.
- Any repo-visible linked source, authority receipt, transition note, or
  dependency named by that surface.
- A timer and one reviewer who was not the author of the most recent edits, if
  available.

### Per-surface task

For each surface, the reviewer records:

| Field | Countable value |
| --- | --- |
| Surface id | Exact id from `epistemic-state.yaml` |
| Controlling artifact found | `Yes / No` |
| Current state found | `Yes / No` |
| Authority or approval boundary found | `Yes / No / Not applicable` |
| Evidence or source basis found | `Yes / No / Not applicable` |
| Dependency or downstream impact found | `Yes / No / Not applicable` |
| Revision trigger found | `Yes / No / Not applicable` |
| Time to reconstruct | Minutes |
| Reviewer confidence | `1-5` |
| Revision-impact answer correct | `Yes / No / Unclear` |
| Notes | Short, repo-visible references only |

### Aggregate metrics

- `retrieval_success`: share of applicable fields found without private
  reconstruction.
- `revision_impact_accuracy`: share of surfaces where the reviewer correctly
  identifies what would need review if the surface changed.
- `human_burden`: `100 - (60 x retrieval_success + 40 x revision_impact_accuracy)`.
- `median_reconstruction_minutes`: median minutes per surface.
- `false_positive_burden`: count of fields initially marked missing that were
  later found to be sufficient and material.
- `immaterial_overhead`: count of checks completed where the answer did not
  affect review, decision, or state reconstruction.

### Acceptance boundary

The exercise may support a composite epistemic measurement only after the
aggregate values are recorded through the existing CLI path described in
`cli/README.md`. A completed structural validator, clean manifest, or reviewer
confidence score alone does not prove recursive improvement.

## Proposed first implementation shape

Use the existing `project epistemic-report` command with measured values:

```powershell
.\tools\run.ps1 project epistemic-report `
  --retrieval-success <0.00-1.00> `
  --revision-impact-accuracy <0.00-1.00>
```

Record the raw review table as a dated advisory packet only after System
Engineer approval. The packet should contain repo-visible references and
aggregate measures, not private evidence bodies.

## Done when

This audit is useful when the operator can see which improvement loops are
currently structural-only, which outcome counters would make them recursive,
and which first measurement should be run without expanding authority or
creating a new governance system.
