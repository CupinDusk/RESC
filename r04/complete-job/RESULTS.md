# Complete per-ranking job costs (local CPU)

One specified synthetic Boolean auditor, common preloaded inputs/scratch, parsing/validation/output I/O excluded equally. Not certificate-service timing, H20 outward audit or GPU/application speedup.

All 870 plans and 41,760 exact decisions retained. Exactly one warmup and nine frozen paired blocks; all 5,508 records and their output hashes audited. No timing rerun.

| All720 six-arm census, queries/job | Raw direct | Closed direct | Cheap | Quartet | Quartet faster/slower than Cheap |
|---:|---:|---:|---:|---:|---:|
| 1 | 283.1 [272.4,353.9] | 671.8 [651.9,820.0] | 514.4 [440.8,798.9] | 579.2 [540.1,782.8] | 2/7 |
| 48 | 9159.2 [8996.1,9406.2] | 9464.9 [9233.8,10928.3] | 2810.3 [2607.4,3126.9] | 2831.5 [2764.9,2941.8] | 4/5 |
| 192 | 31705.7 [31251.2,32259.4] | 30830.4 [30500.4,31381.2] | 8131.0 [8066.5,8232.1] | 8158.9 [7954.4,8329.2] | 3/5 |

Ranges are descriptive min/max of paired blocks, not confidence intervals. Scaling strata are retained separately in RESULTS.json, without frequency/prevalence inference.
