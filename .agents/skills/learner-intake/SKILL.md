---
name: learner-intake
description: Discoverable repository adapter for governed Learning Core learner intake. Use when the operator invokes $learner-intake create or $learner-intake change, asks to onboard a learner, establish an initial learner profile, review new learner evidence, or propose a guardian-approved profile revision.
---

# Learner Intake Discovery Adapter

Treat `skills/student-operating-system/learner-intake/SKILL.md` as the canonical skill.

Before asking intake questions:

1. Resolve the repository root containing this `.agents/skills` directory.
2. Read the canonical `skills/student-operating-system/learner-intake/SKILL.md` completely.
3. Read every canonical reference that its selected mode requires, resolving relative paths against the canonical skill directory.
4. Follow the canonical skill exactly, including its authority, privacy, approval, persistence, and no-repository-write boundaries.

Do not conduct an intake from this adapter alone. Do not duplicate or reinterpret the canonical workflow here. If the canonical skill is missing or unreadable, stop before collecting learner information and report `Hold` with the missing repository path.
