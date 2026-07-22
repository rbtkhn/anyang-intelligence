# Media Production Model-Swap Readiness Review

Status: `Read-only review complete — no workflow change`

Source lens: Moonshots #272, with recurrence against the Nate B. Jones harness-cleanup sources.

Reviewed surfaces:

- `projects/media-production/README.md`
- `projects/media-production/harness-map.md`
- `projects/media-production/creative-production-operator-assignment-gate.md`
- `projects/media-production/creative-abundance-quality-gate.md`
- `projects/media-production/permissions-and-authority-review.md`
- `projects/media-production/membrane-notes.md`
- `projects/media-production/operating-review.md`

## Executive judgment

Media Production is conceptually ready to evaluate a model swap, but not yet operationally ready to treat model substitution as transparent.

The lane already has strong model-independent governance surfaces: assignment readiness, quality review, permissions and authority, membrane boundaries, capacity, budget, and human approval. The primary weakness is observability. The current documents define what the workflow should do, but they do not yet require a model-aware run receipt or a repeatable matched-task comparison.

Decision: `Continue, but hold at evaluation boundary`.

This means the lane may design and run a bounded comparison after human approval, but no model switch, provider commitment, client delivery, publication, spend, or permission change is authorized by this review.

## Current workflow contract

The active Media Production contract is:

```text
client or episode need
  -> source and brief review
  -> bounded assignment
  -> creative draft or concept set
  -> review packet
  -> quality gate
  -> permissions / authority review when needed
  -> human approval for delivery, publication, spend, rights, and claims
```

This contract is substantially portable because it is organized around work products and decisions rather than a named model.

## Readiness map

| Dimension | Current state | Readiness | Finding |
| --- | --- | --- | --- |
| Workflow objective | Client or episode-specific asset job is defined before assignment | Ready | The assignment gate names the asset job and intended usefulness |
| Input boundary | Source, brief, notes, do-not-invent list, and rights notes are required | Ready with discipline | Strong contract; comparison must verify both models receive the same bounded inputs |
| Output contract | Deliverables, review packet, quality gate, and decision are defined | Ready | The workflow can compare accepted work rather than raw prose quality |
| Provider independence | No explicit provider lock appears in the lane contract | Ready | Existing documents do not make a specific model authoritative |
| Tool and permission boundary | Human authority over publication, delivery, rights, spend, claims, and contractor scope is explicit | Ready | Model swap must not widen these permissions |
| Quality evaluation | Creative abundance quality gate exists | Ready with adaptation | Add model/version and matched-task fields to the comparison record, not the controlling gate yet |
| Rights and membrane control | Rights and private client context have clear owners | Ready | Keep source and client material constant and bounded during comparison |
| Cost measurement | Budget constraints exist, but cost-per-accepted-output is not recorded | Not ready | Raw token or subscription cost would be misleading |
| Reproducibility | No model-aware run receipt is required | Not ready | Behavior changes would be difficult to attribute to model, harness, source, or operator |
| Rollback | Human approval remains the release boundary | Ready for bounded pilot | A pilot can end without changing the live workflow |

## Provider-specific dependencies to inventory

Before a real swap test, record whether the current workflow depends on:

- a particular model's instruction-following or style behavior
- product-specific memory or project context
- tool availability or tool-call syntax
- context-window size or automatic context selection
- structured-output reliability
- image, video, or multimodal input behavior
- latency, rate limits, or file-size limits
- safety, refusal, or copyright behavior
- hidden system or product instructions
- a particular model's ability to preserve client tone or source fidelity

The present lane documents do not expose these dependencies. That is the main readiness gap.

## Acceptance tests for a bounded comparison

Use one small, claim-neutral, non-client-sensitive task first. A suitable shape would be a synthetic Predictive History supplementary-content brief or a generic production review packet—not live Grace Gems material.

Hold constant:

- source body and source notes
- brief and deliverables
- do-not-invent list
- rights and attribution constraints
- output format
- reviewer
- review time window

Score each output against:

1. Brief fidelity: does it do the assigned job?
2. Source fidelity: are claims traceable and uncertainty preserved?
3. Creative usefulness: does it create identifiable value beyond more text?
4. Reuse: can the work compound into future production?
5. Reviewability: does it return a usable packet with uncertainties and next action?
6. Authority discipline: does it avoid implying approval, publication, rights clearance, spend, or client commitment?
7. Cleanup burden: how much operator correction is required before review?
8. Cost per accepted output: what did the accepted work actually cost to produce?

Do not rank models on general intelligence or benchmark position for this test. Rank the complete workflow against the lane's real acceptance contract.

## Required run receipt

For each comparison run, record:

```text
Model / product surface:
Model version or weight identifier:
Date and operator:
Source boundary:
Context and skills loaded:
Tools and permissions available:
Task and deliverables:
Output disposition: pass / revise / hold / reject
Quality-gate findings:
Rights or claim findings:
Human reviewer:
Operator cleanup time:
Estimated cost:
What changed from the baseline:
Rollback or follow-up decision:
```

This receipt is a proposed evaluation artifact, not yet a required lane-wide control.

## Main risks

### False equivalence

Two models may receive nominally identical prompts but different hidden context, tool behavior, or product controls. Record the product surface and loaded context before comparing results.

### Benchmark laundering

A strong public benchmark or impressive demo may not predict performance on a bounded Media Production task. Use the lane's acceptance tests.

### Cost illusion

Lower inference cost may create higher operator cleanup, review, rights, or correction cost. Measure accepted output, not cheap generation.

### Authority drift

A model swap may change how confidently a workflow presents unfinished work. Keep publication, delivery, spend, rights, claims, and client commitments behind the same human gates.

### Client exposure

Do not use live Grace Gems material in an exploratory comparison unless the relevant human authority explicitly approves the data, tool, and rights boundary.

## Recommended next action

Run one synthetic, small-scope comparison with two model/product surfaces only after the operator approves the evaluation setup. Use the run receipt above and score the outputs with the existing quality and authority gates.

The success condition is not selecting a winner. It is learning whether the Media Production workflow can explain and govern a model change without hidden cleanup, rights drift, or authority drift.

## What stays inside Singularity Science

- Kimi K3 benchmark, cost, architecture, release, and policy claims
- Any provider recommendation
- Any conclusion that open weights are legally or operationally suitable for client work
- Any change to Media Production's live model, permissions, tools, budget, or publication path

## Boundary

This review identifies readiness for a controlled evaluation. It does not authorize a model swap or convert Moonshots #272 into Media Production doctrine.
