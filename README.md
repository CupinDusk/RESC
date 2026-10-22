# Reproduction artifact: Sharp Ranking-Specific Bounds for Timing Consistency

This snapshot supplies the analysis code, explicit model assumptions, retained
numerical summaries, protocols, expected outputs, and checks for the paper.
It does not contain the manuscript, private implementation overlays, GPU
acquisition programs, server configuration, credentials, or third-party raw CSVs.

## Reproduce

Requires Python 3.12, NumPy 2.3.5, and SciPy 1.16.3.

    python -B -X utf8 run_checks.py --scipy-path /absolute/scipy/module/path

Run the checks in a fresh extraction. The manifest lists every input and SHA-256.
The calculations and expected outcomes, including unfavorable and zero results,
are unchanged from the source research snapshot. Historical release-management
READMEs are omitted; the numerical and argument history remains in analysis/
and expected/. No native hardware experiment is performed by this artifact.

Third-party source headers, copyright notices, and licenses are preserved
verbatim. External data fetching is optional and requires an explicit flag;
the default checks use only bundled numerical summaries.

The authors intend to release the research code under an open-source license
upon publication. This review snapshot is an accessible reproduction package;
it does not claim that every private project component has been released.

## Joint explanation and admission-route checks

`make_separate_witnesses.py` checks two exact rational bias paths that each
satisfy one comparison, and the negative-cycle certificate for their conjunction.
`route_ablation.py` joins all 384,480 retained certified routes and compares
the universal ceiling, quartet flag, their union, and the full ranking factor.
These are mathematical witnesses and graph-fallback counts, not new GPU
measurements or measured runtime. All zero and unfavorable outcomes are retained.

## Settled-clock construction and exact CPU auditor costs

The r03/ extension adds a stipulated digital settled-clock model with exact
rational observations, outward logarithm certificates and a fully separate
Fraction validator. It also adds a prospective exact synthetic CPU-auditor
experiment: all 720 six-arm total orders plus 150 scaling plans, 41,760 queries,
all 5,049 raw timing records, and complete negative/no-gain outcomes. These are
distinct from the retained H20 data and do not calibrate physical GPU drift.

Run the new checks from a fresh extraction using Python 3.12 standard library:

    python -B -X utf8 run_r03_checks.py

To additionally rebuild and validate every C++ query with an existing compiler:

    python -B -X utf8 run_r03_checks.py --zig /path/to/zig

Use a new extraction for each run. The script writes r03-replay/ and refuses to
overwrite completed results. It never collects new timings. The complete clock
certificate stream is regenerated and checked against its uncompressed SHA-256.
Recorded timings are audited, not represented as a repeated benchmark. Three
metadata-only script adaptations and one metadata field removal are documented
in r03/PORTABILITY_CHANGES.json. All earlier public analysis, copyright notices
and licenses remain byte-identical; this command does not rerun that separate
older suite. The older run_checks.py remains available with its stated numerical
library dependencies.

The authors will release the research code under an open-source license upon
publication. This review snapshot contains the reproducible research materials
described above; it does not imply release of private implementation components.

## Changing-clock certificates and complete Boolean jobs (R04)

The additive r04/ directory retains the full specified changing-clock study:
24 vector/path cases, 17,304 reports, 6,360 original-variable admission
certificates, 10,944 negative-cycle rejection certificates, and 5,768 separate
failed-contract dispatches. All 4,176 incorrect but compatible admissions remain.
Its exact independent Fraction/atanh/Floyd checker validates all 289 log bounds,
certificates, adverse outcomes and nine mutation controls. The inherited named
slot mapping was clarified after generation; the addendum is retained honestly.

The complete-job study retains all 870 plans, 41,760 distinct queries, 5,508 raw
elapsed intervals, the seed/order schedule, all 50 scaling strata, original C++
core and driver, independent graph source/output, summaries and audit records.
It measures one synthetic Boolean CPU implementation on one Windows host,
including route-specific setup. It establishes no GPU, RTL, H20 outward-auditor,
certificate-service latency or application speedup. The Q192 quartet/cheap
comparison includes its recorded tie: 3 faster / 5 slower / 1 tie. All adverse
results are included; ranges describe nine paired block averages, not confidence
intervals or individual request latencies.

From a fresh extraction, using Python 3.12 standard library only:

    python -B -X utf8 run_r04_checks.py

To additionally rebuild both C++ correctness paths with an existing Zig compiler:

    python -B -X utf8 run_r04_checks.py --zig /path/to/zig

The default verifies every manifest byte, regenerates the complete changing-clock
certificate stream and compares uncompressed bytes, runs the independent clock
checker, reconstructs every saved timing/order/hash/summary, audits all recorded
independent graph decisions, and regenerates source inputs/core/schedule in a
separate directory. Optional compilation validates all 41,760 queries in both
source and independent graph implementations, without timing. No compiler or
executable is bundled. The saved historical PE/source binding is retained as
evidence but cannot be reverified without the omitted historical timed binary.

The command creates r04-replay/ and refuses to overwrite previous attempts.
It never invokes a time mode and does not rerun the unchanged earlier SciPy
suite. Historical prepare/run_once/check_complete scripts remain source evidence;
use the package-root runner for portable replay. Only separate portable copies
adapt workspace-relative paths and omitted-binary provenance; one historical
native command record removes private installation paths. Exact hashes and each
change appear in r04/PORTABILITY_CHANGES.json and ORIGINAL_INPUT_BINDINGS.json.
All original R03 public research and license bytes remain unchanged, except this
appended README and the extended manifest.

## R05: logical RTL and designed exact-family cost

The additive r05/ directory contains the own RTL/CXXRTL source, fixed schedules,
complete logical traces and certificates, independent edge/graph/mutation
checkers, all 720 new CPU queries, all 2,160 unchanged original timing rows and
all negative cells. See r05/SCOPE.md and both independent/PAPER_READY_FACTS.md.

Fresh Python3.12 stdlib replay (isolated mode supported):

    python -I -S -B -X utf8 run_r05_checks.py

Fresh actual correctness builds with already installed external tools:

    python -B -X utf8 run_r05_checks.py --zig /path/to/zig --yosys /path/to/yosys --include /path/to/yosys/include

For an installed Python YoWASP wrapper, use --yosys-python-wrapper instead of
--yosys. Nothing invokes performance mode. Prior evidence remains exact;
old SciPy legacy scope is not rerun. The runner refuses to overwrite an attempt.
