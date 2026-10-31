# Reproduce

This file gives exact commands for rerunning the checks behind the results in this repository, in increasing cost order. Every command is written for the code as it actually is in this repository. Read the notes in each section before running the expensive steps.

## Environment

* Python 3 (the production runs used CPython 3.12.3 on a Linux x86_64 machine). The Python code uses the standard library alone; there are no third party packages to install.
* A C compiler (gcc 13.3 in the production runs) is needed for two components: the prime kernels used by code/c0-impl2 and code/c1-implA, which the Python drivers compile automatically on first run when the shared library is absent, and Implementation B of the extension, which is a standalone C program (code/c1-implB/engine.c). The compiled products are not in this repository (see EXCLUDED_FILES.md); the sources are.
* All arithmetic in every check is exact integer or exact rational arithmetic. Floating point appears only in wall clock timing reports and in the display of certified asymptotic quantities in the documents.
* The checks were developed and run on a 2 core virtual machine. Runtimes below are from that machine class and are guides, not guarantees; the deposited RESULTS.md file inside each implementation directory records the measured runtimes of the production runs.
* Run the commands from the repository root unless a section says otherwise. Paths below are relative to the repository root.

## (a) Per cluster check scripts (seconds to minutes)

Every cluster's verifier, auditor, prover, and red team check scripts are runnable individually. The scripts are deposited verbatim from the campaign, and their output behaviour differs; what each one does with its results is stated exactly below, so a rerun can be compared against the deposited record. The load bearing ones are the verifier scripts:

```bash
python3 clusters/A/verifier_checks.py
python3 clusters/B/verifier_checks.py
python3 clusters/B/verifier_target_check.py
python3 clusters/D/verifier_main.py
python3 clusters/E/verifier_checks.py
```

Expected results: the Cluster A verifier confirms the intersecting classification (exactly four pairs) to endpoints 60 (deposited record: clusters/A/verifier_results.json); the Cluster B verifiers recompute the sieve quantities behind AUDIT-B.md and TARGET.md (records: clusters/B/verifier_output.txt and clusters/B/verifier_target_output.txt); the Cluster D verifier recomputes the prime square sieve counts and the residual quantities of CLUSTER-D.md (record: clusters/D/verifier_main_results.json); the Cluster E verifier recomputes the checks V0 to V7 behind CLUSTER-E.md, including the regime classification on all intervals with a > b/2 and b ≤ 1000 and the Theorem F family for all 44 primes P ≡ 1 (mod 4) with P ≤ 500 (record: clusters/E/verifier_output.txt). Some red team search scripts are heavier; read the header of a script before running it if time matters.

Output behaviour, script by script. The Cluster A verifier prints its checks and writes verifier_results.json to the current working directory; run it from inside clusters/A/ to place the file beside the deposited record, or diff the file it writes wherever you ran it. A rerun reproduces every value in the deposited record; the deposited script additionally writes three explanatory fields for its check 3 (the number of failures with s at least 3, which is 0, the empty list of them, and a note that the sole raw failure, at (1, 2), has s = 2 and so lies outside the lemma's hypothesis) that the deposited record predates. The Cluster B verifier_checks.py prints every check line as it runs; at the end it attempts to write those lines to the original campaign machine's absolute path (/home/hatch/workspace/math-hunt/erdos-288/clusters/B/verifier_output.txt), so on any other machine the run ends with a FileNotFoundError at that final write, after all checks have executed and printed; compare the printed lines against the deposited clusters/B/verifier_output.txt. The Cluster B verifier_target_check.py prints only; compare its output against the deposited clusters/B/verifier_target_output.txt. The Cluster D verifier_main.py likewise prints each check as it runs and at the end attempts to write its results JSON to the campaign machine's absolute path (/home/hatch/workspace/math-hunt/erdos-288/clusters/D/verifier_main_results.json), ending with the same harmless FileNotFoundError elsewhere; compare the printed checks against the deposited record. The Cluster E verifier prints only; compare its output against the deposited clusters/E/verifier_output.txt. The two absolute paths are a defect of the original scripts, preserved because the scripts are evidence; editing the final open() path in a local copy to the corresponding deposited file makes either script write its record directly.

One honest note from the record: the Cluster E verifier's first run of its check V2 contained a verifier side error (a formula slip in the forced residue), which was caught because 37 of 44 class checks failed against two proved routes; the formula was corrected and the full run repeated clean. The deposited output is from the corrected run, and the episode is recorded in CLUSTER-E.md.

## (b) Census reproduction at the published cutoffs (minutes)

These are the Wave 0 censuses certified in CENSUS0.md. Two independent implementations must agree, and the verifier script must confirm both.

Implementation 1 (exact rational prefix differences; code/c0-impl1):

```bash
cd code/c0-impl1
python3 census1.py --max-b 2000
```

Expected result: the run writes chunk files and a summary to code/c0-impl1/outputs/. The singleton solutions for b ≤ 1600 are exactly the six triples (1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20); to b ≤ 2000 the disjoint singletons (those with m > b) are exactly (1,3,6), (2,3,6), (3,6,20), and the L = 2 branch has no solutions. The deposited record is code/c0-impl1/outputs/summary.json, with code/c0-impl1/RESULTS.md as the implementation's own report. The script's internal cross check is code/c0-impl1/verify_brute.py.

Implementation 2 (prime by prime p-adic tracking; code/c0-impl2):

```bash
cd code/c0-impl2
python3 census2.py --n 2000
```

On first run the script compiles code/c0-impl2/prime_kernel.c into prime_kernel.so with gcc (command recorded in the source: gcc -O3 -std=c11 -shared -fPIC), runs its self test, and then the census. Expected result: code/c0-impl2/outputs/solutions.json lists the same six singleton solutions and no L = 2 solutions, in agreement with Implementation 1. Report: code/c0-impl2/RESULTS.md.

Verifier (code/verifier_census0.py):

```bash
python3 code/verifier_census0.py
```

Expected result: code/verifier_results.json records the verifier's independent confirmation of both implementations against the published tables (Zeraoulia's census to b ≤ 1600, and Nayak's Proposition 16.1 to b ≤ 2000), as certified in CENSUS0.md.

## (c) Census extension to b ≤ 20,000 (the certified frontier)

These are the Wave 1 censuses certified in CENSUS1.md. Again two implementations sharing no decision code must agree, and the verifier's comparison and spot census must confirm them.

Implementation A (scaled prime by prime engine; code/c1-implA):

```bash
cd code/c1-implA
python3 censusA.py --n 5000
python3 censusA.py --n 20000
```

The first command is the benchmark gate at 5,000 that the design required before the full run (deposited record: code/c1-implA/outputs/solutions_n5000.json). The second is the full run. Expected result at 20,000: no new singleton solution in (2000, 20000], the L = 2 branch empty, and the four near miss intervals unchanged ((4,7), (5,7), (9,12), (154,156), each a denominator hit with a nonzero numerator residue). The full run regenerates code/c1-implA/outputs/solutions_n20000.json, which is the one bulk file excluded from this repository for size (3,291,759 bytes; see EXCLUDED_FILES.md). Report: code/c1-implA/RESULTS.md.

Implementation B (multi modular bignum engine in C; code/c1-implB):

```bash
cd code/c1-implB
gcc -O3 -march=native -o engine engine.c
bash run_chunks.sh w1 20000
python3 aggregate.py
python3 verify_candidates.py
```

The chunk driver is resumable and can be run by two workers with different tags in parallel. Expected result: code/c1-implB/outputs/aggregate_full.json agrees with Implementation A exactly (the same six singleton solutions in total, no L = 2 solution), and the candidate decisions are confirmed by verify_candidates.py, which decides candidates by a method independent of the engine's filter logic. Report: code/c1-implB/RESULTS.md.

Verifier comparison and spot census:

```bash
python3 code/verifier_c1_compare.py
python3 code/verifier_c1_spot.py
```

Expected results: code/verifier_c1_compare_results.json records the exact agreement of the two implementations over all 200,010,000 intervals with b ≤ 20,000; code/verifier_c1_spot_results.json records the verifier's own third method spot census over 7,000,650 intervals, including the full band 2000 < b ≤ 3000, reproducing both outputs.

## (d) The stretch to b ≤ 100,000 (not run)

No command in this section was run for the record, and no result at 100,000 is claimed anywhere in this repository. CENSUS1.md, Section 5 preserves the projection data: Implementation A projects 44 to 76 minutes of compute, but its prefix inverse tables grow from about 42 MB to about 909 MB and its kernel, compiled at a maximum of 20,000, needs a memory adaptation and a rebuild before such a run is meaningful; Implementation B projects 51 hours at best and 105 to 255 hours on its other models. The certified 20,000 result already satisfied the design's tenfold extension criterion with a two implementation agreement certificate, so the stretch was not earned under the design's terms. This section is listed so that a future cycle can pick the work up from the documented state.
