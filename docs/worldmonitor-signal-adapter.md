# World Monitor Signal Adapter

This document defines the bounded Anyang Intelligence integration with [World Monitor](https://github.com/koala73/worldmonitor).

## Boundary

World Monitor is an external signal-production layer. It is not a source of truth, decision authority, customer authority, or Anyang doctrine. The adapter is read-only and creates only a normalized source receipt.

The initial surface is the documented World Monitor REST API. MCP is deferred until the REST receipt passes provenance, freshness, authority, and security review.

## Receipt contract

`ExternalSignalReceipt` preserves:

- provider and source URL;
- raw signal identifier;
- retrieval and publication timestamps;
- freshness state;
- source classification (`observation`, `inference`, or `unknown`);
- provider summary;
- empty Anyang inference at intake;
- confidence and uncertainty;
- adapter version and integrity hash;
- lane and explicit `no_authority_created` status.

The receipt is compatible with the repository's source/evidence/claim/outcome/learning-loop concepts, but it does not insert database claims, approvals, work items, permissions, or doctrine.

## Governed flow

`World Monitor signal → normalized receipt → human analysis → strategic question → testable primitive`

The first proving surface is Singularity Science. Any durable primitive, cross-lane transfer, customer use, publication, or permission change requires explicit human approval.

## Licensing and provenance

The adapter consumes World Monitor through its documented external interface and does not copy World Monitor source code. Operators must review the World Monitor AGPL-3.0-only terms and any applicable commercial licensing before deploying a combined or proprietary service.
