# PicoRV32 firmware-regression source study: producer delivery

This is a completed **producer execution**, pending a different agent's fresh
synthesis/execution, independent source/ISA/timer checks and all graph
certificate checks. No paper, scoring or public release is part of this task.

The actual unmodified public CPU is PicoRV32 commit
`ef203c2b0a3fb793280f5114941416c425c5b461`; exact RTL/README/ISC-license bytes
and SHA256 are in `upstream/` and `UPSTREAM_BINDING.json`. `PROTOCOL.json`
was written after that source binding and before all firmware/wrapper/DUT
generation. The fixed design is six own C functions, two deterministic inputs,
six compiler flags, two guard budgets and four divider paths. Programs, inputs,
flags and queries were never selected or tuned from cost/filtering outcomes.

`attempt-007` completes36 actual RV32I firmware binaries,72 independent
ISA/algorithm combinations and576 actual CPU jobs. Its Yosys-generated
processor and controller execute1,888,264 core cycles and1,903,944,322 actual
reference edges, with zero checked reference-edge mismatches. Timer identity
is T=N*D, c=0, under the declared synchronous host-memory/event-scheduler
boundary. N comes from actual processor execution, never a countdown input.

All69,120 total-order queries:2,958 admissions,66,162 rejections,zero numeric
unknowns. Of1,152 producer-truth true orders, all admit;1,806 false admissions
remain. Joint graphs reject63 of3,021 every-anchor-box admissions (63 of1,869
false box admissions). All768 prospective partial conjunctions:333 admissions,
435 rejections,zero unknowns;288 true queries all admit and45 false admissions
remain. Their additional joint rejection is **0/333**. Every cell, including
zero benefit and duplicate binaries, is retained. Eight actual invalid
controller executions and four source-validator mutations are all contract
unknown, without graph audit.

Read `PAPER_READY_FACTS.json` for groups/cells and exact scope,
`NEGATIVE_CYCLE_EXAMPLE.json` for a concrete source-derived changed verdict,
`attempt-007/OBSERVATIONS.json` for source timer/log ranges,
`attempt-007/ALL_REPORTS.jsonl.gz` for every query/certificate, and
`TRACE_SCHEMA.md` for lossless trace decoding and canonical expanded hashes.
The public auditor interface is `attempt-007/AUDITOR_INPUTS.json`; debug N/D
and truth are kept separately. This interface provides no privacy guarantee.

Every failed attempt remains. `AMENDMENTS.md` explains all six adaptations,
none of which changes a workload, flag, input, CPU RTL or divider/query family.
Attempt-006's first actual job remains source-unknown: its too-strict endpoint
validator mistook the normal RAM prefetch at28 after ebreak24 for a wrong
terminal instruction. Address28 is in the original code domain and has no
read side effect. Actual trap/start/stop edges and memory permissions did not
change; that interpretation is an explicit independent-audit obligation.

Original local failure logs/ELF are preserved byte-exact. **Do not recursively
package this research directory.** `portable-v1/` is the separate whitelisted
delivery tree; `PORTABLE_MANIFEST.json` records original and portable hashes,
any metadata-only local-path adaptation, and every local-only exclusion.
No host executable, PDB or installed runtime is in the portable tree. The
failed oversized debug ELF remains local-only. Successful firmware ELF/RAM
images are included as author-owned research data; PicoRV32 licensing remains
with its exact original bytes. No public publication has been performed.

For recomputation, the final `replay_portable.py` freshly compiles firmware
and both RTL designs, executes the processor/reference controller, checks
independent ISA/algorithm outputs, creates all queries/certificates and
lossless gzip streams. It accepts external installed Zig/Yosys/include paths
as arguments. `attempt-007/ATTEMPT.json` preserves the exact older executing
snapshot; `POSTPROCESS_BINDING.json` separately identifies the later auditor
and archive tools. The independent agent must check those bindings, the
prefetch/source boundary and every certificate, not treat this producer
summary as that independent gate.

The result establishes a bounded logical source contract for a fixed
firmware-regression census. It establishes no physical clock calibration,
native Hopper/H20 behavior, silicon/FPGA, PPA/performance, confidentiality,
representative workload frequency, general ISA/compiler proof, or necessity
of the interface/method when a producer chooses to reveal full cycle counts.
