# Independent author-side audit of the complete CPU job study

The saved study passes the independent correctness, source binding, batch hash, order and numerical-summary checks described below. One reporting correction is required: the all720 Q192 quartet-versus-cheap result is **3 faster / 5 slower / 1 tie**, out of nine paired blocks. The original RESULTS files are preserved. No timing was rerun. This is an author-side validation exercise, not a simulated review or external auditor endorsement.

## Evidence checked

`check_complete.py` reads all saved study inputs, protocol, manifest, pre-timing audit, run metadata, schedule, source, validations, expected batch sums, raw measurements, log and summaries. It checks every declared hash, copied R03 input byte, and original R03 decision. All original study files are hashed before and after; their bytes are unchanged. The check writes only within this independent directory.

All 870 plan IDs, all 51 strata and all 41,760 distinct plan/rectangle/budget queries are retained. JSON and native text input values and stream order agree exactly. Each plan has the complete Cartesian set of eight rectangles and budgets {0,1,2,4,16,64}, shuffled into the original fixed 48-query order. Each budget appears 6,960 times. There are 16,970 zero-width interval coordinates; these were retained. The six-arm stratum contains 720 distinct total orders, each with its full 15 original edges, so the complete 6! order census is present. The other 50 strata contain three fixed plans each.

The independent checker regenerates the seeded schedule (20261024), including every Q shuffle and every route shuffle, and checks its equality to both JSON and text forms. It verifies the prescribed repeats: census 1; n=4/8 100; n=16 20; n=32 5; n=64 2. Every one of the 5,508 raw rows is in its predeclared block, stratum, Q, route and position, with the correct repeat count and number of jobs. Every route/stratum/Q has exactly nine observations.

It independently reconstructs all per-job rolling hashes from the R03 decisions, then all 153 expected stratum/Q sums modulo 2^64, and every recorded repeated-batch checksum. It reconstructs every median/min/max, per-query normalization and paired comparison in the saved RESULTS.json. Exact rational elapsed/job values are used to establish win/loss/tie directions. All saved numerical summaries match; tie counts are added explicitly in the independent results.

The complete timing log contains all 27 census completion messages and the final steady-clock/checksum line. The raw elapsed sum is 38,317,789,000 ns, below the saved process wall interval 39,875,388,000 ns, consistent with warmup and I/O being outside intervals. The empirical greatest common divisor of raw intervals is 100 ns, and the shortest interval is 18,600 ns. The reported steady-clock period of 1/1,000,000,000 is a representation period, not evidence of 1 ns empirical resolution.

## Independent graph and classification validation

`independent_graph.cpp` does not include or copy the submitted core implementation. It constructs a separate explicit multigraph: each data inequality and each zero-weight reverse-ranking inequality is stored separately, instead of merging them into the original dense edge matrix. Ranking reachability is computed by per-source graph traversal, instead of the submitted Warshall closure.

For every query, it runs exact signed128 Floyd feasibility checks on both original-edge and closed-ranking graphs, and independently validates BF potentials or negative cycles on each graph. Its BF scans the separate edge list in reverse order, rather than the original dense row-major edge order. Both feasible potentials and rejecting cycle edges are checked against their actual graph inequalities. All four checks agree with each other and with the unchanged R03 and new validation decisions: **25,244 feasible and 16,516 infeasible** queries. The checker also independently enumerates unordered source pairs and disjoint target pairs, with both bijections, to classify all 870 plans; all expected quartet flags agree, with 138 quartet-exact plans.

The raw/closure equivalence has a direct constraint explanation. A ranking a→b contributes the difference bound h[a]≤h[b]. Every closed ranking edge follows a path of those zero-weight reverse edges and adds a redundant bound. Combining a data edge of weight w and a ranking edge of weight 0 as min(w,0), as the submitted graph does, preserves both inequalities. All original boxes have l≤u, so replacing the nonnegative diagonal data bound u[a]−l[a] by 0 also preserves feasibility. The maximum absolute box coordinate is 860 and maximum absolute slot is 190; all actual arithmetic is well within signed128, while quartet distance sums and original coordinate subtraction are also within int64.

Fresh copied original sources were built with the existing Zig 0.14.1 C++17 compiler and the recorded -O3 -DNDEBUG -Wall -Wextra flags, then invoked only with `validate`. Their validation.csv and expected_batches.csv are byte-identical to the saved study outputs. Both the original and independent compilers returned zero, with empty compiler diagnostic logs.

The complete rebuilt EXE hash differs from the saved EXE. Independent PE inspection resolves this: **only 20 bytes differ, all in the COFF timestamp field and .buildid section**. Every other executable byte matches, including all .text, .rdata, .data, .pdata, .tls and .reloc bytes. Thus this is a code/data-identical source rebuild, not a claim of whole-file deterministic binary identity. The source core is also reconstructed from the unchanged R03 source and agrees after only the two documented raw-edge graph edits. See PE_SOURCE_BINDING.json and NATIVE_VALIDATION.json.

## Source and measurement boundary

Source references below are one-based lines of the preserved benchmark.cpp and core.hpp.

| Check | Evidence and consequence |
|---|---|
| Raw baseline has no closure | benchmark.cpp:5–9 prepares a fresh default Plan and copies positions/edges. Only route≥1 calls close. The raw route reaches query with route=0 at line 16. core.hpp:25 uses original reverse edges when R is empty. |
| Closure and flags are paid per job | benchmark.cpp:13 calls prepare_plan from inside each complete_job. Lines 7–9 compute closure, cheap flags, and short-circuited quartet classification for that fresh Plan. The timed loop invokes complete_job at line 78. There is no parser-time closure, cross-plan closure cache, or copied ready-made flag. |
| Distinct closure-direct control | Route 1 calls close but is sent to query route 0, so it pays preparation plus the same BF path without beta/span routing. |
| Independent job state | Plan default member initializers make cheap/exact false and R/pairs empty. Closure rewrites R and pairs. Default rectangle/query vectors in the temporary Plan stay empty; actual immutable boxes and query order are referenced from seed. Calling the job “copying all inputs” would be inaccurate. |
| Scratch meaning | A single Scratch is declared at benchmark.cpp:39 and reused. core.hpp:25 writes every graph entry when BF is needed; line 26 resets all BF labels and predecessors. Capacity can be retained across jobs and routes after the common warmup. Fresh per-job scratch allocation is not included or promised. |
| Equal common exclusions | Parsing occurs at benchmark.cpp:25–38. Correctness/Floyd/certificate work is in the non-timing branch at lines 40–61. Warmup is at lines 68–71. None is in the saved elapsed intervals. |
| Exact interval | Start is at benchmark.cpp:75; lines 76–79 include repeated preparation, routing/BF, complete-job decision-hash generation and batch hash addition. Stop is at line 80. Expected-hash validation and outer volatile checksum addition occur after stop, at line 81. File and progress output occur at lines 83–85. |
| Work consumption and optimization | The per-query rolling uint64 hash is generated at benchmark.cpp:17 and used in the timed batch sum at line 78. The compiler memory barrier at line 77 precedes every job, and the batch sum is checked and added to a volatile global after stop. These protect observable work; the outer volatile store itself is not measured. The freshly rebuilt saved executable has byte-identical executable code and data. |
| Timer | core.hpp:14 uses std::chrono::steady_clock; duration_cast to nanoseconds is at benchmark.cpp:82. The saved log reports is_steady=1 and signed128 size=16. Clock overhead and ordinary OS scheduling remain part of this one-host measurement. |
| Routing semantics | core.hpp:30 rejects beta first; cheap/exact plans may then admit; span and fallback cover the remaining cases. The timed call passes no path-output pointer, so it measures the actual Boolean route without additional path diagnostics. Quartet may stop at its first obstruction and is not evaluated at all when cheap is true. |

The source therefore measures complete warmed Boolean jobs under the stated representation, including fresh route-specific ranking preparation. It does not measure cold input parsing, full per-job input materialization, cold scratch allocation or a certificate-serving service. “Consumed decision checksum” should be qualified to say that hash construction and batch accumulation are inside, while outer volatile consumption and expected-output validation are after the elapsed interval.

## Adverse results and paper wording

The complete all720 table is in PAPER_READY_FACTS.md. At Q=1 both cheap and quartet lose to raw-direct in all nine paired blocks; their setup is not amortized. At the primary Q=48, cheap and quartet beat raw-direct in all nine blocks, but quartet versus cheap is only 4 faster / 5 slower / 0 ties, with overlapping ranges and a slightly higher quartet median. At Q=192, quartet versus cheap is 3/5/1. It would be inaccurate to claim a robust incremental quartet speed benefit from the census timing.

Q48 scaling effects also go both ways. For n=32 contiguous sparse_dag (stratum 35), cheap/quartet median complete-job costs are 61,093.3/72,273.3 ns and quartet loses 8/9 paired blocks. For n=32 sparse-position sparse_dag (stratum 40), costs are 84,480.0/96,046.7 ns and quartet loses 9/9. Conversely, n=4 sparse-position sparse_dag (stratum 10) has 497.7/427.0 ns with quartet winning 9/9. All 50 original scaling strata, including every adverse case, are preserved separately in Q48_STRATA.csv and INDEPENDENT_AUDIT.json; these examples do not replace the full data.

Each scaling stratum has only three fixed plans. Repeated timings are not independent new workload samples. Stratum order remains ascending inside every block while Q/route order is shuffled; ordinary temporal drift and host load are not independently isolated. Min/max describe the nine observed blocks and are not confidence intervals. Q192 is exactly four repeats of the same 48 queries. The setup representations and early exits explain implementation costs; no universal complexity-optimality or prevalence claim follows.

Saved hashes establish file and schedule identity and the recorded provenance chain, but this audit did not observe the historical timing run or establish trusted external timestamps for prospective freezing. No GPU/native timing, H20 outward-auditor latency, application speedup, service throughput or full certificate-serving latency is supported by this supplemental CPU experiment.

## Outputs and replay

INDEPENDENT_AUDIT.json contains all 153 stratum/Q summaries, paired directions including ties, scope limits and original file hashes. PAPER_READY_FACTS.md supplies concise bounded prose and the all720 table. Q48_STRATA.csv exposes each primary scaling stratum. PE_SOURCE_BINDING.json records exact rebuilt code/data identity. NATIVE_VALIDATION.json and the compile/validation logs preserve replay commands. native-validation-replay/ retains the copied sources, generated validation and independent graph CSV, with no timing output. AUDIT_MANIFEST.json binds all independent files except itself.

For a fresh validation, copy this independent directory's checker sources beside a fresh copy of the unchanged study and run check_complete.py with bundled Python using -B -X utf8. The checker deliberately refuses an existing native-validation-replay directory rather than overwriting evidence. It contains no call to timing mode.
