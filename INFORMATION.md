# Erdős Problem #288: information dossier

Gathered 2026-10-30 at Dennis Canter's direction, before any campaign
work. Sources are the two problem pages he named, the catalog's claim
record, and the two working notes (Nayak, Zeraoulia). Verbatim forum
comments and the Nayak PDF full text: retrieval in progress, see the
pending section at the end.

## 1. The problem

Is it true that there are only finitely many pairs of intervals
I_1, I_2 of positive integers such that

    sum_{n in I_1} 1/n + sum_{n in I_2} 1/n  is in N ?

Source: Erdős and Graham, Old and new problems and results in
combinatorial number theory (1980), p. 34, in the form: "It is
probably true that Sigma_{a,b} + Sigma_{c,d} is an integer only
finitely often." The authors expect the proof to be difficult: they
cannot show even that Sigma_{a,b} + 1/n is an integer only finitely
often (the singleton case, |I_2| = 1). They suggest the same
finiteness for any number k of intervals.

Site example: 1/3 + 1/4 + 1/5 + 1/6 + 1/20 = 1, i.e. I_1 = [3,6],
I_2 = {20}.

Related: Problem #289 asks the variant with k separated intervals of
length at least 2 summing to exactly 1.

## 2. Status on both sites (checked 2026-10-30)

erdosproblems.com/288: OPEN; marked "not resolvable by a finite
computation"; Comments (7), Proof claims (0), Proof expositions (0);
formalised statement: yes. Reactions: Open to collaboration:
Rafikzeraoulia2025. Currently working on: Rafikzeraoulia2025,
Ritvik_Nayak. Looks difficult: Rafikzeraoulia2025, Dogmachine.

erdosproblems.ai (wiki E0288): standing open, claim none. One claim
page: Nayak's intersecting-case note, a pending partial claim. The
Zeraoulia note has no claim page (it presents a reduction, not a
proof). The catalog's search found no proof of finiteness, no
infinite family, and no proof claim for the full or singleton
statement. The located published results concern one interval
approaching 1 (Problem #314), not two intervals summing to an
integer.

Formalisation (formal-conjectures, ErdosProblems/288.lean):
erdos_288 stated as answer(sorry) iff Set.Finite of the pair set;
three variants, all research open with proof sorry: singleton
(i2_card_eq_1), k intervals (k_intervals), and existence of some
k > 2 with finiteness (exists_k_gt_2). No disjointness imposed.

## 3. Classical background

No interval other than {1} has an integer reciprocal sum
(Theisinger 1915, Kürschák 1918, for two or more terms; generalised
to arithmetic progressions by Erdős 1932). So apart from the pair
({1},{1}), any integer sum genuinely needs both intervals.

Adjacent published work: Lim and Steinerberger, On differences of
two harmonic numbers (Mathematika 71 (2025); arXiv:2405.11354):
infinitely many single intervals come within 1/(n^2 (log n)^{5/4-eps})
of 1, via convergents of the continued fraction of e. It addresses
Problem #314; for #288 it shows one block can come very close to 1
but produces no exact integer sum and no pair bound.

## 4. The discussion thread (seven comments, as catalogued)

The thread text fetch returns 403; the catalog page catalogues all
seven comments. Verbatim retrieval is in progress (see pending).

- 9 Aug 2025, Dogmachine: Richard K. Guy is said to have asserted
  finiteness for any number of intervals, without proof or
  attribution. Not traced to a source.
- 22 Apr 2026, Dogmachine: the difference variant
  Sigma_{a,b} - Sigma_{c,d} in Z, example 1/2+1/3+1/4-1/12 = 1, said
  to appear in Erdős and Niven (1946). A different question.
- 1 Feb 2026, Zeraoulia Rafik: the singleton note (Section 6 below).
- 2 Feb 2026, Terence Tao: a literature search made with the AI
  system Claude found no published result of this form. Observation:
  if N is the largest element of I_1 union I_2, both intervals have
  length o(N), since otherwise a prime p ~ N divides only boundedly
  many denominators and forces negative p-adic valuation. Expected
  hard case: a dyadic-type interval I_1 = [alpha M, M] together with
  a very short I_2 = [N-h, N] with N much larger than M. A forum
  observation, not a claim.
- 3 May 2026, Ritvik Nayak: the research note (Section 5 below).
  Two replies the same day suggest a compression of the length-2
  condition, and report that an automated check flagged one minor
  issue in the note, without saying which.

## 5. Nayak's note (pending partial claim, 3 May 2026)

"A Research Note on Harmonic Sums over Two Integer Intervals:
Intersecting intervals and reductions in the disjoint case", May
2026, PDF on Google Drive (the file Dennis linked), written with a
great deal of assistance from GPT-5.5 Thinking by the author's own
account. Not on arXiv or in a journal; not on the erdosproblems.com
proof-claim tab; unreviewed ("the corpus records no check of the
proof").

Theorem 3.2 (intersecting case, complete): if intervals I, J
intersect and H(I) + H(J) is an integer, then up to swapping the
pair is one of ([1,1],[1,1]), ([1,2],[1,2]), ([1,2],[2,2]),
([2,2],[2,2]); and all four do have integer sums. Proof idea: the
union of two intersecting intervals is an interval [r,s] on which
the sum has coefficients 1 or 2; for s >= 3 with at least two
elements, Bertrand / Sylvester-Schur gives an odd prime dividing
exactly one denominator in [r,s] (Lemma 3.1), whose term is the
unique term of lowest p-adic valuation, so the sum is not an
integer; the single-element union gives 2/r, integral only for
r = 1, 2; unions inside {1,2} are checked directly.

Disjoint case (Sections 4 to 18; obstructions, no finiteness, and
the note expressly does not claim it): for intervals [a,b], [c,d]
with b < c, every solution has upper length d - c + 1 < b, in fact
o(b) along any infinite family; every denominator c..d divides
lcm(1..b); mirror congruences for large prime powers; a lower bound
for the denominator of H([c,d]); and for fixed upper length L = 2
(Section 14), a solution must have c = P_0 u_0, c + 1 = P_1 u_1 with
P_0, P_1 carrying almost all large prime factors and u_0, u_1 small
smooth cofactors (P_1 u_1 - P_0 u_0 = 1). Nayak's own closing ask:
whether the L = 2 obstruction can be pushed further.

## 6. Zeraoulia's note (singleton case; retrieved in full 2026-10-30)

"The singleton case of Erdős Problem 288: A CRT reduction and a
smooth-number obstruction", Zeraoulia Rafik, February 2026 (revised:
"Path A framing"), ResearchGate preprint,
doi:10.13140/RG.2.2.10862.47684/1. Unreviewed working notes; the
author states plainly they do not prove finiteness. The
erdosproblems.ai assessors could not read it (ResearchGate returned
403 to them); the full text WAS retrieved here via Dennis's link.

Setting: H(a,b) + 1/m in Z, H(a,b) = sum_{n=a}^b 1/n.

- Lemma 1 (denominator forcing): writing H(a,b) = A/B in lowest
  terms, a solution forces m = B exactly, and B | (A + 1). At most
  one candidate m per interval.
- The p-adic sieve: for an odd prime p with p^2 > b, let k(p) be the
  number of multiples of p in [a,b], the multiples p*u..p*(u+k-1),
  and T_p = sum_{j=0}^{k-1} 1/(u+j). Lemma 2: if T_p is not 0 mod p,
  then v_p(m) = 1 and m is congruent to -p * (T_p mod p)^{-1}
  modulo p^2 (the prime contributes a CRT congruence); if
  T_p = 0 mod p (the "bad prime" event), then p does not divide m
  and the prime contributes nothing.
- Lemma 5: T(u) = D'(u)/D(u) in F_p for D(u) = prod (u+j); so for
  fixed k the bad event T(u) = 0 has at most k-1 solutions u in F_p.
  Corollary 6: for fixed (u,k), bad primes divide the numerator of
  T_{u,k}, so only finitely many. For k = 2 the bad case is exactly
  u = (p-1)/2 (the symmetric pair). For u = 1: k = 1 never bad;
  k = 2 bad only at p = 3; k = 3 bad only at p = 11.
- Propositions 8 and 10: when a <= b/3 (resp. a <= b/2), every prime
  in (b/3, b] (resp. (b/2, b]), except p = 3 in one subcase, is good;
  log Q(a,b) >= 2 (theta(b) - theta(b/2)), so log Q >= (1+o(1)) b
  when a <= b/2.
- CRT reduction: any solution has m in ONE residue class
  m = r(a,b) mod Q(a,b), Q the product of p^2 over good primes; and
  m divides lcm(a..b), so m is b-smooth and m <= lcm(a..b).
- Theorem 13 (global target lemma): IF for all b >= B_0 and all a,
  the forced class contains no b-smooth positive integer
  m <= lcm(a..b), THEN the singleton equation has only finitely
  many solutions. Remark 14: Q > lcm alone does NOT suffice; one
  needs the least residue r_0 itself to exceed lcm(a..b) or to be
  non-b-smooth.
- Section 8 (why known results do not reach it): smooth numbers in
  arithmetic progressions are controlled for moduli q <= x^{66/107}
  (Pascadi 2023, improving the x^{3/5} barrier), but here Q can be
  as large as x^{1+o(1)}: a "modulus as large as the search range"
  obstruction. Three possible ways through: (1) a new global
  inequality lower-bounding the least residue or obstructing
  smoothness in the class; (2) smooth-AP results reaching
  q ~ x^{1-o(1)} or exploiting the special structure of r(a,b);
  (3) distance-to-integer lower bounds for H(a,b) avoiding smooth-AP
  technology.
- Section 9 computations (script in Appendix A, exact rational
  arithmetic): exhaustive check of the singleton equation for all
  b <= 1600. The ONLY solutions are (a,b,m) = (1,1,1), (1,2,2),
  (2,2,2), (1,3,6), (2,3,6), (3,6,20). Bad-prime sampling over 5,000
  random intervals with b <= 4000: 1,167,988 prime-interval
  incidences, 1,882 bad (about 0.1611%); mean per-interval bad
  fraction 0.3335. The author notes the script runs in tens of
  seconds at B = 1600 and could be pushed much further.

## 7. What this means for a campaign (orientation, not a plan)

- The intersecting case is claimed settled by Nayak (Theorem 3.2);
  it is short and elementary, and independently verifying it is the
  natural first certified task, including locating the "one minor
  issue" an automated check reportedly flagged.
- The singleton case now has a complete reduction on the table
  (Zeraoulia): everything reduces to the global target lemma about
  b-smooth integers in one forced CRT class, with the bottleneck
  quantified (modulus comparable to the search range). Its lemmas
  are elementary and individually verifiable; its computations stop
  at b <= 1600, a cutoff that can be extended by orders of magnitude.
- The general disjoint case has Nayak's obstructions (denominators
  dividing lcm(1..b); upper length o(b); the rigid L = 2 form),
  each a verifiable statement, and his explicit question whether
  the L = 2 obstruction can be pushed further.
- Tao's comment names the expected hard configuration for the full
  problem: a dyadic interval at scale M plus a very short interval
  at a much larger scale N.

## 8. Retrieval completed 2026-10-30 (all four of Dennis's links followed)

- Nayak PDF: downloaded from the Drive link (22 pages, 439 KB);
  held at sources/Nayak-2026-harmonic-sums-two-intervals.pdf with
  extracted text at sources/Nayak-2026.txt. Details confirmed from
  the document itself: Theorem 4.2 (upper divisor block: every
  n in [c,d] divides Lambda_b, via Lemma 2.3, the denominator
  equality den H([c,d]) = den H([a,b])); Theorem 17.1 (the summary
  disjoint obstruction theorem); Section 16 treats the singleton
  upper interval inside Nayak's own frame: disjoint singleton
  solutions are exactly the lower intervals whose reduced
  denominator D satisfies D > b and A = -1 (mod D), the three known
  examples being ([1,3],{6}), ([2,3],{6}), ([3,6],{20}); and
  Proposition 16.1 records his exact verification through
  b <= 2000: the singleton branch has only the three known
  solutions, and the L = 2 branch has NO disjoint solution for
  b <= 2000. Appendix A is his finite verification script;
  Appendix B is a status and assistance note.
- Forum thread: loaded in the live browser after clearing an
  initial block; all 7 comments transcribed. Points the catalog
  summary did not carry: Tao's hard case has N "perhaps even
  exponentially larger" than M, with many primes of I_1 likely
  forced to divide elements of I_2, and his search also noted
  Graham's 2013 survey; the first reply to Nayak (sammausberg)
  proposes compressing the L = 2 obstruction to ruling out
  Y^2 = 1 + 4 P W with W = u_0 u_1 smooth and small, log P = b + o(b);
  the second reply (Nat Sothanaphan) is exactly: "Thanks! Standard
  check claimed 1 minor issue in the notes." Nothing anywhere on
  the thread says what the issue is, which check flagged it, or
  where in the note it sits. Locating it is therefore an open task
  for whoever audits the note, which is to say, for us if we take
  up the verification.
