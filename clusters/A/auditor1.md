# Auditor 1 (Cluster A, Cycle 1): Line-by-line audit of Nayak, Theorem 3.2 and Lemma 3.1

**Target.** Theorem 3.2 (intersecting intervals) and Lemma 3.1 of Ritvik Nayak,
"A Research Note on Harmonic Sums over Two Integer Intervals" (May 2026), audited
by following the note's own argument exactly as written, together with the tools
the note itself supplies in Section 2 (Lemma 2.1; Corollary 2.2 is not used in
Section 3).

**Source.** `sources/Nayak-2026.txt`, Sections 2 and 3 (PDF cross-checked for the
statements; the extraction of Sections 2–3 is clean). Method: every inference
reconstructed and checked in order; all numeric claims recomputed in exact
rational arithmetic (Section 4 below). Verdict codes: **V** = fully verified;
**U** = correct but under-justified/compressed in the text; **W** = wrong as
written.

---

## 1. Step-by-step audit

### 1a. Lemma 2.1 (the tool Section 3 relies on)

| # | Step (as written) | Verdict | Check |
|---|---|---|---|
| L2.1-1 | Statement: if exactly one term µᵢ/nᵢ attains the minimum p-adic valuation and that minimum is negative, then S is not an integer, and in fact v_p(S) equals that minimum. | V | Standard ultrametric fact; hypotheses are exactly what Theorem 3.2 produces (see T4). µ_i0 ≠ 0 is forced by "minimum negative", so v_p(µ_i0) is defined. |
| L2.1-2 | Proof: scale by p^e (minimum = −e < 0); all other terms become divisible by p in Z_p, the i0-term becomes a p-adic unit, so p^e·S is a unit. | V | After scaling every term has valuation ≥ 0, so all lie in Z_p; the non-i0 terms have valuation ≥ 1; a unit plus a multiple of p in Z_p is a unit. Hence v_p(S) = −e. Correct and complete. |

### 1b. Lemma 3.1: "If s ≥ 3 and [r,s] has length ≥ 2, some odd prime divides exactly one integer in [r,s]"

Preliminary: the note never defines "length" of an interval in Section 3. The
only reading consistent with the rest of the note (L = d−c+1, R = b−a+1 in
Section 1) and with Theorem 3.2's case split (length 1 vs length 2) is
**length = cardinality N = s−r+1**. Under that reading everything below is
coherent. Logged as ambiguity D1.

Set N = s−r+1 ≥ 2. The proof splits on r ≤ s/2 vs r > s/2, then on r > N vs
r ≤ N. The split is exhaustive.

| # | Step (as written) | Verdict | Check |
|---|---|---|---|
| 3.1-1 | Case r ≤ s/2, s = 3 or 4: "the prime 3 gives the claim by direct inspection." | V | s=3 forces r=1, interval [1,3]; s=4 forces r ∈ {1,2}, intervals [1,4], [2,4]. In each, 3 divides exactly one member (3 itself). Verified by enumeration and by computation (§4). |
| 3.1-2 | Case r ≤ s/2, s ≥ 5: Bertrand gives s/2 < p ≤ s; p is odd, lies in [r,s], 2p > s, so p divides exactly one member. | V (one U, see D2) | p > s/2 ≥ r puts p in [r,s]; p > s/2 ≥ 5/2 forces p ≥ 3, hence odd (text asserts oddness without this one-line reason). 2p > s excludes multiples 2p, 3p, … above p, and the only positive multiple below p is none, so p's unique multiple in [r,s] is p itself. Bertrand is applied inside its valid range (s ≥ 5; the needed form "prime in (s/2, s]" is a standard restatement of Bertrand, valid here). |
| 3.1-3 | Case r > s/2, r > N: all N integers exceed N; Sylvester–Schur gives a prime divisor p > N of their product. | V (one U, see D3) | This is the standard Sylvester–Schur statement (product of N consecutive integers each > N has a prime factor > N); hypotheses are met exactly: N ≥ 2 and the smallest member r > N, hence also s > N. The note names the theorem (end of Section 2) but does not restate its hypotheses; the application is within range. Spot-checked computationally (§4). |
| 3.1-4 | "Since the interval has length N, such a prime can divide at most one term. Also p > N ≥ 2, so p is odd." | V / U | p > N ≥ 2 gives p > 2, so the prime p is odd: correct. "At most one term" is correct but the reason is not spelled out: two distinct multiples of p in [r,s] differ by ≥ p > N > s−r = N−1, impossible. Since p divides the product, it divides ≥ 1 term; hence exactly one. Compressed, not wrong (D3). |
| 3.1-5 | Remaining case r > s/2, r ≤ N: r ≤ s−r+1 gives s ≥ 2r−1; r > s/2 gives s < 2r; hence s = 2r−1. | V | Pure integer arithmetic: s < 2r ⇒ s ≤ 2r−1; combined with s ≥ 2r−1 gives equality. Note s ≥ 3 forces r ≥ 2 in this branch (used silently in the next step). |
| 3.1-6 | Bertrand gives r < p < 2r = s+1; so p ∈ [r,s], p odd, 2p > s, p divides exactly one member. | V (one U, see D2) | Bertrand in its textbook form needs r > 1: here r ≥ 2 (from s = 2r−1 ≥ 3), but the text does not state this. p > r ≥ 2 gives p ≥ 3, hence odd (asserted, not derived, in the text). p < s+1 and p integer give p ≤ s; p > r gives p ∈ [r,s]. 2p > 2r > 2r−1 = s, and the unique-multiple argument is as in 3.1-2. Correct. |

**Lemma 3.1 as a statement**: independently confirmed by exhaustive search for
all 19,899 intervals with 1 ≤ r ≤ s ≤ 200, s ≥ 3, N ≥ 2 — no counterexample (§4).

### 1c. Theorem 3.2

| # | Step (as written) | Verdict | Check |
|---|---|---|---|
| T1 | "Since I ∩ J ≠ ∅, the union is an interval [r,s]." | V | Two intersecting integer intervals have interval union: union = [min of left endpoints, max of right endpoints], and the intersection hypothesis is exactly what fills any potential gap. Uses nonemptiness of intervals (standing convention, Section 1). |
| T2 | Write H(I)+H(J) = Σ_{n=r}^{s} µ(n)/n with µ(n) = 1_{n∈I} + 1_{n∈J} ∈ {1,2}. | V | Exact rewriting: every n ∈ [r,s] lies in at least one of I, J (it is in the union), so µ(n) ∈ {1,2}; terms counted with multiplicity reproduce the sum. Crucially, *every* integer of [r,s] occurs as a denominator — this is where intersecting (vs merely disjoint) is used, and it is what lets Lemma 3.1's prime hit an actual term. |
| T3 | Case s ≥ 3, length ≥ 2: Lemma 3.1 gives an odd prime p dividing exactly one denominator n₀; write p^e ∥ n₀. | V | Hypotheses of Lemma 3.1 match exactly. p | n₀ gives e ≥ 1 (not stated, but immediate from p^e ∥ n₀). |
| T4 | "Since p is odd and µ(n₀) ∈ {1,2}, µ(n₀) is not divisible by p. The term µ(n₀)/n₀ is therefore the unique lowest p-adic layer, contradicting Lemma 2.1." | V / U | The conclusion is correct, and this is exactly where **oddness is essential**: v_p(µ(n₀)) = 0 for odd p, so v_p(term) = −e < 0. For every other n, p ∤ n (Lemma 3.1) and v_p(µ(n)) = 0 (p odd, µ ∈ {1,2}), so every other term has valuation 0 > −e. Hence a unique negative minimum, and Lemma 2.1 gives v_p(sum) = −e, so the sum is not an integer. The text compresses the comparison for the *other* terms into "therefore"; the computation is not displayed (D4). **Coefficient-2 check:** the overlap multiplicity µ = 2 breaks nothing here, precisely because p is odd. At p = 2 it would break: v_2(2/2) = 0 ≠ v_2(1/2) = −1, i.e. µ = 2 raises the valuation and can destroy unique minimality (demonstrated in §4). The argument correctly never uses p = 2. |
| T5 | Length-1 union: "both intervals are [r,r], and the total is 2/r, integral only for r = 1, 2." | V | Union a single integer forces I = J = [r,r] (both nonempty). 2/r ∈ Z with r ≥ 1 iff r | 2 iff r ∈ {1,2}. Yields ([1,1],[1,1]) and ([2,2],[2,2]). Also silently disposes of length-1 unions with s ≥ 3 (2/r not integral), which the case split needs — correctly. |
| T6 | Union contained in {1,2}, length 2: "direct checking gives exactly the four listed pairs." | **W as worded** (proof total still correct) | The subcase itself (union exactly [1,2]) contains three intersecting pairs up to swap: ([1,2],[1,2]), ([1,2],[1,1]), ([1,2],[2,2]); direct checking leaves only the first and third (sums 3 and 2; ([1,2],[1,1]) has sum 5/2). The other two listed pairs come from T5, not from this subcase. So the sentence over-attributes: this branch alone gives 2 of the 4 pairs, not "exactly the four". The full proof (T5 + T6) does yield exactly the four. See D5. The pair ([1,1],[2,2]) also has union [1,2] but is disjoint, so it is outside the theorem's hypothesis (its sum 3/2 is non-integral anyway). |
| T7 | Exhaustiveness of the case split. | V | Every union [r,s] falls in exactly one of: length ≥ 2 and s ≥ 3 (T3–T4, no solutions); length 1 (T5); length ≥ 2 and s ≤ 2, which forces [r,s] = [1,2] (T6). No configuration is missed, including s ≥ 3 with length 1 (in T5) and unions inside {1,2} of length 1 (in T5). |
| T8 | "All four pairs work." | V (values not displayed in the note) | Verified by exact computation (§4): sums are 2, 3, 2, 1 respectively. The note asserts this without showing the sums; the reader's check it invites does succeed. |

**Boundary configurations specifically probed** (per assignment): single-element
union (T5, complete); unions inside {1,2} (T5+T6, complete up to D5's wording);
s ≥ 3 with N ≥ 2 (T3–T4, complete); Bertrand at s = 3, 4 (bypassed by direct
inspection, 3.1-1) and at r = 2 in the s = 2r−1 branch (3.1-6, valid);
Sylvester–Schur at N = 2 (smallest allowed length, valid, §4 spot check);
p = 2 (never used, and provably unusable because of µ = 2, T4).

---

## 2. Defects and gaps found (exact list)

No defect affects the truth of Lemma 3.1 or Theorem 3.2, and no step of the
core argument (T1–T5, T7; 3.1-1–3.1-6) is wrong. The complete list of issues,
all minor, is:

- **D1 (ambiguity, Lemma 3.1 statement / Theorem 3.2 proof).** "Length" of an
  interval is never defined in Section 3. It must be read as cardinality
  s−r+1 (consistent with L, R in Section 1 and with the length-1/length-2 case
  split); under the alternative reading s−r the case split would not parse.
  A one-line definition is the needed repair.
- **D2 (under-justification, Lemma 3.1, steps 3.1-2 and 3.1-6).** "p is odd"
  is asserted without derivation in both Bertrand branches. The derivations
  are one line each (branch 1: p > s/2 ≥ 5/2; branch 3: p > r ≥ 2, where
  r ≥ 2 itself follows from s = 2r−1 ≥ 3 and is also the hypothesis Bertrand
  needs), but as written the reader must supply them, including the fact that
  branch 3 has r ≥ 2 so Bertrand applies.
- **D3 (under-justification, Lemma 3.1, steps 3.1-3/3.1-4).** Sylvester–Schur
  is invoked by name without restating its hypotheses, and "can divide at most
  one term" is asserted without the difference argument (two multiples differ
  by ≥ p > N > N−1 = s−r). Both are standard and the application is in range,
  but the text does not show the fit.
- **D4 (under-justification, Theorem 3.2, step T4).** The key valuation
  comparison is compressed to one "therefore": the text shows µ(n₀) is not
  divisible by p but does not display that every *other* term has valuation
  0 > −e (which uses both halves of Lemma 3.1's conclusion: p divides no other
  denominator, and v_p(µ(n)) = 0 since p is odd). Also e ≥ 1 is left implicit.
  The inference is valid; the display is missing.
- **D5 (wording error, Theorem 3.2, step T6).** "Direct checking gives exactly
  the four listed pairs" is false for the subcase it is attached to (union
  contained in {1,2} with length 2): that subcase alone yields only
  ([1,2],[1,2]) and ([1,2],[2,2]); ([1,1],[1,1]) and ([2,2],[2,2]) come from
  the preceding length-1 sentence. Repair: reword to "together with the
  previous case, this gives exactly the four listed pairs", ideally with the
  rejected pair ([1,2],[1,1]) (sum 5/2) named. This is a presentational
  defect only; the classification the proof establishes is correct.

Nothing else was found: in particular, the coefficient-2 overlap does **not**
break the unique-lowest-valuation argument anywhere it is used, because the
prime supplied by Lemma 3.1 is always odd; the Bertrand and Sylvester–Schur
applications are all inside their valid ranges; and all boundary configurations
are enumerated.

---

## 3. Overall verdict

**PROVED WITH GAPS LISTED** — for both Lemma 3.1 and Theorem 3.2, as written.

Reasons: every substantive inference in the note's own line of argument checks
out exactly as written (Sections 1a–1c, all steps V except as noted), the lemma's
statement and the theorem's classification are independently confirmed by exact
computation (Section 4), and the four listed pairs do have integer sums. The
verdict is not "PROVED AS WRITTEN" because of the five logged items in Section 2:
one undefined term (D1), three places where a needed one-line justification is
asserted rather than shown (D2, D3, D4), and one sentence that misattributes
which subcase produces the four pairs (D5). All five are minor and repairable
without changing any argument; none is a logical error in the core proof, so
the verdict is not "NOT PROVED AS WRITTEN".

---

## 4. Computations run and results

Code: `auditor1_checks.py` in this directory (Python `fractions.Fraction`
exact arithmetic throughout; primality by trial division).

1. **The four pairs.** H([1,1])+H([1,1]) = 2; H([1,2])+H([1,2]) = 3/2+3/2 = 3;
   H([1,2])+H([2,2]) = 3/2+1/2 = 2; H([2,2])+H([2,2]) = 1/2+1/2 = 1. All integers. ✔
2. **Rejected neighbour pairs.** ([1,2],[1,1]): sum 5/2, not an integer (the pair
   D5 concerns). ([1,1],[2,2]) (disjoint, outside the hypothesis): sum 3/2.
3. **Length-1 unions.** 2/r is an integer only for r = 1, 2 (checked r = 1…10;
   in general r | 2).
4. **Lemma 3.1 statement, exhaustive.** For all 19,899 intervals with
   1 ≤ r ≤ s ≤ 200, s ≥ 3, N ≥ 2: an odd prime dividing exactly one member
   always exists. Failures: none.
5. **Branch checks.** s = 2r−1 branch: for r = 2…60 a Bertrand prime in (r, 2r)
   exists, is odd, and divides exactly one member of [r, 2r−1]. Failures: none.
   s ∈ {3,4}, r ≤ s/2: prime 3 divides exactly one member in [1,3], [1,4], [2,4].
   Sylvester–Schur branch: for N = 2…12 and r = N+1…N+30, a prime divisor
   p > N of the product exists and divides exactly one member. Failures: none.
6. **Theorem 3.2, brute force.** All ordered pairs of intervals inside [1,30]
   that intersect: exactly 5 have integer sum — the 4 listed unordered pairs,
   with ([1,2],[2,2]) appearing in both orders. Matches the theorem exactly.
7. **Valuation mechanism (T4).** Example union [2,4] with µ = (1,2,1) at p = 3:
   valuations are {n=2: 0, n=3: −1, n=4: 0} — unique negative minimum at the
   overlapped term despite µ = 2. And the p = 2 failure mode: v₂(2/2) = 0 vs
   v₂(1/2) = −1, while v₃(2/3) = v₃(1/3) = −1 — confirming oddness of p is the
   load-bearing hypothesis for the coefficient-2 case.
