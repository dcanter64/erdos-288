# Auditor 2 — INDEPENDENT DRAFT (written before reading Nayak Section 3)

## Statement
If intervals I,J of positive integers intersect and H(I)+H(J) is an integer,
then up to swapping, (I,J) is one of
([1,1],[1,1]), ([1,2],[1,2]), ([1,2],[2,2]), ([2,2],[2,2]),
and all four have integer sum.

## Proof draft

Write I,J nonempty intervals, [r,s] = union (an interval, since they
intersect), c_n = #{intervals containing n} in {1,2}, c_n=2 exactly on
the (nonempty) intersection. S = sum_{n=r}^s c_n/n.

Unique-minimum-valuation principle: if for some prime p one term has
v_p strictly smaller than every other term, then v_p(S) equals that
minimum (ultrametric property, the other terms factor p^{-m} times a
p-integral ... standard), in particular if the minimum is < 0 then S
is not an integer.

Case s=r: I=J=[r,r], S=2/r, integer iff r|2 iff r=1,2. Two listed pairs.

Henceforth s>r.

Case [r,s] subset of {1,2}: then r=1,s=2 (since s>r). Intervals are
among [1,1],[2,2],[1,2]; intersecting, union=[1,2] excludes
([1,1],[1,1]) and ([2,2],[2,2]) (union a singleton, previous case)
and ([1,1],[2,2]) (disjoint). Remaining up to swap:
([1,2],[1,2]): S=3 works; ([1,2],[2,2]): S=2 works;
([1,1],[1,2]): S=1+3/2=5/2 not integer. Done.

Henceforth s>=3, s>r.

Subcase A: 2r <= s+1.
 Bertrand: there is a prime p with s/2 < p <= s
 (if s is prime take p=s; if s composite apply Bertrand in the form
 "for t>1 a prime lies strictly between t and 2t" to t=floor(s/2),
 giving floor(s/2) < p < 2 floor(s/2) <= s, and p>s/2 in both parities).
 Then p>=r: for s even, p>s/2>=r or p>s/2 and ... (if 2r<=s then
 p>s/2>=r; if s odd, 2r<=s+1 gives r<=(s+1)/2<=p since p>s/2 and p
 integer implies p>=(s+1)/2). So p in [r,s].
 p is odd: p>s/2 and s>=3; if s>=4 then p>2; if s=3 then p=3.
 Multiples of p in [r,s]: only p itself, since 2p>s.
 Hence v_p(c_p/p) = -1 (p odd, so v_p(c_p)=0, c_p in {1,2}), while
 for n != p, p does not divide n, so v_p(c_n/n)=0.
 Unique minimum -1 <0, S not an integer.

Subcase B: 2r > s+1.
 Let k = s-r+1 = number of terms, >=2. Then r-k = 2r-s-1 >= 1, so
 r > k: the k consecutive integers r,...,s are all > k.
 Sylvester's theorem (1892; the Sylvester-Schur circle): the product
 of k consecutive positive integers, each > k, has a prime divisor
 p > k. (This is exactly the existence theorem needed here; Bertrand
 alone does NOT suffice in this subcase, e.g. [8,10] is fine via 5,
 but prime-free upper tails like [114,126] need a large prime factor
 of a composite term, e.g. 61 | 122.)
 Such p divides exactly one term n0 in [r,s]: p divides some term
 (it divides the product, prime), and cannot divide two distinct
 terms, whose difference would be a nonzero multiple of p of size
 <= s-r = k-1 < p.
 Also p > k >= 2, so p is odd, v_p(c_{n0})=0, and
 v_p(c_{n0}/n0) = -v_p(n0) <= -1, whereas for n != n0, p does not
 divide n, so v_p(c_n/n)=0. Unique minimum <0, S not an integer.

A and B exhaust all possibilities (2r <= s+1 or 2r > s+1). QED.

Notes on coefficients c_n=2: the danger is only p=2 (v_2(2)=1 could
raise a term's valuation and destroy/create uniqueness). Every prime
used above is odd, so c_n is a p-adic unit and never affects the
argument, whether or not the uniquely divided term lies in the
overlap I cap J. This is why the proof must avoid a 2-adic maximal
power argument, or handle overlap terms at 2 separately; the odd
prime route sidesteps it entirely.
