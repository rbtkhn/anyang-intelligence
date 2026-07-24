# Singularity Intake Performance Audit

## Purpose

Evaluate whether the `Decision Compression` feature improves source-to-decision speed and reduces downstream rework without adding excessive intake burden.

## When to run

Run after the next 10 completed Singularity intake packets, then repeat every 20 packets or quarterly, whichever comes first.

## Record for each intake

```text
source_id:
intake_authoring_minutes:
time_to_first_disposition_minutes:
second_operator_understanding_minutes:
transcript_reread_required: yes|no
routing_rework_minutes:
final_disposition:
```

## Compare against

Use the previous three comparable intake packets as the initial baseline. If timing data is absent, mark the comparison as unavailable rather than reconstructing it from memory.

## Keep the feature if

- decision-retrieval time decreases by at least 15%;
- downstream routing rework decreases by at least 10%; and
- intake authoring burden increases by less than 10%.

## Audit outputs

- observed baseline and post-feature medians;
- authoring burden change;
- decision-retrieval change;
- rework change;
- false-promotion or unnecessary-verification cases;
- operator judgment on whether the five-field section remains useful.

## Boundary

This audit measures operating usefulness, not customer ROI, source truth, rights clearance, primitive validity, or permission to route source material outward.
