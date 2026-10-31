#!/usr/bin/env python3
"""Cluster E, Prover 1 (completion): exact finite checks.

All arithmetic is exact (Python int / fractions.Fraction).
Checks:
  (1) ln 2 series bound used in the strip: partial sum to k=5
      plus geometric tail < 9/8 of the first omitted term.
  (2) Strip bound H(a,b) < 3/4: ALL strip intervals with
      34 <= b <= 2000, H computed exactly from an exact
      harmonic prefix table H_n = sum_{i=1}^n 1/i in Q.
  (3) Prime step: for ALL strip intervals with 34 <= b <= 2000
      and EVERY prime l in (b/4, b/2): k(l) >= 1, l^2 > b,
      and T_l in {1/2, 1/3, 5/6} in F_l, nonzero.
  (4) Subregime A sanity: for all a > b/2 with 34 <= b <= 2000
      and 3a >= 2b+2, R = b-a+1 satisfies 2R <= a, and the
      exact H(a,b) < 1/2 (same prefix table).
  (5) Boundary ownership: for 34 <= b <= 2000, every a > b/2
      lies in exactly one of 3a >= 2b+2 / 3a <= 2b+1; the
      family 3a = 2b+1 is nonempty in the strip range and the
      family 3a = 2b+2 lies in subregime A.
  (6) b <= 33 filtering of AUDIT-B's six certified solutions
      by strict a > b/2 gives exactly the three claimed.
"""
from fractions import Fraction

# ---------- (1) ln 2 bound ----------
S5 = sum(Fraction(1, (2 * k + 1) * 3 ** (2 * k + 1)) for k in range(6))
first_omitted = Fraction(1, 13 * 3 ** 13)
ln2_bound = 2 * (S5 + Fraction(9, 8) * first_omitted)
assert ln2_bound == Fraction(2458234657, 3546482940), ln2_bound
assert ln2_bound < Fraction(111, 160)
assert Fraction(1, 18) + Fraction(111, 160) == Fraction(1079, 1440)
assert Fraction(1079, 1440) < Fraction(3, 4)
print("(1) ln2 < 2458234657/3546482940 =", float(ln2_bound),
      "< 111/160; 1/18 + 111/160 = 1079/1440 < 3/4  OK")

# ---------- primes up to 2000 (sieve of Eratosthenes, exact) ----------
N = 2000
is_prime = [True] * (N + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(N ** 0.5) + 1):
    if is_prime[i]:
        for j in range(i * i, N + 1, i):
            is_prime[j] = False
primes = [i for i, v in enumerate(is_prime) if v]

# ---------- exact harmonic prefix table ----------
prefix = [Fraction(0)] * (N + 1)
for n in range(1, N + 1):
    prefix[n] = prefix[n - 1] + Fraction(1, n)

def H(a, b):
    return prefix[b] - prefix[a - 1]

# ---------- strip / subregime A classification ----------
def strip_as(b):
    # b/2 < a and 3a <= 2b+1
    return [a for a in range(b // 2 + 1, b + 1) if 3 * a <= 2 * b + 1]

def subA_as(b):
    return [a for a in range(b // 2 + 1, b + 1) if 3 * a >= 2 * b + 2]

# ---------- (2) strip H < 3/4, all intervals, b <= 2000 ----------
strip_count = 0
max_H = Fraction(0)
max_at = None
for b in range(34, N + 1):
    for a in strip_as(b):
        strip_count += 1
        h = H(a, b)
        assert h < Fraction(3, 4), (a, b, h)
        assert h <= Fraction(1, a) + ln2_bound  # analytic form, exact comparison vs the proved ln2 bound is NOT used here; see note below
        if h > max_H:
            max_H, max_at = h, (a, b)
print(f"(2) strip H<3/4: {strip_count} intervals, 34<=b<=2000, 0 violations; "
      f"max H = {float(max_H):.6f} at (a,b)={max_at}  OK")
# Note on the assert h <= 1/a + ln2_bound above: ln2_bound is a proved
# rational upper bound for ln 2 and H(a,b) <= 1/a + ln(b/a) < 1/a + ln 2
# analytically; the assert is an exact rational sanity check of the
# numeric inequality H(a,b) < 1/a + (rational bound), not a proof step.

# ---------- (3) prime step, all strip intervals, b <= 2000 ----------
pair_count = 0
t_counts = {"1/2": 0, "1/3": 0, "5/6": 0}
min_l = None
for b in range(34, N + 1):
    ls = [p for p in primes if b / 4 < p < b / 2]
    assert ls, b  # Bertrand supplies at least one
    sas = strip_as(b)
    for p in ls:
        assert p * p > b
        assert p >= 11
        if min_l is None or p < min_l:
            min_l = p
        inv2 = pow(2, -1, p); inv3 = pow(3, -1, p)
        forms = {"1/2": inv2, "1/3": inv3, "5/6": (5 * pow(6, -1, p)) % p}
        assert (inv2 + inv3) % p == forms["5/6"]
        assert all(v != 0 for v in forms.values())
        for a in sas:
            pair_count += 1
            in2 = a <= 2 * p <= b
            in3 = a <= 3 * p <= b
            # no other multiples can occur
            assert not (a <= p <= b) and not (a <= 4 * p <= b)
            assert in2 or in3, (a, b, p)  # k(l) >= 1
            if in2 and in3:
                key = "5/6"
            elif in2:
                key = "1/2"
            else:
                key = "1/3"
            t_counts[key] += 1
print(f"(3) prime step: {pair_count} (interval, prime) pairs, 34<=b<=2000, "
      f"0 with k(l)=0; T_l counts {t_counts}; smallest l seen = {min_l}  OK")

# ---------- (4) subregime A, b <= 2000 ----------
subA_count = 0
for b in range(34, N + 1):
    for a in subA_as(b):
        subA_count += 1
        R = b - a + 1
        assert 2 * R <= a, (a, b, R)
        assert H(a, b) < Fraction(1, 2), (a, b)
print(f"(4) subregime A: {subA_count} intervals, 34<=b<=2000, "
      f"2R<=a and exact H<1/2 throughout, 0 violations  OK")

# ---------- (5) boundary ownership ----------
eq_strip = eq_A = 0
for b in range(34, N + 1):
    for a in range(b // 2 + 1, b + 1):
        inA = 3 * a >= 2 * b + 2
        inS = 3 * a <= 2 * b + 1
        assert inA != inS  # exactly one
        if 3 * a == 2 * b + 1:
            eq_strip += 1; assert inS
        if 3 * a == 2 * b + 2:
            eq_A += 1; assert inA
print(f"(5) boundary: partition exact for all a>b/2, 34<=b<=2000; "
      f"3a=2b+1 (strip) instances: {eq_strip}; 3a=2b+2 (subregime A) instances: {eq_A}  OK")

# ---------- (6) b <= 33 filtering of the six certified solutions ----------
six = [(1, 1, 1), (1, 2, 2), (2, 2, 2), (1, 3, 6), (2, 3, 6), (3, 6, 20)]
kept = [s for s in six if 2 * s[0] > s[1]]
assert kept == [(1, 1, 1), (2, 2, 2), (2, 3, 6)], kept
excluded_eq = [s for s in six if 2 * s[0] == s[1]]
assert excluded_eq == [(1, 2, 2), (3, 6, 20)], excluded_eq
print("(6) filtering six by strict a>b/2: kept", kept,
      "; excluded with a=b/2 exactly:", excluded_eq,
      "; also excluded (a<b/2): (1,3,6)  OK")

print("ALL PROVER1COMPLETION CHECKS PASSED")
