# Grace Mar Website, Domain, and Email Packet

**Prepared:** 2026-08-07
**Status:** Read-only decision packet — no setup or publication authority
**Scope:** `grace-mar.com`, the initial Grace Mar website, and Google Workspace
email
**Excluded:** LLC filing, social-account creation, asset transfer, advertising,
customer contact, and changes to existing Grace Gems storefronts

## Decision summary

The domain is registered and under active DNS, but the public website and
Google email are not configured:

- Namecheap is the registrar and DNS host.
- Registration runs through 2027-02-24 and carries a transfer lock.
- The apex domain points to GitHub Pages but currently returns a GitHub Pages
  `404 Site not found` response.
- `www.grace-mar.com` does not exist in public DNS.
- Mail is routed through Namecheap email forwarding, not Google Workspace.
- The only apex SPF record authorizes Namecheap forwarding.
- No public Google Workspace verification, Google DKIM, or DMARC record was
  found.
- DNSSEC is not enabled.
- The repository still identifies `grace-mar.com` as legacy hosting for
  strategy-codex documentation. Grace Mar does not automatically include Anyang
  Intelligence, so that legacy reference must be retired or relocated before
  the domain is treated as Grace Mar's clean commercial web property.

**Recommended path:** prepare the Grace Mar website locally first; reconcile the
legacy Anyang reference and current Namecheap mail forwards; then perform one
approved, staged cutover that configures the chosen website host and Google
Workspace without losing inbound mail.

No DNS record should be changed until the exact current forwarding destinations,
domain owner, Namecheap administrator, Workspace administrators, website host,
and rollback owner are approved.

## 1. Current public domain state

Observed on 2026-08-07. Public DNS and RDAP do not prove who the beneficial
owner is or who controls the Namecheap account.

| Surface | Current public state | Meaning / risk |
| --- | --- | --- |
| Domain | `grace-mar.com` | Registered; operator reports it was acquired for Grace Mar. Beneficial owner and account controller remain unconfirmed. |
| Registrar | NameCheap, Inc. (`IANA 1068`) | The registrar and DNS control plane appear to be Namecheap. |
| Registration date | 2026-02-24 23:29:34 UTC | Public registry fact. |
| Registry/registrar expiry | 2027-02-24 23:29:34 UTC | Renewal owner, auto-renew state, payment method, and renewal ceiling remain private/missing. |
| Domain status | `client transfer prohibited` | Transfer lock is enabled; this is normally protective. |
| Nameservers | `dns1.registrar-servers.com`, `dns2.registrar-servers.com` | Namecheap-hosted DNS. |
| DNSSEC | Not signed | DNSSEC is not enabled. Do not enable during the same window as an unproven nameserver or host migration. |
| Apex A records | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` | These are the current GitHub Pages apex addresses. |
| Apex website | HTTP and HTTPS return GitHub Pages `404 Site not found` | DNS reaches GitHub, but no active GitHub Pages site currently claims or serves the domain. This is both a broken-site condition and a potential custom-domain governance concern. |
| `www` | No DNS record | `www.grace-mar.com` does not resolve. |
| MX | `eforward1`–`eforward5.registrar-servers.com` | Inbound mail is configured for Namecheap forwarding. The actual forwarding addresses are private and unknown. Replacing MX without inventory can break mail. |
| Apex TXT/SPF | `v=spf1 include:spf.efwd.registrar-servers.com ~all` | Only Namecheap forwarding is authorized by the visible SPF record. Google Workspace sending is not yet authorized. |
| Google verification | Not found in visible apex TXT | No public evidence that the domain is verified in a Google Workspace tenant. |
| Google DKIM | `google._domainkey` does not exist | Google-sent mail would not yet be DKIM-authenticated for this domain. |
| DMARC | `_dmarc` does not exist | No public DMARC policy or reporting destination is configured. |

Registry source: [Verisign RDAP for grace-mar.com](https://rdap.verisign.com/com/v1/domain/grace-mar.com).

## 2. Ownership and administration gate

Keep the following evidence outside Git and Telegram. Return only a sanitized
confirmation and opaque private-evidence reference.

| Decision | Required confirmation |
| --- | --- |
| Current domain owner | Legal or individual registrant entitled to control and transfer the domain. Public RDAP is not enough. |
| Intended owner | Grace Mar LLC after formation, or a named temporary custodian with a written duty to hold and later transfer the domain. |
| Primary domain administrator | Current operator confirmed Namecheap account control on 2026-08-07. This does not establish beneficial/legal ownership. |
| Recovery owner | A distinct recovery owner was confirmed on 2026-08-07; identity and recovery details are intentionally not retained in this packet. |
| Registrar recovery | Recovery email/phone are controlled, current, and not dependent solely on the same domain. |
| Renewal | Auto-renew state, approved payment owner, renewal date, quoted renewal price, and spending ceiling. |
| Account security | Unique credentials, phishing-resistant 2FA, transfer lock, registrar lock, and recovery codes stored in the approved private vault. |
| Existing forwarding | Every Namecheap forwarding source and destination, whether it is in use, and whether messages must be preserved. Do not send test mail without approval. |
| Legacy Anyang use | Named owner decides where strategy-codex documentation moves and removes `grace-mar.com` from legacy configuration before commercial cutover. |

## 3. Recommended website architecture

### Public URL structure

| URL | Proposed role |
| --- | --- |
| `https://www.grace-mar.com/` | Canonical Grace Mar umbrella website. |
| `https://grace-mar.com/` | Permanent redirect to `www`. |
| `https://www.grace-mar.com/grace-gems/` | Brand overview for Grace Gems; not a storefront migration. |
| `shop.grace-mar.com` | Reserved for a later approved commerce decision; do not configure now. |

Using `www` as the canonical host makes future host changes easier and keeps the
apex available for a controlled redirect. No wildcard DNS record is proposed.

### Initial website scope

Build locally and review before any hosting or DNS action.

1. **Home:** Grace Mar as a bounded commercial umbrella and Grace Gems as its
   flagship jewelry brand.
2. **Grace Gems:** a restrained brand overview using only owner-approved copy,
   photography, designs, and claims.
3. **About:** approved business identity and contact route. Do not describe
   Grace Mar as an LLC until official formation evidence supports it.
4. **Contact:** `mailto:hello@grace-mar.com` after email cutover. Avoid a web
   form in the first release so the site does not begin collecting customer
   personal data.
5. **Privacy and terms:** counsel/owner-approved notices matched to the actual
   site. Do not paste generic policies or promise data practices that have not
   been implemented.

### Explicit first-release exclusions

- no checkout, payment collection, account creation, or order migration;
- no customer list, newsletter signup, tracking pixel, ad platform, or analytics
  until consent, privacy, and data ownership are approved;
- no testimonials, reviews, customer photos, or customer stories without
  purpose-specific permission;
- no material, origin, certification, shipping, warranty, or custom-order claim
  not already substantiated and owner-approved;
- no import or redirection of the 13 Etsy storefronts;
- no statement that Grace Mar owns Grace Gems assets until the existing
  `Grace Gems LLC` and asset-title questions are resolved; and
- no Anyang Intelligence documentation or project identity on the Grace Mar
  commercial site.

### Hosting recommendation

Use a dedicated Grace Mar-controlled website account and repository, separate
from Anyang Intelligence and the legacy strategy-codex documentation.

| Option | Fit | Commitment / issue | Disposition |
| --- | --- | --- | --- |
| Commercial static host with source control | Best for the initial umbrella/brand site | Provider, ownership, price, privacy, deployment, rollback, and account-recovery controls must be approved | **Recommended; exact vendor still missing** |
| Managed site builder | Fast nontechnical editing | Recurring subscription and platform lock-in; content rights and admin recovery still required | Credible alternative if the human owner will maintain the site directly |
| Shopify | Appropriate for a later approved Grace Gems store | Recurring commerce commitment, payment/tax/privacy setup, and storefront migration questions | Defer; do not use merely to host the Grace Mar umbrella page |
| Existing GitHub Pages target | DNS is already pointed there, but the site is unclaimed/broken and GitHub Pages has commercial-use limits | Requires verified domain, correct account/repository ownership, public-content discipline, and policy review | Do not reactivate by default; choose only after confirming the site is within GitHub Pages terms |

GitHub warns that DNS should not point at a Pages custom domain unless the
domain has first been added and verified in the intended repository/account;
otherwise a takeover risk can exist. See [GitHub custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
and [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## 4. Google Workspace architecture

### Plan and recurring cost

**Proposed:** Google Workspace Business Starter, Flexible Plan, with two named
users.

| Item | Current standard quote | Proposed limit |
| --- | --- | --- |
| One Business Starter Flexible user | `$8.40 USD/month` | One seat per approved individual who needs a mailbox/login. |
| Two named users | `$16.80/month`; `$201.60/year` before tax/discounts | Recommended secure minimum: primary administrator plus distinct recovery administrator. |
| Annual/Fixed-Term alternative | `$7/user/month`; two users `$168/year` equivalent | Defer because it creates a term commitment while ownership and staffing remain unsettled. |
| Role groups and user aliases | No separate paid mailbox proposed | Confirm Google's then-current terms during setup; no functional paid seats should be created by default. |

Pricing source: [Google Workspace pricing](https://workspace.google.com/pricing.html).

### Accounts and addresses

| Address | Type | Paid user? | Initial control |
| --- | --- | --- | --- |
| `[primary-person]@grace-mar.com` | Named user; initial primary super admin | Yes | One named accountable human. |
| `[recovery-person]@grace-mar.com` | Named user; second super admin/recovery owner | Yes | A different named accountable human. |
| `hello@grace-mar.com` | Google Group | No extra seat proposed | Both users initially; public general inquiries. |
| `support@grace-mar.com` | Google Group / collaborative inbox | No extra seat proposed | Approved support owner plus backup. |
| `social@grace-mar.com` | Restricted Google Group | No extra seat proposed | Social account owner and recovery owner; notices only, never passwords/codes. |
| `legal@grace-mar.com` | Restricted Google Group | No extra seat proposed | Primary owner and approved legal recipient. |
| `finance@grace-mar.com` | Restricted Google Group | No extra seat proposed | Finance owner and one backup. |

No shared `admin@` login is proposed. Each administrator should have an
individually attributable account. The five role addresses should be groups,
not paid user mailboxes, unless later workflow evidence shows a true standalone
mailbox is required.

## 5. Proposed DNS end state

Values that depend on the selected website host or Google-generated token are
shown as placeholders. They must be copied from the approved systems at action
time and returned for review before saving.

| Host | Type | Proposed value | Timing |
| --- | --- | --- | --- |
| `www` | `CNAME` or provider-prescribed record | `<approved-website-host-target>` | After the host account, deployment, custom-domain claim, and rollback are ready. |
| `@` | Host-prescribed apex record or redirect | `<approved-apex-target>` | Same website window; replace the current GitHub Pages A records only after approval. |
| `@` | `TXT` | `google-site-verification=<Google-generated-token>` | After Workspace tenant purchase; verification does not itself redirect website or mail. |
| `@` | `MX` | Priority `1`, `smtp.google.com` | Cutover only after users/groups, recovery, forwarding inventory, and rollback are complete. Remove Namecheap forwarding MX records in the same approved change. |
| `@` | `TXT` SPF | `v=spf1 include:_spf.google.com ~all` if Google is the only sender | Replace the Namecheap-forwarding SPF only after confirming every legitimate sender, including future website/contact/commerce systems. Publish only one SPF record. |
| `google._domainkey` | `TXT` | Google-generated 2048-bit DKIM public key | Generate after Gmail activation; publish, wait for propagation, then start authentication. |
| `_dmarc` | `TXT` | Monitoring policy drafted from approved report destination | Add only after SPF/DKIM align and a private report mailbox/vendor is approved. Begin with monitoring; strengthen policy after reviewing reports. |
| `@` | DNSSEC/DS | Registrar-generated values | Separate later maintenance window after website and email are stable. |

Google's current documentation uses a single Workspace MX destination,
`smtp.google.com`, with priority `1`, and warns that keeping old/incorrect MX
records can disrupt delivery. See [Google Workspace MX setup](https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace).
Google also recommends SPF, DKIM, and DMARC; see [SPF](https://support.google.com/a/answer/33786),
[DKIM](https://knowledge.workspace.google.com/admin/security/set-up-dkim), and
[DMARC](https://knowledge.workspace.google.com/admin/security/set-up-dmarc).

## 6. Cutover-safe execution sequence

Every numbered phase requires an exact approval naming the executor, systems,
records, spending ceiling, and rollback condition. Approval of one phase does
not authorize a later phase.

### Phase 0 — private control inventory

1. Confirm domain registrant/beneficial owner and intended Grace Mar custody.
2. Confirm Namecheap primary admin, distinct recovery owner, 2FA, recovery, lock,
   expiry, auto-renew, payment owner, and renewal quote.
3. Export or record the existing DNS zone privately and create a sanitized DNS
   baseline receipt.
4. Inventory every Namecheap mail forward and destination without sending mail.
5. Decide the destination for legacy Anyang/strategy-codex documentation and
   remove the Grace Mar domain reference from that lane under separate Anyang
   authority.

### Phase 1 — local website draft

1. Approve the website host and accountable owner.
2. Create the dedicated Grace Mar site repository/account only under separate
   authorization.
3. Build and review the first-release pages locally or at a non-public preview
   URL.
4. Complete brand, rights, claim, privacy, accessibility, responsive-layout,
   link, metadata, favicon, and error-page review.
5. Approve the exact public content and deployment artifact.

### Phase 2 — Workspace preparation before MX

1. Approve Business Starter Flexible and maximum recurring spend.
2. Create exactly two named users and identify primary/recovery admins.
3. Enforce phishing-resistant 2FA and store recovery evidence privately.
4. Create the five role groups with restricted membership and posting rules.
5. Add the Google verification TXT record and verify the domain. Google says
   domain verification itself does not affect the website or email.
6. Confirm unmanaged Google-account conflicts for the domain before assigning
   addresses.

### Phase 3 — coordinated website and mail cutover

1. Configure and verify the domain inside the approved website host before
   changing website DNS.
2. Apply the approved `www` and apex records; remove the broken GitHub Pages
   target only within the approved rollback window.
3. Confirm HTTPS, redirects, canonical URL, page content, and absence of
   unauthorized tracking or forms.
4. Replace Namecheap forwarding MX records with Google's single MX record only
   after the approved users/groups and preserved forwarding map are ready.
5. Update SPF for every approved sender; do not leave two SPF records.
6. Activate Gmail, wait for propagation, and run approved inbound/outbound tests
   using non-customer test recipients.
7. Generate and publish 2048-bit Google DKIM; start authentication after DNS
   propagation.
8. Publish a monitoring DMARC policy only after the reporting destination and
   privacy handling are approved.
9. Return one sanitized action receipt for website DNS and one for email/DNS.

### Phase 4 — stabilization

1. Monitor DNS, HTTPS, inbound/outbound delivery, SPF/DKIM/DMARC results, group
   routing, and admin alerts for the approved window.
2. Confirm current mail forwards were either reproduced or explicitly retired.
3. Remove stale DNS only after supported use is disproved.
4. Schedule renewal review at least 60 days before 2027-02-24.
5. Consider DNSSEC in a separate change window.

## 7. Exact decisions needed next

| Decision | Missing answer |
| --- | --- |
| Website role | Is the first release an umbrella landing site only, or does it include a Grace Gems brand page? This packet recommends both, without commerce. |
| Host | Which commercial static host or managed builder, who owns the account, and what recurring ceiling is approved? |
| Content owner | Who approves Grace Mar copy and who separately approves Grace Gems brand assets and claims? |
| Domain owner/admin | Who currently owns and controls the Namecheap registration, and who is the distinct recovery owner? |
| Legacy site | Where will strategy-codex documentation move, and who is authorized to update that Anyang configuration? |
| Existing email forwards | What addresses currently forward through Namecheap and must remain live? |
| Workspace admins | Name the primary and distinct recovery administrator. |
| Workspace spend | Approve or reject two Business Starter Flexible seats at the then-current price, with an exact monthly ceiling. |
| Role-group membership | Name initial members of `hello`, `support`, `social`, `legal`, and `finance`. |
| Private evidence | Name the approved vault/location and the person responsible for domain, billing, recovery, and DNS evidence. |
| Cutover | Name executor, maintenance window, test recipients, rollback owner, and stop conditions. |

## 8. Stop conditions

Stop and return the exact blocker if:

- domain ownership, Namecheap control, recovery, or renewal is uncertain;
- existing Namecheap forwarding destinations cannot be inventoried;
- changing MX would interrupt a known or possibly used address;
- the website host introduces an unapproved recurring commitment or requires
  domain transfer/nameserver changes outside the approved plan;
- the requested website content claims Grace Mar LLC exists before filing;
- Grace Gems assets, testimonials, photos, designs, claims, storefronts, or
  customer data would change or be reused without owner evidence;
- the legacy Anyang domain use is not reconciled;
- a platform requests payment, ID, tax data, personal address, signature,
  credentials, recovery codes, or public verification outside the approved
  private channel;
- the live DNS differs materially from this baseline at action time; or
- the website or mail tests fail and rollback cannot be completed inside the
  approved window.

## 9. Next approval boundary

The next useful approval is **not DNS cutover**. It is a bounded, private
inventory plus a local website draft:

```text
Approved action 1: Inspect and privately inventory Namecheap control,
renewal, current DNS, and current email-forwarding destinations; return only a
sanitized receipt and opaque evidence references.

Approved action 2: Build a non-public Grace Mar website draft containing the
approved umbrella home page and a bounded Grace Gems overview; no deployment,
forms, analytics, commerce, customer data, or DNS changes.
```

Workspace purchase, account creation, public deployment, MX replacement, SPF,
DKIM, DMARC, DNSSEC, email testing, and customer-facing publication remain held
until separately approved with exact limits.
