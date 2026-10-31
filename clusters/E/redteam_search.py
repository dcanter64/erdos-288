#!/usr/bin/env python3
"""Red Team (a): exhaustive exact search for solutions of H(a,b)+1/m in Z
with a > b/2, for b up to BMAX (argv[1], default 5000).

Method (independent of prover code): for fixed b, D = lcm(a_min..b),
a_min = floor(b/2)+1. H(a,b) = N_a / D with N_a built descending.
For b >= 34 we have a >= 18 and H(a,b) < 3/4 < 1 (verified separately),
so by Lemma 1 (gcd argument: kB - A | B and coprime to B, hence = 1)
a solution exists iff B_red - A_red = 1, i.e. D - N_a = gcd(N_a, D).
Cheap screen: d = D - N_a must divide N_a (and D); survivors get the
full gcd check. For b <= 33 the general Fraction test is used instead
(all k), which doubles as attack line (f).
"""
import sys
from fractions import Fraction
from math import gcd

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

def solutions_small(bmax=33):
    sols = []
    for b in range(1, bmax + 1):
        for a in range(b // 2 + 1, b + 1):
            f = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
            A, B = f.numerator, f.denominator
            # general Lemma-1 test: exists k with kB - A = 1 and m = B
            # equivalent: (A + 1) % B == 0 after writing H + 1/B... use:
            # H + 1/m in Z, m = B forced, and B | A + 1 in the k=1 sense;
            # do it fully generally: frac part of H is A/B; need 1 - frac
            # to be 1/B' form: check (B - A % B) ... simplest exact:
            # H + 1/m integer iff (1 - (A mod B)/B) has numerator 1 in
            # lowest terms when nonzero, or A % B == 0 (never, H not int
            # unless H=1). Handle H == 1 (a=b=1) separately.
            if f == 1:
                sols.append((a, b, 1)); continue
            frac = f - (f.numerator // f.denominator)
            inv = 1 / (1 - frac)  # = m candidate if integer
            if inv.denominator == 1:
                sols.append((a, b, inv.numerator))
    return sols

def main():
    sols_small = solutions_small(33)
    print(f"b<=33, a>b/2 solutions (Fraction, general): {sols_small}")
    found = []
    checked = 0
    for b in range(34, BMAX + 1):
        a_min = b // 2 + 1
        D = 1
        for n in range(a_min, b + 1):
            D = D * n // gcd(D, n)
        # N_a descending: N_b = D//b ; N_a = N_{a+1} + D//a
        N = 0
        terms = {}
        for n in range(a_min, b + 1):
            terms[n] = D // n
        N = 0
        for a in range(b, a_min - 1, -1):
            N += terms[a]
            checked += 1
            d = D - N
            if d <= 0:
                print(f"  !! H>=1 at (a,b)=({a},{b})"); continue
            if N % d == 0 and D % d == 0 and gcd(N, D) == d:
                # candidate: verify independently with Fraction
                f = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
                A, B = f.numerator, f.denominator
                ok = (B - A == 1)
                found.append((a, b, B, ok))
                print(f"  CANDIDATE (a,b)=({a},{b}) B={B} fraction-verified={ok}")
    print(f"searched b=34..{BMAX}: {checked} intervals with a>b/2")
    print(f"candidates found: {found}")
    print("RESULT:", "NO new solutions" if not found else "SOLUTIONS FOUND")

if __name__ == "__main__":
    main()
