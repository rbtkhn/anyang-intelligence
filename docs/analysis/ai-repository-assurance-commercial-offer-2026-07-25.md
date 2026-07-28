# AI Repository Assurance Review — Commercial Offer Design

**Offer ID:** `AI-REPOSITORY-ASSURANCE-REVIEW-01`  
**Prepared by:** Chief Executive  
**Decision source:** System Engineer selections `B. Design the repository
assurance audit as a commercial offer` and `B. Develop the audit into a
commercial service offer`
**State:** `internal offer design; not approved for sale, outreach, contracting, delivery, spending, or kernel adoption`  
**Evidence base:** three technical benchmarks, including the [Narrative Systems
audit packet](cross-repo-audits/narrative-systems-2026-07-25/audit-packet.md)
and the [Predictive History audit
packet](cross-repo-audits/predictive-history-2026-07-25/audit-packet.md)
**Current kernel disposition:** `revise`

## Structural conclusion

Anyang Intelligence should develop a fixed-scope **AI Repository Assurance
Review** for small teams that use a Git repository as an AI operating
environment, durable knowledge system, or governed content-production system.

The offer tests one question:

> Does the repository's declared operating state have enough mechanical and
> evidence-lineage support for its owner to rely on it?

This is not a broad code review. It combines a deterministic, read-only
collector with independent Council Steward review and a concise Chief
Executive decision brief. The customer buys prioritized operating confidence,
not a large diagnostic count or an automatic cleanup.

The offer remains pre-commercial until the proof gate in this design passes.
No client solicitation, proposal, price quotation, contract, private access,
or delivery is authorized by this document.

## Development status after the third benchmark

Predictive History completed the previously required third technical
benchmark. It materially strengthened the commercial case:

- all 1,332 tracked files were inventoried without changing the target;
- the repository's 91 native tests passed, yet independent review identified
  eight accepted material finding groups;
- 1,123 mechanical candidates were consolidated into nine findings and seven
  root causes;
- required trace reconstruction reached 39/40, or 97.5%;
- the deterministic broken-link precision sample reached 40/40;
- the System Engineer accepted `PH-STW-01` through `PH-STW-08`;
- the audit produced a bounded remediation plan without allowing findings to
  become repair authority.

This proves a commercially legible customer problem: native tests can pass
while publication paths, source-of-truth inventories, generated navigation,
schemas, and portability controls remain unreliable.

The offer is still not ready for sale. Predictive History is technically
different from Narrative Systems but shares owner and conceptual lineage.
Narrative Systems findings remain unadjudicated, complete labor time is not
instrumented, customer-safe delivery has not been rehearsed, private-repository
handling is unapproved, and an unrelated owner-controlled benchmark remains
required before broad portability claims.

## Why a buyer would purchase it

AI-operated repositories accumulate a distinct class of operating failures:

- instructions say a workflow is active when its runtime or evidence is not;
- manifests, dashboards, and indexes disagree with actual files;
- generated artifacts lose source or approval lineage;
- one controlling defect appears as dozens of unrelated failures;
- machine-local paths masquerade as portable dependencies;
- old drafts, templates, and historical receipts are treated as current state;
- agent output becomes apparent corroboration for the source that generated it;
- a polished artifact appears complete without the approval or evidence needed
  for operational use.

Conventional dependency and security tools remain important, but they answer a
different question. GitHub's supply-chain controls focus on dependencies,
vulnerabilities, build provenance, and attestations. The Anyang review focuses
on declared operating truth, artifact state, authority, and evidence lineage
inside the repository.

The adjacent standards environment supports the need for this category:

- the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
  organizes AI risk work around govern, map, measure, and manage, and its AI
  Resource Center explicitly supports testing, evaluation, verification, and
  validation;
- the [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
  addresses generative-AI-specific governance and content-provenance risks;
- [ISO/IEC 42001](https://www.iso.org/standard/42001) establishes an AI
  management-system framework around governance, traceability, transparency,
  risk, and continuous improvement; and
- [GitHub artifact provenance guidance](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity)
  demonstrates the value of auditable provenance while remaining narrower than
  the repository-state problem addressed here.

Anyang must not describe the offer as NIST conformity, ISO certification,
legal compliance, cybersecurity assurance, or a substitute for those
disciplines.

## Ideal customer profile

### Best-fit buyer

- Founder, technical operator, research director, editorial director, or AI
  operations lead.
- Team of roughly 1–50 people.
- One repository is a material operating surface, not merely source-code
  storage.
- The repository contains agent instructions, generated documents, manifests,
  operating state, research evidence, client-delivery state, or approval
  controls.
- The owner can identify one consequential decision that depends on trusting
  the repository.
- The owner will authorize a sealed, read-only snapshot and the exact native
  validation commands.

### Purchase triggers

- An AI operating system has grown faster than its documentation.
- A migration or major agent-generated change set needs independent review.
- The team cannot tell which artifacts are controlling, current, or complete.
- Native checks produce a noisy or cascading failure set.
- A client, investor, executive, or regulator asks how AI outputs retain
  provenance and approval state.
- The repository is about to become a reusable template, managed service, or
  customer-facing operating system.

### Disqualifiers

Hold or decline the review when:

- the requested outcome is penetration testing, vulnerability assessment,
  formal financial audit, legal opinion, regulated certification, or
  substantive fact-checking;
- access would expose secrets, credentials, payment data, direct personal
  identifiers, child records, medical records, privileged material, or client
  data without an approved handling membrane;
- the customer expects Anyang to fix, publish, migrate, or operate the
  repository under the review authorization;
- repository ownership or authorization is unclear;
- the customer cannot identify controlling surfaces or permit a bounded
  discovery phase;
- the repository depends on private systems that cannot be represented through
  sanitized receipts; or
- the expected review cannot fit a fixed scope without misleading coverage
  claims.

## Customer-visible promise

At completion, the customer receives an evidence-backed answer to:

1. What repository snapshot was actually reviewed?
2. Which declared controls ran, failed, passed, or were unavailable?
3. Which state and lineage claims were supported, contradicted, stale, or
   inaccessible?
4. Which raw diagnostics collapse into the same controlling root cause?
5. Which problems have the greatest operating consequence?
6. What should be retained, fixed, narrowed, retired, or investigated?
7. What evidence and authority would be required before remediation?

The review does not promise zero defects, complete semantic coverage, or proof
that claims about the external world are true.

## Founding-pilot scope

### Included

- One Git repository.
- One sealed branch, commit, or approved dirty-snapshot manifest.
- Up to 5,000 tracked files and 250 MB of tracked content.
- Up to two repository-declared read-only native commands.
- Full tracked-file inventory and snapshot fingerprint.
- Structured-file, link, machine-local-path, and declared-control diagnostics.
- Deterministic sampling of up to 20 high-consequence trace chains.
- Root-cause consolidation.
- Independent Council Steward finding ledger.
- Chief Executive operating implications.
- One System Engineer release review.
- One 60-minute customer readout through the Executive Assistant, if
  separately authorized.
- One bounded remediation-plan option; remediation execution is excluded.

### Excluded

- Repository writes or cleanup.
- Pull requests, issues, commits, pushes, or publication.
- Penetration testing, secret scanning guarantees, dependency vulnerability
  assurance, legal review, or compliance certification.
- External research or verification of substantive domain claims.
- Runtime production-system access.
- Private-system exploration beyond explicitly approved, sanitized evidence.
- Cross-client comparison using protected context.
- More than one reconciliation round.

Unexpected scope returns to qualification; it does not silently expand the
review.

## Deliverable chain

The customer receives three consolidated deliverables:

1. **Snapshot and collector receipt**
   - reviewed identity;
   - commands, exit states, duration, and coverage;
   - inventory and objective diagnostics;
   - mutation proof and declared limitations.
2. **Independent assurance ledger**
   - verified defects;
   - inferred risks;
   - inaccessible evidence;
   - environment-only failures;
   - supported controls;
   - root-cause groups;
   - sealed initial findings.
3. **Executive decision brief**
   - consequence-ranked implications;
   - `retain / fix / narrow / retire / investigate` classifications;
   - immediate operating holds;
   - remediation choices;
   - adoption or next-review recommendation.

Internally, these may remain sections of the existing Council transaction,
collector receipt, and audit-packet family. The customer-facing presentation
must remove internal-only paths, runtime identifiers, unrelated portfolio
context, and protected Council deliberation without changing the finding
substance.

## Delivery protocol and role separation

```text
Customer technical authority identifies the repository and decision
  -> Executive Assistant returns bounded qualification evidence
  -> Chief Executive prepares exact scope and commercial recommendation
  -> System Engineer approves Anyang access, terms, price, and execution
  -> customer authority approves repository access and review boundary
  -> named collector executor seals and mechanically inspects the snapshot
  -> Council Steward independently reviews primary evidence
  -> Chief Executive prepares consequence-ranked implications
  -> System Engineer approves, revises, holds, or rejects external delivery
  -> Executive Assistant delivers the approved packet and records receipt
  -> any remediation requires a new dual-authority decision
```

Minimum Steward independence:

- separate role and runtime identity;
- direct access to the sealed primary evidence packet;
- no Chief Executive hypotheses before the initial ledger is sealed;
- separate prompt and reporting path;
- disclosed model-family overlap;
- no authority to rewrite, fix, price, sell, or approve;
- later interpretation appended without overwriting the sealed ledger.

The Artistic Director is not part of the analytical review. It may later
prepare an approved customer-facing visual system or report layout without
changing findings, severity, evidence, or authority state.

## Pricing and unit-economics hypotheses

Pricing remains a hypothesis until the proof cohort establishes real review
hours and customer willingness to pay.

| Stage | Scope | Price hypothesis | Commercial state |
| --- | --- | ---: | --- |
| Founding pilot | One repository under the limits above | `$3,000` fixed fee | Test only after proof gate and explicit sale approval |
| Standard review | Same core scope with proven delivery baseline | `$5,000` fixed fee | Held until at least three accepted pilots |
| Larger or multi-repository review | Custom scope | No current price | Decline or scope separately |
| Continuous assurance | Monthly delta collection plus quarterly trace review | `$1,000/month` hypothesis | Do not sell until fixed reviews prove repeatable |
| Remediation | Separately approved implementation | No current price | New statement of work required |

The founding price is viable only if:

- total Anyang delivery effort is at most eight hours;
- combined Chief Executive and System Engineer review remains at most two
  hours;
- direct delivery cost remains at or below `$1,200`;
- gross contribution is at least `$1,800`, or 60%;
- there are no unpriced external research, private-access, travel, tool,
  legal, or specialist-review costs.

Because Anyang does not yet have an approved fully loaded hourly-cost model,
these are planning constraints, not demonstrated margins.

At the current `$14,000/month` operating-cost planning baseline, five founding
reviews would produce `$15,000` in monthly revenue before taxes, unrecorded
costs, capacity limits, or collections risk. That arithmetic is not a sales
forecast. A more durable model would combine fewer standard reviews with
separately proven recurring assurance revenue.

## Proof-before-sale gate

Do not market or sell the standard offer until:

- the System Engineer adjudicates each Narrative Systems material finding;
- one unrelated owner-authorized repository benchmark is completed;
- the kernel outcome is `adopt` or a commercially sufficient bounded
  `narrow`, not `revise`;
- total preparation, collection, Steward review, Chief Executive review, and
  System Engineer review minutes are recorded;
- at least 80% of material findings are accepted without substantive revision;
- false-positive findings remain at or below 20%;
- deterministic collection and trace reconstruction each reach at least 90%;
- the complete founding scope can be delivered in eight Anyang hours or less;
- customer-safe redaction and delivery have a tested checklist;
- private-repository handling, deletion, retention, credential, and incident
  rules are approved before any private pilot;
- code ownership and commercial-use rights for the collector are explicit;
- there are zero unauthorized writes, protected-context transfers, external
  communications, or scope expansions.

The first commercial pilot additionally requires a named customer, repository
authority, contract, price, payment terms, data boundary, deletion date,
liability boundary, evidence-return requirements, and stop conditions. This
design supplies none of those approvals.

## Remaining internal productization cohort

### Phase 1 — close benchmark evidence gaps

- Adjudicate the Narrative Systems findings.
- Record or conservatively reconstruct preparation, Steward, Chief Executive,
  and System Engineer review minutes for all three benchmarks.
- Freeze a versioned founding scope and exclusion list.
- Confirm collector ownership and permitted commercial use.

### Phase 2 — unrelated portability benchmark

- Select one owner-controlled repository that is structurally and
  conceptually unrelated to Narrative Systems and Predictive History.
- Run the kernel read-only under an exact System Engineer authorization.
- Measure all labor, tool, review, and reconciliation minutes.

### Phase 3 — customer-safe delivery rehearsal

- Use the [founding-pilot offer
  sheet](ai-repository-assurance-founding-pilot-offer-sheet-2026-07-25.md) as
  the proposed commercial boundary.
- Redact one public-evidence packet as if it were customer-facing.
- Test whether a technically informed owner can identify the first three
  decisions in under 15 minutes.
- Have the Council Steward confirm that redaction did not change finding
  meaning.

### Phase 4 — commercial adjudication

- Compare observed cost with the `$3,000` founding price.
- Decide `sell / revise / narrow / retire`.
- If `sell`, separately authorize one named founding-customer outreach through
  the Executive Assistant.

No public launch, outbound campaign, proposal, or customer contact occurs
inside this cohort without a later approval.

## Commercial scorecard

### Delivery quality

- tracked inventory coverage;
- trace reconstruction rate;
- accepted-finding precision;
- false-positive rate;
- root-cause compression ratio;
- material evidence gaps identified before reliance;
- customer-ranked decision usefulness;
- unauthorized mutation or context-transfer events.

### Economics

- qualification minutes;
- setup and adapter minutes;
- collector runtime and intervention minutes;
- Steward review minutes;
- Chief Executive interpretation minutes;
- System Engineer review minutes;
- Executive Assistant coordination and readout minutes;
- total direct cost;
- realized price;
- gross contribution and gross-margin percentage;
- remediation-plan conversion;
- repeat-review or continuous-assurance conversion.

### Sales learning

- qualified opportunities;
- purchase trigger;
- proposal-to-close rate;
- time to close;
- primary objection;
- disqualification reason;
- price acceptance;
- customer segment;
- time to first decision-useful finding.

Revenue, margin, and conversion remain zero until supported by contracts,
payments, time records, and accepted delivery evidence.

## Principal risks and controls

| Risk | Consequence | Control |
| --- | --- | --- |
| “Audit” implies certification or security assurance | Legal, trust, and scope exposure | Use “AI Repository Assurance Review”; state exclusions in proposal and readout |
| Customer expects automatic remediation | Unpriced labor and authority confusion | Separate review and remediation statements of work |
| Private evidence crosses clients | Severe privacy and trust failure | Repository-specific membrane, sanitized packet, deletion date, no cross-client examples |
| Large diagnostic counts inflate value | Misprioritization and reputational harm | Deduplicate and consolidate controlling root causes |
| Steward merely repeats Chief Executive framing | False independence | Primary-evidence-first review and sealed ledger |
| Fixed price hides unbounded scope | Negative margin | Hard file, size, command, trace, and reconciliation limits |
| Standards references become compliance claims | Misrepresentation | Describe alignment only; never certify NIST or ISO conformity |
| Tool output is treated as substantive truth | Unsafe customer reliance | Separate mechanical diagnostics from semantic findings and domain truth |
| Attractive report outruns evidence | Unsupported external claims | System Engineer release gate and Executive Assistant evidence receipt |

## Commercial positioning

Recommended one-line description:

> **Anyang Intelligence tests whether an AI-operated repository's declared
> state, controls, and evidence lineage are trustworthy enough to rely on—and
> reduces noisy symptoms to the few decisions that matter.**

Do not lead with:

- “AI governance transformation”;
- “complete AI audit”;
- “compliance certification”;
- “security assessment”;
- “autonomous remediation”;
- “we verify your AI is correct.”

## Exact next System Engineer decision

- **A. Approve the remaining internal proof cohort:** adjudicate the Narrative
  Systems findings, run one unrelated owner-controlled benchmark, measure
  delivery burden, and rehearse a customer-safe packet; no outreach or sale.
- **B. Revise the offer design:** change buyer, scope, pricing, proof gate, or
  positioning before any cohort.
- **C. Hold commercialization:** preserve the design without further kernel
  work, outreach, or sale.
