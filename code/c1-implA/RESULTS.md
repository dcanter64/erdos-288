# Erdős #288, Cluster C1, Implementation A (prime-by-prime extension): Results

Both branches are complete at full coverage to **b ≤ 20,000**. There are
**no new singleton solutions** with 2000 < b ≤ 20,000 and **no L = 2
solutions** at any b ≤ 20,000; the L = 2 near-miss list is unchanged from
Wave 0 (the same four intervals, all with b ≤ 156). The b ≤ 2000 segment
reproduces the certified Wave 0 census exactly.

| Branch | Coverage reached | New solutions in 2000 < b ≤ 20,000 |
|---|---|---|
| Singletons | all 200,010,000 intervals [a,b], 1 ≤ a ≤ b ≤ 20,000 | **none** (complete list for b ≤ 20,000 is still the six below) |
| L = 2 disjoint ([a,b] + [c,c+1], b < c, any c) | same sweep; c is forced by B, so c is unbounded in effect | **none**; near-miss list unchanged (four intervals, all b ≤ 156) |

## Benchmark gate (mandatory, run before the 20,000 run)

The singleton-branch sweep (both filters run in the same sweep) was
first run at N = 5,000, timed from the per-chunk JSON records:

| Quantity | Measured at N = 5,000 |
|---|---|
| Intervals | 12,502,500 (= 5000·5001/2) |
| Sweep compute (sum of chunk `sweep_seconds`) | 3.60 s |
| Candidate verification (sum of chunk `verify_seconds`) | 0.52 s |
| Total chunk compute | 4.12 s |
| Run wall time (in-process, excludes interpreter/kernel load) | 4.25 s |
| Per-interval cost (total compute / intervals) | 0.330 µs |

Projection to N = 20,000 made at the gate: interval count grows by
200,010,000 / 12,502,500 = 15.997, so flat per-interval projection
4.12 s × 15.997 ≈ **66 s**, far below the three-day stop threshold, so
the 20,000 run proceeded. The actual 20,000 run took 105.65 s of chunk
compute (sweep 102.25 s + verification 3.40 s; in-process wall 106.5 s):
per-interval cost grew to 0.528 µs, a factor 1.60 above the flat
projection (attributable to the larger valuation ranges and divisor
structure of integers up to 20,000). Both the projection and the actual
figure are three orders of magnitude inside the gate limit.

## Singleton branch

Complete solution list for b ≤ 20,000 (identical to Wave 0; every record
re-verified by direct `Fraction` summation in
`reverify_reported.py`, see Validation):

| a | b | H(a,b) | m = B | disjoint (B > b) |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | no |
| 1 | 2 | 3/2 | 2 | no |
| 2 | 2 | 1/2 | 2 | no |
| 1 | 3 | 11/6 | 6 | yes |
| 2 | 3 | 5/6 | 6 | yes |
| 3 | 6 | 19/20 | 20 | yes |

**New solutions with 2000 < b ≤ 20,000: none (explicit empty list).**
The b ≤ 2000 segment of this run yields exactly the certified six, and
its disjoint subset exactly {(1,3,6), (2,3,6), (3,6,20)}, matching
`../c0-impl2/outputs/solutions.json` record for record (checked
programmatically in the re-verification script).

## L = 2 branch

By the Wave 0 reduction, a solution forces B = c(c+1) exactly with
c > b, and then integrality is the single congruence
A + 2c + 1 ≡ 0 (mod B). Among all 200,010,000 intervals, exactly
20,149 have pronic reduced denominator B (and every one of the 20,149
quadratic-residue prefilter passes was genuinely pronic: the prefilter
had zero false positives at this scale). Their breakdown:

- 19,999 are the two-term intervals [n, n+1] themselves (B = n(n+1),
  c = n < b, structurally barred);
- 140 are one-term intervals [n, n] with n = c(c+1) pronic (c ≤ 140,
  c < b unless n is a near-miss case, none is);
- 6 are short intervals with c ≤ b: (1,3), (1,4), (1,6), (2,4), (2,6),
  (3,6);
- **4 have c > b: the near-miss list below, unchanged from Wave 0.**

Near-miss table (complete for b ≤ 20,000; each recomputed exactly from
scratch, A and B by direct `Fraction` summation; residue =
(A + 2c + 1) mod B):

| a | b | B | c | A | residue | exact sum H(a,b) + H(c,c+1) |
|---|---|---|---|---|---|---|
| 4 | 7 | 420 | 20 | 319 | 360 | 6/7 |
| 5 | 7 | 210 | 14 | 107 | 136 | 68/105 |
| 9 | 12 | 1,980 | 44 | 763 | 852 | 71/165 |
| 154 | 156 | 1,861,860 | 1364 | 36,037 | 38,766 | 71/3410 |

All four residues are nonzero and all four exact sums are non-integers,
exactly as certified in Wave 0. **No interval with 2000 < b ≤ 20,000
even meets the denominator condition with c > b**, and the L = 2
solution list for b ≤ 20,000 is empty.

## Scaling projection for b ≤ 100,000 (measured; the 100,000 range was NOT run)

Measured total per-interval costs: 0.330 µs at N = 5,000 (12,502,500
intervals, 4.12 s) and 0.528 µs at N = 20,000 (200,010,000 intervals,
105.65 s). The interval count at N = 100,000 is
100,000·100,001/2 = 5,000,050,000, exactly 25.00× the 20,000 count.

- Flat per-interval projection: 5,000,050,000 × 0.528 µs ≈ 2,640 s
  ≈ **44 minutes**.
- Power-law fit through the two measured points (per-interval cost
  ∝ N^0.34): per-interval cost at 100,000 ≈ 0.91 µs, total ≈ 4,560 s
  ≈ **76 minutes**.
- Candidate verification adds little: at N = 20,000 it was 3.40 s of
  the 105.65 s total; candidate counts grow roughly linearly in N
  (≈100,000 structural pronic intervals at N = 100,000).

**Projected total for b ≤ 100,000: roughly 0.75 to 1.5 hours** on one
worker process of this VM. Engineering caveats for the stretch
decision: the kernel is compiled with MAXN = 20,000 and would need a
rebuild; its prefix-inverse tables hold sum-of-primes-many uint16
entries, 21,171,191 entries (42 MB) at N = 20,000 but 454,396,537
entries (≈909 MB) at N = 100,000, which exceeds comfortable headroom
on this shared 8 GB VM and would need a memory adaptation (for example
on-demand partial sums for large primes) before a 100,000 run; the QR
moduli would move to the first 24 primes above 100,000.

## Timing records (machine-readable)

All timings below are stored in the JSON outputs, not only in this
prose: per-chunk `sweep_seconds` in `outputs/chunk_a*_n{N}.json`,
per-chunk `verify_seconds` in `outputs/verify_a*_n{N}.json`, totals in
`outputs/solutions_n{N}.json` (`compute_seconds_from_chunks`,
`last_run_wall_seconds`, `kernel_init_seconds`), and
`outputs/selftest.json` (`kernel_init_seconds`, `self_test_seconds`).

| Run | Intervals | Sweep s | Verify s | Compute s | Wall s | µs/interval |
|---|---|---|---|---|---|---|
| Kernel init (once per process) | n/a | n/a | n/a | 0.24 with prebuilt .so; 0.84 in the first process, which included the one-time gcc build | n/a | n/a |
| Self-tests | n/a | n/a | n/a | 5.66 | 6.7 (shell) | n/a |
| N = 5,000 (gate) | 12,502,500 | 3.60 | 0.52 | 4.12 | 4.25 | 0.330 |
| N = 20,000 | 200,010,000 | 102.25 | 3.40 | 105.65 | 106.5 | 0.528 |

Sweep statistics (from `solutions_n20000.json`): 200,010,000 intervals,
40,636,278 delta events, 41,222,761 changed prime records, 10,389
singleton filter passes, 20,149 pronic prefilter passes, overflow flag
0 in every chunk; 26,100 distinct candidates verified exactly.
Checkpointing is per chunk of 250 a-values (80 chunks at N = 20,000);
re-running resumes from the chunk files (verified: a resume re-run of
the N = 5,000 census completed in 0.07 s of wall time with identical
totals). One worker process was used throughout.

## Method (summary; full detail in the code headers)

The engine is the certified C0 Implementation 2 prime-by-prime method,
scaled. For each prime p ≤ b the kernel tracks (V_p, S_p) and derives
the reduced denominator exponent e_p and unit part u_p; the singleton
condition A ≡ −1 (mod B) is tested as the conjunction of prime-power
conditions at the first **12** primes (C0 used 5), with R_f maintained
through the cofactor C_f = (B / f^{e_f}) mod f^{Vmax_f} described in the
kernel header; the pronic condition is prefiltered by 4B + 1 being a
quadratic residue modulo the first **24 primes above 20,000** (C0 used
12 primes above 2000; the moduli must exceed the new MAXN so the delta
updates stay invertible). One scaling restructuring: for odd p, the
non-divisor terms' contributions to S_p cancel over complete residue
blocks (Σ_{r=1}^{p−1} r^{−1} ≡ 0 mod p), so the sweep updates only the
distinct prime divisors of each new index, folding the initial partial
block in from a precomputed prefix-inverse table; p = 2 is updated
directly at every step. Every filter is an exact necessary condition,
and every candidate (26,100 at N = 20,000) was re-derived from scratch
by the kernel's fixed-V strata-sum path (`pk_interval`, a different
accumulation path from the sweep) and decided by CRT assembly in Python
big integers. All decisions are exact integer/modular arithmetic; no
floating point enters any decision.

## Validation performed

In `censusA.py` self-tests (all passed before the census runs;
`outputs/selftest.json`): pure-Python `prime_ref` against `Fraction`
on all 820 intervals with b ≤ 40; kernel scratch against `prime_ref`
on all 5,050 intervals with b ≤ 100 and on 14 sampled intervals with
b up to 20,000; exhaustive scratch verification at b ≤ 120 reproducing
exactly the six singletons, no L = 2 solution, and all 138 pronic
intervals contained in the sweep's candidate set; incremental sweep
state (e_p, u_p, R_f, B-residues for all filter and QR primes) against
scratch factorisation on 369 sampled intervals up to b = 20,000,
including (1, 20000) and (7, 19999).

Independent re-verification (`reverify_reported.py` →
`outputs/independent_recheck.json`, `all_checks_passed: true`): chunk
files aggregate contiguously to exactly 12,502,500 (N = 5,000) and
200,010,000 (N = 20,000) intervals with overflow 0 everywhere; all six
singletons and all four near-misses recomputed by direct `Fraction`
summation and checked from the definitions (the near-miss exact sums
match the Wave 0 verifier's table); the b ≤ 2000 segments compared
record for record against the certified C0 outputs; a seeded random
sample of 150 intervals with 2000 < b ≤ 20,000 recomputed with the
pure-Python `prime_ref` path agreed with the kernel on B and A mod B
and contained no singleton or L = 2 solution.

## Files

- `censusA.py`: driver, self-tests, checkpointed sweep and verification.
- `prime_kernel.c`: scaled prime-by-prime kernel (sparse divisor-update
  sweep, strata-sum scratch path); compiled to `prime_kernel.so` on
  first run. The C0 originals in `../c0-impl2/` are untouched.
- `prime_ref.py`: pure-Python prime-by-prime reference and CRT assembly,
  copied unchanged from C0 Impl2.
- `reverify_reported.py`: independent re-verification described above.
- `outputs/solutions_n5000.json`, `outputs/solutions_n20000.json`:
  machine-readable results with measured timings.
- `outputs/chunk_*.json`, `outputs/verify_*.json`,
  `outputs/progress_n*.json`, `outputs/selftest.json`,
  `outputs/independent_recheck.json`: checkpoints and validation
  records.
