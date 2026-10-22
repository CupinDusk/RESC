"""Independent edge framing, original-variable feasibility, and certificate audit.

No import of producer graph, log, generator, or audit code. The only shared
scientific inputs are PROTOCOL and the intentionally public timer interface.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations
from collections import Counter
import csv,gzip,hashlib,json,struct
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
S=10**60
H=10**70
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def csvrows(p):return [{k:int(v) for k,v in r.items()} for r in csv.DictReader(p.open(encoding='utf-8'))]

# A separately written exact Fraction evaluation, with exact sum rather than
# producer termwise scaled rounding. 170 terms; tail is bounded before any
# integer rounding. Binary reduction is explicit, and input x may be below 1.
@lru_cache(None)
def series(z):
    assert 0<=z<=Q(1,3)
    term=z;total=Q(0)
    for k in range(170):
        total+=term/(2*k+1);term*=z*z
    return 2*total,2*total+2*term/(341*(1-z*z))
@lru_cache(None)
def rational_log(x):
    assert x>0
    if x<1:
        a,b=rational_log(1/x);return -b,-a
    k=0;y=x
    while y>=2:y/=2;k+=1
    a,b=series((y-1)/(y+1));c,d=series(Q(1,3))
    return a+k*c,b+k*d
def floor(v):return v.numerator//v.denominator
def ceil(v):return -floor(-v)
def logints(x):
    a,b=rational_log(x)
    return floor(a*H),ceil(b*H)
def validate_enclosure(x,v):
    a,b=rational_log(x)
    assert Q(v[0],S)<=a<=b<=Q(v[1],S),(str(x),v)

# Original variables are z_i=-theta_i (0..5), bias_j (6..12).
# b_(i+1)-z_i in [l_i,u_i]; each adjacent bias step <=d in
# either direction; theta_p<=theta_q means z_q-z_p<=0.
# This does not use the producer's six-node eliminated graph.
def original_edges(bounds,d,claims,tight):
    edges=[]
    for i in range(6):
        l=bounds['l'][i][1 if tight else 0];u=bounds['u'][i][0 if tight else 1]
        edges.extend([(i,7+i,u),(7+i,i,-l)])
    for j in range(6):edges.extend([(6+j,7+j,d),(7+j,6+j,d)])
    edges.extend((p,q,0) for p,q in claims)
    return edges
def feasible(edges):
    # Synchronous Bellman-Ford relaxation, independently arranged edge-list
    # implementation. At most 12 edges in a simple 13-node path.
    dist=[0]*13
    for _ in range(13):
        nxt=dist.copy()
        for u,v,w in edges:nxt[v]=min(nxt[v],dist[u]+w)
        if nxt==dist:return True
        dist=nxt
    return False
def verdict(bounds,d,claims):
    if feasible(original_edges(bounds,d[0],claims,True)):return 'admit'
    if not feasible(original_edges(bounds,d[1],claims,False)):return 'reject'
    return 'unknown'
def box(bounds,d,claims):
    lo=max([Q(0)]+[Q(bounds['l'][p][0]-bounds['u'][q][1],abs(p-q)) for p,q in claims])
    hi=max([Q(0)]+[Q(bounds['l'][p][1]-bounds['u'][q][0],abs(p-q)) for p,q in claims])
    return ('admit' if hi<=d[0] else 'reject' if lo>d[1] else 'unknown'),lo,hi
def certificate(row,bounds,d,claims):
    cert=row['certificate']
    if row['path']=='admit':
        t=cert['theta_scaled'];b=cert['bias_scaled']
        assert len(t)==6 and len(b)==7 and b[0]==0
        assert all(abs(b[j+1]-b[j])<=d[0] for j in range(6))
        assert all(bounds['l'][i][1]<=t[i]+b[i+1]<=bounds['u'][i][0] for i in range(6))
        assert all(t[p]<=t[q] for p,q in claims)
        # Independent rigorous real-log comparisons in original variables.
        for i,(l,u) in enumerate(zip(CURRENT_LOWER,CURRENT_UPPER)):
            al,bl=rational_log(Q(l,1000));au,bu=rational_log(Q(u,1000))
            x=Q(t[i]+b[i+1],S);assert bl<=x<=au
        da,db=rational_log(Q(201,200))
        assert all(Q(abs(b[j+1]-b[j]),S)<=da for j in range(6))
    elif row['path']=='reject':
        cycle=cert['cycle'];weights=cert['weights']
        assert cycle and len(weights)==len(cycle)
        for k,(a,z) in enumerate(cycle):
            assert 0<=a<6 and 0<=z<6 and a!=z and z==cycle[(k+1)%len(cycle)][0]
            w=bounds['u'][z][1]-bounds['l'][a][0]+d[1]*abs(a-z)
            if (z,a) in claims:w=min(w,0)
            assert w==weights[k]
        assert sum(weights)==cert['total']<0
    else:
        assert row['path']=='unknown'
        assert not feasible(original_edges(bounds,d[0],claims,True))
        assert feasible(original_edges(bounds,d[1],claims,False))

KEYS=['reports','true','false','admit','reject','unknown','true_admit','true_reject','true_unknown','false_admit','false_reject','false_unknown','box_admit','box_reject','box_unknown','box_admit_path_reject']
def add(c,truth,row):
    c['reports']+=1;c['true' if truth else 'false']+=1;c[row['path']]+=1
    c[('true_' if truth else 'false_')+row['path']]+=1;c['box_'+row['box']]+=1
    c['box_admit_path_reject']+=row['box']=='admit' and row['path']=='reject'
def countdict(c):return {k:c[k] for k in KEYS}

def expected_cases(p):
    return [dict(case_id=4*v+i,vector_id=v,path_name=name,N=[2000+x for x in vec],D=ds)
            for v,vec in enumerate(p['vectors_v']) for i,(name,ds) in enumerate(p['divider_paths'].items())]
def invalid_cases(p):
    out=[]
    for fam in p['invalid_families']:
        reason=fam['reason'];key='quiet_edges_before_start' if reason==1 else 'change_at_subsequent_reference_edge' if reason==4 else 'quiet_edges_after_command_reset'
        for value in fam[key]:
            out.append(dict(id=len(out),reason=reason,N=fam['N'],D=fam['D'],quiet=value if reason!=4 else 2,change=value if reason==4 else 0,changed=fam.get('changed_D',fam['D'])))
    return out
def check_schedule(folder,p):
    fields=['rst','commandreset','start','cfgn','cfgd'];schedules=[];jobexpect=[];invalidexpect=[]
    cases=expected_cases(p)
    for c in cases:
        seg=[(1,1,(1,0,0,0,0))];e=1;prev=1000
        for j,(n,d) in enumerate(zip(c['N'],c['D'])):
            reset=e+1;start=e+4;end=start+n*d
            seg.extend([(reset,reset,(0,1,0,n,d)),(reset+1,start-1,(0,0,0,n,d)),(start,start,(0,0,1,n,d)),(start+1,end,(0,0,0,n+777,d))])
            jobexpect.append(dict(case_id=c['case_id'],vector_id=c['vector_id'],slot=j,scenario=c['case_id'],reset_edge=reset,start_edge=start,completion_edge=end,N=n,D=d,previous_D=prev,settled_at_start=2,T=n*d,lower=n*d-1,upper=n*d+1,job_pulses=n,valid=1,reason=0));prev=d;e=end
        schedules.append(seg)
    for f in invalid_cases(p):
        seg=[(1,1,(1,0,0,0,0))];n=f['N'];d=f['D'];q=f['quiet']
        if f['reason']==1:
            if q:seg.append((2,q+1,(0,0,0,n,d)))
            start=q+2
        else:
            seg.append((2,2,(0,1,0,n,d)))
            if q:seg.append((3,q+2,(0,0,0,n,d)))
            start=q+3
        seg.append((start,start,(0,0,1,n,d)));trigger=start
        if f['reason']==4:
            if f['change']>1:seg.append((start+1,start+f['change']-1,(0,0,0,n,d)))
            trigger=start+f['change'];seg.append((trigger,trigger,(0,0,0,n,f['changed'])))
        schedules.append(seg)
        elapsed=f['change']-1 if f['reason']==4 else 0
        invalidexpect.append(dict(invalid_id=f['id'],scenario=32+f['id'],expected_reason=f['reason'],N=n,D=d,quiet=q,change_edge=f['change'],changed_D=f['changed'],trigger_scenario_edge=trigger,actual_reason=f['reason'],valid=0,busy=0,done=0,timer=elapsed,pulses=elapsed//d,graph_audit_licensed=0))
    assert csvrows(folder/'JOBS.csv')==jobexpect
    assert csvrows(folder/'INVALID_CONTROLS.csv')==invalidexpect
    starts=[0]*44;inputs=[[0]*5 for _ in range(44)];rows=0;total=0
    sc=csvrows(folder/'SCENARIOS.csv');assert len(sc)==44
    for i,r in enumerate(sc):
        assert r['scenario']==i and all(r[k]==0 for k in r if k not in ['scenario','type','id'])
    with (folder/'TICKS_RLE.csv').open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sid=int(row['scenario']);first=int(row['first_edge']);count=int(row['count']);delta=[int(row[k]) for k in fields]
            assert count>0;pos=first;stop=first+count-1
            while pos<=stop:
                idx=starts[sid];a,b,expected=schedules[sid][idx]
                assert a<=pos<=b
                last=min(b,stop)
                for point in {pos,last}:
                    observed=tuple(inputs[sid][j]+delta[j]*(point-first+1) for j in range(5))
                    assert observed==expected,(sid,point,observed,expected)
                if last==b:starts[sid]+=1
                pos=last+1
            inputs[sid]=[inputs[sid][j]+count*delta[j] for j in range(5)];rows+=1;total+=count
    assert all(starts[i]==len(schedules[i]) for i in range(44))
    return dict(scenarios=44,jobs=192,invalid_attempts=12,input_rows=rows,input_edges=total,job_rows_all_fields_exact=True,invalid_rows_all_fields_exact=True,independent_schedule=True)

def main():
    global CURRENT_LOWER,CURRENT_UPPER
    p=load(BASE/'PROTOCOL.json');producer=BASE/'attempt-002';fresh=HERE/'fresh-replay'
    inv=load(BASE/'INVENTORY.json');bad=[]
    for item in inv['files']:
        f=BASE/item['path']
        if f.stat().st_size!=item['bytes'] or sha(f)!=item['sha256']:bad.append(item['path'])
    assert not bad,bad
    for folder in [producer,fresh]:
        run=load(folder/'PORTABLE_REPLAY.json')
        assert len(run['commands'])==7 and all(c['returncode']==0 for c in run['commands'])
        for name,digest in run['sources'].items():assert sha(BASE/name)==digest==sha(folder/name)
        for name,digest in run['outputs'].items():assert sha(folder/name)==digest
        im=load(folder/'vectors/INPUT_MANIFEST.json')
        assert im['protocol_sha256']==sha(BASE/'PROTOCOL.json') and im['source_sha256']==sha(BASE/'generate_inputs.py')
        for name,digest in im['files'].items():assert sha(folder/'vectors'/name)==digest
        actualinputs=load(folder/'vectors/INPUTS.json')
        assert actualinputs['valid']==[dict(**c,v=p['vectors_v'][c['vector_id']]) for c in expected_cases(p)]
    provenance=load(BASE/'CORE_PROVENANCE.json')
    assert sha(BASE/'audit_core.py')==provenance['source_sha256']==provenance['local_copy_sha256']=='9a4ad638a45cd69b43e7b2389417d6a43481225ee2c6e67fd9664b58d31f55a9'
    binding={}
    for name in ['netlist.cpp','TICKS_RLE.csv','SCENARIOS.csv','JOBS.csv','INVALID_CONTROLS.csv','RTL_RESULTS.json','AUDITOR_INPUTS.json','OBSERVATIONS.json','vectors/INPUTS.json','vectors/vectors.txt']:
        assert (producer/name).read_bytes()==(fresh/name).read_bytes(),name
        binding[name]=sha(producer/name)
    pa=(producer/'ALL_REPORTS.jsonl.gz').read_bytes();fa=(fresh/'ALL_REPORTS.jsonl.gz').read_bytes()
    assert gzip.decompress(pa)==gzip.decompress(fa)
    # Preserve and report container nonidentity, rather than ignoring the
    # actual hashes or claiming an identical archive. Bind each to its bytes.
    gzip_binding=dict(producer_sha256=sha(producer/'ALL_REPORTS.jsonl.gz'),fresh_sha256=sha(fresh/'ALL_REPORTS.jsonl.gz'),archive_bytes_equal=pa==fa,differing_byte_offsets=[i for i,(a,b) in enumerate(zip(pa,fa)) if a!=b],decompressed_bytes_equal=True,decompressed_sha256=hashlib.sha256(gzip.decompress(pa)).hexdigest())
    pr=load(producer/'AUDIT_RESULTS.json');fr=load(fresh/'AUDIT_RESULTS.json')
    for folder,result in [(producer,pr),(fresh,fr)]:
        for name,digest in result['bindings'].items():assert sha(folder/name)==digest
    assert {k:v for k,v in pr.items() if k!='bindings'}=={k:v for k,v in fr.items() if k!='bindings'}
    assert [k for k in pr['bindings'] if pr['bindings'][k]!=fr['bindings'][k]]==['ALL_REPORTS.jsonl.gz']
    # PE timestamps can vary without changing code. No other binary bytes may
    # be ignored in this comparison.
    pe=[]
    for folder in [producer,fresh]:
        b=bytearray((folder/'simulate.exe').read_bytes());off=struct.unpack_from('<I',b,0x3c)[0];assert b[off:off+4]==b'PE\0\0'
        original=bytes(b);timestamps=[off+8];sections=[]
        ns=struct.unpack_from('<H',b,off+6)[0];optional_size=struct.unpack_from('<H',b,off+20)[0];optional=off+24
        assert struct.unpack_from('<H',b,optional)[0]==0x20b
        table=optional+optional_size
        for i in range(ns):
            s=table+40*i;name=bytes(b[s:s+8]).rstrip(b'\0').decode('ascii');vs,rva,sz,raw=struct.unpack_from('<IIII',b,s+8)
            sections.append((name,rva,raw,sz))
        def fileoffset(rva):
            return next(raw+rva-start for _,start,raw,size in sections if start<=rva<start+size)
        debugrva,debugsize=struct.unpack_from('<II',b,optional+112+6*8);debug=fileoffset(debugrva);guids=[]
        for entry in range(debug,debug+debugsize,28):
            timestamps.append(entry+4);kind=struct.unpack_from('<I',b,entry+12)[0];ptr=struct.unpack_from('<I',b,entry+24)[0]
            if kind==2:
                assert b[ptr:ptr+4]==b'RSDS';guids.append((ptr+4,bytes(b[ptr+4:ptr+20]).hex()))
        for pos in timestamps:b[pos:pos+4]=b'\0'*4
        pe.append(dict(timestamp_offsets=timestamps,timestamp_values=[struct.unpack_from('<I',original,x)[0] for x in timestamps],guid_fields=guids,original=original,normalized=bytes(b),text_sha256=hashlib.sha256(next(original[raw:raw+size] for name,_,raw,size in sections if name=='.text')).hexdigest()))
    exe_equal=pe[0]['normalized']==pe[1]['normalized']
    differences=[i for i,(a,b) in enumerate(zip(pe[0]['original'],pe[1]['original'])) if a!=b]
    allowed_metadata=set()
    for x in pe:
        for start in x['timestamp_offsets']:allowed_metadata.update(range(start,start+4))
        for start,_ in x['guid_fields']:allowed_metadata.update(range(start,start+16))
    assert set(differences)<=allowed_metadata and len(pe[0]['original'])==len(pe[1]['original'])
    assert pe[0]['text_sha256']==pe[1]['text_sha256']
    binary_binding=dict(byte_equal=pe[0]['original']==pe[1]['original'],equal_after_PE_timestamps_only=exe_equal,differing_byte_offsets=differences,text_section_sha256=pe[0]['text_sha256'],classification='PE COFF/debug timestamps and CodeView RSDS build GUID; GUID difference is retained, not ignored',producer={k:v for k,v in pe[0].items() if k not in ['original','normalized']},fresh={k:v for k,v in pe[1].items() if k not in ['original','normalized']})
    schedule=check_schedule(producer,p)
    iface=load(producer/'AUDITOR_INPUTS.json');assert set(iface)=={'kind','valid_reports','invalid_controls','privacy'}
    assert len(iface['valid_reports'])==32 and len(iface['invalid_controls'])==12
    jobs=csvrows(producer/'JOBS.csv')
    for cid,r in enumerate(iface['valid_reports']):
        assert set(r)=={'case_id','jobs'} and r['case_id']==cid and len(r['jobs'])==6
        for j,job in enumerate(r['jobs']):
            assert set(job)=={'slot','slot_name','valid','reason','timer_lower','timer_upper','source_obligations'}
            assert job['slot']==j and job['slot_name']==p['slot_names'][j] and job['valid'] is True and job['reason']=='licensed'
            assert job['timer_lower']==jobs[6*cid+j]['lower'] and job['timer_upper']==jobs[6*cid+j]['upper']
            assert job['source_obligations']==dict(command_reset=True,settled=True,held_divider=True,fixed_cycle_countdown=True,timer_counts_reference_edges=True,adjacent_ratio_guard=True)
    for actual,f in zip(iface['invalid_controls'],invalid_cases(p)):
        assert actual==dict(invalid_id=f['id'],valid=False,status='contract-unknown',reason_code=f['reason'],timer_enclosure=None,graph_audit_licensed=False)
    observations=load(producer/'OBSERVATIONS.json');res=load(producer/'AUDIT_RESULTS.json');d=res['numerics']['delta_scaled'];validate_enclosure(Q(201,200),d);own_d=logints(Q(201,200))
    counters={k:Counter() for k in ['total','partial','tie_total','other_total','tie_partial','other_partial']};pv={str(i):Counter() for i in range(8)};ppv={str(i):Counter() for i in range(8)};percase=[];changed=[]
    count=0;certs=Counter()
    with gzip.open(producer/'ALL_REPORTS.jsonl.gz','rt',encoding='utf-8') as f:
        for case,obs,public in zip(expected_cases(p),observations,iface['valid_reports']):
            cid=case['case_id'];assert obs['case_id']==cid and obs['vector_id']==case['vector_id'] and obs['path_name']==case['path_name']
            CURRENT_LOWER=[x['timer_lower'] for x in public['jobs']];CURRENT_UPPER=[x['timer_upper'] for x in public['jobs']]
            assert obs['timer_lower']==CURRENT_LOWER and obs['timer_upper']==CURRENT_UPPER
            recorded=obs['log_scaled_bounds'];own={'l':[],'u':[]}
            for side,times in [('l',CURRENT_LOWER),('u',CURRENT_UPPER)]:
                for i,t in enumerate(times):validate_enclosure(Q(t,1000),recorded[side][i]);own[side].append(logints(Q(t,1000)))
            local=Counter();partial=Counter()
            for order in list(permutations(range(6)))+[None]:
                row=json.loads(next(f));assert row['case_id']==cid and row['vector_id']==case['vector_id'] and row['path_name']==case['path_name']
                if order is None:
                    claims=[tuple(x) for x in p['audits']['fixed_partial_claims']];assert row['kind']=='fixed_partial' and row['claims']==p['audits']['fixed_partial_claims'];kind='partial'
                else:
                    assert row['kind']=='total_order' and row['order']==list(order)
                    claims=[(order[a],order[b]) for a in range(6) for b in range(a+1,6)];kind='total'
                truth=all(case['N'][a]<=case['N'][b] for a,b in claims);assert row['true']==truth
                independent=verdict(own,own_d,claims);assert row['path']==independent,(cid,order,row['path'],independent)
                rb,lo,hi=box(recorded,d,claims);assert row['box']==rb and Q(row['beta_lower'])==lo and Q(row['beta_upper'])==hi
                ob,_,_=box(own,own_d,claims);assert rb==ob
                certificate(row,recorded,d,claims);assert not truth or independent=='admit'
                add(local if kind=='total' else partial,truth,row);add(counters[kind],truth,row)
                add(counters[('tie_' if case['vector_id']==1 else 'other_')+kind],truth,row)
                add((pv if kind=='total' else ppv)[str(case['vector_id'])],truth,row)
                if kind=='partial' and row['box']=='admit' and row['path']=='reject':changed.append(cid)
                count+=1;certs[row['path']]+=1
            assert countdict(local)==obs['total_order_summary']
            assert row==obs['fixed_partial']
            percase.append(dict(case_id=cid,vector_id=case['vector_id'],path_name=case['path_name'],total=countdict(local),partial=countdict(partial)))
        assert f.read()==''
    assert count==23072
    assert countdict(counters['total'])==res['total_orders'] and countdict(counters['partial'])==res['fixed_partial']
    assert {k:countdict(v) for k,v in pv.items()}==res['per_vector_total_orders']
    assert {k:countdict(v) for k,v in ppv.items()}==res['per_vector_fixed_partial']
    assert countdict(counters['tie_total'])==res['total_orders_by_group']['all_tie']
    assert countdict(counters['other_total'])==res['total_orders_by_group']['distinct_vectors']
    assert countdict(counters['tie_partial'])==res['fixed_partial_by_group']['all_tie']
    assert countdict(counters['other_partial'])==res['fixed_partial_by_group']['distinct_vectors']
    output=dict(status='PASS',producer_inventory_files=len(inv['files']),bindings=binding,gzip_binding=gzip_binding,binary_binding=binary_binding,fresh_replay_semantic_outputs_exact=True,framing=schedule,queries=count,certificates=dict(certs),totals={k:countdict(v) for k,v in counters.items()},per_case=percase,per_vector_total={k:countdict(v) for k,v in pv.items()},per_vector_partial={k:countdict(v) for k,v in ppv.items()},changed_partial_case_ids=changed,independence=dict(graph='13 original variables, separate edge-list synchronous Bellman-Ford',logs='exact Fraction 170-term atanh sum, exact geometric tail, 10^70 graph bounds',producer_modules_imported=False),privacy='Strict interface key whitelist and job binding checked; abstraction privacy only, not inference resistance')
    write(HERE/'GRAPH_AND_FRAMING_CHECK.json',output);print('PASS independent original-variable graph, logs, certificates, framing:',count,flush=True)
if __name__=='__main__':main()
