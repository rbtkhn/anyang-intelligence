# Embodied AI Parent Review Worksheet

This is a parent-review worksheet for any child-facing robot, kiosk, embodied tutor, or similar device considered inside the Learning Core lane.

Its job is to slow down novelty pressure, preserve parent authority, and make the review questions concrete before any use is treated as normal, safe, or plan-worthy.

Use with:

- [embodied-ai-hold-policy.md](embodied-ai-hold-policy.md)
- [parent-approval-record.md](parent-approval-record.md)
- [hold-response-template.md](hold-response-template.md)
- [plan-drafting-gate.md](plan-drafting-gate.md)

## Operating Rule

Default result is `Hold` until this worksheet is clear enough for a parent-approved next step.

This worksheet is for review, not adoption.

## When To Use

Use this worksheet when:

- a parent asks whether a child-facing robot or embodied tutor should be added to the plan
- an operator wants to review a child-facing embodied device separately from the main plan
- a device seems interesting, but the supervision, privacy, authority, or override layer is still unclear

Do not use excitement, marketing language, or general futurist claims as a substitute for these answers.

## Parent Review Worksheet

```text
Embodied AI Parent Review Worksheet

Device or system:
Date reviewed:
Parent or guardian reviewer:

1. Why are we considering this?
- What problem do we think this device might help with?
- What seems attractive about it right now?

2. Why embodiment?
- Could this same need be met with a software-only tool, parent-led activity, tutor, book, or simpler routine?
- If not, what makes the physical / voice / present-in-the-room element important?

3. Child-facing role
- How might the child understand this device's role?
- Could the child mistake it for a teacher, evaluator, or authority figure?
- What language should be used so the child does not over-trust it?

4. Adult authority
- What adult remains clearly in charge during use?
- Who decides when it is used, paused, changed, or removed?
- Would any part of the experience be unsupervised?

5. Privacy and sensing
- What does the device record, sense, store, or send?
- What do we know versus not know yet?
- What is not allowed to be recorded or shared?

6. Human override
- How is the device stopped, muted, unplugged, removed, or disabled?
- Could the child stop it alone, or must an adult do that?
- What happens if it behaves strangely or creates discomfort?

7. Main concerns
- Does it raise concerns about safety, overstimulation, surveillance, attachment, authority, behavior scoring, or false instructional confidence?
- What concern matters most right now?

8. Review decision
- Keep at Hold
- Review again later
- Consider only a very small parent-supervised test

9. If a small test is ever considered
- Exact use case:
- Duration:
- Adult present:
- What would stop the test immediately:
- What would count as "not a fit":

10. Notes for the approval record
- What was approved:
- What was not approved:
- What remains unclear:
```

## Short Parent-Facing Prompt

Use this when the parent wants a lighter way to review:

```text
Before we consider a child-facing robot or embodied tutor, I would want to clarify:

- what exact problem it is meant to solve
- why embodiment is needed instead of a simpler tool
- what the child would think its role is
- what adult stays clearly in charge
- what it records or senses
- how it is stopped or removed if it creates confusion or discomfort

Until those answers are clear, I would keep it in Hold.
```

## How To Use The Result

If the worksheet is incomplete or raises new concerns:

- keep the device at `Hold`
- use [hold-response-template.md](hold-response-template.md) if a parent-facing pause message is needed
- do not insert the device into the plan

If the worksheet is complete and the parent still wants a small test:

- record the decision in [parent-approval-record.md](parent-approval-record.md)
- keep the test narrow, supervised, and reversible
- do not treat a test as standing approval for future use

## Boundary

This worksheet does not recommend purchase, use, or educational value.

It is a review artifact for preserving child safety, parent authority, and truthful decision-making when embodied AI is proposed.
