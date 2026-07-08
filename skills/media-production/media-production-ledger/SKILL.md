---
name: media-production-ledger
preferred_activation: media-production ledger
description: Prepare or append Creative Abundance Ledger entries for Media Production work after assets are approved, shipped, reused, or reviewed, while preserving evidence, source/rights notes, and human authority boundaries.
category: media-production
status: active
scope_class: customer-work
---

# Media Production Ledger Skill

Use this skill when the operator asks for:

- `media-production ledger`
- `creative abundance ledger`
- `ledger entry`
- `record what shipped`
- `record what was learned`
- `log creative abundance`
- `update the media production ledger`
- a Creative Production Operator shipped-work or reuse record

This skill turns shipped, reused, reviewed, or approved Media Production work into evidence-backed creative memory. It can prepare a ledger-ready entry by default. It only appends to `customers/media-production/creative-abundance-ledger-template.md` when the operator explicitly asks to update the file and the shipped/reused evidence is clear.

It does **not** publish, deliver, approve claims, approve spend, mark work shipped without evidence, assign contractor work, or make final performance conclusions by itself.

## Required Reads

Read these first:

1. `customers/media-production/creative-abundance-ledger-template.md`
2. `customers/media-production/executive-os-install.md`
3. `customers/media-production/creative-production-operator-onboarding.md`
4. `customers/media-production/creative-abundance-quality-gate.md`
5. `customers/media-production/README.md`

When available, also read:

- The production brief from `skills/media-production/media-production-brief/SKILL.md`.
- The quality gate review from `skills/media-production/media-production-quality-gate/SKILL.md`.
- The package output from `skills/media-production/media-production-package/SKILL.md`.
- Shipped links, screenshots, exported files, customer-support notes, owner/editor approval, audience signals, or reuse notes.
- For Grace Gems: owner-approved product/listing/customer-support facts and any claim approvals.
- For Predictive History: episode/topic source notes, publication notes, audience signals, and rights/source notes.

If evidence is missing, produce a **ledger hold** rather than treating the work as shipped or valuable.

## Ledger Readiness

Classify the entry before writing:

| Status | Use when | Ledger action |
| --- | --- | --- |
| **Draft record** | Work exists but is not approved, shipped, or reused. | Prepare an internal note only; do not append as shipped value. |
| **Approved pending shipment** | Human approval exists, but delivery/publication/reuse has not happened. | Prepare a pending entry with outcome `pending`; do not claim results. |
| **Shipped** | A human-approved asset was delivered or published and evidence exists. | Prepare or append a shipped entry. |
| **Reused** | A shipped or approved asset was repurposed across another channel/use. | Prepare or append a reuse entry, preserving original source signal. |
| **Learning update** | Outcome, signal, or blocker changed future production judgment. | Prepare a learning entry or next-action note. |
| **Hold** | Source, approval, rights, claim, or shipped evidence is unclear. | Do not append; list missing evidence. |

Do not use `shipped` because a package exists. Use `shipped` only when delivery/publication has happened and evidence is present.

## Lane Guardrails

### Grace Gems

For Grace Gems ledger entries:

- Do **not** record invented product details, prices, dimensions, materials, gemstone identity, authenticity claims, shipping promises, return/repair promises, rush-order commitments, certificate/appraisal language, customer commitments, or policy language.
- Record customer-support signals as generic patterns unless explicit approval allows more detail.
- Mark owner approval as required for product, listing, policy, pricing, authenticity, shipping, promotion, or customer-promise claims.
- If an asset supports Grace Gems through Media Production, list client as `Grace Gems` and keep Media Production capacity/budget notes out of customer-facing claims.

### Predictive History

For Predictive History ledger entries:

- Record what judgment, evidence, prediction/outcome, causal understanding, or lesson the asset supported.
- Do not count decorative history imagery as abundance unless the operator explicitly approved that purpose.
- Keep source/rights uncertainty visible for quotes, images, maps, likenesses, music, archival material, and generated visual references.
- Treat audience response as evidence only when a concrete signal is supplied; otherwise use `audience signal pending`.

## Evidence Standard

A ledger entry should name at least one evidence anchor:

- Published link.
- Delivered file path.
- Package folder path.
- Owner/editor approval.
- Customer support pattern.
- Listing/product reference.
- Screenshot.
- Exported asset.
- Performance metric.
- Reuse note.
- Review note.
- Human-provided shipped confirmation.

If no evidence anchor exists, mark the entry **Hold for evidence**.

## Output Format

Produce this exact structure:

```text
Creative abundance ledger entry:
Lane:
Ledger status:
Client:
Date:
Evidence anchor:

Insight / source signal:
- ...

Assets created:
- ...

Reused where:
- ...

Outcome / signal:
- ...

Next action:
- ...

Source / rights / approval notes:
- ...

Ledger row:
| Date | Client | Insight / source signal | Assets created | Reused where | Outcome / signal | Next action |
| ... |

Missing evidence:
- <only include when needed>

Human authority boundary:
- ...
```

Use `pending` honestly when outcome, audience response, customer response, reuse, or performance is not known.

## Append Rules

Append to `customers/media-production/creative-abundance-ledger-template.md` only when all are true:

- The operator explicitly asks to update or append the ledger.
- The entry is **Shipped**, **Reused**, **Approved pending shipment**, or **Learning update**, not **Draft record** or **Hold**.
- The evidence anchor is present.
- Source, rights, claim, approval, and customer privacy notes are safe enough to preserve.
- The ledger row does not expose private customer facts, customer messages, contractor data, unapproved product claims, or rights-sensitive details.

When appending:

- Add one row to the ledger table.
- Preserve the existing table shape.
- Keep wording concise and generic enough for durable memory.
- Do not rewrite prior ledger entries unless explicitly requested.
- If the entry needs a longer note, add a short `Next action` pointing to the package or review notes instead of stuffing private details into the table.

## Decision Rules

- If shipped/delivered/published status is uncertain, choose **Hold** or **Approved pending shipment**, not **Shipped**.
- If results are unknown, use `signal pending` rather than inventing value.
- If reuse has not happened, write `Not reused yet` or `Reuse pending`.
- If Grace Gems owner approval is missing for an external claim, do not append a row that implies the claim is approved.
- If Predictive History source/rights evidence is missing, do not append a row that implies the asset is cleared.
- If an entry would cross a membrane, translate it into a generic production primitive or keep it local.

## Done When

The operator has:

- A ledger-ready row or a clear ledger hold.
- Evidence anchors for shipped, reused, approved, or learned status.
- Honest `pending` language where outcomes are not known.
- Source, rights, claims, privacy, budget, capacity, and human-approval issues named.
- No accidental publication, delivery, shipped status, spend approval, contractor assignment, or performance claim.
