# R10 conditional arithmetic and complete-order sharpness

The protocol was fixed after all four R9 PDF-only reviews (all4/6), before
examining new width-neighborhood counts or executing the new checks.
No new hardware inputs were collected. Existing R9 numerical reports and
all negative external/stationary evidence remain unchanged historical inputs.

`hopper_exact_certificates.py` interprets the published min/max timing
strings as exact positive decimals. Correctly rounded 80-digit Decimal.ln,
adjacent representable neighbors, and outward rounding to a1e-60 grid
enclose the true logs. Multiplication by60 makes all six-slot pair-distance
divisions integral. Subsequent calculations are exact Python integers.
The declared resolution is eta=1e-8 in log-budget units. This is neither an
LP error estimate nor a physical uncertainty bound.

All64080 complete-order cases receive a checked negative-cycle or feasible
potential certificate:7586 have true window width greater than eta,56494
have width at most eta,0 ambiguous. A certificate file is regenerated,
not bundled, with SHA-256
d996c287eb3c5538c0995d26d916dae87751369e00d55cc4e809a70f708b8fa4.
The smallest positive-window lower bound from the exhibited cycles is
1.2484398026080802e-5, over1200times eta. Replaying the saved certificates
checks every edge and reproduces the full partition without a numerical
LP solver. The remaining cases are not asserted to have exactly zero width.

Descriptive thresholds1e-12/1e-10/1e-9/1e-8 on the historical floating CSV
all give7586; these counts alone would not certify signs. Outward interval
checks at every original fraction0/.005/.01/.02/.05/.10 leave all TableI
counts unchanged and have no ambiguous cases: total-order questions
0/2/11/27/188/635 in0/2/6/14/48/78 cells; two-disjoint questions
0/2/11/18/102/286 in0/2/8/14/48/82 cells. Queries are dependent and
not prevalence, physical-error or wrong-device-ranking rates.

`hopper_full_order_tightness.py` strengthens the bound's attaining family:
every one of the N slots has an arm and the requested ranking is complete.
The positive-width construction is specified in the accompanying argument.
Exact Fraction checks verify all implied comparisons, every endpoint and
the adjacent-bias witness. Prespecified N4/5/6/8/16/32/64 and widths
0/.001/.004 give21 cases. Cross-checks use21 original path-minimum LPs,
852 anchored-box minimum LPs and5238 fixed-budget feasibility LPs.
Maximum radius discrepancies are1.735e-18(path) and8.674e-19(box);
maximum LP-witness ranking violation is1.128e-17. Original-variable LPs
are corroboration; the rational construction is the analytic witness.

These calculations validate conditional arithmetic under the supplied
rectangles and path model. They do not establish adoption of an all-anchor
independent-box reporting workflow, true H20 bias, acquisition correctness,
same-state costs, a causal ordering effect, or improved implementation
choices. Generic graph-Lipschitz extension, minimax isotonic regression,
difference-bound feasibility and inverse optimization are prior machinery.
The new object is the sharp all-anchor marginal/shared-path radius ratio.
