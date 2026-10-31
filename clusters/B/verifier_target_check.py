#!/usr/bin/env python3
"""Verifier supplementary check (for TARGET.md remarks):
intervals b<=300 with P1 nonempty whose den H(a,b) lies in the forced
CRT class. Lemma 2 gives necessary conditions only, so non-solution
intervals may also have den in the class; count them exactly."""
from fractions import Fraction
from math import isqrt

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,isqrt(n)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i,v in enumerate(s) if v]

PRIMES=primes_upto(300)
H=[Fraction(0,1)]; s=Fraction(0,1)
for n in range(1,301):
    s+=Fraction(1,n); H.append(s)

def Tp(a,b,p):
    u=-(-a//p); k=0; tot=0; j=0
    while p*(u+j)<=b:
        tot=(tot+pow(u+j,-1,p))%p; k+=1; j+=1
    return (k,u,tot) if k else None

def sieve(a,b):
    congr=[]
    for p in PRIMES:
        if p==2 or p*p<=b: continue
        t=Tp(a,b,p)
        if t is None: continue
        k,u,tm=t
        if tm!=0: congr.append(((-p*pow(tm,-1,p))%(p*p),p*p))
    r=0; M=1
    for rp,mod in congr:
        r=r+M*(((rp-r)*pow(M%mod,-1,mod))%mod); M*=mod; r%=M
    return M,r

sol=[]; nonsol=[]
for b in range(1,301):
    for a in range(1,b+1):
        f=H[b]-H[a-1]; A,B=f.numerator,f.denominator
        Q,r=sieve(a,b)
        if Q>1 and B%Q==r%Q:
            ((sol if (A+1)%B==0 else nonsol)).append((a,b,B))
print("den in forced class, P1 nonempty, b<=300:")
print("solution intervals:",sol)
print("non-solution intervals:",len(nonsol))
print("non-solution list:",nonsol)
print("powers-of-two family present:",[x for x in nonsol if x[0] in (4,16,32,64,128,256) and x[1]==x[0]+1])
