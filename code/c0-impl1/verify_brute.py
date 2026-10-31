#!/usr/bin/env python3
"""
Independent brute-force cross-check for census1.py (small ranges only).

Differences from census1.py, by design:
  * H(a, b) is recomputed by summing 1/n directly over [a, b]
    (not as H_b - H_{a-1}).
  * The L = 2 branch is checked by an explicit scan over c: the exact
    fractional parts of H(c, c+1) = 1/c + 1/(c+1) for 2 <= c <= cmax are
    tabulated in a dict, and for each (a, b) the complementary fractional
    part is looked up.  No quadratic / discriminant is used.
  * The singleton branch is checked by the direct definition: for each
    (a, b) and each candidate integer value k with 0 < k - H(a, b) <= 1,
    1 / (k - H(a, b)) must be a positive integer m; that m is recorded.
    (k - H(a, b) = 1/m <= 1 forces k to be the unique integer
    floor(H(a, b)) + 1, except when H(a, b) is integral, where
    k = H(a, b) + 1 gives m = 1; both cases are the k used here.)

Writes verify_brute.json beside this script and exits nonzero on any
mismatch with outputs/summary.json restricted to b <= bmax.
"""

import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    bmax = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    cmax = int(sys.argv[2]) if len(sys.argv) > 2 else 20000

    # Tabulate fractional parts of H(c, c+1) for the explicit c-scan.
    frac_to_c = {}
    for c in range(2, cmax + 1):
        g = Fraction(1, c) + Fraction(1, c + 1)
        frac_to_c.setdefault(g - int(g), []).append(c)

    singleton = []
    l2 = []
    for b in range(1, bmax + 1):
        f = Fraction(0, 1)
        for a in range(b, 0, -1):
            f += Fraction(1, a)        # now f == H(a, b), summed directly
            # Singleton, by the direct definition.
            k = int(f) + 1              # f > 0; int() is the floor here
            diff = k - f                # in (0, 1]
            if diff.numerator == 1:     # 1/m == diff with m = denominator
                singleton.append(
                    {"a": a, "b": b, "m": diff.denominator,
                     "disjoint": diff.denominator > b}
                )
            # L = 2, by explicit scan (lookup) over c.
            frac_f = f - int(f)
            need = (1 - frac_f) % 1     # fractional part needed from g
            for c in frac_to_c.get(need, []):
                if c > b:
                    total = f + Fraction(1, c) + Fraction(1, c + 1)
                    assert total.denominator == 1
                    l2.append({"a": a, "b": b, "c": c, "d": c + 1,
                               "sum": total.numerator})

    with open(os.path.join(HERE, "outputs", "summary.json"),
              encoding="utf-8") as fh:
        summary = json.load(fh)
    census_singleton = [s for s in summary["singleton_solutions_all"]
                        if s["b"] <= bmax]
    census_l2 = [s for s in summary["l2_solutions"] if s["b"] <= bmax]

    # The brute scan covers only c <= cmax; a census L2 hit with c > cmax
    # would not be a mismatch, so compare only census hits with c <= cmax.
    census_l2_in_range = [s for s in census_l2 if s["c"] <= cmax]

    key_s = lambda s: (s["b"], s["a"], s["m"])
    key_l = lambda s: (s["b"], s["a"], s["c"])
    singleton.sort(key=key_s)
    census_singleton.sort(key=key_s)
    l2.sort(key=key_l)
    census_l2_in_range.sort(key=key_l)
    ok_singleton = singleton == census_singleton
    ok_l2 = l2 == census_l2_in_range
    record = {
        "bmax": bmax,
        "cmax": cmax,
        "brute_singleton": singleton,
        "brute_l2_c_le_cmax": l2,
        "matches_census_singleton": ok_singleton,
        "matches_census_l2_within_cmax": ok_l2,
    }
    with open(os.path.join(HERE, "verify_brute.json"), "w",
              encoding="utf-8") as fh:
        json.dump(record, fh, indent=1)
    print("singleton matches census:", ok_singleton, singleton)
    print("L2 (c <= %d) matches census:" % cmax, ok_l2, l2)
    if not (ok_singleton and ok_l2):
        sys.exit(1)


if __name__ == "__main__":
    main()
