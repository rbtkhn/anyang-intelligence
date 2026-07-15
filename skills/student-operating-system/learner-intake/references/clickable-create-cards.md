# Clickable Create Cards

Use these cards only for the Success–Friction–Bridge pilot inside `$learner-intake create`. They replace the open-ended Phase 2 and Phase 3 question lists; do not ask both sets.

All cards are single-select unless marked `multi-select` or `matrix`. Show no more than three at once. Keep the selected episode visible in a short, guardian-approved label. A click is an observation path, not a profile claim.

`None fit`, `Not observed`, `Uncertain`, and learner `Skip` are valid terminal answers. Never force the nearest category. Record `Missing`, branch to a bounded alternative set, or classify `Hold` when a required readiness fact remains unresolved.

## Native Clickable-Control Rendering

Use the session's genuine multiple-choice control when it is available. The native control may show at most three questions per batch and two or three mutually exclusive choices per question. Render the canonical cards into that shape without deleting, combining, recommending, or silently choosing any canonical answer.

- For a single-select card with more than three answers, preserve answer order and paginate it. Show the first two answers plus `More choices`; show up to three remaining answers on the final page. `More choices` is navigation only and records no observation. Keep terminal uncertainty or `None fit` answers on the final page.
- A native choice label may be shortened to five words or fewer only when its description displays the exact canonical answer. Record the canonical answer, never the shortened label.
- For `multi-select`, render each substantive candidate as a separate two-choice question: `Select` / `Do not select`. Ask no more than three candidates in one batch. After every candidate has an explicit response, roll the selected candidates up under the original card ID. When none are selected, record the card's canonical neutral answer such as `Nothing named`, `None yet`, or `Not observed`.
- When a multi-select has exclusive terminal answers, first render a gateway with those terminal answers and `Select specific signals`. The gateway is navigation only unless a terminal answer is selected. Expand candidates only after `Select specific signals`.
- For `matrix`, render each named dimension as its own suffixed subcard and apply the single-select or multi-select rule to that dimension. Roll all subcard responses up under the original card ID.
- Suffixes such as `R3-P1` or `R6-D` are interaction identifiers, not new intake questions. Never count navigation or a matrix subcard as additional evidence.
- If a required answer creates `Hold`, stop before rendering the next page or batch. If the genuine control is unavailable, state that exact limitation and show the same rendering as a text fallback; do not imitate clickable controls in Markdown.

### Canonical First Native Batch

Render the beginning of R1–R3 as follows. Resolve any `More choices` navigation before treating that card as answered.

| Native ID | Question | Native choices | Recorded value |
| --- | --- | --- | --- |
| R1-A | **At the end of this month, what would be most useful to understand?** | `Helps learner begin` / `Helps persist or return` / `More choices` | The exact corresponding R1 answer; `More choices` opens R1-B. |
| R1-B | **Which remaining direction fits best?** | `Learner connects ideas` / `Learner increasingly carries choices` / `Not clear yet` | The exact corresponding R1 answer shown in the choice description. |
| R2-A | **What would make the month worthwhile without an academic-level change?** | `Learner notices a helpful condition` / `Learner explains a connection` / `More choices` | The exact corresponding R2 answer shown in the choice description; `More choices` opens R2-B. |
| R2-B | **Which remaining worthwhile outcome fits best?** | `Learner chooses next move` / `Household finds sustainable rhythm` / `Not clear yet` | The exact corresponding R2 answer shown in the choice description. |
| R3-P1 | **Protect a working routine?** | `Select` / `Do not select` | Candidate for R3 Protect. |
| R3-P2 | **Protect a recurring interest or project?** | `Select` / `Do not select` | Candidate for R3 Protect. |
| R3-P3 | **Protect a supportive relationship?** | `Select` / `Do not select` | Candidate for R3 Protect. |
| R3-P4 | **Protect unstructured recovery time?** | `Select` / `Do not select` | Candidate for R3 Protect. |
| R3-A1 | **Avoid public correction or comparison?** | `Select` / `Do not select` | Candidate for R3 Avoid. |
| R3-A2 | **Avoid rigid daily quotas?** | `Select` / `Do not select` | Candidate for R3 Avoid. |
| R3-A3 | **Avoid excessive observation?** | `Select` / `Do not select` | Candidate for R3 Avoid. |
| R3-A4 | **Avoid new tools or apps?** | `Select` / `Do not select` | Candidate for R3 Avoid. |

The first native control call contains R1-A, R2-A, and R3-P1. Subsequent calls resolve navigation and the remaining R3 candidates in batches of no more than three. If all R3 Protect or Avoid candidates are declined, record the corresponding `Nothing named` answer.

## Phase 2A: Readiness Cards

Ask all eleven cards. Each should take less than one minute; stop when a response creates `Hold`.

| Card | Clickable decision | Answers | Destination or consequence |
| --- | --- | --- | --- |
| R1 | **At the end of this month, what would be most useful to understand?** | `What helps the learner begin` / `What helps the learner persist or return` / `How the learner connects ideas` / `Which choices the learner can increasingly carry` / `Not clear yet` | Parent direction. `Not clear yet` leaves required direction unresolved. |
| R2 | **What would make the month worthwhile without an academic-level change?** | `The learner notices a helpful condition` / `The learner makes or explains a connection` / `The learner chooses a meaningful next move` / `The household finds a sustainable rhythm` / `Not clear yet` | Useful outcome; month-end success. |
| R3 | **What must this cycle protect or avoid?** `multi-select matrix` | Protect: `A working routine` / `A recurring interest or project` / `A supportive relationship` / `Unstructured recovery time` / `Nothing named`. Avoid: `Public correction or comparison` / `Rigid daily quotas` / `Excessive observation` / `New tools or apps` / `Nothing named` | What already works; explicit avoidances. |
| R4 | **Where is learning already visible, and has an idea crossed contexts recently?** `multi-select matrix` | Contexts: `Books or formal study` / `Making, play, or projects` / `Conversation or relationships` / `Outdoors, travel, or daily life` / `Not observed`. Connection: `Yes, directly observed` / `Possibly` / `No recent example` | Current contexts; cross-context signal; evidence quality. |
| R5 | **Which choices can the learner carry now, and where is adult structure still needed?** `multi-select matrix` | Learner may choose: `Question or topic` / `Method or medium` / `Meaningful artifact` / `Possible next step` / `None yet`. Adult still structures: `Starting point` / `Pace or duration` / `Materials or tools` / `Recovery after friction` / `Most of the activity` | Learner agency; adult structure. |
| R6 | **Which household rhythm is genuinely sustainable?** `matrix` | Difficult day: `Pause` / `5–10 minutes` / `10–20 minutes` / `More than 20 minutes` / `Uncertain`. Ordinary day: `10–20 minutes` / `20–40 minutes` / `40–60 minutes` / `More than 60 minutes` / `Uncertain`. Shape: `Flexible menu` / `Fixed rhythm` / `Small anchor plus flexible choices` / `Undecided` | Minimum viable and ordinary rhythm. Required uncertainty may produce `Hold`. |
| R7 | **Which operating boundaries should control the first cycle?** `matrix` | Parent preparation: `None beyond review` / `Up to 5 minutes a day` / `Up to 15 minutes a day` / `One weekly setup` / `Uncertain`. Screen rule: `No learning apps` / `Inside an existing limit` / `Separate parent-approved limit` / `Undecided`. Pivot signal `multi-select`: `Fatigue` / `Repeated confusion` / `Visible distress` / `Loss of meaning` / `Parent overload` / `Ordinary pause rules only` / `Not clear yet` | Preparation, screen, shorten/pivot/pause boundaries. `Not clear yet` produces `Hold`. An undecided screen rule produces `Hold` when any app remains approved or undecided. |
| R8 | **Which resources are already easy to use?** `multi-select` | `Books or paper` / `Art or building materials` / `Household or outdoor materials` / `Existing curriculum or project` / `None named` | Current resources; first-week feasibility. |
| R9 | **What is the stance on each optional planning component?** `matrix` | Khan Academy Kids: `Approved` / `Declined` / `Undecided`. Reading basket: `Useful now` / `Optional` / `Declined` / `Undecided`. Detailed daily plans: `Helpful` / `Burdensome` / `Unnecessary` / `Undecided` | Approved, excluded, and undecided tools. Undecided never becomes assumed approval. |
| R10 | **Which evidence boundary would be useful without becoming paperwork?** | `Learner item + parent observation + open question` / `Learner-selected item only` / `Concise parent observation only` / `No preservation beyond live review` / `Not clear yet` | Useful evidence and excessive-capture boundary. `Not clear yet` produces `Hold`; deletion authority remains canonical in Phase 1. |
| R11 | **Is the minimum caution and outside-support boundary clear enough to proceed?** | `No special context; ordinary pause rules apply` / `Context exists and only its approved planning implication may be used` / `Context exists but its planning implication is unclear` / `Prefer not to decide now` | The last two answers produce `Hold`. The second answer triggers R11A. Do not request diagnoses or private histories. |

### Readiness Follow-up

Ask only when triggered; it is not an episode card.

| Card | Trigger | Clickable decision | Answers | Consequence |
| --- | --- | --- | --- | --- |
| R11A | R11 confirms relevant context exists | **What is the minimum approved planning implication?** | `Reduce duration, demand, or stimulation` / `Exclude the affected activity, tool, or topic` / `Pause affected use pending outside-support review` / `Do not use this context in planning` / `The approved implication is not represented` | Preserve only the selected implication. The final answer produces `Hold`; do not collect the underlying history. |

## Phase 2B: Six Core Episode Cards

Ask all six. First choose one recent success scene and one recent friction scene. Keep each scene bound to one time window and context; do not blend several episodes.

| Card | Clickable question | Answers | Profile mapping |
| --- | --- | --- | --- |
| E1 | **During the past 30 days, which scene most clearly showed the learner doing more than merely finishing?** | `Changed an approach after something failed` / `Explained an unexpected connection` / `Pursued a self-chosen question beyond the request` / `Made something and tested whether it worked` / `None fit or not observed` | Positive episode; interest; observed strength. |
| E2 | **What most clearly pulled the learner into that success scene?** | `A visible goal with immediate feedback` / `Meaningful choice of route or medium` / `A surprising question or detail` / `Support from someone who did not take over` / `Uncertain` | Helpful condition; episode spark. |
| E3 | **What is the strongest evidence that understanding changed?** | `The learner explained why something worked` / `A later attempt used a better strategy` / `The idea appeared in another context` / `The learner taught, demonstrated, or defended it` / `Only completion—or no reliable evidence—was visible` | Evidence quality; contextual strength; possible transfer. |
| E4 | **During one recent friction scene, where did the learner's energy first change?** | `The starting point was unclear` / `Instructions or demands expanded` / `A mistake became visible or comparative` / `Method, pace, or purpose became fixed` / `None fit or not observed` | Friction episode; immediate context. |
| E5 | **What happened immediately after that turning point?** | `The learner asked what the task meant or required` / `The learner repeated one move without new information` / `The learner redirected attention or changed activities` / `The learner withdrew, protested, or stopped` / `Not observed` | Friction response; pause signal; support need. |
| E6 | **Which contrast is best supported by these two scenes?** | The operator renders up to three episode-specific contrasts plus `Another context may explain more` and `The evidence is too thin`. | Working hypothesis or `Open Question`; uncertainty and counterevidence. The operator, not the parent, constructs the candidate contrasts. |

### Episode Anchor

After E1 and E4, show a compact confirmation card generated from the selected path:

```text
Use this as the episode we mean?
[selected scene] + [past 7 days / past 30 days] + [home / formal study / project-play / outdoors-daily life]

Yes / Choose a different listed scene / Not enough detail to use
```

This is a confirmation of the same card, not an additional question. `Not enough detail to use` records `Missing`; it never invites an unrestricted learner history.

## Phase 2C: Conditional Cards

Ask only when the trigger applies.

| Card | Trigger | Clickable question and answers | Profile mapping |
| --- | --- | --- | --- |
| X1 | E1 identifies a scene with a visible first move | **Before an adult supplied a method, what did the learner do first?** `Inspected or compared` / `Built, drew, wrote, or tested` / `Asked a narrowing question` / `Explained a possible approach` / `Waited for a first step` | Initiation; agency; adult structure. |
| X2 | The success scene contains an obstacle | **What happened after the first obstacle?** `Changed one part and tried again` / `Asked for a clue while keeping ownership` / `Paused and returned` / `Repeated or handed ownership away` / `Not observed` | Strategy; recovery; counterevidence. |
| X3 | An adult tried to help during friction | **Which response changed the scene most?** `Clarified the endpoint` / `Reduced it to one visible next move` / `Offered meaningful choices` / `Modeled, paused, or returned ownership` / `Nothing clearly helped` | Helpful condition; adult support; counterevidence. |
| X4 | E3 indicates transfer or R4 indicates a possible connection | **What kind of connection was visible?** `Same mechanism in a new setting` / `Earlier knowledge changed a new attempt` / `The learner explained an analogy` / `The learner returned to the idea independently` / `Too uncertain to preserve` | Cross-context connection; evidence quality. |

## Phase 3: Three Learner Cards

Use only after the named guardian approves the exact rendered cards. Refer to the guardian-approved episode labels, ask the learner first, and allow `Skip` without explanation. Show no more than four substantive choices plus `None fit` and `Skip`.

| Card | Clickable question | Answers | Profile mapping |
| --- | --- | --- | --- |
| L1 | **In the moment that went well, what made you want to keep going?** | `I wanted to know what would happen` / `I could make or change something` / `I could choose how to do it` / `I could see myself getting closer` / `None fit` / `Skip` | Learner voice; helpful condition; disagreement. |
| L2 | **In the difficult moment, what got in your way first?** | `I could not see how to begin` / `I did not know why it mattered` / `There were too many things to hold at once` / `The method did not make sense to me` / `None fit` / `Skip` | Learner voice; friction signal; open question. |
| L3 | **For a similar challenge, which bridge would you most like to try?** | The operator renders the four most relevant bounded bridges from approved evidence, such as a visible goal, one clear first move, an example, a choice of medium, a pause, or support without takeover; then adds `None fit` and `Skip`. | Learner-selected bridge; next-signal candidate. |

If `None fit` is selected, rerender that same card once with up to four different guardian-approved choices. If none fit again, preserve `Missing`; do not add a fourth learner question.

## Output Rules

- Preserve selections first as observations, not adjectives.
- Keep parent interpretation, learner voice, operator hypothesis, and counterevidence separate.
- Map each selection only to the destinations named above.
- Treat E6 as a hypothesis decision surface, not a causal finding.
- Use `strong / medium / thin / none` for evidence quality.
- A learner response may disagree with the parent without reducing readiness.
- Do not propose a profile after `Hold`.
- An experiment remains a candidate until an effective profile, separate drafting authorization, and plan-use approval exist.
