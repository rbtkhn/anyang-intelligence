---
name: trust-claim-review
description: Grace Gems trust claim review procedure. Use when drafting or reviewing Grace Gems claims about natural stones, gemstones, gold purity, appraisal certificates, custom work, warranties, returns, repairs, shipping timelines, rush orders, authenticity, support promises, product facts, public copy, listing claims, customer replies, or Media Production assets that include product or policy claims.
---

# Trust Claim Review Skill

Use this skill before Grace Gems product, policy, authenticity, certificate, shipping, repair, return, rush-order, or support claims are published, delivered, or sent to customers.

This is a Grace Gems product-level guardrail skill, not legal advice.

## Purpose

Help Anyang Intelligence keep Grace Gems trust claims evidence-grounded, owner-approved, and safe for marketplace use.

## Standard Output

When this skill is used, produce:

```text
Trust-claim-review checklist:
- Claim text:
- Claim type:
- Source evidence:
- Public-risk level:
- Unsupported expansion:
- Owner approval:
- Safer wording:
- Next action:

Artifact:
<owner-review claim list, claim-safe copy draft, hold recommendation, or evidence request>
```

## Procedure

### 1. Identify The Claim

Name the exact claim and where it will appear:

- Etsy listing.
- Shop policy.
- FAQ.
- Customer reply.
- WeChat/social post.
- Graphic.
- Short video.
- Media Production asset.
- Owner-review draft.

### 2. Classify Claim Type

Use one or more:

- Natural stone or gemstone claim.
- Gold purity claim.
- Appraisal or certificate claim.
- Custom-order claim.
- Warranty, repair, return, or refund claim.
- Shipping or rush-order claim.
- Authenticity claim.
- Support availability or response-speed claim.
- Price, discount, or promotion claim.
- Other product fact.

### 3. Check Evidence

Use only:

- Owner-approved product facts.
- Current listing data.
- Owner-approved shop policy text.
- Owner-approved support language.
- Product documentation.
- Support transcripts as private evidence for owner review.

If evidence is missing, hold the claim and ask for owner approval or source evidence.

### 4. Detect Unsupported Expansion

Flag when a draft:

- Makes a stronger promise than the evidence supports.
- Generalizes from one product to all products.
- Turns optional availability into a guarantee.
- Changes timing, cost, refund, repair, or shipping commitments.
- Adds authenticity, certificate, appraisal, or material claims not approved by the owner.

### 5. Choose Safer Next Action

Use one:

- Approve for owner review.
- Rewrite with narrower wording.
- Hold pending evidence.
- Prepare owner question.
- Route money or refund classification through `skills/tax-financial-governance/SKILL.md`.
- Route listing implications through `skills/grace-gems/marketplace-listing-gate/SKILL.md`.

## Guardrails

Do not:

- Give legal advice.
- Make final authenticity, appraisal, warranty, refund, return, shipping, or policy determinations.
- Expand claims beyond owner-approved evidence.
- Publish public copy without owner approval.
- Treat public Etsy signals as complete business truth.
- Use customer-support transcripts as public proof without approval.

## Done When

Each claim has source evidence, risk level, owner-approval status, unsupported expansions flagged, safer wording if needed, and a next action.
