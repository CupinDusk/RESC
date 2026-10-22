"""Exact finite gap sanity checks and a fixed printed-endpoint two-clause audit."""
from pathlib import Path
from itertools import combinations,permutations
from fractions import Fraction as F
from decimal import Decimal,localcontext
import hashlib,json
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def logs(s):
 with localcontext() as c:
  c.prec=80;v=Decimal(s).ln();return F(v.next_minus()),F(v.next_plus())
def gap_checks():
 counts=swaps=ties=0
 for n in [4,5,6]:
  for pos in [tuple(range(1,n+1)),tuple(i*i+1 for i in range(n))]:
   for k in range(1,n//2+1):
    for P in combinations(pos,k):
     for Q in combinations([x for x in pos if x not in P],k):
      costs=[sum(abs(p-q) for p,q in zip(P,f)) for f in permutations(Q)];best=min(costs)
      ends=sorted(P+Q)
      for f in permutations(Q):
       cost=sum(abs(p-q) for p,q in zip(P,f));excess=0
       for a,b in zip(ends,ends[1:]):
        plus=sum(p<=a and q>=b for p,q in zip(P,f));minus=sum(q<=a and p>=b for p,q in zip(P,f))
        net=sum(p<=a for p in P)-sum(q<=a for q in Q);assert plus-minus==net
        excess+=2*(b-a)*min(plus,minus)
       assert cost-best==excess;counts+=1;ties+=cost==best
       for i,j in combinations(range(k),2):
        p,q=P[i],f[i];r,s=P[j],f[j]
        if (p-q)*(r-s)>=0:continue
        overlap=max(0,min(max(p,q),max(r,s))-max(min(p,q),min(r,s)))
        if not overlap:continue
        assert abs(p-q)+abs(r-s)-abs(p-s)-abs(r-q)==2*overlap;swaps+=1
 return {'matching_gap_identities':counts,'opposite_direction_swap_identities':swaps,'optimum_ties_included':ties,'slots':'consecutive and i^2+1; n4/5/6; all disjoint subsets/every matching'}
def witness(l,u,pos,R,d):
 edges=[(a,b,u[b]-l[a]+d*abs(pos[a]-pos[b])) for a in pos for b in pos if a!=b]+[(q,p,F(0)) for p,q in R]
 theta={a:F(0) for a in pos}
 for turn in range(len(pos)):
  changed=False
  for a,b,w in edges:
   if theta[b]-theta[a]>w:theta[b]=theta[a]+w;changed=True
  if not changed:break
  assert turn<len(pos)-1,'negative_cycle_at_upper_bracket'
 assert all(theta[b]-theta[a]<=w for a,b,w in edges)
 bias={j:max(l[a]-theta[a]-d*abs(j-pos[a]) for a in pos) for j in range(7)};g=bias[0]
 bias={j:x-g for j,x in bias.items()};theta={a:x+g for a,x in theta.items()};x={a:theta[a]+bias[pos[a]] for a in pos}
 assert bias[0]==0 and all(abs(bias[j]-bias[j-1])<=d for j in range(1,7))
 assert all(l[a]<=x[a]<=u[a] for a in pos) and all(theta[p]<=theta[q] for p,q in R)
 return {'b':{str(j):str(v) for j,v in bias.items()},'theta':{a:str(v) for a,v in theta.items()},'x':{a:str(v) for a,v in x.items()}}
def main():
 out=HERE/'HOPPER_R18_EXPOSITION_RESULTS.json';assert not out.exists()
 protocol=json.loads((HERE/'HOPPER_R18_EXPOSITION_PROTOCOL.json').read_text(encoding='utf-8'));assert protocol['status'].startswith('before_')
 ns={'P':('2160.0','2173.1'),'S':('2307.2','2311.8'),'B':('2788.5','2793.1'),'G':('1520.5','1522.2'),'A':('2792.6','2796.8'),'F':('2213.4','2226.4')}
 pos={'P':1,'S':2,'B':3,'G':4,'A':5,'F':6};R=[('P','F'),('A','S')]
 llo={};lhi={};ulo={};uhi={}
 for a,(l,u) in ns.items():llo[a],lhi[a]=logs(l);ulo[a],uhi[a]=logs(u)
 blo=max([F(0)]+[(llo[p]-uhi[q])/abs(pos[p]-pos[q]) for p,q in R]);bhi=max([F(0)]+[(lhi[p]-ulo[q])/abs(pos[p]-pos[q]) for p,q in R]);d=F(7,100)
 Hlo=llo['P']+llo['A']-uhi['S']-uhi['F'];Hhi=lhi['P']+lhi['A']-ulo['S']-ulo['F']
 assert bhi<d and Hlo>2*d
 lo=F((Hlo*10**12)//2,10**12)
 hi=lo+F(1,10**12);assert 2*lo<Hlo<=Hhi<2*hi
 w=witness(lhi,ulo,pos,R,hi)
 own=sum(abs(pos[p]-pos[q]) for p,q in R);free=min(sum(abs(pos[p]-pos[q]) for p,q in zip(['P','A'],qs)) for qs in permutations(['F','S']))
 assert (own,free)==(8,2)
 old=json.loads((HERE/'HOPPER_R18_AUXILIARY_EXCERPT.json').read_text(encoding='utf-8'))['cases'];aux={}
 for key in ['lexicographically_first_certified','lexicographically_first_abstained']:
  a=old[key];support=a['point_cost_ufs']-a['point_cost_ext4nj']+a['frozen_delta']*a['slot_distance'];assert abs(support-a['worst_log_ufs_over_ext4nj_cost_ratio'])<1e-12
  aux[key]={'task':a['task'],'run_num':a['fixed_run_num'],'support':support,'decision':a['certificate']}
 result={'result':'PASS_FIXED_TWO_CLAUSE_AUDIT_GAP_AND_AUXILIARY_EXPOSITION_CHECKS','protocol_sha256':sha(HERE/'HOPPER_R18_EXPOSITION_PROTOCOL.json'),'script_sha256':sha(Path(__file__)),'gap_sanity_checks':gap_checks(),'two_clause':{'R':R,'positions':pos,'declared_delta':'7/100','beta_bounds':[str(blo),str(bhi)],'beta_approx':float((blo+bhi)/2),'H_bounds':[str(Hlo),str(Hhi)],'H_approx':float((Hlo+Hhi)/2),'cycle_upper_at_delta':str(-Hlo+2*d),'cycle_upper_approx':float(-Hlo+2*d),'minimum_bracket':[str(lo),str(hi)],'minimum_bracket_approx':[float(lo),float(hi)],'restricted_cost':own,'unrestricted_cost':free,'sharp_factor':'4','box_decision':'ADMIT','shared_path_decision':'REJECT','rational_upper_original_variable_witness':w},'auxiliary_excerpt_sha256':sha(HERE/'HOPPER_R18_AUXILIARY_EXCERPT.json'),'auxiliary_arithmetic':aux,'scope':'Posthoc exposition of existing printed table and saved aggregate examples; fixed new local query and finite proof sanity checks. No new acquisition, held-out utility, physical budget, deployment or speedup evidence.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['two_clause']}));print(json.dumps({k:v for k,v in result['two_clause'].items() if k not in ['beta_bounds','H_bounds','rational_upper_original_variable_witness']}))
if __name__=='__main__':main()
