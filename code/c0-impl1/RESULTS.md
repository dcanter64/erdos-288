# Erdős #288 — Cluster C0, Implementation 1 (Cycle 1): RESULTS

Independent implementation. All decisions in exact rational / integer
arithmetic (Python `fractions.Fraction`, `math.isqrt`); no floating point
in any decision (floats are used only for wall-clock timing reports).

## Method summary

Code: `census1.py` (main), `verify_brute.py` (independent cross-check).

* Precompute the harmonic numbers `H_n = sum_{k=1}^{n} 1/k`, `n = 0..2000`,
  exactly as `Fraction`s. (The denominator of `H_2000` has 2876 bits.)
* For every `1 <= a <= b <= 2000`, obtain `H(a,b) = H_b - H_{a-1}` exactly;
  `Fraction` subtraction returns it in lowest terms `A/B`.
* Singleton branch: a solution with `m = B` exists iff `B | (A+1)`, i.e.
  `A % B == B - 1`; denominator forcing makes this `B` the only possible
  `m`, so the test is exhaustive. Disjoint iff `m = B > b`.
* L = 2 disjoint branch (`[a,b]` plus `[c, c+1]`, `c > b`, `c` unbounded):
  for `c > b >= 1`, `0 < H(c,c+1) <= 1/(b+1) + 1/(b+2) < 1`, so with
  `f = H(a,b) = A/B` the needed value `t = k - f` (integer `k`) lies in
  `(0, 1)`; hence `f` integral is impossible, and otherwise `k` is forced
  to be `floor(f) + 1`, giving `t = p/B` with `p = B - (A % B)`. Pairs with
  `t > 1/(b+1) + 1/(b+2)` are removed by an exact integer comparison.
  The equation `t = (2c+1)/(c(c+1))` is `p c^2 + (p - 2B) c - B = 0`, with
  discriminant `D = p^2 + 4 B^2`. A solution exists iff `D` is a perfect
  square (`math.isqrt`) and `c = (2B - p + sqrt(D)) / (2p)` is an integer
  `> b`. Every candidate is re-verified by a direct exact `Fraction` sum
  before being recorded. No scan over `c` is used, so `c` of any size is
  covered.
* Coverage: `2000 * 2001 / 2 = 2,001,000` pairs `(a, b)` examined, for both
  branches (they share the same pair loop). The full range was finished;
  nothing is partial.

## Task (i): Singleton census, `1 <= a <= b <= 1600`

Exactly **six** solutions found:

| a | b | m | H(a,b) | H(a,b) + 1/m | disjoint (m > b) |
|---|---|---|--------|--------------|------------------|
| 1 | 1 | 1  | 1      | 2 | no  (m = b) |
| 1 | 2 | 2  | 3/2    | 2 | no  (m = b) |
| 2 | 2 | 2  | 1/2    | 1 | no  (m = b) |
| 1 | 3 | 6  | 11/6   | 2 | yes |
| 2 | 3 | 6  | 5/6    | 1 | yes |
| 3 | 6 | 20 | 19/20  | 1 | yes |

**Agreement:** this is exactly the published expectation (Zeraoulia):
`(1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20)`. Full agreement,
no extra solutions, none missing.

## Task (ii): Extension to `b <= 2000`, classified

**No new singleton solutions at all** occur for `1601 <= b <= 2000` (indeed
none for `7 <= b <= 2000`): the complete list for `b <= 2000` is the same
six as above.

Classification of the six:

* Disjoint (`B = m > b`), exactly three:
  `(a,b,m) = (1,3,6), (2,3,6), (3,6,20)`,
  i.e. `([1,3],{6}), ([2,3],{6}), ([3,6],{20})`.
* Non-disjoint (`m <= b`), exactly three, all with `m = b`:
  `(1,1,1), (1,2,2), (2,2,2)`.

**Agreement:** the disjoint solutions for `b <= 2000` are exactly the three
published ones (Nayak Proposition 16.1, singleton branch). Full agreement.
The only other solutions in range are the three non-disjoint ones listed
above, as the task anticipated for any additional solutions.

## Task (iii): L = 2 disjoint branch, `b <= 2000`, all `c > b`

**No solutions found.** For all 2,001,000 pairs `(a, b)` with
`1 <= a <= b <= 2000`, there is no `c > b` (of any size, via the exact
quadratic criterion above) with `H(a,b) + H(c, c+1)` an integer.

**Agreement:** this matches the published expectation (Nayak
Proposition 16.1) of no L = 2 disjoint solutions for `b <= 2000`.
Full agreement.

## Runtime and checkpoint details

* Machine: this VM, 2 cores; the census ran as a single Python process.
* First (computing) run: **185.64 s** total elapsed (recorded in
  `outputs/summary_first_run.json`; the shell wrapper measured 185.9 s
  real time for the same run); the sum of the per-chunk compute
  times stored in the chunk files is 185.53 s. Per-chunk times grow with
  `b`, from 0.057 s (b = 1–100) to 38.15 s (b = 1801–1900) and 35.35 s
  (b = 1901–2000).
* Checkpointing: work is split into 20 chunks of 100 consecutive `b`
  values. Each finished chunk is written atomically (temporary file +
  `os.replace`) to `outputs/chunk_<lo>_<hi>.json` with its pair count and
  solution lists. A rerun validates and skips finished chunks.
* Resume test: after the full run, `census1.py` was rerun unchanged; all
  20 chunks were checkpoint hits, the run finished in about 0.1 s, and it
  reproduced identical aggregates (2,001,000 pairs, 6 singleton solutions,
  0 L = 2 solutions). Log: `outputs/resume_check.log`. Note:
  `outputs/summary.json` now reflects that resume run
  (`chunks_skipped_from_checkpoint = 20`, elapsed 0.017 s); the first run's
  summary is preserved as `outputs/summary_first_run.json`.

## Independent cross-check (`verify_brute.py`)

A deliberately different check, written separately from the census logic:

* `H(a,b)` recomputed by summing `1/n` directly over `[a, b]`;
* singletons tested by the direct definition (the unique candidate
  integer `k` with `0 < k - H(a,b) <= 1` must give `1/(k - H(a,b))` a
  positive integer `m`);
* L = 2 tested by an explicit scan over `c` (tabulated exact fractional
  parts of `H(c,c+1)`), no quadratic.

Run with `b <= 300`, `c <= 20000` (file: `verify_brute.json`): singleton
list **matches** the census exactly, and no L = 2 solution with
`c <= 20000` exists for `b <= 300`, matching the census. (The scan is
necessarily `c`-bounded; the census itself is not.)

## Raw outputs

In `outputs/`: `chunk_0001_0100.json` … `chunk_1901_2000.json`
(per-chunk raw results / checkpoints), `singleton_solutions.json`
(the six solutions), `l2_solutions.json` (empty list), `summary.json`,
`summary_first_run.json`, `resume_check.log`. Beside them:
`verify_brute.json`.

## Anomalies

* A premature completion notification for an early ad-hoc scratch
  brute-force check (not part of the delivered code, run in `/tmp`)
  reported a spurious list of alleged L = 2 pairs, e.g. `(a,b,c) =
  (1,1,3)`, with an implausibly short runtime for that script's
  algorithm. Those tuples are **not** solutions: direct exact evaluation
  gives `H(1,1) + H(3,4) = 1 + 7/12 = 19/12`, and likewise for the
  others. The notification was discarded in full. The scratch command's
  actual completion (591 s) later arrived and reported **no** L = 2
  pairs for `b <= 80`, `c <= 5000`, in agreement with the census, and it
  also confirmed the checkpoint-skip behaviour on a small test run. The
  deliverable cross-check is the file-backed `verify_brute.py` above,
  whose results are stored in `verify_brute.json` and do check out. No
  census output was affected: the census chunk files were read back from
  disk and their counts and solution lists verified directly.
* The first run of `verify_brute.py` reported a singleton "mismatch" that
  was purely list ordering (it enumerates `a` in decreasing order); the
  solution sets were already identical. The verifier now sorts before
  comparing, and the rerun passes.
* No anomalies in the census computation itself: every chunk's pair count
  matched its expected value, the aggregate pair count matched
  `2000*2001/2` exactly (asserted in the code), and every recorded
  solution was re-verified by direct exact summation.
