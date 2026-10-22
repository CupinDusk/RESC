# Candidate exact worst-case factor for a fixed ranking

Saved before computation. This is an editor research argument, not an
established result until the proof is scrutinized and the planned checks
agree. It uses established assignment duality and difference constraints;
the candidate new object is the exact loss of the specified marginal
relaxation for one retained ranking. No real archive adoption is asserted.

Let R be the strict-pair transitive closure of a non-strict acyclic ranking
on n arms at distinct integer positions j_i. For disjoint nonempty sets
P,Q of equal cardinality, let M_R(P,Q) be the minimum total |j_p-j_q|
of a perfect matching using only pairs (p,q) in R. Ignore sets without
such a matching. Let M_all(P,Q) use unrestricted bijections. All costs
are positive, so their ratio is well defined. Define C_R as the maximum
of 1 and these ratios. An empty ranking has C_R=1 and beta_R=delta_R=0.

## Universal upper bound

At any negative cycle in the closed projected difference graph, contract
data runs by closure and ranking runs by transitivity. A reduced simple
alternating cycle uses disjoint sets P and Q of endpoints and one R-perfect
matching f: q_i -> p_i. Its data edges form another perfect matching g
from P to Q, with total distance d(g). Its observation deficit is

    H(P,Q) = sum_{p in P} l_p - sum_{q in Q} u_q.

For EVERY R-perfect matching h, the implied-pair definition of beta_R gives
l_p-u_h(p) <= beta_R |j_p-j_h(p)|. Summing and minimizing over h gives
H(P,Q) <= beta_R M_R(P,Q). The data matching has distance at least M_all,
so the required normalized cycle radius is at most C_R beta_R. Thus no
negative cycle exists at delta=C_R beta_R, and delta_R<=C_R beta_R.
The prior all-anchor relaxation gives beta_R<=delta_R. If beta_R=0,
all cycle deficits are nonpositive and delta_R=0.

This proof does not require unrestricted and R-restricted optimal matchings
to form a single cycle: every actual reduced cycle already has the two
perfect matchings. In particular, the subset ratio cannot underbound
the true worst-case factor.

## Attainment by a positive-width rectangle

Suppose C_R>1 and take maximizing P,Q. Assignment duality supplies
potentials lambda_p, mu_q such that lambda_p-mu_q<=|j_p-j_q| for every
allowed R edge from P to Q, with sum lambda - sum mu=M_R. For integer
costs an integer optimal dual exists. The experiment will independently
verify both primal matching and every dual inequality/objective exactly.

Set l_p=lambda_p on P and u_q=mu_q on Q. Set every other lower endpoint
to -M and every other upper endpoint to +M, with M larger than all
potential magnitudes plus the maximum distance. Since P and Q are
disjoint, every interval has strictly positive width; all other ranking
deficits are nonpositive. Hence beta_R<=1. Along an optimal R matching,
the nonnegative dual slacks sum to zero, so each is tight; its positive
distance gives beta_R=1.

Take any optimal R matching f and unrestricted matching g. Their union
decomposes into alternating closed cycles. The sum of the data-edge and
zero ranking-edge weights is

    -M_R(P,Q) + delta M_all(P,Q).

It is negative below delta=C_R, so at least one cycle is negative and
delta_R>=C_R. The proved upper bound gives delta_R=C_R. At equality a
rational feasible projected potential exists. The checker constructs one
by exact Bellman-Ford, then uses the Lipschitz cone
b_j=max_i(l_i-theta_i-delta |j-j_i|) and x_i=theta_i+b_(j_i), shifting
b/theta oppositely to fix b0=0. It checks every original bound, adjacent
increment and ranking inequality exactly. This also makes attainment
inspectable beyond a floating LP optimum.

For a paired lower input keep the SAME positive width vector. Pick a
tight allowed edge (p,q) from f. Let b_j=-|j-j_p|+|j_p|, so b0=0 and
b_p-b_q=|j_p-j_q|. Set all theta=0, x_i=b_(j_i); place the p interval
with lower endpoint b_p, the q interval with upper endpoint b_q, and
center every other interval on its b_i. The retained widths are identical.
All requested costs tie at budget1, and the selected pair forces beta_R=1.
Thus the lower input has delta_R=1. Scaling all endpoint values/biases
scales beta and both minima without changing C_R. This is a worst-case
indistinguishability result for the constructed width vector at each
fixed R, not a claim that every arbitrarily prescribed uniform width
allows this construction. The earlier special full-order family does
give uniform positive widths at the global N-2 endpoint.

For C_R=1, lower and upper bounds coincide for every rectangle. That is
stronger than a mandatory generic abstention interval and corrects an
overbroad reading of the R12 archive headline.

## Integer-slot ceiling and aligned-order boundary

For each actual reduced cycle with k>=2, its own R matching costs at most
k(N-k) and its data matching costs at least k; hence the established
N-2 universal upper bound still applies. Since C_R is attained, it too
is at most N-2 on slots1..N, N>=4. For n<4 no two-claim reduced simple
cycle exists, so C_R=1.

If all R pairs agree with the increasing slot order, every allowed
matching cost equals sum j_q - sum j_p. Every unrestricted matching
has cost at least that quantity by the triangle inequality, so M_R=M_all
and C_R=1. The decreasing aligned case is analogous. This is a genuine
ranking-specific exactness condition, rather than a hardware validation.

## Computation and prior machinery

Enumerating disjoint endpoint sets is exponential in arm count. Each
ratio uses standard minimum-cost assignment. The checker brute-forces
bijections at n<=8 for independence; no polynomial-time general algorithm
for computing C_R is claimed. It can be precomputed from slots and R
without observation endpoints, unlike delta_R for a particular rectangle.
At n=6 the complete collection of endpoint-set pairs is small enough
to enumerate every full ranking. An R-specific factor may improve the
worst-case report interface; retaining delta_R itself is also one scalar
when R and original inputs are available. There is no intrinsic archive
storage or generic optimizer novelty claim.

Targeted primary-literature searches found graph Lipschitz, isotonic,
assignment and transport contexts, but no exact duplicate in the sources
inspected. This is not an exhaustive priority guarantee. Generic duality
and matching principles require proper prior attribution in any paper.
