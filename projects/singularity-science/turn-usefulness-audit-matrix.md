# Turn Usefulness Audit Matrix

This matrix scores the cross-repo core audit surfaces using the Singularity Science turn usefulness framework.

Scoring method:

- Default score = weighted average
- Outcome Value = 35%
- Completion Quality = 25%
- Delegation Gain = 25%
- Governance Integrity = 15%
- Governance cap applies only when Governance Integrity is below `0.6`

## Spot-Check Evidence Used

- `anyang_loop.project_cli validate customers` passes for all customer lanes but reports repeated scaffold warnings across the audit scope: missing generated support files and, for several lanes, missing `loop-examples/`.
- `anyang_loop.cli validate projects\learning-core` validates both Learning Core loop definitions successfully.
- YAML inventory confirms additional loop definitions exist in Grace Gems and Mountain Villa, while Media Production, retired Non-Profit project, and Singularity Science currently lack loop-example surfaces.
- Workflow spot checks were performed against:
  - Media Production `creative-production-operator-assignment-gate.md`
  - Grace Gems `loop-examples/listing-gate.yaml`
  - Mountain Villa `loop-examples/seasonal-readiness.yaml`
  - retired Non-Profit project `executive-os-install.md`
  - Learning Core `parent-intake-to-draft-runbook.md`

## Matrix

| Lane | Audit unit | Surface type | Intended user | Likely turn boundary | Outcome Value | Completion Quality | Delegation Gain | Governance Integrity | Overall | Main failure mode | Suggested remediation | Disposition |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| Singularity Science | Research routing core (`README`, `research-operating-model`, `customer-impact-map`) | Routing and policy docs | Research team | Research signal -> lane-safe routing decision | 0.75 | 0.72 | 0.44 | 0.82 | 0.68 | Strong framing with weak workflow instrumentation | Add a research-to-primitive loop example and recurring audit hook | Tighten |
| Singularity Science | Useful-turn evaluation stack (`useful-turn-evaluation-note`, `turn-usefulness-scorecard`) | Evaluation primitives | Research team and future operators | One scored turn -> reusable evaluation judgment | 0.82 | 0.80 | 0.60 | 0.86 | 0.77 | Good scoring logic without live operating examples | Add one worked example scored against a real lane workflow | Preserve |
| Singularity Science | Ambient agency stack (`ambient-agency-review-gate`, `ambient-agency-use-case-map`) | Governance primitives | Research team and lane reviewers | Ambient system proposal -> watch/hold/test review | 0.80 | 0.77 | 0.58 | 0.88 | 0.76 | Strong gate, limited proof it survives lane execution | Apply to one receiving lane and preserve scored result | Preserve |
| Singularity Science | Innermost Loop July cluster package | Archive analysis | Research team | Source cluster -> memo -> primitive candidate | 0.74 | 0.73 | 0.38 | 0.80 | 0.66 | Good synthesis, low completion evidence for downstream use | Add one explicit receiving-lane application artifact | Tighten |
| Learning Core | Parent intake to draft runbook | Runbook | Operator | Parent intake response -> `Ready` / `Provisional` / `Hold` | 0.88 | 0.86 | 0.72 | 0.95 | 0.85 | Slight supervision heaviness because the operator still carries many checks manually | Add compact scorecard or receipt for completed intake turns | Preserve |
| Learning Core | Onboarding readiness checklist | Gate | Operator | Intake facts -> readiness classification | 0.84 | 0.86 | 0.68 | 0.96 | 0.84 | Slight context rebuild across nearby docs | Add a one-screen summary artifact for repeated use | Preserve |
| Learning Core | Plan drafting gate plus evidence map | Gate and traceability worksheet | Operator | Approved intake -> review-ready draft | 0.90 | 0.88 | 0.66 | 0.97 | 0.85 | Lower delegation gain because drafting remains intentionally review-heavy | Add a draft usefulness scorecard for first-pass plan quality | Preserve |
| Learning Core | Parent approval record plus hold response template | Approval and pause artifacts | Operator and parent reviewer | Draft review -> approved / changed / held state | 0.84 | 0.82 | 0.60 | 0.98 | 0.80 | Approval is strong but still document-centric rather than loop-instrumented | Add a lightweight approval receipt loop example | Preserve |
| Learning Core | AI interface training exemplars | Training fixtures | Future operators and agents | Example case -> learned safe behavior | 0.78 | 0.84 | 0.62 | 0.94 | 0.79 | High quality, but examples are not yet tied to score-based regression checks | Add exemplar scoring notes using the turn-usefulness scorecard | Tighten |
| Learning Core | Embodied AI governance pack (`embodied-ai-hold-policy`, worksheet, exemplar) | Specialized governance artifacts | Operator and parent reviewer | Child-facing AI proposal -> `Hold` or narrow test review | 0.82 | 0.84 | 0.56 | 0.99 | 0.79 | Strong governance with intentionally low delegation | Add a reusable approval-record addendum for embodied-AI reviews | Preserve |
| Learning Core | Loop examples (`learning-experience`, `parent-intake-readiness`) | Formal loops | System and operator | Ongoing learning cycle -> approved next action | 0.76 | 0.78 | 0.74 | 0.93 | 0.80 | Limited breadth; only two loops cover the lane's larger workflow | Expand validated loop coverage to draft review and approval update | Tighten |
| Media Production | Core operating docs (`README`, `executive-os-install`) | Install and routing docs | Operator | Need signal -> pipeline or review path | 0.68 | 0.62 | 0.42 | 0.78 | 0.63 | High-level pipeline implies usefulness without enough scored survival detail | Add loop examples and operating review artifacts | Tighten |
| Media Production | Creative Production Operator assignment stack | Assignment gate and onboarding | Operator and contractor | Task proposal -> assign / revise / hold / reject | 0.82 | 0.78 | 0.64 | 0.90 | 0.78 | Strong gate, but no formal loop surface validates repetition quality | Add loop example for assignment -> review packet -> quality gate | Preserve |
| Media Production | Creative abundance quality stack | Quality gate and ledger template | Operator and reviewer | Draft asset -> reviewable / revise / hold | 0.76 | 0.72 | 0.54 | 0.84 | 0.72 | Quality review is explicit, but accepted-output instrumentation is absent | Add asset usefulness scorecard and reuse receipt | Tighten |
| Grace Gems | Core operating docs (`README`, `executive-os-install`) | Install and routing docs | Owner and operator | Product or listing need -> draft / hold / publish review | 0.66 | 0.62 | 0.44 | 0.80 | 0.64 | Owner review is clear in principle but thinly operationalized | Add owner approval artifact and listing review receipt | Tighten |
| Grace Gems | Intake and public signal stack (`business-intake-survey`, `public-shop-signal-brief`) | Intake and external signal review | Owner and operator | Storefront signal -> operating review input | 0.70 | 0.68 | 0.50 | 0.78 | 0.67 | Good context gathering, limited closure into reviewed decisions | Add a recurring operating review template with turn scoring | Tighten |
| Grace Gems | Listing gate loop example | Formal loop | Owner and operator | Listing candidate -> publish / revise / hold / promote | 0.74 | 0.74 | 0.64 | 0.90 | 0.76 | Loop is strong but stands mostly alone | Expand with linked approval record and post-publish learning review | Preserve |
| Mountain Villa | Core operating docs (`README`, `executive-os-install`) | Install and routing docs | Owner and operator | Risk signal -> mitigate / monitor / review decision | 0.64 | 0.60 | 0.42 | 0.82 | 0.63 | Strong risk framing, weak reusable execution scaffolding | Add property review worksheet and risk-usefulness scorecard | Tighten |
| Mountain Villa | Seasonal readiness loop example | Formal loop | Owner and operator | Seasonal risk signal -> approved mitigation action | 0.76 | 0.74 | 0.64 | 0.92 | 0.78 | Strong governance, but only one loop carries the lane | Add companion loops for incident triage and proof-of-mitigation review | Preserve |
| retired Non-Profit project | Core install and governance sections | Install and governance doc | Leadership and operator | Mission / donor / grant signal -> reviewed next action | 0.68 | 0.64 | 0.36 | 0.88 | 0.63 | Strong governance language with low delegation gain and no reusable sub-artifacts | Break out donor-review, board-memo, and impact-evidence artifacts plus loop examples | Tighten |

## Lane Averages

| Lane | Average score | Audit read |
| --- | ---: | --- |
| Learning Core | 0.82 | Strongest audited lane; best governance integrity and richest workflow evidence |
| Singularity Science | 0.72 | Strongest framing lane; mixed completion evidence for research-to-lane execution |
| Media Production | 0.71 | Good review gates and contractor assignment logic; weak loop and instrumentation depth |
| Grace Gems | 0.69 | Coherent marketplace review logic; owner-approval execution surfaces still thin |
| Mountain Villa | 0.71 | Clear risk-first framing and one strong loop; broader operating scaffolding still sparse |
| retired Non-Profit project | 0.63 | Strong governance posture but lowest delegation gain and least developed reusable workflow surfaces |
