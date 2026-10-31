# Cluster E, Prover 2: structural smoothness route

Cycle 1, Erdős Problem #288, singleton case. Route mandated:
structural constraints on a $b$-smooth integer in the forced CRT
class (valuations at good and bad primes, divisibility by
$L(a,b)=\mathrm{lcm}(a,\dots,b)$, and $m=B(a,b)$ exactly), in the
regimes (i) fixed length $R=b-a+1$, $a\to\infty$, and (ii) $a>b/2$.

## Verdict summary (exact quantifiers in the body)

1. **The mandated route fails, in both regimes at once, and the
   failure is a disproof, not a gap.** The exclusion hypothesis
   (H-sieve) of Theorem 13R in TARGET.md is **false for every
   $B_0$**: there are infinitely many intervals, all of length
   $R=2$ and all with $a>b/2$, with $P_1(a,b)$ nonempty, at which
   $m=B(a,b)$ itself is $b$-smooth, satisfies $B\le L(a,b)$ (with
   equality), satisfies $v_p(B)=1$ at every good prime and
   $v_p(B)=0$ at every bad prime (there are no bad primes at these
   intervals), and lies in the forced class $r(a,b)\bmod Q(a,b)$,
   yet the interval is not a solution (Theorem F, §1). The same
   family refutes the single-candidate weakening recorded in
   TARGET.md Remark 2. No argument using only the listed
   structural properties of a class member can exclude these
   intervals, because $B$ is a member satisfying all of them.
2. **Regime (i) is nevertheless CLOSED (finiteness), by size, not
   by the class.** For every fixed $R\ge 2$, any solution of
   length $R$ has $a\le 2R$ (Theorem I, §2); for $R=1$ the only
   solutions are $a=1,2$. The proof uses Lemma 1 ($m=B$) and the
   size of the numerator $A+1$ against $B$. It owes nothing to the
   sieve: at $R=2$ the class condition holds infinitely often
   (§1) while the size condition $A+1\ge B$ fails for all $a>2$.
3. **Regime (ii) is nevertheless CLOSED (complete
   classification), by size plus the prime 2.** The solutions
   with $a>b/2$ are exactly $(a,b,m)=(1,1,1)$, $(2,2,2)$,
   $(2,3,6)$ (Theorem II, §3). For $b\ge 32$ the proof splits at
   $a=2R$: above it, the size argument of §2; below it (the window
   $b/2<a\le (2b+2)/3$), a unique-maximum 2-adic valuation argument
   forces $2^{t-1}\mid B$, $2^t\le b<2^{t+1}$, while an integral
   bound gives $H(a,b)\le 319/420+1/a$, and the two bounds make
   $H+1/B<1$, contradicting integrality. The prime that does the
   work in the hard window is $2$, which the odd-prime sieve
   discards by design.
4. **Where the 83 small failures live, and what kills them.**
   Recomputed independently (Part 1 of prover2_checks.py): of the
   80 non-solution in-class intervals with $b\le 300$, 74 have
   $R=2$, and 78 lie in regime (ii) (the family of §1 lies in the
   intersection of the two regimes, which is why the failure
   hits both). All 83 satisfy every structural condition of the
   mandate (0 failures). For each of the 80 non-solutions, the
   condition $A\equiv-1\pmod B$ fails at some prime power
   $p^e\Vert B$, and such a witness prime $p$ is **never** a good
   or bad sieve prime (proved in §1.4, not just observed): it is
   always $p=2$ or an odd prime with $p^2\le b$, the two classes
   of primes the sieve does not see. Computationally, the least
   witness is $p=2$ in 37 cases and an odd $p$ with $p^2\le b$ in
   43 cases.

## 0. Black boxes used

From AUDIT-B.md, by name only: **Lemma 1** (a solution forces
$m=B(a,b)$, hence integrality is $(A+1)/B\in\mathbb Z$ with
$H(a,b)=A/B$ in lowest terms); **Lemma 2** (the dichotomy at odd
$p$ with $p^2>b$: good primes force $v_p(m)=1$ and
$m\equiv -p\,(T_p\bmod p)^{-1}\pmod{p^2}$; bad primes force
$v_p(m)=0$), including its certified $p$-local form (AUDIT-B §1,
Lemma 2 item (ii): $H(a,b)+1/(pt)$ is $p$-integral iff
$t\equiv-(T_p\bmod p)^{-1}\pmod p$); the **CRT reduction** (a
solution's $m$ lies in the class $r(a,b)\bmod Q(a,b)$, divides
$L(a,b)$, is $b$-smooth); and the **certified census** (all
solutions with $b\le 300$ are exactly $(1,1,1)$, $(1,2,2)$,
$(2,2,2)$, $(1,3,6)$, $(2,3,6)$, $(3,6,20)$). Everything else is
proved here. Notation is TARGET.md's.

One preliminary observation, used repeatedly: a prime power
witness. Since $A\equiv-1\pmod B$ holds iff it holds modulo
$p^e$ for every $p^e\Vert B$ (CRT over the prime powers in $B$),
a non-solution in-class interval must fail at at least one prime
power in $B$.

## 1. The class route fails: an exact characterization at $R=2$ and an infinite family

### 1.1 Lemma (the $R=2$ characterization)

Let $a\ge1$, $b=a+1$. Then $H(a,b)=(2a+1)/(a(a+1))$ in lowest
terms, so $B=a(a+1)$ and $L(a,b)=a(a+1)=B$. Moreover
$P_1(a,b)\ne\emptyset$ and $B$ lies in the forced class if and
only if both of the following hold:

- ($\alpha$) no prime divisor $p$ of $a$ satisfies $p^2>a+1$;
- ($\beta$) some prime divisor $p$ of $a+1$ satisfies $p^2>a+1$.

*Proof.* $\gcd(2a+1,a)=\gcd(1,a)=1$ and
$\gcd(2a+1,a+1)=\gcd(-1,a+1)=1$, so the fraction is reduced and
$B=a(a+1)$; consecutive integers are coprime, so
$L=a(a+1)=B$.

Let $p$ be an odd prime with $p^2>b$ and $k(p)\ge1$. A multiple
of $p$ in $\{a,a+1\}$ is an endpoint, so $p\mid a$ or $p\mid a+1$
(not both). Conversely, if $p$ divides an endpoint and $p^2>b$,
then $k(p)=1$: two distinct multiples of $p$ differ by at least
$p\ge3$, more than the diameter $1$. With $k(p)=1$,
$T_p=1/u\ne0$ in $\mathbf F_p$, where the endpoint is $pu$; so
every such $p$ is **good**, and there are **no bad primes at any
$R=2$ interval**. Hence
$P_1=\{p\text{ odd}: p\mid a(a+1),\ p^2>a+1\}$, and for
$p\in P_1$ the endpoint $pu$ satisfies $u<p$ (since $pu\le b<p^2$)
and $v_p$ of that endpoint is $1$ (since $p^2>b\ge$ endpoint).
The forced residue at $p$ (Lemma 2) is $-pu\bmod p^2$, because
$T_p^{-1}\equiv u\pmod p$.

Case $p\mid a+1$: $B-(-pu)=apu+pu=pu(a+1)$, and $p\mid a+1$
gives $p^2\mid pu(a+1)$. So the congruence at $p$ **always
holds**.

Case $p\mid a$: write $a=pu$. Then $B-(-pu)=pu(a+1)+pu=pu(a+2)$,
and $p^2\mid pu(a+2)$ iff $p\mid a+2$ (as $p\nmid u$). With
$p\mid a$ this forces $p\mid2$, contradicting $p$ odd. So the
congruence at $p$ **always fails**.

Therefore $B$ satisfies all the class congruences iff no good
prime divides $a$, and $P_1\ne\emptyset$ iff some good prime
divides $a$ or $a+1$. Combining gives ($\alpha$) and ($\beta$).
∎

(Verified computationally for all $a\le3000$, Part 2 of
prover2_checks.py: 0 mismatches.)

Note what ($\alpha$) says: every odd prime factor of $a$ is at
most $\sqrt{a+1}$, i.e. it is invisible to the sieve (either
$p=2$ or $p^2\le b$). Squares $a=n^2$ satisfy ($\alpha$)
automatically, since $p\mid n^2$ gives $p\le n$.

### 1.2 Lemma (infinitely many primes $\equiv1\pmod4$)

*Proof.* Suppose $p_1,\dots,p_k$ were all of them (possibly
$k=0$). Let $N=(2p_1\cdots p_k)^2+1$ (with the empty product
equal to $1$, giving $N=5$). $N>1$ is odd; let $q$ be any prime
divisor of $N$. Then $q\nmid 2p_1\cdots p_k$ (else $q\mid1$), and
$x=2p_1\cdots p_k$ satisfies $x^2\equiv-1\pmod q$. Since $q$ is
odd, $-1\ne1\pmod q$, so $x$ has exact order $4$ in
$\mathbf F_q^{\*}$, hence $4\mid q-1$, i.e. $q\equiv1\pmod4$.
But $q$ is none of the $p_i$ (it divides none of them, and if
$q=p_i$ then $p_i\mid N$ and $p_i\mid x$ give $p_i\mid1$), a
contradiction. ∎

### 1.3 Lemma ($\sqrt{-1}$ modulo $P\equiv1\pmod4$)

For prime $P\equiv1\pmod4$, $f=((P-1)/2)!$ satisfies
$f^2\equiv-1\pmod P$.

*Proof.* Wilson: $(P-1)!\equiv-1\pmod P$. Splitting the product
at $(P-1)/2$ and substituting $j\mapsto P-j$ in the upper half
gives $(P-1)!\equiv f\cdot(-1)^{(P-1)/2}f$. For $P=4k+1$,
$(P-1)/2=2k$ is even, so $(P-1)!\equiv f^2$, hence
$f^2\equiv-1$. ∎

### 1.4 Theorem F (the exclusion fails infinitely often, in both regimes)

For each prime $P\equiv1\pmod4$ let $n_P\in[1,(P-1)/2]$ be the
least positive residue of $((P-1)/2)!$ or its negative modulo
$P$, so $n_P^2\equiv-1\pmod P$ by Lemma 1.3, and let
$I_P=(a,b)=(n_P^2,\ n_P^2+1)$. Then:

(a) $P_1(a,b)\ne\emptyset$ (it contains $P$) and $B(a,b)$ lies
in the forced class $r(a,b)\bmod Q(a,b)$;
(b) $B$ is $b$-smooth, $B=L(a,b)$ (so $B\le L(a,b)$),
$v_p(B)=1$ at every good prime, and there are no bad primes;
(c) $I_P$ is not a solution;
(d) the intervals $I_P$ are infinitely many distinct intervals;
each has $R=2$ (regime (i)) and $a>b/2$ (regime (ii), since
$2n_P^2>n_P^2+1$ for $n_P\ge2$).

Consequently (H-sieve) in TARGET.md is false for every $B_0$,
and so is its single-candidate weakening $B(a,b)\ne r(a,b)
\pmod{Q(a,b)}$ (TARGET.md Remark 2): both fail at $I_P$ for all
large $P$.

*Proof.* $n_P\ge2$ for $P>5$ (as $n_P=1$ would give $P\mid2$),
and $n_P=2$ for $P=5$, giving $(4,5)$, which is in the computed
list of §1.5. Apply Lemma 1.1 with $a=n_P^2$. Condition
($\alpha$): a prime divisor $p$ of $a$ divides $n_P$, so
$p\le n_P$ and $p^2\le n_P^2=a<a+1$. Condition ($\beta$):
$P\mid n_P^2+1=a+1$ and $P\ge2n_P+1$ (since
$n_P\le(P-1)/2$), so $P^2>n_P^2+1=a+1$. Hence by Lemma 1.1,
$P_1\ne\emptyset$ and $B$ lies in the class, proving (a). In
fact $P_1=\{P\}$ exactly: a good prime divides $a$ or $a+1$
(Lemma 1.1); it does not divide $a$ (such a prime is $\le n_P$,
with square $\le a<b$); and writing $a+1=Pc$, the cofactor
satisfies $c=(n_P^2+1)/P\le(n_P^2+1)/(2n_P+1)<n_P$, so every
prime divisor of $a+1$ other than $P$ is $<n_P$ and has square
$<b$, hence is not good. For (b): $B=a(a+1)=L$ by
Lemma 1.1, so $B$ is $b$-smooth and $B\le L$; at a good prime
$p$, $p$ divides exactly one endpoint, to the first power
($p^2>b$), and does not divide the other, so $v_p(B)=1$; there
are no bad primes by Lemma 1.1. For (c): a solution would need,
by Lemma 1, $(A+1)/B\in\mathbb Z$; here $A=2a+1$, so
$(A+1)/B=(2a+2)/(a(a+1))=2/a$, which is not an integer for
$a=n_P^2\ge4$. For (d): if the set $\{I_P\}$ were finite, the
set of integers $\{a+1:I_P=(a,b)\}$ would be finite, with
finitely many prime divisors; but $P\mid a_P+1$ for every $P$ in
the infinite set of Lemma 1.2, so $P$ would range over a finite
set, a contradiction. ∎

*Remark (where the failure is located).* For any in-class
non-solution interval, the failing prime power in $B$ lies
outside the sieve. Indeed, at a good prime $p$, AUDIT-B's
certified $p$-local form of Lemma 2 says $H+1/B$ is $p$-integral
iff $B\bmod p^2$ equals the forced residue; and
$H+1/B=(A+1)/B$ is $p$-integral iff $A\equiv-1\pmod p$ (since
$v_p(B)=1$ by Lemma 2). So $B$ in the class gives
$A\equiv-1\pmod{p^{v_p(B)}}$ at **every good prime**: the full
prime-power condition in $B$ at $p$. At a bad prime,
$v_p(B)=0$, so there is no prime power in $B$ to fail. Hence
every witness prime power $p^e\Vert B$ with
$A\not\equiv-1\pmod{p^e}$ has $p=2$ or $p^2\le b$. For the
family $I_P$ this is visible directly: $(A+1)/B=2/a$ fails
exactly at the prime powers dividing $a=n_P^2$, all of whose
primes satisfy $p^2\le a<b$.

### 1.5 Computational map of the 83 (own code)

prover2_checks.py Part 1 recomputes the in-class set for
$b\le300$ independently (full multiples sieve, exact fractions)
and recovers exactly the verifier's 83 (3 solutions, 80
non-solutions). Findings:

- $R$ distribution of the 80 non-solutions: $R=2$: 74; $R=3$: 3;
  $R=4$: 1; $R=5$: 1; $R=6$: 1.
- Regime (ii): 78 of the 80 non-solutions have $a>b/2$ (79 of
  all 83). The exceptions are $(1,6)$ and $(2,6)$.
- Structural conditions on all 83: $v_p(B)=1$ at all good $p$,
  $v_p(B)=0$ at all bad $p$, $B\mid L(a,b)$: 0 failures. The
  extra structure in the mandate kills **none** of the 83.
- Least witness prime for $A\not\equiv-1\pmod{p^e}$ among the
  80: $p=2$ in 37 cases, odd $p$ with $p^2\le b$ in 43 cases,
  a sieve prime in 0 cases (the last is the theorem of §1.4's
  remark; the split is computed).
- The family of Theorem F, checked directly for all 147 primes
  $P\equiv1\pmod4$ with $P\le2000$ (Part 3): $P\in P_1$,
  $B$ in class, non-solution, all 147 intervals distinct; the
  divisor method used there is cross-checked against the full
  multiples sieve for $P\le200$.
- The failure is not an $R=2$ accident computationally: for
  fixed $R=3$ (resp. $4$, $5$) and $R^2\le a\le5000$, the number
  of in-class non-solutions is 37 (resp. 21, 1), with no
  solutions among them (Part 5). Infinitude is proved here only
  for $R=2$; for $R\ge3$ these counts are evidence, not a claim.
- A related vacuity in regime (i): if $R$ is fixed and
  $b>(R-1)^2$, there are **no bad primes at all** in the sieve
  range, since a bad prime needs $k(p)\ge2$ ($k(p)=1$ gives
  $T_p=1/u\ne0$), and $k(p)\ge2$ forces
  $p\le b-a=R-1<\sqrt b<p$, a contradiction. So in regime (i)
  the bad-prime condition, and the finite-bad-prime content of
  Corollary 6 for fixed patterns, is eventually empty: there is
  nothing there to exploit. The good-prime conditions are then
  the whole sieve, and §1.1 shows at $R=2$ they are automatic on
  one side (primes dividing $a+1$) and fatal on the other
  (primes dividing $a$); the intervals that survive are exactly
  those whose $a$-side primes are all sieve-invisible.

## 2. Regime (i): CLOSED for finiteness, by a size lemma

**Lemma S (size).** Let $R=b-a+1\ge2$ and suppose $(a,b,m)$ is
a solution. Then $(A+1)/B<2R/a$; in particular $a\le 2R$.

*Proof.* By Lemma 1, $m=B$ and $(A+1)/B=H(a,b)+1/B$ is a
positive integer, hence $\ge1$. Now
$H(a,b)=\sum_{i=0}^{R-1}1/(a+i)<R/a$ (the first term equals
$1/a$, the other $R-1\ge1$ terms are strictly smaller). Also
$A\ge1$ (a positive sum has positive numerator), so
$B=A/H\ge1/H>a/R$, giving $1/B<R/a$. Adding,
$(A+1)/B<R/a+R/a=2R/a$. Since $(A+1)/B\ge1$, $2R/a>1$. ∎

**Theorem I (regime (i) closed, finiteness).** Fix $R\ge1$.
The singleton equation has only finitely many solutions with
$b-a+1=R$; precisely: for $R=1$ the solutions are exactly
$(1,1,1)$ and $(2,2,2)$; for $R\ge2$ every solution satisfies
$a\le2R$, hence $b\le3R-1$, and the remaining possibilities are
the explicit finite check over $1\le a\le2R$.

*Proof.* $R=1$: $H=1/a$, $A=1$, $B=a$, and by Lemma 1 a
solution needs $2/a=(A+1)/B\in\mathbb Z$, i.e. $a\mid2$.
$R\ge2$: Lemma S. ∎

(Part 6 of prover2_checks.py sanity-checks the equivalent form
$A+1<B$ for $2\le R\le8$, $2R<a\le400$: 0 failures. This is a
sanity check only; the proof is complete without it.)

*Classification addendum.* Combined with the certified census
($b\le300$), Theorem I gives the complete list for every fixed
$R\le100$ (there $b\le3R-1\le299$): the only solutions of fixed
length are $(1,1,1)$, $(2,2,2)$ ($R=1$); $(1,2,2)$, $(2,3,6)$
($R=2$); $(1,3,6)$ ($R=3$); $(3,6,20)$ ($R=4$); and none for
$5\le R\le100$. For $R>100$, Theorem I still proves finiteness;
the classification is reduced to the finite check $a\le2R$,
which has not been run for such $R$ and is not claimed.

Note the division of labour: at $R=2$ the class condition of
§1 holds for infinitely many $a$, while Lemma S's condition
$A+1\ge B$ already fails for every $a>4$. What excludes large
$a$ in regime (i) is the numerator's size, a property of
$m=B$ **exactly**, invisible to any statement about class
membership of a smooth number.

## 3. Regime (ii): CLOSED, complete classification

**Theorem II (regime (ii) closed).** The solutions of the
singleton equation with $a>b/2$ are exactly
$(a,b,m)=(1,1,1)$, $(2,2,2)$, $(2,3,6)$.

*Proof.* For $b<32$ this is exact enumeration: Part 4 of
prover2_checks.py computes $H(a,b)$ exactly for all
$a\le b<32$ and finds the six solutions
$(1,1,1)$, $(1,2,2)$, $(2,2,2)$, $(1,3,6)$, $(2,3,6)$,
$(3,6,20)$, of which exactly the three claimed have $a>b/2$;
this agrees with the certified census for $b\le300$ in
AUDIT-B.md. Assume now $b\ge32$ and $a>b/2$; write
$R=b-a+1$.

If $R=1$ then $a=b\ge32$ and Lemma 1 gives $(A+1)/B=2/a\notin
\mathbb Z$. Suppose $R\ge2$.

*Case 1: $a>2R$.* Lemma S gives $(A+1)/B<2R/a<1$, but a
solution makes $(A+1)/B$ a positive integer (Lemma 1),
contradiction.

*Case 2: $a\le2R$ (the window $b/2<a\le(2b+2)/3$).* Two bounds
collide.

(2-adic bound) Let $2^t\le b<2^{t+1}$; since $b\ge32$, $t\ge5$.
Claim: $\max_{n\in[a,b]}v_2(n)$ is attained at exactly one
integer $n_0$, and its value $s$ satisfies $s\ge t-1$.
If $a\le2^t$, take $n_0=2^t\in[a,b]$, $s=t$: any other
$n\in[a,b]\subseteq[1,2^{t+1})$ with $v_2(n)\ge t$ would be a
multiple of $2^t$ in $[1,2^{t+1})$ other than $2^t$, and there
is none. If $a>2^t$, no $n\in[a,b]$ has $v_2(n)\ge t$ (a
multiple of $2^t$ in the open interval $(2^t,2^{t+1})$ does
not exist), and the integers there with $v_2=t-1$ form the
single value $3\cdot2^{t-1}$ (an odd multiple of $2^{t-1}$ in
$(2^t,2^{t+1})$ has odd part in $(2,4)$, hence $3$). It remains
to see $3\cdot2^{t-1}\in[a,b]$: from $a\le2R$ we get
$R\ge a/2>2^{t-1}$, so $R\ge2^{t-1}+1$; any $2^{t-1}+1$
consecutive integers cover all residues mod $2^{t-1}$, so
$[a,b]$ contains a multiple of $2^{t-1}$, which lies in
$(2^t,2^{t+1})$ and therefore equals $3\cdot2^{t-1}$. So
$s=t-1$ and the maximum is unique. (Mechanism verified for all
751,899 dangerous-window intervals with $32\le b\le3000$,
Part 4: case 1 count 635,421, case 2 count 116,478, 0 failures.)

With the maximum unique, $v_2(H(a,b))=-s$: let $o_n$ be the
odd part of $n$ and $O=\mathrm{lcm}\{o_n\}$ (odd). Every term
of $2^sOH(a,b)=\sum_n 2^{s-v_2(n)}(O/o_n)$ is an integer; the
$n_0$ term is $O/o_{n_0}$, a quotient of odd integers, hence
odd; every other term has $s-v_2(n)\ge1$, hence is even. The
sum is odd, so $v_2(2^sOH)=0$ and $v_2(H)=-s$. Writing
$H=A/B$ in lowest terms, $v_2(A)-v_2(B)=-s$; since
$s\ge t-1\ge4\ge1$, $v_2(B)\ge1$ forces $v_2(A)=0$
($\gcd(A,B)=1$), so $v_2(B)=s$ and
$B\ge2^s\ge2^{t-1}\ge16$.

(Analytic bound) $H(a,b)\le319/420+1/a$. Indeed, for
$n\ge a+1$, $1/n\le\int_{n-1}^{n}dx/x$ (the integrand is
$\ge1/n$ on $[n-1,n]$), so
$H(a,b)\le1/a+\int_a^b dx/x=1/a+\int_1^{b/a}du/u$ (substituting
$x=au$). Here $1<b/a<2$ (as $R\ge2$ and $a>b/2$), and the
integrand is positive, so the integral is at most
$\int_1^2du/u$, which by the upper Riemann sum on four equal
subintervals (integrand decreasing, left endpoints) is at most
$\tfrac14\bigl(1+\tfrac45+\tfrac23+\tfrac47\bigr)
=\tfrac14\cdot\tfrac{319}{105}=\tfrac{319}{420}$.

(Combination) Since $b\ge32$ and $a>b/2$, $a\ge17$. A solution
would give, by Lemma 1, the positive integer
$(A+1)/B=H(a,b)+1/B\le319/420+1/17+1/16=25157/28560<0.881<1$,
a contradiction. This exhausts $b\ge32$. ∎

*Remark.* Case 2 is exactly where regime (ii) could have been
hard for the sieve: the interval is long ($R\ge a/2$), $H$ is
bounded away from $0$, and the odd-prime class condition is
satisfied infinitely often inside this window (Theorem F's
family has $R=2$, so it sits in Case 1's range for large $a$;
the window $a\le2R$ is disjoint from it). What closes Case 2
is the 2-adic valuation of the **exact** denominator, a prime
the sieve never looks at, together with $H$ being bounded away
from $1$ (its limit range is $\log(b/a)\in[\log(3/2),\log2)$).
Bad primes play no role in either case of the proof.

## 4. Bottom line per regime

- **Regime (i), fixed $R$, $a\to\infty$.** Class/smoothness
  route: **fails**; (H-sieve) is false for every $B_0$ already
  at $R=2$ (Theorem F), the bad-prime condition is vacuous for
  $b>(R-1)^2$ (§1.5), and the surviving good-prime conditions
  are automatic exactly at the intervals where $a$'s prime
  factors are all sieve-invisible (Lemma 1.1). Singleton case
  in the regime: **CLOSED** for finiteness for every fixed $R$
  (Theorem I: $R=1$ exactly; $R\ge2$ forces $a\le2R$), with
  complete classification for $R\le100$ via the certified
  census, and an explicit finite check ($1\le a\le2R$) as the
  residual for $R>100$.
- **Regime (ii), $a>b/2$.** Class/smoothness route: **fails**;
  the same infinite family lies in this regime, and 78 of the
  80 small non-solution failures are here. Singleton case in
  the regime: **CLOSED** with the exact solution list
  $(1,1,1)$, $(2,2,2)$, $(2,3,6)$ (Theorem II), the hard window
  $b/2<a\le(2b+2)/3$, $b\ge32$, being closed by the prime 2
  (unique-maximum $v_2$, forcing $2^{t-1}\mid B$) against the
  bound $H\le319/420+1/a$.
- **General consequence for the campaign.** Theorem 13R's
  hypothesis (H-sieve) is not an open asymptotic statement that
  small cases merely fail to support; it is refuted, with the
  refuting family inside both restricted regimes. Any future
  route to finiteness in general must use input the class does
  not contain: numerator size, the prime 2, or primes with
  $p^2\le b$. The witness analysis of §1.4 says this is not an
  artefact of the family: at every in-class non-solution, the
  obstruction to $A\equiv-1\pmod B$ provably sits at such a
  prime.

## 5. Computation (exact arithmetic only)

Code: `prover2_checks.py` in this directory (names start with
`prover2`); raw output: `prover2_output.txt`. Parts: (1)
independent recompute of the 83 in-class intervals, $b\le300$,
with regime classification, structural checks (0 failures), and
least-witness classification (37 at $p=2$, 43 at odd
$p^2\le b$); (2) $R=2$ characterization, $a\le3000$,
0 mismatches; (3) Theorem F family, all 147 primes
$P\equiv1\pmod4$, $P\le2000$, 0 failures, 147 distinct
intervals, cross-checked against the full sieve for $P\le200$;
(4) regime (ii) mechanics: $H<1$ for $a>b/2$, $a>1$, $b\le300$
(22,649 intervals, 0 failures); 2-adic unique maximum in the
dangerous window, $32\le b\le3000$ (751,899 intervals,
0 failures); exact solutions for $b<32$; (5) fixed
$R=3,4,5$ in-class counts for $R^2\le a\le5000$ (37, 21, 1
non-solutions, 0 solutions); (6) size-lemma sanity,
$A+1<B$ for $2\le R\le8$, $2R<a\le400$, 0 failures. No web
posting, emailing, or submitting was done.
