#!/usr/bin/env python3
"""Check whether tagged scenario records survive a filtering pipeline.

Given two CSV/JSONL files - one before filtering and one after - report
how many records carrying a given tag are preserved. Useful when you want
to know if your detector pipeline is dropping the records you care about.

No network activity. Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
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


def record_key(row: dict, fields: list[str]) -> tuple:
    return tuple(str(row.get(f, "")) for f in fields)


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    fail_closed_on_live_args(argv)

    parser = argparse.ArgumentParser(
        description="Check tag preservation across a filtering step."
    )
    parser.add_argument("--before", required=True, help="records before filtering")
    parser.add_argument("--after", required=True, help="records after filtering")
    parser.add_argument(
        "--tag", required=True, help="tag value to track preservation for"
    )
    parser.add_argument(
        "--key",
        default="ts,src,dst,asdu_type,ioa",
        help="comma-separated fields used as identity key",
    )
    args = parser.parse_args(argv)

    fields = [f.strip() for f in args.key.split(",") if f.strip()]
    before = read_records(Path(args.before))
    after = read_records(Path(args.after))

    before_tagged = [r for r in before if r.get("tag") == args.tag]
    after_keys = {record_key(r, fields) for r in after}

    preserved = sum(1 for r in before_tagged if record_key(r, fields) in after_keys)
    total = len(before_tagged)
    rate = (preserved / total) if total else 0.0

    print(f"tag {args.tag}")
    print(f"before {total}")
    print(f"after_preserved {preserved}")
    print(f"rate {rate:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
