#!/usr/bin/env python3
"""
Cluster D Red Team (constructive) -- Erdos #288, L=2 forced-form search.

For a fixed b and a fixed eps in (0,1):
  zb   = b / ((1-eps) * log b)                     (real number)
  Lset = { primes p : zb < p <= b }                (the large primes)
  Ptot = product of Lset
  Bb   = product over primes p <= zb of p^{e_p},  e_p = max e with p^e <= b
         (= the zb-smooth part of Lambda_b; a zb-smooth u divides Lambda_b
            iff u | Bb)

A directed candidate is an ordered partition (S0,S1) of Lset,
P_i = prod(S_i), together with the minimal positive solution of
  P1*u1 - P0*u0 = 1,   u0,u1 >= 1
(the minimal positive solution is unique: u0 is the least positive
residue of -P0^{-1} mod P1, and every other positive solution adds
t*(P1,P0), t>=1, to (u0,u1)).

Filters (all decisions exact integer arithmetic):
  F1 balance : |log P0 - log P1| <= log Bb + 1
               (necessary for F2: if u0,u1 <= Bb then
                log P0 - log P1 = log(u1/u0) + log(c/(c+1)),
                so |.| <= log Bb + log((c+1)/c) < log Bb + 1 for c >= 1;
                float use is safe: for candidates here c >= max prime > 29,
                so log((c+1)/c) < 0.04 and the guard slack is > 0.96,
                dwarfing float error < 1e-11.  For N <= 20 we disable
                this prune entirely and evaluate everything.)
  F2 size    : u0 <= Bb and u1 <= Bb            (exact integer compare)
  F3 smooth  : u0 | Bb and u1 | Bb              (exact trial division
               by the primes <= zb, with exponent caps e_p)
  F4 lambda  : c*(c+1) | Lambda_b, c = P0*u0    (exact big-int mod;
               implied by F3 + the form of P_i, checked anyway)
  F5 interval: exists a in [1,b] with den H([a,b]) = c(c+1) and
               A(a,b) = -(2c+1) (mod c(c+1)), A/B = H([a,b]) reduced
               (exact fractions.Fraction test; only reached if F4 passes)

Enumeration: complement symmetry.  A subset and its complement give the
two directed candidates of one unordered pair {A, Ptot/A}.  Fixing the
largest large prime in A enumerates each unordered pair once
(2^{N-1} states, Gray-code updates of the product A).  The second
direction's Bezout solution is obtained with no second inversion:
if B*u1 - A*u0 = 1 with 1<=u0<B, 1<=u1<A, then the swapped equation
A*x - B*y = 1 has minimal positive solution x = B - u0, y = A - u1
(check: A*(B-u0) - B*(A-u1) = B*u1 - A*u0 = 1, and 1<=x<A... in range).
Degenerate pairs involving P_i = 1 are solved directly.

Checkpoint: one JSON per (b, eps-tag) is written as soon as that b is done.
"""
import argparse, json, math, os, sys, time
from fractions import Fraction


def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, v in enumerate(sieve) if v]


def max_prime_power_exp(p, b):
    e = 0
    q = 1
    while q * p <= b:
        q *= p
        e += 1
    return e


def divides_Bb(u, small_primes_with_caps):
    """Exact: does u divide Bb?  Trial division by primes <= zb.
    (Reference implementation; run_b uses the equivalent gcd test
    math.gcd(u, Bb) == u, verified against this function in
    redteam_gcd_equiv.py.)"""
    t = u
    for p, cap in small_primes_with_caps:
        if t == 1:
            return True
        cnt = 0
        while t % p == 0:
            t //= p
            cnt += 1
            if cnt > cap:
                return False
    return t == 1


def solve_direct(P0, P1):
    """Minimal positive (u0,u1) with P1*u1 - P0*u0 = 1."""
    if P1 == 1:
        return 1, 1 + P0          # u1 = 1 + P0*u0, minimise at u0 = 1
    if P0 == 1:
        return P1 - 1, 1          # P1*1 - 1*(P1-1) = 1
    u0 = (-pow(P0, -1, P1)) % P1
    u1 = (1 + P0 * u0) // P1
    return u0, u1


def interval_test(b, c):
    """F5: exact test for a partner interval [a,b].  Returns a or None."""
    target = c * (c + 1)
    need = (-(2 * c + 1)) % target
    for a in range(1, b + 1):
        h = Fraction(0, 1)
        for n in range(a, b + 1):
            h += Fraction(1, n)
        if h.denominator == target and h.numerator % target == need:
            # double verification by a second, independent summation order
            h2 = sum((Fraction(1, n) for n in range(b, a - 1, -1)), Fraction(0, 1))
            assert h2 == h
            return a
    return None


def run_b(b, eps, outdir, tag):
    t0 = time.time()
    all_primes = primes_upto(b)
    zb = b / ((1.0 - eps) * math.log(b))
    large = [p for p in all_primes if p > zb]
    small_caps = [(p, max_prime_power_exp(p, b)) for p in all_primes if p <= zb]
    Bb = 1
    for p, e in small_caps:
        Bb *= p ** e
    logBb = math.log(Bb)
    Lambda = 1
    for n in range(2, b + 1):
        Lambda = math.lcm(Lambda, n)
    N = len(large)
    Ptot = 1
    for p in large:
        Ptot *= p
    S = sum(math.log(p) for p in large)

    counts = dict(
        directed_total=0, f1_balance=0, bezout_unordered_evaluated=0,
        f2_size=0, f3_smooth=0, f4_lambda=0, f5_interval=0,
    )
    best = None            # (max_u_int, record dict) over evaluated directed
    best_balance = None
    size_survivors = []    # records (capped at 50 stored)
    final_survivors = []

    def consider(P0, P1, u0, u1, get_S0):
        nonlocal best, best_balance
        mx = u0 if u0 >= u1 else u1
        rec = None
        if best is None or mx < best[0]:
            rec = dict(max_u=str(mx), log_max_u=math.log(mx),
                       P0=str(P0), P1=str(P1), u0=str(u0), u1=str(u1),
                       c=str(P0 * u0), S0=get_S0())
            best = (mx, rec)
        # size
        if u0 <= Bb and u1 <= Bb:
            counts["f2_size"] += 1
            srec = dict(max_u=str(mx), log_max_u=math.log(mx),
                        P0=str(P0), P1=str(P1), u0=str(u0), u1=str(u1),
                        c=str(P0 * u0), S0=get_S0())
            if len(size_survivors) < 50:
                size_survivors.append(srec)
            if math.gcd(u0, Bb) == u0 and math.gcd(u1, Bb) == u1:
                counts["f3_smooth"] += 1
                c = P0 * u0
                if Lambda % (c * (c + 1)) == 0:
                    counts["f4_lambda"] += 1
                    a = interval_test(b, c)
                    if a is not None:
                        counts["f5_interval"] += 1
                        final_survivors.append(dict(b=b, a=a, c=str(c), S0=get_S0()))
                    else:
                        final_survivors.append(dict(b=b, a=None, c=str(c), S0=get_S0(),
                                                    note="passed F4, failed F5 for every a"))
        return rec

    if N == 0:
        result = dict(b=b, eps=eps, zb=zb, N=0, note="no large primes")
        _save(result, outdir, tag)
        return result

    p_star = large[-1]
    free = large[:-1]
    logs_free = [math.log(p) for p in free]
    log_star = math.log(p_star)
    prune = N > 20
    thresh = logBb + 1.0

    A = p_star
    lsum = log_star
    in_A = [False] * len(free)   # current Gray state membership for free primes
    states = 1 << (N - 1)
    counts["directed_total"] = 2 * states
    def get_S0_A():
        return [free[j] for j in range(len(free)) if in_A[j]] + [p_star]
    def get_S0_B():
        sA = set(free[j] for j in range(len(free)) if in_A[j]) | {p_star}
        return [p for p in large if p not in sA]
    prev_g = 0
    for i in range(states):
        if i:
            g = i ^ (i >> 1)
            diff = g ^ prev_g
            prev_g = g
            bit = diff.bit_length() - 1
            if (g >> bit) & 1:
                A *= free[bit]
                lsum += logs_free[bit]
                in_A[bit] = True
            else:
                A //= free[bit]
                lsum -= logs_free[bit]
                in_A[bit] = False
        B = Ptot // A
        diff_log = abs(2.0 * lsum - S)
        if prune and diff_log > thresh:
            continue
        counts["f1_balance"] += 2
        counts["bezout_unordered_evaluated"] += 1
        if A == 1 or B == 1:
            u0, u1 = solve_direct(A, B)
            consider(A, B, u0, u1, get_S0_A)
            u0s, u1s = solve_direct(B, A)
            consider(B, A, u0s, u1s, get_S0_B)
        else:
            u0, u1 = solve_direct(A, B)
            consider(A, B, u0, u1, get_S0_A)
            # swapped direction, no new inversion
            u0s, u1s = A - u1, B - u0
            # verify the swapped identity cheaply in exact integers:
            assert A * u1s - B * u0s == 1, "swapped Bezout identity failed"
            consider(B, A, u0s, u1s, get_S0_B)

    elapsed = time.time() - t0
    best_rec = best[1] if best else None
    min_is_global = True
    if prune and best_rec is not None:
        # every non-evaluated directed candidate fails F1, hence has
        # max(u0,u1) > Bb (by the F1 derivation); if the best evaluated
        # max is <= Bb the reported minimum is the global minimum.
        min_is_global = best[0] <= Bb
    result = dict(
        b=b, eps=eps, zb=zb, N=N, large_primes=large,
        log_Ptot=S, half_log_Ptot=S / 2.0, log_Bb=logBb, Bb=str(Bb),
        counts=counts, states_unordered=states,
        prune_used=prune, balance_threshold_log=thresh if prune else None,
        best_directed=best_rec, min_is_global=min_is_global,
        size_survivors_stored=size_survivors,
        final_survivors=final_survivors,
        elapsed_sec=elapsed,
    )
    _save(result, outdir, tag)
    print(f"b={b} eps={eps} N={N} states={states} eval={counts['bezout_unordered_evaluated']} "
          f"F1={counts['f1_balance']} F2={counts['f2_size']} F3={counts['f3_smooth']} "
          f"F4={counts['f4_lambda']} F5={counts['f5_interval']} "
          f"best_log_max_u={best_rec['log_max_u'] if best_rec else None} "
          f"logBb={logBb:.2f} elapsed={elapsed:.1f}s", flush=True)
    return result


def _save(result, outdir, tag):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"redteam_checkpoint_{tag}_{result['b']}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bs", required=True, help="comma-separated b values")
    ap.add_argument("--eps", type=float, required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    for b in [int(x) for x in args.bs.split(",") if x]:
        path = os.path.join(args.outdir, f"redteam_checkpoint_{args.tag}_{b}.json")
        if os.path.exists(path):
            print(f"b={b} tag={args.tag}: checkpoint exists, skipping", flush=True)
            continue
        run_b(b, args.eps, args.outdir, args.tag)


if __name__ == "__main__":
    main()
