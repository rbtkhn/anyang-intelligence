# Governed Pattern Memory v1

## Lead Judgment

Anyang Intelligence may use deterministic retrieval to make approved learning
and sanitized project patterns easier to find, but retrieval does not create
memory authority. The recursive-learning ledger and governing project surfaces
remain authoritative for their declared operations. Every pattern-memory report
is a regenerable, review-only projection with `authority_effect: none`.

## Purpose And Scope

V1 supports pattern reuse inside
`anyang-internal / repository / internal-sanitized`. It searches:

1. `RL-*` entries whose state is `approved`, `implemented`, `validated`, or
   `observed`; and
2. tracked project `README.md`, `executive-os-install.md`,
   `operating-review.md`, and `membrane-notes.md` files.

It excludes tenant-private stores, archives, transcripts, source notes,
analyses, rejected, deferred, candidate, or superseded learning, untracked
files, external sources, and any source that fails repository containment,
allowlist, privacy, or membrane checks.

V1 does not capture conversations, call a model, create embeddings, inject
context into an agent, update canonical memory, promote a Skill, or write to a
project or learning ledger.

## Five Primitives

### Evidence spine

Every result carries a stable candidate ID, source tier, source lane, learning
state when applicable, repository-relative source reference, section, evidence
references, and SHA-256 content hash. A verifier must be able to reconstruct
the candidate from the current eligible corpus. Missing or changed evidence
invalidates reconstruction; a high retrieval score never repairs provenance.

### Derived projection

JSON is the machine projection and Markdown is a rendering of the same fields.
Neither is a peer record. Reports declare:

```text
schema: anyang-pattern-memory-report/v1
authority_effect: none
disposition: review-only
```

Repository-local reports may be written only beneath ignored
`generated-patterns/`. An explicit external output path is also permitted.
Existing files are not overwritten without `--force`.

### Budgeted retrieval

V1 returns no more than five results, no more than 1,000 source characters per
result, and no more than 4,000 source characters in total. Truncation and every
exclusion class are visible in the report. Retrieval uses deterministic local
BM25-style lexical scoring with exact learning-ID, phrase, heading, and lane
boosts. Stable ties resolve by source tier, source reference, then candidate
ID.

### Transactional compilation

The command completes source discovery, tracking checks, parsing, privacy and
membrane classification, ranking, budget enforcement, and rendering before it
writes. Output uses a same-directory temporary file and atomic replacement.
Invalid input, malformed governed learning, privacy failure, prohibited output,
or an unapproved collision writes no report.

### Shadow evaluation

Pattern results inform human review only. The pilot may claim structural
correctness after its tests pass, but not behavioral value. Advancement needs
a ten-query replay with at least eight expected patterns in the top five,
complete provenance reconstruction, and zero ineligible-state, private,
authority, membrane, automatic-promotion, or canonical-mutation incidents.
Human review records usefulness, false positives, missed patterns, and burden.

## Source Tiers And Membranes

`governed-learning` contains eligible operator-approved `RL-*` entries. A
non-sensitive learning may be classified `safe to transfer`; professional,
approval, or local-only terms tighten that posture.

`project-provisional` contains allowlisted sanitized project prose. Every
project result is at least `translate first` and requires human membrane review.
The full vocabulary is:

- `safe to transfer`
- `translate first`
- `approval required`
- `professional review required`
- `keep local`

`keep local` candidates are excluded before ranking. A generic transformation
is advisory and does not prove that private context has been removed.

## Interface

```powershell
.\tools\run.ps1 project pattern-memory query `
  --query "evidence-aware cross-project audit reuse" `
  --target-lane shared-primitives `
  --as-of 2026-08-04T18:00:00Z `
  --format markdown `
  --output generated-patterns/audit-reuse.md
```

All displayed arguments are required. `--format` accepts `markdown` or `json`.
`--repo` exists for controlled fixtures and defaults to the current repository.
`--force` authorizes only replacement of the named derived report.

The projection records the report and query digests, scope, target lane, as-of
time, corpus digest, ranked candidates, exclusions, warnings, limits, and
generation provenance. It never records a selection or outcome automatically.

## Promotion Boundary

```text
report candidate
  -> human membrane review
  -> separately authorized durable-learning decision
  -> existing RL or Skill workflow
```

The existing `extract-patterns` command remains available as the pilot
baseline and is not changed by this contract.

## Review And Retirement

Do not add embeddings until a measured lexical-recall gap justifies the added
model, privacy, version, and reproducibility contract. Narrow or retire the
pilot if false positives, review burden, or membrane risk exceeds demonstrated
reuse value.
