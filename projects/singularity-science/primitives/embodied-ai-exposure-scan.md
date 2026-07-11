# Embodied AI Exposure Scan

This primitive is a lane-by-lane prompt and checklist for spotting where cheap robotics or embodied AI may matter first.

Its purpose is not to predict adoption timelines. Its purpose is to surface early operating exposure while preserving trust, supervision, UX quality, maintenance realism, and human override.

Use with:

- [../research-operating-model.md](../research-operating-model.md)
- [../customer-impact-map.md](../customer-impact-map.md)
- [../../../docs/membranes.md](../../../docs/membranes.md)

## Operating Rule

This scan is advisory.

It may identify where embodied AI deserves watch, prototype, or hold status. It may not create customer obligations, justify purchases, or promote source-specific robotics claims into doctrine.

## Core Questions

Apply these questions before routing any embodied-AI implication into a lane:

1. What task is physical, repetitive, supervision-heavy, or logistically brittle enough that robotics could matter?
2. Is the main exposure about trust, supervision load, UX friction, maintenance burden, or human override?
3. What would failure look like in this lane: inconvenience, quality loss, safety issue, rights issue, financial issue, or authority leak?
4. What human remains accountable when the robot, device, or embodied agent gets it wrong?
5. What proof would be needed before moving from watch to test?

## Common Exposure Dimensions

Score or annotate each lane across these dimensions:

| Dimension | What to look for | Typical first warning |
| --- | --- | --- |
| Trust | Whether people must believe the system is safe, accurate, and non-deceptive | People over-trust demos or assume autonomy where there is none |
| Supervision | How much human checking, intervention, or fallback is still required | The system saves time only if someone constantly watches it |
| UX | Whether the interaction is intuitive, legible, and recoverable when things go wrong | Users cannot tell what the system is doing or how to stop it |
| Maintenance | How much setup, repair, charging, calibration, or environment hardening is required | Operational overhead outweighs the promised labor savings |
| Human override | Whether a clear person can pause, redirect, or shut down the system safely | Responsibility becomes ambiguous during edge cases |

## Lane Scan

### Media Production

Primary exposure areas:

- camera, lighting, capture, or asset-handling automation
- embodied studio tools that promise faster setup or repetitive task relief
- robotics-adjacent production workflows that blend physical capture with AI direction

Checklist:

- Would embodied tooling actually reduce crew burden, or just move effort into supervision?
- Could the operator tell what the system is capturing, moving, or changing at any moment?
- Would a failure damage assets, schedules, client trust, or publication quality?
- Is there a clean human override path during live production moments?
- Does the workflow create new rights or consent concerns around automated capture?

Recommended default status: `watch`

### Grace Gems

Primary exposure areas:

- warehouse or fulfillment automation
- product imaging rigs with embodied handling
- customer-trust impacts from automation language or robotic fulfillment claims

Checklist:

- Is the real opportunity physical handling, or is software/process cleanup the higher-leverage move?
- Would embodied automation create brittle edge cases around product care, packing, or returns?
- Could operator trust be weakened if robotic language overstates reliability?
- What maintenance burden would fall on the owner?
- Can the owner stop or revert the workflow without operational chaos?

Recommended default status: `hold` unless a narrow fulfillment problem is already well defined

### Learning Core

Primary exposure areas:

- child-facing robots, kiosks, or embodied tutoring devices
- classroom-support tools that affect authority, attention, or safety perception
- normalization of robots as companions, guides, or evaluators

Checklist:

- Does the system blur adult authority, teacher authority, or parent authority?
- Would a child understand what the system can and cannot do?
- Could the interface create attachment, false confidence, or surveillance discomfort?
- Is there immediate adult override for every meaningful interaction?
- Would this tool change expectations about care, judgment, or safety in ways adults did not explicitly approve?

Recommended default status: `hold`

### retired Non-Profit project

Primary exposure areas:

- event logistics or facility operations automation
- donor-facing novelty pressure around robotics
- internal experimentation that could be mistaken for mission doctrine

Checklist:

- Is there an actual mission-aligned operational problem, or just technology curiosity?
- Could robotics use create donor confusion, board concern, or staff anxiety?
- Who supervises the system, and who owns failure?
- Would upkeep, training, or support costs exceed the operating gain?
- Does the tool risk shifting institutional tone from service to spectacle?

Recommended default status: `watch`

### Mountain Villa

Primary exposure areas:

- home monitoring, inspection, or patrol robotics
- maintenance aids for repetitive physical tasks
- embodied devices used in weather, emergency, or property-risk contexts

Checklist:

- Would the system improve actual preparedness, or mainly create false reassurance?
- Can it operate reliably under real property conditions, not demo conditions?
- What happens if connectivity, power, or sensing fails during a high-stakes moment?
- Is there a simple manual fallback?
- Could the system complicate insurance, contractor, or safety decisions if trusted too early?

Recommended default status: `watch`, with `hold` for any safety-critical use

### Book Club

Primary exposure areas:

- low-probability novelty use in meetings or shared material handling
- experimental community-facing devices that could affect tone or comfort

Checklist:

- Is there any real need for embodiment here, or would software-only support do the job better?
- Would the device make the space feel performative, transactional, or surveilled?
- Who is responsible if members are uncomfortable?
- Can the experience remain optional and easy to exit?
- Does the novelty add friction instead of value?

Recommended default status: `hold`

## Status Guidance

Use these statuses when the scan is applied:

- `watch`: a real exposure exists, but no test should start without a tighter use case
- `candidate`: a narrow problem is clear enough to design a primitive or test plan
- `hold`: governance, trust, safety, or supervision concerns outweigh current value
- `test`: a small, reversible, human-supervised experiment is justified

## Escalation Triggers

Stop and route through human review when embodied AI touches:

- children or education
- safety-critical physical environments
- emergency response
- money, donor trust, or owner-facing promises
- surveillance, recording, or consent ambiguity
- legal, insurance, or compliance-sensitive claims

## Output Format

When using this primitive, capture findings in this shape:

```text
Lane:
Use case:
Primary exposure dimension:
Main risk:
Human accountable:
Default status:
What would need to be true to move to test:
What stays inside Singularity Science:
```

## Boundary

Do not route source-specific robotics pricing claims, deployment timelines, or transcript rhetoric through this scan.

Route only synthesized operating questions, governance warnings, and narrowly framed primitive ideas.
