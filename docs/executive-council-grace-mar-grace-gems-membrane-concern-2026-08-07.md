# Executive Council Memo: Grace Mar / Grace Gems Membrane Concern

**Date:** 2026-08-07

**From:** Council Steward posture, read-only

**To:** Executive Council

**Status:** Advisory concern memo - no execution authority

**Subject:** Public-language risk at the Grace Mar / Grace Gems membrane

## Summary

The Grace Mar and Grace Gems membrane is mostly well protected in the repository
governance packets. The Grace Mar formation, website, domain, email, and hosting
packets repeatedly hold LLC filing, DNS changes, Workspace purchase, social
account creation, publication, customer contact, asset transfer, and Grace Gems
storefront changes.

My concern is narrower: the Grace Mar landing-page copy describes Grace Gems as
Grace Mar's flagship jewelry brand before the repository-visible evidence
resolves the existing `Grace Gems LLC`, Grace Gems asset ownership, storefront
ownership, brand-goodwill chain, and public-content approval questions.

This does not mean the copy is false. It means the current public wording is
stronger than the evidence chain available to the Council Steward.

## Finding

`Reconciliation Required`

The controlling Grace Mar packets hold ownership, entity relationship, asset
transfer, and public-claim questions. The website copy, if published as written,
could be read by a public visitor as an ownership, control, or authorized
umbrella-brand representation.

## Evidence Reviewed

- `projects/grace-mar/grace-mar-formation-decision-packet-2026-08-07.md`
- `projects/grace-mar/grace-mar-website-domain-email-packet-2026-08-07.md`
- `projects/grace-mar/grace-mar-hosting-dns-approval-packet-2026-08-07.md`
- `projects/grace-mar/website/app/page.tsx`
- `projects/grace-mar/website/app/layout.tsx`
- `projects/grace-gems/membrane-notes.md`
- `projects/grace-gems/README.md`

## Concern Details

The site copy includes language materially similar to:

- Grace Mar is home to Grace Gems;
- Grace Gems is Grace Mar's flagship jewelry brand; and
- Grace Gems is the first expression of Grace Mar.

The governance packets separately say:

- existing `Grace Gems LLC` relationship is unresolved;
- Grace Gems name, goodwill, creative assets, policies, photography, designs,
  storefronts, customer permissions, and account ownership remain held pending
  evidence;
- no Grace Gems asset may be treated as contributed, transferred, licensed, or
  controlled by Grace Mar until title and authority are established;
- no storefront change, customer contact, commerce, product claim, DNS change,
  email change, publication, or public release is currently authorized.

These two surfaces can coexist only if the public copy is approved as a bounded
brand-positioning statement by the person or people with authority over Grace
Gems and Grace Mar. That approval is not visible in the reviewed repository
evidence.

## Risk

If the page is deployed before reconciliation, the Council risks creating or
amplifying ambiguity about:

- whether Grace Mar already owns, controls, or legally contains Grace Gems;
- whether existing Grace Gems storefronts or assets are migrating;
- whether the existing `Grace Gems LLC` has been reconciled;
- whether Grace Gems public brand copy and claims were owner-approved; and
- whether public release occurred ahead of the entity, asset, and authority
  gates documented in the packets.

This is a membrane risk, not a technical-build risk. The local website may be
structurally valid while still being too strong for public release.

## Recommended Hold

Do not deploy or publicly release the Grace Mar site with the current Grace Gems
relationship language until one of these conditions is met:

1. A repository-visible approval records that the authorized Grace Gems and
   Grace Mar decision owner accepts the exact flagship-brand wording for public
   release; or
2. The public copy is softened so it clearly presents Grace Gems as a planned or
   developing brand direction rather than an established owned/control
   relationship.

## Possible Low-Risk Copy Direction

If the Council wants to reduce ambiguity before approval, use language like:

```text
Grace Mar is preparing a considered jewelry expression through Grace Gems.
```

or:

```text
Grace Gems is a planned flagship jewelry direction for Grace Mar, pending final
ownership, asset, and public-release approvals.
```

These are examples only. They are not approved publication copy.

## Authority Boundary

This memo does not approve, reject, or edit the website. It does not authorize
deployment, DNS changes, Workspace setup, LLC filing, social account creation,
asset transfer, customer contact, storefront change, or public claims.

Any persistent correction requires System Engineer approval and returned
evidence. Any public Grace Gems relationship statement also requires the
appropriate Grace Gems and Grace Mar authority, with private evidence kept out
of Git and represented only through a sanitized receipt or opaque reference.

## Next Decision Needed

Name the authority who can approve the Grace Gems relationship language for the
Grace Mar public site, then either:

- approve the exact wording currently in the landing page;
- approve softened wording for pre-formation/pre-transfer use; or
- hold all Grace Gems relationship language from public release until entity,
  title, storefront, and brand-goodwill questions are resolved.
