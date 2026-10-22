# Conditional identification from a fixed arm order

This is a secondary mathematical/optimization audit of the already public retained H20 numeric matrix. There are zero new native measurements. It does not repair the original fixed-order acquisition or the absence of an untouched complete-policy test. The result is a conditional sensitivity function, not a discovered amount of physical drift or a corrected GPU timing.

## Observation and uncertainty set

For a single configured cell, each candidate arm p has one fixed measured position j(p). The source order is floor0, peer pull1, push store2, bulk push3, global4, async store5, flat pull6. Six communication arms are candidates; the floor is not. Let x_p be the log of a retained selected timing summary, and write x_p=theta_p+b_j(p), where exp(theta_p) is a hypothetical same-state cost UNDER THIS MODEL. Fix b_0=0 to remove an irrelevant common offset. For a sensitivity parameter delta>=0, assume |b_(j+1)-b_j|<=delta. This is a restriction per adjacent order position, not per wall-clock second or a measured clock/temperature law. Path-specific state interactions and arbitrary carryover can violate it.

Use either one retained min/mean/max/primary value (L_p=U_p), or the artificial observed-summary rectangle x_p in [log L_p,log U_p], with L/U the selected raw minimum/maximum independently for each arm. The rectangle is not the joint distribution of repetitions, does not imply simultaneous extrema, and is neither a confidence interval nor future coverage. The assumed drift bound applies to the chosen statistic/model, not automatically every physical observation.

## Sharp pair support and fixed-choice regret

For distinct p,q, let d_pq=|j(p)-j(q)|. Then

    sup(theta_p-theta_q)=log(U_p/L_q)+delta*d_pq.

The upper bound follows by interval endpoints and telescoping the bounded adjacent differences. It is attained by x_p=log U_p, x_q=log L_q and a bias path with b_q-b_p=delta*d_pq; extend the path with slope of magnitude at most delta and shift it to b_0=0. Other x values can be arbitrary within their rectangles. Thus this is sharp in the declared uncertainty set. It need not describe a physically achievable GPU state.

The self contrast p=q is exactly0, not log(U_p/L_p). The worst log regret of a fixed selected p is

    rho_p(delta)=max(0,max_(q!=p)[log(U_p/L_q)+delta*d_pq]).

Indeed log regret=theta_p-min_q(theta_q)=max_q(theta_p-theta_q), and a finite maximum commutes with the supremum. Only the maximizing rival's witness is needed. The support witnesses for every rival need not co-occur. exp(rho_p) is the sharp multiplicative ratio bound in this uncertainty set. At delta0, the easy envelope U_p/min_q L_q can be loose because it may treat p's own timing in numerator and denominator as two independent quantities. It remains a conservative envelope; this audit does not claim that the earlier labeled envelope was a false calculation.

For n arms, n(n-1) pair scores determine all risks in O(n^2). A descriptive minimax audit chooses argmin_p rho_p, with the fixed arm tie order. It uses ALL measured arms in the cell and is not a heldout predictor, acquisition saving, deployed policy or independent validation of the earlier bilinear selector. General minmax-regret optimization and support-function calculations are established methods; this is a specialization to the retained-order/summary model.

## Possible and guaranteed winners

Arm p is a possible minimizer iff for every q,

    log(L_p/U_q)<=delta*d_pq.

Necessity follows from the same bounded difference. For sufficiency choose x_p=log L_p, all rivals x_q=log U_q, and the single cone b_j=-delta*|j-j(p)|, shifted to make b_0=0. It has adjacent slope at most delta and makes p no slower than every rival simultaneously. This witness is important: pairwise feasibility does not imply simultaneous feasibility for arbitrary correlated uncertainty sets, but it does for this path/cone model.

Arm p is a guaranteed minimizer iff rho_p=0, equivalently log(U_p/L_q)+delta*d_pq<=0 for every distinct q. Strict inequalities give a unique guaranteed winner. A separated nominal winner remains unique for delta strictly below

    min_(q!=p) log(L_q/U_p)/d_pq.

At the boundary a tie can occur. Negative thresholds mean it is already not guaranteed at delta0 in the summary rectangle. They are not negative physical drift. With no finite drift bound, any chosen vector theta is compatible with the observed x by setting b_j(p)=x_p-theta_p. Hence every candidate can be made uniquely best. Narrow observed ranges alone do not identify a same-state ranking.

## Scope of aggregation

Bias paths are allowed to vary independently across configured cells. Thus the geometric mean of each cell's sharp fixed-policy ratio bound is also the sharp bound for that chosen collection under the product uncertainty model; the corresponding within-cell witnesses can be chosen separately. The maximum bound is immediate. This does not treat cells as independent statistical samples, identify a population effect, or support application/generalization claims.

The original bilinear model and its flat fallback remain fixed choices from an already inspected corpus. The original C2/C4 calibration versus C8 split, features, admission and fallback were designed after C8 inspection. The present sensitivity audit does not fix that exposure. It evaluates these frozen choices as objects of a conditional audit and does not refit them under a favorable test-time perturbation.

## Execution and examples

The chosen finite grid is adjacent multiplicative drift0,0.5%,1%,2%,5%,10%, with delta=log(1+fraction). No grid value is inferred as true. The primary/minimum/mean/maximum point models and the summary rectangle are reported separately. The 89 cells contain623 retained arm rows;35 C8 choices include19 admitted and16 unsupported. Existing per-case identities, all unfavorable cases and raw-block bindings remain.

A separate linear program has six x variables within their log intervals and seven bias variables, b0=0 and twelve adjacent-difference inequalities. At delta=log1.02, maximizing every ordered distinct pair in every cell for point/rectangle models gives5,340 support checks. Adding the five constraints theta_p<=theta_q for every candidate gives1,068 possible-winner feasibility checks. The largest support difference is1.84e-15, with zero observed disagreements. These are independent numerical checks of the specified optimization model, not GPU validation or a machine-checked general proof.

In the rectangle at drift0,33/35 C8 cells have a guaranteed unique winner; at assumed2% per position,20/35 do. Across all89 cells, those counts are85 and55. Flat is guaranteed faster than peer pull in22/35 many-to-one cells at drift0,16/35 at assumed2%, and7/35 at assumed10%. At C8/B32, U_flat/L_peer=831.8/1917.6; its flat-versus-peer guarantee reaches a tie at18.181% adjacent drift across the five-position separation. That large threshold is NOT an estimate that real order bias is smaller than it. Other arms, including push, remain candidates.

For the frozen original policy, the sharp summary-rectangle geometric regret bounds at drift0 are1.00482889 on the19 admitted cases and1.08814645 on all35. At assumed2% they are1.02242471 and1.12645379; maxima are1.14937739 and2.29927243. Original point regrets remain1.00431782 and1.08267879. These are sensitivity envelopes conditional on the uncertainty set, not corrected performance or prospective prediction accuracy. The full report contains all grid values and per-case witnesses/choices. Later manuscript use must keep these distinctions explicit.
