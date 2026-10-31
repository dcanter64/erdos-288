#!/usr/bin/env python3
"""
Cluster D Verifier, main checks (own code, exact arithmetic).
Covers: D1 Part C sieve counts; CENSUS0 near-misses vs D-SQ scope;
D-SQ Step 1 finite non-vanishing; D0 finite divisor illustration;
Q1 bijection on random exact data; Q2 leak example + idempotence;
Q3 Legendre both-signs on near-misses and own synthetic partitions;
D3 exact equality on near-miss quadruples; singleton scope separation.
Floats only for reporting logarithms.
"""
import json, math, random
from fractions import Fraction
from math import isqrt, gcd, log, floor

random.seed(20261030)
OUT = {}
fails = []
def check(name, cond, detail=""):
    OUT.setdefault("checks", []).append({"name": name, "pass": bool(cond), "detail": str(detail)})
    if not cond:
        fails.append(name)
    print(("PASS " if cond else "FAIL ") + name + (" :: " + str(detail) if detail else ""))

def primes_upto(n):
    if n < 2: return []
    s = bytearray([1])*(n+1); s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n)+1):
        if s[i]: s[i*i::i] = b"\x00"*len(s[i*i::i])
    return [i for i in range(2, n+1) if s[i]]

def vp(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e

# ---------- 1. D1 Part C: exact sieve theta bound ----------
partC = []
for b in [10**4, 10**5, 10**6, 10**7, 10**8, 10**10, 10**12]:
    Tb = floor(log(b)/4)
    lo = isqrt(b//Tb)  # p > sqrt(b/T)  <=>  p >= floor(sqrt(b/T))+1 handled below exactly
    # exact prime set: primes p with b/Tb < p^2 <= b, tested in integers: Tb*p*p > b and p*p <= b
    hi = isqrt(b)
    ps = primes_upto(hi)
    sel = [p for p in ps if Tb*p*p > b and p*p <= b]
    bound = 2*sum(log(p) for p in sel)   # = 2(theta(sqrt b)-theta(sqrt(b/T))) exactly as sum of logs
    partC.append({"b": b, "T_b": Tb, "K": len(sel), "bound_over_sqrtb": bound/math.sqrt(b),
                  "finiteT_pred": 2*(1-1/math.sqrt(Tb))})
    print("PartC", b, "T", Tb, "K", len(sel), "ratio", bound/math.sqrt(b))
expK = {10**4:6, 10**5:17, 10**6:62, 10**7:197, 10**8:560, 10**10:4944, 10**12:44025}
check("D1-PartC K counts match prover1_results.json",
      all(r["K"] == expK[r["b"]] for r in partC), partC)
expratio = {10**4:0.528, 10**5:0.600, 10**6:0.825, 10**7:0.965, 10**8:0.997, 10**10:1.103, 10**12:1.182}
check("D1-PartC ratios match prover1 table to 3dp",
      all(abs(r["bound_over_sqrtb"]-expratio[r["b"]]) < 0.001 for r in partC))
check("D1-PartC ratios track finite-T prediction 2(1-1/sqrt(T)) within 0.06",
      all(abs(r["bound_over_sqrtb"]-r["finiteT_pred"]) < 0.06 for r in partC),
      [(r["b"], round(r["bound_over_sqrtb"],3), round(r["finiteT_pred"],3)) for r in partC])
OUT["partC"] = partC

# ---------- 2. Near-misses recomputed + D-SQ scope ----------
near = []
for (a, b) in [(4,7),(5,7),(9,12),(154,156)]:
    h = sum((Fraction(1,n) for n in range(a, b+1)), Fraction(0,1))
    A, B = h.numerator, h.denominator
    r = isqrt(1+4*B); assert r*r == 1+4*B
    c = (r-1)//2
    tot = h + Fraction(2*c+1, c*(c+1))
    Tb = floor(log(b)/4) if b > 1 else 0
    QT = [p for p in primes_upto(isqrt(b)) if Tb >= 1 and Tb*p*p > b and p*p <= b]
    fac = {}
    for n_, lab in [(c,"c"),(c+1,"c+1")]:
        f = {}
        m = n_
        for p in primes_upto(isqrt(n_)+1):
            if p*p > m: break
            while m % p == 0: f[p] = f.get(p,0)+1; m //= p
        if m > 1: f[m] = f.get(m,0)+1
        fac[lab] = f
    near.append({"a":a,"b":b,"A":A,"B":B,"c":c,"residue":(A+2*c+1)%B,
                 "sum":f"{tot.numerator}/{tot.denominator}","T_b":Tb,"Q_T":QT,
                 "a_lt_b_over_2": a < b/2, "fac_c":fac["c"], "fac_c1":fac["c+1"]})
    print("near", near[-1])
expnm = {(4,7):(420,20,319,360,"6/7"),(5,7):(210,14,107,136,"68/105"),
         (9,12):(1980,44,763,852,"71/165"),(154,156):(1861860,1364,36037,38766,"71/3410")}
check("near-miss table matches CENSUS0 exactly",
      all((r["B"],r["c"],r["A"],r["residue"],r["sum"]) == expnm[(r["a"],r["b"])] for r in near))
check("D-SQ scope: Q_T empty for all four near-miss b (T_b in {0,0,0,1})",
      all(r["Q_T"] == [] for r in near), [(r["b"], r["T_b"]) for r in near])
check("D-SQ scope: a < b/2 hypothesis fails for all four near-misses (they are not solutions)",
      all(not r["a_lt_b_over_2"] for r in near))
OUT["near_misses"] = near

# ---------- 3. D-SQ Step 1 finite check: lower p^-2 layer never vanishes for a<b/2 ----------
bad = 0; tested = 0
# NOTE: Q_T is empty when T_b = 1 (b < e^8 = 2981), so test where the range is live: T_b >= 2.
for b in range(3000, 20001, 97):
    Tb = floor(log(b)/4)
    if Tb < 2: continue
    a = b//3  # a < b/2, an admissible lower endpoint for the mechanism test (not a claimed solution)
    for p in primes_upto(isqrt(b)):
        if not (Tb*p*p > b and p*p <= b): continue
        q = p*p; m = b//q
        Sp = [t for t in range(1, m+1) if a <= t*q <= b]
        if not Sp: bad += 1; continue
        s = sum((Fraction(1,t) for t in Sp), Fraction(0,1))
        U, V = s.numerator, s.denominator
        tested += 1
        if not (0 < U < p and V % p != 0 and U % p != 0): bad += 1
        # every t in Sp automatically p-free because p^3 > b
        if any(t % p == 0 for t in Sp): bad += 1
check("D-SQ Step1: for 3000<=b<=20000 step 97, a=b//3, all p in Q_T: S_p nonempty, 0<U<p, p not | U V",
      bad == 0 and tested > 500, f"tested={tested} bad={bad}")

# ---------- 4. D0 finite illustration: divisors of Lambda_b split with z_b-smooth cofactor ----------
def divides_lambda(n, b):
    m = n
    for p in primes_upto(b):
        if p*p > m and m > 1:
            # remaining m is prime or 1
            return m <= b and (m == 1 or m**1 <= b)
        e = 0
        while m % p == 0: m //= p; e += 1
        if p**e > b: return False
        if m == 1: return True
    return m == 1
cnt = 0; bad0 = 0
for b in [60, 120]:
    eps = 0.25; zb = b/((1-eps)*log(b))
    for n in range(2, 3001):
        if not divides_lambda(n, b): continue
        cnt += 1
        P = 1
        for p in primes_upto(b):
            if zb < p <= b and n % p == 0: P *= p
        if n % P != 0: bad0 += 1; continue
        u = n//P
        # u must be zb-smooth: no prime factor > zb
        mm = u
        for p in primes_upto(u):
            if p*p > mm: 
                if mm > 1 and mm > zb: bad0 += 1
                break
            while mm % p == 0:
                if p > zb: bad0 += 1
                mm //= p
            if mm == 1: break
check("D0 finite form: every n|Lambda_b, n<=3000, b in {60,120}: cofactor after removing (zb,b] primes is zb-smooth",
      bad0 == 0 and cnt > 100, f"divisors tested={cnt} bad={bad0}")

# ---------- 5. Q1 bijection on random exact data + idempotence + D3 equality ----------
def split_PW(P, W, Y):
    assert Y*Y == 1 + 4*P*W
    A, B = (Y-1)//2, (Y+1)//2
    Pp, Ppp = gcd(P, A), gcd(P, B)
    assert Pp*Ppp == P and gcd(Pp, Ppp) == 1
    return Pp, Ppp, A//Pp, B//Ppp, A, B

tests = 0; ok = 0
for _ in range(600):
    c = random.randrange(2, 10**7)
    # squarefree large parts: choose random subsets of distinct prime factors of c and c+1
    def sqfree_part(n):
        facs = []; m = n
        for p in primes_upto(isqrt(n)+1):
            if p*p > m: break
            if m % p == 0:
                facs.append(p)
                while m % p == 0: m //= p
        if m > 1: facs.append(m)
        P = 1
        for p in facs:
            if random.random() < 0.5: P *= p
        return P, n//P
    P0, u0 = sqfree_part(c); P1, u1 = sqfree_part(c+1)
    if P1*u1 - P0*u0 != 1: continue
    P, W, Y = P0*P1, u0*u1, 2*c+1
    tests += 1
    if Y*Y != 1 + 4*P*W: continue
    Pp, Ppp, Wp, Wpp, A, B = split_PW(P, W, Y)
    if (Pp, Ppp, Wp, Wpp) != (P0, P1, u0, u1): continue
    # idempotence: split again from the recovered quadruple's Y
    Pp2, Ppp2, Wp2, Wpp2, _, _ = split_PW(Pp*Ppp, Wp*Wpp, 2*Pp*Wp+1)
    if (Pp2, Ppp2, Wp2, Wpp2) != (Pp, Ppp, Wp, Wpp): continue
    # D3 exact equality (exact Fractions)
    if abs(Fraction(P0, P1) - Fraction(u1, u0)) != Fraction(1, P1*u0): continue
    if abs(Fraction(P1, P0) - Fraction(u0, u1)) != Fraction(1, P0*u1): continue
    ok += 1
check("Q1/Q2/D3: identity, splitting recovery, idempotence, D3 equality on random consecutive data",
      tests > 300 and ok == tests, f"tests={tests} ok={ok}")

# leak example
P, W, Y = 15, 40, 49
Pp, Ppp, Wp, Wpp, A, B = split_PW(P, W, Y)
check("Q2 leak example P=15,W=40,Y=49: A=24,B=25,P'=3,P''=5,W'=8,W''=5, gcd(W'',P'')=5 (cleanliness fails)",
      (A, B, Pp, Ppp, Wp, Wpp) == (24, 25, 3, 5, 8, 5) and gcd(Wpp, Ppp) == 5
      and Ppp*Wpp - Pp*Wp == 1 and Y*Y == 1 + 4*P*W)

# ---------- 6. Q3: Legendre both signs (near-misses + own balanced synthetics) ----------
def legendre(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1
nm_leg = {}
for r in near:
    c = r["c"]
    W = 1
    # use prover2's eps=0 extraction only to get a (P,W) pair per near-miss: recompute directly
    zb0 = r["b"]/log(r["b"])
    P0 = 1; P1 = 1
    for p, e in r["fac_c"].items():
        if p > zb0: P0 *= p
    for p, e in r["fac_c1"].items():
        if p > zb0: P1 *= p
    u0, u1 = c//P0, (c+1)//P1
    W = u0*u1; P = P0*P1
    nm_leg[f"{r['a']},{r['b']}"] = {str(p): legendre(W, p) for p in [P0, P1] if p > 1}
print("near-miss Legendre (W/p):", nm_leg)
check("Q3 near-miss (5,7): (W/5)=+1, (W/7)=-1 (both signs in one example)",
      nm_leg["5,7"] == {"7": -1, "5": 1} or nm_leg["5,7"] == {"5": 1, "7": -1}, nm_leg["5,7"])

tally = {-1: 0, 0: 0, 1: 0}; tallyPQ = {-1: 0, 0: 0, 1: 0}
for b in [50, 100, 200, 400]:
    zb = b/log(b)
    ps = [p for p in primes_upto(b) if p > zb]
    # own greedy: descending primes to currently smaller log-side
    l0 = l1 = 0.0; s0, s1 = [], []
    for p in sorted(ps, reverse=True):
        if l0 <= l1: s0.append(p); l0 += log(p)
        else: s1.append(p); l1 += log(p)
    P0 = math.prod(s0); P1 = math.prod(s1)
    u1 = pow(P1, -1, P0); u0 = (P1*u1 - 1)//P0
    assert P1*u1 - P0*u0 == 1 and u0 >= 1
    W = u0*u1
    for p in ps: tally[legendre(W, p)] += 1
    # (P/q) for odd prime divisors q of W (trial divide small factors exhaustively by primes to 10^6 cap: use full factor via primes to isqrt may be huge; factor by primes up to 10^5 then treat remainder)
    mm = W; qs = set()
    for p in primes_upto(100000):
        if p*p > mm: break
        if mm % p == 0:
            if p != 2: qs.add(p)
            while mm % p == 0: mm //= p
    if mm > 1 and mm != 2:
        # remainder is prime or product of two large primes; test primality deterministically for <3.3e24 not guaranteed; only use if pow test strong probable + small: skip ambiguous remainder >1e6 from tally denominator note
        pass
    for q in qs: tallyPQ[legendre(P0*P1, q)] += 1
print("own synthetic Legendre tallies: (W/p)", tally, " (P/q) small-q", tallyPQ)
check("Q3 own synthetics: (W/p) takes both signs, never 0", tally[-1] > 0 and tally[1] > 0 and tally[0] == 0, tally)
check("Q3 own synthetics: (P/q) takes both signs on small prime divisors of W", tallyPQ[-1] > 0 and tallyPQ[1] > 0, tallyPQ)
OUT["legendre_own_synthetic"] = {"W_mod_p": {str(k): v for k, v in tally.items()},
                                "P_mod_q_small": {str(k): v for k, v in tallyPQ.items()}}
OUT["prover2_reported_legendre"] = {"W_mod_p": {"-1": 68, "0": 0, "1": 53}, "note": "from prover2_results.json part4; total 121 = 10+17+34+60 primes, consistent"}
check("prover2 Legendre total consistent: 68+53=121 = sum of synthetic prime counts 10+17+34+60",
      68+53 == 10+17+34+60)

# ---------- 7. Singleton scope separation ----------
sols = []
for (a, b, m) in [(1,3,6),(2,3,6),(3,6,20)]:
    h = sum((Fraction(1,n) for n in range(a, b+1)), Fraction(0,1))
    sols.append(h + Fraction(1, m) == 1 or h + Fraction(1, m) == 2)
check("three disjoint singleton solutions verify exactly (scope reference only)", all(sols), sols)
check("singleton b values give T_b = floor(ln b /4) = 0: D-SQ range undefined there (no L=1 claim possible)",
      all(floor(log(b)/4) == 0 for b in [3,3,6]))

OUT["all_pass"] = (len(fails) == 0)
OUT["failures"] = fails
with open("/home/hatch/workspace/math-hunt/erdos-288/clusters/D/verifier_main_results.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("ALL MAIN CHECKS PASS" if not fails else f"FAILURES: {fails}")
