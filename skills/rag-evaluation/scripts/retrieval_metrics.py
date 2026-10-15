#!/usr/bin/env python3
"""Retrieval metrics for RAG evaluation (stdlib only).

Input JSONL, one query per line:
  {"query_id": "q1", "relevant": {"d1": 1, "d7": 2}, "retrieved": ["d3", "d1", "d9"]}
`relevant` maps doc id -> graded relevance (>0 is relevant); a list of ids is
also accepted and treated as binary relevance 1.

Usage: python3 -I retrieval_metrics.py runs.jsonl --k 5 10

Prints macro-averaged Recall@k, Precision@k, HitRate@k, MRR, and nDCG@k
(linear gain: rel_i / log2(i + 1), positions 1-based), plus the query count and
the number of queries with no relevant document (excluded from averages).
"""
import argparse
import json
import math
import sys


def as_grades(rel):
    if isinstance(rel, dict):
        return {str(k): float(v) for k, v in rel.items() if float(v) > 0}
    return {str(k): 1.0 for k in rel}


def recall_at_k(grades, retrieved, k):
    hits = len({d for d in retrieved[:k] if d in grades})
    return hits / len(grades)


def precision_at_k(grades, retrieved, k):
    # distinct relevant ids in the top k (duplicates count once), divided by k
    return len({d for d in retrieved[:k] if d in grades}) / k


def hit_at_k(grades, retrieved, k):
    return 1.0 if any(d in grades for d in retrieved[:k]) else 0.0


def mrr(grades, retrieved):
    for i, d in enumerate(retrieved, 1):
        if d in grades:
            return 1.0 / i
    return 0.0


def dcg(gains):
    return sum(g / math.log2(i + 1) for i, g in enumerate(gains, 1))


def ndcg_at_k(grades, retrieved, k):
    seen, gains = set(), []
    for d in retrieved[:k]:
        gains.append(grades.get(d, 0.0) if d not in seen else 0.0)
        seen.add(d)
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = dcg(ideal)
    return dcg(gains) / idcg if idcg > 0 else 0.0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--k", type=int, nargs="+", default=[5, 10])
    a = ap.parse_args(argv)

    rows, skipped = [], 0
    with open(a.path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            o = json.loads(line)
            g = as_grades(o.get("relevant", {}))
            if not g:
                skipped += 1
                continue
            rows.append((g, [str(x) for x in o.get("retrieved", [])]))
    n = len(rows)
    print(f"queries={n} skipped_no_relevant={skipped}")
    if not n:
        return 1
    for k in a.k:
        m = {
            "recall": sum(recall_at_k(g, r, k) for g, r in rows) / n,
            "precision": sum(precision_at_k(g, r, k) for g, r in rows) / n,
            "hit_rate": sum(hit_at_k(g, r, k) for g, r in rows) / n,
            "ndcg": sum(ndcg_at_k(g, r, k) for g, r in rows) / n,
        }
        print(f"k={k} " + " ".join(f"{name}@{k}={val:.4f}" for name, val in m.items()))
    print(f"mrr={sum(mrr(g, r) for g, r in rows) / n:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
