"""Command-line interface for Sosmed Scanner."""

import argparse
import json
import sys
from dataclasses import asdict
from typing import List, Optional, Sequence

from sosmed_scanner.scanner import PLATFORMS, ScanResult, scan_username


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sosmed_scanner",
        description="Check whether a username exists on public profile pages.",
    )
    parser.add_argument("username", help="Username to look up")
    parser.add_argument(
        "-p",
        "--platform",
        action="append",
        help="Limit the scan to a platform (repeatable). Available: "
        + ", ".join(PLATFORMS),
    )
    parser.add_argument(
        "--json", action="store_true", help="Print results as JSON"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Seconds to wait between requests (default: 0.5)",
    )
    return parser


def format_results(results: List[ScanResult]) -> str:
    """Render results as aligned plain text."""
    lines = []
    for item in results:
        line = f"{item.platform:<10} {item.status:<10} {item.url}"
        if item.detail:
            line += f"  ({item.detail})"
        lines.append(line)
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the CLI and return an exit code (0 ok, 2 invalid input)."""
    args = build_parser().parse_args(argv)
    try:
        results = scan_username(
            args.username, platforms=args.platform, delay=args.delay
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(item) for item in results], indent=2))
    else:
        print(format_results(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())