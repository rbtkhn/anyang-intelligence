# Systems Design

Use this reference inside `game-design` when two or more mechanics interact
over persistent state, or when emergence, balance, economies, social networks,
institutions, populations, or simulation granularity are central. Do not load
it for a self-contained rule unless interaction effects are the question.

Systems reasoning advises Game Design. It does not select the intended player
experience, authorize implementation, or establish that predicted dynamics
will occur in play.

## Contents

- Establish the boundary
- Build a causal model
- Map spatial topology when needed
- Predict dynamics and failure
- Test at the lowest useful fidelity
- Historical living-world examples
- Return to Game Design

## Establish The Boundary

Name:

- the intended player experience in Robert's words;
- one bounded system question;
- actors and their available information;
- state and resources that persist;
- rules that change that state;
- the relevant time horizon;
- what is deliberately omitted; and
- the evidence that could change the design.

If the intended experience is missing, return to Game Design before optimizing
the system. If the boundary cannot be stated, reduce the question.

## Build A Causal Model

Represent only what is needed to answer the question:

- `stock`: something accumulated or depleted;
- `flow`: a rate that changes a stock;
- `state transition`: a rule moving an actor or object between conditions;
- `incentive`: a consequence that may change behavior;
- `delay`: time between cause and visible effect;
- `threshold`: a point where behavior or rules change;
- `network effect`: value or pressure that depends on relationships;
- `path dependence`: an early event constraining later possibilities.

Draw signed links where useful: `A --(+)-> B` means A tends to increase B;
`A --(-)-> B` means A tends to decrease B. Mark delayed effects. A closed chain
that amplifies change is reinforcing; one that resists change is balancing.
Treat the diagram as a hypothesis, not proof.

## Map Spatial Topology When Needed

When location or routing materially affects outcomes, map the relevant nodes
and directed connections before relying on causal loops alone. For each
connection, record capacity, travel time, control, alternatives, failure
points, and the information available to moving actors. For each node, record
the consequential conditions, such as safety, reception capacity, legal
status, material opportunity, cultural familiarity, and existing
relationships.

When actors are autonomous people, include their reasons, social ties, and
ability to refuse or reroute. Do not load spatial topology when location and
routing do not materially affect the question.

## Predict Dynamics And Failure

Trace rules through information and incentives into repeated behavior. Review:

- dominant strategies and choices that become non-decisions;
- runaway advantage, collapse, or self-reinforcing exclusion;
- stalled states and missing recovery paths;
- brittle dependencies and single points of failure;
- unequal agency between roles;
- incoherent incentives that oppose the intended experience;
- consequences that exist but remain illegible to the player;
- sensitivity to starting conditions and parameter changes; and
- behavior lost when individuals are aggregated or simulated less often.

Express the system hypothesis as:

```text
If <rules> interact under <constraints>,
then actors may <repeated behavior>,
producing <emergent dynamic>,
which may create <intended experience>,
unless <credible counterdynamic>.
```

## Test At The Lowest Useful Fidelity

Prefer, in order: manual turns, a decision table, a paper loop, a spreadsheet,
a text simulation, then code. Choose the first form that can reveal the target
interaction. State the question, prediction, omissions, revision threshold,
and authority boundary before running it.

Separate evidence states:

- `hypothesis`: predicted from the rules;
- `prototype observation`: occurred in a bounded model or simulation;
- `playtest pattern`: occurred in player behavior with its denominator;
- `candidate lesson`: a possible revision not yet retained.

Simulation output does not establish player understanding, emotion, or fun.

## Historical Living-World Examples

`example` - Commitments may increase reputation, reputation may improve access
to authority, and authority may create more commitments. This reinforcing loop
could produce meaningful entanglement or an unbeatable incumbent. Obligations,
succession, coalitions, or reputational fragility are possible counterforces,
not automatic solutions.

`example` - A cultural practice may persist through carriers, institutions,
teaching, and repetition while friction and entropy weaken transmission.
Prestige may reinforce adoption; migration or generational delay may create
mutation or loss. This illustrates a model and does not establish Robert's
permanent preference or historical truth.

## Return To Game Design

Return the causal model, predicted dynamics, strongest failure risk, smallest
test, and remaining uncertainty. Game Design decides whether the modeled
behavior serves the intended experience and whether to continue, revise, or
hold. Technical implementation remains a separate System Engineering action.
