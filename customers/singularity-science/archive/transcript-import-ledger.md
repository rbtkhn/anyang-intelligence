# Transcript Import Ledger

This ledger tracks transcript-level import state across Singularity Science source lanes.

Statuses:

- `imported`: transcript landed in the archive and still needs source-note follow-up
- `blocked-rights`: rights status requires review before commit
- `duplicate`: destination path already exists or collides inside the manifest
- `missing-source`: manifest row points to a source file that was not found
- `needs-source-note`: imported transcript still needs a source note
- `skipped-do-not-commit`: rights status explicitly prevents commit
- `invalid-manifest`: manifest metadata is incomplete or malformed

Manifest: `customers/singularity-science/archive/transcript-intake-manifest.json`

| Lane | Title | Destination | Rights status | Import status | Follow-up | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| innermost-loop | Example Innermost Loop Episode | `innermost-loop/transcripts/2026-07-08-captured-example-innermost-loop-episode.md` | `uncertain-review-needed` | `blocked-rights` | `-` | Rights review required before commit. |
| moonshots | Example Moonshots Episode | `moonshots/transcripts/2026-07-08-captured-example-moonshots-episode.md` | `uncertain-review-needed` | `blocked-rights` | `-` | Rights review required before commit. |
