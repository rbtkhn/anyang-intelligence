---
name: intent-recovery
description: Discoverable repository adapter for recovering and clearly restating the operator's underlying intent. Use only when the operator explicitly invokes $intent-recovery.
---

# Intent Recovery Discovery Adapter

Treat `skills/intent-recovery/SKILL.md` as the canonical skill.

1. Resolve the repository root containing this `.agents/skills` directory.
2. Read the canonical skill completely.
3. Follow its interpretation, confidence, elicitation-routing, and authority boundaries exactly.

Do not recover intent from this adapter alone. If the canonical skill is missing or unreadable, report that `$intent-recovery` is unavailable rather than improvising a replacement contract.
