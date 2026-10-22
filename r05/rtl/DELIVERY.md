# Reference RTL delivery: author execution passed, independent gate pending

The new logical reference RTL was actually synthesized with Yosys0.70,
compiled from its generated CXXRTL with Zig0.14.1 C++17 and executed locally.
`attempt-002/PORTABLE_REPLAY.json` binds all sources, commands, versions,
return codes and generated outputs. No remote work, private/native source,
manuscript edit, release or push was performed.

All declared populations were retained:32 reports,192 jobs,12 invalid attempts,
23,040 total-order queries and32 fixed P<=F/A<=S conjunctions. The executable
sampled389,022,846 reference edges, including387,019,984 valid active edges,
and observed386,440 valid job pulses. Every valid timer was counted by RTL,
completed at the Nth pulse and matched the post-execution induction check.
All12 invalid attempts returned contract-unknown with their intended exact
reason; none entered graph audit.

| Query population | Queries | True, all admitted | False admitted | Joint rejected | Box rejected | Extra joint rejections | Numeric unknown |
|---|---:|---:|---:|---:|---:|---:|---:|
| All total orders | 23040 | 2908 | 5956 | 14176 | 14100 | 76 | 0 |
| All-tie total orders | 2880 | 2880 | 0 | 0 | 0 | 0 | 0 |
| Distinct-vector total orders | 20160 | 28 | 5956 | 14176 | 14100 | 76 | 0 |
| All fixed conjunctions | 32 | 4 | 10 | 18 | 12 | 6 | 0 |
| All-tie fixed conjunctions | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| Distinct-vector fixed conjunctions | 28 | 0 | 10 | 18 | 12 | 6 | 0 |

The total-order extra-rejection denominator is8940 box-admitted queries
(6060 excluding the all-tie vector); among originally false box admissions,
the denominator is6032. The fixed-conjunction denominators are20 box admissions,
16 of them false. These are a fixed designed census, not workload frequencies.
Vectors1,4,5 respectively have0,0,0 extra total-order rejections. The full
32 per-vector/path tables, all zero cells, true/false breakdowns and all
certificate records are retained rather than selecting improved cases.

| Vector ID | v | True total orders | Joint admitted | Joint rejected | Box rejected | Extra joint rejections |
|---|---|---:|---:|---:|---:|---:|
| 0 | 0,20,12,-4,48,4 | 4 | 101 | 2779 | 2757 | 22 |
| 1 | 0,0,0,0,0,0 | 2880 | 2880 | 0 | 0 | 0 |
| 2 | 0,4,8,12,16,20 | 4 | 1615 | 1265 | 1259 | 6 |
| 3 | 20,16,12,8,4,0 | 4 | 1530 | 1350 | 1349 | 1 |
| 4 | 0,1,2,3,4,5 | 4 | 1621 | 1259 | 1259 | 0 |
| 5 | 0,20,40,60,80,100 | 4 | 11 | 2869 | 2869 | 0 |
| 6 | 5,0,4,1,3,2 | 4 | 976 | 1904 | 1871 | 33 |
| 7 | 48,20,12,-4,0,4 | 4 | 130 | 2750 | 2736 | 14 |

The fixed-conjunction changed-verdict cases are case IDs0,2,15,26,27,28;
all other cases are retained too. Admitted false claims demonstrate
compatibility with some hidden source state, not recovery of the original N.

The source argument, precise reset/settling/tick convention, induction,
nonoverflow bounds and abstraction privacy meaning are in SOURCE_CONTRACT.md.
SCHEMA.md gives fresh replay instructions and the full trace/certificate
schemas. PROTOCOL.json predates source generation; its SHA256 is
58e12453c45bda38089478994cdc8a0d76a7c1387ba4fd3bbec1238e9ddcb73c.
The public R04 graph source is copied byte-exact and source-hash bound in
CORE_PROVENANCE.json. Exact rational-series log enclosures with a geometric
tail bound replace its unused Decimal helper. Every admission certificate was
checked in original theta/bias variables and every rejection cycle edgewise.

Primary evidence inventory:

- `reference.v`, `driver.cpp`, `generate_inputs.py`, `replay_portable.py`:
  portable author source; actual RTL edge counting, held divider and countdown.
- `PROTOCOL.json`, `SOURCE_CONTRACT.md`, `SCHEMA.md`, `CORE_PROVENANCE.json`:
  predeclared cases, obligations, arithmetic and reproducibility boundaries.
- `attempt-002/netlist.cpp`, `simulate.exe`, tool stdout/stderr logs:
  generated, compiled and executed CXXRTL, not Python forward simulation.
- `attempt-002/TICKS_RLE.csv`, `SCENARIOS.csv`: lossless representation of every
  sampled reference edge, approximately63MB; preserve exact bytes. A later
  lossless compressed release can bind both compressed and expansion hashes.
- `attempt-002/JOBS.csv`, `INVALID_CONTROLS.csv`, `RTL_RESULTS.json`:
  every timer, pulse count, controller state and exact invalid reason.
- `attempt-002/AUDITOR_INPUTS.json`: obligation/guard validity and integer
  timer enclosures only; N,D are absent. Debug evidence separately discloses N,D.
- `attempt-002/OBSERVATIONS.json`, `ALL_REPORTS.jsonl.gz`, `AUDIT_RESULTS.json`:
  every per-case count, outward bounds, all23072 verdicts and certificates.
- `attempt-001/`: first Yosys generation and failed compiler invocation/logs,
  preserved without modification. AMENDMENTS.md records the include-path fix.
- `INVENTORY.json`: SHA256 and byte count for every file present at delivery,
  excluding the inventory itself. Later independent outputs are separate.

This remains author-side evidence pending fresh independent rebuild, trace
decoding, graph/certificate checks and meaningful mutants. It is not native
Hopper/H20 implementation, physical frequency/timer calibration, FPGA/silicon,
PPA, performance, CPU benchmark or universal source verification. Abstract
privacy has no cryptographic or inference-resistance guarantee. No publication
was performed, and no claim should bypass the independent gate.
