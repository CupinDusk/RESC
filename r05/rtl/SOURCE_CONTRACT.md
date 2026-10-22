# New logical reference job: contract and proof

This is newly written author-owned reference RTL. It was not acquired from a
GPU, native H20/HUSH source, semiconductor implementation or private workload.
The experiment supplies a concrete discrete-time producer for the joint timing
abstraction. It does not establish a physical clock, frequency monitor,
calibrated timer, metastability margin, CDC safety, silicon/FPGA feasibility,
area/power or execution-time performance.

The trusted logical controller observes synchronous reference rising edges.
All input values are stable for each sampled edge; the CXXRTL simulator settles
after each low/high/low transition. A report reset first initializes every
register and sets previous divider to1000. That reset does not license a job.
Each command reset, while idle, latches the private count and configured divider,
clears status/timer/counters, and grants exactly one start license. The previous
divider is deliberately retained across command resets. Two subsequent quiet
edges with configured divider equal to the captured divider set settled=2.
This defines logical settlement; physical analog settlement is untested.

At a start edge the controller requires the reset license, settled=2,
configured divider equal to captured divider, positive latched count/divider,
and both exact unsigned cross-products

    200*D <= 201*previous_D; 200*previous_D <= 201*D.

It consumes the license even if it rejects the start. An accepted start sets
busy/valid, captures D into the guard history and initializes remaining=N,
phase=pulses=timer=0. The start edge is excluded from measured duration.
Every subsequent busy reference edge increments the RTL timer by one. A held
divider produces the one-edge `jobpulse` whenever old phase equals D-1; it
resets phase and decrements remaining once. This is a synchronous job-clock
enable, with no claim of a synthesized physical derived-clock domain.

Induct on subsequent edge k. Initially k=0, timer=phase=pulses=0 and
remaining=N. If phase<D-1, the next edge adds one to timer and phase and leaves
remaining/pulses unchanged. If phase=D-1, it adds one to timer and pulses,
resets phase and subtracts one from remaining. Thus, before terminal completion,

    timer=k; phase=k mod D; pulses=floor(k/D);
    remaining=N-floor(k/D).

The Nth pulse, at k=N*D, leaves remaining=0, busy=0, done=1, valid=1.
No branch writes a multiplied N*D value to the timer. `driver.cpp` reads timer
from the generated model after completion; its N*D multiplication is a
post-execution assertion only. It additionally changes external `cfgn` after
start; latched N is unaffected. Every actual sampled edge is checked and saved
in the lossless trace representation.

The RTL widths are N,D,phase,pulses,remaining32, timer64, and guard products40.
Declared valid N range1996..2100, D range976..1030 and N*D<=2,163,000; even
external `cfgn=N+777` fits32. Each guard product is below201*1030<2^40.
Phase<D, pulses<=N, remaining is decremented only when positive; the last
decrement is1 to0. No declared counter can wrap. Generic zero inputs and
overflow are rejected (reason6/7), although they are outside the declared
control population. Reset while busy is reason5 and repeated start while busy
reason8; these extra branches do not constitute tested coverage.

Missing command reset (reason1), unsettled start (reason2), bad guard jump
(reason3) and configured divider changes at any sampled busy edge (reason4)
produce valid=busy=done=0 and a retained reason. A divider change on a would-be
completion edge has priority over counting/completion. Invalid attempts do not
license a timer observation or any graph decision. All 12 declared attempts
are retained, with distinct trigger edges. The invalid mid-command changes
are input mutations; the independent validation stage also tests semantic
source/certificate mutants separately.

For valid jobs, the model uses T=N*D, theta=log N,
b_j=log(D_j/1000), and log(T/1000)=theta+b_j. The exact guard licenses
|b_j-b_(j-1)|<=log(201/200), with b_0=0. Timers are disclosed only as
integer enclosures[T-1,T+1]. Auditor inputs include obligation/guard validity
and those enclosures, while private count/divider and truth labels appear only
in full producer/debug evidence. This is privacy at an abstraction interface;
it is no cryptographic assurance and does not prevent timing inference.

An admitted query is compatible with some source state satisfying the licensed
abstraction. It need not be true of the original hidden N values. A rejection
refutes the conjunction under that contract. Contract-unknown means the
source obligations did not license graph auditing; numeric-unknown means
outward arithmetic straddles a feasibility boundary. Neither is a rejection.

The unchanged public R04 integer graph functions are source-hash bound.
`exact_logs.py` replaces the numerical input conversion with exact positive
rational series. Binary reduction x=2^k*y,1<=y<2 gives z=(y-1)/(y+1)<=1/3.
Each of120 atanh-series terms is rounded down/up at10^90, and the remaining
positive tail is bounded above by
2*z^(241)/(241*(1-z^2)). The same construction encloses log2. Addition and
outward rescaling to10^60 use integers only. Tight graph feasibility supplies
an admission certificate verified in the original theta/bias variables;
a negative cycle in the relaxed graph supplies a rejection certificate
checked edge by edge. Any unresolved boundary stays unknown.

The source functions and all generated artifacts remain pending a separate
independent fresh rebuild, trace decoding, graph/certificate validation and
meaningful mutants. No publication or manuscript edit is authorized here.
