"""Separate Python-integer implementation, no native decision functions."""
from pathlib import Path
import csv,json,hashlib,platform
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plans=json.loads((HERE/'inputs.json').read_text());oracle={(int(r['plan']),int(r['rectangle']),int(r['delta'])):r for r in csv.DictReader((HERE/'validation.csv').open())}
 checked=0;feasible=0;stream={}
 for p in plans:
  n=p['n'];R=set(map(tuple,p['edges']))
  for k in range(n):R|={(a,b) for a in range(n) for b in range(n) if (a,k) in R and (k,b) in R}
  survivors=[]
  for ri,d in p['queries']:
   r=oracle[p['id'],ri,d]
   if r['beta_path']!='1':survivors.append([ri,d])
   if n>8:continue
   l,u=p['rectangles'][ri];pos=p['slots'];edges=[(a,b,u[b]-l[a]+d*abs(pos[a]-pos[b])) for a in range(n) for b in range(n) if a!=b]+[(b,a,0) for a,b in R]
   theta=[0]*n;ok=False
   for turn in range(n):
    changed=False
    for a,b,w in edges:
     if theta[b]>theta[a]+w:theta[b]=theta[a]+w;changed=True
    if not changed:ok=True;break
   assert int(ok)==int(r['decision']),(p['id'],ri,d)
   if ok:
    b=[max(l[a]-theta[a]-d*abs(j-pos[a]) for a in range(n)) for j in range(max(pos)+1)]
    assert all(abs(b[j]-b[j-1])<=d for j in range(1,len(b)))
    assert all(l[a]<=theta[a]+b[pos[a]]<=u[a] for a in range(n))
    assert all(theta[a]<=theta[c] for a,c in R)
    feasible+=1
   checked+=1
  stream[str(p['id'])]=survivors
 (HERE/'derived_survivor_streams.json').write_text(json.dumps(stream,separators=(',',':'))+'\n')
 result={'status':'PASS_INDEPENDENT_PYTHON_INTEGER_ORIGINAL_VARIABLE_WITNESSES_AND_GRAPH_DECISIONS','native_all_query_validation':41760,'python_n_le_8_queries':checked,'python_feasible_original_variable_witnesses':feasible,'survivor_queries':sum(map(len,stream.values())),'python':platform.python_version(),'sha256':{name:sha(HERE/name) for name in ['PROTOCOL.json','PRE_TIMING_AMENDMENT.json','INPUT_MANIFEST.json','inputs.txt','schedule.txt','benchmark.cpp','benchmark.exe','validation.csv','independent_check.py','derived_survivor_streams.json'] if (HERE/name).is_file()}}
 (HERE/'PRE_TIMING_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
