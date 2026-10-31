# Cluster E, Red Team, Cycle 1: Erdős #288, singleton case

Mandate: break the closure claims of Cluster E Prover 1 and
Prover 2, or say exactly that they survived. All computations are
my own code in this directory (`redteam_*.py`, outputs
`redteam_*_output.txt`), exact arithmetic throughout. No
counterexample was found anywhere; no reported counterexample
needed the double-verification protocol.

Setting: $H(a,b)=\sum_{n=a}^{b}1/n=A/B$ in lowest terms; a
solution is $H(a,b)+1/m\in\mathbb Z$ for a positive integer $m$.
Lemma 1 (AUDIT-B, certified): a solution forces $m=B$ and
$B\mid A+1$; since $\gcd(B,kB-A)=\gcd(A,B)=1$, integrality is
equivalent to $kB-A=1$ for the relevant integer $k$.

---

# Part I: Prover 1

## Preliminary finding (documentation, not mathematics)

`prover1.md` **as filed on disk is truncated**: it ends
mid-sentence at line 226 ("Filtering by the strict ineq"), inside
the $b\le33$ part of Theorem II. The entire $b\ge34$ proof (the
$H<3/4$ bound, the Bertrand prime step, the split at $3a=2b+2$)
is **absent from the file**. I attacked the claims via the proof
sketch supplied by the coordinator. The mathematics survives
(see below), but as a filed proof, Claim 1 is incomplete: the
load-bearing argument is not in the document.

## Claim 1 (regime ii): SURVIVED

Claim: for $a>b/2$ the only solutions are
$(1,1,1)$, $(2,2,2)$, $(2,3,6)$.

### (a) Computational refutation attempt: none found

Exhaustive exact search, own method (per $b$: $D=\mathrm{lcm}$
over the window, descending numerator, screen $D-N\mid N$,
survivors gcd-checked and Fraction-verified):

- $b=34$ to $5000$: **6,252,211 intervals** with $a>b/2$,
  **zero** solutions (`redteam_search.py`).
- $b\le33$ by a separate general Fraction test: exactly
  $(1,1,1)$, $(2,2,2)$, $(2,3,6)$.
- Independent cross-check by a third code path
  (`redteam_bounds.py` (f)): full census $b\le300$ reproduces
  exactly the six AUDIT-B solutions, three in this regime.

**b reached: 5000.**

### (b) The Bertrand step in the strip: sound, stronger than stated

The worry was that a Bertrand prime $\ell\in(b/4,b/2)$ might
divide no term of $[a,b]$ ($k(\ell)=0$). In fact **every** prime
in $(b/4,b/2)$ is valid in **every** strip interval: cofactors
can only be $2,3$ (since $4\ell>b$); $T_\ell\in\{1/2,1/3,5/6\}$
is nonzero mod $\ell$ for $\ell\ge11$ (and $b\ge34$ forces
$\ell>b/4\ge8.5$); $\ell^2>b$ since $\ell>b/4>\sqrt b$ for
$b>16$. An invalid $\ell$ would need $2\ell<a$ and $3\ell>b$;
but $2\ell<a$ gives $3a\ge6\ell+3$, and the strip's
$3a\le2b+1$ then gives $3\ell\le b-1$, contradicting $3\ell>b$.
So the interval $(b/3,a/2)$ that an invalid prime would have to
occupy contains no integer at all in the strip. The choice of
$\ell$ is therefore irrelevant; Bertrand (existence of one
prime in $(b/4,b/2)$) suffices. Note: this gap argument is the
justification the sketch omits; it is fillable in three lines
and is not a break.

Computational confirmation:

- Literal definition (multiples, cofactors, $T_\ell\bmod\ell$
  per prime per interval), exhaustive $34\le b\le200$: 3,298
  strip intervals, 0 with no valid prime, 0 with even one
  invalid prime. Two independent implementations agree.
- Reduced form (invalid iff $b/3<\ell<a/2$, proved equivalent
  above), exhaustive $34\le b\le20000$: **33,339,898 strip
  intervals**, 0 with no valid prime, 0 with any invalid prime.
- Literal large-$b$ sample: $b\in\{10007,10^5,999983,10^6,
  1234567,10^7\}$, 300 strip intervals each (1,800 total):
  0 failures, 0 invalid (prime, interval) pairs.

### (c) The bounds: verified, one phrasing defect (harmless in range)

- $\ln2<111/160$: verified self-containedly by exact rational
  series bound: $2\sum_{k\le5}\frac1{(2k+1)3^{2k+1}}$ plus a
  geometric tail bound ($<9/8$ of the first omitted term) gives
  $\ln2<2458234657/3546482940=0.69314718\ldots<111/160=0.69375$.
- Strip $H<3/4$: worst case $b\le2a-1$ and $a\ge18$ give
  $H\le 1/a+\ln(2-1/a)<1/18+111/160=1079/1440=0.749306<3/4$
  (margin $1/1440$). Exact Fraction check of **all** strip
  intervals $b\le300$: 0 violations; maximum $H=0.707229$ at
  $(a,b)=(18,35)$.
- Boundary ownership is exact: $3a=2b+1$ belongs to the strip,
  $3a=2b+2$ to subregime A; no gap, no overlap. The boundary
  family $3a=2b+2$ ($b\equiv2\pmod3$) was additionally checked
  directly: $H<1/2$ on all 989 such intervals with $b<3000$.
- Subregime A ($3a\ge2b+2$): $R=b-a+1\le a/2$ verified on the
  full grid $b<5000$ (0 violations of $2R\le a$). **Defect in
  the sketch's phrasing:** the bare inequality "$H<R/a$" is
  false for $R=1$ (equality: $H=1/a$). In range this is
  harmless ($R=1$, $b\ge34$ gives $H=1/a\le1/34<1/2$), but
  stated without the $R=1$ caveat it would also "exclude"
  $(2,2,2)$, where $H=1/2$ exactly and a solution exists. The
  claim only needs $b\ge34$, so this does not break it; the
  proof text should carry the caveat.

### (d) $m\in\{2,3\}$ forcing: verified, and $H>1/2$ is not needed

From $0<H<3/4$ alone: $m=1$ gives $H+1\in(1,7/4)$, no integer;
$m\ge2$ forces the sum to be $1$, so $1/m=1-H\in(1/4,1)$ and
$m\in\{2,3\}$. The feared branch "$H\le1/4$ with $m=1$" is
already excluded by the $m=1$ case. Verified on a rational
grid ($H=k/1000<3/4$, $m<50$: no integral sum with
$m\notin\{2,3\}$). Lemma 2 (certified) at the good prime
$\ell\ge11$ forces $\ell\mid m$, contradicting $m\in\{2,3\}$.

Short intervals: lengths $1,2,3$ **never occur in the strip**
for $b\ge34$ (length $L$ in the strip needs $b\le3L-2$; strip
length is $\ge(b+2)/3\ge12$, minimum observed 12 for
$34\le b\le2000$). Length 1 ($a=b$) lies in subregime A and is
covered by its $H<1/2$ argument; lengths $\le3$ with $b<34$
are in the census. No gap.

### (e,f) Base case and quantifiers: verified

My independent census $b\le300$ (Fractions) gives exactly
$(1,1,1),(1,2,2),(2,2,2),(1,3,6),(2,3,6),(3,6,20)$, matching
AUDIT-B/CENSUS0. Filtering by strict $a>b/2$ gives exactly the
claimed three. The boundary is handled correctly: $(1,2,2)$
and $(3,6,20)$ both have $2a=b$ and are correctly **excluded**
by the strict inequality.

## Claim 2 (regime i): SURVIVED

Claim: for fixed $R=b-a+1$ and $a>2R$, no solutions.

The proof is correct: for $R\ge2$,
$H\le\frac1a+\frac{R-1}{a+1}<\frac Ra<\frac12$, and $R=1$ is
separate ($a>2$ gives $H=1/a<1/2$); then $H+1/m$ lies in
$(1,3/2)$ ($m=1$) or $(0,1)$ ($m\ge2$), never an integer.

Boundary $a=2R$, probed exactly: the same chain gives
$H<1/2$ at $a=2R$ for every $R\ge2$ (verified $R\in
\{2,3,4,5,10,50,100\}$, e.g. $R=100$: $H=0.406300<1/2$), so
the claim as stated is true but **not sharp** for $R\ge2$. At
$R=1$, $a=2R=2$: $H=1/2$ exactly and $(2,2,2)$ is a solution,
so the strict $a>2R$ is sharp exactly where it must be. No
break.

---

# Part II: Prover 2

## P2-Claim 1 (regime ii closed, 2-adic mechanism): SURVIVED

- **2-adic unique maximum reproduced independently** on **all**
  window intervals ($b/2<a$, $3a\le2b+2$, $R\ge2$,
  $32\le b\le3000$): **751,899 intervals**, case split
  $a\le2^t$: **635,421**, $a>2^t$: **116,478** — both counts
  match P2 exactly — with **0** failures: the maximum of
  $v_2$ on $[a,b]$ is always attained exactly once and is
  $\ge t-1$. No tie for maximal $v_2$ exists in the window;
  no interval has $v_2(B)<t-1$.
- The derived identity $v_2(B)=s$ was spot-verified with exact
  Fractions on 15,699 window intervals (all $b\le300$ plus a
  seeded sample to 3000): 0 mismatches, $B\ge16$ throughout.
  Both cases of P2's existence argument check out line by
  line, including the substitute $3\cdot2^{t-1}$ when $a>2^t$
  (the residue-covering step uses $R\ge2^{t-1}+1$, which
  follows from $a\le2R$ and $a>2^t$; the multiple of $2^{t-1}$
  so found is forced to be $3\cdot2^{t-1}$).
- **Integral bound verified rigorously.** The Riemann upper
  sum is exact: $\frac14(1+\frac45+\frac23+\frac47)
  =\frac{319}{420}$, and it bounds $\int_1^2du/u$ since the
  integrand decreases; the window has $1<b/a<2$, so
  $H\le319/420+1/a$. Exact Fraction check on all window
  intervals $b\le400$: 0 violations (max $H=0.708069$).
- **Combination arithmetic exact:**
  $319/420+1/17+1/16=25157/28560=0.8808\ldots<1$. The inputs
  are tight and correct: $b\ge32$ gives $t\ge5$, hence
  $B\ge2^{t-1}\ge16$, and $a>b/2$ gives $a\ge17$. With Lemma 1,
  a solution needs $H+1/B=(A+1)/B\ge1$: contradiction stands.
- Split and thresholds: Case 1/Case 2 split at $a=2R$ is exact
  and complementary ($3a\le2b+2$ is the window side; P1's
  strip boundary $3a\le2b+1$ differs by the single family
  $3a=2b+2$, which P2 assigns to the window at $a=2R$ and P1
  to subregime A; each proof covers it, cf. Part I(c)).
  $R=1$ is handled separately ($2/a\notin\mathbb Z$ for
  $a\ge32$). $b<32$ enumeration matches the certified census
  (my recompute, Part I(f)); the $a=b/2$ boundary for even $b$
  is strict and correct ($(3,6,20)$ excluded).

## P2-Claim 2 (regime i finiteness via Lemma S): SURVIVED

Each inequality in the chain attacked separately:

- $H(a,b)<R/a$ for $R\ge2$: true (first term $=1/a$, the rest
  strictly smaller); $R=1$ is handled separately and exactly
  (solutions iff $a\mid2$, i.e. $a\in\{1,2\}$; verified to
  $a<1000$).
- $B>a/R$: **no counterexample exists**; the proof is sound
  and elementary: $B=A/H\ge1/H$ since $A\ge1$, and
  $1/H>a/R$. Verified computationally as part of the chain.
- $(A+1)/B=H+1/B$ exactly, hence $<2R/a$: verified with the
  whole chain on **117,000 intervals** ($2\le R\le40$,
  $a\le3000$), exact Fractions, 0 failures, including
  $A+1<B$ whenever $a>2R$.
- Boundary $a=2R$: strictness survives — at $a=2R$ the chain
  still gives $(A+1)/B<1$ strictly, so in fact $a<2R$; P2's
  stated $a\le2R$ is weaker than what its proof gives, and is
  true. No break.

## P2-Claim 3 (Theorem F: the class route is refuted): SURVIVED

The refutation is correct; (H-sieve) is indeed false for
every $B_0$. Verified exactly for **all 147 primes**
$P\equiv1\pmod4$ with $P\le2000$ (count matches P2), with
$n_P$ from $((P-1)/2)!\bmod P$:

- $P_1=\{P\}$ **exactly**, by two independent computations:
  factor-based sieve data for all 147, and a brute-force scan
  of every odd prime $p\le b$ with $p^2>b$ for $P\le200$
  (0 mismatches). The feared extra good prime does not occur:
  analytically, primes dividing $a=n_P^2$ are $\le n_P$ with
  square $\le a<b$; primes dividing $a+1$ other than $P$
  divide the cofactor $c=(n_P^2+1)/P<n_P<P$ (so $P\nmid c$,
  $v_P(a+1)=1$, and every other prime divisor is $<n_P$,
  hence not good).
- $B=a(a+1)=L$ exactly: $\gcd(2a+1,a)=\gcd(2a+1,a+1)=1$
  verified in code through the reduced fraction; $B$ is in
  the forced class (single congruence mod $P^2$ checked
  directly), $v_P(B)=1$, no bad primes, $B$ $b$-smooth.
- $(A+1)/B=2/a$ exactly, not an integer for $a=n_P^2\ge4$:
  so $B$ satisfies every structural condition of the class
  while the interval is not a solution. The 147 intervals are
  distinct. The conclusion — no argument using only class
  membership, smoothness, $B\le L$, and the good/bad valuation
  profile can exclude these intervals — stands.

## P2's map of the 83: SURVIVED (spot-reproduction became full reproduction)

Independent recompute of all in-class intervals with $b\le300$
(own sieve/CRT code): total **83**, in-class solutions exactly
$(1,3),(2,3),(3,6)$; non-solution $R$ distribution
$74/3/1/1/1$ for $R=2/3/4/5/6$; **78 of 80** non-solutions in
regime (ii); structural conditions ($v_p(B)=1$ at good $p$,
$v_p(B)=0$ at bad $p$) with **0 failures**; least witness
prime for $A\not\equiv-1\pmod{p^e}$: $p=2$ in **37** cases,
odd $p$ with $p^2\le b$ in **43**, a sieve prime in **0**.
Every number matches P2 exactly. (P2's §1.5 vacuity remark
also checks out analytically: a bad prime needs $k(p)\ge2$,
forcing $p\le R-1<\sqrt b$ when $b>(R-1)^2$, outside the sieve
scope.)

---

# Summary of verdicts

| Claim | Verdict |
|---|---|
| P1 Claim 1 (regime ii, Bertrand strip) | **SURVIVED** |
| P1 Claim 2 (regime i, $a>2R$) | **SURVIVED** |
| P2 Claim 1 (regime ii, 2-adic window) | **SURVIVED** |
| P2 Claim 2 (regime i, Lemma S) | **SURVIVED** |
| P2 Claim 3 (Theorem F refutation of (H-sieve)) | **SURVIVED** |
| P2 map of the 83 | **SURVIVED** |

Non-breaking defects recorded: (1) `prover1.md` as filed is
truncated and does not contain the $b\ge34$ proof it asserts —
the claim survives on the coordinator-supplied sketch plus the
justification supplied in Part I(b), but the document itself
is incomplete; (2) the sketch's bare inequality $H<R/a$ fails
at $R=1$ (equality), harmless for $b\ge34$ but false as stated
without the caveat; (3) P1 Claim 2 and P2 Claim 2 are both
non-sharp at the boundary $a=2R$ for $R\ge2$ (the proofs give
$a<2R$); sharpness holds at $R=1$ via $(2,2,2)$.

Coverage: solution search exhaustive to $b=5000$
(6,252,211 regime-(ii) intervals); strip argument exhaustive
to $b=200$ literally (two implementations), to $b=20000$ in
proved-equivalent reduced form (33,339,898 intervals), and
sampled literally to $b=10^7$; P2 window mechanism exhaustive
$32\le b\le3000$ (751,899 intervals, counts matching P2 to the
unit); Lemma S chain on 117,000 intervals; Theorem F family
for all 147 primes $P\equiv1\pmod4$, $P\le2000$; census and
83-map fully recomputed at $b\le300$.

Code and outputs: `redteam_search.py`, `redteam_strip.py`,
`redteam_strip_fast.py`, `redteam_strip_bisect.py`,
`redteam_strip_large.py`, `redteam_bounds.py`,
`redteam_p2.py`, `redteam_p2b.py` in this directory, with
`*_output.txt` beside them. No web posting, emailing, or
submitting was done.
