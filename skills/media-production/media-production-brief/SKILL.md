---
name: media-production-brief
preferred_activation: media-production brief
description: Create review-ready Media Production creative briefs for Grace Gems or Predictive History while preserving claim discipline, rights awareness, capacity limits, and human approval.
category: media-production
status: active
scope_class: customer-work
---

# Media Production Brief Skill

Use [docs/executive-interface-protocol.md](../../../docs/executive-interface-protocol.md) for task dispatch, review responses, escalation, and completion receipts.

Use this skill when the operator asks for:

- `media-production brief`
- `production brief`
- `creative brief`
- a Grace Gems creative support brief
- a Predictive History art, visual, thumbnail, companion graphic, or topic-support brief
- a production brief for the Creative Production Operator

This skill turns a source signal into a review-ready creative production brief. It does **not** publish, package, approve, deliver, append to the creative abundance ledger, or assign contractor work by itself.

## Required Reads

Read these first:

1. `projects/media-production/README.md`
2. `projects/media-production/executive-os-install.md`
3. `projects/media-production/creative-production-operator-onboarding.md`
4. `projects/media-production/creative-abundance-quality-gate.md`

Then read the relevant source for the requested lane:

- **Grace Gems:** product note, listing, customer question, support pattern, service package, trust architecture kit, or operator-provided product context.
- **Predictive History:** episode topic, transcript, outline, source note, prediction/outcome frame, or operator-provided topic context.

If the relevant source is missing, produce a brief with a clear **Missing source needed** section rather than inventing facts.

## Lane Classification

Classify the request before drafting:

| Lane | Use when | Default output posture |
| --- | --- | --- |
| **Grace Gems** | The source is a product, listing, buyer question, marketplace signal, customer-support issue, trust asset, social/WeChat support need, or promotion support need. | Buyer clarity, owner-approved claims, marketplace trust, customer-support usefulness. |
| **Predictive History** | The source is an episode, historical topic, prediction/outcome contrast, quote, judgment lesson, thumbnail need, companion art need, or educational media support need. | Viewer understanding, evidence, causal forces, judgment, prediction vs outcome. |

If both lanes appear, split the brief into two lane-specific briefs instead of blending product claims with educational media support.

## Grace Gems Guardrails

For Grace Gems briefs:

- Do **not** invent product details, prices, dimensions, materials, gemstone identity, authenticity claims, shipping promises, return/repair promises, rush-order commitments, certificate/appraisal language, or project-specific facts.
- Mark product, policy, pricing, authenticity, shipping, and customer-promise claims as **owner approval required** unless already approved in the provided source.
- Use Grace Gems work to improve buyer clarity, listing trust, customer support, FAQ/objection handling, and reusable product communication.
- If the source is a buyer message or support transcript, preserve privacy and convert the issue into a generic customer-confusion pattern unless explicit reuse is approved.

Relevant follow-on skills:

- `skills/grace-gems/trust-claim-review/SKILL.md` for product, policy, authenticity, certificate, shipping, repair, return, rush-order, or support claims.
- `skills/grace-gems/customer-support-intelligence/SKILL.md` for transcript or repeated buyer-message analysis.
- `skills/grace-gems/marketplace-listing-gate/SKILL.md` before listing publish, revision, promotion, or ad decisions.

## Predictive History Guardrails

For Predictive History briefs:

- Do **not** create decorative history wallpaper.
- Every asset must support at least one of: judgment, evidence, prediction/expectation, outcome, causal forces, decision problem, or lesson learned.
- Mark uncertain historical claims, quotes, images, maps, likenesses, music, and source rights as **source/rights check required**.
- Prefer visual concepts that make the viewer understand the problem faster, not concepts that merely look dramatic.
- Avoid sensationalism that distorts the episode's judgment lesson.

## Brief Output

Produce this exact structure:

```text
Production brief:
Lane:
Source signal:
Audience / user:
Asset job:
Core message:

Required facts or source notes:
- ...

Claims / rights / approval risks:
- ...

Concept directions:
1. ...
2. ...
3. ...

Recommended first asset:
<one asset type + why>

Quality gate concerns:
- Strategic fit:
- Abundance created:
- Accuracy and trust:
- Reuse and compounding:
- Audience usefulness:
- Capacity and budget:

Reuse / repurposing path:
- ...

Missing source needed:
- <only include when needed>

Human approval needed before delivery/publication:
- ...
```

Use 3-5 concept directions. If fewer than three honest directions exist, say what source input is missing.

## Recommended Asset Types

Use these as options, not defaults:

- Production brief
- Thumbnail concept
- Illustration concept
- Product FAQ graphic
- Customer-support response asset
- WeChat/social selling support asset
- Quote card
- Timeline or map concept
- Slide/diagram asset
- Short-form video hook
- Storyboard
- Companion graphic
- Visual reference board
- Caption or description draft

## Capacity And Budget Check

Every brief must ask:

- Does this fit current Creative Production Operator capacity?
- Does it require paid tools, paid assets, contractor time, or additional spend?
- Is the $500 contractor allocation or remaining $500 monthly budget implicated?
- Has a human approved any spend or commitment?

If capacity or spend is uncertain, mark the brief **Hold for capacity/budget review** rather than recommending production.

## Done When

The operator has a review-ready production brief that:

- Names the lane.
- Names the source signal.
- Defines the asset job and audience.
- Preserves Grace Gems claim discipline or Predictive History evidence/judgment discipline.
- Identifies rights, claims, source, budget, and approval risks.
- Recommends exactly one first asset.
- Stops before publication, delivery, packaging, ledger update, or contractor assignment.
