# Epistemic Twelve-Surface Human Reviewer Worksheet - 2026-08-06

**Status:** `worksheet - no measurement recorded yet`

**Owner:** System Engineer

**Purpose:** Record the first independent human outcome measurement for the
twelve surfaces listed in `epistemic-state.yaml`.

This worksheet does not change `epistemic-state.yaml`, satisfy composite
acceptance, approve any repository state, or authorize private evidence access.
It is a review packet for measuring whether repository-visible surfaces reduce
human reconstruction burden.

## Reviewer instructions

Use only repository-visible files and opaque approved references. Do not inspect
private evidence bodies. Start a timer before opening each surface. Stop the
timer when you can state the controlling artifact, current state, authority
boundary, evidence basis, dependency, and revision consequence.

If a field is unclear, write `No` or `Unclear`; do not infer from memory,
conversation continuity, or confidence.

## Surface worksheet

| Surface id | Controlling artifact found | Current state found | Authority boundary found | Evidence or source basis found | Dependency found | Revision trigger found | Minutes | Confidence 1-5 | Revision-impact answer correct | Notes |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| `singularity-watch-contract` |  |  |  |  |  |  |  |  |  |  |
| `singularity-q2-watch` |  |  |  |  |  |  |  |  |  |  |
| `singularity-q3-watch` |  |  |  |  |  |  |  |  |  |  |
| `embodied-adoption-gate` |  |  |  |  |  |  |  |  |  |  |
| `learner-intake` |  |  |  |  |  |  |  |  |  |  |
| `learner-profile-template` |  |  |  |  |  |  |  |  |  |  |
| `grace-trust-claim-review` |  |  |  |  |  |  |  |  |  |  |
| `grace-marketplace-gate` |  |  |  |  |  |  |  |  |  |  |
| `media-quality-gate` |  |  |  |  |  |  |  |  |  |  |
| `media-package` |  |  |  |  |  |  |  |  |  |  |
| `mountain-seasonal-readiness` |  |  |  |  |  |  |  |  |  |  |
| `operating-portfolio-dashboard` |  |  |  |  |  |  |  |  |  |  |

## Scoring

- `retrieval_success`: applicable `Yes` fields divided by applicable fields
  across controlling artifact, state, authority boundary, evidence basis,
  dependency, and revision trigger.
- `revision_impact_accuracy`: surfaces with a correct revision-impact answer
  divided by twelve.
- `human_burden`: `100 - (60 x retrieval_success + 40 x revision_impact_accuracy)`.
- `median_reconstruction_minutes`: median of the twelve minute values.
- `false_positive_burden`: fields first marked missing that were later found
  sufficient and material.
- `immaterial_overhead`: checks completed where the answer did not affect
  review, decision, or state reconstruction.

## Aggregate result

| Metric | Value | Notes |
| --- | ---: | --- |
| `retrieval_success` |  |  |
| `revision_impact_accuracy` |  |  |
| `human_burden` |  |  |
| `median_reconstruction_minutes` |  |  |
| `false_positive_burden` |  |  |
| `immaterial_overhead` |  |  |

## Recording boundary

Only after the worksheet is complete should measured values be passed to:

```powershell
.\tools\run.ps1 project epistemic-report `
  --retrieval-success <0.00-1.00> `
  --revision-impact-accuracy <0.00-1.00>
```

Do not record dry-run values, agent-only confidence, structural validator
success, or selection frequency as human outcome measurement.
