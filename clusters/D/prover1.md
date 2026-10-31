# Cluster D, Prover 1 (CRT and smoothness route): L = 2 case

**Deliverable status: a sharpened residual, not a closure.** I do not prove
that no L = 2 disjoint solution exists above a threshold. I prove one new
constraint in full (Theorem D1, a lower bound of order `sqrt(b)` on
`log(u_0 u_1)`, with an exact prime-square divisibility statement behind it),
one elementary approximation constraint (Lemma D3, with a classical
corollary), and a self-contained proof of the flagged Theorem 13.3 step
(Proposition D0), which removes the one unaudited dependence in the forced
form. Section 6 states the residual exactly, including a proof that the
mechanism behind Theorem D1 is saturated: maximal prime-power forcing
cannot, by itself, push the lower bound past `(2 + o(1)) sqrt(b)`, while the
Theorem 14.2 upper bound is of order `b / log b`. The gap between those two
scales is the precise obstruction this route leaves open.

Setting throughout: disjoint intervals `[a,b]`, `[c,d]`, `b < c`,
`H([a,b]) + H([c,d]) in Z`, upper length `L = d - c + 1 = 2`, so `d = c + 1`.
`Lambda_b = lcm(1..b)`, `theta` is Chebyshev's function, `psi(m) = log
lcm(1..m)`, logs are natural. Fix `eps in (0,1)` and use the max form
`z_b = max(L, b/((1-eps) log b))` (Section 12 and Theorem 17.1(7) form; the
dropped max in Section 13 is vacuous for fixed `L` and large `b`, as located
in the Cluster A scan, item D1).

## 0. Inputs used, with audit status

1. **Theorem 4.2** (every upper denominator divides `Lambda_b`): true
   statement, instances verified (task brief; Cluster A scan, Section 2.2).
   Used for `c | Lambda_b`, `c + 1 | Lambda_b`, hence
   `v_p(c + i) <= floor(log_p b)` for every prime `p`.
2. **Theorem 14.1** (`den H([c,c+1]) = c(c+1)`, hence `den H([a,b]) =
   c(c+1)` and `c(c+1) | Lambda_b`): true statement, verified on instances
   to `c <= 2000` (Cluster A scan, Section 2.2; also CENSUS0.md).
3. **Theorem 14.2 forced form**: true statement with exposition-level gaps
   only, except the Theorem 13.3 step flagged in item 4. Used in the form:
   `S_0, S_1` partition `{p : z_b < p <= b}`, `c = P_0 u_0`,
   `c + 1 = P_1 u_1`, `P_1 u_1 - P_0 u_0 = 1`,
   `log P_0 = log P_1 = b/2 + o(b)`,
   `u_i <= exp((1 + o(1)) b/((1-eps) log b))`,
   `P_0 u_0 = -1 (mod P_1)`, `P_1 u_1 = 1 (mod P_0)`.
4. **Theorem 13.3 step** "all prime factors of `u_j` are at most `z_b`":
   justification missing in the note (Cluster A scan, item D3). I do not
   take this on trust; Proposition D0 below proves it, so every use of
   `z_b`-smoothness of `u_0, u_1` in this file rests on D0 plus item 1.
5. **Height bound** `a <= (1 + o(1)) b/e`, in particular `a < b/2` for all
   sufficiently large `b` (proof of Theorem 9.1; Theorem 15.1): Sections 9
   to 12 were re-derived in the Cluster A scan (Section 2.2) with no wrong
   inequality direction found; the task brief licenses Sections 9 to 12
   height bounds as audited-true with gaps flagged. The only consequence I
   use is `a < b/2` eventually.
6. **Classical theorems**, same status as the prime number theorem,
   Mertens and Sylvester-Schur inside the note: the prime number theorem
   in the form `theta(x) = (1 + o(1)) x` and `psi(m) = (1 + o(1)) m`, and
   (Corollary D3.1 only) Legendre's theorem on Diophantine approximation
   (Hardy and Wright, Theorem 184). Nothing else external is used.
7. **CENSUS0.md** (certified): no L = 2 solution for `b <= 2000`; exactly
   four intervals with `b <= 2000` have reduced denominator `c(c+1)`,
   `c > b`, all failing the numerator congruence. My Part A computation
   (Section 5) independently reproduces those four at `b <= 250`.

## 1. Proposition D0: the Theorem 13.3 step, proved

**Proposition D0.** Let `c + j` (`j in {0,1}`) divide `Lambda_b`, and write
`c + j = P_j u_j` with `P_j` the product of the primes in `(z_b, b]`
dividing `c + j`. Then for all sufficiently large `b`, every prime factor
of `u_j` is at most `z_b`.

*Proof.* Suppose a prime `q > z_b` divides `u_j`. Then `q | c + j`, so by
definition of `P_j` (once `q <= b` is known) `q in S_j` and `q | P_j`,
giving `q^2 | c + j`. First, `q <= b`: since `c + j | Lambda_b`, every
prime divisor of `c + j` is at most `b`. Second, `q^2 > b` for large `b`:
`q > z_b >= b/((1-eps) log b)`, and
`b^2 / ((1-eps)^2 (log b)^2) > b` once `b > (1-eps)^2 (log b)^2`. Hence
`v_q(Lambda_b) = floor(log_q b) = 1`, contradicting
`q^2 | c + j | Lambda_b`. So no prime factor of `u_j` exceeds `z_b`. QED.

Consequences used below, all elementary from the forced form and D0:
`u_0, u_1` are `z_b`-smooth; `gcd(u_0, u_1) = 1` (a common prime factor
would divide both `c` and `c + 1`); `gcd(u_i, P_0 P_1) = 1` (a prime
dividing `u_i` is at most `z_b`, a prime dividing `P_0 P_1` exceeds
`z_b`); for every prime `p <= z_b`, `v_p(u_i) = v_p(c + i)`, and at most
one of `v_p(u_0), v_p(u_1)` is nonzero.

## 2. Lemma D-SQ: prime-square forcing into the cofactors

The mirror mechanism of Theorem 12.1, applied to the prime power `p^2`
instead of to a prime `p`, forces the *maximal* square `p^2` (for `p` near
`sqrt(b)`) to divide one of `c, c + 1`. Since such `p` are far below
`z_b`, the square lands in `u_0 u_1`, not in `P_0 P_1`.

**Lemma D-SQ.** Let `T = T(b)` satisfy `T -> infinity` and
`T <= (log b)/4` (for instance `T = floor((log b)/4)` for large `b`). For
all sufficiently large `b`, and for every prime `p` with

```
b/T < p^2 <= b        (equivalently sqrt(b/T) < p <= sqrt(b)),
```

exactly one of `c, c + 1` is divisible by `p^2`, with exact valuation
`v_p = 2`; the other is not divisible by `p` at all. Writing `i(p)` for
the index with `p^2 | c + i(p)`, one has `v_p(u_{i(p)}) = 2`,
`v_p(u_{1-i(p)}) = 0`, and, with `S_p = {t >= 1 : t p^2 in [a,b]}` and
`w = (c + i(p))/p^2`,

```
w * ( sum_{t in S_p} t^{-1} ) = -1   (mod p),   p not dividing w.
```

*Proof.* Fix such a prime `p`, and put `q = p^2`. For large `b`:
`p^3 > b` (since `p > sqrt(b/T)` gives `p^3 > b^{3/2} / T^{3/2} >> b`),
`p > T` (since `sqrt(b/T) >> (log b)/4`), `p <= sqrt(b) < z_b`
(since `z_b >= b/((1-eps) log b) >> sqrt(b)`), and `a < b/2`
(input 5). Hence every integer in `[1, b]`, and (by input 1) each of
`c, c + 1`, has `p`-adic valuation at most `2 = floor(log_p b)`.

*Step 1: the lower `p^{-2}` layer is present and nonzero mod p.* The
lower terms with valuation exactly `-2` are `1/(t q)` for `t in S_p`.
`S_p` is nonempty: with `m = floor(b/q)`, one has `1 <= m < T` (the upper
bound from `q > b/T`), and the largest multiple `m q` exceeds `b/2`:
if `q > b/2` then `m = 1` and `m q = q > b/2`; if `q <= b/2` then
`m q > b - q >= b/2`. Since `a < b/2`, `m q in [a, b]`, so `m in S_p`,
and `S_p` is a set of integers in `[1, m]` containing `m`, with
`m < T < p`. Write `sum_{t in S_p} 1/t = U/V` in lowest terms. With the
common denominator `Lambda_m`, the unreduced numerator is a positive
integer at most `m * Lambda_m`, and reduction only shrinks it, so

```
log U <= log m + psi(m) <= log T + (1 + o(1)) T.
```

Also `V | Lambda_m`, whose prime factors are at most `m < p`, so
`p` does not divide `V`. And
`log p > (1/2)(log b - log T)`, while
`log T + (1 + o(1)) T <= (1 + o(1))(log b)/4 + log log b`; hence
`0 < U < p` for large `b`, so `p` does not divide `U` either, and the
sum `sum_{t in S_p} t^{-1}` is a nonzero element of `F_p` (read in the
local ring `Z_(p)`).

*Step 2: integrality forces an upper term of valuation `-2`.* Multiply
the total sum `H([a,b]) + H([c,c+1])` (an integer) by `q = p^2` and
reduce modulo `p` in `Z_(p)`. Every term whose denominator has
`p`-adic valuation at most `1` contributes a multiple of `p`, hence
`0 mod p`. The lower terms of valuation exactly `-2` contribute
`sum_{t in S_p} t^{-1} != 0 (mod p)` by Step 1. At most one of
`c, c + 1` is divisible by `p` (they are consecutive). If neither upper
term had valuation exactly `-2` (valuation `2` is the maximum possible,
by input 1), the total times `p^2` would be nonzero mod `p`,
contradicting integrality. Therefore exactly one of `c, c + 1` has
`v_p = 2`, the other has `v_p = 0`, and reducing the same congruence
mod `p` with the surviving upper term `1/(p^2 w)`, `p` not dividing
`w`, gives `sum_{t in S_p} t^{-1} + w^{-1} = 0 (mod p)`, the displayed
congruence.

*Step 3: the square lands in the cofactor.* Since `p < z_b`, `p` is not
a factor of `P_0` or `P_1`, so `v_p(u_i) = v_p(c + i)` for both `i`,
giving `v_p(u_{i(p)}) = 2` and `v_p(u_{1-i(p)}) = 0`. QED.

Remark. The case analysis hidden in Step 1 is exactly where the range
restriction comes from: the numerator bound needs
`psi(m) + log m < log p` with `m = floor(b/p^2)`, i.e. roughly
`b/p^2 < (1/2) log b`. For `p <= sqrt(b/T)` with any fixed or slowly
growing `T` the printed argument does not show `U != 0 (mod p)`, and
the lower layer can in principle cancel mod `p`. See Section 6.

## 3. Theorem D1: a lower bound on `log(u_0 u_1)`

**Theorem D1.** Every sufficiently large L = 2 disjoint solution
satisfies

```
prod_{p in Q_T} p^2  |  u_0 u_1,     Q_T = { primes p : b/T < p^2 <= b },
```

with the factors split disjointly between `u_0` and `u_1` (each `p^2`
divides exactly one of them, to the exact power `p^2`). Consequently

```
log(u_0 u_1) >= 2 ( theta(sqrt(b)) - theta(sqrt(b/T)) ) = (2 - o(1)) sqrt(b),
max(log u_0, log u_1) >= (1 - o(1)) sqrt(b).
```

*Proof.* The divisibility and the split are Lemma D-SQ applied to each
`p in Q_T` (distinct primes give coprime factors `p^2`). Taking logs,
`log(u_0 u_1) >= sum_{p in Q_T} 2 log p
= 2 (theta(sqrt(b)) - theta(sqrt(b/T)))`. By the prime number theorem
(input 6) and `T -> infinity`, `theta(sqrt(b)) = (1 + o(1)) sqrt(b)` and
`theta(sqrt(b/T)) = (1 + o(1)) sqrt(b/T) = o(sqrt(b))`, giving
`(2 - o(1)) sqrt(b)`. The max bound is half of the sum bound. QED.

This is to be compared with what the note previously gave in this
direction: Theorem 14.4's lower bound is
`v_i >= (1 - o(1)) (log b)/(log 2)` for the different quantity
`v_i = (c + i)/Q_i` (only top-half primes removed), a polynomial bound.
Theorem D1 gives an `exp((1 - o(1)) sqrt(b))` lower bound on
`max(u_0, u_1)` itself, and `exp((2 - o(1)) sqrt(b))` on the product.

**Proposition D2 (decomposition and ceiling for this mechanism).**
For every prime `p <= sqrt(b)`, `v_p(u_0 u_1) = v_p(c(c+1)) <=
floor(log_p b)`, and `p^{floor(log_p b)} <= b`; hence the total
contribution of all primes with `floor(log_p b) >= 2` to
`log(u_0 u_1)` is at most

```
sum_{p <= sqrt(b)} floor(log_p b) log p <= pi(sqrt(b)) log b = (2 + o(1)) sqrt(b).
```

So Theorem D1 is sharp up to the `o(1)` for the maximal-prime-power
mechanism: no argument that only forces maximal prime powers
`p^{floor(log_p b)}` (`>= p^2`) into `u_0 u_1` can improve the lower
bound beyond `(2 + o(1)) sqrt(b)`. The remaining slack in the
Theorem 14.2 upper bound
`log(u_0 u_1) <= (2 + o(1)) b/((1-eps) log b)` must therefore come from
primes `p` with `floor(log_p b) = 1`, i.e. `sqrt(b) < p <= z_b`,
dividing `c` or `c + 1` to the first power: their total possible
contribution is `theta(z_b) - theta(sqrt(b)) = (1 + o(1)) z_b`, exactly
the scale of `log B_b(z_b)`.

*Proof.* `v_p(u_0 u_1) = v_p(c) + v_p(c + 1) = v_p(c + i)` for the one
index divisible by `p` (the other contributes `0`), and
`c + i | Lambda_b` caps this at `floor(log_p b)` (input 1). The rest is
the prime number theorem. QED.

## 4. Lemma D3: the approximation constraint, elementarily

**Lemma D3.** For all sufficiently large `b`, with
`alpha = P_0 / P_1`:

```
| alpha - u_1 / u_0 | = 1 / (P_1 u_0),     | 1/alpha - u_0 / u_1 | = 1 / (P_0 u_1),
```

and `u_1 / u_0` is a strictly best approximation to `alpha` among
fractions of denominator at most `u_0`: any `x / y != u_1 / u_0` with
`1 <= y <= u_0` satisfies `|alpha - x/y| > |alpha - u_1/u_0|`.

*Proof.* The equalities are `P_1 u_1 - P_0 u_0 = 1` divided by
`P_1 u_0` (resp. `P_0 u_1`). For large `b`, `P_1 > 2 u_0`, since
`log P_1 = b/2 + o(b)` while `log u_0 = O(b / log b)`. If
`x/y != u_1/u_0` then, `gcd(u_0, u_1) = 1` (Section 1) giving a
nonzero integer numerator, `|u_1/u_0 - x/y| >= 1/(u_0 y)`. Hence
`|alpha - x/y| >= 1/(u_0 y) - 1/(P_1 u_0)
= (1/u_0)(1/y - 1/P_1)`. For `y <= u_0 < P_1 / 2` this exceeds
`1/(P_1 u_0) = |alpha - u_1/u_0|`. QED.

**Corollary D3.1 (classical).** By Legendre's theorem (input 6),
`|alpha - u_1/u_0| = 1/(P_1 u_0) < 1/(2 u_0^2)` for large `b`, and
`gcd(u_0, u_1) = 1`; hence `u_1 / u_0` is a convergent of the continued
fraction of `P_0 / P_1`, and symmetrically `u_0 / u_1` is a convergent
of `P_1 / P_0`. So the ratio of the two `z_b`-smooth cofactors is not
an arbitrary good approximation: it is a convergent of the ratio of
the two large prime products. (This corollary is the one place I cite
a classical theorem beyond the prime number theorem; Lemma D3 itself
is proved above without it.)

## 5. Computation (own code, exact arithmetic)

Code: `prover1_checks.py` in this directory; output:
`prover1_results.json`. All decisions are exact (`int`,
`fractions.Fraction`, `math.isqrt`); floating point is used only to
report logarithms of exact integers and the display quantities in
Part C, exactly as in the note's Lemma 13.2 numerics.

**Part A (census spot check, `b <= 250`).** Prefix `Fraction` harmonic
numbers; every interval's reduced denominator tested for the pronic
condition `B = c(c+1)`, `c > b`. Found: exactly the four near-misses
certified in CENSUS0.md for the full range `b <= 2000`, with identical
values, each with nonzero residue and non-integer exact sum:

| (a, b) | B | c | A | (A + 2c + 1) mod B | H([a,b]) + H([c,c+1]) |
|---|---|---|---|---|---|
| (4, 7) | 420 | 20 | 319 | 360 | 6/7 |
| (5, 7) | 210 | 14 | 107 | 136 | 68/105 |
| (9, 12) | 1980 | 44 | 763 | 852 | 71/165 |
| (154, 156) | 1,861,860 | 1364 | 36,037 | 38,766 | 71/3410 |

**Part B (forced-form measurements on the near-misses).** With
`eps = 1/2`, `Z = floor(2b / log b)` (finite-measurement threshold
only), `P_i(Z)` the product of primes in `(Z, b]` dividing `c + i`:
at `b = 156`, `c = 1364 = 2^2 * 11 * 31`, `c + 1 = 1365 = 3 * 5 * 7 *
13`, the range `(61, 156]` contains 18 primes and `c(c+1)` covers
**0** of them, so `log P_0 = log P_1 = 0` against the forced value
`b/2 = 78`. At `b = 12` the range is the single prime `11`, covered by
`c = 44`. At `b = 7` the range is empty (`Z = 7`). The near-misses thus
fail the partition condition of Theorem 14.2 by a wide margin wherever
the range is nondegenerate, in addition to failing the numerator
congruence: the denominator condition alone is far from the forced
form. (These are not solutions, so no forced conclusion is expected;
the measurement quantifies the distance.)

**Part C (the D1 bound at finite `b`).** Exact sieve counts
`K(b) = #{p : T_b p^2 > b, p^2 <= b}`, `T_b = floor((log b)/4)`, and
the theta form of the bound, `2(theta(sqrt(b)) - theta(sqrt(b/T_b)))`:

| b | T_b | K(b) exact | bound / sqrt(b) | finite-T prediction 2(1 - 1/sqrt(T_b)) | bound / upper scale |
|---|---|---|---|---|---|
| 10^4 | 2 | 6 | 0.528 | 0.586 | 1.2 x 10^-2 |
| 10^5 | 2 | 17 | 0.600 | 0.586 | 5.5 x 10^-3 |
| 10^6 | 3 | 62 | 0.825 | 0.845 | 2.8 x 10^-3 |
| 10^7 | 4 | 197 | 0.965 | 1.000 | 1.2 x 10^-3 |
| 10^8 | 4 | 560 | 0.997 | 1.000 | 4.6 x 10^-4 |
| 10^10 | 5 | 4,944 | 1.103 | 1.106 | 6.4 x 10^-5 |
| 10^12 | 6 | 44,025 | 1.182 | 1.184 | 8.2 x 10^-6 |

(Upper scale: the sum of the two Theorem 14.2 upper bounds at
`eps = 1/2`, `2b/((1-eps) log b) = 4b / log b`. At `b = 10^3`,
`T_b = 1` and the range is empty; the lemma is asymptotic.) The
measured ratio tracks the finite-`T` prediction
`2(1 - 1/sqrt(T_b))` closely and climbs toward the limiting
coefficient `2` exactly as slowly as `T_b ~ (log b)/4` dictates, while
the ratio of the new lower bound to the Theorem 14.2 upper scale
decays like `(log b)/sqrt(b)`. The key inequality of Theorem D1 is
therefore already in force, and already seen to be far from the upper
bound, at moderate `b`.

## 6. The precise residual

No contradiction is obtained. Exactly the following survives, for all
sufficiently large `b` (and no L = 2 solution exists for `b <= 2000`,
by CENSUS0.md; the extension to `b <= 20,000` is Cluster C1's, still
running at the time of writing):

1. The full Theorem 14.2 system (input 3), now with the smoothness of
   `u_0, u_1` resting on Proposition D0 rather than on the note's
   unjustified step.
2. **New:** for every prime `p` with `b/T_b < p^2 <= b`
   (`T_b = floor((log b)/4)`), `p^2` divides exactly one of
   `u_0, u_1`, to the exact power `p^2`, with the congruence of
   Lemma D-SQ; in aggregate
   `(2 - o(1)) sqrt(b) <= log(u_0 u_1) <=
   (2 + o(1)) b / ((1-eps) log b)` and
   `max(u_0, u_1) >= exp((1 - o(1)) sqrt(b))`.
3. **New:** `u_1 / u_0` is a strictly best approximation (denominator
   `<= u_0`) to `P_0 / P_1` with error exactly `1/(P_1 u_0)`, and
   (classically) a convergent of `P_0 / P_1`; symmetrically for
   `u_0 / u_1`.
4. The top-half square congruences of Theorem 14.3 and the denominator
   identity `den H([a,b]) = c(c+1)` (inputs 2, and Cluster A scan
   Section 2.2 for 14.3), unchanged.

What this route does **not** force, stated as ranges:

- Primes `p <= sqrt(b / T_b)`: Lemma D-SQ's numerator bound
  (`log U <= log m + psi(m)`, `m = floor(b/p^2)`) no longer beats
  `log p`, so the lower `p^{-2}` layer may cancel mod `p` and no
  divisibility of `u_0 u_1` by `p^2` is proved. (For individual such
  `p` the layer may or may not cancel; nothing here decides it.)
- Prime powers `p^e`, `e >= 3`: the same method forces some of them
  (the analogue of D-SQ for `p^e` near `b^{1/e}`), but their total
  possible contribution is at most `pi(b^{1/3}) log b = O(b^{1/3})
  = o(sqrt(b))`,
  and by Proposition D2 *all* maximal prime powers together are
  capped at `(2 + o(1)) sqrt(b)`, which Theorem D1 already attains.
  This mechanism is exhausted.
- First-power primes `sqrt(b) < p <= z_b` dividing `c` or `c + 1`:
  entirely unforced by anything in this file. By Proposition D2, a
  surviving solution must realise almost all of the possible
  `log(u_0 u_1)` (anything up to the `b / log b` scale) through these
  primes, each contributing a single `log p`, subject only to
  `u_i | B_b(z_b)` and the CRT conditions of Theorem 13.5.

## 7. What would close it from here

Either (a) an upper bound `log(u_0 u_1) < (2 - o(1)) sqrt(b)`, which
by Proposition D2 would have to come from controlling the first-power
primes in `(sqrt(b), z_b]` inside `c` and `c + 1` (a genuinely new
input: the mirror argument stops at `z_b` from above and at
`sqrt(b/T_b)` from below for the same numerator-size reason), or
(b) a lower bound of order `b / log b`, which would have to force a
positive proportion of those same first-power primes, or of the
primes in `(sqrt(b), z_b]`, into prescribed sides. Both directions
meet at the same unforced band `(sqrt(b), z_b]`. The convergent
condition of Corollary D3.1 converts the problem into a statement
about continued fractions of ratios of partition products, but I do
not prove that smoothness of a convergent's numerator and denominator
is impossible at this scale, and I do not claim it: S-unit and
smooth-convergent obstructions of that strength are not in the note
and are not established here.

## Files

- `prover1.md`: this file (the only output that counts).
- `prover1_checks.py`: exact computations of Section 5.
- `prover1_results.json`: machine-readable output of the checks.

Nothing was posted, emailed, or submitted anywhere.
