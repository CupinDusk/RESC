# Independent author-side check of the declared clock construction

The specified model and all serialized outcomes pass this independent check. This is an author-side mathematical and artifact check, not an external paper review or a physical GPU experiment. The validator reads the protocol, numeric addendum, rational observations, result summary, and all compressed report records. It does not read, import, or run `check_clock_contract.py`. Only Python standard-library integers and exact `Fraction` arithmetic are used; no packages, network access, timing measurements, or remote execution are involved.

## What follows from the controller contract

Command slot `j=i+1` runs a reset job with fixed cycle count `N_i`. Its multiplier `M_j` is settled before the timed interval and held throughout that interval. One job cycle lasts `10000/M_j` reference cycles. Summing those exact rational cycle lengths gives

`T_i = N_i * 10000/M_j`, hence `log T_i = theta_i+b_j`,

where `theta_i=log N_i`, `b_j=log(10000/M_j)`, and the reference multiplier gives `b_0=0`. The bidirectional rational guard implies

`|b_j-b_(j-1)| = |log(M_(j-1)/M_j)| <= log(1005/1000) = delta`.

The guard budget is independent of observations. The validator checks all 144 controller edges by cross multiplication, including each reference-to-first transition. It independently accumulates 144,915,000 cycle-length numerators, then divides by the held multiplier once per job, reproducing all 144 declared rational durations. All 48 positive min/max rectangles are checked exactly. The original `theta=log N` and each actual replay satisfy the rectangles by the multiplicative identity above and exact rational containment, not by a fitted numerical estimate.

These conclusions are conditional on fixed cycle counts, resets, settling, and the multiplier being held during the timed interval. Reset/settling overhead is outside that interval. They establish none of those properties for a real device.

## Independent logarithm enclosures

For each positive rational input, reduce it exactly as `x=2^k r` with `1<=r<2`. Set `z=(r-1)/(r+1)`, so `0<=z<1/3`, and use

`log r = 2 sum_(j=0)^129 z^(2j+1)/(2j+1) + R`.

The exact rational tail satisfies

`0 <= R <= 2 z^261 / (261 (1-z^2))`.

The same series at `z=1/3` encloses `log 2`. Multiplying its interval by the signed integer `k` and adding the reduced interval yields a rigorous rational enclosure of `log x`. Every independent enclosure has width below `1e-100` and lies inside the recorded integer interval in units of `1e-60`. This verifies all 97 recorded logarithm enclosures (96 rectangle endpoints plus the guard), covering 33 distinct rational logarithms. It does not assume the original Decimal implementation or its claimed rounding margin is correct.

## Common-path feasibility and certificates

For any fixed `theta`, a bias at slot `i` must lie in `[l_i-theta_i, u_i-theta_i]`. A Lipschitz selection exists exactly when every pair of these intervals obeys

`theta_j-theta_i <= u_j-l_i+|j-i| delta`.

One constructive direction takes the maximum of the lower endpoint cones `l_i-theta_i-delta|s-s_i|`. The pair conditions place its value in every interval at the observed slots. A common shift of every `theta_i` and the opposite shift of the bias function sets `b_0=0` while preserving observations and rankings. Thus the six-node difference graph is valid for this anchored model: an observation edge is `i -> j` with weight `u_j-l_i+|j-i|delta`. The ranking `theta_a<=theta_b` adds `b -> a` with weight zero. This orientation was independently reconstructed and checked.

The validator constructs fresh tightened and relaxed graphs, then performs 11,536 all-pairs shortest-path closures: two for every report. Tightening uses `l_upper`, `u_lower`, and `delta_lower`; relaxing uses `l_lower`, `u_upper`, and `delta_upper`. A feasible tightened graph certifies admission, a negative relaxed cycle certifies rejection, and any unresolved case is explicitly classified `unknown`.

Serialized certificates are checked separately. All 3,677 admitted reports have integer original-variable witnesses satisfying all tightened rectangles, every Lipschitz edge including the anchor, and every ranking. All 2,091 rejected reports have closed cycles whose 4,414 edges match a relaxed observation edge or a correctly oriented zero-weight ranking edge, with strictly negative total weight. The cycle verification does not merely trust the original status or total. There are no unresolved cases in these inputs.

## Meaning of the all-anchor box baseline

The baseline quantifies every real anchor separately. At anchor `a`, the box is `|b_j|<=delta|j-a|`, and its witness may depend on `a`. It does not require one common witness across anchors.

With a report's transitive ranking closure `R`, feasibility in this box is equivalent to

`l_p-u_q <= delta (|j_p-a|+|j_q-a|)` for every `(p,q)` in `R`.

For any pair, the denominator is at least `|j_p-j_q|` by the triangle inequality, and equality holds at every anchor between the two slots. Since the report has finitely many pairs, taking the supremum over all real anchors therefore gives

`sup_a beta_R(a) = max(0, max_((p,q) in R) (l_p-u_q)/|j_p-j_q|)`.

The validator independently recomputes both outward bounds of this expression for all 5,768 reports. Total-order records use all 15 transitive pairs. Using only the five adjacent clauses would weaken this box baseline. The independent formula and classifications match every recorded `beta_lower`, `beta_upper`, and `box` status. Thus the separation is against the every-real-anchor baseline, not only the reference anchor.

## Results reproduced

| Report set | Reports | Admit | Reject | Unknown | True / admitted | Incorrect but admitted | All-anchor boxes admit, common path rejects |
|---|---:|---:|---:|---:|---:|---:|---:|
| All total orders | 5,760 | 3,672 | 2,088 | 0 | 727 / 727 | 2,945 | 14 |
| Fixed two-clause reports | 8 | 5 | 3 | 0 | 1 / 1 | 4 | 2 |
| Combined | 5,768 | 3,677 | 2,091 | 0 | 728 / 728 | 2,949 | 16 |

The all-anchor box baseline admits 3,693 reports, rejects 2,075, and leaves zero unknown. All 720 total orders for each of the eight vectors are present exactly once, as is the fixed partial report for every vector. Truth is computed from the original integer cycle counts. The tied vector accounts for 720 true total orders; the seven distinct-valued vectors add one each. All summaries and serialized partial reports agree with the independently counted records.

For predeclared case 0 and report `P<=F, A<=S`, the all-anchor threshold is approximately `0.0045220652544937642`, the independent controller budget is approximately `0.0049875415110390736`, and the four-arm cycle threshold is approximately `0.0056840965500707850`. These decimals are explanatory only; validation decisions use exact bounds. The cycle is `F->P->S->A->F`, with the two zero-weight ranking edges and total

`2 delta + u_S-l_P+u_F-l_A`.

Its relaxed integer total is `-1393110078063422686339983602860165751932815743525970203342` in units of `1e-60`, so even the relaxed graph is infeasible. The exact outward enclosures prove `beta_R < delta < cycle_threshold`. The fixed partial also separates in case 7; the other six fixed partial outcomes are retained.

## Semantic limits and wording

No mathematical false claim was found in the supplied artifacts under their declared model. The evidence demonstrates a constructive model instance and exhaustive checking of a fixed, finite report domain. It supplies no scientific reproduction, hardware validation, inference about the H20 observations, execution overhead, measurement distribution, or prevalence of such a separation.

All three replay paths are constant after the first boundary. They satisfy the contract but do not stress its intermediate-boundary limit or establish its tightness. The rectangles deliberately abstract the three exact modeled replays; their endpoints are not estimates of experimental noise. Admission establishes compatibility with the abstraction and does not certify the original cycle-count truth: 2,949 incorrect reports are admitted.

The protocol's phrase “Measured normalized duration” must be understood as the duration in the stipulated model. Calling these actual measured hardware durations, or claiming that clock settling and fixed cycles were established for GPUs, would exceed this evidence. Splitting commands or changing what is timed requires transforming the controller contract and its boundary budget.

`VALIDATION.json` binds the input and validator hashes, records exact counts, and preserves the empty failure list. Re-run `validate_clock_independently.py` with bundled Python `-B -X utf8`; it writes only `VALIDATION.json` beside this argument.
