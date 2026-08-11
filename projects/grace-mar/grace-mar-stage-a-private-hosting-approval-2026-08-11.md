# Grace Mar Stage A Private-Hosting Approval

**Transaction ID:** `GM-HOST-STAGE-A-2026-08-11-01`

**Decision class:** Class 2 — external hosting project creation and provider
source persistence

**Project scope:** Grace Mar landing page

**Record version:** `1.0`

**State:** `Stage A evidence returned — saved version complete; no deployment`

## Authority header

- **Acting role:** Chief Executive for recommendation and approval preparation
- **Authority source:** Executive Council role contract and an attributable
  human System Engineer decision recorded in this instrument
- **Domain:** Grace Mar website hosting
- **Named lane:** `projects/grace-mar/website`
- **Target:** One private OpenAI Sites project and one saved, non-deployed
  version
- **Approval required:** Human System Engineer
- **Escalation target:** System Engineer
- **Evidence:** Sites project state, saved-version receipt, access state, exact
  source identity, and cost/commitment report
- **Status:** `Authorized`

## A. Recommendation

**Recommendation ID:** `GM-HOST-STAGE-A-REC-2026-08-11-01`

**Prepared by:** Chief Executive

**Recommendation date:** 2026-08-11

**Recommendation state:** `approved`

### Operating picture

- The Grace Mar landing page source is complete under
  `projects/grace-mar/website`.
- The source was added in repository commit `78c9fd7` and has no current
  Git-visible modifications.
- The last recorded production build and rendered-page tests passed on
  2026-08-07.
- `.openai/hosting.json` contains `d1: null` and `r2: null` but no Sites
  `project_id`.
- No Sites project, saved version, deployment, custom-domain binding, or public
  release is recorded.
- The live apex domain currently points to GitHub Pages and returns `404 Site
  not found`; `www.grace-mar.com` has no DNS record.
- Public deployment, custom-domain binding, and DNS correction are later,
  separately approved stages.

### Decision required

Decide whether one named executor may create a private OpenAI Sites project and
save exactly one non-deployed version of the existing Grace Mar landing page
for owner review.

### Recommendation

Approve Stage A with the exact scope and stop conditions below. Stage A should
end after the saved-version receipt returns. It should create no deployment URL
intended for use, no public access, no custom-domain binding, and no DNS change.

### Proposed success condition

One Sites project titled `Grace Mar` exists under the accountable operator;
one exact-source version is saved but not deployed; access remains limited to
the owner and platform-default workspace administrators; no fee or commitment
is accepted; and the required sanitized evidence is returned.

## B. Authority disposition — complete only through attributable human decision

### Approval statement

The human System Engineer may approve this exact statement:

> **Approve Grace Mar Stage A private hosting.** Authorize the named executor
> to create one OpenAI Sites project titled `Grace Mar` using the preferred
> slug `grace-mar-landing`. Stop if that slug is unavailable; do not select an
> alternative. Use only the exact validated source under
> `projects/grace-mar/website`. Save exactly one version and do not deploy it.
> Confirm that access is limited to the accountable owner and
> platform-default workspace administrators; add no editor, visitor, group,
> workspace-wide, shared-link, or public access. Create no custom-domain
> binding, environment value, database, object storage, analytics SDK, form,
> commerce function, customer-data flow, or external communication. Approved
> spend ceiling is `$0`. Stop before any fee, paid plan, trial conversion,
> payment method, recurring commitment, overage, quota purchase, or broader
> access. Return the project state, saved-version identifier, exact source
> identity, access state, cost and commitment state, and a sanitized execution
> receipt. This approval expires after the first saved version is recorded or
> at 2026-08-18 23:59 America/Denver, whichever occurs first.

### Required decision fields

- **Authority decision ID:** `GM-HOST-STAGE-A-AUTH-2026-08-11-01`
- **Authority:** Human System Engineer
- **Approved by:** System Engineer/operator through explicit selection `C. Execute
  Stage A with Codex as the named executor under this exact approval`
- **Decision date and time:** 2026-08-11, current Codex task
- **Decision state:** `approved`
- **Decision:** `Approve`
- **Named executor:** Codex, acting only as the Stage A hosting executor
- **Accountable Sites owner:** Current operator
- **Approved spend ceiling:** `$0`
- **Expiration:** First saved version or 2026-08-18 23:59 America/Denver,
  whichever occurs first
- **Approval evidence:** Attributable operator selection in the current Codex
  task

Any change to the provider, title, slug, source, owner, access, version count,
cost ceiling, expiry, or deployment state returns this instrument to
`awaiting approval`.

## Exact approved scope if the disposition is `Approve`

The named executor may:

1. Reconfirm that `projects/grace-mar/website` has no Git-visible source
   modifications and that the hosting manifest contains no existing
   `project_id`.
2. Rebuild and test the exact source if the prior build cannot be safely reused.
3. Create one Sites project titled `Grace Mar` with slug
   `grace-mar-landing`.
4. Stop if the preferred slug is unavailable.
5. Persist only the returned `project_id` in `.openai/hosting.json`; retain
   `d1: null` and `r2: null`.
6. Place the exact validated source in the provider-managed source repository
   using the provider's bounded credential handling.
7. Save exactly one deployable version.
8. Do not deploy that version privately, through shared access, or publicly.
9. Confirm the project access state and add no user, group, or link access.
10. Return the evidence listed below and stop.

## Limits and exclusions

This approval does not authorize:

- private, shared, or public deployment;
- a deployment URL for review or use;
- public release, publication, or external delivery;
- `grace-mar.com` or `www.grace-mar.com` custom-domain binding;
- Namecheap login or any DNS, nameserver, registrar, DNSSEC, MX, SPF, DKIM,
  DMARC, forwarding, or TXT-record change;
- a different slug, second project, second saved version, or later source
  update;
- editors, visitors, groups, workspace-wide access, public access, or shared
  links;
- a paid plan, payment method, trial conversion, recurring charge, quota
  purchase, or overage;
- Google Workspace, email, social accounts, analytics, advertising, forms,
  commerce, customer data, or customer contact;
- changes to the Grace Mar or Grace Gems copy;
- an LLC-status claim, asset-transfer claim, ownership claim, or trademark
  conclusion;
- implementation, migration, storefront changes, or Grace Gems CEO contact;
  or
- credential, recovery-code, payment, tax, address, signature, or private
  client-data persistence in Git.

## Stop conditions

Stop before project creation or further action if:

- the human System Engineer approval and named executor are missing;
- `grace-mar-landing` is unavailable;
- an existing Sites project or `project_id` is discovered;
- the source has changed since validation and cannot be rebuilt and tested
  inside this exact scope;
- the service requires deployment to save a version;
- any fee, payment method, paid plan, trial conversion, recurring commitment,
  quota purchase, or overage appears;
- access would be broader than the owner and platform-default workspace
  administrators;
- platform-default administrator access is materially different from the
  recorded assumption;
- database, object storage, secrets, environment values, runtime migrations,
  customer data, or new third-party services become necessary;
- provider terms or platform measurement create a new material privacy or
  commitment question; or
- the requested action reaches deployment, domain binding, DNS, email, or
  external communication.

Return the blocker, consequence, evidence available, missing decision, and next
decision owner. Do not select a workaround by inference.

## Required evidence return

Return a sanitized receipt containing:

- executor and execution timestamp;
- authority decision ID and approval source;
- project title and preferred-slug outcome;
- sanitized project identifier or opaque receipt reference;
- exact repository commit and source-tree identity used;
- build and test outcome;
- saved-version identifier and state;
- explicit confirmation that no deployment occurred;
- project access state and confirmation that no access was added;
- `d1`, `r2`, environment, form, analytics-SDK, commerce, and customer-data
  state;
- amount spent, payment method requested, trial or recurring commitment, and
  quota or overage state;
- local manifest change;
- unexpected facts, deviations, and holds; and
- the next decision required.

Do not record source credentials, access tokens, account identifiers that are
not needed for audit, recovery details, payment information, or private
workspace membership.

## C. Execution and evidence

**Action ID:** `GM-HOST-STAGE-A-ACT-2026-08-11-01`

**Executed by:** Codex

**Execution function:** `other approved action — external hosting preparation`

**Execution state:** `evidence returned`

- **Executor invoked:** yes
- **Execution date:** 2026-08-11
- **Action taken:** Created one Sites project titled `Grace Mar` with the exact
  slug `grace-mar-landing`; persisted its opaque project identifier in the local
  hosting manifest; pushed the exact validated website source; saved version
  `1`; and stopped before deployment.
- **Parties or systems involved:** OpenAI Sites provider-managed project and
  source repository
- **Authority scope used:** Exact Stage A approval only
- **Exact provider source commit:**
  `8ab86f214b168277e4498012f6b0e671a40058c9`
- **Build and test outcome:** Passed `npm test` on 2026-08-11; production build
  completed and both rendered-page tests passed, including the approved
  no-data boundary.
- **Saved version:** Version `1`, opaque version receipt
  `appgprj_6a7b7e2f1cf48191b6d8e0770b333128~appgver_a6a914b53afc81918ace5278e37b1c51`
- **Archive evidence:** 56 files; content hash
  `sha256:d94089404bf2832946cd350a33da0e16f788008baba8057714768ba6835a3f4e`
- **Deployment state:** No deployment occurred; current live URL and preview URL
  are both absent.
- **Access state:** Custom owner-only access; one owner, no added editors, no
  external visitors, and no groups.
- **Runtime state:** `d1: null`; `r2: null`; no environment values, forms,
  analytics SDK, commerce, or customer-data flow added.
- **Cost and commitment state:** No fee, payment method, paid plan, trial
  conversion, recurring commitment, quota purchase, or overage was presented or
  accepted. Amount spent: `$0`.
- **Local change:** Added the returned opaque `project_id` to
  `projects/grace-mar/website/.openai/hosting.json`; retained `d1: null` and
  `r2: null`.
- **Unexpected facts:** The first Git push required Git's OpenSSL backend after
  the Windows Schannel backend could not acquire credentials. The retry changed
  no scope or provider state beyond the approved source push.
- **Deviation:** None material.
- **Follow-up owner:** System Engineer for any Stage B decision
- **Outcome:** Stage A complete; saved version available in Sites; all
  deployment, domain, DNS, email, access-expansion, and public-release actions
  remain held.

## D. Reconciliation

**Reconciliation ID:** `GM-HOST-STAGE-A-RECLOSE-2026-08-11-01`

**Reconciliation state:** `supported`

- **Chief Executive reconciliation:** Returned evidence supports the exact
  Stage A scope: one project, one saved version, owner-only access, `$0` spend,
  and no deployment.
- **Council Steward review required:** no, unless separately activated or a
  material deviation occurs
- **Client decision required:** no for Stage A provider preparation; public
  Grace Mar / Grace Gems wording remains separately gated before release
- **Final supported state:** `Stage A complete; version 1 saved; deployment and
  domain actions held`

## Attestations

- **Proposed by:** Chief Executive
- **Recommended by:** Chief Executive
- **Approved by:** System Engineer/operator through explicit Stage A execution
  selection
- **Executed by:** Codex
- **Verified by:** Chief Executive through Sites project and saved-version
  state inspection
- **Authority scope:** One private Sites project and one saved, non-deployed
  version only
- **Evidence required:** Exact source, saved-version state, access, cost,
  commitment, manifest, and no-deployment confirmations

This instrument did not approve itself; the recorded operator selection supplied
the attributable Stage A decision and named executor. Stage A is now exhausted.
Every additional version, deployment, domain, DNS, email, access-expansion,
spending, and public-release action remains held pending separate authority.
