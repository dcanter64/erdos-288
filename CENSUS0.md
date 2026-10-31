# Erdős #288, Cycle 1, Cluster C0: Census Reproduction Certificate

Verifier record, written by the Cluster C0 Verifier from the two
implementations' on-disk code and machine-readable outputs, from the
published expectations P1 and P2, and from the verifier's own independent
exact computation. All arithmetic in every check below is exact (Python
`int`, `fractions.Fraction`, `math.isqrt`); no floating point enters any
decision. The verifier's own code is
`code/verifier_census0.py` and its full machine-readable record is
`code/verifier_results.json` (field `all_checks_passed: true`,
`failures: []`).

Notation: `H(a,b) = sum_{n=a}^{b} 1/n`, written in lowest terms as `A/B`.
Published expectations: (P1) Zeraoulia's singleton census at `b <= 1600`
has exactly six solutions `(a,b,m) = (1,1,1), (1,2,2), (2,2,2), (1,3,6),
(2,3,6), (3,6,20)`; (P2) Nayak's Proposition 16.1: through `b <= 2000`
the disjoint singleton solutions are exactly `(1,3,6), (2,3,6), (3,6,20)`,
and the `L = 2` disjoint branch (pairs `[a,b]`, `[c,c+1]`, `b < c`, any
`c`) has no solution for `b <= 2000`.

## Per-task verdicts

| Task | Claim tested | Verdict |
|---|---|---|
| (i) Singletons, `b <= 1600`, against P1 | Exactly the six published solutions | **REPRODUCED CERTIFIED** |
| (ii) Singletons, `b <= 2000`, disjoint classification, against P2 | Same six in total; disjoint ones exactly `(1,3,6), (2,3,6), (3,6,20)` | **REPRODUCED CERTIFIED** |
| (iii) `L = 2` disjoint branch, `b <= 2000`, `c > b` unbounded, against P2 | No solutions | **REPRODUCED CERTIFIED** |

Each verdict rests on all three of: the direct output diff in Section 1
(the two implementations agree with each other and with P1/P2), the
coverage aggregation in Section 4 (both implementations demonstrably
examined the full range), and the verifier's own spot census in
Section 3 (a third method reproduces both outputs on `b <= 250`, which
contains all six solutions and all four `L = 2` near-misses). Corroboration
independent of both implementations also exists inside the campaign: the
Cluster A Red Team reran Nayak's own Appendix A script verbatim at
`B = 2000` and its output matched the printed output exactly
(`clusters/A/redteam.md`, Section 2.2; log
`clusters/A/redteam_appendixA_rerun.log`: disjoint singletons
`[(2, 3, 6), (1, 3, 6), (3, 6, 20)]`, `L2 []`, 107.2 s).

## 1. Direct comparison of the machine-readable outputs

The verifier loaded Implementation 1's `outputs/singleton_solutions.json`
and `outputs/l2_solutions.json` and Implementation 2's
`outputs/solutions.json`, normalised the records to `(a, b, m)` integer
triples (Implementation 2 stores `m` and `B` as decimal strings,
Implementation 1 as integers; see the discrepancy list, item D3), and
compared the solution sets directly, not through the prose RESULTS files.

* Task (i), `b <= 1600`: the two sets are **identical**, both equal to
  `{(1,1,1), (1,2,2), (1,3,6), (2,2,2), (2,3,6), (3,6,20)}`, which is
  exactly P1.
* Task (ii), `b <= 2000`: the two full singleton sets are **identical**
  (the same six, so no new solution occurs for `1601 <= b <= 2000`), and
  the two disjoint subsets are **identical**, both equal to
  `{(1,3,6), (2,3,6), (3,6,20)}`, exactly the P2 disjoint list. The three
  non-disjoint solutions each have `m = b`: `(1,1,1)`, `(1,2,2)`,
  `(2,2,2)`.
* Task (iii): both `L = 2` solution lists are **empty**, hence identical,
  matching P2. Implementation 2 additionally records exactly four
  intervals whose reduced denominator is pronic with root `c > b` (the
  only intervals that could possibly be `L = 2` solutions); the verifier
  recomputed all four exactly in Section 3 and confirmed each fails.

The chunk-level unions agree with the headline files in both
implementations (Section 4), so the compared files are not stale
aggregates sitting on top of different chunk data.

## 2. Independence assessment

The verifier read both codebases in full (`census1.py`;
`census2.py`, `prime_ref.py`, `prime_kernel.c`).

**Different engines.** Implementation 1 (`code/c0-impl1/census1.py`)
precomputes the global harmonic numbers `H_n` as exact `Fraction`s and
obtains every `H(a,b)` as a prefix difference `H_b - H_{a-1}` already in
lowest terms. Its singleton test is the global congruence
`A % B == B - 1`, and its `L = 2` test solves a quadratic: the needed
value `t = p/B` must equal `(2c+1)/(c(c+1))`, tested through the
discriminant `D = p^2 + 4B^2` being a perfect square (`math.isqrt`),
with every hit re-verified by a direct `Fraction` sum. Implementation 2
(`code/c0-impl2/`) never forms a global fraction in its census pipeline.
A C kernel (`prime_kernel.c`, 353 lines) tracks, for each prime
`p <= b`, the pair `(V_p, S_p)` (the largest `p`-adic valuation in the
interval and a `p`-adic residue `S_p = (p^{V_p} H(a,b)) mod p^{V_p+1}`),
derives the per-prime denominator exponent `e_p` and unit part `u_p`,
and filters intervals by the prime-power conditions at the five filter
primes `{2,3,5,7,11}` plus a quadratic-residue prefilter for the pronic
condition modulo twelve primes above 2000. Every candidate (3,224
distinct intervals) is then re-derived from scratch by a different
accumulation path (`pk_interval`, a fixed-`V` strata sum) and decided by
CRT assembly in Python big integers (`prime_ref.crt_A`). Its `L = 2`
test is the pronic condition `B = c(c+1)` with `c = isqrt(B)`, plus the
congruence `A + 2c + 1 = 0 (mod B)`.

**No shared decision code.** The two trees share no files (all file
hashes differ), no imports of each other's modules, and no common
helper: Implementation 1 imports only the standard library
(`fractions`, `math.isqrt`, `json`, `os`, `time`, `argparse`);
Implementation 2 imports its own `prime_ref` module, `ctypes` and
`numpy` (the latter only as array plumbing for the C kernel).
Filter logic, candidate generation, and the final decision procedures
are structurally unrelated: a global congruence on a formed fraction
versus a conjunction of prime-power congruences on unformed `p`-adic
state. Implementation 1's internal `verify_brute.py` and Implementation
2's `prime_ref.py` are each confined to their own tree.

**Common-mode risks, stated and weighed.** Three shared elements were
found; none is shared code, and each is mitigated by a check that does
not rely on it.

1. Both implementations use the problem's mathematics of denominator
   forcing: the singleton condition `A = -1 (mod B)` with `m = B`
   forced, and, for `L = 2`, the fact that integrality forces a
   denominator relation (Implementation 1 reaches `c` through its
   quadratic in `t = p/B`; Implementation 2 through `B = c(c+1)`).
   This is the mathematics of the problem statement, not code sharing,
   and the verifier's spot census (Section 3) tests singletons by the
   direct definition (`1/(k - H(a,b))` a positive integer for the
   forced integer `k`) and tests `L = 2` additionally by an explicit
   scan over `c <= 5000`, neither of which assumes denominator forcing.
2. Implementation 2's `census2.py` hardcodes `EXPECTED_SINGLETONS` and
   `EXPECTED_DISJOINT` (lines 73 to 75). Inspection shows
   `EXPECTED_SINGLETONS` is used exactly once, in a self-test assertion
   comparing the exhaustive scratch verification at `b <= 120` against
   the expected six (line 223), and `EXPECTED_DISJOINT` is never used
   at all. The census path (`run()`) never references either constant,
   so no census decision is filtered by the published answer; the
   constant can only make the self-test stricter, not the census
   weaker. Implementation 1 contains no expected-solution list.
3. Both pipelines sit on Python's exact integer arithmetic and
   `math.isqrt`. That is a shared substrate, not shared decision code;
   the verifier's third method (Section 3) leans on the same substrate
   for reduction but reaches its fractions by a different route, and
   Implementation 2's self-tests tie its `p`-adic engine to `Fraction`
   results on all 820 intervals with `b <= 40` and to its own
   pure-Python reference on all 5,050 intervals with `b <= 100`
   (`outputs/selftest.json`).

Conclusion: the two implementations are methodologically independent
in the sense the task requires. Agreement between them is therefore
evidence about the census, not about shared code.

## 3. The verifier's own spot verification

Code: `code/verifier_census0.py`; record: `code/verifier_results.json`.
The spot method is a third, deliberately simple one: one common
denominator `D = lcm(1..250)` (a 107-digit integer), every interval sum
computed as the integer `S = sum_{n=a}^{b} D//n` over `D` and reduced
once. No prefix harmonic numbers (contrast Implementation 1), no
prime-by-prime state, filters, or CRT (contrast Implementation 2).
Singletons were decided by the direct definition, and `L = 2` by two
exact sub-checks: an explicit scan over every `c` with `b < c <= 5000`
(fractional parts of `H(c,c+1)` tabulated, every complementary
candidate re-verified by a direct exact sum), and a forced-denominator
check covering every remaining `c` (each interval whose reduced `B` is
pronic, `B = c(c+1)` with `c > b`, tested by a direct exact sum).

**Coverage and result.** All 31,375 intervals with `1 <= a <= b <= 250`
were recomputed from scratch. The spot singleton set is exactly the six
published solutions (all have `b <= 6`, so all lie in range), and it
equals both implementations' outputs restricted to `b <= 250`. The
spot `L = 2` set is empty under both sub-checks, matching both
implementations. The spot pronic-with-`c > b` set is exactly the four
near-miss intervals below, the same four Implementation 2 records for
the full range to 2000, which independently confirms that no other
interval with `b <= 250` even meets the denominator condition. Spot
runtime: 1.07 s of compute inside the verifier script (whole script
about 1.2 s on this VM).

**The six solutions, verified directly.** For each, `H(a,b)` was
recomputed by naive term-by-term `Fraction` summation and
`H(a,b) + 1/m` evaluated exactly:

| (a, b, m) | H(a,b) | H(a,b) + 1/m | disjoint |
|---|---|---|---|
| (1, 1, 1) | 1 | 2 | no (m = b) |
| (1, 2, 2) | 3/2 | 2 | no (m = b) |
| (2, 2, 2) | 1/2 | 1 | no (m = b) |
| (1, 3, 6) | 11/6 | 2 | yes |
| (2, 3, 6) | 5/6 | 1 | yes |
| (3, 6, 20) | 19/20 | 1 | yes |

All six verify; the disjoint column reproduces the P2 classification.

**The four `L = 2` near-misses, verified exactly.** For each interval
Implementation 2 reported, the verifier recomputed `H(a,b) = A/B` from
scratch, confirmed `B = c(c+1)` with `c > b`, computed the residue
`(A + 2c + 1) mod B`, and computed the exact sum
`H(a,b) + H(c,c+1)`:

| (a, b) | B | c | A | (A + 2c + 1) mod B | exact sum H(a,b) + H(c,c+1) |
|---|---|---|---|---|---|
| (4, 7) | 420 | 20 | 319 | 360 | 6/7 |
| (5, 7) | 210 | 14 | 107 | 136 | 68/105 |
| (9, 12) | 1980 | 44 | 763 | 852 | 71/165 |
| (154, 156) | 1,861,860 | 1364 | 36,037 | 38,766 | 71/3410 |

Every reported value (`B`, `c`, `A`, and the residue) matches
Implementation 2's table exactly, every residue is nonzero, and every
exact sum is a non-integer, so all four fail exactly as stated. They
are the complete list of denominator near-misses: the verifier's spot
census confirms the list is complete for `b <= 250` (all four lie in
that range), and Implementation 1's global method, which has no pronic
filter at all, independently finds no `L = 2` solution anywhere in
`b <= 2000`.

## 4. Coverage and runtime summary

**Implementation 1.** The verifier aggregated the 20 checkpoint files
`outputs/chunk_0001_0100.json` to `chunk_1901_2000.json` directly: the
`b`-ranges are contiguous and cover 1 to 2000, every chunk is marked
complete, every chunk's `pairs_checked` equals the exact count
`sum_{b=lo}^{hi} b` for its range, and the chunk pair counts sum to
exactly **2,001,000** (= `2000 * 2001 / 2`), so tasks (i), (ii) and
(iii) all reached `b = 2000`. The chunk-level singleton union is the
same six solutions and the chunk-level `L = 2` union is empty, matching
`singleton_solutions.json`, `l2_solutions.json`, and both summary
files. Runtime as recorded on disk: the first (computing) run took
185.64 s total (`outputs/summary_first_run.json`;
`chunks_skipped_from_checkpoint = 0`), the sum of the per-chunk compute
times stored in the chunk files is 185.53 s, and the RESULTS file
records a shell-measured 185.9 s for the same run. Implementation 1's
own internal cross-check `verify_brute.py` (direct per-interval
summation and an explicit `c`-scan, a different method again) covers
`b <= 300`, `c <= 20000` and matches the census
(`verify_brute.json`: both match flags true).

**The phantom-notification episode (Implementation 1).** The RESULTS
file's Anomalies section reports that a premature completion
notification from an early ad-hoc scratch brute-force run in `/tmp`
(not part of the delivered code) claimed spurious `L = 2` pairs, for
example `(a,b,c) = (1,1,3)`. The verifier confirms the final on-disk
outputs are the corrected ones, in three ways: the chunk files
themselves (not just the summaries) aggregate to six singletons and an
empty `L = 2` list; `summary_first_run.json` and the resume-run
`summary.json` carry identical solution sets; and the alleged example
is directly false, since `H(1,1) + H(3,4) = 1 + 7/12 = 19/12` is not an
integer, and the verifier's own spot census (which covers `(a,b) =
(1,1)` with an explicit `c`-scan to 5000 and the forced-denominator
check beyond it) finds no `L = 2` partner for `(1,1)` at any `c`.
Current `outputs/summary.json` is the resume run's summary
(`chunks_skipped_from_checkpoint = 20`, elapsed 0.017 s, log in
`outputs/resume_check.log`); the first run's summary is preserved
separately as `summary_first_run.json`, so no runtime figure is lost.

**Implementation 2.** The verifier aggregated the 20 sweep chunk files
`outputs/chunk_a0001_0100_n2000.json` to `chunk_a1901_2000_n2000.json`
and the 20 verification files: the `a`-ranges cover 1 to 2000 with
`N = 2000`, every chunk's interval count equals the exact count
`sum_{a=lo}^{hi} (2000 - a + 1)`, and the chunk interval counts sum to
exactly **2,001,000**, so all 2,001,000 intervals with `b <= 2000` were
examined. The chunk statistics sum to the totals in
`outputs/solutions.json` exactly (605,985 delta events; 632,280 changed
prime records; 1,586 singleton filter passes; 2,265 pronic prefilter
passes; overflow flag 0 in every chunk), the chunk candidate counts sum
to 1,586 and 2,265, the verify files' `candidates_verified` sum to
3,224, matching the candidate-union figure in `solutions.json`, and
the verify files' singleton union is the same six solutions with an
empty `L = 2` union. Runtime as recorded on disk:

> **Repair note, completed ending (2026-10-30).** The original file
> was truncated at this point during writing, and the truncation was
> discovered on 2026-10-30. The ending below was completed by a
> follow-up agent exclusively from the following machine records:
> `code/verifier_results.json`; `code/c0-impl1/RESULTS.md` and its
> `outputs/` summary and chunk JSON files; and
> `code/c0-impl2/RESULTS.md` and its `outputs/` files, including
> `solutions.json`, `progress.json`, `selftest.json`, the 20 sweep
> chunk JSON files, and the 20 verification JSON files. No verdict or
> earlier content was changed. The intact text refers in Section 1 to
> a "discrepancy list, item D3", which indicates that a discrepancy
> list was planned for the part of the file that was lost. The full
> contents, numbering, and wording of that list cannot be
> reconstructed from the machine records named above, so no such list
> is invented here. Item D3 itself is already stated in the intact
> Section 1, namely that Implementation 2 stores `m` and `B` as
> decimal strings while Implementation 1 stores them as integers,
> and the Implementation 2 timing discrepancies that the records do
> establish are stated with both figures below. Any other content
> that may have been planned after Section 4 likewise cannot be
> reconstructed from those records and is not invented here.

In `outputs/solutions.json`, Implementation 2 records
`compute_seconds_from_chunks` as 9.18 s and `total_seconds` as
9.18 s (the same 9.18 s figure recorded in
`code/verifier_results.json` as `compute_seconds_from_chunks_field`),
and `total_intervals` as 2,001,000. Summing the per-chunk fields on
disk gives the same total after rounding: the 20 sweep chunk files'
`sweep_seconds` sum to 7.612 s and the 20 verification files'
`verify_seconds` sum to 1.569 s, for 9.181 s in total.
`outputs/progress.json` records `N` as 2000, `completed_a_up_to` as
2000, `intervals_so_far` as 2,001,000, and `elapsed_seconds` as
0.02 s, and `outputs/solutions.json` records
`last_run_wall_seconds` as 0.02 s (the same progress figures, 2000,
2000, 2,001,000, and 0.02 s, recorded under `progress_json` in
`code/verifier_results.json`).

Implementation 2's prose RESULTS file records different timing
figures, and both versions are stated here without reconciling them.
It records that the full census run (sweep over all chunks plus exact
verification of all 3,224 candidates) took 9.4 s of wall time on the
original run, with 9.18 s summed per-chunk compute
(`outputs/solutions.json`, field `compute_seconds_from_chunks`), as
against the 0.02 s figures recorded under `last_run_wall_seconds` in
`solutions.json` and `elapsed_seconds` in `progress.json` above. It
also records, in the sentence "Kernel build (gcc -O3) plus
self-tests: 7.4 s of self-test time", a 7.4 s self-test figure,
whereas `outputs/selftest.json` records `self_test_seconds` as
3.63 s (the same 3.63 s recorded in `code/verifier_results.json` as
`selftest_json_seconds`).

These are the runtime and coverage figures for Implementation 2
exactly as recorded in the machine files named above, and this
completed ending changes no verdict recorded earlier in this
certificate.