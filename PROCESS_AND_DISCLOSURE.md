# Process and Disclosure

This document follows the spirit of the AGMAI guidance on responsible release of AI generated mathematics: scour and cite the literature, disclose the model and the process, state the compute and time costs, state how the problem was chosen and how much was attempted, and support human understanding of the release. It is the disclosure companion to README.md.

Produced by Meta Muse, prompted by Dennis Canter.

## What this is, and who directed it

This repository contains partial progress on Erdős Problem #288. The problem remains open, and nothing in this repository is a proof of finiteness in general or a proof claim.

Dennis Canter, the human principal, selected Erdős #288 and directed the campaign: he set its scope, gathered the source material (including one note that automated fetching could not reach), decided the design would be fixed in advance, and decided what would be packaged and when. The mathematics, the computation, and these documents were produced by Meta Muse through orchestrated subagents working under that direction.

The site's rules for a proof claim are not met by this package, and no proof claim is made. The principal is not a mathematician (his background is undergraduate mathematics courses) and has not personally verified the analytic arguments; the results stand on the verification record described below, and no Lean formalisation exists. Commenting and proof claims on erdosproblems.com were suspended site wide by the site in October 2026, so the intended channel for these results is this public repository and direct notification of the two audited notes' authors, whose work this cycle builds on and corrects. At the time of writing, nothing has been posted, emailed, or submitted anywhere.

## Method

The campaign ran one proof and audit cycle, designed in advance in CYCLE1_DESIGN.md, with success criteria fixed before launch in three tiers (prize, expected, floor). The coordinator's record, CYCLE1.md, grades the cycle against those criteria and is written exclusively from verifier certified files.

Wave 0 converted the two existing notes into audited ground. Cluster A audited Nayak's note with two auditors who did not see each other's work, a red team tasked with breaking the intersecting case theorem and with hunting a defect that an unnamed check had reportedly flagged, and an independent verifier. Cluster B audited Zeraoulia's note lemma by lemma the same way, and restated its target in campaign form in TARGET.md. Cluster C0 rebuilt both published censuses with two independent implementations and a verifier cross check.

Wave 1 attacked what the notes left open. Cluster C1 extended the censuses with two new implementations sharing no decision code, confirmed by a verifier comparison and a third method spot census. Cluster D attacked the disjoint case at upper length 2 with two provers on mandated different strategies (a CRT and smoothness route, and a quadratic route), a red team attempting construction, and a verifier. Cluster E attacked Zeraoulia's target hypothesis in restricted regimes with two provers, a red team, and a verifier, and closed the two singleton regimes recorded in CYCLE1.md (one completely, one per fixed length with the qualifications stated there).

Verification discipline, stated plainly: verifiers worked from statements and independently recomputed every finite claim before reading the provers' drafts; any claimed solution or closure triggered an extra red team pass before entering the record; defects were logged in the file where they were found and never silently corrected. Computation throughout was exact integer or exact rational arithmetic.

## AI disclosure

Model: Meta Muse. Process: an agentic fan out in which a coordinator briefed independent auditor, prover, red team, and verifier agents, verifiers checked the work claim by claim, and further agents ran and recounted the computations; the coordinator then wrote the record only from the verifier certified files.

The two audited notes are themselves AI assisted work, and that is recorded where they are cited: Nayak's note states on its title page that it was written with assistance from GPT-5.5 Thinking, and Zeraoulia's note is an unreviewed preprint presenting a reduction, not a proof. Neither note had been refereed before this cycle; the audits in AUDIT-A.md and AUDIT-B.md are, to our knowledge, the first documented claim-by-claim independent audits of either. (An earlier check, reported on the problem forum without detail, had flagged one minor issue in Nayak's note before this cycle; see AUDIT-A.md.)

No human mathematician has refereed the results in this repository, and no Lean formalisation exists. Formalisation is not being pursued unless a mathematician working on the problem asks for it.

## Compute and token costs

The token figures come from the measured ledger TOKENS1.md in this repository. The figures there are actuals from the runtime's per run token records, not estimates, and their accounting basis applies in full and is quoted here exactly as the ledger states it: "input" is the attributed input token count, which includes cached context carried into each run, so input figures are much larger than the new text each agent read; "output" is the attributed output token count.

Cycle 1 totals from that ledger: 72,081,720 attributed tokens in all, of which 71,145,957 are attributed input (including cached context) and 935,763 are attributed output, across 27 agent runs (26 child agents plus the coordinator). The design estimate, recorded in advance in CYCLE1_DESIGN.md from an earlier campaign's calibration, was 3 to 5 million tokens; the measured total is far above that estimate, driven almost entirely by attributed input (cached context) rather than output. The ledger says this itself, and it is repeated here so that no reader takes either figure for the other kind.

The censuses were CPU computation in exact arithmetic, not token spend. They ran on a shared 2 core virtual machine; the deposited RESULTS.md file in each implementation directory records the measured runtimes, and CENSUS1.md records the benchmark gate and the projections behind the decision not to run the stretch to 100,000.

## How the problem was chosen, and scope

One problem was attempted in this campaign: Erdős #288, chosen by Dennis Canter from a scouting shortlist of open Erdős problems graded for suitability to an agent proof campaign (elementary statement, decomposition into verifiable cases, manageable literature, meaningful certified partial progress, and no full solution claim recorded on either problem site). The dossier from that selection is INFORMATION.md. One cycle was run. A Cycle 2 specification exists in GAPS.md (items C2-2 to C2-7); it has not been run, and nothing in this repository should be read as a Cycle 2 result.

Failed and refuted directions are part of the record, including the campaign's own. The repairs 13R and 13R+ that Cluster B built to replace Zeraoulia's vacuous Theorem 13 were shown vacuous as routes by Cluster E (CLUSTER-E.md): the implications themselves remain logically valid with correct proofs, but their hypothesis (H-sieve) is false for every threshold, by an explicit infinite family of non-solutions, so both repairs share the original's status, valid implications with unsatisfiable hypotheses. The quadratic reformulation at L = 2 was certified equivalent to the consecutiveness equation, its proposed splitting was shown not to be a descent, and no contradiction of the forms examined in CLUSTER-D.md (certification Q3) exists; arguments in that language using additional structural input are not precluded by anything certified (CLUSTER-D.md). The stretch census to 100,000 was designed, projected, and deliberately not run, with the grounds recorded (CENSUS1.md, Section 5).

## Defect log (summary)

The full logs are in the cluster files; every defect is recorded in the file where it was found. The main items are:

In the audited notes.

* Nayak's note: the proof of Theorem 3.2 ends with a sentence attributing all four intersecting pairs to the length 2 subcase inside {1, 2}, which yields only two of them; the other two come from the preceding length 1 case. A separate inconsistency in the definition of z_b (stated with a maximum in Section 12, without it in Section 13, with the maximum form in Theorem 17.1(7)) is vacuous for fixed L. The whole note scan logged seven items, A-W1 to A-W7, all justification or wording gaps in statements found true (AUDIT-A.md). One of them, the missing justification in Theorem 13.3, was supplied in full by Cluster D (CLUSTER-D.md, result D0).
* Zeraoulia's note: Theorem 13 is valid but vacuous as quantified, its hypothesis being unsatisfiable; Proposition 10's theta bound is false at b = 2 and b = 3 only; the note prints H(3,6) = 49/20 where the correct value is 19/20, a non propagating misprint; and Remark 4's stated asymptotic should tend to log 2 (AUDIT-B.md).

In the campaign's own files.

* Cluster E's Prover 2, Lemma 1.1, omits the word "odd" in its printed conditions and is literally false at a = 1 and a = 2 only; the family it supports has a ≥ 4 and is unaffected, and the certified statement uses the corrected form (CLUSTER-E.md, defect D-E1).
* Cluster D's red team auxiliary meet in the middle table had five wrong rows in its first version, from a faulty preliminary script; it was recomputed by two agreeing implementations and certified in corrected form (CLUSTER-D.md).
* Three deliverable files were truncated during writing during the cycle, each repaired by a dedicated completion agent working only from on disk sources, with an in file repair note; the truncated original of one is preserved beside the restored file (clusters/E/prover1_truncated.md). A final scan at cycle close confirms no other file carries the truncation marker.
* Two verifier side errors were caught and rerun clean during the cycle: the Cluster B verifier's off by one at (1,1), and the Cluster E verifier's first forced residue formula in its check V2. Both are recorded in their files, which is the check working as designed.

## Literature conduct

The campaign's sources are the problem page and forum thread at erdosproblems.com, the problem's catalog page, and the two notes themselves, all gathered in INFORMATION.md before any work began. The classical inputs used are stated where they are used: no interval other than {1} has an integer reciprocal sum (Theisinger 1915, Kürschák 1918), and Tao's forum comment naming the expected hard configuration is treated as orientation, not as a result. Claims are labelled throughout with the campaign's certification vocabulary (certified; certified with qualifications or with located defects; supported as stated; refuted; not certified), and the labels in this README and in the paper are exactly the labels of the underlying files.
