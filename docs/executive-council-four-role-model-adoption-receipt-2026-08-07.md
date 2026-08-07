# Executive Council Four-Role Model — Adoption Receipt

**Receipt ID:** `EC-FOUR-ROLE-MODEL-2026-08-07-01`

**Status:** `adopted — implementation authorized`

**Prepared:** 2026-08-07

**Decision authority:** System Engineer

**Authority effect:** Adopts the four-role Executive Council model and
authorizes only the bounded repository implementation listed in this receipt.
It does not activate a runtime, enlarge a role, create client authority,
authorize external action, or permit historical-record rewriting.

**Related proposal:** [Executive Council Four-Role Model — Amendment
Proposal](executive-council-four-role-model-amendment-proposal-2026-08-07.md)

## Decision

**Decision:** `Adopt`

**Approved by:** System Engineer/operator

**Decision source:** Explicit selection `B. Execute — Adopt the four-role model
and implement the bounded amendment`, 2026-08-07

**Effective date and time:** `2026-08-07T16:28:25-06:00`

This receipt authorizes only the implementation surface and invariants stated
below.

## Proposed adopted structure

The controlling structure becomes:

```text
Anyang Intelligence
|
|-- System Engineer — human owner and authority layer
|
`-- Executive Council
    |-- Chief Executive
    |-- Artistic Director
    |-- Executive Assistant
    `-- Council Steward
```

The four durable Executive Council roles will be:

1. Chief Executive;
2. Artistic Director;
3. Executive Assistant; and
4. Council Steward.

The System Engineer will remain the human owner and final Anyang authority
principal above Council. The System Engineer will not become an AI runtime or
Council operating role.

## Authority effects if adopted

The amendment changes organizational classification and current-state
presentation only. It does not merge recommendation with approval or enlarge
any operating authority.

- **Chief Executive authority change:** none. The Chief Executive continues to
  prepare judgment and recommendations and cannot approve its own work.
- **System Engineer authority change:** none. The human System Engineer
  continues to approve, constrain, delegate, revoke, or stop consequential
  Anyang action.
- **Artistic Director authority change:** none.
- **Executive Assistant authority change:** none.
- **Council Steward authority change:** none. Assurance remains independently
  routed and does not acquire correction or approval authority.
- **Client-authority change:** none. Client CEOs retain separate authority over
  their companies; System Engineer authority cannot substitute for it.
- **Runtime activation change:** none. Durable role, human-holder, runtime, and
  task activation remain separate states.

## Machine-key compatibility

Under this adoption:

- `engineer` remains the machine-readable Anyang authority-principal key;
- `executive`, `artistic`, `interface`, and `steward` remain the four
  machine-readable Council-role keys;
- `client` remains the external client-authority key;
- existing authority domains, approvers, aliases, and dual-authority rules
  remain in force;
- the stored `council_role` event field remains readable and continues to
  accept historical `engineer` attribution; and
- compatibility data does not classify System Engineer as a Council runtime.

## Historical-record treatment

Sources created before the effective date may describe System Engineer as one
of five Executive Council positions. Preserve dated briefs, receipts, event
packets, transaction records, appointment records, decision provenance, and
learning-ledger entries unchanged as historical evidence.

After the effective date, derived current-state views must present four Council
roles with System Engineer above Council. Historical records must not be
silently rewritten to match the new classification.

## Controlling files authorized for amendment

Implementation is limited to:

- `authority-envelope.yaml`;
- `docs/executive-council-identity.md`;
- `docs/authority-model.md`;
- `docs/executive-council-role-contract.md`;
- `cli/anyang_loop/authority.py`;
- `cli/anyang_loop/council_workroom.py`;
- `cli/README.md`;
- `projects/grace-gems/executive-council-role-card.md`;
- `tests/test_authority.py`;
- `tests/test_council_workroom.py`; and
- the related proposal, solely to record its final disposition and link this
  receipt.

Any database-schema migration, historical-record rewrite, authority expansion,
runtime activation, appointment, spending, external action, client decision,
or change outside this list requires separate authority.

## Required implementation sequence

1. Complete this receipt through an explicit human System Engineer decision.
2. Add machine-readable actor classifications while preserving every existing
   actor and authority key.
3. Amend the three controlling identity and authority documents.
4. Correct runtime terminology without renaming the persisted `council_role`
   field.
5. Update the current Grace Gems role card and CLI description.
6. Add composition, authority-preservation, and backward-compatibility tests.
7. Run focused tests followed by the full repository validation gate.
8. Record the resulting commit and validation evidence below.

## Required validation

Implementation must prove:

1. Current identity, authority, and role-contract sources agree on exactly four
   Council roles.
2. `engineer` remains the required Anyang authority principal and approver.
3. No AI-generated artifact can establish System Engineer approval without an
   attributable human decision.
4. Client authority remains separate and non-substitutable.
5. Council Steward remains independently routed.
6. Historical five-role sources remain attributable and unchanged.
7. Current roster logic does not count `engineer` or `client` as Council roles.
8. Existing events using `council_role: engineer` remain readable.
9. Focused tests and the complete repository validation gate pass.

## Rollback method

If implementation violates an invariant or validation fails:

1. stop before commit or publication;
2. restore the last validated controlling current-state files while preserving
   this receipt and all historical records as evidence;
3. retain the existing machine keys and persisted event fields;
4. record the failed invariant and affected validation result; and
5. return the amendment to `held` pending a new System Engineer disposition.

Rollback must not delete or rewrite transaction history.

## Review

**Review date:** `2026-09-07`

Review whether current displays consistently separate the System Engineer from
Council membership, whether users still understand the approval boundary, and
whether compatibility terminology creates material confusion.

## Implementation evidence

**Executed by:** Chief Executive agent for bounded repository reconciliation

**Commit:** The bounded commit containing this receipt and implementation;
identify it by repository history and the receipt ID above

**Validation commands:**

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_authority.py tests/test_council_workroom.py -q
.\tools\validate.ps1
.\tools\run.ps1 project validate-authority
.\tools\run.ps1 project validate projects
.\tools\run.ps1 loop validate projects
git diff --check
```

**Validation result:** Focused authority and compatibility tests passed, 38/38.
The complete pytest suite passed, 536 passed and 3 skipped. Authority-envelope,
project-install, loop-fixture, analytical-interface, artifact-state,
bounded-agency, and epistemic-state validators passed. `git diff --check`
passed with line-ending warnings only. The repository-wide privacy scan passed
with no prohibited tracked content, and the complete CI-equivalent validation
gate exited successfully.

**Exceptions or deviations:** None in the final validation run. An earlier
direct system-Python attempt lacked PyYAML; the documented repository-managed
environment was used for the successful focused and full gates.

**Final state:** `adopted, implemented, and fully validated in the working tree
— uncommitted`
