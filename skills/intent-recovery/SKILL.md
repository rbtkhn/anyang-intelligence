---
name: intent-recovery
description: Recover the likely underlying operator intent from compressed, incomplete, or poorly articulated language and restate it clearly without inventing facts or authority. Use when the operator explicitly invokes $intent-recovery; the canonical elicitation, bravo, friction, product-doctrine, and business-intake workflows may also load it as their bounded automatic subroutine.
---

# Intent Recovery

Recover meaning that is already present but not yet well expressed. Interpret generously without claiming privileged access to the operator's mind.

## Bounded Workflow Composition

Standalone discovery remains explicit-only. The following workflows may load this complete canonical skill automatically when language is compressed, metaphorical, evaluative without explanation, or explicitly difficult to articulate:

- `elicitation`: decide whether meaning can be recovered before asking a question;
- `bravo`: recover the specific quality praised before extracting a reusable pattern;
- `friction`: recover the intended correction before selecting a repair;
- product doctrine: translate an intuitive direction that may affect `docs/thesis.md` or `docs/product.md`;
- `business-intake`: reflect an informally expressed owner goal or constraint before follow-up.

Skip automatic recovery for exact menu selections, clear commands, factual receipts, explicit approvals, or genuinely missing evidence. Do not reinterpret precise language merely because a more elegant formulation is possible.

Use an adaptive receipt for high-confidence recovery that materially affects direction:

```text
Recovered intent: <one concise, clearly labeled inference>
```

Use the full output below for medium confidence, competing interpretations, product doctrine, and business intake. Low confidence routes to elicitation and blocks consequential action.

### Workflow Modes

- **Elicitation:** Recover what is already present. Ask only for the remaining human judgment, evidence, preference, or authority.
- **Bravo:** Name the inferred valued property before classifying the signal. Praise alone never authorizes preservation.
- **Friction:** Name the inferred desired correction before classifying the miss. Dissatisfaction alone never authorizes mutation.
- **Product doctrine:** Produce an operator-voiced articulation and classify it as `Vision`, `Product Hypothesis`, `Doctrine Candidate`, or `Approved Direction`. Never assign `Approved Direction` from interpretation alone; require explicit operator approval before repository edits.
- **Business intake:** Reflect the likely goal or constraint and require owner confirmation before placing it in a proposed context. Never infer economics, capacity, private facts, or approval; use `Missing` instead.

## Procedure

1. Read the operator's current message and only the recent context needed to interpret it.
2. Separate the literal statement from the likely concern, purpose, relationship, or direction beneath it.
3. Produce a clearer first-person articulation that the operator could adopt or correct.
4. Name the practical implication only when it follows from the interpretation.
5. Calibrate confidence. Preserve a meaningful alternative when more than one interpretation remains plausible.
6. Continue without a question when the interpretation is safe and the next step is reversible. Route consequential ambiguity to [elicitation](../elicitation/SKILL.md) before action.

Do not search unrelated project or private context merely to make an interpretation sound deeper. When the message refers to a repository fact, inspect the smallest relevant surface before treating that fact as part of the recovered intent.

## Output

Use natural prose for a simple request. When structure helps, use:

```text
Intent recovered:

What you said:
<literal or surface meaning>

What I think you mean:
<likely underlying intent>

Clearer articulation:
<concise first-person restatement>

Practical implication:
<what this changes, if anything>

Uncertainty:
<confidence, alternative interpretation, or confirmation needed>
```

If the operator says `go deeper`, explain the larger purpose, tension, identity, or system relationship implied by the message while keeping inference visibly separate from fact.

## Confidence And Escalation

- **High confidence:** Restate the intent directly and continue with any already authorized, reversible work.
- **Medium confidence:** State the leading interpretation and one material alternative. Ask only if the distinction changes the next action.
- **Low confidence or consequential action:** Do not choose for the operator. Use elicitation to clarify before changing files, contacting people, spending, publishing, or crossing a project membrane.

Intent recovery is interpretive preparation. It is never approval to execute.

## Guardrails

- Treat recovered intent as inference, not fact.
- Do not diagnose psychology, motives, health, or identity.
- Do not inflate every short message into a grand philosophy.
- Do not overwrite an explicit statement merely because another interpretation sounds more elegant.
- Do not infer publication, spending, hiring, customer-contact, persistence, or source-change authority.
- Do not convert private or project-local context into a general operator identity.
- Let the operator correct the restatement without defending the inference.
- Use `Missing` or ask a bounded question when the needed meaning is not actually present.

## Done When

The operator can recognize, reject, or refine a clearer articulation of what they were trying to express, and any resulting action remains inside its existing authority boundary.

Initial ROI appears as fewer unnecessary clarification questions, fewer wrong-layer repairs, clearer doctrine candidates, and zero authority-boundary violations. Treat these as human outcome signals, not claims proved by contract tests alone.
