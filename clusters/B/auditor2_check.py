#!/usr/bin/env python3
"""Auditor 2 (Cluster B) computational spot-checks for Erdos #288 singleton case.
Independent of any note: checks the derivation in auditor2.md directly.

Checks:
 1. Dichotomy: for all a<=b<=BMAX and all primes p with p^2>b,
    v_p(H(a,b)) == -1 if good (k>=1, T_p != 0 mod p), >=0 if bad/vacuous.
 2. Task 1: solutions in range are exactly intervals with B | A+1, m=B;
    list all solutions with b<=BMAX.
 3. Worked examples (2,3) and (3,6) in full detail.
 4. Bad-u counts: for primes p and k<p, #bad u <= k-1; u=1,k=2 bad iff p=3;
    u=1,k=3 bad iff p=11 (over primes in range).
 5. Size check: log Q vs b for a=1 and a=floor(b/2), b up to 500.
Exact arithmetic via fractions.Fraction; valuations via factorisation.
"""
from fractions import Fraction
from math import gcd, log
import sys

def primes_upto(n):
    sieve = [True]*(n+1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            sieve[i*i::i] = [False]*len(sieve[i*i::i])
    return [i for i, v in enumerate(sieve) if v]

def vp_int(n, p):
    if n == 0:
        return 10**9
    e = 0
    n = abs(n)
    while n % p == 0:
        n //= p; e += 1
    return e

def vp_frac(fr, p):
    return vp_int(fr.numerator, p) - vp_int(fr.denominator, p)

def Tp_mod(a, b, p):
    """Return (k, u, T_p mod p or None if k=0). T_p in F_p via modular inverses."""
    import math
    u = -(-a // p)  # ceil(a/p)
    last = b // p
    k = last - u + 1
    if k <= 0:
        return 0, None, None
    t = 0
    for j in range(k):
        t = (t + pow(u + j, -1, p)) % p
    return k, u, t

def main():
    BMAX = 200
    primes = primes_upto(2000)
    fails = []
    nchecks = 0
    solutions = []
    for b in range(1, BMAX+1):
        H = Fraction(0)
        # build intervals [a,b] by extending a downward
        for a in range(b, 0, -1):
            H += Fraction(1, a)
            A, B = H.numerator, H.denominator
            if (A + 1) % B == 0:
                solutions.append((a, b, B))
            # dichotomy check for all p with p^2 > b
            for p in primes:
                if p * p <= b:
                    continue
                if p > 2000:
                    break
                # only p <= b can have k>=1; p>b gives k=0 (vacuous, v_p(H)>=0 trivially
                # still check p in (b, ...] cheaply skipped: H denom has no prime > b)
                k, u, t = Tp_mod(a, b, p)
                v = vp_frac(H, p)
                nchecks += 1
                if k == 0:
                    if v < 0:
                        fails.append((a, b, p, 'vacuous but v<0', v))
                elif t != 0:
                    if v != -1:
                        fails.append((a, b, p, 'good but v!=-1', v))
                else:
                    if v < 0:
                        fails.append((a, b, p, 'bad but v<0', v))
                if p > b and k == 0:
                    break  # larger p all vacuous with same conclusion; one representative enough? No:
                    # we break only after checking the first p>b; primes > b all give v>=0 since
                    # denominator of H divides lcm(1..b). Counted once per interval.
    print(f"[1] dichotomy checks performed (incl. one vacuous p>b per interval): {nchecks}")
    print(f"[1] dichotomy failures: {len(fails)}")
    for f in fails[:20]:
        print("    FAIL", f)
    print(f"[2] solutions with b<={BMAX}: {solutions}")

    # Worked example (2,3)
    H23 = sum(Fraction(1, n) for n in range(2, 4))
    print(f"[3] H(2,3) = {H23} = {H23.numerator}/{H23.denominator}, m forced = {H23.denominator}")
    for p in [2, 3]:
        k, u, t = Tp_mod(2, 3, p)
        print(f"    p={p}: k={k} u={u} T_p mod p = {t} -> {'GOOD' if t else 'BAD'}"
              f"  predicted class m = {(-p * pow(t, -1, p)) % (p*p)} mod {p*p}" if t else
              f"    p={p}: k={k} u={u} T_p mod p = {t} -> BAD")
    # Worked example (3,6)
    H36 = sum(Fraction(1, n) for n in range(3, 7))
    print(f"[3] H(3,6) = {H36} = {H36.numerator}/{H36.denominator}, m forced = {H36.denominator}")
    for p in [3, 5]:
        k, u, t = Tp_mod(3, 6, p)
        if t:
            print(f"    p={p}: k={k} u={u} T_p mod p = {t} -> GOOD, class m = {(-p * pow(t, -1, p)) % (p*p)} mod {p*p}")
        else:
            print(f"    p={p}: k={k} u={u} T_p mod p = {t} -> BAD (3 does not divide m=20: {20 % 3 != 0})")

    # Bad-u counts and u=1 small k
    print("[4] bad-u counts (max over p<=500) and u=1 special cases:")
    for k in range(1, 9):
        worst = 0
        for p in primes:
            if p > 500:
                break
            if p <= k:
                continue
            # D(u)=prod(u+j); N=D' ; count roots u in F_p with all u+j != 0
            cnt = 0
            for u in range(p):
                if any((u + j) % p == 0 for j in range(k)):
                    continue
                s = sum(pow(u + j, -1, p) for j in range(k)) % p
                if s == 0:
                    cnt += 1
            worst = max(worst, cnt)
        print(f"    k={k}: max #bad u over p<=500 (p>k) = {worst}  (bound k-1 = {k-1})  ok={worst <= k-1}")
    for k, expected in [(1, []), (2, [3]), (3, [11])]:
        badps = []
        for p in primes:
            if p > 2000:
                break
            if p <= k:
                continue
            s = sum(pow(1 + j, -1, p) for j in range(k)) % p
            if s == 0:
                badps.append(p)
        print(f"    u=1, k={k}: bad primes p<=2000 (p>k): {badps}  expected: {expected}  ok={badps == expected}")

    # Size check
    print("[5] size check: log Q (good primes from full sieve, a=1 and a=b//2):")
    for b in [50, 100, 200, 300, 500]:
        for a in [1, max(1, b // 2)]:
            logQ = 0.0
            for p in primes:
                if p * p <= b:
                    continue
                if p > b:
                    break
                k, u, t = Tp_mod(a, b, p)
                if k >= 1 and t != 0:
                    logQ += 2 * log(p)
            print(f"    b={b} a={a}: log Q = {logQ:.1f}, (log Q)/b = {logQ/b:.3f}")

if __name__ == "__main__":
    main()
