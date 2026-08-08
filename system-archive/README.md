# System Archive

The system archive is the repository-level map for archive and source-history
surfaces in Anyang Intelligence.

This index does not move existing archive files yet. It names the archive
domains, preserves their current canonical paths, and records which shelves are
active, historical, or parked. A later migration may move archive contents under
this directory after tooling, validators, and links are updated.

## Purpose

Archive material preserves source evidence, source notes, transcript-derived
analysis, recurrence reviews, and historical shelves that may inform product
judgment, governance warnings, and reusable operating primitives.

Archive material is not automatically:

- public content
- customer-facing copy
- reusable doctrine
- rights-cleared source material
- approval to move private or sensitive context across membranes

## Current Domains

See [archive-manifest.yaml](archive-manifest.yaml) for the controlled index.

| Domain | Current path | Status | Role |
| --- | --- | --- | --- |
| `singularity-science` | `system-archive/singularity-science/` | active | Singularity Science source archive and intake lane material. |
| `ai-frontier` | `system-archive/ai-frontier/` | historical/parked | Earlier AI frontier archive shelf retained for lineage until reviewed. |

## Boundary

Source bodies and transcripts stay inside their archive domain unless a
governed workflow creates original synthesis, an approved implication note, or a
tested operating primitive. Private customer, learner, financial, or sensitive
real-world records stay in operator-controlled tenant-private storage rather
than this archive index.

## Migration Rule

Until a migration is explicitly approved and validated, active tooling continues
to use the current paths listed in the manifest. Do not create a second live
copy of an archive domain under `system-archive/`; that would split authority.
