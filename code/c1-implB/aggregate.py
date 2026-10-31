#!/usr/bin/env python3
"""Aggregate chunk JSONs from the C engine: check contiguous coverage,
sum timing/statistics, merge candidates and near-misses."""
import json, glob, sys

def main():
    paths = sorted(glob.glob("outputs/chunk_*.json"))
    chunks = []
    for p in paths:
        with open(p) as f:
            chunks.append(json.load(f))
    chunks.sort(key=lambda c: c["b_lo"])
    cov_ok = True
    expect = 1
    for c in chunks:
        if c["b_lo"] != expect:
            cov_ok = False
        expect = c["b_hi"] + 1
    stats = {}
    for c in chunks:
        for k, v in c["stats"].items():
            stats[k] = stats.get(k, 0) + v
    cand = sorted({(x["a"], x["b"], x["t"]) for c in chunks for x in c["singleton_candidates"]})
    nms = sorted({(x["a"], x["b"], x["c"]) for c in chunks for x in c["l2_nearmisses"]})
    out = {
        "n_chunks": len(chunks),
        "coverage_ok": cov_ok,
        "coverage_b_max": expect - 1,
        "total_seconds_sum_of_chunks": sum(c["seconds"] for c in chunks),
        "per_chunk_seconds": {f"{c['b_lo']}-{c['b_hi']}": c["seconds"] for c in chunks},
        "stats": stats,
        "expected_intervals": (expect - 1) * expect // 2,
        "singleton_candidates": [{"a": a, "b": b, "t": t} for a, b, t in cand],
        "l2_nearmisses": [{"a": a, "b": b, "c": c} for a, b, c in nms],
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
