"""Prespecified shared-trajectory conjunctions; independent original x/b LPs."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import permutations
import csv,hashlib,json,math
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
MATRIX=HERE.parent/'artifacts/hopper-retained-v1/selected-summary-matrix.csv'
ARMS=['PULL','PULL_FLAT','PUSH_ST','GLOBAL','PUSH_BULK','PUSH_STASYNC']
POS={'PULL':1,'PUSH_ST':2,'PUSH_BULK':3,'GLOBAL':4,'PUSH_STASYNC':5,'PULL_FLAT':6}
GRID=[0,.005,.01,.02,.05,.10]
TOL=1e-10
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def margin(l,u,pos,q,d,anchor=None):
 p,b,r,s=q
 def D(a,b):
  if a==b:return 0.
  dist=abs(pos[a]-pos[b]) if anchor is None else abs(pos[a]-anchor)+abs(pos[b]-anchor)
  return u[b]-l[a]+d*dist
 return [D(p,b),D(r,s),D(p,s)+D(r,b)]
def lp(l,u,pos,q,d,anchor=None):
 arms=list(l);n=len(arms);maxj=max(pos.values());N=n+maxj+1
 bounds=[(l[a],u[a]) for a in arms]
 bounds += [(None,None) if j else (0.,0.) for j in range(maxj+1)] if anchor is None else [(-d*abs(j-anchor),d*abs(j-anchor)) for j in range(maxj+1)]
 cons=[];rhs=[]
 if anchor is None:
  for j in range(1,maxj+1):
   a=[0.]*N;a[n+j]=1;a[n+j-1]=-1
   cons.extend([a,[-v for v in a]]);rhs.extend([d,d])
 for p,r in [(q[0],q[1]),(q[2],q[3])]:
  a=[0.]*N;a[arms.index(p)]=1;a[arms.index(r)]=-1
  a[n+pos[p]]=-1;a[n+pos[r]]=1;cons.append(a);rhs.append(0.)
 res=linprog(np.zeros(N),A_ub=cons,b_ub=rhs,bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 assert res.status in [0,2],res.message
 return res
def main():
 out=HERE/'HOPPER_R7_JOINT_RESULTS.json';rowsout=HERE/'HOPPER_R7_ALL_JOINT_QUERIES.csv'
 assert not out.exists() and not rowsout.exists()
 cells=defaultdict(dict)
 with MATRIX.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):
   cells[(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))][r['arm']]=[float(r['min_ns']),float(r['max_ns'])]
 assert len(cells)==89
 queries=sorted(q for q in permutations(ARMS,4) if q[:2]<q[2:]);assert len(queries)==180
 reports=[];examples={};npath=nbox=0;near=0;maxlpviolation=0.
 with rowsout.open('w',encoding='utf-8',newline='') as f:
  cols=['fraction','pattern','C','launched_clusters','payload_B','p','q','r','s','individual_1','individual_2','path_cross','best_box_cross','median_anchor','category']
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
  for frac in GRID:
   d=math.log1p(frac);counts=Counter()
   for key,row in sorted(cells.items()):
    l={a:math.log(row[a][0]) for a in ARMS};u={a:math.log(row[a][1]) for a in ARMS}
    for q in queries:
     vals=margin(l,u,POS,q,d);positions=sorted(POS[a] for a in q);anchor=(positions[1]+positions[2])/2
     bm=margin(l,u,POS,q,d,anchor);ind=min(vals[:2])>=-TOL;feas=ind and vals[2]>=-TOL
     cat='individual_infeasible' if not ind else 'joint_feasible' if feas else 'joint_infeasible_every_anchor_box_feasible' if bm[2]>=-TOL else 'joint_infeasible_recoverable_by_median_box'
     counts[cat]+=1
     if min(abs(v) for v in vals)<1e-9:near+=1
     rec=dict(zip(cols[:9],[frac,*key,*q]));rec.update(dict(zip(cols[9:],[*vals,bm[2],anchor,cat])));w.writerow(rec)
     if cat not in examples:
      examples[cat]={'query':rec,'all_arm_intervals_ns':row,'positions':POS,'two_path_cross_edges':[u[q[3]]-l[q[0]]+d*abs(POS[q[0]]-POS[q[3]]),u[q[1]]-l[q[2]]+d*abs(POS[q[2]]-POS[q[1]])]}
     if frac==.02:
      res=lp(l,u,POS,q,d);npath+=1
      assert res.success==feas,(key,q,vals,res.message)
      if res.success:
       n=len(l);theta={a:res.x[i]-res.x[n+POS[a]] for i,a in enumerate(l)}
       violation=max(theta[q[0]]-theta[q[1]],theta[q[2]]-theta[q[3]],0.);maxlpviolation=max(maxlpviolation,violation);assert violation<1e-8
      if cat=='joint_infeasible_every_anchor_box_feasible':
       bres=lp(l,u,POS,q,d,anchor);nbox+=1;assert bres.success,(key,q,bm,bres.message)
   assert sum(counts.values())==16020
   reports.append({'fraction':frac,'delta':d,'queries':sum(counts.values()),'counts':dict(counts)})
   print(json.dumps({'fraction':frac,'counts':dict(counts),'path_LPs_so_far':npath,'box_LPs_so_far':nbox}),flush=True)
 fl={str(j):v for j,v in enumerate([.015,0.,0.,.015],1)};fu=dict(fl);fp={str(j):j for j in range(1,5)};fq=('1','3','4','2')
 fm=margin(fl,fu,fp,fq,.01);fb=margin(fl,fu,fp,fq,.01,2.5)
 assert all(abs(a-b)<1e-12 for a,b in zip(fm,[.005,.005,-.01]))
 assert abs(fb[2]-.01)<1e-12 and not lp(fl,fu,fp,fq,.01).success
 br=lp(fl,fu,fp,fq,.01,2.5);assert br.success
 fixture={'positions':fp,'point_log_costs':fl,'query':fq,'delta':.01,'path_margins':fm,'best_box_margins':fb,'median_anchor':2.5,'median_box_original_variable_witness':br.x.tolist(),'path_original_LP_infeasible':True,'negative_cycle_sum':-.01}
 result={'result':'PASS_JOINT_CONJUNCTION_AND_ALL_REAL_ANCHOR_CHARACTERIZATION','protocol_sha256':sha(HERE/'HOPPER_R7_JOINT_PROTOCOL.json'),'argument_sha256':sha(HERE/'HOPPER_R7_JOINT_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),'matrix_sha256':sha(MATRIX),'all_queries_csv_sha256':sha(rowsout),'all_queries':96120,'reports':reports,'lexicographically_first_examples':examples,'known_truth_fixture':fixture,'independent_checks':{'original_path_LPs':npath,'original_median_box_LPs':nbox,'controlled_fixture_LPs':2,'disagreements':0,'maximum_feasible_ranking_violation':maxlpviolation,'analytic_tolerance':TOL,'LP_primal_and_dual_tolerance':1e-9,'cases_with_any_margin_within_1e-9':near},'boundary':'Dependent conditional grid; no newly acquired GPU data, physical bias budget or observed ranking ground truth. Standard difference-constraint closure is prior machinery.'}
 assert npath==16020
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'result':result['result'],'independent_checks':result['independent_checks'],'examples':examples}),flush=True)
if __name__=='__main__':main()
