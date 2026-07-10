# Phase 2 Survey Generation

Privacy classification: synthetic/pseudonymous fixture where named learner examples use pseudonyms and anonymized/example inputs.

This document defines how Elementary School should generate a personalized **Phase 2 onboarding survey** from the completed **Phase 1 parent onboarding survey**.

The goal is to make onboarding adaptive from the beginning.

Phase 1 should classify the case shape.

Phase 2 should ask only the next useful questions needed to move a case from `Provisional` toward `Ready`, or to confirm that it should remain `Hold`.

## Core Logic

Use this sequence:

```text
phase 1 survey completed
  -> classify case shape
  -> identify missing authority / boundary / learner / rhythm / resource details
  -> generate only the follow-up questions needed for this case
  -> collect answers
  -> reclassify as Ready / Provisional / Hold
```

Phase 2 should not repeat the whole intake.

It should close gaps.

## What Phase 1 Decides

Phase 1 should help the operator or system identify:

- learner situation
- planning need
- schooling context
- learner-picture depth
- support level
- rhythm reality
- first-month avoid posture
- starter-app stance
- reading posture
- caution / outside-support posture

Those answers should route the next questions.

## What Phase 2 Should Gather

Phase 2 should gather only the missing items that block a safe draft:

- authority and drafting approval
- save / share boundaries
- current resources and curriculum
- concrete learner interests
- concrete proud-work examples
- concrete friction examples
- reading details when needed
- Khan Academy Kids decision details when needed
- outside-support context when needed
- portfolio setup details when needed
- schedule details when needed

## Routing Rules

### 1. Authority / Boundary Block

Include this block when any of these are missing:

- parent or guardian name
- contact info
- drafting approval
- who approves the plan before use
- what may not be saved
- what may not be shared

Recommended questions:

- Who should be the main parent or guardian contact for this plan?
- Do you approve drafting a first-month plan from the information you have already shared?
- Is there anything you do not want saved?
- Is there anything you do not want shared?

### 2. Learner Detail Block

Include this block when the learner picture is `B`, `C`, or `D`, or when concrete learner examples are still missing.

Recommended questions:

- What topics, activities, books, games, or projects does your child return to most often?
- What is your child proud of right now?
- What currently feels hard, frustrating, or often avoided?
- What kind of learning seems to work best: reading, talking, building, drawing, moving, watching, or playing?

### 3. Rhythm And Household Reality Block

Include this block when the rhythm is variable, moderate-but-unspecified, or likely to create planning guesswork.

Recommended questions:

- Which days are active learning days?
- What time of day usually works best?
- How much adult help is realistic on a lighter day?
- How much adult help is realistic on a fuller day?
- Do you want a fixed rhythm or a flexible menu?

### 4. Resource Block

Include this block when current books, curriculum, materials, or active tools are still unknown.

Recommended questions:

- What books are already in the house?
- Is there a curriculum or program already in use?
- What apps or websites are already being used?
- What materials are easy to use right now?

### 5. Khan Academy Kids Block

Include this block when Phase 1 answer 8 is `B` or `D`.

If answer 8 is `B` (`maybe`), ask:

- Is Khan Academy Kids installed already?
- What would you want help deciding about it?
- If you try it, what time limit feels safe?
- Should it stay inside a broader screen-time budget?

If answer 8 is `D` (`already using it`), ask:

- How much time is it currently used?
- What does your child choose or avoid inside the app?
- What would you want observed or adjusted?

Do not include this block when answer 8 is `C` unless the parent reopens the topic.

### 6. Reading Detail Block

Include this block when Phase 1 answer 9 is `B`, `C`, or `D`.

Recommended questions:

- What kinds of books does your child choose voluntarily?
- What kinds of books are resisted or abandoned?
- Does your child prefer fiction, nonfiction, graphic formats, jokes, field guides, poetry, or read-alouds?
- What does reading frustration look like when it shows up?

### 7. Caution / Outside-Support Block

Include this block when Phase 1 answer 10 is `C` or `D`.

If answer 10 is `C`, ask:

- What specific concern should be handled carefully?
- What usually triggers that concern?
- What kind of planning posture feels safest?

If answer 10 is `D`, ask:

- Are there teacher, tutor, clinician, specialist, or school notes you want considered?
- Do you want that outside-support context included in planning now?
- Is there anything that should stay outside the plan for now?

### 8. Portfolio Block

Include this block when a draft will likely be usable soon but evidence storage is still unclear.

Recommended questions:

- Where would you like work to be saved?
- Do you want a physical portfolio, digital folder, or both?
- Who decides what gets saved?
- Should your child choose proud work each week?

## Phase 2 Composition Rules

Build the survey from blocks, not from one fixed form.

Recommended composition:

- always include the Authority / Boundary Block if missing
- include 2-4 more blocks based on the Phase 1 answers
- keep the total Phase 2 survey compact enough to feel like a continuation, not a restart

Good target:

- 6 to 12 short questions total

## Abigail Example Routing

Abigail's Phase 1 answers imply:

- include Authority / Boundary Block
- include Learner Detail Block
- include Resource Block
- include Khan Academy Kids Block because the answer was `maybe`
- include Reading Detail Block because reading is mixed
- optionally include a light Rhythm Block only if time-of-day or learning-day details are still needed

Do not include a heavy Caution / Outside-Support Block yet, because no explicit high-stakes concern has been named; only ask whether outside-support context exists and may be considered.

## Reclassification Rule

After Phase 2 returns:

- mark `Ready` if authority, boundaries, learner detail, rhythm reality, starter-tool posture, and caution posture are now clear enough to draft without invention
- keep `Provisional` if the core picture is usable but still thin in a few non-blocking areas
- mark `Hold` if outside-support, privacy, authority, or major learner-context gaps still prevent a safe draft

## Boundary

Phase 2 is not:

- a full restart of intake
- a second generic registration form
- a diagnostic instrument
- a substitute for parent approval

It is a personalized gap-closing survey generated from the actual Phase 1 answers.
