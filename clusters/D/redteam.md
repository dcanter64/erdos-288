# Cluster D, Red Team (constructive): trying to build an L = 2 solution from the forced form

**Verdict: no solution found, and none was close at the decisive filter.**
Every directed partition candidate was killed, for every $b$ tested, at or
before the smoothness stage F3, with exactly one exception in the whole run:
at $b=30$ a single candidate passed smoothness and even the
$\Lambda_b$ divisibility stage F4, and then failed the exact interval test
F5 for every $a$ (Section 5). For all $b \ge 40$ tested, **zero** candidates
pass F3. The construction does not die at the size stage: at most $b$ there
are hundreds to tens of thousands of partitions whose minimal Bezout
cofactors $u_0,u_1$ both fit under the exact bound $B_b(z_b)$; it dies at
the requirement that those cofactors actually *divide* $B_b(z_b)$, i.e. be
$z_b$-smooth with the prime-power caps of $\Lambda_b$. The smoothness-defect
quantification (Section 6) measures the margin: even the least defective
size survivor still carries a $B_b$-rough factor of size $e^{D_{\min}}$,
with $D_{\min} = 20.4, 25.9, 33.2$ at $b = 100, 120, 150$ respectively,
and no size survivor at those $b$ within a rough factor of $e^{10}$.

This is a finite computational obstruction map for the instantiations
below, not a proof for large $b$: the forced form of Theorem 14.2 is an
asymptotic statement ("sufficiently large"), and the instantiations here
fix $\varepsilon$ and replace every $o(1)$ by the exact finite object
$B_b(z_b)$. What the computation shows is that the forced form, taken at
face value at these $b$, produces no solution and is not near producing
one at the smoothness stage.

## 1. Method, exactly as run

Code: `redteam_search.py` (enumeration and filters), `redteam_verify_small.py`
(independent re-derivation, Section 7), `redteam_sanity.py` (direct census
cross-check, Section 7), `redteam_defect.py` (Section 6),
`redteam_aggregate.py` (table assembly), `redteam_mitm_counts.py`
(Section 8). Per-$b$ checkpoints: `redteam_checkpoint_<tag>_<b>.json`;
assembled data: `redteam_data.json`. All filter decisions are exact
integer arithmetic (Python `int`); floating point is used only for the
F1 balance prune (with a guard band proved safe below) and for reporting
logarithms.

### 1.1 The instantiation

Fix $\varepsilon \in (0,1)$ and $b$, and put

- $z_b = b\,/\,((1-\varepsilon)\log b)$ (real), as in Theorem 12.1/14.2;
- large primes $\mathcal L_b = \{p \text{ prime} : z_b < p \le b\}$,
  $N = |\mathcal L_b|$, $P_{\mathrm{tot}} = \prod_{p\in\mathcal L_b} p$,
  $S = \log P_{\mathrm{tot}}$;
- $B_b = B_b(z_b) = \prod_{p \le z_b} p^{e_p}$, $e_p = \max\{e : p^e \le b\}$,
  the $z_b$-smooth part of $\Lambda_b = \operatorname{lcm}(1,\dots,b)$
  (Lemma 13.2's $B_b(z)$), computed with exact integer prime powers.

A *directed candidate* is an ordered partition
$\mathcal L_b = S_0 \sqcup S_1$, $P_i = \prod_{p\in S_i} p$, together with
the minimal positive solution of $P_1 u_1 - P_0 u_0 = 1$. Minimality is
exact: the general positive solution is
$(u_0,u_1) + t(P_1,P_0)$, $t \ge 0$, over the least positive residue
$u_0 \equiv -P_0^{-1} \pmod{P_1}$, so the minimal positive solution
simultaneously minimises $u_0$, $u_1$, and $\max(u_0,u_1)$, and has
$u_0 < P_1$, $u_1 < P_0$ (with the $P_i = 1$ degeneracies handled
directly: if $P_1 = 1$ the minimum is at $u_0 = 1$, $u_1 = 1 + P_0$).

This is the Theorem 14.2 form with the asymptotic bounds replaced by
their strongest exact finite analogues: $\log P_i$ near $S/2$ is what
$c = P_0u_0$, $c+1 = P_1u_1$ forces once $u_i$ are small; $u_i \le
\exp((1+o(1)) z_b)$ is replaced by $u_i \le B_b$, and the actual
Theorem 13.3/14.2 requirement $u_i \mid B_b$ is imposed verbatim at F3.

### 1.2 Filters

- **F1, balance.** $|\log P_0 - \log P_1| \le \log B_b + 1$. This is a
  *necessary* condition for F2, not an ad hoc window: if $u_0,u_1 \le B_b$
  and $P_1u_1 - P_0u_0 = 1$ with $c = P_0u_0$, then
  $\log P_0 - \log P_1 = \log(u_1/u_0) + \log\frac{c}{c+1}$, hence
  $|\log P_0 - \log P_1| \le \log B_b + \log\frac{c+1}{c}$. In every run
  $c \ge p_{\max} > 29$, so $\log\frac{c+1}{c} < 0.04$ and the $+1$ guard
  leaves slack $> 0.96$, dwarfing float error ($<10^{-11}$). For $N \le 20$
  the prune was disabled entirely and every partition was evaluated.
  F1 is weak by design: it typically passes $> 97\%$ of partitions.
- **F2, size.** $u_0 \le B_b$ and $u_1 \le B_b$ (exact integer compare).
- **F3, smoothness/divisibility.** $u_0 \mid B_b$ and $u_1 \mid B_b$
  (exact trial division by all $p \le z_b$ with exponent caps $e_p$).
  This is the condition "$u_i$ is $z_b$-smooth and $c, c+1$ can divide
  $\Lambda_b$" in the forced form.
- **F4, $\Lambda_b$.** $c(c+1) \mid \Lambda_b$ for $c = P_0u_0$ (exact
  big-integer mod; implied by F3 plus the shape of $P_i$, checked anyway).
- **F5, interval test.** For a survivor $(b,c)$: test every $1 \le a \le b$
  exactly (`fractions.Fraction`) for $\operatorname{den} H([a,b]) = c(c+1)$
  and $A(a,b) \equiv -(2c+1) \pmod{c(c+1)}$. This is the exact pair-sum
  condition, since $H([c,c+1]) = (2c+1)/(c(c+1))$ in lowest terms
  (Theorem 14.1), so $H([a,b]) + H([c,c+1]) \in \mathbb Z$ iff the
  denominator is exactly $c(c+1)$ and the residues cancel as shown. A
  passing $a$ would be re-verified inside `interval_test` by a second
  summation in reverse order.

### 1.3 Enumeration and the complement symmetry

Subsets are enumerated by Gray code over the $N-1$ free large primes
(the largest large prime is fixed in $S_0$'s side $A$), giving each
*unordered* pair $\{A, P_{\mathrm{tot}}/A\}$ once: $2^{N-1}$ states,
each giving two directed candidates. The second direction needs no
second modular inversion: if $Bu_1 - Au_0 = 1$ with $1 \le u_0 < B$,
$1 \le u_1 < A$, then $A(B-u_0) - B(A-u_1) = 1$, i.e. the swapped
candidate has $(u_0', u_1') = (A - u_1,\; B - u_0)$, and this identity is
asserted in exact integers at every state. Subset-sum (log) pruning is
the F1 test on the running Gray-code log-sum. This symmetry is also
conceptually informative: for each unordered pair, the two directions'
cofactors sum to the opposite moduli ($u_0 + u_1' = P_1$ etc.), so a pair
can only be promising in one direction unless both directions' cofactors
are simultaneously far from the top of their ranges.

## 2. Range covered, and why

Two instantiations:

- **$\varepsilon = 1/4$** ($z_b = \tfrac43 b/\log b$), $b = 30, 40, \dots, 150$
  in steps of 10, plus $b = 160, 175$. Here $N$ grows from 5 to 26;
  $2^{N-1}$ unordered states reach $33.5$ million at $b = 175$.
- **$\varepsilon = 1/2$** ($z_b = 2b/\log b$), $b = 200, 225$. At these $b$
  the $\varepsilon = 1/4$ prime set has $N = 31$ ($b=200$), i.e.
  $2^{30} \approx 1.1\times10^9$ unordered states, outside the budget of
  this run; $\varepsilon = 1/2$ shrinks $\mathcal L_b$ to $N = 25$ while
  *weakening* the smoothness filter ($z_b$ and $B_b$ both grow; at
  $b = 200$, $\log B_b = 83.5 > S/2 = 61.3$, so F2 is vacuous there and
  only F3 bites). The $b=200,225$ rows therefore test a strictly weaker
  instantiation at larger $b$, and they still produce no F3 survivor.

Small $b$ ($30$–$50$) are included as pipeline sanity range, overlapping
the certified census. The range stops at $b = 225$: see Section 8 for the
count explosion beyond it. The forced form is an asymptotic statement,
so no finite $b$ is "the" range; the choices above are exactly the range
in which exhaustive directed enumeration, with an exact Bezout solve at
essentially every F1-passing state, was feasible on this machine.

## 3. Results: per-filter survival counts

Totals over the whole campaign of this cluster: **165,522,272 directed
candidates** were generated; 163,555,002 passed F1; **64,899,301 passed
the size stage F2**; **exactly 1 passed the smoothness stage F3** (at
$b=30$, Section 5); that 1 passed F4 and failed F5. No solution was found.

| b | eps | zb | N | S/2 | log Bb | directed | F1 | F2 | F3 | F4 | F5 | min log max(u) | margin vs log Bb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | 0.25 | 11.8 | 5 | 7.4 | 13.6 | 32 | 32 | 30 | 1 | 1 | 0 | 3.78 | -9.85 |
| 40 | 0.25 | 14.5 | 6 | 9.7 | 16.9 | 64 | 64 | 62 | 0 | 0 | 0 | 5.98 | -10.91 |
| 50 | 0.25 | 17.0 | 8 | 13.9 | 21.7 | 256 | 256 | 239 | 0 | 0 | 0 | 8.30 | -13.37 |
| 60 | 0.25 | 19.5 | 9 | 16.5 | 24.6 | 512 | 512 | 450 | 0 | 0 | 0 | 12.58 | -12.03 |
| 70 | 0.25 | 22.0 | 11 | 20.6 | 25.3 | 2048 | 2048 | 1222 | 0 | 0 | 0 | 13.63 | -11.68 |
| 80 | 0.25 | 24.3 | 13 | 25.5 | 28.4 | 8192 | 8192 | 3556 | 0 | 0 | 0 | 19.70 | -8.74 |
| 90 | 0.25 | 26.7 | 15 | 30.0 | 29.5 | 32768 | 32768 | 1483 | 0 | 0 | 0 | 22.14 | -7.40 |
| 100 | 0.25 | 29.0 | 16 | 32.3 | 29.5 | 65536 | 65536 | 533 | 0 | 0 | 0 | 23.66 | -5.88 |
| 110 | 0.25 | 31.2 | 18 | 38.2 | 36.3 | 262144 | 262144 | 4950 | 0 | 0 | 0 | 27.32 | -9.02 |
| 120 | 0.25 | 33.4 | 19 | 40.5 | 36.3 | 524288 | 524288 | 465 | 0 | 0 | 0 | 30.41 | -5.93 |
| 130 | 0.25 | 35.6 | 20 | 42.9 | 41.0 | 1048576 | 1048576 | 16636 | 0 | 0 | 0 | 32.43 | -8.61 |
| 140 | 0.25 | 37.8 | 22 | 48.5 | 44.7 | 4194304 | 4098458 | 8847 | 0 | 0 | 0 | 35.41 | -9.24 |
| 150 | 0.25 | 39.9 | 23 | 51.0 | 44.7 | 8388608 | 8102446 | 763 | 0 | 0 | 0 | 39.01 | -5.65 |
| 160 | 0.25 | 42.0 | 24 | 54.2 | 48.4 | 16777216 | 16392494 | 4505 | 0 | 0 | 0 | 38.81 | -9.56 |
| 175 | 0.25 | 45.2 | 26 | 60.0 | 54.7 | 67108864 | 65922950 | 29009 | 0 | 0 | 0 | 45.22 | -9.47 |
| 200 | 0.5 | 75.5 | 25 | 61.3 | 83.5 | 33554432 | 33544874 | 31728320 | 0 | 0 | 0 | 44.80 | -38.66 |
| 225 | 0.5 | 83.1 | 25 | 62.3 | 92.2 | 33554432 | 33549364 | 33098231 | 0 | 0 | 0 | 48.59 | -43.66 |

"min log max(u)" is the minimum, over **all** directed candidates at that
$b$ (the checkpoint field `min_is_global` is true for every row: any
F1-pruned candidate has $\max(u_0,u_1) > B_b$, and the reported minimum is
below $B_b$ in every row, so the minima are global, not minima over the
evaluated subset), of $\log \max(u_0,u_1)$ for the minimal Bezout solution.

## 4. The obstruction map

**F1 (balance) obstructs almost nothing.** It passes 97–100% of directed
partitions in every row. This is expected at these $b$: $\log B_b$ is
still a substantial fraction of $S$, so the necessary balance condition
derived from $u_i \le B_b$ is weak. Subset-sum pruning on the logs, by
itself, does not get near a construction or an exclusion.

**F2 (size) obstructs the typical candidate but never the best ones, and
is not where the construction dies.** The minimal achievable
$\log\max(u_0,u_1)$ is consistently *below* the allowed $\log B_b$, by
5.65 to 13.37 log units in the $\varepsilon = 1/4$ rows and by 38.66 and
43.66 log units in the (deliberately weaker) $\varepsilon = 1/2$ rows.
As a function of $b$, the minimum grows roughly linearly and sits at a
remarkably stable fraction of $S/2$: $\min \log\max(u) / (S/2)$ is
between 0.71 and 0.78 for every $b \ge 100$ in both instantiations
(0.73 at $b=100$, 0.75 at $b=120$, 0.77 at $b=150$, 0.75 at $b=175$,
0.73 at $b=200$, 0.78 at $b=225$). A random-model heuristic explains the
level (heuristic only, used nowhere in the counts): with $2^N$ directed
candidates and $\max(u_0,u_1)$ behaving like the maximum of two roughly
uniform quantities on $[1, e^{S/2}]$, the extreme value sits near
$\log\max \approx S/2 - \tfrac12 N\log 2$, which for $b=175$ predicts
$\approx 51$ against the observed $45.2$. The F2 survivor *counts*
fluctuate non-monotonically (465 at $b=120$; 16,636 at $b=130$; 763 at
$b=150$; 29,009 at $b=175$) because $\log B_b$ is piecewise constant
over stretches where no new prime-power cap is reached (e.g.
$\log B_b = 44.65$ at both $b=140$ and $b=150$, while $S/2$ grows from
48.5 to 51.0, squeezing F2), then jumps when $z_b$ crosses a new prime
or a cap $e_p$ increments, reopening F2. At $\varepsilon = 1/2$,
$\log B_b > S/2$, the size condition is weaker than the trivial
$u_0 < P_1$, $u_1 < P_0$ for balanced partitions, and F2 passes
31.7 million (94.6%) and 33.1 million (98.6%) candidates at $b=200,225$.

**F3 (smoothness, $u_i \mid B_b$) is the obstruction, and it is total.**
Of 64,899,301 size survivors across all rows, exactly one, at the
smallest $b$ in the range, has both cofactors dividing $B_b$. For every
$b \ge 40$, in both instantiations, the count is exactly zero, including
33,098,231 size survivors at $b=225$ under the weakest smoothness
demand used ($z_b = 83.1$). Section 6 quantifies how far the size
survivors are from smooth at three representative $b$: not within a
$B_b$-rough factor of $e^{10}$ in a single case.

A random-model heuristic (again, explanatory only) matches this
qualitative picture. An integer $u \le B_b$ divides $B_b$ iff it is one
of the $\tau(B_b)$ divisors of $B_b$, so a uniform model gives
$P(u \mid B_b \mid u \le B_b) \approx \tau(B_b)/B_b$: in $\log_{10}$,
$-14.1$ at $b=150$ ($\varepsilon=1/4$: $\tau(B_b) = 184{,}320$,
$\log B_b = 44.7$) and $-28.1$ at $b=200$ ($\varepsilon=1/2$:
$\tau(B_b) = 141{,}557{,}760$, $\log B_b = 83.5$). Requiring both
cofactors to divide $B_b$ squares the probability, giving expected F3
counts of order $10^{-21}$ ($b=150$: $8.4\times10^6$ directed candidates)
to $10^{-48}$ ($b=200$) under the model, against $2^N$ growth of the
candidate count. The size stage loses because its margin is only
polynomial in the candidate count; the smoothness stage wins because
$\log B_b \approx z_b$ grows like $b/\log b$, whereas $\log \tau(B_b)$
is only $5.5$ to $20.1$ (natural log) across the entire table, so
$\tau(B_b)/B_b$ decays roughly like $\exp(-(1-o(1)) z_b)$. At $b=30$ the
model is not applicable (the one survivor's cofactors, 3 and 44, are
tiny compared with $B_{30}$, a small-number effect), which is exactly
where the single F3 survivor occurs.

## 5. The one candidate that reached F5: exact disposition at $b=30$

At $b=30$, $\varepsilon = 1/4$ ($z_b = 11.76$, large primes
$\{13,17,19,23,29\}$), one directed candidate passes F1–F4:

- $S_0 = \{13,17,29\}$, $P_0 = 6409$; $S_1 = \{19,23\}$, $P_1 = 437$;
- $u_0 = 3$, $u_1 = 44$: check $P_1u_1 - P_0u_0 = 437\cdot44 - 6409\cdot3
  = 19228 - 19227 = 1$;
- $c = P_0u_0 = 19227$, $c+1 = P_1u_1 = 19228$;
- $u_0 = 3 \mid B_{30}$ and $u_1 = 44 = 2^2\cdot11 \mid B_{30}$ (caps at
  $b=30$: $2^4, 3^3, 5^2, 7^1, 11^1$), so F3 passes, and
  $c(c+1) = 369{,}696{,}756$ divides $\Lambda_{30}$, verified by exact
  big-integer mod at F4.

F5 then tests every $a \in [1,30]$ exactly: no $a$ has
$\operatorname{den} H([a,30]) = c(c+1)$ with the required residue, so
this $(b,c)$ is **not** an $L=2$ solution, for any $a$. This is
consistent with, and much weaker than, the certified census (no $L=2$
solution at $b=30$ for any $c$ whatsoever, CENSUS0.md). Its value here
is as a pipeline witness: the forced form at small $b$ genuinely
produces consecutive divisors of $\Lambda_b$ of exactly the required
shape, and only the final interval condition kills this one. No other
candidate in the entire run reached F5.

## 6. Smoothness-defect margins

For the representative $\varepsilon = 1/4$ rows $b = 100, 120, 150$,
`redteam_defect.py` re-ran the enumeration and, for every F2 survivor,
computed the $B_b$-rough part of each cofactor (what remains after
dividing out $p^{\min(v_p(u), e_p)}$ for all $p \le z_b$; a cofactor
passes F3 iff its rough part is 1) and the candidate defect
$D = \max(\log\mathrm{rough}(u_0), \log\mathrm{rough}(u_1))$. The
recomputed F2 counts (533, 465, 763) match the checkpoints exactly.

| b | F2 survivors | min defect $D_{\min}$ | # with $D \le 1$ | # with $D \le 2$ | # with $D \le 5$ | # with $D \le 10$ |
|---|---|---|---|---|---|---|
| 100 | 533 | 20.42 | 0 | 0 | 0 | 0 |
| 120 | 465 | 25.91 | 0 | 0 | 0 | 0 |
| 150 | 763 | 33.22 | 0 | 0 | 0 | 0 |

So at $b=150$ even the least defective of all 763 size survivors still
has a cofactor carrying a $B_b$-rough factor of at least $e^{33.2}
\approx 2.9\times10^{14}$ (at least one prime factor $> z_b$, or a
prime power exceeding its $\Lambda_b$ cap, of that combined size).
$D_{\min}$ grows with $b$ (20.4, 25.9, 33.2 at $b = 100, 120, 150$,
roughly $0.22\,b$ over this range): the smoothness margin is widening,
not closing, over the range covered. The minimising records are stored
in `redteam_defect_<b>_0.25.json`.

## 7. Verification of this pipeline

- **Independent re-derivation at small $b$.** `redteam_verify_small.py`
  enumerates *all* directed subsets directly (no Gray code, no
  complement symmetry, no swapped-identity shortcut) and solves
  $P_1u_1 - P_0u_0 = 1$ by an explicit extended-Euclidean algorithm.
  It reproduces the checkpoints exactly at $b = 30, 40, 50$:
  F2 $= 30, 62, 239$; F3 $= 1, 0, 0$; best $\max(u) = 44, 394, 4007$,
  matching in all nine numbers.
- **F3 implementation equivalence.** The $\varepsilon = 1/4$ runs test
  $u \mid B_b$ by trial division with exponent caps; the
  $\varepsilon = 1/2$ runs use $\gcd(u, B_b) = u$ (the trial-division
  version was the bottleneck at 31.7M size survivors; a first
  $\varepsilon = 1/2$ attempt with it was stopped and rerun with the
  gcd test). `redteam_gcd_equiv.py` compares the two tests on 25,416
  values (every size survivor stored in the $\varepsilon=1/4$
  checkpoints, 20,000 random integers, and all divisors of $B_{60}$
  as positive cases): **0 mismatches**.
- **Swapped-direction identity.** The identity
  $A(B-u_0) - B(A-u_1) = 1$ used to avoid a second inversion is asserted
  in exact integers at every evaluated state; no run aborted.
- **MITM count cross-check.** The Section 8 explosion counts were
  computed twice by independent implementations and agree exactly
  (see the correction log in Section 8).
- **Census cross-check (sanity).** `redteam_sanity.py`, a direct exact
  computation sharing no code with the partition pipeline (downward
  `Fraction` accumulation), recomputes all $H([a,b])$, $b \le 200$:
  it finds exactly the four pronic near-misses of CENSUS0.md,
  $(a,b,c) = (4,7,20), (5,7,14), (9,12,44), (154,156,1364)$, and no
  $L=2$ solution, matching the certified census. The partition
  pipeline's own conclusion over its range (no solution, one F5 test,
  failed) is consistent with this.

## 8. Where the enumeration stopped, exactly

Individual Bezout evaluation of partitions was carried to $b = 175$
($\varepsilon = 1/4$, $N = 26$, $2^{25} = 33.5$M unordered states,
614.6 s elapsed for that $b$ under shared load) and to $b = 225$
($\varepsilon = 1/2$, $N = 25$, 480.2 s for that $b$). Beyond that, the
state counts (computed by meet-in-the-middle subset-sum counting in
`redteam_mitm_counts.py`, which counts F1-passing directed partitions
without evaluating them) are:

| (b, eps) | N | directed total | F1-passing directed |
|---|---|---|---|
| (200, 0.25) | 31 | 2,147,483,648 | 2,089,250,414 |
| (250, 0.5) | 29 | 536,870,912 | 536,807,982 |
| (250, 0.25) | 36 | 68,719,476,736 | 67,267,273,682 |
| (300, 0.5) | 35 | 34,359,738,368 | 34,355,723,640 |
| (300, 0.25) | 43 | 8,796,093,022,208 | 8,665,180,368,898 |
| (400, 0.5) | 46 | 70,368,744,177,664 | 70,364,075,685,400 |

*Correction log (this section).* A first version of this table, transcribed
from an ad-hoc preliminary MITM script, had a faulty large-prime list and
was wrong in five of its six rows (it gave, e.g., $N = 38$ at
$(250, 0.25)$ and $N = 46$ at $(300, 0.25)$; the correct values, from
$\pi(250) - \pi(60) = 53 - 17 = 36$ and $\pi(300) - \pi(70) = 62 - 19 =
43$, are 36 and 43). The table above is the corrected one: every entry
was recomputed by `redteam_mitm_counts.py` and independently reproduced
by `redteam_mitm_verify.py`, which generates its primes by trial
division and its subset sums by `itertools.combinations` with `bisect`
counting (the $(400, 0.5)$ row, whose $2^{23}$-element subset arrays are
impractical for the itertools route, was instead reproduced by the
numpy subset generation run over the trial-division prime list). The
two implementations agree exactly on all six rows. The faulty first
version affected only this auxiliary table; no checkpoint, filter
count, or conclusion in Sections 3–6 comes from it.

At the measured throughput ($2^{24}$ unordered states in 371–480 s),
even the cheapest un-run case, (250, 0.5) with $2^{28}$ unordered
states, is a multi-hour single-threaded run, and (200, 0.25) is
$2^{30}$ states. **No Bezout, size, smoothness, or interval claim is
made for any $b > 225$, or for (200, 0.25) / (225, 0.25).** The stop is
a budget stop, not a mathematical one: nothing in the trend suggests
the obstruction weakens (Sections 4 and 6), but the enumeration simply
does not reach further.

## 9. Caveats

1. Theorem 14.2 is asymptotic; "sufficiently large" is nowhere
   quantified in the note. This report instantiates it at two fixed
   $\varepsilon$ values with exact finite analogues of its bounds. A
   solution at some larger $b$ whose cofactors violate the
   $\varepsilon = 1/4$ or $1/2$ instantiations but satisfy the theorem
   for a different fixed $\varepsilon$ is not excluded by this
   computation, and no claim about $b > 225$ is made.
2. Within the instantiations, the enumeration is exhaustive over
   directed partitions: the only pruning (F1) is a proved necessary
   condition for F2 with a guard band exceeding the float error by
   two orders of magnitude, and it was disabled entirely for $N \le 20$.
3. F5 was triggered exactly once in the whole run (Section 5), so the
   "no solution" conclusion over the covered range rests on F3, not on
   the interval test: the construction dies one stage before the actual
   equation is ever consulted, except at $b=30$.
4. The random-model paragraphs in Section 4 are heuristics explaining
   the observed margins; every count and minimum reported is exact.

