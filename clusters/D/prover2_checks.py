#!/usr/bin/env python3
"""
Cluster D, Prover 2 (quadratic route): exact checks.

All decisions in exact integer / Fraction arithmetic.  Floats are used
ONLY to report logarithms (sizes), never to decide an identity.

Parts
 1. The four certified L=2 near-miss intervals of CENSUS0.md:
    recompute H(a,b)=A/B from scratch, check B=c(c+1), check the
    numerator residue, then build the quadratic-route data
    (extracted large part P, smooth cofactor W, Y=2c+1) and verify
    Y^2 = 1+4PW, the splitting, and its idempotence exactly.
 2. Random consecutive pairs: the identity and the splitting are
    verified for every sampled pair (tautology test).
 3. Balanced synthetic partitions for b in {50,100,200,400}:
    partition the primes in (z_b,b] greedily by log-weight into
    P0,P1 with log P_i ~ b/2; take the Bezout (CRT) representatives
    u1 = P1^{-1} mod P0, u0 = (P1*u1-1)/P0, so P1*u1-P0*u0=1 holds
    exactly; verify Y^2=1+4PW with W=u0*u1; record log W against the
    forced bound scale b/log b (the representatives are generically
    LARGE: identity + balanced partition do not imply small W).
 4. Candidate-contradiction probes on all data above: mod-p sign
    condition, Y mod q for q|W, parity/mod-8, Legendre symbols
    (W/p) for p|P and (P/q) for q|W (record the sign distribution:
    a usable reciprocity contradiction would need a forced sign).
"""
import json, math, random
from fractions import Fraction
from math import gcd, isqrt, log

OUT = {}

def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * len(sieve[i*i::i])
    return [i for i, v in enumerate(sieve) if v]

def factor(n, primes):
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

def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

def splitting(P, W, Y):
    """The mandated splitting of Y^2=1+4PW. Returns dict or raises."""
    assert Y * Y == 1 + 4 * P * W
    A, B = (Y - 1) // 2, (Y + 1) // 2
    assert B - A == 1 and A * B == P * W and gcd(A, B) == 1
    Pp, Ppp = gcd(P, A), gcd(P, B)
    assert Pp * Ppp == P and gcd(Pp, Ppp) == 1
    Wp, Wpp = A // Pp, B // Ppp
    assert Wp * Wpp == W and Ppp * Wpp - Pp * Wp == 1
    # idempotence: splitting the split equation returns the same Y, parts
    Y2 = 2 * A + 1
    assert Y2 == Y and gcd(Pp * Ppp, A) == Pp and gcd(Pp * Ppp, B) == Ppp
    return dict(A=A, B=B, Pp=Pp, Ppp=Ppp, Wp=Wp, Wpp=Wpp)

# ---------------------------------------------------------------- Part 1
near = [  # (a, b) from CENSUS0.md, Section 3 table
    (4, 7), (5, 7), (9, 12), (154, 156),
]
primes = primes_upto(100000)
part1 = []
for (a, b) in near:
    H = sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))
    A, B = H.numerator, H.denominator
    c = isqrt(B)
    assert c * (c + 1) == B and c > b
    residue = (A + 2 * c + 1) % B
    total = H + Fraction(2 * c + 1, c * (c + 1))
    assert total.denominator != 1 and residue != 0  # near miss: fails
    z = b / log(b)  # z_b at eps=0, for extraction only (small-b analogue)
    fc, fc1 = factor(c, primes), factor(c + 1, primes)
    P0 = P1 = 1
    for p in fc:
        if p > z: P0 *= p
    for p in fc1:
        if p > z: P1 *= p
    u0, u1 = c // P0, (c + 1) // P1
    P, W, Y = P0 * P1, u0 * u1, 2 * c + 1
    assert P * W == c * (c + 1) and P1 * u1 - P0 * u0 == 1
    sp = splitting(P, W, Y)
    assert (sp["Pp"], sp["Ppp"], sp["Wp"], sp["Wpp"]) == (P0, P1, u0, u1)
    inrange = [p for p in primes_upto(b) if p > z]
    missing = [p for p in inrange if c % p and (c + 1) % p]
    part1.append(dict(a=a, b=b, A=A, B=B, c=c, residue=residue,
                      exact_sum=str(total), z_b_eps0=round(z, 4),
                      P0=P0, P1=P1, u0=u0, u1=u1, P=P, W=W, Y=Y,
                      identity_ok=True, splitting_recovers=True,
                      primes_in_range=inrange,
                      primes_in_range_missing_from_c_cplus1=missing,
                      legendre_W_mod_p={str(p): legendre(W, p)
                                        for p in factor(P, primes)}))
OUT["part1_near_misses"] = part1

# ---------------------------------------------------------------- Part 2
rng = random.Random(288)
tests = fails = 0
sign_patterns = set()
for _ in range(2000):
    c = rng.randrange(2, 10**7)
    z = max(2.0, log(c) / 2)  # arbitrary extraction threshold
    fc, fc1 = factor(c, primes), factor(c + 1, primes)
    P0 = P1 = 1
    for p in fc:
        if p > z: P0 *= p
    for p in fc1:
        if p > z: P1 *= p
    u0, u1 = c // P0, (c + 1) // P1
    P, W, Y = P0 * P1, u0 * u1, 2 * c + 1
    tests += 1
    try:
        sp = splitting(P, W, Y)
        assert (sp["Wp"], sp["Wpp"]) == (u0, u1)
        sign_patterns.add(tuple(
            1 if (Y % p) == 1 else -1 for p in sorted(factor(P, primes))[:3]))
    except AssertionError:
        fails += 1
OUT["part2_random_consecutive"] = dict(tests=tests, identity_failures=fails,
                                       distinct_sign_prefixes=len(sign_patterns))

# ---------------------------------------------------------------- Part 3
part3 = []
for b in (50, 100, 200, 400):
    z = b / log(b)
    ps = [p for p in primes_upto(b) if p > z]
    # greedy log-balanced partition
    s0 = s1 = 0.0
    S0, S1 = [], []
    for p in sorted(ps, reverse=True):
        if s0 <= s1:
            S0.append(p); s0 += log(p)
        else:
            S1.append(p); s1 += log(p)
    P0 = math.prod(S0); P1 = math.prod(S1)
    assert gcd(P0, P1) == 1
    u1 = pow(P1, -1, P0)            # P1*u1 = 1 (mod P0), 1 <= u1 < P0
    assert (P1 * u1 - 1) % P0 == 0
    u0 = (P1 * u1 - 1) // P0        # 0 < u0 < P1
    assert P1 * u1 - P0 * u0 == 1
    P, W, Y = P0 * P1, u0 * u1, 2 * P0 * u0 + 1
    sp = splitting(P, W, Y)
    assert (sp["Pp"], sp["Ppp"]) == (P0, P1)
    # smoothness of the Bezout cofactors: largest prime factor
    def lpf(n):
        return max(factor(n, primes)) if n > 1 else 1
    part3.append(dict(
        b=b, z_b=round(z, 3), n_primes=len(ps),
        logP0=round(log(P0), 3), logP1=round(log(P1), 3), b_over_2=b / 2,
        logP=round(log(P), 3), logW=round(log(W), 3),
        forced_scale_b_over_logb=round(b / log(b), 3),
        logW_over_forced_scale=round(log(W) / (b / log(b)), 3),
        lpf_u0=lpf(u0), lpf_u1=lpf(u1), z_b_rounded=round(z),
        u0_is_zb_smooth=lpf(u0) <= z, u1_is_zb_smooth=lpf(u1) <= z,
        identity_ok=True, splitting_recovers=True,
        Y_mod_4=Y % 4))
OUT["part3_balanced_synthetic"] = part3

# ---------------------------------------------------------------- Part 4
# Legendre sign distribution on the synthetic data: is any symbol forced?
signs_Wmodp, signs_Pmodq = [], []
for row in part3:
    b = row["b"]; z = b / log(b)
    ps = [p for p in primes_upto(b) if p > z]
    # rebuild P0,P1,u0,u1 exactly as in Part 3
    s0 = s1 = 0.0; S0, S1 = [], []
    for p in sorted(ps, reverse=True):
        if s0 <= s1: S0.append(p); s0 += log(p)
        else: S1.append(p); s1 += log(p)
    P0 = math.prod(S0); P1 = math.prod(S1)
    u1 = pow(P1, -1, P0); u0 = (P1 * u1 - 1) // P0
    W = u0 * u1
    for p in ps:
        signs_Wmodp.append(legendre(W, p))
    for q in factor(W, primes):
        if q > 2:
            signs_Pmodq.append(legendre(P0 * P1, q))
OUT["part4_legendre_distributions"] = dict(
    W_mod_p={s: signs_Wmodp.count(s) for s in (-1, 0, 1)},
    P_mod_q={s: signs_Pmodq.count(s) for s in (-1, 0, 1)})

# ---------------------------------------------------------------- Part 5
# Abstract identity WITHOUT the smoothness of W: a prime of P can leak
# into the corresponding W-part.  A=24, B=25, PW=600, P=15, W=40:
# p=5 divides P'' and also W''=5.  In the forced ranges this is excluded
# only because p>z_b and W is z_b-smooth (so p does not divide W).
sp5 = splitting(15, 40, 49)
assert sp5["A"] == 24 and sp5["B"] == 25 and sp5["Ppp"] == 5 and sp5["Wpp"] == 5
OUT["part5_smoothness_leak_example"] = dict(
    P=15, W=40, Y=49, A=24, B=25, Pp=sp5["Pp"], Ppp=sp5["Ppp"],
    Wp=sp5["Wp"], Wpp=sp5["Wpp"], leaked_prime=5)

print(json.dumps(OUT, indent=1))
with open("prover2_results.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("ALL EXACT ASSERTIONS PASSED")
