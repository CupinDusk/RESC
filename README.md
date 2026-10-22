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
