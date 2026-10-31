#!/usr/bin/env python3
"""Cluster E, Prover 2 (structural smoothness route): exact checks.

All arithmetic exact (int / fractions.Fraction / arithmetic in F_p).
Parts:
 1. Recompute, independently, the intervals b<=300 with P1 nonempty and
    den H(a,b) in the forced CRT class; classify by regime; verify that
    ALL of them satisfy every structural condition of the mandated route
    (v_p(B)=1 at good p, v_p(B)=0 at bad p, B | lcm(a..b)); for the
    non-solutions locate the least witness prime power p^e || B with
    A != -1 (mod p^e) and classify the witness prime.
 2. R=2 characterization, a<=3000 (divisor method).
 3. Infinite-family construction: primes P = 1 (mod 4), P<=2000,
    n_P = least sqrt(-1) representative <= (P-1)/2, interval
    (n_P^2, n_P^2+1): check P in P1, B in class, non-solution, distinct.
    Cross-check the divisor method against the full multiples sieve
    for P<=200.
 4. Regime (ii) mechanics: H(a,b)<1 for a>b/2, a>1, b<=300 (exact);
    unique-maximum 2-adic valuation in the dangerous window
    (a<=2R, i.e. R>=a/2) for 32<=b<=3000 (O(1) mechanism check);
    exact solution list for b<32.
 5. Fixed R=3,4,5: count in-class non-solutions for R^2<=a<=5000
    (divisor method; valid because there p^2>b and p>R force k(p)=1).
 6. Size-argument sanity: for 2<=R<=8 and 2R<a<=400, A+1<B exactly.
"""
from fractions import Fraction
from math import isqrt, gcd
from collections import Counter

def primes_upto(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]

def factorize(n, primes):
    f = {}
    for p in primes:
        if p * p > n:
            break
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e

def v2(n):
    return (n & -n).bit_length() - 1

PR300 = primes_upto(300)
INV = {p: [0, 1] + [pow(i, -1, p) for i in range(2, p)] for p in PR300 if p > 2}

def sieve_full(a, b):
    """Full multiples sieve: returns (Q, r, P1, bad)."""
    congr = []
    P1 = []
    bad = []
    for p in PR300:
        if p == 2 or p * p <= b or p > b:
            continue
        u = -(-a // p)
        tot = 0
        k = 0
        j = 0
        while p * (u + j) <= b:
            tot = (tot + INV[p][u + j]) % p
            k += 1
            j += 1
        if k == 0:
            continue
        if tot != 0:
            P1.append(p)
            congr.append(((-p * pow(tot, -1, p)) % (p * p), p * p))
        else:
            bad.append(p)
    r = 0
    M = 1
    for rp, mod in congr:
        r = r + M * (((rp - r) * pow(M % mod, -1, mod)) % mod)
        M *= mod
        r %= M
    return M, r, P1, bad

# prefix harmonic fractions to 300
H = [Fraction(0, 1)]
_s = Fraction(0, 1)
for _n in range(1, 301):
    _s += Fraction(1, _n)
    H.append(_s)

print("=== Part 1: in-class intervals, b<=300 (independent recompute) ===")
inclass = []
for b in range(1, 301):
    for a in range(1, b + 1):
        f = H[b] - H[a - 1]
        A, B = f.numerator, f.denominator
        Q, r, P1, bad = sieve_full(a, b)
        if Q > 1 and B % Q == r % Q:
            inclass.append((a, b, A, B, P1, bad))
sols = [x for x in inclass if (x[2] + 1) % x[3] == 0]
nonsol = [x for x in inclass if (x[2] + 1) % x[3] != 0]
print("in-class total:", len(inclass), " solutions:", [(a, b, B) for a, b, A, B, _, _ in sols])
print("non-solutions:", len(nonsol))
assert len(inclass) == 83 and len(nonsol) == 80
assert sorted((a, b) for a, b, *_ in sols) == [(1, 3), (2, 3), (3, 6)]
print("R distribution (nonsol):", sorted(Counter(b - a + 1 for a, b, *_ in nonsol).items()))
print("regime (ii) a>b/2: nonsol", sum(1 for a, b, *_ in nonsol if 2 * a > b),
      "of", len(nonsol), "; all in-class:", sum(1 for a, b, *_ in inclass if 2 * a > b), "of", len(inclass))
print("R=2 nonsol:", sum(1 for a, b, *_ in nonsol if b - a + 1 == 2))
# structural conditions on all 83, and witness classification on the 80
struct_fail = 0
wit_class = Counter()
for a, b, A, B, P1, bad in inclass:
    L = 1
    for n in range(a, b + 1):
        L = L * n // gcd(L, n)
    if not (all(vp(B, p) == 1 for p in P1) and all(vp(B, p) == 0 for p in bad) and L % B == 0):
        struct_fail += 1
    if (A + 1) % B != 0:
        fac = factorize(B, PR300)
        wits = [p for p, e in fac.items() if (A + 1) % (p ** e) != 0]
        assert wits and all(p not in P1 and p not in bad for p in wits)
        w = min(wits)
        wit_class['p=2' if w == 2 else 'odd p, p^2<=b'] += 1
print("structural failures (v_p good/bad, B|L) among the 83:", struct_fail)
print("least-witness class (80 nonsol):", dict(wit_class),
      " -- never a good or bad sieve prime (asserted)")

print("=== Part 2: R=2 characterization, a<=3000 ===")
PR_BIG = primes_upto(100000)
def r2_status(a):
    """P1 and per-prime congruence for (a,a+1) via endpoint divisors."""
    b = a + 1
    B = a * b
    P1 = []
    incongr = []
    for endpoint in (a, b):
        for p in factorize(endpoint, PR_BIG):
            if p == 2 or p * p <= b:
                continue
            u = endpoint // p
            P1.append(p)
            if B % (p * p) != (-p * u) % (p * p):
                incongr.append(p)
    return P1, incongr
mism = 0
for a in range(1, 3001):
    b = a + 1
    fa = factorize(a, PR_BIG)
    fb = factorize(b, PR_BIG)
    cond = all(p * p <= b for p in fa if p != 2) and any(p * p > b for p in fb if p != 2)
    P1, incongr = r2_status(a)
    if (bool(P1) and not incongr) != cond:
        mism += 1
print("characterization mismatches:", mism)
assert mism == 0

print("=== Part 3: family from primes P = 1 (mod 4), P<=2000 ===")
cnt = 0
bad = []
seen = {}
for P in primes_upto(2000):
    if P % 4 != 1:
        continue
    r = next(x for x in range(1, P) if (x * x + 1) % P == 0)
    n = min(r, P - r)
    a = n * n
    b = a + 1
    B = a * b
    P1, incongr = r2_status(a)
    issol = (2 * a + 2) % B == 0
    if not (P in P1 and not incongr and not issol):
        bad.append((P, n, a, P1, incongr, issol))
    if P <= 200:  # cross-check divisor method vs full multiples sieve
        Q, rr, P1f, badf = sieve_full(a, b)
        assert sorted(P1f) == sorted(P1) and not badf and B % Q == rr % Q
    cnt += 1
    seen.setdefault(a, []).append(P)
print("primes checked:", cnt, " failures:", bad)
print("distinct intervals:", len(seen), " max fibre:", max(len(v) for v in seen.values()))
assert not bad and cnt == 147

print("=== Part 4: regime (ii) mechanics ===")
bad = 0
cnt = 0
for b in range(2, 301):
    for a in range(b // 2 + 1, b + 1):
        if a <= 1:
            continue
        cnt += 1
        if not (H[b] - H[a - 1]) < 1:
            bad += 1
print("H<1 for a>b/2, a>1, b<=300: checked", cnt, "failures", bad)
assert bad == 0
bad = 0
cnt = 0
c1 = c2 = 0
for b in range(32, 3001):
    t = b.bit_length() - 1
    for a in range(b // 2 + 1, b + 1):
        R = b - a + 1
        if a > 2 * R:
            continue  # size case, not dangerous window
        cnt += 1
        if a <= 2 ** t:
            c1 += 1
            d = 2 ** t
            mults = list(range(-(-a // d) * d, b + 1, d))
            if mults != [d]:
                bad += 1
        else:
            c2 += 1
            d = 2 ** (t - 1)
            n0 = 3 * d
            mults = list(range(-(-a // d) * d, b + 1, d))
            if not (a <= n0 <= b) or [m for m in mults if v2(m) == t - 1] != [n0] \
               or any(v2(m) >= t for m in mults):
                bad += 1
print("2-adic unique maximum, dangerous window, 32<=b<=3000: checked", cnt,
      "case1", c1, "case2", c2, "failures", bad)
assert bad == 0
sol31 = []
for b in range(1, 32):
    for a in range(1, b + 1):
        f = H[b] - H[a - 1]
        if (f.numerator + 1) % f.denominator == 0:
            sol31.append((a, b, f.denominator))
print("solutions with b<32 (exact):", sol31)
print("  of which regime (ii) a>b/2:", [x for x in sol31 if 2 * x[0] > x[1]])

print("=== Part 5: fixed R=3,4,5 in-class non-solutions, R^2<=a<=5000 ===")
PR5 = primes_upto(6000)
def inclass_fixedR(a, R):
    b = a + R - 1
    h = sum(Fraction(1, n) for n in range(a, b + 1))
    A, B = h.numerator, h.denominator
    cand = {}
    for n in range(a, b + 1):
        for p in factorize(n, PR5):
            if p != 2 and p * p > b:
                assert p > R  # hence k(p)=1, sole multiple is n
                cand[p] = n // p
    if not cand:
        return None, A, B
    ok = all(B % (p * p) == (-p * u) % (p * p) for p, u in cand.items())
    return ok, A, B
for R in (3, 4, 5):
    cnt = 0
    sols = 0
    ex = []
    for a in range(R * R, 5001):
        r, A, B = inclass_fixedR(a, R)
        if r:
            cnt += 1
            if (A + 1) % B == 0:
                sols += 1
            elif len(ex) < 5:
                ex.append((a, a + R - 1, B))
    print(f"R={R}: in-class={cnt} solutions={sols} examples={ex}")

print("=== Part 6: size-argument sanity (A+1<B for a>2R) ===")
bad = 0
for R in range(2, 9):
    for a in range(2 * R + 1, 401):
        h = sum(Fraction(1, n) for n in range(a, a + R))
        if not h.numerator + 1 < h.denominator:
            bad += 1
print("failures:", bad)
assert bad == 0
print("ALL CHECKS DONE")
