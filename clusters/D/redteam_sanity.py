#!/usr/bin/env python3
"""Direct sanity check, independent of the partition pipeline.

For every 1 <= a <= b <= 200 compute H([a,b]) = A/B exactly with
fractions.Fraction by accumulating downward from a = b (a different
accumulation order from both census implementations' descriptions
and from interval_test in redteam_search.py).  Record:
  * intervals with B = c(c+1) for some integer c > b   (pronic near misses)
  * among them, those with A = -(2c+1) (mod B), i.e. genuine L=2 solutions
CENSUS0.md certifies for b <= 2000: exactly four pronic near misses
((4,7), (5,7), (9,12), (154,156)) and no L=2 solutions.  Restricting
to b <= 200 must therefore give exactly those four and no solutions.
"""
import json, math, os
from fractions import Fraction

def main():
    BMAX = 200
    pronic = []
    solutions = []
    for b in range(1, BMAX + 1):
        h = Fraction(0, 1)
        for a in range(b, 0, -1):
            h += Fraction(1, a)          # now h == H([a,b])
            B = h.denominator
            c = math.isqrt(B)
            if c * (c + 1) == B and c > b:
                rec = dict(a=a, b=b, c=c, A=str(h.numerator), B=str(B),
                           residue=int((h.numerator + 2 * c + 1) % B))
                pronic.append(rec)
                if rec["residue"] == 0:
                    solutions.append(rec)
    expected = [(4, 7, 20), (5, 7, 14), (9, 12, 44), (154, 156, 1364)]
    got = [(r["a"], r["b"], r["c"]) for r in pronic]
    out = dict(bmax=BMAX, pronic_near_misses=pronic, l2_solutions=solutions,
               expected_pronic=expected, matches_census0=(sorted(got) == sorted(expected) and not solutions))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "redteam_sanity.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("pronic near misses:", got)
    print("L2 solutions:", solutions)
    print("matches CENSUS0 (four near misses, no solutions):", out["matches_census0"])

if __name__ == "__main__":
    main()
