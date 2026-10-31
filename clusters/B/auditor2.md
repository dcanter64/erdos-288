# Cluster B, Auditor 2: Independent re-derivation and audit of Zeraoulia's reduction
## Erdős Problem #288, singleton case: H(a,b) + 1/m in Z

Auditor: Cluster B, Auditor 2 (independent re-derivation route).
Date: 2026-10-30. Cycle 1, Wave 0.

Method and order of work (as mandated): Part 1 below is a fully
independent derivation from the equation H(a,b) + 1/m in Z alone,
written BEFORE reading Section 6 of the dossier
(~/workspace/math-hunt/erdos-288/INFORMATION.md) and before seeing
the note. Only after Part 1 and the computational checks (Part 4)
were complete did I read dossier Section 6 and then fetch the
note's full text via the DOI link recorded there
(doi:10.13140/RG.2.2.10862.47684/1, resolved to the ResearchGate
full text of "The singleton case of Erdős Problem 288: A CRT
reduction and a smooth-number obstruction", Zeraoulia Rafik,
February 2026, revised "Path A framing"). Part 2 and Part 3
therefore compare against BOTH the dossier's account and the
note itself. YES, the note's full text was fetched and used.

Ground rules honoured: nothing posted, emailed, or submitted;
no discrepancy silently repaired; every discrepancy logged
exactly in Part 3, classified as "note is wrong",
"note is right but terse", or "my derivation is inconclusive /
scope difference".

================================================================
# PART 1: INDEPENDENT DERIVATION (from the equation alone)
================================================================

Notation: H(a,b) = sum_{n=a}^b 1/n, 1<=a<=b, m>=1 integer.
Equation: H(a,b) + 1/m in Z. Call such (a,b,m) a (singleton) solution.

## D1. m is forced (Task 1)

Write H(a,b) = A/B in lowest terms, B>0, gcd(A,B)=1 (A>0 since a>=1).
Claim: if H+1/m in Z for some m>=1, then B | A+1, m = B, and
A = -1 (mod B). In particular at most one m per (a,b), and existence
is equivalent to B | A+1.

Proof. Suppose A/B + 1/m = N in Z. Then Am + B = N B m, so
B(Nm - 1) = Am, hence B | Am. Since gcd(A,B)=1, B | m; write
m = Bs, s>=1 integer. Substituting: A/B + 1/(Bs) = N, multiply by B:
A + 1/s = NB. Hence 1/s = NB - A is an integer; s>=1 forces s=1.
Thus m=B and NB - A = 1, i.e. A = NB-1 = -1 (mod B), equivalently
B | A+1. Conversely if B|A+1 then H + 1/B = (A+1)/B in Z. QED.
No error in the claim. Note the proof uses only gcd(A,B)=1 and
positivity; no size hypothesis.

Corollary (valuations). For any prime p, with e=v_p(B)>=0:
v_p(H) = -e if e>=1 (since then p does not divide A), and
v_p(H) >= 0 if e=0. So v_p(H)<0 iff p|B, and then v_p(H)=-v_p(B)
and v_p(m)=v_p(B)=-v_p(H) for a solution.

## D2. The p-adic dichotomy (Task 2)

Fix a prime p with p^2 > b (STRICT; see sharpness below).
Multiples of p in [a,b] are p*t with ceil(a/p) <= t <= floor(b/p).
Since p*t <= b < p^2, t < p, so p does not divide t; also t>=1.
Let k = #{multiples} = max(0, floor(b/p)-ceil(a/p)+1) and, if k>=1,
u = ceil(a/p), so the multiples are p*(u+j), j=0..k-1, with
1 <= u <= u+k-1 = floor(b/p) <= p-1; in particular k <= p-1
(used in D3) and every u+j is in [1,p-1], coprime to p.

Split H = S0 + S1, S0 = sum_{p not| n} 1/n, S1 = sum_j 1/(p(u+j))
(if k=0, S1=0). Each term of S0 has v_p = 0, and a sum of
p-integral rationals is p-integral (common denominator coprime
to p), so v_p(S0) >= 0 (with S0=0 allowed, v=+inf).
Define T_p = sum_{j=0}^{k-1} 1/(u+j) in Z_(p) (denominators coprime
to p). Then S1 = T_p / p, v_p(S1) = v_p(T_p) - 1 >= -1, and
T_p mod p means its image in Z_(p)/pZ_(p) = F_p, i.e.
sum_j (u+j)^{-1} in F_p.

Also pH = p*S0 + T_p with p*S0 in pZ_(p), so
  pH = T_p (mod p) in F_p.   (*)

Dichotomy (k>=1):
 (GOOD) If T_p != 0 in F_p: v_p(S1) = -1 < 0 <= v_p(S0), the
   strict minimum is attained once, so v_p(H) = -1 exactly.
 (BAD) If T_p = 0 in F_p: v_p(T_p)>=1, v_p(S1)>=0, so
   v_p(H) >= 0.
If k=0: S1 absent, v_p(H) >= 0 directly (call this VACUOUS;
it behaves like BAD for m but T_p is undefined and p must not
be counted as good).

Hypotheses audit: (i) p^2 > b is used for t<p and p not| t and
u+j <= p-1. It is SHARP: if p^2 <= b the term 1/p^2 can occur,
e.g. [a,b]=[9,9], p=3: H=1/9, v_3=-2, no -1/>=0 dichotomy.
(ii) p ODD is NOT needed for the dichotomy: the argument is
verbatim for p=2 when 4>b. Oddness may matter elsewhere
(e.g. p=2 in the (b/2,b] range, or 2-invertibility in small-k
computations), but as a hypothesis of the dichotomy itself it
is superfluous. (iii) k>=1 is essential to define T_p.

Forcing on m. Let (a,b,m) be a solution, so m=B by D1.
 GOOD case: v_p(H)=-1 => v_p(m)=v_p(B)=1, i.e. p||m.
   Residue mod p^2: write m = p*m', p not| m'. Integrality gives
   H+1/m in Z_(p); an element x of Q_p has v_p(x)>=0 iff
   v_p(px)>=1 iff px = 0 mod p in Z_(p)/p. Apply to x=H+1/m:
   pH + p/m = 0 in F_p. By (*), pH=T_p in F_p; p/m = 1/m' in F_p.
   Hence 1/m' = -T_p in F_p^*, m' = -T_p^{-1} in F_p^*, i.e.
     m = -p * T_p^{-1} (mod p^2),
   ONE specific residue class mod p^2 (among classes with v_p=1).
 BAD or VACUOUS case: v_p(H)>=0 => p not| B => v_p(m)=0, p not| m.
   NO residue class mod p (or p^2) is forced: H and 1/m are both
   p-integral, their sum is automatically p-integral; local
   integrality at p imposes nothing beyond p not| m. Any claim
   of a forced mod-p^2 class at a bad prime would be FALSE.

## D3. Bad u for fixed k (Task 3)

Fix k>=1 and a prime p>k (in the application k<=p-1 by D2).
For u in F_p with u+j != 0 for all j (i.e. u not in
{0,-1,...,-(k-1)}), set D(u)=prod_{j=0}^{k-1}(u+j),
T(u)=sum_j 1/(u+j) = D'(u)/D(u) (logarithmic derivative:
D'/D = sum_j 1/(u+j) as a polynomial identity over Z, hence mod p).
So T(u)=0 in F_p iff N(u):=D'(u)=0 (denominator nonzero).
N is a polynomial of degree <= k-1 whose u^{k-1}-coefficient is
k (each of the k summands prod_{i != j}(u+i) contributes leading
coefficient 1). Since p>k, p does not divide k, so deg N = k-1
exactly (for k=1, N=1, degree 0), N is not the zero polynomial,
hence N has at most k-1 roots in F_p. Therefore the bad event
has AT MOST k-1 solutions u in F_p (admissible u). Remark:
without p>k (or at least p not| k plus a separate non-vanishing
check) the degree argument alone does not bound the roots;
the hypothesis p>k is automatic in the sieve range but must be
stated for the standalone lemma. Direct check that N is not
identically zero even without the leading coefficient: for
k<=p the roots of D are distinct mod p and simple, and
N(-j)=prod_{i != j}(i-j) != 0 in F_p, so in fact u=-j is never
a bad root; the bound is about the other residues.

Direct computation at u=1:
 k=1: T=1/1=1 != 0 mod p for every p. Never bad. (N=1.)
 k=2: T=1+1/2=3/2. For odd p (2 invertible, and p=2 cannot occur
   with u=1,k=2 under p^2>b since that needs b>=4=2^2):
   T=0 in F_p iff 3=0 in F_p iff p=3. Claimed p=3: CONFIRMED.
   (Check via N(u)=2u+1: root u=-1/2; u=1 is a root mod p iff
   p|3.)
 k=3: T=1+1/2+1/3=11/6. For p>3 (6 invertible; p<=3 cannot occur
   with u=1,k=3 under p^2>b since that needs b>=3p, so p^2>3p,
   p>3): T=0 in F_p iff 11=0 in F_p iff p=11. Claimed p=11:
   CONFIRMED. (N(u)=3u^2+6u+2, N(1)=11.)
In general at u=1, T=H_k (the k-th harmonic number) and bad
primes are exactly the prime divisors >k of the numerator of H_k
in lowest terms (for k=2: numerator 3; k=3: numerator 11).

## D4. CRT assembly and the target lemma (Task 4)

Let G = {primes p : p^2>b, k_p>=1, T_p != 0 mod p} (the good
primes; whether p=2 is admitted when 4>b is immaterial, see D2).
For each p in G, D2 forces m = r_p (mod p^2) with
r_p = -p*T_p^{-1} mod p^2. The moduli p^2 are pairwise coprime,
so CRT gives a UNIQUE class r (mod Q), Q = prod_{p in G} p^2,
such that every solution m satisfies m = r (mod Q).
Also m | L := lcm(a..b): indeed H = S/L with S in Z (each
L/n in Z), so A/B = S/L, LA = BS, gcd(A,B)=1 => B | L, and
m=B. Hence m <= L and every prime factor of m is <= b
(a prime dividing L divides some n in [a,b]): m is b-smooth.
For p in G this is consistent: v_p(m)=1 <= v_p(L) since p
divides the multiple p*u in [a,b]. Primes with p^2<=b are NOT
constrained by D2 at all; they are constrained only by m|L.

Target lemma assessment. Statement as posed: IF for all large b
(uniformly over all 1<=a<=b) the forced class r(a,b) mod Q(a,b)
contains no b-smooth m <= L(a,b) (a fortiori none dividing
L(a,b)), THEN there are only finitely many solutions.
The REDUCTION IS VALID as a conditional: a solution for (a,b)
would have m in exactly that class with m|L, m<=L, m b-smooth;
emptiness for every (a,b) with b>B0 leaves only b<=B0, finitely
many intervals, each with at most one m (D1). Caveats:
 (a) Quantifiers are load-bearing: the hypothesis must hold for
     ALL a<=b with b>B0, not e.g. only a=1, else the conclusion
     covers only those a.
 (b) The hypothesis with "b-smooth and <=L" is STRONGER than
     needed (divisors of L are a subset); using it is valid but
     makes the target harder than necessary. The sharp target
     is: no divisor of L in the class.
 (c) The lemma is a reformulation/target, not progress by
     itself: its hypothesis is where all the difficulty sits.

Caveat about Q > L: CORRECT, Q > L alone does NOT suffice.
Least-residue point, in my own words: CRT does not say m is
large; it says m lies in one arithmetic progression
r, r+Q, r+2Q, ... . If Q > L, at most one term of the progression
can be <= L, namely the least positive residue r0 in [1,Q]
itself. But nothing in "Q>L" prevents r0 from being small,
smooth, or even a divisor of L: the residues r_p are local data,
and CRT can combine large local moduli into a small global
least residue. Size of the modulus controls the SPACING of the
class, not the SIZE of its least element. One must prove
something about r0 itself (r0 > L, or r0 not b-smooth, or
r0 not | L), which is arithmetic information beyond log Q.
Concrete witness: (a,b)=(2,3) is a solution with m=6. Good odd
primes: p=3, Q=9 > L=lcm(2,3)=6, forced class 6 mod 9, and the
least residue 6 IS the solution. Including p=2 (also good):
Q=36 > 6, class 6 mod 36, least residue still 6. So even
Q >> L is compatible with a solution sitting at the least
residue. QED for the caveat.

## D5. Size check, a <= b/2 (Task 5)

Let b>=4 and a <= b/2. Let p be prime, b/2 < p <= b.
Then a <= b/2 < p <= b, so p in [a,b]; 2p > b, so p is the ONLY
multiple of p in [a,b]: k=1, u=1, T_p = 1 != 0 mod p: p is GOOD.
Also p^2 > b: p > b/2 gives p^2 > b^2/4 >= b for b>=4, strict
because p>b/2 is strict (at b=4, p=3, 9>4). And p>2, so p is
odd automatically. Conclusion: for a<=b/2, b>=4, EVERY prime
in (b/2,b] is good. (Bertrand's postulate separately gives at
least one such prime, so Q>1, but the size bound needs PNT.)

Hence, with theta(x) = sum_{p<=x} log p (Chebyshev function),
 log Q >= sum_{b/2<p<=b} log(p^2) = 2*(theta(b) - theta(b/2)).
PNT in theta form: theta(x) = (1+o(1)) x. Therefore
 theta(b)-theta(b/2) = (1+o(1))b - (1+o(1))(b/2)
   = b/2 + o(b),
 log Q >= 2*(b/2 + o(b)) = b + o(b) = (1+o(1)) b,
i.e. liminf_{b->inf} (log Q)/b >= 1 along a<=b/2.
Explicit epsilon form: for any eps>0 and b large,
theta(b)>=(1-eps)b and theta(b/2)<=(1+eps)b/2 give
2*(theta(b)-theta(b/2)) >= b(1-3eps).
Notes: (i) the constant 1 needs the full PNT; elementary
Chebyshev bounds theta(x) ~asymp x give only log Q >= c*b for
some explicit c<1. (ii) This uses only the (b/2,b] primes;
other good primes only enlarge Q. (iii) The regime hypothesis
a<=b/2 is essential: if a>b/2, primes in (b/2,a) have k=0 and
drop out, and the bound becomes 2*(theta(b)-theta(a)) which
can be o(b). (iv) Comparison scale: log lcm(1..b)=psi(b)~b,
so log Q >= (1+o(1))b says Q is at least on the lcm scale;
by D4 that alone does not finish anything.

================================================================
# PART 2: COMPARISON WITH THE NOTE (and the dossier's account)
================================================================

Sources compared: (i) the note itself, full text fetched via the
dossier's DOI link (see header); (ii) dossier INFORMATION.md
Section 6. The dossier's summary was found faithful to the note
in every item below, with two trivial simplifications noted at
Propositions 8/10 and Theorem 13 (the note is marginally more
precise than the summary in both places; neither simplification
is an error in the note).

## Comparison table (verdict per item)

| Item | Note's claim (as stated in the note) | My independent derivation | Verdict |
|---|---|---|---|
| Lemma 1 (denominator forcing) | H(a,b)=A/B lowest terms; a solution forces m = B exactly and B \| (A+1); at most one candidate m per interval. Proof: A/B = (km-1)/m is reduced since gcd(km-1,m)=1, so the reduced denominator is m. | Same statement, proved by a different route (B \| Am, gcd(A,B)=1 gives B \| m, write m=Bs, then 1/s integer forces s=1). Also gives equivalence: solution exists iff B \| A+1. | AGREE. Certified. Note's proof is valid and complete. (One preliminary display, eq. (2), is over-compressed; see Discrepancy D-9. It is not used by the proof.) |
| Lemma 2, case (a) (good prime) | p odd prime, p^2 > b, k(p) >= 1, T_p not 0 mod p: then v_p(m) = 1 and m = -p*(T_p mod p)^{-1} (mod p^2). | Identical, including the sign and the inverse: v_p(H) = -1, pH = T_p in F_p, and p-integrality of H + 1/m forces m' = -T_p^{-1} in F_p for m = p*m'. My derivation does NOT need p odd (works for p=2 when 4 > b); the note restricts to odd primes by design (its Remark 9). | AGREE. Certified. Proof in the note is right but terse at the congruence step, then repaired by its own "for completeness" paragraph (see D-3). |
| Lemma 2, case (b) (bad prime) | T_p = 0 mod p: then v_p(m) = 0, p does not divide m, and the prime contributes no modulus-p^2 congruence to the CRT system. | Identical: v_p(H) >= 0 forces p not dividing B = m, and NO residue class mod p or p^2 is forced (both H and 1/m are p-integral, so their sum is automatically p-integral). | AGREE. Certified. "Contributes nothing" in the dossier's wording means exactly "no congruence", not "no information": the information p not\| m is real but is already implied by m \| lcm (Part 1, D4). |
| Lemma 5 (T(u) = D'/D; at most k-1 bad u) | p odd prime, 1 <= k < p, u in F_p with u,...,u+k-1 nonzero: T(u) = D'(u)/D(u), so T(u) = 0 iff D'(u) = 0, at most k-1 solutions u in F_p. | Identical bound, same logarithmic-derivative argument. I additionally recorded WHY deg D' = k-1 (leading coefficient k, nonzero in F_p because k < p) and that D'(-j) != 0, neither of which the note spells out. | AGREE. Certified. The hypothesis 1 <= k < p that my derivation found necessary IS stated in the note (the dossier's one-line summary omits it; see D-6). Note's proof is one line on the degree; correct under its stated hypothesis (see D-4). |
| Corollary 6 (finite bad primes for fixed (u,k)) | Fix u >= 1, k >= 1, T_{u,k} = N_{u,k}/M_{u,k} in lowest terms. For every prime p > u+k-1: T_{u,k} = 0 mod p iff p \| N_{u,k}; hence only finitely many bad primes for the pair (u,k). | Identical: bad primes (with reduction mod p legitimate) are exactly the prime divisors > k of the numerator; at u=1 these are the prime divisors of the numerator of H_k. The condition p > u+k-1 is exactly what makes p coprime to every u+j, hence to M_{u,k}. | AGREE. Certified. |
| Proposition 8 (a <= b/3 range) | b >= 10, a <= b/3: every prime b/3 < p <= b with p != 3 is good (u=1, k in {1,2}); log Q >= 2(theta(b) - theta(b/3)) - O(1). | Verified: p > b/3 and b >= 10 give p > sqrt(b), i.e. p^2 > b; a <= b/3 < p gives u=1; k=1 for p > b/2, k=2 for b/3 < p <= b/2; k=1 always good; k=2,u=1 bad only at p=3. | AGREE. Certified. The exclusion p != 3 is vacuous under the stated ranges (b >= 10 and p > b/3 force p >= 5); harmless redundancy, see D-5. |
| Proposition 10 (a <= b/2 range) | Hypothesis a <= floor(b/2)+1 (slightly weaker than a <= b/2). Every odd prime b/2 < p <= b has k(p)=1, T_p = 1, hence contributes; log Q >= 2(theta(b) - theta(b/2)). | Identical conclusion under my (slightly stronger) hypothesis a <= b/2, b >= 4: the unique multiple is p itself, u=1, k=1, T_p=1. The note's floor(b/2)+1 hypothesis is also correct: p > b/2 forces p >= floor(b/2)+1 >= a, so p in [a,b]. The theta step: log Q >= 2(theta(b)-theta(b/2)) is immediate since Q is a product over a set CONTAINING these primes. | AGREE. Certified. The note's hypothesis is marginally sharper than the dossier summary's "a <= b/2"; the note is right. The asymptotic log Q >= (1+o(1))b is the note's Remark 11 and explicitly uses the prime number theorem, matching my derivation's caveat that the constant 1 needs full PNT, not merely Chebyshev bounds. |
| CRT reduction (note Section 4) | P1(a,b) = odd primes p with p^2 > b, k(p) >= 1, T_p not 0 mod p; unique class m = r(a,b) (mod Q(a,b)), Q = prod p^2 over P1; and m \| lcm(a..b), hence m <= lcm(a..b) and m b-smooth. | Identical assembly (my Part 1, D4), except my derivation also admits p=2 when 4 > b, so my maximal Q can be a multiple of the note's Q in tiny cases (e.g. (2,3): mine 36, note's 9; the note's class 6 mod 9 is the correct projection). The divisibility m \| lcm(a..b): the note states it in one line from Lemma 1; my derivation proves it (H = S/L with S integral, LA = BS, gcd(A,B)=1 gives B \| L). The note also correctly warns that log lcm(a..b) is NOT psi(b) - psi(a-1) (prime powers below a can contribute via multiples in [a,b]; its example [4,5] contributing 2^2 is correct). | AGREE. Certified. Right but terse at the m \| lcm step (no proof given in the note; the step is correct and I supply the proof in Part 1). Scope difference on p=2 is deliberate in the note (Remark 9) and loses nothing load-bearing. |
| Theorem 13 (global target lemma) | IF there is B0 such that for every b >= B0 and every 1 <= a <= b, the forced class m = r(a,b) (mod Q(a,b)) contains no positive integer m that is b-smooth and <= lcm(a..b), THEN the singleton equation has only finitely many solutions. | Reduction VALID, with exactly these quantifiers (uniform over all a <= b, all b >= B0): a solution would lie in the class with m \| lcm, hence b-smooth and <= lcm; exclusion leaves only b < B0, finitely many intervals, at most one m each (Lemma 1). As in my derivation, the hypothesis with "b-smooth and <= lcm" is STRONGER than the sharp form "no divisor of lcm(a..b) in the class"; valid but harder than necessary. The theorem is a conditional target, not progress toward its own hypothesis; the note says exactly this ("These notes do not prove finiteness unconditionally"). | AGREE. Certified as a conditional reduction. No overclaim in the note. |
| Remark 14 (Q > lcm does not suffice) | If Q > X and m = r (mod Q), 0 < m <= X, then m must equal the least positive representative r0 in {1,...,Q}, and r0 <= X may happen; a large Q collapses the search to at most one candidate m = r0; what is needed is r0 > lcm or r0 non-b-smooth, "not merely a comparison of moduli". | Identical, in substance and in mechanism: CRT controls the SPACING of the class, not the SIZE of its least element; local residues can CRT-combine to a small least residue. My derivation adds a concrete witness the note does not explicitly flag: the note's own Example (2,3) has Q = 9 > lcm(2,3) = 6, and the least residue 6 IS the solution (with p=2 admitted, Q = 36 > 6, least residue still 6). | AGREE. Certified. The caveat is correct and correctly explained in the note. |

## Worked examples, verified exactly (by hand in Part 1 and by code in Part 4)

Example (2,3) [note Section 6.1]: H(2,3) = 1/2 + 1/3 = 5/6, so
A=5, B=6, B | A+1, m = 6 forced, integer value k = 1. Prime p=3:
p^2 = 9 > 3, k(3) = 1, u = 1, T_3 = 1, good; forced class
m = -3 * 1^{-1} = 6 (mod 9). P1 = {3}, Q = 9, class 6 mod 9.
The note's Section 6.1 is CORRECT IN FULL. (My derivation adds:
p=2 is also good here, T_2 = 1, forcing m = 2 (mod 4); 6 satisfies
it; the note's odd-prime Q=9 is a projection of the full class
6 mod 36.)

Example (3,6) [note Section 6.2]: the sieve conclusions are all
correct: H(3,6) has denominator 20, m = 20 forced; p=5: k=1, u=1,
T_5 = 1, good, class m = -5 = 20 (mod 25); p=3: multiples 3,6,
u=1, k=2, T_3 = 1 + 1/2 = 3/2 = 0 (mod 3), BAD, and indeed
3 does not divide 20; P1 = {5}, Q = 25, class 20 mod 25.
BUT the value of H(3,6) printed in the note is wrong as
retrieved; see Discrepancy D-1, which is the one outright
numerical error found in the note.

## Places where the note claims MORE than my derivation supports

None in the load-bearing chain (Lemmas 1, 2, 5, Corollary 6,
Propositions 8, 10, CRT, Theorem 13, Remark 14): every one of
those claims is exactly reproduced by my independent derivation.
Two non-load-bearing overstatements/understatements outside that
chain are logged as D-2 (Remark 4's heuristic asymptotics) and
D-8 (the "as large as" framing of Q's size). The note's Section 8
claims about the literature (Pascadi 2023, q <= x^{66/107};
the x^{3/5} barrier) were NOT independently verified by me and
are outside the derivation's scope; my derivation is inconclusive
on them and they are not used by any audited lemma.

## Places where my derivation needed a hypothesis the note does not state

Only one candidate arose, and on fetching the note it dissolved:
the standalone "at most k-1 bad u" bound needs p > k (leading
coefficient k nonzero in F_p). The NOTE DOES STATE 1 <= k < p in
Lemma 5; only the dossier's one-line summary omits it (D-6).
My derivation also initially flagged "p odd" as a hypothesis of
the dichotomy; the note states it, and my derivation shows it is
a scope restriction rather than a logical need (the dichotomy
holds for p=2 when 4 > b). That is a (deliberate, disclosed)
weakening in the note, not a gap: see D-7.

================================================================
# PART 3: DISCREPANCY LIST (exact statements, nothing repaired silently)
================================================================

D-1. OUTRIGHT ERROR in the note (as retrieved), non-load-bearing.
Note, Section 6.2, prints: "H(3,6) = 1/3 + 1/4 + 1/5 + 1/6 =
49/20". The correct value is 19/20 (1/3+1/4+1/5+1/6 = 57/60 =
19/20; verified by exact rational arithmetic in Part 4). The
printed 49/20 is internally inconsistent with the note itself:
(i) with Lemma 1, since 49 + 1 = 50 is NOT divisible by 20, the
fraction 49/20 would give NO solution at (3,6), contradicting
the same paragraph's "Lemma 1 forces m = 20 and k = 1";
(ii) with the note's Table 1, which lists (a,b,m) = (3,6,20)
with integer value k = 1, and (19+1)/20 = 1 while (49+1)/20 is
not an integer. Every other assertion in Section 6.2 (m=20,
p=5 good with class 20 mod 25, p=3 bad, Q=25) is correct and
depends only on the denominator 20 and the local data, so the
error does not propagate. Caveat on provenance: the full text
was read in ResearchGate's text extraction; a "19" misprinted
or mis-extracted as "49" cannot be distinguished from inside
the extraction. As retrieved, the text says 49/20, and 49/20
is wrong. Classification: note is wrong (numerical/typographical
error in a worked example), conclusions of the example unaffected.

D-2. ERROR in a heuristic remark in the note, non-load-bearing.
Note, Remark 4, states the expected number of bad primes in the
range p > sqrt(b) "should be sum_{p>sqrt(b)} 1/p ~ log log b
(very slowly growing)". For the primes actually in play in the
sieve (sqrt(b) < p <= b, since k(p) >= 1 needs p <= b), Mertens'
theorem for primes gives sum_{sqrt(b)<p<=b} 1/p =
log log b - log log sqrt(b) + o(1) = log 2 + o(1): the sum is
BOUNDED (Theta(1)), not ~ log log b. The remark is explicitly
labelled heuristic ("This is far from a proof"), no lemma uses
it, and the corrected asymptotics make the heuristic conclusion
(bad primes are rare) stronger, not weaker. Classification:
note is wrong on this heuristic asymptotic; no downstream effect.

D-3. Note RIGHT BUT TERSE: Lemma 2's proof, first pass.
The note writes: "Reducing the equality H(a,b) + 1/m in Z modulo
p in Z_p yields the congruence (4)." Read literally this skips a
step, since (1/p)T_p and 1/m are not individually in Z_p. The
note's own "For completeness" paragraph immediately after gives
the correct reduction: with m = p*m1, p not | m1, the integrality
condition reduces in Z_p/pZ_p to T_p + m1^{-1} = 0 (mod p), i.e.
m1 = -T_p^{-1} (mod p), which is (4). (In that paragraph the note
writes the summands as "(1/p)T_p + 1/(p*m1) = 0 in Z_p/pZ_p",
the same shorthand; the resulting congruence is correct, and my
Part 1 derivation via pH = T_p (mod p) is the fully spelled-out
form.) Classification: right but terse; conclusion certified.

D-4. Note RIGHT BUT TERSE: Lemma 5's proof asserts "Since
deg(D') = k-1, D' has at most k-1 roots in F_p" in one line.
The degree assertion needs the leading coefficient of D', which
is k, to be nonzero in F_p; this is guaranteed by the lemma's
stated hypothesis 1 <= k < p, but the note does not say so.
With that one-line supplement the proof is complete.
Classification: right but terse; conclusion certified.

D-5. REDUNDANT (vacuous) exclusion in Proposition 8, not an error.
Proposition 8 excludes p = 3 while assuming b >= 10 and
p > b/3, which already force p > 10/3, i.e. p >= 5. The
exclusion can never trigger. Classification: harmless
redundancy; the proposition is correct as stated.

D-6. Hypothesis present in the note, absent from the dossier summary.
Dossier Section 6 summarises Lemma 5 as "for fixed k the bad
event T(u) = 0 has at most k-1 solutions u in F_p", without the
hypothesis k < p. The note's Lemma 5 states "1 <= k < p"
explicitly. My derivation confirms the hypothesis is needed for
the degree argument as stated (and that it is automatic in the
sieve range, where k <= p-1 follows from p^2 > b). Classification:
dossier summary is terse; the note is complete. Not an error in
the note.

D-7. SCOPE DIFFERENCE (deliberate in the note), not an error.
The note's sieve and Q are built from ODD primes only (Lemma 2
hypothesis; Remark 9 explains p=2 is set aside for a separate
2-adic analysis and "nothing in the CRT construction requires
using p = 2"). My derivation shows the dichotomy itself holds
verbatim for p = 2 whenever 4 > b (e.g. at (2,3), p=2 is good
and forces m = 2 mod 4, an extra congruence the note's Q=9 does
not capture; the full modulus there is 36). All of the note's
claims about its (odd-prime) Q remain correct; Theorem 13's
hypothesis is correspondingly (very slightly) harder to satisfy
with a smaller Q, so the reduction is unaffected. Classification:
note is right within its stated scope; my derivation supports a
marginally stronger CRT modulus in tiny cases only (p=2 can only
satisfy p^2 > b when b <= 3).

D-8. FRAMING imprecision about the SIZE of Q, not a logical error.
The abstract, Remark 12, and Section 8 describe Q as able to be
"as large as exp((1+o(1))b)" / "x^{1+o(1)}". What Propositions 8
and 10 plus Remark 11 actually prove is a LOWER bound,
log Q >= (1+o(1))b in the regime a <= b/2; no upper bound near
(1+o(1))b is proved, and Q can be strictly larger: trivially
log Q <= 2*theta(b) ~ 2b, and my Part 4 computation at b=500,
a=1 gives log Q = 916.9 ~ 1.83*b, while log lcm(1..500) =
psi(500) ~ 500, so there Q exceeds the search range x itself by
a factor ~ x^{0.83} on the log scale. The bottleneck conclusion
the note draws (modulus at least comparable to the search range,
far beyond the x^{66/107} reach of current smooth-number results)
is therefore correct and, if anything, understated. Classification:
note's proved statements are right; the "as large as" phrasing
understates its own lower bound. No downstream effect.

D-9. Note RIGHT BUT the displayed inference is over-compressed.
Note, Section 2, display (2): from (1) the note gets
"A/B = -1/m (mod Z), hence B | m(A+1)". The statement (2) is
TRUE under the standing lowest-terms hypothesis, but it is not
a one-step consequence of the congruence: writing H + 1/m = t
gives m(A+1) = B(mt - 1) + m, so B | m(A+1) iff B | m, and the
missing step is exactly B | Am (from Am + B = Bmt) together
with gcd(A,B) = 1, yielding B | m. With that step supplied,
(2) follows. Display (2) is not used in the note's proof of
Lemma 1 (which is self-contained and correct), so nothing
downstream is affected. Classification: statement correct,
derivation as printed has a gap of one gcd step; terse, not wrong.

No other discrepancies found. In particular: NO place in the
load-bearing chain where the note claims more than my derivation
supports; NO outright errors in any lemma, proposition, the CRT
reduction, Theorem 13, or Remark 14; the only outright errors
in the note as retrieved are D-1 (worked-example numerator) and
D-2 (heuristic asymptotic), both outside the proof chain.

================================================================
# PART 4: COMPUTATIONAL CHECKS AND RESULTS
================================================================

Code: ~/workspace/math-hunt/erdos-288/clusters/B/auditor2_check.py
(exact rational arithmetic via fractions.Fraction; T_p mod p via
modular inverses; independent of the note's Appendix A script).
Captured output: auditor2_check_output.txt in the same directory.
All checks were run BEFORE the comparison in Parts 2-3 was
written, against the Part 1 derivation only.

Check 1 (dichotomy, exhaustive). For every interval [a,b] with
1 <= a <= b <= 200 and every prime p with p^2 > b and p <= b
(plus one representative prime > b per interval; all larger
primes are vacuous since den H(a,b) | lcm(1..b)): computed
v_p(H(a,b)) exactly and compared with the Part 1 dichotomy
(good => v_p = -1; bad or k=0 => v_p >= 0).
Result: 566,655 prime-interval checks, 0 failures.

Check 2 (Lemma 1 / census at small cutoff). Solutions with
b <= 200 are exactly (a,b,m) = (1,1,1), (1,2,2), (2,2,2),
(1,3,6), (2,3,6), (3,6,20): the six known solutions, matching
the note's b <= 1600 census (Section 9 / Table 1) on the overlap.
(Full reproduction to b=1600 is Cluster C0's task, not Auditor 2's;
no mismatch on the b <= 200 overlap.)

Check 3 (worked examples). H(2,3) = 5/6, m = 6; p=3: k=1, u=1,
T_3 = 1 mod 3, good, forced class 6 mod 9 (note correct);
p=2: k=1, u=1, T_2 = 1 mod 2, good, forced class 2 mod 4
(extra congruence outside the note's odd-prime scope, cf. D-7).
H(3,6) = 19/20 (NOT 49/20, cf. D-1), m = 20; p=3: k=2, u=1,
T_3 = 0 mod 3, BAD, and 3 does not divide 20; p=5: k=1, u=1,
T_5 = 1, good, forced class 20 mod 25. All sieve conclusions of
both examples verified exactly.

Check 4 (bad-u bound and small-k classification). For k = 1..8
and all primes p <= 500 with p > k, counted u in F_p (all
u+j nonzero) with T(u) = 0: maximum counts were 0,1,2,3,4,5,6
for k = 1..7 (attaining the bound k-1) and 5 for k=8 (bound 7):
bound k-1 never exceeded. At u=1, over all primes p <= 2000
with p > k: k=1 has NO bad primes; k=2 has bad primes exactly
{3}; k=3 has bad primes exactly {11}. This confirms the claimed
p=3 (k=2) and p=11 (k=3) exactly, and the k=2 symmetric-pair
characterisation is consistent with the root u = -1/2 of
N(u) = 2u+1 (u=1 is that root mod p iff p | 3).

Check 5 (size of Q). log Q(a,b) computed from the full sieve
(all good primes p with p^2 > b, including p=2 where applicable)
for b in {50,100,200,300,500}, a = 1 and a = floor(b/2):
(log Q)/b ranged from 1.425 (b=50) to 1.834 (b=500, a=1),
always >= 1 in this range and always at least the Proposition 10
lower bound 2(theta(b)-theta(b/2)) (the excess over the bound
comes from good primes in (sqrt(b), b/2], which Propositions 8
and 10 do not count). Consistent with log Q >= (1+o(1))b and
with D-8: at b=500 the true log Q ~ 1.83b is well above the
proved lower bound ~ b.

Not checked by Auditor 2 (out of mandated scope): the note's
Section 9 random bad-prime sampling statistics (5,000 intervals,
1,882 bad of 1,167,988 incidences, mean per-interval bad fraction
0.3335) and its Section 8 literature claims. My derivation is
inconclusive on both; neither is used by any audited item.

================================================================
# SUMMARY OF VERDICTS
================================================================

Lemma 1: certified (agree). Lemma 2 case (a): certified (agree;
proof terse at one step, repaired in-note, D-3). Lemma 2 case (b):
certified (agree). Lemma 5: certified (agree; hypothesis k < p
stated in the note). Corollary 6: certified (agree).
Proposition 8: certified (agree; vacuous p != 3 exclusion, D-5).
Proposition 10: certified (agree; hypothesis a <= floor(b/2)+1
in the note is correct and marginally sharper than the dossier's
summary). CRT reduction: certified (agree; m | lcm step terse in
the note, proof supplied in Part 1; odd-prime scope per D-7).
Theorem 13: certified as a conditional reduction (agree;
quantifiers uniform over a, as required). Remark 14: certified
(agree; caveat correct, instantiated by the note's own (2,3)
example with Q = 9 > lcm = 6 and least residue 6 a solution).
Outright errors in the note as retrieved: exactly two, both
outside the proof chain: D-1 (H(3,6) printed as 49/20; correct
19/20) and D-2 (Remark 4's "~ log log b" heuristic; correct
order for sqrt(b) < p <= b is the bounded constant log 2).
