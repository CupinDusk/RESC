# Minimum explanation budget and sharp all-anchor loss

Written after identifying R7's redundant median condition, before new
radius outputs. All comparisons below mean non-strict simultaneous
comparisons on ONE shared nuisance trajectory and one observed rectangle.
No physical budget is inferred. Negative-cycle feasibility is established
DBM machinery; general min-cycle-ratio optimization is not claimed new.

For E=(theta_p<=theta_q AND theta_r<=theta_s), four distinct arms, define
a=l_p-u_q, b=l_r-u_s, d1=|j_p-j_q|, d2=|j_r-j_s|,
c=|j_p-j_s|+|j_r-j_q|, all distances positive. R7's exact cycle tests imply

    delta_pair=max(0,a/d1,b/d2)
    delta_joint=max(delta_pair,(a+b)/c).

Thus the exact discrepancy window is [delta_pair,delta_joint): every
individually feasible comparison is admitted by EVERY independent anchor
box (factorization over four independent coordinates), yet the shared
path rejects their conjunction. R7's median inequality is automatic and
is not an additional condition/result. For a fixed box anchor z, its
minimum feasible budget is max(0,a/(|j_p-z|+|j_q-z|),
b/(|j_r-z|+|j_s-z|)). Its supremum over ALL real anchors is exactly
delta_pair: each term's denominator attains its minimum own distance
between its two endpoints, and a finite max commutes with supremum.
This is the strongest lower budget bound obtainable even from all these
box feasibility answers. It may be strictly smaller than delta_joint.

## Sharp finite-slot factor and lack of a universal constant

Four distinct integer slots lie in1..N, N>=4. If delta_pair=0, then a<=0
and b<=0, hence delta_joint=0. Otherwise

    (a+b)/c <= delta_pair*(d1+d2)/c.

Any two disjoint distances sum to at most (v4-v1)+(v3-v2)<=2N-4,
where v1<v2<v3<v4 are the selected slots. Cross distance c>=2.
Therefore delta_joint/delta_pair<=max(1,(d1+d2)/c)<=N-2.
This is a tight statement for the stated query family and contiguous
integer slot range, not a general graph approximation theorem.

Tight family: slots p1,q=N-1,r=N,s2, log centers x_p=x_r=v,
x_q=x_s=0 and equal symmetric log half-width epsilon in[0,v/2).
a=b=v-2epsilon>0, d1=d2=N-2, c=2, so
delta_pair=(v-2epsilon)/(N-2), delta_joint=v-2epsilon. The ratio is
N-2 even with positive-width rectangles. No constant independent of slot
span can bound the underestimation. A fixed number of observed arms can
also occupy far-separated slots in a longer episode; N counts slots,
not just compared arms. This is a controlled analytical construction.

Operational question: the audit reports the minimum shared bias budget
needed for a proposed joint ranking explanation. If a defensible/sensitivity
budget is below delta_joint, that explanation is impossible under the
model. Boxes can report it possible as early as delta_pair. Rejected
conjunctions do not identify which single inequality is actually false,
nor calibrate a device. The known controlled reference b=0,theta=center
makes both proposed comparisons false, but the audit still quantifies all
alternative admitted explanations, not only that reference.

## Not restricted to an artificially isolated narrative

A controlled full-ranking example has point log costs at slots1..4 equal
(.009,0,0,.018), target order1<=3<=4<=2 and delta.01. Every comparison
implied by this order passes its individual path test; each common-anchor
independent box admits the full order, but the shared path rejects it.
The subclaims1<=3 and4<=2 already have cross-cycle deficit .027 and
cross distance2, requiring at least .0135. This fixture illustrates the
same common-witness error in a complete ranking, not a new general
partial-order algorithm. Independent LP checks must verify this prediction.

## Evidence boundaries

All retained16020 unique queries receive continuous radii and affected-cell
identities, not only counts repeated across six budgets. LP minimization
of delta uses original x/b/delta variables; boundary feasibility and
midpoint checks include tolerances/near-zero records. All prior selected
H20 minima, counterbalanced-data absence and secondary CPU/filesystem
calibration failures remain. Novelty/significance must rest on the scoped
inverse-budget/quantitative-loss result and its transparent use, not on
the number of LPs or a new hardware claim.
