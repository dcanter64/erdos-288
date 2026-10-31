import math, itertools, json
# independent prime generation by trial division
def primes_trial(n):
    out=[]
    for x in range(2,n+1):
        ok=True
        for d in range(2,int(x**0.5)+1):
            if x%d==0: ok=False; break
        if ok: out.append(x)
    return out
def count_F1(b,eps):
    ps=primes_trial(b); zb=b/((1-eps)*math.log(b)); large=[p for p in ps if p>zb]
    logBb=0.0
    for p in ps:
        if p<=zb:
            e=0;q=1
            while q*p<=b: q*=p;e+=1
            logBb+=e*math.log(p)
    logs=[math.log(p) for p in large]; S=sum(logs); N=len(large)
    tau=(logBb+1)/2; target=S/2
    n1=N//2
    A=[sum(c) for r in range(n1+1) for c in itertools.combinations(logs[:n1],r)]
    B=sorted(sum(c) for r in range(N-n1+1) for c in itertools.combinations(logs[n1:],r))
    import bisect
    cnt=0
    for a in A:
        lo=bisect.bisect_left(B, target-tau-a); hi=bisect.bisect_right(B, target+tau-a)
        cnt+=hi-lo
    return dict(b=b,eps=eps,N=N,half_S=S/2,logBb=logBb,directed_total=2**N,f1_directed=cnt)
for b,eps in [(200,0.25),(250,0.5),(250,0.25),(300,0.5),(300,0.25)]:
    print(json.dumps(count_F1(b,eps)))
