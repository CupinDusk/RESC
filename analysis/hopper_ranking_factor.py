"""Prospective exact fixed-ranking matching factor and attaining rectangles."""
from pathlib import Path
from itertools import combinations,permutations
from functools import lru_cache
from fractions import Fraction as F
from collections import Counter
import csv,hashlib,json,math
import numpy as np
from scipy.optimize import linprog
from hopper_explanation_radius import min_lp,POS,MATRIX
from hopper_partial_orders import all_orders,closure,negative_cycle

HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def strings(d):return {str(k):str(v) for k,v in d.items()}

@lru_cache(maxsize=8)
def blocks(positions):
 n=len(positions);arms=tuple(range(n));out=[]
 for k in range(1,n//2+1):
  for P in combinations(arms,k):
   for Q in combinations(tuple(a for a in arms if a not in P),k):
    matches=[]
    for qs in permutations(Q):
     mask=sum(1<<(p*n+q) for p,q in zip(P,qs))
     cost=sum(abs(positions[p]-positions[q]) for p,q in zip(P,qs))
     matches.append((cost,qs,mask))
    matches.sort();out.append((P,Q,tuple(matches)))
 return tuple(out)

def one_cycle(P,f,g):
 inv={q:i for i,q in enumerate(f)};nxt=[inv[q] for q in g]
 seen=set();cur=0
 while cur not in seen:seen.add(cur);cur=nxt[cur]
 return cur==0 and len(seen)==len(P)

def factor(positions,R,check_cycles=False):
 n=len(positions);mask=sum(1<<(p*n+q) for p,q in R)
 best=F(1);selected=None;cycle_best=F(1)
 for P,Q,matchings in blocks(tuple(positions)):
  allowed=[m for m in matchings if m[2]&mask==m[2]]
  if not allowed:continue
  cr=F(allowed[0][0],matchings[0][0])
  if cr>best:
   best=cr;selected=(P,Q,allowed[0],matchings[0])
  if check_cycles:
   for own in allowed:
    for cross in matchings:
     if one_cycle(P,own[1],cross[1]):cycle_best=max(cycle_best,F(allowed[0][0],cross[0]))
 if check_cycles:assert cycle_best==best,(positions,R,best,cycle_best)
 return best,selected

def beta(l,u,pos,R):return max([F(0)]+[(l[p]-u[q])/abs(pos[p]-pos[q]) for p,q in R])

def exact_witness(l,u,pos,R,delta):
 arms=tuple(l);edges=[(a,b,u[b]-l[a]+delta*abs(pos[a]-pos[b])) for a in arms for b in arms if a!=b]+[(q,p,F(0)) for p,q in R]
 theta={a:F(0) for a in arms}
 for turn in range(len(arms)):
  changed=False
  for a,b,w in edges:
   if theta[b]>theta[a]+w:theta[b]=theta[a]+w;changed=True
  if not changed:break
  assert turn<len(arms)-1,('negative_at_claimed_bound',delta,l,u,pos,R)
 assert all(theta[b]-theta[a]<=w for a,b,w in edges)
 bias={j:max(l[a]-theta[a]-delta*abs(j-pos[a]) for a in arms) for j in range(max(pos.values())+1)}
 gauge=bias[0];bias={j:v-gauge for j,v in bias.items()};theta={a:v+gauge for a,v in theta.items()}
 x={a:theta[a]+bias[pos[a]] for a in arms}
 assert bias[0]==0 and all(abs(bias[j]-bias[j-1])<=delta for j in range(1,max(pos.values())+1))
 assert all(l[a]<=x[a]<=u[a] for a in arms) and all(theta[p]<=theta[q] for p,q in R)
 return {'x':strings(x),'bias':strings(bias),'theta':strings(theta)}

def construction(positions,R,C,selected):
 P,Q,own,cross=selected;k=len(P);pos=dict(enumerate(positions))
 rows=[];rhs=[]
 for i,p in enumerate(P):
  for j,q in enumerate(Q):
   if (p,q) not in R:continue
   a=[0.]*(2*k);a[i]=1.;a[k+j]=-1.;rows.append(a);rhs.append(abs(pos[p]-pos[q]))
 bounds=[(None,None)]*(2*k);bounds[k]=(0.,0.)
 res=linprog([-1.]*k+[1.]*k,A_ub=rows,b_ub=rhs,bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 assert res.success,res.message
 lam={p:int(round(res.x[i])) for i,p in enumerate(P)}
 mu={q:int(round(res.x[k+j])) for j,q in enumerate(Q)}
 assert all(lam[p]-mu[q]<=abs(pos[p]-pos[q]) for p in P for q in Q if (p,q) in R)
 assert sum(lam.values())-sum(mu.values())==own[0]
 M=max([abs(x) for x in list(lam.values())+list(mu.values())]+[0])+max(positions)-min(positions)+10
 l={a:F(lam[a] if a in P else -M) for a in pos};u={a:F(mu[a] if a in Q else M) for a in pos}
 assert all(l[a]<u[a] for a in pos) and beta(l,u,pos,R)==1
 upper_witness=exact_witness(l,u,pos,R,C)
 inv={q:p for p,q in zip(P,own[1])};g=dict(zip(P,cross[1]));unseen=set(P);cycles=[]
 while unseen:
  start=min(unseen);p=start;seq=[]
  while True:
   q=g[p];nxt=inv[q];seq.extend([(p,q,'data'),(q,nxt,'ranking')]);unseen.remove(p);p=nxt
   if p==start:break
  deficit=sum(l[a]-u[b] for a,b,t in seq if t=='data')
  distance=sum(abs(pos[a]-pos[b]) for a,b,t in seq if t=='data')
  assert deficit==C*distance
  cycles.append({'edges':seq,'deficit':str(deficit),'distance':distance,'critical_radius':str(deficit/distance),'midpoint_weight':str(-deficit+((1+C)/2)*distance)})
 assert any(F(c['midpoint_weight'])<0 for c in cycles)
 widths={a:(u[a]-l[a])/2 for a in pos};p,q=next((p,q) for p,q in zip(P,own[1]) if lam[p]-mu[q]==abs(pos[p]-pos[q]))
 bias={j:F(pos[p]-abs(j-pos[p])) for j in range(max(positions)+1)}
 centers={a:bias[pos[a]] for a in pos};centers[p]+=widths[p];centers[q]-=widths[q]
 lo={a:centers[a]-widths[a] for a in pos};up={a:centers[a]+widths[a] for a in pos}
 assert all(up[a]-lo[a]==u[a]-l[a] for a in pos) and beta(lo,up,pos,R)==1
 lower_witness=exact_witness(lo,up,pos,R,F(1))
 fits=[]
 for ll,uu,target in [(l,u,C),(lo,up,F(1))]:
  val,wit=min_lp({a:float(v) for a,v in ll.items()},{a:float(v) for a,v in uu.items()},pos,list(R))
  err=abs(val-float(target));assert err<=1e-8 and wit['maximum_ranking_violation']<=1e-8,(C,val,target)
  fits.append({'target':str(target),'LP_minimum':val,'radius_error':err,'maximum_ranking_violation':wit['maximum_ranking_violation']})
 return {'P':P,'Q':Q,'restricted_matching':own[1],'unrestricted_matching':cross[1],
  'restricted_cost':own[0],'unrestricted_cost':cross[0],'lambda':lam,'mu':mu,'positive_half_widths':strings(widths),
  'upper_rectangle':{'lower':strings(l),'upper':strings(u),'beta_R':'1','shared_minimum':str(C),'witness':upper_witness},
  'lower_rectangle':{'lower':strings(lo),'upper':strings(up),'beta_R':'1','shared_minimum':'1','witness':lower_witness},
  'critical_cycles':cycles,'LP_checks':fits}

def main():
 out=HERE/'HOPPER_R13_MATCHING_RESULTS.json';assert not out.exists()
 records=[];complete6={};counts=Counter();cycle_checks=0;dual_LPs=minimum_LPs=0;maxerr=maxviolation=0.
 def case(kind,pos,R,order=None):
  nonlocal cycle_checks,dual_LPs,minimum_LPs,maxerr,maxviolation
  check=len(pos)<=6;C,selected=factor(pos,R,check);cycle_checks+=check
  n=len(pos);span=max(pos)-min(pos)+1
  assert C<=max(1,span-2)
  rec={'kind':kind,'positions':pos,'R':R,'factor':str(C),'order':order}
  if C>1:
   w=construction(pos,R,C,selected);rec['attaining_pair']=w;dual_LPs+=1;minimum_LPs+=2
   maxerr=max(maxerr,*[x['radius_error'] for x in w['LP_checks']]);maxviolation=max(maxviolation,*[x['maximum_ranking_violation'] for x in w['LP_checks']])
  records.append(rec);counts[kind]+=1
  if kind=='complete6':complete6[tuple(order)]=C
 for n in [2,3,4]:
  for R in all_orders(n):case('partial'+str(n),tuple(range(1,n+1)),R)
  print(json.dumps({'stage':'all_partial_orders','n':n,'cases':len(records)}),flush=True)
 for n in [5,6]:
  for order in permutations(range(n)):case('complete'+str(n),tuple(range(1,n+1)),tuple(combinations(order,2)),order)
  print(json.dumps({'stage':'all_complete_orders','n':n,'cases':len(records)}),flush=True)
 rng=np.random.default_rng(20261022)
 for n in [5,6,7,8]:
  for c in range(64):
   N=[n,2*n,4*n][c%3];pos=tuple(map(int,rng.choice(np.arange(1,N+1),size=n,replace=False)))
   topo=list(map(int,rng.permutation(n)));prob=[.2,.5,.8][c%3]
   R=closure(n,[e for e in combinations(topo,2) if rng.random()<prob]);case('seeded'+str(n),pos,R)
  print(json.dumps({'stage':'seeded_partial_orders','n':n,'cases':len(records)}),flush=True)
 assert len(records)==1337 and len(complete6)==720
 assert complete6[tuple(range(6))]==complete6[tuple(range(5,-1,-1))]==1
 csvpath=HERE/'HOPPER_R9_ALL_TOTAL_ORDERS.csv';data=[];maximum_excess=0.;first=None
 with csvpath.open(encoding='utf-8',newline='') as f:
  for index,row in enumerate(csv.DictReader(f)):
   order=tuple(POS[a]-1 for a in row['order'].split('<='));C=complete6[order]
   b=float(row['all_anchor_radius']);d=float(row['shared_path_radius']);excess=d-float(C)*b
   maximum_excess=max(maximum_excess,excess);assert excess<=1e-8
   if first is None and b<=math.log1p(.005)-1e-10 and d>math.log1p(.005)+1e-10:first={'csv_row_zero_based':index,'source_row':row,'factor':str(C)}
   data.append({'row':index,'factor':str(C),'numeric_bound_excess':excess})
 assert len(data)==64080 and first is not None
 result={'result':'PASS_EXACT_FIXED_RANKING_MATCHING_FACTOR_AND_POSITIVE_WIDTH_ATTAINMENT',
  'protocol_sha256':sha(HERE/'HOPPER_R13_MATCHING_PROTOCOL.json'),'argument_sha256':sha(HERE/'HOPPER_R13_MATCHING_ARGUMENT.md'),'script_sha256':sha(Path(__file__)),
  'controlled_cases':len(records),'case_counts':dict(counts),'independent_alternating_cycle_factor_checks':cycle_checks,
  'exact_integer_assignment_dual_witnesses':dual_LPs,'original_variable_minimum_LPs':minimum_LPs,
  'maximum_LP_radius_error':maxerr,'maximum_LP_ranking_violation':maxviolation,
  'six_arm_order_factor_distribution':dict(sorted(Counter(str(v) for v in complete6.values()).items())),
  'retained_input_csv_sha256':sha(csvpath),'retained_all_order_queries':len(data),'maximum_retained_numeric_bound_excess':maximum_excess,
  'printed_example_selection':first,'records':records,
  'scope':'Exact subset matching costs, independently enumerated alternating cycles, verified integer duals and rational original-variable witnesses. LP/retained CSV comparisons are numerical corroboration, not objective-gap or physical model proofs. Exponential enumeration is disclosed. No new hardware or actual archive adoption.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)

if __name__=='__main__':main()
