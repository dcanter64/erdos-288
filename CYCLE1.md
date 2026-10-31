# Erdős Problem #288, Cycle 1: the certified record

Coordinator's record, assembled 2026-10-30 exclusively from the
verifier-certified cluster files in this workspace (AUDIT-A.md,
AUDIT-B.md, TARGET.md, CENSUS0.md, CENSUS1.md, CLUSTER-D.md,
CLUSTER-E.md, GAPS.md), under the design fixed in advance in
CYCLE1_DESIGN.md. Token costs are in TOKENS1.md, from the measured
run ledger. Campaign run by Meta Muse, prompted by Dennis Canter.

**The problem.** Are there only finitely many pairs of intervals
I1, I2 with H(I1) + H(I2) in the integers, where H is the harmonic
sum over the interval (Erdos and Graham, 1980, p. 34)? The problem
is open, and before this cycle it was open even in the singleton
case (upper interval of length 1): H(a,b) + 1/m in Z. Two unreviewed
2026 notes attacked it: Nayak (intersecting case solved; a rigid
necessary-condition package for the disjoint case) and Zeraoulia
(a CRT reduction of the singleton case to a smooth-numbers target).
Cycle 1 set out to convert both notes into audited ground, extend
their censuses tenfold under certification, and attack the two
frontiers the notes name. A full finiteness proof was not a Cycle 1
objective, and Erdős #288 remains open. One frontier, however, fell.

## Grade against the criteria fixed in advance

**Prize tier: MET.** The design's prize was "the L = 2 disjoint
case closed for all b, or the singleton case closed in a named
regime (fixed length R, or a > b/2), each fully verifier-certified."
The second branch is met, twice over (CLUSTER-E.md):

- Regime (ii), a > b/2, is CLOSED completely. The singleton equation
  H(a,b) + 1/m in Z with a > b/2 has exactly the solutions
  (a,b,m) = (1,1,1), (2,2,2), (2,3,6). Two independent prover routes
  reached the classification and both are CERTIFIED: Prover 1 by a
  strip bound H < 3/4 with a Bertrand prime in (b/4, b/2) forced to
  divide m in {2,3}; Prover 2 by a 2-adic unique-maximum window
  argument. A dedicated red team failed to break either proof
  (including an exhaustive regime search to b = 5000).
- Regime (i), fixed length R, is closed in the finiteness sense,
  CERTIFIED WITH QUALIFICATIONS: for each fixed R, every solution
  has a <= 2R, so only finitely many solutions exist at that R, and
  the classification is complete for R <= 100 (solutions at R = 1
  to 4 exactly as in the census, none for 5 <= R <= 100). For
  R > 100 the finite check is specified but has not been run; no
  uniform-in-R statement is certified.

The L = 2 branch of the prize was not met: Cluster D sharpened that
frontier substantially but did not close it (below).

**Expected tier: MET, in full.** Both notes audited to a certified
standard (Wave 0, below). Both censuses extended tenfold with
agreement certificates: the certified census now reaches
b <= 20,000 in both branches (CENSUS1.md). Both frontiers
measurably sharpened: Cluster D produced a new constraint on the
L = 2 cofactors and closed a justification gap in Nayak's
Theorem 13.3, and Cluster E closed two regimes outright and, in
doing so, refuted the target hypothesis Cluster B had repaired.

**Floor tier: exceeded.** Every audit gap is listed exactly in the
cluster files; the censuses reproduce exactly at the published
cutoffs; GAPS.md states the residual map, updated at cycle close,
precisely enough for a mathematician to pick up (its Cycle 2
specification is items C2-2 to C2-7, C2-1 being complete).

## Wave 0: the audits and the census reproduction

**Cluster A (AUDIT-A.md).** Nayak's Theorem 3.2 (the intersecting
case) and Lemma 3.1 are CERTIFIED WITH LOCATED DEFECTS. The theorem
is true and the note's argument proves it; the classification
(exactly four intersecting pairs) was confirmed independently to
endpoints 60 by the verifier and to 1000 by the red team. The
defects are wording and exposition only. The most visible: the
proof's final sentence attributes all four pairs to the length-2
subcase inside {1,2}, which yields only two of them; the other two
come from the preceding length-1 case. All three producers found
this independently, and it is the leading candidate for the "1 minor
issue" an unnamed standard check reportedly flagged on the forum;
the identification is UNRESOLVED, because nothing anywhere records
what that check flagged. The second candidate is the z_b
inconsistency (Section 12 defines z_b with a max, Section 13 drops
it, Theorem 17.1(7) uses the max form; vacuous for fixed L). The
whole-note scan logged items A-W1 to A-W7, all justification or
wording gaps in statements found true, and reran the note's
Appendix A script verbatim at B = 2000 with output matching the
printed output exactly.

**Cluster B (AUDIT-B.md, TARGET.md).** Zeraoulia's sieve chain is
certified item by item: Lemma 1, Lemma 2 (case (a) certified with a
proof-display defect, case (b) certified), Lemma 5, Corollary 6,
Proposition 8, Proposition 10 (certified with a defect: its theta
bound is false at b = 2 and b = 3 only), the CRT reduction, and
Remark 14. The headline finding concerns Theorem 13, the note's
global target lemma: the implication is logically valid, but its
hypothesis is unsatisfiable as quantified (at (a,b) = (q^2, q^2)
the sieve is empty, Q = 1, and m = q^2 is a smooth member of the
forced class at every scale), so Theorem 13 is valid but VACUOUS
and NOT CERTIFIED as a usable target. TARGET.md carries the
campaign's repairs 13R and 13R+, which restrict the hypothesis to
intervals where the sieve is nonempty and add a hypothesis
(H-blind) for the sieve-empty regime. Also confirmed: the note
prints H(3,6) = 49/20 where the correct value is 19/20 (a
non-propagating misprint), and Remark 4's "grows like log log b"
should tend to log 2.

**Cluster C0 (CENSUS0.md).** Two independent implementations
(exact-rational prefix differences; prime-by-prime p-adic tracking)
REPRODUCED CERTIFIED against both published tables: the singleton
census to b <= 1600 has exactly the six solutions (1,1,1), (1,2,2),
(2,2,2), (1,3,6), (2,3,6), (3,6,20); to b <= 2000 the disjoint
singletons are exactly the last three of those with m > b, and the
L = 2 branch is empty. Four denominator near-miss intervals for
L = 2 were recorded exactly: (4,7), (5,7), (9,12), (154,156), each
with B = c(c+1), c > b, and a nonzero numerator residue.

## Wave 1: extension and attack

**Cluster C1 (CENSUS1.md). EXTENSION CERTIFIED in both branches.**
Two new implementations sharing no decision code (a scaled
prime-by-prime engine; a from-scratch multi-modular bignum engine
whose filter soundness the verifier re-derived line by line with no
gap found) each examined all 200,010,000 intervals with
b <= 20,000 and agree exactly: no new singleton solution in
(2000, 20000], the L = 2 branch is empty, and the near-miss list is
unchanged, with no interval above b = 2000 even meeting the L = 2
denominator condition. The verifier's own third-method spot census
reproduced both outputs on 7,000,650 intervals, including the full
band 2000 < b <= 3000. The b = 5,000 benchmark gate passed easily.
Six minor record defects (prose-only wall times and similar) are
logged in CENSUS1.md Section 6; none affects a verdict.

**Stretch decision (coordinator).** The stretch to b <= 100,000 was
NOT run. Implementation A projects 44 to 76 minutes of compute but
its prefix-inverse tables grow from about 42 MB to about 909 MB,
and its kernel, compiled at MAXN = 20,000, needs a memory adaptation
and rebuild first; Implementation B projects 51 hours at best and
105 to 255 hours on its other models. The certified 20,000 result
already satisfies the design's tenfold-extension criterion with a
two-implementation agreement certificate, so the stretch was not
earned under the design's terms. The projection data is preserved
in CENSUS1.md Section 5 for any future cycle.

**Cluster D (CLUSTER-D.md). The L = 2 case is NOT closed; the
frontier is sharpened and the residual is exact.** Four certified
results frame it. D0 is CERTIFIED: the missing justification in
Nayak's Theorem 13.3 (that every prime factor of the cofactors u_j
is at most z_b) is supplied in full, closing AUDIT-A item A-W2 and
clearing that piece of repair debt under the whole fixed-L package.
D1 is CERTIFIED WITH QUALIFICATIONS: a new constraint,
log(u_0 u_1) >= (2 - o(1)) sqrt(b), the first lower bound on the
cofactor product u_0 u_1 itself (Theorem 14.4 of the note bounds a
different, larger quantity and implies nothing here). D2 is
CERTIFIED: the prime-square mechanism behind D1 is saturated at
(2 + o(1)) sqrt(b), so any further size in u_0 u_1 must come from
first-power primes in (sqrt(b), z_b], a band nothing currently
forces. The quadratic route is CERTIFIED as exhausted: the forum's
compression Y^2 = 1 + 4PW is a tautology (Y = 2c + 1; the identity
is in explicit bijection with P_1 u_1 - P_0 u_0 = 1), its splitting
is idempotent rather than a descent, and no modulo or reciprocity
contradiction of the forms examined exists. The red team's
constructive search ran 165,522,272 directed forced-form
candidates; exactly one passed the smoothness filter (b = 30,
c = 19227) and it fails the exact interval test for every a, with
obstruction margins growing over the tested range (least defect
20.42, 25.91, 33.22 at b = 100, 120, 150); no claim is made beyond
b = 225. The final residual R_D (CLUSTER-D.md Section 3) states
exactly what a hypothetical large L = 2 solution must still
satisfy, and names the three extra inputs a closure would need:
E1, the Theorem 13.5 mirror residues and Theorems 14.3 to 14.4
mod-p^2 congruences brought to bear with their values; E2, the
lower interval's numerator congruence A + 2c + 1 = 0 (mod c(c+1))
used asymptotically; E3, an effective S-unit smoothness obstruction
uniform in growing support.

**Cluster E (CLUSTER-E.md). The prize result, and a refutation.**
The two regime closures are stated in the grading section above and
rest on claims C1 to C3, all CERTIFIED (C3 with the quantifier
qualifications stated there). Claim C4 is CERTIFIED WITH
QUALIFICATIONS and is the cycle's other headline: the hypothesis
(H-sieve), on which both of TARGET.md's repairs rest, is REFUTED
for every B_0. Prover 2's Theorem F family (intervals
(n_P^2, n_P^2 + 1) for primes P = 1 (mod 4), where n_P^2 = -1
(mod P)) consists of non-solutions whose denominators lie in the
forced CRT class, are b-smooth, are at most L(a,b), and satisfy
every structural condition the class route can see. So 13R and 13R+
remain logically valid implications with unsatisfiable hypotheses,
the same vacuity status AUDIT-B.md assigned to the original
Theorem 13, now extended to the campaign's own repair. The closures
in regimes (i) and (ii) succeed precisely because they use input
outside the forced class. (H-blind) remains open as a statement but
is moot as a component of 13R+. One minor defect is logged: Prover
2's Lemma 1.1 omits the word "odd" and is literally false at a = 1
and a = 2 only; the family it supports has a >= 4 and is unaffected.

**Cluster F (GAPS.md).** Nayak's Theorem 17.1 is restated clause by
clause with honest audit labels: no clause is verifier-certified,
the strongest label is "supported as stated" from the Cluster A
scan, and the theorem stands as a necessary-condition package that
excludes nothing by itself. The gap list G1 to G7 and the Cycle 2
specification C2-1 to C2-7 were written mid-cycle and updated at
cycle close to final status (dated revision note in the file): G1
is narrowed (two singleton regimes closed by Cluster E, the 13R+
route refuted, the general uniform statement still open), G3 is
replaced by Cluster D's residual R_D, G6's census frontier is now
the certified 20,000, and repair-debt item (ii) is cleared by D0.

## Defects and record integrity, consolidated

Every defect found is logged in the file where it was found; the
headline items are: Nayak's final-sentence misattribution and z_b
inconsistency (AUDIT-A.md); Zeraoulia's vacuous Theorem 13,
Proposition 10 bound false at b = 2, 3, the H(3,6) = 49/20 misprint,
and Remark 4's wrong asymptotic (AUDIT-B.md); Cluster E Prover 2's
Lemma 1.1 missing "odd" (CLUSTER-E.md); the wording items in
Cluster D's producer files, including the red team's auxiliary
meet-in-the-middle table, whose first version had five wrong rows
from a faulty preliminary script and was recomputed by two agreeing
implementations and certified in corrected form (CLUSTER-D.md).
Three deliverable files were truncated during writing with a
literal truncation marker baked in (Cluster E's prover1.md,
AUDIT-A.md, CENSUS0.md); each was repaired by a dedicated completion
agent working only from on-disk sources, with an in-file repair note,
and the truncated original of prover1.md is preserved beside the
restored file. A final scan at cycle close confirms no other file
carries the marker. Two verifier-side errors were also caught and
rerun clean during the cycle (the Cluster B verifier's off-by-one
at (1,1); the Cluster E verifier's first V2 residue formula); both
are recorded in their files, which is the check working as designed.

## What remains open

Erdos #288 itself: finiteness is unproved in general. Specifically:
the singleton case outside the closed regimes (a <= b/2 with the
length R growing with b, and any uniform statement); (H-blind) as a
global statement; the L = 2 case, now exactly residual R_D with
named inputs E1 to E3; every fixed L >= 3, where the
CRT-smoothness package is necessary but not excluding (GAPS.md G2);
the growing-L regime (G4), where the package itself is not yet
stated uniformly; and Tao's configuration, a dyadic lower interval
at scale M with a very short upper interval at a possibly
exponentially larger scale N, which Cycle 1 scoped and did not
attack (G5). The census frontier is certified to b <= 20,000; the
100,000 stretch is documented and unrun.

## Files of the cycle

In this workspace: CYCLE1_DESIGN.md (the controlling design),
INFORMATION.md (the dossier), AUDIT-A.md, AUDIT-B.md, TARGET.md,
CENSUS0.md, CENSUS1.md, CLUSTER-D.md, CLUSTER-E.md, GAPS.md,
CYCLE1.md (this record), TOKENS1.md (the measured ledger), all
census and verifier code under code/ and clusters/, and the primary
sources under sources/. Nothing was posted, emailed, or submitted
anywhere; dissemination is a separate decision for Dennis Canter.
