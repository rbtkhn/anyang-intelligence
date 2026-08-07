# JK Second_Brain Projects Relocation — Codex Prompt

Paste the following prompt into Codex from JK's `Second_Brain` repository.

```text
Reorganize the JK3303/Second_Brain branch `contrib/JK3303/video-game`.

Read the repository-root `AGENTS.md` first. Preserve unrelated work. If the
working tree has unrelated changes, stop and report them.

## Target structure

Move:

- `artistic-director/` -> `projects/artistic-director/`
- `recipes/ob1-games/` -> `projects/game-design/`

Use `git mv` so history remains traceable.

## Project index

Create `projects/README.md`.

Define `projects/` as active, owned work developed using Second_Brain and AI
systems—not as reusable recipes or upstream-endorsed contributions.

List:

| Project | Owner | State |
| --- | --- | --- |
| Artistic Director | JK | Active — internal |
| Game Design | JK | Prototype |

State that project inclusion does not authorize publication, deployment,
spending, external contact, client decisions, or company decisions.

Each project README must identify:

- owner;
- purpose;
- state;
- AI contribution;
- external-authority boundary;
- current entry point;
- next review.

Reusable work moves from `projects/` into `recipes/`, `skills/`, or another
shared OB1 surface only through a separate review.

## Artistic Director README

Replace `projects/artistic-director/README.md`.

Describe it as JK's human-led, AI-supported creative studio.

Explicitly state:

- JK is expected to use and master Codex, Claude, Cursor, and other generative
  systems.
- AI may support research, alternatives, critique, documentation, prototypes,
  and production.
- JK owns creative judgment, selection, rejection, correction, and reusable
  lessons.
- AI mastery is evidenced through JK's direction and resulting work, not
  through avoiding AI.
- Grace Gems is an internal creative exploration.
- “Your Stone, Your Story” is a leading hypothesis, not approved brand policy.
- Repository work does not authorize spending, Shopify setup, customer
  contact, rights-dependent use, publication, or deployment.

Retain a directory guide for `charter/`, `ai/`, `memory/`, `references/`,
`practice/`, `decisions/`, `evaluations/`, and `handoff/`.

Set the current entry point to `handoff/current-state.md`.

Do not alter the substantive Grace Gems artifacts in this task.

## Game Design README

Replace `projects/game-design/README.md`.

Describe it as JK's ongoing game-design workspace, with chess as its first
prototype.

Document:

```text
projects/game-design/
├── README.md
├── framework/
└── games/
    └── chess/
        ├── README.md
        ├── design/
        └── src/
```

State:

- AI may propose mechanics, implement code, test edge cases, and critique work.
- JK owns player-experience and game-design decisions.
- AI-generated code remains unverified until tested and played.
- Methods move into `framework/` only after proving useful across multiple
  games.
- Promotion into a reusable OB1 surface requires separate review.

Set the current entry point to `games/chess/README.md`.

## Metadata and links

In `projects/game-design/metadata.json`:

- change the category from `recipes` to `projects`;
- update the description to identify an active game-design project;
- preserve author, version, and applicable tags.

Update current path references:

- `artistic-director/` -> `projects/artistic-director/`
- `recipes/ob1-games/` -> `projects/game-design/`

Add a short `Projects` section to the root README linking to both projects.
Do not present them as upstream OB1 community contributions.

## Verify

Run:

```powershell
git status --short
git diff --check
git diff --stat
rg -n "artistic-director/|recipes/ob1-games"
```

Confirm both old directories are gone, both new directories exist, no files
were lost, and any remaining old-path references are intentional.

Do not install dependencies, change Grace Gems governance records, commit,
push, or merge.

Return a concise summary, verification results, and the suggested commit
message:

`Reorganize Artistic Director and game design under projects`
```
