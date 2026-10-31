#!/usr/bin/env python3
"""Red Team (b) large-b: sampled strip intervals at large b.
Predicate per prime l in (b/4,b/2) computed LITERALLY (multiples,
cofactors, T_l mod l) for b=10007 (all strip a) and b=100000
(sampled a); for b >= 999983 the exactly-equivalent reduced
predicate (invalid iff b/3 < l < a/2; see redteam_strip_bisect.py)
is used via bisect on a prime list."""
import random
from bisect import bisect_left, bisect_right
from math import isqrt

def primes_upto(n):
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]: s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

def prime_valid_literal(a, b, l):
    cofs = []
    k = -(-a // l)
    while k * l <= b:
        cofs.append(k); k += 1
    if not cofs: return False
    if not all(c in (2, 3) for c in cofs): return False
    if l * l <= b or l % 2 == 0: return False
    T = 0
    for k in cofs: T = (T + pow(k, -1, l)) % l
    return T != 0

random.seed(288)
tested = 0; bad = 0; invalid_pairs = 0
for b in [10007, 100000]:
    P = primes_upto(b // 2)
    primes = [l for l in P if b / 4 < l < b / 2]
    amin, amax = b // 2 + 1, (2 * b + 1) // 3
    avals = list(range(amin, amax + 1))
    if len(avals) > 300: avals = random.sample(avals, 300)
    for a in avals:
        tested += 1; nvalid = 0
        for l in primes:
            if prime_valid_literal(a, b, l): nvalid += 1
            else: invalid_pairs += 1
        if nvalid == 0: bad += 1; print(f"  NO VALID PRIME at ({a},{b})")
    print(f"b={b} literal: primes in range: {len(primes)}, strip a tested: {len(avals)}")
for b in [999983, 10**6, 1234567, 10**7, 10**8]:
    P = primes_upto(b // 2)
    def nprimes(x, y):
        return bisect_left(P, y) - bisect_right(P, x) if y > x else 0
    tot_range = nprimes(b / 4, b / 2)
    amin, amax = b // 2 + 1, (2 * b + 1) // 3
    avals = [amin, amin + 1, (amin + amax) // 2, amax - 1, amax]
    avals += [random.randint(amin, amax) for _ in range(200)]
    for a in avals:
        tested += 1
        ninv = nprimes(b / 3, a / 2)
        invalid_pairs += ninv
        if ninv == tot_range: bad += 1; print(f"  NO VALID PRIME at ({a},{b})")
    print(f"b={b} reduced: primes in range: {tot_range}, strip a tested: {len(avals)}")
print(f"large-b total: {tested} strip intervals, no-valid-prime: {bad}, invalid (prime,interval) pairs: {invalid_pairs}")
