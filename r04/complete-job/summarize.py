"""Audit all predetermined batches and summarize complete-job costs once."""
from pathlib import Path
from collections import defaultdict
from statistics import median
import csv,hashlib,json
HERE=Path(__file__).resolve().parent
MASK=(1<<64)-1
NAMES=['raw_direct','closure_direct','cheap','quartet']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readrows(p):
 with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def stat(a):return dict(median=median(a),min=min(a),max=max(a),blocks=len(a))
def main():
 assert not(HERE/'RESULTS.json').exists()
 manifest=json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
 assert all(sha(HERE/n)==h for n,h in manifest['files'].items())
 meta=json.loads((HERE/'RUN_METADATA.json').read_text(encoding='utf-8'))
 assert meta['status']=='COMPLETE_ONCE' and sha(HERE/'complete_times.csv')==meta['raw_timing_sha256']
 plans=json.loads((HERE/'inputs.json').read_text(encoding='utf-8'))
 decisions={(int(r['plan']),int(r['rectangle']),int(r['delta'])):int(r['decision']) for r in readrows(HERE/'validation.csv')}
 assert len(decisions)==41760
 expected=defaultdict(int)
 for p in plans:
  for q in [1,48,192]:
   h=1469598103934665603
   for i in range(q):
    ri,d=p['queries'][i%48];v=decisions[(p['id'],ri,d)]
    h=((h^(v+2*ri+131*d))*1099511628211)&MASK
   k=(p['stratum'],q);expected[k]=(expected[k]+h)&MASK
 for r in readrows(HERE/'expected_batches.csv'):
  assert int(r['expected_checksum'])==expected[(int(r['stratum']),int(r['queries']))]
 rows=readrows(HERE/'complete_times.csv');schedule=json.loads((HERE/'schedule.json').read_text(encoding='utf-8'))
 assert len(rows)==len(schedule)*4==5508
 series=defaultdict(dict)
 for idx,step in enumerate(schedule):
  for position,route in enumerate(step['routes']):
   r={k:int(v) for k,v in rows[idx*4+position].items()}
   assert [r['block'],r['stratum'],r['queries'],r['position'],r['route']]==[
     step['block'],step['stratum'],step['queries'],position,route]
   assert r['elapsed_ns']>0 and r['repeats']>0
   n=sum(p['stratum']==r['stratum'] for p in plans);assert r['jobs_per_repeat']==n
   assert r['checksum']==r['expected_checksum']==(expected[(r['stratum'],r['queries'])]*r['repeats'])&MASK
   k=(r['stratum'],r['queries'],route);assert r['block'] not in series[k]
   series[k][r['block']]=r['elapsed_ns']/(r['repeats']*r['jobs_per_repeat'])
 summaries=[]
 for sid in range(51):
  sample=next(p for p in plans if p['stratum']==sid)
  for q in [1,48,192]:
   s=dict(stratum=sid,n=sample['n'],geometry=sample['geometry'],family=sample['family'],queries_per_job=q,routes={})
   for route,name in enumerate(NAMES):
    values=series[(sid,q,route)];assert set(values)==set(range(9))
    s['routes'][name]=dict(complete_job_ns=stat(list(values.values())),per_query_ns=stat([v/q for v in values.values()]))
   cheap=series[(sid,q,2)];quad=series[(sid,q,3)];raw=series[(sid,q,0)]
   s['paired_quartet_vs_cheap']=dict(faster=sum(quad[b]<cheap[b] for b in range(9)),
    slower=sum(quad[b]>cheap[b] for b in range(9)),differences_ns=stat([quad[b]-cheap[b] for b in range(9)]))
   s['paired_cheap_vs_raw']=dict(faster=sum(cheap[b]<raw[b] for b in range(9)),
    slower=sum(cheap[b]>raw[b] for b in range(9)),differences_ns=stat([cheap[b]-raw[b] for b in range(9)]))
   summaries.append(s)
 result=dict(status='PASS_ALL_5508_PREDECLARED_COMPLETE_TIMINGS_AND_OUTPUT_HASHES',plans=870,
  distinct_queries=41760,paired_blocks=9,raw_records=len(rows),expected_batches_independently_rehashed=153,
  scale='ns per complete job including fresh route-specific preparation; per-query equivalents derived by division',
  scope='One specified synthetic Boolean auditor, common preloaded inputs/scratch, parsing/validation/output I/O excluded equally. Not certificate-service timing, H20 outward audit or GPU/application speedup.',
  strata=summaries,provenance={n:sha(HERE/n) for n in ['PROTOCOL.json','INPUT_MANIFEST.json','PRE_TIMING_AUDIT.json','RUN_METADATA.json','validation.csv','expected_batches.csv','complete_times.csv','schedule.json','summarize.py']})
 (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 lines=['# Complete per-ranking job costs (local CPU)','',result['scope'],'',
  'All 870 plans and 41,760 exact decisions retained. Exactly one warmup and nine frozen paired blocks; all 5,508 records and their output hashes audited. No timing rerun.','',
  '| All720 six-arm census, queries/job | Raw direct | Closed direct | Cheap | Quartet | Quartet faster/slower than Cheap |',
  '|---:|---:|---:|---:|---:|---:|']
 for s in summaries:
  if s['stratum']!=0:continue
  values=[s['routes'][n]['complete_job_ns'] for n in NAMES]
  cols=[f"{v['median']:.1f} [{v['min']:.1f},{v['max']:.1f}]" for v in values]
  pair=s['paired_quartet_vs_cheap'];lines.append('| '+str(s['queries_per_job'])+' | '+' | '.join(cols)+f" | {pair['faster']}/{pair['slower']} |")
 lines+=['','Ranges are descriptive min/max of paired blocks, not confidence intervals. Scaling strata are retained separately in RESULTS.json, without frequency/prevalence inference.']
 (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('\n'.join(lines))
if __name__=='__main__':main()
