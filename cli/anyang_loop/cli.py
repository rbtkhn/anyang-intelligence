from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .builtins import all_builtins, get_builtin
from .lint import has_errors, validate_loop
from .model import LoopDefinition
from .parser import LoopParseError, load_loop_file, load_loops_from_path
from .render import render_loop, template_loop
from .simulate import simulate_loop


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anyang-loop", description="Anyang Intelligence Loop Grammar Engine")
    subparsers = parser.add_subparsers(required=True)

    validate = subparsers.add_parser("validate", help="Validate loop definitions in a file or directory")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    new = subparsers.add_parser("new", help="Create a starter loop template")
    new.add_argument("name")
    new.add_argument("--format", choices=("yaml", "markdown"), default="yaml")
    new.add_argument("--type", choices=("operating", "governance", "learning", "recursive"), default="operating")
    new.add_argument("--output")
    new.set_defaults(func=cmd_new)

    list_cmd = subparsers.add_parser("list", help="List loop definitions")
    list_cmd.add_argument("path", nargs="?")
    list_cmd.add_argument("--include-builtins", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    simulate = subparsers.add_parser("simulate", help="Simulate one loop cycle")
    simulate.add_argument("target")
    simulate.set_defaults(func=cmd_simulate)

    export = subparsers.add_parser("export", help="Export a loop definition")
    export.add_argument("target")
    export.add_argument("--format", choices=("markdown", "obsidian", "json"), required=True)
    export.add_argument("--output")
    export.set_defaults(func=cmd_export)
    return parser


def cmd_validate(args: argparse.Namespace) -> int:
    loops, parse_errors = load_loops_from_path(args.path)
    exit_code = 0
    for path, message in parse_errors:
        print(f"ERROR {path}: {message}")
        exit_code = 1
    if not loops and not parse_errors:
        print("No loop definitions found.")
        return 1
    for loop in loops:
        diagnostics = validate_loop(loop)
        print_validation(loop, diagnostics)
        if has_errors(diagnostics):
            exit_code = 1
    return exit_code


def cmd_new(args: argparse.Namespace) -> int:
    loop = template_loop(args.name, args.type)
    output = render_loop(loop, "yaml" if args.format == "yaml" else "markdown")
    write_or_print(output, args.output)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    loops: list[LoopDefinition] = []
    errors: list[tuple[Path, str]] = []
    if args.path:
        loops, errors = load_loops_from_path(args.path)
    if args.include_builtins:
        loops.extend(all_builtins())
    for path, message in errors:
        print(f"ERROR {path}: {message}", file=sys.stderr)
    if not loops:
        print("No loop definitions found.")
        return 1
    print("Name\tType\tCadence\tAuthority\tStatus")
    for loop in loops:
        diagnostics = validate_loop(loop)
        status = "invalid" if has_errors(diagnostics) else ("warnings" if diagnostics else "ok")
        print(f"{loop.name}\t{loop.loop_type}\t{loop.cadence}\t{loop.authority}\t{status}")
    return 1 if errors else 0


def cmd_simulate(args: argparse.Namespace) -> int:
    loop = load_target(args.target)
    print(simulate_loop(loop), end="")
    return 1 if has_errors(validate_loop(loop)) else 0


def cmd_export(args: argparse.Namespace) -> int:
    loop = load_target(args.target)
    diagnostics = validate_loop(loop)
    if has_errors(diagnostics):
        print_validation(loop, diagnostics)
        return 1
    output = render_loop(loop, args.format)
    write_or_print(output, args.output)
    return 0


def load_target(target: str) -> LoopDefinition:
    builtin = get_builtin(target)
    if builtin:
        return builtin
    try:
        return load_loop_file(target)
    except LoopParseError as exc:
        raise SystemExit(f"ERROR {target}: {exc}") from exc


def print_validation(loop: LoopDefinition, diagnostics: list) -> None:
    location = f" ({loop.source_path})" if loop.source_path else ""
    if not diagnostics:
        print(f"OK {loop.name}{location}")
        return
    print(f"CHECK {loop.name}{location}")
    for item in diagnostics:
        print(f"- {item.level.upper()} {item.code}: {item.message}")


def write_or_print(output: str, output_path: str | None) -> None:
    if output_path:
        Path(output_path).write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    raise SystemExit(main())

