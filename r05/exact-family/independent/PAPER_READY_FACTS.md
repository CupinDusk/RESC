# Paper-ready bounded facts — independently validated

The prospectively designed synthetic family contains 15 complete rankings
(n=4,8,16,32,64; first, last, all disjoint adjacent pairs reversed) and 48
planted integer rectangles per ranking. All 720 distinct queries admit.
Independent line-matching uncrossing proves C_R=1; exhaustive directed
quartet checks cover 12,118,086 cuts, with full disjoint assignment enumeration
for n=4 and 8. Cheap recognizes 0/15 rankings; quartet recognizes 15/15.
Beta admits every query, the loose span ceiling admits none, so Cheap falls
back to 720/720 graphs while +Q falls back to 0/720. Raw and Closed each use
720/720 graphs. These census counts refer to one pass over distinct queries.

This is a deliberately favorable planted synthetic structural study, not
independent application inputs or an application-presence estimate. A cheaper
family-specific adjacent-reversal flag could replace general quartet detection.
The study establishes neither its necessity nor algorithmic optimality. It
supplements the unchanged adverse R04 results.

Only the original single collection, 2026-10-22 22:07:13.937138 through
22:07:17.404653 UTC, supplies performance observations. All 2,160 rows, all
60 expected batch hashes and nine paired blocks independently validate.
No performance mode was rerun. Q=1 uses rectangle 0; Q=48 uses each of 48
queries once; Q=192 and 768 repeat those inputs four and sixteen times.
The complete jobs include fresh route-specific preparation, graph work when
needed, decision hashing and teardown, over preloaded immutable arrays and
reusable common scratch. Parsing, validation, file output, expected checks
and the outer volatile update are excluded equally.

The recorded process was ordinary Windows on an i9-14900HX; normal
applications/PDF reviews were active and heavy RTL work was requested to
defer around the brief run. No idle, affinity, frequency or priority control
is asserted. These are host CPU-code observations, not GPU/hardware,
physical source-time or certificate-service evidence.

There are 39/60 designed cells with median benefit over Cheap and 36/60 over
the fastest old route. These are counts of chosen design cells, not a
population prevalence estimate. The first sampled median-gain Q versus the
fastest old route is 48 at n=4,8,16; 192 at n=32; 768 at n=64, for all three
families. These are sampled crossovers, not fitted break-even values. At
n=4,Q=1 quartet beats Cheap but loses to Raw in all nine blocks. Two gain
cells contain negative paired blocks: n=16,all,Q=48 wins 8/9 versus each
comparator; n=32,last,Q=192 wins 9/9 versus Cheap and 8/9 versus fastest old.

Each table cell below is the median of nine **within-block** time ratios,
followed by [minimum, maximum] across those same nine ratios. Ratio >1 favors
Quartet; **NO GAIN** marks median <=1. The fastest old route is selected
within each paired block as min(Raw, Closed, Cheap). These are not ratios
of separate timing medians, and no size/family/Q timings are pooled. Full
per-route job-time medians/min/max, all paired values and win/loss/tie counts
are in ALL_STRATA.csv/json.

## Cheap / Quartet

| n | family | Q=1 | Q=48 | Q=192 | Q=768 |
|---:|:---|---:|---:|---:|---:|
| 4 | first | 1.1011 [1.0550, 1.4863] | 3.4740 [2.1821, 3.5355] | 4.2878 [3.6904, 4.5371] | 4.5990 [4.1394, 4.8282] |
| 4 | last | 1.0975 [1.0737, 1.1345] | 3.5114 [3.4624, 3.6150] | 4.3157 [4.1051, 4.8251] | 4.6330 [3.4040, 4.9532] |
| 4 | all | 1.0876 [1.0634, 1.1099] | 3.4875 [3.2114, 3.7860] | 4.2506 [2.9164, 4.7312] | 4.5051 [4.0598, 4.5688] |
| 8 | first | **NO GAIN** 0.6129 [0.5490, 0.8468] | 3.2411 [2.9576, 3.4718] | 4.0816 [3.8887, 4.2690] | 4.4204 [4.2688, 4.7242] |
| 8 | last | **NO GAIN** 0.5963 [0.5534, 0.6577] | 3.2570 [3.0362, 3.3765] | 4.0288 [3.9273, 4.4805] | 4.3393 [3.9928, 4.5880] |
| 8 | all | **NO GAIN** 0.5915 [0.5682, 0.6227] | 3.1381 [3.0161, 4.9548] | 4.0583 [3.9648, 4.5307] | 4.2620 [3.8070, 4.3653] |
| 16 | first | **NO GAIN** 0.1603 [0.1557, 0.1950] | 1.7311 [1.4038, 2.4841] | 3.1881 [2.9053, 3.4969] | 4.2368 [3.5601, 4.4786] |
| 16 | last | **NO GAIN** 0.1571 [0.1462, 0.1749] | 1.7285 [1.6525, 1.8096] | 3.1781 [2.6710, 3.4711] | 4.1395 [4.0622, 4.2135] |
| 16 | all | **NO GAIN** 0.1432 [0.1384, 0.4419] | 1.7311 [0.9830, 3.1761] | 3.1506 [2.6434, 3.5112] | 4.2523 [4.0925, 4.8204] |
| 32 | first | **NO GAIN** 0.0437 [0.0377, 0.0577] | **NO GAIN** 0.5633 [0.5437, 0.6885] | 1.5809 [1.4337, 1.6549] | 3.0833 [2.8529, 3.2068] |
| 32 | last | **NO GAIN** 0.0464 [0.0418, 0.0515] | **NO GAIN** 0.5611 [0.5551, 0.6055] | 1.5864 [1.2977, 1.6856] | 3.0474 [2.7451, 3.1833] |
| 32 | all | **NO GAIN** 0.0362 [0.0331, 0.0764] | **NO GAIN** 0.5437 [0.5040, 0.5532] | 1.5641 [1.4469, 1.6173] | 2.9623 [2.7453, 3.0780] |
| 64 | first | **NO GAIN** 0.0154 [0.0123, 0.0159] | **NO GAIN** 0.1646 [0.1582, 0.1684] | **NO GAIN** 0.5501 [0.4816, 0.5602] | 1.6670 [1.5915, 1.6855] |
| 64 | last | **NO GAIN** 0.0153 [0.0148, 0.0156] | **NO GAIN** 0.1636 [0.1533, 0.1670] | **NO GAIN** 0.5756 [0.5209, 0.6220] | 1.6231 [1.5544, 1.6661] |
| 64 | all | **NO GAIN** 0.0107 [0.0101, 0.0111] | **NO GAIN** 0.1546 [0.1511, 0.1663] | **NO GAIN** 0.5451 [0.5184, 0.5851] | 1.5652 [1.5284, 1.6316] |

## Fastest(Raw, Closed, Cheap) / Quartet

| n | family | Q=1 | Q=48 | Q=192 | Q=768 |
|---:|:---|---:|---:|---:|---:|
| 4 | first | **NO GAIN** 0.5109 [0.4880, 0.5235] | 2.7771 [1.8240, 2.8312] | 3.5337 [3.0692, 3.7278] | 3.7989 [3.2676, 3.9120] |
| 4 | last | **NO GAIN** 0.5109 [0.4655, 0.5219] | 2.8229 [2.7506, 2.9422] | 3.5454 [3.0097, 3.6389] | 3.8483 [2.8015, 4.0165] |
| 4 | all | **NO GAIN** 0.5073 [0.5000, 0.5238] | 2.7864 [2.5815, 2.8648] | 3.4726 [2.3724, 3.5526] | 3.6649 [3.2265, 3.8505] |
| 8 | first | **NO GAIN** 0.2581 [0.2275, 0.3084] | 2.4460 [2.2782, 2.6149] | 3.2834 [3.0267, 3.3884] | 3.5062 [3.3362, 3.6737] |
| 8 | last | **NO GAIN** 0.2523 [0.2332, 0.2710] | 2.4427 [2.2476, 2.8567] | 3.2135 [3.0805, 3.6652] | 3.4216 [3.1053, 3.5227] |
| 8 | all | **NO GAIN** 0.2629 [0.2545, 0.2736] | 2.4172 [2.3432, 2.4701] | 3.1544 [3.0725, 3.4824] | 3.4388 [2.8124, 3.4917] |
| 16 | first | **NO GAIN** 0.0573 [0.0544, 0.0605] | 1.2638 [1.1086, 1.3112] | 2.3667 [2.1489, 2.4717] | 3.1148 [2.9886, 3.2717] |
| 16 | last | **NO GAIN** 0.0577 [0.0547, 0.0642] | 1.2616 [1.1083, 1.3636] | 2.3677 [1.9747, 2.5154] | 3.1038 [3.0537, 3.3845] |
| 16 | all | **NO GAIN** 0.0595 [0.0561, 0.0624] | 1.2277 [0.7153, 1.3117] | 2.4292 [1.9751, 2.5761] | 3.1097 [2.9540, 3.2638] |
| 32 | first | **NO GAIN** 0.0117 [0.0107, 0.0179] | **NO GAIN** 0.3994 [0.3823, 0.4417] | 1.1597 [1.0656, 1.2118] | 2.2008 [1.9677, 2.5181] |
| 32 | last | **NO GAIN** 0.0118 [0.0111, 0.0165] | **NO GAIN** 0.4136 [0.3808, 0.4471] | 1.1552 [0.9450, 1.2287] | 2.2626 [2.0965, 2.3784] |
| 32 | all | **NO GAIN** 0.0119 [0.0103, 0.0155] | **NO GAIN** 0.3910 [0.3553, 0.3976] | 1.1372 [1.0453, 1.1805] | 2.1744 [2.0374, 2.3794] |
| 64 | first | **NO GAIN** 0.0031 [0.0026, 0.0067] | **NO GAIN** 0.1120 [0.1071, 0.1171] | **NO GAIN** 0.4169 [0.3636, 0.4381] | 1.2183 [1.1815, 1.2951] |
| 64 | last | **NO GAIN** 0.0031 [0.0029, 0.0033] | **NO GAIN** 0.1154 [0.1127, 0.1258] | **NO GAIN** 0.4043 [0.3784, 0.4306] | 1.2001 [1.1422, 1.2468] |
| 64 | all | **NO GAIN** 0.0029 [0.0027, 0.0033] | **NO GAIN** 0.1092 [0.1045, 0.1136] | **NO GAIN** 0.3949 [0.3738, 0.4073] | 1.1680 [1.1150, 1.3179] |

## Validation and reproducibility bounds

The independent checker reconstructs all declarations, graphs and rolling
hashes rather than calling the author's validation functions. Rebuilt C++
validation/census outputs are additional byte-identical corroboration.
Source/PE comparison confirms unchanged R04 algorithms except declared storage
capacity and corpus/Q count adaptations. All PE code bytes match after only
documented build timestamp/build GUID normalization. Initial auditor path,
CRLF and incomplete PE-normalization failures are retained in the audit;
producer evidence was not repaired or recollected. A census compiler warning
is analyzed as an unreachable short-circuit path in INDEPENDENT_AUDIT.md.

The analytic family result is general over the stated structural family;
the timing results are limited to the retained single Windows run and its
four measured routes. Do not infer application frequency, optimized-algorithm
superiority, physical-device behavior, GPU speed, hardware performance,
outward-log arithmetic or a cryptographic certificate-service cost.
