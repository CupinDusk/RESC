# Candidate scalar-archive information boundary

This argument is saved before the new witness/LP checks. It is a consequence
and interpretation of the R11 sharp factor plus an additional matching lower
family, not evidence of real archive adoption or of physical device bias.

Fix N>=4, beta>0, common log half-width epsilon>=0, and the complete order
R=(1,N-1,N-2,...,3,N,2). The previously proved upper family, with
t=beta(N-2)+2epsilon, has beta_R=beta and delta_R=(N-2)beta. Every arm has
the same half-width epsilon, and the positive-width case uses epsilon>0.

For the lower family put b_j=-beta*j for j=0..N. Choose x_j=b_j and
theta_j=0. Centers are c_1=b_1+epsilon,
c_(N-1)=b_(N-1)-epsilon and c_j=b_j otherwise, with each interval
[c_j-epsilon,c_j+epsilon]. The chosen x lies in every interval. Bias has
b0=0 and every adjacent difference exactly beta; all ranked costs tie.
Thus delta_R<=beta. For the implied comparison 1<=N-1,
l_1-u_(N-1)=b_1-b_(N-1)=beta(N-2), so beta_R>=beta. The established
beta_R<=delta_R chain forces both to equal beta. This proof works for
every N, beta and nonnegative half-width, not only the validation grid.

The two inputs have identical archive A=(N,R,beta_R,epsilon), including
the complete ranking and all widths. For every assumed budget delta in
[beta,(N-2)beta), the lower input admits the ranking and the upper input
rejects it. No rule receiving only A and delta can be correct on both.
For delta<beta, the all-anchor lower bound excludes both/any compatible
input; for delta>=(N-2)beta the universal theorem admits every compatible
input. Ties at either exact boundary follow the non-strict ranking rule.
This gives a sharp three-way decision interface for the scalar archive:
reject, unknown, or model-conditional feasible. It does not identify a
same-state physical ranking, an optimum device choice or calibrated bias.

The information boundary is deliberately restricted: it does not concern
arbitrary interval outputs, all per-anchor feasibility functions, or full
pair-support arrays. If the original l/u and slot identities are kept,
there is no necessity to archive a dense graph: O(n) input numbers plus
the ranking/model contract reconstruct its O(n^2) D weights. Standard
fixed-budget Bellman-Ford checking costs O(n^3); a returned potential
theta yields b_j=max_i(l_i-theta_i-delta*|j-j_i|), and x_i=theta_i+b_(j_i).
Shift b and theta oppositely to set b0=0. A checked negative cycle rejects.
Minimum-budget optimization remains ordinary LP/graph machinery, not a
new general solver. There is no measured or inherent saving over retaining
the original rectangle and metric; the ratio quantifies what a scalar
summary alone can and cannot authorize.
