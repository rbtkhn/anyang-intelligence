# Mock Ready Plan Evidence Map

This fixture runs the `Ready` case from [mock-intake-simulations.md](mock-intake-simulations.md) through [plan-drafting-gate.md](plan-drafting-gate.md) and [plan-draft-evidence-map.md](plan-draft-evidence-map.md).

This is not a real learner plan. It is an internal traceability test that asks whether a future 30-day plan draft could be supported without inventing learner facts.

## Source Scenario

- Scenario: Structured New Homeschool Parent
- Intake status: `Ready`
- Parent approver: parent
- Privacy boundary: parent notes, portfolio photos, and proud work may be saved; nothing shared outside the household without parent approval
- Accountability boundary: parent handles homeschool requirements separately; the plan supports daily learning only

## Drafting Gate Result

Gate status: `Pass for internal draft preparation`

Reason:

- Parent goal is stated.
- Approval authority is clear.
- Privacy and sharing boundaries are clear.
- Basic learner context is present.
- Schedule and parent-time range are known.
- Current resources, Khan Academy Kids decision, reading basket status, and portfolio approach are known.
- Parent approval before plan use is explicit.

Limit:

- This fixture does not create the parent-facing 30-day plan.
- It only tests whether the evidence map can trace major draft sections to approved sources.

## Evidence Map Header

- Learner or label: mock learner from Scenario 1
- Intake status: `Ready`
- Draft date: mock fixture
- Operator: Anyang Intelligence internal test
- Parent approver: parent
- Missing-input list attached: `no material missing inputs for draft preparation`
- Assumptions attached: `not needed`

## Evidence Map

| Plan section | Draft claim or structure | Source label | Evidence note | Open risk or approval needed |
| --- | --- | --- | --- | --- |
| Plan status | Ready | Parent Input | Scenario classifies intake as `Ready`; parent approval and core inputs are present. | Parent still approves final plan before use. |
| Parent goal | Calm learning rhythm and pride in daily work | Parent Input | First-month goal stated directly by parent. | None for draft; parent reviews wording. |
| Inputs checked / missing inputs | Goal, authority, privacy, learner context, schedule, resources, app, reading basket, portfolio | Parent Input | All required readiness categories are present in Scenario 1. | Screen-time budget is not explicitly named; keep app rule at parent-approved 15 minutes unless parent adds broader budget. |
| Parent authority and safety | Parent approves plan; no outside sharing without approval | Parent Input | Approver and privacy boundary are explicit. | Parent reviews child-facing prompts before use. |
| Week 0 / before start | Confirm goal, privacy, app rule, reading basket, portfolio, weekly review | Template Default | These are template onboarding steps that do not add learner-specific claims. | Mark only as planned unless parent confirms completion. |
| Week 1 setup | Gentle rhythm introduction with observation and light evidence | Template Default | Template supports low-pressure setup. | Parent approves final rhythm and evidence load. |
| Interests | Animals, rocks, nature walks, drawing, building with blocks | Parent Input | Listed directly in mock parent response. | Do not add extra interests. |
| Strengths | Drawing notebook and identifying birds outside | Parent Input | Parent named proud work and observable interest. | Avoid converting pride into broad ability claims. |
| Friction or support signals | Avoids long independent reading and math worksheets | Parent Input | Parent named reading and worksheet friction. | Do not infer reading level, math level, or diagnosis. |
| Parent constraints | Monday-Thursday mid-morning; 45 minutes light day, 90 minutes fuller day | Parent Input | Schedule and parent-time reality are directly stated. | No screen-time budget beyond app limit; ask later if needed. |
| Evidence quality | Medium to strong for draft preparation | Parent Input | Parent supplied multiple learner, schedule, resource, and approval signals. | Final plan should still say these are starting observations. |
| Minimum viable day | Short reading/look-at-books, optional 15-minute app block, one hands-on activity, one parent note | Template Default | Structure comes from template and fits parent time. | Keep app inside the approved 15-minute rule. |
| Standard day | Reading, 15-minute Khan Academy Kids, hands-on math, nature/drawing/building, movement, parent note | Parent Input | Activity categories trace to stated resources/interests/app approval. | Parent approves final daily order and time blocks. |
| Fuller day option | Longer read-aloud, nature walk, drawing/building project, hands-on math game | Parent Input | Uses stated interests, resources, and fuller-day parent time. | Do not make fuller day the default expectation. |
| Week 1 focus | Settle into gentle rhythm and observe what sparks engagement | Template Default | Onboarding focus is generic and safe. | Parent approves child-facing language. |
| Week 2 focus | Repeat what worked and adjust reading/math friction | Parent Input | Tied to named friction and parent goal. | Avoid framing as remediation unless parent chooses that language. |
| Week 3 focus | Build confidence through nature/drawing/building project work | Parent Input | Tied to interests and proud work. | Keep project scope realistic for parent time. |
| Week 4 focus | Review portfolio evidence and choose next-month focus | Template Default | Monthly review is established in the template. | Parent decides next-month direction. |
| Reading basket plan | Animal books, easy readers, parent read-aloud; add confidence/current/stretch structure | Parent Input | Parent named available reading resources and reading comfort. | Do not invent exact titles. |
| Khan Academy Kids use rule | 15 minutes on learning days, parent-supervised, observation/practice only | Parent Input | Parent approved installed app and 15-minute supervised use. | Do not treat app progress as mastery, grade, diagnosis, or full curriculum. |
| Portfolio evidence plan | Physical folder plus parent phone photos; parent decides saves; child may choose proud work weekly | Parent Input | Portfolio approach is directly stated. | Parent approves what gets saved and shared. |
| Weekly parent review | Review enjoyment, resistance, proud work, what to repeat/pause/watch | Template Default | Generic review prompts from template. | Parent chooses review time and final prompts. |
| Monthly portfolio review shape | Proud work, milestones, interests, friction, next steps | Template Default | Monthly review structure from template. | Parent approves what becomes part of review memory. |
| Watch items / support signals | Reading avoidance and worksheet frustration, no high-stakes concern named | Parent Input | Parent named watch items and did not name high-stakes concern. | Do not escalate tone or introduce new concerns. |
| Parent decisions needed | Daily rhythm, app rule, reading basket, portfolio, weekly review questions | Parent Input | Parent explicitly wants to approve these areas. | Plan is not used until parent approval. |
| Next-month options | Continue, refresh reading basket, deepen profile, focus on reading/math/writing/projects/routine, revise plan, or pause | Template Default | Template options are non-specific and parent-choice based. | Parent chooses after month-end evidence. |

## Gate Findings

The `Ready` scenario can move to internal draft preparation because the evidence map can support the major draft sections without invented learner facts.

The strongest source-backed plan directions are:

- calm mid-morning rhythm
- parent-supervised 15-minute Khan Academy Kids block
- animal/nature/drawing/building interests
- hands-on math instead of worksheet-heavy math
- light portfolio evidence chosen by parent and child
- weekly review with parent approval

## Do Not Draft Yet If

Pause before a real parent-facing plan if any of these become true:

- the parent changes privacy or save/share rules
- the parent introduces a screen-time budget that conflicts with the app rule
- the parent adds legal, district, evaluator, or accountability requirements
- the parent names a high-stakes support concern
- the operator cannot trace a learner-specific line to the evidence map

## Recursive Learning

The evidence map caught one useful missing nuance: even a `Ready` case may lack a broader screen-time budget. The safe action is not to invent one; keep the app inside the parent-approved 15-minute rule and ask later if a broader budget matters.
