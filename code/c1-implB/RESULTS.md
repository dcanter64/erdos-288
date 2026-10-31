# Erdős #288, Cycle 1, Cluster C1, Implementation B: Results

Independent multi-modular implementation, written from scratch for
this task (`engine.c` in this directory; no code from `c0-impl1`,
`c0-impl2`, or `c1-implA` was copied or adapted; the only external
input was the certified target values in `../../CENSUS0.md`).

## Headline results

- **Singleton branch, full coverage `b <= 20,000`.** The complete
  solution list is exactly the six certified solutions
  `(a,b,m) = (1,1,1), (1,2,2), (2,2,2), (1,3,6), (2,3,6), (3,6,20)`.
  **New solutions in `(2000, 20000]`: none (explicit empty list).**
  The `b <= 2000` segment returns exactly the certified six, as
  required. The disjoint solutions are exactly
  `(1,3,6), (2,3,6), (3,6,20)`.
- **L = 2 disjoint branch, full coverage `b <= 20,000`** (pairs
  `[a,b]`, `[c,c+1]`, `b < c`, any `c`). **Solution list: empty.**
  The complete near-miss list (intervals meeting the denominator
  condition `den H(a,b) = c(c+1)`, `c > b`) is exactly the four
  certified intervals; **no new near-misses occur for
  `2000 < b <= 20000`** either. Table in Section 4.
- Coverage actually reached: `b = 20,000` in both branches, all
  `200,010,000 = 20000*20001/2` intervals examined (aggregator
  verified contiguity of the 80 chunk ranges and the exact interval
  count; see `outputs/aggregate_full.json`).

## 1. Filter design and soundness argument

### 1.1 Exact substrate

For fixed `b`, the engine sweeps `a = b, b-1, ..., 1` maintaining the
reduced fraction `H(a,b) = A/B` exactly as a custom bignum pair
(64-bit limbs; operations needed are only multiply-by-small, add,
modulo-by-small, divide-by-small). Stepping from `[a+1,b]` to `[a,b]`
with `a' = a` forms `N' = A*a' + B`, `M' = B*a'`, and reduces by
`g' = gcd(N', M')`.

**Lemma L1 (the step gcd is small and structured).** Every prime
dividing `g'` divides `a'`. Proof: if `p | g'` and `p` does not
divide `a'`, then `p | M' = B*a'` forces `p | B`; but then
`N' = A*a' + B` is congruent to `A*a'` modulo `p`, which is nonzero
because `gcd(A,B) = 1` and `p` does not divide `a'`. Hence, with
`e_p` denoting the exponent of `p` in the current `B`,
`g' | D' := prod_{p|a'} p^{e_p + v_p(a')}`, and in fact
`g' = gcd(N', D')` because `D' | M'`. Numerically
`D' = a' * prod_{p|a'} p^{e_p} <= 20000 * 20000^5 < 2^86`, and each
prime-power factor is `< 2^32`, so `g'` is computed by
modulo-by-small passes over `N'` (a single pass with modulus `D'`
when `D' < 2^32`, per-prime-power passes otherwise) and the
reductions of `N'`, `M'` are divide-by-small passes. The exponents
`e_p` are maintained exactly in an array indexed by primes.

### 1.2 The multi-modular singleton filter

Moduli: the three large primes
`P_0 = 1000000007`, `P_1 = 1000000009`, `P_2 = 998244353`, all
greater than `20000`, hence coprime to every `A`, `B` and every `g'`
encountered (all of whose prime factors are `<= 20000`).

For each `j`, the engine maintains the *transported* residues

```
At_j = A * Gamma  (mod P_j),   Bt_j = B * Gamma  (mod P_j),
Gamma = product of all step gcds g' in the current b-sweep.
```

Transport identity: since `A_new = N'/g'` and
`Gamma_new = Gamma * g'`, the division by `g'` cancels against
`Gamma`, giving the inverse-free updates

```
At' = At*a' + Bt,   Bt' = Bt*a',   Gamma' = Gamma*g'   (mod P_j),
```

which is how the residues are in fact updated.

**Filter.** An interval is a *candidate* iff for some `t` in
`[1, 12]`, `At_0 + Gamma_0 = t * Bt_0 (mod P_0)` and the same `t`
also satisfies the congruence modulo `P_1` and `P_2`.

**Soundness (the filter never rejects a true solution).** Suppose
`H(a,b) = A/B` in lowest terms is a singleton solution:
`A = -1 (mod B)`, i.e. `A + 1 = t*B` over the integers for a unique
integer `t`. Since `0 < H(a,b) <= H(1,20000) < 10.49` and
`t = floor(H) + 1` (also when `H` is an integer, where `B = 1` and
`t = H + 1`), every solution has `t` in `[1, 11]`, inside the tested
range `[1, 12]`. By induction on the sweep, the maintained residues
satisfy `At_j = A*Gamma`, `Bt_j = B*Gamma (mod P_j)` with
`Gamma` a product of integers each coprime to `P_j`, so `Gamma` is a
unit modulo `P_j`. Reducing the integer equality `A + 1 = t*B`
modulo `P_j` and multiplying by `Gamma` gives exactly the tested
congruence `At_j + Gamma_j = t * Bt_j (mod P_j)`. Hence every true
solution passes all three moduli and is recorded as a candidate.
The filter may over-admit (a random interval passes `P_0` with
probability about `12/P_0`); candidates are therefore always decided
by an independent exact computation (Section 3), never by the
filter.

Measured behaviour: over all 200,010,000 intervals, the `P_0` stage
passed exactly 6 intervals, the three-modulus filter produced
exactly 6 candidates, and all 6 are true solutions. Zero false
candidates occurred (the expectation from the `12/P_0` rate was
about 2.4 false `P_0` passes; observing 0 is unremarkable).

### 1.3 The L = 2 filter (forced denominator) and pronic cascade

`H(c,c+1) = (2c+1)/(c(c+1))` is in lowest terms
(`gcd(2c+1, c) = gcd(2c+1, c+1) = 1`), and integrality of
`H(a,b) + H(c,c+1)` forces `den H(a,b) = c(c+1)` (the
forced-denominator background fact recorded in `CENSUS0.md`). This
covers every `c > b` with no bound on `c`, since `B` itself is
computed exactly. So an L = 2 solution requires `B` pronic,
`B = c(c+1)` with `c > b`, and then `B | A + 2c + 1`.

Stages, each sound (a pronic `B` passes every stage):

- **Stage A (small moduli).** `4B+1` must be a perfect square, so
  its reduction must be a square modulo `m` for `m = 64` and each
  prime `p <= 47`. `B mod m` is tracked *exactly*, not transported
  through `Gamma` (an early version transported it; because `Gamma`
  accumulates small prime factors, the transported value was
  `0 mod p` for most intervals and the stage was nearly vacuous; it
  was replaced). For each small prime `p`, `B mod p` is `0` when
  `e_p >= 1`, else the unit part `u_p = (B / p^{e_p}) mod p`,
  maintained by the exact update
  `u_p <- u_p * w_a * w_g^{-1} (mod p)`, where `w_a` is `a'` with
  its `p`-part removed and `w_g` is `g'` with its `p`-part removed
  (a `p`-unit, invertible mod `p`); the odd part of `B` modulo 64 is
  maintained the same way. Soundness: if `4B+1 = s^2` in the
  integers, then `4B+1 mod m` is a square mod `m` by reduction.
- **Stages B and C (Legendre, large primes).** For the three filter
  primes and seven further primes near `10^9` (generated and
  Miller-Rabin verified at startup), the transported value
  `Gamma^2 * (4B+1) = Gamma * (4*Bt + Gamma) (mod P)` must be a
  quadratic residue mod `P`: it differs from `4B+1` by the square
  factor `Gamma^2` with `Gamma` a unit mod `P`, so residue status is
  preserved. Reject when the Legendre symbol is `-1`.
- **Stage D (Legendre, direct).** For 20 further startup-generated
  primes near `10^9`, `(4B+1) mod P` is read off the exact bignum
  `B` and the same Legendre test applied.
- **Exact pronic decision.** Survivors get `s = isqrt(4B+1)` by
  Newton iteration on a Knuth Algorithm D bignum division, and the
  decision is the exact multiplication check `s*s == 4B+1`; then
  `c = (s-1)/2`. Near-misses (`c > b`) are recorded and decided
  exactly in Python (Section 3); pronic intervals with `c <= b` are
  counted (they cannot be disjoint L = 2 solutions).

Measured behaviour over the full run: stage totals
A: 195,472,944 passes; B: 24,546,857; C: 211,921; D: 20,149.
The 20,149 stage-D survivors are *exactly* the truly pronic
intervals: `20,149 = 4` near-misses `+ 20,145` pronic with `c <= b`,
and the exact isqrt test confirmed every one of them. No stage-D
survivor was a false positive in 200,010,000 intervals.

## 2. Benchmark gate at b <= 5,000

The gate was run first, in 20 chunks of 250 in `b`, on one worker,
while an unrelated audit process shared the VM (engine-recorded
chunk seconds are therefore contention-inflated and conservative):

- Gate result at `b <= 5000`: singleton candidates exactly the six
  certified solutions; L = 2 near-misses exactly the four certified
  intervals; no candidates of either kind in `(2000, 5000]`.
- Gate engine time (sum of per-chunk records): **246.2 s** for
  12,502,500 intervals.
- Projection: per-`b` cost grows like `b^2` (steps per `b` times
  bignum size per step), so total time scales like `sum b^2`;
  projecting the gate measurement to `b <= 20000` gave
  `246.2 * (sum_{b<=20000} b^2)/(sum_{b<=5000} b^2)`
  which is about **15,750 s single-worker, about 2.2 h on the two
  permitted workers**, far below the three-day stop rule. The gate
  was passed and the run continued to 20,000.
- Actual full-run total: **7,348.3 engine-seconds** summed over all
  80 chunks (the projection overshot because the gate timings were
  contention-inflated), wall time about 73 minutes on two workers
  including one restart (Section 5).

## 3. Independent exact verification of candidates

`verify_candidates.py` (in this directory) re-decides every
candidate by a method independent of the engine: for `[a,b]` it
builds `D = lcm(a..b)` from prime powers, forms the integer
`X = sum_{n=a}^b D // n`, and reduces `X/D` by `gcd`. Over the full
run there were only 6 singleton candidates and 4 near-misses to
decide; all were decided as follows (record:
`outputs/verify_full.json`).

Singleton candidates, all confirmed solutions, with `m = B`:

| (a, b) | m | t = (A+1)/B | disjoint (m > b) |
|---|---|---|---|
| (1, 1) | 1 | 2 | no |
| (1, 2) | 2 | 2 | no |
| (2, 2) | 2 | 1 | no |
| (1, 3) | 6 | 2 | yes |
| (2, 3) | 6 | 1 | yes |
| (3, 6) | 20 | 1 | yes |

## 4. L = 2 near-miss table (complete for b <= 20,000)

Every interval with `den H(a,b) = c(c+1)`, `c > b`, in the whole
range. All four have `b <= 156`; none occur for `b > 2000`, hence
none in `(2000, 20000]`. Each fails the integrality test: the
residue `(A + 2c + 1) mod B` is nonzero and the exact sum
`H(a,b) + H(c,c+1)` is a non-integer (values recomputed by the
independent verifier; they agree with `CENSUS0.md` digit for digit).

| (a, b) | B | c | A | (A + 2c + 1) mod B | exact sum |
|---|---|---|---|---|---|
| (4, 7) | 420 | 20 | 319 | 360 | 6/7 |
| (5, 7) | 210 | 14 | 107 | 136 | 68/105 |
| (9, 12) | 1980 | 44 | 763 | 852 | 71/165 |
| (154, 156) | 1,861,860 | 1364 | 36,037 | 38,766 | 71/3410 |

**L = 2 solution list for `b <= 20,000`: empty.**

Pronic intervals with `c <= b` (denominator condition met but not
disjoint-admissible): 20,145 in total over the full range (2,049 of
them at `b <= 2000`, matching the audits below).

## 5. Audits, anomalies, and timing records

Audits performed, in increasing range:

1. **C self-tests** (`./engine --selftest`, run before every
   production binary use): Knuth-D divmod fuzzed on 4,000 random
   pairs (identity `a = q*b + r`, `r < b`, checked by independent
   multiplication/addition); integer sqrt fuzzed on 300 random
   values plus 100 exact squares. `SELFTEST OK`.
2. **Python brute force, `b <= 300`** (`brute_audit.py`: prefix
   harmonic numbers as exact `Fraction`s, a method sharing no code
   or structure with the engine): singleton list, near-miss list,
   and pronic-`c <= b` count (321) all identical to the engine.
3. **Python brute force, `b <= 2000`** (same independent code,
   a few minutes of wall time): singletons exactly the certified six, near-misses
   exactly the certified four, L = 2 solutions empty, pronic
   `c <= b` count 2,049, all identical to the engine's outputs on
   the same range. This also confirms the required `b <= 2000`
   behaviour against `CENSUS0.md` independently of the engine.
4. **Candidate verification** (Section 3) over the full run.

Anomaly: at 17:23 EDT the two worker processes died simultaneously
(an aborted monitoring session's cleanup reached them) with chunks
72 and 73 (b = 18001..18500) incomplete. Their locks and partial
`.tmp` outputs were removed, the workers were relaunched detached,
and both chunks were recomputed from scratch; the affected ranges
appear in the final aggregation exactly once, and total coverage
and interval counts check exactly (Section "Headline results").
No other anomalies; no claimed result rests on the interrupted
partial outputs.

Timing records: every chunk JSON in `outputs/` carries its own
`"seconds"` field (engine-measured, `CLOCK_MONOTONIC`), its full
filter-stage statistics, and its candidate and near-miss lists, so
the run is machine-readably timed chunk by chunk as specified.
`outputs/aggregate_full.json` (produced by `aggregate.py`) holds
the merged record: 80 chunks, contiguous coverage `1..20000`,
200,010,000 intervals, summed engine time 7,348.3 s, per-chunk
seconds table, merged statistics:

```
intervals                 200,010,000
singleton P_0 passes              6
singleton candidates              6
L2 stage A passes       195,472,944
L2 stage B passes        24,546,857
L2 stage C passes           211,921
L2 stage D passes            20,149
L2 near-misses                    4
L2 pronic, c <= b            20,145
```

Per-branch coverage summary: singleton branch reached
`b = 20,000` (not the fallback frontier; the gate projection was
met). L = 2 branch reached `b = 20,000` with `c` unbounded (the
forced-denominator test is applied to the exact denominator `B`,
which ranges over all sizes). New-solution lists for
`(2000, 20000]`: **singleton: empty. L = 2: empty.**

## 6. Files

- `engine.c`: the complete engine (bignum, filters, sweep, chunk
  JSON writer); build with `gcc -O3 -march=native -o engine engine.c`.
- `run_chunks.sh`: resumable two-worker chunk driver (chunks of 250
  in `b`, atomic lock claiming, descending order).
- `brute_audit.py`: independent `Fraction`-prefix brute force used
  for the `b <= 300` and `b <= 2000` audits.
- `verify_candidates.py`: independent exact candidate decider
  (common-denominator integer sums).
- `aggregate.py`: chunk aggregation and coverage checker.
- `outputs/chunk_0001_0250.json` ... `outputs/chunk_19751_20000.json`:
  the 80 machine-readable chunk records.
- `outputs/aggregate_full.json`, `outputs/aggregate_gate5000.json`:
  merged records for the full run and for the gate.
- `outputs/verify_full.json`, `outputs/verify_gate.json`:
  independent verification records.
- `outputs/brute_300.json`, `outputs/brute_2000.json`: audit outputs.
- `outputs/worker1.log`, `outputs/worker2.log`: driver logs.

Nothing was posted, emailed, or submitted anywhere.
