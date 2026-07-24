# Executive Council Steward Pilot - Activation Receipt

**Receipt status:** `active - sealed read-only pilot; baseline authorized`  
**Receipt ID:** EC-STEWARD-ACTIVATION-2026-07-24-01  
**Pilot scope:** Executive Council portfolio, with Grace Gems as the first
review focus  
**Logical Steward identity:** `executive_council_steward_pilot_01`  
**Related approval:** [Engineer Approval Receipt](council-steward-pilot-engineer-approval-receipt-2026-07-24.md)  
**Related role contract:** [Council Steward Role Contract](../../docs/council-steward-role-contract.md)

> **The Engineer activated the bounded 30-day pilot. The named Steward may read
> only the sealed source manifest and must remain within every boundary below.**

## Activation purpose

This receipt reserves a distinct logical identity and records the controls that
had to be complete before the first Council Steward runtime pilot could begin.
The Steward is an organization-wide Executive Council role; Grace Gems is the
first review focus, not the role's organizational container. Before the
activation decision below was completed, this receipt did not grant source
access. The completed activation gate and Engineer activation decision now
control the bounded pilot.

## Named implementation

- Logical instance name: `executive_council_steward_pilot_01`;
- Implementation class: separate Codex Council Steward AI review instance;
- Proposed model: `gpt-5.6-sol`;
- Actual model and runtime identity: `gpt-5.6-sol` requested through the Codex
  collaboration runtime; the instance self-identifies generically as a Codex
  agent based on GPT-5;
- Actual agent or instance ID:
  `/root/executive_council_steward_pilot_01`;
- Role prompt: exact sealed version of
  `docs/council-steward-role-contract.md`;
- Review context: assembled from the sealed approved source map, not copied
  from the Chief Executive's narrative context;
- Ability to spawn or delegate: prohibited;
- External network, application, account, or communication access: prohibited.

The activation mechanism returned the canonical instance identity above. The
instance entered `READY-HOLD` without reading workspace sources and awaited
the sealed release.

## Authority and role separation

- Engineer: activates, constrains, reviews, pauses, or revokes the pilot;
- Chief Executive: prepared the pilot recommendation and does not act as the
  Steward;
- Executive Assistant: remains the Council's only real-world interface and is
  not contacted or directed by the Steward;
- Council Steward: organization-wide Council role that performs only bounded
  state-and-receipt review after its runtime is activated;
- Grace Gems CEO: retains client-business decision authority.

## Approved permission boundary

After activation, the named Steward may read only:

- `authority-envelope.yaml`;
- `docs/executive-council-role-contract.md`;
- the exact sealed version of `docs/council-steward-role-contract.md`;
- `docs/governance.md`;
- `docs/membranes.md`;
- `docs/data-handling-policy.md`;
- `docs/executive-interface-protocol.md`;
- `templates/chief-executive-brief.md`;
- `templates/approval-receipt.md`;
- `templates/executive-assistant-action-receipt.md`;
- `templates/executive-council-pilot-receipt.md`;
- repository-visible artifacts under `projects/`, with source provenance and
  project membranes preserved;
- Git status, diff, log, and file lineage for this repository, read-only.

The Steward may not:

- read any source before activation;
- access private customer, order, supplier, employee, financial, credential,
  analytics, message, attachment, or tenant-system evidence;
- open the operator's Downloads folder;
- browse the internet or use external applications or accounts;
- communicate with the Executive Assistant, the Grace Gems CEO, or any external
  stakeholder;
- formulate or adopt business strategy;
- approve, execute, publish, spend, price, commit, or make a customer promise;
- change authority, permissions, governance, membranes, or role contracts;
- edit, rename, move, supersede, or delete an existing artifact;
- expand its source map, tools, persistence, term, or authority.

## Persistence boundary

The Steward has no default write authority. If the pilot reaches day 30 or an
authorized early closeout, it may create exactly one proposed findings
artifact at the date-matched path confirmed by the Engineer in this receipt.

All interim findings remain conversational. Every correction is advisory until
the Engineer approves a separate exact change.

## Source-state record

Sealed activation record:

- Repository HEAD:
  `224121c8e4a1b12d7a3304ab6ffa12eff833ae48`;
- Role-contract SHA-256:
  `7C8A657B8861670C94E875E06E2D76D03BEAA65E1F462E11740BF6E2FF371A8B`;
- Provisional approval-receipt SHA-256:
  `5208D2E7F307C667739383C6E3C4E6F7BAF9F50689FEDEEA05C47E66A4F5C2E3`;
- Portfolio source baseline: `469 authorized repository-visible files`;
- Working-tree condition: `dirty - approved source files include uncommitted
  changes and untracked files; every authorized file is sealed individually`;
- Immutable source snapshot:
  `docs/council-steward-source-manifest-2026-07-24.json`;
- Manifest ID: `EC-STEWARD-SOURCE-2026-07-24-01`;
- Manifest aggregate SHA-256: recorded inside the sealed manifest.

Repository HEAD alone is not an adequate snapshot because the approved review
materials are not fully represented by that commit. Activation requires a
manifest of every authorized source path and its SHA-256 hash after this draft
and any approved pre-activation corrections are complete.

## Pilot dates and closeout path

- Activation date: `2026-07-24`;
- Day-15 review date: `2026-08-08`;
- Day-30 review date: `2026-08-23`;
- Pilot expiration: `2026-08-23 at end of day America/Denver, unless revoked
  earlier`;
- Exact closeout artifact path:
  `docs/council-steward-pilot-closeout-2026-08-23.md`.

Confirmed pilot dates:

- Day 15: 2026-08-08;
- Day 30 and expiration: 2026-08-23;
- Closeout path:
  `docs/council-steward-pilot-closeout-2026-08-23.md`.

These dates control this pilot.

## Approved source transitions

The original activation snapshot remains historical evidence. Later approved
source transitions must retain their own manifest ID, path count, aggregate
hash, decision receipt, and effective timestamp.

Current sealed source state before this approved implementation:

- Manifest: `docs/council-steward-source-manifest-2026-07-24-v3.json`;
- Manifest ID: `EC-STEWARD-SOURCE-2026-07-24-03`;
- Files: `471`;
- Aggregate SHA-256:
  `76C9C9D9D223AE44AEBAFEAAC60F010476AE2DAB7CFC57515F615642B33B7A9E`.

Approved implementation transition:

- Decision source: Engineer selection `A. Implement core`, following approval
  of Executive Council target design Option C and the exact read-only redline;
- Approved changes: authority, Council protocol, Executive Assistant protocol,
  Steward independence and status, receipt consolidation, identity, current
  Grace Gems routing, and validation;
- Relocation: prohibited in this transition;
- External communication, private evidence, client action, and Steward
  authority expansion: prohibited;
- Successor manifest:
  `docs/council-steward-source-manifest-2026-07-24-v4.json`;
- Successor manifest ID: `EC-STEWARD-SOURCE-2026-07-24-04`;
- File count and aggregate SHA-256: controlled by the successor manifest after
  validation and sealing;
- Steward notification: required before the successor source set is treated as
  released to the active runtime.

Approved repair transition:

- Decision source: Engineer selection `A. Repair blockers`, following the
  read-only diff review;
- Predecessor: manifest v4, sealed and verified but not released to the Steward
  runtime;
- Repairs: machine-visible dual authority, Steward role-schema enforcement,
  section-level transaction attribution, receipt-pilot consistency, and
  bounded current-document Executive Assistant terminology;
- Narrow source-map expansion:
  `docs/authority-model.md`,
  `docs/executive-council-identity.md`,
  `docs/executive-council-three-receipt-pilot.md`,
  `docs/executive-council-pilot-tracker.md`, and
  `templates/executive-council-transaction-record.md`;
- Relocation: prohibited in this transition;
- External communication, private evidence, client action, and Steward
  authority expansion beyond the named repository sources: prohibited;
- Successor manifest:
  `docs/council-steward-source-manifest-2026-07-24-v5.json`;
- Successor manifest ID: `EC-STEWARD-SOURCE-2026-07-24-05`;
- File count and aggregate SHA-256: controlled by the successor manifest after
  validation and sealing;
- Release state: seal and verify only; do not release to the Steward runtime
  without a separate notification.

## Measured investment gates

The pilot is retained beyond closeout only if the returned evidence supports
the Engineer's decision. The provisional operating targets are:

- at least `3.8` verified benefit-hours per month from faster reconstruction
  and routine rework avoided, net of correction time;
- at least `70%` of material findings accepted or accepted with revision;
- false-positive findings no higher than `20%`;
- combined Engineer and Chief Executive review burden no higher than `2` hours
  per month in the base operating case;
- no more new Steward artifacts than artifacts consolidated or superseded;
- zero privacy, membrane, authority, external-communication, or private-system
  violations.

These are retain-or-revise gates, not claims of measured performance.

## Activation gate

Every item must be complete before the Steward receives source access:

- [x] Logical Steward identity reserved;
- [x] Proposed implementation class recorded;
- [x] Proposed model recorded;
- [x] Provisional Engineer Approval Receipt identified;
- [x] Read, write, communication, privacy, and delegation boundaries recorded;
- [x] Engineer selects `activate` in this receipt;
- [x] Actual model and runtime identity recorded;
- [x] Actual agent or instance ID recorded;
- [x] Exact role-contract version re-hashed and sealed;
- [x] Exact approval-receipt version re-hashed and sealed;
- [x] Authorized source manifest with path and SHA-256 for every file attached;
- [x] Working-tree state and source-manifest relationship recorded;
- [x] Activation, day-15, day-30, and expiration dates recorded;
- [x] Exact date-matched closeout path confirmed;
- [x] Privacy and membrane preflight passed;
- [x] Revocation instruction delivered to the named instance;
- [x] Engineer activation signature completed.

Any unchecked item keeps the pilot inactive.

## Activation decision

Select exactly one:

- [x] activate
- [ ] activate with narrower scope
- [ ] hold pending completed activation gate
- [ ] reject
- [ ] revoke provisional approval

**Engineer conditions or changes:** operate as a measured read-only pilot;
retain, revise, or stop from returned evidence  
**Approved source-manifest reference:**
`docs/council-steward-source-manifest-2026-07-24.json`  
**Privacy and membrane preflight:** passed; repository privacy scan passed and
private/external systems remain excluded  
**Activated by:** Engineer/operator through explicit selection `A. Activate
the measured 30-day Steward pilot`  
**Activation timestamp:** `2026-07-24T14:38:29.4896227-06:00`  
**Actual agent or instance ID:**
`/root/executive_council_steward_pilot_01`  
**Actual model/runtime:** `gpt-5.6-sol` requested through Codex collaboration
runtime; generic runtime self-identification is Codex agent based on GPT-5  
**Revocation path:** Engineer may stop the instance immediately and remove all
source access; historical receipts remain read-only  

## First instructions if activated

The Steward's first action is to:

1. verify its identity, contract hash, source-manifest hash, permission
   boundary, dates, and closeout path against this completed receipt;
2. return `Hold` without reviewing content if any value is missing or differs;
3. if all values match, reconstruct the controlling Executive Council
   portfolio state from the sealed sources, using Grace Gems as the first
   detailed review focus;
4. persist nothing and communicate with no external party;
5. return the day-15 finding to the Engineer or stop immediately on any
   approved stop condition.

## Current authority header

**Proposed by:** Chief Executive  
**Recommended by:** Chief Executive  
**Approved by:** Engineer/operator, 2026-07-24  
**Executed by:** `/root/executive_council_steward_pilot_01`  
**Authority scope:** sealed read-only portfolio state-and-receipt review;
Grace Gems is the first detailed focus  
**Evidence required:** baseline reconstruction, day-15 interim finding, day-30
closeout, measured ROI inputs, and Engineer closeout decision  

**State:** `active - baseline review authorized`

> **The named instance is active only for this bounded pilot. It has no write,
> external, private-system, communication, strategy, or self-expansion
> authority.**
