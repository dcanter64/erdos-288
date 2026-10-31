#!/usr/bin/env python3
"""Cluster C1 Verifier: independent spot census (third method).

Method (the verifier's own code; shares no decision code with
Implementation A (prime-by-prime (V_p, S_p) + CRT) or Implementation B
(C bignum sweep with transported residues at 1e9-scale moduli)):

For fixed b, sweep a = b, b-1, ..., 1 maintaining the reduced fraction
H(a,b) = A/B exactly as a Python integer pair.  The step from [a+1,b]
to [a,b] (a' = a) forms N' = A*a' + B, M' = B*a'; the step gcd
g' = gcd(N', M') is computed as gcd(N' mod D', D') where
D' = prod_{p|a'} p^{v_p(M')} (every prime dividing g' divides a', and
g' | D' | M').  Decisions per interval:

* Singleton: a sound two-modulus filter first.  Maintained residues
  A mod R, B mod R for the verifier's own primes R1 = 2147483647 and
  R2 = 4294967291 (both > 20000, hence coprime to every A, B, g'; the
  residues are updated with the modular inverse of g', unlike
  Implementation B's Gamma transport).  A solution obeys
  A + 1 = t*B over the integers with t in [1,12] (since
  0 < H(a,b) <= H(1,20000) < 10.49 and t = (A+1)/B <= H + 1), so it
  passes (A + 1) = t*B (mod R) for some t in [1,12] at both moduli.
  Every filter survivor is decided exactly on the formed fraction:
  (A + 1) % B == 0, m = B.
* L = 2: the denominator condition B = c(c+1), c > b, is screened by
  quadratic-residue tests on 4B+1 modulo 64, 3, 5, 7, 11, 13 (from
  B mod m, exact small remainders of the formed B) and Legendre tests
  modulo R1, R2 (from the maintained B residues).  A pronic B passes
  every screen (4B+1 is then a perfect square).  Every survivor is
  decided exactly: s = isqrt(4B+1), s*s == 4B+1, c = (s-1)/2, and for
  c > b the residue (A + 2c + 1) mod B on the formed fraction.

Exact arithmetic only (Python int / math.isqrt / math.gcd).
Ranges: self-test 1..250 (must reproduce the certified six singletons,
the four near-misses, empty L = 2), then the census ranges
2001..3000, 10001..10100, 14951..15050, 19901..20000.
Writes verifier_c1_spot_results.json next to itself.
"""
import json, os, sys, time
from fractions import Fraction
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
NMAX = 20000
R1, R2 = 2147483647, 4294967291

# ---------- sieve / factorisation ----------
spf = list(range(NMAX + 1))
for i in range(2, int(NMAX ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, NMAX + 1, i):
            if spf[j] == j:
                spf[j] = i

def factor_distinct(x):
    out = []
    while x > 1:
        p = spf[x]; e = 0
        while x % p == 0:
            x //= p; e += 1
        out.append((p, e))
    return out

def is_prime_det(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1; r = 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in (2, 7, 61):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

assert is_prime_det(R1) and is_prime_det(R2)
FAC = [factor_distinct(x) if x > 1 else [] for x in range(NMAX + 1)]

SQ64 = {(s * s) % 64 for s in range(64)}
SQSMALL = {p: {(s * s) % p for s in range(p)} for p in (3, 5, 7, 11, 13)}

def census_range(b_lo, b_hi):
    singletons = []; l2_solutions = []; nearmisses = []
    pronic_le = 0; intervals = 0
    sing_filter_passes = 0; l2_screen_passes = 0
    t0 = time.time()
    for b in range(b_lo, b_hi + 1):
        A, B = 1, b
        ep = [0] * (b + 1)
        for (p, e) in FAC[b]:
            ep[p] = e
        A1, B1 = 1 % R1, b % R1
        A2, B2 = 1 % R2, b % R2
        a = b
        while True:
            intervals += 1
            # ---- singleton filter (two moduli), then exact decision ----
            lhs1 = A1 + 1
            if lhs1 >= R1:
                lhs1 -= R1
            ok = False; rhs = 0
            for _t in range(1, 13):
                rhs += B1
                if rhs >= R1:
                    rhs -= R1
                if rhs == lhs1:
                    ok = True; break
            if ok:
                lhs2 = A2 + 1
                if lhs2 >= R2:
                    lhs2 -= R2
                ok = False; rhs = 0
                for _t in range(1, 13):
                    rhs += B2
                    if rhs >= R2:
                        rhs -= R2
                    if rhs == lhs2:
                        ok = True; break
            if ok:
                sing_filter_passes += 1
                if (A + 1) % B == 0:
                    singletons.append((a, b, B))
            # ---- L = 2 pronic screens, then exact decision ----
            if (4 * (B % 64) + 1) % 64 in SQ64:
                passed = True
                for p in (3, 5, 7, 11, 13):
                    if (4 * (B % p) + 1) % p not in SQSMALL[p]:
                        passed = False; break
                if passed:
                    v1 = (4 * B1 + 1) % R1
                    if v1 == 0 or pow(v1, (R1 - 1) // 2, R1) == 1:
                        v2 = (4 * B2 + 1) % R2
                        if v2 == 0 or pow(v2, (R2 - 1) // 2, R2) == 1:
                            l2_screen_passes += 1
                            s = isqrt(4 * B + 1)
                            if s * s == 4 * B + 1:
                                c = (s - 1) // 2
                                if c > b:
                                    res = (A % B + 2 * c + 1) % B
                                    nearmisses.append((a, b, B, c, res))
                                    if res == 0:
                                        l2_solutions.append((a, b, c))
                                else:
                                    pronic_le += 1
            if a == 1:
                break
            a -= 1
            # ---- exact step: [a+1, b] -> [a, b] ----
            Nn = A * a + B
            Pp = B * a
            fac = FAC[a]
            Dp = 1
            for (p, f) in fac:
                Dp *= p ** (ep[p] + f)
            g = gcd(Nn % Dp, Dp) if Dp > 1 else 1
            if g > 1:
                Nn //= g; Pp //= g
                gg = g
                for (p, f) in fac:
                    fv = 0
                    while gg % p == 0:
                        gg //= p; fv += 1
                    ep[p] += f - fv
            else:
                for (p, f) in fac:
                    ep[p] += f
            A, B = Nn, Pp
            if g == 1:
                A1 = (A1 * a + B1) % R1; B1 = B1 * a % R1
                A2 = (A2 * a + B2) % R2; B2 = B2 * a % R2
            else:
                inv1 = pow(g % R1, -1, R1)
                A1 = (A1 * a + B1) * inv1 % R1; B1 = B1 * a * inv1 % R1
                inv2 = pow(g % R2, -1, R2)
                A2 = (A2 * a + B2) * inv2 % R2; B2 = B2 * a * inv2 % R2
    return {"b_range": [b_lo, b_hi], "intervals": intervals,
            "singletons": singletons, "l2_solutions": l2_solutions,
            "nearmisses": nearmisses, "pronic_c_le_b": pronic_le,
            "singleton_filter_passes": sing_filter_passes,
            "l2_screen_passes": l2_screen_passes,
            "seconds": round(time.time() - t0, 2)}

def main():
    out = {"method": "verifier descending exact-fraction sweep, "
                     "R1=2147483647, R2=4294967291 filters, exact decisions",
           "ranges": []}
    # self-test: cross-check formed fractions against Fraction, b <= 40
    for b in range(1, 41):
        A, B = 1, b
        ep = [0] * (b + 1)
        for (p, e) in factor_distinct(b):
            ep[p] = e
        a = b
        while True:
            H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
            assert (A, B) == (H.numerator, H.denominator), (a, b, A, B, H)
            if a == 1:
                break
            a -= 1
            Nn = A * a + B; Pp = B * a
            fac = factor_distinct(a)
            Dp = 1
            for (p, f) in fac:
                Dp *= p ** (ep[p] + f)
            g = gcd(Nn % Dp, Dp) if Dp > 1 else 1
            if g > 1:
                Nn //= g; Pp //= g
                gg = g
                for (p, f) in fac:
                    fv = 0
                    while gg % p == 0:
                        gg //= p; fv += 1
                    ep[p] += f - fv
            else:
                for (p, f) in fac:
                    ep[p] += f
            A, B = Nn, Pp
    out["fraction_crosscheck_b<=40"] = "all intervals match Fraction"
    st = census_range(1, 250)
    out["selftest_1_250"] = st
    assert sorted(st["singletons"]) == [(1, 1, 1), (1, 2, 2), (1, 3, 6),
                                         (2, 2, 2), (2, 3, 6), (3, 6, 20)], st["singletons"]
    assert st["l2_solutions"] == []
    assert sorted((x[0], x[1], x[3]) for x in st["nearmisses"]) == \
        [(4, 7, 20), (5, 7, 14), (9, 12, 44), (154, 156, 1364)], st["nearmisses"]
    assert sorted(x[4] for x in st["nearmisses"]) == [136, 360, 852, 38766]
    assert st["pronic_c_le_b"] == 270
    print("self-test 1..250 OK", st["seconds"], "s", flush=True)
    for (lo, hi) in [(2001, 3000), (10001, 10100), (14951, 15050), (19901, 20000)]:
        r = census_range(lo, hi)
        out["ranges"].append(r)
        print(f"range {lo}..{hi}: intervals={r['intervals']} "
              f"singletons={r['singletons']} l2={r['l2_solutions']} "
              f"nearmisses={r['nearmisses']} pronic_le={r['pronic_c_le_b']} "
              f"({r['seconds']} s)", flush=True)
    with open(os.path.join(HERE, "verifier_c1_spot_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("DONE")

if __name__ == "__main__":
    main()
