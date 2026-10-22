"""Constructive settled-clock model; exact controller/times and outward log audit."""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction
from itertools import permutations
import collections,gzip,hashlib,json
HERE=Path(__file__).resolve().parent
SCALE=10**60
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def log_bounds(v):
    assert 0<v.numerator<10**12 and 0<v.denominator<10**12
    with localcontext() as c:
        c.prec=100
        a=Decimal(v.numerator).ln()-Decimal(v.denominator).ln()
        e=Decimal('1e-90')
        lo=int(((a-e)*SCALE).to_integral_value(rounding=ROUND_FLOOR))
        hi=int(((a+e)*SCALE).to_integral_value(rounding=ROUND_CEILING))
    assert lo<=hi
    return lo,hi
def ratio_string(v):return f'{v.numerator}/{v.denominator}'
def bf(mat):
    n=len(mat);d=[0]*n;pre=[None]*n;last=None
    for turn in range(n):
        last=None
        for a in range(n):
            for b in range(n):
                if a==b:continue
                if d[b]>d[a]+mat[a][b]:
                    d[b]=d[a]+mat[a][b];pre[b]=a;last=b
        if last is None:
            assert all(d[b]-d[a]<=mat[a][b] for a in range(n) for b in range(n))
            return True,dict(potential=d)
    v=last
    for _ in range(n):v=pre[v];assert v is not None
    nodes=[v];cur=pre[v]
    while cur!=v:
        assert cur is not None and cur not in nodes
        nodes.append(cur);cur=pre[cur]
    nodes.reverse();edges=[(nodes[i],nodes[(i+1)%len(nodes)]) for i in range(len(nodes))]
    weights=[mat[a][b] for a,b in edges];assert sum(weights)<0
    return False,dict(cycle=edges,weights=weights,total=sum(weights))
def floyd(mat):
    m=[row[:] for row in mat];n=len(m)
    for k in range(n):
        for a in range(n):
            for b in range(n):m[a][b]=min(m[a][b],m[a][k]+m[k][b])
    return all(m[i][i]>=0 for i in range(n))
def matrix(bounds,delta,R,tight):
    l=[v[1 if tight else 0] for v in bounds['l']]
    u=[v[0 if tight else 1] for v in bounds['u']]
    mat=[[0 if a==b else u[b]-l[a]+delta*abs(a-b) for b in range(6)] for a in range(6)]
    for p,q in R:mat[q][p]=min(0,mat[q][p])
    return mat,l,u
def audit(bounds,delta,R):
    tight,l,u=matrix(bounds,delta[0],R,True)
    relaxed,_,_=matrix(bounds,delta[1],R,False)
    t,tc=bf(tight);r,rc=bf(relaxed)
    assert t==floyd(tight) and r==floyd(relaxed)
    assert not t or r
    beta_lower=max([Fraction(0)]+[Fraction(bounds['l'][p][0]-bounds['u'][q][1],abs(p-q)) for p,q in R])
    beta_upper=max([Fraction(0)]+[Fraction(bounds['l'][p][1]-bounds['u'][q][0],abs(p-q)) for p,q in R])
    box='admit' if beta_upper<=delta[0] else 'reject' if beta_lower>delta[1] else 'unknown'
    if t:
        theta=tc['potential']
        bias=[max(l[i]-theta[i]-delta[0]*abs(j-(i+1)) for i in range(6)) for j in range(7)]
        anchor=bias[0];bias=[b-anchor for b in bias];theta=[v+anchor for v in theta]
        assert bias[0]==0 and all(abs(bias[j]-bias[j-1])<=delta[0] for j in range(1,7))
        assert all(l[i]<=theta[i]+bias[i+1]<=u[i] for i in range(6))
        assert all(theta[p]<=theta[q] for p,q in R)
        cert=dict(theta_scaled=theta,bias_scaled=bias);status='admit'
    elif not r:cert=rc;status='reject'
    else:cert=dict(tight_rejection=tc,relaxed_potential=rc);status='unknown'
    assert not(status=='admit' and box=='reject')
    return dict(path=status,box=box,beta_lower=ratio_string(beta_lower),beta_upper=ratio_string(beta_upper),certificate=cert)
def main():
    proto=json.loads((HERE/'PROTOCOL.json').read_text(encoding='utf-8'))
    for name in ['RESULTS.json','OBSERVATIONS.json','ALL_REPORTS.jsonl.gz']:
        assert not(HERE/name).exists(),name
    ref=proto['clock_contract']['reference_multiplier'];guard=Fraction(proto['clock_contract']['per_boundary_max_ratio'].split(' ')[0])
    # Fraction does not accept descriptive strings; the declared literal is 1005/1000.
    assert guard==Fraction(1005,1000)
    delta=log_bounds(guard);obs=[];cases=[];agg=collections.Counter();checks=0
    for ci,counts in enumerate(proto['cycle_count_vectors_in_slot_order']):
        durations=[]
        for path in proto['three_replay_multiplier_sequences']:
            prev=ref
            for m in path:
                assert Fraction(m,prev)<=guard and Fraction(prev,m)<=guard;prev=m;checks+=1
            vals=[Fraction(n*ref,m) for n,m in zip(counts,path)]
            # Independent rational cycle-accumulator checks: quotient/remainder
            # of N reference-clock microcycles under the held multiplier.
            for n,m,v in zip(counts,path,vals):
                q,rem=divmod(n*ref,m);assert Fraction(q)+Fraction(rem,m)==v
            durations.append(vals)
        low=[min(row[i] for row in durations) for i in range(6)]
        high=[max(row[i] for row in durations) for i in range(6)]
        assert all(lo<hi for lo,hi in zip(low,high))
        assert all(low[i]<=Fraction(counts[i])<=high[i] for i in range(6))
        bounds=dict(l=[log_bounds(v) for v in low],u=[log_bounds(v) for v in high])
        ob=dict(case_id=ci,cycles=counts,multipliers=proto['three_replay_multiplier_sequences'],
          normalized_durations=[[ratio_string(v) for v in row] for row in durations],
          lower=[ratio_string(v) for v in low],upper=[ratio_string(v) for v in high],log_scaled_bounds=bounds)
        obs.append(ob);c=collections.Counter();partial=None
        for ri,order in enumerate(permutations(range(6))):
            R=[(order[i],order[j]) for i in range(6) for j in range(i+1,6)]
            res=audit(bounds,delta,R);truth=all(counts[p]<=counts[q] for p,q in R)
            assert not truth or res['path']=='admit',(ci,order,res)
            c['orders']+=1;c[res['path']]+=1;c['true_reports']+=int(truth)
            c['incorrect_but_admitted']+=int(not truth and res['path']=='admit')
            c['boxes_admit_path_reject']+=int(res['box']=='admit' and res['path']=='reject')
            cases.append(dict(case_id=ci,kind='total_order',order=list(order),true=truth,**res))
        R=[(0,5),(4,1)];res=audit(bounds,delta,R);truth=all(counts[p]<=counts[q] for p,q in R)
        assert not truth or res['path']=='admit'
        partial=dict(case_id=ci,kind='fixed_partial',claims=R,true=truth,**res)
        cases.append(partial);agg.update(c)
        ob['total_order_summary']=dict(c);ob['fixed_partial']=partial
    with gzip.open(HERE/'ALL_REPORTS.jsonl.gz','wt',encoding='utf-8',newline='\n') as f:
        for row in cases:f.write(json.dumps(row,separators=(',',':'))+'\n')
    out=dict(status='PASS_EXPLICIT_SETTLED_CLOCK_CONTRACT_AND_OUTWARD_CERTIFICATES',
      scope=proto['scope'],scale=str(SCALE),delta_scaled_enclosure=delta,
      controller_boundary_checks=checks,job_vectors=len(obs),replays=len(obs)*3,
      total_order_summary=dict(agg),fixed_partial=[ob['fixed_partial'] for ob in obs],
      graph_bf_and_independent_floyd_checks=len(cases)*2,
      original_variable_admission_certificates=sum(r['path']=='admit' for r in cases),
      negative_cycle_certificates=sum(r['path']=='reject' for r in cases),unknown=sum(r['path']=='unknown' for r in cases),
      provenance={n:sha(HERE/n) for n in ['PROTOCOL.json','NUMERIC_PROTOCOL_ADDENDUM.json','check_clock_contract.py','ALL_REPORTS.jsonl.gz']})
    (HERE/'OBSERVATIONS.json').write_text(json.dumps(obs,indent=2)+'\n',encoding='utf-8')
    (HERE/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['fixed_partial','provenance']},indent=2))
if __name__=='__main__':main()
