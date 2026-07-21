# World Monitor Signal Pilot Receipt

Status: `testable primitive` candidate; human preservation approval: not requested

## Evidence lineage

- Source: [World Monitor](https://github.com/koala73/worldmonitor)
- Interface: documented REST API, read-only prototype
- Receipt implementation: `cli/anyang_loop/worldmonitor_adapter.py`
- Fixture test: `tests/test_worldmonitor_adapter.py`
- External signal: sanitized infrastructure-event fixture, `fixture-001`
- Evidence status: provisional; fixture demonstrates contract behavior, not world-state truth

## Strategic question

Can a broad situational-awareness signal enter Anyang's learning loop while preserving source lineage, freshness, uncertainty, and human authority without becoming an automatic claim or decision?

## Source observation

The adapter preserves the provider, URL, raw signal ID, retrieval time, freshness, classification, provider summary, confidence, uncertainty, adapter version, and integrity hash. It leaves Anyang inference empty at intake.

## Proposed mechanism

Separate signal receipt from interpretation. Require human analysis to add the strategic question and any inference; prohibit the adapter from creating claims, approvals, work, permissions, customer routing, or doctrine.

## Candidate primitive

**External signal receipt gate:** before using an external monitoring signal, require attributable provenance, retrieval time, freshness status, source classification, uncertainty, integrity hash, explicit human authority, and separate observation/inference fields.

Current level: `testable-primitive`

## Expected benefit

Less context reconstruction, clearer evidence lineage, safer use of model/provider summaries, and lower risk that a dashboard signal is mistaken for decision authority.

## Test result

The fixture suite verifies valid normalization, missing lineage rejection, timestamp validation, authority rejection, duplicate idempotence, stale-signal marking, and provider-summary/inference separation. No network access is required.

## Preservation decision

Remain a candidate pending human review and one real, publicly attributable World Monitor signal processed through the same receipt and analysis flow.

## Remaining uncertainty

The prototype does not establish World Monitor signal accuracy, source independence, operational usefulness, or commercial licensing sufficiency. It also does not test MCP, customer routing, autonomous action, or Learning Core use.

## Boundary

This artifact stays inside Singularity Science. It creates no customer or public authority and must not be promoted to operating doctrine without explicit human approval and evidence from more than one context.
