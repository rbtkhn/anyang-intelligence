# Learn From Choices Active v1

Status: `active-thin`

Policy: `repository-governance-preflight-v1`

Scope: `anyang-internal / anyang-intelligence / repository`

Authority effect: `none`

## Controlling Judgment

Learn From Choices may improve recommendation ordering from explicitly
retained, outcome-supported episodes without restoring automatic choice
logging. Ordinary navigation remains ephemeral. Only a same-task packet that
the operator reviews and explicitly retains may enter the active cohort.

The first policy asks one narrow question:

> Did a bounded preflight before a consequential governed operating-surface
> mutation find material information, prevent rework, change the decision, or
> confirm readiness at acceptable cost?

It does not establish that inspection is generally better than execution.

## Policy Boundary

The policy applies only when all of these fields match:

```yaml
tenant: anyang-internal
workspace_id: anyang-intelligence
lane: repository
choice_kind: next-action
consequence_level: consequential | authority-sensitive
decision_seam: pre-mutation-evidence-depth
work_class: governed-operating-surface
risk_class: consequential
pattern_key: gather-evidence
action_boundary: read-only
```

Governed operating surfaces include authority and governance contracts,
canonical Skills, runtime and validation controls, state machines, ledgers,
privacy or membrane controls, and repository-wide operating doctrine. Ordinary
prose edits, project content, customer work, private evidence bodies, and
external actions are excluded.

Missing or mismatched scope fails closed and produces no active guidance.

## Interaction And Retention

An ordinary letter selection creates no choice-ledger call or receipt.
Bravo, Friction, a completion receipt, or an explicit operator report may
identify a candidate outcome, but candidate identification writes nothing.

Retention requires:

```text
same-task candidate
  -> exact dry-run packet and SHA-256 digest
  -> operator selects Execute retain this reviewed episode
  -> digest match
  -> atomic prompt + selection + outcome write
  -> event-chain verification
```

If the original menu is no longer visible, route the reusable lesson through
the Recursive Learning Ledger and exclude it from choice comparability.

The command is:

```powershell
.\tools\run.ps1 ops --db C:\private\anyang-ops.db choice retain-outcome `
  --tenant anyang-internal --packet retained-outcome.yaml --dry-run
```

After exact approval, repeat without `--dry-run` and pass the displayed digest
through `--approved-packet-hash`. A changed digest requires a new review.

## Outcome Eligibility

Every outcome requires an evidence reference and records preflight minutes,
useful effect, harm effect, and downstream validation. Unsupported dimensions
remain `Missing`.

A favorable episode is `successful`, has a material effect, has no harm, takes
no more than 15 minutes, and has adequate downstream validation. A
`readiness-confirmed` result requires downstream validation to pass.

An unfavorable episode is `unsuccessful` and records a harm, or exceeds the
burden limit without a material effect. Mixed, no-action, not-observable, and
incompletely measured outcomes remain neutral.

## Cohort And Recommendation Effect

The evidence window is 90 days. At least three eligible resolved episodes and
two consistent favorable or unfavorable outcomes with no material
contradiction are required. A contrary outcome neutralizes the prior.

Favored or demoted guidance is a rebuttable prior. Current task evidence and
controlling doctrine remain primary. Guidance may reorder a credible option
and explain why; it may not invent an option, hide a credible overlooked path,
grant authority, or cross a lane membrane.

If multiple active policies ever match the same decision seam, return
`guidance_conflict: true`, apply no recommendation effect, and use current task
evidence.

## Lifecycle And Stop Conditions

```text
proposed -> approved -> active-thin -> active-pattern -> review-due
  -> active | revised | held | retired
```

Review after five eligible episodes or 30 days. Hold immediately for an
authority, privacy, or membrane incident; false provenance; a partial write;
selection-frequency learning; cross-lane use; repeated false holds; or
persistent retention burden. Held and retired policies preserve historical
receipts.

## Success Standard

Success is not more choice records. It is one transparent, evidence-supported
recommendation improvement, or an honest demotion or neutral result, with
complete evidence coverage, acceptable burden, and zero boundary incidents.
