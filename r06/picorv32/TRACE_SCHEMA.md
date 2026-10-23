# Reference-design trace schema

The successful execution is `attempt-007`. Its source snapshots and command
ledger identify the exact executing code. Top-level audit/replay code is a
later portable orchestration layer; it does not retroactively replace that
snapshot. `AMENDMENTS.md` identifies every failed earlier attempt.

`SCENARIOS.csv` has the initial18 signed integer fields for each scenario.
Scenarios0..95 are six-job reports sharing controller state;96..103 are the
eight actual invalid controller controls. Field names appear in the header.
`REFERENCE_RLE.csv` represents **every actual post-reference-edge sample**:
for a row `(scenario,first_edge,count,delta[18])`, repeat `state+=delta`
exactly `count` times, with first sample at the one-based `first_edge`.
Rows are contiguous and deltas are relative to the preceding decoded state,
starting from that scenario's initial state. Inputs/outputs and reset/start/
stop edges are included. This is lossless affine-delta run encoding, with
no skipped interval or interpolation between unobserved CPU states.

`REFERENCE_EXPANDED_HASHES.csv` gives each scenario's SHA256 over a canonical
20-byte record for each decoded sampled state, in this exact sequence:

1. timer: little-endian unsigned64 (state field14)
2. phase: little-endian unsigned32 (field12)
3. pulses: little-endian unsigned32 (field13)
4. pulse,busy,valid,reason: four unsigned8 fields (15,7,8,9)

The C++ producer computes this stream hash while sampling the real model,
before any RLE coalescing, and checks every valid busy edge's timer/phase/
pulse transition. The other sampled fields remain exactly reconstructible
from RLE. The expanded hash does not imply every CPU internal bit is traced.
The SHA256 implementation is author-owned and checks the standard `abc`
known-answer vector before execution. A different checker should independently
decode and hash this stream before publication.

`CORE_CYCLES.csv` has one row for each actual enabled CPU edge. The memory
request/ready transaction is sampled before that edge and trap/trace ports
after it. Each job starts with all-zero RAM plus ELF segments and the fixed
volatile input words, a fresh CXXRTL core, REGS_INIT_ZERO=1 and eight reset
cycles outside the observed interval. The deterministically initialized
CXXRTL state is a model boundary, not a physical power-up guarantee. Rows
include inactive memory values too; only `pre_mem_valid` licenses a bus
transaction. `lastfetch` includes the pipeline prefetch at28 at termination.
No CPU edge occurs between reference pulses. Core-cycle results must be
identical across the eight guard/path pairs for the same function/input/flag.

`JOBS.csv` gives actual `N`, `T`, result and the start/trap/stop reference
edge numbers. N is the count of executed processor edges; it is never a
countdown input. The start edge and stop edge are excluded; trap's pulse
edge is included. Consequently `ref_trap-ref_start=T=N*D`,
`ref_stop=ref_trap+1`, and timer does not increment on the stop edge.

`STREAM_BINDINGS.json` binds gzip bytes and the original uncompressed CSV
bytes separately, and records a full lossless readback verification. Raw CSVs
are retained locally but need not be duplicated in a portable package.
`ALL_REPORTS.jsonl.gz` contains all69888 query decisions and certificates,
including truth only as producer/debug annotation. Its expanded SHA256 is
in `AUDIT_RESULTS.json`. `AUDITOR_INPUTS.json` is the narrower actual audit
interface; it excludes N, D, program labels, producer truth and debug traces.

Neither output counts nor these traces validate a physical clock, hardware
implementation, arbitrary memory timing, analog settling, FPGA/silicon, PPA,
native Hopper, confidentiality or an ISA/toolchain proof outside this census.

For fresh replay, use `replay_portable.py --out NEW_EMPTY_DIRECTORY
--yosys-python-wrapper YOSYS_WRAPPER --zig ZIG --include YOSYS_SHARE_INCLUDE`.
Both include roots are added by the script. Run with Python3.12 `-B -X utf8`.
The final replay script recompiles all36 ELF images and both RTL models,
executes all576 jobs and8 controller controls, runs the independent functional
oracle, creates the graph census and lossless archives. It requires only the
already installed external tools; no host executable/runtime is distributed.
