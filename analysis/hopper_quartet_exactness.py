from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quartet_factor(pos,R):
 n=len(pos);R=set(map(tuple,R));best=F(1);witness=None;tests=0
 for endpoints in combinations(range(n),4):
  for P in combinations(endpoints,2):
   Q=tuple(x for x in endpoints if x not in P);costs=[]
   for order in [Q,Q[::-1]]:
    cost=sum(abs(pos[p]-pos[q]) for p,q in zip(P,order));allowed=all((p,q) in R for p,q in zip(P,order));costs.append((cost,allowed,order))
   tests+=1;allowed=[x for x in costs if x[1]]
   if not allowed:continue
   restricted=min(x[0] for x in allowed);free=min(x[0] for x in costs);ratio=F(restricted,free)
   if ratio>best:best=ratio;witness={'P':P,'Q':Q,'restricted_cost':restricted,'free_cost':free,'ratio':str(ratio)}
 return best,witness,tests
def main():
 out=HERE/'HOPPER_R14_QUARTET_RESULTS.json';assert not out.exists()
 source=HERE/'HOPPER_R13_MATCHING_RESULTS.json';prior=json.loads(source.read_text());records=[];counts=Counter();six=Counter();tests=0;full_greater=[]
 for i,r in enumerate(prior['records']):
  C=F(r['factor']);q,w,t=quartet_factor(r['positions'],r['R']);tests+=t
  assert (C==1)==(q==1),(i,r,C,q)
  assert q<=C
  counts['zero_loss' if q==1 else 'nonunit']+=1
  if r['kind']=='complete6':six['zero_loss' if q==1 else 'nonunit']+=1
  if q<C:full_greater.append({'case':i,'full_factor':str(C),'max_quartet_factor':str(q)})
  records.append({'case':i,'kind':r['kind'],'full_factor':str(C),'max_quartet_factor':str(q),'witness':w,'quartets_tested':t})
 result={'result':'PASS_QUARTET_ZERO_LOSS_CRITERION_ON_ALL_EXISTING_CONTROLLED_CASES','protocol_sha256':sha(HERE/'HOPPER_R14_QUARTET_PROTOCOL.json'),'argument_sha256':sha(HERE/'HOPPER_R14_QUARTET_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),'matching_results_sha256':sha(source),'instances':len(records),'quartet_tests':tests,'classifications':dict(counts),'six_arm_complete_order_classifications':dict(six),'full_factor_larger_than_quartet_max_count':len(full_greater),'all_full_factor_larger_cases':full_greater,'records':records,'scope':'Exact finite corroboration of the manual universal proof; only C_R=1 is claimed polynomially decidable. No new generic matching algorithm, hardware validity, deployed workflow or cost saving.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['records','all_full_factor_larger_cases']},indent=2))
if __name__=='__main__':main()
