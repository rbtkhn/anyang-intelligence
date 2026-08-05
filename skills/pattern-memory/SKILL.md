---
name: pattern-memory
description: Run and inspect Anyang Intelligence governed pattern-memory reports over approved RL learning and allowlisted sanitized project surfaces. Use when the operator invokes pattern-memory, asks what Anyang has learned about a topic, requests reusable or cross-project patterns, wants an evidence-linked pattern search, or asks to inspect or evaluate a generated pattern-memory report.
---

# Pattern Memory

Find reusable operating patterns without turning retrieval into durable memory,
authority, or automatic Skill promotion.

When working inside `anyang-intelligence/operating-substrate`, this skill is
authoritative for the pattern-memory CLI workflow. Read
[`docs/governed-pattern-memory-v1.md`](../../docs/governed-pattern-memory-v1.md)
before running or interpreting a report.

## Modes

- **Query:** Generate a new ignored report from a sanitized topic.
- **Inspect:** Read and assess an existing report without changing it.
- **Evaluate:** Compare retrieval quality across a bounded query cohort. Do not
  represent structural or replay success as human usefulness.

If the request is only explanatory, answer from the RFC without generating a
report.

## Query Workflow

1. Confirm the Git root is `operating-substrate`.
2. Translate the request into a short sanitized query. Do not place names,
   contact details, credentials, customer facts, learner/family facts, private
   financial information, restricted property details, or source excerpts in
   the query.
3. Choose the receiving lane from the request. Use `shared-primitives` only for
   an explicitly cross-project or repository-level search.
4. Use the current offset-aware ISO 8601 timestamp as `--as-of` unless the
   operator names a historical boundary.
5. Write beneath ignored `generated-patterns/` with a descriptive `.md` or
   `.json` name. Do not use `--force` unless the operator explicitly authorizes
   replacement of that exact derived report.
6. Run:

   ```powershell
   .\tools\run.ps1 project pattern-memory query `
     --query "<sanitized query>" `
     --target-lane <receiving-lane> `
     --as-of <offset-aware-timestamp> `
     --format markdown `
     --output generated-patterns/<report-name>.md
   ```

   On macOS or Linux, use `python3 tools/run_repo.py project pattern-memory
   query` with the same arguments.
7. Read the generated report and assess it using the inspection rules below.

## Inspection Rules

For each top result, distinguish:

- **Strong:** directly answers the query and preserves a useful evidence spine.
- **Adjacent:** relevant but needs translation or narrower framing.
- **Noise:** matched vocabulary without adding decision value.

Check:

- `authority_effect` is `none` and `disposition` is `review-only`;
- the source tier and learning state are eligible;
- the source reference, content hash, and evidence references are present;
- project-derived results remain `project-provisional` and require human
  membrane review;
- `keep local` material did not enter the ranked results;
- truncation, exclusions, and budgets are visible;
- transformed wording did not become awkward or change the source meaning.

Lead with the usefulness judgment, then identify the strongest patterns, false
positives, missing evidence, and the boundary on reuse. Link the local report.

## Promotion Boundary

Retrieval is not retention. Always preserve:

```text
report candidate
  -> human membrane review
  -> separately authorized durable-learning decision
  -> existing RL or Skill workflow
```

Do not create or update an `RL-*` entry, Skill, template, project document,
canonical ledger, prompt injection, or recommendation order from a report. A
request to preserve or implement a candidate is a separate action with its own
governing Skill, evidence, and authority.

## Output Shape

```text
Pattern-memory result:
<one-sentence usefulness judgment>

Strong matches:
- <pattern and source>

Noise or limits:
- <false positive, missed pattern, truncation, or provenance gap>

Boundary:
- Review-only; no memory promotion or execution authority.

Report:
- <clickable local report>
```

## Done When

The operator can see what was retrieved, why it may be reusable, how to reach
its evidence, what was noise, which membrane applies, and that no durable state
or execution authority changed.
