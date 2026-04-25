#!/usr/bin/env python3
"""Count raw and grouped queue volume for a CSV/JSONL of toy Zeek-like records.

Reads a file of records and prints:
  - total raw count
  - count per (src, dst)
  - count per asdu_type

No network activity. Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

LIVE_FORBIDDEN = {"--host", "--ip", "--target", "--port", "--connect", "--send"}


def fail_closed_on_live_args(argv: list[str]) -> None:
    bad = [a for a in argv if a.split("=", 1)[0] in LIVE_FORBIDDEN]
    if bad:
        print(
            "refusing to run: live target arguments are not supported "
            f"({', '.join(bad)})",
            file=sys.stderr,
        )
        sys.exit(2)


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"input not found: {path}")
    ext = path.suffix.lower()
    if ext == ".csv":
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    if ext in (".jsonl", ".ndjson"):
        out = []
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out
    raise SystemExit(f"unsupported input extension: {ext}")


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    fail_closed_on_live_args(argv)

    parser = argparse.ArgumentParser(
        description="Count raw and grouped queue volume for toy IEC-104 records."
    )
    parser.add_argument("input", help="csv or jsonl file of records")
    parser.add_argument(
        "--top", type=int, default=10, help="how many groups to print per axis"
    )
    args = parser.parse_args(argv)

    rows = read_records(Path(args.input))
    print(f"raw_count {len(rows)}")

    pair_counts = Counter((r.get("src", ""), r.get("dst", "")) for r in rows)
    type_counts = Counter(r.get("asdu_type", "") for r in rows)

    print("# top peer pairs")
    for (s, d), n in pair_counts.most_common(args.top):
        print(f"pair {s} -> {d} {n}")

    print("# top asdu types")
    for t, n in type_counts.most_common(args.top):
        print(f"asdu_type {t} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
