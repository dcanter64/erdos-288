#!/usr/bin/env python3
"""Cluster C1 Verifier: direct machine comparison + coverage/timing
aggregation for Implementations A and B, Erdős #288 census extension
to b <= 20,000.  Exact integer arithmetic only; compares JSON files,
not prose.  Writes verifier_c1_compare_results.json next to itself.
"""
import json, glob, os, hashlib
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A = os.path.join(ROOT, "code", "c1-implA", "outputs")
B = os.path.join(ROOT, "code", "c1-implB", "outputs")
R = {"checks": {}, "details": {}}

def load(p):
    with open(p) as f:
        return json.load(f)

def S(x):
    return sorted(map(tuple, x))

EXPECTED_SING = [(1, 1, 1), (1, 2, 2), (1, 3, 6), (2, 2, 2), (2, 3, 6), (3, 6, 20)]
EXPECTED_NEAR = [(4, 7, 420, 20, 360), (5, 7, 210, 14, 136),
                 (9, 12, 1980, 44, 852), (154, 156, 1861860, 1364, 38766)]

# ---------- Implementation A: headline + chunk aggregation ----------
solA5 = load(os.path.join(A, "solutions_n5000.json"))
solA20 = load(os.path.join(A, "solutions_n20000.json"))
singA = S((s["a"], s["b"], int(s["m"])) for s in solA20["singleton_solutions_all_b<=N"])
l2A = solA20["l2_solutions"]
nearA = S((p["a"], p["b"], int(p["B"]), p["c"],
           p["residue_A_plus_2c_plus_1_mod_B"]) for p in solA20["pronic_with_c_gt_b"])
R["details"]["A_singletons"] = singA
R["details"]["A_l2_solutions"] = l2A
R["details"]["A_nearmisses"] = nearA
R["details"]["A_pronic_all_count"] = len(solA20["pronic_candidates_all"])

def aggregate_A(N):
    chunks = sorted(glob.glob(os.path.join(A, f"chunk_a*_n{N}.json")))
    verifies = sorted(glob.glob(os.path.join(A, f"verify_a*_n{N}.json")))
    tot_int = 0; sweep_s = 0.0; verify_s = 0.0; overflow = 0
    stats = {"delta_events": 0, "changed_prime_records": 0,
             "single_filter_passes": 0, "l2_filter_passes": 0}
    cand_s = set(); cand_l = set(); ranges = []
    v_sing = set(); v_l2 = []; v_pron = set(); v_pron_gt = set(); cand_verified = 0
    per_chunk_ok = True
    for p in chunks:
        d = load(p)
        ranges.append((d["a0"], d["a1"]))
        expect = sum(N - a + 1 for a in range(d["a0"], d["a1"] + 1))
        if d["stats"]["intervals"] != expect:
            per_chunk_ok = False
        tot_int += d["stats"]["intervals"]
        sweep_s += d["sweep_seconds"]
        overflow += d["stats"]["overflow"]
        for k in stats:
            stats[k] += d["stats"][k]
        cand_s |= {tuple(x) for x in d["single_candidates"]}
        cand_l |= {tuple(x) for x in d["l2_candidates"]}
    for p in verifies:
        d = load(p)
        verify_s += d["verify_seconds"]
        cand_verified += d["candidates_verified"]
        v_sing |= {(s["a"], s["b"], int(s["m"])) for s in d["singleton_solutions"]}
        v_l2 += [(x["a"], x["b"], x["c"]) for x in d["l2_solutions"]]
        for pr in d["pronic_candidates"]:
            v_pron.add((pr["a"], pr["b"], int(pr["B"]), pr["c"]))
            if pr["c_gt_b"]:
                v_pron_gt.add((pr["a"], pr["b"], int(pr["B"]), pr["c"],
                               pr["residue_A_plus_2c_plus_1_mod_B"]))
    ranges.sort()
    contiguous = ranges[0][0] == 1 and ranges[-1][1] == N and \
        all(ranges[i][1] + 1 == ranges[i + 1][0] for i in range(len(ranges) - 1))
    return {"n_chunks": len(chunks), "n_verify": len(verifies),
            "total_intervals": tot_int, "per_chunk_intervals_ok": per_chunk_ok,
            "ranges_contiguous": contiguous, "sweep_seconds_sum": round(sweep_s, 3),
            "verify_seconds_sum": round(verify_s, 3),
            "compute_seconds_sum": round(sweep_s + verify_s, 3),
            "overflow_total": overflow, "stats": stats,
            "chunk_single_candidates": len(cand_s), "chunk_l2_candidates": len(cand_l),
            "verify_candidates_verified_sum": cand_verified,
            "verify_singleton_union": S(v_sing), "verify_l2_union": v_l2,
            "verify_pronic_union_count": len(v_pron),
            "verify_pronic_gt_union": S(v_pron_gt)}

aggA5 = aggregate_A(5000)
aggA20 = aggregate_A(20000)
R["details"]["A_agg_5000"] = aggA5
R["details"]["A_agg_20000"] = aggA20
R["details"]["A_solutions_n5000_fields"] = {
    "total_intervals": solA5["total_intervals"],
    "compute_seconds_from_chunks": solA5["compute_seconds_from_chunks"],
    "last_run_wall_seconds": solA5["last_run_wall_seconds"],
    "kernel_init_seconds": solA5["kernel_init_seconds"]}
R["details"]["A_solutions_n20000_fields"] = {
    "total_intervals": solA20["total_intervals"],
    "compute_seconds_from_chunks": solA20["compute_seconds_from_chunks"],
    "last_run_wall_seconds": solA20["last_run_wall_seconds"],
    "kernel_init_seconds": solA20["kernel_init_seconds"]}
R["details"]["A_progress_n5000"] = load(os.path.join(A, "progress_n5000.json"))
R["details"]["A_progress_n20000"] = load(os.path.join(A, "progress_n20000.json"))
R["details"]["A_selftest"] = {k: v for k, v in load(os.path.join(A, "selftest.json")).items()
                              if not isinstance(v, list) or k in ("filter_primes", "qr_mods")}
R["details"]["A_independent_recheck_all_passed"] = \
    load(os.path.join(A, "independent_recheck.json"))["all_checks_passed"]

# ---------- Implementation B: headline + chunk aggregation ----------
aggBfull = load(os.path.join(B, "aggregate_full.json"))
aggBgate = load(os.path.join(B, "aggregate_gate5000.json"))
verBfull = load(os.path.join(B, "verify_full.json"))
verBgate = load(os.path.join(B, "verify_gate.json"))
singB = S((s["a"], s["b"], s["m"]) for s in verBfull["singleton_candidates_verified"])
l2B = verBfull["l2_solutions"]
nearB = S((x["a"], x["b"], x["B"], x["c"], x["residue_A_plus_2c_plus_1_mod_B"])
          for x in verBfull["l2_nearmisses_verified"])
R["details"]["B_singletons"] = singB
R["details"]["B_l2_solutions"] = l2B
R["details"]["B_nearmisses"] = nearB

def aggregate_B():
    chunks = sorted(glob.glob(os.path.join(B, "chunk_*.json")))
    tot_int = 0; secs = 0.0; ranges = []; per_chunk_ok = True
    stats = {}; cand = set(); nms = set()
    for p in chunks:
        d = load(p)
        ranges.append((d["b_lo"], d["b_hi"]))
        expect = sum(range(d["b_lo"], d["b_hi"] + 1))
        if d["stats"]["intervals"] != expect:
            per_chunk_ok = False
        tot_int += d["stats"]["intervals"]
        secs += d["seconds"]
        for k, v in d["stats"].items():
            stats[k] = stats.get(k, 0) + v
        cand |= {(x["a"], x["b"], x["t"]) for x in d["singleton_candidates"]}
        nms |= {(x["a"], x["b"], x["c"]) for x in d["l2_nearmisses"]}
    ranges.sort()
    contiguous = ranges[0][0] == 1 and ranges[-1][1] == 20000 and \
        all(ranges[i][1] + 1 == ranges[i + 1][0] for i in range(len(ranges) - 1))
    gate_secs = 0.0; gate_int = 0
    for p in chunks:
        d = load(p)
        if d["b_hi"] <= 5000:
            gate_secs += d["seconds"]; gate_int += d["stats"]["intervals"]
    return {"n_chunks": len(chunks), "total_intervals": tot_int,
            "per_chunk_intervals_ok": per_chunk_ok, "ranges_contiguous": contiguous,
            "seconds_sum": round(secs, 3), "stats": stats,
            "chunk_singleton_candidates": S(cand), "chunk_nearmisses": S(nms),
            "gate_seconds_sum_first20": round(gate_secs, 3),
            "gate_intervals_first20": gate_int}

aggB = aggregate_B()
R["details"]["B_agg_chunks"] = aggB
R["details"]["B_aggregate_full_fields"] = {
    "total_seconds_sum_of_chunks": aggBfull["total_seconds_sum_of_chunks"],
    "stats": aggBfull["stats"], "coverage_ok": aggBfull["coverage_ok"]}
R["details"]["B_aggregate_gate_fields"] = {
    "total_seconds_sum_of_chunks": aggBgate["total_seconds_sum_of_chunks"],
    "stats": aggBgate["stats"], "coverage_ok": aggBgate["coverage_ok"]}
R["details"]["B_brute_2000"] = load(os.path.join(B, "brute_2000.json"))
R["details"]["B_brute_300"] = load(os.path.join(B, "brute_300.json"))

# ---------- Direct comparisons ----------
C = R["checks"]
C["singletons_A_eq_B"] = singA == singB
C["singletons_eq_expected_six"] = singA == EXPECTED_SING == singB
C["singletons_none_in_2000_20000"] = all(b <= 2000 for _, b, _ in singA + singB)
C["l2_empty_both"] = l2A == [] == l2B
C["nearmiss_A_eq_B"] = nearA == nearB
C["nearmiss_eq_expected_four"] = nearA == EXPECTED_NEAR == nearB
C["nearmiss_none_b_gt_2000"] = all(b <= 2000 for _, b, *_ in nearA + nearB)
C["A_chunk_union_eq_headline"] = (aggA20["verify_singleton_union"] == singA and
                                  aggA20["verify_l2_union"] == [] and
                                  aggA20["verify_pronic_gt_union"] == nearA and
                                  aggA20["verify_pronic_union_count"] ==
                                  len(solA20["pronic_candidates_all"]))
C["B_chunk_union_eq_aggregate"] = (
    aggB["chunk_singleton_candidates"] ==
    S((x["a"], x["b"], x["t"]) for x in aggBfull["singleton_candidates"]) and
    aggB["chunk_nearmisses"] ==
    S((x["a"], x["b"], x["c"]) for x in aggBfull["l2_nearmisses"]))
C["pronic_totals_crosscheck"] = (
    solA20["sweep_stats_totals"]["l2_filter_passes"] ==
    aggBfull["stats"]["l2_legendreD_passes"] == 20149 and
    aggBfull["stats"]["l2_nearmisses"] + aggBfull["stats"]["l2_pronic_c_le_b"] == 20149 and
    solA5["sweep_stats_totals"]["l2_filter_passes"] ==
    aggBgate["stats"]["l2_legendreD_passes"] == 5079)

# ---------- Coverage ----------
C["A_coverage_20000"] = aggA20["total_intervals"] == 200010000 and aggA20["ranges_contiguous"] \
    and aggA20["per_chunk_intervals_ok"] and aggA20["overflow_total"] == 0 \
    and solA20["total_intervals"] == 200010000
C["A_coverage_5000"] = aggA5["total_intervals"] == 12502500 and aggA5["ranges_contiguous"] \
    and aggA5["per_chunk_intervals_ok"]
C["B_coverage_20000"] = aggB["total_intervals"] == 200010000 and aggB["ranges_contiguous"] \
    and aggB["per_chunk_intervals_ok"] and aggBfull["coverage_ok"]
C["A_stats_match_solutions"] = aggA20["stats"] == solA20["sweep_stats_totals"] and \
    aggA5["stats"] == solA5["sweep_stats_totals"]
C["B_stats_match_aggregate"] = aggB["stats"] == aggBfull["stats"]
C["B_gate_stats_match_aggregate_gate"] = aggBgate["stats"]["intervals"] == 12502500

# ---------- Timings (from JSON records only) ----------
C["A_gate_timing"] = {"chunk_sums": [aggA5["sweep_seconds_sum"], aggA5["verify_seconds_sum"],
                                     aggA5["compute_seconds_sum"]],
                      "solutions_fields": [solA5["compute_seconds_from_chunks"],
                                           solA5["last_run_wall_seconds"]],
                      "match_4.12_within_chunk_rounding":
                          abs(aggA5["compute_seconds_sum"] - 4.12) <= 0.005 and
                          solA5["compute_seconds_from_chunks"] == 4.12,
                      "record_note": "solutions_n5000 last_run_wall_seconds=0.07 is the "
                                     "resume run; the original 4.25 s gate wall is prose-only"}
C["A_full_timing"] = {"chunk_sums": [aggA20["sweep_seconds_sum"], aggA20["verify_seconds_sum"],
                                     aggA20["compute_seconds_sum"]],
                      "solutions_fields": [solA20["compute_seconds_from_chunks"],
                                           solA20["last_run_wall_seconds"]],
                      "match_105.65": aggA20["compute_seconds_sum"] == solA20["compute_seconds_from_chunks"] == 105.65}
C["B_gate_timing"] = {"chunk_sum_first20": aggB["gate_seconds_sum_first20"],
                      "aggregate_gate_field": aggBgate["total_seconds_sum_of_chunks"]}
C["B_full_timing"] = {"chunk_sum": aggB["seconds_sum"],
                      "aggregate_full_field": aggBfull["total_seconds_sum_of_chunks"]}

# ---------- Near-miss / solution exact re-verification from definitions ----------
exact = []
for (a, b, Bc, c, res) in EXPECTED_NEAR:
    H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
    exact.append({"ab": (a, b), "AB": (H.numerator, H.denominator),
                  "B_ok": H.denominator == Bc, "A_ok": H.numerator % Bc == dict(
                      {(4, 7): 319, (5, 7): 107, (9, 12): 763, (154, 156): 36037})[(a, b)],
                  "residue": (H.numerator + 2 * c + 1) % Bc,
                  "residue_ok": (H.numerator + 2 * c + 1) % Bc == res,
                  "sum": str(H + Fraction(2 * c + 1, Bc)),
                  "sum_noninteger": (H + Fraction(2 * c + 1, Bc)).denominator != 1})
R["details"]["nearmiss_exact"] = exact
C["nearmiss_exact_all_ok"] = all(x["B_ok"] and x["A_ok"] and x["residue_ok"]
                                 and x["sum_noninteger"] for x in exact)
sol_exact = []
for (a, b, m) in EXPECTED_SING:
    H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
    sol_exact.append({"abm": (a, b, m), "H": str(H), "ok": (H + Fraction(1, m)).denominator == 1})
R["details"]["singleton_exact"] = sol_exact
C["singleton_exact_all_ok"] = all(x["ok"] for x in sol_exact)

# ---------- Independence: file hashes / shared files ----------
def tree_hashes(d):
    out = {}
    for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isfile(p) and "__pycache__" not in p and not p.endswith((".so", ".pyc")):
            out[os.path.relpath(p, d)] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return out
hA = tree_hashes(os.path.join(ROOT, "code", "c1-implA"))
hB = tree_hashes(os.path.join(ROOT, "code", "c1-implB"))
R["details"]["shared_basenames_A_B"] = sorted(set(hA) & set(hB))
R["details"]["identical_content_files_A_B"] = sorted(
    n for n in set(hA) & set(hB) if hA[n] == hB[n])
code_shared = [n for n in set(hA) & set(hB)
               if n.endswith((".py", ".c", ".sh", ".h"))]
R["details"]["shared_code_files_A_B"] = code_shared
C["no_shared_code_files_A_B"] = not code_shared and \
    not [n for n in set(hA) & set(hB) if hA[n] == hB[n]]

R["all_core_checks_passed"] = all(v for k, v in C.items() if isinstance(v, bool))
with open(os.path.join(HERE, "verifier_c1_compare_results.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
print(json.dumps(C, indent=1, default=str))
print("all_core_checks_passed:", R["all_core_checks_passed"])
