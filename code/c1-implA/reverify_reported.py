#!/usr/bin/env python3
"""Independent re-verification for C1 Implementation A reported records.

Paths used here are independent of the C sweep kernel:
  * exact Fraction summation (fractions.Fraction) for every reported
    singleton solution and every pronic c > b near-miss (all are short
    intervals), deciding the conditions directly from the definition;
  * prime_ref.prime_data (the pure-Python prime-by-prime reference,
    copied from C0 Impl2) on a seeded random sample of intervals with
    2000 < b <= 20000, confirming none is a singleton or L = 2 solution
    and that its B / A mod B agree with the C kernel's scratch path;
  * chunk-file coverage aggregation for N = 5000 and N = 20000;
  * comparison of the b <= 2000 segments against the certified C0
    Implementation 2 outputs on disk.
"""
import json
import os
import random
import sys
from fractions import Fraction
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
sys.path.insert(0, HERE)
import prime_ref  # noqa: E402
import censusA  # noqa: E402


def frac_H(a, b):
    h = Fraction(0, 1)
    for n in range(a, b + 1):
        h += Fraction(1, n)
    return h


def main():
    report = {}
    sol = json.load(open(os.path.join(OUT, "solutions_n20000.json")))

    # --- coverage aggregation from chunk files ---
    for N in (5000, 20000):
        tot = 0
        a_next = 1
        nchunks = 0
        for fn in sorted(os.listdir(OUT)):
            if fn.startswith("chunk_") and fn.endswith(f"_n{N}.json"):
                d = json.load(open(os.path.join(OUT, fn)))
                assert d["a0"] == a_next, (fn, d["a0"], a_next)
                a_next = d["a1"] + 1
                expect = sum(N - a + 1 for a in range(d["a0"], d["a1"] + 1))
                assert d["stats"]["intervals"] == expect, fn
                assert d["stats"]["overflow"] == 0, fn
                tot += d["stats"]["intervals"]
                nchunks += 1
        assert a_next == N + 1
        assert tot == N * (N + 1) // 2, (N, tot)
        report[f"coverage_n{N}"] = {"intervals": tot, "chunks": nchunks}
    print("coverage OK", flush=True)

    # --- singletons by direct Fraction definition ---
    singles = []
    for s in sol["singleton_solutions_all_b<=N"]:
        a, b = s["a"], s["b"]
        h = frac_H(a, b)
        A, B = h.numerator, h.denominator
        assert str(B) == s["B"] and A % B == int(s["A_mod_B"]), (a, b)
        assert A % B == B - 1, (a, b)          # singleton condition
        assert (h + Fraction(1, B)).denominator == 1, (a, b)
        assert bool(B > b) == s["disjoint"], (a, b)
        singles.append((a, b, B))
    report["singletons_fraction_verified"] = singles
    assert singles == censusA.EXPECTED_SINGLETONS, singles
    print("singletons Fraction-verified:", singles, flush=True)

    # --- pronic c > b near-misses by direct Fraction definition ---
    near = []
    for p in sol["pronic_with_c_gt_b"]:
        a, b, c = p["a"], p["b"], p["c"]
        h = frac_H(a, b)
        A, B = h.numerator, h.denominator
        assert str(B) == p["B"] and A == int(p["A_mod_B"]), (a, b)
        assert B == c * (c + 1) and c > b, (a, b, c)
        residue = (A + 2 * c + 1) % B
        assert residue == p["residue_A_plus_2c_plus_1_mod_B"], (a, b)
        assert residue != 0, (a, b)
        total = h + frac_H(c, c + 1)
        assert total.denominator != 1, (a, b, c)   # not an L=2 solution
        near.append({"a": a, "b": b, "B": B, "c": c, "A": A,
                     "residue": residue, "exact_sum": str(total)})
    report["pronic_c_gt_b_fraction_verified"] = near
    print("near-misses Fraction-verified:", len(near), flush=True)

    # --- comparison with certified C0 Impl2 outputs (b <= 2000 segment) ---
    c0 = json.load(open(os.path.join(
        HERE, "..", "c0-impl2", "outputs", "solutions.json")))
    c0_singles = sorted((s["a"], s["b"], int(s["m"]))
                        for s in c0["singleton_solutions_all_b<=N"])
    ours_2000 = sorted((s["a"], s["b"], int(s["m"]))
                       for s in sol["singleton_solutions_b<=2000"])
    assert ours_2000 == c0_singles, (ours_2000, c0_singles)
    c0_near = sorted((p["a"], p["b"], int(p["B"]), p["c"])
                     for p in c0["pronic_with_c_gt_b"])
    ours_near = sorted((p["a"], p["b"], int(p["B"]), p["c"])
                       for p in sol["pronic_with_c_gt_b"] if p["b"] <= 2000)
    assert ours_near == c0_near, (ours_near, c0_near)
    report["c0_segment_match"] = {"singletons": ours_2000, "near": ours_near}
    print("C0 b<=2000 segment matches certified outputs", flush=True)

    # --- seeded random sample of the new range via prime_ref (pure Python) ---
    rng = random.Random(20261031)
    primes_all = prime_ref.sieve_primes(20000)
    checked = 0
    for _ in range(150):
        a = rng.randint(2001, 19960)
        b = a + rng.randint(0, 40)
        data = prime_ref.prime_data(a, b, primes_all)
        is_single, B, A_mod_B, _ = prime_ref.check_singleton(data)
        l2 = prime_ref.check_l2(a, b, data)
        assert not is_single, (a, b)
        assert not l2["is_solution"], (a, b)
        kd = censusA.kernel_interval_active(a, b)
        krec = censusA.verify_from_data(a, b, kd)
        assert krec["B"] == B and krec["A_mod_B"] == A_mod_B, (a, b)
        checked += 1
    report["random_sample_new_range_prime_ref_checked"] = checked
    print("random sample (prime_ref, new range) OK:", checked, flush=True)

    report["all_checks_passed"] = True
    with open(os.path.join(OUT, "independent_recheck.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report, indent=1)[:1200])


if __name__ == "__main__":
    main()
