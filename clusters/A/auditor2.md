# Erdős #288 — Cluster A, Auditor 2 — Independent audit of Nayak Theorem 3.2

Task: independently re-derive Theorem 3.2 of Ritvik Nayak's note (May 2026)
from its statement, by my own route, and only afterwards compare with the
note. My independent draft was written to
`auditor2_draft_proof.md` in this directory *before* I opened Section 3 of
`~/workspace/math-hunt/erdos-288/sources/Nayak-2026.txt`. The proof below is
that draft, polished only in wording. The comparison in Part 2 was written
after reading Sections 2 and 3 of the note.

**Theorem 3.2.** If intervals $I,J$ of positive integers intersect and
$H(I)+H(J)\in\mathbb Z$, then up to swapping the pair is one of
$([1,1],[1,1])$, $([1,2],[1,2])$, $([1,2],[2,2])$, $([2,2],[2,2])$;
all four pairs do have integer sum.

---

## Part 1 — My complete independent proof

### Setup and the valuation principle

Write $S=H(I)+H(J)$. Since $I\cap J\neq\varnothing$, the union $I\cup J$ is
an interval $[r,s]$. For $n\in[r,s]$ let
$c_n=\mathbf 1_{n\in I}+\mathbf 1_{n\in J}\in\{1,2\}$; $c_n=2$ exactly on
the (nonempty) intersection $I\cap J$. Then

$$S=\sum_{n=r}^{s}\frac{c_n}{n}.$$

**Unique-minimum principle.** If for some prime $p$ exactly one term of a
sum of rationals attains the minimal $p$-adic valuation $m$, then
$v_p$ of the sum equals $m$ (the remaining terms have valuation $>m$,
hence their sum has valuation $>m$ by the ultrametric inequality, and a
sum of two rationals of *different* valuations has the smaller valuation).
In particular, if $m<0$ the sum is not an integer.

So it suffices, in each case with $s\ge 3$, to produce an **odd** prime $p$
and a term $n_0$ such that $v_p(c_{n_0}/n_0)<0$ while $v_p(c_n/n)=0$ for
all $n\neq n_0$. Oddness is essential and is the whole point of the
coefficient bookkeeping: for odd $p$, $c_n\in\{1,2\}$ is a $p$-adic unit
($v_p(c_n)=0$), so a coefficient $2$ can neither create nor destroy the
unique minimum, whether or not $n_0$ lies in the overlap $I\cap J$. For
$p=2$ this fails ($v_2(2)=1$ can cancel a factor of $2$ in a denominator
lying in the overlap), which is why this proof never uses a $2$-adic
maximal-power argument.

### Case 1: $s\le 2$

The only intervals with endpoints in $\{1,2\}$ are $[1,1],[2,2],[1,2]$.
The intersecting unordered pairs and their sums are:

| pair | sum |
|---|---|
| $([1,1],[1,1])$ | $2$ ✓ |
| $([1,1],[1,2])$ | $5/2$ ✗ |
| $([1,2],[1,2])$ | $3$ ✓ |
| $([1,2],[2,2])$ | $2$ ✓ |
| $([2,2],[2,2])$ | $1$ ✓ |

($([1,1],[2,2])$ is disjoint and excluded.) This gives exactly the four
listed pairs, and confirms all four work.

### Case 2: $s\ge 3$ and $s=r$ (singleton union)

Then $I=J=[r,r]$ and $S=2/r$ with $r=s\ge 3$, so $0<S<1$: not an integer.

### Case 3: $s\ge 3$ and $s>r$

Put $k=s-r+1\ge 2$ (the number of integers in $[r,s]$). Exactly one of
$2r\le s+1$, $2r>s+1$ holds.

**Subcase A: $2r\le s+1$ (Bertrand).**
*Claim:* there is a prime $p$ with $s/2<p\le s$. Indeed, if $s$ is prime
take $p=s$; otherwise $s\ge 4$ is composite, $t=\lfloor s/2\rfloor\ge 2$,
and Bertrand's postulate in the form "for $t>1$ some prime lies strictly
between $t$ and $2t$" gives $t<p<2t\le s$, with $p>s/2$ in both parities
($p>t=s/2$ if $s$ even; $p>(s-1)/2$, hence $p\ge(s+1)/2>s/2$, if $s$ odd).

This $p$ lies in $[r,s]$: if $s$ is even, $2r\le s+1$ forces $r\le s/2<p$;
if $s$ is odd, $r\le(s+1)/2\le p$ since $p>s/2$ and $p$ is an integer.
Also $p$ is odd: in the composite branch $p>t\ge 2$; in the prime branch
$p=s\ge 3$.

The only multiple of $p$ in $[r,s]$ is $p$ itself, since $2p>s$. Hence
$v_p(c_p/p)=-1$ (as $p$ is odd, $v_p(c_p)=0$), while for $n\neq p$,
$p\nmid n$ gives $v_p(c_n/n)=0$. Unique minimum $-1<0$; $S\notin\mathbb Z$.

**Subcase B: $2r>s+1$ (Sylvester).**
Now $r-k=2r-s-1\ge 1$, i.e. $r>k$: the $k$ consecutive integers
$r,r+1,\dots,s$ are **all greater than $k$**. The existence theorem needed
here, in exactly the form needed, is:

> **Sylvester's theorem (1892).** The product of $k$ consecutive positive
> integers, each greater than $k$, is divisible by a prime $p>k$.

(Bertrand alone does *not* suffice in this subcase: $[r,s]$ may contain
no prime at all, e.g. $[114,126]$; what saves the argument is a large
prime *factor* of a composite term, e.g. $61\mid 122$. I verified the
statement above, with hypothesis "first term $>k$" and no exceptional
cases, against the standard literature — Sylvester's original paper and
the Shorey–Tijdeman survey "Prime factors of arithmetic progressions and
binomial coefficients", both of which state it in this product form.
This is the Sylvester–Schur circle; the equivalent binomial-coefficient
form is the version usually quoted.)

Such a $p$ divides some term $n_0\in[r,s]$ (it divides the product), and
it divides **exactly one** term: two distinct terms divisible by $p$
would differ by a nonzero multiple of $p$, but their difference is at
most $s-r=k-1<p$. Also $p>k\ge 2$, so $p$ is odd. Therefore
$v_p(c_{n_0}/n_0)=-v_p(n_0)\le-1$, while for $n\neq n_0$, $p\nmid n$
gives $v_p(c_n/n)=0$. Unique minimum $<0$; $S\notin\mathbb Z$.
(Note this works for any exponent: if $p^e\| n_0$ with $e\ge 2$, e.g.
$25$ in $[24,26]$, the valuation is $-e$, still the unique minimum.)

Subcases A and B exhaust Case 3. This completes the proof: no pair with
$s\ge 3$ works, Case 2 gives nothing, and Case 1 gives exactly the four
listed pairs. $\square$

*Remark on the boundary.* The split at $2r=s+1$ is chosen so that
Subcase B is *exactly* Sylvester's hypothesis $r>k$. The borderline
$2r=s+1$ (e.g. $[5,9]$, $[8,15]$) belongs to Subcase A, where the
integrality of $p$ and $r$ squeezes the Bertrand prime into $[r,s]$.

---

## Part 2 — Comparison with Nayak's note (Sections 2 and 3)

### Agreements (the note's architecture is the same, and sound)

1. **Same overall route.** §2 Lemma 2.1 is exactly my unique-minimum
   principle, stated for weighted sums $\sum \mu_i/n_i$; its proof
   (multiply by $p^e$, the minimal term becomes a unit, the rest become
   divisible by $p$) is correct. Theorem 3.2 writes the sum with
   $\mu(n)\in\{1,2\}$ over the union $[r,s]$, exactly my $c_n$ setup.
2. **Same key lemma.** Lemma 3.1 asserts precisely what my Case 3 needs:
   for $s\ge 3$ and an interval of (at least) two integers, some **odd**
   prime divides exactly one integer in $[r,s]$. The theorem then
   correctly notes $\mu(n_0)\in\{1,2\}$ is not divisible by the odd $p$,
   writes $p^e\| n_0$, and gets the unique lowest layer of valuation
   $-e$. The coefficient-$2$ danger at $p=2$ is avoided in the note
   exactly as in my proof, by only ever using odd primes.
3. **Same small cases.** Singleton union: total $2/r$, integral only for
   $r=1,2$. Union inside $\{1,2\}$: direct check. These match my Cases
   1–2 and produce the same four pairs.
4. **Sylvester step.** The note's case $r>s/2$, $r>N$ (with $N=s-r+1$)
   applies Sylvester–Schur to get $p>N$ dividing the product, and hence
   at most one term. This is *algebraically identical* to my Subcase B:
   $r>N\iff 2r>s+1$. Its hypothesis check ($N$ consecutive integers, all
   $\ge r>N$) is exactly Sylvester's hypothesis, and the conclusion
   $p>N\ge 2$ correctly gives $p$ odd.

### Differences of route (neither is a gap)

5. **The borderline configuration.** The note splits Lemma 3.1 three
   ways: (i) $r\le s/2$ (Bertrand prime in $(s/2,s]$); (ii) $r>s/2$,
   $r>N$ (Sylvester); (iii) $r>s/2$, $r\le N$, where it correctly derives
   $s=2r-1$ and applies Bertrand again to get $r<p<2r=s+1$. My first
   draft did **not** isolate case (iii): my Subcase A uses the sharper
   threshold $2r\le s+1$, and an integrality/parity squeeze shows *any*
   prime in $(s/2,s]$ already satisfies $p\ge r$ throughout that range,
   including $s=2r-1$. So case (iii) is a case the note handles
   *explicitly* that my draft handled *implicitly*; on inspection both
   arguments are correct, and my computation (§4 below) verified
   witnesses for both splits for all $r<s\le 500$ with zero failures.
   Logged as a difference in exposition, not in coverage.
6. **Small $s$ in the Bertrand case.** For $r\le s/2$ the note treats
   $s=3,4$ separately ("the prime 3 gives the claim by direct
   inspection") before invoking Bertrand for $s\ge 5$. This is correct:
   $s=3$ forces $r=1$, $s=4$ forces $r\in\{1,2\}$, and in each interval
   $3$ divides exactly one member. My draft instead folded $s=3$ into
   the "$s$ prime" endpoint case and $s=4$ into Bertrand at $t=2$.
   Both work; the note's endpoint handling is more elementary, mine
   more uniform. No gap on either side.
7. **Bertrand endpoint $\le s$.** The note asserts a prime with
   $s/2<p\le s$ for $s\ge 5$ without deriving the inclusive right
   endpoint from the strict form $t<p<2t$. This is a standard equivalent
   form of Bertrand's postulate and is true as used, but the note does
   not show the (one-line, parity) derivation my draft supplies. Minor
   omitted justification, not an error.
8. **Slack in the uniqueness bound.** The note says "the interval has
   length $N$, such a prime can divide at most one term". The sharp
   bound is that two terms differ by at most $N-1<N<p$; the note's
   wording is loose but the conclusion holds with room to spare.

### Genuine discrepancies found in the note (logged, not silently repaired)

9. **Mis-counted final sentence of the proof of Theorem 3.2.** The note
   ends: *"If the union is contained in $\{1,2\}$ and has length 2,
   direct checking gives exactly the four listed pairs."* Taken
   literally this is **false for that subcase**: a length-2 union inside
   $\{1,2\}$ is the union $[1,2]$ itself, and up to swapping the
   intersecting pairs with that union are $([1,2],[1,2])$,
   $([1,2],[2,2])$, and $([1,1],[1,2])$, with sums $3$, $2$, $5/2$ —
   exactly **two** solution pairs, not four. The other two listed pairs
   have singleton unions and come from the *preceding* length-1 case.
   The proof as a whole still yields exactly the four pairs (the two
   cases together), so this is a local misstatement / mis-attribution in
   the final sentence, not a hole in the argument. It is the only
   inaccuracy I found anywhere in §3, and it is a plausible candidate
   for the "one minor issue" an automated check reportedly flagged on
   the forum — but the forum record does not say where that issue sits,
   so I cannot confirm they are the same.
10. **"Length" is used but never defined.** Lemma 3.1 says "length at
    least 2" and the theorem says "if the union has length 1, both
    intervals are $[r,r]$". These are consistent **only** if "length"
    means the *number of integers* in the interval ($N=s-r+1$). If
    "length" meant $s-r$, a length-1 union would have two points and
    the quoted conclusion would be false. Under the cardinality reading
    — which Lemma 3.1's own $N=s-r+1$ confirms is intended — every
    step checks out. Terminological ambiguity, not a logical gap.

### Gaps in my first draft that the note covers

None of substance. The note makes two things explicit that my draft left
compressed: the $s=2r-1$ borderline as a named configuration (item 5)
and the exact-exponent notation $p^e\|n_0$ in the theorem (my draft
argued with $-v_p(n_0)$, which covers $e\ge2$ but less crisply). My
draft, conversely, supplies the Bertrand endpoint derivation the note
omits (item 7). Every case my proof needed — singleton union, $s\le2$
enumeration, Bertrand range, Sylvester range, borderline, prime powers,
overlap coefficient $2$ — is also covered by the note, and vice versa.

---

## Part 3 — Verdict

**TRUE AND PROVABLE BY THIS ROUTE.**

Theorem 3.2 is correct, and Nayak's argument proves it: the
unique-lowest-$p$-adic-layer principle (Lemma 2.1), the odd prime
dividing exactly one denominator (Lemma 3.1, via Bertrand and
Sylvester–Schur, with the $s=2r-1$ borderline handled), the singleton
case $2/r$, and the direct check inside $\{1,2\}$ together cover every
case, with the coefficient-$2$ overlap handled correctly by using only
odd primes. The two defects I found — the mis-counted final sentence
(item 9) and the undefined "length" (item 10) — are exposition defects
in the write-up; neither removes a needed case or invalidates a step,
so they do not amount to gaps in the proof.

---

## Part 4 — Computations run and results

All checks used exact rational arithmetic (`fractions.Fraction`); final
script: `auditor2_v3_checks.py` in this directory (two earlier drafts,
`auditor2_checks.py` and `auditor2_fast_checks.py`, were abandoned as
too slow and produced no results used here). Results:

1. **Brute force, endpoints $\le 28$:** all 55,216 intersecting unordered
   interval pairs checked exactly; the *only* integer-sum solutions are
   $([1,1],[1,1])$ (sum $2$), $([1,2],[1,2])$ (sum $3$),
   $([1,2],[2,2])$ (sum $2$), $([2,2],[2,2])$ (sum $1$) — exactly the
   four listed pairs. The excluded pair $([1,1],[1,2])$ gives $5/2$,
   confirming item 9's count.
2. **Lemma 3.1 spot-verification:** for every $r<s\le 200$ with $s\ge3$,
   an odd prime dividing exactly one integer in $[r,s]$ exists —
   **0 failures**.
3. **Case-split witnesses up to $s\le 500$:** my split (Bertrand prime in
   $(s/2,s]\cap[r,s]$ when $2r\le s+1$; Sylvester prime $>k$ dividing
   exactly one term when $2r>s+1$) — **0 failures**. Nayak's three-way
   split (including the forced $s=2r-1$ in the remaining case and a
   prime in $(r,2r)$ there) — **0 failures**.
4. **Sylvester product statement:** for all $2\le k<50$ and all starts
   $k<\text{start}<200$ (terms $\le 478$ via smallest-prime-factor
   sieve), the product of $k$ consecutive integers each $>k$ has a
   prime divisor $>k$ — **0 failures**, consistent with the theorem
   having no exceptions in this form.
