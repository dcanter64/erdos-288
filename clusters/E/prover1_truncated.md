# Cluster E, Prover 1 (least-residue route): Erdős #288, singleton case, Cycle 1

Prover 1, mandated route: least-residue lower bounds.
Regimes assigned: (i) fixed interval length $R=b-a+1$, $a\to\infty$;
(ii) intervals with $a>b/2$.
Code (exact arithmetic only): `prover1_checks.py`, output
`prover1_output.txt`; supplementary code `prover1_extra.py`, output
`prover1_extra_output.txt`, in this directory.
Black boxes used, by name from AUDIT-B.md / TARGET.md only: Lemma 1
(a solution forces $m=B(a,b):=\mathrm{den}\,H(a,b)$ and
$B\mid A+1$), Lemma 2 (the sieve dichotomy for odd primes $p$ with
$p^2>b$), the CRT reduction, and Remark 14 ($Q>L$ alone does not
suffice). Bertrand's postulate is used in the same way TARGET.md
itself uses it in the proof of Theorem 13R. Everything else is
proved here.

## Verdict (read this first; quantifiers are exact)

1. **Pure least-residue exclusion is FALSE in both regimes, for
   arbitrarily large $b$, with $P_1$ nonempty.** Explicit infinite
   family (Section 1): for every prime $p$, the singleton interval
   $(a,b)=(p(p-1),\,p(p-1))$ has $P_1=\{p\}$, $Q=p^2$, and least
   residue $r_0=p$, which satisfies $r_0\le L(a,b)$ and is
   $b$-smooth. So the class $r(a,b)\bmod Q(a,b)$ does contain a
   $b$-smooth integer $\le L$, namely $r_0$ itself. This family
   lies in regime (i) with $R=1$ and in regime (ii) (there
   $a=b$). It refutes the (H-sieve) exclusion, for these regimes,
   as a statement about the class. It does **not** refute
   Theorem 13R's conditional implication; it shows its hypothesis
   cannot be proved, in these regimes, by least-residue size or
   smoothness alone. Note the witness is $r_0$, not $B$: in this
   family $B$ is not in the forced class (computed, Section 5).

2. **Regime (i) is nevertheless CLOSED, for every fixed $R$, by
   the size of $H$ alone (no sieve).** Theorem I (Section 2):
   for every fixed $R\ge1$ and every $a>2R$, the interval
   $[a,a+R-1]$ admits no solution. The remaining initial segment
   is the explicit finite check $1\le a\le 2R$ (so $b\le 3R-1$)
   for that $R$.

3. **Regime (ii) is CLOSED completely (all $b$), by a split
   argument.** Theorem II (Section 3): if $a>b/2$, the only
   solutions are $(a,b,m)=(1,1,1),(2,2,2),(2,3,6)$. For $b\ge34$
   this is a proof given in full below: the subregime
   $3a\ge 2b+2$ falls to the same $H<1/2$ size argument as
   regime (i); the remaining strip $b/2<a$, $3a\le 2b+1$ falls to
   the size bound $H<3/4$ (which forces $m\in\{2,3\}$) combined
   with one specific good prime $\ell\in(b/4,b/2)$, supplied by
   Bertrand, whose Lemma 2 valuation forces $\ell\mid m$, a
   contradiction. For $b\le33$ the statement is the finite part
   of AUDIT-B's certified enumeration (all intervals with
   $b\le300$; solution set exactly the six known intervals),
   filtered by $a>b/2$, and is independently reproduced by
   `prover1_extra.py`.

4. **What is NOT claimed.** The (H-sieve) hypothesis of
   Theorem 13R is not proved for any regime in this file; by
   item 1 it is false pointwise for arbitrarily large $b$ in
   regimes (i) $R=1$ and (ii) (though only the single candidate
   $m=B(a,b)$ matters for solutions, cf. TARGET.md Remark 2,
   and in the item-1 family $B$ is not in the class). No closure
   of (H-blind) is claimed. In the regime (ii) strip, the
   asymptotic behaviour of the full least residue $r_0$ is not
   determined here; the strip proof uses one good prime and a
   bound on $m$, not $r_0$.

## 1. The least-residue approach fails: explicit families

### Family F1 (nondegenerate, $P_1$ nonempty, both regimes)

Let $p$ be any prime and $(a,b)=(p(p-1),p(p-1))$, so $R=1$,
$H=1/a$, $B=L=a$.

*Claim.* $P_1(a,b)=\{p\}$, $Q=p^2$, $r_0=p$.

*Proof.* A prime can have a multiple in the singleton $\{a\}$
only if it divides $a=p(p-1)$. The odd prime divisors of $a$
are $p$ and the prime divisors $q$ of $p-1$. For $q\mid p-1$,
$q\le p-1$, so $q^2\le(p-1)^2=p^2-2p+1<p^2-p=a=b$; hence $q$ is
outside the sieve's scope $q^2>b$. For $p$ itself,
$p^2>p(p-1)=b$, the unique multiple is $a=p\cdot u$ with
$u=p-1<p$, $k(p)=1$, and
$T_p\equiv u^{-1}\equiv(-1)^{-1}\equiv-1\pmod p$, nonzero, so
$p$ is good and it is the only good prime. The forced residue
is $-p\,(T_p\bmod p)^{-1}\bmod p^2$. Since $T_p\equiv-1$,
also $(T_p)^{-1}\equiv-1\pmod p$; taking the representative
$p-1$ of $-1$, the residue is
$-p(p-1)\equiv p\pmod{p^2}$, because $-p(p-1)=-p^2+p$.
As $0<p<p^2$, the least positive residue is $r_0=p$. $\square$

$r_0=p\le L=p(p-1)$ for $p\ge2$, and $r_0$ is $b$-smooth (its
only prime factor is $p\le b$). There are infinitely many
primes, so this failure occurs for arbitrarily large $b$, in
regime (i) at $R=1$, and in regime (ii) since $a=b>b/2$.
Computed instances (`prover1_output.txt`, Section 1):
$p=3,5,7,11,13,101,1009,10007$ give
$(a,b)=(6,6),(20,20),(42,42),(110,110),(156,156),(10100,10100),
(1017072,1017072),(100130042,100130042)$, each with
$Q=p^2$, $r_0=p$, $r_0\le L$, $r_0$ $b$-smooth, and
$B$ **not** in the forced class, exactly as the theory says:
these are not solutions (for $p>2$), and the exclusion fails
not at the true denominator but at the smaller smooth
representative $r_0$ of the same class. Moral, matching
TARGET.md's Remark 14 point in a second form: even $r_0\le L$
with $r_0$ smooth does not require $Q\le L$ (here
$Q=p^2>p(p-1)=L$, yet $r_0=p$). Any least-residue proof must
therefore use more than the data $(Q,L,r_0)$: it must use that
a solution needs $m=B$ exactly. Both closures below do exactly
that (a bound on the *value* $H$, hence on the candidate $m$
via $H+1/m\in\mathbb Z$, plus, in the strip, a valuation of
that specific $m$).

### Family F2 (degenerate, $P_1$ empty, $R=2$; does not touch 13R)

Solutions $(t,s)$ of the Pell equation $t^2-2s^2=-1$ are
infinite: $(1,1)$ is one, and
$(t,s)\mapsto(3t+4s,\,2t+3s)$ preserves the equation, since
$(3t+4s)^2-2(2t+3s)^2=t^2-2s^2$, and strictly increases $t$.
For the interval $(a,b)=(t^2,t^2+1)$ ($R=2$), every prime with
a multiple in $[a,b]$ divides $t^2$ or $t^2+1=2s^2$, hence is
$2$, a divisor of $t$, or a divisor of $s$; all odd such primes
$p$ satisfy $p\le\max(t,s)=t$, so $p^2\le t^2<b$ and $p$ is
outside the sieve's scope. Thus $P_1$ is empty, $Q=1$,
$r_0=1\le L$, $1$ vacuously $b$-smooth. Computed
(`prover1_output.txt`, Section 2): $t=7,41,239,1393$ give
$(49,50),(1681,1682),(57121,57122),(1940449,1940450)$, all
with $Q=1$. This is the $R=2$ analogue of AUDIT-B's
$(q^2,q^2)$ family: it kills the *unrepaired* Theorem 13 style
exclusion and the naive least-residue test in regime (i) at
$R=2$, but, exactly as there, it says nothing about 13R,
whose hypothesis is restricted to $P_1$ nonempty. It is
recorded so the failure map is complete, not as evidence
against the repaired target.

### The $R=2$ characterisation (explains the 83 failures of TARGET.md Remark 4)

For an interval $(a,a+1)$, $a\ge2$: $H=(2a+1)/(a(a+1))$ with
$\gcd(2a+1,a)=\gcd(2a+1,a+1)=1$, so $B=a(a+1)=L$. Every sieve
prime $p$ (odd, $p^2>a+1$) has $k(p)=1$ (consecutive integers
are coprime, and the next multiple is $p>1$ away). If $p\mid a$,
$a=pu$, then $B/p\equiv u\pmod p$, whereas the forced class
requires $B/p\equiv-(T_p^{-1})\equiv-u\pmod p$; since
$1\le u<p$, $u\not\equiv-u\pmod p$, so $B$ is **not** in the
class. If $p\mid a+1$, $a+1=pu$, then
$B/p\equiv u(pu-1)\equiv-u\pmod p$, which **is** the forced
residue. Hence, exactly:
$$B\in\text{forced class}\iff\text{no good prime divides }a,$$
and in that case $B$ itself is a $b$-smooth member of the class
with $B=L\le L$, a pointwise (H-sieve) failure whenever
$P_1$ is nonempty. This accounts for the shape of the verifier's
list in TARGET.md Remark 4 (dominated by $(a,a+1)$ intervals).
Exact scan using this characterisation (`prover1_output.txt`,
Section 3): there are **41,349** values $a\le200{,}000$ for which
$B$ lies in the forced class and $P_1$ is nonempty; the first
twelve were re-verified by direct exact CRT computation (e.g.
$(9,10)$: $Q=25$, $r_0=15$; $(25,26)$: $Q=169$, $r_0=143$;
in these cases even $r_0$ is $\le L$ and $b$-smooth). I did not
find an elementary parametric infinite subfamily with $P_1$
nonempty for $R=2$ (see Dead ends), and none is claimed; the
infinite nondegenerate failure is F1. For the closure of
regime (i) this does not matter, by Theorem I.

### Computed least-residue behaviour, fixed $R$ (finite range)

Exact scan, $R\in\{1,\dots,6\}$, $2\le a$, $b=a+R-1\le300$,
intervals with $Q>1$ (`prover1_output.txt`, Section 4):

| $R$ | $Q>1$ intervals | $r_0>L$ | $r_0\le L$, nonsmooth | $r_0\le L$, $b$-smooth (least-residue fails) |
|---|---|---|---|---|
| 1 | 209 | 176 | 0 | 33 |
| 2 | 284 | 131 | 0 | 153 |
| 3 | 296 | 179 | 25 | 92 |
| 4 | 296 | 200 | 42 | 54 |
| 5 | 295 | 218 | 47 | 30 |
| 6 | 294 | 245 | 37 | 12 |

So in the computed range the pure least-residue test fails on a
substantial fraction of intervals at every $R\le6$, and its
success rate grows with $R$ (consistent with $Q$ growing), but
F1 shows the failure persists to arbitrarily large $b$ at
$R=1$ regardless. This is the exact point where the mandated
route, used alone, stops: it cannot close regime (i) even
though regime (i) is closed, by Theorem I.

## 2. Regime (i): fixed $R$, CLOSED for $a>2R$

**Theorem I.** Fix $R\ge1$. For every $a>2R$, the singleton
equation $H(a,a+R-1)+1/m\in\mathbb Z$ ($m$ a positive integer)
has no solution.

*Proof.* Write $b=a+R-1$, so $H(a,b)$ is a sum of $R$ terms,
each $\le1/a$. If $R=1$, $H=1/a<1/2$ since $a>2$. If $R\ge2$,
$$H(a,b)=\frac1a+\sum_{n=a+1}^{b}\frac1n
\le\frac1a+\frac{R-1}{a+1}<\frac1a+\frac{R-1}{a}=\frac{R}{a}<\frac12,$$
using $a>2R$ in the last step. So in all cases $0<H(a,b)<1/2$.
Now suppose $H+1/m$ is an integer. If $m=1$, then
$H+1\in(1,3/2)$, which contains no integer. If $m\ge2$, then
$0<H+1/m<1/2+1/2=1$, and a number in $(0,1)$ is not an integer.
Both cases are impossible. $\square$

*Quantifiers and the finite remainder.* The statement is: for
each fixed $R$, all $a>2R$ are excluded. What remains, for that
$R$, is the explicit finite check $1\le a\le 2R$ (equivalently
$b\le3R-1$), performed by exact rational arithmetic testing
Lemma 1's candidate, $(A+1)\bmod B=0$. For $R\le100$ this check
is already contained in AUDIT-B's certified $b\le300$
enumeration (there $b\le3R-1\le299$), whose solution list,
split by length, is $R=1$: $(1,1),(2,2)$; $R=2$: $(1,2),(2,3)$;
$R=3$: $(1,3)$; $R=4$: $(3,6)$; no solutions of any other length
with $b\le300$. For $R>100$ the finite check is finite for each
given $R$ but is not precomputed here; no claim about it is
made beyond its finiteness and its exact form above. Note
Theorem I subsumes F1's intervals for $p>2$: there $R=1$ and
$a=p(p-1)>2$. The least-residue data and the truth diverge
exactly because $r_0=p$ is a smooth class member that is not
the denominator candidate; Theorem I never looks at the class.

## 3. Regime (ii): $a>b/2$, CLOSED completely

**Theorem II.** If $a>b/2$, the singleton equation has exactly
the solutions $(a,b,m)=(1,1,1)$, $(2,2,2)$, $(2,3,6)$.

*Proof for $b\le33$.* AUDIT-B's certified Lemma 1 enumeration
over all intervals with $b\le300$ found the solution set to be
exactly $(1,1,1),(1,2,2),(2,2,2),(1,3,6),(2,3,6),(3,6,20)$.
Filtering by the strict ineq
...[truncated 6161 chars]