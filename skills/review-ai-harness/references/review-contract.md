# Semantic Review Contract

Write one UTF-8 JSON object to `.harness-review/semantic-review.input.json`. Start from the generated template and preserve its `schema_version`, `scan_id`, and `baseline_fingerprint` exactly.

## Required shape

```json
{
  "schema_version": 1,
  "scan_id": "scan-generated-value",
  "baseline_fingerprint": "generated-value",
  "run_context": {
    "surface": {"value": "codex", "evidence": "VERIFIED"},
    "model": {"value": "unknown", "evidence": "INACCESSIBLE"},
    "sandbox": {"value": "workspace-write", "evidence": "VERIFIED"},
    "approval_mode": {"value": "unknown", "evidence": "INACCESSIBLE"}
  },
  "summary": {
    "headline": "One plain-English controlling judgment.",
    "what_helps": ["A concrete protection or useful route."],
    "what_gets_in_way": ["A concrete overlap, ambiguity, or coverage gap."]
  },
  "decisions": [
    {
      "action": "KEEP",
      "control_ids": ["ctl-generated-value"],
      "finding": "What the evidence shows.",
      "user_impact": "What the operator notices.",
      "proposal": "No change; preserve this control.",
      "evidence_paths": ["target-relative/path"],
      "risk": "What could go wrong if this judgment is wrong.",
      "approver": "repository-operator",
      "rollback": "Restore the reviewed baseline from Git.",
      "protections": ["The authority or safety property that must survive."],
      "confidence": "high"
    }
  ],
  "unreviewed_control_ids": ["ctl-generated-value"],
  "coverage_gaps": ["A relevant surface the review could not inspect."]
}
```

## Validation rules

- Use only `KEEP`, `ONE_HOME`, `LOAD_LATER`, `MAKE_A_CHECK`, `PROBATION`, or `RETIRE`.
- Use only `VERIFIED`, `USER_REPORTED`, `INFERRED`, `INACCESSIBLE`, or `NOT_APPLICABLE` as evidence labels.
- Use `high`, `medium`, or `low` confidence.
- Cite only target-relative paths present in the inventory.
- Assign each inventory control exactly once: in one decision group or in `unreviewed_control_ids`.
- Do not invent control IDs, evidence paths, owners, load receipts, model IDs, or tool activity.
- Group controls only when one finding, action, risk, protection set, and rollback truthfully applies to all of them.
- Put controls outside the semantic selection ceiling in `unreviewed_control_ids`; do not guess from metadata alone.
- A `KEEP` decision is not numbered as a change proposal. Every other action becomes a stable numbered proposal.
- Keep source content out of the JSON. Record judgments and paths, not copied bodies or secrets.
