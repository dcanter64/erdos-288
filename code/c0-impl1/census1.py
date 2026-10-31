#!/usr/bin/env python3
"""
Erdos Problem #288 -- Cluster C0, Implementation 1 (Cycle 1).

Exact census, no floating point in any decision.

Problem
-------
H(a, b) = sum_{n=a}^{b} 1/n, written in lowest terms as A/B (A, B > 0).

(i)/(ii) Singleton case: H(a, b) + 1/m in Z for some m >= 1.
    H(a, b) + 1/m integral with m = B is equivalent to B | (A + 1),
    i.e. A = -1 (mod B); denominator forcing then says this B is the
    *only* possible m, so testing A % B == B - 1 is exhaustive.
    The solution is disjoint (singleton outside [a, b]) iff m = B > b.

(iii) L = 2 disjoint branch: intervals [a, b] and [c, c+1] with b < c and
    H(a, b) + H(c, c+1) in Z, exhaustively for 1 <= a <= b <= 2000 and
    *all* c > b (c itself is not bounded).

Method (mandated)
-----------------
* Precompute the harmonic numbers H_n = sum_{k=1}^{n} 1/k exactly as
  fractions.Fraction values.
* For every pair (a, b), obtain H(a, b) = H_b - H_{a-1} exactly (Fraction
  subtraction returns the value already reduced to lowest terms), read
  off A = numerator, B = denominator, and test the condition above.

Method for the L = 2 branch (exact quadratic, no scanning over c)
-----------------------------------------------------------------
Fix (a, b) and write f = H(a, b) = A/B in lowest terms.
For c > b >= 1 we have c >= 2, and H(c, c+1) = 1/c + 1/(c+1) is strictly
decreasing in c, so

    0 < H(c, c+1) <= H(b+1, b+2) = 1/(b+1) + 1/(b+2) < 1.

Hence if f + H(c, c+1) = k is an integer, then t := k - f lies in (0, 1).
Therefore:
  * if f is an integer (A % B == 0), no such c exists;
  * otherwise k = floor(f) + 1 is the *only* possible integer, and
    t = (B - (A % B)) / B.  Write p = B - (A % B) (so t = p/B, unreduced
    is fine: scaling p and B by a common factor scales the discriminant
    and the root formula below by the same factor).
Also t must satisfy the exact bound t <= 1/(b+1) + 1/(b+2); pairs failing
that bound are discarded by an exact integer comparison.

For a candidate t = p/B the equation t = (2c+1) / (c(c+1)) is

    p c^2 + (p - 2B) c - B = 0,

whose discriminant is

    D = (p - 2B)^2 + 4 p B = p^2 + 4 B^2.

So a solution exists iff D is a perfect square (tested with the exact
integer square root, math.isqrt) and

    c = (2B - p + sqrt(D)) / (2p)

is a positive integer > b.  Every recorded L = 2 hit is additionally
re-verified by a direct exact Fraction computation of
H(a, b) + 1/c + 1/(c+1) before it is written out.  Because c is obtained
from the quadratic rather than by scanning, c of any size is covered.

Checkpointing
-------------
Work is split into chunks of b-values.  Each finished chunk is written
atomically to outputs/chunk_<lo>_<hi>.json (write to a .tmp file, then
os.replace).  On a rerun, chunks whose files exist and pass a sanity
check (matching b-range and pair count) are skipped and their recorded
results are reused, so an interrupted run resumes where it stopped.

Outputs (in outputs/)
---------------------
chunk_*.json                 per-chunk raw results (the checkpoints)
singleton_solutions.json     all singleton solutions with b <= max_b
l2_solutions.json            all L = 2 disjoint solutions with b <= max_b
summary.json                 coverage counts, timings, sub-census b <= 1600

Usage
-----
    python3 census1.py [--max-b 2000] [--chunk 100]
"""

import argparse
import json
import os
import time
from fractions import Fraction
from math import isqrt


def harmonic_numbers(max_b):
    """Exact H_n for n = 0..max_b as a list of Fractions (H_0 = 0)."""
    h = [Fraction(0, 1)]
    for n in range(1, max_b + 1):
        h.append(h[-1] + Fraction(1, n))
    return h


def examine_chunk(h, b_lo, b_hi):
    """Examine every (a, b) with b_lo <= b <= b_hi and 1 <= a <= b.

    Returns (singleton_solutions, l2_solutions, pairs_checked).
    Pure exact integer / Fraction arithmetic throughout.
    """
    singleton = []
    l2 = []
    pairs = 0
    for b in range(b_lo, b_hi + 1):
        h_b = h[b]
        # Exact upper bound for H(c, c+1) when c > b, as a Fraction
        # comparison done below in integer form:
        #   t <= 1/(b+1) + 1/(b+2) = (2b+3) / ((b+1)(b+2)).
        bound_num = 2 * b + 3
        bound_den = (b + 1) * (b + 2)
        for a in range(1, b + 1):
            f = h_b - h[a - 1]          # exact, already in lowest terms
            A = f.numerator
            B = f.denominator
            pairs += 1

            # ---- singleton branch -------------------------------------
            # B | (A + 1)  <=>  A % B == B - 1 (also correct for B == 1:
            # A % 1 == 0 == B - 1).
            if A % B == B - 1:
                singleton.append(
                    {"a": a, "b": b, "m": B, "disjoint": B > b}
                )

            # ---- L = 2 disjoint branch --------------------------------
            r = A % B
            if r == 0:
                # f integral => k - f integral, but 0 < H(c, c+1) < 1
                # for c > b >= 1.  No solution for this (a, b).
                continue
            p = B - r                   # t = p / B is the needed value
            # Exact bound t <= 1/(b+1) + 1/(b+2):
            #     p / B <= bound_num / bound_den
            if p * bound_den > bound_num * B:
                continue
            # Discriminant of p c^2 + (p - 2B) c - B = 0.
            D = p * p + 4 * B * B
            s = isqrt(D)
            if s * s != D:
                continue
            num = 2 * B - p + s
            den = 2 * p
            if num % den != 0:
                continue
            c = num // den
            if c <= b:
                continue
            # Direct exact re-verification before recording anything.
            total = f + Fraction(1, c) + Fraction(1, c + 1)
            if total.denominator != 1:
                continue
            l2.append(
                {
                    "a": a,
                    "b": b,
                    "c": c,
                    "d": c + 1,
                    "sum": total.numerator,
                }
            )
    return singleton, l2, pairs


def chunk_path(outdir, b_lo, b_hi):
    return os.path.join(outdir, "chunk_%04d_%04d.json" % (b_lo, b_hi))


def load_valid_chunk(path, b_lo, b_hi):
    """Return the parsed chunk dict if it is a usable checkpoint."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    expected_pairs = sum(range(b_lo, b_hi + 1))
    if (
        data.get("b_lo") == b_lo
        and data.get("b_hi") == b_hi
        and data.get("complete") is True
        and data.get("pairs_checked") == expected_pairs
    ):
        return data
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-b", type=int, default=2000)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument(
        "--outdir",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs"),
    )
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    started = time.time()

    print("Precomputing exact harmonic numbers H_n up to n = %d ..." % args.max_b,
          flush=True)
    h = harmonic_numbers(args.max_b)
    print("  done; H_%d has a %d-bit denominator."
          % (args.max_b, h[args.max_b].denominator.bit_length()), flush=True)

    all_singleton = []
    all_l2 = []
    total_pairs = 0
    chunks_done = 0
    chunks_skipped = 0

    b_lo = 1
    while b_lo <= args.max_b:
        b_hi = min(b_lo + args.chunk - 1, args.max_b)
        path = chunk_path(args.outdir, b_lo, b_hi)
        cached = load_valid_chunk(path, b_lo, b_hi)
        if cached is not None:
            singleton = cached["singleton_solutions"]
            l2 = cached["l2_solutions"]
            pairs = cached["pairs_checked"]
            chunks_skipped += 1
            status = "checkpoint hit, skipped"
        else:
            t0 = time.time()
            singleton, l2, pairs = examine_chunk(h, b_lo, b_hi)
            record = {
                "b_lo": b_lo,
                "b_hi": b_hi,
                "complete": True,
                "pairs_checked": pairs,
                "singleton_solutions": singleton,
                "l2_solutions": l2,
                "elapsed_seconds_this_run": round(time.time() - t0, 3),
            }
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(record, fh, indent=1, sort_keys=True)
            os.replace(tmp, path)       # atomic checkpoint
            status = "computed in %.1fs" % (time.time() - t0)
        chunks_done += 1
        total_pairs += pairs
        all_singleton.extend(singleton)
        all_l2.extend(l2)
        print("b %4d..%4d: %s; cumulative pairs %d, singleton %d, L2 %d"
              % (b_lo, b_hi, status, total_pairs,
                 len(all_singleton), len(all_l2)), flush=True)
        b_lo = b_hi + 1

    all_singleton.sort(key=lambda s: (s["b"], s["a"]))
    all_l2.sort(key=lambda s: (s["b"], s["a"], s["c"]))

    expected_pairs = args.max_b * (args.max_b + 1) // 2
    assert total_pairs == expected_pairs, (total_pairs, expected_pairs)

    with open(os.path.join(args.outdir, "singleton_solutions.json"),
              "w", encoding="utf-8") as fh:
        json.dump(all_singleton, fh, indent=1)
    with open(os.path.join(args.outdir, "l2_solutions.json"),
              "w", encoding="utf-8") as fh:
        json.dump(all_l2, fh, indent=1)

    summary = {
        "max_b": args.max_b,
        "pairs_checked": total_pairs,
        "singleton_solutions_all": all_singleton,
        "singleton_solutions_b_le_1600":
            [s for s in all_singleton if s["b"] <= 1600],
        "singleton_disjoint_b_le_max":
            [s for s in all_singleton if s["disjoint"]],
        "singleton_nondisjoint_b_le_max":
            [s for s in all_singleton if not s["disjoint"]],
        "l2_solutions": all_l2,
        "chunks_total": chunks_done,
        "chunks_skipped_from_checkpoint": chunks_skipped,
        "total_elapsed_seconds": round(time.time() - started, 3),
    }
    with open(os.path.join(args.outdir, "summary.json"),
              "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    print(json.dumps(summary, indent=1))
    print("TOTAL elapsed %.1fs" % (time.time() - started))


if __name__ == "__main__":
    main()
