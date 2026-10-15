#!/usr/bin/env python3
"""Read-only quality audit for JSONL datasets (stdlib only).

Usage:
  python3 -I audit_jsonl.py DATA.jsonl --text-field text [--label-field label]
      [--require id,text,label] [--compare OTHER.jsonl]

Reports: parse errors, missing/empty required fields, exact duplicates after
normalisation (lowercase, collapsed whitespace), label distribution, text length
outliers, and exact-duplicate overlap with a second file (e.g. train vs test).
It never modifies files and prints counts and row numbers, not full texts.
"""
import argparse
import collections
import hashlib
import json
import re
import statistics
import sys


def norm(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())


def digest(s):
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()


def load(path):
    rows, errors = [], []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                errors.append(n)
                continue
            if not isinstance(obj, dict):
                errors.append(n)
                continue
            rows.append((n, obj))
    return rows, errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path")
    ap.add_argument("--text-field", required=True)
    ap.add_argument("--label-field")
    ap.add_argument("--require", default="")
    ap.add_argument("--compare")
    a = ap.parse_args(argv)

    rows, errors = load(a.path)
    print(f"rows={len(rows)} parse_errors={len(errors)} first_error_lines={errors[:5]}")

    required = [f for f in a.require.split(",") if f] or [a.text_field]
    for f in required:
        missing = [n for n, o in rows if o.get(f) in (None, "", [])]
        print(f"required field {f!r}: missing_or_empty={len(missing)} first_rows={missing[:5]}")

    seen = collections.defaultdict(list)
    for n, o in rows:
        t = o.get(a.text_field)
        if isinstance(t, str) and t.strip():
            seen[digest(t)].append(n)
    dup_groups = [v for v in seen.values() if len(v) > 1]
    dup_rows = sum(len(v) - 1 for v in dup_groups)
    print(f"exact duplicate groups={len(dup_groups)} redundant_rows={dup_rows}")

    if a.label_field:
        labels = collections.Counter(str(o.get(a.label_field)) for _, o in rows)
        print("label distribution:", dict(labels.most_common()))
        conflicts = 0
        by_text = collections.defaultdict(set)
        for _, o in rows:
            t = o.get(a.text_field)
            if isinstance(t, str) and t.strip():
                by_text[digest(t)].add(str(o.get(a.label_field)))
        conflicts = sum(1 for v in by_text.values() if len(v) > 1)
        print(f"identical texts with conflicting labels={conflicts}")

    lengths = [len(o[a.text_field]) for _, o in rows if isinstance(o.get(a.text_field), str)]
    if len(lengths) >= 2:
        mean, sd = statistics.mean(lengths), statistics.pstdev(lengths)
        outliers = [n for n, o in rows
                    if isinstance(o.get(a.text_field), str)
                    and sd > 0 and abs(len(o[a.text_field]) - mean) > 4 * sd]
        print(f"text length mean={mean:.1f} sd={sd:.1f} min={min(lengths)} max={max(lengths)} "
              f"outliers_4sd={len(outliers)} first_rows={outliers[:5]}")

    if a.compare:
        other, other_err = load(a.compare)
        other_hashes = {digest(o[a.text_field]) for _, o in other
                        if isinstance(o.get(a.text_field), str) and o[a.text_field].strip()}
        leaked = sorted({n for h, ns in seen.items() if h in other_hashes for n in ns})
        print(f"compare parse_errors={len(other_err)} exact_overlap_rows={len(leaked)} first_rows={leaked[:5]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
