#!/usr/bin/env python3
"""
Red Team exhaustive search for Erdős #288, Theorem 3.2 (Nayak).

Exhaustively test all intersecting interval pairs I, J with endpoints in
[1, N] for an integer sum H(I) + H(J), in exact rational arithmetic
(fractions.Fraction throughout).

Method (exhaustive, not a sampling or a modular sieve):
  * prefix[k] = H([1,k]) as an exact Fraction.
  * Every interval [u,v] (1 <= u <= v <= N) is enumerated exactly once;
    its harmonic sum is prefix[v] - prefix[u-1] (exact Fraction), and its
    canonical fractional part (num mod den)/den in lowest terms is stored.
  * H(I) + H(J) is an integer iff frac(H(I)) + frac(H(J)) is 0 or 1, i.e.
    iff frac(H(J)) equals the complement (-frac(H(I))) mod 1.  A dictionary
    keyed by the exact fractional part therefore finds *every* pair of
    intervals (intersecting or not) whose sum is an integer: no pair can be
    missed, because the dictionary contains every interval.
  * Every candidate pair produced by the dictionary is re-verified by a
    direct Fraction addition H(I) + H(J) and a denominator == 1 test.

Checkpointing / resumability:
  * Intervals are generated in blocks of BLOCK right endpoints v.
  * After each block the records are appended to a pickle checkpoint
    (redteam_checkpoint_N.pkl) together with the largest v completed.
  * Re-running with the same N resumes after the last completed block.
  * The matching stage runs only after all blocks are present and writes
    redteam_results_N.json.

Usage: python3 redteam_search.py 1000
"""
import json
import pickle
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = 50
KNOWN = {
    ((1, 1), (1, 1)),
    ((1, 2), (1, 2)),
    ((1, 2), (2, 2)),
    ((2, 2), (2, 2)),
}


def prefix_fractions(n):
    pref = [Fraction(0, 1)]
    for k in range(1, n + 1):
        pref.append(pref[-1] + Fraction(1, k))
    return pref


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    ckpt_path = HERE / f"redteam_checkpoint_{n}.pkl"
    results_path = HERE / f"redteam_results_{n}.json"

    records = []  # (u, v, frac_num, frac_den) with 0 <= frac_num < frac_den, gcd = 1 (or frac 0 = 0/1)
    done_v = 0
    if ckpt_path.exists():
        with ckpt_path.open("rb") as f:
            state = pickle.load(f)
        if state["n"] == n:
            records = state["records"]
            done_v = state["done_v"]
            print(f"resuming at v={done_v}, records={len(records)}", flush=True)

    pref = prefix_fractions(n)
    t0 = time.time()
    v = done_v
    while v < n:
        v_next = min(n, v + BLOCK)
        for vv in range(v + 1, v_next + 1):
            pv = pref[vv]
            for u in range(1, vv + 1):
                s = pv - pref[u - 1]  # exact H([u, vv])
                fn = s.numerator % s.denominator
                if fn == 0:
                    records.append((u, vv, 0, 1))
                else:
                    # s is already in lowest terms; fn/den may share a factor,
                    # reduce via Fraction to get the canonical fractional part.
                    fr = Fraction(fn, s.denominator)
                    records.append((u, vv, fr.numerator, fr.denominator))
        v = v_next
        with ckpt_path.open("wb") as f:
            pickle.dump({"n": n, "done_v": v, "records": records}, f, protocol=4)
        print(f"checkpoint v<={v} records={len(records)} elapsed={time.time()-t0:.1f}s", flush=True)

    total_intervals = n * (n + 1) // 2
    assert len(records) == total_intervals, (len(records), total_intervals)

    # Matching stage: dictionary from exact fractional part to interval indices.
    index = {}
    for idx, (u, vv, fn, fd) in enumerate(records):
        index.setdefault((fn, fd), []).append(idx)

    def intersects(i1, i2):
        a, b = i1
        c, d = i2
        return max(a, c) <= min(b, d)

    found_all = []        # every integer-sum pair (any position), unordered, with repetition allowed
    found_intersecting = []
    candidates_checked = 0
    for idx, (u, vv, fn, fd) in enumerate(records):
        if fn == 0:
            comp = (0, 1)
        else:
            cf = Fraction(fd - fn, fd)  # (-frac) mod 1, canonical
            comp = (cf.numerator, cf.denominator)
        for jdx in index.get(comp, ()):  # all J with complementary fractional part
            if jdx < idx:
                continue
            candidates_checked += 1
            i_int = (u, vv)
            j_int = (records[jdx][0], records[jdx][1])
            # Independent direct exact verification of this candidate.
            hi = pref[i_int[1]] - pref[i_int[0] - 1]
            hj = pref[j_int[1]] - pref[j_int[0] - 1]
            tot = hi + hj
            assert tot.denominator == 1, (i_int, j_int, tot)
            pair = (i_int, j_int)
            found_all.append((pair, int(tot)))
            if intersects(i_int, j_int):
                found_intersecting.append((pair, int(tot)))

    unexpected = [p for p, _ in found_intersecting if p not in KNOWN]
    out = {
        "N": n,
        "intervals_enumerated": total_intervals,
        "candidate_pairs_from_dictionary": candidates_checked,
        "integer_sum_pairs_all_positions": [
            {"pair": [list(p[0]), list(p[1])], "sum": s} for p, s in found_all
        ],
        "integer_sum_pairs_intersecting": [
            {"pair": [list(p[0]), list(p[1])], "sum": s} for p, s in found_intersecting
        ],
        "intersecting_pairs_outside_theorem_3_2_list": [
            {"pair": [list(p[0]), list(p[1])], "sum": s} for p, s in found_intersecting if p not in KNOWN
        ],
        "elapsed_seconds_generation_and_matching_this_run": round(time.time() - t0, 1),
    }
    results_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2), flush=True)


if __name__ == "__main__":
    main()
