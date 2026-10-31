# Erdős #288, Cycle 1, Cluster D, Prover 2 (quadratic route)

**Verdict: the route FAILS, and the failure is exact, not a matter of
insufficient effort.** The discriminant identity
$Y^2 = 1 + 4PW$ is *equivalent* to the consecutiveness equation it was
derived from: the two systems have exactly the same solutions, via an
explicit bijection (§1). The mandated splitting of $P$ according to
$Y \equiv \pm 1 \pmod p$ is complete and is analysed in §2: it
reproduces the original factorisation $(P_0, P_1, u_0, u_1)$ verbatim,
it is idempotent, and every natural size measure is unchanged, so it
is a tautology, not a descent. The only sub-cases it eliminates
($P' = 1$, $P'' = 1$, and unbalanced splits) are eliminated by the
*size hypotheses alone*, not by the identity (§2.3). Every modulo and
quadratic-reciprocity probe in §3 either is automatic from the
existence of $Y$ or takes both signs on exact synthetic data, so no
forced sign exists to contradict. Computation (§5) confirms all of
this: the identity and the splitting hold exactly on all four
certified $L=2$ near-miss intervals of CENSUS0.md, none of which is a
solution, and they hold on balanced synthetic partitions whose
Bézout cofactors violate the smoothness bound by a growing factor,
so the identity plus balance do not even imply small $W$.

**Residual (the exact point of failure).** Everything survives: for
every sign pattern $\sigma \in \{\pm1\}^{\{p:\, z_b < p \le b\}}$ and
every coprime factorisation $W = W'W''$ with
$\log W = O(b/\log b)$, the split system
$P''W'' - P'W' = 1$ with $\log P' = \log P'' = b/2 + O(b/\log b)$ is
consistent with the identity, the splitting, all congruence probes
below, and consecutiveness. Closing $L=2$ therefore requires input
that is *not* a consequence of the identity: precisely, the mirror
congruences of Theorem 13.5 (in particular the top-half
mod-$p^2$ congruences of Theorems 14.3 and 14.4), or the numerator
congruence for the lower interval, or an effective theorem that the
forced CRT representatives cannot be $z_b$-smooth of the required
size (Problem 18.1). See §6 and §7.

**Does this close $L=2$, given Theorem 14.2? No.** It shows the
quadratic compression, by itself, cannot close it, and it maps
exactly which extra input any closure must use.

---

## 0. Inputs used, with audit status

Setting (from the task brief and Nayak's note, Sections 13, 14, 18):
a sufficiently large disjoint $L=2$ solution $[a,b]$, $[c,c+1]$,
$b < c$, $H([a,b]) + H([c,c+1]) \in \mathbb{Z}$ forces

$$c = P_0 u_0, \qquad c+1 = P_1 u_1, \qquad P_1 u_1 - P_0 u_0 = 1,$$

where, for a fixed $\varepsilon \in (0,1)$ and
$z_b = b/((1-\varepsilon)\log b)$:

- $P_i = \prod_{p \in S_i} p$, and $S_0 \sqcup S_1$ partitions the
  primes in $(z_b, b]$;
- $\log P_0 = \log P_1 = b/2 + o(b)$;
- $\log u_i \le (1+o(1))\, b/((1-\varepsilon)\log b)$, in particular
  $\log(u_0 u_1) = O(b/\log b)$.

Audit status, stated precisely. Theorem 14.2 as a *statement* is
taken as audited true with exposition gaps, per the task brief.
On disk, `AUDIT-A.md` certifies Theorem 3.2 (the intersecting case);
the audit evidence bearing on Sections 13 and 14 is the Cluster A
red-team discrepancy scan (`clusters/A/redteam.md`, Part 2), which
records: **D1**, the symbol $z_b$ is redefined between Sections 12
and 13 (the `max(L, .)` is dropped), vacuous for fixed $L$ and large
$b$ since $b/((1-\varepsilon)\log b) > L$ eventually; **D3**, the
proof of Theorem 13.3 asserts "all prime factors of $u_j$ are at most
$z_b$" without justification, and Theorems 13.3, 13.5, 14.2 rest on
it; **D7**, "mutual modular inverses" in Theorem 14.2's closing
sentence is loose terminology next to correct displayed congruences.
The scan's §2.2 records a line-by-line pass over Sections 4 to 15
finding no wrong inequality, range, or cross-reference beyond these
items.

The D3 gap is fillable, and since the smoothness of $W$ is the one
input this route might need, the fill is recorded here in full
(it is the red team's, verified independently below in §2.2):
if a prime $q > z_b$ divided $u_j$, then $q \mid c+j$, so
$q \in S_j$ and $q \mid P_j$, hence $q^2 \mid c+j$. But
$c+j \mid \Lambda_b$ (Theorem 4.2 of the note, whose instances the
red team checked), every prime factor of $c+j$ is at most $b$, and
$q > z_b \gg \sqrt b$ for large $b$ gives $q^2 > b$, so
$v_q(\Lambda_b) = 1$, contradicting $q^2 \mid c+j$. Hence every prime
factor of $u_j$ is at most $z_b$, i.e. $u_j$ is $z_b$-smooth and
$u_j \mid B_b(z_b)$. So: **smoothness of $W = u_0 u_1$ is available,
with dependence Theorem 4.2 plus the D3 fill**, not an open
assumption. The point of this report is that even granting it, the
quadratic route does not bite (§2.2 shows smoothness is used only to
clean up the splitting, never to contradict anything).

Census input: no $L=2$ solution exists for $b \le 2000$, certified in
`CENSUS0.md` (two independent implementations plus a verifier's third
method, exact arithmetic throughout). The four near-miss intervals
used in §5 are the complete list, for $b \le 2000$, of intervals
whose reduced denominator is pronic $B = c(c+1)$ with $c > b$.

Notation for the route: $P = P_0 P_1$ (squarefree, all prime factors
in $(z_b, b]$, $\log P = b + o(b)$), $W = u_0 u_1$.

---

## 1. The discriminant identity is an equivalence, not a compression

Substituting $P_1 = P/P_0$ in $P_1 u_1 - P_0 u_0 = 1$ and clearing
denominators gives the quadratic $u_0 P_0^2 + P_0 - P u_1 = 0$, whose
discriminant is $1 + 4 P W$. This much is the mandated derivation.
The decisive computation is what the square root *is*:

**Proposition 1.1 (the square root is $2c+1$).**
$Y := 2u_0 P_0 + 1$ satisfies $Y^2 = 1 + 4PW$, and
$Y = 2P_1 u_1 - 1 = 2c + 1$.

*Proof.* $Y = 2c+1$ since $u_0 P_0 = c$, and
$Y^2 = (2c+1)^2 = 4c(c+1) + 1 = 4 P_0 u_0 P_1 u_1 + 1 = 1 + 4PW$.
The middle form: $2P_1 u_1 - 1 = 2(c+1) - 1 = 2c+1$. ∎

**Proposition 1.2 (equivalence of the two systems).** The map
$(P_0, P_1, u_0, u_1) \mapsto (P, W, Y)$ above, and the inverse map
of §2 (splitting), are mutually inverse bijections between

(i) quadruples of positive integers with
$P_1 u_1 - P_0 u_0 = 1$, $\gcd(P_0, P_1) = 1$; and

(ii) triples $(P, W, Y)$ with $Y^2 = 1 + 4PW$, $Y$ odd, together with
a splitting datum (a choice, for each $p \mid P$, of a sign, and a
factorisation of $W$ induced by it; §2).

In particular the identity in (ii) carries *exactly* the information
of consecutiveness in (i): the identity is what consecutiveness
looks like after the change of variables
$(c, c+1) \mapsto (PW, 2c+1)$, since $PW = c(c+1)$ and
$Y^2 - 1 = (2c)^2 + 4c = 4c(c+1)$. Any argument that uses only the
identity, the size ranges, and the smoothness of $W$ is therefore an
argument about factorisations of consecutive integers into a large
squarefree part and a small smooth part, restated. It cannot
contradict such a factorisation without contradicting
consecutiveness itself in the same ranges. §5.1 shows this is not a
formality: the near-miss intervals satisfy the identity *and*
consecutiveness *and* $B = c(c+1)$, and are still not solutions.

A Pell-equation remark, for completeness: $Y^2 - 4PW = 1$ is the
Pell equation for the non-square $4PW$ (non-square because
$PW = c(c+1)$ lies strictly between $c^2$ and $(c+1)^2$ up to the
factor: $(2c)^2 < (2c+1)^2 - 1$). Pell equations have infinitely many
solutions $(Y_k, t_k)$ with $Y_k^2 - 4PW\, t_k^2 = 1$; the route
needs the very special solution with $t = 1$. Nothing in the Pell
theory of a *variable* modulus $PW$ (which itself depends on the
unknown factorisation) bounds $t$ away from 1.

---

## 2. The splitting, completely

Assume $Y^2 = 1 + 4PW$, $Y > 0$ (so $Y$ is odd), $P$ squarefree with
all prime factors odd and $> z_b$, and set

$$A = \tfrac{Y-1}{2}, \qquad B = \tfrac{Y+1}{2}, \qquad AB = PW,
\qquad B - A = 1, \qquad \gcd(A, B) = 1.$$

### 2.1 The split

For each $p \mid P$: $Y^2 \equiv 1 \pmod p$, so $Y \equiv \pm 1
\pmod p$; $p \nmid Y$ (else $p \mid 1$); and $p$ divides at most one
of $Y-1, Y+1$, since $p$ is odd and their difference is 2. Hence $p$
divides exactly one of $A, B$. Define

$$P' = \gcd(P, A), \qquad P'' = \gcd(P, B), \qquad
W' = A / P', \qquad W'' = B / P''.$$

Then, exactly:

1. $P = P' P''$, $\gcd(P', P'') = 1$ (each $p \mid P$ lands on
   exactly one side).
2. $W' W'' = W$ (since $AB = PW = P'P'' W'W''$).
3. $\gcd(W', W'') = 1$ (each divides one of the coprime $A, B$).
4. $P'' W'' - P' W' = B - A = 1$: **an equation of exactly the
   original shape**, with the same product $P'P'' = P$ and the same
   product $W'W'' = W$.
5. If in addition $p \nmid W$ for every $p \mid P$ (which the forced
   ranges give, §2.2), then $\gcd(W', P') = \gcd(W', P'') =
   \gcd(W'', P') = \gcd(W'', P'') = 1$: for instance if
   $p \mid P'$ and $p \mid W'$, then $p \mid A$ and, $p \nmid W$
   forcing $v_p(AB) = v_p(PW) = 1$, $p^2 \nmid A$, so $p \nmid W'$;
   the cross cases follow from $\gcd(A, B) = 1$ since $P'' \mid B$,
   $P' \mid A$. Under this cleanliness, $(P', P'', W', W'')$ is a
   quadruple of the original type, with $P', P''$ squarefree and
   coprime, $W', W''$ coprime.

Under the hypotheses of a genuine solution ($P_i$ the large parts of
$c, c+1$), the split returns $(P', P'', W', W'') = (P_0, P_1, u_0,
u_1)$: this is verified exactly on all data in §5.

### 2.2 Where smoothness is used, and the leak without it

Item 5 is the *only* place the route uses the smoothness of $W$,
and it uses only the consequence $p \nmid W$ for $p > z_b$
(which follows from $W$ being $z_b$-smooth). Without it the split
still satisfies items 1 to 4, but a prime of $P$ can leak into the
matching $W$-part. Exact example (code, Part 5): $A = 24$, $B = 25$,
$PW = 600$, $P = 15$, $W = 40$, $Y = 49$: here $P'' = 5$ and
$W'' = 5$, sharing the prime 5. So the dependence is flagged
precisely: *cleanliness of the splitting depends on
$p \nmid W$ for $p \mid P$; nothing else in this report uses
smoothness, and cleanliness produces no contradiction either way.*

### 2.3 Size analysis: which sub-cases die, and what kills them

From $A(A+1) = PW$ with $A < \sqrt{PW} < A+1$:

$$\log A = \tfrac12(\log P + \log W) + o(1)
= \tfrac{b}{2} + O\!\left(\tfrac{b}{\log b}\right),$$

using only $\log P = b + o(b)$ and $0 \le \log W = O(b/\log b)$.
Since $0 \le \log W' \le \log W$ and $\log P' = \log A - \log W'$
(likewise for $P''$):

$$\log P',\ \log P'' \;\in\; \left[\tfrac b2 - O\!\left(\tfrac{b}{\log b}\right),\
 \tfrac b2 + O\!\left(\tfrac{b}{\log b}\right)\right].$$

Consequences:

- **$P' = 1$ and $P'' = 1$ are impossible for large $b$**, and more
  generally any unbalanced split with
  $|\log P' - b/2| = \omega(b/\log b)$ is impossible. This is a
  genuine elimination, but note what does the work: the *size
  hypotheses* ($\log P$ large, $\log W$ small), not the identity and
  not the splitting. Nayak's Theorem 13.3 already gives the same
  balance directly. The quadratic route adds nothing here.
- **Every balanced split survives.** There is no size constraint on
  $W', W''$ individually beyond $W'W'' = W$ and coprimality:
  $W' = 1$ (i.e. $u_0 = 1$), $W'' = 1$, and every intermediate split
  are all consistent with all hypotheses. No sub-case on the
  $W$-side is eliminated by anything in this route.

### 2.4 No descent

Apply the splitting to its own output $(P', P'', W', W'')$: the
associated $Y$ is $2P'W' + 1 = 2A + 1 = Y$, so the second split is
identical to the first. The splitting is **idempotent in one step**.
Every candidate descent measure is constant:
$\log P' + \log P'' = \log P$, $\log W' + \log W'' = \log W$,
$\max(\log P', \log P'')$ is forced into the same
$b/2 + O(b/\log b)$ window before and after, and the equation
$P''W'' - P'W' = 1$ has the same shape and the same scale as
$P_1 u_1 - P_0 u_0 = 1$. There is no smaller instance to descend to.
Formally: the splitting is the inverse map of Proposition 1.2, and a
bijection between a system and itself cannot power a descent.

---

## 3. Modulo and quadratic-form probes, one by one

**3.1 Modulo $p \mid P$.** Gives $Y \equiv \pm 1 \pmod p$ and nothing
else: no condition on $W \bmod p$ results, because the equation mod
$p$ is $Y^2 \equiv 1$, in which $W$ has vanished. Lifting to
mod $p^2$ (for $p \mid P'$, say) gives
$(Y-1)/(2p) \cdot (P/P') \equiv W' \cdot (\text{unit}) \pmod p$: it
*determines* a residue for the cofactor rather than restricting it.
Residues of this shape are exactly the mirror congruences of
Theorem 13.5, which are extra input (§7), not consequences of the
identity that could contradict it.

**3.2 Modulo $q \mid W$.** Symmetrically, $Y^2 \equiv 1 \pmod q$, in
fact $Y \equiv \pm 1 \pmod{q^{v_q(W)}}$ on the side carrying that
prime power (prime powers of $W$ cannot straddle $A, B$, by
coprimality). This refines the splitting to prime powers of $PW$ and
is again a restatement of the factorisation of the consecutive pair
$A, B$. Both signs occur (in §5.1, $Y \equiv 1 \pmod q$ on the $c$
side and $Y \equiv -1 \pmod q$ on the $c+1$ side, by construction of
$Y = 2c+1$). No contradiction is available.

**3.3 Small moduli, parity.** $P$ is odd (all its primes exceed
$z_b \ge 2$, and exceed 2 for large $b$). $Y$ odd gives
$Y^2 \equiv 1 \pmod 8$, so $PW = (Y^2-1)/4$ is even; since $P$ is
odd, $2 \mid W$. That is the true and only content: the even one of
$c, c+1$ has even smooth cofactor (its large part is odd). $Y \bmod
4$ is $1$ if $c$ is even, $3$ if $c$ is odd; both occur in the
synthetic data of §5.3 ($Y \bmod 4 = 3, 3, 3, 1$). No elimination.

**3.4 Legendre symbols and reciprocity.** For an odd prime
$\ell \nmid 2PW$, the identity says $1 + 4PW$ is a square mod $\ell$,
which is automatic once $Y$ exists and constrains only the pair
$(P \bmod \ell, W \bmod \ell)$ jointly; neither residue is fixed by
the hypotheses (the partition, hence $P \bmod \ell$, varies over all
sign patterns, §3.5; $W$ ranges over $z_b$-smooth residues). The
symbols one might hope reciprocity would force are in fact free:
on the synthetic data of §5.3, $(W / p)$ for $p \mid P$ takes the
values $-1$ sixty-eight times and $+1$ fifty-three times (never $0$,
as $p \nmid W$ is forced there by construction of the test, the
$u_i$ being Bézout representatives, and is checked); on the
near-misses of §5.1 it takes both signs already within the single
example $(a,b) = (5,7)$: $(W/5) = +1$, $(W/7) = -1$. Likewise
$(P / q)$ for odd $q \mid W$ on the synthetic data: $-1$ seven times,
$+1$ eight times. A reciprocity contradiction requires a forced
sign; there is none.

**3.5 Counting sign patterns.** By CRT, the solutions of
$Y^2 \equiv 1 \pmod P$ are in bijection with sign patterns
$\sigma \in \{\pm 1\}^{\{p \mid P\}}$: exactly
$2^{\pi(b) - \pi(z_b)}$ residue classes mod $P$, one per partition
of the prime set. The identity imposes no preference among them.
The number of patterns is enormous ($\pi(b) - \pi(z_b) \sim
b/\log b$), so a counting argument ("too many patterns to all fail
smoothness") runs in the wrong direction for this route: most
patterns correspond to non-smooth cofactors (§5.3), and ruling out
the smooth ones pattern by pattern is Problem 18.1, not a
consequence of the identity.

**3.6 Quadratic forms.** $Y^2 = 1 + 4PW$ is the norm equation
$N\big(\tfrac{Y+1}{2} + \tfrac{Y-1}{2}\big)$ in disguise: its
factorisation over $\mathbb{Z}$ is $(Y-1)(Y+1) = 4PW$ with the two
factors differing by 2 and coprime after halving, which is §2.
Factorising in a quadratic ring changes nothing: the norm of
$\frac{Y + \sqrt{Y^2 - 4PW}}{2}$ style elements presupposes the
discriminant $1 + 4PW$ one is trying to rule out. No class-group or
genus condition is available, because the form's discriminant is the
unknown $PW$ itself, not a fixed integer.

---

## 4. Does the argument use consecutiveness, or only the identity?

Only the identity, plus the size and smoothness hypotheses. Every
step of §§2 and 3 starts from $Y^2 = 1 + 4PW$. And by Proposition
1.2 this is not an accident of the attempts made here: the splitting
*outputs* consecutiveness ($B - A = 1$ with $A = P'W'$, $B = P''W''$)
from the identity, so "identity plus splitting" and
"consecutiveness" are the same system. The exact residual of this
route is therefore:

> **Residual $R_D$.** Rule out, for all sufficiently large $b$, a
> consecutive pair $A, A+1$ in which every prime in $(z_b, b]$
> divides exactly one of $A, A+1$ to the first power, the two large
> parts are balanced ($\log = b/2 + o(b)$), and both complementary
> cofactors are $z_b$-smooth of log-size $O(b/\log b)$.

But $R_D$ is precisely the content of Theorem 14.2's system restated
(it is Problem 18.1 of the note, minus the mirror congruences and
the denominator identity). The quadratic route returns the problem
to exactly where Nayak left it. Any proof that goes further must,
at some step, use a property of the *lower* interval $[a,b]$ or of
the mirror residues $R_p$, neither of which appears anywhere in
$Y^2 = 1 + 4PW$.

---

## 5. Exact computation

Code: `prover2_checks.py` in this directory; full machine-readable
output: `prover2_results.json`; run log: `prover2_run.log`. All
decisions in exact integer and `Fraction` arithmetic (`math.isqrt`,
`gcd`, modular inverses); floats appear only in reported logarithms.
Every assertion in the code passed (`ALL EXACT ASSERTIONS PASSED`).

### 5.1 The four certified near-misses: the identity holds, the solution fails

For each near-miss interval, $H([a,b]) = A/B$ was recomputed from
scratch, $B = c(c+1)$ with $c > b$ verified, and the route data
built by extracting the prime factors $> z_b$ (at $\varepsilon = 0$,
$z_b = b/\log b$; a small-$b$ analogue, used only to exhibit the
factorisation) into $P_0, P_1$:

| $(a,b)$ | $B$ | $c$ | $(P_0, P_1)$ | $(u_0, u_1)$ | $Y$ | $(A{+}2c{+}1) \bmod B$ | $H([a,b]) + H([c,c{+}1])$ |
|---|---|---|---|---|---|---|---|
| $(4,7)$ | 420 | 20 | $(5, 7)$ | $(4, 3)$ | 41 | 360 | $6/7$ |
| $(5,7)$ | 210 | 14 | $(7, 5)$ | $(2, 3)$ | 29 | 136 | $68/105$ |
| $(9,12)$ | 1980 | 44 | $(11, 5)$ | $(4, 9)$ | 89 | 852 | $71/165$ |
| $(154,156)$ | 1861860 | 1364 | $(31, 1)$ | $(44, 1365)$ | 2729 | 38766 | $71/3410$ |

In all four cases: $Y^2 = 1 + 4PW$ holds exactly
(e.g. $41^2 = 1681 = 1 + 4\cdot 35\cdot 12$;
$2729^2 = 7447441 = 1 + 4\cdot 31\cdot 60060$);
$P_1 u_1 - P_0 u_0 = 1$ holds; and the splitting of §2, computed from
$(P, W, Y)$ alone via gcds, recovers $(P_0, P_1, u_0, u_1)$ exactly.
None of the four is a solution: each fails the numerator residue
$(A + 2c + 1) \bmod B \ne 0$, and each exact total is a non-integer,
matching CENSUS0.md's table entry for entry. **Conclusion: the
identity, consecutiveness, and even the denominator condition
$B = c(c+1)$ together do not imply a solution. Whatever kills these
four (the numerator congruence, a property of the lower interval) is
invisible to this route, and a large-$b$ proof along this route
would need an input that, unlike the identity, can see it.**
Small-$b$ honesty: the full partition of $(z_b, b]$ holds for the
first two rows (primes 5, 7, none missing) but fails for
$(9,12)$ (prime 7 missing) and $(154,156)$ (25 of the 26 primes in
range missing), as expected since Theorem 14.2 is a sufficiently-large
statement; the identity and splitting, by contrast, hold in all four
rows with no largeness hypothesis, which is the point.

### 5.2 Random consecutive pairs: the identity is a tautology, tested

2000 random $c \in [2, 10^7)$, each factored at an extraction
threshold, $Y = 2c+1$: the identity $Y^2 = 1 + 4PW$ and exact
recovery of the factorisation by the gcd splitting passed in
2000 of 2000 cases, 0 failures. This is the computational shadow of
Proposition 1.2: there was no case to fail.

### 5.3 Balanced synthetic partitions: identity and balance do not imply small $W$

For $b \in \{50, 100, 200, 400\}$, $z_b = b/\log b$, the primes in
$(z_b, b]$ were partitioned greedily by log-weight into $P_0, P_1$
(full partition, squarefree, coprime, balanced to within one prime:
$|\log P_0 - \log P_1| \le \log b$ in all four cases), and the Bézout
representatives $u_1 = P_1^{-1} \bmod P_0 \in [1, P_0)$,
$u_0 = (P_1 u_1 - 1)/P_0$ were taken, so
$P_1 u_1 - P_0 u_0 = 1$ holds exactly by construction (these $u_i$
are the Theorem 13.5 representatives: the unique ones in range with
the forced congruences). The identity and the gcd splitting were
verified exactly in all four cases. The cofactor sizes:

| $b$ | primes in range | $\log P_0$ | $\log P_1$ | $\log W$ | $b/\log b$ | $\log W \,/\, (b/\log b)$ | $u_0, u_1$ $z_b$-smooth? |
|---|---|---|---|---|---|---|---|
| 50 | 10 | 16.673 | 16.543 | 28.253 | 12.781 | 2.211 | no, no |
| 100 | 17 | 35.373 | 32.268 | 65.489 | 21.715 | 3.016 | no, no |
| 200 | 34 | 79.431 | 79.497 | 157.753 | 37.748 | 4.179 | no, no |
| 400 | 60 | 158.826 | 158.788 | 313.426 | 66.762 | 4.695 | no, no |

(Finite-$b$ note: $\log P = \theta(b) - \theta(z_b)$ is still visibly
below its asymptotic $b + o(b)$ at these $b$; the tested properties
are the full partition and the balance between the two halves, which
hold.) The generic Bézout cofactor has $\log W$ comparable to
$\log P$, exceeding the forced scale $b/\log b$ by a factor growing
from 2.2 to 4.7, and its largest prime factors are enormous
(e.g. at $b = 200$, $\mathrm{lpf}(u_0) =
18619644087876950840844529606705141$, against $z_b \approx 37.7$).
**Conclusion: the identity, the full partition, and the balance
condition, taken together, are satisfied by data whose $W$ violates
the smoothness and size conclusions by orders of magnitude. The
smallness of $W$ in a genuine solution is therefore entirely an
*input* (Theorem 13.3, via $c+j \mid \Lambda_b$), and the identity
provides no mechanism that could derive or contradict it.** The one
candidate contradiction that "bites" anywhere in this section is the
smoothness input itself, biting generic synthetic data; it does not
bite, and cannot be made to bite, from within the quadratic route.

### 5.4 Which candidate contradictions bite: summary

| Candidate | Near-misses (§5.1) | Random consecutive (§5.2) | Balanced synthetic (§5.3) | Verdict |
|---|---|---|---|---|
| $Y \equiv \pm1 \pmod p$, $p \mid P$ | holds | holds | holds | automatic, no bite |
| Splitting balance | recovers parts | recovers parts | recovers parts | tautology (§2) |
| $P' = 1$ / unbalanced split | n/a at small $b$ | size kills it | size kills it | killed by size hypotheses, not the identity (§2.3) |
| $Y \bmod q$, $q \mid W$ | holds, both signs | holds | holds | automatic (§3.2) |
| Parity, $Y \bmod 4$, mod 8 | holds | holds | both residues occur | only $2 \mid W$ (§3.3) |
| Legendre $(W/p)$, $(P/q)$ | both signs | both signs | 68 vs 53; 7 vs 8 | no forced sign (§3.4) |
| Smallness / smoothness of $W$ | holds (small $b$) | varies | **fails by factor 2.2 to 4.7 and in smoothness** | an input, not a consequence (§5.3) |
| Numerator residue $\bmod B$ | **fails (all four)** | n/a | n/a | kills the near-misses; outside this route (§5.1) |

---

## 6. The surviving sub-case, stated as the residual

After everything in this route is applied, the surviving
configuration is the *whole* balanced region, with no sub-case
removed except the size-impossible unbalanced splits of §2.3:

> For sufficiently large $b$, a hypothetical $L=2$ solution is, in
> this route's variables, a choice of sign pattern
> $\sigma \in \{\pm 1\}^{\{p:\, z_b < p \le b\}}$ (all
> $2^{\pi(b)-\pi(z_b)}$ patterns survive) and a coprime factorisation
> $W = W'W''$ (all survive, including $W' = 1$ and $W'' = 1$), with
> $P' = \prod_{\sigma_p = +1} p$, $P'' = \prod_{\sigma_p = -1} p$
> automatically balanced, satisfying $P''W'' - P'W' = 1$.

Equivalently $R_D$ of §4. In the ranges: all large $b$; the route
gives no threshold, no excluded sub-range of $b$, no excluded sign
pattern, and no excluded cofactor split. This is a precisely mapped
failure: the quadratic compression is a change of variables with a
bijective splitting, and changes of variables do not prove
non-existence.

---

## 7. What extra input would be needed (beyond the identity)

Any one of the following would be genuinely new information relative
to this route; none is a consequence of $Y^2 = 1 + 4PW$:

- **(E1) The mirror congruences with their residues.**
  Theorem 13.5: $u_j \cdot (P_j / p) \equiv -R_p^{-1} \pmod p$ for
  $p \in S_j$, where $R_p$ is computed from the *lower* interval.
  These pin each $u_j$ into one CRT class modulo $P_j$ with
  prescribed residues. The identity sees only the class of $Y$ mod
  $p$ (a sign); the values $R_p$ are exactly the lower-interval data
  the identity has discarded. The top-half specialisation
  (Theorem 14.3: $c \equiv -p \pmod{p^2}$ or $c+1 \equiv -p
  \pmod{p^2}$ for $p > b/2$) and its consequence Theorem 14.4
  ($v_i \sum_{p \in T_i} 1/p = h_i - 1/Q_i$, forcing
  $v_i \ge (1-o(1)) (\log b)/(\log 2)$) are of this type. Audit
  status: supported by the Cluster A scan (§0); these are the
  natural next inputs for Cluster D, and they belong to Prover 1's
  side of the design or a Cycle 2 cluster, not to the quadratic
  identity.
- **(E2) The numerator congruence of the lower interval.**
  Integrality is equivalent (Proposition 16.1's verification
  condition, certified as the correct criterion in CENSUS0.md) to
  $B = c(c+1)$ *and* $A + 2c + 1 \equiv 0 \pmod{c(c+1)}$ for
  $H([a,b]) = A/B$. Section 5.1 proves by four exact examples that
  the first condition plus the identity plus consecutiveness do not
  imply the second. Any closure must use the second, or an
  equivalent lower-interval condition, somewhere.
- **(E3) An effective smoothness obstruction for the forced class.**
  A theorem that the CRT representative of §5.3 type cannot be
  $z_b$-smooth with $\log u = O(b/\log b)$ when the modulus is a
  balanced product of *all* primes in $(z_b, b]$. This is an
  $S$-unit equation problem ($P''W'' - P'W' = 1$ with prime support
  in $\{p \le b\}$, the large primes each used exactly once): for
  *fixed* support, $S$-unit equations have finitely many solutions
  with effective bounds, but here the support grows with $b$ and any
  usable bound must be uniform in that growth. That uniformity is
  the mathematical content of Problem 18.1, and it is where the
  actual difficulty of the $L=2$ case lives. The quadratic route
  neither supplies it nor reduces it.

Conversely, this report also certifies a negative service for the
campaign: no future cluster needs to re-attempt the discriminant
compression, the $Y \bmod p$ splitting, or reciprocity probes on
$Y^2 = 1 + 4PW$. They are closed, by equivalence (Proposition 1.2),
not merely unproductive so far.

---

## 8. Files

| File | Role |
|---|---|
| `prover2.md` | This report. |
| `prover2_checks.py` | All exact computations of §5 (near-misses from scratch, random consecutive pairs, balanced synthetic partitions with Bézout representatives, Legendre distributions, the §2.2 leak example). |
| `prover2_results.json` | Machine-readable output of the checks. |
| `prover2_run.log` | Run log; final line `ALL EXACT ASSERTIONS PASSED`. |

Nothing was posted, emailed, or submitted anywhere.
