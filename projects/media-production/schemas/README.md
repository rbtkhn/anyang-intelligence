# Artistic Director AI Factory Schemas

The [Artistic Director AI Factory schema](artistic-director-ai-factory.schema.json) validates dashboard and memory records for the prepare-only factory contract.

The schema is validation-only. A valid record does not grant publication, client, spend, rights, contractor, or external communication authority.

Record types supported:

- `dashboard`
- `thesis`
- `batch`
- `canon_entry`
- `decision`
- `reference`
- `experiment`
- `review`
- `compounding`

Cross-record rules—such as verifying that a referenced ID exists, checking whether a decision is current, or preventing a dashboard projection from becoming a source of truth—remain application-level validation responsibilities.

Repository doctrine and gates define the permitted operating boundary. The
private Executive Council ledger remains canonical for live authority,
execution, evidence, and outcome state. Schema-valid records are supporting
creative-memory objects only; validity has `authority_effect: none`.

Focused Draft 2020-12 behavior is tested in
`tests/test_artistic_director_ai_factory_schema.py`.
