#!/usr/bin/env python3
"""Auditor 1 (Cluster A, Cycle 1) exact checks for Nayak Thm 3.2 / Lemma 3.1.
All arithmetic exact via fractions.Fraction. No floating point for verdicts.
"""
from fractions import Fraction
from math import isqrt
import itertools

def H(u, v):
    return sum((Fraction(1, n) for n in range(u, v+1)), Fraction(0))

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    r = isqrt(n)
    for d in range(3, r+1, 2):
        if n % d == 0: return False
    return True

def primes_upto(N):
    return [n for n in range(2, N+1) if is_prime(n)]

# --- 1. The four listed pairs ---
print("=== Four listed pairs ===")
pairs = [((1,1),(1,1)), ((1,2),(1,2)), ((1,2),(2,2)), ((2,2),(2,2))]
for (a,b),(c,d) in pairs:
    s = H(a,b)+H(c,d)
    print(f"  ( [{a},{b}], [{c},{d}] ): H1={H(a,b)} H2={H(c,d)} sum={s} integer={s.denominator==1}")

# The extra intersecting pair with union [1,2] NOT in the list:
print("=== Extra union-[1,2] intersecting pair (must be non-integer) ===")
s = H(1,2)+H(1,1)
print(f"  ([1,2],[1,1]): sum={s} integer={s.denominator==1}")
# Disjoint pair with union [1,2] (excluded by intersecting hypothesis):
s = H(1,1)+H(2,2)
print(f"  ([1,1],[2,2]) disjoint: sum={s} integer={s.denominator==1}")

# 2/r integrality for length-1 unions
print("=== 2/r ===")
for r in range(1, 11):
    v = Fraction(2, r)
    print(f"  r={r}: 2/r={v} integer={v.denominator==1}")

# --- 2. Lemma 3.1 brute check: s>=3, N>=2, exists ODD prime dividing exactly one n in [r,s] ---
print("=== Lemma 3.1 brute check, 1<=r<=s<=200, s>=3, N>=2 ===")
failures = []
for s_ in range(3, 201):
    for r_ in range(1, s_):  # N>=2
        ok = False
        for p in primes_upto(s_):
            if p == 2: continue
            cnt = sum(1 for n in range(r_, s_+1) if n % p == 0)
            if cnt == 1:
                ok = True; break
        if not ok:
            failures.append((r_, s_))
print(f"  failures: {failures if failures else 'NONE'} (checked {sum(1 for s_ in range(3,201) for r_ in range(1,s_))} intervals)")

# Which prime witnesses the third branch s=2r-1 (Bertrand prime in (r,2r))?
print("=== Third branch s=2r-1, r=2..60: Bertrand prime in (r,2r) ===")
bad3 = []
for r_ in range(2, 61):
    cands = [p for p in primes_upto(2*r_-1) if r_ < p < 2*r_]
    if not cands: bad3.append(r_)
    else:
        p = cands[0]
        cnt = sum(1 for n in range(r_, 2*r_) if n % p == 0)
        if cnt != 1 or p % 2 == 0: bad3.append((r_, p, cnt))
print(f"  failures: {bad3 if bad3 else 'NONE'}")

# First branch s=3,4 direct inspection
print("=== s=3,4, r<=s/2: prime 3 divides exactly one ===")
for s_ in (3,4):
    for r_ in range(1, s_+1):
        if r_ <= s_/2 and s_-r_+1 >= 2:
            cnt = sum(1 for n in range(r_, s_+1) if n % 3 == 0)
            print(f"  [{r_},{s_}]: count of multiples of 3 = {cnt}")

# Second branch sanity: Sylvester-Schur witness p>N exists for r>N, small range
print("=== Sylvester-Schur branch sanity, N=2..12, r in (N, N+30] ===")
badSS = []
for N in range(2, 13):
    for r_ in range(N+1, N+31):
        s_ = r_+N-1
        # prime divisors of product
        prod_primes = set()
        for n in range(r_, s_+1):
            m = n
            for p in primes_upto(n):
                if m % p == 0: prod_primes.add(p)
        big = [p for p in prod_primes if p > N]
        if not big: badSS.append((r_, s_, N))
        else:
            p = big[0]
            cnt = sum(1 for n in range(r_, s_+1) if n % p == 0)
            if cnt != 1: badSS.append((r_, s_, N, p, cnt))
print(f"  failures: {badSS if badSS else 'NONE'}")

# --- 3. Brute-force Theorem 3.2 for all intersecting pairs with endpoints <= 30 ---
print("=== Theorem 3.2 brute check: all intersecting interval pairs inside [1,30] ===")
intervals = [(a,b) for a in range(1,31) for b in range(a,31)]
sols = []
for I, J in itertools.product(intervals, repeat=2):
    if max(I[0], J[0]) > min(I[1], J[1]): continue  # disjoint
    ssum = H(*I)+H(*J)
    if ssum.denominator == 1:
        sols.append((I,J,ssum))
print(f"  integer-sum intersecting ordered pairs found: {len(sols)}")
for I,J,v in sols: print(f"    {I} {J} sum={v}")
expected = {((1,1),(1,1)), ((1,2),(1,2)), ((2,2),(1,2)), ((1,2),(2,2)), ((2,2),(2,2))}
found = {(I,J) for I,J,_ in sols}
print(f"  matches expected ordered set (4 unordered / 5 ordered): {found==expected}")

# --- 4. p-adic valuation check of the key step: coefficient 2 at odd p vs p=2 ---
def vp_frac(fr, p):
    # fr is Fraction
    def vp_int(n):
        if n == 0: return 10**9
        e = 0
        while n % p == 0: n //= p; e += 1
        return e
    return vp_int(fr.numerator) - vp_int(fr.denominator)

print("=== Valuation demo: union [2,4], terms mu(n)/n ===")
# I=[2,3], J=[3,4] overlap at 3 -> mu = [1,2,1] on [2,4]; Lemma prime: 3 divides exactly... check p=3? multiples: 3 only. p odd.
mu = {2:1, 3:2, 4:1}
for p in (3,):
    vals = {n: vp_frac(Fraction(mu[n], n), p) for n in mu}
    print(f"  p={p}: valuations {vals}, unique min at n={min(vals, key=vals.get)}, min={min(vals.values())} <0")
print("=== Why p=2 would fail (coefficient 2 cancels): term 2/6 ===")
print(f"  v2(1/3)={vp_frac(Fraction(1,3),2)}, v2(2/6)=v2(1/3)={vp_frac(Fraction(2,6),2)}; "
      f"v2(2/2)={vp_frac(Fraction(2,2),2)} vs v2(1/2)={vp_frac(Fraction(1,2),2)} -- mu=2 raises v2 by 1, can destroy uniqueness/minimality")
print(f"  v3(2/3)={vp_frac(Fraction(2,3),3)} vs v3(1/3)={vp_frac(Fraction(1,3),3)} -- odd p unaffected by mu=2")
