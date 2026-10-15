#!/usr/bin/env python3
"""Paired bootstrap for comparing two systems on the same eval items (stdlib only).

Input: JSONL with {"id": ..., "a": 0/1 or float score, "b": 0/1 or float score}.
Usage: python3 -I paired_bootstrap.py scores.jsonl [--iters 10000] [--seed 0]
Prints mean(a), mean(b), mean difference (b - a), a 95% percentile bootstrap CI
of the difference, and the share of resamples where b > a.
Pairing matters: both systems are scored on identical items, so resample items,
not scores independently.
"""
import argparse
import json
import random
import sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--iters", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)

    diffs, sa, sb = [], 0.0, 0.0
    with open(a.path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                o = json.loads(line)
                diffs.append(float(o["b"]) - float(o["a"]))
                sa += float(o["a"])
                sb += float(o["b"])
    n = len(diffs)
    if n < 2:
        print("need at least 2 items")
        return 1
    rng = random.Random(a.seed)
    means = []
    for _ in range(a.iters):
        means.append(sum(diffs[rng.randrange(n)] for _ in range(n)) / n)
    means.sort()
    lo, hi = means[int(0.025 * a.iters)], means[int(0.975 * a.iters) - 1]
    better = sum(1 for m in means if m > 0) / a.iters
    print(f"n={n} mean_a={sa / n:.4f} mean_b={sb / n:.4f} diff={sum(diffs) / n:.4f} "
          f"ci95=[{lo:.4f}, {hi:.4f}] p(b>a)={better:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
