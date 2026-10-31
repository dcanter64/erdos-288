#!/usr/bin/env python3
"""Cluster E verifier: independent exact-arithmetic recomputation.
All arithmetic exact (Fraction / integers). No floats except for
printing already-exact quantities as decimals for readability."""
from fractions import Fraction
import math

# ---------- helpers ----------
def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0: sieve[0] = 0
    if n >= 1: sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            step = i; start = i * i
            sieve[start:n+1:step] = b"\x00" * (((n - start)//step) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

def v_p_int(n, p):
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e

def vp2(n):
    # v2 of a positive integer, and of a Fraction via numerator/denominator
    if isinstance(n, Fraction):
        return v_p_int(n.numerator, 2) - v_p_int(n.denominator, 2)
    return v_p_int(n, 2)

print("=== V0: analytic bounds ===")
# ln 2 series bound as presented in prover1.md
S5 = sum(Fraction(1, (2*k+1) * 3**(2*k+1)) for k in range(6))
tail_first = Fraction(1, 13 * 3**13)
ratios_ok = True
for k in range(0, 30):
    t_k = Fraction(1, (2*k+1) * 3**(2*k+1))
    t_k1 = Fraction(1, (2*k+3) * 3**(2*k+3))
    if not (t_k1 / t_k == Fraction(2*k+1, 2*k+3) / 9 < Fraction(1, 9)):
        ratios_ok = False
ln2_bound = 2 * (S5 + Fraction(9, 8) * tail_first)
print("term ratios <1/9 (checked k=0..29):", ratios_ok)
print("ln2 upper bound =", ln2_bound, " claimed 2458234657/3546482940:",
      ln2_bound == Fraction(2458234657, 3546482940))
print("bound < 111/160:", ln2_bound < Fraction(111, 160),
      " difference 111/160 - bound =", Fraction(111,160)-ln2_bound,
      " claimed diff numerator check:", Fraction(111,160)-ln2_bound == Fraction(17103061, 28371863520))
print("1/18 + 111/160 =", Fraction(1,18)+Fraction(111,160),
      " == 1079/1440:", Fraction(1,18)+Fraction(111,160) == Fraction(1079,1440),
      " < 3/4:", Fraction(1079,1440) < Fraction(3,4),
      " margin:", Fraction(3,4)-Fraction(1079,1440))
# 319/420 Riemann-sum bound as presented in prover2.md
rs = Fraction(1,4) * (Fraction(1,1) + Fraction(4,5) + Fraction(2,3) + Fraction(4,7))
print("Riemann sum (1/4)(1+4/5+2/3+4/7) =", rs, " == 319/420:", rs == Fraction(319,420))
comb = Fraction(319,420) + Fraction(1,17) + Fraction(1,16)
print("319/420 + 1/17 + 1/16 =", comb, " == 25157/28560:", comb == Fraction(25157,28560), " < 1:", comb < 1)

print()
print("=== V1/V3/V4/V5: single descending sweep, b<=1000 (other checks b<=500) ===")
solutions_ii = []
regime_ii_count = 0
chain_count = 0; chain_fail = []
window_count = 0; window_fail = []
strip_intervals = 0; strip_pairs = 0; strip_fail = []
strip_T_counts = {}
for b in range(1, 1001):
    H = Fraction(0, 1)
    for a in range(b, 0, -1):
        H += Fraction(1, a)
        R = b - a + 1
        A, B = H.numerator, H.denominator
        # regime (ii)
        if 2*a > b:
            regime_ii_count += 1
            if (A + 1) % B == 0:
                solutions_ii.append((a, b, B))  # m = B by Lemma 1
        if b > 500:
            continue
        # chain inequality, R>=2
        if R >= 2:
            chain_count += 1
            # (A+1)/B < 2R/a  <=>  (A+1)*a < 2R*B
            if not ((A+1)*a < 2*R*B):
                chain_fail.append((a, b))
            if not (Fraction(A, B) < Fraction(R, a) and Fraction(1, B) < Fraction(R, a)):
                chain_fail.append((a, b, "component"))
        # window 2-adic claim: 32<=b<=500, b/2<a<=(2b+2)/3, R>=2
        if 32 <= b and 2*a > b and 3*a <= 2*b + 2 and R >= 2:
            window_count += 1
            t = b.bit_length() - 1  # 2^t <= b < 2^(t+1)
            assert 2**t <= b < 2**(t+1)
            vals = [v_p_int(n, 2) for n in range(a, b+1)]
            s = max(vals)
            if not (vals.count(s) == 1 and s >= t-1 and vp2(H) == -s
                    and v_p_int(B, 2) == s and B >= 2**s >= 2**(t-1) >= 16):
                window_fail.append((a, b, s, t))
        # strip prime claim: 34<=b<=500, b/2<a, 3a<=2b+1
        if 34 <= b and 2*a > b and 3*a <= 2*b + 1:
            strip_intervals += 1
            # all primes l in (b/4, b/2)
            for ell in primes_upto(b//2):
                if not (4*ell > b and 2*ell < b):
                    continue
                mults = [n for n in range(a, b+1) if n % ell == 0]
                strip_pairs += 1
                if len(mults) < 1:
                    strip_fail.append((a, b, ell, "k=0")); continue
                cof = [n // ell for n in mults]
                if any(c not in (2, 3) for c in cof):
                    strip_fail.append((a, b, ell, "cofactor", cof)); continue
                T = sum(Fraction(1, c) for c in cof)  # exact rational representative
                # value in F_ell
                Tmod = (T.numerator * pow(T.denominator, -1, ell)) % ell
                if Tmod == 0 or ell*ell <= b or ell < 11:
                    strip_fail.append((a, b, ell, "T/ell^2")); continue
                key = str(T)
                strip_T_counts[key] = strip_T_counts.get(key, 0) + 1
print("regime (ii) intervals checked (b<=1000):", regime_ii_count)
print("regime (ii) solutions found:", solutions_ii)
print("chain intervals (b<=500, R>=2):", chain_count, " failures:", len(chain_fail), chain_fail[:5])
print("window intervals (32<=b<=500):", window_count, " failures:", len(window_fail), window_fail[:5])
print("strip intervals (34<=b<=500):", strip_intervals, " (interval,prime) pairs:", strip_pairs,
      " failures:", len(strip_fail), strip_fail[:5])
print("strip T_l value counts:", strip_T_counts)

print()
print("=== V2: Theorem F family, primes P=1 mod 4, P<=500 ===")
PR = primes_upto(70000)
primes_1mod4 = [p for p in primes_upto(500) if p % 4 == 1]
print("count of such primes <=500:", len(primes_1mod4))
fam_fail = []
intervals = []
for P in primes_1mod4:
    f = math.factorial((P-1)//2) % P
    nP = min(f, P - f)
    if not (1 <= nP <= (P-1)//2 and (nP*nP) % P == P - 1):
        fam_fail.append((P, "nP")); continue
    a = nP*nP; b = a + 1
    intervals.append((a, b))
    H = Fraction(2*a + 1, a*(a+1))
    A, B = H.numerator, H.denominator
    if not (B == a*(a+1) and A == 2*a + 1):
        fam_fail.append((P, "B")); continue
    L = a*(a+1) // math.gcd(a, a+1)
    if not (B == L):
        fam_fail.append((P, "L")); continue
    # P1 exactly {P}, by the sieve definition (all odd primes p, p^2>b, multiples in [a,b])
    P1 = []
    for p in PR:
        if p == 2 or p*p <= b:
            continue
        if p > b:
            break
        # multiples of p in [a,b]
        first = ((a + p - 1)//p) * p
        mults = list(range(first, b+1, p))
        if not mults:
            continue
        cof = [n // p for n in mults]
        Tmod = sum(pow(c, -1, p) for c in cof) % p
        if Tmod != 0:
            P1.append(p)
    if P1 != [P]:
        fam_fail.append((P, "P1", P1)); continue
    # B in forced class: single congruence mod P^2
    u = (a+1)//P  # P | a+1, cofactor; T_P = u^{-1} in F_P, so (T_P)^{-1} = u mod P
    forced = (-P * (u % P)) % (P*P)
    if B % (P*P) != forced:
        fam_fail.append((P, "class")); continue
    # B b-smooth: prime factors of B are <= b (trivially factors of a, a+1)
    # (A+1)/B = 2/a exactly, not an integer
    if not (Fraction(A+1, B) == Fraction(2, a) and Fraction(2, a).denominator != 1):
        fam_fail.append((P, "2/a")); continue
    # v_P(B)=1
    if v_p_int(B, P) != 1:
        fam_fail.append((P, "vP")); continue
print("family intervals distinct:", len(set(intervals)) == len(intervals), " count:", len(intervals))
print("family failures:", len(fam_fail), fam_fail[:5])
print("first three intervals:", intervals[:3])

print()
print("=== V6: census filtering / thresholds ===")
census = [(1,1,1),(1,2,2),(2,2,2),(1,3,6),(2,3,6),(3,6,20)]
filt = [s for s in census if 2*s[0] > s[1]]
print("AUDIT-B census filtered by strict a>b/2:", filt)
print("excluded with a=b/2 exactly:", [s for s in census if 2*s[0] == s[1]])
# R=1 exact
r1 = [(a, a) for a in range(1, 2001) if Fraction(2, a).denominator == 1]
print("R=1: a<=2000 with 2/a an integer:", r1)

print()
print("=== V7: Prover 2 Lemma 1.1, literal vs odd-prime reading, a<=3000 ===")
def prime_divs(n):
    ds = set(); d = 2
    while d*d <= n:
        if n % d == 0:
            ds.add(d)
            while n % d == 0: n //= d
        d += 1 if d == 2 else 2
    if n > 1: ds.add(n)
    return ds
lit_mismatch = []; odd_mismatch = []
for a in range(1, 3001):
    b = a + 1; B = a * b
    fa = prime_divs(a); fb = prime_divs(b)
    P1 = [p for p in prime_divs(a*b) if p != 2 and p*p > b]
    inclass = all(B % (p*p) == (-p * ((a if a % p == 0 else b)//p)) % (p*p) for p in P1)
    actual = bool(P1) and inclass
    lit = all(p*p <= b for p in fa) and any(p*p > b for p in fb)
    odd = all(p*p <= b for p in fa if p != 2) and any(p*p > b for p in fb if p != 2)
    if lit != actual: lit_mismatch.append(a)
    if odd != actual: odd_mismatch.append(a)
print("literal (alpha)/(beta) mismatches, a<=3000:", lit_mismatch)
print("odd-prime (alpha)/(beta) mismatches, a<=3000:", odd_mismatch)
