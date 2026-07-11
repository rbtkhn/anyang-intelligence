# Deep Audit: Turn Usefulness Across Anyang Intelligence

This report audits turn usefulness across the cross-repo core:

- Singularity Science
- Media Production
- Elementary School
- Non-Profit
- Mountain Home
- Grace Gems

The audit uses the Singularity Science framework as its standard:

- [useful-turn-evaluation-note.md](useful-turn-evaluation-note.md)
- [turn-usefulness-scorecard.md](turn-usefulness-scorecard.md)
- [primitives/ambient-agency-review-gate.md](primitives/ambient-agency-review-gate.md)

Companion score matrix:

- [turn-usefulness-audit-matrix.md](turn-usefulness-audit-matrix.md)

## Executive Summary

The repo already contains a meaningful turn-usefulness philosophy, but maturity is uneven across lanes.

The strongest pattern is in Elementary School: turns are tightly gated, approvals are meaningful, and loop definitions survive validator checks. The weakest pattern is not bad governance. It is incomplete workflow instrumentation in the other lanes. Many lanes already say the right things, but fewer can yet prove that a good turn survives repeated use without hidden supervision or symbolic approval.

The central repo-wide finding is:

- **governance integrity is ahead of delegation instrumentation**

That is a good failure mode to have, but it limits useful-turn compounding. The next phase should not relax governance. It should add more repeatable loop, receipt, and scoring surfaces so strong review design produces stronger measurable turn completion.

## Method

Audit units were scored at three levels:

- artifact level: templates, checklists, runbooks, training exemplars, primitives
- loop level: formal loop definitions, gating paths, approval structures
- workflow level: likely operator paths validated through static spot checks

Default scoring model:

- Outcome Value `35%`
- Completion Quality `25%`
- Delegation Gain `25%`
- Governance Integrity `15%`

Governance cap:

- if Governance Integrity is below `0.6`, overall usefulness may not exceed `0.6`

Workflow evidence used:

- `anyang_loop.install_cli validate customers`
- `anyang_loop.cli validate customers\elementary-school`
- YAML inventory of lane loop examples
- targeted review of workflow-facing artifacts in each target lane

## Findings Taxonomy

The audit used this failure taxonomy:

- **low outcome value**: the surface does not reliably create meaningful forward motion
- **high cleanup burden**: outputs are useful but too rough for efficient review
- **weak delegation gain**: humans still carry too much prompting, stitching, or context rebuild
- **symbolic approval**: approval exists on paper but may not be meaningful in practice
- **hidden authority leak**: the surface risks moving decisions out of visible human control
- **weak override visibility**: escalation or stop paths are implied but not concretely surfaced
- **excessive context rebuild**: adjacent artifacts do good work but require too much rereading or manual recomposition

## Lane Findings

### Elementary School

This is the strongest lane in the audit and the calibration lane for the scoring model.

Why it scores highest:

- multiple gates survive a real workflow path
- explicit `Ready` / `Provisional` / `Hold` states reduce symbolic progress
- parent authority remains visible across intake, drafting, approval, and hold states
- loop examples validate successfully through `anyang_loop.cli`
- training exemplars show how safe turns should behave, not only what docs say

Weakness:

- delegation gain is intentionally constrained by the lane's safety requirements
- some strong surfaces are still document-heavy rather than receipt-heavy

Read:

- best governance integrity in repo
- useful-turn maturity is real, not rhetorical
- next gains should come from score-based regression checks and compact receipts, not looser automation

### Singularity Science

This lane is strongest at framing, routing, and primitive creation.

Why it scores well:

- it now has a coherent evaluation vocabulary
- the useful-turn and ambient-agency artifacts are reusable
- archive analysis is increasingly producing primitive candidates instead of staying at commentary level

Weakness:

- no loop-example surface yet for research -> primitive -> lane application
- archive analyses are strong, but downstream application evidence is still thin
- validator warnings show missing installation scaffolding similar to other lanes

Read:

- strongest conceptual maturity in repo
- mixed workflow completion evidence
- highest leverage move is to instrument one preserved research-to-lane loop

### Media Production

This lane has good production and assignment logic, especially around contractor-facing work and quality review.

Why it scores solidly:

- the assignment gate is explicit about source truth, rights, capacity, and authority
- the lane already thinks in review packets and quality gates rather than freeform generation

Weakness:

- no loop examples
- validator still reports missing scaffold surfaces
- strong gate logic has not yet been converted into repeatable score-bearing workflow loops

Read:

- best candidate for next useful-turn instrumentation outside Elementary School
- turn usefulness is implied well, but not yet measured well

### Grace Gems

This lane has a coherent marketplace loop and decent owner-governed framing.

Why it scores respectably:

- the listing gate loop is a strong operating unit
- owner authority is explicit
- intake and public-signal artifacts create a real context base

Weakness:

- owner approval is present more as principle than as repeated receipt artifact
- lane-level operating review structure is still thin

Read:

- strongest next step is an owner-review receipt or listing usefulness scorecard

### Mountain Home

This lane has strong risk framing and one strong formal loop.

Why it scores well enough:

- the seasonal readiness loop has a clear authority boundary
- risk-first thinking compresses ambiguity well

Weakness:

- one loop carries too much of the lane
- broader artifact depth is still light
- false reassurance remains the main ambient failure risk

Read:

- good governance core
- needs more review and override artifacts to raise usefulness without raising automation risk

### Non-Profit

This lane has the lowest score in the audited core, but mainly because it is under-instrumented, not because it is careless.

Why it still scores meaningfully:

- governance language is strong
- mission, donor, grant, and board boundaries are explicit

Weakness:

- almost all workflow logic still lives inside the install doc
- low delegation gain because key work is not broken into reusable reviewed units
- no loop examples and no dedicated artifacts for donor review, board memo preparation, or impact-evidence closure

Read:

- strongest candidate for turning high-quality governance language into reusable workflow surfaces

## Cross-Repo Patterns

### What is working

- Most lanes are better at preserving authority than at chasing unsafe automation.
- The repo is increasingly good at gates, holds, and approval boundaries.
- Research-side Singularity Science now has a reusable framework for evaluating useful turns.
- Elementary School proves that turn usefulness can be made concrete and governed.

### What is missing

- Too many lanes still lack loop examples.
- Install docs often carry workflow intent that has not yet been broken into reusable audited units.
- Generated support files are missing across the audit scope, which weakens repeatable operating review.
- Few lanes have explicit receipt or scorecard artifacts that prove a good turn survived review.

## Prioritized Remediations

### Quick wins

1. **Add generated support files across the audited lanes**
   - Target: Singularity Science, Media Production, Grace Gems, Mountain Home, Non-Profit, Elementary School
   - Problem: repeated validator warnings weaken operating review completeness
   - Expected usefulness gain: moderate
   - Governance benefit: clearer recurring review surfaces and explicit risk handling
   - Artifact type: generated support docs and `loop-examples/` where missing

2. **Add loop examples for Media Production and Non-Profit**
   - Target: Media Production, Non-Profit
   - Problem: strong workflow intent, weak repeatable formal loops
   - Expected usefulness gain: high
   - Governance benefit: makes approval and review paths more inspectable
   - Artifact type: loop example YAML plus linked README/install references

3. **Add receipt-style approval artifacts to Grace Gems**
   - Target: Grace Gems
   - Problem: owner approval exists, but closure evidence is thin
   - Expected usefulness gain: medium
   - Governance benefit: reduces symbolic approval risk
   - Artifact type: owner approval record or listing review receipt

### Medium lifts

4. **Add score-based regression checks to Elementary School**
   - Target: Elementary School
   - Problem: strongest lane is still mostly document- and exemplar-driven
   - Expected usefulness gain: medium
   - Governance benefit: preserves safety while making quality drift visible earlier
   - Artifact type: scored exemplar notes or turn-usefulness receipt template

5. **Add a risk-review worksheet for Mountain Home**
   - Target: Mountain Home
   - Problem: one strong seasonal loop, thin broader execution support
   - Expected usefulness gain: medium
   - Governance benefit: reduces false reassurance and hidden escalation drift
   - Artifact type: property review worksheet or override-sensitive triage artifact

### Structural work

6. **Instrument the Singularity Science research-to-lane pipeline**
   - Target: Singularity Science
   - Problem: primitives exist, but preserved application evidence is thin
   - Expected usefulness gain: high
   - Governance benefit: shows whether research signals survive membrane review without authority leak
   - Artifact type: research-to-primitive loop example, receiving-lane test receipts, or preserved audit traces

7. **Create lane-specific turn-usefulness scorecards**
   - Target: Media Production, Grace Gems, Non-Profit, Mountain Home
   - Problem: general scorecard exists, but lane-level operating tasks are not yet measured consistently
   - Expected usefulness gain: high
   - Governance benefit: turns polished-looking outputs into inspectable work units
   - Artifact type: lane-adapted scorecards or review checklists

## Audit Conclusion

The repo is not weak at turn usefulness. It is uneven.

Elementary School already demonstrates what a governed high-usefulness lane can look like. Singularity Science now has the conceptual machinery to evaluate turns and ambient agency well. The next repo-wide move is to push that maturity outward: formalize loops, add review receipts, and make useful-turn survival measurable in the lanes where good judgment already exists but completion evidence is still thin.
