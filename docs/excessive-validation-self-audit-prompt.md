# Excessive Validation Self-Audit Prompt

Copy and paste everything inside the block below into an agent working at the
root of the repository to be audited.

```text
Audit this repository for excessive validation overhead.

Objective:
Determine what percentage of observable execution time is consumed by
validation, identify the dominant validation operations, and recommend a
safer, faster validation strategy without weakening release confidence.

Operating constraints:
1. Read and follow all repository instructions before running commands.
2. Treat the repository's canonical validation launcher as authoritative.
3. Begin read-only. Do not modify files, dependencies, Git state, CI, or the
   validation policy.
4. Preserve existing user changes.
5. Measure observable tool and process wall time only. Do not claim to measure
   hidden model reasoning or token-processing time.
6. Reuse existing evidence first:
   - recent command output;
   - test summaries;
   - CI logs;
   - validation caches;
   - retained temporary-file timestamps; and
   - existing timing reports.
7. Do not run another complete validation cycle merely to obtain prettier
   profiling data.
8. Time cheap validation phases independently when safe.
9. If existing evidence is insufficient, instrument and run the canonical
   full gate at most once. Explain why the run is necessary before doing it.
10. Do not invoke test runners directly when repository policy requires a
    wrapper or canonical launcher.

Audit procedure:
1. Locate the canonical validation entry point and enumerate every phase it
   executes, in order.
2. Determine whether phases run sequentially, concurrently, redundantly, or
   more than once during a normal change cycle.
3. Establish two denominators:
   - named validation time: the sum of measured validation phases; and
   - end-to-end task time: validation plus observable non-validation work.
4. For every validation phase, report:
   - elapsed seconds;
   - percentage of named validation time;
   - percentage of end-to-end time when measurable;
   - measurement source; and
   - confidence level: measured, reconstructed, or inferred.
5. Attribute test-runner time more deeply:
   - identify the slowest test files, groups, fixtures, setup operations,
     subprocesses, network calls, repository creation, timeouts, or
     platform-specific tests;
   - use existing duration data or retained timestamps before rerunning tests;
     and
   - distinguish measured timing from causal inference.
6. Identify repeated full-suite runs caused by small corrections and estimate
   their cumulative cost.
7. Look for:
   - integration tests embedded in the ordinary feedback loop;
   - repeated environment or bootstrap work;
   - duplicate structural checks;
   - validators scanning unaffected areas;
   - fixed sleeps and intentional timeout tests;
   - expensive per-test repository, database, or process setup;
   - validation reruns against content-equivalent repository states; and
   - caches invalidated by commit identity even though file content is
     unchanged.
8. Decide whether validation is excessive relative to the change that
   triggered it. State the basis for that judgment.

Required output:

A. Executive conclusion
- Is validation excessive: yes, no, or uncertain?
- What percentage of observable task time did validation consume?
- What was the single largest contributor?

B. Runtime breakdown
Provide a descending table with these columns:
Operation | Seconds | % of validation | % of task | Evidence | Confidence

C. Root causes
Separate:
- measured causes;
- strongly supported inferences; and
- unresolved possibilities.

D. Recommended validation policy
Design a fail-closed Fast/Full policy:
- Full remains the authoritative default unless repository requirements say
  otherwise.
- Fast is for bounded editing feedback.
- Define exact path classes eligible for Fast.
- Map eligible paths to focused tests and structural validators.
- Always retain essential integrity, privacy, and security checks.
- Automatically escalate unknown, renamed, deleted, runtime, dependency,
  schema, validation-tooling, security-boundary, or cross-repository changes
  to Full.
- Require Full before merge, release, deployment, or repository-wide
  "validated" claims.
- Set explicit latency budgets for Fast and Full.
- Print selected checks, routing reasons, phase timings, and effective mode.
- Cache successful Full results only against a content-equivalent repository
  plus relevant runtime fingerprint.
- Do not invalidate the cache solely because the same validated content was
  committed.
- Provide an explicit force-rerun option.

E. Optimization opportunities
Rank each recommendation by:
- expected time saved;
- implementation effort;
- confidence; and
- safety risk.

F. Proposed next step
Recommend the smallest change that improves future evidence, usually phase
timing, before proposing broad routing changes.

Important:
- Do not implement recommendations during this audit.
- Do not describe a failed validation run as evidence that an optimization
  works.
- Report flaky or load-sensitive tests separately from failures caused by the
  audited change.
- Preserve complete coverage in the Full gate.
- Be explicit about limitations and uncertainty.
```

The prompt deliberately starts with existing evidence so the audit does not
reproduce the validation cost it is meant to investigate.
