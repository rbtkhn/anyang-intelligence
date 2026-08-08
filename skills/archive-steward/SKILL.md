---
name: archive-steward
description: Governed archive and library stewardship for source collections, intake, manifests, tombstones, migrations, lane catalogs, provenance, retention, duplicate detection, and read-only archive audits. Use when Codex needs to establish, inspect, land, consolidate, migrate, or route archive contents under system-archive or another governed archive root without collapsing source attribution, rights status, or project authority.
---

# Archive Steward

Use this skill when the work is about the archive as an archive: shelves,
catalogs, manifests, paths, tombstones, lineage, intake safety, migration
safety, duplicate detection, retention status, or archive-readiness.

This skill is the librarian and migration governor. Domain skills remain the
analysts. For Singularity Science interpretation, intake analysis, recurrence,
or learning updates, use the relevant Singularity skill after this skill has
settled the archive surface.

## Core Law

`archive root -> shelf -> lane or collection -> source packet -> derived artifacts -> downstream receipt`

Preserve the distinction between source material, metadata, analysis, ledgers,
receipts, and doctrine. A better catalog does not create stronger evidence,
rights certainty, publication authority, customer authority, or doctrine.

## First Read

When present, read these before changing or judging archive structure:

1. `system-archive/README.md`
2. `system-archive/archive-manifest.yaml`
3. the shelf README, for example `system-archive/<shelf>/README.md`
4. any lane README, ledger, or manifest directly governing the requested shelf

Read [references/archive-statuses.md](references/archive-statuses.md) when
assigning or revising archive status labels.

## Modes

Choose the narrowest mode that satisfies the request.

### Inspect

Inventory the requested archive root, shelf, or lane. Report current paths,
manifest entries, lane names, tombstones, ledgers, untracked or empty shelves,
and unresolved ambiguity. Do not edit.

### Establish

Create a new archive root, shelf, lane, or manifest only when explicitly
authorized. Include a README or manifest entry that names purpose, status,
owner or governing skill, allowed contents, excluded contents, and downstream
handoff boundary.

### Intake

Land a neutral source packet only when the source body or source object is
already present. Confirm shelf, lane or collection, source title, source date,
ingest date, source URL or explicit unavailable status, rights status, capture
method, provenance, source type, planned path, manifest row, and downstream
governing skill.

Preflight duplicate URL, duplicate planned path, missing body, ambiguous shelf
or lane, path escape, and rights uncertainty before writing. If any of these
are unresolved, stop with a hold receipt rather than creating a partial archive
object.

Preserve source material with minimal transformation. Apply deterministic
cleanup only when the shelf has an explicit rule. Do not summarize, synthesize,
classify claims, or create doctrine during intake.

For large source bodies, use a bounded sidecar or script-based landing route
when one exists. If no safe landing route exists, stop and propose the smallest
safe landing plan instead of attempting a fragile write.

End with an intake receipt: landed path, manifest path, transformations
applied, unresolved uncertainty, validation, and next governing skill.

### Consolidate

Compare shelves or lanes for overlap. Identify duplicates, parked material,
historical surfaces, generated derivatives, stale pointers, and likely
canonical locations. Do not merge distinct sources merely because their themes
match.

### Migrate

Move archive material only with explicit migration authority. Use tracked moves
when possible. Preserve old-path discoverability with a tombstone, manifest
history, or clear pointer. After moving, update active references and classify
remaining old references as one of: active blocker, tombstone, generated,
historical, or external.

### Repair

Fix broken active links, stale manifests, missing README pointers, duplicated
status language, or lane catalog drift. Keep repairs mechanical unless the
operator separately asks for domain interpretation.

### Query

Answer archive inventory questions from local files. Prefer `rg`, manifests,
README files, and ledgers. Separate confirmed tracked contents from inferred,
untracked, generated, or missing contents.

## Required Checks

For structural edits, run the smallest relevant checks first, then broaden if
the change touches shared governance:

- path/reference scan for old and new paths;
- `git status --short` to confirm unrelated work stays separate;
- any archive-specific CLI or dry run named by the governing skill;
- repository validators when manifests, bounded agency, analytical interfaces,
  or shared docs changed.

Report validators that were not run and why.

## Boundaries

Do not:

- interpret source claims beyond what is needed to classify archive structure;
- establish rights certainty;
- fetch or ingest new sources unless another invoked workflow permits it;
- land source stubs, summaries, or routing notes as if they were source packets;
- promote archive material into doctrine, memory, or customer/project state;
- collapse domain archives into a generic library without preserving governing
  skill, source provenance, and authority boundaries;
- delete parked, historical, generated, or duplicate material without explicit
  delete authority.

## Completion Report

End archive-steward work by naming:

- archive root and shelf touched or inspected;
- mode used;
- canonical paths and parked or historical paths;
- source packet, manifest, README, tombstone, or ledger changes;
- intake receipt fields when source material was landed;
- unresolved gaps or ambiguity;
- validation performed;
- what remains governed by a domain-specific skill.
