# Tax And Financial Governance Guardrail Skill

Use this skill when a task involves money, tax-sensitive classification, accounting evidence, or financial governance risk.

This skill is a governance guardrail. It helps Anyang Intelligence keep money legible, evidence preserved, and professional-review questions clear.

It does **not** provide final tax, legal, accounting, payroll, nonprofit compliance, or investment advice.

## Trigger

Use this skill when the work involves:

- Revenue.
- Retainers or prepaid services.
- Donations or donor-funded support.
- Optional member support.
- Salaries, payroll, contractor payments, or stipends.
- Outsourced contractor country, residency, work-location, withholding, or W-8/W-9 questions.
- Reimbursements.
- Subscriptions, tools, software, or operating expenses.
- Inventory, cost of goods, discounts, refunds, repairs, or returns.
- Asset values, real estate, capital improvements, insurance, or property expenses.
- Sales tax, marketplace tax, import tax, shipping charges, or customer payments.
- Nonprofit funds, restricted funds, board approvals, donor notes, grants, or program spending.
- Education-service payments, parent payments, tuition-like payments, or subscription hypotheses.

Also use this skill when the operator asks:

- Is this revenue?
- Is this deductible?
- How should this be classified?
- What records do we need?
- Does this create a tax issue?
- Does it matter which country a contractor is in?
- Should this be treated as a donation, retainer, salary, expense, reimbursement, asset, or income?

## Purpose

The purpose is to separate cash movement from economic meaning.

A payment may look simple, but it can mean different things:

- Service revenue.
- Retainer or prepaid service obligation.
- Donor-funded support.
- Optional donation.
- Salary or contractor expense.
- Reimbursement.
- Inventory or cost of goods.
- Asset value.
- Capital improvement.
- Restricted nonprofit funds.
- Unknown until reviewed.

Do not collapse these categories.

## Standard Output

When this skill is used, produce a short financial-governance check with these fields:

```text
Money movement:
<what moved, between whom, when, and amount if known>

Working classification:
<revenue | retainer/prepaid service | donor-funded support | optional donation | salary/expense | reimbursement | asset value | inventory/cost-of-goods | capital improvement | unknown>

Evidence needed:
<invoice, receipt, contract, payment record, donor note, payroll record, owner approval, listing/order export, bank record, board approval, or other records>

Governance risk:
<low | medium | high | professional review required>

Required review:
<owner | bookkeeper | CPA/tax professional | attorney | board | parent/guardian | other>

Next safe action:
<record | ask for missing evidence | hold classification | prepare professional-review question | update project state>
```

## Review Procedure

### 1. Identify The Money Movement

Name:

- Amount.
- Payer.
- Recipient.
- Date or cadence, if known.
- Purpose claimed by the operator or source.
- Whether the money is received, promised, spent, reimbursed, or only hypothesized.

If any of these are unknown, say so.

### 2. Classify Conservatively

Choose the safest working classification:

- Revenue.
- Retainer/prepaid service.
- Donor-funded support.
- Optional donation.
- Salary/expense.
- Reimbursement.
- Asset value.
- Inventory/cost-of-goods.
- Capital improvement.
- Unknown.

If classification is uncertain, the correct output is:

```text
Working classification: unknown
Next safe action: hold classification and prepare professional-review question
```

### 3. Preserve Evidence

Identify the records needed before the organization relies on the classification.

Common evidence types:

- Invoice.
- Receipt.
- Contract or service agreement.
- Payment record.
- Donor note.
- Payroll record.
- Contractor agreement.
- Owner approval.
- Listing/order export.
- Bank record.
- Board approval.
- Property record.
- Appraisal, valuation note, or insurance record.
- Parent or guardian approval for education-service payments.
- Contractor country/residency statement.
- Work-location statement for the services performed.
- W-8BEN, W-8BEN-E, W-9, or other bookkeeper/CPA-requested tax documentation.

### 4. Assign Governance Risk

Use:

- `low` when the classification is obvious, low-stakes, and evidence is available.
- `medium` when the classification affects project state, reporting, reimbursement, expense tracking, or future pricing.
- `high` when the classification affects payroll, taxes, nonprofit funds, real estate, restricted funds, inventory, customer refunds, legal commitments, or external claims.
- `professional review required` when a tax, accounting, legal, payroll, nonprofit, investment, or jurisdictional position would be needed.

### 5. Name Required Review

Do not say "the AI can decide" for tax-sensitive issues.

Choose the appropriate reviewer:

- Owner.
- Bookkeeper.
- CPA/tax professional.
- Attorney.
- Board.
- Parent/guardian.
- Property professional.
- Marketplace/accounting export owner.

### 6. Choose The Next Safe Action

Use one:

- Record the fact.
- Ask for missing evidence.
- Hold classification.
- Prepare a CPA/bookkeeper question.
- Prepare an owner/board approval question.
- Update project state after classification is clear.

## Portfolio-Specific Guardrails

Preserve these distinctions unless the operator gives a new confirmed fact:

- Grace Gems paying Media Production is service revenue to Media Production, but Grace Gems business economics remain unknown.
- Book Club participation is free; donor-funded support is not paid access.
- Learning Core's `$1,000` retainer is payment from Learning Core to Anyang Intelligence for a scoped 30-Day Personalized Learning Plan for new students, including onboarding. Customer pricing has not been designed yet.
- Mountain Villa has property stewardship implications but no current revenue.
- Media Production's `$500/month` Creative Production Operator allocation is a planned outsourced contractor/service-expense allocation while the role is unfilled; any actual payment requires appropriate contract, invoice, payment, and tax/accounting review.
- Contractor country matters for governance. Before paying an outsourced contractor, preserve the contractor's country/residency, where the work is physically performed, contract, invoice, payment record, and W-8/W-9 status as applicable. Do not make a final withholding, reporting, treaty, payroll, labor-law, VAT/GST, sanctions/export-control, or permanent-establishment conclusion without professional review.

## Boundaries

Anyang Intelligence may:

- Organize financial facts.
- Classify money movements as working categories.
- Identify missing evidence.
- Prepare questions for owners, bookkeepers, CPAs, attorneys, boards, or other professionals.
- Update repo state after facts are confirmed.

Anyang Intelligence may not:

- Give final tax advice.
- Decide deductibility.
- Decide payroll treatment.
- Decide nonprofit compliance treatment.
- Decide sales-tax obligations.
- Decide legal entity treatment.
- Decide investment, valuation, or real-estate tax positions.
- Present a working classification as a professional conclusion.

## Done When

The money movement has a conservative working classification, required evidence is named, governance risk is clear, and the next safe human/professional review path is explicit.
