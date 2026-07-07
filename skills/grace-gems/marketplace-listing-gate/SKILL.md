---
name: marketplace-listing-gate
description: Grace Gems marketplace listing gate procedure. Use before publishing, revising, or promoting Etsy listings or Grace Gems product pages, especially when reviewing product identity, photo/product match, SEO/search intent, pricing or margin evidence, customer promise, shipping or return implications, support questions, owner approval, or hold/publish recommendations.
---

# Marketplace Listing Gate Skill

Use this skill before a Grace Gems listing is published, revised, promoted, or sent for owner review.

This is a Grace Gems product-level skill, not a generic Etsy checklist.

## Purpose

Help Anyang Intelligence protect Grace Gems from listings that are unclear, unsupported, low-margin, weakly differentiated, or risky to promote.

## Standard Output

When this skill is used, produce:

```text
Marketplace-listing-gate checklist:
- Listing/product:
- Product identity:
- Photo/product match:
- SEO/search intent:
- Price/margin evidence:
- Customer promise:
- Shipping/return implications:
- Support questions:
- Owner approval:
- Recommendation:

Artifact:
<listing review, hold/publish recommendation, owner question list, or revision brief>
```

## Procedure

### 1. Identify The Listing

Name the product, storefront, listing status, and intended action:

- Publish.
- Revise.
- Promote.
- Hold.
- Retire.
- Send to owner review.

If the listing identity is unclear, stop and request the listing link or product reference.

### 2. Check Marketplace Fit

Review:

- Product identity and differentiation.
- Storefront fit.
- Search intent and likely buyer query.
- First-image strength.
- Photo/product match.
- Copy clarity.
- Customer promise clarity.

Do not invent performance data, Etsy policy conclusions, or product facts.

### 3. Check Business Evidence

Look for:

- Price.
- Material cost.
- Labor time.
- Shipping cost.
- Packaging cost.
- Ad spend or promotion assumption.
- Margin risk.
- Inventory or custom-order constraints.

If money, pricing, margin, refunds, taxes, accounting, or payment classification matters, route through `skills/tax-financial-governance/SKILL.md`.

### 4. Check Owner-Approval Needs

Owner approval is required before changing or publishing:

- Product claims.
- Pricing.
- Shop policies.
- Refunds or returns.
- Shipping promises.
- Rush-order promises.
- Appraisal or certificate language.
- Authenticity claims.
- Customer commitments.

### 5. Choose Recommendation

Use one:

- Publish.
- Revise.
- Promote.
- Hold.
- Retire.
- Request owner approval.
- Request missing evidence.

## Guardrails

Do not:

- Publish or promote without owner approval.
- Expand product claims beyond evidence.
- Treat public Etsy signals as complete business truth.
- Recommend ad spend when margin evidence is missing.
- Change customer promises, refunds, returns, shipping, rush timing, certificate language, authenticity claims, or pricing without owner approval.

## Done When

The listing has a clear recommendation, missing evidence is named, owner-approval needs are explicit, and the next artifact is ready for owner review or operational follow-up.
