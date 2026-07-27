# Phase 1 Onboarding Instructions — Artistic Director Studio Formation

**Recipient:** JK3303  
**Repository:** `https://github.com/JK3303/OB1`  
**Phase:** 1 — create your Artistic Director studio  
**Important:** This phase is job-neutral. Do not work on live external projects
or commissioned campaigns yet.

## Fastest way to begin

From the root of the repository, copy and paste the complete prompt in
[Phase 1 Claude Code Prompt](artistic-director-phase-1-claude-code-prompt.md)
into Claude Code. Let Claude Code create the small starter overlay, then read
and personalize each file yourself.

## What you are building

You already have an OB1 repository. OB1 is a technical foundation for working
with AI and memory. Your first assignment is to add a small Artistic Director
studio on top of it.

This is a place for you and an AI to learn how to work together creatively. You
do not need to understand all of OB1 before beginning, and you do not need to
make finished work yet.

## Safety rules

Your repository is public. Do not put any of the following in it:

- passwords, API keys, tokens, or credential spreadsheets;
- private information about other people;
- project-specific information or assets supplied by someone else;
- private conversations, financial information, or account details; or
- unlicensed images, music, fonts, or other protected material.

The GitHub repository and any external OB1 database are separate. Protect both.
Do not connect another person or AI to your entire personal memory database
without an explicit, limited access decision.

## Step 1 — Look around OB1

Read the existing `README.md`. You do not need to understand every technical
detail yet.

Create `artistic-director/README.md` and answer three questions:

1. What do you think OB1 does?
2. What do you want an Artistic Director studio to help you do?
3. What are you most curious or uncertain about?

Do not change the existing Open Brain setup yet.

## Step 2 — Create the small starter overlay

Create only this structure for now:

```text
artistic-director/
├── README.md
├── role-and-boundaries.md
├── how-i-work-with-ai.md
├── ai-instructions.md
├── first-exercise.md
└── lessons.md
```

This is deliberately small. Do not create a larger memory, reference,
evaluation, or handoff system until you have completed the first exercise and
know what you actually need.

## Step 3 — Describe the role and boundaries

In `role-and-boundaries.md`, write your own understanding of the Artistic
Director role. Include:

- what you believe an Artistic Director is responsible for;
- what you want to learn and become good at;
- what you want the AI to help you do;
- what must remain your human judgment; and
- what the role should never pretend to authorize or approve.

Also record that this studio does not independently authorize:

- contacting customers or other outside parties;
- publishing or delivering work externally;
- spending money or hiring people;
- approving claims or clearing rights;
- accessing private information supplied by someone else; or
- making commitments or granting permissions on someone else's behalf.

## Step 4 — Describe how you want to work with AI

In `how-i-work-with-ai.md`, answer in plain language:

- how you will give the AI an objective;
- how the AI should ask questions;
- how many alternatives it should produce;
- how you will critique its work;
- how it should respond to disagreement; and
- how you will decide whether a lesson is worth remembering.

In `ai-instructions.md`, tell the AI to:

- help you explore rather than rush to one answer;
- generate materially different concepts;
- explain its creative reasoning;
- identify weak fit, cliché, uncertainty, factual risk, and rights risk;
- ask for your judgment when taste is unresolved;
- distinguish an experiment from a decision;
- never treat a polished draft as approved for publication or delivery; and
- propose lessons for your review instead of silently changing its behavior.

Use this simple collaboration loop:

```text
human objective
  -> AI asks questions and restates the brief
  -> AI generates distinct options
  -> human critiques the options
  -> AI revises and explains the changes
  -> human accepts, rejects, or holds a lesson
```

You do not need to write a perfect AI instruction file. Write a useful first
version and improve it after the exercise.

## Step 5 — Complete one harmless first exercise

Choose a public or self-created subject unrelated to any live external project
or commissioned assignment. Examples include:

- a local place;
- a favorite book or film;
- a personal hobby;
- a fictional product;
- a historical idea; or
- an abstract theme such as calm, motion, trust, or abundance.

Ask the AI for three materially different creative directions for that subject.
Write the request, the three outputs, and your response in
`first-exercise.md`. Then:

Use the complete [Phase 1 Calibration Exercise](artistic-director-phase-1-calibration-exercise.md)
for the prompt and exercise steps.

1. choose what works and what does not;
2. explain your critique in plain language;
3. ask the AI to revise one direction;
4. record one lesson you want the AI to remember in `lessons.md`;
5. record one thing you do not want it to repeat in `lessons.md`; and
6. record what the AI still misunderstood in `lessons.md`.

Do not worry about producing impressive final art. Clear critique is more
valuable than polish at this stage.

## Step 6 — Finish the README

Add a short final section to `README.md` recording:

- what you built;
- which AI tool you used;
- what the AI understands better now;
- what it still misunderstands;
- what you want to try next; and
- what help you need.

## Phase 1 completion evidence

Send the designated observer:

1. the repository link;
2. the commit or pull request containing the overlay;
3. the link to `first-exercise.md`;
4. the link to `lessons.md`; and
5. a short note answering: “What did you learn about working with AI?”

The designated observer will review the repository read-only. Observation is
for understanding your development and identifying useful patterns. It is not
a request to edit your studio, take ownership of it, or silently turn your
work into someone else's permanent rules.

## Completion gate

Phase 1 is complete when you can explain:

- the difference between a prompt, a memory entry, a creative decision, and a
  permission;
- what information is safe to place in a public repository;
- how to ask the AI for distinct creative options;
- how to critique and revise an AI output;
- how a lesson becomes accepted, rejected, or held; and
- when you must stop and ask for human permission.

Do not begin live external or commissioned work until this small starter phase
has been reviewed. The larger studio structure can be designed afterward.
