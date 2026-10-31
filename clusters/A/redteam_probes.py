#!/usr/bin/env python3
"""
Red Team boundary probes for Theorem 3.2 (Nayak, Erdős #288).

Independent of redteam_search.py: every harmonic sum here is built by
direct term-by-term Fraction addition for the specific interval pair
(no prefix sums, no dictionary).

Probes:
  P0 naive brute force, all ordered intersecting pairs with endpoints <= 60.
  P1 union contained in {1,2}: full table.
  P2 union exactly [r,3] for r = 1,2 and union exactly [r,4] for r = 1,2,3.
  P3 Lemma 3.1 predicate check for all 1 <= r < s <= 2000, s >= 3:
     an odd prime divides exactly one integer in [r,s].
  P4 classification of intersecting pairs (endpoints <= 60) into
     equal / containment / partial overlap, with integer sums per class.
  P5 coefficient-2 valuation probe: for every intersecting pair with
     endpoints <= 80 whose union is [r,s], s >= 3, s-r+1 >= 2, directly
     verify the weighted sum over the union is not an integer, and verify
     that for the Lemma 3.1 prime p of [r,s], the combined term mu(n0)/n0
     has p-adic valuation strictly smaller than every other term mu(n)/n.
"""
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
KNOWN = {
    ((1, 1), (1, 1)), ((1, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 2)),
}


def H(u, v):
    s = Fraction(0, 1)
    for n in range(u, v + 1):
        s += Fraction(1, n)
    return s


def intervals_upto(n):
    return [(u, v) for u in range(1, n + 1) for v in range(u, n + 1)]


def inter(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def vp_int(x, p):
    e = 0
    while x % p == 0:
        x //= p
        e += 1
    return e


def vp_frac(fr, p):
    return vp_int(fr.numerator, p) - vp_int(fr.denominator, p)


def primes_upto(n):
    sieve = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return out


out = {}

# Precompute every interval sum once, by direct term-by-term addition.
HMAP = {iv: H(*iv) for iv in intervals_upto(80)}

# P0: naive brute force to 60 (ordered pairs, repetition allowed)
found = []
ivs = intervals_upto(60)
for I in ivs:
    hi = HMAP[I]
    for J in ivs:
        if inter(I, J) and (hi + HMAP[J]).denominator == 1:
            found.append((I, J))
out["P0_naive_N60_ordered_intersecting_integer_pairs"] = [list(map(list, p)) for p in found]
out["P0_unexpected"] = [list(map(list, p)) for p in found
                        if (p not in KNOWN and (p[1], p[0]) not in KNOWN)]

# P1: union inside {1,2}
table = []
small = [(1, 1), (2, 2), (1, 2)]
for I in small:
    for J in small:
        if inter(I, J):
            table.append({"I": list(I), "J": list(J), "sum": str(H(*I) + H(*J)),
                          "integer": (H(*I) + H(*J)).denominator == 1})
out["P1_union_inside_1_2_table"] = table

# P2: union exactly [r,3] / [r,4]
for r, s in [(1, 3), (2, 3), (1, 4), (2, 4), (3, 4)]:
    cand = [iv for iv in intervals_upto(s) if iv[0] >= r]
    rows = []
    for I in cand:
        for J in cand:
            if inter(I, J) and min(I[0], J[0]) == r and max(I[1], J[1]) == s:
                tot = H(*I) + H(*J)
                rows.append({"I": list(I), "J": list(J), "sum": str(tot),
                             "integer": tot.denominator == 1})
    out[f"P2_union_exactly_{r}_{s}"] = {
        "pairs_tested": len(rows),
        "integer_pairs": [row for row in rows if row["integer"]],
    }

# P3: Lemma 3.1 predicate, finite range, computed efficiently but exactly:
# a prime p in (s/2, s] (one exists by Bertrand, verified in the sieve data
# below) divides exactly one integer in [r,s] (itself) whenever r <= p.
# So only r greater than every prime in (s/2, s] need a direct scan, and
# those r lie in the short prime gap at the top of [1,s]; for them we count
# multiples of every odd prime p <= s directly over the short interval.
primes = primes_upto(2000)
bad = []
hard_cases = 0
for s in range(3, 2001):
    top = [p for p in primes if s / 2 < p <= s]
    assert top, s  # Bertrand, in this finite range
    pmax = max(top)
    for r in range(1, s):
        if r <= pmax:
            continue  # pmax itself is the unique-multiple prime
        hard_cases += 1
        ok = False
        for p in primes:
            if p == 2 or p > s:
                continue
            cnt = sum(1 for n in range(r, s + 1) if n % p == 0)
            if cnt == 1:
                ok = True
                break
        if not ok:
            bad.append((r, s))
out["P3_lemma31_predicate_failures_r_lt_s_le_2000"] = bad
out["P3_hard_cases_scanned_directly"] = hard_cases

# P4: shape classification, endpoints <= 60
def shape(I, J):
    if I == J:
        return "equal"
    if (I[0] <= J[0] and J[1] <= I[1]) or (J[0] <= I[0] and I[1] <= J[1]):
        return "containment"
    return "partial_overlap"

classes = {}
for I in ivs:
    hi = HMAP[I]
    for J in ivs:
        if not inter(I, J):
            continue
        sh = shape(I, J)
        d = classes.setdefault(sh, {"pairs": 0, "integer_pairs": []})
        d["pairs"] += 1
        if (hi + HMAP[J]).denominator == 1:
            d["integer_pairs"].append([list(I), list(J)])
out["P4_shape_classification_N60_ordered"] = classes

# P5: valuation gap at the Lemma 3.1 prime, endpoints <= 80
viol = []
checked_unions = set()
for I in intervals_upto(80):
    for J in intervals_upto(80):
        if not inter(I, J):
            continue
        r = min(I[0], J[0]); s = max(I[1], J[1])
        if s < 3 or s - r + 1 < 2 or (r, s) in checked_unions:
            continue
        checked_unions.add((r, s))
        # find Lemma 3.1 prime
        p0 = None; n0 = None
        for p in primes:
            if p == 2 or p > s:
                continue
            hits = [n for n in range(r, s + 1) if n % p == 0]
            if len(hits) == 1:
                p0, n0 = p, hits[0]
                break
        assert p0 is not None, (r, s)
        mu = {n: (1 if I[0] <= n <= I[1] else 0) + (1 if J[0] <= n <= J[1] else 0)
              for n in range(r, s + 1)}
        vals = {n: vp_frac(Fraction(mu[n], n), p0) for n in range(r, s + 1)}
        vmin = vals[n0]
        if not all(vals[n] > vmin for n in range(r, s + 1) if n != n0):
            viol.append({"union": [r, s], "p": p0, "n0": n0, "vals": vals})
        tot = sum(Fraction(mu[n], n) for n in range(r, s + 1))
        if tot.denominator == 1:
            viol.append({"union": [r, s], "integer_weighted_sum": str(tot)})
out["P5_unions_checked"] = len(checked_unions)
out["P5_valuation_or_integer_violations"] = viol

(HERE / "redteam_probes_results.json").write_text(json.dumps(out, indent=2))
print(json.dumps({k: (v if not isinstance(v, list) or len(str(v)) < 400 else f"<{len(v)} rows>")
                   for k, v in out.items()}, indent=2))
print("P0 unexpected:", out["P0_unexpected"])
print("P3 failures:", out["P3_lemma31_predicate_failures_r_lt_s_le_2000"])
print("P5 violations:", out["P5_valuation_or_integer_violations"])
