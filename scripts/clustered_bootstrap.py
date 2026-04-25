#!/usr/bin/env python3
"""Small clustered bootstrap helper.

Reads a CSV with a numeric value column and a cluster id column, resamples
clusters with replacement, and prints the bootstrap mean and percentile
confidence interval. No network activity.
"""
from __future__ import annotations

import argparse
import csv
import random
import statistics
import sys
from collections import defaultdict
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


def percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return float("nan")
    if q <= 0:
        return sorted_values[0]
    if q >= 1:
        return sorted_values[-1]
    pos = q * (len(sorted_values) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    fail_closed_on_live_args(argv)

    parser = argparse.ArgumentParser(
        description="Clustered bootstrap mean and percentile CI."
    )
    parser.add_argument("input", help="csv with cluster and value columns")
    parser.add_argument("--cluster-col", default="cluster")
    parser.add_argument("--value-col", default="value")
    parser.add_argument("--iters", type=int, default=2000)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    rng = random.Random(args.seed)

    clusters: dict[str, list[float]] = defaultdict(list)
    with Path(args.input).open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                v = float(row[args.value_col])
            except (KeyError, ValueError):
                continue
            cid = row.get(args.cluster_col, "")
            clusters[cid].append(v)

    cluster_ids = list(clusters.keys())
    if not cluster_ids:
        print("no clusters found", file=sys.stderr)
        return 1

    means: list[float] = []
    n = len(cluster_ids)
    for _ in range(args.iters):
        sample_values: list[float] = []
        for _ in range(n):
            cid = rng.choice(cluster_ids)
            sample_values.extend(clusters[cid])
        if sample_values:
            means.append(statistics.fmean(sample_values))

    means.sort()
    point = statistics.fmean(means) if means else float("nan")
    lo = percentile(means, args.alpha / 2)
    hi = percentile(means, 1 - args.alpha / 2)

    print(f"clusters {n}")
    print(f"iters {args.iters}")
    print(f"mean {point:.6f}")
    print(f"ci_low {lo:.6f}")
    print(f"ci_high {hi:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
