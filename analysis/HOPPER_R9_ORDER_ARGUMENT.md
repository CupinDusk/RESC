# Partial-ranking all-anchor radius and slot-span bound

This proof is recorded before executing the R9 checks. It extends the R8
two-claim result; it does not claim new general graph or isotonic algorithms.

Let observed arm i have independent log interval [l_i,u_i] and distinct
integer position j_i in 1..N. Let R be the transitive closure of a requested
acyclic non-strict ranking: (p,q) means theta_p <= theta_q. All optimization
answers concern relative costs; common gauge shifts are free.

For anchor a define r_i=delta*|j_i-a|. Eliminating the independently bounded
biases gives theta_i in [l_i-r_i,u_i+r_i]. An isotonic interval selection
exists iff l_p-r_p <= u_q+r_q for every (p,q) in R. Necessity is immediate.
For sufficiency choose theta_q as the maximum of lower endpoints over q and
all its predecessors. Transitivity makes this isotonic and the pairwise
conditions put it below each upper endpoint.

Consequently the minimum budget at a is the maximum of zero and
(l_p-u_q)/(|j_p-a|+|j_q-a|) over R. The supremum over real a commutes with this
finite maximum. Triangle inequality gives a denominator >=|j_p-j_q|,
with equality at every a between these two positions. Thus

    delta_box_all = max(0, max_R (l_p-u_q)/|j_p-j_q|).

This is the minimum delta for which EVERY real-anchor box admits the full
ranking, with a different allowed witness for each anchor. It is not a
requirement for a single witness belonging to all boxes.

The projected shared-path bounds are theta_b-theta_a <=
D(a,b)=u_b-l_a+delta*|j_a-j_b| (D(a,a)=0). This graph is already closed:
D(a,c)+D(c,b)-D(a,b) is interval width at c plus a nonnegative triangle
excess. Add a zero edge q->p for every (p,q) in R.

Any negative cycle contains a negative simple cycle. Among such cycles take
one with the fewest edges. Consecutive D edges can be replaced by a closed
D edge of no greater weight, and consecutive ranking edges can be replaced
by one transitive ranking edge. The new cycle remains negative and shorter,
so a minimum-edge negative simple cycle must alternate. If an edge admits
both interpretations, choose the interpretation used in the cycle; the
same compression argument applies to every consecutive pair of one type.

For k=1 this is a single ranking pair and its reverse D edge, whose radius
is bounded by delta_box_all. For k>=2 the alternating simple cycle has2k
distinct endpoints. Write its ranking pairs (p_i,q_i), with observation
edges p_i->q_(i+1), cyclically. Its weight is

    -sum_i(l_pi-u_qi) + delta*sum_i |j_pi-j_q(i+1)|.

Let beta=delta_box_all. Each deficit <=beta*|j_pi-j_qi|. Among2k distinct
integer slots in1..N, the sum of k matching distances is at most the sum of
the k largest selected slots minus the k smallest, at most k(N-k).
Every crossed distance is at least1. Hence for delta=(N-2)*beta,

    cycle weight >= -beta*k(N-k) + beta*(N-2)*k >=0, since k>=2.

Thus no negative cycle exists at this budget. Every path witness can be
interpolated/extended Lipschitzly to any real anchor a and gauge-shifted to
zero there, so it belongs, modulo gauge, to Box(a). This gives the lower
bound beta<=delta_path. For N>=3,

    beta <= delta_path <= max(1,N-2)*beta.

For N2 there is at most one nontrivial partial-order pair and equality
holds; the max(1,N-2) convention also covers it. If beta=0 all cycle deficits
are nonpositive and budget0 is feasible.

For N>=4 sharpness follows from R8's two disjoint claims at p1,qN-1,rN,s2,
log centers (t,0,t,0) and common half-width epsilon<t/2. There are no extra
implied comparisons, beta=(t-2epsilon)/(N-2), path=t-2epsilon. This proves
sharpness over all partial rankings, not sharpness within every total-order
subfamily or a claim that every interval algorithm loses this factor.

The transitive-closure requirement is substantive. The R8 reviewer3
diagnostic has positions(p,q,r)=(1,2,3), point logs(0,.01,-.02), claims
q<=p and p<=r. Testing only those supplied pairs gives .01, whereas the
implied q<=r needs .03, and both the all-anchor full-ranking radius and
shared-path radius are .03. It also refutes extending the one-direction
winner-star theorem to arbitrary mixed-direction stars.

Published context retrieved for R9: Agarwal, Phillips and Sadri,
Lipschitz Unimodal and Isotonic Regression on Paths and Trees,
arXiv:0912.5182. Full PDF retrieved; abstract, Sec1 problem statement and
Sec2 definition inspected. They optimize squared fit error of a function
subject to prescribed Lipschitz/isotonic constraints. Our conditional
question minimizes a latent bias-path budget for an interval-valued cost
decomposition and quantifies a specified marginal-box relaxation. This
comparison is not an exhaustive novelty guarantee and does not claim
general isotonic feasibility, closure or fitting as new.
