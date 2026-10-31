#!/usr/bin/env python3
"""Equivalence check: u | Bb  via trial division (divides_Bb) vs via
math.gcd(u, Bb) == u, on (i) every size survivor stored in the
eps=1/4 checkpoints for b=120,150,175, (ii) 20000 random integers of
comparable size for b=150, (iii) all divisors of Bb for b=60 (positive cases)."""
import glob, json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redteam_search import primes_upto, max_prime_power_exp, divides_Bb

def setup(b, eps):
    ps = primes_upto(b)
    zb = b / ((1 - eps) * math.log(b))
    caps = [(p, max_prime_power_exp(p, b)) for p in ps if p <= zb]
    Bb = 1
    for p, e in caps: Bb *= p ** e
    return caps, Bb

random.seed(288)
tests = 0; mism = 0
here = os.path.dirname(os.path.abspath(__file__))
for path in sorted(glob.glob(os.path.join(here, "redteam_checkpoint_e25_*.json"))):
    d = json.load(open(path))
    caps, Bb = setup(d["b"], d["eps"])
    for rec in d["size_survivors_stored"]:
        for key in ("u0", "u1"):
            u = int(rec[key]); tests += 1
            if divides_Bb(u, caps) != (math.gcd(u, Bb) == u): mism += 1
for u in [random.randrange(1, 10**20) for _ in range(20000)]:
    caps, Bb = setup(150, 0.25); tests += 1
    if divides_Bb(u, caps) != (math.gcd(u, Bb) == u): mism += 1
caps, Bb = setup(60, 0.25)
# all divisors of Bb for b=60 (positive cases) plus multiples by a large prime
divs = [1]
for p, e in caps:
    divs = [x * p**k for x in divs for k in range(e + 1)]
for u in divs + [u * 101 for u in divs[:500]]:
    tests += 1
    if divides_Bb(u, caps) != (math.gcd(u, Bb) == u): mism += 1
print(f"{tests} tests, {mism} mismatches between trial-division and gcd F3 tests")
