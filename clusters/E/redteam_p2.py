#!/usr/bin/env python3
"""Red Team vs Prover 2: independent verification of P2-Claims 1,2,3
and the 83-map. Own implementations throughout."""
from fractions import Fraction
from math import gcd, isqrt
import random

def primes_upto(n):
    if n < 2: return []
    s = bytearray(b"\x01") * (n + 1); s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]: s[i*i::i] = b"\x00" * len(s[i*i::i])
    return [i for i, v in enumerate(s) if v]

def spf_upto(n):
    spf = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j: spf[j] = i
    return spf

def v2(n): return (n & -n).bit_length() - 1

# ---------- P2-Claim 1: 2-adic unique maximum in the window ----------
print("=== P2-1: 2-adic unique maximum, window b/2<a, 3a<=2b+2, 32<=b<=3000 ===")
total = 0; case1 = 0; case2 = 0; failures = []
for b in range(32, 3001):
    t = b.bit_length() - 1            # 2^t <= b < 2^(t+1)
    assert 2**t <= b < 2**(t + 1)
    amax = (2 * b + 2) // 3           # 3a <= 2b+2
    amin = b // 2 + 1                 # a > b/2
    # scan a descending from b, maintain (maxv, count) over [a,b]
    maxv = -1; cnt = 0
    v2s = [0] + [v2(n) for n in range(1, b + 1)]
    for a in range(b, amin - 1, -1):
        w = v2s[a]
        if w > maxv: maxv, cnt = w, 1
        elif w == maxv: cnt += 1
        if a > amax: continue
        R = b - a + 1
        if R < 2: continue            # R=1 handled separately by P2
        total += 1
        if a <= 2**t: case1 += 1
        else: case2 += 1
        if cnt != 1 or maxv < t - 1:
            failures.append((a, b, maxv, cnt, t))
print(f"window intervals: {total} (P2: 751899); case a<=2^t: {case1} (P2: 635421); "
      f"case a>2^t: {case2} (P2: 116478); failures (tie or s<t-1): {len(failures)} {failures[:5]}")

print()
print("=== P2-1 spot: v2(B) == s exactly, exact Fractions (window, b<=300 all + sample) ===")
bad = 0; tested = 0
random.seed(42)
samples = []
for b in range(32, 301):
    for a in range(b // 2 + 1, (2 * b + 2) // 3 + 1):
        if b - a + 1 >= 2: samples.append((a, b))
for b in range(301, 3001):
    for _ in range(3):
        a = random.randint(b // 2 + 1, (2 * b + 2) // 3)
        samples.append((a, b))
for (a, b) in samples:
    f = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
    B = f.denominator
    s = max(v2(n) for n in range(a, b + 1))
    tested += 1
    if v2(B) != s or B < 16:
        bad += 1; print("  v2(B)!=s at", a, b, v2(B), s)
print(f"spot intervals: {tested}, v2(B)!=s or B<16: {bad}")

print()
print("=== P2-1 analytic bound: Riemann sum and combination, exact ===")
rs = Fraction(1, 4) * (1 + Fraction(4, 5) + Fraction(2, 3) + Fraction(4, 7))
print(f"(1/4)(1+4/5+2/3+4/7) = {rs} ; claimed 319/420 = {Fraction(319,420)} ; equal: {rs == Fraction(319,420)}")
comb = Fraction(319, 420) + Fraction(1, 17) + Fraction(1, 16)
print(f"319/420 + 1/17 + 1/16 = {comb} ; claimed 25157/28560 ; equal: {comb == Fraction(25157,28560)} ; <1: {comb < 1}")
# H <= 319/420 + 1/a exact spot check on ALL window intervals b<=400:
viol = 0; mx = Fraction(0)
for b in range(32, 401):
    for a in range(b // 2 + 1, (2 * b + 2) // 3 + 1):
        H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
        if H > Fraction(319, 420) + Fraction(1, a): viol += 1; print("  bound violated", a, b)
        if H > mx: mx = H
print(f"window b<=400 exact: H <= 319/420 + 1/a violations: {viol}; max H seen: {float(mx):.6f}")

print()
print("=== P2-2: Lemma S chain: H < R/a, B > a/R, (A+1)/B < 2R/a, A+1<B if a>2R ===")
bad = 0; tested = 0
for R in range(2, 41):
    for a in range(1, 3001):
        b = a + R - 1
        f = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
        A, B = f.numerator, f.denominator
        tested += 1
        if not (f < Fraction(R, a)): bad += 1; print("  H!<R/a", a, b)
        if not (B * R > a): bad += 1; print("  B!>a/R at", a, b, B, a / R)
        if not (Fraction(A + 1, B) < Fraction(2 * R, a)): bad += 1; print("  (A+1)/B!<2R/a", a, b)
        if a > 2 * R and not (A + 1 < B): bad += 1; print("  A+1<B fails (would be solution?)", a, b)
        if a == 2 * R and not (Fraction(A + 1, B) < 1): bad += 1; print("  a=2R boundary: (A+1)/B !< 1 at", a, b)
print(f"intervals (2<=R<=40, a<=3000): {tested}, chain failures: {bad}")
# R=1 exact: solutions iff a | 2
r1 = [a for a in range(1, 1000) if (1 + 1) % a == 0]
print(f"R=1: (A+1)/B = 2/a integer iff a in {r1} (expect [1, 2])")

# ---------- sieve data (own implementation) for family + map ----------
SPF = spf_upto(6000)
def sieve_data(a, b):
    """Returns (A, B, P1 list, good residues dict, bad list)."""
    L = 1
    for n in range(a, b + 1): L = L * n // gcd(L, n)
    N = sum(L // n for n in range(a, b + 1))
    g = gcd(N, L); A, B = N // g, L // g
    cand = set()
    for n in range(a, b + 1):
        m = n
        while m > 1:
            p = SPF[m]
            if p != 2 and p * p > b: cand.add(p)
            while m % p == 0: m //= p
    P1 = []; badp = []; res = {}
    for p in sorted(cand):
        first = -(-a // p) * p
        T = 0; m = first
        while m <= b:
            T = (T + pow(m // p, -1, p)) % p; m += p
        if T != 0:
            P1.append(p); res[p] = (-p * pow(T, -1, p)) % (p * p)
        else:
            badp.append(p)
    return A, B, L, P1, res, badp

print()
print("=== P2-3: Theorem F family, primes P = 1 mod 4, P <= 2000 ===")
P4 = [p for p in primes_upto(2000) if p % 4 == 1]
print(f"primes P=1 mod 4, P<=2000: {len(P4)} (P2: 147)")
fam_fail = []; intervals = set()
for P in P4:
    f = 1
    for k in range(2, (P - 1) // 2 + 1): f = f * k % P
    nP = min(f, P - f)
    assert (nP * nP + 1) % P == 0
    a = nP * nP; b = a + 1
    A, B, L, P1, res, badp = sieve_data(a, b)
    intervals.add((a, b))
    ok = (P1 == [P] and B == a * (a + 1) == L and not badp
          and B % (P * P) == res[P]
          and Fraction(A + 1, B) == Fraction(2, a)
          and Fraction(2, a).denominator != 1)
    # v_p(B)=1 at the good prime:
    ok = ok and (B % P == 0 and B % (P * P) != 0)
    if not ok:
        fam_fail.append((P, nP, a, P1, B == a * (a + 1), badp))
print(f"family failures: {len(fam_fail)} {fam_fail[:5]}; distinct intervals: {len(intervals)}")
# brute-force cross-check of P1 for P <= 200 (scan ALL odd primes p<=b, p^2>b):
bf_fail = 0
for P in [p for p in P4 if p <= 200]:
    f = 1
    for k in range(2, (P - 1) // 2 + 1): f = f * k % P
    nP = min(f, P - f); a = nP * nP; b = a + 1
    P1bf = []
    for p in primes_upto(b):
        if p == 2 or p * p <= b: continue
        mults = [n for n in range(a, b + 1) if n % p == 0]
        if not mults: continue
        T = sum(pow(n // p, -1, p) for n in mults) % p
        if T != 0: P1bf.append(p)
    if P1bf != [P]: bf_fail += 1; print("  brute P1 mismatch", P, P1bf)
print(f"brute-force P1 cross-check P<=200: mismatches: {bf_fail}")

print()
print("=== P2 map of the 83: in-class intervals b<=300, own recompute ===")
inclass = []
for b in range(1, 301):
    for a in range(1, b + 1):
        A, B, L, P1, res, badp = sieve_data(a, b)
        if not P1: continue
        if all(B % (p * p) == res[p] for p in P1):
            inclass.append((a, b, A, B, P1, badp))
def is_sol(A, B):
    inv = Fraction(1, 1) / (1 - (Fraction(A, B) - (A // B)))
    return inv.denominator == 1
sols = []; nonsol = []
for (a, b, A, B, P1, badp) in inclass:
    f = Fraction(A, B)
    frac = f - (f.numerator // f.denominator)
    if f == 1 or (frac != 0 and (1 / (1 - frac)).denominator == 1):
        sols.append((a, b))
    else:
        nonsol.append((a, b, A, B, P1, badp))
print(f"in-class total: {len(inclass)} (P2: 83); solutions among them: {sols} (P2: [(1,3),(2,3),(3,6)])")
from collections import Counter
print(f"nonsol R distribution: {sorted(Counter(b - a + 1 for a, b, *_ in nonsol).items())} (P2: R2:74,R3:3,R4:1,R5:1,R6:1)")
print(f"nonsol in regime (ii): {sum(1 for a, b, *_ in nonsol if 2 * a > b)} of {len(nonsol)} (P2: 78 of 80)")
# structural conditions + least witness
struct_fail = 0; wit = Counter()
for (a, b, A, B, P1, badp) in [(x[0], x[1], x[2], x[3], x[4], x[5]) for x in inclass]:
    for p in P1:
        if (B // p) % p == 0 or B % p != 0: struct_fail += 1  # v_p(B) != 1
    for p in badp:
        if B % p == 0: struct_fail += 1                        # v_p(B) != 0
    if L % B != 0 and False: pass
for (a, b, A, B, P1, badp) in nonsol:
    # prime powers p^e || B with A != -1 mod p^e
    BB = B; least = None
    m = BB; facs = {}
    while m > 1:
        p = SPF[m]; e = 0
        while m % p == 0: m //= p; e += 1
        facs[p] = e
    for p in sorted(facs):
        pe = p ** facs[p]
        if A % pe != pe - 1:
            least = p; break
    if least is None:
        wit['NONE?!'] += 1
    elif least == 2: wit['p=2'] += 1
    elif least * least <= b: wit['odd p, p^2<=b'] += 1
    else: wit['SIEVE PRIME'] += 1
print(f"structural failures among 83: {struct_fail} (P2: 0)")
print(f"least-witness classes: {dict(wit)} (P2: p=2: 37, odd p^2<=b: 43, sieve: 0)")
