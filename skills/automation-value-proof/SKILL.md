---
name: automation-value-proof
description: Define and audit measurable value, evidence, ROI, approvals, and stop conditions for exactly one approved automation opportunity before a bounded pilot.
---

# Automation Value Proof

Use this skill after `automation-opportunity-review` has produced exactly one proposed opportunity and `business-intake` has supplied the effective authority and data boundaries.

This skill defines evidence. It does not run the workflow, authorize deployment, publish, contact customers, change policy, or persist private records.

Use `templates/automation-value-proof.md` as the canonical packet and `anyang-project validate-value-proof` for objective validation.

## Required inputs

- Exactly one opportunity ID and exact business-context version.
- Named recurring constraint and baseline measurement.
- Target metric and measurement method.
- Approved tools, inputs, paths, privacy class, owner, and reviewer.
- Explicit approval boundary and prohibited actions.

Return `Hold` if the opportunity is ambiguous, the baseline cannot be reconstructed, the data route is unapproved, or authority is missing.

## Evidence contract

The packet must contain:

- representative test cases;
- exception behavior;
- quality/revision checks;
- minimum pilot threshold;
- before/after evidence fields;
- human review burden;
- maintenance estimate;
- unresolved uncertainty;
- completion-receipt contract;
- explicit statement of what the workflow must not decide.

Separate planning assumptions from measured facts. Use:

```text
Net performance value =
verified hours saved
+ avoided rework/error cost
- human review burden
- maintenance cost
```

Do not convert a planned hourly value, market claim, or single demo into realized ROI.

## Gate rules

- A quantitative claim requires a baseline and before/after evidence.
- One successful demo does not establish repeatability.
- The pilot must define representative runs and exception handling before execution.
- Human review remains mandatory at consequential boundaries.
- A faster result with lower quality fails the proof.
- If the threshold is not met, return `Too thin`, not a positive ROI claim.

## Handoff

Only a human-approved packet with status `Approved for pilot` may be passed to `bounded-workflow-pilot`. Proof approval authorizes the named pilot scope only; it does not authorize deployment or external action.

## Boundary

Validator success checks structure and objective safety conditions. It does not decide whether the automation is valuable, creative, editorially correct, or ready for deployment.

