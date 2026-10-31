from fractions import Fraction
from math import isqrt

def spf_upto(N):
    spf=list(range(N+1))
    for i in range(2,isqrt(N)+1):
        if spf[i]==i:
            for j in range(i*i,N+1,i):
                if spf[j]==j: spf[j]=i
    return spf

def prime_divisors(n,spf):
    out=set()
    while n>1:
        p=spf[n]; out.add(p)
        while n%p==0: n//=p
    return out

N=600
spf=spf_upto(N)
primes=[i for i in range(2,N+1) if spf[i]==i]
pdiv={n: prime_divisors(n,spf) for n in range(1,N+1)}

# Brute force exact rational check, LIM=36, precomputed interval sums
LIM=36
H={}
for a in range(1,LIM+1):
    s=Fraction(0)
    for b in range(a,LIM+1):
        s+=Fraction(1,b); H[(a,b)]=s
intervals=list(H.keys())
sols=[]; cnt=0
for ii,(a,b) in enumerate(intervals):
    for (c,d) in intervals[ii:]:
        if max(a,c)<=min(b,d):
            cnt+=1
            v=H[(a,b)]+H[(c,d)]
            if v.denominator==1:
                sols.append(((a,b),(c,d),int(v)))
print(f"BRUTE LIM={LIM}: intersecting unordered pairs checked={cnt}, solutions={sols}")

# Odd prime dividing exactly one denominator in [r,s], r<s<=500, s>=3
fails=[]
for r in range(1,501):
    for s in range(r+1,501):
        if s<3: continue
        found=False
        for p in primes:
            if p==2: continue
            if p>s: break
            if sum(1 for n in range(r,s+1) if n%p==0)==1:
                found=True; break
        if not found: fails.append((r,s))
print(f"LEMMA odd-prime-exactly-one-denominator r<s<=500,s>=3: fails={fails} count={len(fails)}")

# My case split witnesses up to 500
case_fails=[]
for r in range(1,501):
    for s in range(r+1,501):
        if s<3: continue
        k=s-r+1
        if 2*r<=s+1:
            ps=[p for p in primes if p<=s and 2*p>s]
            if not ps or min(ps)<r: case_fails.append(('A',r,s))
        else:
            cntdiv={}
            for n in range(r,s+1):
                for p in pdiv[n]: cntdiv[p]=cntdiv.get(p,0)+1
            if not any(p>k and c==1 for p,c in cntdiv.items()):
                case_fails.append(('B',r,s))
print(f"CASE-SPLIT witnesses up to 500: fails={case_fails} count={len(case_fails)}")

# Nayak's three-way split witnesses up to 500
note_fails=[]
for r in range(1,501):
    for s in range(r+1,501):
        if s<3: continue
        Nn=s-r+1
        ok=False
        if r<=s/2:
            ok=any(2*p>s and p<=s for p in primes) or s in (3,4)
            # prime 3 check for s=3,4
            if s in (3,4): ok=(sum(1 for n in range(r,s+1) if n%3==0)==1)
        elif r>Nn:
            cntdiv={}
            for n in range(r,s+1):
                for p in pdiv[n]: cntdiv[p]=cntdiv.get(p,0)+1
            ok=any(p>Nn and c==1 for p,c in cntdiv.items())
        else:
            ok=(s==2*r-1) and any(r<p<2*r for p in primes)
        if not ok: note_fails.append((r,s))
print(f"NAYAK-SPLIT witnesses up to 500: fails={note_fails} count={len(note_fails)}")

# Sylvester product statement: k consecutive ints all > k have prime divisor > k
sylv_fails=[]
for k in range(2,80):
    for start in range(k+1,400):
        ps=set()
        for n in range(start,start+k): ps|=pdiv[n] if n<=N else set()
        if not any(p>k for p in ps): sylv_fails.append((k,start))
print(f"SYLVESTER check k<80,start<400,start>k (terms<=478): fails count={len(sylv_fails)} {sylv_fails[:5]}")

# Four pairs and the excluded [1,2]-union pair
for I,J in [((1,1),(1,1)),((1,2),(1,2)),((1,2),(2,2)),((2,2),(2,2)),((1,1),(1,2))]:
    def HH(I): return sum(Fraction(1,n) for n in range(I[0],I[1]+1))
    print("PAIR",I,J,HH(I)+HH(J))
