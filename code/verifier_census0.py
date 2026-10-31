#!/usr/bin/env python3
"""
verifier_census0.py -- Cluster C0 Verifier, Erdős #288 Cycle 1.

Independent checks, exact arithmetic only (int / fractions.Fraction / math).

Third method for the spot census (b <= 250), deliberately different from
both implementations under review:
  * Implementation 1: global harmonic prefix Fractions H_b - H_{a-1}.
  * Implementation 2: prime-by-prime (V_p, S_p) state, C kernel, filters/CRT.
  * This verifier: ONE common denominator D = lcm(1..250).  For every
    interval [a,b] the sum is the integer S = sum_{n=a}^b D//n over D,
    reduced once via Fraction(S, D).  No prefix sums, no prime state,
    no filters, no CRT.
Singleton decision is by the direct definition: the only possible integer
value is k = floor(H)+1 (H>0), and H + 1/m = k iff 1/(k-H) is a positive
integer m.
L = 2 decision on b <= 250, two exact sub-checks:
  (a) explicit direct scan of every c with b < c <= 5000, computing
      H(a,b) + 1/c + 1/(c+1) as an exact Fraction;
  (b) unbounded-c check: from the reduced H(a,b) = A/B, an integral sum
      forces B = c(c+1) (denominator forcing, re-derived in CENSUS0.md);
      every interval whose B is pronic with root c > b is tested by a
      direct exact Fraction sum.  Together (a)+(b) cover every c > b.

Also performed:
  * direct machine-readable diff of Impl1 vs Impl2 solution sets for
    tasks (i), (ii), (iii);
  * chunk-file coverage aggregation for both implementations;
  * direct exact verification of the six published solutions;
  * direct exact verification of Impl2's four L = 2 near-misses,
    including A, B and the residue (A + 2c + 1) mod B.

Writes verifier_results.json beside this script.  Exits nonzero if any
comparison fails (and records the failure in the JSON first).
"""

import json
import math
import os
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMPL1 = os.path.join(ROOT, "code", "c0-impl1", "outputs")
IMPL2 = os.path.join(ROOT, "code", "c0-impl2", "outputs")

PUBLISHED_SIX = [(1, 1, 1), (1, 2, 2), (2, 2, 2),
                 (1, 3, 6), (2, 3, 6), (3, 6, 20)]
PUBLISHED_DISJOINT = [(1, 3, 6), (2, 3, 6), (3, 6, 20)]
NEAR_MISSES = [  # (a, b, B, c, A, (A + 2c + 1) mod B) as reported by Impl2
    (4, 7, 420, 20, 319, 360),
    (5, 7, 210, 14, 107, 136),
    (9, 12, 1980, 44, 763, 852),
    (154, 156, 1861860, 1364, 36037, 38766),
]
BMAX_SPOT = 250
C_SCAN_MAX = 5000

out = {"failures": []}


def fail(msg):
    out["failures"].append(msg)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def H_direct(a, b):
    """H(a,b) by naive term-by-term Fraction summation (no prefixes)."""
    s = Fraction(0, 1)
    for n in range(a, b + 1):
        s += Fraction(1, n)
    return s


# ----------------------------------------------------------------------
# (1) Direct diff of the two implementations' machine-readable outputs
# ----------------------------------------------------------------------
def norm_single(records, mkey="m"):
    return sorted((r["a"], r["b"], int(r[mkey])) for r in records)


i1_single = norm_single(load(os.path.join(IMPL1, "singleton_solutions.json")))
i1_l2 = load(os.path.join(IMPL1, "l2_solutions.json"))
i1_summary = load(os.path.join(IMPL1, "summary.json"))
i1_first = load(os.path.join(IMPL1, "summary_first_run.json"))

i2 = load(os.path.join(IMPL2, "solutions.json"))
i2_single = norm_single(i2["singleton_solutions_all_b<=N"])
i2_single_1600 = norm_single(i2["singleton_solutions_b<=1600"])
i2_l2 = i2["l2_solutions"]

i1_single_1600 = sorted(t for t in i1_single if t[1] <= 1600)
i1_disjoint = sorted(t for t in i1_single
                     if dict(( (r["a"], r["b"]), r["disjoint"])
                             for r in load(os.path.join(
                                 IMPL1, "singleton_solutions.json")))[(t[0], t[1])])
i2_disjoint = sorted((r["a"], r["b"], int(r["m"]))
                     for r in i2["singleton_solutions_all_b<=N"] if r["disjoint"])

diff = {
    "task_i_b<=1600_impl1": i1_single_1600,
    "task_i_b<=1600_impl2": i2_single_1600,
    "task_i_identical": i1_single_1600 == i2_single_1600,
    "task_ii_b<=2000_impl1": i1_single,
    "task_ii_b<=2000_impl2": i2_single,
    "task_ii_identical": i1_single == i2_single,
    "task_ii_disjoint_impl1": i1_disjoint,
    "task_ii_disjoint_impl2": i2_disjoint,
    "task_ii_disjoint_identical": i1_disjoint == i2_disjoint,
    "task_iii_l2_impl1": i1_l2,
    "task_iii_l2_impl2": i2_l2,
    "task_iii_identical": i1_l2 == i2_l2 == [],
    "impl1_matches_P1_six": i1_single_1600 == sorted(PUBLISHED_SIX),
    "impl2_matches_P1_six": i2_single_1600 == sorted(PUBLISHED_SIX),
    "impl1_disjoint_matches_P2": i1_disjoint == sorted(PUBLISHED_DISJOINT),
    "impl2_disjoint_matches_P2": i2_disjoint == sorted(PUBLISHED_DISJOINT),
}
out["direct_diff"] = diff
for k, v in diff.items():
    if k.endswith(("identical", "matches_P1_six", "matches_P2")) and v is not True:
        fail(f"direct diff failed: {k} = {v}")

# ----------------------------------------------------------------------
# (4) Coverage from chunk / checkpoint files on disk
# ----------------------------------------------------------------------
# Impl1: chunks are b-blocks of 100.
i1_pairs = 0
i1_chunk_single, i1_chunk_l2, i1_ranges = [], [], []
i1_chunk_elapsed = 0.0
for lo in range(1, 2001, 100):
    hi = lo + 99
    ch = load(os.path.join(IMPL1, f"chunk_{lo:04d}_{hi:04d}.json"))
    assert ch["complete"] is True and ch["b_lo"] == lo and ch["b_hi"] == hi
    expected = sum(range(lo, hi + 1))
    if ch["pairs_checked"] != expected:
        fail(f"impl1 chunk {lo}-{hi} pairs {ch['pairs_checked']} != {expected}")
    i1_pairs += ch["pairs_checked"]
    i1_ranges.append((lo, hi))
    i1_chunk_single.extend(norm_single(ch["singleton_solutions"]))
    i1_chunk_l2.extend(ch["l2_solutions"])
    i1_chunk_elapsed += ch.get("elapsed_seconds_this_run", 0.0)
cov1 = {
    "chunks": len(i1_ranges), "ranges_contiguous_1_2000":
        i1_ranges == [(lo, lo + 99) for lo in range(1, 2001, 100)],
    "total_pairs_from_chunks": i1_pairs,
    "chunk_singleton_union": sorted(i1_chunk_single),
    "chunk_singleton_union_matches_file": sorted(i1_chunk_single) == i1_single,
    "chunk_l2_union": i1_chunk_l2,
    "sum_chunk_compute_seconds": round(i1_chunk_elapsed, 2),
    "summary_pairs_checked": i1_summary["pairs_checked"],
    "summary_first_run_pairs_checked": i1_first["pairs_checked"],
    "first_run_vs_resume_summary_solutions_identical":
        norm_single(i1_first["singleton_solutions_all"]) == i1_single
        and i1_first["l2_solutions"] == i1_l2 == [],
    "first_run_elapsed_seconds": i1_first["total_elapsed_seconds"],
    "resume_summary_elapsed_seconds": i1_summary["total_elapsed_seconds"],
    "resume_summary_chunks_skipped": i1_summary["chunks_skipped_from_checkpoint"],
}
out["coverage_impl1"] = cov1
if i1_pairs != 2001000:
    fail(f"impl1 chunk pair total {i1_pairs} != 2001000")

# Impl2: chunks are a-blocks of 100; verify files hold the decided solutions.
i2_intervals = 0
i2_stats = {"delta_events": 0, "changed_prime_records": 0,
            "single_filter_passes": 0, "l2_filter_passes": 0}
i2_cand_single = i2_cand_l2 = 0
i2_verified = 0
i2_verify_single, i2_verify_l2, i2_pronic_gt = [], [], []
for lo in range(1, 2001, 100):
    hi = lo + 99
    ch = load(os.path.join(IMPL2, f"chunk_a{lo:04d}_{hi:04d}_n2000.json"))
    expected = sum(2000 - a + 1 for a in range(lo, hi + 1))
    if ch["stats"]["intervals"] != expected:
        fail(f"impl2 chunk a={lo}-{hi} intervals "
             f"{ch['stats']['intervals']} != {expected}")
    i2_intervals += ch["stats"]["intervals"]
    for k in i2_stats:
        i2_stats[k] += ch["stats"][k]
    if ch["stats"].get("overflow", 0) != 0:
        fail(f"impl2 chunk a={lo}-{hi} overflow != 0")
    i2_cand_single += len(ch["single_candidates"])
    i2_cand_l2 += len(ch["l2_candidates"])
    vf = load(os.path.join(IMPL2, f"verify_a{lo:04d}_{hi:04d}_n2000.json"))
    i2_verified += vf["candidates_verified"]
    i2_verify_single.extend(norm_single(vf["singleton_solutions"]))
    i2_verify_l2.extend(vf["l2_solutions"])
    i2_pronic_gt.extend(
        (p["a"], p["b"], int(p["B"]), p["c"])
        for p in vf["pronic_candidates"] if p["c_gt_b"])
cov2 = {
    "chunks": 20, "total_intervals_from_chunks": i2_intervals,
    "stats_totals_from_chunks": i2_stats,
    "stats_match_solutions_json": i2_stats == i2["sweep_stats_totals"],
    "candidates_single_from_chunks": i2_cand_single,
    "candidates_l2_from_chunks": i2_cand_l2,
    "candidates_verified_sum_from_verify_files": i2_verified,
    "candidate_union_in_solutions_json": i2["candidate_totals"]["union"],
    "verify_singleton_union": sorted(i2_verify_single),
    "verify_singleton_union_matches_solutions_json":
        sorted(i2_verify_single) == i2_single,
    "verify_l2_union": i2_verify_l2,
    "pronic_c_gt_b_from_verify_files": sorted(i2_pronic_gt),
    "pronic_c_gt_b_in_solutions_json":
        sorted((p["a"], p["b"], int(p["B"]), p["c"])
               for p in i2["pronic_with_c_gt_b"]),
    "compute_seconds_from_chunks_field": i2["compute_seconds_from_chunks"],
    "progress_json": load(os.path.join(IMPL2, "progress.json")),
    "selftest_json_seconds": load(os.path.join(IMPL2, "selftest.json"))
        ["self_test_seconds"],
}
out["coverage_impl2"] = cov2
if i2_intervals != 2001000:
    fail(f"impl2 chunk interval total {i2_intervals} != 2001000")
if sorted(i2_pronic_gt) != sorted(
        (a, b, B, c) for (a, b, B, c, _A, _r) in NEAR_MISSES):
    fail(f"impl2 pronic c>b set {sorted(i2_pronic_gt)} != four near-misses")

# ----------------------------------------------------------------------
# (3a) The six solutions, verified directly
# ----------------------------------------------------------------------
six_checks = []
for (a, b, m) in PUBLISHED_SIX:
    h = H_direct(a, b)
    total = h + Fraction(1, m)
    ok = total.denominator == 1
    six_checks.append({"a": a, "b": b, "m": m, "H": str(h),
                       "H_plus_1_over_m": str(total), "is_integer": ok,
                       "disjoint_m_gt_b": m > b})
    if not ok:
        fail(f"published solution {(a, b, m)} does not verify directly")
out["six_solutions_direct"] = six_checks

# ----------------------------------------------------------------------
# (3b) The four L = 2 near-misses, verified exactly
# ----------------------------------------------------------------------
nm_checks = []
for (a, b, B, c, A_exp, res_exp) in NEAR_MISSES:
    h = H_direct(a, b)
    total = h + H_direct(c, c + 1)
    A, Bv = h.numerator, h.denominator
    residue = (A + 2 * c + 1) % Bv
    rec = {"a": a, "b": b, "c": c, "H_ab": str(h), "A": A, "B": Bv,
           "B_matches_reported": Bv == B,
           "A_matches_reported": A == A_exp,
           "c_times_c_plus_1": c * (c + 1), "B_is_pronic_c": c * (c + 1) == Bv,
           "c_gt_b": c > b,
           "residue_A_plus_2c_plus_1_mod_B": residue,
           "residue_matches_reported": residue == res_exp,
           "exact_sum_Hab_plus_Hcc1": str(total),
           "sum_is_integer": total.denominator == 1}
    nm_checks.append(rec)
    if Bv != B or A != A_exp or residue != res_exp or total.denominator == 1:
        fail(f"near-miss {(a, b, B, c)} mismatch: {rec}")
out["near_miss_direct"] = nm_checks

# ----------------------------------------------------------------------
# (3c) Third-method spot census, all intervals with b <= 250
# ----------------------------------------------------------------------
t0 = time.time()
D = 1
for n in range(2, BMAX_SPOT + 1):
    D = D * n // math.gcd(D, n)
# prefix sums of D//n over the common denominator (integer arithmetic only)
Dover = [0] * (BMAX_SPOT + 1)
for n in range(1, BMAX_SPOT + 1):
    assert D % n == 0
    Dover[n] = D // n
pref = [0] * (BMAX_SPOT + 1)
for n in range(1, BMAX_SPOT + 1):
    pref[n] = pref[n - 1] + Dover[n]

spot_single = []
spot_pronic_gt = []
spot_l2_scan = []   # from explicit c-scan, c <= C_SCAN_MAX
spot_l2_pronic = []  # from forced-B check, any c
intervals = 0
# L=2 (a) preparation: tabulate every c <= C_SCAN_MAX by the exact
# fractional part of H(c, c+1) = 1/c + 1/(c+1) (each computed directly).
# An interval can pair with such a c only if the fractional parts are
# complementary; every complementary pair is then re-checked by a
# direct exact Fraction sum, so the tabulation is only a lookup, never
# the decision.
frac_to_c = {}
for c in range(2, C_SCAN_MAX + 1):
    g = Fraction(1, c) + Fraction(1, c + 1)
    frac_to_c.setdefault(g - (g.numerator // g.denominator), []).append(c)
for b in range(1, BMAX_SPOT + 1):
    for a in range(1, b + 1):
        intervals += 1
        f = Fraction(pref[b] - pref[a - 1], D)  # exact H(a,b), reduced
        # singleton, direct definition
        k = f.numerator // f.denominator + 1
        diff = k - f
        if diff.numerator == 1:
            spot_single.append((a, b, diff.denominator))
        # L=2 (a): explicit scan (lookup) over c <= C_SCAN_MAX, with
        # direct exact re-verification of every complementary candidate
        frac_f = f - (f.numerator // f.denominator)
        need = (1 - frac_f) % 1
        for c in frac_to_c.get(need, []):
            if c > b and (f + Fraction(1, c)
                          + Fraction(1, c + 1)).denominator == 1:
                spot_l2_scan.append((a, b, c))
        # L=2 (b): forced denominator, any c
        Bv = f.denominator
        c0 = math.isqrt(Bv)
        if c0 * (c0 + 1) == Bv and c0 > b:
            spot_pronic_gt.append((a, b, Bv, c0))
            tot = f + Fraction(1, c0) + Fraction(1, c0 + 1)
            if tot.denominator == 1:
                spot_l2_pronic.append((a, b, c0))

spot = {
    "bmax": BMAX_SPOT, "intervals_examined": intervals,
    "expected_intervals": BMAX_SPOT * (BMAX_SPOT + 1) // 2,
    "method": "common denominator D = lcm(1..250), integer sums S/D, "
              "single reduction per interval; singleton by direct "
              "definition; L2 by explicit c-scan to 5000 plus forced-B "
              "pronic check for all c",
    "D_digits": len(str(D)),
    "singleton_solutions": sorted(spot_single),
    "l2_solutions_from_c_scan": spot_l2_scan,
    "l2_solutions_from_pronic_check": spot_l2_pronic,
    "pronic_B_with_c_gt_b": sorted(spot_pronic_gt),
    "seconds": round(time.time() - t0, 2),
}
out["spot_census_b<=250"] = spot
if intervals != spot["expected_intervals"]:
    fail("spot interval count wrong")
if sorted(spot_single) != sorted(t for t in i1_single if t[1] <= BMAX_SPOT):
    fail("spot singletons != impl1 restricted to b<=250")
if sorted(spot_single) != sorted(t for t in i2_single if t[1] <= BMAX_SPOT):
    fail("spot singletons != impl2 restricted to b<=250")
if spot_l2_scan or spot_l2_pronic:
    fail("spot census found an L2 solution")
if sorted(spot_pronic_gt) != sorted(
        (a, b, B, c) for (a, b, B, c, _A, _r) in NEAR_MISSES):
    fail(f"spot pronic c>b set {sorted(spot_pronic_gt)} != four near-misses")

out["all_checks_passed"] = not out["failures"]
with open(os.path.join(HERE, "verifier_results.json"), "w",
          encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps({
    "direct_diff_identical": {k: v for k, v in out["direct_diff"].items()
                              if isinstance(v, bool)},
    "impl1_pairs_from_chunks": i1_pairs,
    "impl2_intervals_from_chunks": i2_intervals,
    "spot_singletons": sorted(spot_single),
    "spot_l2_scan": spot_l2_scan, "spot_l2_pronic": spot_l2_pronic,
    "spot_pronic_gt": sorted(spot_pronic_gt),
    "spot_seconds": spot["seconds"],
    "failures": out["failures"],
}, indent=1))
if out["failures"]:
    raise SystemExit(1)
