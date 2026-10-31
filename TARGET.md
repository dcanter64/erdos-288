# Cluster B: the target lemma for the singleton case, in campaign notation

Source: Zeraoulia Rafik, "The singleton case of Erdos Problem 288:
A CRT reduction and a smooth-number obstruction", February 2026,
doi:10.13140/RG.2.2.10862.47684/1, Theorem 13 and Remark 14.
Certification record: AUDIT-B.md in this workspace (Cluster B
verifier). This file keeps the note's statement and the campaign's
repair visibly distinct. Nothing in the repair is attributed to
the note.

## Campaign notation

- H(a,b) = sum_{n=a}^b 1/n = A(a,b)/B(a,b) in lowest terms;
  B(a,b) = den H(a,b). Singleton equation: H(a,b) + 1/m in Z.
- L(a,b) = lcm(a, a+1, ..., b).
- For an odd prime p with p^2 > b, let k(p) be the number of
  multiples of p in [a,b], the multiples p*u, ..., p*(u+k(p)-1),
  and T_p = sum_{j=0}^{k(p)-1} 1/(u+j), read in F_p.
- P1(a,b) = { odd primes p : p^2 > b, k(p) >= 1, T_p != 0 (mod p) }
  (the good primes). Q(a,b) = product of p^2 over p in P1(a,b),
  with Q(a,b) = 1 if P1(a,b) is empty.
- r(a,b): the CRT residue class modulo Q(a,b) assembled from
  Lemma 2(a), m = -p*(T_p mod p)^{-1} (mod p^2) for p in P1(a,b);
  r_0(a,b) its least positive representative (r_0 = 1 when
  Q(a,b) = 1).

Certified facts used below (AUDIT-B.md): Lemma 1 (a solution
forces m = B(a,b) and A(a,b) = -1 (mod B(a,b))); Lemma 2 and the
CRT reduction (a solution's m lies in the class r(a,b) mod
Q(a,b), divides L(a,b), is b-smooth and <= L(a,b)); Proposition 10
(for b >= 4 and a <= floor(b/2)+1, every odd prime in (b/2, b]
lies in P1(a,b), so in particular P1(a,b) is nonempty).

## The note's Theorem 13, as stated

> Theorem 13 (Global target lemma (smooth numbers in a forced CRT
> class)). Assume that there exists B_0 such that for every
> b >= B_0 and every 1 <= a <= b, the congruence class
> m = r(a,b) (mod Q(a,b)) contains no positive integer m
> satisfying (i) all prime factors of m are <= b (i.e. m is
> b-smooth), (ii) m <= lcm(a, a+1, ..., b). Then the singleton
> equation has only finitely many solutions (a, b, m).

Certified status (AUDIT-B.md, Section 2): the implication is
logically valid and its proof in the note is correct, BUT the
hypothesis is unsatisfiable as stated, so the theorem is vacuous
and NOT CERTIFIED as a usable target. Reason: for (a, b) =
(q^2, q^2), q any prime, no odd prime p with p^2 > b has a
multiple in [a, b] (p > q is forced by p^2 > q^2, and p | q^2
forces p = q), so P1 is empty, Q = 1, the forced class is all
integers, and m = q^2 is b-smooth with m = L(a,b); the exclusion
fails for arbitrarily large b, hence for every B_0. (The same
failure occurs with m = 1, and even under the sharper hypothesis
"no divisor of L(a,b) in the class", since 1, q, q^2 all divide
L(q^2, q^2) = q^2 and lie in the class modulo 1. Weakening the
condition on m therefore cannot repair the statement; the
(a, b) quantifier itself must be restricted.)

## The campaign's repair (NOT the note's statement)

The defect is confined to intervals where the sieve is empty
(P1(a,b) empty, Q(a,b) = 1): there the CRT class carries no
information, yet the note's hypothesis demands an exclusion
there. The minimal repair restricts the exclusion hypothesis to
intervals where the sieve is nonempty, and says separately what
is needed in the sieve-empty regime.

> **Theorem 13R (campaign repair, minimal form).** Assume there
> exists B_0 such that for every b >= B_0 and every 1 <= a <= b
> with **P1(a,b) nonempty**, the class m = r(a,b) (mod Q(a,b))
> contains no b-smooth positive integer m <= L(a,b). Then the
> singleton equation has only finitely many solutions with
> P1(a,b) nonempty. In particular, it has only finitely many
> solutions with a <= floor(b/2)+1.

Proof. Let (a, b, m) be a solution with b >= B_0 and P1(a,b)
nonempty. By Lemma 1, m = B(a,b); hence m | L(a,b), m <= L(a,b),
and m is b-smooth. By Lemma 2 and the CRT reduction, m lies in
the class r(a,b) (mod Q(a,b)). This contradicts the assumed
exclusion. So every solution with P1(a,b) nonempty has b < B_0;
there are finitely many such pairs (a, b), each with at most one
m by Lemma 1. For the "in particular": if b >= 4 and
a <= floor(b/2)+1, Proposition 10 puts every odd prime in
(b/2, b] in P1(a,b), and such a prime exists by Bertrand's
postulate, so P1(a,b) is nonempty and the conclusion applies.
QED.

> **Theorem 13R+ (campaign repair, full-finiteness form).**
> Assume there exists B_0 such that
> (H-sieve) for every b >= B_0 and every 1 <= a <= b with
> P1(a,b) nonempty, the class m = r(a,b) (mod Q(a,b)) contains
> no b-smooth positive integer m <= L(a,b); and
> (H-blind) there is no solution (a, b, m) with P1(a,b) empty
> and b >= B_0.
> Then the singleton equation has only finitely many solutions.

Proof. Let (a, b, m) be a solution with b >= B_0. If P1(a,b) is
nonempty, Lemma 1 and the CRT reduction put m in the forced
class with m b-smooth and m <= L(a,b), contradicting (H-sieve).
If P1(a,b) is empty, (a, b, m) contradicts (H-blind). Hence all
solutions have b < B_0, finitely many pairs (a, b), at most one
m each. QED.

Remarks on the repair, for later clusters.

1. (H-blind) is a genuine remaining target, not a formality, and
   it is exactly the sieve-blind regime. P1(a,b) empty forces
   strong structure: for b >= 4 it forces a > floor(b/2)+1 (else
   Proposition 10 supplies a good prime), and it forces every odd
   prime p with p^2 > b and k(p) >= 1 to be bad, in particular
   there is no such prime with k(p) = 1 (k(p) = 1 gives
   T_p = 1/u != 0 mod p, always good). Closing (H-blind) needs an
   idea outside the note's sieve (e.g. the prime 2 and primes
   with p^2 <= b that the sieve discards, or a short-interval
   argument for a > b/2).
2. In (H-sieve), the exclusion is needed only for the single
   candidate m = B(a,b): a solution forces m = B(a,b), and
   B(a,b) is automatically b-smooth and <= L(a,b). So (H-sieve)
   may be weakened, without weakening the conclusions above, to:
   for every b >= B_0 and every a with P1(a,b) nonempty,
   B(a,b) != r(a,b) (mod Q(a,b)), i.e. the forced denominator
   candidate fails at least one good prime's congruence. This
   single-candidate form is the weakest target of this shape
   that still implies the conclusions. It is recorded for
   logical completeness, not as an easier target: the verifier
   found it already fails at 80 non-solution intervals with
   b <= 300 (see Remark 4), so there is no computational
   evidence that it becomes true for large b.
3. By Remark 14 (certified), (H-sieve) would follow from either
   r_0(a,b) > L(a,b) or r_0(a,b) not b-smooth, for all large b
   and all a with P1(a,b) nonempty; a bare comparison
   Q(a,b) > L(a,b) does not suffice (witness (a, b) = (2, 3):
   Q = 9 > L = 6, r_0 = 6 = L, and (2, 3, 6) is a solution).
4. The hypothesis of 13R / 13R+ is not known to be true; unlike
   the note's Theorem 13 hypothesis, it is not refuted by any
   infinite family either: the (q^2, q^2) family does not touch
   it (P1 empty there). But it is an asymptotic statement only,
   and it already fails pointwise in the computed range: the
   exclusion in (H-sieve) fails at every interval whose
   denominator candidate B(a,b) itself lies in the forced class
   (B(a,b) is b-smooth and <= L(a,b)), and the verifier found
   83 such intervals with P1 nonempty and b <= 300: the 3
   solution intervals with Q > 1, namely (1,3), (2,3), (3,6),
   and 80 non-solution intervals, among them the family
   (2^k, 2^k+1) for k = 2, 4, 5, 6, 7, 8 and intervals up to
   (297, 298) (clusters/B/verifier_target_check.py and
   verifier_target_output.txt). Lemma 2 gives necessary
   conditions only, so B(a,b) lying in the class does not make
   (a,b) a solution; these pointwise failures do not falsify
   the asymptotic hypothesis (B_0 may exceed 300), but later
   clusters should treat (H-sieve) as a statement about large
   b whose truth is open, not as a near-truth suggested by
   small cases.

## Addendum (2026-10-30)

Cluster E update (certified, see CLUSTER-E.md): the pointwise hypothesis (H-sieve) is false for every B_0 (Theorem F family); the singleton case is nevertheless closed in regimes (i) and (ii) by arguments using input outside the forced class.
