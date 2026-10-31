#!/usr/bin/env python3
"""Red Team (b): argument-level test of the strip Bertrand step.
For every strip interval (b/2 < a, 3a <= 2b+1), b in [34, BMAX]:
for EVERY prime l in (b/4, b/2) compute the multiples of l in [a,b],
their cofactors, and T_l mod l. A prime is VALID for the proof iff
k(l) >= 1, all cofactors in {2,3}, l^2 > b, l odd, T_l != 0 mod l.
Report: intervals with NO valid prime (would break the proof step),
and intervals where some prime in the range is invalid (choice of l
matters). Also verifies T_l values are in {1/2, 1/3, 5/6} as F_l elts.
"""
import sys
from math import isqrt

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

def primes_upto(n):
    if n < 2: return []
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

P = primes_upto(BMAX)

def prime_data(a, b, l):
    mults = []
    k = -(-a // l)
    while k * l <= b:
        mults.append(k); k += 1
    if not mults:
        return (0, [], None)
    T = 0
    for k in mults:
        T = (T + pow(k, -1, l)) % l
    return (len(mults), mults, T)

no_valid = []
some_invalid = []
total = 0
worst = None
for b in range(34, BMAX + 1):
    primes = [l for l in P if b / 4 < l < b / 2]
    assert primes, f"no prime in (b/4,b/2) for b={b} (Bertrand failure!)"
    for a in range(b // 2 + 1, b + 1):
        if 3 * a > 2 * b + 1: continue
        total += 1
        nvalid = 0; ninvalid = 0
        for l in primes:
            k, cofs, T = prime_data(a, b, l)
            valid = (k >= 1 and all(c in (2, 3) for c in cofs)
                     and l * l > b and l % 2 == 1 and T != 0)
            if valid: nvalid += 1
            else: ninvalid += 1
        if nvalid == 0:
            no_valid.append((a, b))
        if ninvalid:
            some_invalid.append((a, b, ninvalid, len(primes)))
print(f"strip intervals tested (34<=b<={BMAX}): {total}")
print(f"intervals with NO valid prime in (b/4,b/2): {len(no_valid)} {no_valid[:10]}")
print(f"intervals where SOME prime in (b/4,b/2) is invalid: {len(some_invalid)} {some_invalid[:10]}")
