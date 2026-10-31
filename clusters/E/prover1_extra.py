#!/usr/bin/env python3
"""Extra exact checks for prover1: strip r0-smooth exceptions (b<=200)
and the regime-(ii) finite check b<=33."""
from fractions import Fraction
from prover1_checks import interval_data, is_b_smooth, primes_upto

P200 = primes_upto(200)
print("strip intervals (b/2<a, 3a<=2b+1, b<=200) with r0<=L:")
for b in range(10, 201):
    for a in range(b//2+1, b+1):
        if 3*a > 2*b+1: continue
        B,L,Q,r0,P1 = interval_data(a,b,P200)
        if Q>1 and r0<=L:
            print(f"  (a,b)=({a},{b}) r0={r0} smooth={is_b_smooth(r0,b,P200)} B_in_class={B%Q==r0%Q}")

print()
print("regime (ii) finite check, b<=33, a>b/2: exact solution test via Lemma 1 candidate")
print("H(a,b)=A/B lowest terms; solution iff (A+1) % B == 0 (then m=B).")
sols=[]
for b in range(1,34):
    H=Fraction(0)
    for a in range(1,b+1):
        pass
    s=Fraction(0)
    # compute prefix sums once per b is unnecessary at this size; direct:
    for a in range(1,b+1):
        if 2*a<=b: continue
        f=sum((Fraction(1,n) for n in range(a,b+1)), Fraction(0))
        A,B=f.numerator, f.denominator
        if (A+1)%B==0:
            sols.append((a,b,B))
print("solutions with a>b/2, b<=33:", sols)
