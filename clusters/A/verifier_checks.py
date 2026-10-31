#!/usr/bin/env python3
"""
Verifier (Cluster A, independent) checks for Nayak Theorem 3.2 / Lemma 3.1.
Exact rational arithmetic only (fractions.Fraction, integer arithmetic).
Written before reading auditor1/auditor2/redteam reports.

Checks:
 1. Four listed pairs have integer H(I)+H(J); near-miss ([1,1],[1,2]) = 5/2.
 2. Exhaustive: all intersecting unordered interval pairs, endpoints <= 60,
    exactly the four have integer sum.
 3. Lemma 3.1 predicate: for all 1 <= r < s <= 500 (so s>=3 cases included;
    also r<s with s<3 checked separately for scope), exists odd prime p
    dividing exactly one integer in [r,s].
 4. Valuation mechanism: for sampled intersecting (I,J) with union [r,s],
    s>=3, s-r+1>=2, let p be (a) odd prime found in check 3 for [r,s].
    Verify: p divides exactly one n0 in [r,s]; e=v_p(n0)>=1;
    v_p(mu(n0)/n0) = -e (mu in {1,2}, p odd => v_p(mu)=0);
    all other terms have valuation >= 0 > -e; hence unique minimum -e;
    and exact v_p(H(I)+H(J)) == -e < 0 (so sum not integer).
    Includes forced cases where n0 lies in the overlap I∩J (mu(n0)=2).
"""
from fractions import Fraction
from math import gcd
import json, random, sys

def H(a, b):
    return sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))

def vp_int(n, p):
    if n == 0:
        return None
    n = abs(n); e = 0
    while n % p == 0:
        n //= p; e += 1
    return e

def vp_frac(x: Fraction, p):
    return vp_int(x.numerator, p) - vp_int(x.denominator, p)

def primes_upto(N):
    sieve = [True] * (N + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = [False] * len(sieve[i*i::i])
    return [i for i, v in enumerate(sieve) if v]

PRIMES = primes_upto(5000)
ODD_PRIMES = [p for p in PRIMES if p % 2 == 1]

def lemma_prime(r, s):
    """Return an odd prime dividing exactly one integer in [r,s], or None."""
    for p in ODD_PRIMES:
        if p > 2 * s and p > s:
            # a prime > s can divide no element; primes <= s suffice to test,
            # but a prime in (s, ...] divides none, so break after p>s and
            # count==0 for all larger too -- actually any p>s divides none.
            if p > s:
                break
        cnt = sum(1 for n in range(r, s + 1) if n % p == 0)
        if cnt == 1:
            return p
    return None

results = {}

# ---- Check 1 ----
four = [((1,1),(1,1)), ((1,2),(1,2)), ((1,2),(2,2)), ((2,2),(2,2))]
c1 = []
for I, J in four:
    tot = H(*I) + H(*J)
    c1.append({"I": I, "J": J, "sum": str(tot), "is_integer": tot.denominator == 1})
near = H(1,1) + H(1,2)
results["check1"] = {"pairs": c1, "all_integer": all(x["is_integer"] for x in c1),
                     "near_miss_11_12": str(near), "near_miss_is_5_2": near == Fraction(5,2)}
print("CHECK1", results["check1"])

# ---- Check 2 ----
N = 60
intervals = [(a,b) for a in range(1, N+1) for b in range(a, N+1)]
found = []
pairs_tested = 0
for ii, I in enumerate(intervals):
    for J in intervals[ii:]:  # unordered, up to swapping
        if max(I[0], J[0]) > min(I[1], J[1]):
            continue  # disjoint
        pairs_tested += 1
        if (H(*I) + H(*J)).denominator == 1:
            found.append((I, J))
results["check2"] = {"bound": N, "intersecting_unordered_pairs_tested": pairs_tested,
                     "integer_sum_pairs": [[list(a), list(b)] for a,b in found],
                     "exactly_the_four": sorted(found) == sorted(four)}
print("CHECK2 tested", pairs_tested, "found", found)

# ---- Check 3 ----
fail = []
tested3 = 0
for r in range(1, 500):
    for s in range(r+1, 501):
        tested3 += 1
        if lemma_prime(r, s) is None:
            fail.append((r, s))
fail_in_scope = [x for x in fail if x[1] >= 3]  # Lemma 3.1 requires s>=3
results["check3"] = {"r_lt_s_le_500_tested": tested3, "failures": fail[:20],
                     "num_failures": len(fail),
                     "failures_with_s_ge_3": fail_in_scope,
                     "num_failures_with_s_ge_3": len(fail_in_scope),
                     "note": "sole failure (1,2) has s=2<3, outside the lemma's hypothesis"}
print("CHECK3 tested", tested3, "failures", len(fail), fail[:10])

# ---- Check 4 ----
def check_union(I, J, p_override=None):
    r = min(I[0], J[0]); s = max(I[1], J[1])
    mu = {n: (1 if I[0] <= n <= I[1] else 0) + (1 if J[0] <= n <= J[1] else 0)
          for n in range(r, s+1)}
    p = p_override if p_override is not None else lemma_prime(r, s)
    assert p is not None and p % 2 == 1
    divs = [n for n in range(r, s+1) if n % p == 0]
    assert len(divs) == 1, (I, J, p, divs)
    n0 = divs[0]; e = vp_int(n0, p); assert e >= 1
    vals = {n: vp_frac(Fraction(mu[n], n), p) for n in range(r, s+1)}
    ok_unique = vals[n0] == -e and all(v > -e for n, v in vals.items() if n != n0)
    ok_others_nonneg = all(vals[n] >= 0 for n in vals if n != n0)
    total = H(*I) + H(*J)
    vtot = vp_frac(total, p)
    return {"I": I, "J": J, "union": [r, s], "p": p, "n0": n0, "e": e,
            "mu_n0": mu[n0], "val_n0": vals[n0],
            "unique_min": ok_unique, "others_nonneg": ok_others_nonneg,
            "vp_total_exact": vtot, "vp_total_eq_minus_e": vtot == -e,
            "total_is_integer": total.denominator == 1}

random.seed(28832)
cases = []
# systematic small cases
for a in range(1, 12):
    for b in range(a, 12):
        for c in range(1, 12):
            for d in range(c, 12):
                I, J = (a,b), (c,d)
                if max(a,c) > min(b,d): continue
                r, s = min(a,c), max(b,d)
                if s >= 3 and s - r + 1 >= 2:
                    cases.append((I,J))
sample = random.sample(cases, 300)
overlap_cases = []
# force overlap cases: search until we have >=100 with mu(n0)==2
for I, J in cases:
    r, s = min(I[0],J[0]), max(I[1],J[1])
    p = lemma_prime(r, s)
    if p is None: continue
    n0 = [n for n in range(r, s+1) if n % p == 0][0]
    if I[0] <= n0 <= I[1] and J[0] <= n0 <= J[1]:
        overlap_cases.append((I,J))
    if len(overlap_cases) >= 150: break
# also larger random unions
big = []
for _ in range(200):
    a = random.randint(1, 400); b = random.randint(a, min(500, a+random.randint(0,80)))
    c = random.randint(max(1,a-40), 450); d = random.randint(c, min(500, c+random.randint(0,80)))
    I, J = (a,b), (c,d)
    if max(a,c) > min(b,d): continue
    r, s = min(a,c), max(b,d)
    if s >= 3 and s - r + 1 >= 2:
        big.append((I,J))

all_runs = []
for I, J in sample + overlap_cases + big:
    rec = check_union(I, J)
    all_runs.append(rec)
n_overlap_run = sum(1 for x in all_runs if x["mu_n0"] == 2)
all_ok = all(x["unique_min"] and x["others_nonneg"] and x["vp_total_eq_minus_e"]
             and not x["total_is_integer"] for x in all_runs)
results["check4"] = {"cases_run": len(all_runs), "overlap_mu2_cases": n_overlap_run,
                     "all_ok": all_ok,
                     "example_overlap": next((x for x in all_runs if x["mu_n0"]==2), None),
                     "example_plain": all_runs[0] if all_runs else None}
print("CHECK4 cases", len(all_runs), "overlap mu=2:", n_overlap_run, "all_ok", all_ok)
print("CHECK4 example overlap", results["check4"]["example_overlap"])

with open("verifier_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("OVERALL", results["check1"]["all_integer"] and results["check1"]["near_miss_is_5_2"]
      and results["check2"]["exactly_the_four"] and results["check3"]["num_failures_with_s_ge_3"]==0
      and results["check4"]["all_ok"])
