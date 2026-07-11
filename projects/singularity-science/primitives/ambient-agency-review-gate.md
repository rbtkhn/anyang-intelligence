# Ambient Agency Review Gate

This primitive is a review gate for AI systems that act in the background, stay continuously present, surface only selected decisions, or blur the boundary between "tool" and "actor."

Its purpose is to catch authority leak early when delegation becomes ambient rather than explicit.

Use with:

- [README.md](README.md)
- [embodied-ai-exposure-scan.md](embodied-ai-exposure-scan.md)
- [../research-operating-model.md](../research-operating-model.md)
- [../customer-impact-map.md](../customer-impact-map.md)
- [../../../docs/membranes.md](../../../docs/membranes.md)

## Operating Rule

Default state: `watch` or `hold` until approval, override, and visibility are clear.

This gate does not ask whether a system is smart. It asks whether a system changes the practical location of agency.

## What Counts As Ambient Agency

Apply this gate when a system:

- runs in the background
- queues or completes tasks without continuous human prompting
- stays present through voice, chat, wearable, or embedded interfaces
- uses memory, monitoring, or persistent context to act over time
- asks for approval only on selected steps
- changes what a human notices, approves, or remembers doing

Examples include:

- coworker agents
- background workflow automations
- continuous voice assistants
- monitoring agents
- approval-minimizing task runners
- meta-harnesses that rewrite or reroute their own scaffolding

## Core Questions

1. What exactly is being delegated?
2. What does the human stop seeing once this system is in place?
3. Which decisions are still explicitly approved, and which are now assumed?
4. Could a user confuse "I reviewed this" with "the system handled this"?
5. What happens when the system is wrong quietly rather than dramatically?

## Review Dimensions

| Dimension | What to ask | Typical warning sign |
| --- | --- | --- |
| Visibility | Can the human see what the system did, changed, skipped, or assumed? | Important work disappears into background execution |
| Approval | Are the approval points real, legible, and appropriately placed? | Humans approve outputs without understanding the decisions underneath |
| Override | Can a human pause, inspect, redirect, or fully stop the system? | Stopping the system is possible in theory but awkward in practice |
| Memory | What prior context or personal data is the system carrying forward? | Old context keeps shaping action without fresh consent |
| Drift | Could the system begin doing more than the user thinks it is doing? | Scope creep happens through convenience rather than explicit choice |
| Accountability | Who owns the outcome when the ambient system gets it wrong? | Responsibility becomes socially or operationally ambiguous |

## Lane Review Prompts

### Media Production

- Is the system only accelerating workflow, or is it beginning to decide quality, rights, sequencing, or publication posture?
- Would a producer clearly know what the system drafted, routed, changed, or suppressed?
- Could ambient capture, background generation, or auto-assembly create rights or consent surprises?

Recommended default: `watch`

### Grace Gems

- Is the system helping with support and listing workflow, or beginning to imply owner-approved claims?
- Could background automation drift into pricing, customer promises, or return-language changes without explicit review?
- Does convenience make the owner approve more than they meaningfully inspected?

Recommended default: `watch`

### Learning Core

- Does the system change what the parent notices, approves, or says directly to the child?
- Could a child experience the system as an authority even if the parent technically remains in charge?
- Are approvals still parent-visible, or has agency already shifted through convenience?

Recommended default: `hold`

### retired Non-Profit project

- Is the system drafting or is it quietly steering donor language, reporting tone, or board-facing framing?
- Could institutional review become symbolic because the system is doing too much before review?
- Does the background layer create mission drift or compliance ambiguity?

Recommended default: `watch`

### Mountain Villa

- Is the system only surfacing signals, or beginning to substitute for owner judgment about risk or response?
- Would the owner know what was ignored, escalated, or automatically categorized?
- Can the system be stopped quickly in a high-stakes environment?

Recommended default: `watch`, with `hold` for safety-critical use

### Book Club

- Is the system helping memory and coordination, or beginning to shape tone, prompts, or participation patterns invisibly?
- Could members feel steered or observed without understanding how?
- Does the ambient layer make the space feel less voluntary or more transactional?

Recommended default: `watch`

## Status Guidance

- `watch`: ambient delegation is plausible, but no live use should be normalized yet
- `candidate`: enough repeated pressure exists to preserve a lane-specific review artifact
- `hold`: authority, privacy, safety, or consent concerns outweigh current value
- `test`: a narrow, reversible, clearly supervised use case is defined

## Escalation Triggers

Route through human review immediately when ambient agency affects:

- children or education
- donor, board, or public-facing claims
- rights-sensitive media or capture
- safety-critical monitoring or response
- money, pricing, or commitments
- hidden memory, surveillance, or persistent profiling

## Output Shape

When this gate is applied, capture:

```text
Lane:
System or workflow:
What is being delegated:
What becomes less visible:
Approval point:
Override path:
Main authority risk:
Default state:
What would need to be true to move to test:
What stays inside Singularity Science:
```

## Boundary

Do not route source-specific launch hype, benchmark claims, or vendor rhetoric through this primitive.

Route only the governance question: where has agency quietly moved, and what must stay human-visible?
