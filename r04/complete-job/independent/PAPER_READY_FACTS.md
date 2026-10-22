# Independently checked complete CPU job costs

Author-side validation, not a simulated peer review. No timing was rerun. All 870 fixed plans and 41,760 distinct decisions were preserved; all 153 expected batch hashes and 5,508 recorded measurements were independently reconstructed. A separately written checker validated raw and closed graphs with exact Floyd and BF certificates on every query, including all 870 quartet classifications. Fresh original-source validation reproduced both CSV outputs byte for byte.

## All 720 six-arm total orders

Costs are block-average ns per complete job, median [min, max] over nine paired blocks; each interval is divided by its repeats and number of plans, rather than timing individual jobs. Each job includes fresh route-specific ranking preparation, Boolean query evaluation and rolling decision-hash construction; expected-hash checking and the outer volatile update occur after the elapsed interval. The common immutable boxes/query arrays and scratch capacity are preloaded.

| Queries/job | Raw original-edge BF | Closure + BF | Cheap | Quartet | Quartet vs cheap: faster/slower/tie |
|---:|---:|---:|---:|---:|---:|
| 1 | 283.1 [272.4, 353.9] | 671.8 [651.9, 820.0] | 514.4 [440.8, 798.9] | 579.2 [540.1, 782.8] | 2/7/0 |
| 48 | 9159.2 [8996.1, 9406.2] | 9464.9 [9233.8, 10928.3] | 2810.3 [2607.4, 3126.9] | 2831.5 [2764.9, 2941.8] | 4/5/0 |
| 192 | 31705.7 [31251.2, 32259.4] | 30830.4 [30500.4, 31381.2] | 8131.0 [8066.5, 8232.1] | 8158.9 [7954.4, 8329.2] | 3/5/1 |

At the primary Q=48 setting, cheap and quartet median block-average complete-job costs are 0.307 and 0.309 times raw-direct cost (raw/cheap 3.259, raw/quartet 3.235). The quartet median is 0.76% higher than cheap and wins only 4 of 9 paired blocks; their observed ranges overlap. These are local descriptive comparisons, not estimated application speedups.

At Q=1, cheap and quartet each lose to raw-direct in all nine paired blocks. Setup is not amortized at this reuse level. Per-query figures in the JSON are batch-derived equivalents, not directly measured individual request latencies.

## Scaling evidence and limits

The 50 original scaling strata remain separate in Q48_STRATA.csv and INDEPENDENT_AUDIT.json: n=4,8,16,32,64; contiguous/sparse positions; aligned, reverse, winner_star, mixed_total and sparse_dag families. Each stratum contains only three fixed plans. No cross-stratum pooling or population/prevalence inference is supported. Repeated jobs and timing blocks increase measurement repetition, not independent input count. Q192 repeats the same 48 queries four times.

Raw-direct avoids closure entirely. Closure-direct pays fresh closure then uses the same dense BF. Cheap pays closure and its structural flags; quartet pays those and classifies only when cheap is false, stopping on the first obstruction. Each job copies positions and original edges, while box/query arrays are shared immutable inputs. All graph entries and BF state are reset on use; Scratch vector capacity is shared across jobs after common warmup.

Scaling effects go both ways. At Q48, n=32 contiguous sparse_dag has cheap/quartet medians 61,093.3/72,273.3 ns, with quartet losing 8 of 9 paired blocks; n=32 sparse-position sparse_dag has 84,480.0/96,046.7 ns and quartet loses all nine. The complete per-stratum data, rather than selected examples, bounds any scaling claim.

The preserved original RESULTS table omits an explicit Q192 tie. Use 3 faster / 5 slower / 1 tie, with denominator nine. Original source, timings and summaries were not overwritten.

The fresh executable has byte-identical code/data and all other bytes outside the COFF timestamp and .buildid section; only those 20 bytes differ. This supports saved executable/source binding without claiming whole-file deterministic rebuild identity.

This evidence covers one exact-integer synthetic CPU Boolean auditor on one Windows host. It does not measure GPU/native execution, H20 outward auditing, certificate-serving service latency, application throughput or a universally optimal implementation. Min/max are descriptive ranges, not confidence intervals. Hash bindings verify the saved files and ordering; this author-side audit did not observe the historical measurement process or independently certify trusted predeclaration timestamps.
