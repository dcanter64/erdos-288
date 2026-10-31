# Erdős #288, Cycle 1, Cluster C1: Census Extension Certificate (b ≤ 20,000)

Verifier record, written by the Cluster C1 Verifier from the two
implementations' on-disk code and machine-readable outputs, from the
certified Wave 0 record (`CENSUS0.md`), and from the verifier's own
independent exact computation. All arithmetic in every check below is
exact (Python `int`, `fractions.Fraction`, `math.isqrt`, `math.gcd`);
no floating point enters any decision (floating point appears only in
the stretch projections of Section 5, which are data for the
coordinator, not decisions). The verifier's own code is
`code/verifier_c1_compare.py` (machine record
`code/verifier_c1_compare_results.json`, field
`all_core_checks_passed: true`) and `code/verifier_c1_spot.py`
(machine record `code/verifier_c1_spot_results.json`).

Notation: `H(a,b) = sum_{n=a}^{b} 1/n = A/B` in lowest terms.
Singleton equation: `H(a,b) + 1/m` in Z, which forces `m = B` and
`A = -1 (mod B)`. L = 2 branch: pairs `[a,b]`, `[c,c+1]`, `b < c`,
any `c`; integrality forces `B = c(c+1)` and then the single
congruence `A + 2c + 1 = 0 (mod B)`. Certified baseline (CENSUS0):
singleton solutions exactly `(1,1,1), (1,2,2), (2,2,2), (1,3,6),
(2,3,6), (3,6,20)`; L = 2 branch empty; four near-miss intervals with
`B = c(c+1)`, `c > b`: `(4,7,420,20,res 360), (5,7,210,14,res 136),
(9,12,1980,44,res 852), (154,156,1861860,1364,res 38766)`.

## Per-branch verdicts

| Branch | Claim tested | Verdict |
|---|---|---|
| Singletons, `b <= 20,000` | Exactly the six certified solutions; none with `2000 < b <= 20,000` | **EXTENSION CERTIFIED** |
| L = 2 disjoint, `b <= 20,000`, `c > b` unbounded | No solutions; near-miss list exactly the four certified intervals, none with `b > 2000` | **EXTENSION CERTIFIED** |

Each verdict rests on all three of: the direct file comparison in
Section 1 (the two implementations agree with each other and with
the certified baseline, at headline and at chunk level), the
coverage aggregation in Section 2 (both implementations
demonstrably examined all 200,010,000 intervals), and the verifier's
own spot census in Section 4 (a third method reproduces both outputs
on 7,000,650 intervals in the extension range, including the full
band `2000 < b <= 3000` and three slices beyond 10,000). The
independence and filter-soundness assessment in Section 3 is what
licenses treating the two implementations' agreement as evidence:
in particular, Implementation B's filter was audited line by line
and its soundness argument was re-derived, because in B almost every
interval is filter-decided (Section 3.3).

## 1. Direct comparison of the machine-readable outputs

The verifier loaded Implementation A's `outputs/solutions_n20000.json`
(singleton list, `l2_solutions`, `pronic_with_c_gt_b`) and
Implementation B's `outputs/verify_full.json` (its exact candidate
decisions) plus `outputs/aggregate_full.json`, normalised the records
to integer tuples, and compared the sets directly, not through the
prose RESULTS files. It also rebuilt each headline list from the
chunk files (A's 80 verify JSONs; B's 80 chunk JSONs) and confirmed
the chunk unions equal the headline files, so neither headline is a
stale aggregate.

* Singletons, `b <= 20,000`: the two sets are **identical**, both
  equal to `{(1,1,1), (1,2,2), (1,3,6), (2,2,2), (2,3,6), (3,6,20)}`
  (A stores `m` as a decimal string, B as an integer; normalised
  before comparison). No solution has `b > 2000`, so the extension
  range `(2000, 20000]` contributes an explicitly empty new-solution
  list in both implementations.
* L = 2 solutions: **empty in both**, hence identical.
* Near-misses (intervals with `B = c(c+1)`, `c > b`): the two lists
  are **identical**, both equal to the four certified intervals with
  the same `B`, `c` and residue values:
  `(4,7,420,20,360), (5,7,210,14,136), (9,12,1980,44,852),
  (154,156,1861860,1364,38766)`. None has `b > 2000`. The verifier
  additionally recomputed all four from the definitions with direct
  `Fraction` summation: every `A`, `B`, `c` and residue matches, every
  residue is nonzero, and every exact sum `H(a,b) + H(c,c+1)` is the
  certified non-integer (`6/7`, `68/105`, `71/165`, `71/3410`). All
  six singletons were likewise re-verified by direct `Fraction`
  summation (`H(a,b) + 1/m` an integer in each case).
* Cross-check of independent tallies: the total number of pronic
  denominators found agrees exactly between the two unrelated
  engines, at both scales. At `N = 5,000`: A's `l2_filter_passes`
  5,079 = B's stage-D passes 5,079 (= 4 near-misses + 5,075 pronic
  with `c <= b`). At `N = 20,000`: A's 20,149 = B's 20,149
  (= 4 + 20,145), and A's `pronic_candidates_all` has exactly 20,149
  entries. B's own Python brute-force audits (`outputs/brute_300.json`,
  `outputs/brute_2000.json`, prefix `Fraction` method) match the
  engine on their ranges, including pronic `c <= b` counts 321
  (`b <= 300`) and 2,049 (`b <= 2000`).

## 2. Coverage and timing verification

### Implementation A (a-partitioned chunks, 250 a-values per chunk)

The verifier aggregated all chunk and verify JSONs for both runs.
For every chunk the recorded `stats.intervals` equals the exact
count `sum_{a=a0}^{a1} (N - a + 1)` for its range, the a-ranges are
contiguous from 1 to N, and the overflow flag is 0 in every chunk.

* Gate, `N = 5,000`: 20 chunks, total **12,502,500** intervals.
  Summed per-chunk times: sweep 3.601 s, verification 0.522 s, total
  4.123 s, against `compute_seconds_from_chunks` 4.12 s in
  `solutions_n5000.json` (difference 0.003 s, accounted for by the
  per-chunk times being stored rounded to 3 decimals and the total
  to 2). The task's stated gate figure of 4.12 s is verified as the
  chunk-compute total. See discrepancy D1 for the gate wall time.
* Full, `N = 20,000`: 80 chunks, total **200,010,000** intervals
  (= `sum_{b=1}^{20000} b`). Summed per-chunk times: sweep 102.251 s,
  verification 3.399 s, total **105.650 s**, exactly the recorded
  `compute_seconds_from_chunks` 105.65 s and the task's stated
  figure. `last_run_wall_seconds` 106.5 s and
  `progress_n20000.json` (`completed_a_up_to` 20000,
  `intervals_so_far` 200,010,000, elapsed 106.49 s) are consistent.
  Aggregated sweep statistics equal `sweep_stats_totals` in
  `solutions_n20000.json` exactly (40,636,278 delta events;
  41,222,761 changed prime records; 10,389 singleton filter passes;
  20,149 pronic passes), the verify files' `candidates_verified`
  sum to 26,100 (= `candidate_totals.union`), and A's own
  `independent_recheck.json` records `all_checks_passed: true`.

### Implementation B (b-partitioned chunks, 250 b-values per chunk)

The verifier aggregated all 80 chunk JSONs in `outputs/`. For every
chunk the recorded `stats.intervals` equals `sum_{b=b_lo}^{b_hi} b`,
the b-ranges are contiguous from 1 to 20,000, and the summed
statistics equal `aggregate_full.json` exactly (200,010,000
intervals; 6 P_0 passes; 6 singleton candidates; stage passes
A 195,472,944, B 24,546,857, C 211,921, D 20,149; 4 near-misses;
20,145 pronic with `c <= b`).

* Gate, `b <= 5,000`: the first 20 chunk files (the gate chunks are
  the first phase of the same run; their per-chunk seconds are the
  ones reused in `aggregate_gate5000.json`) sum to **246.211 s** for
  12,502,500 intervals, exactly the `total_seconds_sum_of_chunks`
  246.211 in `aggregate_gate5000.json`. Per-interval gate cost:
  19.69 µs.
* Full, `b <= 20,000`: summed chunk seconds **7,348.311 s**, exactly
  the `total_seconds_sum_of_chunks` in `aggregate_full.json`
  (7,348.3 s in B's prose). Per-interval full-run cost: 36.74 µs.
  All B timings that the census rests on are therefore
  machine-readable per chunk, as specified. See discrepancy D2 for
  the one figure that is not.

## 3. Independence and filter-soundness assessment

### 3.1 No shared decision code

The verifier read both codebases in full (A: `censusA.py`,
`prime_kernel.c`, `prime_ref.py`, `reverify_reported.py`; B:
`engine.c`, `verify_candidates.py`, `brute_audit.py`,
`aggregate.py`, `run_chunks.sh`) and hashed both trees. The only
common filename is `RESULTS.md`, with different content; no code
file is shared and no file contents are identical. B imports nothing
from A or from the C0 trees (its Python files use only the standard
library; `engine.c` is standalone C). A is, by design, the certified
C0 Implementation 2 prime-by-prime engine scaled (its `prime_ref.py`
is copied unchanged from C0 Impl2), so A is not independent of Wave 0;
the independence that matters here is A versus B, and it holds.

The methods are structurally unrelated. A tracks, for each prime
`p <= b`, the pair `(V_p, S_p)`, derives the denominator exponent
`e_p` and unit part `u_p`, filters singletons by prime-power
conditions at the first 12 primes and the pronic condition by
quadratic residues modulo the first 24 primes above 20,000, and
decides every candidate by a from-scratch strata-sum path plus CRT
assembly. B maintains the reduced fraction `A/B` itself as a custom
bignum pair in a descending-a sweep, and filters singletons by a
transported-residue congruence modulo three primes near `10^9`,
with an unrelated pronic cascade (small-modulus square tests from
exactly tracked unit parts, then Legendre tests). One shared
element, stated and weighed as in CENSUS0: both use the problem's
mathematics of denominator forcing (the singleton condition
`A = -1 (mod B)` with `m = B` forced, and the L = 2 forced
denominator `B = c(c+1)`). That is the mathematics of the problem
statement, not code sharing, and the verifier's spot census
(Section 4) tests singletons by the direct definition on formed
fractions and the L = 2 denominator condition by exact square
testing, so it does not rely on either engine's filter logic.
A's `censusA.py` hardcodes `EXPECTED_SINGLETONS` and
`EXPECTED_DISJOINT` (lines 48 to 50); inspection shows the former is
used exactly once, in the self-test assertion on the exhaustive
scratch verification at `b <= 120` (line 234), and the latter is
never used. The census path never references either constant (the
same finding as CENSUS0 for the C0 ancestor).

### 3.2 Implementation A: scaling changes audited

Three changes from the certified C0 engine were checked. (i) The
singleton filter now uses the first 12 primes instead of 5: each
added prime-power condition is still an exact necessary condition
for `A = -1 (mod B)`, so the filter remains sound (it can only
reject intervals that fail a necessary condition). (ii) The QR
prefilter moduli are the first 24 primes above 20,000 (list verified
in `outputs/selftest.json`: 20011 through 20219, all > MAXN = 20,000,
which is what the delta updates require for invertibility). (iii)
The new sparsity restructuring rests on the lemma in the
`prime_kernel.c` header: for odd `p`, the `v_p(n) = 0` terms over a
complete residue block contribute `sum_{r=1}^{p-1} r^{-1} = sum_r r
= p(p-1)/2 = 0 (mod p)`, since inversion permutes the nonzero
residues. The verifier re-derived this identity; it is correct for
every odd prime, and `p = 2` (where the block sum is 1, not 0) is
updated directly at every step, as the header states. The kernel's
own self-tests (recorded in `outputs/selftest.json`) tie the sweep
state to the scratch path on 369 sampled intervals up to
`b = 20,000` and the scratch path to the pure-Python reference on
all intervals with `b <= 100` plus 14 sampled intervals up to
20,000; Sections 1 and 4 supply further independent corroboration.

### 3.3 Implementation B: filter soundness, re-derived line by line

This is the load-bearing audit for B, because of how little of B's
range is exactly decided (Section 3.4). The verifier read
`engine.c` (795 lines) in full and re-derived each claim.

**Exact substrate (Lemma L1).** Stepping from `[a+1,b]` to `[a,b]`
with `a' = a` forms `N' = A*a' + B`, `M' = B*a'`, `g' = gcd(N', M')`.
The proof that every prime dividing `g'` divides `a'` is correct
(if `p | g'`, `p` not dividing `a'`, then `p | B`, and
`N' = A*a' (mod p)` is nonzero since `gcd(A,B) = 1`). Hence
`g' = gcd(N', D')` with `D' = prod_{p|a'} p^{v_p(M')}`, and the
code's two routes (single pass when `D' < 2^32`, per-prime-power
passes otherwise, with `f = v_p(N')` read off `N' mod p^{v_p(M')}`,
including the `r = 0` case giving `f = v_p(M')`) compute exactly
that gcd. The size bounds in the header check out: `a'` has at most
5 distinct prime factors (the product of the first 6 primes exceeds
20,000), each `p^{e_p} <= 20,000` (the denominator exponent `e_p`
cannot exceed the largest `p`-adic valuation of an integer in the
interval), so `D' = a' * prod p^{e_p} <= 20000^6 < 2^86`, and each
prime-power factor `p^{v_p(M')} <= 20000 * 20000 = 4 * 10^8 < 2^32`,
which is what the divide-by-small passes require. The exponent
array update `ep[p] += v_p(a') - v_p(g')` is exactly
`v_p(B_new) = v_p(M') - v_p(g')`. Bignum capacity: the allocation
`1.5 * b_hi / 64 + 64` limbs gives 34,048 bits at `b = 20,000`;
`log2 B <= psi(20000) / ln 2`, about 28,900 bits, and the largest
intermediates (`B * a'`, `A * a' + B`, `4B + 1` in a `cap + 8`
scratch) stay below about 29,000 bits, so the fixed capacity holds
with roughly 5,000 bits of headroom. The code has no runtime
overflow guard; the headroom is an arithmetic fact about the
bounds, and the end-to-end agreement with A and with Section 4 is
the empirical corroboration.

**Singleton filter.** The transported residues satisfy
`At_j = A * Gamma`, `Bt_j = B * Gamma (mod P_j)` by induction: the
step multiplies `Gamma` by `g'` and divides `A, B` by `g'`, so the
products update inverse-free as `At' = At*a' + Bt`,
`Bt' = Bt*a'`, exactly as coded (all three branches of the
`gp == 1` / `gp < 2^64` / general `u128` case distinction compute
the same residues; `Gamma` is a unit modulo each `P_j` because
every `g'` has all prime factors `<= 20000 < P_j`). The tested
range of `t` is sound: a solution obeys `A + 1 = t * B` over the
integers with `t = (A+1)/B <= H(a,b) + 1 <= H(1,20000) + 1`; the
crude bound `H(1,20000) <= 1 + ln 20000 < 10.91` already gives
`t <= 11`, inside the tested `[1, 12]` (B's stated bound
`H(1,20000) < 10.49` is also correct). Reducing the integer
equality modulo `P_j` and multiplying by `Gamma` gives exactly the
tested congruence, so **a true solution passes all three moduli and
is recorded: the filter never rejects a true solution**. The
moduli in the chunk JSONs are `[1000000007, 1000000009, 998244353]`
as stated. The filter over-admits in principle (rate about `12/P_0`
per interval at the first modulus); measured over the full run it
passed exactly 6 intervals, all true solutions, and every candidate
was then decided exactly by `verify_candidates.py` (common
denominator `lcm(a..b)` integer sums, a method sharing nothing with
the engine).

**L = 2 cascade.** Each stage is a necessary condition for
`4B + 1` to be a perfect square, checked against the code:
Stage A uses `B mod m` tracked exactly (for odd small `p`,
`B mod p` is 0 when `e_p >= 1`, else the unit part `u_p`; the
update `u_p <- u_p * w_a * w_g^{-1} (mod p)`, with `w_a`, `w_g` the
`p`-parts removed, is exactly the unit-part recurrence for
`B <- B * a' / g'`, and the table indices it uses are in range
since `v_p(g') <= v_p(M') <= 28`, the `POWT` table's second
dimension; the mod-64 odd part is maintained the same way with 2s
excluded, and the check reconstructs `B mod 64` from
`2^{e_2} * odd part` correctly, including the `e_2 >= 6` case).
Stages B and C apply Legendre tests to `Gamma^2 * (4B + 1)`,
which differs from `4B + 1` by the square of a unit modulo each
prime (all transport primes exceed 20,000 and are coprime to
`Gamma`), so residue status is preserved and a square is never
rejected. Stage D applies Legendre tests to `(4B + 1) mod P` read
directly off the exact bignum. Survivors of all stages get the
exact decision `s = isqrt(4B + 1)` (Newton iteration on the
fuzz-tested Knuth-D division) with the deciding check the exact
multiplication `s*s == 4B + 1`. Measured: the 20,149 stage-D
survivors are exactly the truly pronic intervals (20,149 =
20,145 with `c <= b` + 4 near-misses), so no stage-D survivor was a
false positive and, by the soundness of each stage, no pronic
interval was rejected earlier.

**Conclusion on B's soundness argument:** the argument in B's
RESULTS Section 1 is rigorous and the code implements it as
stated. No gap was found. The affected-range caveat in the task
does not bite: there is no range in which a gap leaves intervals
decided by an unsound filter.

### 3.4 Filter-decided versus exactly decided

| Implementation | Branch | Exactly decided | Filter-decided (rejected) |
|---|---|---|---|
| A | Singleton + L = 2 (one sweep) | 26,100 candidate intervals (union of 10,389 singleton filter passes and 20,149 pronic passes), each re-derived by `pk_interval` and decided by CRT in Python | 199,983,900 intervals |
| B | Singleton | 6 candidates, decided by `verify_candidates.py` (lcm method) | 200,009,994 intervals |
| B | L = 2 | 20,149 stage-D survivors, decided by exact `isqrt` multiplication in the engine; the 4 near-misses additionally decided in Python | 199,989,851 intervals |

Certification of the filter-decided intervals rests on the filter
soundness established in Sections 3.2 and 3.3 (for A, the method
family was already certified in CENSUS0 and the scaling changes are
audited above; for B, the audit is new and complete), together with
the chunk-level coverage of Section 2 and the third-method spot
census of Section 4.

## 4. The verifier's own spot verification

Code: `code/verifier_c1_spot.py`; record:
`code/verifier_c1_spot_results.json`. The spot method is a third
one, written for this task: for fixed `b`, a descending sweep
maintains the reduced fraction `H(a,b) = A/B` exactly as a Python
integer pair, the step gcd computed as `gcd(N' mod D', D')` (the
same small-gcd identity as B's Lemma L1, independently derived in
the verifier's header, but no bignum library, no Gamma transport,
and different filters). Singleton candidates are screened by the
congruence `A + 1 = t * B (mod R)`, `t in [1,12]`, at the verifier's
own primes `R1 = 2147483647` and `R2 = 4294967291` (both > 20,000,
primality verified in the script; the residues are maintained with
modular inverses of the step gcd, not by transport), and every
survivor is decided exactly on the formed fraction,
`(A + 1) % B == 0`. The L = 2 denominator condition is screened by
quadratic-residue tests on `4B + 1` modulo 64, 3, 5, 7, 11, 13 from
exact small remainders of the formed `B`, plus Legendre tests at
`R1, R2`; every survivor is decided exactly by `isqrt(4B + 1)` and
the multiplication check, and for `c > b` by the residue
`(A + 2c + 1) mod B` on the formed fraction. Before the census
ranges, the script cross-checked its formed fractions against naive
`Fraction` sums on every interval with `b <= 40`, and ran the full
spot census on `b <= 250`, reproducing exactly the six certified
singletons, the four certified near-misses with residues
360, 136, 852, 38766, an empty L = 2 list, and 270 pronic intervals
with `c <= b` (matching B's first chunk statistic).

**Coverage and results.** The full band `2000 < b <= 3000` and
three b-slices of width 100 beyond 10,000 were recomputed
completely (every `a <= b` in each):

| Range | Intervals | Singletons | L = 2 solutions | Near-misses (`c > b`) | Pronic `c <= b` |
|---|---|---|---|---|---|
| 2001..3000 | 2,500,500 | none | none | none | 1,010 |
| 10001..10100 | 1,005,050 | none | none | none | 101 |
| 14951..15050 | 1,500,050 | none | none | none | 101 |
| 19901..20000 | 1,995,050 | none | none | none | 100 |
| **Total** | **7,000,650** | **none** | **none** | **none** | **1,312** |

Every entry matches both implementations restricted to the same
ranges. The pronic `c <= b` counts are an exact, nontrivial
cross-check beyond the headline lists: 1,010 for 2001..3000 equals
both A's pronic candidates in that band and the sum of B's chunk
statistics over its four chunks covering 2001..3000, and the slice
counts 101, 101, 100 equal A's pronic candidates in those bands
exactly. The singleton filter passed 0 intervals in all four ranges
(expected false-pass count at the stated rate is below 0.1), so no
interval in the spot ranges even survived screening, and all
7,000,650 intervals were nevertheless carried through the exact
sweep with the L = 2 survivors (1,754,901 screen passes in total)
each decided by the exact square test. Spot runtime: 827.5 s
summed over the four ranges (79.24, 88.51, 202.03, 457.73 s).

## 5. Stretch projection data for b <= 100,000 (data only; the stretch was NOT run)

Interval count at `N = 100,000`: `100,000 * 100,001 / 2 =
5,000,050,000`, which is 24.999 times the 20,000 count.

### Implementation A

Measured per-interval costs (from the chunk sums verified in
Section 2): 0.330 µs at `N = 5,000` (4.123 s / 12,502,500) and
0.528 µs at `N = 20,000` (105.650 s / 200,010,000).

* Flat per-interval projection: `5,000,050,000 * 0.528 µs =
  2,640 s`, about **44 minutes**.
* Power-law fit through the two measured points (per-interval cost
  proportional to `N^0.339`): per-interval cost at 100,000 about
  0.91 µs, total about **4,556 s, about 76 minutes**. A's own stated
  range, 0.75 to 1.5 hours on one worker, is consistent with these
  two figures.
* Memory (A's flagged caveat, verified): the prefix-inverse tables
  hold one `uint16` per entry with entry counts scaling as the sum
  of the primes up to `N`. The verifier recomputed the prime sums:
  `sum_{p <= 20000} p = 21,171,191` (42 MB at 2 bytes per entry) and
  `sum_{p <= 100000} p = 454,396,537`, giving 908,793,074 bytes,
  about **909 MB**, at `N = 100,000`, a factor 21.46 growth. The
  kernel is compiled with `MAXN = 20,000` and would need a rebuild;
  at about 909 MB the tables exceed comfortable headroom on this
  shared 8 GB VM and would need a memory adaptation before a
  100,000 run. **A's stretch bottleneck is memory, not time.**

### Implementation B

Measured per-interval costs (from the chunk sums verified in
Section 2): 19.69 µs at `b <= 5,000` (246.211 s / 12,502,500) and
36.74 µs at `b <= 20,000` (7,348.311 s / 200,010,000). The three
standard extrapolations disagree widely, and all three are reported
as data:

* Flat per-interval: `5,000,050,000 * 36.74 µs = 183,700 s`, about
  **51 hours** on one worker (about 25.5 hours on the two workers
  B used).
* Power-law fit through the two measured points (per-interval cost
  proportional to `N^0.450`): per-interval cost at 100,000 about
  75.8 µs, total about **379,000 s, about 105 hours** on one worker
  (about 53 hours on two).
* B's own gate model (total time proportional to `sum_b b^2`, the
  model B used for its gate projection): the ratio
  `sum_{b<=100000} b^2 / sum_{b<=20000} b^2 = 124.99` gives about
  **918,500 s, about 255 hours** on one worker (about 128 hours on
  two). This model overshot at the 20,000 gate (it projected about
  15,750 s against the measured 7,348.3 s, because the gate timings
  were contention-inflated), so it is best read as an upper envelope.
* Memory (derived from `engine.c`, not measured): the bignum
  capacity formula `1.5 * b_hi / 64 + 64` limbs gives 2,407 limbs,
  about 19.3 KB per bignum, at `b_hi = 100,000`, with about ten live
  bignums (under 0.2 MB in total). The fixed tables would need
  resizing for the 9,592 primes up to 100,000: `POWT` from
  `[2262][29][14]` to `[9592][29][14]` bytes (about 3.9 MB) and
  `Wtab` to about 1.4 MB; the sieve arrays are negligible. Total
  well under 10 MB. `NMAX` is hardcoded 20,000 and would need a
  rebuild. **B's stretch bottleneck is time, not memory** (on the
  most optimistic model it is still about 70 times A's flat
  projection).

## 6. Discrepancies and record defects (complete list)

No discrepancy was found in any solution list, near-miss list,
coverage count, sweep statistic, or chunk-compute timing total.
The following record defects and prose imprecisions were found;
none affects a verdict.

* **D1 (A, gate wall time).** `solutions_n5000.json` records
  `last_run_wall_seconds: 0.07` and `progress_n5000.json` records
  `elapsed_seconds: 0.07`: both are the resume re-run's figures
  (A's RESULTS discloses the resume). The original gate run's wall
  time, 4.25 s, appears only in A's prose RESULTS; it is not in any
  JSON. The gate's chunk-compute total, the figure the gate
  decision rested on, is fully machine-recorded and verified
  (Section 2). This is the same class of defect the C0 verifier
  flagged in C0 Implementation 2's records.
* **D2 (B, total wall time).** B's prose "wall time about 73
  minutes on two workers" is not machine-recorded anywhere. The
  worker logs on disk (`outputs/worker1.log`, `worker2.log`) cover
  only the post-restart session, 17:36:53 to 18:15:25 EDT (the
  logs begin at the relaunched chunks 72 and 73), so the full
  run's wall span cannot be reconstructed from records. The
  authoritative timing record is the per-chunk `seconds` sum,
  7,348.311 worker-seconds, verified in Section 2; it is
  consistent with the prose figure (about 61 worker-minutes of
  compute per worker plus the disclosed restart), but the 73
  minutes itself is prose-only.
* **D3 (A, prose ratio).** A's RESULTS calls the 100,000 interval
  count "exactly 25.00x" the 20,000 count; the exact ratio is
  24.999 (5,000,050,000 / 200,010,000). A's projection totals were
  computed from per-interval costs, not from the ratio, and are
  unaffected (Section 5).
* **D4 (A, table entry count).** A's stated prefix-table entry
  counts, 21,171,191 at 20,000 and 454,396,537 at 100,000, are the
  sums of all primes up to `N` (verified by the verifier's own
  prime sums). The tables are built for odd primes only, so the
  exact entry counts are smaller by 2 (the prime 2's entries),
  a 4-byte difference at either scale; the 42 MB and 909 MB
  figures are unaffected at the stated precision.
* **D5 (A, kernel init times).** `kernel_init_seconds` is 0.837 in
  `selftest.json`, 0.304 in `solutions_n5000.json`, and 0.244 in
  `solutions_n20000.json`. A's RESULTS explains the spread (the
  first process included the one-time gcc build; later processes
  loaded the prebuilt `.so`), and all three figures are
  machine-recorded, so this is a resolved note, not a defect.
* **D6 (B, gate chunk reuse).** `aggregate_gate5000.json` is an
  aggregation of the same first 20 chunk files that the full run
  later aggregated into `aggregate_full.json` (per-chunk seconds
  identical), i.e. the gate was the first phase of the single run
  rather than a separate run. This is consistent with B's RESULTS
  and is recorded here only so the gate figures are not mistaken
  for an independent second measurement.

## Summary

Both branches of the census extension to `b <= 20,000` are
**EXTENSION CERTIFIED**. The two implementations, which share no
decision code, produce identical singleton lists (exactly the six
certified solutions, none new in `(2000, 20000]`), identical empty
L = 2 lists, and identical near-miss lists (exactly the four
certified intervals, none with `b > 2000`), with chunk-level
coverage of all 200,010,000 intervals verified for both, all
chunk-compute timings verified against the JSON records,
Implementation B's filter soundness re-derived from its code with
no gap found, and a third-method spot census over 7,000,650
intervals in the extension range (including the complete band
`2000 < b <= 3000`) reproducing both implementations exactly,
pronic sub-counts included.

Nothing was posted, emailed, or submitted anywhere.
