#!/usr/bin/env python3
"""Smoothness-defect quantification for F2 (size) survivors.

Re-runs the partition enumeration for one (b, eps) with the same code
path as redteam_search.py, but for every directed candidate passing
F2 (u0,u1 <= Bb) computes, for each u in {u0,u1}, the Bb-rough part
    rough(u) = u with, for every prime p <= zb, the factor p^{min(v_p(u), e_p)}
               divided out   (e_p = max exponent with p^{e_p} <= b),
so u | Bb iff rough(u) = 1.  Candidate defect = max(log rough(u0), log rough(u1)).
Reports the minimum defect over all F2 survivors and the count of F2
survivors with defect <= thresholds 1,2,5,10.  This measures by what
margin the smoothness filter F3 kills the size survivors.
"""
import argparse, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redteam_search import primes_upto, max_prime_power_exp, solve_direct

def rough_log(u, caps):
    t = u
    removed = 0.0
    for p, cap in caps:
        if t == 1:
            break
        cnt = 0
        while cnt < cap and t % p == 0:
            t //= p
            cnt += 1
            removed += math.log(p)
    return math.log(t) if t > 1 else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--b", type=int, required=True)
    ap.add_argument("--eps", type=float, required=True)
    args = ap.parse_args()
    b, eps = args.b, args.eps
    ps = primes_upto(b)
    zb = b / ((1 - eps) * math.log(b))
    large = [p for p in ps if p > zb]
    caps = [(p, max_prime_power_exp(p, b)) for p in ps if p <= zb]
    Bb = 1
    for p, e in caps:
        Bb *= p ** e
    Ptot = 1
    for p in large:
        Ptot *= p
    N = len(large)
    p_star = large[-1]
    free = large[:-1]
    logs = [math.log(p) for p in free]
    S = sum(math.log(p) for p in large)
    lsum = math.log(p_star)
    thresh = math.log(Bb) + 1.0
    A = p_star
    prev_g = 0
    in_A = [False] * len(free)
    f2 = 0
    min_defect = None
    min_rec = None
    buckets = {1: 0, 2: 0, 5: 0, 10: 0}
    for i in range(1 << (N - 1)):
        if i:
            g = i ^ (i >> 1)
            diff = g ^ prev_g
            prev_g = g
            bit = diff.bit_length() - 1
            if (g >> bit) & 1:
                A *= free[bit]; lsum += logs[bit]; in_A[bit] = True
            else:
                A //= free[bit]; lsum -= logs[bit]; in_A[bit] = False
        B = Ptot // A
        if abs(2 * lsum - S) > thresh:
            continue
        if A == 1 or B == 1:
            directed = [(A, B, *solve_direct(A, B)), (B, A, *solve_direct(B, A))]
        else:
            u0, u1 = solve_direct(A, B)
            directed = [(A, B, u0, u1), (B, A, A - u1, B - u0)]
        for P0, P1, u0, u1 in directed:
            if u0 <= Bb and u1 <= Bb:
                f2 += 1
                d = max(rough_log(u0, caps), rough_log(u1, caps))
                for t in buckets:
                    if d <= t:
                        buckets[t] += 1
                if min_defect is None or d < min_defect:
                    min_defect = d
                    min_rec = dict(P0=str(P0), P1=str(P1), u0=str(u0), u1=str(u1),
                                   c=str(P0 * u0), defect_log=d)
    out = dict(b=b, eps=eps, zb=zb, N=N, f2_recomputed=f2,
               min_defect_log=min_defect, min_defect_rec=min_rec,
               defect_bucket_counts={str(k): v for k, v in buckets.items()})
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, f"redteam_defect_{b}_{eps}.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
