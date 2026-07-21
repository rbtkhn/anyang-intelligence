---
name: world-monitor
description: Governed review of World Monitor REST signals for Singularity Science. Use when Codex needs to capture, normalize, assess, compare, or route a World Monitor signal while preserving provenance, freshness, uncertainty, human authority, and the boundary between observation and inference.
---

# World Monitor

Use this skill to turn a World Monitor signal into a reviewable source receipt. The skill is a read-only intelligence-signal workflow, not an autonomous alerting, decision, or action system.

## Core flow

`World Monitor signal -> normalized receipt -> human analysis -> strategic question -> bounded test -> observed outcome`

The first receiving surface is `projects/singularity-science/`. Do not route to customer lanes, Learning Core, public outputs, or operating doctrine automatically.

## Hard boundaries

- Use the documented REST API first. Defer MCP until the REST receipt passes provenance, freshness, authority, and security review.
- Create only a normalized external signal receipt. Do not create claims, approvals, work items, permissions, customer obligations, public authority, or doctrine.
- Treat World Monitor as an external signal-production layer, not a source of truth.
- Preserve provider attribution, source URL, raw signal ID, retrieval time, publication time when available, freshness, classification, confidence, uncertainty, adapter version, and integrity hash.
- Keep provider summaries separate from Anyang interpretation. Intake begins with an empty Anyang inference field.
- Stale, thin, conflicting, or uncorroborated signals remain visible as provisional; never upgrade them through language alone.
- Respect World Monitor's AGPL-3.0-only license and do not copy its source code into Anyang artifacts.

## Modes

Choose the narrowest mode that satisfies the request:

### Capture

Normalize one signal with `cli/anyang_loop/worldmonitor_adapter.py`. Record the receipt and stop. This mode requires no strategic interpretation.

### Review

Use the receipt to separate source observation, provider inference, Anyang inference, and uncertainty. Produce a bounded review packet with source lineage, strategic question, possible relevance, authority required, evidence still needed, and non-generalization boundary.

### Compare

Compare the signal against existing Singularity Science sources. Identify recurrence, contradiction, novelty, and source dependence. Do not call a pattern durable unless the evidence lineage and independence are explicit.

### Route

Propose a receiving lane or research task, but do not create it automatically. State why the lane is appropriate, what stays inside Singularity Science, what human approval is required, and what customer or public authority is explicitly not created.

Use `cli/anyang_loop/worldmonitor_promotion_gate.py` when deciding whether a receipt should remain a receipt, be held, be rejected as noise, or become eligible for human-reviewed Singularity Science source-note promotion. A promote disposition requires `archive_approval_status=approved` and a non-empty `archive_approval_receipt_ref`; the gate never writes an archive artifact.

### Closeout

After a human-approved bounded test, record whether the signal was useful, redundant, misleading, unresolved, or strategically important. Preserve a learning event only at the approved level. Never promote directly from source observation to doctrine.

## Required receipt fields

Use the `ExternalSignalReceipt` contract in `cli/anyang_loop/worldmonitor_adapter.py`. A complete receipt requires provider and source URL, raw signal identifier, retrieval timestamp, publication timestamp when available, freshness, source classification, provider summary, empty Anyang inference at intake, confidence, uncertainty, adapter version, integrity hash, explicit `no_authority_created` status, and receiving lane.

Read [references/review-packet.md](references/review-packet.md) when producing analysis or routing output.

## Completion contract

Report the receipt path or identifier, source and freshness status, observation versus inference distinction, strategic question if used, human authority required, proposed disposition, unresolved uncertainty, and what remained inside Singularity Science.

End with no implied operational action unless the operator separately authorizes it and a human authority approves it.
