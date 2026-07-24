# Executive Council Steward Pilot — Engineer Approval Receipt

**Receipt status:** `provisionally approved - activation conditions pending; pilot not activated`  
**Receipt ID:** EC-STEWARD-APPROVAL-2026-07-24-01  
**Related contract:** [Council Steward Role Contract](../../docs/council-steward-role-contract.md)  
**Pilot scope:** Executive Council portfolio, with Grace Gems as the first
review focus  
**Proposed term:** 30 calendar days from activation

## Engineer Approval Receipt

**Brief ID:** EC-STEWARD-PILOT-BRIEF-2026-07-24-01  
**Decision under review:** Whether to activate a separate Council Steward AI
instance for a bounded, read-mostly 30-day portfolio state-and-receipt
integrity pilot, beginning with Grace Gems.

The Council Steward is an organization-wide Executive Council role. Locating
this first pilot receipt in the Grace Gems project records the initial review
focus; it does not make the role part of or subordinate to Grace Gems.

### Provisionally approved scope

The Steward may:

1. inspect the approved source map below;
2. reconstruct the current Executive Council portfolio state, using Grace Gems
   as the first detailed review focus;
3. identify contradictory statuses, missing receipts, stale commitments,
   broken lineage, duplicate decision artifacts, and unsupported completion
   claims;
4. prepare State Support, Reconciliation Required, Insufficient Evidence,
   Contradiction, Supersession, Aging Obligation, or Completion Gate findings;
5. return a day-15 read-only interim finding to the Engineer;
6. prepare one day-30 proposed closeout artifact at the exact path named below;
7. recommend exact corrections without applying them.

### Provisionally approved source map

Read-only:

- `authority-envelope.yaml`;
- `docs/executive-council-role-contract.md`;
- `docs/council-steward-role-contract.md`;
- `docs/governance.md`;
- `docs/membranes.md`;
- `docs/data-handling-policy.md`;
- `docs/executive-interface-protocol.md`;
- `templates/chief-executive-brief.md`;
- `templates/approval-receipt.md`;
- `templates/executive-assistant-action-receipt.md`;
- `templates/executive-council-pilot-receipt.md`;
- repository-visible artifacts under `projects/`;
- Git status, diff, log, and file lineage for the current repository, read-only.

Portfolio access does not authorize cross-project merging of private context.
The Steward must preserve provenance, apply membranes, and keep its detailed
first review centered on Grace Gems unless the Engineer names another review
question.

### Proposed Steward implementation

- Steward role: independent AI review instance;
- Implementation class: separate Codex Council Steward AI review instance,
  distinct from the Chief Executive;
- Model, runtime, and agent ID: `Missing - must be recorded in an Activation
  Receipt before access`;
- Role prompt: exact approved version of
  `docs/council-steward-role-contract.md`;
- Chief Executive context copied into Steward context: no, except exact source
  artifacts in the approved source map;
- External network access: no;
- External application or account access: no;
- Private client-system access: no;
- Communication with the Executive Assistant, the CEO, or other stakeholders:
  no;
- Ability to spawn or delegate to other agents: no unless separately approved;
- Repository write posture: prohibited except for the one proposed closeout
  artifact described below.

### One permitted persistent artifact

If this receipt is approved and the pilot reaches closeout, the Steward may
create exactly one new proposed findings file:

`docs/council-steward-pilot-closeout-2026-08-23.md`

Conditions:

- creation occurs only at day 30 or authorized early closeout;
- it contains sanitized findings and opaque references only;
- it does not edit, supersede, rename, delete, or move any existing artifact;
- every proposed correction remains advisory;
- the Engineer must separately approve any correction to controlling state;
- if activation occurs after 2026-07-24, the Engineer must replace the filename
  date before approval or authorize the exact revised path.

Interim findings remain conversational and are not persisted by the Steward.

### Limits and exclusions

The Steward may not:

- access customer, order, supplier, employee, financial, credential, analytics,
  communication, or other tenant-private systems;
- open the operator's Downloads folder or private attachments;
- browse the public internet;
- contact or direct the Executive Assistant, the Grace Gems CEO, Eric,
  Jonathan, customers, suppliers, or other stakeholders;
- prepare business strategy or substitute its judgment for the Chief
  Executive;
- approve, execute, publish, spend, price, commit, or communicate externally;
- change roles, authority, permissions, membranes, or governance;
- modify current project files during the audit;
- mark a proposal approved or an action complete;
- treat the role contract or this draft receipt as activation;
- expand its own source map, tools, persistence, or term.

### Required evidence

- named Steward runtime or model identity;
- activation date and calculated day-15 and day-30 dates;
- immutable source-map snapshot or commit reference;
- baseline artifact count and current-state reconstruction time;
- list of claimed controlling artifacts;
- every finding linked to exact repository-visible evidence;
- privacy and membrane check;
- day-15 interim finding;
- day-30 closeout finding;
- time spent by Steward, Chief Executive, and Engineer;
- count of contradictions, missing receipts, stale obligations, overlapping
  artifacts, and false-positive findings;
- count of artifacts proposed for consolidation versus new Steward artifacts;
- Engineer closeout decision.

### Success conditions

The pilot succeeds only if:

- the Steward identifies the controlling state more quickly than the current
  manual reconstruction baseline;
- material contradictions or missing receipts are identified accurately;
- no private or external evidence is accessed;
- no external communication or operational action occurs;
- no existing artifact is modified;
- findings reduce rather than multiply controlling artifacts;
- correction burden is lower than the rework or ambiguity prevented;
- the Engineer can accept, revise, or reject each finding from cited evidence;
- the Chief Executive and Steward remain distinguishable in role and output.

### Stop conditions

Stop immediately and return `Hold` or `Escalated` if:

- the Steward requires a source outside the approved map;
- private or restricted information is encountered;
- the Steward attempts strategy, external communication, execution, or
  self-expansion;
- a finding depends on reconstructing missing authority;
- the Steward modifies or attempts to modify an existing artifact;
- the role cannot remain independent from the Chief Executive's framing;
- false positives or receipt burden exceed demonstrated value;
- the Engineer revokes or narrows the pilot.

### Review cadence

- Activation review: before any Steward access;
- Day 15: read-only interim review with Engineer;
- Day 30: closeout and retain/revise/hold/reject decision;
- Early review: any stop condition, scope conflict, membrane issue, or material
  disagreement.

### Decision

Select exactly one:

- [ ] approved as-is
- [ ] approved with changes
- [x] provisional
- [ ] held
- [ ] rejected
- [ ] escalated

**Required changes or conditions:** Before activation, record a separate
Council Steward instance ID, model and runtime identity, immutable source-map
snapshot or commit, activation date, day-15 and day-30 dates, and exact
date-matched closeout path. No access or execution occurs until every condition
is confirmed.  
**Named Steward implementation:** `executive_council_steward_pilot_01`;
separate Codex Council Steward AI review instance; exact agent ID pending
Activation Receipt  
**Activation date:** pending  
**Day-15 review date:** pending activation date  
**Day-30 review date:** pending activation date  
**Exact closeout path confirmed:** no; proposed path must be date-matched at
activation  

### What remains unapproved

- a permanent Steward runtime appointment;
- any Steward access outside repository-visible `projects/` and the named
  canonical source map;
- private evidence access;
- external tools, accounts, applications, communication, or action;
- edits to existing artifacts;
- adoption of any Steward finding;
- detailed review of another project without an Engineer-named review
  question;
- operation beyond the exact pilot term.

### Authority

**Approval authority:** Engineer  
**Approval date:** 2026-07-24  
**Expiration:** 30 calendar days after activation, or earlier revocation  

**Proposed by:** Chief Executive  
**Recommended by:** Chief Executive  
**Approved by:** Engineer/operator through explicit in-session selection of
provisional approval  
**Executed by:** proposed logical instance
`executive_council_steward_pilot_01`; runtime not created  
**Authority scope:** provisional pilot scope only; no source access or execution
until an Activation Receipt completes every condition  
**Evidence required:** all evidence listed above

**State:** `provisional - activation held`

> **The pilot scope is provisionally approved. No Council Steward instance is
> appointed, no source access is active, and no pilot execution begins until
> the Activation Receipt is complete.**
