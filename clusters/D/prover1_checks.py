#!/usr/bin/env python3
"""
Cluster D, Prover 1: exact computations.

Part A: independent exact census spot-check, b <= 250 (Fraction prefix sums).
        Finds every interval whose reduced denominator B is pronic,
        B = c(c+1) with c > b (the L=2 denominator near-misses), and
        verifies each fails the numerator congruence exactly.
Part B: for each near-miss, exact measurements relative to the forced form:
        with eps = 1/2, Z = floor(2b / ln b) (the integer threshold used for
        this finite measurement only), factor c and c+1 exactly (trial
        division), compute P_i(Z) = product of primes in (Z, b] dividing
        c+i, u_i(Z) = (c+i)/P_i(Z), the coverage of the prime range (Z, b]
        by c(c+1), and log-size comparisons (floats used ONLY to report
        logarithms of exact integers; every decision is exact).
Part C: exact prime counts for the prime-square forcing lemma.
        For b in a geometric range and T_b = floor(ln b / 4) (integer),
        K(b) = #{primes p : sqrt(b/T_b) < p <= sqrt(b)} is computed by an
        exact sieve; the resulting lower bound K(b) * ln(b/T_b) on
        log(u0*u1) is evaluated in float for display, and compared with
        the Theorem 14.2 upper scale 2b/((1-eps) ln b), eps = 1/2.
Part D: for each near-miss, exact list of prime squares p^2 (p <= sqrt(b))
        dividing c or c+1.
All decisions are exact integer / Fraction arithmetic.
"""
import json, math
from fractions import Fraction
from math import isqrt, log, floor

# ---------- Part A: census spot check b <= 250 ----------
BMAX = 250
prefix = [Fraction(0, 1)]
for n in range(1, BMAX + 1):
    prefix.append(prefix[-1] + Fraction(1, n))

near_misses = []
for b in range(1, BMAX + 1):
    for a in range(1, b + 1):
        h = prefix[b] - prefix[a - 1]
        A, B = h.numerator, h.denominator
        disc = 1 + 4 * B
        r = isqrt(disc)
        if r * r == disc and (r - 1) % 2 == 0:
            c = (r - 1) // 2
            if c > b:
                residue = (A + 2 * c + 1) % B
                total = h + Fraction(2 * c + 1, c * (c + 1))
                near_misses.append({
                    "a": a, "b": b, "A": A, "B": B, "c": c,
                    "residue_mod_B": residue,
                    "sum_numerator": total.numerator,
                    "sum_denominator": total.denominator,
                    "sum_is_integer": total.denominator == 1,
                })
print("Part A: pronic-denominator near misses, b <= 250:", len(near_misses))
for nm in near_misses:
    print("  ", nm)

# ---------- helpers: exact factorisation by trial division ----------
def factor(n):
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out

def primes_upto(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = b"\x00" * len(sieve[i * i::i])
    return [i for i in range(2, n + 1) if sieve[i]]

# ---------- Part B: forced-form measurements on the near misses ----------
partB = []
for nm in near_misses:
    b, c = nm["b"], nm["c"]
    if b < 3:
        continue
    Z = floor(2 * b / log(b))  # eps = 1/2 threshold, finite measurement only
    rng = [p for p in primes_upto(b) if p > Z]
    fac0, fac1 = factor(c), factor(c + 1)
    P = [1, 1]
    covered = []
    for p in rng:
        if c % p == 0:
            P[0] *= p; covered.append(p)
        if (c + 1) % p == 0:
            P[1] *= p; covered.append(p)
    u = [c // P[0], (c + 1) // P[1]]
    squares = []
    for p in primes_upto(isqrt(b)):
        if c % (p * p) == 0:
            squares.append((p, 0))
        if (c + 1) % (p * p) == 0:
            squares.append((p, 1))
    rec = {
        "a": nm["a"], "b": b, "c": c, "Z_eps_half": Z,
        "primes_in_(Z,b]": len(rng), "covered_by_c(c+1)": len(covered),
        "covered_primes": covered,
        "log_P0": log(P[0]) if P[0] > 1 else 0.0,
        "log_P1": log(P[1]) if P[1] > 1 else 0.0,
        "b_over_2": b / 2,
        "log_u0": log(u[0]), "log_u1": log(u[1]),
        "factor_c": {str(k): v for k, v in fac0.items()},
        "factor_c+1": {str(k): v for k, v in fac1.items()},
        "prime_squares_dividing": squares,
    }
    partB.append(rec)
    print("Part B:", json.dumps(rec))

# ---------- Part C: exact counts for the square-forcing lower bound ----------
partC = []
for b in [10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**10, 10**12]:
    Tb = floor(log(b) / 4)
    lo = isqrt(b // Tb)  # p > sqrt(b/Tb)  <=>  p >= lo+1 when Tb | ... handled below exactly
    # exact count: primes p with b/Tb < p^2 <= b, i.e. Tb*p^2 > b and p^2 <= b
    sq = isqrt(b)
    K = 0
    theta_diff = 0.0
    for p in primes_upto(sq):
        if Tb * p * p > b:
            K += 1
            theta_diff += log(p)
    lb = K * log(b / Tb)            # float display of the exact-count bound
    lb_theta = 2 * theta_diff       # float display: 2*(theta(sqrt b)-theta(sqrt(b/Tb)))
    upper_scale = 2 * b / (0.5 * log(b))  # sum of the two Thm 14.2 upper bounds, eps=1/2
    rec = {"b": b, "T_b": Tb, "K_exact": K,
           "lower_bound_K_log(b/T)": lb,
           "lower_bound_2_theta_diff": lb_theta,
           "sqrt_b": b ** 0.5,
           "ratio_lb_over_sqrt_b": lb_theta / (b ** 0.5),
           "upper_scale_2b/((1-eps)log b)": upper_scale,
           "ratio_lb_over_upper": lb_theta / upper_scale}
    partC.append(rec)
    print("Part C:", json.dumps(rec))

out = {"partA_near_misses": near_misses, "partB": partB, "partC": partC}
with open("prover1_results.json", "w") as f:
    json.dump(out, f, indent=1)
print("wrote prover1_results.json")
