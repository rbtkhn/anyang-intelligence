# Learn From Choices Continuity Contract v0.3

Status: `active bounded policy`

This version preserves schema-v8 choice storage and all v0.2 projections while
adding outcome-triggered retention for Active v1. V0.2 classifications remain
valid and byte-compatible; new active packets use
`LFC-CONTINUITY-v0.3`.

## Retained Episode

A retained episode contains the immutable option set, selected branch,
comparison context, same-task provenance, reviewed packet hash, outcome,
policy-specific measurements, and evidence reference. The prompt, selection,
and outcome are written in one transaction and verified before commit.

Ordinary selections remain ephemeral. Historical reconstruction without a
visible same-task menu may become an operator-approved `RL-*` learning but is
ineligible for choice cohorts.

## Comparison Context

Active policies require exact `decision_seam`, `work_class`, and `risk_class`
values. They are stored in the immutable selection event and covered by its
event hash. Missing context, policy mismatch, unverified lineage, missing
measurements, missing evidence, or scope mismatch excludes the episode.

## Active Policy Rules

Only `repository-governance-preflight-v1` is active. The existing
`repository-authorized-push-v1` remains diagnostic-only. Active evidence uses
a 90-day window, a three-resolved floor, and two consistent outcomes with no
material contradiction. Selection frequency, displayed letters, semantic
roles, and unretained navigation never create cohorts.

Active guidance retains `authority_effect: none`, preserves an overlooked
path, yields to current controlling evidence, and becomes neutral on a
guidance conflict. Authority, privacy, safety, and membrane incidents remain
immediate guardrails regardless of sample size.

## Append-Only Compatibility

Original option packets, selections, outcomes, and corrections are never
rewritten. A held, revised, or retired policy changes projection behavior, not
historical receipts. No database migration is introduced by this contract.
