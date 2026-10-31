#!/usr/bin/env python3
"""Independent small-b check of redteam_search.py.

Different method: enumerate ALL directed subsets directly (no Gray code,
no complement symmetry, no swapped-identity shortcut), solve
P1*u1 - P0*u0 = 1 with an explicit extended-Euclidean algorithm,
and compare F2/F3 counts and the best (minimal) max(u0,u1) against the
checkpoint JSON produced by redteam_search.py.
"""
import json, math, sys, os

def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = b"\x00" * (((n - i*i)//i) + 1)
    return [i for i, v in enumerate(sieve) if v]

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def minimal(P0, P1):
    # P1*u1 - P0*u0 = 1 ; find integers x,y with P1*x - P0*y = 1 via egcd on (P1,P0)
    g, x, y = egcd(P1, P0)   # P1*x + P0*y = g = 1
    assert g == 1
    u1, u0 = x, -y           # P1*u1 - P0*u0 = 1
    # general solution: u1 += t*P0, u0 += t*P1 ; shift to minimal positive u0 in 1..P1
    if P1 == 1:
        return 1, 1 + P0
    t = (-u0) % P1
    # choose representative u0' = u0 + t*P1 in 0..P1-1, then if 0 use P1 and adjust
    u0b = (u0 + t * P1) % P1
    if u0b == 0:
        u0b = P1
    # recompute u1 exactly from equation using the t that gives u0b
    # u0b = u0 + T*P1 for some integer T (possibly the mod representative shifted by P1)
    T, rem = divmod(u0b - u0, P1)
    assert rem == 0
    u1b = u1 + T * P0
    assert P1 * u1b - P0 * u0b == 1 and u0b >= 1 and u1b >= 1
    return u0b, u1b

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ok = True
    for b, tag in [(30, "e25"), (40, "e25"), (50, "e25")]:
        eps = 0.25
        data = json.load(open(os.path.join(here, f"redteam_checkpoint_{tag}_{b}.json")))
        zb = b / ((1 - eps) * math.log(b))
        ps = primes_upto(b)
        large = [p for p in ps if p > zb]
        caps = []
        Bb = 1
        for p in ps:
            if p <= zb:
                e, q = 0, 1
                while q * p <= b:
                    q *= p; e += 1
                caps.append((p, e)); Bb *= p ** e
        Ptot = 1
        for p in large: Ptot *= p
        def divides(u):
            t = u
            for p, cap in caps:
                c = 0
                while t % p == 0:
                    t //= p; c += 1
                    if c > cap: return False
                if t == 1: return True
            return t == 1
        f2 = f3 = 0
        best = None
        N = len(large)
        for mask in range(1 << N):
            P0 = 1
            for j in range(N):
                if mask >> j & 1: P0 *= large[j]
            P1 = Ptot // P0
            u0, u1 = minimal(P0, P1)
            mx = max(u0, u1)
            if best is None or mx < best: best = mx
            if u0 <= Bb and u1 <= Bb:
                f2 += 1
                if divides(u0) and divides(u1): f3 += 1
        exp_f2 = data["counts"]["f2_size"]; exp_f3 = data["counts"]["f3_smooth"]
        exp_best = int(data["best_directed"]["max_u"])
        match = (f2 == exp_f2 and f3 == exp_f3 and best == exp_best)
        ok &= match
        print(f"b={b}: independent F2={f2} (checkpoint {exp_f2}), F3={f3} (checkpoint {exp_f3}), "
              f"best_max_u={best} (checkpoint {exp_best}) -> {'MATCH' if match else 'MISMATCH'}")
    print("ALL MATCH" if ok else "FAILURE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
