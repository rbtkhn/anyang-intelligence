# Grace Gems Phase 2 Shipping-Origin Claim Review

**Review date:** 2026-07-24  
**Related review:** [Phase 2 Storefront First-Review](storefront-first-review-observation-matrix-2026-07-24.md)  
**Evidence boundary:** Public Etsy shop and listing surfaces only  
**Status:** `evidence review complete - owner verification required; no changes authorized`

## Executive finding

Three storefronts contain confirmed public inconsistencies between narrative
production or shipping-origin statements and Etsy's visible dispatch location:

- CrownJewelsCoUS;
- ForgeFacetUS;
- StoneCraftArtistry.

This review does not establish the actual production or logistics arrangement.
It establishes that a customer can encounter statements that are difficult to
reconcile and that owner evidence is required before recommending corrections.

## Evidence matrix

| Storefront | Narrative statement observed | Etsy dispatch evidence observed | Assessment |
| --- | --- | --- | --- |
| [CrownJewelsCoUS](https://www.etsy.com/listing/1874843592/handmade-santa-maria-aquamarine-ring) | “Every item is handmade in Denver Colorado, United States” | “Ships from: Hong Kong” | **Confirmed public inconsistency.** Production, quality-control, and dispatch locations need separate verification. |
| [ForgeFacetUS](https://www.etsy.com/listing/4409901905/unique-jadeite-jade-flower-stud-earrings) | Listings state that all items are shipped from the U.S.; some also state free shipping from the U.S. with no tariffs | “Ships from: Hong Kong”; another indexed listing displays a possible tariffs/duties notice | **Confirmed public inconsistency.** Dispatch and tariff language require immediate verification. |
| [StoneCraftArtistry](https://www.etsy.com/listing/1804102720/blue-topaz-earrings-gold-plated-silver) | “All items are shipped from the U.S. with worldwide delivery available” | “Ships from: Hong Kong” | **Confirmed public inconsistency.** The customer-visible shipping-origin promise needs verification. |
| [GraceGemsUS](https://www.etsy.com/listing/918181582/custom-14k-gold-diamond-engagement-ring) | Made and shipped from a Denver workshop | “Ships from: Littleton, CO” | **No material conflict in the sampled evidence.** Denver and Littleton wording is geographically close but should still use an approved location standard. |
| [AmorFineJewelryArt](https://www.etsy.com/listing/1624119016/genuine-emerald-18k-rose-gold-ringdainty) | Crafted and shipped from Denver | “Ships from: Littleton, CO” | **No material conflict in the sampled evidence.** Use one precise customer-facing location convention. |
| [LaLuneStoneJewelry](https://www.etsy.com/listing/1662950403/dainty-icy-green-jade-ring-18k-gold) | Jewelry may ship from Canada and the U.S. | Sampled listing: “Ships from: Littleton, CO” | **Compatible but underspecified.** The rule determining Canadian versus U.S. dispatch was not observed. |

The remaining storefronts were not assessed as consistent or inconsistent
because the bounded evidence did not provide both a narrative origin statement
and a reliable dispatch field.

## Why this matters

`Designed in`, `made in`, `quality checked in`, `warehoused in`, `sold from`,
and `shipped from` describe different facts. Treating them as interchangeable
can affect:

- customer expectations about craftsmanship and provenance;
- delivery-time expectations;
- tariff, duty, and import-fee expectations;
- return routing and cost;
- marketplace policy accuracy;
- the credibility of an independent Grace Gems website.

The issue is not that international production or dispatch is inherently
problematic. The issue is whether each public statement accurately describes
the specific product and fulfillment path.

## Minimum owner evidence request

Do not request a broad order, supplier, or logistics export. For each of the
three flagged storefronts, request only a sanitized answer for each active
fulfillment pattern:

1. Where is the product designed?
2. Where are its main manufacturing steps performed?
3. Where is final quality control performed?
4. From which country and city is the parcel first accepted by the carrier?
5. Is the order shipped from stocked U.S. inventory, transferred to the U.S.
   before customer dispatch, or sent directly from another country?
6. Who is responsible for duties, tariffs, and import fees?
7. Which return location is supplied to the customer?

The response should identify product or fulfillment **patterns**, not customer
names, addresses, order numbers, supplier identities, or financial details.
Any supporting private records must remain outside Git in an approved private
location.

## Recommended source-of-truth fields

For each product or fulfillment pattern:

| Field | Required value |
| --- | --- |
| Design location | Country and, only if publicly used, city |
| Manufacturing location | Country or countries plus responsible production stage |
| Final quality-control location | Country and accountable role |
| Inventory location | Country or `made to order` |
| Carrier acceptance location | Country and, where material, city |
| Customer-facing dispatch statement | Approved exact wording |
| Duties and tariffs | Seller-paid, buyer-paid, included, or conditional |
| Return destination | Country and approved disclosure rule |
| Evidence owner | Accountable internal role |
| Last verified | Date |

## Decision boundary

After the owner verifies the operating facts, the Executive Council may prepare
a correction recommendation. It must not directly edit listings or infer that
all products in a shop use the same fulfillment path.

No listing, website, policy, price, customer communication, production,
fulfillment, return, or spending change is authorized by this review.

## Owner-verification instrument

- [Shipping-Origin Owner Verification Request](shipping-origin-owner-verification-request-2026-07-24.md)
