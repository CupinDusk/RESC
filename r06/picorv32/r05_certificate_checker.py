"""Audit actual generated-RTL timer observations, without N/D in auditor input."""
from pathlib import Path
from fractions import Fraction
from itertools import permutations
from collections import Counter
import csv,gzip,hashlib,json
import audit_core as core
import exact_logs
HERE=Path(__file__).resolve().parent
KEYS=['reports','true','false','admit','reject','unknown','true_admit','true_reject','true_unknown','false_admit','false_reject','false_unknown','box_admit','box_reject','box_unknown','box_admit_path_reject']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def counts(c):return {k:c[k] for k in KEYS}
def add(c,truth,r):
    c['reports']+=1;c['true' if truth else 'false']+=1;c[r['path']]+=1
    c[('true_' if truth else 'false_')+r['path']]+=1;c['box_'+r['box']]+=1
    c['box_admit_path_reject']+=r['box']=='admit' and r['path']=='reject'
def check_certificate(b,delta,claims,r):
    cert=r['certificate']
    if r['path']=='admit':
        t=cert['theta_scaled'];bias=cert['bias_scaled'];assert len(t)==6 and len(bias)==7 and bias[0]==0
        assert all(abs(bias[j]-bias[j-1])<=delta[0] for j in range(1,7))
        assert all(b['l'][i][1]<=t[i]+bias[i+1]<=b['u'][i][0] for i in range(6))
        assert all(t[p]<=t[q] for p,q in claims)
    elif r['path']=='reject':
        edges=cert['cycle'];assert edges and all(edges[j][1]==edges[(j+1)%len(edges)][0] for j in range(len(edges)))
        weights=[]
        for a,z in edges:
            w=b['u'][z][1]-b['l'][a][0]+delta[1]*abs(a-z)
            if (z,a) in claims:w=min(w,0)
            weights.append(w)
        assert weights==cert['weights'] and sum(weights)==cert['total']<0
    else:
        tight,_,_=core.matrix(b,delta[0],claims,True);relaxed,_,_=core.matrix(b,delta[1],claims,False)
        assert not core.floyd(tight) and core.floyd(relaxed)
def main():
    proto=json.loads((HERE/'PROTOCOL.json').read_text(encoding='utf-8'))
    inputs=json.loads((HERE/'vectors/INPUTS.json').read_text(encoding='utf-8'))
    rows=list(csv.DictReader((HERE/'JOBS.csv').open(encoding='utf-8')))
    invalid=list(csv.DictReader((HERE/'INVALID_CONTROLS.csv').open(encoding='utf-8')))
    assert len(rows)==192 and len(invalid)==12
    valid=[]
    for case in inputs['valid']:
        jobs=[]
        for j in range(6):
            r=rows[6*case['case_id']+j];assert int(r['case_id'])==case['case_id'] and int(r['slot'])==j
            assert int(r['valid'])==1 and int(r['reason'])==0 and int(r['upper'])-int(r['lower'])==2
            jobs.append(dict(slot=j,slot_name=proto['slot_names'][j],valid=True,reason='licensed',timer_lower=int(r['lower']),timer_upper=int(r['upper']),source_obligations=dict(command_reset=True,settled=True,held_divider=True,fixed_cycle_countdown=True,timer_counts_reference_edges=True,adjacent_ratio_guard=True)))
        valid.append(dict(case_id=case['case_id'],jobs=jobs))
    invalid_interface=[dict(invalid_id=int(r['invalid_id']),valid=False,status='contract-unknown',reason_code=int(r['actual_reason']),timer_enclosure=None,graph_audit_licensed=False) for r in invalid]
    assert all(int(r['actual_reason'])==int(r['expected_reason']) and r['graph_audit_licensed']=='0' for r in invalid)
    interface=dict(kind='auditor abstraction interface; private N,D excluded',valid_reports=valid,invalid_controls=invalid_interface,privacy='Interface abstraction only; no cryptographic or inference-resistance assurance')
    write(HERE/'AUDITOR_INPUTS.json',interface)
    # From this point all graph inputs come only from the abstraction interface.
    iface=json.loads((HERE/'AUDITOR_INPUTS.json').read_text(encoding='utf-8'))
    delta=exact_logs.bounds(Fraction(201,200));assert core.SCALE==exact_logs.SCALE
    total=Counter();partial=Counter();groups={k:Counter() for k in ['all_tie','distinct_vectors']};pgroups={k:Counter() for k in groups}
    pervector={str(i):Counter() for i in range(8)};ppv={str(i):Counter() for i in range(8)}
    observations=[];query_count=0;certs=Counter();examples=[]
    with gzip.open(HERE/'ALL_REPORTS.jsonl.gz','wt',encoding='utf-8',newline='\n') as out:
        for public,debug in zip(iface['valid_reports'],inputs['valid']):
            assert public['case_id']==debug['case_id']
            lower=[Fraction(j['timer_lower'],1000) for j in public['jobs']];upper=[Fraction(j['timer_upper'],1000) for j in public['jobs']]
            b=dict(l=[exact_logs.bounds(x) for x in lower],u=[exact_logs.bounds(x) for x in upper])
            stats=Counter();ps=Counter();group='all_tie' if len(set(debug['N']))==1 else 'distinct_vectors'
            for order in permutations(range(6)):
                claims=[(order[i],order[j]) for i in range(6) for j in range(i+1,6)]
                r=core.audit(b,delta,claims);check_certificate(b,delta,claims,r)
                truth=all(debug['N'][a]<=debug['N'][z] for a,z in claims)
                assert not truth or r['path']=='admit'
                row=dict(case_id=debug['case_id'],vector_id=debug['vector_id'],path_name=debug['path_name'],kind='total_order',order=order,true=truth,**r)
                out.write(json.dumps(row,separators=(',',':'))+'\n');add(stats,truth,r);query_count+=1;certs[r['path']]+=1
                if r['box']=='admit' and r['path']=='reject' and not any(e['case_id']==debug['case_id'] for e in examples):examples.append(row)
            claims=[tuple(x) for x in proto['audits']['fixed_partial_claims']]
            r=core.audit(b,delta,claims);check_certificate(b,delta,claims,r);truth=all(debug['N'][a]<=debug['N'][z] for a,z in claims)
            assert not truth or r['path']=='admit'
            row=dict(case_id=debug['case_id'],vector_id=debug['vector_id'],path_name=debug['path_name'],kind='fixed_partial',claims=claims,true=truth,**r)
            out.write(json.dumps(row,separators=(',',':'))+'\n');add(ps,truth,r);query_count+=1;certs[r['path']]+=1
            observations.append(dict(case_id=debug['case_id'],vector_id=debug['vector_id'],path_name=debug['path_name'],group=group,timer_lower=[j['timer_lower'] for j in public['jobs']],timer_upper=[j['timer_upper'] for j in public['jobs']],log_scaled_bounds=b,total_order_summary=counts(stats),fixed_partial=row))
            total.update(stats);partial.update(ps);groups[group].update(stats);pgroups[group].update(ps);pervector[str(debug['vector_id'])].update(stats);ppv[str(debug['vector_id'])].update(ps)
    assert query_count==23072 and total['reports']==23040 and partial['reports']==32
    write(HERE/'OBSERVATIONS.json',observations)
    result=dict(status='PASS_AUTHOR_RTL_TIMER_GRAPH_AUDIT_PENDING_INDEPENDENT_GATE',valid_reports=32,jobs=192,queries=query_count,total_orders=counts(total),fixed_partial=counts(partial),total_orders_by_group={k:counts(v) for k,v in groups.items()},fixed_partial_by_group={k:counts(v) for k,v in pgroups.items()},per_vector_total_orders={k:counts(v) for k,v in pervector.items()},per_vector_fixed_partial={k:counts(v) for k,v in ppv.items()},certificates=dict(certs),invalid_controls_contract_unknown=len(invalid),numerics=dict(delta_scaled=delta,**exact_logs.proof_metadata()),changed_verdict_examples=examples,bindings={n:sha(HERE/n) for n in ['PROTOCOL.json','reference.v','driver.cpp','audit_core.py','CORE_PROVENANCE.json','exact_logs.py','audit_reports.py','JOBS.csv','INVALID_CONTROLS.csv','AUDITOR_INPUTS.json','OBSERVATIONS.json','ALL_REPORTS.jsonl.gz']},limitations=proto['scope'])
    write(HERE/'AUDIT_RESULTS.json',result)
    print(json.dumps({k:result[k] for k in ['status','queries','total_orders','fixed_partial','certificates']},indent=2))
if __name__=='__main__':main()
