from __future__ import annotations

import argparse
import sys

from .coffee import build_coffee_data, render_coffee_json, render_coffee_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="anyang-coffee", description="Native Anyang Intelligence coffee re-entry brief")
    parser.add_argument("--repo", default=".", help="Path to the operating-substrate root. Defaults to the current directory.")
    parser.add_argument("--db", help="Optional external cadence SQLite database.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        data = build_coffee_data(args.repo, args.db)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    output = render_coffee_json(data) if args.format == "json" else render_coffee_text(data) + "\n"
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
