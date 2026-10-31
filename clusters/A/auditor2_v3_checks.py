from fractions import Fraction
from math import isqrt
from bisect import bisect_left, bisect_right
import time
t0=time.time()

def spf_upto(N):
    spf=list(range(N+1))
    for i in range(2,isqrt(N)+1):
        if spf[i]==i:
            for j in range(i*i,N+1,i):
                if spf[j]==j: spf[j]=i
    return spf

N=600
spf=spf_upto(N)
primes=[i for i in range(2,N+1) if spf[i]==i]
def pdivs(n):
    out=set()
    while n>1:
        p=spf[n]; out.add(p)
        while n%p==0: n//=p
    return out
PDIV=[set()]+[pdivs(n) for n in range(1,N+1)]

# --- Brute force exact rational, LIM=28, via prefix harmonic fractions
LIM=28
pref=[Fraction(0)]
for n in range(1,LIM+1): pref.append(pref[-1]+Fraction(1,n))
def HH(a,b): return pref[b]-pref[a-1]
intervals=[(a,b) for a in range(1,LIM+1) for b in range(a,LIM+1)]
sols=[]; cnt=0
for ii,(a,b) in enumerate(intervals):
    Hab=HH(a,b)
    for (c,d) in intervals[ii:]:
        if max(a,c)<=min(b,d):
            cnt+=1
            v=Hab+HH(c,d)
            if v.denominator==1: sols.append(((a,b),(c,d),int(v)))
print(f"[{time.time()-t0:.1f}s] BRUTE LIM={LIM}: intersecting unordered pairs checked={cnt}, solutions={sols}", flush=True)

# --- Lemma: odd prime dividing exactly one denominator, r<s<=200, using divisor unions + O(1) counts
def mult_count(r,s,p): return s//p-(r-1)//p
fails=[]
for r in range(1,201):
    for s in range(r+1,201):
        if s<3: continue
        cand=set()
        for n in range(r,s+1): cand|=PDIV[n]
        if not any(p!=2 and mult_count(r,s,p)==1 for p in cand):
            fails.append((r,s))
print(f"[{time.time()-t0:.1f}s] LEMMA odd-prime-exactly-one r<s<=200,s>=3: fails={fails} count={len(fails)}", flush=True)

# --- My case split, up to 500
case_fails=[]
for s in range(3,501):
    ps_half=[p for p in primes if p<=s and 2*p>s]
    for r in range(1,s):
        k=s-r+1
        if 2*r<=s+1:
            if not ps_half or ps_half[0]<r: case_fails.append(('A',r,s))
        else:
            cntdiv={}
            for n in range(r,s+1):
                for p in PDIV[n]: cntdiv[p]=cntdiv.get(p,0)+1
            if not any(p>k and c==1 for p,c in cntdiv.items()): case_fails.append(('B',r,s))
print(f"[{time.time()-t0:.1f}s] MY-CASE-SPLIT up to 500: fails={case_fails} count={len(case_fails)}", flush=True)

# --- Nayak three-way split, up to 500
note_fails=[]
for s in range(3,501):
    for r in range(1,s):
        Nn=s-r+1; ok=False
        if r<=s/2:
            if s in (3,4): ok=(mult_count(r,s,3)==1)
            else: ok=any(2*p>s and p<=s and r<=p for p in primes)
        elif r>Nn:
            cntdiv={}
            for n in range(r,s+1):
                for p in PDIV[n]: cntdiv[p]=cntdiv.get(p,0)+1
            ok=any(p>Nn and c==1 for p,c in cntdiv.items())
        else:
            ok=(s==2*r-1) and any(r<p<2*r for p in primes)
        if not ok: note_fails.append((r,s))
print(f"[{time.time()-t0:.1f}s] NAYAK-SPLIT up to 500: fails={note_fails} count={len(note_fails)}", flush=True)

# --- Sylvester product statement
sylv_fails=[]
for k in range(2,50):
    for start in range(k+1,200):
        ps=set()
        for n in range(start,start+k): ps|=PDIV[n]
        if not any(p>k for p in ps): sylv_fails.append((k,start))
print(f"[{time.time()-t0:.1f}s] SYLVESTER k<50,start in (k,200): fails count={len(sylv_fails)} {sylv_fails[:5]}", flush=True)

for I,J in [((1,1),(1,1)),((1,2),(1,2)),((1,2),(2,2)),((2,2),(2,2)),((1,1),(1,2))]:
    print("PAIR",I,J, HH(*I)+HH(*J), flush=True)
print(f"total {time.time()-t0:.1f}s")
