#!/usr/bin/env python3
"""Independent exact verification of every candidate produced by the
C engine (Implementation B).  Method, independent of engine.c:
for an interval [a,b], let D = lcm(a..b) (built from prime powers),
X = sum_{n=a}^b D // n; then H(a,b) = X/D, reduced by gcd(X, D).
No code or state from the engine is reused.
"""
import json, sys, glob
from math import gcd

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i, v in enumerate(sieve) if v]

PRIMES = primes_upto(20000)

def interval_frac(a, b):
    D = 1
    for p in PRIMES:
        if p > b:
            break
        # largest power of p dividing some n in [a,b]: use exponent of
        # the max prime power <= b that has a multiple in [a,b].
        # Simpler exact route: exponent = max v_p(n) over n in [a,b].
        e = 0
        pp = p
        while pp <= b:
            # does [a,b] contain a multiple of pp?
            first = ((a + pp - 1) // pp) * pp
            if first <= b:
                e += 1
                if pp > b // p:
                    break
                pp *= p
            else:
                break
        if e:
            D *= p ** e
    X = 0
    for n in range(a, b + 1):
        X += D // n
    g = gcd(X, D)
    return X // g, D // g

def main(paths):
    cand = []
    nms = []
    for path in paths:
        with open(path) as f:
            data = json.load(f)
        cand += [(c["a"], c["b"], c["t"]) for c in data["singleton_candidates"]]
        nms += [(x["a"], x["b"], x["c"]) for x in data["l2_nearmisses"]]
    cand = sorted(set(cand))
    nms = sorted(set(nms))
    sing_out = []
    for a, b, t in cand:
        A, B = interval_frac(a, b)
        ok = (A % B == B - 1)
        tt = (A + 1) // B if ok else None
        sing_out.append({
            "a": a, "b": b, "m": B, "is_solution": ok,
            "t_engine": t, "t_exact": tt, "disjoint": B > b,
            "A_mod_check": A % B,
        })
    nm_out = []
    for a, b, c in nms:
        A, B = interval_frac(a, b)
        den_ok = (B == c * (c + 1))
        # H(a,b) + H(c,c+1) = A/B + (2c+1)/B when den_ok
        s_num = A + (2 * c + 1)
        is_sol = den_ok and (s_num % B == 0)
        nm_out.append({
            "a": a, "b": b, "c": c, "B": B, "A": A,
            "denominator_condition": den_ok,
            "residue_A_plus_2c_plus_1_mod_B": s_num % B if den_ok else None,
            "is_solution": is_sol,
        })
    result = {
        "singleton_candidates_verified": sing_out,
        "all_singleton_candidates_are_solutions": all(x["is_solution"] for x in sing_out),
        "l2_nearmisses_verified": nm_out,
        "l2_solutions": [x for x in nm_out if x["is_solution"]],
    }
    print(json.dumps(result, indent=1))

if __name__ == "__main__":
    main(sys.argv[1:])
