# GAPS.md: Cluster F, Cycle 1: the gap map for the general disjoint case

**Revision note, 2026-10-30.** This file was updated at Cycle 1 close
to replace the pending marks with certified outcomes. What changed:
the header status paragraph now gives the final status of Clusters
C1, D and E, citing CENSUS1.md, CLUSTER-D.md and CLUSTER-E.md; the
furthermore paragraph in Section 2 notes that the Theorem 13.3 gap
(D3) is now filled by Cluster D claim D0; Gap G1 is narrowed and its
closing assertion is restated (two singleton regimes closed by
Cluster E, the 13R+ route refuted); Gap G3 is replaced and narrowed
by Cluster D residual R_D, and Gap G2 is sharpened accordingly at
its first instance; Gap G6 records the census frontier certified to
`b <= 20,000`, with the stretch to 100,000 not run; Gap G7 item (ii)
is marked cleared by D0; Section 4 items C2-1, C2-3, C2-4 and C2-7
are updated to the landed state; and the Section 5 summary table
and Bottom line are updated to match. No other gap analysis was
rewritten.

**Role.** This file is a scoping document, not a proof attempt. It restates
the general disjoint problem exactly, restates Nayak's Theorem 17.1 in
campaign notation with an audit status for every clause, lists every
distinct mathematical gap between the certified record and a finiteness
proof as a precise assertion that would close it, and specifies what a
Cycle 2 would need. Precision over completeness: every status label is
traceable to a named file in this workspace, cited at the point of use.

**Sources used.** INFORMATION.md (dossier); AUDIT-A.md (Cluster A
verifier: Theorem 3.2 and Lemma 3.1 certified with located defects);
clusters/A/redteam.md Sections 2.1 and 2.2 (the Cluster A full-note
discrepancy scan of Nayak Sections 1 to 18: the adjudicated whole-note
items used below, namely the `z_b` inconsistency and the justification
gaps in Theorems 7.1, 13.3 and 15.2, Lemma 2.4 and Lemma 2.1);
AUDIT-B.md and TARGET.md (Cluster B: Zeraoulia's machinery certified;
Theorem 13 valid as an implication but vacuous as stated; campaign
repairs 13R and 13R+); CENSUS0.md (certified censuses to `b <= 2000`);
CENSUS1.md (Cluster C1 census extension, EXTENSION CERTIFIED to
`b <= 20,000`); CLUSTER-D.md (Cluster D verifier record for
`L = 2`); CLUSTER-E.md (Cluster E verifier record for the singleton
case); sources/Nayak-2026.txt (the note itself, especially Sections 16, 17
and 18). One traceability caveat, recorded plainly: AUDIT-A.md as it
stands in the workspace certifies Sections 2 to 3 and its defect list
runs through item A-D5; the whole-note items are cited here to
clusters/A/redteam.md, the Cluster A file that records them, rather
than to AUDIT-A.md.

**Final status of the Cycle 1 clusters, at Cycle 1 close
(2026-10-30).** Cluster C1 (census extension) is complete and
verifier-certified in CENSUS1.md: the extension to `b <= 20,000` is
EXTENSION CERTIFIED in both branches. Cluster D (the `L = 2`
frontier) is complete and verifier-certified in CLUSTER-D.md: it
does not close `L = 2`, and its final residual is R_D in
CLUSTER-D.md Section 3. Cluster E (the target lemma in restricted
regimes) is complete and verifier-certified in CLUSTER-E.md: it
closes the singleton regimes (ii) `a > b/2` and (i) fixed `R` (with
qualifications), and it refutes (H-sieve) for every `B_0`. Every
statement below that depends on any of them now cites the certified
outcome from those files.

**Status vocabulary.**
- *Certified*: a cluster verifier certified the statement from its
  statement, with independent exact computation where the statement is
  finite (AUDIT-A.md Sections 1 to 3; AUDIT-B.md Section 1; CENSUS0.md).
- *True with justification gaps*: the statement is believed true on the
  campaign record, a named step in the printed proof is unjustified,
  and the missing justification is on record.
- *Supported as stated (scan level)*: the Cluster A red team's
  line-by-line rederivation of Nayak Sections 4 to 15 found the
  argument correct (clusters/A/redteam.md Section 2.2), but no
  verifier has certified the statement independently in the sense of
  AUDIT-A.md Sections 1 to 2. This is a weaker label than *certified*
  and is used for most of Theorem 17.1, whose constituent theorems lie
  outside AUDIT-A.md's certified scope.
- *Instance-verified only*: exact finite instances were checked and
  passed; the general statement rests on the scan-level label above.
- *Extension certified / Certified with qualifications*: the exact
  verdict wording quoted from CENSUS1.md, CLUSTER-D.md or
  CLUSTER-E.md at the point of use.

---

## 1. The general disjoint problem, restated exactly

For positive integers `u <= v`, write

    H([u,v]) = sum_{n=u}^{v} 1/n,   H(a,b) = H([a,b]).

**Problem (Erdos Problem #288, disjoint case).** Let `[a,b]` and
`[c,d]` be nonempty intervals of positive integers with

    b < c,   H([a,b]) + H([c,d]) in Z.

**Question: is the set of such pairs `([a,b],[c,d])` finite?**

Campaign notation, following sources/Nayak-2026.txt Section 1 and
TARGET.md: `L = d - c + 1` (upper length), `R = b - a + 1` (lower
length), `Lambda_b = lcm(1, 2, ..., b)`, `M_{a,b} = lcm(a, ..., b)`,
`den(x)` the reduced denominator of a rational `x`. The known disjoint
solutions are exactly three, all with `L = 1`:
`([1,3],[6,6])`, `([2,3],[6,6])`, `([3,6],[20,20])` (INFORMATION.md
Section 8; certified as the complete list for `b <= 2000` in
CENSUS0.md, tasks (i) and (ii)).

**What is already settled, so the gap map is about the remainder.**
The intersecting case is closed: if the two intervals intersect and
the sum is an integer, the pair is one of `([1,1],[1,1])`,
`([1,2],[1,2])`, `([1,2],[2,2])`, `([2,2],[2,2])` (Nayak Theorem 3.2,
CERTIFIED WITH LOCATED DEFECTS, AUDIT-A.md Section 1; the defects are
wording and exposition only). So a full solution of #288 is exactly a
finiteness proof for the disjoint case above.

**Trivial reductions, stated because they organise the gaps.**

1. *The singleton case is a sub-problem.* Setting `L = 1` gives
   `H(a,b) + 1/m in Z` with `m = d > b`. A finiteness proof for the
   general disjoint problem settles the singleton case, and the
   singleton case is itself open: Erdős and Graham record that they
   could not show even this case is finite (INFORMATION.md Section 1).
   Conversely the singleton case has its own complete reduction
   (Section 3, Gap G1 below), so it is a genuine first gap, not a
   corollary waiting on the general case.
2. *Each fixed `L` is a sub-problem.* The solution set is the disjoint
   union over `L >= 1` of the solution sets with upper length `L`. A
   full solution must settle the singleton case (`L = 1`) and each
   fixed `L >= 2`, and must in addition control the regime where `L`
   grows with `b` (Gap G4): finiteness for each fixed `L` separately,
   with a threshold `B_0(L)` allowed to depend on `L`, does not by
   itself imply finiteness of the union.
3. *Fixed `b` is finite.* For fixed `b`, every disjoint solution has
   `c < b * Lambda_b` (Nayak Corollary 4.3; supported as stated, scan
   level). Finiteness is therefore purely an asymptotic question as
   `b` grows: an infinite solution set contains solutions with
   `b -> infinity`, and every obstruction below is stated for such an
   infinite family.

---

## 2. Nayak's Theorem 17.1 in campaign notation, clause by clause

**Statement (sources/Nayak-2026.txt, Theorem 17.1).** Let `[a,b]` and
`[c,d]` be a *sufficiently large* disjoint solution, `b < c`, with
`L`, `R`, `Lambda_b` as above. Then clauses (1) to (11) below hold,
and if in addition `L >= 2` is *fixed*, the CRT-smoothness package in
the "furthermore" paragraph holds. Two global caveats precede the
clauses. First, "sufficiently large" is nowhere quantified in the
note: no explicit threshold `B_0` is given for any clause, which
matters for Gap G6. Second, the audit status of the whole theorem at
scan level is: each of items (1) to (11) was checked against the
result it cites and "every item is supported as stated; the only
wrinkle is the `z_b` form in item (7) versus the furthermore
paragraph" (clusters/A/redteam.md Section 2.2). No clause of
Theorem 17.1 is *certified* in the AUDIT-A.md sense; the per-clause
labels below give the strongest label the record supports for each.

**(1) Length bound and sublinearity.** `L < b`, and `L = o(b)` in
every infinite disjoint family (Theorems 4.1 and 7.1).
*Status: true with a justification gap.* Theorem 4.1 was rederived
clean at scan level. Theorem 7.1's proof has gap D4(a) of
clusters/A/redteam.md Section 2.1: at txt line 427, "the lowest
p-adic layer must cancel against the lower interval" treats the
upper denominator's `p`-exponent as 1 without splitting off the case
of exponent at least 2; the missing sentence (if `p^2 > b` then an
upper exponent at least 2 would already give a unique lowest layer)
is fillable and on record. The clause is also consistent with the
certified census range (CENSUS0.md).

**(2) Upper divisor block.** Every upper denominator divides
`Lambda_b`: `n | Lambda_b` for `c <= n <= d` (Theorem 4.2, via the
denominator equality `den H([c,d]) = den H([a,b])` of Lemma 2.3).
*Status: supported as stated (scan level); instance-verified* on the
three known disjoint solutions (Theorems 4.2, 6.1, 10.1 instances all
hold, clusters/A/redteam.md Section 2.2).

**(3) Maximal prime-power mirror congruences.** For every prime `p`
with maximal power `Q = p^e <= b < p^{e+1}` and `Q > L`, writing
`R_p = sum (n/Q)^{-1} (mod p)` over the multiples `n` of `Q` in
`[a,b]` (inverses in `F_p`): (i) if `R_p = 0 (mod p)`, the upper
interval contains no multiple of `Q`; (ii) if `R_p != 0 (mod p)`, the
upper interval contains exactly one multiple `m_p = Q * t_p`, and
`t_p = -R_p^{-1} (mod p)`, equivalently
`m_p = -Q * R_p^{-1} (mod pQ)` (Theorem 5.1).
*Status: supported as stated (scan level); instance-verified* in the
strongest available form: all 7 prime instances with `Q > L` across
the three known disjoint solutions satisfy the dichotomy and, in
case (ii), the congruence, including a genuine case (i) instance
(`([3,6],[20,20])` at `p = 3`, clusters/A/redteam.md Section 2.2).

**(4) Binomial divisibilities.** `C(d, L) | Lambda_b` and
`C(d, L) | lcm(M_{a,b}, Lambda_L)` (Theorems 6.1 and 6.2, both via
Lemma 2.4: `C(d, L) | lcm(c, ..., d)`). Consequences on record:
`d <= L * Lambda_b^{1/L} <= L * 4^{b/L}`.
*Status: true with a justification gap.* Lemma 2.4's proof has gap
D4(b) of clusters/A/redteam.md Section 2.1: at txt line 162 the
vanishing of the summand `A_j - floor(L / p^j)` when `j > v_p(M)`
also needs `floor(L / p^j) = 0`, which is true but not stated.
Lemma 2.4 itself is *instance-verified* exhaustively in range:
`C(d, L) | lcm(c..d)` for all 45,150 pairs `1 <= c <= d <= 300`, zero
failures (clusters/A/redteam.md Section 2.2). Theorems 6.1 and 6.2
were rederived clean at scan level, and Theorem 6.1's instances on
the known solutions hold.

**(5) Denominator lower bound.**
`den H([c,d]) >= (1 / Lambda_L) * C(d, L)` (Theorem 10.1).
Equivalently `C(d, L) <= Lambda_L * den H([c,d])`: cancellation
inside the upper block can remove only the `Lambda_L` part of its
lcm.
*Status: supported as stated (scan level); instance-verified* with
equality on all three known disjoint solutions (upper denominators
6, 6, 20 against bounds 6, 6, 20; clusters/A/redteam.md Section 2.2).

**(6) Large-prime product condition.** For every fixed `theta > 0`,
in every sufficiently large disjoint solution, every prime
`theta * b < p <= b` divides some upper denominator:
`prod_{theta*b < p <= b} p | prod_{n=c}^{d} n` (Theorem 9.1).
Consequence: `L log d >= (1 - o(1)) b` (Corollary 9.2).
*Status: supported as stated (scan level).* The statement is
asymptotic ("sufficiently large", threshold unquantified), so it
admits no finite instance check; Theorem 9.1 was rederived clean in
the scan (clusters/A/redteam.md Section 2.2).

**(7) Fixed-length CRT-smoothness package, first half: forcing down
to the logarithmic scale.** For every fixed `eps in (0,1)`, with

    z_b = max( L, b / ((1 - eps) log b) ),

every sufficiently large disjoint solution satisfies
`prod_{z_b < p <= b} p | prod_{n=c}^{d} n` (Theorem 12.1).
Consequence: `L log d >= theta(b) - theta(z_b)` (Corollary 12.2,
clause (8) of the note).
*Status: true with a wording defect.* This is adjudicated item D1 of
clusters/A/redteam.md Section 2.1: the note defines `z_b` in
Section 12 (Theorem 12.1) with the `max(L, .)` form quoted above,
then *redefines* the same symbol in Section 13 without the
`max(L, .)`, and Sections 13, 14 and Problem 18.1 use the second
form, while Theorem 17.1 item (7) states the forcing with the first
form. The defect is harmless where the package is actually used
(for fixed `L`, `b / ((1 - eps) log b)` eventually exceeds `L`, so
the two forms coincide for large `b`), but as printed the definition
is inconsistent, and the two forms diverge materially exactly in
the growing-`L` regime of Gap G4, where `L` can exceed
`b / ((1 - eps) log b)`. Theorem 12.1 itself was rederived clean at
scan level.

**Furthermore paragraph (fixed `L >= 2`): the CRT-smoothness
package, second half.** For fixed `L >= 2` and fixed `eps in (0,1)`,
with `z_b` in the Section 13 form `b / ((1 - eps) log b)`, the
primes in `(z_b, b]` are partitioned among sets `S_0, ..., S_{L-1}`,
and writing `P_j = prod_{p in S_j} p`, every sufficiently large
solution has

    c + j = P_j * u_j   (0 <= j < L),
    log P_j = b/L + o(b),
    log u_j <= (1 + o(1)) * b / ((1 - eps) log b),   so u_j = P_j^{o(1)},

where each `u_j` is a `z_b`-smooth divisor of `Lambda_b` (precisely,
`u_j | B_b(z_b)`, the `z_b`-smooth part of `Lambda_b`), and each
`u_j` is the *unique* integer with `0 < u_j < P_j` satisfying the
forced mirror congruences `u_j * (P_j / p) = -R_p^{-1} (mod p)` for
all `p in S_j`, that is, `u_j` lies in one prescribed CRT residue
class modulo `P_j = exp(b/L + o(b))` (Theorems 13.3, 13.4, 13.5).
*Status: true with a justification gap.* Adjudicated item D3 of
clusters/A/redteam.md Section 2.1: Theorem 13.3's proof asserts "all
prime factors of `u_j` are at most `z_b`" citing only
`u_j | Lambda_b` (Theorem 4.2), which does not by itself bound the
prime factors; the missing two-line argument (a prime
`q in (z_b, b]` dividing `u_j` would lie in `S_j` and give
`q^2 | c + j`, contradicting `c + j | Lambda_b` since `q^2 > b`)
is on record, and the assertion is true. Theorems 13.3, 13.5 and
the `L = 2` specialisation Theorem 14.2 all rest on this step.
Theorem 13.4 was rederived clean at scan level. (Update at Cycle 1
close: that D3 gap is now filled. In CLUSTER-D.md, claim D0 is
CERTIFIED, and CLUSTER-D.md records: "Status of the Theorem 13.3
gap after D0: CLOSED." The step flagged as AUDIT-A.md item A-W2,
and as item D3 in repair debt G7 below, is now supplied with a
complete proof, so G7 item (ii) is cleared for that step.)

**Remaining clauses of the note's Theorem 17.1, for completeness.**
(8) `L log d >= theta(b) - theta(z_b)`: corollary of (7), same
status. (9) If `L = o(b / log b)` then `log d ~ b / L` (Theorem 9.3,
height pinning): *supported as stated (scan level)*. (10) If
`R <= eta * b` for fixed `eta in (0,1)` then `d >= eta^2 b^2`
(Theorem 11.1): *supported as stated (scan level)*. (11) For fixed
`L >= 2`, no sufficiently large solution has `R <= 2L - 1`
(Theorem 11.3): *supported as stated (scan level)*.
Two shared tools carry their own recorded items, neither affecting
any application: Lemma 2.1's "more precisely" clause is stated for
any unique minimum but its proof covers only a negative minimum
(item D5, clusters/A/redteam.md Section 2.1; every application in
the note has a negative minimum); and Theorem 15.2's endpoint
pinning (not itself a clause of Theorem 17.1) uses an ansatz whose
boundedness is not established, item D6, with the final constant
independently rederived and correct.

**Net audit position on Theorem 17.1.** Every clause is supported as
stated at scan level; clauses (1), (4), (7) and the furthermore
paragraph carry the named, fillable defects D4(a), D4(b), D1 and D3
respectively; no clause is verifier-certified, and no clause is
known to be false. The theorem is a *necessary-condition package*:
it constrains any sufficiently large solution but excludes none.
That is the starting point of the gap list.

---

## 3. The gap list

Each gap is stated as: the precise assertion whose proof would close
it; what is known; a difficulty note. Gaps G1 to G5 are the distinct
mathematical obstructions. Gap G6 is the effectivity gap that would
remain even if G1 to G5 were closed non-effectively in the wrong
quantifier order. Gap G7 collects the repair debt in the existing
record, which is not an obstruction but must be cleared before any
of G1 to G5 can be built on safely.

### G1. The singleton case (`L = 1`) is narrowed: two regimes closed, the general case remains open

**Closing assertion, restated at Cycle 1 close.** 13R+ no longer
serves as the closing route. Cluster E refuted (H-sieve) for every
`B_0` (see below), so the hypotheses of TARGET.md repairs 13R and
13R+ are unsatisfiable, and a Cycle 2 singleton closure outside the
regimes Cluster E closed needs a different mechanism outside the
forced class. The original campaign form is recorded here for
traceability only. Theorem 13R+:
there exists `B_0` such that (H-sieve) for every `b >= B_0` and
every `1 <= a <= b` with `P1(a,b)` nonempty, the forced CRT class
`m = r(a,b) (mod Q(a,b))` contains no `b`-smooth positive integer
`m <= L(a,b)`; and (H-blind) there is no singleton solution
`(a, b, m)` with `P1(a,b)` empty and `b >= B_0`. Here `P1(a,b)`,
`Q(a,b)`, `r(a,b)`, `L(a,b)` are as in TARGET.md (good primes are
the odd primes `p` with `p^2 > b`, at least one multiple in
`[a,b]`, and `T_p != 0 (mod p)`). Given 13R+, finiteness of the
singleton case follows by the certified machinery (AUDIT-B.md:
Lemmas 1 and 2 and the CRT reduction are CERTIFIED; TARGET.md gives
the proof of 13R+ from its hypotheses). By the remark in TARGET.md,
(H-sieve) may be weakened to its single-candidate form: for all
large `b` and all `a` with `P1(a,b)` nonempty, the forced candidate
`B(a,b) = den H(a,b)` does not itself lie in the class
`r(a,b) (mod Q(a,b))`.

**What is known.**
- Zeraoulia's original Theorem 13, which quantifies (H-sieve) over
  *all* `a`, is valid as an implication but its hypothesis is
  *unsatisfiable as stated*, hence vacuous and NOT CERTIFIED as a
  usable target (AUDIT-B.md Section 2): at `(a,b) = (q^2, q^2)` for
  any prime `q`, `P1` is empty, `Q = 1`, the class is all integers,
  and `m = q^2` is `b`-smooth with `m = L(a,b)`. The repair *must*
  restrict the `(a,b)` quantifier; weakening the condition on `m`
  does not repair it (AUDIT-B.md Section 2, point (i)).
- (H-sieve) already *fails pointwise* in the computed range: the
  exclusion fails at 83 intervals with `P1` nonempty and
  `b <= 300`, namely the 3 solution intervals with `Q > 1` and 80
  non-solution intervals, among them the family
  `(2^k, 2^k + 1)` for `k = 2, 4, 5, 6, 7, 8` (TARGET.md Remark 4;
  clusters/B/verifier_target_output.txt). The single-candidate
  weakening fails at the same 80 non-solution intervals. At Cycle 1
  close this status is superseded: in CLUSTER-E.md, claim C4 is
  CERTIFIED WITH QUALIFICATIONS, and its certified statement S3
  states that (H-sieve) is false for every `B_0`. The refuting
  family is the Theorem F family: for each prime `P = 1 (mod 4)`,
  the interval `(n_P^2, n_P^2 + 1)`, where `n_P^2 = -1 (mod P)`.
  Hence TARGET.md repairs 13R and 13R+ have unsatisfiable
  hypotheses. (H-sieve) is no longer an open asymptotic statement.
- The uniformity in `a` is the content. For `a <= floor(b/2) + 1`,
  Proposition 10 (CERTIFIED WITH DEFECT D2 of AUDIT-B.md: its
  displayed theta bound is false at `b = 2, 3` only; the goodness
  claim and asymptotics are unaffected) puts every odd prime in
  `(b/2, b]` in `P1(a,b)`, so `log Q(a,b) >= (1 + o(1)) b` there.
  The modulus is therefore at least on the scale of the search
  range `L(a,b)`, and AUDIT-B.md item D6 records that the note
  *understates* the maximal size: `log Q` can reach
  `(2 + o(1)) b` (measured maximum `log Q / b = 1.8448` over
  `b <= 300`), i.e. `Q` up to about `x^{2 + o(1)}` for
  `x = lcm(1..b)`. A bare comparison `Q > L(a,b)` would not suffice
  in any case (Remark 14, CERTIFIED: witness `(a,b) = (2,3)`,
  `Q = 9 > L = 6`, least residue `r_0 = 6`, an actual solution).
  What would suffice is `r_0(a,b) > L(a,b)` or `r_0(a,b)` not
  `b`-smooth, uniformly in `a` (TARGET.md Remark 3).
- The sieve-blind regime (H-blind) has forced structure but no
  argument: for `b >= 4`, `P1(a,b)` empty forces
  `a > floor(b/2) + 1` (else Proposition 10 supplies a good prime),
  and forces every odd prime `p` with `p^2 > b` and a multiple in
  `[a,b]` to be bad, in particular there is no such prime with
  exactly one multiple in `[a,b]` (a single multiple always gives
  `T_p = 1/u != 0`) (TARGET.md Remark 1). Closing (H-blind) needs
  an idea outside the note's sieve: the prime 2 and the primes with
  `p^2 <= b` that the sieve discards, or a short-interval argument
  for `a > b/2`. At Cycle 1 close, (H-blind) remains open as a
  statement, but it is moot as a component of 13R+, whose other
  conjunct (H-sieve) is refuted (CLUSTER-E.md Section 5). Cluster E
  did close the regime `a > b/2` completely, by a non-sieve
  argument (see the Cluster E bullet below), which is a separate
  result from (H-blind) itself.
- In Nayak's frame the same gap appears as Section 16 of the note:
  disjoint singleton solutions are exactly the lower intervals with
  reduced denominator `D > b` and `A = -1 (mod D)`, and height
  pinning gives `log D ~ b` for `L = 1`, so a large singleton
  solution requires `H([a,b])` to be exponentially (in `b`) close
  to an integer. The three known examples are the complete list
  for `b <= 2000` (CENSUS0.md, CERTIFIED), and the census
  extension to `b <= 20,000` is EXTENSION CERTIFIED in both
  branches in CENSUS1.md: the singletons are exactly the six known,
  with none new in `(2000, 20000]`.
- Cluster E closed two singleton regimes by direct arguments in
  CLUSTER-E.md, not via 13R+. This is a prize-tier result.
  Regime (ii), `a > b/2`, is CLOSED completely: in CLUSTER-E.md,
  claims C1 and C2 are both CERTIFIED, by two independent certified
  routes, and the certified statement S1 is that the singleton
  solutions with `a > b/2` are exactly `(1,1,1)`, `(2,2,2)`,
  `(2,3,6)`. Regime (i), fixed `R`, is CERTIFIED WITH
  QUALIFICATIONS (claim C3): per fixed `R` any solution has
  `a <= 2R`, so finiteness holds per fixed `R`; classification is
  complete only for `R <= 100` via the census, and for `R > 100`
  the finite check is specified, not run. (H-sieve) is REFUTED for
  every `B_0` by the Theorem F family above, so 13R and 13R+ have
  unsatisfiable hypotheses, and (H-blind) remains open as a
  statement but is moot as a component of 13R+. Consequence: G1
  remains open outside those two regimes, namely `a <= b/2` with
  `R` growing, and the general uniform statement.

**Difficulty.** Very hard, and the barrier is quantified rather
than rhetorical. Smooth numbers in arithmetic progressions are
controlled in the literature the note cites only for moduli
`q <= x^{66/107}` (Pascadi 2023, per Zeraoulia Section 8; the
AUDIT-B.md verifier did *not* verify the note's Section 8
literature claims, and no audited item depends on them), while
here `Q` is on the scale `x^{1 + o(1)}` to `x^{2 + o(1)}`: a
"modulus as large as the search range" obstruction. The note's
Section 8 names the three conceivable routes: a new global
inequality lower-bounding the least residue or obstructing
smoothness in the class; smooth-AP results reaching
`q ~ x^{1 - o(1)}` or exploiting the special structure of
`r(a,b)`; or distance-to-integer lower bounds for `H(a,b)` of the
form "the distance from `H(a,b)` to the nearest integer exceeds
`exp(-(1 - eps) b)` for all large intervals in the sieve regime",
which would contradict the required closeness `1/D` with
`log D ~ b`. None of the three routes currently exists.

### G2. For each fixed `L >= 2`, the CRT-smoothness package is necessary, not excluding

**Closing assertion (per fixed `L >= 2`).** There exists
`B_0(L)` such that for no `b >= B_0(L)` does there exist a
partition of the primes in `(z_b, b]` into `L` parts
`S_0, ..., S_{L-1}` with products `P_j`, and `z_b`-smooth integers
`u_j | B_b(z_b)` with `log u_j <= (1 + o(1)) b / ((1 - eps) log b)`,
such that the `u_j` satisfy the forced mirror CRT systems of
Theorem 13.5 modulo `P_j` *and* the numbers `c + j = P_j u_j` are
consecutive. (Given Theorem 13.5, scan level with gap D3 repaired
by Cluster D claim D0, CERTIFIED in CLUSTER-D.md,
this non-existence statement is exactly the exclusion of all
sufficiently large solutions of upper length `L`.)

**What is known.** The full necessary package is on record:
Theorem 17.1 clauses (1) to (11) and the furthermore paragraph
(Section 2 above), including height pinning `log d ~ b / L` when
`L = o(b / log b)` and the denominator saturation
`log den H([a,b]) = b + o(b)` for fixed `L` (Corollary 10.3 of the
note). What is missing is any mechanism that converts "each `u_j`
is a very small smooth number in one prescribed residue class
modulo `exp(b/L + o(b))`" into a contradiction. The modulus `P_j`
is exponentially larger than the candidate `u_j` itself
(`u_j = P_j^{o(1)}`), so this is the same modulus-versus-range
barrier as G1 in a second form: a smooth number in a prescribed
class modulo `P_j`, where the class is determined by data (the
residues `R_p`) that itself depends on the unknown lower interval.
Two partial exclusions exist at the edges and show the shape of
what is missing: no sufficiently large solution with fixed `L`
has `R <= 2L - 1` (Theorem 11.3), and for `L = 2` none has
`R <= 4` (Theorem 14.5); both argue through the height barrier
`d >= (1 - o(1)) b^2` against denominator equality, and neither
touches `R` proportional to `b`, which Theorem 15.1 of the note
shows is the regime any infinite family must actually live in
(`a <= (1 + o(1)) b / e`, so `R >= (1 - 1/e - o(1)) b`).

**Difficulty.** Very hard. For each fixed `L` this is a
smooth-numbers-in-arithmetic-progressions problem with modulus
exponentially larger than the smooth candidates, compounded by
the consecutiveness coupling between the `L` classes. No result
in either note, and no result cited in either note, reaches it.
Cluster E's restricted regimes are singleton regimes and do not
bear on this gap. At Cycle 1 close, G2's first instance (`L = 2`)
is sharpened by Cluster D residual R_D (see G3), not closed; for
`L > 2` nothing in Cluster D or Cluster E changes this gap.

### G3. The case `L = 2` (first non-singleton case) is open

**Closing assertion.** Nayak's Problem 18.1 (sources/Nayak-2026.txt
Section 18): show that no partition of the primes in
`(b / ((1 - eps) log b), b]` into two parts can produce coprime
products `P_0, P_1 = exp(b/2 + o(b))` whose mutual modular inverses
are both `b / log b`-smooth divisors of `Lambda_b` of size
`exp(O(b / log b))`, while also satisfying the top-half square
congruences and the denominator identity
`den H([a,b]) = c(c + 1)`. Equivalently: there is no sufficiently
large disjoint solution with `L = 2`.

**What is known.** This is the most rigid special case on record.
Theorem 14.1 gives the exact denominator
`den H([c, c+1]) = c(c + 1)` (instance-verified for all
`c <= 2000`, zero failures; clusters/A/redteam.md Section 2.2), so
a solution forces `den H([a,b]) = c(c + 1)` and
`c(c + 1) | Lambda_b`. Theorem 14.2 (resting on Theorem 13.3, gap
D3 above, now filled by Cluster D claim D0, CERTIFIED in
CLUSTER-D.md) forces `c = P_0 u_0`, `c + 1 = P_1 u_1` with `S_0, S_1`
partitioning the primes in `(z_b, b]`,
`log P_0 = log P_1 = b/2 + o(b)`,
`u_0, u_1 <= exp((1 + o(1)) b / ((1 - eps) log b))`, and
`P_1 u_1 - P_0 u_0 = 1` with `P_0 u_0 = -1 (mod P_1)`,
`P_1 u_1 = 1 (mod P_0)` (the note's phrase "mutual modular
inverses" for `u_0, u_1` is item D7 of the red team scan:
terminology only, the displayed congruences are correct).
Theorem 14.3 adds the square-level congruences: for `p > b/2`,
`c = -p (mod p^2)` if `p | c`, and `c + 1 = -p (mod p^2)` if
`p | c + 1`. Theorem 14.4 adds the reciprocal identity and the
lower bound `v_i >= (1 - o(1)) (log b) / (log 2)` on the cofactors
over the top-half primes. The forum compression of sammausberg
(INFORMATION.md Section 8) restates the target as ruling out
`Y^2 = 1 + 4 P W` with `W = u_0 u_1` smooth and small and
`log P = b + o(b)`. Finitely, there is no `L = 2` solution for
`b <= 2000` (CENSUS0.md task (iii), CERTIFIED), and the complete
list of denominator near-misses in that range is exactly four
intervals, `(4,7)`, `(5,7)`, `(9,12)`, `(154,156)`, each with
`den H([a,b])` pronic and each failing the numerator congruence
(CENSUS0.md Section 3). The census extension in CENSUS1.md is
EXTENSION CERTIFIED for the `L = 2` branch to `b <= 20,000` as
well: the branch is empty, and the near-miss list is unchanged,
exactly the four intervals only, none with `b > 2000`. No
sufficiently large solution has `R <= 4` (Theorem 14.5).

**Status of the attack, at Cycle 1 close.** Cluster D is complete
in CLUSTER-D.md, and `L = 2` is NOT closed. G3 remains OPEN, but
it is now replaced and narrowed by the final residual R_D in
CLUSTER-D.md Section 3. Its certified components are as follows.
D0 is CERTIFIED: it fills the Nayak Theorem 13.3 justification gap
(AUDIT-A.md item A-W2, GAPS item D3), so repair debt G7 item (ii)
is CLOSED for that step. D1 is CERTIFIED WITH QUALIFICATIONS: the
new constraint `log(u_0 u_1) >= (2 - o(1)) sqrt(b)`, the first
bound on `u_0 u_1` itself. D2 is CERTIFIED: the prime-square
mechanism is saturated at `(2 + o(1)) sqrt(b)`, and the residual
slack must come from first-power primes in `(sqrt(b), z_b]`. The
quadratic route is CERTIFIED as exhausted: `Y^2 = 1 + 4 P W` is a
tautology equivalent to `P_1 u_1 - P_0 u_0 = 1`, the splitting is
idempotent, and there is no modulo or reciprocity bite within the
forms examined. The red team examined 165,522,272 directed
candidates, with exactly one F3 survivor (`b = 30`, `c = 19227`)
failing the exact test; no claim is made beyond `b = 225`. The
final residual R_D, in CLUSTER-D.md Section 3, names the extra
inputs a closure would need: E1 (mirror residues, Theorems 14.3
and 14.4 mod-`p^2`), E2 (the numerator congruence
`A + 2c + 1 = 0 (mod c(c + 1))` asymptotically), and E3 (an
effective S-unit obstruction uniform in growing support).

**Difficulty.** Hard, but the most concrete target in the whole
problem: one equation `P_1 u_1 - P_0 u_0 = 1` with both products
pinned at `exp(b/2 + o(b))`, both cofactors smooth and
`P_i^{o(1)}`, plus square-level congruences at every top-half
prime. It is the natural Cycle 2 prize (Section 4).

### G4. The growing-`L` regime: `L -> infinity` with `L = o(b)` is untouched

**Closing assertion.** There exist a function `L_0(b) -> infinity`
and a threshold `B_0` such that the fixed-`L` exclusion of G2
holds *uniformly* for all `2 <= L <= L_0(b)` and all `b >= B_0`,
together with an exclusion for the complementary range
`L_0(b) < L = o(b)`. (Clause (1) of Theorem 17.1 already confines
any infinite family to `L = o(b)`, so these two ranges exhaust the
non-singleton problem apart from G1.)

**What is known.** Almost nothing in this regime. The entire
CRT-smoothness package (Theorems 13.3, 13.5, 14.2) is proved for
*fixed* `L`: the estimates `log P_j = b/L + o(b)` and
`log u_j = O(b / log b)` are compared as `b -> infinity` with `L`
constant, and the comparison collapses when `L` grows (for
`L` near `b / log b`, `b / L` and `b / log b` are the same order,
so `u_j = P_j^{o(1)}` fails). Height pinning `log d ~ b / L`
requires the stronger hypothesis `L = o(b / log b)`
(Theorem 9.3); for `b / log b <= L = o(b)` the record gives only
the two-sided squeeze of Corollary 9.2 (`L log d >= (1 - o(1)) b`)
and Theorem 6.1 (`log d <= (b log 4 + L log L) / L`, roughly).
The `z_b` defect D1 is material here and only here: with the
Section 12 form `z_b = max(L, b / ((1 - eps) log b))`, the forcing
range `(z_b, b]` shrinks as `L` grows and is empty of content once
`L` approaches `b`; the Section 13 form silently assumes `L`
below the logarithmic scale. Even the counting changes character:
with `L` parts, the partition is of roughly `b / log b` large
primes into `L` sets, and no analogue of the "each part carries
`b / L + o(b)` of log-mass" balance has been proved uniformly.

**Difficulty.** The structurally hardest gap after G5, because it
is not one problem but a continuum of regimes interpolating
between the fixed-`L` CRT problem (G2) and Tao's configuration
(G5), and because the quantifier order blocks the cheap route:
proving G2 for each fixed `L` with `B_0(L)` growing arbitrarily
fast leaves G4 entirely open. Any Cycle 2 work here first needs a
uniform-in-`L` restatement of Theorems 12.1 and 13.3 with explicit
error terms, which does not currently exist (see G6).

### G5. Tao's configuration: the expected hard case has no excluding obstruction

**Configuration (Tao, forum comment of 2 Feb 2026, as transcribed
in INFORMATION.md Sections 4 and 8).** A dyadic-type lower interval
`I_1 = [alpha M, M]` together with a very short upper interval
`I_2 = [N - h, N]` at a scale `N` much larger than `M`, "perhaps
even exponentially larger", with many primes of `I_1` likely forced
to divide elements of `I_2`. In campaign notation: `b = M`,
`R` proportional to `b` (consistent with, and in fact forced by,
Theorem 15.1: any infinite family has `a <= (1 + o(1)) b / e`),
`L = h + 1` fixed or slowly growing, and `d = N`.

**Why no current obstruction excludes it.** Every clause of
Theorem 17.1 is *compatible* with this configuration, and several
clauses actively predict its shape. Clause (2) forces each of the
`L` consecutive integers near `N` to divide `Lambda_b`: they must
be `b`-smooth numbers at height `N`. Clause (7) forces every prime
in `(z_b, b]` to divide one of those `L` numbers, so the `L`
numbers must collectively absorb all large primes up to `b`, each
to the first power only (a prime `p > z_b` has `p^2 > b`, so it
occurs in `Lambda_b`, hence in any divisor, to the first power):
this is exactly Tao's "heavy prime sharing between the intervals".
Height pinning (clause (9)) applies because `L` is short:
`log N ~ b / L`, so the exponential separation `N` versus `M = b`
is not an extra assumption but a *consequence* the obstructions
already force. Clause (5) is also compatible: it requires
`den H([c,d]) >= C(d, L) / Lambda_L`, of size roughly
`exp((1 - o(1)) b)` by height pinning, while denominator equality
allows anything up to `den H([a,b]) | Lambda_b` with
`log Lambda_b = b + o(b)`; Corollary 10.3 shows the two sides must
in fact saturate (`log den H([a,b]) = b + o(b)`), which is a tight
fit, not a contradiction. The mirror congruences (clause (3)) and,
for `L = 2`, the square congruences (Theorem 14.3) constrain the
configuration prime by prime but are local conditions with no
proved global incompatibility.

**Closing assertion.** Any one of the following would close this
gap for short `L` (and is, at present, a research problem, not a
lemma): (a) a counting theorem showing that for large `b` there do
not exist `L` consecutive divisors of `Lambda_b` at height
`exp((1 + o(1)) b / L)` whose product is divisible by every prime
in `(z_b, b]`; (b) a global incompatibility between the mirror
congruences of clause (3) summed over all maximal prime powers
`Q <= b`, for instance a size or character-sum estimate on the
system `t_p = -R_p^{-1} (mod p)` as `p` ranges over `(b/2, b]`;
(c) for `L = 2`, Problem 18.1 (which is G3, the special case of
this configuration with `h = 1`).

**Difficulty.** This is the configuration Tao's comment identifies
as the expected hard case, and the design of Cycle 1
(CYCLE1_DESIGN.md) scoped it rather than attacking it. It
concentrates the whole difficulty of G1 and G2 into one family:
`L` smooth numbers at exponential height, rigidly partitioned
large-prime content, and a lower interval whose denominator must
saturate `Lambda_b`. A Cycle 2 should treat any claimed progress
here with an extra red-team pass before reporting it.

### G6. Effectivity and stitching: the record's thresholds are unquantified

**Closing assertion.** Explicit thresholds for the combined
obstruction package: a computable `B_0` such that every clause of
Theorem 17.1 used in an exclusion argument holds for all
`b >= B_0`, with the dependence of each threshold on the
parameters (`theta`, `eps`, `eta`, and `L` where applicable) made
explicit.

**What is known.** Every asymptotic clause of Theorem 17.1 is
stated for "sufficiently large" solutions with no bound extracted:
Theorems 7.1, 9.1, 9.3, 11.1, 11.3, 12.1, 13.3, 13.5, 14.2 all have
this form. The certified finite record reaches `b <= 2000`
(CENSUS0.md: singleton branch, disjoint classification, and the
`L = 2` branch, all CERTIFIED). The extension to `b <= 20,000`
is EXTENSION CERTIFIED in CENSUS1.md, in both branches:
singletons are exactly the six known, with none new in
`(2000, 20000]`, and the `L = 2` branch is empty, with the
near-miss list unchanged (exactly the four intervals only). The
stretch to 100,000 was NOT run, by coordinator decision:
Implementation A needs a memory adaptation of about 909 MB, and
Implementation B projects 51+ hours, and the 20,000 result already
satisfies the design's tenfold criterion. The stitching consequence is exact: even if a future
argument excludes all solutions with `b >= B_0` for some
*ineffective* `B_0`, the classification of the remaining finite
range is only as good as the census, and conversely no census
extension, however large, substitutes for the missing `B_0`.
Finiteness (as opposed to classification) needs only an
ineffective `B_0`, so G6 is subordinate to G1 to G5; it is listed
because the campaign's standard (only verifier-certified files
count, CYCLE1_DESIGN.md) makes the unquantified thresholds a real
defect of the present record, and because G4 cannot even be
*stated* uniformly until the `L`-dependence of the thresholds in
Theorems 12.1 and 13.3 is extracted.

**Difficulty.** Mechanical but laborious for the clauses that
rest on the prime number theorem in the form
`theta(x) = x + o(x)` (explicit bounds for `theta` exist in the
literature and would have to be imported and checked); genuinely
blocked wherever it depends on G2 or G4.

### G7. Repair debt in the existing record (not an obstruction)

The following located defects sit underneath the clauses used
above. Each has its fix on record; none is known to affect any
conclusion; all should be cleared in any Cycle 2 restatement so
that later work does not inherit them. (i) The `z_b` inconsistency,
item D1 of clusters/A/redteam.md (clause (7) above). (ii) CLEARED
by Cluster D claim D0, CERTIFIED in CLUSTER-D.md: the formerly
unjustified step "all prime factors of `u_j` are at most `z_b`" in
Theorem 13.3, item D3 (furthermore paragraph above), is now
proved, so this item is closed for that step; Theorems
13.5 and 14.2 rested on it. (iii) The two one-line valuation gaps,
item D4: Theorem 7.1's unsplit exponent case (clause (1)) and
Lemma 2.4's unstated `floor(L / p^j) = 0` (clause (4)). (iv)
Lemma 2.1's proof covering only the negative-minimum case its
applications need, item D5. (v) Theorem 15.2's unproved
boundedness of the ansatz coefficient, item D6 (peripheral; the
constant was independently rederived). (vi) On the Zeraoulia side:
Proposition 10's theta bound false at `b = 2, 3`, AUDIT-B.md item
D2 (repair: add `b >= 4`, or sum over odd primes, or subtract
`O(1)`); the misprint `H(3,6) = 49/20` for `19/20`, item D4
(non-propagating); Remark 4's wrong asymptotic, item D5 (the
correction strengthens the note's heuristic point); and the
understated maximal size of `Q`, item D6, which is already
incorporated in G1 above. (vii) Theorem 3.2's and Lemma 3.1's
wording and exposition defects A-D1 to A-D5 of AUDIT-A.md, which
do not affect the certified intersecting case.

---

## 4. What a Cycle 2 would need: specification in priority order

Each item states its target assertion, the new idea or external
result it requires, and the Cycle 1 output it builds on. Items are
ordered so that each is pickable-up directly and independently
unless it says otherwise.

**C2-1. Land the Cycle 1 clusters before opening new
fronts. COMPLETE (clusters landed).** Targets, as landed: Cluster
D's verdict on `L = 2` is the sharpened residual R_D in
CLUSTER-D.md Section 3 (not a closure, and no solution found);
Cluster E's verdict on the target lemma in the regimes (fixed `R`;
`a > b/2`) is in CLUSTER-E.md (regime (ii) closed, regime (i)
CERTIFIED WITH QUALIFICATIONS, (H-sieve) refuted); Cluster C1's
census extension to `b <= 20,000` is EXTENSION CERTIFIED in
CENSUS1.md. Builds on: CENSUS0.md's two implementations and
verifier; TARGET.md; Theorem 14.2 as audited in Section 2 above.
No new idea required; this was completion and certification of
work already specified in CYCLE1_DESIGN.md, and it is done.

**C2-2. A clean, repaired, effectivised restatement of Theorem
17.1.** Target: one campaign-owned file restating Theorem 17.1
with the `z_b` definition fixed once (recommendation: keep the
Section 12 form `max(L, b / ((1 - eps) log b))` and re-derive the
Section 13 package under it, flagging every step where fixed `L`
is used), the justification D3 as supplied by Cluster D claim D0
(CERTIFIED in CLUSTER-D.md) and the missing justifications
D4(a), D4(b) written in,
Lemma 2.1 proved for all signs of the unique minimum, and explicit
thresholds extracted wherever the underlying estimates allow,
including the `L`-dependence of Theorems 12.1 and 13.3. Builds
on: AUDIT-A.md; clusters/A/redteam.md Section 2; AUDIT-B.md item
D2's repair for the parallel Zeraoulia statement. Requires: no
new mathematics, but explicit prime-number-theorem bounds
(external, standard) where thresholds are wanted. This item is
the prerequisite for stating C2-5 precisely.

**C2-3. Close `L = 2` ( Problem 18.1 ), if Cluster D has not.**
Cluster D has not closed it: at Cycle 1 close G3 is replaced by
residual R_D in CLUSTER-D.md Section 3, and the quadratic route
(route (b) below) is CERTIFIED as exhausted in CLUSTER-D.md, so a
Cycle 2 attempt needs one of the extra inputs E1, E2 or E3 named
there, or the combined-modulus route (c) below.
Target assertion: G3's closing assertion. Routes, in the order
Cluster D ran them: (a) CRT and smoothness: force
a contradiction between `P_1 u_1 - P_0 u_0 = 1`, the bounds
`u_i = P_i^{o(1)}` with `u_i` smooth and dividing `Lambda_b`, and
the partition of *all* primes in `(z_b, b]`; the new idea needed
is an estimate that uses the partition globally (for instance,
that `u_0` and `u_1` cannot simultaneously be inverse to the
complementary products modulo each other's `P_i` while both
staying smooth), since prime-by-prime conditions are already
exhausted by Theorems 14.2 to 14.4. (b) The quadratic route:
exclude `Y^2 = 1 + 4 P W` with `W = u_0 u_1` in the forced ranges
(sammausberg's compression, INFORMATION.md Section 8), by modulo
and quadratic-form arguments. (c) A combined-modulus route, not
in either note: the top-half square congruences of Theorem 14.3
determine `c` modulo `p^2` for every `p in (b/2, b]` on its side
of the partition; since `sum_{b/2 < p <= b} 2 log p` is about
`b`, larger than `log c = b/2 + o(b)`, a Cycle 2 prover should
determine whether the combined system overdetermines `c` given
the partition, reducing the problem to a bound on the number of
admissible partitions. Builds on: CENSUS0.md Section 3 (the four
pronic near-misses are the finite shadow of this system);
CLUSTER-D.md for the final state of routes (a) and (b) (route (b)
CERTIFIED as exhausted, route (a) narrowed to residual R_D).

**C2-4. The singleton case outside the regimes Cluster E
closed.** Cluster E closed regime (ii) `a > b/2` completely and
regime (i) fixed `R` with qualifications, by direct arguments in
CLUSTER-E.md, not via 13R+. Its closure of `a > b/2` was by a
non-sieve argument, which partially addresses the short-interval
idea in (i) below, while (H-blind) as a global statement about
`P1`-empty intervals remains open. Targets, in order: (i)
(H-blind): no singleton solution with `P1(a,b)` empty and `b`
large. New idea needed: an obstruction from the discarded primes
(the prime 2, or primes `p` with `p^2 <= b`, where the denominator
of `H(a,b)` can carry higher powers and the analysis is genuinely
different), or a short-interval theorem for `a > b/2` exploiting
that `P1` empty forbids any prime in `(b/2, b]` inside `[a,b]`
and forbids any singly-occurring prime power configuration
(TARGET.md Remark 1). Builds on: AUDIT-B.md (certified sieve);
TARGET.md; CLUSTER-E.md for the `a > b/2` closure. (ii) The
remaining singleton range outside the Cluster E regimes, namely
`a <= b/2` with `R` growing: (H-sieve) is not available as a
target here, because Cluster E refuted it for every `B_0` (the
Theorem F family), and the single-candidate form of TARGET.md
Remark 2 is refuted at the same intervals. (iii) The
uniform-in-`a` singleton statement itself (Gap G1), by a mechanism
outside the forced class: 13R+ no longer serves as the closing
route, since its hypotheses are unsatisfiable.

**C2-5. A uniform-in-`L` CRT-smoothness package.** Target: the
closing assertion of G4, in two steps: first, Theorems 12.1 and
13.3 restated with all error terms explicit in `L`, valid for
`2 <= L <= L_0(b)` with `L_0(b)` as large as the estimates allow
(at minimum `L_0(b)` a power of `log b`; the natural barrier is
`L_0(b)` of order `b / log b`, where `u_j = P_j^{o(1)}` fails);
second, an exclusion in the complementary range
`L_0(b) < L = o(b)`, where the upper block is long and different
tools (the large-prime pairing and square reflection of the
note's Section 8, which are uniform in `L` as printed) are the
available starting point. Builds on: C2-2 (for the explicit
`L`-dependence) and clause (1). Requires: new uniformity work,
not new external results, for step one; step two is open-ended.

**C2-6. Tao's configuration as a direct target.** Target: any of
the three closing assertions (a), (b), (c) of G5, for fixed short
`L` in the first instance. External results a prover would need
to import or replace: distribution of smooth numbers in short
intervals at exponential height (for (a)); a large-sieve or
character-sum incompatibility for the simultaneous mirror system
(for (b)). Builds on: clauses (2), (3), (5), (7), (9) of
Section 2, and C2-3 if `L = 2` falls first (route (c) of G5 is
exactly G3). Difficulty: the highest on this list; the design
document's decision to scope rather than attack it in Cycle 1
stands until C2-3 or C2-4 produces a tool that bears on it.

**C2-7. Census as evidence, continued.** Current frontier: the
census extension to `b <= 20,000` is EXTENSION CERTIFIED in
CENSUS1.md, in both branches (singletons exactly the six known,
none new in `(2000, 20000]`; `L = 2` branch empty, near-miss list
unchanged, four intervals only). The stretch to 100,000 was NOT
run, by coordinator decision: Implementation A needs a memory
adaptation of about 909 MB, Implementation B projects 51+ hours,
and the 20,000 result already satisfies the design's tenfold
criterion. Target, if a Cycle 2 reopens it: extend the certified
census as far as the C1 pipeline benchmarks allow (design stretch
goal `b <= 100,000` for the singleton branch, after the memory
adaptation for Implementation A), and in parallel census the
structured near-miss families the theory singles out
(pronic-denominator intervals for `L = 2`; intervals with
`B(a,b)` in the forced CRT class for the singleton
single-candidate form, extending the `b <= 300` list of 83 in
TARGET.md Remark 4). Purpose: evidence about whether the
asymptotic hypotheses of G1 and G3 have any small-case support,
and early warning of a counterexample, which would settle #288
in the negative and outrank every other item on this list.
Builds on: CENSUS0.md; CENSUS1.md for the current frontier.

---

## 5. Summary table

| Gap | Content | Closing assertion (short form) | Status of inputs |
|---|---|---|---|
| G1 | Singleton `L = 1` | A mechanism outside the forced class, for `a <= b/2` with `R` growing and the general uniform statement (13R+ route refuted) | Machinery CERTIFIED (AUDIT-B.md); (H-sieve) REFUTED for every `B_0` by the Theorem F family in CLUSTER-E.md, so 13R and 13R+ have unsatisfiable hypotheses; (H-blind) remains open as a statement but is moot as a component of 13R+; regimes (ii) `a > b/2` CLOSED (exactly `(1,1,1)`, `(2,2,2)`, `(2,3,6)`) and (i) fixed `R` CERTIFIED WITH QUALIFICATIONS, both by direct arguments in CLUSTER-E.md |
| G2 | Fixed `L >= 2` | Per-`L` non-existence of the CRT-smoothness system | Necessary package supported as stated, with gap D3 now filled by D0 (CERTIFIED, CLUSTER-D.md); no exclusion known; first instance `L = 2` sharpened by residual R_D, not closed |
| G3 | `L = 2` | Problem 18.1, as narrowed by residual R_D | OPEN, replaced by residual R_D in CLUSTER-D.md Section 3 (extra inputs E1, E2, E3); D0 CERTIFIED, D1 CERTIFIED WITH QUALIFICATIONS, D2 CERTIFIED, quadratic route CERTIFIED as exhausted; census EXTENSION CERTIFIED to `b <= 20,000` in CENSUS1.md |
| G4 | Growing `L = o(b)` | Uniform exclusion to `L_0(b)`, plus complementary range | Untouched; `z_b` defect D1 material here |
| G5 | Tao configuration | Counting theorem, or global mirror incompatibility, or G3 | All clauses of Theorem 17.1 compatible with it; several predict its shape |
| G6 | Effectivity | Explicit `B_0` and parameter dependence for Theorem 17.1 | Thresholds unquantified; census frontier EXTENSION CERTIFIED to `b <= 20,000` in CENSUS1.md, stretch to 100,000 NOT run |
| G7 | Repair debt | Write in fixes D1, D4, D5, D6 and AUDIT-B.md D2, D4 (D3 cleared) | Item (ii) (Theorem 13.3 gap, D3) CLEARED by D0, CERTIFIED in CLUSTER-D.md; remaining fixes on record in clusters/A/redteam.md and AUDIT-B.md; none affects a conclusion |

**Bottom line.** The certified record settles the intersecting
case, certifies the singleton reduction machinery, extends both
censuses to `b <= 20,000` (EXTENSION CERTIFIED in CENSUS1.md, with
the stretch to 100,000 not run), and supports Nayak's Theorem 17.1
as a necessary-condition package with four named, fillable
defects, one of which (D3, the Theorem 13.3 step) is now filled by
Cluster D claim D0, so G7 item (ii) is cleared. At Cycle 1 close,
G1 is narrowed: Cluster E closed the singleton regimes (ii)
`a > b/2` completely and (i) fixed `R` with qualifications, by
direct arguments, while refuting (H-sieve) for every `B_0`, so the
13R+ route is dead and G1 remains open only outside those regimes.
G3 remains open, now replaced by Cluster D residual R_D, which
sharpens G2 at its first instance without closing it. Between
that record and finiteness stand the remaining mathematical gaps:
the singleton case outside the closed regimes (G1), the fixed-`L`
CRT-smoothness exclusion (G2, first instance G3 as narrowed by
R_D), the growing-`L` regime (G4), and the Tao configuration that
concentrates them (G5), with effectivity (G6, census frontier now
certified to 20,000) and the remaining repair debt (G7) as the
bookkeeping gaps underneath. Nothing was posted, emailed, or
submitted anywhere.
