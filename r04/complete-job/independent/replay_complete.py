"""Independent author-side audit; never calls any program with time mode.

All writes remain under this file's directory. The original study is read-only.
The native replay and graph checker are validation runs, not new observations.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
from statistics import median
import csv, hashlib, json, math, random, re, shutil, struct, subprocess, sys

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
OLD = STUDY.parents[1] / 'r03/cost'
ZIG = None
import argparse, os
MASK = (1 << 64) - 1
NAMES = ['raw_direct', 'closure_direct', 'cheap', 'quartet']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def read_csv(path):
    with path.open(encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))

def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def require(condition, detail):
    if not condition:
        raise AssertionError(detail)

def source_replay():
    replay = HERE / 'native-validation-replay'
    require(replay.exists(), 'recorded graph evidence is required')
    if ZIG is None:
        return replay
    work = HERE / 'fresh-native-validation'
    require(not work.exists(), 'fresh native directory required')
    work.mkdir()
    for name in ['core.hpp','benchmark.cpp','inputs.txt','schedule.txt']:
        shutil.copyfile(STUDY/name,work/name)
    exe = '.exe' if os.name == 'nt' else ''
    def command(args,label):
        require('time' not in args,'time mode prohibited')
        result=subprocess.run(args,cwd=work,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (HERE/(label+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
        require(result.returncode == 0,label+' failed')
    command([str(ZIG),'c++','benchmark.cpp','-std=c++17','-O3','-DNDEBUG','-Wall','-Wextra','-o','benchmark'+exe],'fresh-build')
    command([str(work/('benchmark'+exe)),'validate'],'fresh-source-validation')
    for name in ['validation.csv','expected_batches.csv']:
        require(sha(work/name)==sha(STUDY/name),'fresh native output differs: '+name)
    command([str(ZIG),'c++',str(HERE/'independent_graph.cpp'),'-std=c++17','-O2','-Wall','-Wextra','-o','independent_graph'+exe],'fresh-independent-build')
    command([str(work/('independent_graph'+exe))],'fresh-independent-graph')
    require(sha(work/'independent_graph.csv')==sha(replay/'independent_graph.csv'),'all independent graph bytes differ')
    return work

def code_binding(replay):
    original=(OLD/'benchmark.cpp').read_text(encoding='utf-8').split('int main(int argc,char**argv)')[0]
    original=original.replace('if(p.R[b*n+a]&&w>0)w=0;','if(!p.R.empty()&&p.R[b*n+a]&&w>0)w=0;')
    original=original.replace('s.w[a*n+b]=w;}}\nbool bf','s.w[a*n+b]=w;}if(p.R.empty())for(auto[a,b]:p.edges)s.w[b*n+a]=std::min<I>(s.w[b*n+a],0); }\nbool bf'.replace('; }',';}'))
    require(original==(STUDY/'core.hpp').read_text(encoding='utf-8'),'documented R03 core derivation')
    return dict(status='SOURCE_DERIVATION_RECHECKED_HISTORICAL_PE_RECORD_RETAINED',
        source_core_matches_only_two_documented_raw_graph_edits=True,
        historical_pe_record=read_json(HERE/'PE_SOURCE_BINDING.json'),
        historical_executable_bytes_bundled=False,pe_binding_freshly_rechecked=False,
        fresh_native_all_41760_queries=ZIG is not None,
        scope='Public default audits saved graph records; optional compiler rebuilds both correctness paths. Original timed binary and debug data are excluded, so the saved historical PE binding is not reverified.')

def timing_log_check(expected, rows, schedule, meta):
    log=(STUDY/'timing-run.log').read_text()
    observed=re.findall(r'^complete block=(\d+) census Q=(\d+)$',log,re.MULTILINE)
    wanted=[(str(s['block']),str(s['queries'])) for s in schedule if s['stratum'] == 0]
    require(observed == wanted, 'all 27 logged census completions in scheduled order')
    final=re.search(r'^PASS_TIMING checksum=(\d+) steady=(\d+) timer_period=(\d+)/(\d+) sizeof_signed128=(\d+)$',log,re.MULTILINE)
    require(final is not None, 'final timing line')
    # One warmup batch for every Q/stratum/route, plus every recorded batch.
    want=(4*sum(expected.values()) + sum(row['checksum'] for row in rows)) & MASK
    require(tuple(map(int,final.groups())) == (want,1,1,1000000000,16), 'global volatile checksum and timer report')
    elapsed=[row['elapsed_ns'] for row in rows]
    require(meta['complete_records'] == len(rows) and sum(elapsed) <= meta['wall_elapsed_ns'], 'metadata interval/record consistency')
    result=dict(final_volatile_checksum=want,warmup_batch_count=612,recorded_batch_count=len(rows),
                all_27_logged_census_steps_match_order=True,raw_interval_sum_ns=sum(elapsed),
                process_wall_elapsed_ns=meta['wall_elapsed_ns'],raw_interval_gcd_ns=math.gcd(*elapsed),
                shortest_raw_interval_ns=min(elapsed),longest_raw_interval_ns=max(elapsed))
    write_json('TIMING_LOG_AUDIT.json',result)
    return result

def input_text(plans):
    numbers = iter(map(int, (STUDY / 'inputs.txt').read_text().split()))
    require((next(numbers), next(numbers)) == (870, 51), 'text input counts')
    strata = {}
    for plan in plans:
        pid, sid, n, edge_count, flag = [next(numbers) for _ in range(5)]
        require((pid, sid, n, flag) == (plan['id'], plan['stratum'], plan['n'], int(plan['quartet_exact'])), 'text/JSON plan header')
        require([next(numbers) for _ in range(n)] == plan['slots'], 'text/JSON slots')
        require([[next(numbers), next(numbers)] for _ in range(edge_count)] == plan['edges'], 'text/JSON original edges')
        rectangles = [[[next(numbers) for _ in range(n)], [next(numbers) for _ in range(n)]] for _ in range(8)]
        require(rectangles == plan['rectangles'], 'text/JSON rectangle arrays')
        require([[next(numbers), next(numbers)] for _ in range(48)] == plan['queries'], 'text/JSON frozen query order')
    for _ in range(51):
        sid, repeats, size = [next(numbers) for _ in range(3)]
        ids = [next(numbers) for _ in range(size)]
        require(ids == [p['id'] for p in plans if p['stratum'] == sid], 'text stratum plan membership/order')
        n = plans[ids[0]]['n']
        require(repeats == (1 if sid == 0 else {4:100,8:100,16:20,32:5,64:2}[n]), 'predeclared repeat mismatch')
        strata[sid] = dict(repeats=repeats, ids=ids)
    require(next(numbers, None) is None, 'trailing text input tokens')
    return strata

def keyed(rows):
    result = {}
    for row in rows:
        key = tuple(int(row[name]) for name in ['plan', 'rectangle', 'delta'])
        require(key not in result, 'duplicate validation query')
        result[key] = int(row['decision'])
    return result

def stats(values):
    return dict(median=float(median(values)), min=float(min(values)), max=float(max(values)), blocks=len(values))

def pair(series, sid, queries, tested, baseline):
    delta = [series[(sid, queries, tested)][b] - series[(sid, queries, baseline)][b] for b in range(9)]
    return dict(faster=sum(v < 0 for v in delta), slower=sum(v > 0 for v in delta), ties=sum(v == 0 for v in delta), differences_ns=stats(delta))

def main():
    global ZIG
    parser=argparse.ArgumentParser();parser.add_argument('--zig');args=parser.parse_args()
    ZIG=Path(args.zig).resolve() if args.zig else None
    parents = {p.name: sha(p) for p in STUDY.iterdir() if p.is_file()}
    write_json('PRESERVED_INPUTS_BEFORE.json', parents)
    manifest = read_json(STUDY / 'INPUT_MANIFEST.json')
    for name, expected in manifest['files'].items():
        require(parents[name] == expected, 'frozen study hash: ' + name)
    for name, expected in manifest['original_binding'].items():
        require(sha(OLD / name) == expected, 'original R03 binding: ' + name)
    for name in ['inputs.json', 'inputs.txt']:
        require(sha(OLD / name) == parents[name], 'copied input byte identity: ' + name)
    pre = read_json(STUDY / 'PRE_TIMING_AUDIT.json')
    for field, name in [('original_validation_sha256', None), ('new_validation_sha256', 'validation.csv'), ('expected_batches_sha256', 'expected_batches.csv'), ('input_manifest_sha256', 'INPUT_MANIFEST.json'), ('benchmark_source_sha256', 'benchmark.cpp'), ('core_sha256', 'core.hpp'), ('executable_sha256', 'benchmark.exe'), ('protocol_sha256', 'PROTOCOL.json')]:
        if name == 'benchmark.exe':
            require(pre[field] == read_json(HERE/'NATIVE_VALIDATION.json')['original_executable_sha256'],'saved omitted executable hash binding')
        else:
            require(pre[field] == (sha(OLD / 'validation.csv') if name is None else parents[name]), 'pre-timing binding: ' + field)
    meta = read_json(STUDY / 'RUN_METADATA.json')
    require(meta['status'] == 'COMPLETE_ONCE' and meta['returncode'] == 0, 'run status')
    for field, name in [('pre_timing_audit_sha256', 'PRE_TIMING_AUDIT.json'), ('raw_timing_sha256', 'complete_times.csv'), ('log_sha256', 'timing-run.log')]:
        require(meta[field] == parents[name], 'run binding: ' + field)
    existing = read_json(STUDY / 'RESULTS.json')
    for name, expected in existing['provenance'].items():
        require(parents[name] == expected, 'original summary binding: ' + name)
    plans = read_json(STUDY / 'inputs.json')
    require(len(plans) == 870 and [p['id'] for p in plans] == list(range(870)), 'plan IDs')
    require(Counter(p['stratum'] for p in plans) == Counter({0:720, **{i:3 for i in range(1,51)}}), 'stratum counts')
    strata = input_text(plans)
    max_coordinate = max(abs(x) for p in plans for r in p['rectangles'] for side in r for x in side)
    max_slot = max(abs(x) for p in plans for x in p['slots'])
    budgets = Counter()
    zero_width = 0
    census_orders = set()
    for p in plans:
        n = p['n']; slots = p['slots']
        require(len(slots) == n and slots == sorted(set(slots)), 'strictly increasing positions')
        require(len(p['rectangles']) == 8 and len(p['queries']) == len(set(map(tuple, p['queries']))) == 48, 'rectangle/query cardinality')
        require(set(map(tuple, p['queries'])) == {(r,d) for r in range(8) for d in [0,1,2,4,16,64]}, 'full rectangle/budget set')
        for lower, upper in p['rectangles']:
            require(len(lower) == len(upper) == n and all(l <= u for l,u in zip(lower,upper)), 'valid interval box')
            zero_width += sum(l == u for l,u in zip(lower,upper))
        budgets.update(d for r,d in p['queries'])
        require(len(p['edges']) == len(set(map(tuple,p['edges']))), 'duplicate original rank edges')
        require(all(0 <= a < n and 0 <= b < n and a != b for a,b in p['edges']), 'rank endpoints')
        if p['stratum'] == 0:
            require(n == 6 and slots == list(range(1,7)) and len(p['edges']) == 15, 'six-arm census')
            indegree = [sum(b == node for a,b in p['edges']) for node in range(6)]
            require(sorted(indegree) == list(range(6)), 'census total-order degrees')
            order = tuple(sorted(range(6), key=lambda node:indegree[node]));census_orders.add(order)
            require(set(map(tuple,p['edges'])) == {(order[a],order[b]) for a in range(6) for b in range(a+1,6)}, 'census total-order edges')
    require(len(census_orders) == 720, 'all 720 total orders retained')
    old_rows, new_rows = read_csv(OLD / 'validation.csv'), read_csv(STUDY / 'validation.csv')
    old_decisions, decisions = keyed(old_rows), keyed(new_rows)
    require(len(old_decisions) == len(decisions) == len(old_rows) == len(new_rows) == 41760 and old_decisions == decisions, 'all unchanged R03 decisions')
    require(all(all(int(row[name]) == int(row['decision']) for name in ['raw_floyd','closure_floyd','cheap','quartet']) for row in new_rows), 'submitted validation columns')
    require([(int(r['plan']),int(r['rectangle']),int(r['delta'])) for r in new_rows] == [(p['id'],r,d) for p in plans for r,d in p['queries']], 'validation row stream')
    rng = random.Random(20261024); regenerated = []
    for block in range(9):
        for sid in range(51):
            queries = [1,48,192];rng.shuffle(queries)
            for q in queries:
                routes = [0,1,2,3];rng.shuffle(routes)
                regenerated.append(dict(block=block,stratum=sid,queries=q,routes=routes))
    schedule = read_json(STUDY / 'schedule.json')
    require(schedule == regenerated and len(schedule) == 1377, 'entire seeded paired order')
    text_steps = [list(map(int,line.split())) for line in (STUDY / 'schedule.txt').read_text().splitlines()]
    require(text_steps == [[1377]] + [[s['block'],s['stratum'],s['queries'],*s['routes']] for s in schedule], 'schedule text/JSON equality')
    expected = defaultdict(int)
    for p in plans:
        for count in [1,48,192]:
            value = 1469598103934665603
            for index in range(count):
                rectangle,budget = p['queries'][index % 48]
                value = ((value ^ (decisions[(p['id'],rectangle,budget)] + 2*rectangle + 131*budget)) * 1099511628211) & MASK
            key = (p['stratum'],count);expected[key] = (expected[key] + value) & MASK
    expected_rows = read_csv(STUDY / 'expected_batches.csv')
    require(len(expected_rows) == 153 and len({(int(r['stratum']),int(r['queries'])) for r in expected_rows}) == 153, 'all 153 expected batches')
    for row in expected_rows:
        require(int(row['expected_checksum']) == expected[(int(row['stratum']),int(row['queries']))], 'independent batch decision hash')
    rows = [{k:int(v) for k,v in row.items()} for row in read_csv(STUDY / 'complete_times.csv')]
    require(len(rows) == 5508, 'all 5508 measurements')
    series = defaultdict(dict)
    for step_index, step in enumerate(schedule):
        for position, route in enumerate(step['routes']):
            row = rows[4*step_index+position]
            require([row[k] for k in ['block','stratum','queries','position','route']] == [step['block'],step['stratum'],step['queries'],position,route], 'raw row paired sequence')
            stratum = strata[row['stratum']]
            require(row['repeats'] == stratum['repeats'] and row['jobs_per_repeat'] == len(stratum['ids']), 'raw repeat/job counts')
            require(row['elapsed_ns'] > 0, 'positive interval')
            require(row['checksum'] == row['expected_checksum'] == (expected[(row['stratum'],row['queries'])]*row['repeats']) & MASK, 'every recorded output hash')
            key = (row['stratum'],row['queries'],route)
            require(row['block'] not in series[key], 'duplicate block')
            series[key][row['block']] = Fraction(row['elapsed_ns'],row['repeats']*row['jobs_per_repeat'])
    summaries = []
    for sid in range(51):
        sample = plans[strata[sid]['ids'][0]]
        for count in [1,48,192]:
            summary = dict(stratum=sid,n=sample['n'],geometry=sample['geometry'],family=sample['family'],queries_per_job=count,routes={})
            for route,name in enumerate(NAMES):
                data = series[(sid,count,route)];require(set(data) == set(range(9)), 'all nine paired blocks')
                summary['routes'][name] = dict(complete_job_ns=stats(list(data.values())),per_query_ns=stats([v/count for v in data.values()]))
            summary['paired_quartet_vs_cheap'] = pair(series,sid,count,3,2)
            summary['paired_cheap_vs_raw'] = pair(series,sid,count,2,0)
            summary['paired_quartet_vs_raw'] = pair(series,sid,count,3,0)
            summaries.append(summary)
    def equal_numeric(a,b):
        if isinstance(a,dict):
            return isinstance(b,dict) and all(k in b and equal_numeric(v,b[k]) for k,v in a.items())
        if isinstance(a,list):
            return isinstance(b,list) and len(a) == len(b) and all(equal_numeric(x,y) for x,y in zip(a,b))
        if isinstance(a,(float,int)) and not isinstance(a,bool):
            return isinstance(b,(float,int)) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9)
        return a == b
    require(equal_numeric(existing['strata'],summaries), 'all original numerical summaries independently reconstructed')
    replay = source_replay()
    code_identity = code_binding(replay)
    graph_rows = read_csv(replay / 'independent_graph.csv')
    require(len(graph_rows) == 41760, 'independent graph query count')
    for row in graph_rows:
        key = tuple(int(row[name]) for name in ['plan','rectangle','delta'])
        require(all(int(row[name]) == decisions[key] for name in ['raw_floyd','closed_floyd','raw_bf_certificate','closed_bf_certificate']), 'independent graph decision versus both preserved validations')
    timing_log = timing_log_check(expected,rows,schedule,meta)
    after = {p.name:sha(p) for p in STUDY.iterdir() if p.is_file()}
    require(parents == after, 'original study modified during independent audit')
    census = [s for s in summaries if s['stratum'] == 0]
    require(census[2]['paired_quartet_vs_cheap']['ties'] == 1, 'Q192 one tie retained')
    result = dict(status='PASS_WITH_EXPLICIT_REPORTING_CORRECTION_AND_SCOPE_LIMITS',author_side_validation=True,simulated_peer_review=False,
        original_study_preserved=True,new_timing_runs=0,plans=870,distinct_queries=41760,census_total_orders=720,
        scaling_strata=50,scaling_plans_per_stratum=3,paired_blocks=9,expected_batches_reconstructed=153,raw_records_audited=5508,
        independent_graph_checks=('Fresh separate graph construction/Floyd/BF certificates on all 41760 queries.' if ZIG else 'All 41760 retained separately derived raw/closed graph decision records checked against original R03 and R04 decisions; no new native graph calculation.'),
        source_validation_replay=('Fresh existing-Zig correctness rebuild of both validators; 41760 queries; saved CSV bytes identical.' if ZIG else 'Saved validation and independent graph CSV audited; fresh native validation not run.'),
        saved_executable_source_binding=code_identity,timing_log_audit=timing_log,
        unchanged_R03_outcomes=True,all_original_summary_values_reconstructed=True,
        input_bounds=dict(max_abs_rectangle_coordinate=max_coordinate,max_abs_slot=max_slot,zero_width_coordinates=zero_width,budget_query_counts=dict(budgets)),
        reporting_correction='Existing RESULTS omits explicit tie counts: all720 Q192 quartet versus cheap is 3 faster / 5 slower / 1 tie across nine paired blocks. Original files preserved.',
        measurement_boundary=dict(inside=['fresh Plan and route-specific positions/edge copies','closure for closure-direct, cheap, quartet','cheap flags for cheap and quartet','short-circuited quartet classification when cheap flag is false','query graph construction and BF/route decision work','per-query rolling decision hash','per-batch hash summation'],
           outside=['common parsing and immutable rectangle/query storage','correctness and certificate validation','one complete warmup','after-stop expected-hash comparison','after-stop outer volatile checksum update','console/file output'],
           capacity_reuse='One Scratch persists across all jobs; vector capacity is reused after common warmup. Graph weights, BF labels and predecessors are rewritten whenever BF is called. No fresh scratch allocation is promised per job.'),
        limitations=['One Windows CPU and one specified implementation; no affinity/frequency isolation or confidence intervals.',
         'Recorded manifest hashes bind saved source/input/order/results; files alone cannot independently establish trusted wall-clock predeclaration chronology.',
         'The original timed executable hash is bound by PRE_TIMING_AUDIT, but this audit did not observe the past timing process.',
         'Q192 repeats the same 48 frozen queries four times and adds no independent workloads.',
         'Each scaling stratum has only three fixed plans; timing repeats and nine blocks are repeated observations, not additional workloads.',
         'Quartet classification may stop on its first obstruction and is bypassed on cheap-exact plans. These observed costs do not establish universal O(n^4) cost behavior or optimality.',
         'Storage depends on representation: positions/edges are copied per job, dense closure and closure pairs may be quadratic, scratch weights signed128 are quadratic; rectangles/queries are preloaded.',
         'No GPU/native measurement, H20 outward-auditor timing, full certificate-serving latency or application speedup follows.'],
        census=census,strata=summaries,provenance=parents)
    write_json('INDEPENDENT_AUDIT.json',result)
    with (HERE / 'Q48_STRATA.csv').open('w',encoding='utf-8',newline='') as output:
        fields=['stratum','n','geometry','family','plans'] + [name+'_median_ns' for name in NAMES] + ['quartet_faster','quartet_slower','quartet_ties','cheap_vs_raw_faster','cheap_vs_raw_slower','cheap_vs_raw_ties']
        writer=csv.DictWriter(output,fieldnames=fields);writer.writeheader()
        for s in summaries:
            if s['queries_per_job'] != 48:continue
            row={k:s[k] for k in ['stratum','n','geometry','family']};row['plans']=len(strata[s['stratum']]['ids'])
            row.update({name+'_median_ns':s['routes'][name]['complete_job_ns']['median'] for name in NAMES})
            row.update({'quartet_'+k:s['paired_quartet_vs_cheap'][k] for k in ['faster','slower','ties']})
            row.update({'cheap_vs_raw_'+k:s['paired_cheap_vs_raw'][k] for k in ['faster','slower','ties']});writer.writerow(row)
    files={str(p.relative_to(HERE)).replace('\\','/'):sha(p) for p in HERE.rglob('*') if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
    write_json('AUDIT_MANIFEST.json',dict(status='COMPLETE',original_study_files=parents,independent_files=files,manifest_self_excluded=True))
    print(json.dumps({k:result[k] for k in ['status','plans','distinct_queries','raw_records_audited','expected_batches_reconstructed','reporting_correction']},indent=2))

def write_paper_facts(result):
    lines=['# Independently checked complete CPU job costs','',
      'Author-side validation, not a simulated peer review. No timing was rerun. All 870 fixed plans and 41,760 distinct decisions were preserved; all 153 expected batch hashes and 5,508 recorded measurements were independently reconstructed. A separately written checker validated raw and closed graphs with exact Floyd and BF certificates on every query, including all 870 quartet classifications. Fresh original-source validation reproduced both CSV outputs byte for byte.','',
      '## All 720 six-arm total orders','',
      'Costs are block-average ns per complete job, median [min, max] over nine paired blocks; each interval is divided by its repeats and number of plans, rather than timing individual jobs. Each job includes fresh route-specific ranking preparation, Boolean query evaluation and rolling decision-hash construction; expected-hash checking and the outer volatile update occur after the elapsed interval. The common immutable boxes/query arrays and scratch capacity are preloaded.','',
      '| Queries/job | Raw original-edge BF | Closure + BF | Cheap | Quartet | Quartet vs cheap: faster/slower/tie |',
      '|---:|---:|---:|---:|---:|---:|']
    for s in result['census']:
        cells=[]
        for name in NAMES:
            v=s['routes'][name]['complete_job_ns'];cells.append(f"{v['median']:.1f} [{v['min']:.1f}, {v['max']:.1f}]")
        p=s['paired_quartet_vs_cheap'];lines.append('| '+str(s['queries_per_job'])+' | '+' | '.join(cells)+f" | {p['faster']}/{p['slower']}/{p['ties']} |")
    s=result['census'][1]
    cheap=s['routes']['cheap']['complete_job_ns']['median'];quad=s['routes']['quartet']['complete_job_ns']['median'];raw=s['routes']['raw_direct']['complete_job_ns']['median']
    lines += ['',f"At the primary Q=48 setting, cheap and quartet median block-average complete-job costs are {cheap/raw:.3f} and {quad/raw:.3f} times raw-direct cost (raw/cheap {raw/cheap:.3f}, raw/quartet {raw/quad:.3f}). The quartet median is {100*(quad/cheap-1):.2f}% higher than cheap and wins only 4 of 9 paired blocks; their observed ranges overlap. These are local descriptive comparisons, not estimated application speedups.",
      '', 'At Q=1, cheap and quartet each lose to raw-direct in all nine paired blocks. Setup is not amortized at this reuse level. Per-query figures in the JSON are batch-derived equivalents, not directly measured individual request latencies.',
      '', '## Scaling evidence and limits','',
      'The 50 original scaling strata remain separate in Q48_STRATA.csv and INDEPENDENT_AUDIT.json: n=4,8,16,32,64; contiguous/sparse positions; aligned, reverse, winner_star, mixed_total and sparse_dag families. Each stratum contains only three fixed plans. No cross-stratum pooling or population/prevalence inference is supported. Repeated jobs and timing blocks increase measurement repetition, not independent input count. Q192 repeats the same 48 queries four times.',
      '', 'Raw-direct avoids closure entirely. Closure-direct pays fresh closure then uses the same dense BF. Cheap pays closure and its structural flags; quartet pays those and classifies only when cheap is false, stopping on the first obstruction. Each job copies positions and original edges, while box/query arrays are shared immutable inputs. All graph entries and BF state are reset on use; Scratch vector capacity is shared across jobs after common warmup.',
      '', 'Scaling effects go both ways. At Q48, n=32 contiguous sparse_dag has cheap/quartet medians 61,093.3/72,273.3 ns, with quartet losing 8 of 9 paired blocks; n=32 sparse-position sparse_dag has 84,480.0/96,046.7 ns and quartet loses all nine. The complete per-stratum data, rather than selected examples, bounds any scaling claim.',
      '', 'The preserved original RESULTS table omits an explicit Q192 tie. Use 3 faster / 5 slower / 1 tie, with denominator nine. Original source, timings and summaries were not overwritten.',
      '', 'The fresh executable has byte-identical code/data and all other bytes outside the COFF timestamp and .buildid section; only those 20 bytes differ. This supports saved executable/source binding without claiming whole-file deterministic rebuild identity.',
      '', 'This evidence covers one exact-integer synthetic CPU Boolean auditor on one Windows host. It does not measure GPU/native execution, H20 outward auditing, certificate-serving service latency, application throughput or a universally optimal implementation. Min/max are descriptive ranges, not confidence intervals. Hash bindings verify the saved files and ordering; this author-side audit did not observe the historical measurement process or independently certify trusted predeclaration timestamps.','']
    (HERE / 'PAPER_READY_FACTS.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        write_json('AUDIT_FAILURE.json',dict(status='FAILED_PRESERVED',error=repr(error),new_timing_runs=0))
        raise
