import math, numpy as np, json
def primes_upto(n):
    sieve=bytearray(b'\x01')*(n+1); sieve[0:2]=b'\x00\x00'
    for i in range(2,int(n**0.5)+1):
        if sieve[i]: sieve[i*i:n+1:i]=b'\x00'*(((n-i*i)//i)+1)
    return [i for i,v in enumerate(sieve) if v]
def count_F1(b,eps):
    ps_all=primes_upto(b); zb=b/((1-eps)*math.log(b)); large=[p for p in ps_all if p>zb]
    logBb=0.0
    for p in ps_all:
        if p<=zb:
            e=0;q=1
            while q*p<=b: q*=p; e+=1
            logBb+=e*math.log(p)
    logs=np.array([math.log(p) for p in large]); S=logs.sum(); N=len(large); n1=N//2
    def subs(arr):
        s=np.array([0.0])
        for x in arr: s=np.concatenate([s,s+x])
        return s
    A=subs(logs[:n1]); B=subs(logs[n1:]); B.sort()
    # directed subsets total 2^N; F1: |2*sum-S| <= logBb+1  <=> sum in [ (S-(logBb+1))/2 , (S+(logBb+1))/2 ]
    tau=(logBb+1)/2
    lo=np.searchsorted(B, S/2-tau-A); hi=np.searchsorted(B, S/2+tau-A, side='right')
    cnt=int((hi-lo).sum())
    return dict(b=b,eps=eps,zb=zb,N=N,half_S=S/2,logBb=logBb,directed_total=2**N,f1_directed=cnt)
for b,eps in [(200,0.25),(250,0.5),(250,0.25),(300,0.5),(300,0.25),(400,0.5)]:
    print(json.dumps(count_F1(b,eps)))
