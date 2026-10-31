#!/usr/bin/env python3
"""
Red Team rerun of Nayak Appendix A (the finite verification script for
Proposition 16.1), transcribed verbatim from Nayak-2026.txt Appendix A,
with only timing added around it. B = 2000 as printed.

Printed output in the note:
    singleton [(2, 3, 6), (1, 3, 6), (3, 6, 20)]
    L2 []
"""
import time
from fractions import Fraction
from math import isqrt

t0 = time.time()

B = 2000
singletons = []
L2 = []

for b in range(1, B + 1):
    s = Fraction(0, 1)
    for a in range(b, 0, -1):
        s += Fraction(1, a)
        A, D = s.numerator, s.denominator

        # Singleton upper interval [D, D].
        if D > b and (A + 1) % D == 0:
            singletons.append((a, b, D))

        # L = 2: D must be c(c + 1), with c > b.
        disc = 1 + 4 * D
        root = isqrt(disc)
        if root * root == disc and (root - 1) % 2 == 0:
            c = (root - 1) // 2
            if c > b and (A + 2 * c + 1) % D == 0:
                L2.append((a, b, c))
    if b % 250 == 0:
        print(f"b<={b} elapsed={time.time()-t0:.1f}s", flush=True)

print("singleton", singletons)
print("L2", L2)
print(f"total elapsed={time.time()-t0:.1f}s")
expected_singletons = [(2, 3, 6), (1, 3, 6), (3, 6, 20)]
print("MATCHES PRINTED OUTPUT:", singletons == expected_singletons and L2 == [])
