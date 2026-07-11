# Customer State Update Skill

Use this skill when a customer fact changes or a new customer fact is introduced.

Examples:

- Revenue, retainer, donation, salary, budget, asset value, or pricing changes.
- A customer moves from hypothesis to paid obligation.
- A customer service scope is defined, corrected, or marked unplanned.
- A relationship changes across customers, such as one customer buying services from another.
- A customer-facing, employee-facing, or internal-only language boundary needs correction.

If the fact involves money, tax-sensitive classification, accounting evidence, payroll, donations, retainers, reimbursements, asset values, inventory, real estate, or nonprofit funds, run the `tax-financial-governance` check before updating customer state.

## Purpose

Keep customer state coherent across the Anyang Intelligence repo.

The goal is to prevent drift between customer folders, portfolio dashboards, comparison matrices, commercial hypotheses, and service-package documents.

## Update Procedure

### 1. Classify The Fact

Before editing, classify the new fact:

- Confirmed fact.
- Hypothesis.
- Paid retainer.
- Donor-funded support.
- Optional donation.
- Revenue.
- Salary or expense.
- Asset value.
- Scope still unplanned.
- Service scope defined.
- Internal note only.
- Employee-facing instruction.
- Customer-facing instruction.

Do not collapse these categories. For example, a donor-funded retainer is not the same as paid participation.

For any money-related fact, also classify the financial-governance status using `skills/tax-financial-governance/SKILL.md`. If classification is uncertain, hold the classification and prepare a professional-review question instead of presenting a final tax, accounting, payroll, or legal conclusion.

### 2. Identify Affected Documents

Check whether the fact belongs in:

- `customers/<customer>/README.md`
- `customers/<customer>/executive-os-install.md`
- Customer-specific service package docs.
- Employee onboarding docs.
- `customers/operating-portfolio-dashboard.md`
- `customers/comparison-matrix.md`
- `customers/commercial-hypotheses.md`
- Root `README.md`
- Shared templates, playbooks, or docs.

If the fact affects money or obligations, the operating portfolio dashboard almost always needs an update.

### 3. Preserve Layer Boundaries

Before writing, decide the document audience:

- Internal Anyang Intelligence operating document.
- Customer-facing document.
- Employee-facing document.
- Public/service document.

Avoid leaking internal platform language into employee-facing or customer-facing docs unless intentionally part of the artifact.

### 4. Remove Stale Contradictions

Search for old versions of the fact.

Recommended search patterns:

- Customer name.
- Dollar amount.
- `retainer`
- `paid`
- `free`
- `donor`
- `donation`
- `hypothesis`
- `not yet planned`
- `first client`
- `first paying client`

Update or remove stale claims in the same change.

### 5. Update Portfolio State

When relevant, update the customer's:

- Current status.
- Revenue / asset status.
- Active obligation.
- Next decision.
- Confidence level.
- Known cash events.
- Unknown or pending items.
- Immediate decision queue.
- Priority order.

### 6. Mark Scope Discipline

If money has been received but work is not yet scoped, say so explicitly.

Include:

- What has been received.
- Who provided it, if relevant.
- Whether participation or access is paid/free.
- What the funds may support.
- What must be decided before delivery begins.
- What authority boundary applies.
- Whether tax, accounting, payroll, nonprofit, real estate, or professional review is required.

### 7. Verify

Before committing:

- Run a text search for stale contradictory terms.
- Review the diff.
- Confirm money, scope, and language audience are represented correctly.
- Confirm the repo has no unrelated changes staged.

## Output Standard

Every customer state update should leave the repo with:

- One clear source of truth for the current fact.
- No obvious contradictions across portfolio docs.
- A clear next decision if the fact creates an obligation.
- Explicit separation between confirmed facts and hypotheses.
