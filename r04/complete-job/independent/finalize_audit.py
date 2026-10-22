"""Finalize descriptive audit files and refresh hashes; never compiles or times."""
from pathlib import Path
import json
import check_complete as audit

here=Path(__file__).resolve().parent
result=audit.read_json(here/'INDEPENDENT_AUDIT.json')
before=audit.read_json(here/'PRESERVED_INPUTS_BEFORE.json')
after={p.name:audit.sha(p) for p in here.parent.iterdir() if p.is_file()}
audit.require(before == after, 'preserved study changed')
result['measurement_boundary']['normalization']='Each elapsed interval is divided by repeats*plans_in_stratum; summary values are medians/min/max of nine block-average ns/job observations. Per-query equivalents are further divided by Q, not separately timed query latencies.'
result['source_review']=dict(
    raw_no_closure='benchmark.cpp:5-9,13,16 and core.hpp:25; raw Plan is freshly default-initialized and uses original reverse edges only.',
    setup_inside='benchmark.cpp:13 and 75-80; prepare_plan occurs in every timed complete_job, with route-specific closure and flags.',
    route_one='benchmark.cpp:7 and 16; closure-direct constructs closure then requests graph-only query route 0.',
    shared_buffers='benchmark.cpp:39; core.hpp:25-26 rewrites graph matrix and BF labels/predecessors; capacity is reused.',
    hash_boundary='benchmark.cpp:17,75-81; per-query hashing and batch sum inside, final volatile update and expected comparison after stop.',
    common_exclusions='benchmark.cpp:25-38,40-71,83-85; parsing, validation/certificates, warmup, I/O excluded.',
    anti_hoist='benchmark.cpp:77 has a compiler memory barrier per job; results are checked and consumed after stop.',
    timer='steady_clock; saved is_steady=1, period=1/1e9; actual raw interval GCD=100ns does not establish 1ns resolution.',
    classification='Quartet is evaluated only when cheap is false and stops on its first obstruction; no all-quartets-per-job cost claim.',
    semantics='Raw and closed zero-weight ranking constraints have identical feasible sets by path transitivity; separately constructed graph validation covers every actual query.')
result['limitations'].extend([
    'Strata occur in ascending order per block; Q and route orders are shuffled, but stratum/time effects are not independently randomized.',
    'Normalized values are block averages across plans, not a distribution of individually timed job or query requests.',
    'CPU/OS identity and historical controls are run metadata; this audit did not observe host controls during the earlier run.'
])
audit.write_json('INDEPENDENT_AUDIT.json',result)
audit.write_paper_facts(result)
files={str(p.relative_to(here)).replace('\\','/'):audit.sha(p) for p in here.rglob('*') if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
audit.write_json('AUDIT_MANIFEST.json',dict(status='COMPLETE',original_study_files=before,independent_files=files,manifest_self_excluded=True))
print(json.dumps(dict(status='FINALIZED',original_files_preserved=len(before),independent_files_bound=len(files),new_timing_runs=0)))
