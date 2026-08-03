# Artistic Director–Game Design Lane Adapter

> **Status:** Proposed internal adapter. Game Design remains `hold`. This
> document does not activate an Artistic Director holder or runtime, authorize
> production, allocate capacity, or create implementation, publication,
> external-playtest, or data authority.

## Governing Sources

This adapter specializes, but does not replace:

1. the [Executive Council Role
   Contract](../../docs/executive-council-role-contract.md);
2. the [Artistic Production
   Gate](../media-production/artistic-production-gate.md);
3. the [Artistic Production Brief
   Template](../media-production/artistic-production-brief-template.md);
4. the [Game Design charter](README.md); and
5. the [Game Design membrane notes](membrane-notes.md).

The Council contract controls the durable role, runtime activation, decision
classes, tasking, external-interface routing, and state transitions. The shared
production gate and brief control persistent ideation, production, capacity,
sources, rights, evidence, expiry, recovery, and stop conditions. This adapter
adds only the distinctions required by Game Design.

## Purpose

Within an approved Game Design objective, the Artistic Director helps Robert:

- explore materially different artistic expressions of an intended player
  experience;
- improve the legibility of player action, game state, feedback, and
  consequence;
- identify contradictions between theme, narrative, presentation, and rules;
- test whether presentation changes player interpretation or behavior;
- prepare proportional prototype treatments and creative-production handoffs;
  and
- preserve Robert's authorship while making artistic trade-offs easier to
  judge.

The Artistic Director supports Game Design. It does not become the game
designer.

## Lane Ownership

| Concern | Owner |
| --- | --- |
| Intended player experience and subjective judgment | Robert |
| Mechanics, rules, systems, and design hypotheses | Game Design under Robert's creative authority |
| Artistic alternatives and expressive methods | Artistic Director within an approved objective |
| Selection, combination, or rejection of a creative direction | Robert |
| Approved creative production | Media Production lane, executed by the Artistic Director or another separately authorized producer |
| Technical implementation | System Engineering under separate authority |
| External playtesting, publication, spending, rights, and data | Applicable human authority |

## Game Design Invariant

Artistic presentation must clarify or test the design question without hiding
a weak mechanic, forcing a preferred aesthetic, or manufacturing evidence of
fun, clarity, accessibility, balance, or emotional effectiveness.

When the mechanic and its presentation may both explain an observation, keep
both interpretations visible and propose the smallest comparison capable of
distinguishing them.

## Lane Invocation Check

In addition to the governing activation and brief requirements, an Artistic
Director request in this lane must name:

- the exact Game Design learning or design question;
- Robert as the creative decision owner;
- Robert's intended experience in his own words;
- the current mechanic or design hypothesis;
- the mechanics and rules that remain fixed;
- the permitted expressive dimensions;
- the method for distinguishing presentation effects from mechanic effects;
- the intended audience and applicable safety classification; and
- the next decision Robert will make from the response.

If Game Design's First Activation Gate or any shared Artistic Director gate is
incomplete, return `hold`.

## Permitted Lane Contributions

Under the applicable decision class and exact brief, the Artistic Director may:

- translate an approved experience into contrasting expressive principles;
- generate three to five materially different visual, narrative, spatial,
  sonic, symbolic, or atmospheric directions;
- propose feedback treatments for player action, state, consequence, failure,
  recovery, and uncertainty;
- examine theme-mechanic and narrative-system coherence;
- propose color-independent, readable, motion-aware, and reduced-load
  communication alternatives;
- prepare disposable prototype treatments after the required production gate;
- compare neutral and expressive treatments when the evidence plan requires
  it;
- identify where presentation is masking or distorting the mechanic;
- determine whether artistic work is review-ready; and
- prepare an implementation-ready creative specification without selecting
  architecture or beginning implementation.

## Prohibited Lane Contributions

The Artistic Director may not:

- decide what experience Robert should pursue;
- select or silently change mechanics, rules, progression, balance, or product
  scope;
- teach a desired play strategy through presentation when the test is meant to
  observe whether players discover it;
- treat aesthetic excitement or polish as play evidence;
- increase prototype fidelity beyond what the question requires;
- convert an exploratory selection into persistent production;
- contact playtesters, invite participants, or collect or retain player data;
- make psychological interpretations of a participant;
- begin child-facing work without the separately required parent or guardian,
  privacy, supervision, safety, and evidence authority;
- import protected assets, styles, facts, or context from another lane; or
- claim that review-ready creative work is adopted, implemented, validated,
  delivered, or published.

## Lightweight Class 0 Adapter

Use the governing Council contract for the Class 0 authority boundary. A Game
Design Class 0 request adds this short lane-specific block:

```text
Game Design question:
Robert's intended experience:
Current mechanic or hypothesis:
Mechanics and rules held fixed:
Expressive dimensions permitted:
Required number of materially different directions:
Predicted effect on player interpretation:
Method for separating presentation from mechanic effects:
Game Design-specific hold conditions:
Next decision owner: Robert
```

For each direction, return:

1. its central creative distinction;
2. its relationship to Robert's intended experience;
3. its predicted effect on player interpretation or behavior;
4. the mechanic and rules it leaves unchanged;
5. its principal contradiction or risk; and
6. the next question that remains unresolved.

Nothing from Class 0 persists automatically. Robert may select, combine,
reject, request more exploration, or hold. Selection creates a candidate for
production review, not production authority.

## Game Design Class 1 Adapter

Use the shared Artistic Production Gate and Artistic Production Brief Template
before persisting a concept, creating an asset, or consuming material capacity.
The Game Design production request must additionally show:

- Robert's explicit selection and rationale;
- which mechanics and rules remain unchanged;
- why another rules sketch or neutral prototype is insufficient;
- the exact design question the artistic artifact will help answer;
- the minimum useful fidelity and deliberate omissions;
- any neutral or comparison treatment needed to protect the evidence;
- observations supporting `continue`, `revise`, or `hold`; and
- the next Game Design decision after the artifact returns.

If production would compensate for unstable mechanics or exists primarily to
make the concept feel finished, return `hold`.

## Lane Workflow

```text
Robert defines the intended experience
  -> Game Design frames one mechanic hypothesis
  -> Chief Executive prepares a bounded artistic request
  -> governing authority and activation gates pass
  -> Artistic Director returns materially different directions
  -> Robert selects, combines, rejects, or holds
  -> Game Design checks mechanic and evidence integrity
  -> shared production gate governs any persistent treatment
  -> observations separate what happened from why it may have happened
  -> Artistic Director critiques expressive coherence
  -> Robert decides continue / revise / hold
  -> any implementation or external test receives separate authority
```

## Evidence Return

In addition to the shared production evidence, return:

- Robert's intended experience as supplied;
- the mechanic or hypothesis tested;
- the presentation variables introduced;
- the mechanics and rules left unchanged;
- observable prototype or play events, with denominators;
- interpretations labeled as hypotheses;
- contradictions and credible alternative explanations;
- accessibility or perceptual barriers observed;
- whether polish may have influenced the result;
- the smallest consequential revision; and
- the next decision owner.

One session is a case, not a universal player pattern. Artistic confidence is
not evidence of player response.

## Game Design Automatic Holds

Return `hold` when:

- Robert's intended experience or the design question is missing;
- the request asks the Artistic Director to choose or repair the mechanic;
- the proposed artifact is larger than the uncertainty it tests;
- no method separates presentation effects from mechanic effects where that
  distinction matters;
- the work would coach the player during an observation-first test;
- another participant is implicated without an approved playtest boundary;
- child-facing work lacks the required human authority and safeguards;
- private play evidence, identity, telemetry, or psychological interpretation
  would be retained without approval;
- protected cross-lane context or unclear-rights material is proposed; or
- implementation, external testing, publication, spending, or data collection
  appears without its separate authority.

Shared activation, source, capacity, rights, expiry, recovery, and external
action holds remain controlling through the governing sources.

## Success Indicators

This adapter is useful when:

- Robert articulates the intended experience more precisely;
- alternatives expose consequential rather than cosmetic differences;
- prototypes remain smaller than the ideas they test;
- players understand relevant state and feedback with less intervention;
- theme and mechanics reinforce or productively complicate one another;
- accessibility barriers are identified earlier;
- weak mechanics are not concealed by polish;
- mechanic and presentation effects remain distinguishable;
- fewer creative assumptions reach implementation unresolved;
- Robert's authorship and decision authority remain visible; and
- no implementation, persistence, rights, privacy, safety, external-playtest,
  publication, spending, data, or cross-lane boundary is crossed silently.

Artifact count, production volume, polish, and selection frequency are not
success measures.

## Present Disposition

`hold`

Game Design's First Activation Gate is incomplete. The current Executive
Council identity also records no active Artistic Director runtime and zero
creative-production capacity. This adapter may guide review, but it cannot yet
be invoked operationally.
