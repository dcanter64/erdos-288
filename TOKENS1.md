# Erdős #288, Cycle 1: Token Ledger (TOKENS1.md)

Measured ledger, extracted 2026-10-30 after all 26 child agent runs
had completed, from the runtime's per-run token records
(`agent.agent_message_token_usage`, one attributed row per agent run,
summed per agent). The separate `agent.token_usage` table is empty in
this deployment, so it could not be used. Figures below are actuals
from those records, not estimates.

Accounting basis, stated plainly: "input" is the attributed input
token count, which includes cached context carried into each run, so
input figures are much larger than the new text each agent read;
"output" is the attributed output token count. Design estimates for
this cycle were 3 to 5 million tokens total (CYCLE1_DESIGN.md, from
the #699 calibration); the measured total is far above that estimate,
driven almost entirely by attributed input (cached context) rather
than output. The coordinator row is counted through the coordinator
message current at extraction; the small additional coordinator cost
of writing CYCLE1.md and this file after extraction is not in the
table.

## Per-agent ledger

| Role | Agent (short id) | Input | Output |
|---|---|---:|---:|
| Coordinator | 931aa956 | 12,164,597 | 57,968 |
| A, Auditor 1 | dd720b81 | 352,343 | 15,930 |
| A, Auditor 2 | 84970e1a | 1,029,583 | 29,125 |
| A, Red Team | 2f3c5738 | 4,714,072 | 57,913 |
| A, Verifier | 91db184c | 1,123,626 | 12,919 |
| B, Auditor 1 | f2729c0e | 1,498,197 | 30,844 |
| B, Auditor 2 | 89531e13 | 1,284,928 | 33,806 |
| B, Verifier | 051a3281 | 1,979,228 | 47,294 |
| C0, Implementation 1 | 7f0e366b | 1,687,733 | 23,505 |
| C0, Implementation 2 | c1a0a6fe | 3,100,953 | 75,044 |
| C0, Verifier | 32fe619a | 1,487,025 | 17,346 |
| C1, Implementation A | 1c6ace7f | 2,016,243 | 51,766 |
| C1, Implementation B | fdff87b0 | 7,477,061 | 12,843 |
| C1, Verifier | 452fac3a | 4,740,183 | 50,065 |
| D, Prover 1 | 287d5687 | 1,180,480 | 38,242 |
| D, Prover 2 | 78a0bdf0 | 1,118,974 | 27,064 |
| D, Red Team | ebdca759 | 4,024,503 | 20,016 |
| D, Verifier | a6f1bf3e | 2,261,476 | 49,584 |
| E, Prover 1 | 990f55e9 | 1,284,983 | 55,794 |
| E, Prover 2 | 402afbce | 1,941,380 | 67,363 |
| E, Red Team | a84e4e32 | 3,800,387 | 50,388 |
| E, Verifier | 6656eaf1 | 1,702,323 | 26,684 |
| F, GAPS author | 250868d4 | 1,507,629 | 21,241 |
| F, GAPS final-status update | b32dde96 | 3,502,903 | 16,116 |
| Repair, AUDIT-A completion | 310d745b | 535,274 | 8,123 |
| Repair, CENSUS0 completion | 3a112e89 | 859,323 | 8,766 |
| Repair, E Prover 1 completion | f42f9944 | 2,770,550 | 30,014 |

## Totals

| Scope | Input | Output | Total |
|---|---:|---:|---:|
| 26 child agents | 58,981,360 | 877,795 | 59,859,155 |
| Coordinator | 12,164,597 | 57,968 | 12,222,565 |
| **Cycle 1 total** | **71,145,957** | **935,763** | **72,081,720** |

27 agent runs in total (26 children plus the coordinator), against a
design budget of about 18 runs plus coordination; the three repair
runs and the second Cluster F run account for most of the overage in
run count.

Nothing was posted, emailed, or submitted anywhere.
