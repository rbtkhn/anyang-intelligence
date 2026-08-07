# Grace Mar Hosting and DNS Approval Packet

**Prepared:** 2026-08-07
**Status:** Decision packet only — no external action authorized
**Scope:** Hosting the completed Grace Mar landing page and later routing
`grace-mar.com` to it
**Excluded:** Google Workspace, mail-record changes, LLC filings, social
accounts, analytics, forms, commerce, customer contact, asset transfers, and
changes to existing Grace Gems storefronts

## Decision summary

The first Grace Mar landing page is complete locally and passes its production
build. It can be hosted without forms, analytics, customer data, commerce, or an
active email link.

**Recommended path:** use OpenAI Sites for the current build, first as a saved,
non-deployed version and only later as a public site. Keep Namecheap as the
registrar and DNS host. Do not transfer the domain or change nameservers. After
the hosted review is approved, bind both `grace-mar.com` and
`www.grace-mar.com`, obtain the provider-generated DNS values, and return those
exact values for a final DNS approval before changing Namecheap.

This path is recommended because the completed site already uses the compatible
Sites build format and contains `.openai/hosting.json`. The hosting file has no
project identifier, so no Sites project has been created and no hosting
commitment currently exists.

## 1. Confirmed facts

| Item | Confirmed state | Decision consequence |
| --- | --- | --- |
| Local website | Landing page completed under `operating-substrate/projects/grace-mar/website` | The content is ready for a bounded hosted review. |
| Build | `npm run build` completed successfully on 2026-08-07 | No additional development is required before a private hosting review. |
| Initial content | Grace Mar umbrella, Grace Gems flagship introduction, approach, and coming-soon message | No LLC claim, storefront, customer data, form, analytics, or active email route is present. |
| Hosting project | None recorded in `.openai/hosting.json` | Creating a Sites project would be a new external action and requires approval. |
| Registrar/DNS host | Namecheap | Keep it in place; no registrar transfer or nameserver migration is proposed. |
| Namecheap controller | Current operator confirmed control on 2026-08-07 | This confirms operational account control, not beneficial or legal ownership. |
| Namecheap recovery owner | A distinct recovery owner was confirmed on 2026-08-07; identity intentionally not retained here | Recovery evidence and identity remain private. |
| Current apex web DNS | Four GitHub Pages A records | These remain untouched until the final cutover approval. |
| Current apex response | GitHub Pages `404 Site not found` at last inspection | The present public site is broken, but that does not justify an unapproved DNS change. |
| `www` DNS | No record at last inspection | A new `www` record will be needed for the proposed canonical hostname. |
| Mail DNS | Namecheap forwarding MX records and forwarding SPF are active | Hosting approval must not change MX, SPF, DKIM, DMARC, or forwarding. |
| Legacy boundary | Strategy-codex still refers to `https://grace-mar.com` in a legacy configuration | Resolve this under separate Anyang authority before public cutover. |

## 2. Proposed hosting decision

### Provider and ownership

| Decision | Proposal |
| --- | --- |
| Host | OpenAI Sites |
| Site title | `Grace Mar` |
| Preferred site slug | `grace-mar-landing` |
| Slug fallback | Stop and return alternatives if unavailable; do not choose one speculatively. |
| Accountable owner | Current operator, confirmed 2026-08-07. |
| Recovery/editor access | A new Site is limited to its owner and workspace administrators by default. Add no editor, visitor, group, workspace-wide, or public access during the saved-version phase. |
| Source | The exact validated local landing-page source. |
| Runtime data | None required. |
| Database/storage | None; retain `d1: null` and `r2: null`. |
| Secrets/environment values | None. |
| Analytics/cookies | No analytics SDK, advertising tracker, or cookie mechanism is included in the Grace Mar source. Sites automatically records deployed-site unique visitors and page views; this platform measurement must be accepted or Sites rejected. |
| Custom domain | None during private review. |

### Cost and commitment

No hosting price, billing term, quota, or included-usage allowance has been
quoted in the available project or hosting interface. Therefore:

- **Approved spend remains `$0` unless a later approval names a different
  ceiling.**
- Project creation must stop before accepting a paid plan, trial conversion,
  billing method, overage, or recurring commitment.
- If the interface presents any price or commitment, return the exact quote,
  taxes if shown, renewal/overage terms, and cancellation boundary for approval.
- Namecheap renewal and Google Workspace costs are outside this packet and must
  not be altered or accepted.

## 3. Two-stage release boundary

### Stage A — project provisioning and saved-version review

Purpose: place the exact production build in Sites as a saved deployment
candidate without deploying it. Every Sites deployment URL is a production
deployment, even when access is restricted, so Stage A intentionally stops at
the saved-version boundary.

If specifically approved, the executor may:

1. Create one Sites project titled `Grace Mar` using the preferred slug.
2. Record its project identifier only in the local hosting configuration.
3. Place the exact validated source in the provider-managed source location.
4. Save one deployable version.
5. Confirm the project is limited to the owner and any workspace administrators
   who have platform-default access, with no added users or groups.
6. Do not deploy the saved version.
7. Return the saved-version number, confirmed project access state, sanitized
   receipt, and any fee or limitation encountered.

Stage A does **not** authorize any deployment, public access, custom-domain
binding, Namecheap login, DNS changes, email changes, customer contact, or
later versions.

### Stage B — public release and domain binding

Purpose: publish the already-approved version and obtain the exact DNS values
needed for `grace-mar.com`.

This stage requires a separate approval after Stage A review. If specifically
approved, the executor may:

1. Publish the approved saved version publicly.
2. Request custom-domain bindings for both `grace-mar.com` and
   `www.grace-mar.com`.
3. Return the exact provider-generated A, CNAME, and validation records without
   changing Namecheap.
4. Prepare a record-by-record diff against a fresh DNS export.

Stage B does not itself authorize saving the DNS diff. The final Namecheap
change remains Stage C.

### Stage C — Namecheap web-only DNS cutover

Purpose: point the domain to the approved public site without touching mail.

This stage requires a final approval containing the exact old and new DNS
values, executor, window, and rollback owner. The approved executor may then:

1. Reconfirm the live DNS zone and export a private backup.
2. Add only provider-required ownership/validation records.
3. Replace only the four current GitHub Pages apex A records with the exact
   provider-generated apex records.
4. Add the exact provider-generated `www` CNAME.
5. Configure or verify the canonical redirect from apex to `www` if supported
   by the host.
6. Verify HTTPS, both hostnames, canonical routing, approved page content, and
   the absence of forms or trackers.
7. Return a sanitized action receipt.

Stage C must leave nameservers, transfer lock, MX, SPF, Namecheap forwarding,
and every unrelated TXT record unchanged.

## 4. Proposed DNS end state

Exact provider values are intentionally unavailable until Stage B creates the
custom-domain bindings. Placeholders are not executable DNS instructions.

| Host | Type | Proposed value | Change boundary |
| --- | --- | --- | --- |
| `@` | `A` | `<Sites-generated apex IPv4 target(s)>` | Replace only the four GitHub Pages A records after exact-value approval. |
| `www` | `CNAME` | `<Sites-generated CNAME target>` | Add after exact-value approval. |
| Provider validation host(s) | Provider-specified | `<Sites-generated validation value(s)>` | Add only if required and included in the approved diff. |
| `@` | `MX` | Existing Namecheap forwarding records | No change. |
| `@` | `TXT` SPF | Existing Namecheap forwarding SPF | No change. |
| All unrelated records | Existing | Preserve | No change. |

No wildcard record, URL-frame redirect, registrar transfer, nameserver change,
DNSSEC change, Workspace verification, or mail record belongs in this cutover.

## 5. Acceptance and rollback

### Release acceptance

The public cutover succeeds only if all of the following are true:

- `https://www.grace-mar.com/` returns the approved Grace Mar page over valid
  HTTPS;
- `https://grace-mar.com/` resolves and routes to the chosen canonical host;
- the page displays Grace Mar as the umbrella and Grace Gems as its flagship;
- no LLC status, ownership transfer, product claim, storefront change, form,
  advertising tracker, cookie banner, third-party analytics tag, or
  customer-data collection has been introduced;
- Sites' automatic visitor and page-view measurement has been explicitly
  accepted for the public release;
- mail DNS is byte-for-byte unchanged from the pre-cutover web-only baseline;
  and
- the public site contains no Anyang Intelligence or strategy-codex content.

### Rollback trigger

Rollback the web-only DNS change if HTTPS does not become valid within the
approved window, either hostname returns the wrong site, a provider-generated
record differs from the approved record, mail DNS changes unexpectedly, or the
approved content is not served.

### Rollback action

Restore the four saved GitHub Pages apex A records and remove only the newly
added `www` and provider-validation records. Although this returns the apex to
the prior GitHub Pages 404 state, it restores the known DNS baseline while the
hosting issue is investigated. Do not alter mail records during rollback.

## 6. Missing decisions and unresolved facts

| Item | Required answer or evidence |
| --- | --- |
| Accountable owner | Current operator confirmed as the Sites project owner and hosted-review approver on 2026-08-07. |
| Cost | No Sites price is quoted. Confirm whether `$0` is the required stop ceiling for Stage A. |
| Saved-version review | Confirm that Stage A should save but not deploy a version; review remains local until public release is separately approved. |
| Platform analytics | Confirm whether Sites' automatic unique-visitor and page-view measurement is acceptable. If the requirement is zero host-level traffic measurement, choose another host. |
| Workspace-admin access | Confirm that platform-default workspace-administrator access is acceptable during project review. |
| Public content approval | Name who approves Grace Mar copy and who has authority over the Grace Gems name and brand description. |
| Domain control | Namecheap control by the current operator and a distinct recovery owner are confirmed. Beneficial/legal ownership and private recovery evidence remain unconfirmed here. |
| Legacy Anyang reference | Approve a separate owner to retire or relocate `site_url: https://grace-mar.com` before public cutover. |
| Canonical hostname | Approve `www.grace-mar.com` as canonical and the apex as redirect. |
| DNS executor | Name the authorized Namecheap operator and a distinct rollback owner. |
| Cutover window | Define the maintenance window and maximum propagation/verification period. |
| Exact DNS values | Unavailable until custom-domain binding; they must be returned for approval before Namecheap changes. |
| Slug availability | `grace-mar-landing` has not been reserved; stop if unavailable. |

## 7. Risks and stop conditions

Stop and return the blocker if:

- any hosting price, payment method, recurring commitment, overage, trial, or
  broader access is requested;
- Sites' automatic unique-visitor and page-view measurement conflicts with the
  approved privacy boundary;
- the preferred slug is unavailable;
- project ownership or recovery is uncertain;
- any deployment or public access is required to complete Stage A;
- platform-default workspace-administrator access is unacceptable or broader
  access appears;
- the host requires a domain transfer or nameserver change;
- custom-domain values cannot be obtained before DNS editing;
- the current DNS differs materially from the recorded baseline;
- an action would touch MX, SPF, DKIM, DMARC, Namecheap forwarding, DNSSEC, or
  unrelated TXT records;
- Grace Gems ownership, copy, designs, photography, or customer permissions are
  required beyond the approved landing-page language;
- the legacy Anyang domain reference has not been resolved before Stage C; or
- credentials, recovery codes, payment details, tax IDs, personal addresses,
  signatures, or private records would need to enter Telegram or Git.

## 8. Next approval requested

The next smallest useful approval is Stage A only:

```text
Approved action — Grace Mar saved Sites version

Create one OpenAI Sites project titled “Grace Mar” using the slug
“grace-mar-landing”; stop if that slug is unavailable. Use only the completed
local landing-page source. Save one version and do not deploy it. Confirm the
project is limited to the owner and platform-default workspace administrators;
add no editors, visitors, groups, workspace-wide access, public access, custom
domain, environment variables, database, storage, analytics SDK, forms, or
customer data. Approved spend ceiling: $0. Stop before any fee, trial,
recurring commitment, payment request, quota overage, or broader access.
Return the saved-version number, confirmed access state, and a sanitized
receipt.

Named accountable owner: current operator
```

Approval of Stage A grants no authority for any deployment, public access,
domain binding, DNS changes, email changes, account invitations, or subsequent
versions. Public release also requires explicit acceptance of Sites' automatic
visitor and page-view measurement.
