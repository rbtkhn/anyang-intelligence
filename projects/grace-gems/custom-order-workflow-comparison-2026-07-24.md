# Grace Gems Phase 2 Custom-Order Workflow Comparison

**Review date:** 2026-07-24  
**Related review:** [Phase 2 Storefront First-Review](storefront-first-review-observation-matrix-2026-07-24.md)  
**Evidence boundary:** Public Etsy shop and listing surfaces only  
**Status:** `comparison complete - CEO decision pending; implementation held`

## Executive finding

The public storefronts do not consistently distinguish four materially
different transactions:

1. **Personalization** - engraving, gift message, or another low-complexity
   addition to an existing product.
2. **Configuration** - changing size, metal, stone, or another predefined
   option on an existing design.
3. **Made to order** - producing an existing design after purchase.
4. **Bespoke commission** - developing a new or substantially modified design
   through requirements, quote, design approval, stone approval, production,
   and final acceptance.

Calling all four `custom` creates customer-expectation and operating risk.
Return eligibility, cancellation fees, deposits, change control, delivery
dates, certificates, and approval requirements should not be identical across
these transaction types.

## Public workflow comparison

| Workflow control | GraceGemsUS | GlamGemsBoutique | AmorFineJewelryArt | CrownJewelsCoUS | LaLuneStoneJewelry |
| --- | --- | --- | --- | --- | --- |
| Customer inquiry or reference image | Contact invitation and custom-request field observed | Custom-request field and public custom listing observed | Contact invitation observed | Explicitly requests ideas or reference images | Personalized-request field observed |
| Requirements captured in structured fields | Engraving plus open text; ring/material options vary by listing | Engraving plus open text; some size and metal selectors | Not observed beyond contact/listing options | Not observed as a structured specification | Engraving plus open text; size/material selectors |
| Quote before commitment | Contact for some nonstandard sizing; otherwise not observed | Not observed | Not observed | Free quote explicitly stated | Not observed |
| Deposit or layaway rule | Public 30% layaway language; custom-payment trigger not clearly separated | Public custom layaway listing observed | 30% layaway language; remaining balance within one month | Partial or full payment precedes CAD; another listing states 50% deposit for installment work | 25% installment plan with two-to-three-month payoff window |
| Design or CAD approval | Not observed | Not observed | Not observed | Explicit 3D CAD approval | Not observed |
| Stone selection and approval | Natural-stone and certificate promises observed; order-level approval not observed | Authenticity claims observed; order-level approval not observed | Natural/untreated and appraisal promises observed; order-level approval not observed | Images and videos of selected stones after CAD approval | Natural-stone claims observed; order-level approval not observed |
| Change-control cutoff | Not observed | Free cancellation within 48 hours appears on indexed listings; later deductions mentioned | Not observed | Not observed | 24-hour cancellation window visible in shop policy |
| Production start authorization | Not observed | Not observed | Not observed | Begins after CAD and stone approval | Not observed |
| Published production window | Generally two-to-three weeks; rush language also visible | Listing-specific delivery estimates; one indexed policy describes custom cancellation | Two-to-three weeks; paid rush described as two weeks | Approximately two-to-three weeks | One-to-two weeks on an indexed made-to-order listing |
| Progress updates | Not observed | Not observed | Not observed | Explicit updates during production | Not observed |
| Final image or acceptance gate | Not observed | Not observed | Not observed | Final images and videos before shipping | Not observed |
| Balance-before-shipment rule | Layaway must be resolved, but custom rule is not clearly separated publicly | Custom layaway listing suggests staged payment; general rule not observed | Balance timing stated for layaway, not bespoke work specifically | Full payment before shipment is explicitly stated for installment work | Installment balance paid before shipping |
| Custom cancellation/return consequence | Custom, customized, resized, layaway, sale, and discounted pieces described as final sale | Custom cancellation language appears, but public rules vary by surface | Thirty-day return excludes custom items | A money-back warranty is visible, but custom-specific eligibility is not clear in the bounded evidence | Custom orders and installment orders described as nonreturnable; installment payments nonrefundable |
| Certificate/documentation gate | Appraisal certificate on request for added fee/time | Appraisal language observed at shop level | Appraisal certificate on request for added fee/time | IGI certification on request for added charge | Material authenticity claims observed; order-level certificate rule not observed |
| Aftercare | One-year repair promise appears publicly | One-year repair promise appears at shop level | Free one-year repair warranty | Lifetime paid maintenance after warranty appears on an indexed listing | One-year warranty shown in listing imagery; detailed scope not observed |

`Not observed` means the control was not visible in the bounded public review;
it does not prove that the business lacks the control.

## Strongest existing pattern

[CrownJewelsCoUS](https://www.etsy.com/listing/1874843592/handmade-santa-maria-aquamarine-ring)
shows the most complete public bespoke sequence:

```text
idea or reference image
  -> free quote
  -> partial or full payment
  -> 3D CAD approval
  -> stone images and videos
  -> production
  -> progress updates
  -> final images and videos
  -> shipment
```

This is the best starting pattern, but it is not yet a complete operating
standard. The public sequence does not clearly define the signed specification,
number of included revisions, price-change triggers, approval timeout,
post-approval change cost, certificate decision deadline, defect acceptance
criteria, or custom-specific cancellation and remedy rules.

## Highest-risk gaps

### 1. No common definition of `custom`

An engraving request and a new CAD-designed ring should not carry the same
approval or final-sale rule. The portfolio needs transaction classes before it
needs new customer copy.

### 2. Open-text requests are not an order specification

Several listings invite customers to enter “other custom requests” in a free
text field. That helps discovery but does not reliably capture:

- exact design reference and allowed deviations;
- dimensions and size standard;
- metal type, purity, color, and weight tolerance;
- stone species, treatment, origin, dimensions, color, clarity, and
  substitution permission;
- certificate requirement;
- engraving text and typography;
- budget, deposit, balance, and change fees;
- required-by date versus estimated delivery date;
- packaging and shipping requirements;
- approval evidence.

### 3. Payment often precedes a fully visible approval contract

Public layaway and deposit language exists, but it is not consistently tied to
the moment a design becomes approved, materials become committed, or payments
become nonrefundable.

### 4. Return and warranty language is too coarse

The shops commonly exclude custom items from returns while also making broad
quality, repair, or money-back promises. A bespoke policy must distinguish:

- customer preference change;
- approved-specification change;
- seller deviation from the approved specification;
- material or workmanship defect;
- carrier loss or damage;
- resizing or repair after acceptance.

### 5. Timing language conflates production and delivery

Published windows sometimes describe processing, sometimes rush production,
and sometimes expected arrival. The custom process should separately state
design time, approval time, production time, certification time, carrier time,
and customer-caused delay.

## Proposed minimum custom-order spine

This is an internal control proposal, not approved customer-facing language.

```text
1. classify request
   -> personalization / configuration / made-to-order / bespoke
2. capture specification
   -> product, materials, measurements, stone, certificate, packaging, deadline
3. feasibility review
   -> maker capacity, material availability, claim support, delivery risk
4. quote and terms
   -> price, deposit, revision allowance, cancellation point, estimated dates
5. customer approval
   -> versioned specification and reference images
6. design approval, when applicable
   -> CAD/rendering plus recorded approval
7. material approval, when applicable
   -> stone images/video, treatment disclosure, certificate decision
8. production release
   -> approved version locked; later changes become a documented change order
9. quality check
   -> specification, finish, measurements, setting, engraving, documentation
10. final evidence
    -> photos/video and exception resolution
11. balance and shipment
    -> payment receipt, packaging, carrier, insurance, tracking, delivery promise
12. aftercare
    -> acceptance, defect path, repair/warranty record
```

## Minimum record for one bespoke order

The controlled record should contain:

- unique order identifier;
- storefront and customer-visible product reference;
- request class;
- approved specification version;
- approved reference images or CAD;
- material and stone disclosures;
- certificate requirement;
- quote, deposit, remaining balance, and refundability;
- included revisions and approved change orders;
- production and delivery estimates with assumptions;
- approval timestamps;
- quality-check receipt;
- packaging, carrier, insurance, and tracking receipt;
- warranty and repair rule supplied to the customer.

Customer identity, payment details, private messages, addresses, and order files
must remain in an approved private system and outside Git.

## Recommended pilot

Test the internal control on two future orders only after CEO approval:

- **Fine-jewelry pilot:** one genuinely bespoke order requiring CAD and stone
  approval.
- **Affordable-jewelry pilot:** one personalization or configuration order.

The purpose is to prove that the four transaction classes can use different
levels of control without creating unnecessary work.

## CEO decisions required

1. Approve the four custom-order transaction classes.
2. Decide when payment becomes nonrefundable for each class.
3. Decide which classes require a versioned specification, CAD approval, stone
   approval, and final images.
4. Assign one accountable person for feasibility and promise approval.
5. Authorize or reject the two-order internal pilot.

No storefront, policy, price, customer communication, fulfillment, or
technology change is authorized by this comparison.

## Decision instrument

- [CEO Custom-Order Decision Memo](ceo-custom-order-decision-memo-2026-07-24.md)
