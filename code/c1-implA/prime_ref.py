"""prime_ref.py -- pure-Python prime-by-prime reference for Erdős #288 (C0, Impl 2).

This is the slow, transparent implementation of exactly the same prime-wise
mathematics that prime_kernel.c accelerates.  It never forms the global
fraction H(a,b) (except inside the explicitly-flagged tiny spot-check helper
at the bottom, used only in self-tests on intervals with b <= 60).

Per prime p and interval [a, b]:
  V = max v_p(n) over n in [a, b]
  S = sum_n p^(V - v_p(n)) * (n')^{-1}   (mod p^(V+1)),   n = p^(v_p(n)) * n'
  t = v_p(S) if S != 0 else infinity
  e = V - t if t < V else 0                      (denominator exponent of p)
  u = (S / p^t) mod p^e                          (unit part: p^e * H = u in Z_(p))

Global assembly (exact Python big integers, from the per-prime data only):
  B        = prod p^e
  A mod p^e = u * ((B / p^e) mod p^e) mod p^e
  A mod B  is assembled from those residues by CRT.
"""

from math import isqrt


def sieve_primes(n):
    bs = bytearray(b"\x01") * (n + 1)
    bs[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if bs[i]:
            bs[i * i::i] = b"\x00" * len(bs[i * i::i])
    return [i for i in range(2, n + 1) if bs[i]]


def vp_factor(n, p):
    """Return (v_p(n), n with all factors p removed)."""
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, n


def prime_data(a, b, primes=None):
    """Per-prime data for H(a, b): dict p -> (e_p, u_p), only e_p > 0 kept,
    plus the full dict including zeros if keep_all.  Pure prime-wise."""
    if primes is None:
        primes = sieve_primes(b)
    out = {}
    for p in primes:
        if p > b:
            break
        terms = []
        V = 0
        for n in range(a, b + 1):
            v, np_ = vp_factor(n, p)
            terms.append((v, np_))
            if v > V:
                V = v
        mod = p ** (V + 1)
        S = 0
        for v, np_ in terms:
            w = pow(np_, -1, p ** (v + 1))
            S = (S + p ** (V - v) * w) % mod
        e, u = 0, 0
        if S != 0:
            t, tmp = 0, S
            while tmp % p == 0:
                tmp //= p
                t += 1
            if t < V:
                e = V - t
                u = tmp % p ** e
        out[p] = (e, u)
    return out


def assemble_B(data):
    """B = prod p^e_p from per-prime data {p: (e, u)}."""
    B = 1
    for p, (e, _u) in data.items():
        if e:
            B *= p ** e
    return B


def a_residues(data, B=None):
    """A mod p^e for every active prime, from u_p and B (CRT components)."""
    if B is None:
        B = assemble_B(data)
    res = {}
    for p, (e, u) in data.items():
        if e:
            q = p ** e
            res[p] = (u * ((B // q) % q)) % q
    return res, B


def crt_A(data, B=None):
    """Assemble A mod B from the prime-power residues via CRT.
    Returns (A_mod_B, B).  For B == 1 returns (0, 1)."""
    res, B = a_residues(data, B)
    x, M = 0, 1
    for p, r in res.items():
        q = p ** data[p][0]
        if q == 1:
            continue
        t = ((r - x) % q) * pow(M % q, -1, q) % q
        x += M * t
        M *= q
        x %= M
    return x, B


def check_singleton(data):
    """Exact singleton decision from per-prime data.
    Returns (is_solution, B, A_mod_B, local_ok) where local_ok is the
    conjunction of the prime-power conditions A = -1 (mod p^e)."""
    res, B = a_residues(data)
    local_ok = True
    for p, r in res.items():
        q = p ** data[p][0]
        if r != q - 1:
            local_ok = False
            break
    A_mod_B, _ = crt_A(data, B)
    # CRT form of the same statement (both are reported; must agree):
    crt_ok = (B == 1) or (A_mod_B == B - 1)
    assert local_ok == crt_ok
    return local_ok, B, A_mod_B, local_ok


def check_l2(a, b, data):
    """Exact L=2 disjoint decision for the pair [a,b], [c,c+1], b < c.

    Reduction (proved in RESULTS.md): with H(a,b) = A/B in lowest terms and
    H(c,c+1) = (2c+1)/(c(c+1)) in lowest terms, the sum is an integer iff
    B = c(c+1) AND A + 2c + 1 = 0 (mod B).  Hence c is forced by B through
    the integer square root; no search over c is involved or needed.
    Returns a dict of the exact intermediate facts."""
    res, B = a_residues(data)
    A_mod_B, _ = crt_A(data, B)
    c = isqrt(B)
    pronic = (c * (c + 1) == B)
    out = {
        "B": B,
        "A_mod_B": A_mod_B,
        "pronic": pronic,
        "c": c if pronic else None,
        "c_gt_b": bool(pronic and c > b),
        "congruence": False,
        "is_solution": False,
    }
    if pronic and c > b:
        cong_local = True
        for p, r in res.items():
            q = p ** data[p][0]
            if r != (-(2 * c + 1)) % q:
                cong_local = False
                break
        cong_crt = (A_mod_B + 2 * c + 1) % B == 0
        assert cong_local == cong_crt
        out["congruence"] = cong_crt
        out["is_solution"] = cong_crt
    return out


# ---------------------------------------------------------------------------
# Tiny spot-check helper ONLY (self-tests, intervals with b <= 60).
# This is the one place a global Fraction is formed, as permitted for small
# internal spot checks; it is never used in the census pipeline.
# ---------------------------------------------------------------------------
def fraction_spot_check(a, b):
    from fractions import Fraction
    h = Fraction(0, 1)
    for n in range(a, b + 1):
        h += Fraction(1, n)
    return h.numerator, h.denominator
