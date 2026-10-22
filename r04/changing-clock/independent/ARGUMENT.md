# Independent argument for the specified changing-clock evidence

The executable check returned **PASS** on the serialized evidence. This is an independent mathematical and numerical certificate validation of a specified digital-source model. It is not a scientific peer review and establishes no RTL, silicon, GPU acquisition, physical calibration, execution overhead, workload prevalence, or application speedup result.

The checker reads the new `PROTOCOL.json`, `OBSERVATIONS.json`, `RESULTS.json`, compressed report stream, and slot-mapping addendum. It reads the prior R03 protocol's explicit slot mapping and was adapted from the prior independent validator. It never opens, imports, executes, or independently hashes the new producer `build_and_check.py` or `audit_core.py`. Source hash strings quoted inside `RESULTS.json` remain producer provenance claims; the independent manifest binds the serialized inputs and this checker separately.

## 1. Scope and inherited slot names

The prospective supplemental protocol fixes eight integer cycle-count vectors, six slots, reference multiplier 10000, guard 201/200, three legal multiplier formulas, path-specific timer rectangles, and all 720 orders plus one fixed partial per vector/path. The serialized evidence has exactly these 24 vector/path cases. The checker constructs the expected paths and vector set independently and verifies exact set coverage without filtering any outcomes.

The supplemental protocol originally listed numeric slots 1 through 6 while naming the partial report `P<=F,A<=S`. Its slot-mapping addendum was created after generation during validation. The checker reads the prior R03 protocol and verifies that both use `P=1,S=2,B=3,G=4,A=5,F=6`. Thus the named partial is exactly the serialized zero-based clauses `[(0,5),(4,1)]`. This repairs documentation of the inherited meaning; it is not prospective preregistration of that clarification, and does not change observations, rectangles, claims, or outcomes. Original supplemental protocol and evidence bytes remain bound by their hashes.

## 2. Exact source and controller obligations

Write the guard as `g=201/200` and let `M0=10000`. The checker constructs:

- rising: `Mj=10000*g^j`;
- falling: `Mj=10000/g^j`;
- alternating: `Mj=10050` for odd slots and `10000` for even slots.

Every adjacent edge, including the reference-to-first edge, obeys both `Mj/M(j-1)<=g` and its reciprocal. Indeed `max(Mj/M(j-1),M(j-1)/Mj)=g` exactly. These identities are checked using rational arithmetic for all 144 edges across the 24 cases. Unlike the older constant-path replay, these paths change at every edge and attain the declared boundary at every edge. This says nothing about a physical controller's ability to implement the formulas.

For each positive integer original cycle count `Ni`, the separately reset job, settled clock, and multiplier held throughout the command imply exactly

`Ti=Ni*10000/Mi`.

The checker derives all 144 durations from this algebraic model and compares them with the serialized rational durations. This is an exact model calculation, not measured timing or an independent implementation of job acquisition. For each case separately it derives

`Li=floor(Ti)-1`, `Ui=ceil(Ti)+1`.

It verifies the corresponding own-path rectangle, strict positivity, containment of `Ti`, and width two cycles for an integer duration or three for a noninteger duration. No minimum, maximum, or budget is fitted across paths. The timer enclosure is a specified interface assumption, not a demonstrated timer property.

Let `theta_i=ln(Ni)` and `b_i=ln(10000/Mi)`, with `b0=0` and `delta=ln(g)`. Then `theta_i+b_i=ln(Ti)` exactly and `|b_i-b_(i-1)|<=delta`. This supplies the mathematical reason the original integer ordering has a feasible model witness. Independent checks still require that every serialized true report was actually admitted.

## 3. Independent outward logarithm verification

All numerical bounds have integer scale `S=10^60`. No producer Decimal routine, binary floating point, mpmath routine, or external numeric package is used.

For positive rational `x`, the checker finds an integer `k` and rational `r` with `x=2^k*r` and `1<=r<2`. Put `z=(r-1)/(r+1)`, so `0<=z<1/3`. It evaluates 130 exact rational terms of

`ln(r)=2*sum_(j>=0) z^(2j+1)/(2j+1)`.

The omitted tail is nonnegative and at most

`2*z^261 / (261*(1-z^2))`.

The same expansion at `z=1/3` encloses `ln(2)`. Adding `k*ln(2)` with endpoint reversal for negative `k` gives a rigorous rational enclosure for `ln(x)`. Every such independent interval is narrower than `10^-100` and lies wholly inside its serialized scaled integer interval. All recorded intervals have width at most one scaled unit. The checker verifies the guard logarithm plus all lower/upper endpoint logarithms: 289 serialized bounds, covering 179 distinct rational arguments. The ratio-domain digit limits for durations are also checked.

This validates the claimed outward bounds themselves. It does not assume the producer's stated Decimal precision or guard was sufficient.

## 4. Independent graph decision and original-variable certificates

Set `l_i=ln(Li)` and `u_i=ln(Ui)`. From `l_i<=theta_i+b_i<=u_i` and Lipschitz drift, every feasible assignment obeys

`theta_j-theta_i <= u_j-l_i+|j-i|*delta`.

A ranking clause `theta_a<=theta_b` contributes an edge from `b` to `a` of weight zero. Total orders retain all 15 transitive ranking pairs, while the fixed partial retains exactly its two clauses.

These pair constraints also suffice up to a common additive shift: the intervals for `b_i` are `[l_i-theta_i,u_i-theta_i]`; pairwise separation by at most `|i-j|*delta` permits a Lipschitz selection, for example the maximum of all lower endpoint cones. The resulting path can be extended to slot zero and shifted so `b0=0`, shifting all `theta_i` oppositely without changing ranks or rectangle sums. Thus anchor normalization introduces no missing restriction on ranking feasibility.

The independent checker builds two integer graphs. The relaxed graph uses lower endpoints of the lower logarithms, upper endpoints of the upper logarithms, and the upper guard bound. The tightened graph uses the opposite endpoints and the lower guard bound. A fresh Floyd-Warshall closure checks both graphs for every record, for 34,608 closures. It does not reuse the producer's search routine or trust its reported status.

The decision rule is conservative:

- a negative cycle in the relaxed graph certifies rejection;
- feasibility of the tightened graph permits admission;
- otherwise the numerical decision is unknown.

Every admission is separately checked in the original variables, not accepted solely because of a graph decision: all six integer `theta` coordinates, seven integer `bias` coordinates, anchor zero, six tightened rectangle sums, six lower-bound Lipschitz inequalities, and every ranking clause are checked. This covers 6,360 admissions, 38,160 rectangle checks, 38,160 drift checks, and 95,218 rank checks.

Every rejection's serialized cycle is separately checked for valid node indices, directed continuity, and each edge's exact relaxed pair weight or a licensed zero-weight rank edge. Its weights must sum exactly to the serialized strictly negative total. This covers 10,944 cycles and 22,554 edges. A relaxed negative cycle would contradict any original-variable feasible witness, so its rejection is certified independently of the producer's search.

## 5. Box baseline and unresolved boundaries

For a real anchor `t`, the separate anchor boxes allow each arm a drift radius `delta*|i-t|`. For a required pair `a<=b`, box feasibility requires

`l_a-u_b <= delta*(|a-t|+|b-t|)`.

The minimum denominator over real `t` is `|a-b|`, attained between the two slots. Therefore the all-real-anchor threshold is

`beta_R=max(0,max_(a,b in report) (l_a-u_b)/|a-b|)`.

This quantifies each real anchor separately; it does not supply one common drift path or one witness shared by different anchors. The checker derives lower and upper rational threshold bounds for every record from the verified endpoint log bounds, checks the exact serialized rational thresholds, and independently applies `beta_upper<=delta_lower` for admission and `beta_lower>delta_upper` for rejection. It preserves the unknown case between them. All 17,304 thresholds are checked.

There are no unresolved graph or box decisions in this actual stream. This is an observed property of these inputs, not an instruction to resolve future boundaries. The checker exercises separate synthetic uncertainty controls: overlapping interval bounds produce graph `unknown` and box `unknown`, and exact box equality remains admissible under the weak comparison. These controls test the abstention branches; they are not additional clock observations or evidence of any prevalence of boundary cases. The minimum positive observed box margin is recorded exactly in `VALIDATION.json`.

## 6. Complete populations and actual results

The exact Cartesian population is 8 vectors times 3 paths times `(720 total orders + 1 partial) = 17,304` records. The checker verifies each permutation appears once per case and each fixed partial appears once per case, including all ties in the original `Ni` values. Truth is evaluated solely from those original integer counts, never from the distorted observations.

| Population | Reports | Admit | Reject | Numeric unknown | True reports admitted | Incorrect but admitted | Box admits / path rejects |
|---|---:|---:|---:|---:|---:|---:|---:|
| Total orders | 17,280 | 6,346 | 10,934 | 0 | 2,181 | 4,165 | 38 |
| Fixed partials | 24 | 14 | 10 | 0 | 3 | 11 | 1 |
| All audit records | 17,304 | 6,360 | 10,944 | 0 | 2,184 | 4,176 | 39 |

All 2,184 true reports are admitted and none is rejected. An incorrect-but-admitted report establishes compatibility with some allowed model witness, not correctness of its original cycle-count ranking. The 4,176 such admissions remain in the evidence. Per-case summaries and the aggregate producer counts are all recomputed and checked. There was no outcome-dependent replacement.

## 7. Failed-contract and mutation controls

The separate failed-contract path is exactly `[10000,10060,10000,10000,10000,10000]`. The forward edge at slot 2 violates `10060/10000<=201/200`, and the reciprocal edge at slot 3 violates the same bound. All other edges pass, so the exact bad-edge set is `[2,3]`.

The checker independently dispatches every 720-order-plus-partial report for all eight vectors. Because the guard fails, all `8*721=5,768` dispatches return `contract-unknown` before graph or box audit; the numerical audit count for this control is zero. These 5,768 are a separate contract population, not the 17,304 serialized legal-path audit stream. No theorem-based admit or reject is licensed for the control.

Nine executed mutation controls alter selected validation inputs or certificates: an inward-shifted logarithm bound, a changed duration, a changed rectangle endpoint, a changed witness anchor, a changed original-variable coordinate, a changed negative-cycle edge with its sum updated, a changed cycle total, a flipped truth flag, and a changed box threshold. All nine are detected by the corresponding independent predicates. These are predicate-level controls, not nine regenerated experimental datasets.

## 8. Reproduction and limits

Run the supplied checker with bundled Python 3.12, `-B -X utf8`. `VALIDATION.json` was created exclusively on the completed run; a repeat uses `--check-only` or a new unused output filename. The manifest records exact SHA256 hashes of the checked serialized inputs, inherited mapping source, checker, validation report, and explanatory files. It deliberately excludes independent hashing of forbidden producer sources.

The executable check completed with 157,431 assertions and no failures. These results validate only the specified model and serialized certificates. They establish no physical reset/settle/hold behavior, fixed-cycle property of real workloads, actual timer enclosure, GPU/RTL implementation, H20 observation, drift prevalence, or application performance claim.
