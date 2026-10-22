"""Freeze exact original inputs, derived own-research core and paired schedule."""
from pathlib import Path
import hashlib,json,random,shutil
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'r03-analysis/hopper-cost'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
  assert not (HERE/'INPUT_MANIFEST.json').exists()
  for name in ['inputs.txt','inputs.json']:
    assert not (HERE/name).exists();shutil.copyfile(OLD/name,HERE/name)
  original=(OLD/'benchmark.cpp').read_text(encoding='utf-8')
  core=original.split('int main(int argc,char**argv)')[0]
  a='if(p.R[b*n+a]&&w>0)w=0;'
  b='if(!p.R.empty()&&p.R[b*n+a]&&w>0)w=0;'
  assert core.count(a)==1;core=core.replace(a,b)
  a='s.w[a*n+b]=w;}}\nbool bf'
  b='s.w[a*n+b]=w;}if(p.R.empty())for(auto[a,b]:p.edges)s.w[b*n+a]=std::min<I>(s.w[b*n+a],0);}\nbool bf'
  assert core.count(a)==1;core=core.replace(a,b)
  (HERE/'core.hpp').write_text(core,encoding='utf-8')
  plans=json.loads((HERE/'inputs.json').read_text(encoding='utf-8'))
  assert len(plans)==870 and sum(len(p['queries']) for p in plans)==41760
  strata=sorted({p['stratum'] for p in plans});assert strata==list(range(51))
  rng=random.Random(20261024);schedule=[]
  for block in range(9):
    for sid in strata:
      qs=[1,48,192];rng.shuffle(qs)
      for q in qs:
        routes=list(range(4));rng.shuffle(routes)
        schedule.append(dict(block=block,stratum=sid,queries=q,routes=routes))
  (HERE/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n',encoding='utf-8')
  (HERE/'schedule.txt').write_text(str(len(schedule))+'\n'+''.join(
    ' '.join(map(str,[r['block'],r['stratum'],r['queries'],*r['routes']]))+'\n' for r in schedule),encoding='utf-8')
  manifest=dict(status='FROZEN_BEFORE_NATIVE_VALIDATION_AND_TIMING',
    original_binding={n:sha(OLD/n) for n in ['inputs.txt','inputs.json','benchmark.cpp']},
    plans=870,distinct_queries=41760,strata=51,paired_blocks=9,
    core_changes=['Remove original main; retain own research query/closure/flag/BF/Floyd functions.',
      'An empty ranking-closure payload means use only original reverse ranking edges in the complete data graph. This is solely the raw-direct baseline; routed plans still close first.'],
    files={n:sha(HERE/n) for n in ['PROTOCOL.json','inputs.txt','inputs.json','core.hpp','schedule.json','schedule.txt','benchmark.cpp','prepare.py']})
  (HERE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
  print(json.dumps({k:v for k,v in manifest.items() if k not in ['files','original_binding','core_changes']}))
if __name__=='__main__':main()
