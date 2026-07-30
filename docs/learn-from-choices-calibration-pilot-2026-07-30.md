# Learn From Choices Calibration Pilot

Status: `Conditional lifecycle — see Activation state`

Pilot reference: `LFC-CAL-2026-07-30-01`

Specification version: `LFC-CAL-v1.0`

Period: `2026-07-30` through `2026-08-05`, America/Denver

## Activation state

- Before the exact contract is committed: `Hold — repository persistence
  pending`.
- After the exact contract is committed but before `2026-07-30`,
  America/Denver: `Approved for pilot — activation scheduled`.
- From `2026-07-30` through `2026-08-05`, America/Denver: `Active — Phase 1
  calibration`.
- After the observation window without an explicit disposition:
  `Awaiting disposition — recommendation ordering remains frozen`.

No prose status or elapsed clock overrides missing repository persistence.

Boundary: internal `anyang-internal / anyang-intelligence / repository`
possibility navigation only. This pilot grants no customer, external-action,
execution, spending, publication, communication, commit, push, deployment, or
authority-expansion permission.

## Lead judgment

Activate seven days of prospective calibration because the private ledger and
semantic verifier are healthy, while outcome evidence remains too sparse to
change recommendation ordering. During this phase, capture objective evidence
with minimal interruption and keep outcome-informed recommendation learning
frozen.

## Authorization and lineage

- Design selection:
  `CHOICE-20260729-DESIGN-CHOICE-EXPERIMENT-001`.
- Read-only readiness preflight:
  `CHOICE-20260729-PREFLIGHT-CHOICE-PILOT-001`.
- Exact calibration execution selection:
  `CHOICE-20260729-EXECUTE-CHOICE-CALIBRATION-001`.
- Authority effect of every selection: `none`.
- Human owner and decision owner: Anyang operator.
- Recording steward: Council Steward.
- Pilot route: `manual workflow`.
- Automation involved: `no`.
- External action or deployment authorization: `no`.

The execution selection authorizes only the exact internal calibration scope in
this version. It does not approve a later version, another tenant or lane, an
automated schedule, or an outcome-informed recommendation change.

## Baseline

The read-only preflight snapshot recorded:

- 17 selected branches;
- 5 observed outcomes;
- 12 unresolved choices;
- 17 of 17 semantic and integrity verifications passed;
- 5 of 5 observed outcomes had evidence references;
- 0 cognitive-load observations;
- 3 advanced-momentum observations;
- 3 confirmed-known-path observations;
- 0 new-useful-path observations;
- 0 authority incidents;
- 0 membrane incidents;
- 0 comparable cohorts at the three-outcome learning floor.

Closing the preflight outcome and selecting activation changed the starting
ledger counts to 18 selections, 6 outcomes, and 12 unresolved choices. These
counts are activity and coverage context, not evidence that navigation works.

## Exact pilot question

Can seven days of prospective Learn From Choices calibration produce reliable,
scoped outcome evidence with low operator burden while recommendation ordering
remains independent of pilot outcomes and selection frequency?

## Approved tools, paths, and data

Permitted tools and surfaces:

- the existing `learn-from-choices` response contract;
- the existing `anyang-ops choice` CLI;
- the private Anyang SQLite ledger at its configured external path;
- `coffee` for at most one lightweight outcome-review branch per five resolved
  selections;
- this repository contract and derived, sanitized review output.

Permitted data:

- stable choice and option keys;
- semantic option roles;
- bounded decision, success, and risk summaries;
- outcome enums;
- timestamps, event hashes, and evidence references;
- bounded observations that pass the repository privacy policy.

Prohibited data:

- raw private evidence bodies;
- customer-private or cross-tenant content;
- credentials, private contact details, payment identifiers, or restricted
  locations;
- inferred cognitive states represented as observations.

Git stores this reusable contract. The private SQLite ledger remains canonical
for selections and outcomes.

## Run limit and cadence

- Duration: seven calendar days.
- Population: branches selected prospectively in the declared scope.
- Minimum run count: none; sparse activity remains honest evidence.
- Maximum follow-up: one optional `coffee` outcome-review branch per five
  resolved selections.
- No recurring automation, notification, background job, or external message.
- Review gate: end of day `2026-08-05`, America/Denver.

At expiry, stop the calibration phase. Do not silently extend it.
Outcome-informed recommendation ordering remains frozen until an explicit
review disposition authorizes a later state.

## Calibration behavior

During the pilot:

1. Continue presenting three or four meaningful possibilities.
2. Preserve recommended, alternative, overlooked, and pause-or-deepen roles
   when all are credible.
3. Explain recommendations from current task evidence and controlling
   doctrine.
4. Treat all pilot outcome patterns as diagnostic only.
5. Do not reorder, favor, or demote options using pilot outcomes, even if a
   three-outcome pattern appears.
6. Never use selection frequency as learning evidence.
7. Add `LFC-CAL-2026-07-30-01` to `learning_refs` for every selection in the
   exact pilot scope and observation window.
8. Exclude an untagged selection from the pilot cohort and disclose the
   tagging gap.
9. Record only selected branches.
10. Derive objective outcomes from receipts when possible.
11. Leave cognitive load, momentum, discovery, or rework as `Missing` when not
   observed.
12. Use `coffee` as the only unresolved-outcome follow-up route.
13. Preserve the separate authority boundary for every consequential action.

Authority, privacy, safety, or membrane incidents remain immediate guardrails;
the freeze does not suppress them.

## Measures

| Measure | Baseline | Calibration threshold |
| --- | ---: | --- |
| Selection receipt coverage | 100% of selected branches | 100% |
| Semantic and integrity verification | 17 / 17 | 100% |
| Evidence coverage on observed outcomes | 5 / 5 | 100% |
| Cognitive-load observations | 0 / 5 outcomes | Observe when natural; never force |
| Advanced momentum | 3 / 3 observed | Report denominator; no optimization target |
| New-useful-path discovery | 0 observed | Capture only when operator-supported |
| Authority incidents | 0 | 0 |
| Membrane incidents | 0 | 0 |
| Recommendation changes from pilot evidence | 0 | 0 |
| Recommendation changes from selection frequency | 0 | 0 |
| Tagged pilot selections | 0 prospectively | 100% of in-window cohort |
| Coffee review opportunities | Not measured | At most 1 per 5 resolved choices |

Counts and rates must disclose missingness and denominators. No composite score
is authorized.

## Quality and burden guardrails

Quality requires:

- valid option-role structure;
- one initial selection event;
- `authority_effect: none`;
- a valid append-only event chain;
- exact tenant, workspace, and lane scope;
- evidence references for observed operational results.

Pause and review if:

- any letter is interpreted as action authority;
- an authority or membrane incident occurs;
- recommendation ordering uses pilot outcomes during calibration;
- selection frequency influences ranking;
- subjective outcomes are inferred without evidence;
- outcome review interrupts ordinary work outside `coffee`;
- more than one review opportunity is offered per five resolved choices;
- the operator reports persistent higher load attributable to the workflow;
- option diversity becomes artificial or credible overlooked paths disappear;
- private persistence, privacy scanning, or semantic verification fails.

## Required evidence

Retain privately:

- selected option sets and stable semantic roles;
- selection and outcome event chains;
- review deferrals, corrections, and supersessions;
- evidence references;
- authority and membrane incident flags.

The end-of-phase review must report:

- selection, outcome, and unresolved counts;
- integrity and evidence coverage;
- missingness by outcome dimension;
- outcome distributions with denominators;
- comparable cohort sizes;
- framing or preference-bubble findings;
- operator burden evidence or `Missing`;
- any exception and its disposition.

## Pilot handoff packet

- Loop reference and approved specification version:
  `LFC-CAL-2026-07-30-01 / LFC-CAL-v1.0`.
- Specification approval receipt:
  `CHOICE-20260729-EXECUTE-CHOICE-CALIBRATION-001`.
- Specification persistence receipt: the Git commit containing this exact
  version; until then persistence is pending.
- Specification state: conditional according to Activation state.
- Pilot route: `manual workflow`.
- Automation involved: `no`.
- Exact scope: seven-day internal calibration in the declared tenant,
  workspace, and lane.
- Approved tools, paths, and data classes: as declared above.
- Run limit: seven days; selected branches only; no minimum volume.
- Named owner and reviewer: Anyang operator.
- Baseline and target: as declared above.
- Quality and burden thresholds: as declared above.
- Required evidence and receipts: private choice events plus a sanitized
  derived review.
- Exceptions and stop conditions: as declared above.
- Approved automation-value-proof reference: `not applicable`.
- `bounded-workflow-pilot` prerequisites satisfied: `yes` only after exact
  repository persistence; otherwise `no`.
- Pilot authorization: `approved`.
- Deployment or external-action authorization: `no`.
- Status: conditional according to Activation state.

## Activation receipt

- Loop reference: `LFC-CAL-2026-07-30-01`.
- Exact approved specification version: `LFC-CAL-v1.0`.
- Transition: `initial activation`.
- Prior pause receipt: `not applicable`.
- Readiness evidence:
  `CHOICE-20260729-PREFLIGHT-CHOICE-PILOT-001`.
- Named activating operator: Anyang operator.
- Named loop owner and decision owner: Anyang operator.
- Effective date: `2026-07-30`, America/Denver.
- Permitted actions: internal possibility navigation, selected-branch
  retention, objective outcome capture, bounded private review, and sanitized
  derived reporting.
- Prohibited actions: recommendation reordering from pilot evidence, inferred
  subjective measurement, automation, external action, authority expansion,
  cross-membrane learning, deployment, commit, or push by implication.
- Evidence destination: private Anyang SQLite ledger; this file contains
  doctrine only.
- Cadence: prospective capture; one end-of-phase review.
- Guardrails and stop conditions: as declared above.
- Review date: `2026-08-05`.
- Activation confirmed: `yes` only after repository persistence and the
  effective date; otherwise `no`.
- State: conditional according to Activation state.

## End-of-phase disposition

Return exactly one pilot status:

- `Complete`;
- `Too thin`;
- `Revised`;
- `Blocked`;
- `Rejected`.

Pair it with one reviewer decision:

- `Adopt`;
- `Revise`;
- `Hold`;
- `Reject`.

No disposition automatically activates outcome-informed learning, expands the
pilot, promotes a repository learning, or changes authority.
