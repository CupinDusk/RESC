# Independent author-side validation

**PASS**, bounded to the declared new logical reference RTL and real log
abstraction. There is no native H20, physical clock, PPA, performance or
publication result. Producer evidence is unchanged: all 77 delivered inventory
entries still match their exact sizes and SHA256 values, including attempt-001
and its missing-runtime-header compilation failure.

## What was independently checked

1. The frozen protocol, source contracts, schema, source code, all attempt-002
   artifacts, provenance and actual command records were inspected. No reviews
   or manuscripts were consulted. The copied audit_core.py hash is
   9a4ad638a45cd69b43e7b2389417d6a43481225ee2c6e67fd9664b58d31f55a9.
2. Fresh actual Yosys synthesis and generated CXXRTL compilation/execution used
   the portable producer runner under independent/fresh-replay. This alone was
   not the independent gate. edge_oracle.cpp, independent_checks.py and
   mutant_harness.cpp are separately written and import no producer checker.
3. edge_oracle.cpp explicitly expands every RLE span (1,166,181 rows per trace)
   into all 389,022,846 sampled states. Every output register is compared to
   its independently computed next state on every edge, including reset,
   license, two quiet settlement edges, both guard inequalities, held divider,
   remaining/phase/pulses, timer, jobpulse, completion and reason priority.
4. independent_checks.py reconstructs every input control segment from the
   frozen protocol, not from producer job labels, and checks every affine input
   span against that schedule. All 192 job rows and all 12 invalid rows match
   independently derived values in every column. This binds actual private
   latched cycle counts to the fixed vectors, changing cfgn=N+777 after capture,
   actual completion edges, and integer [T-1,T+1] intervals. All scenarios,
   initial vectors, field framing, edge contiguity and no-loss census are checked.
5. The audited interface has an exact field whitelist. No N,D, phases, pulse
   counts, truth or vector labels enter it. Intervals and validity bits are
   bound back to decoded jobs. Invalid controls have a null interval and no
   graph permission; all 12 produce their designated reason, with family counts
   3 missing reset, 2 unsettled, 3 invalid guard and 4 busy divider changes.
6. All graph inputs after interface construction come only from that interface.
   Producer N is used solely for separate truth annotation. An independent
   13-variable original-state difference-constraint graph is solved using
   synchronous edge-list Bellman-Ford; it does not call or import the producer
   six-node matrix/Bellman-Ford/Floyd implementation. Independent exact Fraction
   logarithms use 170 terms, rational arithmetic and a geometric remainder,
   with 10^70 outward graph endpoints. Every supplied 10^60 enclosure contains
   the separately certified true log interval. All 23,072 statuses, box beta
   fractions, true/false annotations, group/per-vector/per-case counts and all
   certificates match. Zero and no-improvement cells are retained.
7. For admissions the original theta,bias witness satisfies every observation,
   guard step and query, including direct comparisons against separately
   enclosed real logarithms. For rejection, every cycle is closed, every edge
   weight is independently derived from the observation plus bias-distance
   bound (or the queried zero-order edge), and the exact sum is negative.
8. Six extra actual RTL builds comprise the independent baseline and five
   semantic mutants, each synthesized, compiled, executed and logged. All five
   mutants are killed at a contract-observable post-edge state; baseline passes.
   These are not file-difference or compile-failure tests. They use the same
   independent transition oracle as full-trace validation.

## Induction and source-level argument

Synchronous report reset writes every RTL register and previous_D=1000. The
pre-reset simulator vector is only a decoding origin. Idle command reset
captures N,D, clears counters and settlement, grants one license, and preserves
guard history. Two subsequent quiet edges at the captured D establish the
logical settled state. Start consumes the license even on rejection. For an
accepted start, phase=pulses=timer=0 and remaining=N, with busy and valid true.
The guarded history update makes both exact inequalities equivalent to
|log(D_j/1000)-log(D_(j-1)/1000)|<=log(201/200), including the initial D0=1000.

For k subsequent valid busy edges, induct on divider phase: a nonpulse edge
increments phase and timer; phase=D-1 emits exactly one jobpulse, clears phase,
increments pulses and decrements remaining. Therefore timer=k, phase=k mod D,
pulses=floor(k/D), remaining=N-floor(k/D), until k=N*D. The Nth pulse makes
remaining=0,busy=0,done=1. This is the first completion and the timer was counted
on actual RTL edges, not assigned a product. All 192 full edge sequences match
this argument and use a stable held divider despite the changed cfgn input.

N in [1996,2100], D in [976,1030] and ND<=2,163,000 are independently bound to
the protocol and actual edges. Phase<D, pulses<=N and remaining>=0 preclude
wraparound. All declared guard products are below 201*1030<2^40. The 32-bit
count and 64-bit timer cannot overflow here. A configured-divider change has
priority over counting or completion and returns reason4; no invalid attempt
licenses an observation. Busy reset, repeated start, zero inputs and overflow
branches were source-reviewed; only the first three were additionally exercised
in the small independent harness. Overflow injection is outside this evidence.

For graph equivalence, write z_i=-theta_i. Each observation is the pair of
edges b_(i+1)-z_i<=u_i and z_i-b_(i+1)<=-l_i, adjacent bias edges have weight
delta in each direction, and theta_p<=theta_q is z_q-z_p<=0. All 13 variables
can be translated together to make b0=0 without changing these constraints.
The producer six-node eliminated weights upper_b-lower_a+delta*|a-b| are the
corresponding necessary pairwise bounds, and its constructive Lipschitz bias
witness restores the original constraints on admission. The independent graph,
original-variable witness checks and edgewise cycles validate all critical
producer matrix, feasibility, anchoring, beta and certificate logic on this
declared census. This is not a universal formal proof of the software.

## Retained failures and replay nonidentity

The producer attempt-001 remains byte-exact: actual synthesis succeeded and
compilation failed because cxxrtl/cxxrtl.h required the runtime include root.
The independent replay supplies both include roots and no RTL/input edit.

Independent check attempt-001 first stopped at an overly strong whole-file
AUDIT_RESULTS byte-equality assertion. Investigation showed gzip mtime at
offsets 4,5 changed its actual archive hash, and only that binding changed in
AUDIT_RESULTS. Independent attempt-002 then stopped at an executable-equality
assertion: the PE timestamps and CodeView RSDS build GUID differ. Both failed
check logs are preserved. The final checker does not suppress these facts or
normalize the GUID: it records exact differences, validates each actual hash,
requires .text/code and all semantic outputs exact, and separately reports
whole-file byte inequality. Checks attempt-003 and final attempt-004 pass.
No producer source, output, manifest or failure evidence was repaired.

The archives' decompressed query records are byte-exact. Executables differ
only in parsed PE timestamp fields and RSDS GUID bytes; .text section SHA256
is 854ab5c540ef3b64d7e3e1ac1d3f5fea4d8b7dff9d1fbc1390df6c0d4446682d.
The exact 17 executable byte offsets and both actual archive hashes are in
GRAPH_AND_FRAMING_CHECK.json. A deterministic package/build claim is not made.

## Scope and limitations

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

All outputs of this validation are under independent/. No remote data, native
private code, reviewers, manuscript, publication, push or global installation
was used or modified. No CPU performance timings were collected. Reproduction
commands and actual per-stage logs are in COMMANDS.json, fresh-replay's
PORTABLE_REPLAY.json and each mutants/*/RESULT.json.
