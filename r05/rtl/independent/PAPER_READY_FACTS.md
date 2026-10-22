# Independently validated paper facts

PASS for the declared logical reference RTL and real-valued log abstraction.
This is author-side independent validation, not a blind review or score.

Actual Yosys 0.70 synthesis and Zig 0.14.1 C++17 compilation were rerun in
`fresh-replay/`. A separately written oracle explicitly expanded and checked
all 389,022,846 post-edge states in each of the original and fresh traces.
The census contains 32 valid reports, 192 jobs, 387,019,984 valid active ticks,
386,440 valid job pulses, and 12 exact-reason contract-unknown controls.
Every valid job completed after exactly N*D subsequent reference rising edges;
the start edge is excluded. The reported timers came from generated RTL.

All 23,040 total orders and all 32 fixed P<=F/A<=S conjunctions were recomputed
using 13 original z=-theta and bias variables with an independent edge-list
algorithm. Exact Fraction log sums and geometric tail bounds supplied separate
10^70 outward bounds. All 8,878 admitted witnesses were checked in the original
variables, including direct rigorous real-log comparisons. Every one of the
14,194 relaxed negative cycles was checked edge by edge with its exact weights.

| Population | Queries | True admitted | False admitted | Joint rejected | Box rejected | Extra joint rejections | Unknown |
|---|---:|---:|---:|---:|---:|---:|---:|
| All total orders | 23040 | 2908 | 5956 | 14176 | 14100 | 76 | 0 |
| All-tie total orders | 2880 | 2880 | 0 | 0 | 0 | 0 | 0 |
| Other-vector total orders | 20160 | 28 | 5956 | 14176 | 14100 | 76 | 0 |
| All fixed conjunctions | 32 | 4 | 10 | 18 | 12 | 6 | 0 |
| All-tie fixed conjunctions | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| Other-vector fixed conjunctions | 28 | 0 | 10 | 18 | 12 | 6 | 0 |

The 2,880 all-tie true total orders account for most of the 2,908 true orders;
the other seven vectors contribute 28. No true claim was rejected or unknown.
The extra total-order rejection count is 76 among 8,940 box admissions, or
among 6,060 after excluding all ties; 6,032 box admissions are originally
false. The extra fixed-conjunction count is 6 among 20 box admissions, 16 of
which are false. These are designed-census denominators, not workload rates.
The changed fixed-conjunction case IDs are 0, 2, 15, 26, 27, 28.

| Vector | True total orders | Admitted | Rejected | Box rejected | Extra rejections |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 101 | 2779 | 2757 | 22 |
| 1 | 2880 | 2880 | 0 | 0 | 0 |
| 2 | 4 | 1615 | 1265 | 1259 | 6 |
| 3 | 4 | 1530 | 1350 | 1349 | 1 |
| 4 | 4 | 1621 | 1259 | 1259 | 0 |
| 5 | 4 | 11 | 2869 | 2869 | 0 |
| 6 | 4 | 976 | 1904 | 1871 | 33 |
| 7 | 4 | 130 | 2750 | 2736 | 14 |

Vectors 1, 4, and 5 have zero incremental total-order rejection. All 32 per-case
tables, including every zero cell, are in PAPER_READY_FACTS.json.

Admission means feasibility in the licensed real-valued log abstraction. It
does not recover original N, establish an alternate concrete integer RTL
realization, or guarantee secrecy against timing inference. A rejection
refutes the queried conjunction for any concrete source state mapping into
that abstraction under the trusted source obligations.

The five actually synthesized and compiled semantic mutants widened the guard,
removed held-divider checking, shortened the countdown, removed the reset
license, or removed the settlement gate. The independent harness detected all
five, while its unmodified RTL baseline passed.

The replay is semantically exact, not wholly byte-identical. Gzip mtime bytes
and the resulting archive binding differ. The executable differs in PE
timestamps and CodeView RSDS build GUID bytes; no GUID bytes are silently
ignored. Its .text section, generated netlist, all sampled trace bytes, all
jobs/intervals/observations and decompressed graph records are exact. Both
actual archive hashes and binary differences are retained in the evidence.

- Author-side independent validation, not a blind review and not a conference judgment.
- New logical reference RTL and synchronous reference ticks only; no native Hopper/H20/HUSH, GPU, silicon, FPGA, physical clock calibration, CDC/metastability, PPA, latency, or performance validation.
- All 32 designed reports and 23,072 graph queries are a fixed census, not workload frequencies or a representative distribution; all-tie admissions dominate the true-order population.
- Admission is feasibility of a real-valued log abstraction; it does not identify the original private N, prove concrete alternate integer N/D RTL realizability, or provide cryptographic/inference-resistant privacy.
- Source trust still includes truthful guard/obligation bits and the timer interface. Full debug evidence intentionally discloses N/D, while the audited interface excludes them.
- Reset initializes the synchronous model; pre-reset CXXRTL zero values are recorded but are not a hardware initialization guarantee. Logical settlement means two stable quiet sampled edges, not analog settling.
- The explicit full-edge oracle uses signed int64 trace storage and is valid on the declared bounded runs; it is not a proof for arbitrary uint64 overflow states.
- Declared maximum N=2100, D=1030, N*D<=2163000 makes all 32-bit counters, 64-bit timer, and 40-bit products nonoverflowing. Overflow reason7 was source-reviewed but not forced by simulation. The small independent harness additionally exercised zero inputs (reason6), busy reset (reason5), and repeated busy start (reason8), without adding them to the 12 declared controls.
- The generated executable is not byte-identical even after PE timestamps alone: CodeView RSDS build GUID bytes also differ. Its .text section and all semantic outputs are exact; the GUID difference is preserved and not ignored.
- The gzip query archives have different mtime bytes and actual SHA256 bindings; their decompressed bytes are exact. No archive byte-identity or fully deterministic-build claim is made.
- Independent finite-census/certificate verification and state induction do not constitute a general formal proof of arbitrary RTL/compiler/toolchain behavior.
