# Phase 1 Claude Code Prompt — Artistic Director Studio Formation

Copy and paste everything inside the block below into Claude Code while the
terminal is opened at the root of the `OB1` repository.

```text
You are helping me create the starter workspace for my Artistic Director
studio inside this existing repository.

First, inspect the repository root and read README.md. Do not modify, delete,
rename, deploy, or reconfigure any existing Open Brain infrastructure. Do not
install packages, run database commands, create accounts, use API keys, or
connect to external services.

This phase is job-neutral. Do not mention or create anything for a live
project, client, campaign, customer, or commissioned assignment.

Create only these six Markdown files under a new `artistic-director/`
directory:

1. `artistic-director/README.md`
2. `artistic-director/role-and-boundaries.md`
3. `artistic-director/how-i-work-with-ai.md`
4. `artistic-director/ai-instructions.md`
5. `artistic-director/first-exercise.md`
6. `artistic-director/lessons.md`

Use clear headings and short prompts for me to complete. Do not invent my
artistic philosophy, preferences, biography, or experience. Wherever my own
judgment is needed, write a brief TODO question for me instead.

Populate the files as follows:

README.md
- Explain that this is an independent creative studio and AI-learning space.
- Explain that it is built on the existing repository but does not need to
  reproduce the repository's structure.
- Include TODO questions asking what I think the system does, what I want the
  studio to help me do, and what I am curious or uncertain about.
- Include a short section called "What I built" with TODO prompts.

role-and-boundaries.md
- Explain the general Artistic Director function without pretending to know my
  personal style.
- Include TODO prompts for what I want to learn, what I want AI to help with,
  and what must remain human judgment.
- State that the studio does not independently authorize outside contact,
  publication, delivery, spending, hiring, claims approval, rights clearance,
  access to someone else's private information, or commitments on someone
  else's behalf.

how-i-work-with-ai.md
- Include short TODO prompts for how I will give the AI an objective, how it
  should ask questions, how many alternatives it should produce, how I will
  critique it, and how I will decide whether a lesson is worth remembering.
- Include this collaboration loop:
  human objective -> AI questions and restatement -> distinct options -> human
  critique -> AI revision -> human accepts, rejects, or holds a lesson.

ai-instructions.md
- Write starter instructions telling the AI to explore before converging,
  generate materially different concepts, explain its reasoning, identify
  weak fit and cliché, flag uncertainty and rights risk, ask for human
  judgment, distinguish experiment from decision, and never treat a polished
  draft as approved for publication or delivery.
- Tell the AI to propose lessons for human review rather than silently changing
  its behavior.

first-exercise.md
- Add a heading called "Waiting for first exercise".
- Tell me to use a fictional or self-created subject and to paste in the
  separate calibration exercise when I am ready.
- Do not complete the exercise for me.

lessons.md
- Add three empty sections: Keep, Avoid, and Still unclear.
- Explain that these sections should be filled only after the first exercise.

After creating the files:

1. Show me a concise list of files created.
2. Show me any existing files you changed. The answer should be "none".
3. Do not commit, push, publish, or open a pull request unless I explicitly
   ask you to do that later.
4. Stop and wait for me to read the files.
```

After Claude Code finishes, read every new file and replace the TODO prompts
with your own words. Then complete the separate calibration exercise.

