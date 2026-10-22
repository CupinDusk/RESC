# Draft: N-2 is sharp even for a complete order of all N arms

Derived during R9 review; no R10 numerical checks have yet run. This is a
prospective strengthening, not a result already in the R9 PDF/artifact.

R9 proves the upper bound for every acyclic partial ranking. Its displayed
tight example uses two disjoint comparisons, but the same factor is attained
even by a complete ranking involving an arm at EVERY slot1..N, N>=4.

Take t>0, common interval half-width0<=epsilon<t/2. Let
v=t-2epsilon>0 and beta=v/(N-2). Log centers are

    c_1=t, c_2=v-beta, c_(N-1)=0, c_N=t+v-beta,
    c_j=v-beta*(j-1) for j=3,..,N-2.

Ask the complete non-strict order

    theta_1 <= theta_(N-1) <= theta_(N-2) <= ... <= theta_3
            <= theta_N <= theta_2.

At N4 the middle sequence is empty:1<=3<=4<=2.
Every implied-pair deficit/distance is <=beta. The two pairs
1<=(N-1) and N<=2 have deficits v and distance N-2;1<=2 has
deficit beta and distance1. For1<=j in3..N-2, deficit is
v-c_j=beta*(j-1), also binding. Every other implied pair has
nonpositive deficit (or is already among these). Therefore the all-anchor
box radius is exactly beta, including positive-width intervals.

The two disjoint pairs have crossed distance2 and combined deficit2v,
so their shared path needs delta>=v. At delta=v use

    b_0=b_1=b_N=0; b_j=-v for j=2,..,N-1.

All adjacent increments are <=v. Select x_1=t-epsilon,
x_(N-1)=epsilon, x_N=t+v-beta-epsilon, x_2=v-beta+epsilon,
and x_j=c_j+epsilon for j=3,..,N-2. These are legal interval endpoints.
The resulting theta values are

    theta_1=theta_(N-1)=t-epsilon,
    theta_j=t-epsilon+c_j (middle j in reverse physical order),
    theta_N=theta_2=t-epsilon+v-beta.

The middle centers increase from beta to v-2beta in the requested order,
which lies between0 and v-beta. Thus the full order holds and delta=v
attains it. The exact shared/all-box radius ratio is N-2 even for full
rankings of all positions. For N4,epsilon0,point logs(.01,.005,0,.015)
have beta.005/shared.01, unlike the less sharp R8 full-order fixture.

Possible evaluation if this enters R10: freeze a protocol before numerical
execution; use N4/5/6/8/16/32/64,t.01,epsilon0/.001/.004. Check all implied
pair thresholds, every integer/half anchor, original x/b minimum shared LP,
an original interval-box minimum LP at all position anchors, all endpoint
and midpoint classifications, and the displayed analytic endpoint witness.
Preserve all R9 evidence/reviews; no new physical H20 model or acquisition.
