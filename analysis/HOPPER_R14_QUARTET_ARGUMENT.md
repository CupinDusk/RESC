# Candidate quartet criterion for universal exactness on a line

Save before computation. Costs are |j_p-j_q| on distinct ordered slots.
R is fixed and transitively closed as in the existing factor theorem.
Call a quartet bad if disjoint P,Q of size2 have an allowed R-perfect
matching and M_R(P,Q)>M_all(P,Q). The candidate claim is:

    C_R=1 iff no bad quartet exists.

One direction follows because the full factor maximizes over these sets.
For the converse suppose C_R>1 on some larger P,Q and choose a
minimum-cost R-perfect matching f. Its cost exceeds the unrestricted
optimum. The following standard one-dimensional uncrossing fact applies.

For each open gap between consecutive endpoint coordinates, a matching's
distance cost equals gap length times the number of edges crossing it.
The difference between left-to-right and right-to-left crossing counts
depends only on P and Q. The unrestricted sorted matching attains the
sum of gap length times absolute net crossing count. Thus a nonoptimal
matching must have one gap crossed in both directions by two of its edges.
Swapping their Q endpoints strictly reduces distance, by twice the
positive overlap length of those opposite-direction segments.

Apply this to f. If both swapped edges belonged to R, the swap would
give a cheaper R-perfect matching, contradiction. On the four distinct
endpoints the original allowed matching therefore exists, its cheaper
swapped matching is not allowed, and these are the only two bijections.
Their restricted/free optimum ratio is greater than1: a bad quartet.
This proves the converse. The proof uses only a classical line-assignment
uncrossing fact, derived explicitly above; no new uncrossing algorithm is
claimed. The new scoped conclusion is the four-arm characterization of
zero representation loss for this ranking relaxation.

Enumerate 4 endpoints and a split into two pairs; test the two possible
bijections. That uses O(n^4) arithmetic/membership operations once R is
closed. Costs and Boolean tests are exact for integer slots. A full
nonunit factor is still computed by the existing exponential procedure;
no equality between its value and the maximum quartet ratio is assumed.

In planning, this predicate alone can certify marginal-only processing
for every future rectangle. A bad quartet instead requests relational
checking or optional tighter-factor precomputation. This is a conditional
reference workflow, not proof of deployment, timing validity or savings.
