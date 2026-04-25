#!/usr/bin/env python3
"""Merge synthetic scenario records into a toy Zeek-like log.

Inputs are CSV or JSONL files. The script does not open sockets, does not
reach out to any host, and refuses to run if anything that looks like a live
target parameter is passed.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

LIVE_FORBIDDEN = {"--host", "--ip", "--target", "--port", "--connect", "--send"}

EXPECTED_FIELDS = (
    "ts",
    "src",
    "dst",
    "asdu_type",
    "cot",
    "ioa",
    "tag",
)


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


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(EXPECTED_FIELDS)
    for row in rows:
        for k in row.keys():
            if k not in fields:
                fields.append(k)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def merge(base: list[dict], scenario: list[dict], tag: str) -> list[dict]:
    tagged = []
    for row in scenario:
        new_row = dict(row)
        new_row.setdefault("tag", tag)
        tagged.append(new_row)
    combined = list(base) + tagged
    combined.sort(key=lambda r: float(r.get("ts", 0) or 0))
    return combined


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    fail_closed_on_live_args(argv)

    parser = argparse.ArgumentParser(
        description="Merge a synthetic scenario file into a toy Zeek-like log."
    )
    parser.add_argument("--base", required=True, help="base records file (csv/jsonl)")
    parser.add_argument(
        "--scenario", required=True, help="scenario records file (csv/jsonl)"
    )
    parser.add_argument(
        "--tag", default="scenario", help="tag value to attach to scenario rows"
    )
    parser.add_argument("--out", required=True, help="output csv path")
    args = parser.parse_args(argv)

    base = read_records(Path(args.base))
    scenario = read_records(Path(args.scenario))
    merged = merge(base, scenario, args.tag)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(out_path, merged)
    print(f"wrote {len(merged)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
