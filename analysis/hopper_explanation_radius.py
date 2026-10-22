"""Post-review inverse joint-budget audit; all retained cases and fixed fixtures."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import permutations
import csv,hashlib,json,math
import numpy as np
from scipy.optimize import linprog
from hopper_joint_queries import lp,margin
HERE=Path(__file__).resolve().parent
MATRIX=HERE.parent/'artifacts/hopper-retained-v1/selected-summary-matrix.csv'
ARMS=['PULL','PULL_FLAT','PUSH_ST','GLOBAL','PUSH_BULK','PUSH_STASYNC']
POS={'PULL':1,'PUSH_ST':2,'PUSH_BULK':3,'GLOBAL':4,'PUSH_STASYNC':5,'PULL_FLAT':6}
GRID=[0,.005,.01,.02,.05,.10]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def radius(l,u,pos,q):
 p,t,r,s=q;a=l[p]-u[t];b=l[r]-u[s]
 d1=abs(pos[p]-pos[t]);d2=abs(pos[r]-pos[s]);c=abs(pos[p]-pos[s])+abs(pos[r]-pos[t])
 pair=max(0.,a/d1,b/d2);joint=max(pair,(a+b)/c)
 assert joint<=pair*(max(pos.values())-min(pos.values())-1)+1e-10 if pair else joint==0
 return {'a':a,'b':b,'own_distances':[d1,d2],'cross_distance':c,'pair_radius':pair,'joint_radius':joint,'window_width':joint-pair,'ratio':joint/pair if pair else None}
def min_lp(l,u,pos,comparisons):
 arms=list(l);n=len(arms);maxj=max(pos.values());last=n+maxj+1;N=last+1
 bounds=[(l[a],u[a]) for a in arms]+[(0.,0.) if not j else (None,None) for j in range(maxj+1)]+[(0.,None)]
 cons=[];rhs=[]
 for j in range(1,maxj+1):
  a=[0.]*N;a[n+j]=1;a[n+j-1]=-1;a[last]=-1
  b=[-v for v in a];b[last]=-1;cons.extend([a,b]);rhs.extend([0.,0.])
 for p,q in comparisons:
  a=[0.]*N;a[arms.index(p)]=1;a[arms.index(q)]=-1;a[n+pos[p]]=-1;a[n+pos[q]]=1;cons.append(a);rhs.append(0.)
 objective=[0.]*N;objective[-1]=1
 res=linprog(objective,A_ub=cons,b_ub=rhs,bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 assert res.success,res.message
 theta={a:float(res.x[i]-res.x[n+pos[a]]) for i,a in enumerate(arms)}
 return float(res.fun),{'x':[float(v) for v in res.x[:n]],'bias':[float(v) for v in res.x[n:-1]],'theta':theta,'maximum_ranking_violation':max([theta[p]-theta[q] for p,q in comparisons]+[0.])}
def feasibility(l,u,pos,comparisons,d,anchor=None):
 # Independent generic LP, allowing more than two ranking edges.
 arms=list(l);n=len(arms);maxj=max(pos.values());N=n+maxj+1
 bounds=[(l[a],u[a]) for a in arms]+([(0.,0.) if not j else (None,None) for j in range(maxj+1)] if anchor is None else [(-d*abs(j-anchor),d*abs(j-anchor)) for j in range(maxj+1)])
 cons=[];rhs=[]
 if anchor is None:
  for j in range(1,maxj+1):
   a=[0.]*N;a[n+j]=1;a[n+j-1]=-1;cons.extend([a,[-v for v in a]]);rhs.extend([d,d])
 for p,q in comparisons:
  a=[0.]*N;a[arms.index(p)]=1;a[arms.index(q)]=-1;a[n+pos[p]]=-1;a[n+pos[q]]=1;cons.append(a);rhs.append(0.)
 res=linprog([0.]*N,A_ub=cons,b_ub=rhs,bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9});assert res.status in [0,2]
 return res.success
def main():
 out=HERE/'HOPPER_R8_RADIUS_RESULTS.json';csvout=HERE/'HOPPER_R8_ALL_RADII.csv';assert not out.exists() and not csvout.exists()
 cells=defaultdict(dict)
 with MATRIX.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):cells[(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))][r['arm']]=[float(r['min_ns']),float(r['max_ns'])]
 queries=sorted(q for q in permutations(ARMS,4) if q[:2]<q[2:]);assert len(queries)==180 and len(cells)==89
 records=[];positive=[];affected={f:defaultdict(list) for f in GRID};lpcount=boundcount=0;maxerr=0.;maxviolation=0.;nearwidth=0
 with csvout.open('w',encoding='utf-8',newline='') as f:
  fields=['pattern','C','clusters','payload_B','p','q','r','s','pair_radius','joint_radius','window_width','ratio'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for key,row in sorted(cells.items()):
   l={a:math.log(row[a][0]) for a in ARMS};u={a:math.log(row[a][1]) for a in ARMS}
   for q in queries:
    rad=radius(l,u,POS,q);rec={'cell':key,'query':q,**rad};records.append(rec)
    w.writerow(dict(zip(fields,[*key,*q,rad['pair_radius'],rad['joint_radius'],rad['window_width'],rad['ratio']])))
    if 0<rad['window_width']<=1e-12:nearwidth+=1
    if rad['window_width']>1e-12:
     positive.append(rec)
     for d,expected in [(rad['pair_radius'],False),((rad['pair_radius']+rad['joint_radius'])/2,False),(rad['joint_radius'],True)]:
      result=lp(l,u,POS,q,d).success;boundcount+=1
      # At the pair boundary, only the joint margin controls the negative answer.
      assert result==expected,(key,q,d,rad,result)
    for frac in GRID:
     m=margin(l,u,POS,q,math.log1p(frac))
     if min(m[:2])>=-1e-10 and m[2]<-1e-10:
      affected[frac][key].append(rec)
      if frac==.02:
       val,wit=min_lp(l,u,POS,[(q[0],q[1]),(q[2],q[3])]);lpcount+=1;maxerr=max(maxerr,abs(val-rad['joint_radius']));maxviolation=max(maxviolation,wit['maximum_ranking_violation']);assert abs(val-rad['joint_radius'])<1e-8
       rec['independent_minimum_LP']={'delta':val,'witness':wit}
 print(json.dumps({'retained_queries':len(records),'positive_windows':len(positive),'min_delta_LPs':lpcount,'boundary_LPs':boundcount}),flush=True)
 family=[];controlLP=0
 for N in [4,5,6,8,16,32,64]:
  pos={'p':1,'q':N-1,'r':N,'s':2};q=('p','q','r','s');center={'p':.01,'q':0.,'r':.01,'s':0.}
  for eps in [0.,.001,.004]:
   l={a:v-eps for a,v in center.items()};u={a:v+eps for a,v in center.items()};rad=radius(l,u,pos,q)
   assert abs(rad['ratio']-(N-2))<1e-10
   minval,wit=min_lp(l,u,pos,[('p','q'),('r','s')]);controlLP+=1;assert abs(minval-rad['joint_radius'])<1e-9
   samples=[]
   for d in [.99*rad['pair_radius'],rad['pair_radius'],(rad['pair_radius']+rad['joint_radius'])/2,.999*rad['joint_radius'],rad['joint_radius'],1.001*rad['joint_radius']]:
    path=feasibility(l,u,pos,[('p','q'),('r','s')],d);controlLP+=1
    individual=[feasibility(l,u,pos,[claim],d) for claim in [('p','q'),('r','s')]];controlLP+=2
    assert path==(d>=rad['joint_radius']-1e-12) and all(individual)==(d>=rad['pair_radius']-1e-12)
    anchors=sorted(set([j/2 for j in range(2*N+1)]+[(N+1)/2]));bok=[feasibility(l,u,pos,[('p','q'),('r','s')],d,a) for a in anchors];controlLP+=len(anchors)
    if d>=rad['pair_radius']-1e-12:assert all(bok)
    else:assert not all(bok)
    samples.append({'delta':d,'shared_path_feasible':path,'individual_feasible':individual,'checked_anchors':anchors,'box_feasible':bok})
   family.append({'N':N,'v':.01,'epsilon':eps,'positions':pos,'log_center':center,**rad,'attaining_LP_delta':minval,'samples':samples})
 l={'1':.009,'2':0.,'3':0.,'4':.018};u=dict(l);pos={a:int(a) for a in l};order=['1','3','4','2'];edges=list(zip(order,order[1:]));d=.01
 fullval,wit=min_lp(l,u,pos,edges);controlLP+=1
 implied=[(a,b) for i,a in enumerate(order) for b in order[i+1:]]
 pair_margins=[{'p':a,'q':b,'margin':u[b]-l[a]+d*abs(pos[a]-pos[b])} for a,b in implied]
 assert all(r['margin']>0 for r in pair_margins)
 path=feasibility(l,u,pos,edges,d);controlLP+=1;assert not path
 anchors=[j/2 for j in range(9)];boxes=[feasibility(l,u,pos,edges,d,a) for a in anchors];controlLP+=len(anchors);assert all(boxes)
 full={'point_logs':l,'order':order,'delta':d,'all_implied_pair_margins':pair_margins,'shared_path_feasible':path,'checked_anchors':anchors,'box_feasible':boxes,'minimum_shared_budget_LP':fullval,'attaining_witness':wit}
 counts=[sum(map(len,affected[f].values())) for f in GRID];assert counts==[0,2,11,18,102,286]
 distributions={'queries':len(records),'positive_width_windows':len(positive),'distinct_cells_with_any_positive_window':len({tuple(r['cell']) for r in positive}),'zero_pair_radius':sum(r['pair_radius']==0 for r in records),'positive_width_below_1e-12':nearwidth,'maximum_ratio':max(r['ratio'] for r in records if r['ratio'] is not None),'maximum_width':max(r['window_width'] for r in records),'ratio_of_positive_window_quantiles':dict(zip(['min','q25','median','q75','max'],map(float,np.quantile([r['ratio'] for r in positive],[0,.25,.5,.75,1]))))}
 affected_reports=[]
 for f in GRID:
  affected_reports.append({'fraction':f,'delta':math.log1p(f),'dependent_query_count':sum(map(len,affected[f].values())),'distinct_affected_cells':len(affected[f]),'cells':[{'cell':k,'query_count':len(v),'queries':v} for k,v in sorted(affected[f].items())]})
 first=positive[0];maxratio=max(positive,key=lambda r:r['ratio'])
 for rec in [first,maxratio]:rec['all_arm_intervals_ns']=cells[tuple(rec['cell'])];rec['positions']=POS
 result={'result':'PASS_MINIMUM_SHARED_EXPLANATION_BUDGET_AND_SHARP_SLOT_FACTOR','protocol_sha256':sha(HERE/'HOPPER_R8_RADIUS_PROTOCOL.json'),'argument_sha256':sha(HERE/'HOPPER_R8_RADIUS_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),'matrix_sha256':sha(MATRIX),'complete_radius_csv_sha256':sha(csvout),'distribution':distributions,'affected_by_old_budget':affected_reports,'lexicographically_first_positive_window':first,'maximum_ratio_case':maxratio,'controlled_tight_family':family,'controlled_full_ranking':full,'independent_checks':{'minimum_delta_original_LPs':lpcount,'positive_window_boundary_and_midpoint_LPs':boundcount,'controlled_original_LPs':controlLP,'maximum_radius_error':maxerr,'maximum_attaining_ranking_violation':maxviolation,'disagreements':0,'solver':'SciPy linprog HiGHS','primal_and_dual_feasibility_tolerance':1e-9,'positive_window_threshold':1e-12,'retained_margin_classification_tolerance':1e-10},'boundary':'Post-review secondary analytic/controlled evaluation; finite-slot inverse-budget loss, not new general DBM/cycle-ratio algorithms. No physical H20 budget, new hardware, same-state truth or causal identification.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'result':result['result'],'distribution':distributions,'affected_counts':[(r['fraction'],r['dependent_query_count'],r['distinct_affected_cells']) for r in affected_reports],'first_window':first,'maximum_ratio':maxratio,'full_ranking':full,'checks':result['independent_checks']},indent=2),flush=True)
if __name__=='__main__':main()
