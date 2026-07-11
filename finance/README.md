# Financial Records Stay Internal Until Reconciliation Makes Them Fit for Use

Title rationale: The guide names the governing boundary: operating figures remain internal evidence objects until dates, sources, and reconciliation support their intended use.

## Lead Judgment

Anyang Intelligence financial records may organize operating facts and missing evidence, but they must not become public claims, tax conclusions, customer commitments, or management decisions merely because a ledger contains a number.

## Controlling Object

Whether each financial record has a stable identifier, effective date, evidence reference, reconciliation status, and accountable review sufficient for its intended decision.

## Authority and Storage

- `anyang-intelligence-ledger.xlsx` is the provisional authoritative operating ledger.
- `anyang-intelligence-ledger.csv` is a source snapshot retained for traceability, not a second writable source of truth.
- `archive/` preserves superseded or divergent source copies until a human confirms their evidence has been reconciled.
- CSV, XLSX, and archived ledger files are ignored by Git and remain internal unless the owner explicitly authorizes a sanitized publication artifact.
- The repository may track this governance guide, validation code, and empty templates; it must not track row-level financial records by default.

## Required Record Fields

Every operating record should contain:

- a stable `record_id`;
- an `effective_date`, or a visibly unresolved date with evidence requested;
- an `evidence_reference` pointing to an invoice, receipt, contract, bank reference, approval, or other authorized record;
- a `reconciliation_status` of `unreconciled`, `matched to source`, `reviewed`, or `not applicable`;
- a classification separating confirmed cash, planned amounts, donor-supported funds, targets, and non-cash references;
- the accountable human or professional review required before consequential use.

## Reconciliation Rule

Do not overwrite a conflicting source silently. Preserve the source in `archive/`, compare it with the authoritative ledger, and resolve the difference through evidence or an explicit human decision. A missing date or reference remains unresolved rather than being inferred.

## Publication Boundary

Do not publish row-level amounts, counterparties, payroll or contractor information, customer economics, donor-supported funds, property references, tax information, bank references, or evidence locations without explicit owner approval and the applicable privacy, contractual, accounting, tax, legal, or professional review.

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Unreconciled—several source records lack effective dates or evidence references | Treat totals and classifications as provisional operating context, not financial statements | Dated source records, evidence references, reconciliation receipts, and bookkeeper or CPA review where applicable |

## Professional Boundary

This ledger can organize facts and identify missing evidence. It is not a bank statement, tax return, appraisal, payroll record, audited financial statement, or substitute for a bookkeeper, CPA, attorney, broker, appraiser, or other qualified professional.
