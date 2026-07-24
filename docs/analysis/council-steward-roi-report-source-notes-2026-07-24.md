# Council Steward ROI Report Source Notes

## Reporting job

- Question: What future ROI should the Engineer expect from the new Council
  Steward position?
- Decision: whether to activate and measure the proposed 30-day portfolio
  pilot, then retain, revise, or stop the position.
- Audience: product stakeholders / Engineer.
- Scope: six current projects; year-one portfolio economics.
- Baseline: no measured Steward pilot exists.
- Confidence: provisional and scenario-based.

## Evidence inventory

1. `projects/README.md` establishes six current installations.
2. A repository file count on 2026-07-24 observed 458 files under `projects/`.
   File count is a complexity indicator only and is not used as a value
   multiplier.
3. `projects/grace-gems/council-steward-pilot-engineer-approval-receipt-2026-07-24.md`
   defines the proposed term, required measurements, success conditions, and
   stop conditions.
4. `projects/grace-gems/executive-council-three-role-receipt-reconstruction-2026-07-24.md`
   demonstrates manual reconstruction work and unresolved receipt gaps but
   does not record reconstruction time.
5. `docs/executive-interface-protocol.md` supplies existing expansion anchors:
   two or more hours saved per week, 25% less clarification or rework, 90%+
   receipt coverage, material escalation improvement, or zero authority/client
   boundary violations.
6. `docs/analysis/council-steward-roi-model-2026-07-24.py` contains the complete
   scenario assumptions and formulas.

## Metric definitions

- Year-one gross benefit = 12 x (reconstruction hours saved + routine rework
  hours avoided) x labor value.
- Year-one cost = setup hours x labor value + 12 x (human review hours x labor
  value + AI runtime/tool cost).
- Year-one net benefit = gross benefit - cost.
- Year-one ROI = net benefit / cost.
- Break-even benefit hours per month = average monthly year-one cost / labor
  value.
- Setup payback = setup cost / monthly net benefit after recurring cost;
  undefined when monthly net benefit is non-positive.

## KPI recommendation

Primary:

1. Verified net benefit-hours per month: time saved and routine rework avoided,
   minus Steward review and correction time.
2. Accepted material-finding rate: accepted or accepted-with-revision material
   findings divided by all material findings.
3. Year-one-equivalent ROI: annualized verified benefit value minus annualized
   cost, divided by annualized cost.

Drivers:

- state reconstruction minutes per review;
- routine rework incidents and hours prevented;
- missing receipts, contradictions, stale obligations, and unsupported
  completion claims found.

Guardrails:

- zero privacy, membrane, authority, or external-communication violations;
- false-positive rate no higher than 20%;
- new Steward artifacts no greater than artifacts consolidated or superseded;
- Engineer plus Chief Executive review burden no higher than two hours per
  month in the base operating case.

## Chart map

- Segment: The position is attractive if it clears a low operational hurdle.
- Question: How does year-one net benefit vary across the three scenarios and
  the assumption-weighted expectation?
- Family: comparison.
- Type: vertical bar.
- Fields: outcome label and year-one net benefit; scenario probability, gross
  benefit, cost, ROI, and break-even hours retained in the dataset.
- Supported claim: the downside is bounded in the conservative case while the
  base and weighted cases are economically positive.
- Palette: single blue root plus neutral zero reference; signed labels carry
  direction without red/green semantics.
- Final QA surface: Data Analytics MCP report artifact.

## Required-structure mapping

- Title: `Council Steward ROI Outlook`.
- Executive summary: visible immediately after the title.
- Key findings with visual evidence: scenario comparison and break-even
  interpretation.
- Recommended next steps: 30-day investment test and retain/revise/stop gates.
- Further questions: baseline, accepted findings, actual runtime cost, and
  cross-project reuse.
- Caveats and assumptions: scenario inputs, judgmental probabilities, excluded
  benefits, and missing pilot baseline.

## Validation notes

- The Python model executed successfully on 2026-07-24.
- An independent JavaScript recomputation matched all scenario benefits, costs,
  net benefits, ROI values, break-even hours, and weighted totals.
- Notebook JSON is structurally valid. Top-to-bottom Jupyter execution was not
  available because `nbformat`, `nbclient`, and Jupyter are not installed in
  the available Python environments. The identical companion Python model was
  executed directly.
- Confidence assessment: `Share with caveats`.

## Omitted value

The model excludes revenue uplift, major privacy or authority incident
avoidance, customer trust and retention effects, and cross-project learning
value beyond routine time savings. These could be material but cannot be
quantified from current evidence without inventing loss probabilities or
business economics.
