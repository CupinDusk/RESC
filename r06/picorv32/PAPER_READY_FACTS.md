# Bounded producer facts; independent gate pending

Actual unmodified PicoRV32 commit `ef203c2b0a3fb793280f5114941416c425c5b461` executes36 fixed
RV32I firmware binaries across72 function/input/flag combinations and576
reference-design jobs. All72 independent ISA/algorithm checks and576 actual
RTL outputs agree. The controller counts 1903944322 actual
reference edges and the processor executes 1888264 core cycles.
Observed timer identity is T=N*D with start/reset/stop outside and c=0.

All69120 total orders: admit=2958, reject=66162,
unknown=0, false admissions=1806.
Additional joint rejections beyond every-anchor boxes:
63/3021 box admissions.
All768 fixed partials: admit=333, reject=435,
unknown=0, false admissions=45;
additional joint rejections=0/333.
Every report, tie/duplicate binary, zero-effect cell and failed attempt is
retained. Twelve invalid-control/source-validator cases return unknown.

These are producer-verified discrete-event reference-design facts. They
remain pending a different agent's fresh synthesis/execution, independent
timer-trace decode and69888 certificate checks. No publication or PDF use
is authorized by this file alone. No physical clock, native Hopper, silicon,
FPGA, PPA, performance or confidentiality conclusion follows.
