# Learn From Choices Continuity Contract v0.2

Status: testable primitive candidate

This contract adds explicit option strategy classification, action-boundary
visibility, comparability cohorts, and append-only classification correction.
It does not change the private ledger schema: SQLite remains schema v8. Choice
projection and context documents use schema v2.

## Option classification

Classification is optional for backward compatibility. If any classification
field is present, the classification must be complete and valid:

```yaml
classification_version: LFC-CONTINUITY-v0.2
pattern_key: execute-bounded
action_boundary: external-action
comparability_key: repository-authorized-push-v1
```

Allowed pattern keys are:

- `gather-evidence`
- `design-next-move`
- `execute-bounded`
- `explore-adjacent`
- `seek-authority`
- `pause-preserve`

Allowed action boundaries are:

- `read-only`
- `workspace-mutation`
- `external-action`
- `authority-decision`
- `stop`

Patterns are diagnostic descriptions, not authority. Action boundaries expose
the next permission seam but retain `authority_effect: none`. Selecting an
exploratory option enters its branch without mutation. Selecting an explicitly
action-labeled option such as `Execute`, `Commit`, `Push`, or `Send` authorizes
only that named bounded action, subject to the existing authority envelope.

Legacy options remain byte-semantically unchanged in stored `options_json`.
Their projections add `unclassified` and `Missing`; there is no historical
classification backfill.

## Comparability policy registry

Only a valid explicit comparability policy can form a learning cohort.
Repeated option keys, displayed letters, roles, patterns, and selection frequency
cannot form cohorts or change recommendations.

The initial registry entry is:

| Policy | Status | Tenant | Workspace | Lane | Kind | Pattern | Boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `repository-authorized-push-v1` | `diagnostic-only` | `anyang-internal` | `anyang-intelligence` | `repository` | `next-action` | `execute-bounded` | `external-action` |

Unknown, disabled, or scope-mismatched policies are invalid. A
`diagnostic-only` policy may report cohort evidence but cannot favor, demote,
or reorder a recommendation. No active production comparability policy ships
in v0.2.

An active future policy may influence guidance only after at least three
eligible resolved outcomes, two consistent favorable or unfavorable results,
and no material contradiction. `mixed`, `no_action`, and `not_observable` are
neutral. Calibration freezes remain controlling.

Learning eligibility excludes unresolved, superseded, unverified,
unclassified, policy-invalid, and missing-evidence choices. Authority,
privacy, safety, and membrane incidents remain immediate guardrails.

## Append-only correction

The immutable original classification is retained. A `corrected` event may
contain one classification correction:

```yaml
event_key: correct-recorded-boundary
event_type: corrected
recorded_by: Council Steward
action_summary: Correct the recorded action boundary
payload:
  reason: Correct the recorded boundary
  classification_correction:
    option_key: recommended
    field: action_boundary
    prior_value: workspace-mutation
    replacement_value: external-action
    policy_ref: LFC-CONTINUITY-v0.2
```

The target field is `pattern_key`, `action_boundary`, or `comparability_key`.
`prior_value` must equal the effective value at that event sequence. When
adding or replacing comparability, `policy_ref` names the allowed replacement
policy. When removing comparability with `replacement_value: Missing`,
`policy_ref` names the registered prior policy.
Outcome replacement and classification correction cannot share one event.
Reason-only legacy corrections remain valid.

Classification-only corrections do not change operational state. Corrections
are append-only, hash-chained lineage; original packets are never rewritten.

## Projection and context

Choice projection schema v2 exposes:

- `original_classification`
- `effective_classification`
- `classification_corrections`
- `classification_verified`
- `learning_eligibility`
- `comparability_policy`

Choice context schema v2 preserves exact option-key `outcome_patterns` as
descriptive-only data and adds:

- `diversity_diagnostics`
- `comparability_cohorts`
- favored and demoted comparability keys
- diagnostic favored and demoted comparability keys
- deprecated, always-empty favored and demoted option-key arrays

Dry-run selection validates packet structure, classification, privacy, and
policy scope while deferring actor and database idempotency checks. Dry-run
outcome validates correction shape while deferring choice-specific actor,
prior-value, and idempotency checks.

No classification is promoted into repository learning automatically.
