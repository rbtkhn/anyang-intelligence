# Moonshots Archive

This folder stores internal analysis material for Moonshots transcripts and source notes.

Moonshots uses the same archive discipline as [Innermost Loop](../innermost-loop/README.md), but it now uses a distinct **seam-first ROI extraction** workflow because Moonshots episodes are rhetoric-dense, multi-topic, and verification-sensitive.

```text
moonshots/
  transcripts/
  source-notes/
  analyses/
  source-note-template.md
  analysis-template.md
  roi-ledger.md
```

Use these Moonshots-specific artifacts:

- [source-note-template.md](source-note-template.md)
- [analysis-template.md](analysis-template.md)
- [roi-ledger.md](roi-ledger.md)

## Moonshots ROI Pipeline

Moonshots is optimized for **primitive yield per seam**, not generic episode summarization.

Standard flow:

1. Land transcript.
2. Create a Moonshots source note with dominant seams, rhetoric risk, verification-priority claims, best candidate primitive, and likely best receiving lane.
3. Create a seam-first analysis that extracts 2-5 seams and assigns exactly one ROI disposition to each seam.
4. Update [roi-ledger.md](roi-ledger.md) with one row per seam.
5. Preserve, verify, route, or hold based on the seam disposition.

ROI dispositions:

- `primitive-candidate`
- `needs-verification`
- `lane-test-ready`
- `worldview-only`
- `preserved`

The standard routing packet for `lane-test-ready` seams is:

```text
Source episode:
Seam:
Transferable question or checklist:
Receiving lane:
Membrane classification:
Human authority required:
Evidence still needed:
What stays inside Singularity Science:
```

Current worked exemplar:

- Episode [#268](analyses/2026-07-08-moonshots-268-sonnet-5-fable-5-fusion-philip-johnston.analysis.md) is the first full seam-first exemplar.

## Boundary

Full transcripts are internal analysis material. Do not quote, republish, or customer-route transcript text without rights review and source attribution.

When uncertain, preserve the transcript locally and commit only source notes and original analysis.
