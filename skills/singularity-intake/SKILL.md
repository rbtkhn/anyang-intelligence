---
name: singularity-intake
description: Repo-specific Singularity Science intake for already-available transcripts, newsletters, essays, reports, interviews, or pasted source bodies. Use when the source belongs to an existing archive lane and the task requires transcript landing, a lane source note, lane analysis, and the canonical ledger update.
---

# Singularity Intake

Use this skill for `projects/singularity-science/` when the operator has supplied source material and wants the complete governed archive intake. Preserve the core law:

`project lane -> archive lane -> lane templates -> ledger`

## Scope

Known lanes are `innermost-loop`, `moonshots`, `nate-b-jones`, and `external-interviews`. Do not use this skill to fetch sources, create a lane, publish outward-facing doctrine, customer-route transcript bulk, or establish rights certainty.

If the channel is unknown or ambiguous, stop and ask the operator to map it to an existing lane, use `external-interviews`, or establish a new lane separately. Never auto-scaffold a lane.

## Required workflow

1. Confirm that the source body is materially present.
2. Select a known archive lane and explain the choice.
3. Read that lane's `README.md`, `source-note-template.md`, `analysis-template.md`, and canonical ledger.
4. Create exactly one transcript in `projects/singularity-science/archive/<lane>/transcripts/`, following the lane's existing `YYYY-MM-DD-title-slug.md` convention and metadata pattern. Include rights status, attribution, URL or an explicit unavailable note, and no invented publication date. Redact direct contact strings unless explicitly approved.
5. Create exactly one template-conforming source note in `source-notes/`.
6. Create exactly one template-conforming analysis in `analyses/`.
7. Update only the lane's canonical ledger: `research-ledger.md` for Innermost Loop, otherwise `roi-ledger.md`.
8. Stop when those four internal archive outputs are complete.

Source notes and analyses must be original synthesis, not transcript-paraphrase dumps. Keep uncertainty, attribution, rights, and membrane boundaries explicit. Do not turn source claims into Anyang Intelligence claims, create customer obligations, or move transcript bulk outside the archive.

## Lane rules

Innermost Loop: add one research-ledger row per source or source cluster; emphasize product implication, governance pressure, primitive candidate, and authority-leak risk.

Moonshots, Nate B. Jones, and External Interviews: use seam-first ROI extraction with 2-5 seams and exactly one disposition per seam. Allowed dispositions are `primitive-candidate`, `needs-verification`, `lane-test-ready`, `worldview-only`, and `preserved`. Nate B. Jones is practitioner-demo and orchestration-heavy; preserve rhetoric as rhetoric. External Interviews require especially careful provenance and contested-claim handling.

Every `lane-test-ready` seam must include:

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

## Stop boundary

Do not automatically preserve primitive candidates, create implications memos, run verification, or perform recurrence review. These can be recommended as later moves. At completion, report the transcript, source-note, analysis, and ledger paths, and state what remained inside Singularity Science.
