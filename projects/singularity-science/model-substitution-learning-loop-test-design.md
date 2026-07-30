# Model Substitution Learning-Loop Test Design

Status: `designed — human approval required before execution`

Purpose: test whether the amended Model Substitution Readiness Gate preserves evidence ownership, feedback rights, evaluation continuity, state portability, lane-local learning, and measurable value when a workflow changes model.

No model switch, provider commitment, customer data use, lane change, or publication is authorized by this design.

## Test 1 — Singularity source-analysis cycle

### Question

Can two model configurations analyze the same governed source packet without losing provenance, uncertainty, correction history, or the boundary between source observation and Anyang judgment?

### Scope

- Use one non-customer-facing Singularity source packet with an existing source note and analysis.
- Keep source body, templates, instructions, evidence set, and reviewer constant.
- Compare the reviewed baseline configuration with one candidate configuration.
- Do not use unverified external claims as test truth; evaluate preservation and reasoning discipline.

### Measures

- Source IDs, attribution, and uncertainty preserved.
- Evidence gaps and verification-sensitive claims correctly retained.
- Seam and disposition agreement with the reviewed baseline.
- Correction count and type after human review.
- Operator cleanup time and rediscovery burden.
- Whether the candidate invents authority, verification, or downstream approval.
- Whether the resulting receipt records model/version, context, evidence, corrections, and rollback state.

### Learning-loop fields

- Evidence owner: Singularity Science / named human reviewer.
- Feedback owner: named reviewer; no provider-training assumption.
- Evaluation continuity: same source-note and analysis acceptance criteria.
- State portability: source IDs, notes, analysis, and corrections remain readable without the candidate model.
- Local versus shared learning: corrections remain test-local unless separately approved.
- Compounding value: lower cleanup or rediscovery burden without lower evidence discipline.

### Hold conditions

- The candidate loses attribution or uncertainty.
- A correction cannot be traced to a reviewer or source.
- The model's context or retained memory cannot be disclosed.
- A successful output is used to justify a lane or doctrine change.

### Evidence artifact

One completed Model Substitution Readiness Gate output plus one Translation Integrity Review receipt. Keep the test artifact inside Singularity Science.

## Test 2 — Media Production synthetic workflow comparison

### Question

Can the Media Production workflow compare two model/product surfaces on accepted, reviewable work while keeping publication, rights, client, spend, and delivery authority unchanged?

### Scope

- Use one synthetic, claim-neutral production brief.
- Hold source body, brief, do-not-invent list, rights notes, deliverables, output format, reviewer, and review window constant.
- Compare two model/product surfaces without live Grace Gems or client-sensitive material.
- Do not publish, deliver, spend, or change the live workflow.

### Measures

- Brief fidelity and source fidelity.
- Creative usefulness and reuse potential.
- Reviewability and uncertainty disclosure.
- Authority discipline: no implied publication, rights clearance, client commitment, or spend.
- Operator cleanup time and correction burden.
- Cost per accepted output, not token price alone.
- Model/product context, tools, permissions, and hidden dependencies disclosed.
- Rollback to the baseline without loss of receipts or work state.

### Learning-loop fields

- Evidence owner: Media Production reviewer; no provider ownership assumed.
- Feedback rights: record whether prompts, outputs, corrections, and usage data are retained or reused.
- Evaluation continuity: use the existing creative-production quality and authority gates.
- State portability: retain brief, outputs, review packet, corrections, and acceptance decision outside the model surface.
- Local versus shared learning: no correction becomes a general production rule without human review.
- Compounding value: accepted-output usefulness must exceed added cleanup and review burden.

### Hold conditions

- The candidate changes the publication, rights, spend, delivery, or client-authority boundary.
- Product-specific memory, hidden instructions, or tool behavior cannot be recorded.
- Cost savings disappear after cleanup, review, or rights work.
- The workflow cannot return to the baseline without losing evidence or accountability.

### Evidence artifact

One completed Media Production model-swap run receipt, one amended Model Substitution Readiness Gate output, and one Translation Integrity Review receipt. Keep the result at the evaluation boundary; no live workflow change follows automatically.

## Decision rule

Do not promote the amended gate to operating doctrine from one successful test. Require both tests, human review, and evidence that learning-loop continuity improved or preserved decision quality without material new burden or authority ambiguity.
