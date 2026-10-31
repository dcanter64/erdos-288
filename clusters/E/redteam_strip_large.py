#!/usr/bin/env python3
"""Red Team (b) large-b sample: for selected large b, test EVERY strip
interval's full prime set in (b/4, b/2) for validity (same def as
redteam_strip.py)."""
import random
from math import isqrt

def primes_upto(n):
    if n < 2: return []
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

def prime_valid(a, b, l):
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
bad = 0; tested = 0; invalid_prime_seen = 0
for b in [10007, 100000, 999983, 10**6, 1234567, 10**7]:
    P = primes_upto(b // 2)
    primes = [l for l in P if b / 4 < l < b / 2]
    amin = b // 2 + 1
    amax = (2 * b + 1) // 3
    # test all strip a for smaller b, sample 300 for larger
    avals = list(range(amin, amax + 1))
    if len(avals) > 300: avals = random.sample(avals, 300)
    for a in avals:
        tested += 1
        nvalid = 0
        for l in primes:
            if prime_valid(a, b, l): nvalid += 1
            else: invalid_prime_seen += 1
        if nvalid == 0:
            bad += 1; print(f"  NO VALID PRIME at (a,b)=({a},{b})")
    print(f"b={b}: primes in (b/4,b/2): {len(primes)}, strip a tested: {len(avals)}")
print(f"large-b sample: {tested} strip intervals, intervals with no valid prime: {bad}, "
      f"invalid (prime,interval) pairs seen: {invalid_prime_seen}")
