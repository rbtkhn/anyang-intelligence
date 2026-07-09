from __future__ import annotations

import argparse
from pathlib import Path

from .install_model import InstallInputError, load_install_input
from .install_render import build_customer_files, render_html_dashboard, render_obsidian, write_files
from .install_validate import validate_install_path
from .membrane import extract_patterns, render_pattern_report
from .catalog_import import (
    CatalogImportError,
    import_catalog,
    render_catalog_completion_report,
    render_catalog_import_summary,
)
from .transcript_import import (
    TranscriptImportError,
    import_transcripts,
    render_completion_report,
    render_import_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except InstallInputError as exc:
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anyang-install", description="Anyang Intelligence customer installer generator")
    subparsers = parser.add_subparsers(required=True)

    new = subparsers.add_parser("new", help="Scaffold a customer install folder")
    new.add_argument("input")
    new.add_argument("--output", required=True)
    new.add_argument("--force", action="store_true")
    new.set_defaults(func=cmd_new)

    render = subparsers.add_parser("render", help="Render install files without requiring customer placement")
    render.add_argument("input")
    render.add_argument("--format", choices=("markdown", "obsidian", "html"), required=True)
    render.add_argument("--output", required=True)
    render.add_argument("--force", action="store_true")
    render.set_defaults(func=cmd_render)

    extract = subparsers.add_parser("extract-patterns", help="Extract membrane-aware cross-customer pattern candidates")
    extract.add_argument("customers_path")
    extract.add_argument("--output", required=True)
    extract.set_defaults(func=cmd_extract_patterns)

    import_cmd = subparsers.add_parser(
        "import-transcripts", help="Import Singularity Science transcripts from a manifest into the archive"
    )
    import_cmd.add_argument("--manifest", required=True)
    import_cmd.add_argument("--dry-run", action="store_true")
    import_cmd.set_defaults(func=cmd_import_transcripts)

    report_cmd = subparsers.add_parser(
        "report-transcript-import", help="Report transcript import completeness from a Singularity Science manifest"
    )
    report_cmd.add_argument("--manifest", required=True)
    report_cmd.set_defaults(func=cmd_report_transcript_import)

    import_catalog_cmd = subparsers.add_parser(
        "import-catalog", help="Import Elementary School catalog entries from a manifest into the catalog area"
    )
    import_catalog_cmd.add_argument("--manifest", required=True)
    import_catalog_cmd.add_argument("--dry-run", action="store_true")
    import_catalog_cmd.set_defaults(func=cmd_import_catalog)

    report_catalog_cmd = subparsers.add_parser(
        "report-catalog-import", help="Report Elementary School catalog import completeness from a manifest"
    )
    report_catalog_cmd.add_argument("--manifest", required=True)
    report_catalog_cmd.set_defaults(func=cmd_report_catalog_import)

    validate = subparsers.add_parser("validate", help="Validate customer install folders")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)
    return parser


def cmd_new(args: argparse.Namespace) -> int:
    spec = load_install_input(args.input)
    files = build_customer_files(spec)
    write_files(files, Path(args.output), force=args.force)
    print(f"Created customer install scaffold: {args.output}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    spec = load_install_input(args.input)
    output = Path(args.output)
    if args.format == "markdown":
        files = build_customer_files(spec)
        write_files(files, output, force=args.force)
    elif args.format == "obsidian":
        write_files(render_obsidian(spec), output, force=args.force)
    else:
        write_files({"index.html": render_html_dashboard(spec)}, output, force=args.force)
    print(f"Rendered {args.format} install output: {args.output}")
    return 0


def cmd_extract_patterns(args: argparse.Namespace) -> int:
    candidates = extract_patterns(args.customers_path)
    report = render_pattern_report(candidates)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote pattern candidate report: {args.output}")
    return 0


def cmd_import_transcripts(args: argparse.Namespace) -> int:
    summary = import_transcripts(args.manifest, dry_run=args.dry_run)
    print(render_import_summary(summary))
    error_statuses = {"invalid-manifest", "missing-source"}
    return 1 if any(result.status in error_statuses for result in summary.results) else 0


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
    results = validate_install_path(args.path)
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


if __name__ == "__main__":
    raise SystemExit(main())
