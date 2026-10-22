"""Quartet-only offline flags and standard per-rectangle fallback, no full factor."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter,defaultdict
from decimal import Decimal
import csv,hashlib,json
import hopper_exact_certificates as ec
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def classify(pos,R):
 allowed=set(R);tests=0
 for four in combinations(range(len(pos)),4):
  for P in combinations(four,2):
   Q=tuple(x for x in four if x not in P);two=[]
   for match in [Q,Q[::-1]]:
    cost=sum(abs(pos[p]-pos[q]) for p,q in zip(P,match))
    two.append((cost,all((p,q) in allowed for p,q in zip(P,match))))
   tests+=1;restricted=[v for v,ok in two if ok]
   if not restricted:continue
   if min(restricted)>min(v for v,_ in two):
    return False,{'P':P,'Q':Q,'allowed_cost':min(restricted),'free_cost':min(v for v,_ in two)},tests
 return True,None,tests
def main():
 out=HERE/'HOPPER_R16_QUARTET_AUDITOR_RESULTS.json';routes=HERE/'HOPPER_R16_ALL_QUARTET_ROUTES.csv'
 assert not out.exists() and not routes.exists()
 orders=list(permutations(sorted(range(6),key=lambda a:ec.ARMS[a])))
 plans=[]
 for order in orders:
  R=list(combinations(order,2));flag,witness,tests=classify(ec.POS,R)
  plans.append((order,R,flag,witness,tests))
 assert sum(flag for _,_,flag,_,_ in plans)==40
 # Plans above use neither endpoints nor any full-factor value.
 previous=HERE/'HOPPER_R14_AUDITOR_RESULTS.json';old=json.loads(previous.read_text())
 old_csv=HERE/'HOPPER_R14_ALL_AUDITOR_ROUTES.csv';assert sha(old_csv)==old['full_route_csv_sha256']
 with old_csv.open(encoding='utf-8',newline='') as f:oracle={(int(r['case']),r['fraction']):r['exact_decision'] for r in csv.DictReader(f)}
 assert len(oracle)==384480 and set(oracle.values())=={'admit','reject'}
 raw=defaultdict(dict)
 with ec.MATRIX.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):raw[(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))][r['arm']]=(Decimal(r['min_ns']),Decimal(r['max_ns']))
 budgets={f:ec.log_bounds(str(Decimal(1)+Decimal(f))) for f in ec.GRID}
 stats={f:Counter() for f in ec.GRID};unknown=total=0
 with routes.open('w',encoding='utf-8',newline='') as stream:
  writer=csv.writer(stream);writer.writerow(['case','fraction','quartet_exact','route','decision'])
  for ci,(key,low,high) in enumerate(ec.load_cells()):
   for oi,(order,R,exact,_,_) in enumerate(plans):
    blo,bhi=ec.beta_bounds(low,high,R)
    zero=all(raw[key][ec.ARMS[p]][0]<=raw[key][ec.ARMS[q]][1] for p,q in R)
    if zero:
     greatest=Decimal(0);fit={}
     for a in order:
      greatest=max(greatest,raw[key][ec.ARMS[a]][0]);fit[a]=greatest
      assert raw[key][ec.ARMS[a]][0]<=fit[a]<=raw[key][ec.ARMS[a]][1]
     assert all(fit[p]<=fit[q] for p,q in R);blo=bhi=0
    for fraction,(dlo,dhi) in budgets.items():
     if dhi<blo:route,decision='marginal_reject','reject'
     elif exact and dlo>=bhi:route,decision='exact_marginal_admit','admit'
     else:
      route='graph_fallback'
      if zero:decision='admit'
      elif 'potential' in ec.exact_feasibility(ec.graph(low,high,R,dlo,False)):decision='admit'
      elif 'cycle' in ec.exact_feasibility(ec.graph(low,high,R,dhi,True)):decision='reject'
      else:decision='unknown';unknown+=1
     case=ci*720+oi;assert decision==oracle[(case,fraction)],(case,fraction,route,decision)
     stats[fraction][route]+=1;stats[fraction]['output_'+decision]+=1
     writer.writerow([case,fraction,int(exact),route,decision]);total+=1
 assert total==384480 and not unknown
 matching=json.loads((HERE/'HOPPER_R13_MATCHING_RESULTS.json').read_text())['records'][397]
 quartet=json.loads((HERE/'HOPPER_R14_QUARTET_RESULTS.json').read_text())['records'][397]
 assert matching['order']==[0,2,4,1,3,5] and matching['factor']=='7/3' and quartet['max_quartet_factor']=='5/3'
 result={'result':'PASS_QUARTET_ONLY_PLANS_AND_ALL_CERTIFIED_DECISIONS','protocol_sha256':sha(HERE/'HOPPER_R16_QUARTET_AUDITOR_PROTOCOL.json'),'script_sha256':sha(Path(__file__)),'matrix_sha256':sha(ec.MATRIX),'previous_auditor_result_sha256':sha(previous),'previous_certified_route_csv_sha256':sha(old_csv),'plans':720,'exact_plans':40,'nonexact_plans':680,'planning_quartets_visited':sum(t for _,_,_,_,t in plans),'full_factors_used_by_quartet_route':False,'fixed_budget_outputs':total,'unresolved_decisions_retained':unknown,'budgets':{f:dict(c) for f,c in stats.items()},'all_routes_sha256':sha(routes),'existing_case397':{'order_slots':[1,3,5,2,4,6],'full_factor':'7/3','max_quartet':'5/3','full_restricted_cost':7,'full_free_cost':3},'scope':'Conditional prototype, no full-factor preprocessing required. All outputs checked against prior independently certified decisions. Shared endpoint/model premises remain; not physical validity, adoption or measured runtime/storage/policy benefit.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
