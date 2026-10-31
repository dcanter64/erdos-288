# CLUSTER-D.md — Cluster D, Cycle 1: Verifier record for the L = 2 case

**Role and protocol.** This file is the Cluster D record, written by the
Cluster D Verifier. The verifier formed a check plan from the claim
statements, verified the proofs line by line against the source text
(`sources/Nayak-2026.txt`, Sections 12–14, 17, 18, and Theorem 4.2), and
recomputed every finite claim with its own code in exact arithmetic
(Python `int`, `fractions.Fraction`, `math.isqrt`; floating point only
for reporting logarithms and for the two explicitly float-based
auxiliary counts, F1 balances and MITM subset sums, exactly as in the
producers' own auxiliary computations). Verifier code:
`clusters/D/verifier_main.py`, `clusters/D/verifier_redteam.py`,
`clusters/D/verifier_prune140.py`; machine-readable output:
`clusters/D/verifier_main_results.json`,
`clusters/D/verifier_redteam_results.json`,
`clusters/D/verifier_prune140_results.json`. All verifier checks passed;
the individual results are cited per claim below. No producer file was
patched; defects are logged in Section 5.

**Setting (common to all claims).** Disjoint intervals `[a,b]`, `[c,c+1]`,
`b < c`, `H([a,b]) + H([c,c+1]) ∈ ℤ`, upper length `L = 2`.
`Λ_b = lcm(1..b)`, `θ` Chebyshev's function, `ψ(m) = log lcm(1..m)`,
`ε ∈ (0,1)` fixed, `z_b = max(L, b/((1-ε) log b))` in the max form
(Section 12 / Theorem 17.1(7)); the dropped max in Section 13 (item
A-W1 of `AUDIT-A.md`) is immaterial everywhere below, because every
argument uses only `z_b ≥ b/((1-ε) log b)`, which both forms satisfy,
and the two forms coincide for all sufficiently large `b` at fixed `L`.
Theorem 14.2's forced form is taken in the form stated by both provers:
`S_0 ⊔ S_1` partitions `{p : z_b < p ≤ b}`, `c = P_0 u_0`,
`c+1 = P_1 u_1`, `P_1 u_1 - P_0 u_0 = 1`,
`log P_0 = log P_1 = b/2 + o(b)`,
`u_i ≤ exp((1+o(1)) b/((1-ε) log b))`.

---

## 1. Per-claim verdicts

### D0 (Theorem 13.3 gap fill; Prover 1, Proposition D0; independently recorded by Prover 2, §0) — CERTIFIED

Claim: if a prime `q > z_b` divided `u_j`, a contradiction follows;
hence every prime factor of `u_j` is at most `z_b`.

The exact chain, verified step by step:

1. Assume `q` prime, `q > z_b`, `q | u_j` (`j ∈ {0,1}`). By definition
   `c + j = P_j u_j`, where `P_j = ∏_{p ∈ S_j} p` and
   `S_j = {p : z_b < p ≤ b, p | c+j}`; in particular `q | c+j`.
2. `c + j | Λ_b`: this is Theorem 4.2 of the note applied to the upper
   denominator `n = c+j ∈ [c, d]` (Theorem 4.2 states `n | Λ_b` for
   every `c ≤ n ≤ d`; audited true, instances verified, per the
   Cluster A scan). Hence every prime divisor of `c+j` is at most `b`,
   so `q ≤ b`. This step must come first, and in Prover 1's proof it
   does: membership `q ∈ S_j` is only available once `q ≤ b` is known.
3. Now `z_b < q ≤ b` and `q | c+j`, so `q ∈ S_j` by the definition of
   `S_j`, hence `q | P_j`, with `v_q(P_j) = 1` (`P_j` is a product of
   distinct primes).
4. `v_q(c+j) ≥ 2` follows because `q` divides **both** factors of the
   product decomposition: `v_q(c+j) = v_q(P_j) + v_q(u_j) ≥ 1 + 1 = 2`.
   Hence `q² | c+j`. This is the step the task flagged, and it is
   exactly right: the first power comes from `P_j`, the second from
   the assumed `q | u_j`.
5. `q² > b` for all sufficiently large `b`: `q > z_b ≥ b/((1-ε) log b)`,
   so `q² > b²/((1-ε)² (log b)²)`, and the right side exceeds `b` under
   the explicit sufficient condition `b > (1-ε)² (log b)²`, which holds
   eventually for every fixed `ε ∈ (0,1)`.
6. `v_q(Λ_b) = max{e : q^e ≤ b} = 1`, since `q ≤ b < q²` by steps 2
   and 5.
7. But `q² | c+j | Λ_b` (steps 4 and 2) forces `v_q(Λ_b) ≥ 2`,
   contradicting step 6. ∎

Consequences drawn by Prover 1 are also correct: `u_0, u_1` are
`z_b`-smooth; `gcd(u_0, u_1) = 1`; `gcd(u_i, P_0 P_1) = 1`; for
`p ≤ z_b`, `v_p(u_i) = v_p(c+i)`, and at most one of `v_p(u_0)`,
`v_p(u_1)` is nonzero (consecutiveness). Prover 2's §0 version is the
same argument in compressed form ("`q > z_b ≫ √b`"); it is certified
by the same chain. Finite illustration by the verifier: for `b ∈
{60, 120}` (`ε = 1/4`), every `n | Λ_b` with `n ≤ 3000` (2,591
divisors) splits as `n = P·u` with `P` the product of its prime
factors in `(z_b, b]` and `u` indeed `z_b`-smooth, zero exceptions
(`verifier_main.py`, check "D0 finite form").

**Status of the Theorem 13.3 gap after D0: CLOSED.** The step flagged
as red-team item D3 in the Cluster A scan and as item A-W2 in
`AUDIT-A.md` ("all prime factors of `u_j` are at most `z_b`",
asserted in the note from `u_j | Λ_b` alone, which does not suffice)
is now supplied with a complete proof using only Theorem 4.2, the
definition of `S_j`/`P_j`, and the size of `z_b`. Every use of
`z_b`-smoothness of `u_0, u_1` in Theorems 13.3, 13.5, 14.2 and in
both Cluster D prover files therefore rests on a proved step. The
only remaining dependence is Theorem 4.2 itself, at its audited
status. The `z_b` inconsistency A-W1 does not touch the fill (see
the setting note above).

### D-SQ (prime-square forcing; Prover 1, Lemma D-SQ) — CERTIFIED WITH QUALIFICATIONS

Claim: for `T = T(b)` with `T → ∞`, `T ≤ (log b)/4`, and every prime
`p` with `b/T < p² ≤ b`, exactly one of `c, c+1` has `v_p = 2`, the
other has `v_p = 0`; writing `i(p)` for the divisible side,
`v_p(u_{i(p)}) = 2`, `v_p(u_{1-i(p)}) = 0`, and with
`S_p = {t ≥ 1 : t p² ∈ [a,b]}`, `w = (c+i(p))/p²`:
`w · (∑_{t ∈ S_p} t⁻¹) ≡ -1 (mod p)`, `p ∤ w`.

Line-by-line verification:

*Preliminaries.* For large `b`: `p³ > b` (from `p > √(b/T)`,
`p³ > b^{3/2}/T^{3/2} > b` iff `b > T³`, and `T ≤ (log b)/4` gives
`T³ ≪ b`); `p ≤ √b < z_b` (`z_b/√b ≥ √b/((1-ε) log b) → ∞`);
`a < b/2` eventually (audited height bound `a ≤ (1+o(1)) b/e`,
`1/e < 1/2`); hence `v_p ≤ floor(log_p b) = 2` for every integer in
`[1,b]` and, via `c+j | Λ_b` (Theorem 4.2), for `c, c+1`. The maximal
prime power is `Q = p² ≤ b < p³`, so this is the Theorem 5.1 mirror
mechanism at `Q = p²` (`Q > L = 2` is automatic since `p² > b/T`),
re-derived directly rather than cited, which is legitimate.

*Step 1 (lower layer nonzero mod p).* With `q = p²`, `m = floor(b/q)`:
`1 ≤ m < T` (`q ≤ b` gives `m ≥ 1`; `q > b/T` gives `b/q < T`).
The largest multiple `mq > b/2` (if `q > b/2`, `m = 1` and `mq = q`;
else `mq > b - q ≥ b/2`), and `a < b/2 < mq ≤ b` puts `m ∈ S_p`, so
`S_p ⊆ [1, m]` is nonempty. Every `t ∈ S_p` satisfies `p ∤ t`
(otherwise `p³ | t p² ≤ b`, against `p³ > b`). Writing
`∑_{t ∈ S_p} 1/t = U/V` in lowest terms: with common denominator
`Λ_m`, the unreduced numerator is a positive integer at most
`m·Λ_m` (each `Λ_m/t` is an integer, there are at most `m` terms),
and reduction only shrinks it, so `log U ≤ log m + ψ(m)`. Also
`V | Λ_m`, whose prime factors are at most `m < p`, so `p ∤ V`.
The comparison `log U < log p` is the range-restricting step and it
is correct exactly where claimed: `log p > ½(log b - log T)`, while
`log U ≤ log T + (1+o(1)) T ≤ (1+o(1))(log b)/4 + log log b`, and
`¼ log b` is eventually beaten by `½ log b - ½ log T` with margin
`~¼ log b`. Hence `0 < U < p`, `p ∤ U`, and the layer sum is a
nonzero element of `F_p`. For `p ≤ √(b/T)` (equivalently `m ≥ T`)
this bound no longer beats `log p`, and the proof correctly claims
nothing there: the restriction `b/T < p²` is exactly the hypothesis
`log m + ψ(m) < log p` in disguise (`m ≈ b/p² ≲ ½ log b` needed;
`T ≤ (log b)/4` supplies it with a factor-2 margin).

*Step 2 (integrality forces the upper `p⁻²` layer).* Multiply the
integer total by `p²` and reduce mod `p` in `ℤ_(p)`. Terms of
valuation `≥ -1` contribute `0 mod p`; the lower terms of valuation
exactly `-2` contribute `∑_{t ∈ S_p} t⁻¹ ≠ 0 (mod p)` by Step 1.
At most one of `c, c+1` is divisible by `p` (consecutive integers).
If neither had `v_p = 2` (the maximum possible), the total times
`p²` would be nonzero mod `p`, contradicting integrality. Hence
exactly one has `v_p = 2`, the other `v_p = 0`, and reducing the
same congruence with the surviving term `1/(p² w)`, `p ∤ w`, gives
`∑ t⁻¹ + w⁻¹ ≡ 0`, i.e. the displayed congruence after multiplying
by `w`. Correct.

*Step 3 (the square lands in the cofactor).* `p < z_b` implies
`p ∤ P_0 P_1`, so `v_p(u_i) = v_p(c+i)` for both `i`. Correct.

Qualifications (exposition compressions in Prover 1's Step 1, both
filled here, neither affecting validity): (i) the printed bound
`log m + ψ(m) ≤ log T + (1+o(1)) T` compresses the monotonicity step
`ψ(m) ≤ ψ(⌈T⌉) = (1+o(1)) T` (valid since `m < T` and `ψ` is
nondecreasing); (ii) "`p > T` (since `√(b/T) ≫ (log b)/4`)" is
shorthand for the uniform check `√(b/T) > T ⟺ b > T³`, which holds
for all admissible `T` since `T ≤ (log b)/4`.

Finite support (verifier's own): the lemma is asymptotic and no
large solution exists to test it on, so the verifier tested its
engine, Step 1, directly: for `b` from 3000 to 20000 (step 97;
`Q_T` is empty for `T_b = 1`, i.e. `b < e^8`), with the admissible
endpoint `a = ⌊b/3⌋ < b/2`, for every `p ∈ Q_T` (1,129 pairs):
`S_p` nonempty, `0 < U < p`, `p ∤ U V`, and no `t ∈ S_p` divisible
by `p`. Zero failures.

Scope separation from CENSUS0, as instructed. The four near-misses
`(a,b) = (4,7), (5,7), (9,12), (154,156)` (recomputed exactly by the
verifier; `B, c, A`, residues `360, 136, 852, 38766` and sums
`6/7, 68/105, 71/165, 71/3410` all match CENSUS0) are **not**
instances of D-SQ and do not test it: they are not solutions (the
total is a non-integer), the height hypothesis fails for all four
(`a < b/2` is false in each: `4 > 7/2`, `5 > 7/2`, `9 > 6`,
`154 > 78`), and with `T_b = floor((log b)/4)` the range is empty
for all four (`T_b = 0, 0, 0, 1`; for `T_b = 1` the conditions
`p² > b` and `p² ≤ b` are incompatible). So `Q_T = ∅` and D-SQ
makes no prediction about their factorisations
(`c = 2²·5`, `2·7`, `2²·11`, `2²·11·31`; the few prime squares
present, `2²` and `3²`, sit in the unforced region). No conflict
and no confirmation arises, in either direction. Likewise, D-SQ is
stated only for the `L = 2` upper interval `[c, c+1]`; Prover 1
makes **no** claim about any `L = 1` analogue for the three known
disjoint singleton solutions `(1,3,6), (2,3,6), (3,6,20)` (verified
exactly by the verifier as solutions, for reference only), whose
`b ∈ {3, 6}` in any case give `T_b = 0`, where the range is
undefined. The scopes are disjoint and are kept disjoint in the
residual of Section 3.

### D1 (lower bound on `log(u_0 u_1)`; Prover 1, Theorem D1) — CERTIFIED WITH QUALIFICATIONS

Claim: `∏_{p ∈ Q_T} p² | u_0 u_1` with each `p²` dividing exactly
one factor to the exact power `p²` (`Q_T = {p : b/T_b < p² ≤ b}`,
`T_b = floor((log b)/4)`); hence
`log(u_0 u_1) ≥ 2(θ(√b) - θ(√(b/T_b))) = (2 - o(1))√b` and
`max(u_0, u_1) ≥ exp((1 - o(1))√b)`.

Verification. The divisibility and disjoint split are D-SQ applied
prime by prime (distinct primes give coprime factors `p²`); taking
logs gives the `θ`-difference exactly, since
`{p : b/T < p² ≤ b} = {p : √(b/T) < p ≤ √b}`. The asymptotics are
the prime number theorem in the form `θ(x) = (1+o(1)) x`:
`θ(√b) = (1+o(1))√b` and `θ(√(b/T)) = (1+o(1))√(b/T) = o(√b)`
because `T → ∞`; the difference is `(1 - o(1))√b`, doubled as
claimed. The max bound is half the product bound. The theorem
itself is certified without reservation.

Numerical verification (verifier's own sieve, exact prime
enumeration; bound computed as `2·∑_{p ∈ Q_T} log p`): for
`b = 10^4, 10^5, 10^6, 10^7, 10^8, 10^10, 10^12`, the exact counts
`K(b) = |Q_T|` are `6, 17, 62, 197, 560, 4944, 44025`, matching
Prover 1's Part C data (`prover1_results.json`) exactly, and
`bound/√b` is `0.528, 0.600, 0.825, 0.965, 0.997, 1.103, 1.182`,
matching Prover 1's table to three decimals and tracking the
finite-`T` prediction `2(1 - 1/√T_b)` = `0.586, 0.586, 0.845,
1.000, 1.000, 1.106, 1.184` within `0.06` throughout, climbing
toward the limiting coefficient `2` exactly as slowly as
`T_b ~ (log b)/4` dictates. At `b = 10^3`, `T_b = 1` and the range
is empty, as Prover 1 notes; the statement is asymptotic.

Qualification (the comparison framing, adjudicated as instructed).
Prover 1 writes that Theorem 14.4 is what "the note previously gave
in this direction". Read as a bound on the **same quantity**, that
framing is **not accurate**, and Prover 1's own sentence contains
the disclosure that prevents it from misleading: Theorem 14.4
bounds a **different and larger** quantity,
`v_i = (c+i)/Q_i`, where only the top-half primes (`b/2 < p ≤ b`)
are removed, whereas `u_i = (c+i)/P_i` removes all primes in
`(z_b, b]`. Since `Q_i | P_i`, one has `v_i = u_i · (P_i/Q_i) ≥ u_i`,
so a lower bound on `v_i` implies no lower bound on `u_i` at all;
Theorem 14.4 is also conditional on `T_i ≠ ∅`. Before D1, the note
gave no lower bound on `max(u_0, u_1)` or on `u_0 u_1` beyond the
trivial `≥ 1`. D1 is therefore certified as the first lower bound
on `u_0 u_1` itself in this system, **not** as an improvement of
Theorem 14.4 on its own quantity. (Minor wording point, logged as
defect P1-a in Section 5: Prover 1 calls Theorem 14.4's bound
`v_i ≥ (1-o(1)) (log b)/(log 2)` "a polynomial bound"; the bound is
of order `log b` in `v_i` itself, which is sub-polynomial. The
comparison's substance, an `exp(Θ(√b))` bound against an
`O(log b)` bound on a larger quantity, is unaffected.)

### D2 (ceiling / saturation; Prover 1, Proposition D2) — CERTIFIED

Claim: all maximal prime powers together contribute at most
`π(√b) log b = (2 + o(1))√b` to `log(u_0 u_1)`, so the prime-square
mechanism is saturated and the residual slack must come from
first-power primes in `(√b, z_b]`.

Verification. For `p ≤ z_b`, `v_p(u_0 u_1) = v_p(c) + v_p(c+1) =
v_p(c+i)` for the one divisible index, and `c+i | Λ_b` caps this at
`floor(log_p b)`. For `p ≤ √b` (exactly the primes with
`floor(log_p b) ≥ 2`), each contribution is
`floor(log_p b)·log p = log(p^{floor(log_p b)}) ≤ log b`, and there
are `π(√b)` such primes, giving the stated sum bound;
`π(√b) ~ √b / log √b = 2√b / log b` (prime number theorem) yields
`(2 + o(1))√b`. Since D1 attains `(2 - o(1))√b`, no argument that
only forces maximal prime powers `p^{floor(log_p b)}` into
`u_0 u_1` can improve the lower bound beyond `(2 + o(1))√b`: the
mechanism is saturated, as claimed. The residual-slack conclusion
follows by splitting `log(u_0 u_1) = ∑_{p ≤ z_b} v_p log p` at
`√b`: primes above `√b` and at most `z_b` have `v_p ≤ 1`
(`p² > b`), so anything in `log(u_0 u_1)` beyond the
`(2 + o(1))√b` maximal-power ceiling, up to the Theorem 14.2 upper
scale `(2 + o(1)) b/((1-ε) log b)`, must come from first-power
primes in `(√b, z_b]`. Certified.

### D3 (approximation constraint; Prover 1, Lemma D3 and Corollary D3.1) — CERTIFIED

Claim: `|P_0/P_1 - u_1/u_0| = 1/(P_1 u_0)` (and symmetrically
`|P_1/P_0 - u_0/u_1| = 1/(P_0 u_1)`), and `u_1/u_0` is a convergent
of `P_0/P_1`.

Verification. The equalities are `P_1 u_1 - P_0 u_0 = 1` divided by
`P_1 u_0` (resp. `P_0 u_1`): `P_0/P_1 - u_1/u_0 =
(P_0 u_0 - P_1 u_1)/(P_1 u_0) = -1/(P_1 u_0)`. The verifier also
checked both equalities in exact `Fraction` arithmetic on 600
random exact quadruples satisfying the Bezout equation (Section 2).
The elementary Lemma D3 (strictly best approximation among
denominators `≤ u_0`) is proved correctly: distinct fractions
differ by `≥ 1/(u_0 y)` (nonzero integer numerator, using
`gcd(u_0, u_1) = 1`), the triangle inequality gives
`|α - x/y| ≥ (1/u_0)(1/y - 1/P_1)`, and `y ≤ u_0 < P_1/2`
(available for large `b` since `log P_1 = b/2 + o(b)` against
`log u_0 = O(b/log b)`) makes this exceed `1/(P_1 u_0)`.
The corollary applies Legendre's theorem (Hardy and Wright,
Theorem 184, a cited classical result at the same status as the
prime number theorem in this campaign): `1/(P_1 u_0) < 1/(2 u_0²)`
for large `b` (equivalent to `2 u_0 < P_1`), with
`gcd(u_0, u_1) = 1`, so `u_1/u_0` is a convergent of `P_0/P_1`,
and symmetrically `u_0/u_1` of `P_1/P_0`. Certified, with the
corollary's dependence on the cited classical theorem recorded
exactly as Prover 1 records it.

### Q1 (discriminant identity is an equivalence; Prover 2, Propositions 1.1–1.2) — CERTIFIED WITH QUALIFICATIONS

Claim: `Y = 2c + 1` tautologically, and `Y² = 1 + 4PW` is in
explicit bijection with `P_1 u_1 - P_0 u_0 = 1`.

Algebra, both directions, verified. Forward: given
`P_1 u_1 - P_0 u_0 = 1`, set `c = P_0 u_0`, so `P_1 u_1 = c + 1`,
`P = P_0 P_1`, `W = u_0 u_1`, `PW = c(c+1)`, and
`Y := 2u_0 P_0 + 1 = 2c + 1 = 2P_1 u_1 - 1` satisfies
`Y² = (2c+1)² = 4c(c+1) + 1 = 1 + 4PW`. The square root is not an
unknown: it is `2c + 1` by construction, which is the sense in
which the discriminant computation compresses nothing. Reverse
(the splitting of Prover 2, §2): given `Y² = 1 + 4PW`, `Y` odd
positive, `P` squarefree with odd prime factors, set
`A = (Y-1)/2`, `B = (Y+1)/2`; then `AB = (Y²-1)/4 = PW`,
`B - A = 1`, `gcd(A, B) = 1`; each `p | P` satisfies
`Y² ≡ 1 (mod p)`, `p ∤ Y`, and `p` (odd) divides exactly one of
`A, B`; hence `P' = gcd(P, A)`, `P'' = gcd(P, B)` give
`P = P'P''`, `gcd(P', P'') = 1`, and with `W' = A/P'`,
`W'' = B/P''` (integers, since `P' | A`, `P'' | B`):
`W'W'' = W` and `P''W'' - P'W' = B - A = 1`, an equation of exactly
the original shape. The two maps are mutually inverse: splitting
after the forward map returns the original quadruple (each prime
of `P_0` divides `A = c` and not `B = c+1`, and conversely), and
the forward map after splitting returns `Y' = 2P'W' + 1 = 2A + 1 =
Y`. Verifier computation: 600 random exact consecutive pairs with
random squarefree large parts (including cases where `u_i` shares a
prime with `P_i`): identity, exact recovery of the quadruple by the
gcd splitting, and idempotence all held in 600 of 600 cases.

Qualifications. (i) The bijection is certified under the standing
hypotheses in force in Prover 2's §2 (`P` squarefree, all prime
factors odd, in the application `> z_b ≥ 2`; `Y` odd positive);
the oddness is what makes each `p | P` divide exactly one of
`A, B`. (ii) The "splitting datum" of Proposition 1.2 is not an
independent choice: the sign at `p` is forced to be `Y mod p` and
the `W`-split is induced by `A, B`. The bijection is between the
quadruple system and the triple system **with its induced split**,
which is exactly the equivalence Prover 2's argument uses.
(iii) Recovery of a quadruple **of the forced type** (in particular
`gcd(W', P'P'') = 1`) needs the extra hypothesis `p ∤ W` for
`p | P`; without it items 1–4 of the split still hold but
cleanliness can fail (see Q2's leak example). Prover 2 flags this
dependence itself (§2.2); in a genuine solution the hypothesis
holds by D0. None of the qualifications touches the conclusion:
the identity carries exactly the information of consecutiveness,
no more.

### Q2 (splitting is idempotent, not a descent; Prover 2, §2) — CERTIFIED

Verification. Idempotence: the split's own associated square root
is `2P'W' + 1 = 2A + 1 = Y`, so a second splitting performs the
same gcd computations and returns `(P', P'', W', W'')` verbatim;
also verified computationally in the 600 random cases of Q1 and on
all four near-misses in Prover 2's §5.1 data. All size measures are
unchanged by construction: `log P' + log P'' = log P`,
`log W' + log W'' = log W` exactly, and the output equation has the
same shape and scale as the input. The size window is correct:
`A(A+1) = PW` gives `log A = ½(log P + log W) + o(1) =
b/2 + O(b/log b)` from `log P = b + o(b)` and
`0 ≤ log W = O(b/log b)` alone, and `log P' = log A - log W'` with
`0 ≤ log W' ≤ log W` confines both `log P', log P''` to
`b/2 ± O(b/log b)`. Hence the killed sub-cases (`P' = 1`, `P'' = 1`,
and any split with `|log P' - b/2| = ω(b/log b)`) die by the size
hypotheses alone: no arithmetic property of the identity beyond
the size of `PW` enters the window argument, and Theorem 13.3
already gives the same balance directly. Every balanced split and
every coprime split `W = W'W''` (including `W' = 1`, `W'' = 1`)
survives. A bijection between a system and itself cannot power a
descent; certified.

The smoothness leak example and its role, verified exactly by the
verifier: `P = 15`, `W = 40`, `Y = 49`: `49² = 2401 = 1 + 4·15·40`;
`A = 24`, `B = 25`; `P' = gcd(15, 24) = 3`, `P'' = gcd(15, 25) = 5`,
`W' = 8`, `W'' = 5`; the split equation `5·5 - 3·8 = 1` holds, but
`gcd(W'', P'') = 5 ≠ 1`: the prime `5 | P` has leaked into the
matching `W`-part. Its role is exactly the one Prover 2 assigns
it: it isolates the single place the route uses smoothness
(cleanliness of the split, item 5 of §2.1), shows that cleanliness
is equivalent to the extra input `p ∤ W` for `p | P`, and shows
that even with cleanliness granted, no contradiction results.

### Q3 (no modulo or reciprocity contradiction at this level; Prover 2, §3) — CERTIFIED WITH QUALIFICATIONS

Certified statement, scoped exactly: **no contradiction of the
forms Prover 2 examined in its §3.1–§3.6 exists.** The forms are:
mod `p | P` and its lift to mod `p²` (§3.1); mod `q | W` and its
prime powers (§3.2); parity, mod 4 and mod 8 (§3.3); Legendre
symbols `(W/p)` for `p | P`, `(P/q)` for `q | W`, and any sign
forced by quadratic reciprocity from them (§3.4); counting of
CRT sign patterns (§3.5); and quadratic-form / norm / genus
arguments on `Y² = 1 + 4PW` (§3.6). This is not certified as a
universal impossibility for arguments outside those forms.

Verification. §3.1: mod `p | P` the identity is `Y² ≡ 1`, in which
`W` does not appear, so no condition on `W mod p` can result; the
mod-`p²` lift determines a cofactor residue (the mirror congruence
shape of Theorem 13.5) rather than restricting it. §3.2:
symmetrically `Y² ≡ 1 (mod q)`, refining the prime-power split,
with both signs realised by construction of `Y = 2c+1` on the two
sides. §3.3: `P` odd and `Y` odd give `PW = (Y²-1)/4` even, hence
`2 | W`, and nothing more; both `Y mod 4` residues occur in the
data. §3.5: for squarefree odd `P`, `Y² ≡ 1 (mod P)` has exactly
`2^{π(b) - π(z_b)}` CRT classes, one per sign pattern, with no
preference among them. §3.6: the factorisation `(Y-1)(Y+1) = 4PW`
over `ℤ` is §2 itself, and the form's discriminant is the unknown
`PW`, so no fixed-discriminant class-group input exists. §3.4
(signs are genuinely free, the one empirical component): the
verifier recomputed the Legendre data with its own code. On the
near-miss `(a,b) = (5,7)` alone, `(W/5) = +1` and `(W/7) = -1`,
both signs in a single example. On the verifier's own balanced
synthetic partitions for `b ∈ {50, 100, 200, 400}` (greedy
log-weight partition of the primes in `(z_b, b]`, Bézout
representatives, full partition and balance), `(W/p)` over
`p | P` took the values `-1` 68 times and `+1` 53 times, never `0`,
reproducing Prover 2's reported tally (`68 / 53`, total `121 =
10 + 17 + 34 + 60`) exactly; `(P/q)` took both signs already on
the small prime divisors of `W` (verifier subset tally `-1` 4
times, `+1` 7 times; Prover 2's full tally is `7 / 8`). A
reciprocity contradiction requires a forced sign; there is none.
Certified at the stated scope.

### R1 (red team constructive search) — CERTIFIED WITH QUALIFICATIONS

Claims: coverage and totals (165,522,272 directed candidates;
163,555,002 through F1; 64,899,301 through F2; exactly one through
F3, at `b = 30`, which passed F4 and failed F5); the obstruction
map (F1 obstructs almost nothing, F2 never kills the best
candidates, F3 is total for `b ≥ 40`); the defect margins
`D_min = 20.4, 25.9, 33.2` at `b = 100, 120, 150`.

Verifier reproduction, in layers.

(a) *Own spot implementation (independent code path).* The
verifier enumerated **all** directed partitions directly (bitmask
over all `2^N` subsets, own extended-Euclid Bezout solver, F3 by
trial division with exponent caps, no Gray code, no complement
symmetry, no F1 prune) at `b = 30, 40, 50`, `ε = 1/4`. Results:
`(N, directed, F2, F3) = (5, 32, 30, 1)`, `(6, 64, 62, 0)`,
`(8, 256, 239, 0)`, matching the checkpoints exactly in all twelve
numbers; best `max(u)` values `44, 394, 4007`, matching both the
checkpoints and the red team's own independent
`redteam_verify_small.py`. At `b = 100` the verifier re-ran the
full directed enumeration (65,536 candidates) computing the
smoothness defect of every F2 survivor: `F2 = 533`,
`D_min = 20.424659307988424` (the producers' `20.42`), and zero
survivors with `D ≤ 1, 2, 5, 10`, matching
`redteam_defect_100_0.25.json` exactly.

(b) *The F1 prune at a pruned row.* The producers disabled the
float F1 prune for `N ≤ 20` and used it for `N ≥ 21` (first at
`b = 140`, `N = 22`). The verifier re-enumerated `b = 140`,
`ε = 1/4`, with **no prune at all** (4,194,304 directed candidates,
one exact Bezout solve per unordered state, second direction by
the swapped identity asserted in integers at every state):
`F2 = 8847`, `F3 = 0`, and best `max(u) = 2389115168466718`, all
three matching `redteam_checkpoint_e25_140.json` exactly
(`verifier_prune140.py`, 95 s). The prune therefore removed no F2
survivor at the first and smallest pruned row.

(c) *Aggregation.* Summing the 17 on-disk checkpoint files gives
exactly the claimed totals: directed `165,522,272`, F1
`163,555,002`, F2 `64,899,301`, F3 `1`, F4 `1`, F5 `0`; every
checkpoint records `min_is_global = true`, so the tabulated minima
of `log max(u_0, u_1)` (consistently below `log B_b`, margins
`-5.65` to `-13.37` in the `ε = 1/4` rows) are global, as claimed.

(d) *The `b = 30` candidate, verified exactly by the verifier.*
`S_0 = {13,17,29}`, `P_0 = 6409`; `S_1 = {19,23}`, `P_1 = 437`;
`u_0 = 3`, `u_1 = 44`; `437·44 - 6409·3 = 19228 - 19227 = 1`;
`c = 19227`, `c+1 = 19228`; `u_0 | B_30` and
`u_1 = 2²·11 | B_30` by trial division against the caps
(`2^4, 3^3, 5^2, 7, 11`); `c(c+1) = 369,696,756 | Λ_30` by exact
mod. F5 failure: for every `a ∈ [1,30]` the verifier computed
`H([a,30])` exactly (two summation orders, asserted equal) and
`H([a,30]) + H([19227,19228])`; no `a` gives an integer, and no
`a` satisfies the denominator-plus-residue condition. The
candidate is not an `L = 2` solution for any `a`, exactly as
claimed. It is the unique F3 survivor of the whole run.

(e) *Defect margins at `b = 120, 150`.* Accepted from the
producers' `redteam_defect_120_0.25.json` and
`redteam_defect_150_0.25.json` (`F2` recomputed there as `465`
and `763`, matching their checkpoints; `D_min = 25.912…` and
`33.218…`), with the `b = 100` row of the same pipeline
independently reproduced by the verifier in (a).

Qualifications. (i) The instantiation scope is exactly as the red
team states: two fixed `ε` values (`1/4` for `b = 30..175`,
`1/2` for `b = 200, 225`), exact finite analogues of the
asymptotic forced form; **no claim is certified for `b > 225`, for
`(200, 1/4)` or `(225, 1/4)`, or for other `ε`.** The obstruction
map is a finite computational statement, not a proof for large
`b`. (ii) Rows `b ∈ {150, 160, 175}` (`ε = 1/4`) and
`b ∈ {200, 225}` (`ε = 1/2`) were not independently re-enumerated
by the verifier; they are certified on the strength of checkpoint
aggregation (c), the producers' internal independent checks
(independent re-derivation at `b ≤ 50`, gcd-vs-trial-division F3
equivalence on 25,416 values with 0 mismatches, a no-shared-code
census sanity check recovering exactly the four CENSUS0
near-misses), and the verifier's no-prune reproduction at the
first pruned row (b). (iii) A justification defect in the F1
guard-band wording is logged as RT-a in Section 5; it does not
affect any count, per (b).

### R2 (red team Section 8 correction, MITM table) — CERTIFIED

Claim: the first version of the auxiliary meet-in-the-middle table
was wrong in five of six rows (faulty large-prime list); the
corrected table was recomputed by `redteam_mitm_counts.py` and
independently reproduced by `redteam_mitm_verify.py`, agreeing
exactly on all six rows; corrected values include `N = 36` at
`(250, 1/4)` and `N = 43` at `(300, 1/4)`.

Verifier spot-verification, own code. Prime counting by trial
division (a third prime-generation path, distinct from both
producers' sieves): for all six rows, `N = π(b) - π(⌊z_b⌋)` is
`31` at `(200, 1/4)`, `29` at `(250, 1/2)`, `36` at `(250, 1/4)`,
`35` at `(300, 1/2)`, `43` at `(300, 1/4)`, `46` at `(400, 1/2)`,
matching the corrected table in all six rows. The two differences
printed in the correction log check out exactly:
`π(250) - π(60) = 53 - 17 = 36` (`z_b = 60.37…`) and
`π(300) - π(70) = 62 - 19 = 43` (`z_b = 70.12…`). Subset-sum
counting by the verifier's own MITM (combinations-generated first
half, iterative-doubling second half, `bisect` counting; a
different generation mix from both producer scripts) reproduces
the F1-passing directed counts exactly on the two rows counted in
full: `(200, 1/4)`: `2,089,250,414` of `2^31 = 2,147,483,648`
directed; `(250, 1/2)`: `536,807,982` of `2^29 = 536,870,912`
directed. These counts are float-log based in all three
implementations (the F1 condition is a condition on log-sums);
exact agreement across three implementations with different
summation orders is the recorded evidence, and no filter count or
conclusion in R1 depends on this auxiliary table, exactly as the
correction log states. The correction itself is certified: the
faulty first version is superseded by the table in Section 8 of
`redteam.md` as printed there.

---

## 2. Theorem 13.3 gap: final status

**Closed by D0 (certified above).** Item A-W2 of `AUDIT-A.md`
records the gap; Cluster D supplies the missing two-line argument
in full. Theorems 13.3, 13.5 and 14.2 now rest on a proved
smoothness step, with the sole remaining dependence being
Theorem 4.2 at its audited status and "sufficiently large `b`"
(explicit sufficient condition recorded in the D0 chain, step 5).
Item A-W1 (the `z_b` max-form inconsistency) remains on record as
a wording item; it is vacuous in the regime used and does not
affect D0, D-SQ, or any other claim certified here.

---

## 3. The final certified residual R_D

For all sufficiently large `b`, a hypothetical `L = 2` disjoint
solution must satisfy **all** of the following, and nothing in
Cluster D removes any part of it. (For `b ≤ 2000` no solution
exists at all, by CENSUS0, certified.)

**(R_D.1) The forced form of Theorem 14.2**, now with proved
smoothness: `S_0 ⊔ S_1` partitions `{p : z_b < p ≤ b}`;
`c = P_0 u_0`, `c+1 = P_1 u_1`, `P_1 u_1 - P_0 u_0 = 1`;
`log P_0 = log P_1 = b/2 + o(b)`; `u_0, u_1` are `z_b`-smooth
divisors of `Λ_b` with `log u_i ≤ (1+o(1)) b/((1-ε) log b)`;
`P_0 u_0 ≡ -1 (mod P_1)`, `P_1 u_1 ≡ 1 (mod P_0)`; and
`den H([a,b]) = c(c+1)`.

**(R_D.2) The certified prime-square constraints (D-SQ / D1).**
For every prime `p` with `b/T_b < p² ≤ b`,
`T_b = floor((log b)/4)`: `p²` divides exactly one of `u_0, u_1`,
to the exact power `p²`, the other being prime to `p`, with
`w · (∑_{t ∈ S_p} t⁻¹) ≡ -1 (mod p)` for `w` the `p`-free part of
the divisible cofactor's `c+i`. In aggregate,
`(2 - o(1))√b ≤ log(u_0 u_1) ≤ (2 + o(1)) b/((1-ε) log b)` and
`max(u_0, u_1) ≥ exp((1 - o(1))√b)`.

**(R_D.3) The ceiling (D2).** Maximal prime powers contribute at
most `(2 + o(1))√b` to `log(u_0 u_1)` in total, so the mechanism of
(R_D.2) is saturated: any surviving solution must realise the bulk
of `log(u_0 u_1)` (anything up to the `b/log b` scale) through
first-power primes in `(√b, z_b]` dividing `c` or `c+1`, a band
forced by nothing in Cluster D. Primes `p ≤ √(b/T_b)` are likewise
unforced by the prime-square mechanism (the numerator bound
`log U ≤ log m + ψ(m)`, `m = floor(b/p²)`, no longer beats
`log p` there, so the lower `p⁻²` layer may cancel mod `p`).

**(R_D.4) The approximation constraint (D3).**
`|P_0/P_1 - u_1/u_0| = 1/(P_1 u_0)` exactly; `u_1/u_0` is a
strictly best approximation to `P_0/P_1` at denominators `≤ u_0`
and (Legendre) a convergent of `P_0/P_1`; symmetrically for
`u_0/u_1`. No impossibility of smooth convergents at this scale
is proved or claimed.

**(R_D.5) The quadratic reformulation adds no independent leverage
(Q1–Q3).** `Y² = 1 + 4PW` with `Y = 2c+1` is equivalent to
(R_D.1)'s consecutiveness equation via the explicit bijection of
Q1; the §2 splitting is that bijection's inverse, is idempotent,
preserves every size measure, and kills only the size-impossible
unbalanced splits; and no contradiction of the forms examined in
Prover 2's §3.1–§3.6 (mod `p | P`, mod `q | W`, small moduli,
Legendre/reciprocity signs, sign-pattern counting, quadratic-form
arguments) exists. Any future attempt through the discriminant
identity, the `Y mod p` splitting, or reciprocity probes on
`Y² = 1 + 4PW` alone is closed by equivalence, not merely
unproductive so far.

**(R_D.6) The computational obstruction map (R1, R2).** In the
instantiations `ε = 1/4` (`b = 30, …, 175`) and `ε = 1/2`
(`b = 200, 225`), of 165,522,272 directed forced-form candidates,
64,899,301 pass the size stage and exactly one passes the
smoothness stage `u_i | B_b(z_b)`: the `b = 30` candidate
(`P_0 = 6409, P_1 = 437, u_0 = 3, u_1 = 44, c = 19227`), which
passes `c(c+1) | Λ_b` and fails the exact interval test for every
`a`. For every `b ≥ 40` tested the smoothness count is zero,
including 33,098,231 size survivors at `b = 225` under the weakest
smoothness demand used. The least smoothness defect among size
survivors grows over the range (`D_min = 20.42, 25.91, 33.22` at
`b = 100, 120, 150`): no size survivor is within a `B_b`-rough
factor `e^{10}` of smooth. No statement is made for `b > 225` or
other `ε`.

**(R_D.7) Named extra inputs that a closure would need** (none is
a consequence of anything certified above):

* **E1.** The Theorem 13.5 mirror residues brought to bear with
  their values: the congruences
  `u_j · (P_j/p) ≡ -R_p^{-1} (mod p)` for `p ∈ S_j`, with `R_p`
  computed from the lower interval, in particular the top-half
  mod-`p²` congruences of Theorems 14.3–14.4
  (`c ≡ -p (mod p²)` or `c+1 ≡ -p (mod p²)` for `p > b/2`, and the
  reciprocal identity for `v_i = (c+i)/Q_i`). The identity of Q1
  sees only the sign `Y mod p`; the residues `R_p` are exactly the
  lower-interval data it discards.
* **E2.** The numerator congruence of the lower interval,
  `A + 2c + 1 ≡ 0 (mod c(c+1))` for `H([a,b]) = A/B` in lowest
  terms, brought to bear asymptotically. It is independent of the
  denominator identity plus consecutiveness plus the quadratic
  identity: all four CENSUS0 near-misses satisfy those and fail
  exactly this congruence (residues `360, 136, 852, 38766`, all
  nonzero), as does the red team's unique F4 survivor at the F5
  stage.
* **E3.** An effective `S`-unit smoothness obstruction uniform in
  growing support: a theorem that the forced CRT representatives
  modulo the balanced products `P_j` (equivalently, solutions of
  `P''W'' - P'W' = 1` with large primes each used exactly once)
  cannot be `z_b`-smooth of log-size `O(b/log b)`, with bounds
  uniform as the support `{p ≤ b}` grows with `b`. Fixed-support
  `S`-unit finiteness does not suffice. Equivalently, by (R_D.3):
  control, in either direction, of the first-power primes in
  `(√b, z_b]` inside `c` and `c+1`, or an upper bound
  `log(u_0 u_1) < (2 - o(1))√b`, which by D2 would have to come
  from exactly that band.

This residual is Problem 18.1 of the note, sharpened by (R_D.2) to
(R_D.4) and mapped computationally by (R_D.6), with the quadratic
route certified exhausted by (R_D.5). **Cluster D does not close
the `L = 2` case.**

---

## 4. Verifier's computational coverage (own code, exact arithmetic)

| Check | Coverage | Result |
|---|---|---|
| D1 Part C sieve counts | `b = 10^4 … 10^12`, exact prime enumeration to `√b ≤ 10^6` | `K(b)` and `bound/√b` match Prover 1 exactly / to 3 dp; tracks `2(1 - 1/√T_b)` within 0.06 |
| CENSUS0 near-misses | all four, exact `Fraction` recomputation | `B, c, A`, residues, sums match CENSUS0 exactly; `Q_T = ∅`, `a < b/2` fails, for all four |
| D-SQ Step 1 engine | `3000 ≤ b ≤ 20000` (step 97), `a = ⌊b/3⌋`, 1,129 `(b,p)` pairs | `S_p` nonempty, `0 < U < p`, `p ∤ UV`, `p ∤ t ∈ S_p`: zero failures |
| D0 finite form | `b ∈ {60, 120}`, all `n | Λ_b`, `n ≤ 3000` (2,591 divisors) | cofactor after removing `(z_b, b]` primes is `z_b`-smooth: zero exceptions |
| Q1 / Q2 / D3 | 600 random exact consecutive quadruples | identity, splitting recovery, idempotence, both D3 equalities: 600/600 |
| Q2 leak example | `P = 15, W = 40, Y = 49` | split `(3, 5, 8, 5)`, `gcd(W'', P'') = 5`, as claimed |
| Q3 Legendre | four near-misses; own balanced synthetics `b ∈ {50, 100, 200, 400}` | near-miss `(5,7)` both signs; synthetic `(W/p)`: `-1` 68, `+1` 53, `0` 0 (matches Prover 2 tally exactly); `(P/q)` both signs |
| Singleton scope | `(1,3,6), (2,3,6), (3,6,20)` exact | all three verify as solutions; `T_b = 0` at their `b`; no D-SQ claim applies |
| R1 own enumeration | `b = 30, 40, 50` (`ε = 1/4`), all directed partitions, no prune, trial-division F3 | `(F2, F3) = (30, 1), (62, 0), (239, 0)`; best `max(u) = 44, 394, 4007`: all match |
| R1 defect | `b = 100`, all 65,536 directed candidates | `F2 = 533`, `D_min = 20.424659307988424`, zero with `D ≤ 10`: matches |
| R1 prune validation | `b = 140` (`N = 22`, first pruned row), no-prune enumeration, 4,194,304 directed | `F2 = 8847`, `F3 = 0`, best `max(u) = 2389115168466718`: all match checkpoint |
| R1 `b = 30` candidate | full exact verification incl. F5 for all `a ∈ [1,30]`, two summation orders | passes F1–F4 exactly; fails F5 for every `a` |
| R1 aggregation | all 17 checkpoint files | totals `165,522,272 / 163,555,002 / 64,899,301 / 1 / 1 / 0`; `min_is_global` true in all |
| R2 MITM | `N` by trial-division primes, all six rows; full MITM counts for `(200, 1/4)`, `(250, 1/2)` | `N` matches all six rows; F1 counts `2,089,250,414` and `536,807,982` reproduced exactly |

Producer computations not independently re-run by the verifier and
relied on only as stated in the qualifications: the defect rows at
`b = 120, 150` (pipeline cross-validated at `b = 100`), the
enumeration rows `b ∈ {150, 160, 175, 200, 225}` (cross-validated
by aggregation, the producers' internal independent checks, and the
verifier's `b = 140` no-prune reproduction), and Prover 2's full
`(P/q)` tally (both signs independently confirmed on a subset).

---

## 5. Defects found, stated exactly

**P1-a (Prover 1, §3, wording only).** Theorem 14.4's bound is
described as "a polynomial bound". The bound is
`v_i ≥ (1 - o(1)) (log b)/(log 2)`, of order `log b` in `v_i`
itself, which is sub-polynomial. No consequence: the comparison's
substance is the different-quantity point adjudicated under D1.

**P1-b (Prover 1, Lemma D-SQ Step 1, exposition compressions).**
Two one-line steps are compressed: the passage from `ψ(m)` to
`(1 + o(1)) T` (needs monotonicity of `ψ`, supplied in the D-SQ
verification above) and the justification of `p > T` (cleanest via
`b > T³`, also supplied there). Both are fillable from facts in
the file; the lemma's proof is complete once they are read in.
No validity impact.

**P2-a (Prover 2, Proposition 1.2, wording only).** The phrase
"splitting datum (a choice, for each `p | P`, of a sign…)" can be
read as an independent choice; the datum is in fact forced by
`(P, W, Y)` (signs `= Y mod p`, `W`-split induced by `A, B`), as
Prover 2's own §2 construction shows. The bijection claim is
correct for the induced datum, which is the form the argument
uses. No validity impact.

**RT-a (Red Team, §1.2 and `redteam_search.py` docstring,
justification overbreadth).** The F1 guard-band justification
states "In every run `c ≥ p_max > 29`". As written this is false
for degenerate directed candidates (a side with `P_i = 1` has
`c = u_i`, which the stated inequality does not bound below by
`p_max`). The prune's safety does not rest on the sentence as
written: the prune was disabled for `N ≤ 20`; at any candidate
near the F1 boundary both `P_i` are large (their logs sum to `S`
and differ by at most `log B_b + 1`), forcing `c` large and
`log((c+1)/c)` negligible there; and the verifier's no-prune
re-enumeration at `b = 140` (the first pruned row) reproduces
`F2`, `F3`, and the exact best `max(u)`. No count is affected.

**No other defects found.** In particular: no wrong inequality
direction, wrong range, or wrong count was found in any claim
listed in Section 1; Prover 1's Part A census spot check (four
near-misses at `b ≤ 250`) and Part B forced-form measurements
(at `b = 156`: 18 primes in `(61, 156]`, 0 covered by `c(c+1)`;
at `b = 12`: the single prime `11`, covered) were recomputed and
are correct; Prover 2's §5.1 near-miss table (identity and
splitting hold in all four rows, numerator residue fails in all
four) and §5.3 synthetic size table are consistent with the
verifier's own recomputations at every point checked.

---

## 6. Files

| File | Role |
|---|---|
| `CLUSTER-D.md` | This record (the cluster's certified output). |
| `clusters/D/verifier_main.py` / `verifier_main_results.json` | Verifier checks for D0, D-SQ, D1, D3, Q1, Q2, Q3, near-miss and singleton scope. |
| `clusters/D/verifier_redteam.py` / `verifier_redteam_results.json` | Verifier checks for R1 (small enumeration, `b = 30` candidate, aggregation, defect at `b = 100`) and R2 (MITM). |
| `clusters/D/verifier_prune140.py` / `verifier_prune140_results.json` | Verifier no-prune re-enumeration at `b = 140` validating the F1 prune at a pruned row. |
| Producer files (unmodified) | `prover1.md`, `prover2.md`, `redteam.md` with their code, results, checkpoints and logs beside them in `clusters/D/`. |

Nothing was posted, emailed, or submitted anywhere.
