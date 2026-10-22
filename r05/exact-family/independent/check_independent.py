"""Independent author-side R05 audit. Never executes benchmark time mode.

Only writes beside this script. Graphs use separate inequality edges and a
synchronous shortest-path algorithm; assignment enumeration does not call the
author's quartet/BF/Floyd implementation. Python integers are unbounded.
"""
from pathlib import Path
from itertools import combinations, permutations
from datetime import datetime, timezone
import csv, difflib, hashlib, json, math, random, re, statistics, struct

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
OLD = BASE.parents[1] / 'r04-analysis/hopper-end-to-end'
MASK = (1 << 64) - 1
QS = [1, 48, 192, 768]
ROUTES = ['Raw', 'Closed', 'Cheap', 'Quartet']
checks = []

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def ck(name, condition, detail=None):
    checks.append(dict(name=name, status='PASS' if condition else 'FAIL', detail=detail))
    if not condition:
        raise AssertionError(name + ': ' + str(detail))

def readjson(n):
    return json.loads((BASE/n).read_text(encoding='utf-8'))

def rows(p):
    with p.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def writejson(n, value):
    (OUT/n).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def declarations():
    result = []
    repeat = {4:100, 8:20, 16:5, 32:2, 64:1}
    for n in [4, 8, 16, 32, 64]:
        for family in ['first', 'last', 'all']:
            swapped = {0} if family == 'first' else {n-2} if family == 'last' else set(range(0,n,2))
            order = [i+1 if i in swapped else i-1 if i-1 in swapped else i for i in range(n)]
            rank = [order.index(i) for i in range(n)]
            rect = []
            for k in range(48):
                delta = 32 + k % 5
                bias = delta if k % 2 == 0 else -delta
                theta = [(1+k%3)*r for r in rank]
                centre = [theta[i]+bias*(i+1) for i in range(n)]
                halfwidth = 1+k%4
                rect.append(dict(l=[x-halfwidth for x in centre], u=[x+halfwidth for x in centre], theta=theta, slope=bias))
            i = len(result)
            result.append(dict(id=i, stratum=i, n=n, family=family, order=order,
                positions=list(range(1,n+1)), edges=[list(x) for x in zip(order,order[1:])],
                expected_exact=True, rectangles=rect, queries=[[k,32+k%5] for k in range(48)], repeats=repeat[n]))
    return result

def independent_text(plans):
    lines = ['15 15']
    for p in plans:
        lines += [f"{p['id']} {p['id']} {p['n']} {p['n']-1} 1", ' '.join(map(str,p['positions']))]
        lines += [' '.join(map(str,e)) for e in p['edges']]
        for r in p['rectangles']:
            lines += [' '.join(map(str,r[z])) for z in ['l','u']]
        lines += [' '.join(map(str,q)) for q in p['queries']]
    lines += [f"{p['id']} {p['repeats']} 1 {p['id']}" for p in plans]
    # Actual producer is Windows Path.write_text(newline=None): CRLF bytes.
    return ('\r\n'.join(lines)+'\r\n').encode()

def assignment_checks(p):
    """Enumerate all directed disjoint two-set assignments, then all sizes n<=8."""
    n = p['n']; rank = [p['order'].index(i) for i in range(n)]
    admitted = tested = 0
    for endpoints in combinations(range(n), 4):
        for source in combinations(endpoints, 2):
            target = tuple(x for x in endpoints if x not in source)
            free = sum(abs(a-b) for a,b in zip(source,target))
            best = math.inf
            for target_order in (target, target[::-1]):
                if all(rank[a] < rank[b] for a,b in zip(source,target_order)):
                    best = min(best, sum(abs(a-b) for a,b in zip(source,target_order)))
            tested += 1
            if best != math.inf:
                admitted += 1
                if best != free:
                    raise AssertionError(('quartet counterexample',p['id'],source,target,best,free))
    full = {'tested_endpoint_pairs':0, 'admitted_endpoint_pairs':0, 'enumerated_bijections':0}
    if n <= 8:
        for size in range(1,n//2+1):
            for source in combinations(range(n),size):
                rest = [x for x in range(n) if x not in source]
                for target in combinations(rest,size):
                    full['tested_endpoint_pairs'] += 1
                    free = min(sum(abs(a-b) for a,b in zip(source,t)) for t in permutations(target))
                    allowed = []
                    for t in permutations(target):
                        full['enumerated_bijections'] += 1
                        if all(rank[a]<rank[b] for a,b in zip(source,t)):
                            allowed.append(sum(abs(a-b) for a,b in zip(source,t)))
                    if allowed:
                        full['admitted_endpoint_pairs'] += 1
                        if min(allowed) != free:
                            raise AssertionError(('assignment counterexample',p['id'],source,target))
    return dict(plan=p['id'], n=n, family=p['family'], quartet_directed_cuts=tested,
                quartet_admitted_cuts=admitted, full_assignment=full if n<=8 else 'not enumerated; analytic proof and all quartets')

def edges_for(p, r, delta, closed):
    """Parallel edge inequality system, not an author dense-graph translation."""
    n=p['n']; edges=[]
    # theta[v] - theta[u] <= U[v]-L[u] + delta*|j[v]-j[u]|.
    for u in range(n):
        for v in range(n):
            if u != v:
                edges.append((u,v,r['u'][v]-r['l'][u]+delta*abs(p['positions'][v]-p['positions'][u])))
    if closed:
        for a,b in combinations(p['order'],2):
            edges.append((b,a,0))
    else:
        edges.extend((b,a,0) for a,b in p['edges'])
    return edges

def synchronous_shortest_paths(n, edges):
    # Dynamic programming for paths of <=k edges from a zero super-source.
    d=[0]*n
    for turn in range(n):
        nextd=d.copy()
        for u,v,w in edges:
            nextd[v]=min(nextd[v],d[u]+w)
        if nextd==d:
            assert all(d[v]-d[u]<=w for u,v,w in edges)
            return True,d,turn+1
        d=nextd
    return False,d,n

def independent_query(p, r, delta):
    rank = [p['order'].index(i) for i in range(p['n'])]
    pairs = [(a,b) for a in range(p['n']) for b in range(p['n']) if rank[a]<rank[b]]
    cheap = (p['n']<4 or all(a<b for a,b in pairs) or all(a>b for a,b in pairs)
             or len({a for a,b in pairs})<=1 or len({b for a,b in pairs})<=1)
    beta = all(r['l'][a]-r['u'][b]<=delta*abs(a-b) for a,b in pairs)
    span = all((p['n']-2)*(r['l'][a]-r['u'][b])<=delta*abs(a-b) for a,b in pairs)
    return cheap,beta,span

def binary_binding():
    """Ignore COFF timestamp, its .buildid debug copies, and RSDS build GUID."""
    paths=[BASE/'benchmark.exe',OUT/'benchmark.exe']
    raw=[bytearray(p.read_bytes()) for p in paths]
    detail=[]
    for b in raw:
        pe=struct.unpack_from('<I',b,0x3c)[0]
        assert b[pe:pe+4]==b'PE\0\0'
        stamp=pe+8
        rsds=[m.start() for m in re.finditer(b'RSDS',b)]
        assert len(rsds)==1
        guid=rsds[0]+4
        opt=pe+24
        assert struct.unpack_from('<H',b,opt)[0]==0x20b
        debugrva,debugsize=struct.unpack_from('<II',b,opt+112+6*8)
        count=struct.unpack_from('<H',b,pe+6)[0]
        sectionbase=opt+struct.unpack_from('<H',b,pe+20)[0]
        sections=[struct.unpack_from('<8sIIIIIIHHI',b,sectionbase+i*40) for i in range(count)]
        section=next(s for s in sections if s[2]<=debugrva<s[2]+s[1])
        assert section[0].rstrip(b'\0')==b'.buildid'
        debugraw=debugrva-section[2]+section[4]
        debugstamps=[]
        for at in range(debugraw,debugraw+debugsize,28):
            assert b[at+4:at+8]==b[stamp:stamp+4]
            debugstamps.append(at+4)
        detail.append(dict(bytes=len(b),timestamp_offset=stamp,coff_timestamp=bytes(b[stamp:stamp+4]).hex(),
                           build_guid_offset=guid,build_guid=bytes(b[guid:guid+16]).hex(),
                           buildid_debug_timestamp_copies=debugstamps,
                           pdb_suffix=bytes(b[guid+20:b.index(0,guid+20)]).decode(errors='replace')))
        for at in debugstamps:
            b[at:at+4]=bytes(4)
        b[stamp:stamp+4]=bytes(4)
        b[guid:guid+16]=bytes(16)
    differences=[i for i,(x,y) in enumerate(zip(raw[0],raw[1])) if x!=y]
    normalized_equal=(raw[0]==raw[1])
    ck('Rebuilt PE equal after only COFF timestamp, its buildid copies and RSDS GUID normalization',normalized_equal,
       dict(original_sha256=sha(paths[0]),rebuilt_sha256=sha(paths[1]),headers=detail,remaining_differences=differences[:40]))
    return checks[-1]['detail']

def main():
    plans=declarations()
    ck('All 15 rankings and 720 full rectangle declarations equal independent reconstruction',readjson('inputs.json')==plans)
    ck('Entire inputs.txt exactly equals independent declaration serialization',(BASE/'inputs.txt').read_bytes()==independent_text(plans))
    actual_inputs={(tuple(p['order']),tuple(p['positions']),tuple(r['l']),tuple(r['u']),32+k%5) for p in plans for k,r in enumerate(p['rectangles'])}
    ck('All 720 actual ranking/rectangle/budget queries are distinct',len(actual_inputs)==720)
    manifest=readjson('INPUT_MANIFEST.json')
    ck('All frozen input manifest hashes',all(sha(BASE/n)==h for n,h in manifest['files'].items()),manifest['files'])
    ck('R04 source binding hashes',all(sha(OLD/n)==h for n,h in manifest['source_binding'].items()))
    oldcore=(OLD/'core.hpp').read_text(); newcore=(BASE/'core.hpp').read_text()
    oldcpp=(OLD/'benchmark.cpp').read_text(); newcpp=(BASE/'benchmark.cpp').read_text()
    ck('Core algorithm bytes identical except Rect 8 to 48',newcore==oldcore.replace('std::array<Rect,8>','std::array<Rect,48>'))
    expectedcpp=oldcpp.replace('np==870&&ns==51','np==15&&ns==15').replace('nr==9*51*3','nr==9*15*4')
    expectedcpp=expectedcpp.replace('for(int q:{1,48,192})','for(int q:{1,48,192,768})').replace('std::array<uint64_t,3>','std::array<uint64_t,4>')
    expectedcpp=expectedcpp.replace('q==1?0:q==48?1:2','q==1?0:q==48?1:q==192?2:3').replace('b.q==1?0:b.q==48?1:2','b.q==1?0:b.q==48?1:b.q==192?2:3')
    expectedcpp=expectedcpp.replace('complete_batch_hashes=153','complete_batch_hashes=60')
    ck('Benchmark identical except declared corpus counts and Q indexing',newcpp==expectedcpp)
    diff=''.join(difflib.unified_diff(oldcore.splitlines(True),newcore.splitlines(True),fromfile='R04/core.hpp',tofile='R05/core.hpp'))
    diff+=''.join(difflib.unified_diff(oldcpp.splitlines(True),newcpp.splitlines(True),fromfile='R04/benchmark.cpp',tofile='R05/benchmark.cpp'))
    ck('Declared SOURCE_DIFF.patch equals actual R04 to R05 diff',(BASE/'SOURCE_DIFF.patch').read_text()==diff)
    source=(BASE/'prepare.py').read_text()
    ck('Generator has expected guarded initialization and frozen seed',"assert not (HERE/'INPUT_MANIFEST.json').exists()" in source and 'random.Random(20261025)' in source)
    replay=OUT/'generator-replay'
    replay.mkdir(exist_ok=True)
    if not (replay/'INPUT_MANIFEST.json').exists():
        for name in ['prepare.py','PROTOCOL.md']:
            (replay/name).write_bytes((BASE/name).read_bytes())
        replay_source=source.replace('HERE = Path(__file__).resolve().parent','HERE = REPLAY').replace("OLD = HERE.parents[1] / 'r04-analysis/hopper-end-to-end'",'OLD = BASELINE')
        env=dict(__file__=str(BASE/'prepare.py'),__name__='independent_generator_replay',REPLAY=replay,BASELINE=OLD)
        exec(compile(replay_source,str(BASE/'prepare.py'),'exec'),env)
        env['main']()
    ck('Actual frozen generator replays byte-exact in independent directory',all((replay/n).read_bytes()==(BASE/n).read_bytes() for n in [*manifest['files'],'INPUT_MANIFEST.json']))
    # Independent schedule reproduction checks actual rows and shuffle seed.
    rng=random.Random(20261025); schedule=[]
    for block in range(9):
        for p in plans:
            queries=QS.copy(); rng.shuffle(queries)
            for q in queries:
                routes=list(range(4)); rng.shuffle(routes)
                schedule.append(dict(block=block,stratum=p['id'],queries=q,routes=routes))
    ck('All 540 shuffled batches equal prospectively seeded schedule',schedule==readjson('schedule.json'))
    schedulebytes=(str(len(schedule))+'\n'+''.join(' '.join(map(str,[s['block'],s['stratum'],s['queries'],*s['routes']]))+'\n' for s in schedule)).replace('\n','\r\n').encode()
    ck('Whole schedule.txt equals independent schedule',(BASE/'schedule.txt').read_bytes()==schedulebytes)
    pre=readjson('PRE_TIMING_AUDIT.json'); meta=readjson('RUN_METADATA.json')
    ck('All pre-timing bindings still match',all(sha(BASE/n)==h for n,h in pre['bindings'].items()))
    ck('Run metadata bindings match frozen audit, raw rows, and log',meta['source_audit_sha256']==sha(BASE/'PRE_TIMING_AUDIT.json') and meta['raw_timing_sha256']==sha(BASE/'complete_times.csv') and meta['log_sha256']==sha(BASE/'timing-run.log'))
    binding=binary_binding()
    assembly=(OUT/'benchmark.s').read_text(encoding='utf-8')
    required_asm=['call\t_Z12prepare_planRK4Plani','call\t_Z5queryRK4PlanRK4RectiiR7ScratchPi',
                  'call\t_Z12complete_jobRK4PlaniiR7Scratch','movabs\trax, 1099511628211',
                  'movabs\trsi, 1469598103934665603','#APP','#NO_APP',
                  'call\t_ZNSt3__16chrono12steady_clock3nowEv','call\t_Z7quartetRK4Plan','call\t_Z5closeR4Plan']
    ck('Optimized assembly retains preparation, query loop, hash multiply and timed complete-job calls',all(x in assembly for x in required_asm),dict(assembly_sha256=sha(OUT/'benchmark.s'),symbols=required_asm))
    ck('Rebuilt validation rows match original byte for byte',(OUT/'validation.csv').read_bytes()==(BASE/'validation.csv').read_bytes())
    ck('Rebuilt complete hash rows match original byte for byte',(OUT/'expected_batches.csv').read_bytes()==(BASE/'expected_batches.csv').read_bytes())
    ck('Rebuilt census rows match original byte for byte',(OUT/'routing_census.csv').read_bytes()==(BASE/'routing_census.csv').read_bytes())
    assignments=[]
    for p in plans:
        assignments.append(assignment_checks(p))
        print('Independent assignments PASS',p['id'],p['n'],p['family'],flush=True)
    writejson('ASSIGNMENT_CHECKS.json',assignments)
    ck('Independent quartet checks all 15 complete rankings',True,dict(directed_cuts=sum(x['quartet_directed_cuts'] for x in assignments),admitted_cuts=sum(x['quartet_admitted_cuts'] for x in assignments)))
    validation=rows(BASE/'validation.csv'); certs=[]; census=[]; expected={}
    bound=0
    for p in plans:
        n=p['n']; cg=qg=0
        for ri,r in enumerate(p['rectangles']):
            delta=32+ri%5; cheap,beta,span=independent_query(p,r,delta)
            ckrow=[]
            for closed in [False,True]:
                e=edges_for(p,r,delta,closed)
                bound=max(bound,max(abs(w) for a,b,w in e))
                decision,potential,turns=synchronous_shortest_paths(n,e)
                assert decision
                assert all(r['theta'][b]-r['theta'][a]<=w for a,b,w in e)
                ckrow.append(dict(graph='closed' if closed else 'raw',potential=potential,turns=turns,edges=len(e)))
            vr=validation[p['id']*48+ri]
            assert (int(vr['plan']),int(vr['rectangle']),int(vr['delta']))==(p['id'],ri,delta)
            assert all(vr[k]=='1' for k in ['decision','raw_floyd','closure_floyd','cheap','quartet'])
            assert not cheap and beta and not span
            cg+=1
            certs.append(dict(plan=p['id'],rectangle=ri,delta=delta,admit=True,cheap=cheap,beta_admit=beta,span_admit=span,graphs=ckrow))
        census.append(dict(plan=p['id'],n=n,cheap_flag=0,quartet_flag=1,queries=48,cheap_graph=cg,quartet_graph=qg))
        for q in QS:
            h=1469598103934665603
            for qi in range(q):
                ri=qi%48; d=32+ri%5
                h=((h ^ (1+2*ri+131*d))*1099511628211)&MASK
            expected[p['id'],q]=h
    writejson('GRAPH_CERTIFICATES.json',certs)
    ck('All 720 decisions independently feasible with raw and closed graph certificates',len(certs)==720,dict(graph_certificates=1440,planted_edge_certificates=1440,max_absolute_edge_weight=bound))
    ck('Actual all-admit routing census matches independent beta/span/flags', [{k:int(v) for k,v in r.items()} for r in rows(BASE/'routing_census.csv')]==census,census)
    ck('All 60 complete batch rolling hashes independently reconstructed',all(expected[int(r['stratum']),int(r['queries'])]==int(r['expected_checksum']) for r in rows(BASE/'expected_batches.csv')) and len(rows(BASE/'expected_batches.csv'))==60)
    raw=rows(BASE/'complete_times.csv'); index={}; sequence=[]; outer=0
    for p in plans:
        for q in QS:
            outer=(outer+4*expected[p['id'],q])&MASK
    for r in raw:
        b,s,q,pos,route,reps,jobs,elapsed=[int(r[k]) for k in ['block','stratum','queries','position','route','repeats','jobs_per_repeat','elapsed_ns']]
        assert reps==plans[s]['repeats'] and jobs==1 and elapsed>0
        assert int(r['checksum'])==int(r['expected_checksum'])==(expected[s,q]*reps)&MASK
        key=(b,s,q,route); assert key not in index
        index[key]=elapsed/reps
        sequence.append((b,s,q,pos,route))
        outer=(outer+int(r['checksum']))&MASK
    desired=[(s['block'],s['stratum'],s['queries'],pos,route) for s in schedule for pos,route in enumerate(s['routes'])]
    ck('All 2160 raw rows, checksums, repeats, exact order and paired nine blocks',len(raw)==2160 and sequence==desired)
    log=(BASE/'timing-run.log').read_text()
    ck('Outer volatile checksum independently includes warmup and every timed hash',f'PASS_TIMING checksum={outer} steady=1 timer_period=1/1000000000 sizeof_signed128=16' in log,dict(checksum=outer))
    author=readjson('SUMMARY.json')['strata']; strata=[]
    for p in plans:
        sid=p['id']
        for q in QS:
            vals=[[index[b,sid,q,r] for b in range(9)] for r in range(4)]
            cheap_ratios=[vals[2][b]/vals[3][b] for b in range(9)]
            fastest_ratios=[min(vals[r][b] for r in range(3))/vals[3][b] for b in range(9)]
            a=author[len(strata)]
            assert a['plan']==sid and a['queries']==q
            assert a['medians_ns']==[statistics.median(v) for v in vals]
            assert a['minima_ns']==list(map(min,vals)) and a['maxima_ns']==list(map(max,vals))
            assert a['cheap_over_quartet_paired_ratios']==cheap_ratios
            assert a['quartet_faster']==sum(x>1 for x in cheap_ratios)
            assert a['quartet_slower']==sum(x<1 for x in cheap_ratios)
            assert a['quartet_ties']==sum(x==1 for x in cheap_ratios)
            row=dict(plan=sid,n=p['n'],family=p['family'],Q=q)
            for route,v in zip(ROUTES,vals):
                row[route+'_median_ns']=statistics.median(v); row[route+'_min_ns']=min(v); row[route+'_max_ns']=max(v)
            for name,v in [('Cheap_over_Quartet',cheap_ratios),('Fastest_old_over_Quartet',fastest_ratios)]:
                row[name+'_median']=statistics.median(v); row[name+'_min']=min(v); row[name+'_max']=max(v)
                row[name+'_quartet_wins']=sum(x>1 for x in v); row[name+'_quartet_losses']=sum(x<1 for x in v); row[name+'_ties']=sum(x==1 for x in v)
                row[name+'_paired_values']=v
            strata.append(row)
    ck('All author per-stratum medians/min/max and paired ratios recompute',len(strata)==60)
    writejson('ALL_STRATA.json',strata)
    keys=[k for k in strata[0] if not k.endswith('_paired_values')]
    with (OUT/'ALL_STRATA.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in strata)
    # Retain every no-gain cell and every mixed paired cell; no pooled timing median.
    crossover=[]
    for p in plans:
        group=[r for r in strata if r['plan']==p['id']]
        crossover.append(dict(n=p['n'],family=p['family'],
            first_sampled_Q_median_gain_vs_Cheap=next((r['Q'] for r in group if r['Cheap_over_Quartet_median']>1),None),
            first_sampled_Q_median_gain_vs_fastest_old=next((r['Q'] for r in group if r['Fastest_old_over_Quartet_median']>1),None),
            no_gain_Q_vs_Cheap=[r['Q'] for r in group if r['Cheap_over_Quartet_median']<=1],
            no_gain_Q_vs_fastest_old=[r['Q'] for r in group if r['Fastest_old_over_Quartet_median']<=1]))
    writejson('CROSSOVERS.json',crossover)
    facts=dict(status='PASS',scope='Author-side independent validation of a prospectively designed favorable synthetic CPU routing study; not a blind review.',
        plans=15,distinct_queries=720,query_counts=QS,raw_timing_rows=2160,paired_blocks=9,
        routing=dict(admitted=720,cheap_flags=0,quartet_flags=15,cheap_graph_queries=720,quartet_graph_queries=0,raw_graph_queries=720,closed_graph_queries=720),
        timed_logical_work=dict(complete_jobs_per_route=9*len(QS)*sum(p['repeats'] for p in plans),
            queries_per_route=9*sum(QS)*sum(p['repeats'] for p in plans),
            graph_builds_per_route=dict(Raw=9*sum(QS)*sum(p['repeats'] for p in plans),Closed=9*sum(QS)*sum(p['repeats'] for p in plans),Cheap=9*sum(QS)*sum(p['repeats'] for p in plans),Quartet=0),
            warmup_jobs_per_route=len(plans)*len(QS),warmup_queries_per_route=len(plans)*sum(QS)),
        exactness=dict(analytic='C_R=1 for arbitrary disjoint reversed adjacent pairs, proved in INDEPENDENT_AUDIT.md',quartet_directed_cuts=sum(x['quartet_directed_cuts'] for x in assignments),full_assignment_small_n=[x for x in assignments if x['n']<=8]),
        timing_original_only=dict(start_utc=meta['start_utc'],end_utc=meta['end_utc'],records=2160,performance_rerun=False),
        median_gain_cells_vs_Cheap=sum(r['Cheap_over_Quartet_median']>1 for r in strata),
        median_gain_cells_vs_fastest_old=sum(r['Fastest_old_over_Quartet_median']>1 for r in strata),
        no_gain_cells_vs_Cheap=[{k:r[k] for k in ['n','family','Q','Cheap_over_Quartet_median','Cheap_over_Quartet_min','Cheap_over_Quartet_max']} for r in strata if r['Cheap_over_Quartet_median']<=1],
        no_gain_cells_vs_fastest_old=[{k:r[k] for k in ['n','family','Q','Fastest_old_over_Quartet_median','Fastest_old_over_Quartet_min','Fastest_old_over_Quartet_max']} for r in strata if r['Fastest_old_over_Quartet_median']<=1],
        mixed_paired_cells=[{k:r[k] for k in ['n','family','Q','Cheap_over_Quartet_quartet_wins','Fastest_old_over_Quartet_quartet_wins']} for r in strata if 0<r['Cheap_over_Quartet_quartet_wins']<9 or 0<r['Fastest_old_over_Quartet_quartet_wins']<9],
        crossovers=crossover,
        limitations=['Deliberately favorable planted synthetic family; no independent application inputs or presence estimate.',
            'A cheaper adjacent-reversal family flag could replace the general quartet recognizer; no necessity/optimality claim.',
            'Q=192 and 768 repeat the same 48 immutable inputs; Q=1 uses only rectangle 0.',
            'One original ordinary Windows run, normal apps/PDF reviews active, heavy RTL deferred by request; no idle/affinity/frequency control claim.',
            'Steady-clock CPU process observations, no hardware/GPU/physical-time/outward-certificate-service claim.',
            'R04 adverse plans and timing remain unchanged; source baseline files were read only.'])
    writejson('PAPER_READY_FACTS.json',facts)
    audit=dict(status='PASS',created_utc=datetime.now(timezone.utc).isoformat(),checks=checks,
        binary_binding=binding,arithmetic_domain=dict(max_abs_graph_edge=bound,largest_n=64,signed128=True,
          comment='Actual geometry/width/delta tiny; even n^3*max_edge is far below 2^127. Precast int64 slot/span/quartet arithmetic and int hash payload also fit. uint64 rolling hash wraps deliberately.'),
        initial_failures=[
          'Independent auditor initial compile command selected parent workdir but created a redundant nested outputs directory; output independent directory missing. Only empty auditor-created directories removed after absolute-path and emptiness checks; original evidence unchanged.',
          'Independent auditor second command selected independent workdir while still using parent-relative source/output paths, causing census compile/copy failures and validation inputs missing. Corrected relative paths; no producer artifacts changed.',
          'First independent checker run failed its byte-exact inputs.txt serialization check because it assumed LF. Producer Path.write_text on Windows generated CRLF. Independent reconstruction corrected to actual declared platform byte serialization; original files/hashes unchanged.',
          'Second checker run failed incomplete PE normalization: two .buildid IMAGE_DEBUG_DIRECTORY TimeDateStamp copies were not yet normalized. Parsing proved these equal the corresponding COFF timestamp. Normalization now covers only that timestamp and its two .buildid copies plus RSDS GUID; all other PE bytes must match. FAILURE_PRESERVED.json retains this pre-correction result.',
          'Census recompilation emits -Wsometimes-uninitialized for b after short-circuit require. On any false first operand require exits through noreturn fail, so the read is unreachable. All planted admissions execute both operands; no observed/semantic undefined read. Source preserved.'],
        performance_rerun=False,limitations=facts['limitations'])
    writejson('INDEPENDENT_AUDIT.json',audit)
    # Source evidence immutable across the audit, including original timing/binary.
    source_names=['PROTOCOL.md','EXACT_FAMILY_ARGUMENT.md','prepare.py','core.hpp','benchmark.cpp','census.cpp','SOURCE_DIFF.patch','INPUT_MANIFEST.json','PRE_TIMING_AUDIT.json','inputs.json','inputs.txt','schedule.json','schedule.txt','validation.csv','expected_batches.csv','routing_census.csv','complete_times.csv','timing-run.log','RUN_METADATA.json','CPU_INVENTORY.json','summarize.py','SUMMARY.json','ALL_STRATA.csv','benchmark.exe','census.exe']
    writejson('SOURCE_MANIFEST.json',dict(status='PASS',files={n:sha(BASE/n) for n in source_names},baseline={n:sha(OLD/n) for n in ['core.hpp','benchmark.cpp']}))
    print('PASS independent audit checks=',len(checks),'strata=',len(strata),flush=True)

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        destination='FAILURE_PRESERVED.json'
        if (OUT/destination).exists():
            destination='FAILURE_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json'
        writejson(destination,dict(status='FAIL',exception=repr(e),checks=checks))
        raise
