# Exact synthetic audit costs: source and recorded evidence

These files preserve one CPU experiment on a Windows 11 i9-14900HX, using
Zig 0.14.1 / C++17 -O3. They do not time the retained H20 auditor or establish
physical bias, GPU behavior, or an improved hardware choice. Every raw elapsed
time and all unfavorable/no-gain cases are retained. Input parsing and exact
validation are outside timing regions; closure, cheap flags and additional
quartets are separate preprocessing stages. The direct implementation consumes
the same closed ranking relation; a raw-edge direct implementation could avoid
closure and was not measured here.

The complete stream is primary; the beta-survivor stream is a conditional
diagnostic. Nine paired blocks on one host are repeated measurements, not nine
independent systems. Modeled setup-plus-query totals are computed from separately
measured stage medians, not new end-to-end timings. Quartets add marginal graph
pruning but this study does not establish an incremental runtime advantage.

Use the package-root run_r03_checks.py in a fresh extraction. It creates a
separate r03-replay directory. The standard-library default regenerates all
inputs, independently checks 37,440 small graph decisions and 22,658 feasible
original-variable witnesses against the retained validation CSV, audits every
recorded timing/order/checksum, and recomputes the summaries. Passing --zig with
an existing Zig compiler additionally rebuilds C++17 and runs validate on all
41,760 queries, checking all routes, separate Floyd, BF potentials and negative
cycles. No native executable or compiler is bundled. The replay never invokes
the time mode. Original scripts differ only in skipping absent files when
collecting provenance hashes; PORTABILITY_CHANGES.json gives both source hashes.

For a genuinely new timing experiment, use a separate fresh directory, copy the
scripts/protocols, execute generate_inputs.py, compile benchmark.cpp with a
C++17 compiler supporting signed __int128 and GNU inline asm, run benchmark
validate, run independent_check.py, and only then benchmark time. Re-run the
summarizer and final audit. Preserve the recorded run; the generator/summarizer
refuse to overwrite completed manifests. New elapsed times will vary by host.
