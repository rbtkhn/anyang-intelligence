# External Skill Adoption Preserves Capability Lineage

- **Status:** Provisional advisory contract
- **Owner:** Repository operator
- **Review trigger:** After three completed receipts or one material adoption failure

## Lead Judgment

An externally sourced or materially derived skill should enter the repository
with a compact adoption receipt that identifies its purpose, origin, capability
surface, local modifications, evidence, decision owner, and rollback path. The
receipt records a human decision; it does not grant the skill execution or
external-action authority.

Use [the skill-adoption receipt template](../templates/skill-adoption-receipt.md).
Keep the receipt beside the adopted skill as `skills/<skill-name>/ADOPTION.md`
so it remains available for review without expanding routine skill context.

## Scope

Use this contract when a skill is:

- copied or installed from an external repository, marketplace, plugin, or
  other distribution source;
- forked from an external skill;
- generated from substantial third-party instructions or operating logic; or
- materially derived from an identifiable external skill or method.

Do not require a receipt merely because an AI tool helped draft a native local
skill. Native skills remain governed by their normal review and tests unless
they inherit material external instructions, mechanisms, rights, or authority
assumptions.

## Separation Of Concerns

```text
SKILL.md
  = discovery metadata and operating contract

ADOPTION.md
  = provenance, capability-transfer, modification, and adoption evidence

review-ai-harness
  = portfolio interaction review

repository operator
  = adoption and authority decision
```

Do not move the full receipt into `SKILL.md` frontmatter. Discovery metadata
should remain concise, and adoption evidence should load only for adoption,
modification, or audit work.

## Minimum Review

Before an adoption decision, the reviewer should establish:

1. **Purpose:** the bounded job and why an existing capability is insufficient.
2. **Origin:** the author or organization, source location, immutable version or
   commit when available, and license or rights status.
3. **Capability:** activation mode; tools, scripts, network, files, and data the
   skill may reach; permitted effects; and prohibited effects.
4. **Lineage:** the inherited mechanism, local modifications, rationale, and
   reviewed local baseline.
5. **Evidence:** inspected files, representative tests, portfolio interaction
   review, known gaps, reviewer, and rollback method.

Use `Missing`, `Unknown`, or `Not tested` instead of smoothing over absent
evidence. Missing source identity, unresolved rights, opaque executable
behavior, unbounded permissions, or no credible rollback produces `Hold`.

## Decision States

| State | Meaning | Authority effect |
| --- | --- | --- |
| `Proposed` | Review is incomplete. | None. |
| `Probation` | Provenance and boundaries are reviewable, but bounded behavioral or portfolio evidence remains incomplete. | Only the exact operator-approved evaluation scope. |
| `Adopted` | The operator accepts the reviewed skill into the repository for its stated purpose and boundaries. | Repository inclusion only; no external-action authority. |
| `Hold` | Material evidence, rights, capability, or rollback information is missing or unsafe. | None. |
| `Rejected` | The reviewed candidate will not be adopted. | None. |
| `Retired` | A formerly adopted skill is no longer active; its lineage remains available. | None. |

Adoption never implies publication, deployment, spending, customer contact,
private-data access, installation in another environment, or permission to run
scripts or tools. Those actions remain governed by the active environment,
repository contracts, and explicit operator authority.

## Change And Review Rules

Create or revise the receipt when any of these materially changes:

- upstream version or source identity;
- activation mode or trigger scope;
- tools, scripts, network, data, permissions, or write surface;
- inherited mechanism or local operating logic;
- license or rights status;
- representative test result or portfolio-conflict finding; or
- rollback method.

Preserve the prior decision in Git history. Do not represent a content hash,
test result, harness review, or source inspection as current after the reviewed
baseline changes.

## Relationship To Existing Controls

- Use the repository's evidence-awareness classifications for material claims.
- Use `$review-ai-harness` for read-only portfolio mapping and interaction
  proposals; an adoption receipt does not replace that review.
- Keep canonical skill instructions, adapters, and compatibility aliases in
  their existing one-home architecture.
- Add this receipt to `artifact-state.yaml` only if repeated use demonstrates
  that it has become a consequential durable artifact class.

### Harness visibility pilot

The AI harness scanner inventories tracked `skills/*/ADOPTION.md` files as
`skill-adoption-receipt` controls. It reserves at most three slots inside the
existing 50-file semantic ceiling for the provisional receipt cohort, then
fills the remaining slots through the existing priority order. The scan scope
reports which otherwise-selected controls the reservation displaced and how
many receipts exceeded the pilot reservation.

Untracked receipts remain excluded. Semantic selection makes a receipt
reviewable; it does not validate its claims, approve its status, grant the
associated skill authority, or authorize a source change.

## Provisional Control Boundary

This contract does not add a blocking validator. First collect three real
receipts or observe one material adoption failure. Then review omissions,
false confidence, operator burden, and whether any failure is consequential,
recurring, and objectively detectable. Only that evidence can justify a schema
or blocking check.
