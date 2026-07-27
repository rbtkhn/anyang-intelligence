# Artistic Director Folder Specification for OB1

**Status:** Phase 1 design specification  
**Purpose:** Define the minimum viable `artistic-director/` folder that a human Artistic Director may create inside the existing OB1 repository as an independent creative studio and AI-training environment.

## Design decision

The human Artistic Director's `artistic-director/` folder is a seed-grown
studio inside the existing OB1 repository. OB1 remains the single GitHub
repository. The folder develops according to the holder's judgment, taste,
experiments, and working method.

The folder is not required to remain in exact sync with any other Artistic
Director specification or organizational memory surface. It may diverge
creatively within OB1. Only selected, approved material crosses from the folder
into a governed project or organizational memory surface.

## OB1 repository ownership and access

The intended arrangement is the existing OB1 repository with the
`artistic-director/` folder added inside it. No second repository is required.
The folder is the holder's independent creative studio and AI-training
environment within the shared repository.

The applicable engagement agreement must separately define confidentiality,
approved-output rights, backup or export, departure handling, and successor
access. Folder write access must not create access to private client systems
or client authority. The right to observe or selectively adopt approved work
must be stated separately from ownership of the holder's creative contributions.

Minimum access model:

- Artistic Director: write, organize, and evolve `artistic-director/`.
- Chief Executive: read-only observation and bounded review of the folder,
  subject to the repository's access model.
- System Engineer: governs consequential activation and access decisions; does
  not automatically receive control of the holder's creative work.
- AI runtime: only the explicitly approved folder paths and tools under the
  holder's operating arrangement.
- Client: no repository access unless separately approved.

Read access does not create tasking, approval, publication, spending, or
client authority.

## Phase 1 must be job-neutral

Phase 1 establishes the studio and the human-AI working relationship. It must
not preload Grace Gems strategy, client-specific facts, campaign requirements,
private evidence, or assumptions about the first commercial assignment.

The role-level seed may include the Artistic Director's general purpose,
creative responsibility, authority boundaries, review states, and memory rules.
Everything else should be discovered or chosen by the human during studio
formation.

## Minimum repository structure

```text
artistic-director/
├── README.md
├── charter/
│   ├── role-charter.md
│   ├── working-agreement.md
│   └── boundaries.md
├── ai-system/
│   ├── agent-instructions.md
│   ├── collaboration-protocol.md
│   ├── critique-rubric.md
│   ├── evaluation-set.md
│   └── change-log.md
├── creative-memory/
│   ├── principles.md
│   ├── vocabulary.md
│   ├── accepted-lessons.md
│   ├── rejected-lessons.md
│   └── open-questions.md
├── references/
│   ├── reference-log.md
│   ├── rights-notes.md
│   └── safe-generic-lessons.md
├── briefs/
│   ├── practice/
│   └── approved-work/
├── studio/
│   ├── experiments/
│   ├── concepts/
│   ├── prototypes/
│   └── production/
├── decisions/
│   ├── creative-decisions.md
│   ├── holds-and-rejections.md
│   └── review-receipts.md
├── evaluations/
│   ├── human-reviews/
│   ├── ai-reviews/
│   └── cohort-reviews/
├── handoff/
│   ├── current-state.md
│   ├── successor-guide.md
│   └── exit-record.md
└── .gitignore
```

The human may rename or extend this structure after the initial setup. The
minimum requirement is that creative work, AI instructions, decisions,
references, evaluations, and handoff material remain distinguishable within
the OB1 repository.

## Required Phase 1 files

### `README.md`

Must explain:

- who the Artistic Director is;
- what this folder is for;
- that the folder is an independent studio and training surface within OB1;
- how the Chief Executive observes it;
- where creative work begins and where approved work ends; and
- where to find the boundaries, AI instructions, and handoff guide.

### `charter/role-charter.md`

Must begin from the governed Artistic Director role, while allowing the human
to add a personal artistic philosophy. It must distinguish:

- role-level responsibilities;
- holder-specific preferences;
- AI-assistance responsibilities; and
- decisions reserved to Anyang Intelligence, the Chief Executive, the System
  Engineer, or a client owner.

### `charter/boundaries.md`

Must state that the studio repository does not independently authorize:

- client contact or client tasking;
- publication or external delivery;
- spending, hiring, contracting, or payment;
- rights clearance or claims approval;
- access to raw private client data; or
- changes to the Executive Council authority model.

### `ai-system/agent-instructions.md`

Must define the AI agent's role, tone, creative responsibilities, refusal
conditions, review states, memory rules, and escalation behavior. It should
explicitly say that human teaching is evidence for learning, not automatic
permission to act.

### `ai-system/critique-rubric.md`

Must provide a repeatable way to assess work for creative quality, strategic
fit, clarity, originality, audience usefulness, factual discipline, rights
risk, reuse value, and cleanup burden.

### `handoff/current-state.md`

Must explain the current AI behavior, active experiments, durable lessons,
known weaknesses, unresolved questions, and next calibration exercises.

## Memory model

The repository must keep four kinds of memory separate:

1. **Role memory:** approved responsibilities and constraints that survive a
   holder change.
2. **Holder memory:** the current human's taste, preferences, methods, and
   judgments, clearly attributed to that person.
3. **AI working memory:** prompts, examples, evaluations, and behavior changes
   used to improve the agent.
4. **Project memory:** client or campaign-specific facts, decisions, and
   artifacts that remain inside their governing project boundary.

No private client fact becomes general creative memory merely because it
influenced an idea. Record only a safe generic lesson unless the governing
owner approves broader reuse.

## Chief Executive observation protocol

The Chief Executive may observe the `artistic-director/` folder to understand:

- how the human is developing the Artistic Director practice;
- what the AI is learning and where it remains weak;
- which creative principles appear reusable;
- what work is blocked, risky, or ready for review; and
- what should be considered for selective adoption by Anyang Intelligence.

Observation should occur through read-only access, review notes, and bounded
briefs. The Chief Executive should not silently edit the folder, convert
observations into task authority, or treat a polished artifact as approved for
client use.

## Import boundary

Material may move from the folder into a governed project or organizational
memory surface only through an explicit selection decision. The import record
should identify:

- source path and author;
- whether the item is a deliverable, generic principle, or experiment;
- rights and privacy status;
- destination and permitted use;
- approving authority;
- required attribution; and
- any restrictions or expiry.

No automatic mirror, synchronization job, or broad copy of the folder is
required.

## Phase 1 completion gate

Phase 1 is complete when:

- the `artistic-director/` folder exists inside OB1 and access is verified;
- the minimum structure exists;
- the human has written or accepted the role charter and boundaries;
- the AI instructions and critique rubric exist;
- a harmless practice exercise has been completed;
- the Chief Executive can observe without write access;
- no client-private material has been loaded; and
- the human has identified the first calibration questions for the AI.

Completion of Phase 1 does not activate client production or require the human
to adopt any other repository's internal file structure. It establishes the
independent studio folder from which Phase 2 may begin.

## Succession rule

The human may leave, pause, or be replaced without destroying the durable
Artistic Director position. On succession, preserve attributable history,
separate holder-specific preferences from role memory, revoke the outgoing
holder's active access, and run a successor calibration before consequential
work resumes.
