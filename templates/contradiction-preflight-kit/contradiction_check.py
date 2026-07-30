"""Standalone CLI adapter for the contradiction-preflight kernel."""

from __future__ import annotations

import argparse

from contradiction_kernel import (
    ContradictionPacketError,
    evaluate_contradictions,
    load_contradiction_packet,
    render_contradiction_json,
    render_contradiction_markdown,
)
from host_policy import HOST_POLICY, scan_packet_privacy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="contradiction-check")
    parser.add_argument("--packet", required=True)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    args = parser.parse_args(argv)
    try:
        result = evaluate_contradictions(
            load_contradiction_packet(args.packet),
            policy=HOST_POLICY,
            privacy_scanner=scan_packet_privacy,
        )
    except ContradictionPacketError as exc:
        print(f"ERROR: {exc}")
        return 1
    rendered = (
        render_contradiction_json(result)
        if args.format == "json"
        else render_contradiction_markdown(result)
    )
    print(rendered, end="")
    return 0 if result["disposition"] in {"continue", "continue-provisional"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
