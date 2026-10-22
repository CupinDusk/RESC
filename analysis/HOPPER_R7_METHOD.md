# Joint queries and finite-sample calibration references

This is a same-scope secondary analysis after R6's four PDF-only reviews
(all Weak Reject). Prior PDFs, original reports, splits, negative cases
and exact candidate-centered winner result are retained. There is no new
measurement acquisition, physical H20 bias bound, same-state truth or
prospective selector test. The fixed plan is HOPPER_R7_JOINT_PROTOCOL.json.

The proof written before execution is HOPPER_R7_JOINT_ARGUMENT.md. Ordinary
difference-constraint negative-cycle closure is established machinery,
not an original general algorithm: Mine's PADO 2001 paper, public author
preprint https://arxiv.org/pdf/cs/0703073, Secs.2-3, Theorems1-2, retrieved
in full and those sections read. The new scoped proposition characterizes
two disjoint comparisons under ONE shared path, and precisely when EVERY
real-anchor independent box fails to reject that conjunction. It does not
contradict the prior exactness for each candidate's winner-star query.

All 180 query pairs per cell are retained at every old budget: 96120
dependent cases. Every one of 16020 original x/b path LPs at log(1.02)
agrees; the 18 relevant median-box LPs admit the joint claim, also agreeing.
No-anchor-recovery counts by fractions 0/.005/.01/.02/.05/.10 are
0/2/11/18/102/286. All individual-infeasible and jointly feasible cases
remain in the full generated CSV; no queries were screened by outcomes.
The first corpus example occurs at .5% for 1:N,C8,one cluster,B8192,
claims F<=P and B<=A. Individual margins .00656263/.01294717 are nonnegative;
the path cross margin -.000440361 is negative, whereas the best of ALL
real anchors has box cross margin .019509805. This rejects the conjunction
conditionally, not either individual comparison nor a hardware fact.

Calibration maxima normally fail out of sample. For iid continuous episode
scores with a fixed definition, each assessment score exceeds the maximum
of m calibration scores with probability1/(m+1), so expected count n/(m+1).
The unique overall maximum falls in assessment with probability n/(m+n),
exactly the probability of any exceedance. This rank-symmetry argument is
a reference, not an exchangeability assertion about observed corpora.
For m=n25/50/5 the expected counts are .96154/.98039/.83333 and P(any)=.5.

Prespecified stationary Gaussian-log/no-order controls use seed20261021,
10000 replications for (arms,m,n)=(3,25,25),(3,50,50),(20,5,5). The same
randomized-order fitting/max-envelope recipe compares known centers,
centers fitted on calibration, and centers independently fitted on m
episodes. Mean exceedances are respectively .9828/1.2155/.9782,
.9850/1.1350/.9834 and .8408/2.0704/.8308; P(any) is
.5028/.5677/.4946, .4994/.5408/.4976, .4999/.8323/.4985.
Thus center reuse alone can amplify failures without any order effect.
These toy controls are not a significance test of the observed2/2/2.
All histograms, ratio distributions and Monte Carlo standard errors remain.

All five prespecified cyclic half-splits are reported, not selected:
random assessment coverage memcached23/21/25/25/25 of25;
NPBench48/50/50/49/48 of50; uFS3/5/5/5/4 of5. They are dependent
sensitivity analyses and do not replace the chronological primary table.

The uFS queries are two-arm comparisons using point cost=-log throughput,
original full-20-command slot distance10 and frozen delta .3122178823.
For heldout fixed run10, LsMP throughput50602.1658/1118.1192 gives support
-.6901675 (certificate); ADPS115008.6256/42925.8242 gives2.1366453 (abstain).
Observed random reference ranges separate in both, but are not confidence
intervals or same-state ground truth. All50 naive choices already agree;
the audit still certifies10/abstains40. No improved choice claim follows.

Public package excludes all upstream raw CSVs/reset/launch code. It bundles
our aggregate results and only two necessary worked numerical examples;
the full50-query point-value listing and full96120-query CSV are generated
locally from pinned inputs. Exact hashes/aggregate expected outputs check
the complete enumeration. Codex assisted arguments, implementation and prose.
