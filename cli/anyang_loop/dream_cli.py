from __future__ import annotations

import argparse

from .dream import build_dream_brief


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="anyang-dream", description="Native Anyang Intelligence dream closeout brief")
    parser.add_argument("--repo", default=".", help="Path to the repo_probe root. Defaults to the current directory.")
    args = parser.parse_args(argv)
    print(build_dream_brief(args.repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
