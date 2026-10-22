# Replay and evidence schema

Use a new `--out` directory. `replay_portable.py` copies source snapshots,
generates only PROTOCOL inputs, records actual tool versions, synthesizes
`netlist.cpp`, compiles it into `simulate.exe`, runs that executable and audits
its outputs. Example from the workspace root:

    python -B -X utf8 run_r05_checks.py --zig /path/to/zig --yosys /path/to/yosys --include /path/to/yosys/include

Other hosts may supply `--yosys` and a C++17 compiler instead of the local
wrapper/Zig options. Generated0.70 netlist uses the runtime include root too;
the runner supplies both include roots. Tools remain external to the artifact.
No CPU runtime benchmark or wall-time performance claim is collected.

`PORTABLE_REPLAY.json` records source SHA256, exact argument arrays, every
return code, status, and hashes of all output files. Each command has separate
stdout/stderr logs. A failed attempt is retained in its original directory;
see AMENDMENTS.md. No subsequent attempt overwrites it.

`vectors/INPUTS.json` and `vectors/vectors.txt` carry all producer cases, private
N,D values, invalid triggers and stable IDs. `vectors/INPUT_MANIFEST.json` binds
the protocol and generator. There are32 valid reports, six jobs each, and12
invalid scenarios, not a sampled workload population.

`SCENARIOS.csv` columns are scenario,type,id and19 actual initial state fields.
Type0 is a valid report with caseid=scenario in0..31; type1 is invalid attempt
id=scenario-32 in0..11. A report uses one model and preserves guard history
across six command resets. Each scenario starts with an actual synchronous
report reset at reference edge1. Initial model values before that edge are
recorded for lossless decoding; scientific claims begin after report reset.

`TICKS_RLE.csv` columns are scenario,first_edge,count followed by those same19
field names. The entries in the19 fields are **signed state deltas**, not
absolute state. Rows are in scenario/edge order; a row starting at e of length
c means that for every edge k=e..e+c-1,

    state(k)=state(k-1)+row_delta.

Start from the actual initial state in SCENARIOS. Every next row starts at
previous first_edge+count, so every reference rising edge is represented once.
The producer builds a new delta from actual sampled CXXRTL state on every
edge, coalescing only equal adjacent delta vectors. Clock high/low simulator
delta cycles are settled by CXXRTL `step()` and are not reference input edges.

The19 state fields, in order, are rst,commandreset,start,cfgn,cfgd,licensed,
settled,busy,done,valid,reason,nlatched,heldd,previousd,remaining,phase,pulses,
timer,jobpulse. Configured private cfgn changes after each accepted start to
test count latching; it is not a new job parameter. A compressed span is fully
affine; checking all its integer states can use an affine invariant proof or
explicit expansion. Recorded spans are not skipped simulation edges.

`JOBS.csv` is full debug evidence: case_id,vector_id,slot,scenario,reset_edge,
start_edge,completion_edge,N,D,previous_D,settled_at_start,T,lower,upper,
job_pulses,valid,reason. T is read from the RTL timer after done. Completion
minus start in actual scenario edges must equal T. These192 rows supply every
valid observed interval. `INVALID_CONTROLS.csv` retains all12 expected/actual
reason codes, trigger edges, partial timers/pulses and graph permission0.

`AUDITOR_INPUTS.json` is the research abstraction interface. Its valid records
contain only case/slot IDs, timer endpoints and obligation/guard validity.
Its invalid records expose exact reason codes but no licensed timer interval.
N,D,phase,pulses and private truth labels are absent. It is intentionally
separate from full debug data and is not a secrecy mechanism.

`OBSERVATIONS.json` contains all32 sets of rigorous scaled log endpoint bounds,
all720-order count tables and each fixed partial verdict. `ALL_REPORTS.jsonl.gz`
contains exactly23,072 query rows, case order stable: all720 permutations then
the fixed partial query for each case. Total orders store a six-slot
permutation whose15 implied pairwise claims are tested. Partial claims are
P<=F and A<=S, stored as[[0,5],[4,1]]. `true` refers to the original producer
N values and is not included in the auditor input.

Each query contains path,box,beta lower/upper rationals and a certificate.
Admission certificates have six theta_scaled and seven bias_scaled integers
with bias0=0 at scale10^60. Rejections have a closed directed cycle, its relaxed
edge weights and a strictly negative exact total. Numeric-unknown includes
both a tightened rejection and relaxed feasible potential. Invalid controls
never enter this file. `AUDIT_RESULTS.json` retains every per-vector and
per-path count, aggregate tables, all-tie separation, precise arithmetic
metadata and source/output bindings. No zero cells are suppressed.
