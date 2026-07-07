---
name: media-production-package
preferred_activation: media-production package
description: Package approved or review-ready Media Production assets for Grace Gems or Predictive History with clear files, source notes, reuse paths, and human approval boundaries before delivery or publication.
category: media-production
status: active
scope_class: customer-work
---

# Media Production Package Skill

Use this skill when the operator asks for:

- `media-production package`
- `package asset`
- `package approved asset`
- `delivery package`
- `review package`
- `asset package`
- `package and repurpose`
- a Creative Production Operator package for review, delivery, publishing prep, or archive handoff

This skill turns an approved or review-ready asset into an organized package that another human can review, deliver, publish, reuse, or archive. It does **not** publish, deliver to a client, mark work as shipped, append to the creative abundance ledger, approve spending, assign contractor work, or make final rights/claims decisions by itself.

## Required Reads

Read these first:

1. `customers/media-production/README.md`
2. `customers/media-production/executive-os-install.md`
3. `customers/media-production/creative-production-operator-onboarding.md`
4. `customers/media-production/creative-abundance-quality-gate.md`
5. `customers/media-production/creative-abundance-ledger-template.md`

When available, also read:

- The production brief from `skills/media-production/media-production-brief/SKILL.md`.
- The quality gate review from `skills/media-production/media-production-quality-gate/SKILL.md`.
- The asset files, draft text, captions, exports, source notes, rights notes, or operator-provided package contents.
- For Grace Gems: relevant product/listing/customer-support source and owner-approved facts.
- For Predictive History: relevant topic, transcript, outline, source note, or prediction/outcome frame.

If the brief, asset, quality gate review, source notes, or rights notes are missing, create a **Package hold** with missing items instead of presenting the package as delivery-ready.

## Package Readiness Rule

Before packaging, identify the current quality gate decision:

| Gate status | Package action |
| --- | --- |
| **Approve** | Create an approved package for the next human-authorized step. |
| **Review-ready / no final gate yet** | Create a review package and mark quality gate approval still needed. |
| **Revise** | Create a revision package only if it helps focus edits; do not present as approved. |
| **Hold** | Create a hold package listing blockers; do not prepare delivery/publication assets. |
| **Reject** | Do not package for delivery; summarize rejection and archive only if requested. |

Approval from the quality gate means readiness for the next human-approved step, not autonomous delivery or publication.

## Lane Guardrails

### Grace Gems

For Grace Gems packages:

- Do **not** invent product details, prices, dimensions, materials, gemstone identity, authenticity claims, shipping promises, return/repair promises, rush-order commitments, certificate/appraisal language, customer commitments, or policy language.
- Include source notes for product, listing, customer-support, pricing, policy, authenticity, shipping, and promise-related claims.
- Mark any claim not already owner-approved as **owner approval required**.
- Convert buyer-message or support-derived material into generic customer-confusion patterns unless explicit reuse is approved.
- Keep final delivery, publication, listing edits, customer replies, and owner commitments under human authority.

### Predictive History

For Predictive History packages:

- Package assets around judgment, evidence, prediction/expectation, outcome, causal forces, decision problem, or lesson learned.
- Do not package decorative history wallpaper as a finished asset unless the operator explicitly approves that job.
- Include source/rights notes for historical claims, quotes, maps, images, likenesses, music, archival material, and generated visual references.
- Flag sensational visuals, misleading simplifications, or unsupported historical claims before review.
- Keep final publication, captions, episode positioning, rights decisions, and editorial claims under human authority.

## Default Folder Structure

Use or recommend this structure unless the operator provides a different destination:

```text
<lane-slug>/<topic-or-product-slug>/
  README.md
  brief/
  source-notes/
  assets/
    source/
    working/
  exports/
  review/
  reuse/
```

Folder meanings:

- `README.md`: package overview, status, reviewer decision needed, and human approval boundary.
- `brief/`: production brief and any strategy notes.
- `source-notes/`: facts, rights notes, claim notes, citations, product references, or customer-pattern notes.
- `assets/source/`: original inputs, references, prompts, raw captures, or editable source material.
- `assets/working/`: editable drafts and intermediate files.
- `exports/`: review-ready PNG, JPG, MP4, PDF, Markdown, captions, descriptions, or upload-prep files.
- `review/`: quality gate review, decision notes, requested changes, and approval record.
- `reuse/`: repurposing notes, derivatives, captions, alternate crops, short-form ideas, or archive notes.

## File Naming

Prefer clear, boring names that make review and reuse easy:

```text
<lane>-<topic-or-product>-<asset-type>-<status>-YYYY-MM-DD.<ext>
```

Use these status labels:

- `draft`: early work for feedback.
- `review`: ready for quality or owner/editor review.
- `approved`: approved for the next human-authorized step.
- `revision-needed`: blocked until specific edits are made.
- `hold`: blocked by source, rights, claim, capacity, budget, or authority issue.
- `shipped`: use only when a human confirms publication or delivery already happened.

Do not mark assets `shipped` only because they are packaged.

## Package Output

Produce this exact structure:

```text
Media production package:
Lane:
Package status:
Asset set:
Source signal / brief:
Quality gate decision checked:
Destination / reviewer:

Folder structure:
- ...

Files to include:
- ...

Source / rights notes:
- ...

Captions / descriptions / support text:
- ...

Reuse / repurposing paths:
- ...

Ledger-ready summary:
- Source signal:
- Assets created:
- Reused where:
- Outcome / signal:
- Next action:

Missing items:
- <only include when needed>

Human approval needed before delivery/publication:
- ...

Next action:
<one concrete next action>
```

If producing actual files is requested and enough inputs are present, create the package files. If inputs are not present, output the package plan and missing items.

## Reuse And Ledger Discipline

Every package must identify at least one reuse path or explicitly say why no reuse path is appropriate.

Possible reuse paths:

- Grace Gems listing support.
- Grace Gems FAQ or customer-support response.
- Grace Gems WeChat/social selling support.
- Product education graphic.
- Predictive History YouTube thumbnail.
- Predictive History short-form clip hook.
- Quote card.
- Companion illustration.
- Newsletter or Substack image.
- Archive note.
- Future template candidate.

The ledger-ready summary is preparation only. Do not append to the creative abundance ledger unless the operator explicitly asks and the shipped/reused status is known.

## Decision Rules

- If quality gate approval is missing, mark the package **review**, **revision-needed**, or **hold**, not **approved**.
- If source or rights notes are missing for material claims or external assets, choose **hold** unless the package is only for internal review.
- If Grace Gems owner-approved facts are missing for product/policy/customer claims, choose **hold** or **review** and name the approval needed.
- If Predictive History assets do not support evidence, judgment, prediction/outcome, causality, or learning, choose **revision-needed** rather than packaging as finished.
- If the package implies spend, contractor work, publishing, delivery, listing edits, or external commitments, flag human approval required.
- When in doubt, preserve the package as review-ready and avoid delivery-ready language.

## Done When

The operator has a package that:

- Names the lane, source signal, asset set, and reviewer.
- Preserves brief and quality gate context.
- Separates source files, working files, exports, review notes, and reuse notes.
- Names source, rights, claims, budget, capacity, and authority blockers.
- Includes a reuse path and ledger-ready summary without updating the ledger automatically.
- Stops before publication, client delivery, shipped status, spend approval, or contractor assignment.
