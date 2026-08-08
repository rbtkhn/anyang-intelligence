# Agent Memory Phase 1 Acceptance

**Version:** 1
**Status:** pending review
**Authority effect:** `none`
**Phase 2 authorized:** false

## Scope delivered

Phase 1 contains an advisory constitution, conformance specification, kernel
specification, disabled machine-readable manifest, read-only validator,
focused contract tests, and canonical validation routing.

## Explicit exclusions

Phase 1 does not inspect sessions, create private storage, configure a database,
ingest events, generate candidates, infer preferences, retrieve memory, inject
context, activate a skill, add an automation, or claim recursive-learning ROI.

## Acceptance checklist

### Documentation

- [ ] Versions and terminology agree across all documents.
- [ ] Every normative rule has a stable `AMC-*` identifier.
- [ ] Specification, implementation, validation, activation, and observation
  remain distinct.

### Machine contract

- [ ] Every required rule family exists and identifiers are unique.
- [ ] Every rule maps to an article and planned test.
- [ ] Runtime, collection, ingestion, promotion, retrieval, and automatic
  injection remain disabled.
- [ ] Storage is unconfigured and authority effect remains `none`.

### Safety and privacy

- [ ] No session body was read or retained for Phase 1.
- [ ] No private path, personal fact, database, or runtime artifact entered Git.
- [ ] Validator success grants no operational authority.
- [ ] Privacy validation passes.

### Validation

- [ ] Focused contract tests pass.
- [ ] The contract validator passes deterministically.
- [ ] Full repository validation passes.
- [ ] The diff remains inside the declared Phase 1 paths.

## Open design questions

- The exact private storage location is not authorized.
- The source corpus and collection declarations are not approved.
- The Phase 2 schema and migration are not implemented.
- The first shadow task cohort is not selected.

## Human disposition

The operator must separately choose `adopt`, `revise`, `reject`, or `defer`.
Completion of this checklist does not authorize Phase 2.
