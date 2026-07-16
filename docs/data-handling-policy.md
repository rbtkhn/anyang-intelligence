# Customer Data Handling Policy

## Purpose

The product repository contains reusable code, schemas, synthetic fixtures, and doctrine. It is not a tenant data store. Identifiable customer, child, family, donor, contractor, support-message, financial, or security-sensitive records must remain outside Git.

## Classification

| Class | Examples | Repository rule |
| --- | --- | --- |
| Public | Approved public storefront facts and published assets | May be referenced with provenance and freshness metadata |
| Internal | Operating templates, sanitized metrics, non-identifying plans | May be tracked only when no tenant-private context is embedded |
| Private | Customer messages, learner records, contact details, exact finances | Store in the operator-controlled tenant store; Git holds an opaque reference only |
| Restricted | Child/family records, credentials, legal/medical records, property access, raw transcripts | Never place in product Git; access must be explicitly authorized and minimized |

The strictest applicable class wins.

## Consent And Authority

- Record who supplied the data, the approved purpose, the permitted audience, and any reuse restriction before operational use.
- Approval to review data is not approval to publish, train on, generalize, or transfer it.
- Parent or guardian authority is required for child-related records. Customer owner authority is required for private business records and external claims.
- Raw customer-support transcripts remain outside v1 operating state. Store only an approved external reference and a redacted confusion pattern.

## Access And Storage

- Use [The File Extension Does Not Decide Which Record Governs](data-store-roles.md) to assign distinct authority to SQLite operational state, XLSX review/reconciliation surfaces, and CSV source or interchange files.
- Set `ANYANG_DATA_DIR` to an operator-controlled location outside the repository, or pass an explicit external `--db` path.
- Limit tenant-store access to named operators with a current operating need.
- Back up tenant state only through an operator-approved encrypted mechanism. Repository commits are not backups for customer data.
- Do not place tenant databases, exports, screenshots, raw messages, or private attachments in repository subdirectories.

## Retention, Deletion, And Return

- Assign a review date when private data is collected. Retain only what supports an active obligation, audit requirement, or approved learning purpose.
- At engagement close, export approved customer records, revoke access, and delete unneeded working copies and backups according to the agreed schedule.
- A deletion request applies to active stores, generated exports, working copies, and documented backups. Git-history remediation requires a separate exposure review because deletion from HEAD is not deletion from history.

## Redaction And Reuse

- Replace names and identifying combinations with synthetic data before creating examples or tests.
- Preserve the reusable operating pattern, not the customer's facts.
- Sanitized exports must omit private evidence bodies, contact details, raw messages, exact child/family context, credentials, and restricted locations.
- Do not label an example synthetic unless every person, event, amount, and observation in it is fabricated or safely generalized.
- Pseudonymous learner examples may remain in Git only when the file explicitly marks itself as a `synthetic-fixture` and contains no real identifying combinations or private evidence body.

## Forbidden Git Content

- Identifiable learner, child, family, donor, customer, or contractor records.
- Raw customer-support transcripts or screenshots.
- Email addresses, phone numbers, credentials, tokens, private keys, or private database files.
- Exact private property access/security details.
- Tenant folders named `tenant-private`, `customer-private`, or `raw-customer-transcripts`.
- Unredacted intake summaries or project-specific plan-input drafts.

Run `.\tools\run.ps1 ops privacy-scan --repo .` before commit and the canonical validation driver in CI. A finding blocks shipment until the content is removed, replaced with a synthetic fixture, or the scanner rule is narrowly corrected without weakening this policy.

## Incident Response

If restricted data enters Git:

1. Stop further copying and quarantine the current file outside the repository.
2. Record affected records, commits, remotes, likely access, and containment status without repeating the sensitive content.
3. Decide with the operator and affected authority whether notification, credential rotation, or history rewriting is required.
4. Coordinate history rewriting separately; never force-push as an automatic scanner response.
5. Preserve a sanitized incident record and add a preventive control.
