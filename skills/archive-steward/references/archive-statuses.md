# Archive Statuses

Use these labels when classifying archive shelves, lanes, source packets, or
migration remnants.

## Canonical

The governing manifest or README names this as the current source of truth for
the shelf or lane. Active tools and docs should target this path.

## Candidate

The material may become canonical, but ownership, lane mapping, rights,
metadata, or structure remains unresolved. Candidate status should name the
approval or evidence needed.

## Parked

The material is intentionally retained but not currently active. Parked shelves
must state whether they are empty, historical, awaiting review, or held for
lineage.

## Historical

The material records prior state, old analysis, previous locations, or obsolete
workflow outputs. Historical material may remain useful for audit but should not
govern current tooling unless explicitly named.

## Derived

The material was generated from other artifacts, such as ledgers, reports,
indexes, snapshots, or validation outputs. Derived material should identify its
source or generation process when possible.

## Quarantined

The material is retained but should not be reused without review because of
rights uncertainty, privacy risk, provenance failure, corruption, suspected
duplication, or safety concern. Quarantined status must name the blocker.

## Tombstone

The path exists to redirect readers from an old location to the current one or
to explain why content was removed, moved, or never tracked there. Tombstones
are not active archive shelves unless the manifest says so.
