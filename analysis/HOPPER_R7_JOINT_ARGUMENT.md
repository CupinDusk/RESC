# Conditional joint-ranking characterization, written before new query execution

Input: one observed log rectangle l_i <= x_i <= u_i, theta_i=x_i-b_ji,
and a shared bias with adjacent increments bounded by delta. A common
additive shift is immaterial to ranking. No data-based physical delta is asserted.

## Exact projection and its established antecedent

Set t=-b. The inequalities theta_i-t_ji <= u_i and
t_ji-theta_i <= -l_i, together with |t_j-t_(j-1)|<=delta,
are ordinary difference constraints. Negative-cycle feasibility/shortest-path
closure is established DBM machinery (Mine, PADO 2001); it is not a new algorithm.
Eliminating t gives theta_b-theta_a <= D(a,b), where
D(a,b)=u_b-l_a+delta*|j_a-j_b| for distinct arms, D(a,a)=0.
These bounds are closed: an intermediate arm adds its nonnegative interval
width and a nonnegative triangle excess. Conversely, a theta satisfying
all bounds admits a Lipschitz selection from the bias intervals: take the
lower envelope max_i(l_i-theta_i-delta*|j-j_i|) for b_j, whose value
at each observed position is at most u_i-theta_i. Shift b and theta by
opposite common constants to set b_0=0. Thus no higher-order constraint was lost.

## Two disjoint comparisons on one shared trajectory

Claim E: theta_p<=theta_q AND theta_r<=theta_s, all four arms distinct.
Add zero-weight edges q->p and s->r to the closed D graph. A negative
simple cycle contains at most these two new edges. A cycle containing
one needs D(p,q)<0 or D(r,s)<0. A cycle containing both has minimum
weight D(p,s)+D(r,q). Consequently E is feasible iff all three quantities
are nonnegative. Equality permits ties; strict negativity rejects the
shared explanation. Individual witnesses must not be combined as though
they were one common path. General conjunctions use the same established
DBM procedure and an explicit negative-cycle certificate.

## Precise limit of reanchoring independent boxes

For box(a), replace the metric in D by |j_a-a|+|j_b-a|. This is the
exact interval projection. Candidate-centered boxes recover every
single-candidate winner-star query, but that theorem does not apply
to arbitrary conjunctions. For the cross cycle here, the box penalty is
delta times the sum of four distances to the common real anchor a.
Its minimum is attained between the two median positions and equals
delta*((j_max-j_min)+(j_mid_hi-j_mid_lo)). Individual box tests are
weaker than the path tests at every anchor. Therefore, when the two
individual path tests pass, the path cross cycle is negative, and this
best-box cross cycle is nonnegative, EVERY common-anchor box admits E
but no shared path admits E. This characterizes all-real-anchor failure
for this four-distinct-arm query family, not just a sampled set of anchors.

## Controlled fixture, no GPU observation

Positions 1,2,3,4, point log costs .015,0,0,.015, delta .01.
E is theta_1<=theta_3 AND theta_4<=theta_2. Individual feasibility margins
are .005 and .005. Path cross margin=-.01; best-box cross margin=.01.
The impossible path requires b_3-b_1<=-.015 and b_2-b_4<=-.015.
Together with b_1-b_2<=.01 and b_4-b_3<=.01, these sum to 0<=-.01.
Every anchor box admits E. This construction extends to equal endpoint
log costs a with delta<a<=2*delta: path cross=2*(delta-a)<0,
best-box cross=4*delta-2*a>=0. At a=delta the path admits a tie.

## Scope and checking

The new proposition delineates which queried correlations can be
recovered by reanchoring; it does not improve or invent general DBMs,
interval optimality, or Lipschitz optimization. All original retained
counts/calibration failures remain. The fixed protocol enumerates all
180 disjoint directed comparison pairs in each of 89 cells at all six
old budgets. Original x/b LPs independently check all 16020 queries
at log(1.02), with no outcome-based selection. The corpus is a conditional
example grid, not independently sampled tasks or hardware rank truth.
