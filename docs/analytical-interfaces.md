# Analytical Interfaces: Make the Repository's Judgment Recoverable at a Glance

Title rationale: This title states the method's test: labels succeed when a scanning reader can recover the judgment they organize.

## Lead Judgment

Reader-facing titles, headings, object names, summaries, forecasts, questions, roles, and uncertainty labels are part of the analysis. They must expose the governing distinction, mechanism, tension, threshold, or change rather than merely identify a container.

Evidence awareness governs whether a claim is supported. Analytical-interface discipline governs whether that supported judgment remains visible to the next reader. Both contracts apply at publication and decision boundaries.

## Controlling Object

Whether a reader scanning only labels, headings, summaries, and tables can reconstruct the repository's major judgments without opening every document.

## Governed Surfaces

- Titles compress the central claim or tension; document types belong in metadata or subtitles.
- Lead judgments state what changed, why it matters, the mechanism, and what remains uncertain.
- Objects name a bounded contested relationship or threshold whose state can change with evidence.
- Headings expose the reasoning chain. Functional navigation headings such as `Sources`, `Methods`, `Evidence Status`, and `Appendix` remain permitted.
- Forecasts are causal wagers with observable claims, time bounds, strengthening and weakening evidence, resolution criteria, alternatives, and an authorized unresolved state.
- Questions contain a disputed premise, tradeoff, mechanism, or threshold that can produce differentiated answers.
- Roles describe recurring operations that guide retrieval and task selection, not personalities or stereotypes.
- Uncertainty names its evidentiary cause, consequence, and the evidence that would reduce it.

## Drafting Procedure

1. Write the central argument in one sentence.
2. Identify the governing mechanism, asymmetry, reversal, threshold, or unresolved tension.
3. Draft at least three materially different titles and reject any that could label unrelated documents.
4. Select the most accurate distinctive title and record a one-sentence `Title rationale:`.
5. State the lead judgment and controlling object before filling supporting sections.
6. Replace generic analytical headings with claims while retaining useful navigation headings.
7. Name uncertainty causes and build causal forecast or deliberative-question fields when those surfaces apply.
8. Run `anyang-project validate-interfaces`; then obtain accountable human review for analytical quality.

## Working Pattern

```markdown
# [Distinctive title that compresses the central judgment]

Title rationale: [What argument, tension, mechanism, or reversal does the title compress?]

## Lead Judgment

[State what changed, why it matters, and the governing mechanism.]

## Controlling Object

[Name the contested relationship or threshold.]

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
|  |  |  |
```

## Examples That Carry the Judgment

- Replace `Authentication` with `Whether Session Recovery Can Remain Secure without Repeated User Friction`.
- Replace `Customer churn` with `When Failed Activation Becomes Irrecoverable Churn`.
- Replace `Infrastructure` with `Whether Queue Growth Outruns Worker Scaling`.
- Replace `Security expert` with `Tests feature proposals against privilege boundaries and abuse paths`.
- Replace `What do we think about the migration?` with `Does the migration reduce operational risk enough to justify losing local reversibility?`.
- Replace `Low confidence` with `Low confidence—behavior is inferred from six self-selected interviews`.

## Fidelity Boundary

Do not analytically rewrite source titles, quotations, transcripts, archive filenames, canonical identifiers or slugs, database keys, API or CLI names, schema fields, forecast IDs, imported metadata, or legal and regulatory terminology. Functional filenames may remain literal and searchable while their displayed titles become analytical.

The curated manifest governs only named publication, decision, and reusable template surfaces. It does not authorize mass-retitling archives, migration backups, probes, tenant-private material, or legacy documents. Archive analysis templates may govern future analysis outputs while archived source material remains immutable.

## Automation Boundary

Automation may detect exactly-one-H1 failures, placeholders, administrative-only titles, absent or trivial title rationales, prohibited generic analytical headings, missing controlling objects, incomplete causal forecasts, nondiscriminating template questions, and uncertainty without named causes.

Automation must not judge beauty, metaphor, taste, importance, originality, or whether prose is genuinely insightful. Those are human editorial judgments.

## Review Ownership

Authors and operators draft the analytical interfaces, preserve provenance, and clear objective diagnostics. The accountable human reviewer decides whether the labels faithfully express the evidence, approves exceptions, and prevents formulaic compliance. Publication and decision owners must not treat validator success as editorial approval.

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Provisional—reader-outcome baselines do not yet exist | Compliance can be measured before retrieval or recall gains are demonstrated | Timed document-choice tests, delayed recall checks, and recorded editorial overrides |

## Success Measures

Track validator pass rate, placeholder rejection rate, drafting time, retrieval success, ability to predict the argument from the title, delayed recall, forecasts with reviewable mechanisms, uncertainty labels with evidentiary causes, and editorial overrides caused by formulaic compliance. Expand enforcement only when these measures show lower semantic entropy rather than more elaborate prose.
