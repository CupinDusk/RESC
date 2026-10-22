"""Freeze exact synthetic census and block schedules before native timing."""
from pathlib import Path
from itertools import combinations, permutations
import hashlib,json,random,platform
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def closure(n,edges):
 r=[[False]*n for _ in range(n)]
 for p,q in edges:r[p][q]=True
 for k in range(n):
  for i in range(n):
   if r[i][k]:
    for j in range(n):r[i][j]|=r[k][j]
 assert not any(r[i][i] for i in range(n))
 return r
def classify(pos,r):
 for four in combinations(range(len(pos)),4):
  for P in combinations(four,2):
   Q=tuple(x for x in four if x not in P)
   a,b=P;c,d=Q
   cost1=abs(pos[a]-pos[c])+abs(pos[b]-pos[d]);cost2=abs(pos[a]-pos[d])+abs(pos[b]-pos[c])
   ok1=r[a][c] and r[b][d];ok2=r[a][d] and r[b][c]
   if (ok1 or ok2) and min([cost1 if ok1 else 10**9,cost2 if ok2 else 10**9])>min(cost1,cost2):return False,(P,Q,max(cost1,cost2))
 return True,None
def rectangles(pos,r,seed,order):
 n=len(pos);rng=random.Random(seed);out=[([0]*n,[0]*n),([-1]*n,[1]*n)]
 for width in (0,2,16):
  c=[rng.randint(-32,32) for _ in range(n)];out.append(([x-width for x in c],[x+width for x in c]))
 b=[0]
 for j in range(1,max(pos)+1):b.append(b[-1]+rng.randint(-4,4))
 rank={v:k for k,v in enumerate(order)};c=[2*rank[i]+b[pos[i]] for i in range(n)]
 out.append(([x-1 for x in c],[x+1 for x in c]))
 c=[rng.randint(-32,32) for _ in range(n)];w=[rng.randint(0,8) for _ in range(n)];out.append(([x-y for x,y in zip(c,w)],[x+y for x,y in zip(c,w)]))
 exact,bad=classify(pos,r);M=4*(max(pos)-min(pos)+1)+100
 lo=[-M]*n;hi=[M]*n
 if bad:
  P,Q,target=bad;best=None;span=max(pos)-min(pos)
  for t in range(-2*span,2*span+1):
   mu={Q[0]:0,Q[1]:t};lam={p:min(abs(pos[p]-pos[q])+mu[q] for q in Q if r[p][q]) for p in P}
   value=sum(lam.values())-sum(mu.values())
   if best is None or value>best[0]:best=(value,lam,mu)
  assert best[0]==target
  for p,v in best[1].items():lo[p]=v
  for q,v in best[2].items():hi[q]=v
 out.append((lo,hi));assert len(out)==8 and all(all(a<=b for a,b in zip(l,u)) for l,u in out)
 return out,exact,bad
def main():
 assert not (HERE/'INPUT_MANIFEST.json').exists()
 plans=[];strata=[]
 def add_group(n,geo,family,seeds,orders=None):
  sid=len(strata);ids=[];pos=list(range(1,n+1)) if geo=='contiguous' else [1+3*i+i%3 for i in range(n)]
  for index,seed in enumerate(seeds):
   rng=random.Random(seed);order=list(range(n))
   if orders is not None:order=list(orders[index]);edges=list(combinations(order,2))
   elif family=='aligned':edges=list(combinations(order,2))
   elif family=='reverse':order.reverse();edges=list(combinations(order,2))
   elif family=='winner_star':rng.shuffle(order);edges=[(order[0],q) for q in order[1:]]
   elif family=='mixed_total':rng.shuffle(order);edges=list(combinations(order,2))
   elif family=='sparse_dag':rng.shuffle(order);edges=[(p,q) for p,q in combinations(order,2) if rng.random()<min(.25,2/n)]
   else:raise ValueError(family)
   r=closure(n,edges);rects,exact,bad=rectangles(pos,r,seed+100000+index,order)
   query=list((ri,d) for ri in range(8) for d in [0,1,2,4,16,64]);random.Random(seed+200000+index).shuffle(query)
   rec={'id':len(plans),'stratum':sid,'n':n,'geometry':geo,'family':family,'seed':seed,'slots':pos,'edges':edges,'rectangles':rects,'queries':query,'quartet_exact':exact,'bad_quartet':bad}
   ids.append(rec['id']);plans.append(rec)
  reps=1 if family=='all720' else {4:100,8:100,16:20,32:5,64:2}[n]
  strata.append({'id':sid,'n':n,'geometry':geo,'family':family,'plans':ids,'query_repeats':reps})
 orders=list(permutations(range(6)));add_group(6,'contiguous','all720',[20261023]*720,orders)
 for n in [4,8,16,32,64]:
  for geo in ['contiguous','sparse']:
   for family in ['aligned','reverse','winner_star','mixed_total','sparse_dag']:add_group(n,geo,family,[20261023,20261024,20261025])
 assert len(plans)==870 and len(strata)==51 and sum(p['quartet_exact'] for p in plans[:720])==40
 (HERE/'inputs.json').write_text(json.dumps(plans,separators=(',',':'))+'\n',encoding='utf-8')
 with (HERE/'inputs.txt').open('w',encoding='ascii') as f:
  f.write(f'{len(plans)} {len(strata)}\n')
  for p in plans:
   f.write(f"{p['id']} {p['stratum']} {p['n']} {len(p['edges'])} {int(p['quartet_exact'])}\n")
   f.write(' '.join(map(str,p['slots']))+'\n')
   for a,b in p['edges']:f.write(f'{a} {b}\n')
   for l,u in p['rectangles']:f.write(' '.join(map(str,l))+'\n'+' '.join(map(str,u))+'\n')
   for ri,d in p['queries']:f.write(f'{ri} {d}\n')
  for s in strata:f.write(f"{s['id']} {s['query_repeats']} {len(s['plans'])} "+' '.join(map(str,s['plans']))+'\n')
 rng=random.Random(20261023);schedule=[]
 for block in range(9):
  order=list(range(len(strata)));rng.shuffle(order)
  for sid in order:
   routes=list(range(4));rng.shuffle(routes);prep=list(range(3));rng.shuffle(prep)
   schedule.append({'block':block,'stratum':sid,'routes':routes,'preprocess':prep})
 (HERE/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n',encoding='utf-8')
 with (HERE/'schedule.txt').open('w',encoding='ascii') as f:
  f.write(f'{len(schedule)}\n')
  for s in schedule:f.write(' '.join(map(str,[s['block'],s['stratum']]+s['routes']+s['preprocess']))+'\n')
 manifest={'status':'INPUTS_AND_REALIZED_SCHEDULE_FROZEN_BEFORE_NATIVE_VALIDATION_OR_TIMING','plans':len(plans),'queries':sum(len(p['queries']) for p in plans),'strata':strata,'quartet_exact_plans':sum(p['quartet_exact'] for p in plans),'python':platform.python_version(),'files':{name:sha(HERE/name) for name in ['PROTOCOL.json','generate_inputs.py','inputs.json','inputs.txt','schedule.json','schedule.txt']}}
 (HERE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in manifest.items() if k!='strata'}))
if __name__=='__main__':main()
