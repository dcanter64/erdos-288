# Erdős #288, Cluster C0, Implementation 2 (prime-by-prime): Results

All three tasks are complete at full coverage. Every published expectation
was reproduced exactly; there is no disagreement anywhere.

| Task | Published expectation | This implementation | Verdict |
|---|---|---|---|
| (i) Singletons, b ≤ 1600 | exactly six solutions | exactly the same six | AGREE |
| (ii) Singletons, b ≤ 2000, disjoint ones | only (1,3,6), (2,3,6), (3,6,20) disjoint | same six solutions in total, same three disjoint | AGREE |
| (iii) L = 2 disjoint branch, b ≤ 2000, c unbounded | no solutions | no solutions | AGREE |

Coverage actually reached: all 2,001,000 intervals [a,b] with
1 ≤ a ≤ b ≤ 2000 (= 2000·2001/2), which includes task (i)'s range
b ≤ 1600 in full. Nothing was truncated.

## Method

### Prime-by-prime representation (the primary engine)

No global fraction H(a,b) is ever formed in the census pipeline. For each
prime p ≤ b (303 primes at b = 2000) and each interval [a,b] the engine
tracks, prime by prime:

- V_p = max over n in [a,b] of v_p(n), the largest p-adic valuation in the
  interval;
- S_p = (p^{V_p} · H(a,b)) mod p^{V_p+1}, a residue in the p-adic integers,
  maintained by the transition rules for appending a term 1/n, where
  v = v_p(n) and w = (n/p^v)^{-1} mod p^{v+1} is a precomputed modular
  inverse:
  - if v ≤ V_p: S_p ← S_p + p^{V_p−v}·w (mod p^{V_p+1});
  - if v > V_p: S_p ← p^{v−V_p}·S_p + w (mod p^{v+1}), and V_p ← v.

  The stored precision p^{V_p+1} is exactly what these transitions consume
  (in the second case S_p is needed mod p^{V_p+1} and no more), and each
  summand is smaller than the modulus, so the update is one multiplication,
  one addition and one conditional subtraction in 32-bit integer arithmetic.

From (V_p, S_p) the local data of the reduced fraction H(a,b) = A/B are
read off exactly: with t = v_p(S_p) (and S_p ≠ 0), the exponent of p in B is
e_p = V_p − t if t < V_p, else e_p = 0; the unit part is
u_p = (S_p/p^t) mod p^{e_p}, i.e. p^{e_p}·H(a,b) ≡ u_p in Z_(p). Then
B = ∏ p^{e_p} and A mod p^{e_p} = u_p · ((B/p^{e_p}) mod p^{e_p}) mod p^{e_p},
so the singleton condition A ≡ −1 (mod B) is the conjunction of the
prime-power conditions u_p·R_p ≡ −1 (mod p^{e_p}) with
R_p = (B/p^{e_p}) mod p^{e_p}, and A mod B is assembled from those residues
by CRT in the verification stage.

### Sweep, filters, and exact candidate verification

The sweep fixes a and appends b = a, a+1, …, 2000, updating the state above
for all 303 primes per step (this inner loop runs in a small C kernel,
prime_kernel.c, called from census2.py; the mathematics implemented is
exactly the representation above). Two sparsity facts keep the global
quantities cheap, and both are proved from the representation:

1. e_p and u_p can change only when p divides the new index n (if
   v_p(n) = 0 the new term changes S_p only by a multiple of p^{V_p},
   leaving S_p mod p^{V_p}, hence t, e_p, u_p, unchanged). So B changes
   only at sparse "delta events" (605,985 events and 632,280 individual
   prime-exponent changes across the whole census).
2. At a delta event B_new = B_old · Fn/Fd with
   Fn = ∏_{δ>0} p^δ, Fd = ∏_{δ<0} p^{−δ} (64-bit integers). Quantities
   depending multiplicatively on B are updated only there: R_f for the
   filter primes f ∈ {2, 3, 5, 7, 11} (multiplied by Fn and by the modular
   inverse of Fd mod f^{e_f}, invertible since Fd's prime factors differ
   from f; if f's own exponent changed, R_f is recomputed from the full
   exponent vector), and B modulo twelve auxiliary primes (see below).

Filters applied to every interval, both of them exact necessary
conditions, so no solution can be filtered out:

- Singleton filter: for every filter prime f ∈ {2,3,5,7,11} with e_f > 0,
  u_f·R_f ≡ −1 (mod f^{e_f}) must hold. 1,586 of 2,001,000 intervals pass.
- Pronic prefilter (for task (iii)): if B = c(c+1) then
  4B + 1 = (2c+1)^2 must be a square modulo every modulus; the sweep tests
  this modulo the twelve primes 2003, 2011, 2017, 2027, 2029, 2039, 2053,
  2063, 2069, 2081, 2083, 2087 (all > 2000, so the delta-event updates of
  B modulo them are valid, Fd being coprime to each). 2,265 intervals pass.

Every interval passing either filter (3,224 distinct candidates) is then
re-derived from scratch by a different accumulation path
(pk_interval: for the fixed interval, V_p is computed directly and S_p is
formed as the strata sum Σ_n p^{V_p−v_p(n)}·w_p(n) mod p^{V_p+1}), its B
and A mod B are assembled with Python big integers from the per-prime data
only, and the exact conditions of tasks (i) to (iii) are decided there.
Claims in this file rest on that candidate verification, and the
validation section below ties the filters to the scratch path.

### Why no L = 2 case can be missed (exhaustiveness for task (iii))

H(c,c+1) = (2c+1)/(c(c+1)) is already in lowest terms (2c+1 is coprime to
both c and c+1). Write H(a,b) = A/B in lowest terms and
g = gcd(B, c(c+1)), B = gB′, c(c+1) = gD′ with gcd(B′,D′) = 1. The sum,
written over the common denominator gB′D′, has numerator AD′ + (2c+1)B′,
which is coprime to B′ (any prime dividing B′ divides neither A nor D′) and
coprime to D′ (any prime dividing D′ divides neither 2c+1 nor B′). For the
sum to be an integer its reduced denominator must be 1, forcing
B′ = D′ = 1, i.e. B = c(c+1) exactly, and then integrality is the single
congruence A + 2c + 1 ≡ 0 (mod B). Hence c is not a search variable at
all: it is forced by B through the integer square root (c = ⌊√B⌋, check
c(c+1) = B), and c > b is checked explicitly. Enumerating all [a,b] with
b ≤ 2000 and testing these two exact conditions is therefore exhaustive
for c of any size, bounded or not.

### Validation performed before trusting the pipeline

All checks are in census2.py's self-test (outputs/selftest.json), run and
passed before the census:

- The pure-Python prime-by-prime reference (prime_ref.py, same mathematics,
  independent code) agrees with Fraction computations of H(a,b) (B and
  A mod B) on all 820 intervals with b ≤ 40. Fraction is used only here,
  as a spot check on tiny intervals, as permitted; it appears nowhere else.
- The C kernel's scratch path agrees with the pure-Python reference on all
  5,050 intervals with b ≤ 100 (every prime's (e_p, u_p)).
- Exhaustive scratch verification of all intervals with b ≤ 120 reproduces
  exactly the six singletons and no L = 2 solution, and the candidate
  pipeline restricted to b ≤ 120 returns the identical solution sets;
  every pronic-B interval at b ≤ 120 (138 of them) is inside the QR
  candidate set, as the necessity argument requires.
- The incremental sweep state (e_p, u_p for all p, R_f for the five filter
  primes, and B modulo all twelve QR primes) agrees with the scratch
  factorisation on 306 sampled intervals up to b = 2000, including
  (1, 2000) and (1999, 2000).

## Task (i): singleton census, b ≤ 1600

Exactly six solutions (a, b, m), with m = B forced in each case:

| a | b | H(a,b) | m = B | disjoint (B > b) |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | no |
| 1 | 2 | 3/2 | 2 | no |
| 2 | 2 | 1/2 | 2 | no |
| 1 | 3 | 11/6 | 6 | yes |
| 2 | 3 | 5/6 | 6 | yes |
| 3 | 6 | 19/20 | 20 | yes |

AGREEMENT with Zeraoulia's published expectation: exact. The same six, no
others, and (for (1,1), the B = 1 edge case, the condition A ≡ −1 (mod B)
is the vacuous congruence mod 1 and m = 1).

## Task (ii): singletons to b ≤ 2000 and disjoint classification

Extending the census from 1600 to 2000 (the additional a-ranges up to
a = 2000, all b ≤ 2000) produces no new singleton solutions: the complete
list for b ≤ 2000 is the same six as above. Classifying by B > b, the
disjoint solutions are exactly (1,3,6), (2,3,6), (3,6,20); each of the
other three has B = b (m = b = 2 for (1,2,2) and (2,2,2), and the
degenerate (1,1,1) with B = b = 1), so none of them is disjoint.

AGREEMENT with Nayak's Proposition 16.1 expectation for the singleton
branch: exact. The only disjoint singleton solutions with b ≤ 2000 are
(1,3,6), (2,3,6), (3,6,20).

## Task (iii): L = 2 disjoint branch, b ≤ 2000, c unbounded

No solutions. By the reduction proved above, a solution would need an
interval [a,b], b ≤ 2000, whose reduced denominator B is pronic,
B = c(c+1) with c > b, and with A + 2c + 1 ≡ 0 (mod B). Among all
2,001,000 intervals, exactly four satisfy the denominator condition with
c > b, and all four fail the congruence (A is the reduced numerator;
note A < B in each case, so A mod B = A):

| a | b | B | c | A | (A + 2c + 1) mod B |
|---|---|---|---|---|---|
| 4 | 7 | 420 | 20 | 319 | 360 |
| 5 | 7 | 210 | 14 | 107 | 136 |
| 9 | 12 | 1980 | 44 | 763 | 852 |
| 154 | 156 | 1,861,860 | 1364 | 36,037 | 38,766 |

AGREEMENT with the published expectation (no L = 2 disjoint solutions for
b ≤ 2000): exact.

## Runtime and checkpointing

Machine: this VM, 2 cores. Kernel build (gcc -O3) plus self-tests:
7.4 s of self-test time. The full census run (sweep over all chunks plus
exact verification of all 3,224 candidates) took 9.4 s of wall time on
the original run, 9.18 s summed per-chunk compute (outputs/solutions.json,
field compute_seconds_from_chunks). Sweep totals:
2,001,000 intervals examined, 605,985 delta events, 1,586 singleton filter
passes, 2,265 pronic prefilter passes.

Checkpointing: the sweep is split into 20 chunks by a-value
(a = 1–100, 101–200, …, 1901–2000). Each chunk's candidate lists and stats
are written to outputs/chunk_aXXXX_YYYY_n2000.json before the next chunk
starts, each chunk's candidate verification to
outputs/verify_aXXXX_YYYY_n2000.json, and outputs/progress.json is updated
after every chunk (intervals so far, elapsed time). Re-running census2.py
resumes from existing chunk and verification files; --force recomputes.

## Anomalies and notes

- The four denominator near-misses in task (iii) are the only intervals
  with B = c(c+1) and c > b; the closest arithmetic structure to a
  solution in the whole range is (154, 156), where the congruence fails
  by the residue 38,766 out of B = 1,861,860. None of the four is close
  to satisfying the congruence in any obvious sense; all residues are
  far from 0 relative to B.
- Pronic denominators are otherwise common but structurally barred from
  task (iii): 2,053 of the candidate intervals have B exactly pronic.
  Of these, 1,999 are the two-term intervals [n, n+1] themselves, whose
  denominator is n(n+1) with c = n < b by construction; 44 are the
  one-term intervals [n, n] with n itself pronic (n = c(c+1), c ≤ 44);
  the remaining handful have c ≤ b as well, except the four near-misses
  above, which are the only ones with c > b.
- No numerical anomalies, no filter overflows (overflow flag 0 in every
  chunk), and no interval had to be dropped or approximated: every
  decision in the pipeline is exact integer or modular arithmetic.

## Files

- census2.py: driver, self-tests, checkpointed sweep and verification.
- prime_kernel.c: the prime-by-prime kernel (incremental sweep state,
  scratch per-interval prime data, filter and QR-prefilter maintenance);
  compiled to prime_kernel.so by census2.py on first run.
- prime_ref.py: pure-Python prime-by-prime reference and CRT assembly,
  plus the tiny-interval Fraction spot-check helper used only in
  self-tests.
- outputs/solutions.json: machine-readable final results (solution lists,
  candidate totals, sweep statistics, near-miss records).
- outputs/selftest.json: machine-readable validation record.
- outputs/chunk_*.json, outputs/verify_*.json, outputs/progress.json:
  checkpoint files as described above.
