from fractions import Fraction
from math import prod, isqrt
import sys

def primes_upto(N):
    sieve=[True]*(N+1)
    sieve[0]=sieve[1]=False
    for i in range(2,isqrt(N)+1):
        if sieve[i]:
            step=i; start=i*i
            sieve[start:N+1:step]=[False]*(((N-start)//step)+1)
    return [i for i,ok in enumerate(sieve) if ok]

def prime_factors(n):
    out={}
    d=2
    x=n
    while d*d<=x:
        while x%d==0:
            out[d]=out.get(d,0)+1
            x//=d
        d+=1 if d==2 else 2
    if x>1: out[x]=out.get(x,0)+1
    return out

def H(a,b):
    return sum(Fraction(1,n) for n in range(a,b+1))

# 1) Brute force intersecting pairs, union max <= LIM
LIM=60
sols=[]
count=0
intervals=[(a,b) for a in range(1,LIM+1) for b in range(a,LIM+1)]
for i,(a,b) in enumerate(intervals):
    for (c,d) in intervals:
        # unordered / ordered doesn't matter for existence; enforce (a,b)<=(c,d) lexicographically to avoid dup
        if (c,d)<(a,b): continue
        if max(a,c)<=min(b,d): # intersect
            count+=1
            if (H(a,b)+H(c,d)).denominator==1:
                sols.append(((a,b),(c,d),int(H(a,b)+H(c,d))))
print(f"brute intersecting unordered pairs with endpoints <= {LIM}: checked {count}, integer-sum solutions: {sols}")

# 2) Test claimed simple lemma: odd prime dividing exactly one denominator in [r,s], for r<s, s>=3
fails=[]
examples={}
for r in range(1,301):
    for s in range(r+1,301):
        if s<3: continue
        found=[]
        # primes up to s (a prime divisor of a number <=s is <=s)
        for p in primes_upto(s):
            if p==2: continue
            cnt=sum(1 for n in range(r,s+1) if n%p==0)
            if cnt==1:
                found.append(p)
        if not found:
            fails.append((r,s))
        elif (r,s) in [(8,10),(14,16),(24,26),(114,126),(1,3),(2,3)]:
            examples[(r,s)]=found[:5]
print(f"lemma odd prime dividing exactly one denominator: fails for r<s<=300, s>=3: {fails[:10]} (count {len(fails)})")
print("examples:", examples)

# 3) Test my case split witnesses
def bertrand_prime_in_half(s):
    # prime p with s/2 < p <= s, if exists
    ps=[p for p in primes_upto(s) if p*2>s]
    return ps

case_fails=[]
for r in range(1,501):
    for s in range(r+1,501):
        if s<3: continue
        L=s-r; k=L+1
        if 2*r <= s+1:
            ps=bertrand_prime_in_half(s)
            if not ps or ps[0]<r:
                case_fails.append(('case1',r,s,ps))
        else:
            # Sylvester: prime divisor > k of product r..s, dividing exactly one term
            facs={}
            for n in range(r,s+1):
                for p in prime_factors(n):
                    facs[p]=facs.get(p,0)+1 # number of terms divisible (not exponent)
            good=[p for p,cnt in facs.items() if p>k and cnt==1]
            if not good:
                case_fails.append(('case2',r,s,facs))
print(f"case-split witnesses (Bertrand case1 / Sylvester case2): fails up to 500: {case_fails[:10]} (count {len(case_fails)})")

# 4) Direct Sylvester product statement check: k consecutive integers, all > k => prime divisor > k
sylv_fails=[]
for k in range(2,60):
    for start in range(k+1,300):
        nums=list(range(start,start+k))
        ps=set()
        for n in nums:
            ps.update(prime_factors(n).keys())
        if not any(p>k for p in ps):
            sylv_fails.append((k,start))
print(f"Sylvester product check k<60, start<300, start>k: fails {sylv_fails[:10]} (count {len(sylv_fails)})")

# 5) The four claimed pairs
for I,J in [((1,1),(1,1)),((1,2),(1,2)),((1,2),(2,2)),((2,2),(2,2))]:
    print(I,J, H(*I)+H(*J))
# near misses in [1,2] union
for I,J in [((1,1),(1,2)),((1,1),(1,1)),((2,2),(1,2))]:
    print("check",I,J,H(*I)+H(*J))
