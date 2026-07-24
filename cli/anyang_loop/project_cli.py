from __future__ import annotations

import argparse
import json
from pathlib import Path

from .project_model import ProjectInputError, load_project_input
from .project_render import build_project_files, render_html_dashboard, render_obsidian, write_files
from .project_validate import validate_project_path
from .membrane import extract_patterns, render_pattern_report
from .catalog_import import (
    CatalogImportError,
    import_catalog,
    render_catalog_completion_report,
    render_catalog_import_summary,
)
from .transcript_import import (
    TranscriptImportError,
    execute_import_plan,
    import_transcripts,
    import_summary_dict,
    recover_import,
    render_completion_report,
    render_import_summary,
)
from .analytical_interfaces import validate_manifest
from .artifact_state import validate_artifact_manifest
from .epistemic_state import epistemic_report, validate_epistemic_manifest
from .epistemic_benchmark import (
    EpistemicBenchmarkError,
    render_epistemic_benchmark_markdown,
    score_epistemic_benchmark,
)
from .bounded_agency import AgencyContractError, validate_agency_manifest
from .authority import authority_preflight, validate_authority_envelope
from .authority_inventory import inventory_authority, render_inventory
from .phase_preflight import (
    TRANSCRIPT_PHASE,
    render_preflight,
    render_preflight_json,
    run_preflight,
    validate_phase_result,
    verify_transition,
)
from .repo_snapshot import collect_repo_snapshot
from .harness_review import HarnessReviewError, record_decisions, render_harness, scan_harness
from .automation_value_proof import validate_value_proof
from .context_audit import audit_repository, render_markdown, write_audit
from .singularity_intake_validate import validate_lane
from .recurrence_validate import validate_directory


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ProjectInputError as exc:
        print(f"ERROR: {exc}")
        return 1
    except FileExistsError as exc:
        print(f"ERROR: {exc}")
        return 1
    except TranscriptImportError as exc:
        print(f"ERROR: {exc}")
        return 1
    except CatalogImportError as exc:
        print(f"ERROR: {exc}")
        return 1
    except AgencyContractError as exc:
        print(f"ERROR: {exc}")
        return 1
    except EpistemicBenchmarkError as exc:
        print(f"ERROR: {exc}")
        return 1
    except HarnessReviewError as exc:
        print(f"ERROR: {exc}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anyang-project", description="Anyang Intelligence project installer generator")
    subparsers = parser.add_subparsers(required=True)

    new = subparsers.add_parser("new", help="Scaffold a project install folder")
    new.add_argument("input")
    new.add_argument("--output", required=True)
    new.add_argument("--force", action="store_true")
    new.set_defaults(func=cmd_new)

    render = subparsers.add_parser("render", help="Render install files without requiring project placement")
    render.add_argument("input")
    render.add_argument("--format", choices=("markdown", "obsidian", "html"), required=True)
    render.add_argument("--output", required=True)
    render.add_argument("--force", action="store_true")
    render.set_defaults(func=cmd_render)

    extract = subparsers.add_parser("extract-patterns", help="Extract membrane-aware cross-project pattern candidates")
    extract.add_argument("projects_path")
    extract.add_argument("--output", required=True)
    extract.set_defaults(func=cmd_extract_patterns)

    import_cmd = subparsers.add_parser(
        "import-transcripts", help="Import Singularity Science transcripts from a manifest into the archive"
    )
    import_cmd.add_argument("--manifest", required=True)
    import_cmd.add_argument("--dry-run", action="store_true")
    import_cmd.add_argument("--format", choices=("text", "json"), default="text")
    import_cmd.set_defaults(func=cmd_import_transcripts)

    report_cmd = subparsers.add_parser(
        "report-transcript-import", help="Report transcript import completeness from a Singularity Science manifest"
    )
    report_cmd.add_argument("--manifest", required=True)
    report_cmd.set_defaults(func=cmd_report_transcript_import)

    import_catalog_cmd = subparsers.add_parser(
        "import-catalog", help="Import Learning Core catalog entries from a manifest into the catalog area"
    )
    import_catalog_cmd.add_argument("--manifest", required=True)
    import_catalog_cmd.add_argument("--dry-run", action="store_true")
    import_catalog_cmd.set_defaults(func=cmd_import_catalog)

    report_catalog_cmd = subparsers.add_parser(
        "report-catalog-import", help="Report Learning Core catalog import completeness from a manifest"
    )
    report_catalog_cmd.add_argument("--manifest", required=True)
    report_catalog_cmd.set_defaults(func=cmd_report_catalog_import)

    validate = subparsers.add_parser("validate", help="Validate project install folders")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    interfaces = subparsers.add_parser(
        "validate-interfaces", help="Validate curated reader-facing analytical interfaces"
    )
    interfaces.add_argument("--manifest")
    interfaces.add_argument("--path")
    interfaces.set_defaults(func=cmd_validate_interfaces)

    value_proof = subparsers.add_parser(
        "validate-value-proof", help="Validate a governed automation value-proof packet"
    )
    value_proof.add_argument("--path", required=True)
    value_proof.set_defaults(func=cmd_validate_value_proof)

    artifacts = subparsers.add_parser(
        "validate-artifacts", help="Validate curated artifact authority, provenance, mutability, and recovery contracts"
    )
    artifacts.add_argument("--manifest")
    artifacts.set_defaults(func=cmd_validate_artifacts)

    agency = subparsers.add_parser("validate-agency", help="Validate repository-anchored bounded-agency contracts")
    agency.add_argument("--manifest")
    agency.set_defaults(func=cmd_validate_agency)

    authority = subparsers.add_parser("validate-authority", help="Validate the Anyang AI CEO authority envelope")
    authority.add_argument("--manifest")
    authority.set_defaults(func=cmd_validate_authority)

    authority_preflight_cmd = subparsers.add_parser("authority-preflight", help="Report authority without granting it")
    authority_preflight_cmd.add_argument("--domain", required=True)
    authority_preflight_cmd.add_argument("--action", required=True)
    authority_preflight_cmd.add_argument("--manifest")
    authority_preflight_cmd.add_argument("--format", choices=("text", "json"), default="text")
    authority_preflight_cmd.set_defaults(func=cmd_authority_preflight)

    inventory = subparsers.add_parser("authority-inventory", help="Inventory role and authority drift without mutation")
    inventory.add_argument("--repo", default=".")
    inventory.add_argument("--format", choices=("text", "json"), default="text")
    inventory.set_defaults(func=cmd_authority_inventory)

    epistemics = subparsers.add_parser(
        "validate-epistemics", help="Validate curated claim state, provenance, dependency, and transition contracts"
    )
    epistemics.add_argument("--manifest")
    epistemics.add_argument("--format", choices=("text", "json"), default="text")
    epistemics.set_defaults(func=cmd_validate_epistemics)

    entropy = subparsers.add_parser(
        "epistemic-report", help="Report repository operational epistemic entropy"
    )
    entropy.add_argument("--manifest")
    entropy.add_argument("--retrieval-success", type=float)
    entropy.add_argument("--revision-impact-accuracy", type=float)
    entropy.set_defaults(func=cmd_epistemic_report)

    benchmark = subparsers.add_parser(
        "epistemic-benchmark", help="Score the fixed human epistemic-outcome cohort"
    )
    benchmark_sub = benchmark.add_subparsers(required=True)
    benchmark_score = benchmark_sub.add_parser("score", help="Score sanitized benchmark responses")
    benchmark_score.add_argument("--manifest")
    benchmark_score.add_argument("--responses", required=True)
    benchmark_score.add_argument("--format", choices=("markdown", "json"), default="markdown")
    benchmark_score.set_defaults(func=cmd_epistemic_benchmark_score)

    preflight = subparsers.add_parser("preflight", help="Reconstruct live state for a bounded operating phase")
    preflight.add_argument("--phase", required=True)
    preflight.add_argument("--manifest", required=True)
    preflight.add_argument("--format", choices=("text", "json"), default="text")
    preflight.set_defaults(func=cmd_preflight)

    harness = subparsers.add_parser("harness", help="Review the visible repository AI harness without source mutation")
    harness_sub = harness.add_subparsers(required=True)
    harness_scan = harness_sub.add_parser("scan", help="Create a tracked-file harness inventory and review template")
    harness_scan.add_argument("--repo", default=".")
    harness_scan.add_argument("--output")
    harness_scan.set_defaults(func=cmd_harness_scan)
    harness_render = harness_sub.add_parser("render", help="Validate a semantic review and render the reader packet")
    harness_render.add_argument("--packet", required=True)
    harness_render.add_argument("--review", required=True)
    harness_render.set_defaults(func=cmd_harness_render)
    harness_decide = harness_sub.add_parser("decide", help="Record explicit proposal approvals and rejections")
    harness_decide.add_argument("--packet", required=True)
    harness_decide.add_argument("--approve", nargs="*", type=int, default=[])
    harness_decide.add_argument("--reject", nargs="*", type=int, default=[])
    harness_decide.set_defaults(func=cmd_harness_decide)
    context_audit = subparsers.add_parser("context-audit", help="Run the read-only repository context-integrity audit")
    context_audit.add_argument("--repo", default=".")
    context_audit.add_argument("--format", choices=("markdown", "json"), default="markdown")
    context_audit.add_argument("--output")
    context_audit.set_defaults(func=cmd_context_audit)
    intake_validate = subparsers.add_parser("validate-singularity-intake", help="Validate a Singularity Science intake lane")
    intake_validate.add_argument("--lane", required=True)
    intake_validate.set_defaults(func=cmd_validate_singularity_intake)
    recurrence_validate = subparsers.add_parser("validate-recurrence-reviews", help="Validate derived Singularity recurrence packets")
    recurrence_validate.add_argument("--path", required=True)
    recurrence_validate.set_defaults(func=cmd_validate_recurrence_reviews)
    return parser


def cmd_new(args: argparse.Namespace) -> int:
    spec = load_project_input(args.input)
    files = build_project_files(spec)
    write_files(files, Path(args.output), force=args.force)
    print(f"Created project install scaffold: {args.output}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    spec = load_project_input(args.input)
    output = Path(args.output)
    if args.format == "markdown":
        files = build_project_files(spec)
        write_files(files, output, force=args.force)
    elif args.format == "obsidian":
        write_files(render_obsidian(spec), output, force=args.force)
    else:
        write_files({"index.html": render_html_dashboard(spec)}, output, force=args.force)
    print(f"Rendered {args.format} install output: {args.output}")
    return 0


def cmd_extract_patterns(args: argparse.Namespace) -> int:
    candidates = extract_patterns(args.projects_path)
    report = render_pattern_report(candidates)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote pattern candidate report: {args.output}")
    return 0


def cmd_import_transcripts(args: argparse.Namespace) -> int:
    preflight = run_preflight(TRANSCRIPT_PHASE, args.manifest)
    if preflight.exit_code:
        print(render_preflight_json(preflight) if args.format == "json" else render_preflight(preflight))
        return preflight.exit_code
    if args.dry_run:
        summary = preflight.summary
        if summary is None:
            return 1
        if args.format == "json":
            print(json.dumps({"preflight": preflight.as_dict(), "import": import_summary_dict(summary)}, indent=2, sort_keys=True))
        else:
            print(render_preflight(preflight))
            print()
            print(render_import_summary(summary))
        return 0

    before = preflight.snapshot
    summary = preflight.summary
    if summary is None:
        return 1
    summary.dry_run = False
    recover_import(summary)
    execute_import_plan(summary)
    summary.executed = True
    after = collect_repo_snapshot(before.root)
    transition = verify_transition(before, after, preflight.expected_writes)
    validation_results = validate_phase_result(preflight, summary, transition)
    validation_passed = all(result["status"] == "pass" for result in validation_results)
    handoff = {
        "status": "validated" if validation_passed and summary.complete else "blocked",
        "next_phase": preflight.phase.next_phase,
        "authority": "advisory-only; successor must run a new preflight",
    }
    if args.format == "json":
        print(json.dumps({"preflight": preflight.as_dict(), "import": import_summary_dict(summary), "transition": transition, "validation_results": validation_results, "handoff": handoff}, indent=2, sort_keys=True))
    else:
        print(render_import_summary(summary))
        print()
        print(f"Postflight delta: {transition['status']}")
        for path in transition["unexpected_delta"]:
            print(f"- BLOCK unexpected-delta: {path}")
        print(f"Phase validators: {'pass' if validation_passed else 'fail'}")
        for result in validation_results:
            print(f"- {result['status'].upper()} {result['code']}")
        print(f"Handoff: {handoff['status']} -> {handoff['next_phase']['owner']} ({handoff['authority']})")
    return 0 if validation_passed and summary.complete else 1


def cmd_report_transcript_import(args: argparse.Namespace) -> int:
    summary = import_transcripts(args.manifest, dry_run=True)
    print(render_completion_report(summary))
    return 0


def cmd_import_catalog(args: argparse.Namespace) -> int:
    summary = import_catalog(args.manifest, dry_run=args.dry_run)
    print(render_catalog_import_summary(summary))
    error_statuses = {"invalid-manifest", "missing-source"}
    return 1 if any(result.status in error_statuses for result in summary.results) else 0


def cmd_report_catalog_import(args: argparse.Namespace) -> int:
    summary = import_catalog(args.manifest, dry_run=True)
    print(render_catalog_completion_report(summary))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    results = validate_project_path(args.path)
    exit_code = 0
    for result in results:
        label = result.path.as_posix()
        if result.ok:
            print(f"OK {label}")
        else:
            print(f"CHECK {label}")
            exit_code = 1
        for warning in result.warnings:
            print(f"- WARNING: {warning}")
        for error in result.errors:
            print(f"- ERROR: {error}")
    return exit_code


def cmd_validate_interfaces(args: argparse.Namespace) -> int:
    diagnostics = validate_manifest(args.manifest, args.path)
    for diagnostic in diagnostics:
        print(f"ERROR {diagnostic.code} {diagnostic.path.as_posix()}: {diagnostic.message}")
    if diagnostics:
        return 1
    print("OK analytical interfaces")
    return 0


def cmd_validate_artifacts(args: argparse.Namespace) -> int:
    diagnostics = validate_artifact_manifest(args.manifest)
    for diagnostic in diagnostics:
        print(f"ERROR {diagnostic.code} {diagnostic.path.as_posix()}: {diagnostic.message}")
    if diagnostics:
        return 1
    print("OK artifact state contracts")
    return 0


def cmd_validate_agency(args: argparse.Namespace) -> int:
    diagnostics = validate_agency_manifest(args.manifest)
    for diagnostic in diagnostics:
        print(f"ERROR {diagnostic.code} {diagnostic.path.as_posix()}: {diagnostic.message}")
    if diagnostics:
        return 1
    print("OK bounded agency contracts")
    return 0


def cmd_validate_value_proof(args: argparse.Namespace) -> int:
    diagnostics = validate_value_proof(args.path)
    for diagnostic in diagnostics:
        location = f":{diagnostic.line}" if diagnostic.line else ""
        print(f"ERROR {diagnostic.code} {args.path}{location}: {diagnostic.message}")
    if diagnostics:
        return 1
    print("OK automation value proof")
    return 0


def cmd_validate_authority(args: argparse.Namespace) -> int:
    diagnostics = validate_authority_envelope(args.manifest)
    for diagnostic in diagnostics:
        print(f"ERROR {diagnostic.code} {diagnostic.path.as_posix()}: {diagnostic.message}")
    if diagnostics:
        return 1
    print("OK AI CEO authority envelope")
    return 0


def cmd_authority_preflight(args: argparse.Namespace) -> int:
    result = authority_preflight(args.domain, args.action, args.manifest)
    if args.format == "json":
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
    else:
        print(f"{result.status.upper()}: {result.domain}/{result.action}")
        print(f"- approver: {result.authority}")
        print(f"- approval required: {result.approval_required}")
        print(f"- enforcement: preflight reports; never grants authority")
        for blocker in result.blockers:
            print(f"- blocker: {blocker}")
    return 1 if result.status == "blocked" else 0


def cmd_authority_inventory(args: argparse.Namespace) -> int:
    print(render_inventory(inventory_authority(args.repo), args.format), end="")
    return 0


def cmd_validate_epistemics(args: argparse.Namespace) -> int:
    diagnostics = validate_epistemic_manifest(args.manifest)
    if args.format == "json":
        print(
            json.dumps(
                [
                    {"code": item.code, "path": str(item.path), "message": item.message, "critical": item.critical}
                    for item in diagnostics
                ],
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for diagnostic in diagnostics:
            severity = "CRITICAL" if diagnostic.critical else "ERROR"
            print(f"{severity} {diagnostic.code} {diagnostic.path.as_posix()}: {diagnostic.message}")
    if diagnostics:
        return 1
    if args.format == "text":
        print("OK epistemic state contracts")
    return 0


def cmd_epistemic_report(args: argparse.Namespace) -> int:
    report = epistemic_report(
        args.manifest,
        retrieval_success=args.retrieval_success,
        revision_impact_accuracy=args.revision_impact_accuracy,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["acceptance"]["zero_critical_gaps"] else 1


def cmd_epistemic_benchmark_score(args: argparse.Namespace) -> int:
    result = score_epistemic_benchmark(args.manifest, args.responses)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_epistemic_benchmark_markdown(result), end="")
    return 0 if result["acceptance"]["zero_critical_gaps"] else 1


def cmd_preflight(args: argparse.Namespace) -> int:
    preflight = run_preflight(args.phase, args.manifest)
    print(render_preflight_json(preflight) if args.format == "json" else render_preflight(preflight))
    return preflight.exit_code


def cmd_harness_scan(args: argparse.Namespace) -> int:
    packet = scan_harness(args.repo, args.output)
    print(f"Created harness review packet: {packet}")
    print(f"Semantic review template: {packet / '.harness-review' / 'semantic-review.template.json'}")
    return 0


def cmd_harness_render(args: argparse.Namespace) -> int:
    report = render_harness(args.packet, args.review)
    print(f"Rendered AI setup report: {report}")
    return 0


def cmd_harness_decide(args: argparse.Namespace) -> int:
    review = record_decisions(args.packet, args.approve, args.reject)
    print(f"Recorded proposal decisions: {review}")
    print("No source changes were applied; v1 has no apply command.")
    return 0


def cmd_context_audit(args: argparse.Namespace) -> int:
    report = audit_repository(args.repo)
    rendered = json.dumps(report, indent=2, sort_keys=True) if args.format == "json" else render_markdown(report)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Wrote context audit: {output}")
    else:
        print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


def cmd_validate_singularity_intake(args: argparse.Namespace) -> int:
    diagnostics = validate_lane(args.lane)
    for diagnostic in diagnostics:
        print(f"{diagnostic.severity.upper()} {diagnostic.code} {diagnostic.path}: {diagnostic.message}")
    if diagnostics:
        return 1
    print(f"OK Singularity intake lane: {args.lane}")
    return 0


def cmd_validate_recurrence_reviews(args: argparse.Namespace) -> int:
    diagnostics = validate_directory(args.path)
    for diagnostic in diagnostics:
        print(f"{diagnostic.severity.upper()} {diagnostic.code} {diagnostic.path}: {diagnostic.message}")
    if diagnostics:
        return 1
    print(f"OK recurrence review packets: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
