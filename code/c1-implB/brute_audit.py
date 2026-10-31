#!/usr/bin/env python3
"""Independent brute-force audit for Implementation B (not the engine).

Method ( deliberately different from engine.c ): prefix harmonic
numbers as exact Fractions, H(a,b) = H_b - H_{a-1}; singleton test
A % B == B - 1 on the formed fraction; L=2 near-miss test B pronic
via math.isqrt; L=2 solution test by exact Fraction sum.
Used only on small ranges to audit the C engine end to end.
"""
import json, sys
from fractions import Fraction
from math import isqrt

def census(bmax):
    H = [Fraction(0)]
    for n in range(1, bmax + 1):
        H.append(H[-1] + Fraction(1, n))
    singletons = []
    nearmiss = []
    l2_solutions = []
    pronic_le = 0
    for b in range(1, bmax + 1):
        for a in range(1, b + 1):
            f = H[b] - H[a - 1]
            A, B = f.numerator, f.denominator
            if A % B == B - 1:
                singletons.append((a, b, B))
            c = isqrt(B)
            if c * (c + 1) == B:
                if c > b:
                    nearmiss.append((a, b, c))
                    s = f + Fraction(2 * c + 1, B)
                    if s.denominator == 1:
                        l2_solutions.append((a, b, c))
                else:
                    pronic_le += 1
    return singletons, nearmiss, l2_solutions, pronic_le

if __name__ == "__main__":
    bmax = int(sys.argv[1])
    s, nm, l2, ple = census(bmax)
    print(json.dumps({
        "bmax": bmax,
        "singletons": s,
        "l2_nearmisses": nm,
        "l2_solutions": l2,
        "l2_pronic_c_le_b": ple,
    }, indent=1))
