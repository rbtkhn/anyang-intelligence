# Repository Context-Integrity Audit — 2026-07-23

## Executive judgment

This read-only baseline identifies discoverability, linkage, freshness, broken-reference, and membrane risks. Findings are evidence for review, not proof of operational failure or ROI.

Findings: 388 (error: 11, info: 310, warning: 67)

## Priority queue

- **ERROR broken-link** `projects/singularity-science/archive/moonshots/analyses/2026-06-09-moonshots-emerging-anthropic-global-pause-recursive-self-improvement-ai-personhood.analysis.md`: linked target does not exist. Action: Repair the link or mark the reference intentional.
- **ERROR broken-link** `projects/singularity-science/archive/moonshots/analyses/2026-06-09-moonshots-emerging-anthropic-global-pause-recursive-self-improvement-ai-personhood.analysis.md`: linked target does not exist. Action: Repair the link or mark the reference intentional.
- **ERROR broken-link** `projects/singularity-science/archive/moonshots/analyses/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-openai-ipo-delay.analysis.md`: linked target does not exist. Action: Repair the link or mark the reference intentional.
- **ERROR broken-link** `projects/singularity-science/archive/moonshots/analyses/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-openai-ipo-delay.analysis.md`: linked target does not exist. Action: Repair the link or mark the reference intentional.
- **ERROR broken-link** `projects/singularity-science/archive/moonshots/analyses/2026-07-08-moonshots-268-sonnet-5-fable-5-fusion-philip-johnston.analysis.md`: linked target does not exist. Action: Repair the link or mark the reference intentional.

## Findings

| ID | Severity | Category | Path | Line | Evidence | Human decision |
| --- | --- | --- | --- | ---: | --- | --- |
| CIA-0001 | info | discoverability | `.agents/skills/business-intake/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0002 | info | discoverability | `.agents/skills/business-intake/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0003 | info | discoverability | `.agents/skills/intent-recovery/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0004 | warning | freshness-metadata | `.agents/skills/intent-recovery/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0005 | info | discoverability | `.agents/skills/intent-recovery/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0006 | info | discoverability | `.agents/skills/learner-intake/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0007 | warning | freshness-metadata | `.agents/skills/learner-intake/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0008 | info | discoverability | `.agents/skills/learner-intake/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0009 | info | discoverability | `.github/workflows/validate.yml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0010 | info | discoverability | `AGENTS.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0011 | warning | authority-conflict | `C:/dev/anyang-intelligence/operating-substrate` |  | 8 document(s) describe granting authority while 5 describe withholding it | yes |
| CIA-0012 | info | discoverability | `authority-envelope.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0013 | info | discoverability | `docs/authority-model.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0014 | warning | freshness-metadata | `docs/authority-model.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0015 | info | discoverability | `docs/cadence-loop-example.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0016 | info | discoverability | `docs/data-handling-policy.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0017 | info | discoverability | `docs/epistemic-entropy-baseline.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0018 | info | discoverability | `docs/executive-assistant-ai-onboarding-handoff.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0019 | info | discoverability | `docs/executive-council-identity.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0020 | warning | freshness-metadata | `docs/executive-council-identity.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0021 | info | discoverability | `docs/executive-council-migration-report.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0022 | warning | freshness-metadata | `docs/executive-council-migration-report.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0023 | info | discoverability | `docs/executive-council-pilot-tracker.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0024 | warning | freshness-metadata | `docs/executive-council-pilot-tracker.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0025 | info | discoverability | `docs/executive-council-role-contract.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0026 | info | discoverability | `docs/executive-council-three-receipt-pilot.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0027 | warning | freshness-metadata | `docs/executive-council-three-receipt-pilot.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0028 | info | discoverability | `docs/executive-interface-protocol.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0029 | info | discoverability | `docs/exposure-audit-2026-07-09.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0030 | info | discoverability | `docs/governance.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0031 | info | discoverability | `docs/implementation-model.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0032 | info | discoverability | `docs/nested-intelligence-loops-strategy.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0033 | info | discoverability | `docs/product.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0034 | info | discoverability | `docs/recursive-self-enhancement-checklist.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0035 | warning | freshness-metadata | `docs/recursive-self-enhancement-checklist.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0036 | info | discoverability | `docs/recursive-self-enhancement.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0037 | info | discoverability | `docs/thesis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0038 | info | discoverability | `docs/trusted-intelligence-integration.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0039 | info | discoverability | `docs/worldmonitor-signal-adapter.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0040 | warning | freshness-metadata | `docs/worldmonitor-signal-adapter.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0041 | info | discoverability | `os/coordination-loop.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0042 | info | discoverability | `os/decision-system.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0043 | info | discoverability | `os/executive-memory.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0044 | info | discoverability | `os/learning-loop.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0045 | info | discoverability | `playbooks/decision-memo.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0046 | info | discoverability | `playbooks/installation-sprint.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0047 | info | discoverability | `playbooks/weekly-executive-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0048 | info | discoverability | `projects/book-club/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0049 | warning | freshness-metadata | `projects/book-club/executive-os-install.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0050 | info | discoverability | `projects/commercial-hypotheses.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0051 | info | discoverability | `projects/comparison-matrix.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0052 | info | discoverability | `projects/grace-gems/30-day-plan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0053 | info | discoverability | `projects/grace-gems/90-day-proof-baseline.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0054 | info | discoverability | `projects/grace-gems/approval-quality-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0055 | info | discoverability | `projects/grace-gems/authority-card.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0056 | warning | freshness-metadata | `projects/grace-gems/authority-card.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0057 | info | discoverability | `projects/grace-gems/business-intake-survey.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0058 | info | discoverability | `projects/grace-gems/ceo-follow-up-message-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0059 | info | discoverability | `projects/grace-gems/ceo-meeting-capture-2026-07-23.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0060 | info | discoverability | `projects/grace-gems/ceo-meeting-preparation-bundle-2026-07-23.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0061 | info | discoverability | `projects/grace-gems/customer-support-findings-2026-07-17.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0062 | info | discoverability | `projects/grace-gems/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0063 | info | discoverability | `projects/grace-gems/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0064 | info | discoverability | `projects/grace-gems/first-review-brief-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0065 | info | discoverability | `projects/grace-gems/four-cycle-proof-tracker.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0066 | info | discoverability | `projects/grace-gems/membrane-notes.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0067 | info | discoverability | `projects/grace-gems/operating-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0068 | info | discoverability | `projects/grace-gems/public-shop-signal-brief.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0069 | info | discoverability | `projects/grace-gems/public-signal-preflight-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0070 | info | discoverability | `projects/grace-gems/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0071 | info | discoverability | `projects/grace-gems/turn-usefulness-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0072 | info | discoverability | `projects/learning-core/30-day-plan-inputs.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0073 | info | discoverability | `projects/learning-core/30-day-plan-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0074 | info | discoverability | `projects/learning-core/30-day-plan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0075 | info | discoverability | `projects/learning-core/abigail-phase-2-onboarding-survey.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0076 | warning | freshness-metadata | `projects/learning-core/ai-interface-training/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0077 | info | discoverability | `projects/learning-core/ai-interface-training/approved-with-changes-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0078 | info | discoverability | `projects/learning-core/ai-interface-training/embodied-ai-hold-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0079 | warning | freshness-metadata | `projects/learning-core/ai-interface-training/embodied-ai-hold-exemplar.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0080 | info | discoverability | `projects/learning-core/ai-interface-training/hold-after-review-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0081 | info | discoverability | `projects/learning-core/ai-interface-training/ready-plan-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0082 | info | discoverability | `projects/learning-core/approval-quality-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0083 | info | discoverability | `projects/learning-core/catalog-doctrine.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0084 | warning | freshness-metadata | `projects/learning-core/catalog-doctrine.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0085 | info | discoverability | `projects/learning-core/catalog/catalog-recommendation-mapping.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0086 | warning | freshness-metadata | `projects/learning-core/catalog/catalog-recommendation-mapping.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0087 | info | discoverability | `projects/learning-core/catalog/catalog-schema.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0088 | info | discoverability | `projects/learning-core/catalog/khan-kids-curated-catalog.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0089 | info | discoverability | `projects/learning-core/catalog/khan-kids-in-app-capture-spec.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0090 | warning | freshness-metadata | `projects/learning-core/catalog/khan-kids-in-app-capture-spec.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0091 | info | discoverability | `projects/learning-core/continuity-invitation-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0092 | info | discoverability | `projects/learning-core/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0093 | info | discoverability | `projects/learning-core/embodied-ai-hold-policy.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0094 | info | discoverability | `projects/learning-core/embodied-ai-parent-review-worksheet.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0095 | warning | freshness-metadata | `projects/learning-core/embodied-ai-parent-review-worksheet.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0096 | info | discoverability | `projects/learning-core/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0097 | info | discoverability | `projects/learning-core/hold-response-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0098 | info | discoverability | `projects/learning-core/initial-learner-profile-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0099 | warning | freshness-metadata | `projects/learning-core/initial-learner-profile-template.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0100 | info | discoverability | `projects/learning-core/khan-academy-signal-pipeline.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0101 | warning | freshness-metadata | `projects/learning-core/khan-academy-signal-pipeline.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0102 | info | discoverability | `projects/learning-core/khan-adapter-layer.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0103 | warning | freshness-metadata | `projects/learning-core/khan-adapter-layer.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0104 | info | discoverability | `projects/learning-core/khan-transition-point.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0105 | warning | freshness-metadata | `projects/learning-core/khan-transition-point.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0106 | info | discoverability | `projects/learning-core/khan-transition-readiness-target.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0107 | warning | freshness-metadata | `projects/learning-core/khan-transition-readiness-target.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0108 | info | discoverability | `projects/learning-core/learning-core-ob1-integration.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0109 | warning | freshness-metadata | `projects/learning-core/learning-core-ob1-integration.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0110 | info | discoverability | `projects/learning-core/loop-examples/learning-experience.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0111 | info | discoverability | `projects/learning-core/loop-examples/parent-intake-readiness.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0112 | info | discoverability | `projects/learning-core/membrane-notes.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0113 | warning | freshness-metadata | `projects/learning-core/membrane-notes.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0114 | info | discoverability | `projects/learning-core/mock-intake-simulations.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0115 | info | discoverability | `projects/learning-core/mock-ready-plan-evidence-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0116 | warning | freshness-metadata | `projects/learning-core/mock-ready-plan-evidence-map.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0117 | info | discoverability | `projects/learning-core/monthly-portfolio-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0118 | warning | freshness-metadata | `projects/learning-core/monthly-portfolio-review.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0119 | info | discoverability | `projects/learning-core/naming-architecture.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0120 | warning | freshness-metadata | `projects/learning-core/naming-architecture.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0121 | info | discoverability | `projects/learning-core/nested-loop-authority-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0122 | info | discoverability | `projects/learning-core/onboarding-readiness-checklist.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0123 | info | discoverability | `projects/learning-core/one-time-retainer-scope.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0124 | info | discoverability | `projects/learning-core/operating-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0125 | info | discoverability | `projects/learning-core/parent-approval-checklist.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0126 | info | discoverability | `projects/learning-core/parent-approval-record.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0127 | info | discoverability | `projects/learning-core/parent-guide-signals.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0128 | warning | freshness-metadata | `projects/learning-core/parent-guide-signals.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0129 | info | discoverability | `projects/learning-core/parent-intake-message.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0130 | info | discoverability | `projects/learning-core/parent-intake-summary-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0131 | info | discoverability | `projects/learning-core/parent-intake-to-draft-runbook.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0132 | info | discoverability | `projects/learning-core/parent-journey-pressure-test.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0133 | warning | freshness-metadata | `projects/learning-core/parent-journey-pressure-test.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0134 | info | discoverability | `projects/learning-core/parent-onboarding-survey.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0135 | warning | freshness-metadata | `projects/learning-core/parent-onboarding-survey.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0136 | info | discoverability | `projects/learning-core/phase-2-survey-generation.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0137 | info | discoverability | `projects/learning-core/plan-draft-evidence-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0138 | info | discoverability | `projects/learning-core/plan-drafting-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0139 | info | discoverability | `projects/learning-core/reading-basket.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0140 | info | discoverability | `projects/learning-core/recursive-self-enhancement.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0141 | info | discoverability | `projects/learning-core/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0142 | info | discoverability | `projects/learning-core/startup-bundle.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0143 | info | discoverability | `projects/learning-core/student-portfolio.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0144 | info | discoverability | `projects/learning-core/subscription-boundary.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0145 | info | discoverability | `projects/learning-core/subscription-experience.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0146 | info | discoverability | `projects/learning-core/success-friction-bridge-intake-report.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0147 | info | discoverability | `projects/learning-core/turn-usefulness-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0148 | info | discoverability | `projects/media-production/30-day-plan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0149 | warning | freshness-metadata | `projects/media-production/30-day-plan.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0150 | warning | freshness-metadata | `projects/media-production/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0151 | info | discoverability | `projects/media-production/abundance-principle.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0152 | info | discoverability | `projects/media-production/creative-abundance-ledger-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0153 | info | discoverability | `projects/media-production/creative-abundance-quality-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0154 | info | discoverability | `projects/media-production/creative-production-operator-14-day-ramp.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0155 | warning | freshness-metadata | `projects/media-production/creative-production-operator-14-day-ramp.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0156 | info | discoverability | `projects/media-production/creative-production-operator-assignment-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0157 | info | discoverability | `projects/media-production/creative-production-operator-assignment-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0158 | info | discoverability | `projects/media-production/creative-production-operator-onboarding.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0159 | info | discoverability | `projects/media-production/creative-production-operator-prerequisite-skills-test.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0160 | info | discoverability | `projects/media-production/creative-production-operator-readiness-exercise.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0161 | info | discoverability | `projects/media-production/creative-production-operator-readiness-sprint.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0162 | info | discoverability | `projects/media-production/creative-production-operator-training-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0163 | info | discoverability | `projects/media-production/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0164 | info | discoverability | `projects/media-production/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0165 | info | discoverability | `projects/media-production/grace-gems-monthly-service-package.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0166 | info | discoverability | `projects/media-production/grace-gems-trust-architecture-kit.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0167 | info | discoverability | `projects/media-production/harness-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0168 | info | discoverability | `projects/media-production/loop-examples/creative-production-review.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0169 | info | discoverability | `projects/media-production/membrane-notes.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0170 | warning | freshness-metadata | `projects/media-production/membrane-notes.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0171 | info | discoverability | `projects/media-production/operating-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0172 | warning | freshness-metadata | `projects/media-production/operating-review.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0173 | info | discoverability | `projects/media-production/permissions-and-authority-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0174 | warning | freshness-metadata | `projects/media-production/permissions-and-authority-review.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0175 | info | discoverability | `projects/media-production/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0176 | info | discoverability | `projects/media-production/turn-usefulness-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0177 | info | discoverability | `projects/mountain-villa/30-day-plan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0178 | info | discoverability | `projects/mountain-villa/business-intake-survey.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0179 | info | discoverability | `projects/mountain-villa/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0180 | info | discoverability | `projects/mountain-villa/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0181 | info | discoverability | `projects/mountain-villa/loop-examples/seasonal-readiness.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0182 | info | discoverability | `projects/mountain-villa/membrane-notes.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0183 | info | discoverability | `projects/mountain-villa/operating-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0184 | info | discoverability | `projects/mountain-villa/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0185 | info | discoverability | `projects/mountain-villa/turn-usefulness-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0186 | info | discoverability | `projects/operating-portfolio-dashboard.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0187 | info | discoverability | `projects/portfolio-knowledge-synergies.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0188 | info | discoverability | `projects/singularity-science/2026-q1-china-humanoid-market-watch.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0189 | info | discoverability | `projects/singularity-science/2026-q2-china-humanoid-market-watch.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0190 | info | discoverability | `projects/singularity-science/2026-q3-china-humanoid-market-watch.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0191 | info | discoverability | `projects/singularity-science/30-day-plan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0192 | warning | freshness-metadata | `projects/singularity-science/30-day-plan.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0193 | warning | freshness-metadata | `projects/singularity-science/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0194 | info | discoverability | `projects/singularity-science/ambient-agency-use-case-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0195 | info | discoverability | `projects/singularity-science/approval-quality-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0196 | info | discoverability | `projects/singularity-science/approval-receipt-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0197 | warning | freshness-metadata | `projects/singularity-science/archive/external-interviews/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0198 | info | discoverability | `projects/singularity-science/archive/external-interviews/analyses/2026-07-09-emad-mostaque-ai-will-run-our-countries-soon.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0199 | info | discoverability | `projects/singularity-science/archive/external-interviews/analysis-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0200 | info | discoverability | `projects/singularity-science/archive/external-interviews/roi-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0201 | info | discoverability | `projects/singularity-science/archive/external-interviews/source-note-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0202 | info | discoverability | `projects/singularity-science/archive/external-interviews/source-notes/2026-07-09-emad-mostaque-ai-will-run-our-countries-soon.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0203 | warning | freshness-metadata | `projects/singularity-science/archive/innermost-loop/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0204 | info | discoverability | `projects/singularity-science/archive/innermost-loop/analyses/2026-07-08-july-5-to-july-8-innermost-loop-cluster.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0205 | info | discoverability | `projects/singularity-science/archive/innermost-loop/analyses/2026-07-20-july-14-to-july-17-cluster.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0206 | info | discoverability | `projects/singularity-science/archive/innermost-loop/analyses/2026-07-21-worldmonitor-gated-fixture-infrastructure-event.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0207 | info | discoverability | `projects/singularity-science/archive/innermost-loop/analysis-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0208 | info | discoverability | `projects/singularity-science/archive/innermost-loop/research-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0209 | info | discoverability | `projects/singularity-science/archive/innermost-loop/source-note-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0210 | info | discoverability | `projects/singularity-science/archive/innermost-loop/source-notes/2026-07-08-july-5-to-july-8-innermost-loop-cluster.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0211 | info | discoverability | `projects/singularity-science/archive/innermost-loop/source-notes/2026-07-20-july-14-to-july-17-cluster.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0212 | info | discoverability | `projects/singularity-science/archive/innermost-loop/source-notes/2026-07-21-worldmonitor-gated-fixture-infrastructure-event.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0213 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-06-09-moonshots-emerging-anthropic-global-pause-recursive-self-improvement-ai-personhood.analysis.md` | 13 | linked target does not exist | no |
| CIA-0214 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-06-09-moonshots-emerging-anthropic-global-pause-recursive-self-improvement-ai-personhood.analysis.md` | 14 | linked target does not exist | no |
| CIA-0215 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-openai-ipo-delay.analysis.md` | 13 | linked target does not exist | no |
| CIA-0216 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-openai-ipo-delay.analysis.md` | 14 | linked target does not exist | no |
| CIA-0217 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-07-08-moonshots-268-sonnet-5-fable-5-fusion-philip-johnston.analysis.md` | 14 | linked target does not exist | no |
| CIA-0218 | error | broken-link | `projects/singularity-science/archive/moonshots/analyses/2026-07-08-moonshots-269-claude-conscious-fable-5-government-deal-openai.analysis.md` | 14 | linked target does not exist | no |
| CIA-0219 | info | discoverability | `projects/singularity-science/archive/moonshots/analyses/2026-07-19-kimi-k3-delivers-frontier-ai-at-1-percent-of-the-cost-ai-sputnik-moment-emad-mostaque.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0220 | info | discoverability | `projects/singularity-science/archive/moonshots/analysis-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0221 | info | discoverability | `projects/singularity-science/archive/moonshots/roi-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0222 | info | discoverability | `projects/singularity-science/archive/moonshots/source-note-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0223 | info | discoverability | `projects/singularity-science/archive/moonshots/source-notes/2026-07-08-moonshots-269-claude-conscious-fable-5-government-deal-openai.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0224 | info | discoverability | `projects/singularity-science/archive/moonshots/source-notes/2026-07-19-kimi-k3-delivers-frontier-ai-at-1-percent-of-the-cost-ai-sputnik-moment-emad-mostaque.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0225 | error | broken-link | `projects/singularity-science/archive/moonshots/transcripts/2026-06-09-moonshots-emerging-anthropic-pause-ai-personhood-2026-06-09.md` | 56 | linked target does not exist | no |
| CIA-0226 | error | broken-link | `projects/singularity-science/archive/moonshots/transcripts/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-2026-06-19.md` | 61 | linked target does not exist | no |
| CIA-0227 | error | broken-link | `projects/singularity-science/archive/moonshots/transcripts/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-2026-06-19.md` | 62 | linked target does not exist | no |
| CIA-0228 | error | broken-link | `projects/singularity-science/archive/moonshots/transcripts/2026-06-19-moonshots-265-spacex-ipo-anthropic-export-control-2026-06-19.md` | 63 | linked target does not exist | no |
| CIA-0229 | warning | freshness-metadata | `projects/singularity-science/archive/nate-b-jones/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0230 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/analyses/2026-07-09-claude-fable-5-bossed-20-cheap-ai-agents-site-cost-8.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0231 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/analyses/2026-07-17-codex-vs-fable-which-ai-agent-picked-the-better-problem.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0232 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/analyses/2026-07-17-fable-5-and-gpt-5-6-dont-need-better-prompts-they-need-a-clean-setup.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0233 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/analyses/2026-07-17-your-roadmap-is-why-youre-losing-to-ai-native-teams.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0234 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/analysis-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0235 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/roi-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0236 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/source-note-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0237 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/source-notes/2026-07-09-claude-fable-5-bossed-20-cheap-ai-agents-site-cost-8.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0238 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/source-notes/2026-07-17-codex-vs-fable-which-ai-agent-picked-the-better-problem.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0239 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/source-notes/2026-07-17-fable-5-and-gpt-5-6-dont-need-better-prompts-they-need-a-clean-setup.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0240 | info | discoverability | `projects/singularity-science/archive/nate-b-jones/source-notes/2026-07-17-your-roadmap-is-why-youre-losing-to-ai-native-teams.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0241 | warning | freshness-metadata | `projects/singularity-science/archive/nate-herk/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0242 | info | discoverability | `projects/singularity-science/archive/nate-herk/analyses/2026-07-22-how-id-make-money-with-claude-if-my-life-depended-on-it.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0243 | info | discoverability | `projects/singularity-science/archive/nate-herk/analyses/2026-07-22-how-you-can-provide-the-most-ai-value-to-businesses.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0244 | info | discoverability | `projects/singularity-science/archive/nate-herk/analyses/2026-07-23-steal-my-exact-ai-os-setup-5-simple-tips.analysis.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0245 | info | discoverability | `projects/singularity-science/archive/nate-herk/analysis-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0246 | info | discoverability | `projects/singularity-science/archive/nate-herk/roi-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0247 | info | discoverability | `projects/singularity-science/archive/nate-herk/source-note-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0248 | info | discoverability | `projects/singularity-science/archive/nate-herk/source-notes/2026-07-22-how-id-make-money-with-claude-if-my-life-depended-on-it.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0249 | info | discoverability | `projects/singularity-science/archive/nate-herk/source-notes/2026-07-22-how-you-can-provide-the-most-ai-value-to-businesses.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0250 | info | discoverability | `projects/singularity-science/archive/nate-herk/source-notes/2026-07-23-steal-my-exact-ai-os-setup-5-simple-tips.source-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0251 | info | discoverability | `projects/singularity-science/archive/transcript-import-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0252 | info | discoverability | `projects/singularity-science/china-humanoid-market-watch.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0253 | info | discoverability | `projects/singularity-science/cross-lane-nested-loop-comparison.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0254 | info | discoverability | `projects/singularity-science/customer-impact-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0255 | info | discoverability | `projects/singularity-science/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0256 | info | discoverability | `projects/singularity-science/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0257 | info | discoverability | `projects/singularity-science/loop-examples/research-to-primitive-routing.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0258 | info | discoverability | `projects/singularity-science/media-production-harness-baseline-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0259 | info | discoverability | `projects/singularity-science/media-production-model-swap-evaluation-packet.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0260 | info | discoverability | `projects/singularity-science/media-production-model-swap-readiness-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0261 | warning | freshness-metadata | `projects/singularity-science/media-production-model-swap-readiness-review.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0262 | info | discoverability | `projects/singularity-science/media-production-model-swap-run-a-output.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0263 | warning | freshness-metadata | `projects/singularity-science/media-production-model-swap-run-a-output.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0264 | info | discoverability | `projects/singularity-science/membrane-notes.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0265 | warning | freshness-metadata | `projects/singularity-science/membrane-notes.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0266 | info | discoverability | `projects/singularity-science/moonshots-272-learning-loop-ownership-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0267 | warning | freshness-metadata | `projects/singularity-science/moonshots-272-learning-loop-ownership-review.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0268 | info | discoverability | `projects/singularity-science/moonshots-272-recursive-self-improvement-deep-dive.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0269 | info | discoverability | `projects/singularity-science/moonshots-272-research-to-improvement-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0270 | info | discoverability | `projects/singularity-science/moonshots-272-singularity-implications-memo.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0271 | info | discoverability | `projects/singularity-science/nate-b-jones-clean-setup-lane-implications-memo.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0272 | info | discoverability | `projects/singularity-science/operating-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0273 | info | discoverability | `projects/singularity-science/orchestration-failure-mode-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0274 | info | discoverability | `projects/singularity-science/orchestration-usefulness-exemplar.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0275 | info | discoverability | `projects/singularity-science/primitives/acceleration-source-verification-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0276 | warning | freshness-metadata | `projects/singularity-science/primitives/acceleration-source-verification-gate.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0277 | info | discoverability | `projects/singularity-science/primitives/ambient-agency-review-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0278 | info | discoverability | `projects/singularity-science/primitives/embodied-agency-adoption-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0279 | info | discoverability | `projects/singularity-science/primitives/embodied-ai-exposure-scan.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0280 | info | discoverability | `projects/singularity-science/primitives/permissions-and-authority-review-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0281 | info | discoverability | `projects/singularity-science/primitives/translation-integrity-review-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0282 | info | discoverability | `projects/singularity-science/research-operating-model.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0283 | info | discoverability | `projects/singularity-science/research-to-improvement-receipt-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0284 | info | discoverability | `projects/singularity-science/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0285 | info | discoverability | `projects/singularity-science/templates/china-humanoid-quarterly-watch-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0286 | info | discoverability | `projects/singularity-science/translation-integrity-audit-receipt-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0287 | info | discoverability | `projects/singularity-science/translation-integrity-ledger.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0288 | info | discoverability | `projects/singularity-science/translation-integrity-roi-audit-2026-07-22.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0289 | info | discoverability | `projects/singularity-science/translation-integrity-validation-2026-07-22.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0290 | info | discoverability | `projects/singularity-science/turn-receipt-template.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0291 | info | discoverability | `projects/singularity-science/turn-usefulness-audit-matrix.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0292 | info | discoverability | `projects/singularity-science/turn-usefulness-audit-report.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0293 | info | discoverability | `projects/singularity-science/turn-usefulness-scorecard.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0294 | warning | freshness-metadata | `projects/singularity-science/turn-usefulness-scorecard.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0295 | info | discoverability | `projects/singularity-science/useful-turn-evaluation-note.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0296 | warning | freshness-metadata | `projects/singularity-science/useful-turn-evaluation-note.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0297 | info | discoverability | `projects/singularity-science/worldmonitor-signal-pilot-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0298 | info | discoverability | `projects/singularity-science/worldmonitor-signal-to-archive-promotion-gate.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0299 | error | broken-link | `skills/README.md` | 13 | linked target does not exist | no |
| CIA-0300 | info | discoverability | `skills/automation-opportunity-review/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0301 | info | discoverability | `skills/automation-opportunity-review/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0302 | info | discoverability | `skills/automation-value-proof/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0303 | info | discoverability | `skills/automation-value-proof/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0304 | info | discoverability | `skills/bounded-workflow-pilot/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0305 | info | discoverability | `skills/bounded-workflow-pilot/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0306 | info | discoverability | `skills/bravo/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0307 | warning | freshness-metadata | `skills/bravo/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0308 | info | discoverability | `skills/business-intake/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0309 | info | discoverability | `skills/business-intake/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0310 | info | discoverability | `skills/business-intake/references/output-contracts.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0311 | info | discoverability | `skills/business-intake/references/question-strategy.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0312 | info | discoverability | `skills/elicitation/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0313 | info | discoverability | `skills/friction/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0314 | info | discoverability | `skills/grace-gems/customer-support-intelligence/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0315 | info | discoverability | `skills/grace-gems/marketplace-listing-gate/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0316 | info | discoverability | `skills/grace-gems/trust-claim-review/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0317 | info | discoverability | `skills/intent-recovery/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0318 | info | discoverability | `skills/intent-recovery/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0319 | info | discoverability | `skills/media-production/media-production-brief/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0320 | info | discoverability | `skills/media-production/media-production-ledger/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0321 | info | discoverability | `skills/media-production/media-production-package/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0322 | info | discoverability | `skills/media-production/media-production-quality-gate/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0323 | info | discoverability | `skills/project-state-update/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0324 | info | discoverability | `skills/project-state-update/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0325 | info | discoverability | `skills/review-ai-harness/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0326 | warning | freshness-metadata | `skills/review-ai-harness/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0327 | info | discoverability | `skills/review-ai-harness/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0328 | info | discoverability | `skills/review-ai-harness/references/review-contract.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0329 | warning | freshness-metadata | `skills/review-ai-harness/references/review-contract.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0330 | info | discoverability | `skills/singularity-intake/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0331 | warning | freshness-metadata | `skills/singularity-intake/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0332 | info | discoverability | `skills/singularity-learning-update/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0333 | warning | freshness-metadata | `skills/singularity-learning-update/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0334 | info | discoverability | `skills/singularity-learning-update/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0335 | info | discoverability | `skills/singularity-recurrence-review/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0336 | warning | freshness-metadata | `skills/singularity-recurrence-review/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0337 | info | discoverability | `skills/singularity-recurrence-review/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0338 | info | discoverability | `skills/student-operating-system/learner-intake/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0339 | info | discoverability | `skills/student-operating-system/learner-intake/references/clickable-create-cards.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0340 | warning | freshness-metadata | `skills/student-operating-system/learner-intake/references/clickable-create-cards.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0341 | info | discoverability | `skills/student-operating-system/learner-intake/references/output-contracts.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0342 | info | discoverability | `skills/student-operating-system/learner-intake/references/question-strategy.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0343 | warning | freshness-metadata | `skills/student-operating-system/learner-intake/references/question-strategy.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0344 | info | discoverability | `skills/student-operating-system/learner-profile/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0345 | warning | freshness-metadata | `skills/student-operating-system/learner-profile/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0346 | info | discoverability | `skills/student-operating-system/learning-core-lane/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0347 | info | discoverability | `skills/student-operating-system/learning-plan/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0348 | info | discoverability | `skills/student-operating-system/new-student-30-day-plan/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0349 | info | discoverability | `skills/student-operating-system/parent-interface/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0350 | warning | freshness-metadata | `skills/student-operating-system/parent-interface/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0351 | info | discoverability | `skills/student-operating-system/student-experience/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0352 | warning | freshness-metadata | `skills/student-operating-system/student-experience/SKILL.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0353 | info | discoverability | `skills/student-operating-system/weekly-parent-review/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0354 | info | discoverability | `skills/tax-financial-governance/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0355 | info | discoverability | `skills/world-monitor/SKILL.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0356 | info | discoverability | `skills/world-monitor/agents/openai.yaml` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0357 | info | discoverability | `skills/world-monitor/references/review-packet.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0358 | info | discoverability | `templates/approval-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0359 | info | discoverability | `templates/assistant-approval-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0360 | info | discoverability | `templates/authority-access-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0361 | info | discoverability | `templates/authority-header.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0362 | warning | freshness-metadata | `templates/authority-header.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0363 | info | discoverability | `templates/authority-revocation-rollback.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0364 | warning | freshness-metadata | `templates/authority-revocation-rollback.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0365 | info | discoverability | `templates/chief-executive-brief.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0366 | warning | freshness-metadata | `templates/chief-executive-brief.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0367 | info | discoverability | `templates/claim-discipline-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0368 | info | discoverability | `templates/commitment-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0369 | info | discoverability | `templates/company-context-map.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0370 | info | discoverability | `templates/decision-log.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0371 | info | discoverability | `templates/escalation-record.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0372 | info | discoverability | `templates/executive-assistant-action-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0373 | info | discoverability | `templates/executive-council-pilot-receipt.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0374 | info | discoverability | `templates/executive-task.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0375 | info | discoverability | `templates/grace-gems-90-day-proof-report.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0376 | info | discoverability | `templates/interface-correction.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0377 | info | discoverability | `templates/interface-handoff.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0378 | info | discoverability | `templates/interface-response.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0379 | info | discoverability | `templates/meeting-to-execution-packet.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0380 | warning | freshness-metadata | `templates/meeting-to-execution-packet.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0381 | info | discoverability | `templates/pilot-metrics-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0382 | warning | freshness-metadata | `templates/project-install/README.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0383 | info | discoverability | `templates/project-install/executive-os-install.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0384 | info | discoverability | `templates/risk-register.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0385 | info | discoverability | `templates/singularity-learning-update.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0386 | warning | freshness-metadata | `templates/singularity-learning-update.md` |  | authority language has no visible date, owner, cadence, or freshness marker | yes |
| CIA-0387 | info | discoverability | `templates/singularity-recurrence-review.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |
| CIA-0388 | info | discoverability | `templates/workflow-correction-proposal.md` |  | artifact is not named by a README, index, ledger, or manifest scan | yes |

## Non-findings

- Existing validators remain authoritative for project installs, authority envelopes, epistemic manifests, artifact state, bounded agency, and privacy scans.
- Archive transcripts are not treated as orphaned merely because they are not customer-routed.
- Ordinary findings do not affect command exit status.

## Boundary

This audit is internal repository evidence. It does not grant authority, approve publication or routing, establish rights or security clearance, or establish customer ROI.
