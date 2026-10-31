#!/usr/bin/env python3
"""Red Team (c),(d),(e),(f): bounds, boundaries, m-forcing, census."""
from fractions import Fraction
from math import gcd

print("=== (c1) ln 2 < 111/160, self-contained exact check ===")
# ln 2 = 2 * sum_{k>=0} 1/((2k+1) 3^{2k+1}); bound tail geometrically:
# terms decrease, ratio of successive terms < 1/9 * (2k+1)/(2k+3) < 1/9.
s = Fraction(0)
for k in range(6):
    s += Fraction(1, (2 * k + 1) * 3 ** (2 * k + 1))
# tail after k=5: first omitted term t6, tail < t6 * (1/(1-1/9)) = t6*9/8
t6 = Fraction(1, 13 * 3 ** 13)
upper = 2 * (s + t6 * Fraction(9, 8))
print(f"2*partial+tailbound = {upper} = {float(upper):.8f}; 111/160 = {float(Fraction(111,160)):.8f}")
print("ln2 < 111/160:", upper < Fraction(111, 160))

print()
print("=== (c2) strip H < 3/4 chain, exact endpoint arithmetic ===")
# worst case: b = 2a-1 (max length), a >= 18 (since b >= 34, a > b/2).
# H(a,2a-1) <= 1/a + ln((2a-1)/a) < 1/a + ln 2 < 1/18 + 111/160.
val = Fraction(1, 18) + Fraction(111, 160)
print(f"1/18 + 111/160 = {val} = {float(val):.6f} < 3/4: {val < Fraction(3,4)}"
      f"  (margin {float(Fraction(3,4)-val):.6f})")
# exact spot verification of H < 3/4 on ALL strip intervals, b <= 300:
bad = 0; mx = (Fraction(0), None)
for b in range(34, 301):
    for a in range(b // 2 + 1, b + 1):
        if 3 * a > 2 * b + 1: continue
        H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
        if H >= Fraction(3, 4): bad += 1; print("  H>=3/4 at", a, b, H)
        if H > mx[0]: mx = (H, (a, b))
print(f"strip b<=300 exact: violations of H<3/4: {bad}; max H = {float(mx[0]):.6f} at {mx[1]}")
# short intervals in the strip (attack line d): lengths 1,2,3 exact scan b<=2000
mxlen = {}
for b in range(34, 2001):
    for L in (1, 2, 3):
        a = b - L + 1
        if 2 * a > b and 3 * a <= 2 * b + 1:
            H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
            if L not in mxlen or H > mxlen[L][0]: mxlen[L] = (H, (a, b))
for L in (1, 2, 3):
    if L in mxlen:
        print(f"  strip length {L}: max H = {float(mxlen[L][0]):.6f} at {mxlen[L][1]}")
    else:
        print(f"  strip length {L}: NO strip intervals with b in [34,2000] "
              f"(length L in strip needs 3(b-L+1)<=2b+1, i.e. b<=3L-2; "
              f"for b>=34 strip length is >= (b+2)/3 >= 12)")
minlen = min(b - a + 1 for b in range(34, 2001) for a in range(b // 2 + 1, b + 1)
             if 3 * a <= 2 * b + 1)
print(f"  minimum strip interval length for 34<=b<=2000: {minlen}")

print()
print("=== (c3) subregime A (3a >= 2b+2): R <= a/2 and H < 1/2, endpoints ===")
# R = b-a+1; 3a>=2b+2 -> b <= (3a-2)/2 -> R <= a/2 (real ineq). H <= R/a,
# equality iff R=1. Check the inequality chain over a grid + R=1 case:
viol = 0
for b in range(34, 5001):
    for a in range(b // 2 + 1, b + 1):
        if 3 * a >= 2 * b + 2:
            R = b - a + 1
            if 2 * R > a: viol += 1; print("  2R>a at", a, b)
print(f"grid b<5000: violations of 2R<=a in subregime A: {viol}")
print("R=1 in subregime A (b>=34): a=b>=34, H=1/a<=1/34<1/2 OK; note H=R/a exactly,")
print("so the bare claim 'H < R/a' FAILS at R=1 (equality); at a=b=2, H=1/2 exactly")
print("and (2,2,2) IS a solution -- outside b>=34 range, so harmless there.")

print()
print("=== (d) m-forcing from 0 < H < 3/4 (pure enumeration) ===")
# H + 1/m = integer k. m=1: sum in (1, 7/4): no integer. m>=2: sum in
# (0, 5/4): only k=1, giving 1/m = 1-H in (1/4,1), so m in {2,3}.
# No lower bound H>1/2 needed. Verify logic on a fine rational grid:
bad = 0
for num in range(1, 750):
    H = Fraction(num, 1000)  # 0 < H < 3/4
    for m in range(1, 50):
        ssum = H + Fraction(1, m)
        if ssum.denominator == 1 and m not in (2, 3):
            bad += 1; print("  unexpected m", H, m)
print(f"grid check (H=k/1000<3/4, m<50): solutions with m not in {{2,3}}: {bad}")

print()
print("=== (e) Claim 2 boundary a = 2R ===")
# prover's chain for R>=2: H <= 1/a + (R-1)/(a+1) < R/a; at a=2R this is
# still < 1/2 strictly. At R=1, a=2: H=1/2 and (2,2,2) is a solution.
for R in [1, 2, 3, 4, 5, 10, 50, 100]:
    a = 2 * R; b = a + R - 1
    H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
    print(f"  R={R} a=2R={a} b={b}: H={float(H):.6f} <1/2: {H < Fraction(1,2)}"
          f"  bound 1/a+(R-1)/(a+1)={float(Fraction(1,a)+Fraction(R-1,a+1)):.6f} < R/a={R/a:.4f}: "
          f"{Fraction(1,a)+Fraction(R-1,a+1) < Fraction(R,a)}")
print("  R=1,a=2: H=1/2 exactly, (2,2,2) solution -> a>2R is SHARP at R=1;")
print("  for R>=2 the same proof gives a>=2R too (claim true as stated, not sharp).")

print()
print("=== (f) census b<=300 filter a>b/2 (recompute, compare AUDIT-B list) ===")
sols = []
for b in range(1, 301):
    for a in range(1, b + 1):
        f = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
        if f == 1:
            sols.append((a, b, 1)); continue
        frac = f - (f.numerator // f.denominator)
        if frac == 0: continue
        inv = 1 / (1 - frac)
        if inv.denominator == 1:
            sols.append((a, b, inv.numerator))
print("all solutions b<=300:", sols)
filt = [s for s in sols if 2 * s[0] > s[1]]
print("filtered a>b/2:", filt)
print("boundary: (1,2,2): 2a=b -> excluded by strict >; (3,6,20): 2a=b -> excluded.")
