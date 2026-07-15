# Learning Through Contrast

## Success–Friction–Bridge Learner Intake Report

## Executive Finding

Success–Friction–Bridge is a promising evidence-first structure for Learning Core learner intake.

Its value does not come from collecting one positive story and one difficult story. Its value comes from comparing two concrete episodes involving the same learner:

```text
When learning flowed, what conditions were present?
When learning broke down, what changed?
Which useful condition might bridge the difference?
```

This shifts intake away from abstract personality inventories and toward observable relationships among context, agency, reasoning, persistence, feedback, and recovery. The result is not a fixed description of the child. It is a bounded set of working hypotheses and one possible experiment for a later, separately authorized learning cycle.

The design remains a proposal until tested in a real, parent-authorized, privacy-approved intake. It must not be described as validated assessment methodology.

## The Problem With Trait-First Intake

Questions such as these appear efficient:

- Is the learner persistent?
- Is the learner creative?
- Is the learner visual or hands-on?
- Does the learner like challenges?
- Is the learner independent?

They are weak intake questions because they ask the parent to summarize the learner before the operator has evidence. They encourage broad labels, hide contextual variation, and make one impression sound stable.

A polished profile can then become more certain than its sources.

Success–Friction–Bridge starts somewhere narrower:

- one recent episode in which engagement and learning became visible;
- one recent episode in which engagement stalled or broke down;
- the learner's perspective on both episodes, when participation is approved and comfortable;
- one testable bridge between the two.

The method asks what happened before asking what the episode means.

## Why Contrast Is Useful

A success episode alone creates a risk of flattering overinterpretation. A friction episode alone creates a risk of deficit labeling. Paired episodes produce a within-learner contrast.

| Dimension | Success evidence | Friction evidence |
| --- | --- | --- |
| Initiation | What drew the learner in? | What made beginning difficult? |
| Meaning | Why did the activity matter? | When did it stop feeling meaningful? |
| Ownership | What could the learner choose? | Where was choice absent or unclear? |
| Challenge | What made the work satisfyingly difficult? | Was it repetitive, confusing, exposed, or overwhelming? |
| Strategy | How did the learner approach the problem? | Which strategy stopped working? |
| Flexibility | How did the learner adapt? | Did the learner repeat, switch, pause, or seek help? |
| Feedback | What information supported progress? | What correction or feedback changed engagement? |
| Regulation | What sustained energy? | What preceded withdrawal, distraction, or escalation? |
| Social context | Who supported without taking over? | Did interaction help or inhibit engagement? |
| Transfer | What did the learner do afterward? | What might make returning possible? |

The contrast does not prove cause. It identifies a relationship worth testing.

## Proposed Intake Structure

Success–Friction–Bridge is the central evidence module inside `$learner-intake create`; it is not a replacement for the governed intake. Direction, household fit, tools, caution boundaries, evidence handling, readiness classification, profile approval, persistence, drafting, and plan use remain governed by the existing learner-intake contracts.

### Phase 1: Registration And Authority

Target: 8–10 minutes.

Confirm the minimum conditions required to proceed:

- opaque learner reference;
- parent-approved display label;
- guardian authority;
- intake permission;
- privacy and preservation boundaries;
- duplicate or existing-profile status;
- permission for optional learner participation.

Do not collect personality or capability claims during registration. Unresolved authority, privacy, identity, safety, or duplication conditions produce `Hold`.

### Phase 2: Parent Episode Reconstruction

Target: 15–20 minutes.

The parent selects one recent success and one recent friction episode. The interface then uses clickable, scene-based questions to reconstruct each sequence. The operator asks only the additional governed questions needed to establish direction, cross-context learning, household fit, tools, caution boundaries, evidence handling, and readiness. Episode reconstruction alone cannot produce `Ready`.

#### Success sequence

```text
spark
  -> learner's first move
  -> intellectual action
  -> first obstacle
  -> adaptation
  -> visible evidence of understanding
  -> spontaneous extension
```

#### Friction sequence

```text
starting condition
  -> exact turning point
  -> learner's immediate response
  -> adult response
  -> recovery attempt
  -> return, transformation, or non-return
```

Questions should refer to observable scenes rather than categories. For example:

> In the difficult episode, what was the exact turning point when the learner's energy changed?

Clickable answers might distinguish:

- instructions becoming unclear or expanding;
- a mistake becoming visible or exposing comparison;
- the activity losing meaning or learner ownership.

The selected answer is a structured signal. It is not yet a profile claim.

### Phase 3: Learner Bridge

Target: 5–7 minutes. Participation is optional and requires parent approval.

The learner responds to the actual episodes selected by the parent. The learner answers first, may skip every question, and is not required to agree with the parent's interpretation.

The three approved learner prompts ask:

- what pulled the learner into the successful episode;
- what the difficult moment felt like from the learner's perspective;
- which support, condition, or next move the learner would choose to try.

Every prompt should use clickable choices and a visible `Skip` action. The named guardian must approve the exact child-facing questions before they are shown. Parent and learner disagreement becomes an `Open Question`, not an error to resolve during intake.

### Operational Clickable Question Set

The canonical operational set now lives in the learner-intake skill's [clickable create cards](../../skills/student-operating-system/learner-intake/references/clickable-create-cards.md). Keeping one source prevents the report, parent message, and skill from drifting into different question sets.

The set contains:

- eleven short readiness cards covering direction, preservation, contexts, agency, household fit, tools, evidence, and caution, plus one bounded caution follow-up when triggered;
- six core episode cards;
- four conditional episode cards shown only when triggered;
- three learner cards with no more than four substantive choices plus `None fit` and `Skip`.

An episode-anchor confirmation binds selections to one recent scene without inviting an unrestricted history. The operator constructs episode-specific contrast choices for parent confirmation rather than asking the parent to perform causal analysis. A second bounded choice set may rerender the same learner card once when `None fit` is selected; it does not become a fourth learner question.

### Closing Gate: Parent Verification

The operator first prepares the governed authority receipt and intake/readiness packet. A `Hold` ends with only the missing decision and deciding human. For `Ready` or `Provisional`, the operator may then prepare a separate proposed initial learner profile. The parent then:

- corrects factual errors;
- distinguishes observation from interpretation;
- removes information that should not be preserved;
- approves, rejects, or requests changes to the exact profile;
- separately decides whether drafting may begin.

An approved profile remains `Awaiting Persistence` until an authorized operator confirms preservation in the tenant-private store. Intake, readiness, profile approval, persistence, plan drafting, and plan use remain separate decisions.

## Clickable Interaction Design

Clickable questions reduce response burden and make the intake easier to complete, but static answer lists can become generic taxonomies. The interface should therefore branch from specific scenes.

### Design rules

1. Ask no more than three question cards at once.
2. Anchor every Phase 2 question to one recent episode.
3. Describe observable actions in answer choices.
4. Use the parent's selection to determine the next question.
5. Keep `not observed`, `uncertain`, and learner `Skip` outcomes available.
6. Avoid recommended or preferred answers.
7. Do not translate a click directly into a personality adjective.
8. Preserve contradictions and missing evidence.

### Evidence metadata

Where the interface supports it, attach click-only metadata:

- recency: past 7 days / past 30 days / older;
- source: parent observed / visible artifact / learner reported;
- evidence quality: strong / medium / thin / none.

These fields improve traceability but do not make weak evidence strong.

## Amplified Operating Model

The strongest version can inform a small learning experiment after the profile is effective and the guardian separately authorizes drafting and plan use:

```text
Success
  -> Friction
  -> Contrast
  -> Learner bridge
  -> Small experiment
  -> New evidence
  -> Parent-reviewed profile decision
```

### Step 1: Reconstruct

Preserve both episodes as factual sequences. Keep parent interpretation separate.

### Step 2: Contrast

Identify conditions present in the success episode and absent or changed in the friction episode.

### Step 3: Form A Working Hypothesis

Use contextual language:

> When the goal is visible and the method remains selectable, the learner currently appears more willing to revise an unsuccessful attempt.

Avoid fixed language:

> The learner is a hands-on learner.

### Step 4: Invite A Learner Bridge

Let the learner choose one condition worth trying, such as:

- a clearer first move;
- meaningful choice of method;
- a visible example;
- a smaller initial challenge;
- a different medium;
- time to pause and return;
- collaboration with a particular person;
- a clearer purpose.

### Step 5: Propose One Small Experiment

Name:

- the condition being changed;
- the observable response expected;
- evidence that would strengthen the hypothesis;
- evidence that would weaken it;
- the parent-controlled pause condition.

During intake, this remains only a candidate. It may enter a 30-day plan only after the profile is effective, drafting is separately authorized, and the resulting plan is approved for use. The experiment should reveal the learner, not pressure the learner to confirm the profile.

## Analytical Outputs Within Governed Packets

These outputs do not replace the authority and privacy receipt, intake/readiness packet, proposed profile, exact guardian decision, approved profile packet, or persistence handoff. They are optional analytical components placed inside those governed surfaces when evidence supports them.

### Episode Pair

A concise factual reconstruction of the success and friction episodes.

### Contrast Map

The conditions that remained stable, appeared, disappeared, or changed between episodes.

### Working Hypothesis

A contextual and provisional statement with evidence and counterevidence.

### Learner Bridge

The support, condition, or next direction selected by the learner, when learner voice is available.

### Experiment Candidate

One possible change small enough to observe without increasing family burden materially. Intake approval does not authorize its use.

### Next Signal

One behavior that could strengthen or weaken the working hypothesis.

## Synthetic Illustration

The following example is fictional and contains no real learner information.

### Success

A learner chose to build a small bridge from available materials. The goal was visible, the method was open, and feedback was immediate: the bridge either held weight or did not. After the first collapse, the learner changed the supports and tried again.

### Friction

During a separate multi-step worksheet, the starting point was unclear, the method was fixed, and errors were visible before the learner understood the overall goal. The learner stopped after the first correction.

### Weak Interpretation

> The learner is hands-on and dislikes worksheets.

### Better Working Hypothesis

> A visible endpoint and meaningful method choice may currently support initiation and revision after failure. When the entry point is unclear and the method is fixed, engagement may fall before problem-solving begins.

### Learner Bridge

Choose between drawing the solution and building a small model before writing the final response.

### Next Experiment

For the next multi-step task, show the endpoint, offer two starting methods, and observe whether the learner begins and attempts a second strategy with less adult prompting.

### Evidence That Would Strengthen The Hypothesis

The learner initiates more readily and revises after an unsuccessful attempt when the endpoint and method choice are visible.

### Evidence That Would Weaken The Hypothesis

The learner still withdraws despite a clear endpoint and meaningful choice, or persists equally well in a fixed-method task when the starting step is clear.

## Risks And Controls

### Anecdote Inflation

Two episodes remain a small sample. Use them to form hypotheses and experiments, not stable ability claims.

### Parent Selection Bias

The parent may choose unusually memorable events. Preserve recency, context, and evidence source, and ask what would count as a counterexample.

### False Causality

Success and friction may differ because of fatigue, domain familiarity, relationship, timing, or other unobserved factors. Name alternatives and test only one change at a time.

### Learner Conformity

The learner may echo the parent. Ask the learner first, allow skipping, and preserve differences without correction pressure.

### Profile Fixation

Do not turn a useful condition into a permanent learning-style label. Require two aligned signals before an ordinary profile-change proposal and exact guardian approval before changing an effective profile.

### Learner Correction Or Removal

The learner may request correction or removal of learner-voice content. Stop reusing the affected content while guardian resolution is pending. An approved removal preserves only the minimum audit fact and never repeats the removed sensitive material.

### Excessive Observation

Do not convert the experiment into continuous monitoring. Preserve only one useful next signal under the parent's evidence boundary.

## Usefulness For Learning Core

Success–Friction–Bridge can help Learning Core:

- obtain multiple learner signals from two memorable episodes;
- reduce abstract parent paperwork;
- make learner voice concrete and low pressure;
- connect context, agency, reasoning, persistence, and recovery;
- produce one humane first-cycle experiment;
- preserve uncertainty and counterevidence;
- improve profiles through governed recursive learning;
- help the learner increasingly notice what supports their own learning.

It supports the Learning Core principle that school becomes something the learner carries. The learner begins to notice not only what they learned, but how they entered a question, responded to difficulty, made a connection, and chose what to try next.

## Recommendation

Use Success–Friction–Bridge as the leading candidate for the first real learner-intake cycle, not yet as universal doctrine.

The next proof should be one bounded, parent-authorized intake that tests:

- whether the clickable questions produce concrete rather than generic answers;
- whether the episode contrast yields a useful but appropriately provisional hypothesis;
- whether the learner can choose a bridge without pressure;
- whether the resulting experiment is feasible for the household;
- whether the parent finds the proposed profile accurate, respectful, and worth preserving.

After that cycle, record what worked, what produced friction, what should remain family-specific, and whether the method deserves refinement or broader adoption.
