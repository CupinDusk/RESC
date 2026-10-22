# Certifying a resolution-based window partition

Recorded before R10 numerical certification. eta=1e-8 is a declared window
resolution, not a claim about solver objective error or hardware accuracy.

For each exact positive decimal timing endpoint, Decimal.ln at80 significant
digits is correctly rounded per Python3.12 documentation. Its two adjacent
representable neighbors enclose the true logarithm. Taking outward integral
floor/ceiling after scaling by10^60 retains this enclosure. Multiplying by60
makes exact division by every six-slot distance1..5 integral. The checker
then uses only integer arithmetic at scaleU=60*10^60.

Let l^-<=l<=l^+ and u^-<=u<=u^+ be those endpoint enclosures. All arms have
their original distinct slots. For the ranking transitive closure R,

    beta^- = max(0,max_R(l_p^- - u_q^+)/d_pq),
    beta^+ = max(0,max_R(l_p^+ - u_q^-)/d_pq).

Then beta^-<=beta_true<=beta^+. We do not equate an LP residual tolerance
with error in beta or the shared optimum.

For any fixed delta define D^+(a,b)=u_b^+-l_a^-+delta*d_ab and
D^-(a,b)=u_b^--l_a^++delta*d_ab, off diagonal, and diagonal0.
These bound every true projected edge D_true(a,b). Include zero edges
q->p for every requested theta_p<=theta_q. Standard difference-constraint
negative-cycle feasibility is prior machinery; the independent checker
uses exact integers, not an approximate LP solver.

At delta=beta^++eta, a negative cycle in D^+ also rejects the tighter true
system. Since every true box admits by beta^+, the true window is wider
than eta. For a reported cycle with observation constant sum c and distance
sum d>0, every shared path needs delta>=-c/d; therefore
-c/d-beta^+ is an exact lower bound on the true window width. This is the
positive certificate; each edge/weight and the negative sum are checked.

At delta=beta^-+eta, an integer potential satisfying all D^- and ranking
edges also satisfies D_true and its exact relative-cost projection. Thus
delta_path<=beta^-+eta<=beta_true+eta. This proves the true window cannot
exceed eta, even if its exact width is a tiny positive number. D^- need
not itself arise from a valid tighter rectangle when a min/max interval
has zero width; only the edgewise inequality D^-<=D_true is used. Validate
the entire potential against every tighter edge, not just solver status.

These two certificates give a complete partition if none is ambiguous.
The historical numerical claim of exactly zero width is replaced, where
appropriate, by an upper bound eta; sub-resolution signs are not invented.

For a fixed hypothetical delta=ln(1+f), its own enclosure is used. A gap
is certified if beta^+<=delta^- and D^+(delta^+) has a negative cycle.
There is no gap if beta^->delta^+ or D^-(delta^-) has a feasible potential.
Other cases are explicitly ambiguous. At f0 the path and every box are
the same zero-bias ranking set, so no gap is possible by definition.
The two-claim fixed-grid audit similarly outward-bounds all three margins.

This certifies conditional arithmetic for the exact decimal timing inputs
and their natural logarithms. It does not justify those rectangles as
physical uncertainty sets, calibrate a bias budget, or establish device
ranking truth. Correctness relies on the documented Decimal rounding
contract and the standard projected difference-constraint theorem; it is
not a machine-checked proof of those libraries or graph principles.

Primary documentation retrieved: https://docs.python.org/3.12/library/decimal.html
ln is documented correctly rounded using ROUND_HALF_EVEN; adjacent context
values therefore provide safe bracketing before outward grid rounding.

New primary literature read for R10: Kyng/Rao/Sachdeva/Spielman,
Algorithms for Lipschitz Learning on Graphs, arXiv1505.00290v2, full PDF
retrieved with formulation/Lemma3.5 and minimum-gradient interpretation
inspected. Kyng/Rao/Sachdeva, Fast, Provable Algorithms for Isotonic
Regression in all L_p-norms, NIPS2015, full PDF retrieved with Sec1.1/1.3
and Sec4's weighted-infinity isotonic-to-Lipschitz construction inspected.
These are closer established minimax extension/radius machinery than only
squared-error regression. The proposed claim remains the exact ratio of
the specified all-anchor marginal relaxation to one shared path, not a
new graph-extension optimizer. No exhaustive priority guarantee is made.
