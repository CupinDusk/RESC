# Correctness/tool compatibility amendments

1. Before any firmware executes, attempt-001 fails at the first compilation:
   Zig 0.14.1 reports `unsupported linker arg: --no-relax`. The protocol's
   linker spelling is replaced by the Clang compilation spelling `-mno-relax`,
   retaining startup `.option norelax`. This disables emitted relaxation
   relocations without requesting an unsupported Zig linker option. Programs,
   optimization flags, inputs, CPU, divider paths and queries are unchanged.
   The complete failed attempt, protocol and old command remain in attempt-001.
   Actual tool support and emitted RV32I ELF will be checked before execution.

2. Attempt-002 fails before any firmware compilation succeeds: Zig interprets
   `-march=rv32i` as an unknown CPU name. Its installed
   `lib/std/Target/riscv.zig` defines `generic_rv32` with only `32bit` and `i`
   features (lines 1941-1947), whereas `baseline_rv32` includes extensions.
   Replace the spelling with `-mcpu=generic_rv32`, retaining `-mabi=ilp32`.
   This names the same intended RV32I ISA in this installed Zig driver.
   No workload or optimization changes; attempt-002 retains the diagnostic.

3. Attempt-003 first compiles successfully, but its ELF PT_LOAD text is
   325936 bytes, exceeding the prospective8192-byte firmware domain; the
   extraction assertion rejects it before DUT execution. The link script
   collects unused compiler-rt code, while default compiler-rt debug data is
   also present. Add `-rtlib=none -g0 -Wl,--gc-sections` to request freestanding
   no-runtime linking and dead-code removal. The bound remains8192. This is
   a code-domain correctness fix before any cycle/filtering observation,
   with all source functions and optimization levels unchanged.

4. Attempt-004 fails during the first link, before executing firmware:
   Zig's default UBSan runtime still introduces undefined software divide/
   multiply helper references after compiler-rt is disabled. Add
   `-fno-sanitize=all` so this bounded bare-metal C execution does not include
   an OS-oriented diagnostic runtime. The unsigned C functions and their
   well-defined inputs are unchanged. Diagnostics that contain local tool
   cache paths are sanitized to portable placeholders with raw-log hashes
   retained; no source bytes or diagnostic meaning are discarded.

5. Attempt-005 compiles all36 bounded firmware images and synthesizes both
   unmodified CPU and controller, then C++ compilation rejects integration
   spelling: Yosys escapes underscore ports to double underscores, both
   generated translation units export `cxxrtl_design_create`, and a generic
   helper needs C++'s dependent-template disambiguator. Correct driver port
   spelling, rename only the two unused C factory symbols with preprocessor
   aliases, and add the `template` keyword. No RTL/upstream semantics change.
   This is diagnosed before any DUT execution; generated old units/logs remain.

6. Attempt-006's first actual processor job reaches trap at core cycle729,
   with correct result MMIO already written. The strict `last fetched ==
   ebreak` validator fails: bus trace shows ebreak0x00100073 fetched at
   address24, then the legal next word `jal x0,0` at28 is prefetched on the
   trap edge. That prefetch is observable PicoRV32 behavior, not execution
   of a different terminal instruction. Keep the failed job as contract
   unknown and revise only the endpoint validator: ebreak must have been
   fetched, and the final fetch must be the fixed startup's word at28
   (0x0000006f). An independent RV32I functional interpreter additionally
   checks each binary/input halts at ebreak address24 with the expected
   result. No CPU/firmware/clock/cost change is made, and no filtering result
   has been computed. All failed actual trace/timer evidence remains.
