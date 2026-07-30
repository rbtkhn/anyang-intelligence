# Measurement Addendum — Cleanup, Cost, and Repeated-Cycle Value

Date: 2026-07-29
Related receipt: [Model Substitution Learning-Loop Research-to-Improvement Receipt](model-substitution-learning-loop-research-to-improvement-receipt.md)
Status: `measurement gap recorded`

## Observed evidence

| Measure | Test 1 | Test 2 Run A | Judgment |
| --- | --- | --- | --- |
| Operator cleanup time | Not recorded | Not recorded | Missing |
| Inference or tool cost | Not available | Not available | Missing |
| Review burden | Qualitatively described as duplicated gate language | Not timed | Missing |
| Repeated-cycle reuse | Not observed | Not observed | Missing |
| Accepted-output value | No downstream decision | Provisional synthetic pass | Insufficient |

No numerical cleanup, cost, or repeated-cycle value is inferred from the available artifacts.

## Minimal measurement protocol

For each future bounded cycle, record:

```text
Cycle ID:
Model / configuration:
Task and fixed inputs:
Start time:
Generation complete time:
Human review start:
Human review complete:
Cleanup minutes:
Corrections by category:
Rights / provenance corrections:
Authority corrections:
Evidence or factual corrections:
Accepted output: yes / no / revise / hold
Estimated direct cost:
Review burden: low / medium / high
Reusable artifact produced:
Used in a later cycle: yes / no
Later-cycle benefit observed:
Rollback or rejection reason:
```

## Measurement rules

- Compare only like-for-like tasks with the same source, brief, output contract, and reviewer where possible.
- Count accepted, reviewed output—not generated volume—as the value unit.
- Include cleanup, rights, provenance, review, migration, and correction burden in total cost.
- Keep source-specific corrections local unless a human approves cross-lane reuse.
- Do not count a successful draft as compounding value until a later cycle actually reuses it and records a benefit.
- Do not use a single cycle to rank models or promote doctrine.

## Current judgment

The tests demonstrate governance usefulness but not economic or operational efficiency. The amended gate remains `testable-primitive`; promotion requires at least two comparable cycles with measured cleanup and review burden, plus independent model-surface evidence for substitution claims.

## Repeat-cycle result

Two same-runtime synthetic cycles were completed and recorded in [Same-Runtime Repeat-Cycle Measurement](media-production-learning-loop-repeat-cycles.md). Contract adherence was stable at 12/12 measured points in each cycle, with creative variation between recommendations. Human cleanup time, direct cost, and later-cycle reuse remain unobserved, so no compounding-value claim is made.
