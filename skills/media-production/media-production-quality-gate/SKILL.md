---
name: media-production-quality-gate
preferred_activation: media-production quality gate
description: Review Media Production assets against the Creative Abundance Quality Gate and return Approve, Revise, Hold, or Reject while preserving human authority.
category: media-production
status: active
scope_class: customer-work
---

# Media Production Quality Gate Skill

Use this skill when the operator asks for:

- `media-production quality gate`
- `quality gate`
- `abundance gate`
- `review this asset`
- `approve/revise/hold/reject`
- a readiness review for a Grace Gems or Predictive History asset
- a Creative Production Operator draft review

This skill reviews a draft or review-ready Media Production asset before it is treated as ready for client review, publication, delivery, packaging, or ledger entry. It does **not** publish, deliver, package, append to the creative abundance ledger, assign contractor work, or approve spending by itself.

## Required Reads

Read these first:

1. `customers/media-production/creative-abundance-quality-gate.md`
2. `customers/media-production/creative-production-operator-onboarding.md`
3. `customers/media-production/executive-os-install.md`
4. `customers/media-production/README.md`

When available, also read:

- The production brief produced by `skills/media-production/media-production-brief/SKILL.md`.
- The asset, draft text, concept description, source notes, or operator-provided review package.
- For Grace Gems: relevant product/listing/customer-support source and owner-approved facts.
- For Predictive History: relevant topic, transcript, outline, source note, or prediction/outcome frame.

If the brief, asset, or source notes are missing, do not invent context. Mark the decision **Hold** until the missing input is supplied.

## Decision Labels

Return exactly one final decision:

| Decision | Meaning |
| --- | --- |
| **Approve** | Ready for the next human-approved step. No material quality, source, rights, claim, capacity, or budget blocker remains. |
| **Revise** | Direction is useful, but specific changes are needed before review/delivery/publication. |
| **Hold** | Do not proceed because source, approval, rights, capacity, budget, or governance information is missing. |
| **Reject** | The asset is strategically wrong, misleading, too generic, unsafe, low-value, or not worth revising in its current direction. |

Approval from this skill is **review readiness**, not autonomous publication or client delivery. Humans retain final authority over creative direction, publication, client commitments, rights decisions, spending, hiring, and external claims.

## Gate Dimensions

Review the asset against all six dimensions from the Creative Abundance Quality Gate:

### 1. Strategic Fit

Ask:

- What client need, topic need, product need, or audience need does this asset serve?
- What decision, sale, lesson, customer action, or audience understanding should become easier?
- Is this tied to an approved brief, product need, production priority, or topic frame?

Pass condition: the asset has a clear job.

### 2. Abundance Created

Ask what the asset makes more abundant:

- Buyer confidence.
- Product clarity.
- Audience understanding.
- Customer support capacity.
- Reusable creative memory.
- Sales support.
- Community participation.
- Calm execution.
- Other clearly named value.

Pass condition: the asset creates identifiable value beyond existing as content.

### 3. Accuracy And Trust

Ask:

- Are product details, historical claims, prices, dimensions, timelines, or commitments accurate?
- Is uncertainty clearly flagged?
- Does the asset avoid exaggeration, invented claims, sensationalism, or misleading visuals?
- Are source notes, product references, rights notes, or approval needs recorded?

Pass condition: no material claim is unsupported or misleading.

### 4. Reuse And Compounding

Ask:

- Can this asset be reused, adapted, split, or repurposed?
- Does the file name or asset description make reuse easy?
- Are source files, prompts, captions, exports, or notes preserved where future work can find them?
- Is there a next asset this should generate?

Pass condition: the asset can compound instead of disappearing after one use.

### 5. Audience Or Customer Usefulness

Ask:

- Would this help a real customer, buyer, viewer, or community member?
- Is the message readable on the intended device or channel?
- Is the hook clear without being misleading?
- Does the asset reduce confusion or improve understanding?

Pass condition: the asset is useful to someone outside the production process.

### 6. Capacity And Budget

Ask:

- Does this fit the Creative Production Operator's current workload?
- Does it require paid tools, paid assets, contractor time, subscriptions, distribution spend, or other budget?
- If spending is needed, has a human approved it?
- Does this asset create enough value to justify the effort?

Pass condition: the work fits current capacity and budget constraints.

## Lane-Specific Guardrails

### Grace Gems

For Grace Gems assets:

- Any product, policy, pricing, authenticity, shipping, repair, return, certificate/appraisal, rush-order, or customer-promise claim requires owner-approved source evidence.
- Buyer-message or support-derived assets must preserve privacy and convert private customer facts into generic confusion patterns unless explicit reuse is approved.
- If a claim is unsupported, decision must be **Hold** or **Revise**, not **Approve**.

Use follow-on skills when needed:

- `skills/grace-gems/trust-claim-review/SKILL.md`
- `skills/grace-gems/customer-support-intelligence/SKILL.md`
- `skills/grace-gems/marketplace-listing-gate/SKILL.md`

### Predictive History

For Predictive History assets:

- The asset must support judgment, evidence, prediction/expectation, outcome, causal forces, decision problem, or lesson learned.
- Decorative history wallpaper, generic drama, or visuals that distort the lesson should be **Reject** or **Revise**.
- Uncertain historical claims, quotes, images, maps, likenesses, music, and source rights require source/rights review before approval.

## Output Format

Produce this exact structure:

```text
Quality gate review:
Lane:
Asset reviewed:
Source / brief checked:
Current status:

Decision:
<Approve | Revise | Hold | Reject>

Reason:
<short decision rationale>

Gate scores:
- Strategic fit: Pass / Revise / Hold / Reject - <reason>
- Abundance created: Pass / Revise / Hold / Reject - <reason>
- Accuracy and trust: Pass / Revise / Hold / Reject - <reason>
- Reuse and compounding: Pass / Revise / Hold / Reject - <reason>
- Audience/customer usefulness: Pass / Revise / Hold / Reject - <reason>
- Capacity and budget: Pass / Revise / Hold / Reject - <reason>

Required changes or blockers:
- ...

Source / rights / approval needs:
- ...

Next action:
<one concrete next action>

Human authority boundary:
- <what still requires human approval before delivery/publication/spend>
```

## Decision Rules

- If any material source, rights, claim, capacity, budget, or approval input is missing, choose **Hold** unless the asset can be safely revised without that input.
- If the asset is useful but needs concrete improvement, choose **Revise** and name the smallest sufficient changes.
- If the asset fails the core job or would create misleading/generic/low-value work, choose **Reject**.
- Choose **Approve** only when every gate dimension passes and no human-approval blocker remains for the next step.
- When in doubt between **Approve** and **Revise**, choose **Revise**.
- When in doubt between **Revise** and **Hold** because source or authority is missing, choose **Hold**.

## Done When

The operator has:

- One clear decision: `Approve`, `Revise`, `Hold`, or `Reject`.
- A reason tied to the six quality-gate dimensions.
- Any source, rights, claim, budget, or human-approval blockers named.
- One concrete next action.
- No accidental publication, delivery, packaging, ledger update, spend approval, or contractor assignment.

