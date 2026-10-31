> **Provenance (completion, Cycle 1).** The original prover
> file for this document was truncated during its original
> writing: it ended mid-sentence, at the words "Filtering by
> the strict ineq", inside the $b\le33$ part of the proof of
> Theorem II in Section 3, followed by a literal
> truncation marker, and the entire $b\ge34$ proof was
> missing from disk. The truncated original is preserved
> unchanged in this directory as `prover1_truncated.md`.
> Sections 1-2 below are the original text verbatim, as are
> the statement of Theorem II and the opening of its
> $b\le33$ proof, up to the mid-word truncation point
> "ineq". The completion of Section 3, beginning by
> completing that word and sentence and continuing with the
> full $b\ge34$ proof, was written by a completion agent
> following the original prover's argument as sketched in
> the campaign brief and as verified by the red team
> (`redteam.md`, Part I: both Prover 1 claims SURVIVED),
> including the red team's strengthened Bertrand step. The
> completion was then subject to the cluster verifier.
> A completion-agent verification note, including an
> erratum check on the intact text, appears after the proof
> at the end of this file and is not part of the original
> prover's text.

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
Filtering by the strict inequality $a>b/2$, equivalently $2a>b$, leaves exactly
$(1,1,1)$, $(2,2,2)$ and $(2,3,6)$. In detail: $(1,1,1)$ has
$2a=2>1=b$ and $(2,2,2)$ has $2a=4>2=b$ and $(2,3,6)$ has
$2a=4>3=b$, so all three are kept. The other three are not
kept: $(1,3,6)$ has $2a=2<3=b$; and the two boundary cases
have $a=b/2$ exactly, namely $(1,2,2)$ with $2a=2=b$ and
$(3,6,20)$ with $2a=6=b$, so both are excluded by the strict
inequality. Since AUDIT-B's enumeration covers all $b\le300$,
it in particular covers all $b\le33$, and the $b\le33$ part of
Theorem II is proved. $\square$ (for $b\le33$)

*Proof for $b\ge34$.* Assume $b\ge34$ and $a>b/2$. The two
subregimes
$$
3a\ge 2b+2
\qquad\text{and}\qquad
b/2<a,\ \ 3a\le 2b+1
$$
partition this range exactly: $3a$ and $2b+1$ are integers,
so every $a$ satisfies exactly one of $3a\le2b+1$ and
$3a\ge2b+2$, with no gap and no overlap. Boundary ownership
is exact: $3a=2b+1$ belongs to the second subregime (the
strip), and $3a=2b+2$ belongs to the first subregime.

### Subregime A: $3a\ge2b+2$ falls to $H<1/2$

Write $R=b-a+1$ for the interval length, so $b=a+R-1$ and
$3a\ge2b+2=2a+2R$ gives $a\ge2R$, i.e. $R\le a/2$.

Now $H(a,b)$ is a sum of $R$ terms $1/n$ with $a\le n\le b$,
each $\le1/a$, so $H(a,b)\le R/a$, with equality if and only
if $R=1$. (The bare inequality $H<R/a$ is false at $R=1$;
the $R=1$ case is handled separately here and in Theorem I.)
If $R\ge2$, every term after the first is $<1/a$, so
$H(a,b)<R/a\le1/2$. If $R=1$, then $a=b\ge34$ and
$H(a,b)=1/a\le1/34<1/2$. Hence in all cases
$0<H(a,b)<1/2$.

Suppose $H(a,b)+1/m\in\mathbb Z$ for a positive integer $m$.
If $m=1$, then $H+1/m\in(1,3/2)$, which contains no integer.
If $m\ge2$, then $0<H+1/m<1/2+1/2=1$, and a number in $(0,1)$
is not an integer. Both cases are impossible, so there is no
solution in subregime A.

### The strip: $b/2<a$ and $3a\le2b+1$

Assume now $b\ge34$, $a>b/2$ and $3a\le2b+1$. Then
$a>b/2\ge17$, so, $a$ being an integer, $a\ge18$; and
$a>b/2$ gives $b<2a$, i.e. $b\le2a-1$.

#### Step 1: $H(a,b)<3/4$

For each $n\ge a+1$ and each $x\in[n-1,n]$, $1/x\ge1/n$;
integrating over $[n-1,n]$ gives
$1/n\le\int_{n-1}^{n}dx/x$. Summing over $n=a+1,\dots,b$
(the sum is empty, and the bound trivial, if $b=a$, a case
the strip in fact excludes for $a\ge18$) gives
$$
H(a,b)\le \frac1a+\int_a^b\frac{dx}{x}
=\frac1a+\log\frac ba
\le\frac1a+\log\Bigl(2-\frac1a\Bigr),
$$
using $b\le2a-1$ in the last step. Since $b/a<2$, it is
enough to bound $\log 2$; we bound it self-containedly.

For $|x|<1$,
$\log\frac{1+x}{1-x}=2\sum_{k=0}^{\infty}\frac{x^{2k+1}}{2k+1}$
(the difference of the Taylor series of $\log(1+x)$ and
$\log(1-x)$). At $x=1/3$, $\frac{1+x}{1-x}=2$, so
$$
\log 2
=2\sum_{k=0}^{\infty}\frac{1}{(2k+1)\,3^{2k+1}}.
$$
Take the terms $k=0,\dots,5$ exactly. Each successive term
is obtained from the previous one by multiplying by
$\frac{2k+1}{2k+3}\cdot\frac19<\frac19$, so the tail from
$k=6$ on is bounded, term by term, by a geometric series
with ratio $1/9$ whose first term is the $k=6$ term
$\frac{1}{13\cdot3^{13}}=\frac1{20726199}$; hence the tail
is $<\frac98\cdot\frac1{20726199}$ (the factor
$1+\frac19+\frac1{81}+\cdots=\frac98$). Exact rational
arithmetic therefore gives
$$
\log 2
\;<\;2\Bigl(\sum_{k=0}^{5}\frac{1}{(2k+1)\,3^{2k+1}}
+\frac98\cdot\frac1{20726199}\Bigr)
=\frac{2458234657}{3546482940}
=0.69314718\ldots
<\frac{111}{160}=0.69375,
$$
the last inequality being the exact rational comparison
$\frac{111}{160}-\frac{2458234657}{3546482940}
=\frac{17103061}{28371863520}>0$.
This is exactly the bound recorded by the red team
(redteam.md, Part I(c)).

Consequently, in the whole strip,
$$
H(a,b)\;\le\;\frac1a+\log\Bigl(2-\frac1a\Bigr)
\;<\;\frac1{18}+\frac{111}{160}
=\frac{1079}{1440}
=0.749306\ldots<\frac34,
$$
where $1/a\le1/18$ uses $a\ge18$, and
$\log(2-1/a)<\log2<111/160$ uses monotonicity of $\log$.
Exact range covered: this bound uses only $a\ge18$ and
$b\le2a-1$ (with the integral comparison valid for every
$b\ge a$); both hold for every strip interval with
$b\ge34$, so the $H<3/4$ bound holds on the entire strip,
with margin $3/4-1079/1440=1/1440$. Also $H(a,b)>0$
trivially. Hence every strip interval satisfies
$0<H(a,b)<3/4$.

#### Step 2: a solution in the strip forces $m\in\{2,3\}$

Suppose $H+1/m\in\mathbb Z$ for a positive integer $m$, and
write $s=H+1/m$. Since $H>0$ and $1/m>0$, $s>0$; so the
integer $s$, if it exists, cannot be $0$ or negative, i.e.
$s\ge1$.

If $m=1$, then $s=H+1\in(1,7/4)$, since $0<H<3/4$; there is
no integer strictly between $1$ and $7/4$, so this case is
impossible.

If $m\ge2$, then $1/m\le1/2$ and
$s=H+1/m<3/4+1/2=5/4$. Combined with $s\ge1$ this forces
$s=1$: the integer $s$ cannot be $\ge2$, because $s<5/4$,
and cannot be $0$, as shown above. Hence $1/m=1-H$, and
$0<H<3/4$ gives $1/m\in(1/4,1)$. Inverting positive
quantities gives $m\in(1,4)$; with $m\ge2$ an integer,
$m\in\{2,3\}$.

So $0<H<3/4$ alone (no lower bound on $H$ beyond $H>0$ is
needed) forces: any solution in the strip has
$m\in\{2,3\}$. This is the forcing the red team verified
(redteam.md, Part I(d)). By Lemma 1 (certified, AUDIT-B.md)
a solution moreover has $m=B(a,b)=\mathrm{den}\,H(a,b)$, but
only $m\in\{2,3\}$ is needed for the contradiction in
Step 4.

#### Step 3: every prime $\ell\in(b/4,b/2)$ is good in the strip

Bertrand's postulate supplies at least one prime in
$(b/4,b/2)$: applied to the integer $n=\lfloor b/4\rfloor>1$
($b\ge34$ gives $n\ge8$), it gives a prime $\ell$ with
$n<\ell<2n$; then $\ell>b/4$ (since $\ell>n=\lfloor b/4\rfloor$,
and either $b/4$ is an integer, in which case $\ell>b/4$
directly, or $\lfloor b/4\rfloor<b/4<\lfloor b/4\rfloor+1\le\ell$)
and $\ell<2n\le b/2$. We prove the required properties for
*every* prime $\ell\in(b/4,b/2)$, so any such prime supplied
by Bertrand will do; the choice of $\ell$ is irrelevant.

Such an $\ell$ satisfies $\ell>b/4\ge34/4=8.5$; hence
$\ell\ge9$ as an integer, and, $\ell$ being prime,
$\ell\ge11$. In particular $\ell>5$ and $\ell$ is odd.
Also $\ell^2>b$: $\ell>b/4$ gives $\ell^2>b^2/16$, and
$b^2/16\ge b$ exactly when $b\ge16$; since $b\ge34>16$,
$\ell^2>b^2/16>b$. So Lemma 2's hypothesis $\ell^2>b$ holds.

The multiples of $\ell$ that could lie in $[a,b]$ are
severely restricted. The multiple $1\ell=\ell$ satisfies
$\ell<b/2<a$, so $\ell<a$ and $\ell\notin[a,b]$. Every
multiple $k\ell$ with $k\ge4$ satisfies $k\ell\ge4\ell>b$,
since $\ell>b/4$, so it is not in $[a,b]$ either. Hence the
only possible multiples of $\ell$ in $[a,b]$ are $2\ell$
and $3\ell$, and a priori $k(\ell)\in\{0,1,2\}$.

We show $k(\ell)\ge1$ in every strip interval: at least one
of $2\ell,3\ell$ always lies in $[a,b]$. Suppose not.
First, $2\ell<b$ (from $\ell<b/2$), so $2\ell\notin[a,b]$
forces $2\ell<a$, i.e. $\ell<a/2$. Second, $3\ell>3b/4$,
while the strip gives $a\le(2b+1)/3\le3b/4$ (the second
inequality is $8b+4\le9b$, i.e. $b\ge4$), so $3\ell>a$;
hence $3\ell\notin[a,b]$ forces $3\ell>b$, i.e.
$\ell>b/3$. Together,
$$
\frac b3<\ell<\frac a2\le\frac{2b+1}{6}=\frac b3+\frac16,
$$
using $3a\le2b+1$ for $a/2\le(2b+1)/6$. Multiplying by $3$,
$$
b<3\ell<b+\frac12.
$$
But $3\ell$ is an integer and $b$ is an integer, and there
is no integer strictly between $b$ and $b+1/2$: a
contradiction. Therefore $k(\ell)\ge1$ for every prime
$\ell\in(b/4,b/2)$ and every strip interval. (This is the
red team's strengthened form of the Bertrand step,
redteam.md, Part I(b): an invalid prime would have to
occupy $(b/3,a/2)$, and in the strip that interval contains
no integer at all. The red team phrases the final
contradiction equivalently as $3\ell\le b-1$ against
$3\ell>b$; the form $b<3\ell<b+1/2$ above is the same
contradiction stated with the strip bound used directly,
not a different or stronger claim.)

With $k(\ell)\ge1$, the value $T_\ell\in\mathbf F_\ell$
(TARGET.md's definition, cofactors $u,u+1,\dots$ of the
multiples of $\ell$ in $[a,b]$) is, case by case:

- exactly $2\ell\in[a,b]$: $k(\ell)=1$, cofactor $2$,
  $T_\ell=1/2$ in $\mathbf F_\ell$;
- exactly $3\ell\in[a,b]$: $k(\ell)=1$, cofactor $3$,
  $T_\ell=1/3$ in $\mathbf F_\ell$;
- both $2\ell,3\ell\in[a,b]$: $k(\ell)=2$, cofactors $2,3$,
  $T_\ell=1/2+1/3=5/6$ in $\mathbf F_\ell$.

In each case $T_\ell\ne0$ in $\mathbf F_\ell$: $1/2$ and
$1/3$ are inverses of the nonzero elements $2,3\bmod\ell$
($\ell\ge11$, so $\ell\nmid6$), and $5/6=5\cdot6^{-1}$ has
$5\not\equiv0\pmod\ell$ (as $\ell\ge11>5$) and $6$
invertible mod $\ell$. So $\ell$ is a good prime for
$[a,b]$ in TARGET.md's sense: $\ell$ odd, $\ell^2>b$,
$k(\ell)\ge1$, $T_\ell\ne0$ in $\mathbf F_\ell$; i.e.
$\ell\in P_1(a,b)$.

#### Step 4: Lemma 2 forces $\ell\mid m$, contradicting $m\in\{2,3\}$

Let $(a,b,m)$ be a solution in the strip. By Step 2,
$m\in\{2,3\}$. By Lemma 2, case (a) (certified, AUDIT-B.md,
Section 1), at the good prime $\ell$ of Step 3 a solution
forces $v_\ell(m)=1$; in particular $\ell\mid m$. But
$\ell\ge11$ (indeed $\ell\ge9$ already suffices) and
$m\in\{2,3\}$: no prime $\ge9$ divides $2$ or $3$. This is
a contradiction. Hence there is no solution in the strip.

Subregime A and the strip exhaust all $a>b/2$ with
$b\ge34$, and neither contains a solution. Combined with
the $b\le33$ case, the solutions with $a>b/2$ are exactly
$(a,b,m)=(1,1,1)$, $(2,2,2)$, $(2,3,6)$. This completes the
proof of Theorem II. $\square$

---

## Completion-agent notes (not part of the original prover's text)

### Verification of the completion's finite ingredients

The finite ingredients of the completion above were checked
with exact arithmetic by the completion agent's own code,
`prover1completion_checks.py` in this directory, with output
in `prover1completion_output.txt`:

- The $\log 2$ bound: the partial sum to $k=5$ plus the
  $9/8$ geometric tail bound gives exactly
  $2458234657/3546482940<111/160$, and
  $1/18+111/160=1079/1440<3/4$. This matches the red team's
  independently computed value in `redteam_bounds_output.txt`.
- Strip bound $H<3/4$: checked exactly (harmonic sums as
  exact fractions) on **all 333,898 strip intervals** with
  $34\le b\le2000$: 0 violations; the maximum $H$ in the
  range is $0.707229\ldots$, attained at $(a,b)=(18,35)$,
  consistent with the red team's $b\le300$ maximum at the
  same interval. The code also checked, for each of these
  intervals, the exact rational inequality
  $H(a,b)\le1/a+2458234657/3546482940$ (the proved chain's
  endpoint form): 0 violations.
- Prime step: for **all** strip intervals with
  $34\le b\le2000$ and **every** prime
  $\ell\in(b/4,b/2)$, a total of **17,276,937
  (interval, prime) pairs**: 0 pairs with $k(\ell)=0$;
  $\ell^2>b$ and $\ell\ge11$ throughout; and $T_\ell$ took
  the value $1/2$ in 11,334,720 pairs, $1/3$ in 2,964,151
  pairs, and $5/6$ in 2,978,066 pairs, nonzero in
  $\mathbf F_\ell$ in every pair.
- Subregime A: all 666,813 intervals with $34\le b\le2000$
  and $3a\ge2b+2$ satisfy $2R\le a$ and have exact
  $H(a,b)<1/2$: 0 violations.
- Boundary ownership: for all $a>b/2$ with $34\le b\le2000$
  exactly one of $3a\ge2b+2$, $3a\le2b+1$ holds (0 failures
  of the partition); the boundary family $3a=2b+1$ occurs
  656 times in the range, all in the strip, and $3a=2b+2$
  occurs 656 times, all in subregime A.
- The $b\le33$ filtering (item (6) of the code): filtering
  AUDIT-B's six certified solutions by strict $a>b/2$ keeps
  exactly $(1,1,1)$, $(2,2,2)$, $(2,3,6)$, and the two
  solutions excluded with $a=b/2$ exactly are $(1,2,2)$ and
  $(3,6,20)$, as stated in the proof.
- No truncation marker remains in this file: the bracketed
  truncation marker of the original does not occur anywhere
  in the completed `prover1.md` (checked after writing, by
  searching the file for that marker's opening bracket and
  first word). The truncated original, with the marker, is
  `prover1_truncated.md`, byte-identical to the
  `prover1.md` as originally filed (md5
  9e98b5b72d017ed6548ce62bc89cf775).

### Erratum check on the intact text (the $H<R/a$ nit)

The red team (redteam.md, Part I(c), and
`redteam_bounds_output.txt` (c3)) noted that the bare
inequality "$H<R/a$" is false at $R=1$, where equality
$H=1/a=R/a$ holds; stated without the $R=1$ caveat it would
also wrongly exclude $(2,2,2)$, where $H=1/2$ exactly.
The completion agent checked the intact original text for
this assertion. It does **not** occur there without
qualification: in the proof of Theorem I the inequality
$H(a,b)<R/a$ is asserted only inside the $R\ge2$ branch,
where it is correct (the terms after the first are
strictly smaller than $1/a$), and the $R=1$ case is
handled separately and correctly ($H=1/a<1/2$ for $a>2$).
The defect the red team flagged was in the coordinator's
proof sketch, not in the filed Sections 1-2. Accordingly
no erratum to the original text is required, and no part
of the original text has been edited. For the record: had
the bare assertion appeared, the correct statement is
$H(a,b)\le R/a$ with equality if and only if $R=1$, and
$H(a,b)<R/a$ for $R\ge2$; in the range where Theorem II
uses the bound ($b\ge34$) the $R=1$ case has
$H=1/a\le1/34<1/2$, so the nit does not affect Theorem I
as used or Theorem II. The completion's Subregime A proof
above carries this $R=1$ caveat explicitly.
