---
name: business-plan
description: Discoverable repository adapter for governed owner-facing business planning. Use only when the operator explicitly invokes $business-plan create, $business-plan resume, or $business-plan change to create, continue, or revise an evidence-backed plan from an effective context.
---

# Business Plan Discovery Adapter

Treat `skills/business-plan/SKILL.md` as the canonical skill.

Before collecting private planning evidence:

1. Resolve the repository root containing this `.agents/skills` directory.
2. Read the canonical `skills/business-plan/SKILL.md` completely.
3. Read every canonical reference required by the selected mode.
4. Follow the canonical authority, evidence, scenario, approval, data, handoff, and no-repository-write boundaries.

Do not prepare a plan from this adapter alone. If the canonical skill or a required reference is missing or unreadable, stop before collecting private information and report `Hold` with the missing repository path.
