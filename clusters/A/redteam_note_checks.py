#!/usr/bin/env python3
"""
Red Team finite checks of individual claims in Nayak's note (Task 2).
Each check is exact (integer / Fraction arithmetic) over the stated range.

  C1 Lemma 2.4:  C(d, L) | lcm(c..d) for all 1 <= c <= d <= 300.
  C2 Theorem 14.1: den H([c, c+1]) == c(c+1) for all 1 <= c <= 2000.
  C3 Theorem 5.1 instances on the three known disjoint solutions:
     for every prime p with Q = largest p-power <= b satisfying Q > L,
     verify case (i)/(ii) and the congruence tp = -Rp^{-1} (mod p).
  C4 Theorem 4.2 / 6.1 / 10.1 instances on the three known disjoint
     solutions (divisor block, binomial divisibility, denominator bound).
  C5 Lemma 13.2 numerics: log B_b(z) / z at b = 200000, z = b / log b,
     computed exactly as a sum of prime-power logs, plus the identity
     log B_b(z) = sum_{r>=1} theta(min(z, b^{1/r})).
  C6 The seven known examples: exact sums.
"""
import json
from fractions import Fraction
from math import comb, gcd, log
from pathlib import Path

HERE = Path(__file__).resolve().parent
out = {}

def lcm(a, b):
    return a // gcd(a, b) * b

def H(u, v):
    return sum((Fraction(1, n) for n in range(u, v + 1)), Fraction(0, 1))

# C1
bad = []
for d in range(1, 301):
    for c in range(1, d + 1):
        L = d - c + 1
        m = 1
        for n in range(c, d + 1):
            m = lcm(m, n)
        if m % comb(d, L) != 0:
            bad.append((c, d))
out["C1_lemma24_failures_c_le_d_le_300"] = bad

# C2
bad = []
for c in range(1, 2001):
    if H(c, c + 1).denominator != c * (c + 1):
        bad.append(c)
out["C2_theorem141_failures_c_le_2000"] = bad

# C3 + C4 on the three known disjoint solutions
KNOWN_DISJOINT = [((1, 3), (6, 6)), ((2, 3), (6, 6)), ((3, 6), (20, 20))]
c3_rows, c4_rows = [], []
for (a, b), (c, d) in KNOWN_DISJOINT:
    L = d - c + 1
    # C4: divisor block, binomial, denominator bound
    lam_b = 1
    for n in range(1, b + 1):
        lam_b = lcm(lam_b, n)
    lam_L = 1
    for n in range(1, L + 1):
        lam_L = lcm(lam_L, n)
    c4_rows.append({
        "pair": [[a, b], [c, d]],
        "all_upper_divide_lambda_b": all(lam_b % n == 0 for n in range(c, d + 1)),
        "binom_divides_lambda_b": lam_b % comb(d, L) == 0,
        "den_upper": H(c, d).denominator,
        "den_bound_rhs": str(Fraction(comb(d, L), lam_L)),
        "den_bound_holds": Fraction(H(c, d).denominator) >= Fraction(comb(d, L), lam_L),
        "L_lt_b": L < b,
    })
    # C3: Theorem 5.1 for every prime p <= b (and p where Q defined)
    primes = [p for p in range(2, b + 1)
              if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    for p in primes:
        e = 0
        while p ** (e + 1) <= b:
            e += 1
        Q = p ** e
        if Q <= L:
            continue
        low = [n for n in range(a, b + 1) if n % Q == 0]
        Rp = sum(pow(n // Q, -1, p) for n in low) % p
        up = [n for n in range(c, d + 1) if n % Q == 0]
        if Rp == 0:
            ok = len(up) == 0
            case = "i"
            tp_ok = None
        else:
            case = "ii"
            ok = len(up) == 1
            tp_ok = ok and (up[0] // Q) % p == (-pow(Rp, -1, p)) % p
        c3_rows.append({"pair": [[a, b], [c, d]], "p": p, "Q": Q, "Rp_mod_p": Rp,
                        "upper_multiples_of_Q": up, "case": case,
                        "statement_holds": bool(ok), "tp_congruence_holds": tp_ok})
out["C3_theorem51_on_known_disjoint"] = c3_rows
out["C4_checks_on_known_disjoint"] = c4_rows

# C5
def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]

b = 200000
z = b / log(b)
zi = int(z)
primes = primes_upto(b)
logB = 0.0
for p in primes:
    if p > zi:
        break
    e = 1
    while p ** (e + 1) <= b:
        e += 1
    logB += e * log(p)
theta_sum = 0.0
r = 1
while b ** (1.0 / r) >= 2:
    lim = min(zi, int(b ** (1.0 / r)))
    theta_sum += sum(log(p) for p in primes if p <= lim)
    r += 1
out["C5_lemma132_b200000"] = {
    "z": z, "logB": logB, "logB_over_z": logB / z,
    "theta_identity_sum": theta_sum,
    "identity_abs_diff": abs(logB - theta_sum),
}

# C6
examples = [((1, 1), (1, 1)), ((1, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 2)),
            ((1, 3), (6, 6)), ((2, 3), (6, 6)), ((3, 6), (20, 20))]
out["C6_seven_examples"] = [
    {"pair": [list(I), list(J)], "sum": str(H(*I) + H(*J))}
    for I, J in examples]

(HERE / "redteam_note_checks_results.json").write_text(json.dumps(out, indent=2))
print("C1 failures:", out["C1_lemma24_failures_c_le_d_le_300"])
print("C2 failures:", out["C2_theorem141_failures_c_le_2000"])
print("C3 all hold:", all(r["statement_holds"] and (r["tp_congruence_holds"] in (True, None))
                           for r in c3_rows), f"({len(c3_rows)} prime instances)")
print("C4 all hold:", all(r["all_upper_divide_lambda_b"] and r["binom_divides_lambda_b"]
                          and r["den_bound_holds"] and r["L_lt_b"] for r in c4_rows))
print("C5:", out["C5_lemma132_b200000"])
print("C6:", out["C6_seven_examples"])
