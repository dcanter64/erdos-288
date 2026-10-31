#!/usr/bin/env python3
"""Red Team (b), optimized: for each strip interval and each prime l in
(b/4,b/2), validity depends on a only through whether a<=2l and a<=3l.
T_l for J={2},{3},{2,3} precomputed once per prime. Same definitions
as redteam_strip.py; cross-checked against it on b<=200 (identical
verdicts required)."""
import sys
from math import isqrt

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

def primes_upto(n):
    if n < 2: return []
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]: s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

P = primes_upto(BMAX // 2)
total = 0; no_valid = []; some_invalid = 0
for b in range(34, BMAX + 1):
    primes = []
    for l in P:
        if l * 4 > b and l * 2 < b:   # b/4 < l < b/2
            i2 = pow(2, -1, l); i3 = pow(3, -1, l)
            primes.append((l, i2, i3, (i2 + i3) % l))
    assert primes
    for a in range(b // 2 + 1, b + 1):
        if 3 * a > 2 * b + 1: continue
        total += 1
        nvalid = 0; ninvalid = 0
        for (l, i2, i3, i23) in primes:
            has2 = a <= 2 * l            # 2l <= b automatic (l < b/2)
            has3 = 3 * l <= b and a <= 3 * l
            if not (has2 or has3):
                ninvalid += 1; continue
            T = i23 if (has2 and has3) else (i2 if has2 else i3)
            if T != 0 and l * l > b:
                nvalid += 1
            else:
                ninvalid += 1
        if nvalid == 0: no_valid.append((a, b))
        if ninvalid: some_invalid += 1
print(f"strip intervals tested (34<=b<={BMAX}): {total}")
print(f"intervals with NO valid prime: {len(no_valid)} {no_valid[:10]}")
print(f"intervals where SOME prime invalid: {some_invalid}")
