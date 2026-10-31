# Erdős #288, Cycle 1, Cluster A: Red Team report

Scope: (1) try to break Nayak's Theorem 3.2 (intersecting case) by exhaustive exact
search and by boundary probing; (2) hunt the defect an unnamed forum "standard check"
reportedly flagged in Nayak's note (forum, 3 May 2026; no detail exists anywhere).
All computations are exact (Python `Fraction` / integer arithmetic) unless a step is
labelled as a modular filter whose candidates were then verified exactly.
Line references are to the extracted source text `sources/Nayak-2026.txt`.

Headline: **Theorem 3.2 was not broken.** The exhaustive search reached the full
target bound N = 1000 and found no intersecting pair outside the four listed.
**No defect that makes any stated theorem false was located.** Seven candidate
minor defects were located and are ranked in Part 2; the two most plausible
candidates for the flagged "1 minor issue" are a redefinition of `zb` between
Sections 12 and 13 (D1) and a misattributed subcase in the final sentence of the
proof of Theorem 3.2 itself (D2).

---

## Part 1: Task 1, breaking Theorem 3.2

### 1.1 Computational search (exact rational arithmetic)

Method (primary, `redteam_search.py`): prefix sums `prefix[k] = H([1,k])` as exact
Fractions. Every interval `[u,v]` with `1 <= u <= v <= N` is enumerated exactly once;
its sum is `prefix[v] - prefix[u-1]` (exact Fraction) and its canonical fractional
part is stored in a dictionary. A pair has integer sum iff the fractional parts are
complementary mod 1, so the dictionary finds every integer-sum pair of intervals,
intersecting or not; nothing can be missed because the dictionary contains every
interval. Every candidate pair was re-verified by a direct exact Fraction addition
with denominator test. Generation was checkpointed to a pickle after every block
of 50 right endpoints and is resumable from the last completed block.

Coverage actually reached:

| Run | N | Intervals enumerated | Candidate pairs from dictionary | Result |
|---|---|---|---|---|
| Pilot | 120 | 7,260 | 7 | only the 7 known pairs (below) |
| Full | 1000 | 500,500 | 7 | only the 7 known pairs (below) |

Full run timing: last generation checkpoint at 75.7 s; generation plus matching
105.3 s total (`redteam_results_1000.json`, `redteam_search_1000.log`).

Integer-sum pairs found at N = 1000, all positions, unordered, repetition allowed:
exactly seven, namely the four intersecting pairs of Theorem 3.2

- `([1,1],[1,1])`, sum 2
- `([1,2],[1,2])`, sum 3
- `([1,2],[2,2])`, sum 2
- `([2,2],[2,2])`, sum 1

and the three known disjoint singleton pairs

- `([1,3],[6,6])`, sum 2
- `([2,3],[6,6])`, sum 1
- `([3,6],[20,20])`, sum 1

**Intersecting pairs outside the Theorem 3.2 list: none.** The search in fact shows
the stronger finite statement that at N = 1000 there is no integer-sum pair of
intervals of any kind outside the seven known examples.

Independent second implementation (`redteam_verify_modular.py`, a different route):
interval values computed modulo the two primes 1000003 and 1000033 (both > N, so all
denominators are invertible), with the possible integer values bounded by
`0 < H(I) + H(J) < 15` (since `H([1,1000]) < 7.5`, asserted exactly), so a true pair
must match a complementary key for some K in 1..14 under both moduli and cannot
escape the filter. It produced 8 candidates. Seven are the pairs above. One was a
double-modulus collision, `([63,178],[613,806])` with claimed K = 11, and exact
Fraction arithmetic rejects it (its sum is not an integer; the pair is in any case
disjoint, so it never threatened Theorem 3.2). After exact verification the modular
implementation's all-position pair set and intersecting pair set agree with the
primary Fraction search exactly (both agreement flags True in its output).

A third, naive implementation (`redteam_probes.py`, interval sums built term by term,
no prefix sums and no dictionary) brute-forced all ordered intersecting pairs with
endpoints at most 60: exactly 5 ordered integer pairs, namely the four known
unordered pairs with `([1,2],[2,2])` counted in both orders. No unexpected pair.

### 1.2 Boundary probes

Each probe was asked in the form: produce a counterexample, or state precisely why
it cannot. All probes failed to break the theorem, for the reasons stated.
Probe code: `redteam_probes.py`, results in `redteam_probes_results.json`.

**Probe A, union a single element.** If the union is `{r}`, both intervals are
nonempty subsets of `{r}`, so both are `[r,r]` and the sum is `2/r`, integral iff
`r` divides 2, i.e. `r = 1, 2`. These give exactly `([1,1],[1,1])` and
`([2,2],[2,2])` from the list. No other configuration exists in this case, so the
probe cannot produce anything new. (Covered directly by the algebra and by the
search.)

**Probe B, union inside {1,2}.** All 7 intersecting ordered pairs of subintervals
of `[1,2]` were tabulated exactly:

| I | J | Sum | Integer? |
|---|---|---|---|
| [1,1] | [1,1] | 2 | yes (listed) |
| [1,1] | [1,2] | 5/2 | no |
| [1,2] | [1,1] | 5/2 | no |
| [2,2] | [2,2] | 1 | yes (listed) |
| [2,2] | [1,2] | 2 | yes (listed) |
| [1,2] | [2,2] | 2 | yes (listed) |
| [1,2] | [1,2] | 3 | yes (listed) |

(The remaining two ordered pairs, `([1,1],[2,2])` and its swap, are disjoint, hence
out of scope; their sum 3/2 is not an integer anyway.) No unlisted pair. Note for
Part 2: the integer pairs whose union is exactly `[1,2]` are only
`([1,2],[1,2])` and `([1,2],[2,2])` (plus order); see defect candidate D2.

**Probe C, union `[r,s]` with `s = 3`.** Every intersecting ordered pair whose union
is exactly `[1,3]` (13 pairs tested) or exactly `[2,3]` (5 pairs tested) was computed
exactly: no integer sum in either case. The same was done for `s = 4` (unions
`[1,4]`, `[2,4]`, `[3,4]`: 25, 13, 5 pairs tested, no integer sum). Why the proof's
mechanism already works at `s = 3`: the prime 3 divides exactly one integer of
`[r,3]` (the integer 3 itself, for both `r = 1` and `r = 2`), it is odd, so the
combined coefficient `mu(3)` in `{1,2}` is a 3-adic unit and the term `mu(3)/3` has
valuation `-1` strictly below every other term. There is no smaller case with
`s >= 3` and union length at least 2, so the boundary is exactly where the proof
says it is.

**Probe D, Lemma 3.1 predicate at scale.** For every `1 <= r < s <= 2000` with
`s >= 3` it was checked that some odd prime divides exactly one integer in `[r,s]`.
No failures. Method: a prime in `(s/2, s]` (present in the sieve data for every
`s <= 2000`) is itself in `[r,s]` with no second multiple whenever `r` is at most
that prime; the remaining 6,963 pairs `(r,s)`, where `r` exceeds every prime in
`(s/2, s]`, were scanned directly over all odd primes. This is finite support for
the lemma, not a substitute for its Bertrand / Sylvester-Schur proof, which I also
checked case by case (including the edge cases `s = 3, 4` in the `r <= s/2` branch
and the forced equality `s = 2r - 1` in the last branch, where Bertrand's prime
`r < p < 2r = s + 1` lands in `[r,s]` and is odd because `r >= 2` there).

**Probe E, coefficient 2 on the prime's denominator; valuation ties.** This is the
configuration most likely to break the weighted-sum argument, so it was checked
two ways.

- Argument: write the sum over the union `[r,s]` with coefficients
  `mu(n) = 1_{n in I} + 1_{n in J}` in `{1,2}`. Lemma 3.1 gives an **odd** prime `p`
  dividing **exactly one integer** `n0` of `[r,s]`. Let `p^e || n0`, `e >= 1`. For
  the combined term, `v_p(mu(n0)/n0) = v_p(mu(n0)) - e = -e`, because `p` is odd
  and `mu(n0)` is 1 or 2, hence not divisible by `p`. Overlap putting coefficient
  2 on `n0` therefore does **not** shift the valuation; it would shift it only at
  `p = 2`, and the lemma's insistence on an odd prime is exactly what blocks that.
  For every other `n`, `p` does not divide `n` and `mu(n)` in `{1,2}` is again a
  `p`-adic unit, so `v_p(mu(n)/n) >= 0 > -e`. The minimum is unique, and by
  Lemma 2.1 the sum has valuation `-e < 0`. A tie would require a second
  denominator divisible by `p`, which "divides exactly one integer" excludes in
  the strong form: it excludes even a second denominator divisible by `p^e` or
  by `p` to any power. Reduction of the single combined term `mu(n0)/n0` to lowest
  terms cannot remove `p^e` either, since `gcd(mu(n0), p) = 1`; and no numerator
  cancellation from the other terms is possible because they are `p`-adic
  integers while the `n0` term is `p^{-e}` times a unit.
- Computation (probe P5): for every union `[r,s]` arising from intersecting pairs
  with endpoints at most 80 (3,159 unions, i.e. all `r < s <= 80` with `s >= 3`),
  the Lemma 3.1 prime was found and `v_p(mu(n)/n)` was computed for every `n` in
  the union, for a witnessing pair. In all 3,159 cases the value at `n0` was
  strictly smaller than at every other `n`, and the weighted sum was never an
  integer. No violations.

**Probe F, containment versus partial overlap.** The weighted formulation only
sees the union and the multiplicity pattern (1 on the parts covered once, 2 on the
overlap), so the shape of the overlap cannot matter to the proof; the computation
confirms there is nothing hidden in either shape. With endpoints at most 60,
ordered intersecting pairs classified as: equal intervals, 1,830 pairs, integer
sums only the three diagonal known pairs `([1,1],[1,1])`, `([1,2],[1,2])`,
`([2,2],[2,2])`; strict containment, 1,187,670 pairs, integer sums only
`([1,2],[2,2])` in its two orders; partial overlap (intersecting, neither contains
the other), 1,043,710 pairs, **zero** integer sums. The known list's only
containment example is `([1,2],[2,2])`; no partial-overlap example exists even at
this small scale, matching the shape-blind proof.

### 1.3 Task 1 conclusion

No counterexample to Theorem 3.2 was found. The exhaustive exact search reached
N = 1000 in full (500,500 intervals, all integer-sum pairs determined, not only
the intersecting ones), was reproduced by an independent modular implementation,
and every boundary configuration named in the task (single-element union, union
inside {1,2}, `s = 3`, coefficient 2 on the distinguished prime's denominator,
containment versus partial overlap, valuation ties through the coefficient or
through reduction) was either enumerated outright or shown to be blocked by the
odd-prime / exactly-one-denominator properties of Lemma 3.1.

---

## Part 2: Task 2, hunt for the flagged defect

Full-note discrepancy scan of Sections 1 to 18 and Appendices A and B of Nayak's
note, with every checkable finite claim I suspected rerun in exact arithmetic.
Findings first, then the claims that were checked and found correct. Nothing found
makes any stated theorem false; the candidates below are minor in exactly the
sense of the forum remark. I cannot determine which candidate, if any, the unnamed
check flagged; no other discrepancy was located in the scan.

### 2.1 Candidate defects, ranked by confidence

**D1. `zb` is defined inconsistently between Sections 12 and 13.**
Confidence: high that the inconsistency is present; medium that it is the flagged
issue. Impact: none in the regimes actually used.
Location: Section 12, Theorem 12.1 (txt line 707) defines
`zb = max(L, b/((1 - eps) log b))`. Section 13 (txt line 769) redefines, for the
same symbol and the same eps, `zb = b/((1 - eps) log b))`, dropping the `max(L, .)`.
Sections 13 and 14 and Problem 18.1 use the second form, while Theorem 17.1 item
(7) (txt line 1184) states the forcing result with the first (`max`) form.
Evidence: the two displayed definitions as quoted; the partition claim at txt
line 776 ("Theorem 12.1 says that the sets S0, ..., S_{L-1} partition the primes
in (zb, b]") is made with Section 13's `zb`, whereas Theorem 12.1 itself only
delivers the partition above its own larger `zb`. Why it does not break anything:
from Section 13 on, `L` is fixed, and for all sufficiently large `b` the term
`b/((1 - eps) log b)` exceeds `L`, so the two definitions eventually coincide.
As printed, though, a definition is used inconsistently, one of the discrepancy
classes a standard check plausibly flags.

**D2. The last sentence of the proof of Theorem 3.2 misattributes which subcase
gives which pairs.** Confidence: high that the sentence is inaccurate as written;
medium that it is the flagged issue. Impact: none on the theorem statement; the
sentence sits inside the note's headline proof.
Location: proof of Theorem 3.2 (txt lines 229 to 230): "If the union is contained
in {1, 2} and has length 2, direct checking gives exactly the four listed pairs."
Evidence: the length-2 subcase alone yields exactly **two** of the four unordered
pairs, `([1,2],[1,2])` (sum 3) and `([1,2],[2,2])` (sum 2); the other two,
`([1,1],[1,1])` and `([2,2],[2,2])`, have union of length 1 and are delivered by
the preceding sentence (the `2/r` case). Full enumeration is Probe B in Part 1.
Read as a summary of both small cases together the conclusion is right; read as
written, the direct check in the length-2 case does not give all four pairs.

**D3. Theorem 13.3's proof asserts a step it does not justify: "all prime factors
of `uj` are at most `zb`".** Confidence: high that the justification is absent from
the printed proof; medium-low that it is the flagged issue. Impact: the assertion
is true, and Theorems 13.3, 13.5 and 14.2 rest on it, but a two-line argument is
missing.
Location: proof of Theorem 13.3 (txt line 820). The printed text cites only
`uj | Lambda_b` (Theorem 4.2), which by itself does not bound the prime factors
of `uj`. The missing step: if a prime `q` with `zb < q <= b` divided `uj`, it also
divides `c + j`, so it lies in `Sj` and divides `Pj`, giving `q^2 | c + j`; but
`q > zb` implies `q^2 > b` for large `b`, so `q` occurs in `Lambda_b` only to the
first power, contradicting `c + j | Lambda_b`; and `q > b` is excluded by
`c + j | Lambda_b` directly. With that step the conclusion `uj | B_b(zb)` and the
size bounds follow as printed.

**D4. Two one-line valuation gaps of the same kind.**
Confidence: medium that each is a genuine (fillable) gap; low that either is the
flagged issue. Impact: none on the conclusions.
(a) Theorem 7.1 (txt line 427): "The lowest p-adic layer must cancel against the
lower interval." The text then treats the upper denominator's `p`-exponent as 1.
The case of exponent at least 2 is not split off: since `p^2 > b`, every lower
denominator has `p`-exponent at most 1, so an upper exponent of at least 2 would
already make the upper term the unique lowest layer, which is impossible; the
argument needs that sentence before proceeding with exponent 1.
(b) Lemma 2.4 (txt line 162): "If `j > v_p(M)`, then no element of the interval
is divisible by `p^j`, so `A_j = 0` and the summand is 0." The summand is
`A_j - floor(L / p^j)`; vanishing also needs `floor(L / p^j) = 0`, which follows
because `p^j <= L` would force a multiple of `p^j` among any `L` consecutive
integers, contradicting `A_j = 0`. Not stated.

**D5. Lemma 2.1's "more precisely" clause is stated more broadly than its proof.**
Confidence: medium; low that it is the flagged issue. Impact: none, since every
application in the note has a negative minimum.
Location: Section 2, Lemma 2.1. The statement says `v_p(S)` equals the unique
minimum, with no sign hypothesis; the proof begins "Let the unique minimum be
`-e < 0`", covering only the negative case. The claim is in fact true for a
nonnegative unique minimum as well by the same factorisation, but the printed
proof does not cover it.

**D6. Theorem 15.2's expansion uses an ansatz whose boundedness is not
established.** Confidence: low-medium; low that it is the flagged issue. Impact:
peripheral asymptotic; the final constant is correct.
Location: proof of Theorem 15.2 (txt line 1086), writing
`a - 1 = e^{-m} b + beta + O(1/b)` and then requiring the coefficient of `1/b`
to vanish. Boundedness of `beta_b = (a - 1) - e^{-m} b` is not proved before the
expansion is used. I re-derived the constant independently: the `1/b` coefficient
is `-beta e^m + (1 - e^m)/2`, its vanishing gives `beta = (e^{-m} - 1)/2`, and
`a = (a - 1) + 1` then gives the printed `(1 + e^{-m})/2`. So the result stands;
the derivation as printed skips a step.

**D7. "Mutual modular inverses" is the wrong term for the L = 2 cofactors.**
Confidence: high that the term is inaccurate; low that it is the flagged issue.
Impact: terminology only; the displayed congruences are correct.
Location: Theorem 14.2, closing sentence (txt line 938), and the same phrasing in
Problem 18.1. What is proved is `P0 u0 = -1 (mod P1)` and `P1 u1 = 1 (mod P0)`:
`u0` is, up to sign, the inverse of `P0` modulo `P1`, and `u1` is the inverse of
`P1` modulo `P0`. The cofactors `u0` and `u1` are not inverses of each other, and
nothing in the note uses them as such.

### 2.2 Claims checked and found correct (so they are not the defect)

All reruns are in `redteam_note_checks.py` / `redteam_note_checks_results.json`
unless stated otherwise.

- **Proposition 16.1 and Appendix A.** The Appendix A script was transcribed
  verbatim and rerun at the printed bound B = 2000 (`redteam_appendixA_rerun.py`,
  log `redteam_appendixA_rerun.log`, 107.2 s). Output:
  `singleton [(2, 3, 6), (1, 3, 6), (3, 6, 20)]` and `L2 []`, exactly the output
  printed in the note. The claimed computation is therefore not the defect, and
  the verification method in Section 16 was also checked by hand: denominator
  equality forces `D = N` in the singleton branch and `D = c(c+1)` in the L = 2
  branch, and the two congruences the script tests are exactly the integrality
  conditions.
- **Lemma 2.4 (finite instances).** `C(d, L)` divides `lcm(c..d)` for all
  45,150 pairs `1 <= c <= d <= 300`. Zero failures.
- **Theorem 14.1 (finite instances).** `den H([c, c+1]) = c(c+1)` for all
  `1 <= c <= 2000`. Zero failures.
- **Theorem 5.1 (instances on the known disjoint solutions).** All 7 prime
  instances with `Q > L` across the three known disjoint solutions satisfy the
  stated dichotomy and, in case (ii), the congruence `t_p = -R_p^{-1} (mod p)`.
  This includes a genuine case (i) instance: for `([3,6],[20,20])` at `p = 3`,
  `R_3 = 0 (mod 3)` and the upper interval contains no multiple of 3, as required.
- **Theorems 4.2, 6.1, 10.1 (instances on the known disjoint solutions).** All
  hold; Theorem 10.1's denominator bound is an equality on all three examples
  (upper denominators 6, 6, 20 against bounds 6, 6, 20).
- **Lemma 13.2 (numerics).** At `b = 200000`, `z = b / log b`: the exactly summed
  `log B_b(z) / z = 1.0231`, consistent with `(1 + o(1)) z`, and the identity
  `log B_b(z) = sum_{r >= 1} theta(min(z, b^{1/r}))` holds to float precision
  (absolute difference `1.5e-11`).
- **The seven known examples** (Section 1) all have the claimed integer sums:
  2, 3, 2, 1 for the intersecting four and 2, 1, 1 for the disjoint three,
  verified exactly (check C6, and independently by the Part 1 search).
- **Theorem 17.1, items (1) to (11), cross-references.** Each item was checked
  against the result it cites (Theorems 4.1, 7.1, 4.2, 5.1, 6.1, 6.2, 10.1, 9.1,
  12.1, 12.2, 9.3, 11.1, 11.3, 13.3, 13.5). Every item is supported as stated;
  the only wrinkle is the `zb` form in item (7) versus the "furthermore"
  paragraph, which is candidate D1.
- **Sections 4 to 15, line-by-line pass.** Beyond D3, D4 and D6, the arguments of
  Theorems 4.1, 4.2, 5.1, 6.1, 6.2, 7.1, 8.2, 8.4, 9.1, 9.3, 10.1, 11.1, 11.3,
  12.1, 13.4, 13.5, 14.3, 14.4, 14.5 and 15.1 were re-derived and no wrong
  inequality direction, wrong range, or unsupported cross-reference was found.
  In particular the constants most exposed to an arithmetic slip are correct:
  Mertens' theorem gives `sum_{b/2 < p <= b} 1/p ~ (log 2)/(log b)`, matching
  Theorem 14.4's lower bound `(1 - o(1)) (log b)/(log 2)` for `v_i`; the
  `b^4` versus `b^4 / 2` comparison in Theorem 14.5 is in the right direction;
  and Corollary 6.3's rearranged inequality
  `L log(b/(4L)) < R log b` follows from the displayed chain as printed.

### 2.3 Task 2 conclusion

The scan located seven candidate minor defects (D1 to D7), ranked above. None of
them falsifies a stated result: D1 is a notational inconsistency that is vacuous
in the regime where it is used, D2 is a misattribution inside a proof whose
conclusion is correct, D3, D4 and D6 are missing justifications for true steps,
D5 is a proof narrower than its statement in a case never used, and D7 is loose
terminology next to correct displayed formulas. The one fully checkable claim a
standard check would most naturally rerun, the Appendix A computation behind
Proposition 16.1, reproduces its printed output exactly, so it is excluded as
the flagged item. If the flagged "1 minor issue" is in the note at all, D1 and
D2 are my ranked favourites; I state plainly that this identification is a
ranking of located candidates, not a determination, since nothing anywhere
records what the unnamed check flagged.

---

## Part 3: Code inventory

All files in `~/workspace/math-hunt/erdos-288/clusters/A/`, names beginning
`redteam`:

| File | Role |
|---|---|
| `redteam_search.py` | Primary exhaustive search: exact Fraction prefix sums, fractional-part dictionary over all intervals, direct exact re-verification of every candidate; checkpointed every 50 right endpoints, resumable. |
| `redteam_results_1000.json` | Full run record: N = 1000, 500,500 intervals, 7 candidate pairs, the 7 integer-sum pairs, intersecting list, empty outside-list. |
| `redteam_results_120.json` | Pilot run record at N = 120 (same 7 pairs). |
| `redteam_search_1000.log` | Checkpoint log of the full run (one line per block of 50). |
| `redteam_verify_modular.py` | Independent second implementation: two-modulus filter (1000003, 1000033), K in 1..14, exact Fraction verification of all candidates, set comparison against the primary results. |
| `redteam_verify_modular_1000.json` | Its record: 8 candidates, 1 rejected double-modulus collision `([63,178],[613,806])`, agreement with the primary search on both pair sets. |
| `redteam_probes.py` | Boundary probes P0 to P5: naive term-by-term brute force to 60, {1,2} table, exact-union tables for s = 3 and s = 4, Lemma 3.1 predicate to s = 2000, shape classification, valuation-gap check over 3,159 unions. |
| `redteam_probes_results.json` | Probe results (tables, counts, empty failure lists). |
| `redteam_appendixA_rerun.py` | Nayak's Appendix A script transcribed verbatim (only timing added), B = 2000. |
| `redteam_appendixA_rerun.log` | Its output: singletons `[(2, 3, 6), (1, 3, 6), (3, 6, 20)]`, `L2 []`, "MATCHES PRINTED OUTPUT: True", 107.2 s. |
| `redteam_note_checks.py` | Finite checks C1 to C6 of individual claims in the note (Lemma 2.4, Theorem 14.1, Theorem 5.1 and Theorems 4.2/6.1/10.1 instances, Lemma 13.2 numerics, the seven examples). |
| `redteam_note_checks_results.json` | Their full result records. |
| `redteam.md` | This report. |

Notes on artifacts: the search checkpoint pickles (105 MB at N = 1000) were
removed after the run completed; the JSON result files and the checkpoint log
above are the durable record, and `redteam_search.py` recreates checkpoints on
any rerun. No other agent's files in this directory were used or modified.
Nothing was posted, emailed, or submitted anywhere.
