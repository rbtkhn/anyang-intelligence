# The File Extension Does Not Decide Which Record Governs

Title rationale: The repository needs an authority rule, not a format preference: SQLite, XLSX, and CSV serve different operations, and none becomes canonical merely by existing.

## Lead Judgment

SQLite should govern transactional operating state, XLSX should govern human-reviewed analysis and reconciliation when a workbook is explicitly designated authoritative, and CSV should carry source snapshots or interchange data. Git stores the reusable rules around these formats—not private operating records by default.

## Controlling Object

Whether every stored fact has one declared authority, a visible provenance path, and a controlled route between machine state, human review, and portable exchange without creating competing sources of truth.

## One Authority per Decision

Authority belongs to a declared record and purpose, not to a file extension. Before using a dataset, identify:

- what decision or workflow it supports;
- whether it is a source, canonical state, review surface, or export;
- who may edit, approve, reconcile, publish, or delete it;
- what evidence and timestamp establish freshness;
- which downstream files are derived and therefore must not be edited as peers.

When two files claim the same authority, stop and reconcile them. Do not choose the newest timestamp, largest file, or most polished presentation without evidence.

## SQLite Holds Transactional Operating State

SQLite is the canonical control plane for state that changes through governed events: tenants, actors, authority grants, sources, claims, work, evidence, approvals, outcomes, learning events, cadence handoffs, and cadence measurements.

Use SQLite when the system needs:

- typed records and relational constraints;
- atomic state transitions;
- append-only events or durable audit history;
- deterministic queries and generated reviews;
- multiple workflows reading the same current state;
- migrations that preserve schema evolution.

SQLite rules:

- Store operational databases outside the repository through `ANYANG_DATA_DIR` or an explicit external `--db` path.
- Treat generated Markdown, JSON, CSV, or XLSX reports as views unless a separate contract explicitly grants them authority.
- Do not edit database files manually or resolve disagreement by copying one `.db` file over another.
- Keep `.db`, `.db-wal`, and `.db-shm` files out of Git; repository history is not a database backup.
- Back up SQLite only through an operator-approved encrypted process that preserves the database and relevant write-ahead-log state safely.

## XLSX Holds Human-Reviewed Analysis and Reconciliation

XLSX is appropriate when a human must inspect assumptions, formulas, classifications, checks, exceptions, and evidence gaps in one auditable review surface. A workbook may be authoritative for a bounded analytical process—such as the internal finance ledger—when its documentation names it explicitly.

Use XLSX when the work needs:

- formulas and visible checks;
- typed dates, currency, rates, and periods;
- reviewable assumptions and reconciliation status;
- multiple sheets separating inputs, calculations, checks, and sources;
- a presentation surface that an accountable human can approve or correct.

XLSX rules:

- Name whether the workbook is authoritative, provisional, or derived.
- Keep raw inputs separate from calculations and outputs.
- Surface failed checks rather than smoothing incomplete records into a passing summary.
- Record version, owner, effective period, source references, and reconciliation status.
- Do not treat workbook formatting, formulas, or totals as evidence of approval.
- Keep workbooks containing real financial, customer, learner, donor, contractor, property, or security-sensitive records outside Git unless a sanitized publication artifact receives explicit approval.

## CSV Carries Source Snapshots and Interchange Data

CSV is a portable row-and-column exchange format. It is useful for imports, exports, manifests, source snapshots, deterministic fixtures, and simple append-only feeds. It lacks workbook formulas, relational constraints, types, access control, and embedded review state.

Use CSV when the system needs:

- a stable import or export boundary;
- compatibility across tools;
- a small, inspectable source snapshot;
- deterministic synthetic test data;
- row-wise data that does not require formulas or multiple related tables.

CSV rules:

- Declare whether the file is an input, export, snapshot, fixture, or authoritative ledger.
- Preserve headers, encoding, delimiter, units, and date conventions.
- Add stable row identifiers when records require discussion, evidence, or reconciliation.
- Do not maintain `Copy`, `Final`, or date-suffixed variants as competing writable ledgers.
- Archive divergent sources until evidence resolves them; never overwrite a conflict silently.
- Treat blank dates, missing evidence references, and unreconciled classifications as explicit failures.
- Scan CSV and TSV content for prohibited identifiers before commit. Real operating exports remain outside Git by default.

## Adjacent Formats Complete the Data Lifecycle

SQLite, XLSX, and CSV form the central state/review/exchange axis, but several adjacent formats carry intent, events, transformations, analytical snapshots, evidence, or runtime configuration.

| Format | Primary role | Authority posture | Git default |
| --- | --- | --- | --- |
| YAML (`.yaml`, `.yml`) | Human-readable manifests, loop definitions, policy configuration, and fixtures | Declarative intent or import instruction; it does not prove that execution occurred | Track reusable, sanitized contracts and synthetic fixtures |
| JSON (`.json`) | Machine interchange, API payloads, manifests, and generated snapshots | Source or derived snapshot; declare provenance, generation time, and whether edits may flow back | Track schemas, deterministic fixtures, and sanitized manifests; keep private exports external |
| JSONL / NDJSON (`.jsonl`, `.ndjson`) | Append-only event streams, diagnostics, inspection output, and bulk interchange | Event history or derived diagnostic output; ordering and append semantics matter | Track only synthetic fixtures or approved public data; ignore real logs and private event streams |
| TOML (`.toml`) | Package, tool, and repository configuration | Governs tool behavior, not operating facts | Track when it is the selected tool's configuration source |
| Lockfiles (`.lock` and tool-specific variants) | Exact dependency or environment resolution | Canonical for reproducible dependency selection under the named package manager | Usually track; regenerate only through the owning tool |
| SQL (`.sql`) | Schemas, migrations, constraints, and controlled transformations | Governs database structure or repeatable mutations; it is not current database state | Track reviewed migrations and reusable queries; never embed secrets or private exports |
| Parquet / Arrow (`.parquet`, `.arrow`, `.feather`) | Typed, compressed analytical snapshots and data-lake partitions | Derived analytical storage unless a data-platform contract declares otherwise | Usually external; track schema, source query, as-of time, partition rules, and checksum instead |
| PDF (`.pdf`) | Immutable evidence, issued statements, signed records, or approved publications | Authority depends on issuer, signature, provenance, and purpose—not immutability alone | Track only approved public or sanitized publications; private evidence remains external |
| Environment files (`.env`) | Runtime configuration and secrets | Local runtime input, never an operating record | Never track real values; track only a sanitized `.env.example` |
| Logs (`.log`) | Diagnostic and execution history | Operational evidence with bounded retention, not canonical business state | Ignore by default; preserve only sanitized incident excerpts or synthetic fixtures |
| Bundles and backups (`.zip`, `.bak`, `Copy`, `Final`) | Transfer or recovery artifacts | No inherent authority; duplicates commonly conceal divergence | Keep external and inventory them; do not treat naming or modification time as reconciliation |
| SQLite sidecars (`.db-wal`, `.db-shm`) | Write-ahead and shared-memory state for a live SQLite database | Part of the database consistency boundary, not independent records | Never commit or copy independently; use a SQLite-safe backup procedure |
| Markdown (`.md`) | Governance contracts, narrative analysis, generated reviews, and approved summaries | Doctrine or reader-facing view; normally not transactional state | Track when sanitized and intentionally durable |

These formats do not replace the central authority decision. YAML may instruct an import, JSON may describe its result, SQLite may hold the accepted state, XLSX may support human reconciliation, CSV may carry a portable extract, Parquet may support analysis, and PDF may preserve an issued conclusion. Each remains bounded to its declared operation.

## Controlled Movement between Formats

| Movement | Permitted role | Required control |
| --- | --- | --- |
| CSV → SQLite | Import source into transactional state | Validate schema, identifiers, types, provenance, privacy, and duplicate handling before mutation |
| SQLite → CSV | Portable export or integration feed | Mark the export derived, record its generation time, and prevent edits from silently flowing back |
| SQLite → XLSX | Human review or analytical report | Preserve query/as-of metadata and keep the database authoritative unless the contract says otherwise |
| CSV → XLSX | Reconciliation or analysis | Preserve the source snapshot, add audit fields and visible checks, and declare workbook authority explicitly |
| XLSX → CSV | Flattened export | State which sheet/range produced it and accept that formulas, formatting, comments, and controls are lost |
| XLSX → SQLite | Approved corrections or structured import | Require explicit mapping, validation, evidence, and a governed mutation command; never sync implicitly |
| YAML / JSON → SQLite | Declarative configuration or manifest-driven import | Validate schema, provenance, authorization, idempotency, and dry-run output before mutation |
| SQLite → JSONL / NDJSON | Event-stream or bulk diagnostic export | Preserve ordering, event identifiers, as-of time, and redaction; prevent derived output from becoming a second event writer |
| SQLite / CSV → Parquet | Analytical extraction | Record the source query or snapshot, schema, partition logic, timestamp, and checksum; treat the result as derived |
| Any governed store → PDF | Issued evidence or publication | Record issuer, source version, approval, generation time, and audience; do not infer that a PDF is public |

Every derived artifact should point back to its source and as-of time. A round trip must not create two writable authorities.

## Git Stores Rules, Not Private State

Git may track:

- schemas, migrations, validators, import/export code, and tests;
- YAML, JSON, TOML, SQL, and lockfiles that serve as sanitized reusable contracts or reproducibility controls;
- empty or synthetic templates and fixtures;
- sanitized governance guides and approved aggregate publications;
- documentation describing storage, authority, privacy, reconciliation, and recovery.

Git should not track by default:

- operational SQLite databases or sidecar files;
- real environment files, logs, analytical Parquet/Arrow snapshots, backups, or unapproved PDFs;
- row-level financial, customer, child/family, donor, contractor, property, or security records;
- private XLSX workbooks or CSV exports;
- divergent backups whose authority is unresolved;
- evidence bodies, bank references, credentials, contact details, or restricted locations.

Run `.\tools\run.ps1 ops privacy-scan --repo .` before commit. Passing the scanner is a minimum control, not publication approval.

## Recovery and Deletion Differ by Format

- SQLite recovery restores the governed database and verifies schema, integrity, and recent events.
- XLSX recovery restores the last approved workbook version and checks formulas, sources, and reconciliation status.
- CSV recovery restores an immutable source snapshot and re-runs the documented import or reconciliation process.
- YAML, JSON, TOML, SQL, and lockfile recovery restores the reviewed contract and re-runs the owning tool or migration process.
- JSONL/NDJSON recovery verifies event identity, ordering, truncation, and redaction before replay or analysis.
- Parquet/Arrow recovery reproduces the snapshot from its source query, schema, partition rules, timestamp, and checksum.
- PDF recovery verifies the issuer, approved source version, signature or generation receipt, and intended audience.
- Git recovery restores reusable code and doctrine; it must not be used to reconstruct private operational state.

Deletion from the current workspace does not remove a file from Git history, shared drives, backups, exports, or recipient copies. Retention and deletion therefore follow the data classification and approved storage system, not merely the active filename.

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Context-dependent—some future workflows may need a different canonical store or approved sanitized export | Do not generalize the current SQLite/XLSX/CSV authority pattern without naming the receiving workflow and data class | A documented workflow contract, access model, migration path, reconciliation test, retention rule, and accountable owner |

## Review Checklist

Before introducing or relying on a data, configuration, event, analytical, evidence, or backup file, confirm:

- one authority is declared for the relevant decision;
- source and derived roles are labeled;
- provenance, effective date, and freshness are visible;
- identifiers and reconciliation rules prevent duplicate ambiguity;
- privacy classification and storage location are appropriate;
- imports validate before mutation and exports cannot silently flow back;
- backup, retention, and deletion responsibilities are assigned;
- the owning tool and regeneration procedure are named for configuration, lock, migration, and derived analytical files;
- event ordering, replay, and truncation rules are defined for append-only streams;
- issuer, approval, audience, and source version are visible for immutable evidence or publications;
- environment files, logs, sidecars, and backups cannot enter Git accidentally;
- human approval remains explicit for publication and consequential use.

For the repository's curated high-consequence boundaries, encode these answers in [`artifact-state.yaml`](../artifact-state.yaml) and run `.\tools\run.ps1 project validate-artifacts`. The manifest governs declarations, including paths to private external storage; it does not authorize the validator to open private artifacts or make subjective authority decisions.

Review the value and cost of these controls through [Governance Earns Its Place by Preventing More Risk than It Creates](governance-control-review.md). A declaration or validator remains infrastructure only while it prevents more risk than it introduces.
