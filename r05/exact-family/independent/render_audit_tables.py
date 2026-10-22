"""Render all fixed n/family/Q cells with paired ranges, never pool timings."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
f=json.loads((HERE/'PAPER_READY_FACTS.json').read_text(encoding='utf-8'))
rows=json.loads((HERE/'ALL_STRATA.json').read_text(encoding='utf-8'))
text='''# Paper-ready bounded facts — independently validated

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
'''
for prefix,label in [('Cheap_over_Quartet','Cheap / Quartet'),('Fastest_old_over_Quartet','Fastest(Raw, Closed, Cheap) / Quartet')]:
    text+='\n## '+label+'\n\n| n | family | Q=1 | Q=48 | Q=192 | Q=768 |\n|---:|:---|---:|---:|---:|---:|\n'
    for n in [4,8,16,32,64]:
        for family in ['first','last','all']:
            cells=[]
            for q in [1,48,192,768]:
                r=next(r for r in rows if (r['n'],r['family'],r['Q'])==(n,family,q))
                m,lo,hi=[r[prefix+'_'+suffix] for suffix in ['median','min','max']]
                cell=f'{m:.4f} [{lo:.4f}, {hi:.4f}]'
                if m<=1:
                    cell='**NO GAIN** '+cell
                cells.append(cell)
            text+=f'| {n} | {family} | '+' | '.join(cells)+' |\n'
text+='''
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
'''
(HERE/'PAPER_READY_FACTS.md').write_text(text,encoding='utf-8')
print('Rendered all 120 comparator cells, with negative medians and paired ranges.')
