#!/usr/bin/env python3
"""census2.py -- Erdős #288, Cluster C0, Implementation 2 (prime-by-prime).

Tasks
  (i)   singleton census for all 1 <= a <= b <= 1600;
  (ii)  singleton extension to b <= 2000 with disjoint classification (B > b);
  (iii) L = 2 disjoint branch for b <= 2000: pairs [a,b], [c,c+1], b < c,
        with H(a,b) + H(c,c+1) in Z.

Method (no global fraction arithmetic anywhere in the census pipeline)
-----------------------------------------------------------------------
For each prime p <= b and interval [a,b] the engine tracks, prime by prime,
  V_p = max v_p(n) over the interval, and
  S_p = (p^{V_p} H(a,b)) mod p^{V_p+1}   (a p-adic residue),
updated by the transition rules proved in prime_kernel.c's header:
  v = v_p(new n), w = (n/p^v)^{-1} mod p^{v+1}:
    v <= V_p:  S_p += p^{V_p-v} w (mod p^{V_p+1});
    v >  V_p:  S_p = p^{v-V_p} S_p_old + w (mod p^{v+1}), V_p := v.
From (V_p, S_p): t = v_p(S_p); e_p = V_p - t if t < V_p else 0 (the exponent
of p in the reduced denominator B = prod p^{e_p}); u_p = (S_p/p^t) mod p^{e_p}
(the unit part, p^{e_p} H(a,b) = u_p in Z_(p)).  The singleton condition
A = -1 (mod B) is the conjunction of u_p * R_p = -1 (mod p^{e_p}) over p,
with R_p = (B/p^{e_p}) mod p^{e_p}, assembled CRT-wise in the verification
stage (prime_ref.crt_A) from per-prime data recomputed from scratch.

Sparsity used by the sweep: e_p, u_p (hence B) can change only when the new
term's index is divisible by p, so B changes only at sparse "delta events";
there the sweep updates R_f for a filter set of primes {2,3,5,7,11} and
B modulo twelve auxiliary primes > 2000 (used only as an exact necessary
quadratic-residue prefilter for the pronic condition B = c(c+1): if
B = c(c+1) then 4B+1 = (2c+1)^2 must be a square modulo every modulus).
Intervals passing the filter-prime singleton conditions, resp. the QR
prefilter, are candidates; EVERY candidate is then re-derived from scratch
(pk_interval: fixed-V strata sum, a different accumulation path), assembled
with Python big integers, and decided exactly.  The self-tests below
validate the filter state (R_f and B-residues) directly against scratch
factorisations on sampled intervals up to b = 2000, validate the whole
pipeline exhaustively against scratch verification for all b <= 120, and
validate the pure-Python prime_ref implementation against Fraction spot
checks on tiny intervals (b <= 40; the only Fraction use anywhere).

L = 2 exhaustiveness: H(c,c+1) = (2c+1)/(c(c+1)) is already in lowest
terms.  If H(a,b) = A/B (lowest terms) and the sum is integral, comparing
the two denominators after writing both over gcd(B, c(c+1)) shows each
"gcd-free part" must be 1 (the combined numerator is coprime to each), so
B = c(c+1) is FORCED, and then integrality is A + 2c + 1 = 0 (mod B).
Thus c is determined by B via integer square root; enumerating all
[a,b] with b <= 2000 and testing B for being pronic with root c > b,
plus the congruence, misses no c (bounded or not).

Checkpointing: the sweep runs in chunks of a-values; each chunk's
candidate lists and stats are written to outputs/chunk_*.json before the
next chunk starts, and verification likewise per chunk
(outputs/verify_*.json).  Re-running resumes from existing chunk files.
"""

import argparse
import ctypes
import json
import os
import random
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
sys.path.insert(0, HERE)
import prime_ref  # noqa: E402

EXPECTED_SINGLETONS = [(1, 1, 1), (1, 2, 2), (1, 3, 6),
                       (2, 2, 2), (2, 3, 6), (3, 6, 20)]
EXPECTED_DISJOINT = [(1, 3, 6), (2, 3, 6), (3, 6, 20)]

# --------------------------------------------------------------------------
# C kernel loading
# --------------------------------------------------------------------------
_lib = None
NP = 0
PRIMES = []
FILTER_PRIMES = []
QR_MODS = []


def load_kernel():
    global _lib, NP, PRIMES, FILTER_PRIMES, QR_MODS
    if _lib is not None:
        return _lib
    src = os.path.join(HERE, "prime_kernel.c")
    so = os.path.join(HERE, "prime_kernel.so")
    if (not os.path.exists(so)) or os.path.getmtime(src) > os.path.getmtime(so):
        cmd = ["gcc", "-O3", "-std=c11", "-shared", "-fPIC", src, "-o", so]
        print("[build]", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)
    lib = ctypes.CDLL(so)
    lib.pk_init.restype = ctypes.c_int
    lib.pk_init.argtypes = [ctypes.c_int]
    lib.pk_interval.argtypes = [ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(ctypes.c_uint8),
                                ctypes.POINTER(ctypes.c_uint32)]
    lib.pk_debug_state.argtypes = [ctypes.c_int, ctypes.c_int,
                                   ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.POINTER(ctypes.c_uint32),
                                   ctypes.POINTER(ctypes.c_uint32),
                                   ctypes.POINTER(ctypes.c_uint32)]
    lib.pk_sweep_chunk.restype = ctypes.c_int
    lib.pk_sweep_chunk.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                   ctypes.POINTER(ctypes.c_uint16), ctypes.c_uint64,
                                   ctypes.POINTER(ctypes.c_uint16), ctypes.c_uint64,
                                   ctypes.POINTER(ctypes.c_uint64)]
    lib.pk_get_qr_mods.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
    lib.pk_get_filter_primes.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
    NP = lib.pk_init(2000)
    assert NP > 0
    PRIMES.extend(prime_ref.sieve_primes(2000))
    assert len(PRIMES) == NP
    buf = (ctypes.c_uint32 * 5)()
    lib.pk_get_filter_primes(buf)
    FILTER_PRIMES.extend(int(x) for x in buf)
    buf2 = (ctypes.c_uint32 * 12)()
    lib.pk_get_qr_mods(buf2)
    QR_MODS.extend(int(x) for x in buf2)
    _lib = lib
    return lib


def kernel_interval(a, b):
    """Per-prime data {p: (e, u)} for [a,b], computed from scratch by the
    kernel's fixed-V strata sum (not the incremental sweep path)."""
    lib = load_kernel()
    e_arr = np.zeros(NP, dtype=np.uint8)
    u_arr = np.zeros(NP, dtype=np.uint32)
    lib.pk_interval(a, b,
                    e_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                    u_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)))
    return {PRIMES[i]: (int(e_arr[i]), int(u_arr[i]))
            for i in range(NP) if PRIMES[i] <= b}


def kernel_debug_state(a, b):
    lib = load_kernel()
    e_arr = np.zeros(NP, dtype=np.uint8)
    u_arr = np.zeros(NP, dtype=np.uint32)
    rf_arr = np.zeros(len(FILTER_PRIMES), dtype=np.uint32)
    bres_arr = np.zeros(len(QR_MODS), dtype=np.uint32)
    lib.pk_debug_state(a, b,
                       e_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                       u_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),
                       rf_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),
                       bres_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)))
    data = {PRIMES[i]: (int(e_arr[i]), int(u_arr[i]))
            for i in range(NP) if PRIMES[i] <= b}
    return data, [int(x) for x in rf_arr], [int(x) for x in bres_arr]


def verify_from_data(a, b, data):
    """Exact combined verification of one interval from per-prime data.
    Returns a record dict (big integers as Python ints)."""
    res, B = prime_ref.a_residues(data)
    A_mod_B, _ = prime_ref.crt_A(data, B)
    single_local = all(res[p] == p ** data[p][0] - 1 for p in res)
    single = single_local and (B == 1 or A_mod_B == B - 1)
    from math import isqrt
    c = isqrt(B)
    pronic = (c * (c + 1) == B)
    l2 = {"pronic": pronic, "c": c if pronic else None,
          "c_gt_b": bool(pronic and c > b), "congruence": False,
          "is_solution": False}
    if pronic and c > b:
        cong = (A_mod_B + 2 * c + 1) % B == 0
        l2["congruence"] = cong
        l2["is_solution"] = cong
    return {"a": a, "b": b, "B": B, "A_mod_B": A_mod_B,
            "singleton": single, "l2": l2,
            "n_active_primes": len(res)}


# --------------------------------------------------------------------------
# Self-tests
# --------------------------------------------------------------------------
def self_test():
    t0 = time.time()
    report = {}
    # (1) pure-Python prime_ref vs Fraction spot checks, tiny intervals only
    primes40 = prime_ref.sieve_primes(40)
    n_checked = 0
    for a in range(1, 41):
        for b in range(a, 41):
            data = prime_ref.prime_data(a, b, primes40)
            num, den = prime_ref.fraction_spot_check(a, b)
            A_mod_B, B = prime_ref.crt_A(data)
            assert B == den, (a, b, B, den)
            assert A_mod_B == num % den, (a, b)
            n_checked += 1
    report["fraction_spot_intervals_b<=40"] = n_checked

    # (2) kernel scratch vs pure-Python prime_ref, all intervals b <= 100
    primes100 = prime_ref.sieve_primes(100)
    n2 = 0
    for a in range(1, 101):
        for b in range(a, 101):
            kd = kernel_interval(a, b)
            pd = prime_ref.prime_data(a, b, primes100)
            for p in pd:
                assert kd[p] == pd[p], (a, b, p, kd[p], pd[p])
            n2 += 1
    report["kernel_vs_pythonref_intervals_b<=100"] = n2

    # (3) exhaustive scratch verification for all b <= 120 (both branches),
    #     compared against the candidate pipeline restricted to b <= 120.
    sols_single, sols_l2, pronic_set = [], [], set()
    for a in range(1, 121):
        for b in range(a, 121):
            rec = verify_from_data(a, b, kernel_interval(a, b))
            if rec["singleton"]:
                sols_single.append((a, b, rec["B"]))
            if rec["l2"]["is_solution"]:
                sols_l2.append((a, b, rec["l2"]["c"]))
            if rec["l2"]["pronic"]:
                pronic_set.add((a, b))
    assert sols_single == EXPECTED_SINGLETONS, sols_single
    assert sols_l2 == [], sols_l2
    report["exhaustive_b<=120_singletons"] = sols_single
    report["exhaustive_b<=120_l2_solutions"] = sols_l2
    report["exhaustive_b<=120_pronic_intervals"] = sorted(pronic_set)

    # candidate sweep at N=120, then exact verification of candidates only:
    cand_s, cand_l, stats = sweep_chunk_inmemory(1, 120, 120)
    ver_s, ver_l = [], []
    cand_pairs = sorted(set(cand_s) | set(cand_l))
    for (a, b) in cand_pairs:
        rec = verify_from_data(a, b, kernel_interval(a, b))
        if rec["singleton"]:
            ver_s.append((a, b, rec["B"]))
        if rec["l2"]["is_solution"]:
            ver_l.append((a, b, rec["l2"]["c"]))
    assert ver_s == sols_single and ver_l == sols_l2, (ver_s, ver_l)
    # every pronic interval must have passed the QR prefilter:
    assert pronic_set.issubset(set(cand_l)), pronic_set - set(cand_l)
    report["sweep_N120_stats"] = stats
    report["sweep_N120_single_candidates"] = len(cand_s)
    report["sweep_N120_l2_candidates"] = len(cand_l)

    # (4) incremental state (e, u, R_f, B-residues) vs scratch factorisation
    #     on sampled intervals up to b = 2000.
    rng = random.Random(20261030)
    samples = [(1, 1), (1, 2), (3, 6), (1, 2000), (1999, 2000), (1024, 1024)]
    for _ in range(300):
        a = rng.randint(1, 2000)
        b = rng.randint(a, min(2000, a + rng.randint(0, 600)))
        samples.append((a, b))
    for (a, b) in samples:
        data, rf, bres = kernel_debug_state(a, b)
        sdata = kernel_interval(a, b)
        for p in sdata:
            assert data[p] == sdata[p], (a, b, p, data[p], sdata[p])
        _res, B = prime_ref.a_residues(data)
        for fi, f in enumerate(FILTER_PRIMES):
            e_f = data[f][0] if f <= b else 0
            if e_f > 0:
                q = f ** e_f
                assert rf[fi] == (B // q) % q, (a, b, f, rf[fi], (B // q) % q)
            else:
                assert rf[fi] == 0, (a, b, f, rf[fi])
        for j, m in enumerate(QR_MODS):
            assert bres[j] == B % m, (a, b, m, bres[j], B % m)
    report["debug_state_samples"] = len(samples)
    report["self_test_seconds"] = round(time.time() - t0, 2)
    return report


def sweep_chunk_inmemory(a0, a1, N):
    lib = load_kernel()
    n_intervals = sum(N - a + 1 for a in range(a0, a1 + 1))
    out_s = np.zeros(2 * n_intervals, dtype=np.uint16)
    out_l = np.zeros(2 * n_intervals, dtype=np.uint16)
    stats = np.zeros(6, dtype=np.uint64)
    lib.pk_sweep_chunk(a0, a1, N,
                       out_s.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16)),
                       np.uint64(n_intervals),
                       out_l.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16)),
                       np.uint64(n_intervals),
                       stats.ctypes.data_as(ctypes.POINTER(ctypes.c_uint64)))
    st = {"intervals": int(stats[0]), "delta_events": int(stats[1]),
          "changed_prime_records": int(stats[2]),
          "single_filter_passes": int(stats[3]),
          "l2_filter_passes": int(stats[4]), "overflow": int(stats[5])}
    assert st["overflow"] == 0
    assert st["single_filter_passes"] == int(stats[3])
    ns, nl = st["single_filter_passes"], st["l2_filter_passes"]
    cand_s = [(int(out_s[2 * i]), int(out_s[2 * i + 1])) for i in range(ns)]
    cand_l = [(int(out_l[2 * i]), int(out_l[2 * i + 1])) for i in range(nl)]
    return cand_s, cand_l, st


# --------------------------------------------------------------------------
# Main pipeline (checkpointed)
# --------------------------------------------------------------------------
def chunk_name(a0, a1, N):
    return os.path.join(OUT, f"chunk_a{a0:04d}_{a1:04d}_n{N}.json")


def verify_name(a0, a1, N):
    return os.path.join(OUT, f"verify_a{a0:04d}_{a1:04d}_n{N}.json")


def run(N=2000, chunk=100, force=False):
    os.makedirs(OUT, exist_ok=True)
    load_kernel()
    t_all = time.time()
    chunks = []
    a = 1
    while a <= N:
        chunks.append((a, min(N, a + chunk - 1)))
        a += chunk
    total_intervals = 0
    comp_seconds = 0.0  # summed per-chunk sweep+verify compute (resume-safe)
    tot_stats = {"delta_events": 0, "changed_prime_records": 0,
                 "single_filter_passes": 0, "l2_filter_passes": 0}
    all_single_sols, all_l2_sols = [], []
    all_pronic = []
    cand_totals = {"single": 0, "l2": 0, "union": 0}
    for (a0, a1) in chunks:
        cpath = chunk_name(a0, a1, N)
        if os.path.exists(cpath) and not force:
            with open(cpath) as fh:
                cdat = json.load(fh)
        else:
            t0 = time.time()
            cand_s, cand_l, st = sweep_chunk_inmemory(a0, a1, N)
            cdat = {"a0": a0, "a1": a1, "N": N, "stats": st,
                    "single_candidates": cand_s, "l2_candidates": cand_l,
                    "sweep_seconds": round(time.time() - t0, 3)}
            with open(cpath + ".tmp", "w") as fh:
                json.dump(cdat, fh)
            os.replace(cpath + ".tmp", cpath)
        comp_seconds += cdat.get("sweep_seconds", 0.0)
        total_intervals += cdat["stats"]["intervals"]
        for k in tot_stats:
            tot_stats[k] += cdat["stats"][k]
        cand_totals["single"] += len(cdat["single_candidates"])
        cand_totals["l2"] += len(cdat["l2_candidates"])
        # verification of this chunk's candidates (checkpointed separately)
        vpath = verify_name(a0, a1, N)
        if os.path.exists(vpath) and not force:
            with open(vpath) as fh:
                vdat = json.load(fh)
            cand_totals["union"] += vdat["candidates_verified"]
        else:
            t0 = time.time()
            pairs = sorted(set(map(tuple, cdat["single_candidates"])) |
                           set(map(tuple, cdat["l2_candidates"])))
            cand_totals["union"] += len(pairs)
            s_sols, l_sols, pron = [], [], []
            for (aa, bb) in pairs:
                rec = verify_from_data(aa, bb, kernel_interval(aa, bb))
                if rec["singleton"]:
                    s_sols.append({"a": aa, "b": bb, "m": str(rec["B"]),
                                   "B": str(rec["B"]),
                                   "A_mod_B": str(rec["A_mod_B"]),
                                   "disjoint": bool(rec["B"] > bb)})
                if rec["l2"]["pronic"]:
                    pron.append({"a": aa, "b": bb, "B": str(rec["B"]),
                                 "c": rec["l2"]["c"],
                                 "c_gt_b": rec["l2"]["c_gt_b"],
                                 "congruence": rec["l2"]["congruence"],
                                 "is_solution": rec["l2"]["is_solution"]})
                if rec["l2"]["is_solution"]:
                    l_sols.append({"a": aa, "b": bb, "c": rec["l2"]["c"],
                                   "B": str(rec["B"])})
            vdat = {"a0": a0, "a1": a1, "N": N,
                    "candidates_verified": len(pairs),
                    "singleton_solutions": s_sols, "l2_solutions": l_sols,
                    "pronic_candidates": pron,
                    "verify_seconds": round(time.time() - t0, 3)}
            with open(vpath + ".tmp", "w") as fh:
                json.dump(vdat, fh)
            os.replace(vpath + ".tmp", vpath)
        comp_seconds += vdat.get("verify_seconds", 0.0)
        all_single_sols.extend(vdat["singleton_solutions"])
        all_l2_sols.extend(vdat["l2_solutions"])
        all_pronic.extend(vdat["pronic_candidates"])
        with open(os.path.join(OUT, "progress.json"), "w") as fh:
            json.dump({"N": N, "completed_a_up_to": a1,
                       "intervals_so_far": total_intervals,
                       "elapsed_seconds": round(time.time() - t_all, 2)}, fh)
        print(f"[chunk a={a0}-{a1}] intervals so far {total_intervals}, "
              f"single sols {len(all_single_sols)}, l2 sols {len(all_l2_sols)}",
              flush=True)
    summary = {
        "N": N,
        "total_intervals": total_intervals,
        "sweep_stats_totals": tot_stats,
        "candidate_totals": cand_totals,
        "singleton_solutions_all_b<=N": all_single_sols,
        "singleton_solutions_b<=1600":
            [s for s in all_single_sols if s["b"] <= 1600],
        "l2_solutions": all_l2_sols,
        "pronic_candidates_all": all_pronic,
        "pronic_with_c_gt_b":
            [p for p in all_pronic if p["c_gt_b"]],
        "compute_seconds_from_chunks": round(comp_seconds, 2),
        "total_seconds": round(comp_seconds, 2),
        "last_run_wall_seconds": round(time.time() - t_all, 2),
    }
    with open(os.path.join(OUT, "solutions.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--self-test-only", action="store_true")
    ap.add_argument("--skip-self-test", action="store_true")
    args = ap.parse_args()
    load_kernel()
    if not args.skip_self_test:
        rep = self_test()
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "selftest.json"), "w") as fh:
            json.dump(rep, fh, indent=1, default=str)
        print("[self-test] PASS", json.dumps(
            {k: v for k, v in rep.items() if not isinstance(v, list)},
            default=str), flush=True)
        if args.self_test_only:
            return
    summary = run(N=args.n, chunk=args.chunk, force=args.force)
    print(json.dumps({k: summary[k] for k in
                      ("N", "total_intervals", "candidate_totals",
                       "total_seconds")}, indent=1))
    print("singleton solutions:", summary["singleton_solutions_all_b<=N"])
    print("l2 solutions:", summary["l2_solutions"])


if __name__ == "__main__":
    main()
