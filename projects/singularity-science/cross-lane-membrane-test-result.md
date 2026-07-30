# Cross-Lane Membrane Test Result

Date: 2026-07-29
Status: `completed — review exercise only`
Primitive tested: Model Substitution Readiness Gate, including Cross-lane membrane rules

## Artifacts reviewed

- Learning Core: [Nested-Loop Authority Review](../learning-core/nested-loop-authority-review.md)
- Media Production: [Model-Swap Readiness Review](media-production-model-swap-readiness-review.md)

## Shared method tested

`evidence → bounded draft or test → human review → observed outcome → correction → approved reuse`

The test asked whether this method could transfer while keeping evidence, corrections, and authority inside each lane.

## Results

| Rule | Learning Core | Media Production | Judgment |
|---|---|---|---|
| Lane-local evidence | Approved evidence and preservation boundaries are required | Source, brief, rights, and client boundaries are required | pass |
| Canonical human authority | Parent/guardian remains canonical | Producer, client, and rights authority remain human | pass |
| Observation versus interpretation | Explicitly required | Source fidelity and uncertainty review required | pass |
| No automatic cross-lane judgment transfer | Child, family, and educational authority are held | Client, publication, rights, spend, and creative authority are held | pass |
| Model/state portability | No live model change permitted; artifact remains bounded | Model-independent workflow contract; observability gap remains | pass with hold |
| Cross-lane reuse approval | Default is hold for missing authority | Translation and lane-owner review remain required | pass |
| Evidence of operational benefit | Not measured | Cleanup, cost, and independent comparison incomplete | hold |

## What transferred safely

- The review sequence and ownership questions.
- The distinction between evidence, interpretation, correction, and approved reuse.
- The requirement for visible authority, rollback, and portability.
- The rule that a shared method may transfer only after translation review.

## What stayed separate

- Learning Core's child, family, privacy, and parent-authority judgments.
- Media Production's client, publication, rights, spend, and creative-approval judgments.
- Source-specific evidence, prompts, retained context, and provider behavior.
- Any claim that either lane is ready for a live model change.

## Decision

`Review exercise only`.

The membrane rules successfully prevent automatic transfer of lane-specific authority while allowing the governance method to be shared. No lane artifact was mutated, no cross-lane doctrine was created, and no customer or child-facing action was authorized.

## Remaining evidence gap

The test does not establish that the shared method improves outcomes, reduces burden, or preserves learning under an actual independent model change. Those questions remain subject to the measurement addendum and independent-surface requirement.
