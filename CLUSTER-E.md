# Cluster E, Verifier: certification record, Cycle 1, Erdős Problem #288, singleton case

Verifier, Cluster E, Cycle 1. Date: 2026-10-30.

Inputs read in full: `clusters/E/prover1.md` (restored file; provenance
header explains the truncation, the truncated original is
`prover1_truncated.md`), `clusters/E/prover2.md`, `clusters/E/redteam.md`,
`AUDIT-B.md`, `TARGET.md`. Black boxes used, as certified in AUDIT-B.md:
Lemma 1 (a solution forces m = B(a,b) and B | A+1), Lemma 2 (the sieve
dichotomy at odd primes p with p^2 > b, including its p-local form), the
CRT reduction, and the certified census (all solutions with b <= 300 are
exactly (1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20)).
Bertrand's postulate is used as in TARGET.md. Everything else in
claims C1 to C4 was checked line by line by the verifier, independently
of the red team; the red team's survival verdicts were treated as
evidence only, not as certification.

Verifier code (exact arithmetic only, Python `fractions.Fraction` and
integers): `clusters/E/verifier_checks.py`; raw output:
`clusters/E/verifier_output.txt`. Section numbers V0 to V7 below refer
to that output.

Notation: H(a,b) = sum_{n=a}^{b} 1/n = A/B in lowest terms,
R = b - a + 1, L(a,b) = lcm(a, ..., b), and P1, Q, T_p, r(a,b) as in
TARGET.md.

## 1. Per-claim verdicts

| Claim | Verdict |
|---|---|
| C1 (regime (ii), Prover 1's route) | **CERTIFIED** |
| C2 (regime (ii), Prover 2's route) | **CERTIFIED** |
| C3 (regime (i), both provers) | **CERTIFIED WITH QUALIFICATIONS** (Q1, Q2 below; both are part of the claim as tasked, not new restrictions) |
| C4 (the class route refuted, Theorem F) | **CERTIFIED WITH QUALIFICATIONS** (Q3 below; the qualification concerns the printed statement of the supporting Lemma 1.1 at a = 1, 2 only, outside the range used) |

Qualifications, stated exactly.

- Q1 (C3, quantifiers). C3 is a statement per fixed R, not uniform in
  R: for each fixed R the bound is a <= 2R, and the finite check grows
  with R. No uniform-in-R finiteness and no classification for all R
  at once is certified.
- Q2 (C3, range of classification). The complete classification is
  certified for R <= 100 only, via the certified census
  (b <= 3R - 1 <= 299). For R > 100 only finiteness is certified,
  together with the specified finite check (1 <= a <= 2R, testing
  (A+1) mod B = 0); that check has not been run for R > 100 and no
  solution list for R > 100 is certified.
- Q3 (C4, supporting lemma). Prover 2's Lemma 1.1, as printed, states
  its conditions (alpha) and (beta) for "prime divisor p" without the
  word "odd". In that literal reading the lemma is false at a = 1 and
  at a = 2 (defect D-E1, Section 6). With "odd prime divisor" in both
  conditions, which is what the lemma's own proof proves, what the
  note after it says, and what Prover 2's code checks, the lemma is
  correct. The two readings coincide for every a >= 3, because then
  b = a + 1 >= 4 and 2^2 <= b, so the prime 2 never satisfies
  p^2 > b. The Theorem F family has a = n_P^2 >= 4, so Theorem F and
  every consequence drawn from it in C4 are unaffected. C4 is
  certified for Theorem F itself, with Lemma 1.1 understood in its
  corrected odd-prime form.

No claim is marked NOT CERTIFIED. No prover file was patched.

## 2. The certified statements, in final precise form

These are the statements the cycle record may quote.

**S1 (regime (ii) classification).** If a > b/2 (strict), the
singleton equation H(a,b) + 1/m in Z, with m a positive integer, has
exactly the solutions (a,b,m) = (1,1,1), (2,2,2), (2,3,6). Certified
by two independent routes: C1 (Section 3.1) and C2 (Section 3.2).

**S2 (regime (i), per fixed R).** Fix R >= 1. The singleton equation
with b - a + 1 = R has only finitely many solutions. Precisely:
for R = 1 the solutions are exactly (a,m) = (1,1) and (2,2)
(i.e. a in {1,2}); for R >= 2 every solution satisfies a <= 2R
(in fact a < 2R, by the strict chain in Section 3.3), hence
b <= 3R - 1, and all solutions for that R are found by the explicit
finite check over 1 <= a <= 2R. The classification is complete for
R <= 100: the solutions are (1,1,1), (2,2,2) at R = 1; (1,2,2),
(2,3,6) at R = 2; (1,3,6) at R = 3; (3,6,20) at R = 4; and none for
5 <= R <= 100. For R > 100 the finite check is specified but not run.

**S3 (Theorem F: (H-sieve) is false for every B_0).** For each prime
P = 1 (mod 4), let n_P in [1, (P-1)/2] satisfy n_P^2 = -1 (mod P)
(such n_P exists, by Wilson's theorem), and let
(a,b) = (n_P^2, n_P^2 + 1). Then: R = 2 and a > b/2; P1(a,b) = {P}
exactly; B(a,b) = a(a+1) = L(a,b), so B is b-smooth and B <= L;
B lies in the forced class r(a,b) mod Q(a,b); v_p(B) = 1 at every
good prime p and there are no bad primes; and (A+1)/B = 2/a, which
is not an integer (a >= 4), so (a,b) is not a solution. The
intervals obtained are infinitely many distinct intervals. Hence
the hypothesis (H-sieve) of TARGET.md fails for every B_0, and so
does its single-candidate weakening (B(a,b) not in the forced
class): both fail at these intervals for all large P.

**S4 (consequence for method).** No argument whose only input is
membership of a b-smooth integer (in particular of m = B(a,b)
itself) in the forced class, together with B <= L and the good/bad
prime valuation profile, can exclude the intervals of S3, in
either regime (i) (the family has fixed R = 2) or regime (ii)
(the family has a > b/2). The closures S1 and S2 use input outside
the forced class: the size of the numerator A + 1 against B
(regime (i) and regime (ii), Case 1), the prime 2 (regime (ii),
window case of C2), and a single specific good odd prime together
with a bound on m (regime (ii), strip case of C1).

## 3. Line-by-line verification

### 3.1 C1: Prover 1's proof of Theorem II

Thresholds and strictness. The split is b <= 33 versus b >= 34.
The b <= 33 part rests on the certified census, which covers
b <= 300 and therefore b <= 33 with room to spare. Filtering the
six census solutions by the strict inequality 2a > b keeps exactly
(1,1,1), (2,2,2), (2,3,6): (1,3,6) has 2a < b, and the two boundary
solutions (1,2,2) and (3,6,20) have 2a = b exactly and are correctly
excluded. Independently recomputed in V6 and V1.

Partition for b >= 34. The subregimes 3a >= 2b + 2 and 3a <= 2b + 1
partition all cases exactly, since 3a and 2b + 1 are integers;
3a = 2b + 1 belongs to the strip, 3a = 2b + 2 to subregime A.

Subregime A. Writing b = a + R - 1, the condition 3a >= 2b + 2
gives a >= 2R. Then H <= R/a, with equality only at R = 1; for
R >= 2 the terms after the first are strictly below 1/a, so
H < R/a <= 1/2, and for R = 1 (so a = b >= 34) H = 1/a <= 1/34 < 1/2.
Hence 0 < H < 1/2, and H + 1/m is in (1, 3/2) for m = 1 and in
(0,1) for m >= 2: never an integer. The restored file carries the
R = 1 caveat explicitly, in Theorem I and in subregime A; the bare
inequality "H < R/a" that the red team flagged in the coordinator's
sketch does not occur unqualified in the restored file. Correct.

Strip, Step 1 (H < 3/4). The integral comparison is correct:
for n >= a + 1, 1/n <= the integral of 1/x over [n-1, n], since
1/x >= 1/n there; summing gives H <= 1/a + log(b/a), and the strip
gives b <= 2a - 1, so H <= 1/a + log(2 - 1/a). The bound
log 2 < 111/160 was verified from its derivation, not just
numerically: the series log((1+x)/(1-x)) =
2 sum_{k>=0} x^{2k+1}/(2k+1) at x = 1/3 gives log 2; successive
terms have ratio ((2k+1)/(2k+3)) * (1/9) < 1/9, so the tail from
k = 6 is bounded by 9/8 times its first term 1/(13 * 3^13); the
exact rational value of the resulting bound is
2458234657/3546482940, and 111/160 minus that value is
17103061/28371863520 > 0 (V0). With a >= 18 in the strip
(a > b/2 >= 17, a integer), H < 1/18 + 111/160 = 1079/1440 < 3/4,
margin exactly 1/1440 (V0). Correct.

Strip, Step 2 (m in {2,3}). From 0 < H < 3/4 alone: a solution sum
s = H + 1/m is a positive integer, so s >= 1; m = 1 gives
s in (1, 7/4), impossible; m >= 2 gives s < 3/4 + 1/2 = 5/4, so
s = 1, 1/m = 1 - H in (1/4, 1), and m in {2,3}. No lower bound on
H beyond H > 0 is used, correctly. Correct.

Strip, Step 3 (the prime ell). Bertrand applied to
n = floor(b/4) >= 8 supplies a prime ell with n < ell < 2n, and
then b/4 < ell < b/2 (checked in both cases, b/4 integral or not).
The proof correctly shows that every prime ell in (b/4, b/2)
works: ell >= 11 (prime above 8.5), ell^2 > b (ell > b/4 and
b > 16), the only possible multiples of ell in [a,b] are 2ell and
3ell (1ell < b/2 < a; 4ell > b), and k(ell) >= 1 always: otherwise
2ell < a and 3ell > b (using 3ell > 3b/4 >= a, from
a <= (2b+1)/3 <= 3b/4 for b >= 4), giving
b/3 < ell < a/2 <= b/3 + 1/6, i.e. b < 3ell < b + 1/2, impossible
for integers. The values of T_ell are then exactly 1/2 (only 2ell),
1/3 (only 3ell), or 5/6 (both), each nonzero in F_ell since
ell >= 11 does not divide 2, 3, or 5 and 6 is invertible mod ell.
So ell is good, ell in P1(a,b). Correct; recomputed exhaustively
in V4.

Strip, Step 4. By certified Lemma 2, case (a), a solution at the
good prime ell forces v_ell(m) = 1, in particular ell | m. With
ell >= 11 and m in {2,3} this is impossible. Correct. C1 is
therefore a complete proof of S1.

### 3.2 C2: Prover 2's proof of Theorem II

Threshold. b < 32 is enumeration; Prover 2's own Part 4 enumeration
agrees with the certified census, which covers b < 32, and the
verifier's sweep V1 covers b <= 1000 independently. Assume
b >= 32, a > b/2. R = 1 is handled separately: (A+1)/B = 2/a is
not an integer for a = b >= 32. For R >= 2 the split at a = 2R is
exact: a <= 2R if and only if 3a <= 2b + 2, i.e.
a <= (2b+2)/3 (the window); this assigns the boundary family
3a = 2b + 2 to the window, where C1 assigns it to subregime A;
each proof covers it, there is no gap.

Lemma S (used in Case 1, and in C3). For R >= 2: H < R/a (the
first term equals 1/a, the other R - 1 terms are strictly
smaller); A >= 1 (positive numerator), so B = A/H >= 1/H > a/R,
giving 1/B < R/a; adding, (A+1)/B = H + 1/B < 2R/a. A solution
makes (A+1)/B a positive integer, hence >= 1, so a <= 2R (the
proof gives the strict a < 2R). Each step checked; the full chain,
including both component inequalities, recomputed on all
124,750 intervals with b <= 500 and R >= 2 in V5, 0 failures.
Case 1 (a > 2R) follows: (A+1)/B < 2R/a < 1 contradicts
integrality. Correct.

Window (Case 2), 2-adic bound. With 2^t <= b < 2^{t+1}, t >= 5:
if a <= 2^t, the maximum of v_2 on [a,b] is t, attained only at
2^t (no other multiple of 2^t lies in [1, 2^{t+1})); if a > 2^t,
no element has v_2 >= t, and the unique candidate with v_2 = t - 1
is 3 * 2^{t-1} (odd part in (2,4) forces odd part 3), which lies in
[a,b] because a <= 2R gives R >= 2^{t-1} + 1 (from R >= a/2 >
2^{t-1}, R integer), so [a,b] covers all residues mod 2^{t-1} and
contains a multiple of 2^{t-1}, necessarily that one.
So the maximum s is attained exactly once and s >= t - 1.
With O the lcm of the odd parts (odd), 2^s * O * H(a,b) is a sum
of integers whose n_0 term is odd and whose other terms are even,
hence is odd, so v_2(H) = -s; writing H = A/B in lowest terms
gives v_2(B) = s (one compressed sentence in Prover 2's text, see
D-E2) and B >= 2^s >= 2^{t-1} >= 16. Recomputed on all 21,066
window intervals with 32 <= b <= 500 in V3: unique maximum,
s >= t - 1, v_2(H) = -s, v_2(B) = s, B >= 16, 0 failures. Correct.

Window, analytic bound. For n >= a + 1, 1/n <= the integral of
1/x over [n-1, n]; summing and substituting x = a*u gives
H <= 1/a + the integral of 1/u from 1 to b/a, with 1 < b/a < 2.
The integrand is positive and decreasing, so the integral is at
most the integral from 1 to 2, which is at most its upper Riemann
sum on four equal subintervals (left endpoints):
(1/4)(1 + 4/5 + 2/3 + 4/7) = (1/4)(319/105) = 319/420, verified
exactly in V0 from the derivation. Combination: b >= 32 and
a > b/2 give a >= 17, so a solution would give the positive
integer (A+1)/B = H + 1/B <= 319/420 + 1/17 + 1/16 =
25157/28560 < 1 (V0), a contradiction. Correct. C2 is therefore a
complete second proof of S1.

### 3.3 C3: regime (i)

Prover 2's chain is Lemma S above: for R >= 2 any solution has
a <= 2R; for R = 1, (A+1)/B = 2/a in Z if and only if a | 2, so
a in {1,2}, and both occur. Prover 1's Theorem I is equivalent in
effect: for a > 2R, H < 1/2 (R = 1 separately; for R >= 2,
H <= 1/a + (R-1)/(a+1) < R/a < 1/2), and H + 1/m in (1, 3/2)
(m = 1) or (0,1) (m >= 2) is never an integer. Both arguments are
correct, and they prove exactly S2: finiteness per fixed R, with
the explicit finite check 1 <= a <= 2R (equivalently
b <= 3R - 1) as the complete residual for that R. For R <= 100
that residual lies inside the certified census (b <= 299), giving
the classification in S2. Quantifier hygiene was checked
specifically: neither prover claims a bound uniform in R, a
classification for R > 100, or that the R > 100 check was run;
the certified statement S2 makes the per-fixed-R scope explicit
(Q1, Q2).

### 3.4 C4: Theorem F and the refutation of the class route

Lemma 1.2 (infinitely many primes = 1 (mod 4)). The Euclid
argument is correct: from a supposed complete list p_1, ..., p_k,
any prime divisor q of N = (2 p_1 ... p_k)^2 + 1 is odd, does not
divide x = 2 p_1 ... p_k, satisfies x^2 = -1 (mod q) with
-1 not equal to 1 (mod q), so x has exact order 4 in F_q*, hence
4 | q - 1, and q is a new such prime. Correct.

Lemma 1.3 (sqrt(-1) mod P). Wilson's theorem split at (P-1)/2,
with (P-1)/2 even for P = 1 (mod 4), gives
((P-1)/2)!^2 = -1 (mod P). Correct. The least residue n_P of that
factorial or its negative lies in [1, (P-1)/2] and retains
n_P^2 = -1 (mod P); n_P >= 2 for P >= 5.

Lemma 1.1 (R = 2 characterisation), corrected form. In the
odd-prime reading (Q3, D-E1) the proof is correct in both
directions: B = a(a+1) = L (the fraction (2a+1)/(a(a+1)) is in
lowest terms, consecutive integers coprime); every odd prime p
with p^2 > b and a multiple in {a, a+1} has k(p) = 1 and
T_p = 1/u, nonzero, so it is good and there are no bad primes at
any R = 2 interval; at a good prime the forced residue is
-p*u (mod p^2); if p | a + 1 the congruence for B holds always
(p^2 | p*u*(a+1), since p | a + 1), and if p | a it fails always
(it would force p | a + 2 with p | a, so p | 2, against p odd).
Hence B is in the class if and only if no good prime divides a;
and, since P1 is nonempty if and only if some good prime divides
a or a + 1, the lemma's conjunction (P1 nonempty and B in class)
is equivalent to the odd-prime forms of (alpha) and (beta). Verified in V7: odd-prime reading,
0 mismatches for a <= 3000; literal reading, mismatches exactly
at a = 1, 2.

Theorem F family. With a = n_P^2: condition (alpha) holds since
every prime divisor of a divides n_P, so its square is <= a < a + 1;
condition (beta) holds via P itself, since P | n_P^2 + 1 = a + 1
and P >= 2 n_P + 1 (from n_P <= (P-1)/2), so P^2 > a + 1. By the
corrected Lemma 1.1, P1 is nonempty and B is in the class.
P1 = {P} exactly: a good prime cannot divide a (its square would
be <= a < b); a good prime dividing a + 1 other than P divides
the cofactor c = (n_P^2 + 1)/P <= (n_P^2 + 1)/(2 n_P + 1) < n_P,
so it is below n_P and its square is below b. (b) B = a(a+1) = L,
b-smooth, v_p(B) = 1 at good primes (a good prime divides exactly
one endpoint, to the first power, since p^2 > b), no bad primes.
(c) (A+1)/B = (2a+2)/(a(a+1)) = 2/a, not an integer for a >= 4.
(d) Distinctness and infinitude: if the intervals were finite in
number, the values a + 1 would form a finite set with finitely
many prime divisors, but P | (a_P + 1) for every P in the infinite
set of Lemma 1.2, a contradiction. All steps correct; the family
recomputed from the sieve definition for all 44 primes
P = 1 (mod 4) with P <= 500 in V2, 0 failures (P1 = {P} exactly,
B = a(a+1) = L, the congruence mod P^2, v_P(B) = 1,
(A+1)/B = 2/a, 44 distinct intervals).

Refutation. Each family interval has P1 nonempty, b arbitrarily
large (infinitely many distinct intervals), and its own
denominator candidate B is a b-smooth member of the forced class
with B <= L. So (H-sieve) fails for every B_0, and the
single-candidate weakening of TARGET.md Remark 2 (it suffices
that B not lie in the class) fails at the same intervals. The
family lies in regime (i) (R = 2, fixed) and in regime (ii)
(2 n_P^2 > n_P^2 + 1 for n_P >= 2), so the refutation applies in
each regime separately as well. Correct. For the record, Prover
1's family F1 (singleton intervals (p(p-1), p(p-1)), least
residue r_0 = p, b-smooth and <= L) also refutes (H-sieve) as
stated, since (H-sieve) excludes every smooth class member; but
in F1 the candidate B is not in the class, so F1 does not refute
the single-candidate weakening. Theorem F is the result that
refutes both forms; that distinction is part of the certified
record.

## 4. Verifier's computational coverage (exact arithmetic)

Code `clusters/E/verifier_checks.py`, output
`clusters/E/verifier_output.txt`. The verifier's first run of V2
contained a verifier-side error (the forced residue was computed
with (T_P)^{-1} replaced by T_P); it was caught because 37 of 44
class checks failed against two proved routes, the formula was
corrected to -P * (u mod P), and the full run was repeated clean.
The final numbers below are from the corrected, complete run.

- V0, analytic bounds. ln 2 series bound: term ratios < 1/9
  (checked k = 0..29), bound value exactly
  2458234657/3546482940 < 111/160 with exact difference
  17103061/28371863520; 1/18 + 111/160 = 1079/1440 < 3/4, margin
  1/1440. Riemann sum (1/4)(1 + 4/5 + 2/3 + 4/7) = 319/420
  exactly. Combination 319/420 + 1/17 + 1/16 = 25157/28560 < 1.
- V1, regime (ii) classification. All 250,500 intervals with
  a > b/2 and b <= 1000, H computed exactly by a descending
  Fraction sweep, solutions tested by (A+1) mod B = 0 (Lemma 1's
  candidate). Solutions found: exactly (1,1,1), (2,2,2), (2,3,6).
- V2, Theorem F. All 44 primes P = 1 (mod 4) with P <= 500:
  P1 exactly {P} by the sieve definition (scan of every odd prime
  p with p^2 > b having a multiple in [a,b], T_p computed in F_p),
  B = a(a+1), B = L, B in the forced class (congruence mod P^2),
  v_P(B) = 1, (A+1)/B = 2/a not an integer, 44 distinct
  intervals, 0 failures.
- V3, window 2-adic claim. All 21,066 window intervals
  (b/2 < a <= (2b+2)/3, R >= 2) with 32 <= b <= 500: maximum of
  v_2 attained exactly once, s >= t - 1, v_2(H) = -s,
  v_2(B) = s, B >= 2^s >= 16; 0 failures.
- V4, strip prime claim. All 20,898 strip intervals
  (b/2 < a, 3a <= 2b + 1) with 34 <= b <= 500, and every prime
  ell in (b/4, b/2) for each: 332,675 (interval, prime) pairs,
  k(ell) >= 1 in every pair, ell^2 > b and ell >= 11 throughout,
  T_ell values: 1/2 in 219,155 pairs, 1/3 in 55,998 pairs,
  5/6 in 57,522 pairs, nonzero in F_ell in every pair; 0 failures.
- V5, chain inequality. All 124,750 intervals with b <= 500 and
  R >= 2: (A+1)/B < 2R/a, and both components H < R/a and
  1/B < R/a; 0 failures.
- V6, census and thresholds. AUDIT-B's six solutions filtered by
  strict a > b/2 give exactly the three of S1; the solutions
  excluded with a = b/2 exactly are (1,2,2) and (3,6,20).
  R = 1: 2/a is an integer for a <= 2000 exactly at a in {1,2}.
- V7, Lemma 1.1 readings. For a <= 3000: the corrected odd-prime
  form of (alpha) and (beta) matches (P1 nonempty and B in class)
  with 0 mismatches; the literal printed form mismatches exactly
  at a = 1 and a = 2 (see D-E1).

Coverage boundary, stated plainly: computation is corroboration
for the proofs in Section 3, which are complete without it; the
ranges above are the ranges actually computed by the verifier,
and no coverage beyond them is claimed.

## 5. Status of TARGET.md after C4: what is killed and what is not

Certified by S3: the pointwise hypothesis (H-sieve), as stated in
TARGET.md for 13R and as the first conjunct of 13R+, is **false
for every B_0**. The Theorem F intervals are counterexamples with
P1 nonempty, at arbitrarily large b, in both restricted regimes.
TARGET.md Remark 4's status line is therefore superseded: (H-sieve)
is no longer "an asymptotic statement whose truth is open"; it is
refuted.

What this kills.

- (H-sieve) itself, in both its forms in TARGET.md: the full form
  (no b-smooth m <= L in the class) and the single-candidate
  weakening of Remark 2 (B(a,b) not in the class). Both fail at
  the Theorem F intervals.
- The applicability of 13R and of 13R+. The implications 13R and
  13R+ themselves remain logically valid, with correct proofs
  (certified in AUDIT-B.md and TARGET.md); but 13R's hypothesis is
  (H-sieve), and 13R+'s hypothesis is the conjunction of (H-sieve)
  with (H-blind). Since the (H-sieve) conjunct is false for every
  B_0, both hypotheses are unsatisfiable, both implications are
  vacuous as routes to finiteness, and neither can ever be applied
  to conclude finiteness. This is the same status AUDIT-B.md
  assigned to the note's original Theorem 13, now extended to the
  campaign's repair.
- Any exclusion strategy, in either regime, whose only input is
  the forced class and the structural properties listed in S4.

What this does not kill.

- (H-blind) as a statement. (H-blind) says there is no solution
  with P1(a,b) empty and b >= B_0. The Theorem F intervals have
  P1 = {P}, nonempty, so they neither prove nor refute (H-blind),
  and Prover 1's families do not either (F1 has P1 nonempty; F2
  has P1 empty but is not a solution). Status of (H-blind) after
  C4, exactly: unchanged, still open as a global asymptotic
  statement, neither proved nor refuted by anything in Cluster E.
  It is, however, now moot as a component of 13R+: completing it
  could not revive 13R+, whose other conjunct is false.
- The logical validity of 13R and 13R+ as implications (above),
  and all certified inputs: Lemmas 1 and 2, the CRT reduction,
  the census.
- The finiteness question for the singleton case in general.
  Cluster E closes regimes (i) and (ii) by arguments outside the
  class (S4); it does not close, and C4 does not bear on,
  intervals outside those regimes (for example a <= b/2 with R
  growing with b).

## 6. Defects found in the prover files, stated exactly

Scope note: this section records every defect the verifier found
in the material supporting C1 to C4 and their supporting lemmas.
Auxiliary computational maps in the prover files that are not
load-bearing for C1 to C4 (for example Prover 2's Section 1.5
counts and Prover 1's least-residue tables) were not themselves
certified here; the red team's independent reproductions of them
are recorded in redteam.md.

- D-E1 (Prover 2, Lemma 1.1, statement only; does not affect any
  claim). The printed conditions (alpha) and (beta) quantify over
  "prime divisor p" without restricting to odd primes, and in that
  literal reading the lemma's if-and-only-if is false at exactly
  two small cases (verifier V7, a <= 3000):
  a = 1: literal (alpha) holds vacuously and literal (beta) holds
  via p = 2 (2 divides a + 1 = 2 and 2^2 > 2), so the literal form
  predicts "P1 nonempty and B in class"; in fact P1(1,2) is empty,
  so the conjunction is false.
  a = 2: literal (alpha) fails via p = 2 (2 divides a and
  2^2 > 3), so the literal form predicts the conjunction is false;
  in fact P1(2,3) = {3} and B = 6 satisfies the forced congruence
  mod 9 (residue 6), so the conjunction is true.
  The lemma's proof quantifies over odd primes throughout, the
  note following it reads (alpha) as a statement about odd prime
  factors, and Prover 2's Part 2 code implements the conditions
  with p != 2; the corrected odd-prime form has 0 mismatches for
  a <= 3000 (V7). The two readings coincide for all a >= 3. The
  Theorem F application has a >= 4. No conclusion in C1 to C4 is
  affected. The prover file was not patched, per instructions;
  the correction is recorded here and in Q3.
- D-E2 (Prover 2, Theorem II, window case; expository compression,
  not an error). The sentence deriving v_2(B) = s says
  "v_2(B) >= 1 forces v_2(A) = 0 (gcd(A,B) = 1)", taking
  v_2(B) >= 1 as a premise at that point. The premise follows
  immediately from the preceding line: v_2(A) - v_2(B) = -s < 0
  gives v_2(B) = v_2(A) + s >= s >= 1, after which gcd(A,B) = 1
  indeed forces v_2(A) = 0 and v_2(B) = s. With that one line
  supplied, the argument is complete and correct; the verifier
  supplied it, and V3 verifies the conclusion directly.
- No defect found in the restored prover1.md. For the record: the
  red team's two non-breaking findings against Prover 1 concerned
  the file as originally filed (truncated, with the b >= 34 proof
  absent) and the coordinator's sketch (the inequality H < R/a
  stated without the R = 1 caveat). In the restored file the proof
  is present in full, and the caveat is carried explicitly in
  Theorem I and in subregime A of Theorem II; neither finding
  applies to the restored text that was certified here.

Nothing was posted, emailed, or submitted.
