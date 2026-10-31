#!/usr/bin/env python3
"""Red Team (b), reduced exhaustive form. For a strip interval
(b/2<a, 3a<=2b+1, b>=34) and prime l in (b/4,b/2):
  cofactors can only be 2,3 (4l>b); l>=11 so T_l in {1/2,1/3,5/6}
  is nonzero mod l; l^2>b (l>b/4>sqrt(b), b>16);
  3l<=b  => 3l in [a,b] (3l>3b/4>a as a<=(2b+1)/3<3b/4 for b>4);
  2l>=a  => 2l in [a,b] (2l<b).
Hence l is INVALID iff 2l<a and 3l>b, i.e. iff l in (b/3, a/2).
An interval has NO valid prime iff primes(b/4,b/2) all lie in
(b/3,a/2). Prime counting by bisect: exact and fast.
Literal-definition versions (redteam_strip.py, redteam_strip_fast.py)
agree with this reduction on all of b<=200 (3298 intervals)."""
import sys
from bisect import bisect_left, bisect_right
from math import isqrt

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 100000

def primes_upto(n):
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]: s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

P = primes_upto(BMAX // 2)
def nprimes(x, y):  # primes in (x, y), real bounds
    return bisect_left(P, y) - bisect_right(P, x) if y > x else 0

total = 0; no_valid = 0; some_invalid = 0; ex_nv = None; ex_si = None
for b in range(34, BMAX + 1):
    tot_range = nprimes(b / 4, b / 2)
    assert tot_range >= 1, f"Bertrand failure at b={b}"
    for a in range(b // 2 + 1, b + 1):
        if 3 * a > 2 * b + 1: continue
        total += 1
        ninv = nprimes(b / 3, a / 2)
        if ninv == tot_range:
            no_valid += 1; ex_nv = ex_nv or (a, b)
        if ninv > 0:
            some_invalid += 1; ex_si = ex_si or (a, b)
print(f"strip intervals (34<=b<={BMAX}): {total}")
print(f"intervals with NO valid prime: {no_valid} (example: {ex_nv})")
print(f"intervals with SOME invalid prime in (b/4,b/2): {some_invalid} (example: {ex_si})")
