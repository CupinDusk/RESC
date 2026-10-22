"""Pre-observation ranking plan, then certified gates and standard graph fallback."""
from pathlib import Path
from itertools import permutations,combinations
from collections import defaultdict,Counter
from decimal import Decimal
from fractions import Fraction as F
import csv,hashlib,json
import hopper_exact_certificates as ec
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def route(blo,bhi,dlo,dhi,C):
 if dhi<blo:return 'marginal_reject'
 if dlo*C.denominator>=C.numerator*bhi:return 'factor_admit'
 return 'graph_fallback'
def main():
 out=HERE/'HOPPER_R14_AUDITOR_RESULTS.json';csvout=HERE/'HOPPER_R14_ALL_AUDITOR_ROUTES.csv';assert not out.exists() and not csvout.exists()
 matching=json.loads((HERE/'HOPPER_R13_MATCHING_RESULTS.json').read_text())
 factors={tuple(r['order']):F(r['factor']) for r in matching['records'] if r['kind']=='complete6'};assert len(factors)==720
 # Planning uses only ranking and slots; no endpoint is loaded until below.
 orders=list(permutations(sorted(range(6),key=lambda a:ec.ARMS[a])))
 plans=[(order,list(combinations(order,2)),factors[tuple(ec.POS[a]-1 for a in order)]) for order in orders]
 assert sum(C==1 for _,_,C in plans)==40
 budgets={f:ec.log_bounds(str(Decimal(1)+Decimal(f))) for f in ec.GRID}
 raw=defaultdict(dict)
 with ec.MATRIX.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):raw[(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))][r['arm']]=(Decimal(r['min_ns']),Decimal(r['max_ns']))
 stats={f:{'ranking_specific':Counter(),'universal4':Counter(),'exact_decisions':Counter(),'graph_certificates':Counter()} for f in ec.GRID}
 total=zero_inputs=uncertain=gate_decisions=0;examples={}
 with csvout.open('w',encoding='utf-8',newline='') as stream:
  w=csv.writer(stream);w.writerow(['case','fraction','C_R','ranking_specific_route','universal4_route','exact_decision'])
  for ci,(key,low,high) in enumerate(ec.load_cells()):
   rows=raw[key]
   for oi,(order,R,C) in enumerate(plans):
    blo,bhi=ec.beta_bounds(low,high,R)
    zero=all(rows[ec.ARMS[p]][0]<=rows[ec.ARMS[q]][1] for p,q in R)
    if zero:
     # Exact positive decimal costs yield an original-variable witness: b=0,
     # theta_i=log(max predecessor lower endpoint). Check every interval/rank.
     fitted={};greatest=Decimal(0)
     for a in order:
      greatest=max(greatest,rows[ec.ARMS[a]][0]);fitted[a]=greatest
      assert rows[ec.ARMS[a]][0]<=fitted[a]<=rows[ec.ARMS[a]][1]
     assert all(fitted[p]<=fitted[q] for p,q in R);blo=bhi=0;zero_inputs+=1
    for fraction,(dlo,dhi) in budgets.items():
     a=route(blo,bhi,dlo,dhi,C);b=route(blo,bhi,dlo,dhi,F(4))
     if zero:decision='admit';certificate='exact_zero_bias_witness'
     else:
      tight=ec.exact_feasibility(ec.graph(low,high,R,dlo,False))
      if 'potential' in tight:decision='admit';certificate='integer_potential'
      else:
       relaxed=ec.exact_feasibility(ec.graph(low,high,R,dhi,True))
       if 'cycle' in relaxed:decision='reject';certificate='integer_negative_cycle'
       else:decision='unknown';certificate='outward_boundary_unresolved';uncertain+=1
     for r in [a,b]:
      if r!='graph_fallback':
       gate_decisions+=1;assert decision==('reject' if r=='marginal_reject' else 'admit'),(key,order,fraction,r,decision)
     assert not (a=='graph_fallback' and b!='graph_fallback')
     for name,r in [('ranking_specific',a),('universal4',b)]:stats[fraction][name][r]+=1
     stats[fraction]['exact_decisions'][decision]+=1;stats[fraction]['graph_certificates'][certificate]+=1
     w.writerow([ci*720+oi,fraction,str(C),a,b,decision]);total+=1
     if a!=b and fraction not in examples:examples[fraction]={'cell':key,'order':[ec.ARMS[x] for x in order],'C_R':str(C),'ranking_specific_route':a,'universal4_route':b,'exact_decision':decision}
   if ci%16==0 or ci==88:print(json.dumps({'stage':'planned_auditor','cells':ci+1,'queries':total}),flush=True)
 assert total==384480
 result={'result':'PASS_ALL_PLANNED_AUDITOR_GATES_AGREE_WITH_INDEPENDENT_EXACT_CHECKS' if uncertain==0 else 'ALL_GATES_CHECKED_WITH_RETAINED_UNRESOLVED_BOUNDARIES',
 'protocol_sha256':sha(HERE/'HOPPER_R14_AUDITOR_PROTOCOL.json'),'script_sha256':sha(Path(__file__)),
 'matrix_sha256':sha(ec.MATRIX),'matching_results_sha256':sha(HERE/'HOPPER_R13_MATCHING_RESULTS.json'),
 'ranking_plans':720,'exact_for_all_rectangles_plans':40,'fallback_capable_plans':680,
 'complete_order_inputs':64080,'zero_beta_original_witnesses':zero_inputs,'all_fixed_budget_queries':total,
 'both_plans_gated_decisions_checked':gate_decisions,'unresolved_exact_decisions_preserved':uncertain,
 'all_budget_outcomes':{f:{k:dict(v) for k,v in t.items()} for f,t in stats.items()},
 'first_difference_per_fixed_budget':examples,'full_route_csv_sha256':sha(csvout),
 'scope':'Constructed conditional reference auditor. Slots/R determine the plan before loading endpoints; all gates independently checked. Dependent routing counts are not measured cost savings, deployed adoption, calibrated physical timing or improved choices.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
