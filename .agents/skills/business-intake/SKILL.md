---
name: business-intake
description: Discoverable repository adapter for governed owner-facing business intake. Use only when the operator explicitly invokes $business-intake create, $business-intake resume, or $business-intake change to establish, continue, or revise an approved business context.
---

# Business Intake Discovery Adapter

Treat `skills/business-intake/SKILL.md` as the canonical skill.

Before asking business questions:

1. Resolve the repository root containing this `.agents/skills` directory.
2. Read the canonical `skills/business-intake/SKILL.md` completely.
3. Read every canonical reference and project-specific question set required by the selected mode.
4. Follow the canonical skill exactly, including its authority, data, approval, persistence, financial-routing, and no-repository-write boundaries.

Do not conduct intake from this adapter alone. Do not duplicate or reinterpret the canonical workflow here. If the canonical skill or a required reference is missing or unreadable, stop before collecting private business information and report `Hold` with the missing repository path.
