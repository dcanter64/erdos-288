# Erdős #288, Cycle 1: design

Designed 2026-10-30, after the information dossier (INFORMATION.md
in this workspace). Not launched. Launch requires Dennis Canter's
explicit go-ahead on this design. All theorem references are to the
two working notes in sources/: Nayak (May 2026) and Zeraoulia
(Feb 2026). Ground rule, carried over from the #699 campaign: only
verifier-certified files count as the record; agent chat summaries
are never evidence; every error found is logged in the file where
it is found.

## Objective

Convert the two unreviewed 2026 notes into audited ground the
campaign owns, extend their finite censuses by at least an order of
magnitude under our certification standard, and attack the two
frontiers the notes themselves name: the disjoint length-2 case
(Nayak, Sections 14 and 18) and Zeraoulia's global target lemma in
restricted regimes. A full proof of finiteness is not a Cycle 1
objective; Tao's named hard configuration (a dyadic interval at
scale M with a very short interval at a much larger scale N) is
scoped, not attacked.

## Wave 0: audits and census reproduction (independent clusters)

Cluster A. Audit of Nayak's intersecting case.
Target: Theorem 3.2 (if I and J intersect and H(I) + H(J) is an
integer, the pair is one of ([1,1],[1,1]), ([1,2],[1,2]),
([1,2],[2,2]), ([2,2],[2,2])) and its Lemma 3.1.
Agents: two auditors with mandated different routes (Auditor 1
follows the note's own Bertrand / Sylvester-Schur argument line by
line; Auditor 2 re-derives the result independently from the
statement, using the coefficient-1-or-2 union formulation and
direct p-adic valuation bookkeeping), plus one red-team agent whose
sole task is to break the theorem: search computationally for an
intersecting pair outside the four, and probe the boundary cases
(union a single element; union inside {1,2}; s = 3) for gaps.
The red team also owns the hunt for the "1 minor issue" an unnamed
standard check reportedly flagged in the note (forum, 3 May 2026;
no detail exists anywhere, so the hunt is a full-note discrepancy
scan, with Sections 4 to 18 in scope, not only Section 3).
One verifier certifies from the statement, not from the proofs.
Deliverable: AUDIT-A.md, with Theorem 3.2 marked certified,
certified with a located defect (stated exactly), or not certified
(reasons stated exactly).

Cluster B. Audit of Zeraoulia's reduction.
Target: Lemma 1 (denominator forcing), Lemma 2 (the p-adic sieve
dichotomy), Lemma 5 and Corollary 6 (the T(u) = D'(u)/D(u)
characterisation and the finite bad-prime set for fixed (u,k)),
Propositions 8 and 10 (good-prime ranges and the size of Q), the
CRT reduction, and Theorem 13 (the global target lemma) with its
Remark 14 caveat.
Agents: two auditors (one follows the note; one re-derives the
sieve from the statement H(a,b) + 1/m in Z), one verifier.
Deliverable: AUDIT-B.md certifying each lemma individually, and a
campaign-notation restatement of the target lemma, TARGET.md.

Cluster C0. Census reproduction.
Two independent implementations (different authors, different
methods: one exact-rational with incremental updates; one
prime-by-prime denominator and numerator tracking) reproduce:
(i) Zeraoulia's singleton census, all b <= 1600, exactly six
solutions (1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20);
(ii) Nayak's Proposition 16.1: singleton branch through b <= 2000
has only the three disjoint examples, and the L = 2 disjoint branch
has no solution for b <= 2000.
A verifier cross-checks the two implementations against each other
and against the published tables on the full overlap. Any mismatch
halts the cycle until resolved; the pipeline is not trusted past a
mismatch.
Deliverable: CENSUS0.md plus both codebases, kept.

## Wave 1: extension and attack (starts only on Wave 0 certification)

Cluster C1. Census extension.
Singleton branch: extend the certified census to b <= 20,000,
with a benchmark gate at b = 5,000 (if the measured cost projects
past three days of compute for 20,000, fall back to the largest
completed checkpoint and report it as the frontier). Stretch, only
if the prime-by-prime implementation benchmarks well: b <= 100,000.
L = 2 disjoint branch: extend using Theorem 4.2's divisor-block
restriction (every upper denominator divides Lambda_b, and at L = 2,
c(c+1) divides Lambda_b) as the pruning filter, to b <= 20,000.
Every extension ships the full solution list (expected: no new
solutions) and the two implementations' agreement certificate.
Deliverable: CENSUS1.md.

Cluster D. The length-2 frontier.
Target: disjoint solutions with upper length L = 2, in the form
Nayak's Theorem 14.2 forces: c = P_0 u_0, c + 1 = P_1 u_1,
P_1 u_1 - P_0 u_0 = 1, with S_0 and S_1 partitioning the primes in
(z_b, b], log P_0 = log P_1 = b/2 + o(b), and u_0, u_1 smooth and
small. (Cluster D consumes Theorem 14.2 only as audited in
Wave 0's discrepancy scan; any unaudited step it needs is audited
by the cluster's verifier first.)
Agents: Prover 1, CRT and smoothness route: push the size and
smoothness constraints toward a contradiction (the u_i bounds
against the partition condition). Prover 2, quadratic route:
sammausberg's compression from the forum, rule out
Y^2 = 1 + 4 P W with W = u_0 u_1 in the forced ranges, by modulo
and quadratic-form arguments. Red team: attempt to construct an
L = 2 solution from the CRT conditions directly (a construction
settles the problem the other way, and a failed systematic attempt
maps the obstruction). One verifier.
Deliverable: CLUSTER-D.md: the L = 2 case closed, or the exact
sharpened residual (which ranges of b, which sub-conditions
survive), or a found solution.

Cluster E. The target lemma in restricted regimes.
Target: Zeraoulia's Theorem 13 hypothesis (no b-smooth integer in
the forced class m = r(a,b) mod Q(a,b) with m <= lcm(a..b)) in
regimes where the modulus does not reach the barrier of his
Section 8: (i) short intervals, length R = b - a + 1 fixed, where
lcm(a..b) is small relative to Q; (ii) intervals with a > b/2.
Agents: two provers with different routes (least-residue lower
bounds; structural smoothness obstructions inside the class), one
verifier.
Deliverable: CLUSTER-E.md: the target lemma proved for an explicit
regime (which would close the singleton case in that regime), or
the exact point where each regime's argument fails.

Cluster F. Scoping the general disjoint case (no proof target).
One agent restates Nayak's Theorem 17.1 in campaign form, assembles
the full gap list between the audited obstructions and finiteness
(including Tao's configuration), and specifies what a Cycle 2
would need. Deliverable: GAPS.md.

## Verification architecture

Every cluster has its own verifier agent who works from statements
and recomputes every finite claim independently; verifiers do not
read the provers' drafts before forming their own check plan. Two
provers per proof cluster always carry mandated different
strategies, because same-model agents share blind spots (in #699
Cycle 2, both provers on one cluster produced the same false gloss;
the verifier caught it). Load-bearing results (the Theorem 3.2
audit, any closure claimed in D or E) additionally carry a red-team
agent tasked only with refutation. The coordinator assembles
CYCLE1.md exclusively from certified cluster files and writes
TOKENS1.md from the measured run ledger.

## Success criteria, fixed in advance

Prize: the L = 2 disjoint case closed for all b, or the singleton
case closed in a named regime (fixed length R, or a > b/2), each
fully verifier-certified.
Expected: both notes audited to a certified standard (Theorem 3.2
certified or its defect located and characterised; Zeraoulia's
reduction lemmas certified individually); both censuses extended
at least tenfold with agreement certificates; at least one
frontier measurably sharpened (a new constraint in D, or a regime
of E reduced to an explicit finite check).
Floor: audits complete with every gap listed exactly; censuses
reproduced exactly at the published cutoffs, validating the
pipeline; the residual map (GAPS.md) restated precisely enough for
a mathematician to pick up. The floor is a successful cycle.

## Budget, stop rules, risks

Budget: about 18 agent runs plus coordination. Measured #699
cycles ran 0.85 to 2.1 million tokens for 12 runs; Cycle 1 here is
estimated at 3 to 5 million tokens, small against the weekly
budget. Compute runs on this machine (2 cores); census work is
checkpointed and resumable.
Stop rules: a Wave 0 mismatch or an uncertifiable load-bearing
lemma stops Wave 1 for the affected cluster only, and is reported,
not worked around. The b = 5,000 benchmark gate governs C1. Any
claimed solution or closure triggers an immediate extra red-team
pass before it is reported to Dennis.
Risks, stated plainly: the intersecting theorem may contain the
flagged minor issue, which would make Cluster A a correction
exercise rather than a certification (still valuable, and the
floor covers it); the L = 2 and target-lemma attacks may both end
at sharpened residuals rather than closures, which the expected
tier prices in; and finiteness itself very likely needs an idea
outside both notes, which is Cycle 2's problem, not this cycle's
failure.

## Deliverables

CYCLE1.md (the certified record), TOKENS1.md, AUDIT-A.md,
AUDIT-B.md, TARGET.md, CENSUS0.md, CENSUS1.md, CLUSTER-D.md,
CLUSTER-E.md, GAPS.md, and all census code, in this workspace.
Nothing is posted, emailed, or submitted anywhere; dissemination
is a separate decision, as with #699.
