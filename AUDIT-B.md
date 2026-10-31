# Cluster B, Verifier: certified audit of Zeraoulia's singleton reduction

Verifier, Cluster B, Cycle 1 (Erdos Problem #288, singleton case).
Subject: Zeraoulia Rafik, "The singleton case of Erdos Problem 288:
A CRT reduction and a smooth-number obstruction", February 2026
(revised: Path A framing), doi:10.13140/RG.2.2.10862.47684/1.

Method (verifier discipline). The check plan was formed from the
statements in the note itself (full primary text retrieved via the
DOI above, ResearchGate text, 10 pages, Sections 1 to 9 and
Appendix A), and all independent checks were run BEFORE the two
auditors' files were opened. Auditor files compared afterwards:
clusters/B/auditor1.md and clusters/B/auditor2.md, with their code
and outputs beside them. Verifier code (exact arithmetic only:
Python fractions.Fraction and arithmetic in F_p):
clusters/B/verifier_checks.py; raw output:
clusters/B/verifier_output.txt.

Notation: H(a,b) = A/B in lowest terms, B = den H(a,b); for odd p
with p^2 > b and k(p) >= 1 multiples p*u, ..., p*(u+k-1) in [a,b],
T_p = sum_{j=0}^{k-1} 1/(u+j) read in F_p; P1(a,b) = set of good
primes (Lemma 2 case (a)); Q(a,b) = product of p^2 over P1(a,b)
(empty product = 1); L(a,b) = lcm(a, ..., b).

## 1. Per-item certification

- **Lemma 1 (denominator forcing): CERTIFIED.**
  A solution of H(a,b) + 1/m in Z forces m = B and B | (A+1); at
  most one candidate m per interval. Verifier: exhaustive over all
  45,150 intervals with b <= 300, finding ALL m by enumerating the
  integer k = H(a,b) + 1/m (not just testing the candidate):
  0 failures; solution set in range is exactly (1,1,1), (1,2,2),
  (2,2,2), (1,3,6), (2,3,6), (3,6,20). Both auditors agree.

- **Lemma 2, case (a) (T_p not 0 mod p): CERTIFIED WITH DEFECT.**
  Statement: v_p(m) = 1 and m = -p*(T_p mod p)^{-1} (mod p^2).
  The statement is fully verified (below). The defect is in the
  note's proof exposition only (defect D3): the "for completeness"
  paragraph writes (1/p)T_p + 1/(p*m1) = 0 "in Z_p / pZ_p", but
  both terms have valuation -1 and are not elements of Z_p, so the
  displayed congruence is formally meaningless as written. The
  correct step, multiplication of the integrality equation by p,
  yields T_p + m1^{-1} = 0 (mod p), which is exactly what the note
  uses next; the conclusion is unaffected. Verifier evidence for
  the statement: (i) valuation form, unconditional: at all
  1,417,462 good incidences over b <= 300, v_p(den H(a,b)) = 1,
  0 failures; (ii) congruence form, in its correct conditional
  (p-local) form: for all intervals with b <= 60, all good p, and
  all t in [1, p-1], H(a,b) + 1/(p*t) is p-integral if and only if
  t = -(T_p mod p)^{-1} mod p: 321,242 exact tests, 0 failures;
  (iii) on all six solution intervals with b <= 300, den H lies in
  the full CRT class (see CRT item).

- **Lemma 2, case (b) (T_p = 0 mod p, bad prime): CERTIFIED.**
  Statement: v_p(m) = 0, i.e. p does not divide m, and p
  contributes no mod-p^2 congruence. Verifier: at all 17,036 bad
  incidences over b <= 300, v_p(den H(a,b)) = 0, 0 failures. (The
  incidence totals 1,417,462 + 17,036 = 1,434,498 agree exactly
  with Auditor 1's independent count.) Both auditors agree.

- **Lemma 5 (T(u) = D'(u)/D(u); at most k-1 bad u in F_p):
  CERTIFIED.** The hypothesis 1 <= k < p is stated explicitly in
  the note (verified in the primary text); any suggestion that it
  is merely implicit in the note is refuted (it is only the
  dossier's one-line summary that omits it). Verifier: for every
  odd prime p <= 199 and every 1 <= k < p, the bad u in F_p are
  exactly the roots of D'(u) on the domain D(u) != 0, and their
  number never exceeds k-1 (0 failures); the bound k-1 is attained
  (max root counts for k = 2, 3, 4, 5 are 1, 2, 3, 4). Recorded
  gap G1 (not a defect): the note asserts deg D' = k-1 without
  noting this uses the leading coefficient k != 0 in F_p, supplied
  by k < p.

- **Corollary 6 (fixed (u,k): only finitely many bad primes;
  bad primes p > u+k-1 are exactly the prime divisors of the
  numerator N_{u,k}): CERTIFIED.** Verifier: grid u in [1,8],
  k in [1,6], all primes p <= 300 with p > u+k-1: bad iff
  p | N_{u,k}, 0 failures. The u = 1 classifications are exact:
  k = 1, T = 1, no bad primes; k = 2, T = 3/2, bad only at p = 3;
  k = 3, T = 11/6, bad only at p = 11. The k = 2 symmetric-pair
  characterisation (bad iff u = (p-1)/2) is consistent with the
  root count (D'(u) = 2u+1) and with both auditors' tests.
  Recorded gap G2 (not a defect): the note does not state that the
  reduced denominator M_{u,k} is prime to p; it holds because
  M_{u,k} | lcm(u, ..., u+k-1) and p > u+k-1.

- **Proposition 8 (a <= b/3, b >= 10: every prime in (b/3, b],
  p != 3, is good; log Q >= 2(theta(b) - theta(b/3)) - O(1)):
  CERTIFIED.** Verifier: all b in [10, 300] and all a <= b/3
  (14,938 intervals): every prime in (b/3, b] lies in P1(a,b),
  0 failures. Cosmetic note (both auditors): under b >= 10 the
  exclusion p != 3 is vacuous (p > b/3 > 3) and the -O(1) is
  unnecessary; not an error.

- **Proposition 10 (a <= floor(b/2)+1: every odd prime in
  (b/2, b] contributes; log Q >= 2(theta(b) - theta(b/2))):
  CERTIFIED WITH DEFECT.** Defect D2: the displayed theta bound
  is FALSE as stated for b = 2 and b = 3, because the theta
  difference counts the prime 2, which never contributes to Q
  (Q is built from odd primes only). Counterexamples satisfying
  the hypothesis: (a,b) = (1,2): log Q = 0 < 2 log 2 = 1.3863;
  (a,b) = (2,3) (the note's own worked example): log Q =
  log 9 = 2.1972 < 2(theta(3) - theta(3/2)) = 3.5835. Verifier:
  over all b <= 300 and all a <= floor(b/2)+1, violations occur
  exactly at b = 2 and b = 3 (4 violating pairs: (1,2), (2,2),
  (1,3), (2,3)) and nowhere else; the same bound summed over odd
  primes only has 0 violations in range. The goodness claim
  itself (k(p) = 1, u = 1, T_p = 1 for odd p in (b/2, b]) is
  certified in the same range, the note's hypothesis
  a <= floor(b/2)+1 is correct (the dossier summary's "a <= b/2"
  is a weakening), and Remark 11's asymptotic consequence
  log Q >= (1+o(1)) b is unaffected. Repair: add b >= 4, or sum
  over odd primes, or subtract O(1) as in Proposition 8.

- **CRT reduction (any solution has m = r(a,b) (mod Q(a,b));
  m | L(a,b), hence m <= L(a,b) and m is b-smooth): CERTIFIED.**
  Verifier: den H(a,b) | L(a,b) for all 45,150 intervals with
  b <= 300 (0 failures); for each of the six solution intervals,
  den H lies in the CRT class assembled from all good primes
  (0 failures). The corrected formula for log L(a,b) (sum over
  p <= b of e_p(a,b) log p, not psi(b) - psi(a-1)) and the [4,5]
  illustration are correct. Recorded gap G3 (not a defect): the
  note asserts m | L(a,b) from m = den H in one line; the one-line
  justification (H(a,b) = (integer)/L(a,b), so the reduced
  denominator divides L(a,b)) is standard and correct. Also
  recorded: gap G4 (Auditor 1's G4 / Auditor 2's D-9): Section 2's
  display (2), B | m(A+1), is true but its printed derivation
  skips the gcd step (B | Am and gcd(A,B) = 1 give B | m); it is
  not used by the proof of Lemma 1. No conclusion is affected.

- **Theorem 13 (global target lemma): NOT CERTIFIED as stated.**
  Adjudication (b), in full in Section 2 below: the implication
  is logically valid and its proof is correct, but its hypothesis
  is unsatisfiable as quantified, so the theorem is vacuous and
  unusable as a target. The campaign's repaired statement is in
  TARGET.md.

- **Remark 14 (Q > L(a,b) alone does not suffice): CERTIFIED.**
  The argument is correct: Q > X and 0 < m <= X in the class force
  m to equal the least positive representative r_0, and r_0 <= X
  is not excluded by size alone; what is needed is r_0 > L(a,b)
  or r_0 not b-smooth. Concrete witness, verified by the verifier:
  (a,b) = (2,3) has Q = 9 > L = 6, yet r_0 = 6 <= 6, 3-smooth, and
  an actual solution. Both auditors agree.

## 2. Theorem 13 adjudication in full

The note's Theorem 13 (quoted verbatim in TARGET.md): IF there
exists B_0 such that for every b >= B_0 and every 1 <= a <= b the
forced class m = r(a,b) (mod Q(a,b)) contains no b-smooth positive
integer m <= L(a,b), THEN the singleton equation has only finitely
many solutions.

Auditor 2 calls this a valid conditional with correct uniform
quantifiers and certifies it. Auditor 1 (defect D1) argues the
hypothesis is unsatisfiable as stated. The verifier decides for
Auditor 1, on direct computation:

For every prime q (verified for q = 2, 3, 5, 7, 11, 13, 17, 19,
23, 29, 31), take (a, b) = (q^2, q^2). An odd prime p with
p^2 > b = q^2 has p > q; a multiple of p in the singleton {q^2}
would force p | q^2, i.e. p = q, contradicting p > q; and p = 2
is outside the sieve's odd-prime scope (also 2^2 > q^2 fails for
q >= 2 except q = 2, where 4 > 4 is false). Hence P1(q^2, q^2) is
empty, Q = 1, and the forced class modulo 1 is the class of all
integers. That class contains m = q^2, which is b-smooth (its only
prime factor is q <= q^2 = b) and satisfies m = q^2 = L(q^2, q^2),
i.e. m <= L(a,b). It also contains m = 1, which satisfies the
note's condition (i) vacuously. So the required exclusion fails
at (q^2, q^2) for every prime q; these b = q^2 are arbitrarily
large, so no B_0 makes the hypothesis true. The hypothesis is
false, for every B_0. Note that (q^2, q^2) is not a solution
(H = 1/q^2, A = 1, and A = -1 (mod B) fails since q^2 does not
divide 2): the defect is purely that the hypothesis demands an
exclusion at intervals where the sieve carries no information,
not that any solution escapes the sieve.

The implication itself is valid: its proof (Lemma 1, the bound
m | L(a,b), and the CRT class) is correct, so Theorem 13 is a
true but vacuous implication. Auditor 2's certification is
therefore correct about the conditional's validity but incomplete:
it does not ask whether the hypothesis can hold, and with the
hypothesis false the "global target lemma" cannot serve as a
sufficient target: no future argument can prove a false statement.
Verdict: (b) valid as an implication, vacuous as stated, NOT
CERTIFIED as a usable target. Two further points. (i) Weakening
the m-quantifier does not repair it: even the sharp form "no
divisor of L(a,b) in the class" fails at (q^2, q^2), since 1, q
and q^2 all divide L = q^2 and lie in the class modulo 1. Any
repair must restrict the (a, b) quantifier (or otherwise exclude
sieve-empty intervals); see TARGET.md. (ii) Under the alternative
reading that r(a,b) is undefined when P1 is empty, the hypothesis
is ill-formed at those pairs instead of false; either reading is
a formulation defect in the note, not in the underlying sieve.
No other item depends on Theorem 13, so the damage is confined to
the note's closing framing.

## 3. Confirmed defect list (both auditors merged, adjudicated)

Defects in the note (statements wrong, or formally invalid, as
printed):

- **D1 (Auditor 1; Auditor 2 missed it). Theorem 13 hypothesis
  unsatisfiable (vacuity). CONFIRMED** by the verifier's (q^2, q^2)
  computation for 11 primes q (Section 2). Fatal to Theorem 13's
  use as a target; touches nothing else.
- **D2 (Auditor 1; Auditor 2 missed it). Proposition 10's theta
  bound false at b = 2, 3. CONFIRMED** by the verifier: violations
  exactly at b in {2, 3} over b <= 300; the odd-prime form and all
  b >= 4 hold in range. Auditor 2's certification of Proposition
  10 is refuted as stated for the note's printed statement (its
  own derivation assumed b >= 4). The goodness claim and the
  asymptotics are unaffected.
- **D3 (Auditor 1 = Auditor 2's D-3). Lemma 2 proof's
  "in Z_p / pZ_p" step formally invalid. CONFIRMED** as an
  exposition defect: the terms have valuation -1 and are not in
  Z_p; the intended multiply-by-p step is correct and the
  statement is exhaustively verified (Section 1). No mathematical
  content is affected.
- **D4 (both auditors). Section 6.2 prints H(3,6) = 49/20; the
  correct value is 19/20. CONFIRMED in the note as published:**
  the verifier's own independent retrieval of the primary text
  (DOI above) reads 49/20, as do both auditors' retrievals; the
  same text layer renders every other fraction in the note
  correctly (5/6, 3/2, 11/6, 20/25 class data, Table 1), so this
  is a misprint in the note, not an extraction artifact of this
  audit. (Residual provenance caveat, recorded for honesty: all
  readers saw the ResearchGate text; a corruption inside that
  text layer cannot be excluded with absolute certainty, but the
  published text says 49/20 and 49/20 is wrong.) Read literally it
  contradicts the same paragraph (20 does not divide 49+1) and
  Table 1; every other claim in the example (m = 20, k = 1, p = 5
  good with class 20 mod 25, p = 3 bad, Q = 25) is correct for
  19/20 and was verified exactly. Non-propagating typographical
  defect.
- **D5 (Auditor 2's D-2; Auditor 1 did not audit Remark 4).
  Remark 4's claim that sum_{p > sqrt(b)} 1/p grows like
  log log b. CONFIRMED as an error** (heuristic remark, explicitly
  "far from a proof", used by no lemma): for the primes in play,
  sqrt(b) < p <= b (k(p) >= 1 forces p <= b), Mertens gives
  sum_{sqrt(b) < p <= b} 1/p = log log b - log log sqrt(b) + o(1)
  = log 2 + o(1), bounded. Verifier numeric: 0.6266, 0.6324,
  0.6802, 0.6827, 0.6892 at b = 10^2, 10^3, 10^4, 10^5, 10^6,
  converging to log 2 = 0.6931, while log log b grows to 2.6258.
  The corrected asymptotics strengthen the remark's heuristic
  point (bad primes rarer than claimed), so nothing downstream
  is weakened.
- **D6 (Auditor 2's D-8). "Q can be as large as exp((1+o(1))b)" /
  "x^{1+o(1)}" (abstract, Remark 12, Section 8) understates the
  maximal size of Q. CONFIRMED as a framing imprecision, not a
  false proved statement:** what is proved (Propositions 8, 10,
  Remark 11) is the lower bound log Q >= (1+o(1)) b in the regime
  a <= b/2, and that lower bound is certified. But log Q can be
  strictly larger: the trivial envelope is
  log Q <= 2(theta(b) - theta(sqrt(b))) = (2+o(1)) b, and the
  verifier measured max log Q / b = 1.8448 over all a with
  4 <= b <= 300 (attained at (a, b) = (18, 283)); at a = 1,
  log Q / b = 1.4245, 1.5676, 1.7825, 1.7592 at b = 50, 100, 200,
  300, the b = 300 value equalling the full envelope
  2(theta(300) - theta(sqrt(300)))/300 exactly. Auditor 2's
  b = 500, a = 1 value 1.834 is consistent. So Q can reach
  exp((2+o(1)) b), i.e. about x^{2+o(1)} for x = lcm(1..b); the
  note's bottleneck conclusion (modulus at least on the search
  range scale, beyond the x^{66/107} reach it cites) is correct
  and, if anything, understated.

Gaps (correct steps, missing or compressed justification; all
CONFIRMED as gaps, none affects any conclusion): G1 (Lemma 5:
deg D' = k-1 uses k != 0 in F_p, from k < p, unstated); G2
(Corollary 6: reduced denominator prime to p, unstated); G3 (CRT
section: m | lcm(a..b) asserted in one line); G4 (Section 2
display (2): gcd step skipped; statement true, unused by Lemma 1's
proof); G5 (Proposition 8: p != 3 exclusion vacuous under
b >= 10; P1 used before its Section 4 definition). Auditor 2's
D-7 (the dichotomy also holds for p = 2 when 4 > b; the note's
odd-prime scope is deliberate per its Remark 9) is CONFIRMED as a
scope observation, not a defect: the note's claims about its
odd-prime Q are correct as stated.

Refuted items: (i) any claim that Lemma 5's k < p hypothesis is
missing from the note: REFUTED, it is explicit in the statement
(only the dossier summary omits it); (ii) Auditor 2's unqualified
certification of Theorem 13 ("no overclaim in the note"):
REFUTED in part, see D1; (iii) Auditor 2's unqualified
certification of Proposition 10: REFUTED in part, see D2.

Unresolved / out of scope (stated plainly): the note's Section 8
literature claims (e.g. Pascadi 2023, q <= x^{66/107}) and its
Section 9 random bad-prime sampling statistics (unseeded) were
not verified by the verifier or by either auditor, and no audited
item depends on them.

## 4. Verifier's computational coverage

All in clusters/B/verifier_checks.py, exact arithmetic, output in
clusters/B/verifier_output.txt.

- Lemma 1: all 45,150 intervals, b <= 300, all m found by
  k-enumeration; 0 failures; six solutions exactly. (The
  verifier's first pass had an off-by-one at the single interval
  (1,1), k <= H+1 vs k < H+1; caught by the equivalence check,
  fixed, rerun clean. Recorded here so the record shows the
  check bit in both directions.)
- Lemma 2 dichotomy: all intervals b <= 300, all odd p with
  p^2 > b and k(p) >= 1: 1,417,462 case-(a) incidences
  (v_p(den H) = 1 throughout) and 17,036 case-(b) incidences
  (v_p(den H) = 0 throughout); 0 failures. Case-(a) congruence in
  conditional p-local form: b <= 60, 321,242 exact tests,
  0 failures. (An unconditional "den H satisfies (4) for every
  interval" reading was also tested and fails, as it must: (4) is
  conditional on a solution existing, e.g. (a,b,p) = (3,3,3) has
  den mod 9 = 3 against the predicted 6. This is a property of
  the statement, not a defect.)
- Worked examples (2,3) and (3,6) recomputed from scratch:
  H(2,3) = 5/6, P1 = {3}, Q = 9, class 6 mod 9; H(3,6) = 19/20,
  P1 = {5}, Q = 25, class 20 mod 25; all as the note concludes
  (modulo D4's printed numerator).
- Bad primes, u = 1: k = 1, 2, 3 give bad-prime sets {}, {3},
  {11} over primes p <= 300 (p > u+k-1), exactly as claimed.
  Lemma 5 root counts: all odd p <= 199, all k < p, 0 failures.
  Corollary 6: grid u <= 8, k <= 6, p <= 300, 0 failures.
- Theorem 13 family: (q^2, q^2) for q = 2, 3, 5, 7, 11, 13, 17,
  19, 23, 29, 31: P1 empty, Q = 1, m = q^2 b-smooth with
  m = L(a,b), in the class; A = -1 (mod B) false throughout.
- Proposition 10 bound: all b <= 300, all a <= floor(b/2)+1:
  violations exactly at b = 2, 3. Proposition 8: all b in
  [10, 300], a <= b/3: 0 failures.
- Remark 4: reciprocal-prime sums to b = 10^6 (Section 3, D5).
- Size of Q: all a, 4 <= b <= 300: max log Q / b = 1.8448.
- CRT and divisibility: den H | L(a,b) on all 45,150 intervals;
  CRT class membership on all six solutions; 0 failures.
- Remark 14 witness: (2,3), Q = 9 > L = 6, r_0 = 6 <= 6.
- Supplementary (for TARGET.md, verifier_target_check.py /
  verifier_target_output.txt): intervals with b <= 300, P1
  nonempty, and den H(a,b) in the forced CRT class: exactly 83,
  namely the 3 solution intervals with Q > 1 and 80 non-solution
  intervals. This certifies nothing about the lemmas (Lemma 2 is
  a necessary condition only); it is recorded because it governs
  how the repaired target in TARGET.md may be read.

Bottom line: the sieve chain (Lemmas 1, 2, 5, Corollary 6,
Propositions 8, 10, CRT) is correct, with one small-case defect
(D2) and proof-exposition defects (D3, gaps G1 to G5) that change
no conclusion; the worked example carries one misprint (D4);
Remark 4's heuristic asymptotic is wrong in the note's favour
(D5); the size framing understates Q (D6); and Theorem 13, the
note's closing target, is vacuous as stated (D1) and is replaced
for campaign use by the repaired statement in TARGET.md. Nothing
was posted, emailed, or submitted.
