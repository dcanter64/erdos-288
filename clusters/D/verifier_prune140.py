#!/usr/bin/env python3
"""Verifier extra: no-prune enumeration at b=140, eps=1/4 (N=22 > 20, the first
row where the producers' F1 float prune was active). Enumerates every unordered
pair once (largest prime fixed in A), one exact Bezout solve per state (own
extended Euclid), second direction by the exact swapped identity
A*(B-u0) - B*(A-u1) = 1 (asserted in integers per state). No F1 prune anywhere.
Compares F2/F3/best against redteam_checkpoint_e25_140.json. F3 by gcd test
(cross-validated against trial division in verifier_redteam.py at b<=100)."""
import json, math
from math import isqrt, gcd, log

def primes_sieve(n):
    s = bytearray([1])*(n+1); s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n)+1):
        if s[i]: s[i*i::i] = b"\x00"*len(s[i*i::i])
    return [i for i in range(2, n+1) if s[i]]

def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a//b)*y1)

b, eps = 140, 0.25
ps = primes_sieve(b)
zb = b/((1-eps)*log(b))
large = [p for p in ps if p > zb]
Bb = 1
for p in ps:
    if p <= zb:
        e = 0; q = 1
        while q*p <= b: q *= p; e += 1
        Bb *= p**e
N = len(large); Ptot = math.prod(large)
print("N", N, "zb", zb, flush=True)
p_star = large[-1]; free = large[:-1]
f2 = f3 = 0; best = None
states = 1 << (N-1)
for mask in range(states):
    A = p_star
    for i, p in enumerate(free):
        if mask >> i & 1: A *= p
    B = Ptot//A
    if B == 1:
        sols = [(A, 1, 1, 1 + A), (1, A, A - 1, 1)]  # (P0,P1,u0,u1) both directions, degenerate
        # direction 1: P0=A,P1=1 -> u0=1,u1=1+A ; direction 2: P0=1,P1=A -> u0=A-1,u1=1
        sols = [(A, 1, 1, 1 + A), (1, A, A - 1, 1)]
    elif A == 1:
        sols = [(1, B, B - 1, 1), (B, 1, 1, 1 + B)]
    else:
        g, x, y = egcd(B, A)      # x*B + y*A = 1 -> u1 = x mod A
        u1 = x % A
        if u1 == 0: u1 = A
        u0 = (B*u1 - 1)//A
        assert B*u1 - A*u0 == 1 and 1 <= u0 < B and 1 <= u1 < A
        u0s, u1s = A - u1, B - u0  # swapped direction: A*u1s - B*u0s = 1 (u0' = A-u1, u1' = B-u0)
        assert A*u1s - B*u0s == 1
        sols = [(A, B, u0, u1), (B, A, u0s, u1s)]
    for (P0, P1, u0, u1) in sols:
        mx = max(u0, u1)
        if best is None or mx < best: best = mx
        if u0 <= Bb and u1 <= Bb:
            f2 += 1
            if gcd(u0, Bb) == u0 and gcd(u1, Bb) == u1: f3 += 1
with open("/home/hatch/workspace/math-hunt/erdos-288/clusters/D/redteam_checkpoint_e25_140.json") as f:
    ck = json.load(f)
print("own no-prune: F2", f2, "F3", f3, "best", best)
print("checkpoint  : F2", ck["counts"]["f2_size"], "F3", ck["counts"]["f3_smooth"],
      "best", ck["best_directed"]["max_u"], "F1", ck["counts"]["f1_balance"], "prune", ck["prune_used"])
ok = (f2 == ck["counts"]["f2_size"] and f3 == ck["counts"]["f3_smooth"]
      and str(best) == ck["best_directed"]["max_u"])
print("PRUNE140 MATCH" if ok else "PRUNE140 MISMATCH")
json.dump({"b": b, "eps": eps, "N": N, "F2": f2, "F3": f3, "best_max_u": str(best), "match": ok},
          open("/home/hatch/workspace/math-hunt/erdos-288/clusters/D/verifier_prune140_results.json", "w"), indent=1)
