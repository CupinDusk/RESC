"""Theory-led full partial-ranking checks against original-variable LPs."""
from pathlib import Path
from itertools import permutations, combinations, product
from collections import defaultdict
import csv, hashlib, json, math
import numpy as np
from scipy.optimize import linprog
from hopper_explanation_radius import min_lp, ARMS, POS, MATRIX, GRID

HERE=Path(__file__).resolve().parent
TOL=1e-8

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def closure(n,edges):
 a=[[False]*n for _ in range(n)]
 for p,q in edges:a[p][q]=True
 for k in range(n):
  for i in range(n):
   for j in range(n):a[i][j]=a[i][j] or (a[i][k] and a[k][j])
 assert not any(a[i][i] for i in range(n))
 return tuple((i,j) for i in range(n) for j in range(n) if a[i][j])

def all_orders(n):
 found=set()
 for order in permutations(range(n)):
  forward=list(combinations(order,2))
  for bits in range(1<<len(forward)):
   found.add(closure(n,[e for i,e in enumerate(forward) if bits>>i&1]))
 return sorted(found)

def box_formula(l,u,pos,edges,anchor=None):
 return max([0.]+[(l[p]-u[q])/(abs(pos[p]-pos[q]) if anchor is None else abs(pos[p]-anchor)+abs(pos[q]-anchor)) for p,q in edges])

def box_min_lp(l,u,pos,edges,anchor):
 arms=list(l);n=len(arms);maxj=max(pos.values());last=n+maxj+1;N=last+1
 bounds=[(l[a],u[a]) for a in arms]+[(None,None)]*(maxj+1)+[(0.,None)]
 cons=[];rhs=[]
 for j in range(maxj+1):
  a=[0.]*N;a[n+j]=1;a[last]=-abs(j-anchor)
  b=[0.]*N;b[n+j]=-1;b[last]=-abs(j-anchor)
  cons.extend([a,b]);rhs.extend([0.,0.])
 for p,q in edges:
  a=[0.]*N;a[arms.index(p)]=1;a[arms.index(q)]=-1;a[n+pos[p]]=-1;a[n+pos[q]]=1
  cons.append(a);rhs.append(0.)
 objective=[0.]*N;objective[-1]=1
 res=linprog(objective,A_ub=cons,b_ub=rhs,bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 assert res.success,res.message
 return float(res.fun)

def negative_cycle(l,u,pos,edges,delta):
 arms=list(l);graph=[(a,b,u[b]-l[a]+delta*abs(pos[a]-pos[b]),'observation') for a in arms for b in arms if a!=b]
 graph += [(q,p,0.,'ranking') for p,q in edges]
 dist={a:0. for a in arms};pred={};updated=None
 for _ in arms:
  updated=None
  for a,b,w,kind in graph:
   if dist[b]>dist[a]+w+1e-13:
    dist[b]=dist[a]+w;pred[b]=(a,b,w,kind);updated=b
  if updated is None:return None
 v=updated
 for _ in arms:v=pred[v][0]
 start=v;back=[]
 while True:
  e=pred[v];back.append(e);v=e[0]
  if v==start:break
 cycle=list(reversed(back));weight=sum(e[2] for e in cycle)
 assert weight < -1e-10,(cycle,weight)
 return {'delta':delta,'edges':[{'from':a,'to':b,'weight':w,'kind':kind} for a,b,w,kind in cycle],'weight':weight,'edge_semantics':'theta_to - theta_from <= weight'}

def main():
 out=HERE/'HOPPER_R9_ORDER_RESULTS.json';csvout=HERE/'HOPPER_R9_ALL_TOTAL_ORDERS.csv'
 assert not out.exists() and not csvout.exists()
 checks={'exhaustive_cases':0,'random_cases':0,'path_minimum_LPs':0,'box_minimum_LPs':0,'maximum_box_radius_error':0.,'maximum_path_witness_ranking_violation':0.,'maximum_factor_excess':0.,'maximum_lower_bound_excess':0.,'zero_box_radius_cases':0,'positive_windows_at_or_below_1e-10':0,'disagreements':0}
 def check(l,u,pos,edges,anchors,kind):
  beta=box_formula(l,u,pos,edges);path,wit=min_lp(l,u,pos,edges);checks['path_minimum_LPs']+=1
  checks[kind+'_cases']+=1
  checks['maximum_path_witness_ranking_violation']=max(checks['maximum_path_witness_ranking_violation'],wit['maximum_ranking_violation'])
  excess=path-max(1,max(pos.values())-2)*beta;lower=beta-path
  checks['maximum_factor_excess']=max(checks['maximum_factor_excess'],excess);checks['maximum_lower_bound_excess']=max(checks['maximum_lower_bound_excess'],lower)
  assert excess<=TOL and lower<=TOL,(kind,l,u,pos,edges,beta,path)
  if beta<=1e-12:checks['zero_box_radius_cases']+=1;assert path<=TOL
  if 0<path-beta<=1e-10:checks['positive_windows_at_or_below_1e-10']+=1
  achieved=0.
  for a in anchors:
   predicted=box_formula(l,u,pos,edges,a);actual=box_min_lp(l,u,pos,edges,a);checks['box_minimum_LPs']+=1
   checks['maximum_box_radius_error']=max(checks['maximum_box_radius_error'],abs(predicted-actual));assert abs(predicted-actual)<=TOL
   achieved=max(achieved,actual)
  assert abs(achieved-beta)<=TOL,(achieved,beta,anchors,pos)
  return beta,path
 poset_counts={}
 for n in [2,3,4]:
  orders=all_orders(n);poset_counts[str(n)]=len(orders);assert len(orders)=={2:3,3:19,4:219}[n]
  pos={i:i+1 for i in range(n)}
  for values in product([0.,.01],repeat=n):
   for eps in [0.,.001]:
    l={i:values[i]-eps for i in range(n)};u={i:values[i]+eps for i in range(n)}
    for edges in orders:check(l,u,pos,edges,list(range(1,n+1)),'exhaustive')
  print(json.dumps({'stage':'exhaustive','n':n,'posets':len(orders),'cumulative_cases':checks['exhaustive_cases']}),flush=True)
 rng=np.random.default_rng(20261022)
 for n in [5,6,7,8]:
  for case in range(64):
   N=[n,2*n,4*n][case%3];positions=rng.choice(np.arange(1,N+1),size=n,replace=False)
   pos={i:int(positions[i]) for i in range(n)};topo=list(map(int,rng.permutation(n)));prob=[.2,.5,.8][case%3]
   edges=closure(n,[e for e in combinations(topo,2) if rng.random()<prob])
   values=rng.uniform(-.02,.02,size=n);widths=rng.uniform(0,.002,size=n)
   l={i:float(values[i]-widths[i]) for i in range(n)};u={i:float(values[i]+widths[i]) for i in range(n)}
   points=sorted(pos.values());anchors=points+[(a+b)/2 for a,b in zip(points,points[1:])]+[-1,N+1]
   check(l,u,pos,edges,anchors,'random')
  print(json.dumps({'stage':'random','n':n,'cumulative_cases':checks['random_cases']}),flush=True)
 # Review-discovered mixed-direction-star diagnostic; direct edges are insufficient.
 l={'p':0.,'q':.01,'r':-.02};u=dict(l);pos={'p':1,'q':2,'r':3};direct=[('q','p'),('p','r')];implied=direct+[('q','r')]
 beta=box_formula(l,u,pos,implied);path,wit=min_lp(l,u,pos,direct)
 diagnostic={'origin':'R8 independent reviewer3 counterexample, not new device data','point_logs':l,'positions':pos,'direct_claims':direct,'direct_pair_radius':box_formula(l,u,pos,direct),'transitive_all_anchor_radius':beta,'minimum_path_radius':path,'witness':wit}
 assert abs(beta-.03)<1e-12 and abs(path-.03)<1e-9
 # An exact, interpretable attaining path for the existing first retained example.
 first_l={'F':math.log(2213.4),'P':math.log(2160.),'B':math.log(2788.5),'A':math.log(2792.6)}
 first_u={'F':math.log(2226.4),'P':math.log(2173.1),'B':math.log(2793.1),'A':math.log(2796.8)}
 first_pos={'F':6,'P':1,'B':3,'A':5};h1=first_l['F']-first_u['P'];h2=first_l['B']-first_u['A'];d=(h1+h2)/3
 b=[0.,0.,d,2*d,3*d,4*d,5*d]
 x={'F':first_l['F'],'P':first_u['P'],'B':first_l['B'],'A':first_u['A']};theta={a:x[a]-b[first_pos[a]] for a in x}
 cycle=[{'inequality':'b1-b6 <= -h1','rhs':-h1},{'inequality':'b5-b3 <= -h2','rhs':-h2},{'inequality':'b6-b5 <= delta','rhs':d},{'inequality':'b3-b1 <= 2delta','rhs':2*d}]
 # This simple linear path only attains both claims if their individual
 # thresholds agree. Otherwise construct the boundary witness independently.
 optimum,first_wit=min_lp(first_l,first_u,first_pos,[('F','P'),('B','A')])
 assert abs(optimum-d)<=1e-9
 worked={'intervals_ns':{a:[math.exp(first_l[a]),math.exp(first_u[a])] for a in x},'positions':first_pos,'h1':h1,'h2':h2,'delta_joint':d,'cycle':cycle,'negative_cycle_at_half_percent_total':3*math.log1p(.005)-h1-h2,'attaining_original_LP_witness':first_wit}
 cells=defaultdict(dict)
 with MATRIX.open(encoding='utf-8',newline='') as f:
  for row in csv.DictReader(f):cells[(row['pattern'],int(row['C']),int(row['launched_clusters']),int(row['payload_B']))][row['arm']]=[float(row['min_ns']),float(row['max_ns'])]
 affected={f:{'queries':0,'cells':set()} for f in GRID};total=positive=zero=small=0;ratios=[];first=None;maximum=None;max_excess=max_lower=max_wit=0.
 orders=list(permutations(sorted(ARMS)))
 with csvout.open('w',encoding='utf-8',newline='') as f:
  fields=['pattern','C','clusters','payload_B','order','all_anchor_radius','shared_path_radius','window_width','ratio'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for cell_index,(key,row) in enumerate(sorted(cells.items())):
   l={a:math.log(row[a][0]) for a in ARMS};u={a:math.log(row[a][1]) for a in ARMS}
   for order in orders:
    implied=list(combinations(order,2));chain=list(zip(order,order[1:]));beta=box_formula(l,u,POS,implied);path,wit=min_lp(l,u,POS,chain)
    total+=1;difference=path-beta;ratio=path/beta if beta>1e-12 else None
    max_excess=max(max_excess,path-4*beta);max_lower=max(max_lower,beta-path);max_wit=max(max_wit,wit['maximum_ranking_violation'])
    assert path<=4*beta+TOL and path>=beta-TOL,(key,order,beta,path)
    if beta<=1e-12:zero+=1;assert path<=TOL
    if 0<difference<=1e-10:small+=1
    writer.writerow(dict(zip(fields,[*key,'<='.join(order),beta,path,difference,ratio])))
    if difference>1e-10:
     positive+=1;ratios.append(ratio)
     rec={'cell':key,'order':order,'all_anchor_radius':beta,'shared_path_radius':path,'window_width':difference,'ratio':ratio,'all_arm_intervals_ns':row,'positions':POS,'attaining_witness':wit}
     if first is None:
      first=rec;first['midpoint_negative_cycle']=negative_cycle(l,u,POS,chain,(beta+path)/2)
     if maximum is None or ratio>maximum['ratio']:maximum=rec
    for frac in GRID:
     delta=math.log1p(frac)
     if beta<=delta+1e-10 and path>delta+1e-10:affected[frac]['queries']+=1;affected[frac]['cells'].add(key)
   if (cell_index+1)%16==0:print(json.dumps({'stage':'retained_total_orders','cells':cell_index+1,'queries':total}),flush=True)
 assert total==89*720
 retained={'queries':total,'positive_width_windows':positive,'zero_all_anchor_radius':zero,'small_positive_differences_at_or_below_1e-10':small,'positive_window_ratio_quantiles':dict(zip(['min','q25','median','q75','max'],map(float,np.quantile(ratios,[0,.25,.5,.75,1])))) if ratios else {},'affected_old_budgets':[{'fraction':frac,'queries':v['queries'],'distinct_cells':len(v['cells']),'cell_identities':sorted(v['cells'])} for frac,v in affected.items()],'first_lexicographic_positive_window':first,'maximum_ratio_case':maximum,'maximum_factor_excess':max_excess,'maximum_lower_bound_excess':max_lower,'maximum_attaining_ranking_violation':max_wit,'original_minimum_path_LPs':total,'complete_csv_sha256':sha(csvout)}
 result={'result':'PASS_ALL_ANCHOR_PARTIAL_RANKING_RADIUS_AND_GENERAL_SHARP_SLOT_BOUND','protocol_sha256':sha(HERE/'HOPPER_R9_ORDER_PROTOCOL.json'),'argument_sha256':sha(HERE/'HOPPER_R9_ORDER_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),'matrix_sha256':sha(MATRIX),'poset_counts':poset_counts,'independent_checks':checks,'mixed_direction_star_diagnostic':diagnostic,'first_H20_explicit_cycle_and_boundary':worked,'retained_total_orders':retained,'solver':'SciPy1.16.3 linprog HiGHS; primal/dual tolerance1e-9; radius tolerance1e-8; window classification1e-10','scope':'Own controlled and retained conditional calculations, no new hardware or known-truth device validation. Standard isotonic/DBM/LP procedures are prior, not a new optimizer.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'result':result['result'],'poset_counts':poset_counts,'checks':checks,'retained':{k:v for k,v in retained.items() if k not in ['first_lexicographic_positive_window','maximum_ratio_case','affected_old_budgets']},'affected':[(v['fraction'],v['queries'],v['distinct_cells']) for v in retained['affected_old_budgets']],'first':first,'maximum':maximum,'H20_boundary_witness':first_wit},indent=2),flush=True)

if __name__=='__main__':main()
