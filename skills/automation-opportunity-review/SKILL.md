---
name: automation-opportunity-review
description: Review an approved business context and rank bounded, measurable automation opportunities. Use after business-intake has produced an effective context and before creating a value-proof packet or running any pilot.
---

# Automation Opportunity Review

Use this skill only after `business-intake` supplies an approved context reference and version, permitted data sources, operating constraints, and human authority boundaries.

This skill selects opportunities. It does not build, run, schedule, deploy, publish, contact customers, change authority, or persist private business records.

## Required inputs

- Effective business context reference and exact version.
- Permitted sources and data classes.
- Known operating constraints, capacity, and budget boundaries.
- Named human authority for opportunity selection.

If any required input is missing, stale, contradictory, or private-only without an approved external route, return `Hold` and name the deciding human.

## Workflow

1. Confirm the context version and authority boundary; do not reconstruct either from memory.
2. List recurring manual constraints supported by the approved evidence.
3. Create one candidate per constraint, never one candidate per tool.
4. For each candidate, identify the baseline, target metric, value category, recurrence, effort, risk, privacy class, and required approval.
5. Exclude candidates that would make consequential decisions, expose private data, publish, contact customers, change authority, or require unsupported claims.
6. Rank surviving candidates by expected value, recurrence, evidence quality, implementation effort, review burden, and governance risk.
7. Produce the ranked opportunity packet and stop. Do not create a pilot automatically.

## Required output

Return status: `Proposed`, `Hold`, or `Rejected`.

For each candidate include:

- opportunity ID and context version;
- recurring constraint;
- baseline measurement and evidence reference;
- target metric;
- value category: `time`, `error/rework`, or `money`;
- expected recurrence and implementation effort;
- approved inputs and tools;
- privacy/data class;
- human owner and approval boundary;
- failure and exception concerns;
- reason for ranking, holding, or rejecting.

The packet must state:

- time from effective context to first ranked opportunity;
- clarification/rework rounds;
- percentage of candidates with measurable baselines;
- candidates rejected before implementation for evidence, privacy, or authority reasons.

## Handoff

Exactly one `Proposed` opportunity may be handed to `automation-value-proof`. Do not pass multiple opportunities into a proof packet. A proposed opportunity is not approval to run it.

## Boundary

Do not infer ROI, capacity, customer facts, authority, or tool permission. Human judgment decides whether a candidate is worth proving. The next skill must establish the baseline and pilot threshold.

