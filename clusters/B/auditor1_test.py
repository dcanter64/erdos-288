#!/usr/bin/env python3
"""
Auditor 1 (Cluster B) computational tests for Zeraoulia Rafik,
"The singleton case of Erdos Problem 288" (Feb 2026).

Exact arithmetic only (fractions.Fraction / integer modular arithmetic).

Tests:
 T1 Worked examples (2,3) and (3,6), incl. the H(3,6) value printed in the note.
 T2 Lemma 1 solution scan for all b <= B: solutions and Lemma-1 condition.
 T3 Lemma 2 dichotomy for ALL intervals 1<=a<=b<=B (solution or not):
    for every odd prime p with p^2 > b and k(p) >= 1:
      good (T_p != 0 mod p)  => v_p(den H(a,b)) == 1
      bad  (T_p == 0 mod p)  => v_p(den H(a,b)) == 0
    T_p mod p computed two independent ways: (i) modular inverses in F_p,
    (ii) numerator/denominator of the exact Fraction T_p.
    For solution intervals additionally: m = den H satisfies the
    congruence m = -p * (T_p mod p)^{-1} (mod p^2) for good p, p ∤ m for bad p,
    and m lies in the full CRT class mod Q.
 T4 Lemma 5: T(u)=0 in F_p iff D'(u)=0 (D(u)!=0), and #bad u <= k-1.
 T5 Corollary 6 / Remark 7: u=1, k=1,2,3 bad primes up to a prime bound;
    k=2 classification: bad iff u=(p-1)/2.
 T6 Propositions 8 and 10: primes in the stated ranges are good.
    Plus Prop 10's theta lower bound checked numerically for small b
    (search for b where log Q < 2*(theta(b)-theta(b/2)) under its hypothesis).
 T7 Theorem 13 vacuity probe: intervals (a,b)=(q^2,q^2), q prime:
    P1 empty, Q=1, yet m=1 is b-smooth and <= lcm(a..b), so the stated
    exclusion hypothesis fails for these (a,b) at every scale.
"""
from fractions import Fraction
from math import gcd, log, isqrt
import sys

B = 300

def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * len(sieve[i*i::i])
    return [i for i in range(n + 1) if sieve[i]]

PRIMES = primes_upto(B)
ODD_PRIMES = [p for p in PRIMES if p % 2 == 1]

def vp_int(n, p):
    """p-adic valuation of a positive integer n."""
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def interval_primes(a, b):
    """Odd primes p with p^2 > b and at least one multiple in [a,b].
    Yields (p, u, k) with multiples p*u .. p*(u+k-1)."""
    out = []
    for p in ODD_PRIMES:
        if p * p <= b:
            continue
        if p > b:            # smallest positive multiple p*1 > b => k=0
            if a > p:
                continue
            # p > b >= a impossible to have a multiple <= b; skip
            continue
        u = -(-a // p)       # ceil(a/p)
        if p * u > b:
            continue
        k = b // p - u + 1
        out.append((p, u, k))
    return out

def Tp_modp(u, k, p):
    """T_p mod p via modular inverses in F_p (method i)."""
    s = 0
    for j in range(k):
        s = (s + pow(u + j, -1, p)) % p
    return s

def Tp_fraction(u, k):
    s = Fraction(0)
    for j in range(k):
        s += Fraction(1, u + j)
    return s

def good_primes(a, b):
    """P1(a,b): list of (p, Tp_mod_p) for good odd primes p^2>b, k>=1."""
    res = []
    for (p, u, k) in interval_primes(a, b):
        t = Tp_modp(u, k, p)
        if t != 0:
            res.append((p, t))
    return res

def crt_class(a, b):
    """Return (Q, r) with forced class m = r (mod Q), r in [0, Q)."""
    Q = 1
    r = 0
    for (p, t) in good_primes(a, b):
        mod = p * p
        rp = (-p * pow(t, -1, p)) % mod   # m = rp (mod p^2); note rp determined mod p^2 via t in F_p
        # rp as computed is only determined mod p^2 because m = p*m1, m1 = -t^{-1} mod p:
        rp = (p * ((-pow(t, -1, p)) % p)) % mod
        # CRT merge r (mod Q) with rp (mod mod), gcd(Q, mod)=1
        inv = pow(Q % mod, -1, mod)
        r = r + Q * (((rp - r) * inv) % mod)
        Q *= mod
        r %= Q
    return Q, r

failures = []
def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL:", msg)

print("=" * 72)
print("T1. Worked examples")
print("=" * 72)
# (2,3)
H23 = sum(Fraction(1, n) for n in range(2, 4))
print(f"H(2,3) = {H23}  (note prints 5/6)")
check(H23 == Fraction(5, 6), "H(2,3) != 5/6")
A, Bd = H23.numerator, H23.denominator
check((A + 1) % Bd == 0 and Bd == 6, "Lemma1 (2,3): m=6 fails")
m = Bd
Q, r = crt_class(2, 3)
print(f"(2,3): m={m}, Q={Q}, CRT r={r} (note: Q=9, class m=6 mod 9); "
      f"p=3 congruence: m mod 9 = {m % 9}, -3*T^-1 mod 9 = {(-3 * pow(1, -1, 3)) % 9}")
check(Q == 9 and r == 6 and m % Q == r, "CRT class (2,3) mismatch")
check(m == 6, "(2,3) m != 6")

# (3,6)
H36 = sum(Fraction(1, n) for n in range(3, 7))
print(f"H(3,6) = {H36}  (note Section 6.2 prints 49/20)")
print(f"  exact value is {H36}; 49/20 = {Fraction(49,20)}; equal? {H36 == Fraction(49,20)}")
A, Bd = H36.numerator, H36.denominator
print(f"  Lemma 1 on TRUE value: A={A}, B={Bd}, (A+1) % B = {(A+1) % Bd}, "
      f"k=(A+1)/B = {(A+1)//Bd if (A+1)%Bd==0 else 'n/a'}")
check(H36 == Fraction(19, 20), "H(3,6) != 19/20")
check((A + 1) % Bd == 0 and Bd == 20, "Lemma1 (3,6): m=20 fails for true H")
# Literal reading of the printed 49/20:
Al, Bl = 49, 20
print(f"  Lemma 1 on PRINTED value 49/20: (49+1) % 20 = {(Al+1) % Bl} "
      f"-> printed value would give NO solution (20 does not divide 50)")
check((Al + 1) % Bl != 0, "expected printed 49/20 to fail Lemma 1 condition")
m = Bd
ip = interval_primes(3, 6)
print(f"  odd primes p^2>6 with k>=1 in [3,6]: {ip}")
for (p, u, k) in ip:
    t = Tp_modp(u, k, p)
    print(f"    p={p}: u={u}, k={k}, T_p mod p = {t} "
          f"({'BAD' if t == 0 else 'good'}), v_p(m=20) = {vp_int(20, p)}")
    if t != 0:
        cong = (p * ((-pow(t, -1, p)) % p)) % (p * p)
        print(f"      forced congruence m = {cong} (mod {p*p}); 20 mod {p*p} = {20 % (p*p)}")
        check(20 % (p * p) == cong, f"(3,6) congruence fails at p={p}")
    else:
        check(20 % p != 0, f"(3,6) bad prime {p} divides m")
Q, r = crt_class(3, 6)
print(f"  (3,6): Q={Q}, CRT r={r} (note: Q=25, class m=20 mod 25)")
check(Q == 25 and r == 20, "CRT class (3,6) mismatch")

print()
print("=" * 72)
print(f"T2+T3. Lemma 1 scan and Lemma 2 dichotomy, ALL intervals b <= {B}")
print("=" * 72)
solutions = []
n_intervals = 0
n_incidences = 0
n_good = 0
n_bad = 0
dich_fail = 0
cong_fail = 0
crt_fail = 0
tp_method_mismatch = 0
# iterate b, then a descending with running H(a,b)
for b in range(1, B + 1):
    H = Fraction(0)
    for a in range(b, 0, -1):
        H += Fraction(1, a)
        n_intervals += 1
        A, Bd = H.numerator, H.denominator
        is_sol = ((A + 1) % Bd == 0)
        if is_sol:
            solutions.append((a, b, Bd, (A + 1) // Bd))
        for (p, u, k) in interval_primes(a, b):
            n_incidences += 1
            t_mod = Tp_modp(u, k, p)
            tf = Tp_fraction(u, k)
            # method (ii): T_p as exact fraction; p must not divide its denominator
            if tf.denominator % p == 0:
                tp_method_mismatch += 1
                print(f"FAIL: p divides den(T_p) at a={a},b={b},p={p}")
                continue
            t_frac = (tf.numerator % p) * pow(tf.denominator % p, -1, p) % p
            if t_frac != t_mod:
                tp_method_mismatch += 1
                print(f"FAIL: T_p methods disagree at a={a},b={b},p={p}")
                continue
            v = vp_int(Bd, p)
            if t_mod != 0:
                n_good += 1
                if v != 1:
                    dich_fail += 1
                    if dich_fail <= 5:
                        print(f"FAIL dichotomy(good): a={a},b={b},p={p},u={u},k={k}, v_p(denH)={v}")
                if is_sol:
                    m = Bd
                    cong = (p * ((-pow(t_mod, -1, p)) % p)) % (p * p)
                    if m % (p * p) != cong or vp_int(m, p) != 1:
                        cong_fail += 1
                        print(f"FAIL solution congruence: a={a},b={b},p={p}")
            else:
                n_bad += 1
                if v != 0:
                    dich_fail += 1
                    if dich_fail <= 5:
                        print(f"FAIL dichotomy(bad): a={a},b={b},p={p},u={u},k={k}, v_p(denH)={v}")
                if is_sol and Bd % p == 0:
                    cong_fail += 1
                    print(f"FAIL bad prime divides m: a={a},b={b},p={p}")
        if is_sol:
            Q, r = crt_class(a, b)
            if Bd % Q != r % Q:
                crt_fail += 1
                print(f"FAIL CRT: a={a},b={b}, m={Bd}, Q={Q}, r={r}")
print(f"intervals tested: {n_intervals}")
print(f"solutions found (a,b,m,k): {solutions}")
print(f"prime-interval incidences (odd p, p^2>b, k>=1): {n_incidences}")
print(f"  good: {n_good}, bad: {n_bad}")
print(f"dichotomy failures: {dich_fail}")
print(f"T_p method mismatches: {tp_method_mismatch}")
print(f"solution congruence failures: {cong_fail}, CRT failures: {crt_fail}")
check(dich_fail == 0, "dichotomy failures present")
check(tp_method_mismatch == 0, "T_p method mismatch")
check(cong_fail == 0 and crt_fail == 0, "congruence/CRT failures")
check(sorted(solutions) == sorted([(1, 1, 1, 2), (1, 2, 2, 2), (2, 2, 2, 1),
                    (1, 3, 6, 2), (2, 3, 6, 1), (3, 6, 20, 1)]),
      f"unexpected solution list {solutions}")

print()
print("=" * 72)
print("T4. Lemma 5: T(u)=0 iff D'(u)=0 in F_p; #roots <= k-1")
print("=" * 72)
l5_fail = 0
cases = 0
for p in [q for q in primes_upto(120) if q % 2 == 1]:
    for k in range(1, min(p, 12) + 1):
        # D(u) = prod_{j<k} (u+j); D'(u) via polynomial arithmetic in F_p
        D = [1]
        for j in range(k):
            D2 = [0] * (len(D) + 1)
            for i, c in enumerate(D):
                D2[i] = (D2[i] + c * j) % p
                D2[i + 1] = (D2[i + 1] + c) % p
            D = D2
        Dp = [(i * D[i]) % p for i in range(1, len(D))]
        def ev(poly, x):
            s = 0
            for c in reversed(poly):
                s = (s * x + c) % p
            return s
        roots_Dp = [u for u in range(p) if ev(Dp, u) == 0]
        bad_u = []
        for u in range(p):
            if ev(D, u) == 0:
                continue
            if Tp_modp(u, k, p) == 0:
                bad_u.append(u)
        cases += 1
        if bad_u != roots_Dp or len(bad_u) > k - 1:
            l5_fail += 1
            print(f"FAIL Lemma5: p={p},k={k}, bad_u={bad_u}, D' roots={roots_Dp}")
print(f"(p,k) cases: {cases}, Lemma 5 failures: {l5_fail}")
check(l5_fail == 0, "Lemma 5 failures")

print()
print("=" * 72)
print("T5. Corollary 6 / Remark 7: u=1 cases; k=2 classification")
print("=" * 72)
PLIM = 500
plist = [q for q in primes_upto(PLIM) if q % 2 == 1]
for k in (1, 2, 3):
    bad = [p for p in plist if p > 1 + k - 1 and Tp_modp(1, k, p) == 0]
    # cross-check with numerator of exact T_{1,k}
    tf = Tp_fraction(1, k)
    print(f"u=1,k={k}: T={tf}, numerator={tf.numerator}, bad primes <={PLIM} (p>u+k-1): {bad}")
    prime_divs = [p for p in plist if tf.numerator % p == 0]
    check(bad == prime_divs, f"u=1,k={k}: bad set != prime divisors of numerator")
check(Tp_fraction(1, 1) == 1 and Tp_fraction(1, 2) == Fraction(3, 2)
      and Tp_fraction(1, 3) == Fraction(11, 6), "u=1 exact T values wrong")
k2_fail = 0
for p in plist:
    for u in range(1, p - 1):   # u+k-1 = u+1 < p, the Lemma-2 regime
        bad = (Tp_modp(u, 2, p) == 0)
        if bad != (u == (p - 1) // 2):
            k2_fail += 1
            print(f"FAIL k=2: p={p},u={u}")
print(f"k=2 classification failures (p<={PLIM}, all u): {k2_fail}")
check(k2_fail == 0, "k=2 classification failures")

print()
print("=" * 72)
print("T6. Propositions 8 and 10 range-goodness; Prop 10 theta bound small-b probe")
print("=" * 72)
p8_fail = p10_fail = 0
for b in range(10, 501):
    for a in range(1, b + 1):
        if a <= b // 3 or (3 * a <= b):
            pass
        # Prop 8: a <= b/3
        if 3 * a <= b:
            for p in plist:
                if p <= B and b / 3 < p <= b and p != 3:
                    u = -(-a // p)
                    if p * u > b:
                        continue
                    k = b // p - u + 1
                    if k >= 1 and Tp_modp(u, k, p) == 0:
                        p8_fail += 1
                        print(f"FAIL Prop8: a={a},b={b},p={p} bad")
        # Prop 10: a <= floor(b/2)+1
        if a <= b // 2 + 1:
            for p in plist:
                if b / 2 < p <= b:
                    u = -(-a // p)
                    if p * u > b:
                        continue
                    k = b // p - u + 1
                    if k >= 1 and Tp_modp(u, k, p) == 0:
                        p10_fail += 1
                        print(f"FAIL Prop10: a={a},b={b},p={p} bad")
    # (loops above are heavy; break pattern handled by counters only)
print(f"Prop 8 range-bad failures: {p8_fail}")
print(f"Prop 10 range-bad failures: {p10_fail}")
check(p8_fail == 0 and p10_fail == 0, "Prop 8/10 goodness failures")

# Prop 10 theta-bound probe for small b: find (a,b) with a<=floor(b/2)+1
# where log Q(a,b) < 2*(theta(b)-theta(b/2)).
def theta(x):
    return sum(log(p) for p in primes_upto(int(x)))
viol = []
for b in range(2, 13):
    for a in range(1, b // 2 + 2):
        Q, r = crt_class(a, b)
        rhs = 2 * (theta(b) - theta(b / 2))
        if log(Q) < rhs - 1e-12:
            viol.append((a, b, Q, round(rhs, 4), round(log(Q), 4)))
print("Prop 10 theta-bound violations for b<=12 (a,b,Q, RHS 2(theta(b)-theta(b/2)), log Q):")
for v in viol:
    print("   ", v)

print()
print("=" * 72)
print("T7. Theorem 13 vacuity probe: (a,b) = (q^2, q^2)")
print("=" * 72)
for q in [3, 5, 7, 11, 13]:
    a = b = q * q
    gp = good_primes(a, b)
    from math import lcm as _lcm
    L = 1
    for n in range(a, b + 1):
        L = _lcm(L, n)
    sol = (Fraction(1, a).numerator + 1) % Fraction(1, a).denominator == 0
    print(f"q={q}: (a,b)=({a},{b}), P1={gp}, Q=1 (empty product), "
          f"lcm(a..b)={L}, m=1 is b-smooth and 1 <= {L}: exclusion hypothesis "
          f"FAILS for this pair; actual H=1/{a} is a Lemma-1 solution? {sol}")
    check(gp == [], f"P1 nonempty for ({a},{b})")

print()
print("TOTAL recorded check() failures:", len(failures))
for f in failures:
    print(" -", f)
print("DONE")
