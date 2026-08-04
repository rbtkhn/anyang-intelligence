# Dual-Surface Decision Envelope v1.1

Status: `shadow calibration; gated operation disabled`

Authority owner: System Engineer
Measurement owner: Council Steward

## Safety posture

Version 1.1 derives a sanitized machine envelope and escaped human receipt
from the schema-v8 append-only Council ledger. It does not migrate SQLite.
Generation uses the requested RFC3339 `as_of` as a real event-history cutoff;
live pilot transaction and event recording times are server-owned. A supplied
Council role must equal the active actor's stored role.

The generated contract is `council-decision-envelope/v1.1`. Offline readers
continue to accept legacy v1 packets. The v1.1 export allowlists event payload
fields and carries both a sanitized projection hash and a canonical ledger
projection hash. Internal envelope and pilot-review artifacts may be written
only to an absolute path outside the repository. Markdown renders untrusted
scalar content as escaped, single-line text. JSON input rejects duplicate
keys, non-finite numbers, excessive nesting, oversized values, and packets
larger than 2 MiB.

Critical receipt coverage distinguishes structural presence from known facts.
`Missing` remains visible and prevents a transaction from qualifying as a
complete pilot receipt. Approved work requires a named invoked executor,
returned evidence, and complete reconciliation. Held or rejected work requires
an explicit no-action execution receipt and terminal disposition.

## Protected shadow pilot

The System Engineer starts a pilot only through a currently authorized Class
1 or Class 2 control transaction:

```text
anyang-ops council envelope-pilot-start --tenant anyang-internal \
  --control-transaction-id CONTROL_ID --actor-id ENGINEER_ACTOR_ID
```

The returned activation event ID is the `source_ref` for every new
`decision-envelope-v1-shadow` transaction. Pilot timestamps are recorded by
the service. Direct use of the reserved envelope measurement names is rejected.

Each measured transaction uses two protected sessions, with reviewer roles
assigned deterministically between Council Steward and Executive Assistant:

```text
anyang-ops council envelope-review-open --transaction-id TX_ID \
  --pilot-id PILOT_ID --surface baseline --reviewer-actor-id ACTOR_ID
anyang-ops council envelope-review-submit SESSION_ID --packet answers.yaml
anyang-ops council envelope-pilot-review --tenant anyang-internal \
  --pilot-id PILOT_ID --as-of TIME --format markdown
```

Opening freezes a decision-state hash and semantic receipt digest. Submitting
requires exactly five normalized answers. The service derives elapsed time and
correctness; caller-authored outcome metrics never qualify for gate or ROI
calculations. The report derives its start from the protected activation event.

The report may return `Eligible for gated review` after sufficient observed
evidence, but `shadow_gate.ready` remains false. Creation or execution of a
`decision-envelope-v1-gated` transaction is held in v1.1. A later reviewed
contract and explicit System Engineer decision are required to activate gated
operation. Envelopes and measurement receipts have `authority_effect: none`.

## Read-only interfaces

```text
anyang-ops council envelope TRANSACTION_ID --as-of TIME --format json|markdown
anyang-ops council envelope-verify --packet ENVELOPE.json
anyang-ops council envelope-verify --packet ENVELOPE.json --receipt RECEIPT.md
anyang-ops --db DB council envelope-compare --packet ENVELOPE.json
anyang-ops --db DB council envelope-pilot-review --tenant anyang-internal \
  --pilot-id PILOT_ID --as-of TIME --format json|markdown
```

Generation, verification, comparison, and review do not write operating state.
Hashes demonstrate internal consistency, not truth, authorship, or authority.
Ledger comparison is required to establish parity with canonical state.
