#!/usr/bin/env python3
"""
Cluster D Verifier, red-team checks (own code, exact arithmetic).
- Own direct enumeration (bitmask over ALL directed subsets, own extended
  Euclid, trial-division F3 -- no Gray code, no complement shortcut,
  no F1 prune) at b=30,40,50, eps=1/4; compare F2/F3/best with checkpoints.
- b=30 F5 candidate verified exactly (all a, Fraction sums both orders).
- Aggregation of all checkpoints vs redteam.md totals.
- Smoothness defect recomputation at b=100 (full directed enumeration,
  own code) and comparison with redteam_defect_100_0.25.json.
- MITM spot verification: N by own trial-division prime counting for
  (250,1/4),(300,1/4) plus all rows; F1 counts by own MITM
  (itertools.combinations half + iterative-doubling half, bisect)
  for (200,1/4) and (250,1/2).
Floats only for F1/defect logarithms (as in the producers' auxiliary counts).
"""
import json, math, bisect, itertools, os
from fractions import Fraction
from math import isqrt, gcd, log

D = "/home/hatch/workspace/math-hunt/erdos-288/clusters/D"
OUT = {}; fails = []
def check(name, cond, detail=""):
    OUT.setdefault("checks", []).append({"name": name, "pass": bool(cond), "detail": str(detail)})
    if not cond: fails.append(name)
    print(("PASS " if cond else "FAIL ") + name + (" :: " + str(detail) if detail else ""), flush=True)

def primes_sieve(n):
    if n < 2: return []
    s = bytearray([1])*(n+1); s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n)+1):
        if s[i]: s[i*i::i] = b"\x00"*len(s[i*i::i])
    return [i for i in range(2, n+1) if s[i]]

def primes_trial(n):
    out = []
    for x in range(2, n+1):
        r = isqrt(x); ok = True
        for d in range(2, r+1):
            if x % d == 0: ok = False; break
        if ok: out.append(x)
    return out

def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a//b)*y1)

def solve_min(P0, P1):
    # minimal positive (u0,u1), P1*u1 - P0*u0 = 1, via own extended Euclid
    if P1 == 1: return (1, 1 + P0)
    if P0 == 1: return (P1 - 1, 1)
    g, x, y = egcd(P1, P0)   # x*P1 + y*P0 = 1 -> u1 = x mod P0, u0 = -y mod P1... use residues:
    u1 = x % P0
    if u1 == 0: u1 = P0
    u0 = (P1*u1 - 1)//P0
    assert P1*u1 - P0*u0 == 1 and u0 >= 1 and u1 >= 1
    return (u0, u1)

def build(b, eps):
    ps = primes_sieve(b)
    zb = b/((1-eps)*log(b))
    large = [p for p in ps if p > zb]
    caps = []
    Bb = 1
    for p in ps:
        if p <= zb:
            e = 0; q = 1
            while q*p <= b: q *= p; e += 1
            caps.append((p, e)); Bb *= p**e
    return zb, large, caps, Bb

def divides_Bb_trial(u, caps):
    t = u
    for p, cap in caps:
        if t == 1: return True
        cnt = 0
        while t % p == 0:
            t //= p; cnt += 1
            if cnt > cap: return False
    return t == 1

# ---------- own enumeration b=30,40,50 ----------
enum_res = {}
for b in [30, 40, 50]:
    eps = 0.25
    zb, large, caps, Bb = build(b, eps)
    N = len(large); Ptot = math.prod(large)
    f2 = f3 = 0; best = None
    for mask in range(1 << N):   # mask = S0 membership; every directed partition once
        P0 = 1
        for i, p in enumerate(large):
            if mask >> i & 1: P0 *= p
        P1 = Ptot//P0
        u0, u1 = solve_min(P0, P1)
        mx = max(u0, u1)
        if best is None or mx < best: best = mx
        if u0 <= Bb and u1 <= Bb:
            f2 += 1
            if divides_Bb_trial(u0, caps) and divides_Bb_trial(u1, caps): f3 += 1
    enum_res[b] = {"N": N, "directed": 1 << N, "F2": f2, "F3": f3, "best_max_u": best}
    print("enum", b, enum_res[b], flush=True)
exp_enum = {30: (5, 32, 30, 1), 40: (6, 64, 62, 0), 50: (8, 256, 239, 0)}
check("R1 own enumeration b=30,40,50: (N,directed,F2,F3) match checkpoints",
      all((enum_res[b]["N"], enum_res[b]["directed"], enum_res[b]["F2"], enum_res[b]["F3"]) == exp_enum[b] for b in exp_enum),
      enum_res)
check("R1 own enumeration best max(u): b=30 -> 44 (u1 of the F3 survivor)",
      enum_res[30]["best_max_u"] == 44, enum_res[30]["best_max_u"])
OUT["own_enum"] = enum_res

# ---------- b=30 candidate exact ----------
P0, P1, u0, u1 = 6409, 437, 3, 44
c = P0*u0
zb, large, caps, Bb = build(30, 0.25)
Lam = 1
for n in range(2, 31): Lam = math.lcm(Lam, n)
cand_ok = (P1*u1 - P0*u0 == 1 and c + 1 == P1*u1 and large == [13,17,19,23,29]
           and math.prod([13,17,29]) == P0 and math.prod([19,23]) == P1
           and divides_Bb_trial(u0, caps) and divides_Bb_trial(u1, caps)
           and Lam % (c*(c+1)) == 0)
check("R1 b=30 candidate: Bezout, c=19227, F3 (trial division), F4 (Lambda_30 mod) all exact", cand_ok,
      f"c={c} c(c+1)={c*(c+1)}")
f5_hits = []
for a in range(1, 31):
    h = sum((Fraction(1,n) for n in range(a, 31)), Fraction(0,1))
    h2 = sum((Fraction(1,n) for n in range(30, a-1, -1)), Fraction(0,1))
    assert h == h2
    tot = h + Fraction(2*c+1, c*(c+1))
    if tot.denominator == 1: f5_hits.append(a)
    if h.denominator == c*(c+1) and (h.numerator + 2*c + 1) % (c*(c+1)) == 0: f5_hits.append(("res", a))
check("R1 b=30 candidate fails F5 for every a in [1,30] (exact sums, both orders)", f5_hits == [], f5_hits)
OUT["b30"] = {"P0": P0, "P1": P1, "u0": u0, "u1": u1, "c": c}

# ---------- aggregation of checkpoints ----------
tot = {"directed": 0, "f1": 0, "f2": 0, "f3": 0, "f4": 0, "f5": 0}
rows = 0; min_global_all = True
import glob
for fn in sorted(glob.glob(os.path.join(D, "redteam_checkpoint_*.json"))):
    with open(fn) as f: ck = json.load(f)
    cn = ck["counts"]
    tot["directed"] += cn["directed_total"]; tot["f1"] += cn["f1_balance"]
    tot["f2"] += cn["f2_size"]; tot["f3"] += cn["f3_smooth"]
    tot["f4"] += cn["f4_lambda"]; tot["f5"] += cn["f5_interval"]
    rows += 1
    if not ck.get("min_is_global", False): min_global_all = False
print("aggregated", rows, tot)
check("R1 totals over 17 checkpoint files: 165,522,272 directed / 163,555,002 F1 / 64,899,301 F2 / F3=1 / F4=1 / F5=0",
      tot == {"directed": 165522272, "f1": 163555002, "f2": 64899301, "f3": 1, "f4": 1, "f5": 0}, tot)
check("R1 every checkpoint records min_is_global = true", min_global_all and rows == 17, f"rows={rows}")
OUT["totals"] = tot

# ---------- defect recomputation at b=100 ----------
b = 100; eps = 0.25
zb, large, caps, Bb = build(b, eps)
N = len(large); Ptot = math.prod(large)
capd = dict(caps)
def rough_log(u):
    r = u
    for p, cap in caps:
        cnt = 0
        while r % p == 0 and cnt < cap:
            r //= p; cnt += 1
    return r
f2 = 0; dmin = None; buckets = {1: 0, 2: 0, 5: 0, 10: 0}
for mask in range(1 << N):
    P0 = 1
    for i, p in enumerate(large):
        if mask >> i & 1: P0 *= p
    P1 = Ptot//P0
    u0, u1 = solve_min(P0, P1)
    if u0 <= Bb and u1 <= Bb:
        f2 += 1
        Dv = max(log(rough_log(u0)), log(rough_log(u1))) if max(rough_log(u0), rough_log(u1)) > 1 else 0.0
        if dmin is None or Dv < dmin: dmin = Dv
        for t in buckets:
            if Dv <= t: buckets[t] += 1
print("defect b=100: F2", f2, "Dmin", dmin, "buckets", buckets, flush=True)
check("R1 defect b=100: F2=533, D_min=20.42 (2dp), zero survivors with D<=10",
      f2 == 533 and abs(dmin - 20.424659307988424) < 0.005 and all(v == 0 for v in buckets.values()),
      {"f2": f2, "dmin": dmin, "buckets": buckets})
OUT["defect100"] = {"f2": f2, "dmin": dmin, "buckets": buckets}

# ---------- MITM spot verification ----------
def mitm_count(b, eps):
    ps = primes_trial(b)
    zb = b/((1-eps)*log(b))
    large = [p for p in ps if p > zb]
    logBb = 0.0
    for p in ps:
        if p <= zb:
            e = 0; q = 1
            while q*p <= b: q *= p; e += 1
            logBb += e*log(p)
    logs = [log(p) for p in large]
    S = sum(logs); N = len(large); tau = (logBb + 1)/2; target = S/2
    n1 = N//2
    A = [sum(cb) for r in range(n1+1) for cb in itertools.combinations(logs[:n1], r)]
    # second half by iterative doubling (different generation path from producers' verify script)
    B = [0.0]
    for x in logs[n1:]: B = B + [v + x for v in B]
    B.sort()
    cnt = 0
    for a_ in A:
        cnt += bisect.bisect_right(B, target + tau - a_) - bisect.bisect_left(B, target - tau - a_)
    return {"b": b, "eps": eps, "zb": zb, "N": N, "directed_total": 2**N, "f1_directed": cnt,
            "pi_b": len(ps)}
mitm = {}
for (bb, ee) in [(250, 0.25), (300, 0.25), (200, 0.25), (250, 0.5), (300, 0.5), (400, 0.5)]:
    # N only (prime counting) for all rows; full count below for two rows
    ps = primes_trial(bb)
    zb = bb/((1-ee)*log(bb))
    N = sum(1 for p in ps if p > zb)
    mitm[f"{bb},{ee}"] = {"N": N, "pi_b": len(ps), "pi_floor_zb": sum(1 for p in ps if p <= zb)}
    print("MITM N", bb, ee, mitm[f"{bb},{ee}"], flush=True)
expN = {"250,0.25": 36, "300,0.25": 43, "200,0.25": 31, "250,0.5": 29, "300,0.5": 35, "400,0.5": 46}
check("R2 MITM N by own trial-division primes matches corrected table for all six rows",
      all(mitm[k]["N"] == expN[k] for k in expN), mitm)
check("R2 pi differences as printed: pi(250)-pi(60)=53-17=36; pi(300)-pi(70)=62-19=43",
      mitm["250,0.25"]["pi_b"] == 53 and mitm["250,0.25"]["pi_floor_zb"] == 17
      and mitm["300,0.25"]["pi_b"] == 62 and mitm["300,0.25"]["pi_floor_zb"] == 19)
for (bb, ee, expf1) in [(200, 0.25, 2089250414), (250, 0.5, 536807982)]:
    r = mitm_count(bb, ee)
    mitm[f"full {bb},{ee}"] = r
    print("MITM full", r, flush=True)
    check(f"R2 MITM F1 count own implementation ({bb},{ee}) = {expf1}",
          r["f1_directed"] == expf1 and r["directed_total"] == 2**r["N"], r)
OUT["mitm"] = mitm

OUT["all_pass"] = (len(fails) == 0); OUT["failures"] = fails
with open(os.path.join(D, "verifier_redteam_results.json"), "w") as f:
    json.dump(OUT, f, indent=1)
print("ALL REDTEAM CHECKS PASS" if not fails else f"FAILURES: {fails}")
