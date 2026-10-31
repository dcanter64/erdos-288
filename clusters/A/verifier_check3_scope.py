#!/usr/bin/env python3
"""Verifier: Lemma 3.1 predicate, scope-explicit rerun (exact integer arithmetic).
For all 1<=r<s<=500, find odd prime dividing exactly one integer in [r,s].
Reports failures split by the lemma's hypothesis s>=3 vs s<3."""
import json
def primes_upto(N):
    sieve=[True]*(N+1); sieve[0:2]=[False,False]
    for i in range(2,int(N**0.5)+1):
        if sieve[i]: sieve[i*i::i]=[False]*len(sieve[i*i::i])
    return [i for i,v in enumerate(sieve) if v and i%2==1]
OP=primes_upto(500)
fail=[]; tested=0
for r in range(1,500):
    for s in range(r+1,501):
        tested+=1
        ok=False
        for p in OP:
            if p>s: break
            if sum(1 for n in range(r,s+1) if n%p==0)==1:
                ok=True; break
        if not ok: fail.append((r,s))
in_scope=[x for x in fail if x[1]>=3]
out_scope=[x for x in fail if x[1]<3]
print(json.dumps({"tested":tested,"failures":fail,"failures_s_ge_3":in_scope,
                  "failures_s_lt_3":out_scope}, indent=2))
assert in_scope==[] and out_scope==[(1,2)]
print("LEMMA 3.1 PREDICATE: holds for all r<s<=500 with s>=3; sole exception (1,2) is out of scope (s=2).")
