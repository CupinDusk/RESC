"""Six-arm printed example with outward logs and exact original-variable checks."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
from decimal import Decimal
import csv,hashlib,json
import hopper_exact_certificates as ec
from hopper_ranking_factor import exact_witness
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=HERE/'HOPPER_R13_WORKED_ORDER_RESULTS.json';assert not out.exists()
 selected=json.loads((HERE/'HOPPER_R13_MATCHING_RESULTS.json').read_text())['printed_example_selection']
 row=selected['source_row'];key=(row['pattern'],int(row['C']),int(row['clusters']),int(row['payload_B']))
 raw={}
 with ec.MATRIX.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):
   if r['arm'] in ec.ARMS and (r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))==key:raw[r['arm']]=[r['min_ns'],r['max_ns']]
 assert len(raw)==6
 order=[ec.ARMS.index(a) for a in row['order'].split('<=')];R=list(combinations(order,2))
 low=[ec.log_bounds(raw[a][0]) for a in ec.ARMS];high=[ec.log_bounds(raw[a][1]) for a in ec.ARMS]
 blo,bhi=ec.beta_bounds(low,high,R);oldlo,oldhi=ec.log_bounds('1.005')
 assert bhi<oldlo
 neg=ec.exact_feasibility(ec.graph(low,high,R,oldhi,True));assert 'cycle' in neg
 dl=int(Decimal('.005134328557')*ec.U);du=int(Decimal('.005134328558')*ec.U)
 below=ec.exact_feasibility(ec.graph(low,high,R,dl,True));assert 'cycle' in below
 above=ec.exact_feasibility(ec.graph(low,high,R,du,False));assert 'potential' in above
 pos=dict(enumerate(ec.POS));l={a:F(low[a][1],ec.U) for a in range(6)};u={a:F(high[a][0],ec.U) for a in range(6)}
 witness=exact_witness(l,u,pos,R,F(du,ec.U))
 edges=[{'from':ec.ARMS[a],'to':ec.ARMS[b],'weight_scaled':str(w),'constant_scaled':str(c),'distance':d,'kind':kind} for a,b,w,c,d,kind in neg['cycle']]
 total=sum(e[2] for e in neg['cycle']);assert total<0
 critical=below['cycle'];distance=sum(e[4] for e in critical)
 lower_radius=F(-sum(e[3] for e in critical),distance*ec.U)
 assert F(dl,ec.U)<lower_radius<F(du,ec.U)
 result={'result':'PASS_SIX_ARM_COMPLETE_ORDER_OUTWARD_CYCLE_AND_RATIONAL_PATH',
 'protocol_sha256':sha(HERE/'HOPPER_R13_WORKED_ORDER_PROTOCOL.json'),'script_sha256':sha(Path(__file__)),
 'matching_results_sha256':sha(HERE/'HOPPER_R13_MATCHING_RESULTS.json'),'matrix_sha256':sha(ec.MATRIX),
 'selection':selected,'cell':key,'intervals_ns':raw,'slots':dict(zip(ec.ARMS,ec.POS)),
 'order':[ec.ARMS[a] for a in order],'beta_bracket':[float(F(blo,ec.U)),float(F(bhi,ec.U))],
 'integer_scale':str(ec.U),'minimum_radius_bracket':['.005134328557','.005134328558'],
 'cycle_radius_lower_bound':str(lower_radius),'assumed_log_budget_bracket':[str(F(oldlo,ec.U)),str(F(oldhi,ec.U))],
 'negative_cycle':edges,'negative_cycle_sum_scaled':str(total),'negative_cycle_sum':float(F(total,ec.U)),
 'exact_original_variable_witness_at_upper_bracket':witness,
 'rounded_bias_b0_to_b6':[round(float(F(witness['bias'][str(j)])),12) for j in range(7)],
 'rounded_theta_in_order':[round(float(F(witness['theta'][str(a)])),12) for a in order],
 'scope':'Rational witness obeys the tightened rectangle and every original adjacent/ranking inequality. Printed decimals are approximations; saved rational values and outward logs certify the bracket. No new hardware or physical-budget validation.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k not in ['exact_original_variable_witness_at_upper_bracket','assumed_log_budget_bracket']},indent=2))
if __name__=='__main__':main()
