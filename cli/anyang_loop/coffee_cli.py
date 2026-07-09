from __future__ import annotations

import argparse

from .coffee import build_coffee_brief


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="anyang-coffee", description="Native Anyang Intelligence coffee re-entry brief")
    parser.add_argument("--repo", default=".", help="Path to the operating-substrate root. Defaults to the current directory.")
    args = parser.parse_args(argv)
    print(build_coffee_brief(args.repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
