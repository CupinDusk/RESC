"""Prospective paired exact constructions: a scalar archive cannot decide."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib,json
from hopper_explanation_radius import min_lp

HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stringify(values):return {str(k):str(v) for k,v in values.items()}

def main():
 out=HERE/'HOPPER_R12_ARCHIVE_RESULTS.json';assert not out.exists()
 records=[];lp_count=0;max_error=0.;max_violation=0.
 for N in [4,5,6,8,16,32,64]:
  for eps in [F(0),F(1,1000),F(1,250)]:
   t=F(1,100);v=t-2*eps;beta=v/(N-2);mid=(beta+v)/2
   order=[1,N-1]+list(range(N-2,2,-1))+[N,2]
   assert sorted(order)==list(range(1,N+1))
   pairs=list(combinations(order,2));chain=list(zip(order,order[1:]))
   upper={1:t,2:v-beta,N-1:F(0),N:t+v-beta}
   upper.update({j:v-beta*(j-1) for j in range(3,N-1)})
   lower={j:-beta*j for j in range(1,N+1)}
   lower[1]+=eps;lower[N-1]-=eps
   families=[]
   for name,c,radius in [('lower',lower,beta),('upper',upper,v)]:
    l={j:c[j]-eps for j in c};u={j:c[j]+eps for j in c}
    assert all(u[j]-l[j]==2*eps for j in c)
    actual_beta=max([F(0)]+[(l[p]-u[q])/abs(p-q) for p,q in pairs])
    assert actual_beta==beta
    if name=='lower':
     bias={j:-beta*j for j in range(N+1)}
     x={j:bias[j] for j in c}
    else:
     bias={j:(-v if 2<=j<=N-1 else F(0)) for j in range(N+1)}
     x={j:l[j] if j in [1,N] else u[j] for j in c}
    theta={j:x[j]-bias[j] for j in c}
    assert bias[0]==0 and max(abs(bias[j]-bias[j-1]) for j in range(1,N+1))==radius
    assert all(l[j]<=x[j]<=u[j] for j in c)
    assert all(theta[p]<=theta[q] for p,q in pairs)
    if name=='lower':
     assert l[1]-u[N-1]==beta*(N-2)
     assert max(abs(bias[j]-bias[j-1]) for j in range(1,N+1))<mid
     midpoint={'admitted':True,'exact_witness_budget':str(beta)}
    else:
     deficit=l[1]-u[N-1]+l[N]-u[2]
     assert deficit==2*v and 2*mid-deficit<0
     midpoint={'admitted':False,'cycle':[N-1,1,2,N,N-1],
               'exact_cycle_weight':str(2*mid-deficit)}
    val,witness=min_lp({j:float(l[j]) for j in c},{j:float(u[j]) for j in c},
                       {j:j for j in c},chain)
    lp_count+=1;error=abs(val-float(radius));max_error=max(max_error,error)
    max_violation=max(max_violation,witness['maximum_ranking_violation'])
    assert error<=1e-8 and witness['maximum_ranking_violation']<=1e-8
    families.append({'name':name,'centers':stringify(c),'lower':stringify(l),'upper':stringify(u),
      'beta_R':str(actual_beta),'exact_shared_minimum':str(radius),'x':stringify(x),
      'bias':stringify(bias),'theta':stringify(theta),'midpoint_check':midpoint,
      'original_variable_LP_minimum':val,'LP_maximum_ranking_violation':witness['maximum_ranking_violation']})
   archives=[{'N':N,'R_complete_order':order,'beta_R':f['beta_R'],'common_half_width':str(eps)} for f in families]
   assert archives[0]==archives[1]
   records.append({'archive':archives[0],'midpoint_budget':str(mid),'instances':families})
  print(json.dumps({'stage':'scalar_archive_pairs','N':N,'pairs':len(records),'original_path_LPs':lp_count}),flush=True)
 result={'result':'PASS_IDENTICAL_SCALAR_ARCHIVES_ATTAIN_BOTH_SHARP_RADIUS_ENDPOINTS',
  'protocol_sha256':sha(HERE/'HOPPER_R12_ARCHIVE_PROTOCOL.json'),
  'argument_sha256':sha(HERE/'HOPPER_R12_ARCHIVE_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),
  'LP_helper_sha256':sha(HERE/'hopper_explanation_radius.py'),
  'paired_instances':len(records),'original_variable_minimum_LPs':lp_count,
  'positive_width_pairs':sum(F(r['archive']['common_half_width'])>0 for r in records),
  'maximum_LP_radius_error':max_error,'maximum_LP_ranking_violation':max_violation,
  'records':records,
  'scope':'Exact rational witnesses/cycles establish the paired constructions; LP tolerances are numerical corroboration. This only concerns archive (N,R,beta_R,common half-width), not arbitrary box outputs or all anchor functions. Original rectangle/slots/model suffice to reconstruct exact graph. No new hardware, external data, physical model validation, real archive adoption or storage/runtime gain.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)

if __name__=='__main__':main()
