---
name: learner-profile
description: Internal Student Operating System procedure for analyzing evidence and preparing guardian-reviewable learner profiles or exact profile change proposals. Use inside $learner-intake create or $learner-intake change, or when comparing approved learner evidence with the latest effective profile; do not use it as a separate family-facing intake or as authority to mutate a profile.
---

# Learner Profile

Use this skill as the evidence-analysis subroutine behind `$learner-intake`. Produce observations, interpretations, profile wording, and exact proposed changes without claiming mutation authority.

## Required Inputs

For an initial profile, require a parent-verified intake packet and its authority receipt.

For a revision, require:

- opaque learner reference;
- latest confirmed-effective profile and version;
- corresponding approval receipt;
- current authority and preservation boundaries;
- new evidence permitted for this use.

Return `Hold` instead of reconstructing missing authority or profile state from memory.

## Analyze Evidence

1. Separate observed events from parent interpretation, learner voice, and operator hypothesis.
2. Classify evidence as `strong`, `medium`, `thin`, or `none`.
3. Preserve context and counterevidence.
4. Use `Missing` instead of making the profile appear complete.
5. Keep app activity, one episode, and operator intuition from becoming mastery, diagnosis, grade, or fixed-trait claims.
6. Keep only information that could change a planning, support, evidence, or safety decision.

## Prepare An Initial Profile

Use `projects/learning-core/initial-learner-profile-template.md`. Keep it `Proposed Initial Profile` until the complete contents are explicitly approved by the guardian named in the authority receipt.

Approval produces an `Approved Initial Profile Packet` in `Awaiting Persistence`. Only operator confirmation of tenant-private preservation makes it `Effective`.

## Prepare A Change

Compare new evidence with the effective profile and produce one outcome:

- `No Change`;
- `Open Question`;
- exact `Profile Change Proposal`;
- `Hold`.

Require two aligned signals for an ordinary proposal. A single signal may add an open question but may not replace an effective profile claim.

For a proposal, show:

- current effective version;
- each affected field;
- exact before-and-after wording;
- evidence and counterevidence;
- uncertainty retained;
- preservation or deletion implications;
- complete proposed resulting profile.

Do not modify the effective profile. Exact guardian approval creates an approved packet; operator-confirmed preservation creates the new effective version. The prior version remains effective until then.

## Approval And Removal

- Accept approval only from the guardian named in the current authority receipt.
- Bind approval to the exact displayed contents and base version.
- Rerender a smaller change set before accepting partial approval.
- Never infer approval from silence, continued use, weekly review, readiness, drafting authorization, or plan approval.
- Allow guardian-requested reconsideration at any time, but authorize only the exact confirmed correction, revision, or removal.
- Stop use and return `Hold` for safety or privacy concerns without silently rewriting profile content.
- Keep learner-requested content out of use while correction or removal awaits guardian resolution.
- For approved removal, retain only the minimum audit fact; do not repeat removed sensitive content.

## Next Use

Connect an effective profile to one bounded next action, such as choosing a resource, adjusting a rhythm, identifying a next signal, or informing an authorized plan draft. Never let the profile replace parent, teacher, tutor, clinician, or specialist judgment.

## Done When

The output is evidence-grounded, non-diagnostic, explicit about uncertainty, bound to the right authority, and in one honest state: proposed, awaiting guardian decision, awaiting persistence, effective after operator confirmation, no change, deferred, rejected, or hold.
