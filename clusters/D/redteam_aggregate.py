#!/usr/bin/env python3
"""Aggregate all redteam_checkpoint_*.json into redteam_data.json and
print a Markdown table (b, eps, N, counts per filter, margins)."""
import glob, json, math, os

def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = b"\x00" * (((n - i*i)//i) + 1)
    return [i for i, v in enumerate(sieve) if v]

def tau_Bb(b, eps):
    zb = b / ((1 - eps) * math.log(b))
    tau = 1
    for p in primes_upto(b):
        if p <= zb:
            e, q = 0, 1
            while q * p <= b:
                q *= p; e += 1
            tau *= (e + 1)
    return tau

here = os.path.dirname(os.path.abspath(__file__))
rows = []
for path in sorted(glob.glob(os.path.join(here, "redteam_checkpoint_*.json"))):
    d = json.load(open(path))
    c = d["counts"]
    best = d["best_directed"]
    rows.append(dict(
        b=d["b"], eps=d["eps"], zb=d["zb"], N=d["N"],
        half_log_Ptot=d["half_log_Ptot"], log_Bb=d["log_Bb"],
        directed=c["directed_total"], f1=c["f1_balance"], f2=c["f2_size"],
        f3=c["f3_smooth"], f4=c["f4_lambda"], f5=c["f5_interval"],
        best_log_max_u=best["log_max_u"] if best else None,
        margin_best_minus_logBb=(best["log_max_u"] - d["log_Bb"]) if best else None,
        elapsed=d["elapsed_sec"], file=os.path.basename(path),
        tau_Bb=tau_Bb(d["b"], d["eps"]),
        final_survivors=d.get("final_survivors", []),
    ))
rows.sort(key=lambda r: (r["eps"], r["b"]))
with open(os.path.join(here, "redteam_data.json"), "w") as f:
    json.dump(rows, f, indent=1)
print("| b | eps | zb | N | S/2 | log Bb | directed | F1 | F2 | F3 | F4 | F5 | min log max(u) | margin vs log Bb |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['b']} | {r['eps']} | {r['zb']:.1f} | {r['N']} | {r['half_log_Ptot']:.1f} | "
          f"{r['log_Bb']:.1f} | {r['directed']} | {r['f1']} | {r['f2']} | {r['f3']} | {r['f4']} | {r['f5']} | "
          f"{r['best_log_max_u']:.2f} | {r['margin_best_minus_logBb']:+.2f} |")
