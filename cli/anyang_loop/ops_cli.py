from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

from .ops_db import connect, connect_readonly, migrate, schema_version
from .epistemic_review import (
    claim_explanation_data,
    epistemic_review_data,
    impact_packet_data,
    render_claim_explanation_markdown,
    render_epistemic_review_markdown,
    render_impact_packet_markdown,
)
from .ops_render import audit_data, render_json, render_weekly_markdown, weekly_review_data
from .ops_service import (
    APPROVAL_SCOPES,
    AUTHORITY_SCOPES,
    DEPENDENCY_ROLES,
    DEPENDENCY_TYPES,
    EVIDENCE_CLASSIFICATIONS,
    EPISTEMIC_STATES,
    SOURCE_INDEPENDENCE_STATES,
    WORK_STATES,
    OpsError,
    add_actor,
    add_claim,
    add_claim_dependency,
    add_evidence,
    add_source,
    create_work,
    grant_authority,
    init_tenant,
    list_epistemic_impacts,
    now_utc,
    record_approval,
    record_outcome,
    revoke_approval,
    revoke_authority,
    retire_claim_dependency,
    transition_claim,
    transition_work,
    update_epistemic_impact,
)
from .intake_control import (
    authorize_review,
    bootstrap_context,
    decide_context,
    intake_status,
    load_manifest,
    manifest_hash,
    persist_context,
    propose_context,
    render_intake_status,
)
from .privacy_scan import render_findings, scan_repo
from .cadence_metrics import (
    COMPLETION_STATUSES,
    EVENT_TYPES as CADENCE_EVENT_TYPES,
    STATE_SOURCES,
    measurement_report,
    record_measurement,
)
from .council_workroom import (
    EVENT_TYPES as COUNCIL_EVENT_TYPES,
    backfill_friction_pilot,
    compare_council_envelope,
    council_decision_envelope,
    council_envelope_pilot_review,
    council_inbox,
    council_pilot_review,
    council_projection,
    create_council_transaction,
    friction_backfill_plan,
    load_envelope_packet,
    load_packet,
    open_envelope_review_session,
    record_council_event,
    render_council_inbox_markdown,
    render_council_envelope_markdown,
    render_council_envelope_pilot_review_markdown,
    render_council_markdown,
    render_council_pilot_review_markdown,
    start_envelope_pilot,
    submit_envelope_review_session,
    verify_council_transaction,
    verify_council_envelope,
)
from .choice_learning import (
    assert_choice_scope,
    choice_context,
    choice_projection,
    choice_review,
    load_choice_packet,
    record_choice_event,
    record_retained_choice_outcome,
    record_choice_selection,
    render_choice_context_markdown,
    render_choice_markdown,
    render_choice_review_markdown,
    validate_choice_event_packet,
    validate_retained_outcome_packet,
    validate_choice_selection_packet,
    verify_choice,
)
from .choice_continuity import (
    choice_status,
    clear_choice_continuity,
    configure_choice_continuity,
    render_choice_status_markdown,
)
from .external_ledger import resolve_ledger


REPO_ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OpsError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anyang-ops", description="Governed Anyang operating ledger")
    parser.add_argument("--db", help="SQLite database path; otherwise ANYANG_DATA_DIR/anyang-ops.db")
    sub = parser.add_subparsers(required=True)

    init = sub.add_parser("init", help="Initialize a database and tenant")
    _tenant(init)
    init.add_argument("--name", required=True)
    init.add_argument("--policy-profile", required=True)
    init.add_argument("--retainer-cents", type=int, default=0)
    init.add_argument("--contractor-budget-cents", type=int, default=0)
    init.add_argument("--tool-budget-cents", type=int, default=0)
    _dry(init)
    init.set_defaults(func=cmd_init)

    actor = sub.add_parser("actor", help="Manage human actors")
    actor_sub = actor.add_subparsers(required=True)
    actor_add = actor_sub.add_parser("add")
    _tenant(actor_add)
    actor_add.add_argument("--name", required=True)
    actor_add.add_argument("--role", required=True)
    _dry(actor_add)
    actor_add.set_defaults(func=lambda args: mutate(args, add_actor, args.tenant, args.name, args.role))

    authority = sub.add_parser("authority", help="Manage authority grants")
    authority_sub = authority.add_subparsers(required=True)
    authority_grant = authority_sub.add_parser("grant")
    _tenant(authority_grant)
    authority_grant.add_argument("--actor-id", required=True)
    authority_grant.add_argument("--scope", choices=AUTHORITY_SCOPES, required=True)
    authority_grant.add_argument("--effective-at")
    authority_grant.add_argument("--expires-at")
    _dry(authority_grant)
    authority_grant.set_defaults(func=lambda args: mutate(args, grant_authority, args.tenant, args.actor_id, args.scope, args.effective_at, args.expires_at))
    authority_revoke = authority_sub.add_parser("revoke")
    authority_revoke.add_argument("grant_id")
    authority_revoke.add_argument("--actor", required=True)
    _dry(authority_revoke)
    authority_revoke.set_defaults(func=lambda args: mutate(args, revoke_authority, args.grant_id, args.actor))

    source = sub.add_parser("source")
    source_sub = source.add_subparsers(required=True)
    source_add = source_sub.add_parser("add")
    _tenant(source_add)
    source_add.add_argument("--title", required=True)
    source_add.add_argument("--source-type", required=True)
    source_add.add_argument("--provenance", required=True)
    source_add.add_argument("--sensitivity", choices=("public", "internal", "private", "restricted"), required=True)
    source_add.add_argument("--rights-status", required=True)
    source_add.add_argument("--evidence-ref", required=True)
    source_add.add_argument("--fresh-until")
    source_add.add_argument("--origin-group")
    source_add.add_argument("--independence-status", choices=SOURCE_INDEPENDENCE_STATES, default="unknown")
    source_add.add_argument("--redacted-summary", default="")
    source_add.add_argument("--actor", default="operator")
    _dry(source_add)
    source_add.set_defaults(func=cmd_source_add)

    claim = sub.add_parser("claim")
    claim_sub = claim.add_subparsers(required=True)
    claim_add = claim_sub.add_parser("add")
    _tenant(claim_add)
    claim_add.add_argument("--text", required=True)
    claim_add.add_argument("--classification", choices=EVIDENCE_CLASSIFICATIONS, required=True)
    claim_add.add_argument("--evidence-strength", choices=("strong", "medium", "thin", "none"), required=True)
    claim_add.add_argument("--scope", required=True)
    claim_add.add_argument("--status", choices=("active", "provisional", "hold", "retired"), required=True)
    claim_add.add_argument("--epistemic-state", choices=EPISTEMIC_STATES, default="unresolved")
    claim_add.add_argument("--source-id", action="append", default=[])
    claim_add.add_argument("--expires-at")
    claim_add.add_argument("--actor", default="operator")
    _dry(claim_add)
    claim_add.set_defaults(func=cmd_claim_add)
    claim_transition = claim_sub.add_parser("transition")
    claim_transition.add_argument("claim_id")
    claim_transition.add_argument("target", choices=EPISTEMIC_STATES)
    claim_transition.add_argument("--cause-type", required=True)
    claim_transition.add_argument("--cause-ref", required=True)
    claim_transition.add_argument("--actor", required=True)
    claim_transition.add_argument("--rationale", required=True)
    _dry(claim_transition)
    claim_transition.set_defaults(
        func=lambda args: mutate(
            args,
            transition_claim,
            args.claim_id,
            args.target,
            args.cause_type,
            args.cause_ref,
            args.actor,
            args.rationale,
        )
    )

    dependency = sub.add_parser("dependency", help="Manage downstream epistemic dependencies")
    dependency_sub = dependency.add_subparsers(required=True)
    dependency_add = dependency_sub.add_parser("add")
    _tenant(dependency_add)
    dependency_add.add_argument("--upstream-claim-id", required=True)
    dependency_add.add_argument("--downstream-type", choices=DEPENDENCY_TYPES, required=True)
    dependency_add.add_argument("--downstream-ref", required=True)
    dependency_add.add_argument("--role", choices=DEPENDENCY_ROLES, required=True)
    dependency_add.add_argument("--actor", required=True)
    _dry(dependency_add)
    dependency_add.set_defaults(
        func=lambda args: mutate(
            args,
            add_claim_dependency,
            args.tenant,
            args.upstream_claim_id,
            args.downstream_type,
            args.downstream_ref,
            args.role,
            args.actor,
        )
    )
    dependency_retire = dependency_sub.add_parser("retire")
    dependency_retire.add_argument("dependency_id")
    dependency_retire.add_argument("--actor", required=True)
    _dry(dependency_retire)
    dependency_retire.set_defaults(
        func=lambda args: mutate(args, retire_claim_dependency, args.dependency_id, args.actor)
    )

    impact = sub.add_parser("impact", help="Review downstream epistemic impacts")
    impact_sub = impact.add_subparsers(required=True)
    impact_list = impact_sub.add_parser("list")
    _tenant(impact_list)
    impact_list.add_argument("--status", choices=("open", "acknowledged", "resolved"))
    impact_list.set_defaults(func=cmd_impact_list)
    impact_ack = impact_sub.add_parser("acknowledge")
    impact_ack.add_argument("impact_id")
    impact_ack.add_argument("--actor", required=True)
    _dry(impact_ack)
    impact_ack.set_defaults(
        func=lambda args: mutate(args, update_epistemic_impact, args.impact_id, "acknowledged", args.actor)
    )
    impact_resolve = impact_sub.add_parser("resolve")
    impact_resolve.add_argument("impact_id")
    impact_resolve.add_argument("--actor", required=True)
    impact_resolve.add_argument("--resolution", required=True)
    _dry(impact_resolve)
    impact_resolve.set_defaults(
        func=lambda args: mutate(
            args, update_epistemic_impact, args.impact_id, "resolved", args.actor, args.resolution
        )
    )

    epistemic = sub.add_parser("epistemic", help="Explain and review live epistemic state")
    epistemic_sub = epistemic.add_subparsers(required=True)
    epistemic_review = epistemic_sub.add_parser("review", help="Show the prioritized epistemic review queue")
    _tenant(epistemic_review)
    epistemic_review.add_argument("--as-of")
    _read_format(epistemic_review)
    epistemic_review.set_defaults(func=cmd_epistemic_review)
    epistemic_explain = epistemic_sub.add_parser("explain", help="Explain one controlling claim")
    _tenant(epistemic_explain)
    epistemic_explain.add_argument("--claim-id", required=True)
    _read_format(epistemic_explain)
    epistemic_explain.set_defaults(func=cmd_epistemic_explain)
    epistemic_packet = epistemic_sub.add_parser("packet", help="Build an evidence-change review packet")
    _tenant(epistemic_packet)
    epistemic_packet.add_argument("--impact-id", required=True)
    _read_format(epistemic_packet)
    epistemic_packet.set_defaults(func=cmd_epistemic_packet)

    work = sub.add_parser("work")
    work_sub = work.add_subparsers(required=True)
    work_create = work_sub.add_parser("create")
    _tenant(work_create)
    work_create.add_argument("--title", required=True)
    work_create.add_argument("--asset-job", required=True)
    work_create.add_argument("--owner", required=True)
    work_create.add_argument("--reviewer", required=True)
    work_create.add_argument("--deliverable", required=True)
    work_create.add_argument("--assignee", default="")
    work_create.add_argument("--source-id", action="append", default=[])
    work_create.add_argument("--claim-id", action="append", default=[])
    work_create.add_argument("--due-at")
    work_create.add_argument("--capacity-hours", type=float, required=True)
    work_create.add_argument("--budget-cents", type=int, default=0)
    work_create.add_argument("--actor", default="operator")
    _dry(work_create)
    work_create.set_defaults(func=cmd_work_create)
    transition = work_sub.add_parser("transition")
    transition.add_argument("work_id")
    transition.add_argument("target", choices=WORK_STATES)
    transition.add_argument("--actor", required=True)
    transition.add_argument("--reason", default="")
    transition.add_argument("--responsible-human", default="")
    _dry(transition)
    transition.set_defaults(func=lambda args: mutate(args, transition_work, args.work_id, args.target, args.actor, args.reason, args.responsible_human))

    evidence = sub.add_parser("evidence")
    evidence_sub = evidence.add_subparsers(required=True)
    evidence_add = evidence_sub.add_parser("add")
    _tenant(evidence_add)
    evidence_add.add_argument("--work-id")
    evidence_add.add_argument("--type", required=True, dest="evidence_type")
    evidence_add.add_argument("--reference", required=True)
    evidence_add.add_argument("--creator", required=True)
    evidence_add.add_argument("--integrity-hash")
    _dry(evidence_add)
    evidence_add.set_defaults(func=cmd_evidence_add)

    approval = sub.add_parser("approval")
    approval_sub = approval.add_subparsers(required=True)
    approval_record = approval_sub.add_parser("record")
    _tenant(approval_record)
    approval_record.add_argument("--work-id", required=True)
    approval_record.add_argument("--approver-actor-id", required=True)
    approval_record.add_argument("--scope", choices=APPROVAL_SCOPES, required=True)
    approval_record.add_argument("--decision", choices=("approved", "approved_with_changes", "rejected"), required=True)
    approval_record.add_argument("--conditions", default="")
    approval_record.add_argument("--expires-at")
    _dry(approval_record)
    approval_record.set_defaults(func=cmd_approval_record)
    approval_revoke = approval_sub.add_parser("revoke")
    approval_revoke.add_argument("approval_id")
    approval_revoke.add_argument("--actor", required=True)
    _dry(approval_revoke)
    approval_revoke.set_defaults(func=lambda args: mutate(args, revoke_approval, args.approval_id, args.actor))

    outcome = sub.add_parser("outcome")
    outcome_sub = outcome.add_subparsers(required=True)
    outcome_record = outcome_sub.add_parser("record")
    _tenant(outcome_record)
    outcome_record.add_argument("--work-id", required=True)
    outcome_record.add_argument("--expected-result", required=True)
    outcome_record.add_argument("--observed-result", default="pending")
    outcome_record.add_argument("--metric", required=True)
    outcome_record.add_argument("--metric-value", type=float)
    outcome_record.add_argument("--observation-window", required=True)
    outcome_record.add_argument("--confidence", choices=("high", "medium", "low", "pending"), required=True)
    outcome_record.add_argument("--actor", default="operator")
    _dry(outcome_record)
    outcome_record.set_defaults(func=cmd_outcome_record)

    review = sub.add_parser("review")
    review_sub = review.add_subparsers(required=True)
    weekly = review_sub.add_parser("weekly")
    _tenant(weekly)
    weekly.add_argument("--week", required=True, help="Week start in YYYY-MM-DD")
    weekly.add_argument("--as-of")
    weekly.add_argument("--format", choices=("markdown", "json"), default="markdown")
    weekly.add_argument("--output")
    weekly.set_defaults(func=cmd_weekly)

    audit = sub.add_parser("audit")
    _tenant(audit)
    audit.add_argument("--as-of")
    audit.add_argument("--format", choices=("markdown", "json"), default="markdown")
    audit.set_defaults(func=cmd_audit)

    intake = sub.add_parser("intake", help="Govern business-context intake and effectiveness")
    intake_sub = intake.add_subparsers(required=True)

    intake_propose = intake_sub.add_parser("propose", help="Import a sanitized intake-control manifest")
    _tenant(intake_propose)
    intake_propose.add_argument("--manifest", required=True)
    _dry(intake_propose)
    intake_propose.set_defaults(func=cmd_intake_propose)

    intake_bootstrap = intake_sub.add_parser("bootstrap", help="Import one exact pre-existing effective context")
    _tenant(intake_bootstrap)
    intake_bootstrap.add_argument("--manifest", required=True)
    intake_bootstrap.add_argument("--actor-id", required=True)
    intake_bootstrap.add_argument("--subject-hash", required=True)
    intake_bootstrap.add_argument("--approval-receipt-ref", required=True)
    intake_bootstrap.add_argument("--persistence-ref", required=True)
    _dry(intake_bootstrap)
    intake_bootstrap.set_defaults(func=cmd_intake_bootstrap)

    intake_decide = intake_sub.add_parser("decide", help="Bind an owner decision to an exact proposal")
    _tenant(intake_decide)
    intake_decide.add_argument("--version", required=True)
    intake_decide.add_argument("--actor-id", required=True)
    intake_decide.add_argument("--decision", choices=("approved", "rejected", "changes_requested"), required=True)
    intake_decide.add_argument("--subject-hash", required=True)
    intake_decide.add_argument("--conditions", default="")
    _dry(intake_decide)
    intake_decide.set_defaults(func=cmd_intake_decide)

    intake_persist = intake_sub.add_parser("persist", help="Confirm external preservation and make a context effective")
    _tenant(intake_persist)
    intake_persist.add_argument("--version", required=True)
    intake_persist.add_argument("--actor-id", required=True)
    intake_persist.add_argument("--subject-hash", required=True)
    intake_persist.add_argument("--external-ref", required=True)
    _dry(intake_persist)
    intake_persist.set_defaults(func=cmd_intake_persist)

    intake_authorize = intake_sub.add_parser("authorize-review", help="Separately authorize the first operating review")
    _tenant(intake_authorize)
    intake_authorize.add_argument("--version", required=True)
    intake_authorize.add_argument("--actor-id", required=True)
    intake_authorize.add_argument("--decision", choices=("approved", "declined"), required=True)
    intake_authorize.add_argument("--subject-hash", required=True)
    intake_authorize.add_argument("--conditions", default="")
    _dry(intake_authorize)
    intake_authorize.set_defaults(func=cmd_intake_authorize_review)

    intake_status_parser = intake_sub.add_parser("status", help="Render the compact intake-state receipt")
    _tenant(intake_status_parser)
    _read_format(intake_status_parser)
    intake_status_parser.set_defaults(func=cmd_intake_status)

    cadence = sub.add_parser("cadence", help="Measure cadence reconstruction performance")
    cadence_sub = cadence.add_subparsers(required=True)
    cadence_record = cadence_sub.add_parser("record", help="Record one completed or attempted cadence event")
    cadence_record.add_argument("--repo-id", required=True)
    cadence_record.add_argument("--event-type", choices=CADENCE_EVENT_TYPES, required=True)
    cadence_record.add_argument("--scheduled", action=argparse.BooleanOptionalAction, required=True)
    cadence_record.add_argument("--completion-status", choices=COMPLETION_STATUSES, required=True)
    cadence_record.add_argument("--state-source", choices=STATE_SOURCES, required=True)
    cadence_record.add_argument("--manual-reconstruction", action=argparse.BooleanOptionalAction, required=True)
    cadence_record.add_argument("--reconstruction-minutes", type=float, required=True)
    cadence_record.add_argument("--evidence-check-passed", action=argparse.BooleanOptionalAction, required=True)
    cadence_record.add_argument("--privacy-check-passed", action=argparse.BooleanOptionalAction, required=True)
    cadence_record.add_argument("--authority-check-passed", action=argparse.BooleanOptionalAction, required=True)
    cadence_record.add_argument("--recorded-by", required=True)
    cadence_record.add_argument("--occurred-at")
    _dry(cadence_record)
    cadence_record.set_defaults(func=cmd_cadence_record)
    cadence_report = cadence_sub.add_parser("report", help="Report the latest cadence measurement sample")
    cadence_report.add_argument("--repo-id", required=True)
    cadence_report.add_argument("--limit", type=int, default=10)
    cadence_report.set_defaults(func=cmd_cadence_report)

    council = sub.add_parser("council", help="Operate the local Executive Council workroom")
    council_sub = council.add_subparsers(required=True)

    council_create = council_sub.add_parser("create", help="Create an immutable Council transaction")
    _tenant(council_create)
    council_create.add_argument("--packet", required=True)
    _dry(council_create)
    council_create.set_defaults(func=cmd_council_create)

    council_record = council_sub.add_parser("record", help="Append one Council event")
    council_record.add_argument("--transaction-id", required=True)
    council_record.add_argument("--event", choices=COUNCIL_EVENT_TYPES, required=True)
    council_record.add_argument("--packet", required=True)
    _dry(council_record)
    council_record.set_defaults(func=cmd_council_record)

    council_show = council_sub.add_parser("show", help="Render one transaction projection")
    council_show.add_argument("transaction_id")
    _read_format(council_show)
    council_show.set_defaults(func=cmd_council_show)

    council_inbox_parser = council_sub.add_parser(
        "inbox", help="Render the prioritized Council attention inbox"
    )
    _tenant(council_inbox_parser)
    council_inbox_parser.add_argument("--as-of")
    _read_format(council_inbox_parser)
    council_inbox_parser.set_defaults(func=cmd_council_inbox)

    council_review = council_sub.add_parser(
        "pilot-review", help="Generate the ledger-derived 30-day pilot metrics review"
    )
    _tenant(council_review)
    council_review.add_argument("--as-of")
    _read_format(council_review)
    council_review.set_defaults(func=cmd_council_pilot_review)

    council_verify = council_sub.add_parser("verify", help="Verify one event hash chain")
    council_verify.add_argument("transaction_id")
    council_verify.set_defaults(func=cmd_council_verify)

    council_backfill = council_sub.add_parser(
        "backfill-friction-pilot", help="Reconstruct the five-case friction cohort"
    )
    _tenant(council_backfill)
    council_backfill.add_argument("--cohort", required=True)
    council_backfill.add_argument("--tracker", required=True)
    _dry(council_backfill)
    council_backfill.set_defaults(func=cmd_council_backfill)

    council_envelope = council_sub.add_parser(
        "envelope", help="Render a deterministic machine envelope or human receipt"
    )
    council_envelope.add_argument("transaction_id")
    council_envelope.add_argument("--as-of", required=True)
    _read_format(council_envelope)
    council_envelope.set_defaults(func=cmd_council_envelope)

    council_envelope_verify = council_sub.add_parser(
        "envelope-verify", help="Verify a decision envelope without opening SQLite"
    )
    council_envelope_verify.add_argument("--packet", required=True)
    council_envelope_verify.add_argument("--receipt")
    council_envelope_verify.set_defaults(func=cmd_council_envelope_verify)

    council_envelope_compare = council_sub.add_parser(
        "envelope-compare", help="Compare a decision envelope with the current ledger"
    )
    council_envelope_compare.add_argument("--packet", required=True)
    council_envelope_compare.set_defaults(func=cmd_council_envelope_compare)

    council_envelope_review = council_sub.add_parser(
        "envelope-pilot-review", help="Measure the 30-day staged envelope pilot"
    )
    _tenant(council_envelope_review)
    council_envelope_review.add_argument("--from", dest="from_time")
    council_envelope_review.add_argument("--as-of", required=True)
    council_envelope_review.add_argument("--attention-value-per-hour", type=float)
    council_envelope_review.add_argument("--pilot-id")
    _read_format(council_envelope_review)
    council_envelope_review.set_defaults(func=cmd_council_envelope_pilot_review)

    council_pilot_start = council_sub.add_parser(
        "envelope-pilot-start", help="Record the authorized shadow-pilot activation"
    )
    _tenant(council_pilot_start)
    council_pilot_start.add_argument("--control-transaction-id", required=True)
    council_pilot_start.add_argument("--actor-id", required=True)
    _dry(council_pilot_start)
    council_pilot_start.set_defaults(func=cmd_council_envelope_pilot_start)

    council_review_open = council_sub.add_parser(
        "envelope-review-open", help="Open one protected reconstruction session"
    )
    council_review_open.add_argument("--transaction-id", required=True)
    council_review_open.add_argument("--pilot-id", required=True)
    council_review_open.add_argument("--surface", choices=("baseline", "receipt"), required=True)
    council_review_open.add_argument("--reviewer-actor-id", required=True)
    _dry(council_review_open)
    council_review_open.set_defaults(func=cmd_council_envelope_review_open)

    council_review_submit = council_sub.add_parser(
        "envelope-review-submit", help="Submit one protected reconstruction result"
    )
    council_review_submit.add_argument("session_id")
    council_review_submit.add_argument("--packet", required=True)
    _dry(council_review_submit)
    council_review_submit.set_defaults(func=cmd_council_envelope_review_submit)

    choice = sub.add_parser("choice", help="Operate outcome-aware possibility navigation")
    choice_sub = choice.add_subparsers(required=True)

    choice_configure = choice_sub.add_parser(
        "configure", help="Explicitly configure external private choice continuity"
    )
    choice_configuration = choice_configure.add_mutually_exclusive_group(required=True)
    choice_configuration.add_argument("--data-dir")
    choice_configuration.add_argument("--clear", action="store_true")
    _dry(choice_configure)
    choice_configure.set_defaults(func=cmd_choice_configure)

    choice_status_parser = choice_sub.add_parser(
        "status", help="Inspect choice continuity without opening the ledger for writes"
    )
    _read_format(choice_status_parser)
    choice_status_parser.set_defaults(func=cmd_choice_status)

    choice_context_parser = choice_sub.add_parser(
        "context", help="Read comparable outcomes without using selection frequency"
    )
    _tenant(choice_context_parser)
    choice_context_parser.add_argument("--workspace", required=True)
    choice_context_parser.add_argument("--lane", required=True)
    choice_context_parser.add_argument("--kind", required=True)
    choice_context_parser.add_argument("--as-of")
    _read_format(choice_context_parser)
    choice_context_parser.set_defaults(func=cmd_choice_context)

    choice_select = choice_sub.add_parser(
        "select", help="Atomically retain a presented possibility set and selected branch"
    )
    _tenant(choice_select)
    choice_select.add_argument("--packet", required=True)
    _dry(choice_select)
    choice_select.set_defaults(func=cmd_choice_select)

    choice_retain = choice_sub.add_parser(
        "retain-outcome",
        help="Atomically retain one explicitly reviewed choice and outcome",
    )
    _tenant(choice_retain)
    choice_retain.add_argument("--packet", required=True)
    choice_retain.add_argument("--approved-packet-hash")
    _dry(choice_retain)
    choice_retain.set_defaults(func=cmd_choice_retain_outcome)

    choice_outcome = choice_sub.add_parser(
        "outcome", help="Append an outcome, deferral, correction, or supersession"
    )
    choice_outcome.add_argument("choice_id")
    choice_outcome.add_argument("--packet", required=True)
    _dry(choice_outcome)
    choice_outcome.set_defaults(func=cmd_choice_outcome)

    choice_review_parser = choice_sub.add_parser(
        "review", help="Read the prioritized unresolved-outcome queue"
    )
    _tenant(choice_review_parser)
    choice_review_parser.add_argument("--workspace", required=True)
    choice_review_parser.add_argument("--as-of")
    _read_format(choice_review_parser)
    choice_review_parser.set_defaults(func=cmd_choice_review)

    choice_show = choice_sub.add_parser("show", help="Render one selected possibility set")
    choice_show.add_argument("choice_id")
    _tenant(choice_show)
    choice_show.add_argument("--workspace", required=True)
    choice_show.add_argument("--lane", required=True)
    _read_format(choice_show)
    choice_show.set_defaults(func=cmd_choice_show)

    choice_verify = choice_sub.add_parser("verify", help="Verify one choice event chain")
    choice_verify.add_argument("choice_id")
    _tenant(choice_verify)
    choice_verify.add_argument("--workspace", required=True)
    choice_verify.add_argument("--lane", required=True)
    choice_verify.set_defaults(func=cmd_choice_verify)

    privacy = sub.add_parser("privacy-scan")
    privacy.add_argument("--repo", default=".")
    privacy.set_defaults(func=cmd_privacy_scan)
    return parser


def resolve_db(args: argparse.Namespace, *, allow_new: bool = False) -> Path:
    resolution = resolve_ledger(args.db)
    if resolution.database is None:
        raise OpsError(
            "Provide --db, set ANYANG_DATA_DIR, or explicitly run choice configure; "
            "project state is never created inside the repo implicitly"
        )
    path = resolution.database
    if not allow_new and not path.exists():
        raise OpsError(f"Database does not exist: {path}")
    return path


def cmd_init(args: argparse.Namespace) -> int:
    path = resolve_db(args, allow_new=True)
    if args.dry_run:
        return print_result({"dry_run": True, "action": "initialize", "db": str(path), "tenant": args.tenant})
    connection = connect(path, create_parent=True)
    migrate(connection, now_utc())
    result = init_tenant(
        connection,
        slug=args.tenant,
        name=args.name,
        policy_profile=args.policy_profile,
        retainer_cents=args.retainer_cents,
        contractor_budget_cents=args.contractor_budget_cents,
        tool_budget_cents=args.tool_budget_cents,
    )
    return print_result({"db": str(path), "schema_version": schema_version(connection), **result.as_dict()})


def mutate(args: argparse.Namespace, function: Callable, *positional, **keywords) -> int:
    if args.dry_run:
        return print_result({"dry_run": True, "action": function.__name__, "inputs": _safe(vars(args))})
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = function(connection, *positional, **keywords)
    return print_result(result.as_dict())


def cmd_source_add(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, add_source, args.tenant, **_pick(values, "title", "source_type", "provenance", "sensitivity", "rights_status", "evidence_ref", "fresh_until", "origin_group", "independence_status", "redacted_summary", "actor"))


def cmd_claim_add(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, add_claim, args.tenant, args.source_id, **_pick(values, "text", "classification", "evidence_strength", "scope", "status", "epistemic_state", "expires_at", "actor"))


def cmd_impact_list(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        impacts = list_epistemic_impacts(connection, args.tenant, args.status)
    return print_result({"tenant": args.tenant, "impacts": impacts})


def cmd_epistemic_review(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        data = epistemic_review_data(connection, args.tenant, args.as_of)
    return _emit_read_output(args, data, render_epistemic_review_markdown)


def cmd_epistemic_explain(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        data = claim_explanation_data(connection, args.tenant, args.claim_id)
    return _emit_read_output(args, data, render_claim_explanation_markdown)


def cmd_epistemic_packet(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        data = impact_packet_data(connection, args.tenant, args.impact_id)
    return _emit_read_output(args, data, render_impact_packet_markdown)


def cmd_work_create(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, create_work, args.tenant, args.source_id, args.claim_id, **_pick(values, "title", "asset_job", "owner", "reviewer", "deliverable", "assignee", "due_at", "capacity_hours", "budget_cents", "actor"))


def cmd_evidence_add(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, add_evidence, args.tenant, **_pick(values, "work_id", "evidence_type", "reference", "creator", "integrity_hash"))


def cmd_approval_record(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, record_approval, args.tenant, **_pick(values, "work_id", "approver_actor_id", "scope", "decision", "conditions", "expires_at"))


def cmd_outcome_record(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    return mutate(args, record_outcome, args.tenant, **_pick(values, "work_id", "expected_result", "observed_result", "metric", "metric_value", "observation_window", "confidence", "actor"))


def cmd_weekly(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        data = weekly_review_data(connection, args.tenant, args.week, args.as_of)
    output = render_json(data) if args.format == "json" else render_weekly_markdown(data)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        data = audit_data(connection, args.tenant, args.as_of)
    if args.format == "json":
        print(render_json(data), end="")
    else:
        print(f"Audit: {'PASS' if data['ok'] else 'FAIL'}")
        for issue in data["issues"]:
            print(f"- {issue['code']}: {issue['message']}")
    return 0 if data["ok"] else 1


def cmd_intake_propose(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    if args.dry_run:
        return print_result(
            {
                "dry_run": True,
                "action": "propose_context",
                "tenant": args.tenant,
                "version": manifest["version"],
                "base_version": manifest.get("base_version"),
                "content_hash": manifest_hash(manifest),
                "evidence_bindings": len(manifest["evidence"]),
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = propose_context(connection, args.tenant, manifest)
    return print_result(result.as_dict())


def cmd_intake_bootstrap(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    if args.dry_run:
        return print_result(
            {
                "dry_run": True,
                "action": "bootstrap_context",
                "tenant": args.tenant,
                "version": manifest["version"],
                "content_hash": manifest_hash(manifest),
                "supplied_subject_hash": args.subject_hash,
                "actor_id": args.actor_id,
                "approval_receipt_ref": args.approval_receipt_ref,
                "persistence_ref": args.persistence_ref,
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = bootstrap_context(
            connection,
            args.tenant,
            manifest,
            args.actor_id,
            args.subject_hash,
            args.approval_receipt_ref,
            args.persistence_ref,
        )
    return print_result(result.as_dict())


def cmd_intake_decide(args: argparse.Namespace) -> int:
    return mutate(
        args,
        decide_context,
        args.tenant,
        args.version,
        args.actor_id,
        args.decision,
        args.subject_hash,
        args.conditions,
    )


def cmd_intake_persist(args: argparse.Namespace) -> int:
    return mutate(
        args,
        persist_context,
        args.tenant,
        args.version,
        args.actor_id,
        args.subject_hash,
        args.external_ref,
    )


def cmd_intake_authorize_review(args: argparse.Namespace) -> int:
    return mutate(
        args,
        authorize_review,
        args.tenant,
        args.version,
        args.actor_id,
        args.decision,
        args.subject_hash,
        args.conditions,
    )


def cmd_intake_status(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = intake_status(connection, args.tenant)
    return _emit_read_output(args, data, render_intake_status)


def cmd_cadence_record(args: argparse.Namespace) -> int:
    values = _pick(
        vars(args), "repo_id", "event_type", "scheduled", "completion_status", "state_source",
        "manual_reconstruction", "reconstruction_minutes", "evidence_check_passed",
        "privacy_check_passed", "authority_check_passed", "recorded_by", "occurred_at",
    )
    if args.dry_run:
        return print_result({"dry_run": True, "action": "record_cadence_measurement", "inputs": values})
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        measurement = record_measurement(connection, **values)
    return print_result(measurement.as_dict())


def cmd_cadence_report(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        report = measurement_report(connection, args.repo_id, args.limit)
    return print_result(report)


def cmd_council_create(args: argparse.Namespace) -> int:
    packet = load_packet(args.packet)
    if args.dry_run:
        return print_result(
            {
                "dry_run": True,
                "action": "create_council_transaction",
                "tenant": args.tenant,
                "packet": packet,
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = create_council_transaction(connection, args.tenant, packet)
    return print_result(result.as_dict())


def cmd_council_record(args: argparse.Namespace) -> int:
    packet = load_packet(args.packet)
    if args.dry_run:
        return print_result(
            {
                "dry_run": True,
                "action": "record_council_event",
                "transaction_id": args.transaction_id,
                "event": args.event,
                "packet": packet,
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = record_council_event(
            connection, args.transaction_id, args.event, packet, historical=False
        )
    return print_result(result.as_dict())


def cmd_council_show(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = council_projection(connection, args.transaction_id)
    return _emit_read_output(args, data, render_council_markdown)


def cmd_council_inbox(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = council_inbox(connection, args.tenant, args.as_of)
    return _emit_read_output(args, data, render_council_inbox_markdown)


def cmd_council_pilot_review(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = council_pilot_review(connection, args.tenant, args.as_of)
    return _emit_read_output(args, data, render_council_pilot_review_markdown)


def cmd_council_verify(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = verify_council_transaction(connection, args.transaction_id)
    print(render_json(result), end="")
    return 0 if result["ok"] else 1


def cmd_council_backfill(args: argparse.Namespace) -> int:
    plan = friction_backfill_plan(args.cohort, args.tracker)
    if args.dry_run:
        return print_result(
            {
                "dry_run": True,
                "action": "backfill_friction_pilot",
                "tenant": args.tenant,
                **plan,
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = backfill_friction_pilot(
            connection, args.tenant, args.cohort, args.tracker
        )
    return print_result(result.as_dict())


def cmd_council_envelope(args: argparse.Namespace) -> int:
    with connect_readonly(resolve_db(args)) as connection:
        data = council_decision_envelope(
            connection, args.transaction_id, as_of=args.as_of
        )
    _reject_internal_envelope_output(args, data["tenant"])
    return _emit_read_output(args, data, render_council_envelope_markdown)


def cmd_council_envelope_verify(args: argparse.Namespace) -> int:
    packet = load_envelope_packet(args.packet)
    receipt = (
        Path(args.receipt).read_text(encoding="utf-8") if args.receipt else None
    )
    result = verify_council_envelope(packet, receipt=receipt)
    print(render_json(result), end="")
    return 0 if result["ok"] else 1


def cmd_council_envelope_compare(args: argparse.Namespace) -> int:
    packet = load_envelope_packet(args.packet)
    with connect_readonly(resolve_db(args)) as connection:
        result = compare_council_envelope(connection, packet)
    print(render_json(result), end="")
    return 0 if result["ok"] else 1


def cmd_council_envelope_pilot_review(args: argparse.Namespace) -> int:
    with connect_readonly(resolve_db(args)) as connection:
        data = council_envelope_pilot_review(
            connection,
            args.tenant,
            from_time=args.from_time,
            as_of=args.as_of,
            attention_value_per_hour=args.attention_value_per_hour,
            pilot_id=args.pilot_id,
        )
    _reject_internal_envelope_output(args, data["tenant"])
    return _emit_read_output(
        args, data, render_council_envelope_pilot_review_markdown
    )


def cmd_council_envelope_pilot_start(args: argparse.Namespace) -> int:
    return mutate(
        args,
        start_envelope_pilot,
        args.tenant,
        args.control_transaction_id,
        args.actor_id,
    )


def cmd_council_envelope_review_open(args: argparse.Namespace) -> int:
    return mutate(
        args,
        open_envelope_review_session,
        args.transaction_id,
        args.pilot_id,
        args.surface,
        args.reviewer_actor_id,
    )


def cmd_council_envelope_review_submit(args: argparse.Namespace) -> int:
    packet = load_packet(args.packet)
    return mutate(args, submit_envelope_review_session, args.session_id, packet)


def cmd_choice_configure(args: argparse.Namespace) -> int:
    if args.db:
        raise OpsError("choice configure uses --data-dir or --clear, not --db")
    if args.clear:
        return print_result(
            clear_choice_continuity(REPO_ROOT, dry_run=args.dry_run)
        )
    return print_result(
        configure_choice_continuity(
            args.data_dir,
            REPO_ROOT,
            dry_run=args.dry_run,
        )
    )


def cmd_choice_status(args: argparse.Namespace) -> int:
    data = choice_status(resolve_ledger(args.db))
    return _emit_read_output(args, data, render_choice_status_markdown)


def cmd_choice_context(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = choice_context(
            connection,
            args.tenant,
            args.workspace,
            args.lane,
            args.kind,
            args.as_of,
        )
    return _emit_read_output(args, data, render_choice_context_markdown)


def cmd_choice_select(args: argparse.Namespace) -> int:
    packet = load_choice_packet(args.packet)
    if args.dry_run:
        normalized = validate_choice_selection_packet(packet, args.tenant)
        return print_result(
            {
                "dry_run": True,
                "action": "record_choice_selection",
                "tenant": args.tenant,
                "packet": normalized,
                "authority_effect": "none",
                "deferred_checks": ["actor-exists-in-tenant", "idempotency-conflict"],
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = record_choice_selection(connection, args.tenant, packet)
    return print_result(result.as_dict())


def cmd_choice_retain_outcome(args: argparse.Namespace) -> int:
    packet = load_choice_packet(args.packet)
    normalized = validate_retained_outcome_packet(packet, args.tenant)
    if args.dry_run:
        if args.approved_packet_hash:
            raise OpsError("--approved-packet-hash is prohibited during dry run")
        return print_result(
            {
                "dry_run": True,
                "action": "record_retained_choice_outcome",
                **normalized,
                "deferred_checks": ["actor-exists-in-tenant", "idempotency-conflict"],
            }
        )
    if not args.approved_packet_hash:
        raise OpsError("--approved-packet-hash is required for retained outcome mutation")
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = record_retained_choice_outcome(
            connection,
            args.tenant,
            packet,
            args.approved_packet_hash,
        )
    return print_result(result.as_dict())


def cmd_choice_outcome(args: argparse.Namespace) -> int:
    packet = load_choice_packet(args.packet)
    if args.dry_run:
        normalized = validate_choice_event_packet(packet)
        return print_result(
            {
                "dry_run": True,
                "action": "record_choice_event",
                "choice_id": args.choice_id,
                "packet": normalized,
                "deferred_checks": [
                    "choice-exists",
                    "actor-exists-in-tenant",
                    "classification-prior-value",
                    "idempotency-conflict",
                ],
            }
        )
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        result = record_choice_event(connection, args.choice_id, packet)
    return print_result(result.as_dict())


def cmd_choice_review(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        data = choice_review(connection, args.tenant, args.workspace, args.as_of)
    return _emit_read_output(args, data, render_choice_review_markdown)


def cmd_choice_show(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        assert_choice_scope(
            connection,
            args.choice_id,
            args.tenant,
            args.workspace,
            args.lane,
        )
        data = choice_projection(connection, args.choice_id)
    return _emit_read_output(args, data, render_choice_markdown)


def cmd_choice_verify(args: argparse.Namespace) -> int:
    with connect(resolve_db(args)) as connection:
        migrate(connection, now_utc())
        assert_choice_scope(
            connection,
            args.choice_id,
            args.tenant,
            args.workspace,
            args.lane,
        )
        data = verify_choice(connection, args.choice_id)
    print(render_json(data), end="")
    return 0 if data["ok"] else 1


def cmd_privacy_scan(args: argparse.Namespace) -> int:
    findings = scan_repo(args.repo)
    print(render_findings(findings), end="")
    return 1 if findings else 0


def print_result(value: dict) -> int:
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


def _tenant(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tenant", required=True)


def _dry(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dry-run", action="store_true")


def _read_format(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output")


def _emit_read_output(args: argparse.Namespace, data: dict, markdown_renderer: Callable[[dict], str]) -> int:
    output = render_json(data) if args.format == "json" else markdown_renderer(data)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def _reject_internal_envelope_output(args: argparse.Namespace, tenant: str) -> None:
    if tenant != "anyang-internal" or not getattr(args, "output", None):
        return
    output = Path(args.output)
    if not output.is_absolute():
        raise OpsError("Internal envelope output requires an absolute external path")
    resolved = output.resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return
    raise OpsError("Internal envelope output may not be written inside the repository")


def _pick(values: dict, *keys: str) -> dict:
    return {key: values[key] for key in keys}


def _safe(values: dict) -> dict:
    return {key: value for key, value in values.items() if key not in {"func"}}


if __name__ == "__main__":
    raise SystemExit(main())
