# Erdős Problem #288: Partial Progress

Partial progress on Erdős Problem #288, which asks whether there are only finitely many pairs of intervals I1, I2 of positive integers such that the sum of the reciprocals over I1 plus the sum of the reciprocals over I2 is an integer (Erdős and Graham, 1980, p. 34).

Produced by Meta Muse, prompted by Dennis Canter.

## Status

This repository records partial progress only. Erdős #288 remains open. Nothing here is a proof of finiteness in general, and no proof claim is made, for the whole problem or for any case beyond the items listed below with the exact scope stated for each. The singleton case, where the second interval has length 1, is closed in two regimes (below); the general singleton case, the disjoint case at upper length 2, and every other case remain open.

The results were produced by Meta Muse, an AI system run as orchestrated agents (independent provers, independent verifiers, and dedicated red teams), at the direction of Dennis Canter, who selected the problem and directed the campaign. No human mathematician has refereed these results. No Lean formalisation exists. The full process record, including the defect log and the measured cost ledger, is in PROCESS_AND_DISCLOSURE.md.

A note on the human principal. Dennis Canter is not a mathematician; his background is undergraduate mathematics courses. He does not personally vouch for the analytic arguments in this repository. The results stand on the verification record itself: every claim below traces to a verifier certified file in this repository, and the files record, claim by claim, what was certified, what was certified with qualifications, and what was refuted.

The campaign record files (CYCLE1.md, AUDIT-A.md, AUDIT-B.md, TARGET.md, CENSUS0.md, CENSUS1.md, CLUSTER-D.md, CLUSTER-E.md, GAPS.md, TOKENS1.md, INFORMATION.md, CYCLE1_DESIGN.md, and the code/ and clusters/ trees) are reproduced byte for byte from the original record, including their original typography. The edited presentation layer is this README, the paper, REPRODUCE.md, PROCESS_AND_DISCLOSURE.md, and EXCLUDED_FILES.md, and those documents are the ones held to the house style (including no em dashes). A small number of excluded files (third party material, build products, one bulk output file, one superseded draft) is listed, with sizes and regeneration instructions, in EXCLUDED_FILES.md. One scope note: CLUSTER-D.md's summary of the quadratic route result uses broader wording (the route "closed by equivalence") than its own certification Q3, which scopes the result to the forms of argument examined there. The presentation layer states the result with Q3's scope, and CLUSTER-D.md should be read with that scope.

## What is certified

The two inputs to the campaign are recent unreviewed notes. Nayak's note claims the intersecting case (certified below, with wording defects) and gives a necessary condition package for the disjoint case (scanned by the campaign, not certified line by line; its components carry the labels recorded in GAPS.md, from supported as stated to true with a justification gap); Zeraoulia's note reduces the singleton case to a smooth numbers target (its target lemma is valid but vacuous, below). Cycle 1 audited both notes, extended both of their censuses under certification, and attacked the two frontiers the notes name. Full statements, proofs, and verifier classifications are in the cluster files; the consolidated record is CYCLE1.md.

Audits (Wave 0).

* Nayak's Theorem 3.2 (the intersecting case) and Lemma 3.1 are certified with located defects (AUDIT-A.md). The theorem is true and the note's argument proves it: if two intervals intersect and the sum of their reciprocal sums is an integer, the pair is one of exactly four pairs. The classification was confirmed independently to endpoints 60 by the verifier and to 1000 by the red team. The located defects are wording and exposition only; the most visible is that the proof's final sentence attributes all four pairs to the length 2 subcase inside {1, 2}, which yields only two of them, the other two coming from the preceding length 1 case. Whether this is the one minor issue an unnamed check reportedly flagged on the problem forum is unresolved, because nothing anywhere records what that check flagged.
* Zeraoulia's sieve chain is certified item by item (AUDIT-B.md): Lemma 1, Lemma 2 (case (a) certified with a defect: a proof display defect in the note's proof, the statement itself fully verified; case (b) certified), Lemma 5, Corollary 6, Propositions 8 and 10 (Proposition 10 with a defect: its theta bound is false at b = 2 and b = 3 only), the CRT reduction, and Remark 14. The headline finding concerns his Theorem 13, the note's global target lemma. The implication is logically valid, but its hypothesis is unsatisfiable as quantified, so Theorem 13 is valid but vacuous and is not certified as a usable target. TARGET.md records the campaign's repairs, 13R and 13R+, and Cluster E then refuted the repaired hypothesis as well (below).

Regime closures (Cluster E, CLUSTER-E.md).

* The singleton case is closed for intervals starting in the top half. If a > b/2, the equation H(a,b) + 1/m in the integers, where H(a,b) is the sum of reciprocals over [a, b], has exactly the solutions (a, b, m) = (1,1,1), (2,2,2), (2,3,6). Two independent provers reached the classification by different routes (a strip bound with a forced Bertrand prime; a 2-adic unique maximum window argument), both routes are certified, and a dedicated red team failed to break either proof, including an exhaustive search of the regime to b = 5000.
* Finiteness per fixed length is certified, with qualifications: for each fixed R, every solution of the singleton equation with b − a + 1 = R satisfies a ≤ 2R, so only finitely many solutions exist at that R. The classification is complete for R ≤ 100 (solutions at R = 1 to 4 exactly as in the census, none for 5 ≤ R ≤ 100). For R > 100 the finite check is specified but has not been run, and no statement uniform in R is certified.
* The class route is refuted. The hypothesis (H-sieve), on which both repairs in TARGET.md rest, is false for every threshold: an explicit infinite family of non-solutions (intervals (n_P^2, n_P^2 + 1) for primes P ≡ 1 (mod 4), with n_P^2 ≡ −1 (mod P)) has its denominator inside the forced CRT class, b-smooth, and at most the interval lcm, satisfying every structural condition the class route can see. So 13R and 13R+ remain logically valid implications with unsatisfiable hypotheses. (The refutation itself is certified with one qualification, carried in full in the paper: the supporting characterisation lemma behind it is certified in its corrected odd prime form, being literally false at a = 1 and a = 2 as printed; the family has a ≥ 4 and is unaffected.) The two closures above succeed precisely because they use input outside the forced class.

The L = 2 frontier (Cluster D, CLUSTER-D.md): sharpened, not closed.

* A justification gap in Nayak's Theorem 13.3 is closed (every prime factor of the cofactors is at most z_b), clearing that piece of repair debt under the whole fixed length package.
* A new constraint is certified, with qualifications: log(u_0 u_1) ≥ (2 − o(1)) sqrt(b), the first lower bound on the cofactor product itself. The prime square mechanism behind it is certified saturated at (2 + o(1)) sqrt(b), so any further size must come from first power primes in (sqrt(b), z_b], a band nothing currently forces.
* The quadratic reformulation is certified equivalent, and its proposed splitting is not a descent: the forum suggestion Y^2 = 1 + 4PW is a tautology (Y = 2c + 1), in explicit bijection with the consecutiveness equation, and no modulo or reciprocity contradiction of the forms examined (CLUSTER-D.md, certification Q3) exists. The equivalence alone does not rule out a future argument in that language that uses additional structural input.
* The residual R_D (CLUSTER-D.md, Section 3) states exactly what a hypothetical large L = 2 solution must still satisfy, and names the three extra inputs a closure would need (E1, the mirror residues and mod p^2 congruences with their values; E2, the lower interval numerator congruence used asymptotically; E3, an effective S-unit smoothness obstruction uniform in growing support). The red team's constructive search ran 165,522,272 directed candidates and found no solution; no claim is made beyond b = 225 for that search.

## What is computation

All computation is exact integer or exact rational arithmetic. REPRODUCE.md gives the commands. The certified record is CENSUS0.md and CENSUS1.md.

* Reproduction at the published cutoffs (two independent implementations, exact rational prefix differences and prime by prime p-adic tracking): the singleton census to b ≤ 1600 has exactly the six solutions (1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20); to b ≤ 2000 the disjoint singletons are exactly the three of those with m > b, and the L = 2 branch is empty.
* Extension (two new implementations sharing no decision code): each examined all 200,010,000 intervals with b ≤ 20,000 and the two agree exactly. There is no new singleton solution with 2000 < b ≤ 20,000, the L = 2 branch is empty throughout, and no interval above b = 2000 even meets the L = 2 denominator condition. A verifier spot census by a third method reproduced both outputs on 7,000,650 intervals, including the full band 2000 < b ≤ 3000.
* The extension to b ≤ 100,000 was not run. CENSUS1.md, Section 5 records why (one engine's memory grows to about 909 MB and its kernel needs adaptation and a rebuild; the other projects 51 hours at best) and preserves the projection data for a future cycle. No result at 100,000 is claimed anywhere in this repository.

## What remains open

* Erdős #288 itself: finiteness is unproved in general.
* The singleton case outside the closed regimes: a ≤ b/2 with the length R growing with b, and any statement uniform in R.
* The hypothesis (H-blind) as a global statement. It remains open, and it is moot as a component of the repair 13R+, whose other conjunct is refuted.
* The L = 2 case, at the residual R_D with named inputs E1 to E3.
* Every fixed upper length L ≥ 3, where the CRT smoothness package is necessary but not excluding, and the growing L regime, where the package is not yet stated uniformly.
* The configuration Terence Tao named on the problem thread: a dyadic lower interval at scale M with a very short upper interval at a possibly exponentially larger scale N. Cycle 1 scoped this configuration and did not attack it.
* GAPS.md states the full residual map and a Cycle 2 specification (items C2-2 to C2-7; item C2-1 is complete).

## Repository layout

* CYCLE1.md: the certified record of Cycle 1, assembled by the coordinator exclusively from the verifier certified cluster files, graded against the success criteria fixed in advance in CYCLE1_DESIGN.md.
* CYCLE1_DESIGN.md: the design fixed before launch (clusters, agent allocation, success criteria in prize, expected, and floor tiers).
* AUDIT-A.md: the audit of Nayak's note, including the whole note defect scan (items A-W1 to A-W7).
* AUDIT-B.md and TARGET.md: the audit of Zeraoulia's note, lemma by lemma, and the campaign's repaired target statements with their status.
* CENSUS0.md and CENSUS1.md: the census reproduction at the published cutoffs and the certified extension to b ≤ 20,000.
* CLUSTER-D.md: the L = 2 frontier: certified results D0 to D2, the quadratic route equivalence, the constructive search, and the residual R_D.
* CLUSTER-E.md: the regime closures and the refutation of the class route, in the verifier's certification record.
* GAPS.md: the residual map for the whole problem, with honest audit labels on Nayak's Theorem 17.1 and the Cycle 2 specification.
* TOKENS1.md: the measured token ledger for the cycle, with its accounting basis stated in the file.
* INFORMATION.md: the pre campaign dossier (problem, sources, and the state of play as gathered on 2026-10-30).
* paper/paper.tex (PDF: paper/paper.pdf): the consolidated paper style write-up of the partial results.
* code/: the four census implementations (c0-impl1, c0-impl2, c1-implA, c1-implB), the verifier comparison and spot census code, their outputs, and their RESULTS.md files.
* clusters/: the per cluster working files behind the certified reports: auditor, prover, red team, and verifier documents, check scripts, and result files for clusters A, B, D, and E.
* EXCLUDED_FILES.md: the manifest of files not copied from the campaign workspace, with sizes and regeneration instructions.

## Sources for the two audited notes

* Ritvik Nayak, "A Research Note on Harmonic Sums over Two Integer Intervals: Intersecting intervals and reductions in the disjoint case", May 2026, written with assistance from GPT-5.5 Thinking, announced on the erdosproblems.com forum thread for Problem #288, 3 May 2026. Unreviewed; a pending partial claim on the problem's catalog page. Cited here, not redistributed (see EXCLUDED_FILES.md).
* Zeraoulia Rafik, "The singleton case of Erdős Problem 288: A CRT reduction and a smooth-number obstruction", February 2026, ResearchGate preprint, DOI 10.13140/RG.2.2.10862.47684/1. Unreviewed working notes, presenting a reduction and not a proof.

## How to cite

This work is free to use, with no conditions attached. If you do cite it, we would be grateful for credit in this form: Meta Muse, prompted by Dennis Canter. Title: Partial Progress on Erdős Problem #288. The repository documents CYCLE1.md and the cluster files are the record of the results.

To cite the problem: T. F. Bloom, Erdős Problem #288, https://www.erdosproblems.com/288, accessed 2026-10-30. The problem is Erdős and Graham, Old and new problems and results in combinatorial number theory (1980), p. 34.

## Reading further

REPRODUCE.md gives exact commands and expected outputs for rerunning the censuses and the verifications, in increasing cost order, with honest notes on the expensive steps and on the unrun 100,000 stretch. PROCESS_AND_DISCLOSURE.md gives the method, the AI disclosure, the compute and token costs, and the defect log.
