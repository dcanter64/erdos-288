#!/usr/bin/env python3
"""Cluster B VERIFIER independent checks for Zeraoulia's singleton note.
Exact arithmetic only (Fractions and F_p modular arithmetic).
Written from the STATEMENTS in the note, before reading the auditors.
"""
from fractions import Fraction
from math import gcd, log, isqrt
import sys

def primes_upto(n):
    sieve = [True]*(n+1)
    sieve[0]=sieve[1]=False
    for i in range(2,isqrt(n)+1):
        if sieve[i]:
            for j in range(i*i,n+1,i): sieve[j]=False
    return [i for i,v in enumerate(sieve) if v]

BMAX=300
PRIMES=primes_upto(BMAX)
PRIMESET=set(PRIMES)

# prefix harmonic numbers, exact
H=[Fraction(0,1)]
s=Fraction(0,1)
for n in range(1,BMAX+1):
    s+=Fraction(1,n); H.append(s)
def Hab(a,b): return H[b]-H[a-1]

def vp_int(n,p):
    if n==0: return None
    e=0
    while n%p==0: n//=p; e+=1
    return e

def lcm_range(a,b):
    l=1
    for n in range(a,b+1): l=l*n//gcd(l,n)
    return l

def Tp_modp(a,b,p):
    """Return (k, u, Tp mod p) with Tp = sum 1/(u+j) in F_p, or None if k=0."""
    u=-(-a//p)  # ceil(a/p)
    k=0
    tot=0
    j=0
    while p*(u+j)<=b:
        tot=(tot+pow(u+j,-1,p))%p
        k+=1; j+=1
    if k==0: return None
    return k,u,tot

def sieve_data(a,b):
    """Return (P1 list, Q, r) : good odd primes, CRT modulus and residue (r in [0,Q))."""
    P1=[]; congr=[]
    for p in PRIMES:
        if p==2: continue
        if p*p<=b: continue
        t=Tp_modp(a,b,p)
        if t is None: continue
        k,u,tm=t
        if tm!=0:
            P1.append(p)
            rp=(-p*pow(tm,-1,p))%(p*p)
            congr.append((rp,p*p))
    Q=1
    for p in P1: Q*=p*p
    # CRT
    r=0
    for rp,mod in congr:
        # solve r + Q_partial ... do iterative CRT
        pass
    # iterative CRT properly:
    r=0; M=1
    for rp,mod in congr:
        # find t: r + M*t = rp (mod mod)
        inv=pow(M%mod,-1,mod)
        t=((rp-r)*inv)%mod
        r=r+M*t; M*=mod; r%=M
    return P1,Q,r

out=[]
def P(*args):
    line=" ".join(str(x) for x in args)
    out.append(line); print(line); sys.stdout.flush()

# ---------- V1: Lemma 1 denominator forcing, exhaustive b<=300 ----------
# For each interval, find ALL m>=1 with H+1/m integer by enumerating k=H+1/m in Z:
# 1/m = k - A/B = (kB-A)/B  =>  need kB-A > 0 dividing B, m = B/(kB-A).
fails=0; sols=[]
for b in range(1,BMAX+1):
    for a in range(1,b+1):
        f=Hab(a,b); A,Be=f.numerator,f.denominator
        found=[]
        k=1
        while Fraction(k,1) <= f+1:  # 1/m <=1 so k <= H+1 ; k>=1 since H>0 (<= : k=H+1 occurs at (1,1), m=1)
            d=k*Be-A
            if d>0 and Be%d==0:
                found.append(Be//d)
            k+=1
        # also k could equal ceil? loop condition k < f+1 covers k <= floor(f+... ) since 1/m>0 => k>H, and 1/m<=1 => k<=H+1
        for m in found:
            if m!=Be or (A+1)%Be!=0:
                fails+=1; P("V1 FAIL",a,b,m,Be)
            else:
                sols.append((a,b,m))
        # equivalence: solution exists iff A = -1 mod B
        if ((A+1)%Be==0) != (len(found)>0):
            fails+=1; P("V1 EQUIV FAIL",a,b)
P("V1 Lemma1: intervals checked", BMAX*(BMAX+1)//2, "failures", fails)
P("V1 solutions b<=300:", sols)

# ---------- V2: Lemma 2 dichotomy, b<=300 ----------
failsA=0; failsB=0; nA=0; nB=0; congfails=0
for b in range(1,BMAX+1):
    for a in range(1,b+1):
        f=Hab(a,b); den=f.denominator
        for p in PRIMES:
            if p==2 or p*p<=b: continue
            t=Tp_modp(a,b,p)
            if t is None: continue
            k,u,tm=t
            v=vp_int(den,p)
            if tm!=0:
                nA+=1
                if v!=1:
                    failsA+=1
                    if failsA<=5: P("V2a FAIL v_p",a,b,p,"vp=",v)
                # NOTE: congruence (4) is conditional on (1) holding; it is NOT
                # claimed for den of a non-solution interval. Checked properly in V2c/V9.
                pass
            else:
                nB+=1
                if v!=0:
                    failsB+=1
                    if failsB<=5: P("V2b FAIL",a,b,p,"vp=",v)
P("V2 Lemma2: case(a) incidences",nA,"vp failures",failsA,"(congruence checked conditionally in V2c/V9)")
P("V2 Lemma2: case(b) incidences",nB,"vp failures",failsB)

# ---------- V3: worked examples ----------
f23=Hab(2,3); P("V3 H(2,3) =",f23)
P("V3 (2,3) sieve:",sieve_data(2,3), "lcm",lcm_range(2,3))
f36=Hab(3,6); P("V3 H(3,6) =",f36, " (note prints 49/20 per ResearchGate text layer)")
P("V3 (3,6) sieve:",sieve_data(3,6), "lcm",lcm_range(3,6))
P("V3 H(3,6)+1/20 =",f36+Fraction(1,20))

# ---------- V4: bad-prime classifications u=1; Lemma 5; Corollary 6 ----------
def Tu_k(u,k): return sum((Fraction(1,u+j) for j in range(k)),Fraction(0,1))
for k in (1,2,3):
    t=Tu_k(1,k)
    bad=[p for p in PRIMES if p>1+k-1 and t.numerator%p==0]
    P(f"V4 u=1 k={k}: T={t} numerator={t.numerator} bad primes (p<=300, p>u+k-1):",bad)
# Lemma 5 root counts: for primes p<=199, all 1<=k<p, count u in F_p, D(u)!=0, D'(u)=0
l5fail=0; l5max={}
for p in [q for q in PRIMES if q<=199 and q!=2]:
    for k in range(1,p):
        cnt=0
        for u in range(p):
            terms=[(u+j)%p for j in range(k)]
            if 0 in terms: continue
            if sum(pow(x,-1,p) for x in terms)%p==0: cnt+=1
        if cnt>k-1: l5fail+=1; P("V5 FAIL",p,k,cnt)
        l5max[k]=max(l5max.get(k,0),cnt)
P("V4 Lemma5: root-count failures (p<=199, all k<p):",l5fail,"max roots for k=2,3,4,5:",[l5max.get(k) for k in (2,3,4,5)])
# Corollary 6 grid: (u,k) small; bad primes p>u+k-1 must divide numerator, and conversely
c6fail=0
for u in range(1,9):
    for k in range(1,7):
        t=Tu_k(u,k); N=t.numerator
        for p in PRIMES:
            if p<=u+k-1 or p>300: continue
            bad = (sum(pow(u+j,-1,p) for j in range(k))%p==0)
            if bad != (N%p==0): c6fail+=1; P("C6 FAIL",u,k,p)
P("V4 Corollary6 grid failures:",c6fail)

# ---------- V5: Theorem 13 (q^2,q^2) family ----------
for q in [2,3,5,7,11,13,17,19,23,29,31]:
    a=b=q*q
    P1,Q,r=sieve_data(a,b)
    L=lcm_range(a,b)
    m=q*q
    smooth=all((pp<=b) for pp in PRIMESET if m%pp==0)
    hden=q*q; hnum=1  # H(q^2,q^2) = 1/q^2 exactly
    P(f"V5 q={q} (a,b)=({a},{b}): P1={P1} Q={Q} r={r} lcm={L} m=q^2={m} b-smooth={smooth} m<=lcm={m<=L} m in class (mod Q)={ (m-r)%Q==0 if Q>0 else None } H den={hden} A={hnum} A==-1 mod B? {(hnum+1)%hden==0}")
# also m=1 in class when Q=1
P("V5 note: when Q=1 the class mod 1 contains every positive integer, incl. m=1 and m=q^2.")

# ---------- V2c: Lemma 2(a) congruence in its correct conditional (p-local) form ----------
# Claim: if v_p(m)=1 and H(a,b)+1/m is p-integral (necessary for (1)), then
# m = -p * (T_p mod p)^{-1} (mod p^2). m mod p^2 is determined by t = m/p mod p.
# Exact check with Fractions, b<=60, all t in [1,p-1].
def vp_frac(fr,p):
    return vp_int(fr.numerator,p)-vp_int(fr.denominator,p)
l2c_fail=0; l2c_n=0; l2c_wit=0
for b in range(1,61):
    for a in range(1,b+1):
        f=Hab(a,b)
        for p in PRIMES:
            if p==2 or p*p<=b: continue
            t=Tp_modp(a,b,p)
            if t is None: continue
            k,u,tm=t
            if tm==0: continue
            pred=pow(-pow(tm,-1,p)%p,1,p)  # t must equal -T_p^{-1} mod p
            pred_t=(-pow(tm,-1,p))%p
            for tt in range(1,p):
                l2c_n+=1
                integral = vp_frac(f+Fraction(1,p*tt),p)>=0
                if integral != (tt==pred_t):
                    l2c_fail+=1
                    if l2c_fail<=5: P("V2c FAIL",a,b,p,tt,"integral",integral,"pred_t",pred_t)
                if integral: l2c_wit+=1
P("V2c Lemma2(a) p-local congruence: tests",l2c_n,"failures",l2c_fail,"p-integral witnesses",l2c_wit)

# ---------- V6: Proposition 10 bound at small b and in general ----------
def theta(x):
    return sum(log(p) for p in PRIMES if p<=x)
viol=[]
for b in range(2,301):
    rhs=2*(theta(b)-theta(b/2))
    for a in range(1,b+1):
        if a> b//2+1: continue
        P1,Q,r=sieve_data(a,b)
        if log(Q) < rhs-1e-9:
            viol.append((a,b,round(log(Q),4),round(rhs,4)))
P("V6 Prop10 logQ >= 2(theta(b)-theta(b/2)) violations (a<=floor(b/2)+1), count:",len(viol))
P("V6 violations with b<=6:",[v for v in viol if v[1]<=6][:20])
P("V6 distinct b with violations:",sorted(set(v[1] for v in viol)))
# odd-prime-only version of the bound
viol2=[]
for b in range(2,301):
    rhs=sum(2*log(p) for p in PRIMES if p!=2 and b/2<p<=b)
    for a in range(1,b+1):
        if a> b//2+1: continue
        P1,Q,r=sieve_data(a,b)
        if log(Q) < rhs-1e-9: viol2.append((a,b))
P("V6 Prop10 odd-prime product bound violations:",len(viol2))
# Proposition 8 divisibility, b>=10, a<=b/3
v8=0; n8=0
for b in range(10,301):
    need=[p for p in PRIMES if p!=3 and b/3<p<=b]
    for a in range(1,b+1):
        if a*3>b: continue
        n8+=1
        P1,Q,r=sieve_data(a,b)
        for p in need:
            if p not in P1: v8+=1; P("V8 FAIL",a,b,p) if v8<=5 else None
P("V6 Prop8: intervals checked",n8,"missing-prime failures",v8)

# ---------- V7: Remark 4 Mertens check ----------
def S(bound):
    pr=primes_upto(bound)
    return sum(1.0/p for p in pr if p*p>bound and p<=bound)
for bound in (100,1000,10000,100000,1000000):
    P(f"V7 b={bound}: sum_{{sqrt(b)<p<=b}} 1/p = {S(bound):.4f}  log2={log(2):.4f}  loglog b={log(log(bound)):.4f}")

# ---------- V8: log Q / b measurements ----------
maxr=0; argmax=None; a1={}
for b in range(4,301):
    for a in range(1,b+1):
        P1,Q,r=sieve_data(a,b)
        if Q>1:
            ratio=log(Q)/b
            if ratio>maxr: maxr=ratio; argmax=(a,b)
    P1,Q,r=sieve_data(1,b)
    a1[b]=log(Q)/b if Q>1 else 0.0
P("V8 max logQ/b over all a, 4<=b<=300:",round(maxr,4),"at (a,b)=",argmax)
P("V8 a=1: logQ/b at b=50,100,200,300:",[round(a1[x],4) for x in (50,100,200,300)])
P("V8 theoretical upper envelope 2(theta(b)-theta(sqrt(b)))/b at b=300:",round(2*(theta(300)-theta(300**0.5))/300,4))

# ---------- V9: CRT reduction + den | lcm, all b<=300 ----------
crtfail=0; divfail=0; nsol=0
for b in range(1,BMAX+1):
    for a in range(1,b+1):
        f=Hab(a,b); A,Be=f.numerator,f.denominator
        L=lcm_range(a,b)
        if L%Be!=0: divfail+=1
        if (A+1)%Be==0:
            nsol+=1
            P1,Q,r=sieve_data(a,b)
            if Q>0 and Be%Q!=r%Q and not (Q==1):
                crtfail+=1; P("V9 CRT FAIL",a,b,Be,Q,r)
            if Q==1 and Be%1!=0: crtfail+=1
P("V9 CRT: solutions checked",nsol,"CRT failures",crtfail,"den|lcm failures",divfail)

# ---------- V10: Remark 14 illustration ----------
P1,Q,r=sieve_data(2,3); L=lcm_range(2,3)
P("V10 (2,3): Q=",Q,"lcm=",L,"Q>lcm:",Q>L,"least positive residue r0=",r if r!=0 else Q,"r0<=lcm:",(r if r!=0 else Q)<=L)

with open("/home/hatch/workspace/math-hunt/erdos-288/clusters/B/verifier_output.txt","w") as fh:
    fh.write("\n".join(out)+"\n")
P("DONE")
