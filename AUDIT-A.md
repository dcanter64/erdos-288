# AUDIT-A.md — Cluster A, Cycle 1: Certified record for Nayak Theorem 3.2 and Lemma 3.1

**Subject.** Ritvik Nayak, "A Research Note on Harmonic Sums over Two Integer
Intervals" (May 2026), Sections 2–3: Lemma 3.1 and Theorem 3.2 (the intersecting
case of Erdős Problem #288). Source text: `sources/Nayak-2026.txt`.

**Verifier protocol.** The verifier wrote and ran its own checks first
(`clusters/A/verifier_checks.py`, `clusters/A/verifier_check3_scope.py`,
results in `clusters/A/verifier_results.json`), using exact rational arithmetic
only (`fractions.Fraction` / integer arithmetic), and only afterwards read the
producer reports (`auditor1.md`, `auditor2.md` with `auditor2_draft_proof.md`,
`redteam.md`, with their code beside them). Defects below are quoted as found;
the note's text has not been repaired or paraphrased into correctness anywhere
in this record.

---

## 1. Theorem 3.2 — verdict: CERTIFIED WITH LOCATED DEFECTS

The theorem is true and the note's argument proves it: every substantive step
(the union rewriting with coefficients μ(n) ∈ {1,2}, the appeal to Lemma 3.1's
odd prime dividing exactly one denominator, the unique-lowest-p-adic-layer
contradiction via Lemma 2.1 at a negative minimum, the singleton case 2/r, and
the exhaustive case split) was reconstructed and checks out, and the
classification is independently confirmed by exact computation (verifier:
endpoints ≤ 60, exactly the four pairs out of 1,117,520 intersecting unordered
pairs; Red Team: endpoints ≤ 1000, same four, reproduced by a second modular
implementation). The located defects (Section 4 below) are one wording error
in the proof's final sentence and several exposition gaps; none affects the
validity of the argument or the truth of the statement, because each missing
justification is fillable in one or two lines from facts already in the note,
and the misattributed final sentence is backed by the preceding length-1 case
which does supply the remaining two pairs. Hence certification, with the
defects on record rather than a clean "as written" pass.

## 2. Lemma 3.1 — verdict: CERTIFIED WITH LOCATED DEFECTS

The lemma is true and its proof's three branches (Bertrand for r ≤ s/2, with
s = 3, 4 by inspection; Sylvester–Schur for r > s/2 with r > N; the forced
s = 2r − 1 borderline with Bertrand again) are each valid and together
exhaustive, with every application inside the invoked theorem's range. The
verifier confirmed the lemma's predicate for all r < s ≤ 500 with s ≥ 3 (zero
failures; the sole failure over all r < s ≤ 500 is (1,2), which has s = 2 and
is outside the lemma's hypothesis), and the Red Team confirmed it to s ≤ 2000.
The located defects touching the lemma (undefined "length"; "p is odd"
asserted without derivation in the two Bertrand branches; Sylvester–Schur's
hypotheses not restated and the "at most one term" step compressed) are
exposition gaps only and do not affect validity.

---

## 3. Verifier's independent checks: coverage and results

All in `clusters/A/verifier_checks.py` unless noted; exact arithmetic only.

1. **The four pairs and the near-miss.** H-sums, exactly:
   ([1,1],[1,1]) = 2; ([1,2],[1,2]) = 3; ([1,2],[2,2]) = 2; ([2,2],[2,2]) = 1 —
   all integers, so all four listed pairs work. The near-miss ([1,1],[1,2])
   has sum exactly 5/2, not an integer. **Pass.**
2. **Exhaustive intersecting check, endpoints ≤ 60.** All 1,117,520 unordered
   intersecting interval pairs with endpoints in [1,60] were summed exactly.
   Integer sums occur for exactly the four listed pairs and no other.
   **Pass.**
3. **Lemma 3.1 predicate, r < s ≤ 500** (`verifier_check3_scope.py`). All
   124,750 intervals tested: an odd prime dividing exactly one integer in
   [r,s] exists in every case with s ≥ 3. The only failure in the whole range
   is (r,s) = (1,2), where s = 2 < 3, outside the lemma's hypothesis.
   **Pass, in scope.**
4. **Valuation mechanism spot-check, including coefficient-2 overlap.** 486
   intersecting pairs (I,J) with union [r,s], s ≥ 3, at least two elements —
   systematic small cases, random cases with endpoints up to 500, and forced
   overlap cases — were checked at the odd prime p the verifier's own code
   finds for [r,s]. In every case: p divides exactly one denominator n₀;
   writing e = v_p(n₀) ≥ 1, the term valuation v_p(μ(n₀)/n₀) is exactly −e,
   every other term has valuation ≥ 0 > −e, the minimum is unique, and the
   exact total satisfies v_p(H(I)+H(J)) = −e < 0 (never an integer), exactly
   as Lemma 2.1's application in the proof requires. In 322 of the 486 cases
   n₀ lay in the overlap I ∩ J, i.e. μ(n₀) = 2, and the mechanism was
   unaffected, because p odd makes μ(n₀) ∈ {1,2} a p-adic unit. Example:
   I = [2,11], J = [7,8], union [2,11], p = 7, n₀ = 7, μ(n₀) = 2, e = 1,
   v₇(total) = −1. **Pass.**

Producer computations (not the verifier's, recorded for convergence): Auditor 1
— brute force to endpoints ≤ 30 (ordered), Lemma 3.1 exhaustive to s ≤ 200,
branch and Sylvester–Schur spot checks, all clean. Auditor 2 — brute force to
≤ 28, Lemma 3.1 to s ≤ 200, both case splits' witnesses to s ≤ 500, Sylvester
product form instances, all clean. Red Team — exhaustive exact search to
N = 1000 (500,500 intervals; the only integer-sum pairs anywhere are the seven
known examples), an independent two-modulus implementation agreeing after
exact rejection of one collision, Lemma 3.1 predicate to s ≤ 2000, and a
valuation-gap probe over 3,159 unions, all clean.

---

## 4. Merged, adjudicated defect list — the intersecting-case proof (Sections 2–3)

Severity key: **affects validity** / **wording only** / **exposition gap**.
Convergence is noted where independent producers found the same item.

### A-D1. "Length" is never defined — CONFIRMED — wording only / exposition gap
Location: Lemma 3.1 statement ("s ≥ 3 and length at least 2") and Theorem 3.2's
proof ("the union has length at least 2"; "If the union has length 1, both
intervals are [r, r]"). The note nowhere defines the length of an interval in
Section 3. The text is coherent only under the cardinality reading
length = s − r + 1 (consistent with L = d − c + 1, R = b − a + 1 in Section 1
and with Lemma 3.1's own N = s − r + 1); under the alternative reading s − r
the length-1 conclusion quoted above would be false. Logged independently by
Auditor 1 (its D1) and Auditor 2 (its item 10), and the verifier confirms no
definition appears in the source text. No step fails under the intended
reading, so this does not affect validity.

### A-D2. "p is odd" asserted without derivation in both Bertrand branches of Lemma 3.1 — CONFIRMED — exposition gap
Location: Lemma 3.1 proof, branch r ≤ s/2, s ≥ 5 ("This prime is odd") and
branch s = 2r − 1 ("p ∈ [r, s], p is odd"). In neither place is oddness
derived. The derivations are one line each (branch 1: p > s/2 ≥ 5/2, so
p ≥ 3; branch 3: p > r ≥ 2, where r ≥ 2 follows from s = 2r − 1 ≥ 3 and is
also what Bertrand's postulate needs), but the reader must supply them. (In
the Sylvester–Schur branch the note does derive it: "p > N ≥ 2, so p is odd".)
Logged by Auditor 1 (its D2); the verifier confirms the assertions stand
underived in the printed text and that the one-line derivations are correct.

### A-D3. Sylvester–Schur invoked without restated hypotheses; "at most one term" compressed — CONFIRMED — exposition gap
Location: Lemma 3.1 proof, branch r > s/2, r > N. The note names
Sylvester–Schur (at the end of Section 2) without restating its hypotheses,
and asserts "Since the interval has length N, such a prime can divide at most
one term" without the difference argument (two distinct multiples of p differ
by at least p > N > s − r = N − 1). The application is in range (N ≥ 2
consecutive integers, each ≥ r > N) and the conclusion correct, but the fit
is not shown. Logged by Auditor 1 (its D3); Auditor 2 independently restated
the theorem in exactly the needed product form and verified its instances,
and the verifier's predicate check (Section 3, item 3) is consistent with it
throughout the tested range.

### A-D4. The valuation comparison in Theorem 3.2 is compressed to one "therefore" — CONFIRMED — exposition gap
Location: Theorem 3.2 proof: "Since p is odd and µ(n₀) ∈ {1, 2}, the
coefficient µ(n₀) is not divisible by p. The term µ(n₀)/n₀ is therefore the
unique lowest p-adic layer, contradicting Lemma 2.1." The text does not
display that every other term has valuation 0 > −e (which uses both halves of
Lemma 3.1's conclusion: p divides no other denominator, and v_p(µ(n)) = 0 for
odd p), and e ≥ 1 is left implicit. Logged by Auditor 1 (its D4). The
inference is valid; the verifier's check 4 (Section 3 above) verifies the
full comparison exactly in 486 cases, 322 of them with µ(n₀) = 2, so the gap
is in the display, not the mathematics.

### A-D5. Final sentence of Theorem 3.2's proof misattributes the four pairs — CONFIRMED — wording only
Location: Theorem 3.2 proof, final sentence, quoted as found: "If the union
is contained in {1, 2} and has length 2, direct checking gives exactly
the four listed pairs." (Source text, `sources/Nayak-2026.txt`, lines
229–230, end of the proof.) Read as written, the sentence is false for the
subcase it is attached to. A length-2 union contained in {1, 2} is the
union [1, 2] itself, and direct checking of that subcase alone yields
exactly two of the four unordered listed pairs, ([1,2],[1,2]) (sum 3) and
([1,2],[2,2]) (sum 2); the remaining intersecting pair with that union,
([1,1],[1,2]), has sum exactly 5/2 and is not an integer case. The other
two listed pairs, ([1,1],[1,1]) and ([2,2],[2,2]), have unions of length 1
and are delivered by the preceding sentence of the proof, the singleton
case in which both intervals are [r, r] and the total is 2/r, integral
only for r = 1, 2. Read as a summary of the two small cases together the
conclusion is right; read as written, the final sentence misattributes
all four pairs to the length-2 check alone. The proof as a whole does
yield exactly the four pairs, so the defect is in the wording of the
attribution, not in the argument or the classification.
Logged independently by all three producers: Auditor 1 (its D5, which
calls it a wording error and proposes the repair "together with the
previous case, this gives exactly the four listed pairs"), Auditor 2
(its item 9, "mis-counted final sentence", the only inaccuracy it found
in Section 3), and the Red Team (its D2, with the full enumeration in
its Probe B, Part 1). The verifier's own checks are consistent with
that adjudication and are recorded in `verifier_results.json`: check 1
confirms all four listed pairs have integer sums and the near-miss
([1,1],[1,2]) is exactly 5/2, and check 2 confirms exhaustively, over
all 1,117,520 intersecting unordered pairs with endpoints at most 60,
that exactly the four listed pairs have integer sums. The Red Team's
evidence gives the same severity as the heading above (inaccurate as
written, impact none on the theorem statement), so no different
severity follows from its file.

---

## Repair note (added 2026-10-30)

The original file was truncated mid-A-D5 during writing (discovered
2026-10-30); the file ended mid-quotation inside item A-D5, with a
literal truncation marker baked in, and everything from that point
onward was missing. The completion of A-D5 above and Sections 5 and 6
below were written by a follow-up agent from `clusters/A/redteam.md`,
`clusters/A/verifier_results.json` (with `clusters/A/verifier_checks.py`),
and the source text `sources/Nayak-2026.txt`. No verdict above the cut
was changed.

## 5. Whole-note adjudicated items (outside Theorem 3.2's scope, non-blocking)

The items below come from the Red Team's whole-note discrepancy scan
of Sections 1 to 18 and Appendices A and B (`redteam.md`, Sections 2.1
to 2.2, its candidate defects D1 and D3 to D7; its D2 is item A-D5
above, inside Theorem 3.2's scope). Each item is a justification or
wording gap in a statement the scan found true; none of them makes any
stated theorem false, none blocks the certifications in Sections 1
and 2 above, and each disposition below is the Red Team's as recorded
in its report.

### A-W1. The symbol z_b is defined inconsistently between Sections 12 and 13 — CONFIRMED — wording / notation only
Section 12, Theorem 12.1 (source line 707), defines
z_b = max(L, b/((1 − eps) log b)). Section 13 (source line 769)
redefines the same symbol, for the same eps, as
z_b = b/((1 − eps) log b), dropping the max(L, ·). Sections 13 and 14
and Problem 18.1 use the second form, while Theorem 17.1 item (7)
(source line 1184) states the forcing result with the first, max, form.
The partition claim at source line 776 ("Theorem 12.1 says that the
sets S_0, …, S_{L−1} partition the primes in (z_b, b]") is made with
Section 13's z_b, whereas Theorem 12.1 itself only delivers the
partition above its own, larger, z_b. The inconsistency is vacuous in
the regime actually used: from Section 13 on, L is fixed, and for all
sufficiently large b the term b/((1 − eps) log b) exceeds L, so the
two definitions eventually coincide. Red Team candidate D1 (high
confidence the inconsistency is present; impact none in the regimes
actually used).

### A-W2. Theorem 13.3's proof asserts a prime-factor bound it does not justify — CONFIRMED — exposition / justification gap
Location: proof of Theorem 13.3 (source line 820), the step "all prime
factors of u_j are at most z_b". The printed text cites only
u_j | Lambda_b (Theorem 4.2), which by itself does not bound the prime
factors of u_j. The Red Team records the missing argument (its D3):
if a prime q with z_b < q ≤ b divided u_j, it would also divide c + j,
so it would lie in S_j and divide P_j, giving q^2 | c + j; but
q > z_b implies q^2 > b for large b, so q occurs in Lambda_b only to
the first power, contradicting c + j | Lambda_b; and q > b is excluded
by c + j | Lambda_b directly. With that step supplied, the conclusion
u_j | B_b(z_b) and the size bounds follow as printed. The assertion is
true, and Theorems 13.3, 13.5 and 14.2 rest on it, but the two-line
justification is absent from the printed proof.

### A-W3. Theorem 7.1 does not split off the upper exponent at least 2 — CONFIRMED — exposition / justification gap
Location: Theorem 7.1 (source line 427): "The lowest p-adic layer must
cancel against the lower interval." The text then treats the upper
denominator's p-exponent as 1. The case of exponent at least 2 is not
split off (Red Team candidate D4(a)): since p^2 > b, every lower
denominator has p-exponent at most 1, so an upper exponent of at
least 2 would already make the upper term the unique lowest layer,
which is impossible; the argument needs that sentence before
proceeding with exponent 1. The gap is fillable as stated and the
conclusion stands.

### A-W4. Lemma 2.4's vanishing summand needs a second unstated step — CONFIRMED — exposition / justification gap
Location: Lemma 2.4 (source line 162): "If j > v_p(M), then no element
of the interval is divisible by p^j, so A_j = 0 and the summand is 0."
The summand is A_j − floor(L / p^j); its vanishing also needs
floor(L / p^j) = 0, which follows because p^j ≤ L would force a
multiple of p^j among any L consecutive integers, contradicting
A_j = 0 (Red Team candidate D4(b)). That step is not stated. The Red
Team also checked the lemma's statement on finite instances
(`redteam.md`, Section 2.2): C(d, L) divides lcm(c..d) for all 45,150
pairs 1 ≤ c ≤ d ≤ 300, with zero failures.

### A-W5. Lemma 2.1 is proved only for a negative minimum — CONFIRMED — exposition / justification gap
Location: Section 2, Lemma 2.1 (Red Team candidate D5). The
statement's "more precisely" clause says v_p(S) equals the unique
minimum, with no sign hypothesis; the proof begins "Let the unique
minimum be −e < 0", covering only the negative case. The claim is in
fact true for a nonnegative unique minimum as well, by the same
factorisation, but the printed proof does not cover it. The gap has
no effect inside the note, since every application of Lemma 2.1 in
the note has a negative minimum (the application in Theorem 3.2, at
valuation −e < 0, is the Cluster A instance; see item A-D4 above).

### A-W6. Theorem 15.2's ansatz is used before its boundedness is established — CONFIRMED — exposition / justification gap
Location: proof of Theorem 15.2 (source line 1086), writing
a − 1 = e^{−m} b + beta + O(1/b) and then requiring the coefficient of
1/b to vanish (Red Team candidate D6, recorded there at low-medium
confidence). Boundedness of beta_b = (a − 1) − e^{−m} b is not proved
before the expansion is used. The Red Team re-derived the constant
independently: the 1/b coefficient is −beta e^m + (1 − e^m)/2, its
vanishing gives beta = (e^{−m} − 1)/2, and a = (a − 1) + 1 then gives
the printed (1 + e^{−m})/2. The final constant is therefore correct;
the derivation as printed skips the boundedness step. The item is
peripheral asymptotics and does not affect any other result.

### A-W7. "Mutual modular inverses" is the wrong term in Theorem 14.2 — CONFIRMED — wording / terminology only
Location: Theorem 14.2, closing sentence (source line 938), and the
same phrasing in Problem 18.1 (Red Team candidate D7). What is proved
is P_0 u_0 = −1 (mod P_1) and P_1 u_1 = 1 (mod P_0): u_0 is, up to
sign, the inverse of P_0 modulo P_1, and u_1 is the inverse of P_1
modulo P_0. The cofactors u_0 and u_1 are not inverses of each other,
and nothing in the note uses them as such. The displayed congruences
are correct; only the term is inaccurate.

### Closing note on the scan's positive checks
The scan also reran the note's one fully checkable computation, and
it is excluded as a defect on that evidence: the Appendix A script
behind Proposition 16.1 was transcribed verbatim by the Red Team and
rerun at the printed bound B = 2000, and its output,
singleton [(2, 3, 6), (1, 3, 6), (3, 6, 20)] and L2 [], matched the
printed output exactly (`redteam.md`, Section 2.2; rerun log recorded
there as `redteam_appendixA_rerun.log`). Section 2.2 of `redteam.md`
likewise records the other finite claims it checked and found
correct, among them Lemma 2.4's instances (item A-W4 above), Theorem
14.1's denominator identity for all 1 ≤ c ≤ 2000, the Theorem 5.1 and
Theorems 4.2, 6.1, 10.1 instances on the known disjoint solutions,
Lemma 13.2's numerics, the seven known examples' integer sums, the
cross-references of Theorem 17.1 items (1) to (11) (with the z_b form
in item (7) the sole wrinkle, item A-W1 above), and a line-by-line
pass over Sections 4 to 15 that found no further wrong inequality
direction, wrong range, or unsupported cross-reference beyond the
items above.

## 6. Remains unverified

Two points are left open on this record, stated plainly.

**Bertrand's postulate and Sylvester–Schur are taken as standard
literature.** Neither theorem was re-proved by the verifier or by any
producer. What was done, on the evidence on disk, is range-checking
of their applications in Lemma 3.1 (every application inside the
invoked theorem's range, per Sections 1 and 2 above and items A-D2
and A-D3) and finite confirmation of Lemma 3.1's predicate: by the
verifier for all r < s ≤ 500 with s ≥ 3, zero failures in scope
(`verifier_results.json`, check 3), and by the Red Team to s ≤ 2000
(`redteam.md`, Probe D, which also records its case-by-case check of
the proof's branches, including the s = 3, 4 inspections and the
forced s = 2r − 1 borderline). The two named theorems themselves
stand on their published proofs, not on anything in this cluster's
files.

**Which candidate was the forum's flagged "1 minor issue" is
UNRESOLVED.** No record in this cluster, and nothing in the forum
remark as reported in `redteam.md` (forum, 3 May 2026; no detail
exists anywhere), identifies what the unnamed standard check flagged.
The final-sentence defect of Theorem 3.2 (item A-D5) is the leading
candidate, on the ground that all three producers found it
independently (Auditor 1's D5, Auditor 2's item 9, the Red Team's
D2); Auditor 2 likewise calls it a plausible candidate while stating
it cannot confirm the two are the same. The z_b inconsistency (item
A-W1) is the second candidate: the Red Team ranks its D1 and D2 as
its two most plausible candidates for the flagged issue
(`redteam.md`, headline and Section 2.3), while stating plainly that
the identification is a ranking of located candidates, not a
determination, since nothing anywhere records what the unnamed check
flagged. No stronger identification is certified here.