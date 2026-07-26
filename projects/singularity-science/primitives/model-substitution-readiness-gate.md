# Model Substitution Readiness Gate

This primitive evaluates whether a workflow can safely change its underlying AI model without confusing benchmark strength with operational readiness.

It is designed for model swaps across hosted providers, open-weight releases, local deployments, and materially different model versions. It does not recommend a vendor, approve a purchase, or grant authority to deploy.

## Use When

Apply this gate when:

- a workflow may switch models for cost, speed, quality, availability, or sovereignty reasons;
- a new open-weight or local model is being considered;
- a model change affects data location, logging, permissions, tool use, or human review;
- a benchmark or demo is being used to justify a consequential substitution;
- the replacement model's provenance, licensing, security history, or rollback path is unclear.

Use with the [Acceleration-Source Verification Gate](acceleration-source-verification-gate.md), [Permissions and Authority Review Gate](permissions-and-authority-review-gate.md), and [Translation Integrity Review Gate](translation-integrity-review-gate.md).

## Operating Rule

Default state: `review-required`. A model is not ready merely because it is cheaper, newer, open-weight, or better on a benchmark.

## Readiness Surface

| Dimension | What to record | Hold condition |
| --- | --- | --- |
| Task fit | Representative tasks, failure cases, quality threshold, and matched evaluation | Evidence comes from unrelated benchmarks, demos, or vendor claims only |
| Provenance | Source attribution, license, training-data or output-provenance concerns, and rights review status | Provenance or rights status is unknown for a consequential use |
| Security | Model source, dependency chain, isolation, monitoring, abuse behavior, and incident history | The model or repository cannot be inspected or safely isolated |
| Data boundary | What data the model sees, where inference occurs, retention, logging, and exposure | Privacy, residency, retention, or sensitive-data treatment is unresolved |
| Tool and action authority | Tools, APIs, write access, send/publish ability, spending, and downstream triggers | The replacement silently expands authority or bypasses review |
| Human authority | Named owner, approval point, override, stop path, and fallback operator | No accountable owner or practical stop path exists |
| Economics | Total cost per useful task, latency, review burden, migration cost, and switching cost | Savings are based only on token price, parameters, or headline valuation |
| Reversibility | Rollback version, interface compatibility, retained artifacts, and exit plan | Rollback is untested or the workflow becomes provider/model locked |
| Evidence status | Primary sources, test results, unresolved gaps, and review date | A single successful demo is carrying the decision |

## Statuses

- `ready`: all critical dimensions have evidence, authority is explicit, and a bounded rollback-tested trial is approved.
- `review-required`: the substitution is plausible, but evidence, ownership, or lane review is incomplete.
- `hold`: the workflow may be evaluated, but deployment or routing must wait.
- `blocked`: rights, safety, security, privacy, or authority conditions make the substitution unacceptable in the proposed context.

## Core Questions

1. What exact task and failure modes are being compared?
2. Is the evaluation matched to the real workflow rather than a public leaderboard?
3. What changes in provenance, licensing, security, data handling, and observability?
4. Does the replacement change what the system can read, write, send, spend, or approve?
5. Who owns the decision, and can that person stop or reverse the change?
6. What is the total cost of a useful, reviewed outcome—not merely inference cost?
7. Can the workflow return to the prior model without losing state, evidence, or accountability?
8. What evidence would cause the team to reject or reverse the substitution?

## Output Shape

```text
Workflow:
Current model:
Candidate model:
Task and failure modes:
Evaluation evidence:
Provenance / rights status:
Security and data boundary:
Changed tool or action authority:
Human owner and approval point:
Override / rollback path:
Total cost and review burden:
Default state:
Unresolved risk:
Next review trigger:
What stays inside Singularity Science:
```

## First Internal Test

Use this gate on one non-customer-facing research workflow with two model configurations. Compare a fixed task set, failure recovery, review time, provenance evidence, data handling, and rollback—not just answer quality or speed. Record the result with the Translation Integrity Review Gate before considering lane routing.

## Boundary

This gate is an internal readiness aid. It does not establish legal rights, security certification, medical or professional suitability, vendor approval, customer permission, or deployment authority. A `ready` result means only that the proposed bounded test or substitution has met the stated evidence and authority conditions; it is not permanent doctrine.
