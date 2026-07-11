# Evidence Awareness Checklist

This checklist is the repo-wide claim discipline gate for Anyang Intelligence.

Use [Analytical Interfaces](analytical-interfaces.md) alongside this checklist: this document governs whether a claim is supportable, while that contract governs whether the resulting judgment is recoverable from reader-facing labels and structure.

Use it when a doc, skill, customer artifact, research analysis, recommendation, plan, brief, operating review, or generated output makes claims that could affect action, trust, spending, child-facing decisions, customer commitments, publication, rights, governance, or cross-lane transfer.

The goal is not to make every sentence bureaucratic. The goal is to prevent polished language from outrunning evidence.

## Core Rule

Every material claim should be classified before it becomes operational.

Use the lightest classification that is honest:

| Classification | Use when | Allowed action |
| --- | --- | --- |
| `source-backed` | A specific source, artifact, receipt, metric, URL, transcript, ledger, or record supports the claim | May be used with attribution and any required rights or membrane limits |
| `customer-approved` | The relevant customer, owner, parent, board, or authority layer explicitly approved or supplied the claim | May be used inside that lane within the approved scope |
| `template-default` | The statement is neutral reusable structure, not a specific factual claim about a customer, learner, asset, or source | May be used if it does not imply false specificity |
| `provisional-assumption` | The claim is plausible but incomplete, and is visibly labeled as an assumption | May support draft work only; must return for approval or evidence before final use |
| `speculative-scenario` | The claim is a forecast, worldview, hypothesis, or scenario pressure | May inform research or planning; must not be presented as fact or doctrine |
| `unsupported-hold` | The claim lacks support or authority for the intended use | Do not use operationally; mark missing, ask for evidence, or hold |

## Claim Discipline Questions

Before using a material claim, ask:

- What exact sentence or recommendation depends on this claim?
- What source, approval, artifact, or observation supports it?
- Who has authority to approve or reject it?
- Is it local to one project lane or safe to generalize?
- Is it stable, or could it change with time, policy, prices, ownership, model behavior, law, or customer context?
- What would go wrong if this claim is false, overstated, stale, or used outside its membrane?
- Should the output say `unknown`, `provisional`, `needs review`, or `hold` instead?

## Evidence Strength

Use this simple strength scale when a claim matters:

| Strength | Meaning |
| --- | --- |
| `strong` | Direct evidence from an authoritative source, customer approval, official record, validated artifact, or first-party observation |
| `medium` | Reasonable support exists, but it depends on interpretation, partial source coverage, or context that should remain visible |
| `thin` | The claim depends on incomplete intake, weak source notes, analogy, memory, simulation, or a single unverified source |
| `none` | No usable support for the intended claim |

Strong evidence can still be unsafe if the authority boundary is wrong. Thin evidence can still be useful if it is labeled and kept provisional.

## Source-To-Claim Map

For high-trust or externally visible work, create a compact source-to-claim map:

| Claim | Classification | Evidence strength | Source / approval | Scope | Boundary |
| --- | --- | --- | --- | --- | --- |
|  | source-backed / customer-approved / template-default / provisional-assumption / speculative-scenario / unsupported-hold | strong / medium / thin / none |  | customer-local / reusable primitive / research-only / public-ready |  |

Use [templates/claim-discipline-map.md](../templates/claim-discipline-map.md) when a reusable table is helpful.

## Lane Defaults

### Learning Core

Default to `unsupported-hold` unless the claim comes from parent-approved intake, parent-approved student voice, approved resources, or a neutral template default.

Never treat app progress, mock simulations, or operator intuition as proof of mastery, diagnosis, legal compliance, or child-facing approval.

### Media Production

Default to `provisional-assumption` for product details, rights, dates, pricing, materials, dimensions, authenticity, publication captions, customer commitments, and claims about what an asset proves.

Move to `source-backed` or `customer-approved` only when source notes, owner approval, product references, or rights review support the claim.

### Grace Gems

Default to `unsupported-hold` for authenticity, material, stone, price, shipping, return, policy, customer commitment, or listing claim details unless owner-approved or source-backed.

### Singularity Science

Default to `speculative-scenario` for forecasts, model capability claims, governance predictions, personhood claims, BCI timelines, political claims, and source rhetoric.

Move to `source-backed` only with source metadata, verification notes, and rights-aware attribution. Move outward only after membrane translation.

### retired Non-Profit project

Default to `provisional-assumption` or `unsupported-hold` for donor intent, restricted funds, grant compliance, board authority, tax treatment, employment, or program impact claims unless the appropriate authority and evidence are visible.

### Mountain Villa

Default to `provisional-assumption` for safety, property condition, maintenance urgency, insurance, vendor, cost, and legal implications unless supported by records, photos, owner review, professional inspection, or other direct evidence.

### Book Club

Default to `template-default` for generic community structure and `customer-approved` for organizer-specific tone, boundaries, events, or donor language. Do not turn community enthusiasm into obligations.

## Failure Modes

Watch for these evidence-awareness failures:

- **Polished guess:** a draft sounds complete because missing inputs were smoothed over.
- **Approval mirage:** the output says approval is needed but does not name who approves what.
- **Source laundering:** a transcript, interview, or external source becomes Anyang doctrine without verification.
- **Membrane leak:** a customer-local fact becomes a reusable product claim.
- **Evidence inflation:** a weak signal is described as proof, mastery, diagnosis, completion, or validation.
- **Temporal drift:** a claim about prices, laws, product specs, people, model capability, policy, or schedules is treated as stable.
- **Authority inversion:** the AI-generated recommendation becomes the decision instead of returning to the human authority layer.

## Minimum Passing Standard

An artifact is evidence-aware enough to proceed when:

- material claims are classified or obviously neutral
- weak claims are labeled as provisional, speculative, missing, or hold
- source-backed claims include source metadata or a clear evidence pointer
- customer-approved claims name the relevant authority layer
- reusable primitives do not contain private customer facts
- high-trust lanes preserve the strictest applicable approval boundary

If these conditions are not met, revise before delivery, publication, lane transfer, or durable doctrine.

## Relation To Artificial Enlightened Intelligence

[Artificial Enlightened Intelligence](artificial-enlightened-intelligence.md) requires evidence awareness.

An AI system does not become more enlightened by sounding certain. It moves in the right direction when it can say:

```text
this is supported
this is approved
this is a template default
this is provisional
this is speculative
this should hold
```

That classification is how capability stays honest.
