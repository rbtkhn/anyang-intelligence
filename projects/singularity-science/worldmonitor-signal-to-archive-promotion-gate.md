# World Monitor Signal-to-Archive Promotion Gate

This gate is the bridge between the World Monitor receipt layer and the Innermost Loop archive. It makes a recommendation only; a human must perform and approve any source-note promotion.

## Outcomes

- `retain-as-external-receipt`: signal is useful or potentially useful, but remains outside the archive.
- `promote-to-singularity-source-note`: evidence is sufficient for human-reviewed source-note intake; no write is automatic.
- `hold-for-more-evidence`: source body, rights, freshness, confidence, or corroboration is insufficient.
- `reject-as-noise`: signal is not materially relevant to the current Singularity Science question.

## Gate questions

- Is the signal materially relevant to a current Singularity Science question?
- Is the source body available, rather than only a dashboard summary?
- Are rights and attribution status sufficiently known?
- Is the signal fresh enough for the proposed use?
- Is the signal a duplicate of an existing receipt?
- Is there independent corroboration?
- Does promotion preserve observation/inference separation?
- What human approval is required before source-note creation?

## Boundary

The gate does not create a source note, transcript, claim, approval, customer routing, public statement, permission, or doctrine. Its output is a recommendation for the existing Singularity Intake workflow.
