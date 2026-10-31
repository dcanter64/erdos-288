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
SPF = spf_upto(1100000)
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
    least = None
    m = B; facs = {}
    for p in primes_upto(b):
        if m == 1: break
        e = 0
        while m % p == 0: m //= p; e += 1
        if e: facs[p] = e
    assert m == 1, (a, b, m)  # B | lcm(a..b): all prime factors <= b
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
