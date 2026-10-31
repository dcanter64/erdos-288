#!/usr/bin/env python3
"""
Independent second implementation for the Theorem 3.2 search (Red Team).

Completely different route from redteam_search.py (which uses exact
Fraction fractional parts):

  * Work modulo two primes P1, P2, both > N (so every denominator 1..N is
    invertible mod Pi).  prefix harmonic sums are computed with modular
    inverses; an interval's value mod Pi is pref[v] - pref[u-1] mod Pi.
  * A pair of intervals can have an integer sum only if, for both primes,
    val(I) + val(J) == K (mod Pi) for the *same* integer K, where
    1 <= K <= 14: every interval sum is positive and at most H([1,1000])
    < 7.5 (asserted exactly with Fractions below), so a pair sum lies in
    (0, 15) and its integer value, if any, is in 1..14.
  * Hence no integer-sum pair can escape the modular dictionary: for each
    interval I and each K in 1..14 we look up the complementary key
    (K - val1(I) mod P1, K - val2(I) mod P2).  This is a necessary
    condition, so the candidate set is a superset of the true set.
  * Every candidate is then verified by direct exact Fraction addition.

Usage: python3 redteam_verify_modular.py 1000
Output: redteam_verify_modular_N.json ; compared against the primary
redteam_results_N.json by the driver code at the bottom.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1, P2 = 1000003, 1000033  # both prime, both > 1000 >= N


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1 if i == 2 else 2
    return True


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    assert is_prime(P1) and is_prime(P2) and P1 > n and P2 > n

    # Exact bound for the possible integer values K.
    hn = sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0, 1))
    assert Fraction(0) < hn < Fraction(15, 2), hn
    kmax = 14  # pair sum in (0, 15)

    def mod_prefix(p):
        pref = [0] * (n + 1)
        for k in range(1, n + 1):
            pref[k] = (pref[k - 1] + pow(k, -1, p)) % p
        return pref

    pref1, pref2 = mod_prefix(P1), mod_prefix(P2)
    records = []  # (u, v, val1, val2)
    index = {}
    for v in range(1, n + 1):
        for u in range(1, v + 1):
            key = ((pref1[v] - pref1[u - 1]) % P1, (pref2[v] - pref2[u - 1]) % P2)
            records.append((u, v) + key)
            index.setdefault(key, []).append(len(records) - 1)
    assert len(records) == n * (n + 1) // 2

    def hexact(u, v):
        return sum((Fraction(1, k) for k in range(u, v + 1)), Fraction(0, 1))

    found_all, found_inter, cand, false_pos = [], [], 0, []
    for idx, (u, v, a1, a2) in enumerate(records):
        for k in range(1, kmax + 1):
            comp = ((k - a1) % P1, (k - a2) % P2)
            for jdx in index.get(comp, ()):
                if jdx < idx:
                    continue
                cand += 1
                I = (u, v); J = (records[jdx][0], records[jdx][1])
                tot = hexact(*I) + hexact(*J)
                if tot.denominator != 1:
                    # Expected: with ~1.25e11 interval pairs and moduli whose
                    # product is ~1e12, O(1) double-modulus collisions occur.
                    # Exact arithmetic rejects them; they are not solutions.
                    false_pos.append({"pair": [list(I), list(J)], "claimed_K": k})
                    continue
                assert int(tot) == k, (I, J, tot, k)
                found_all.append(((I, J), k))
                if max(I[0], J[0]) <= min(I[1], J[1]):
                    found_inter.append(((I, J), k))

    out = {
        "N": n,
        "moduli": [P1, P2],
        "intervals_enumerated": len(records),
        "candidates_from_modular_dictionary": cand,
        "candidates_rejected_by_exact_arithmetic": false_pos,
        "integer_sum_pairs_all_positions": [
            {"pair": [list(p[0]), list(p[1])], "sum": s} for p, s in found_all],
        "integer_sum_pairs_intersecting": [
            {"pair": [list(p[0]), list(p[1])], "sum": s} for p, s in found_inter],
    }
    (HERE / f"redteam_verify_modular_{n}.json").write_text(json.dumps(out, indent=2))

    primary = json.loads((HERE / f"redteam_results_{n}.json").read_text())

    def as_set(lst):
        return {(tuple(map(tuple, e["pair"])), e["sum"]) for e in lst}

    agree_all = as_set(primary["integer_sum_pairs_all_positions"]) == as_set(out["integer_sum_pairs_all_positions"])
    agree_inter = as_set(primary["integer_sum_pairs_intersecting"]) == as_set(out["integer_sum_pairs_intersecting"])
    print("candidates from modular dictionary:", cand)
    print("candidates rejected by exact arithmetic (double-modulus collisions):",
          len(false_pos), false_pos)
    print("all-position pairs agree with primary Fraction search:", agree_all)
    print("intersecting pairs agree with primary Fraction search:", agree_inter)
    print(json.dumps(out["integer_sum_pairs_intersecting"], indent=2))


if __name__ == "__main__":
    main()
