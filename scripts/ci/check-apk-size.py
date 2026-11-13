#!/usr/bin/env python3
"""Fail CI when the shipping APK exceeds a size budget (default 100 MiB)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MIB = 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path, help="Path to the .apk file")
    parser.add_argument(
        "--max-mib",
        type=float,
        default=100.0,
        help="Maximum allowed size in mebibytes (default: 100)",
    )
    args = parser.parse_args()
    apk: Path = args.apk
    if not apk.is_file():
        print(f"::error::APK not found: {apk}", file=sys.stderr)
        return 1

    size = apk.stat().st_size
    mib = size / MIB
    limit = int(args.max_mib * MIB)
    print(f"APK size: {mib:.2f} MiB ({size:,} bytes); limit {args.max_mib:.0f} MiB")

    if size > limit:
        print(
            f"::error::APK is {mib:.2f} MiB, above the {args.max_mib:.0f} MiB limit",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
