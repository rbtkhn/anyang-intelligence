# Customer Data Exposure Audit — 2026-07-09

## Scope

Reviewed the tracked working tree, file names, Git history indicators, configured remote, repository ignore rules, and current project-data doctrine. This audit records exposure shape without reproducing sensitive content.

## Findings

1. Two identifiable learner records were tracked in the Learning Core lane. They contained a child's first name, age, schooling context, and learning observations.
2. The records were moved to `C:\dev\anyang-intelligence\tenant-private\learning-core`, outside the `operating-substrate` Git repository. Their tracked versions are deleted.
3. The records remain present in prior Git commits. No history rewrite has been performed.
4. An `origin` GitHub remote is configured. This local audit does not establish repository visibility, clone count, cache state, or who may have accessed prior commits.
5. The previous repository controls described membranes but did not technically prevent identifiable tenant data from being committed.

## Containment

- Current working copies are quarantined outside Git.
- Database and generated-review patterns are ignored.
- The privacy scanner blocks known identifying content, common contact/credential patterns, private tenant paths, and project-specific intake filenames.
- The data-handling policy now makes tenant storage, consent, retention, deletion, and incident response explicit.

## Required Follow-Up

1. Confirm the external tenant directory has operator-approved access controls and backup behavior.
2. Verify remote repository visibility and access logs through the repository owner.
3. Decide whether the affected parent/guardian or other authority requires notification.
4. After steps 1–3, choose one history action: retain with documented risk, purge affected paths with coordinated history rewriting, or migrate to a new clean repository.
5. If rewriting, enumerate affected refs and collaborators first, create a protected backup, use a dedicated history-rewrite tool, rotate the remote, and require fresh clones.

## Decision Boundary

History rewriting is intentionally not authorized by this audit. It changes shared commit identities and requires explicit operator approval and collaborator coordination.
