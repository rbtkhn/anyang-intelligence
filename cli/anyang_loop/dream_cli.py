from __future__ import annotations

import argparse
import sys

from .dream import build_dream_data, render_dream_json, render_dream_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="anyang-dream", description="Native Anyang Intelligence dream closeout brief")
    parser.add_argument("--repo", default=".", help="Path to the operating-substrate root. Defaults to the current directory.")
    parser.add_argument("--db", help="External cadence SQLite database; required for --record unless ANYANG_DATA_DIR is set.")
    parser.add_argument("--verify", choices=("fast", "full", "none"), default="fast")
    parser.add_argument("--record", action="store_true", help="Explicitly record a sanitized handoff in external SQLite.")
    parser.add_argument("--recorded-by", default="operator")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        data = build_dream_data(
            args.repo,
            db_path=args.db,
            verify=args.verify,
            record=args.record,
            recorded_by=args.recorded_by,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    output = render_dream_json(data) if args.format == "json" else render_dream_text(data) + "\n"
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
