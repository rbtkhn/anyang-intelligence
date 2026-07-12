# Governance Earns Its Place by Preventing More Risk than It Creates

Title rationale: The title states the repository's control budget: executable governance remains justified only while its demonstrated protection exceeds interruption, maintenance, and judgment costs.

## Lead Judgment

Anyang Intelligence should consolidate, measure, narrow, and retire controls before adding new validator families. Blocking automation belongs at consequential, recurring, objectively detectable boundaries; subjective quality and reversible low-risk work remain human-review concerns.

## Controlling Object

Whether each executable control still prevents a meaningful failure more reliably than it creates false positives, delay, maintenance work, formulaic compliance, or shadow workflows.

## Quarterly Control Review

The repository operator reviews curated manifests and blocking CI checks quarterly. For each control, record:

- the concrete failure it prevents and whether that failure occurred;
- pass, failure, false-positive, bypass, and exception counts when available;
- operator or reviewer time imposed;
- legitimate work blocked or pushed into a shadow workflow;
- whether enforcement should remain blocking, become advisory, narrow, or retire;
- the accountable owner and next review date.

Do not create a new metrics subsystem merely to satisfy this review. Use CI results, issue history, review receipts, and a short decision note until repeated use justifies structured instrumentation.

## Bounded Exceptions

Exceptions must be narrow, reviewable, and temporary. Record the control, scope, concrete reason, approving authority, expiration date, and condition that will trigger review. Prefer a bounded exception over globally weakening a valid rule. Expired exceptions fail validation.

## Expansion and Retirement Tests

Add a blocking control only when the failure is consequential, plausible or observed, recurrent, and objectively detectable. Keep a control blocking only while detection remains reliable and the expected protection exceeds false-positive, interruption, exception, and maintenance costs.

Retire or narrow a control when it never finds the intended failure, is routinely bypassed, generates formulaic artifacts, duplicates a stronger control, blocks legitimate work disproportionately, or no longer has an accountable owner.

## Recovery Evidence

Recovery declarations are promises until exercised. Use synthetic data to test SQLite-safe backup, integrity, schema version, and restoration behavior. Do not access tenant-private data merely to prove that the recovery control exists.

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Provisional—control-cost and false-positive baselines do not yet exist | Hold the current validator set stable and avoid treating pass counts as quality gains | One quarterly review containing CI outcomes, exceptions, false positives, operator time, and explicit keep, narrow, advisory, or retire decisions |
