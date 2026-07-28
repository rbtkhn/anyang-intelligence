# Knowledge-Custodian Review Gate

This primitive governs agents that maintain durable knowledge: catalogs, archives, semantic indexes, memory stores, retrieval plans, or context supplied to another model.

Its purpose is to prevent autonomous curation from becoming silent authority over what an owner can find, remember, or infer.

## Operating Rule

Default state: `watch` until ownership, provenance, write scope, correction, rollback, and succession are explicit.

## Core Questions

1. Who owns the collection and the curated state?
2. What sources may the custodian read, write, rank, merge, suppress, or delete?
3. Can every material change be traced to a source, rule, model, operator, and timestamp?
4. How are conflicting records preserved and escalated rather than silently resolved?
5. Can a human inspect, correct, roll back, export, replace, or shut down the custodian?
6. What survives provider, hardware, operator, jurisdiction, or model changes?

## Review Dimensions

| Dimension | Required check | Warning sign |
| --- | --- | --- |
| Ownership | Named owner and authority over data, indexes, memory, and outputs | Vendor or agent implicitly owns the effective archive |
| Provenance | Source lineage and transformation history remain visible | Summaries replace source identity |
| Write scope | Agent permissions are narrow, explicit, and reversible | Agent can rewrite canonical records without review |
| Conflict handling | Disagreement is preserved and escalated | One ranking silently becomes truth |
| Change receipt | Additions, deletions, merges, and re-rankings are logged | The archive changes without an audit trail |
| Correction and rollback | Human correction and version restoration are tested | “Undo” exists only as a support request |
| Succession | Collection remains usable if the agent, provider, or host fails | Memory is trapped in one runtime or account |
| Boundary | Customer, child, donor, private, and public data remain separated | One memory layer crosses membranes by convenience |

## Output Shape

```text
Collection:
Owner:
Sources admitted:
Agent read scope:
Agent write scope:
Provenance receipt:
Conflict policy:
Human correction path:
Rollback and export path:
Succession or shutdown plan:
Membrane classification:
Default state:
What stays inside Singularity Science:
```

## Boundary

Do not treat physical remoteness, encryption, or a “sovereign” label as proof of legal sovereignty, security, or accountability. The gate governs curation and authority; it does not validate a vendor, launch, jurisdiction, or mission claim.
