"""Recompute exact models and audit all recorded timings, without new timing."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,csv,gzip,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def run_script(p):
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(p)],cwd=p.parent,capture_output=True,text=True,encoding='utf-8')
 (p.parent/(p.stem+'.replay.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 assert r.returncode==0,(p.name,r.returncode,r.stdout[-3000:],r.stderr[-3000:])
 print(p.name,'PASS',flush=True)
def same(a,b,omit=()):
 assert {k:v for k,v in a.items() if k not in omit}=={k:v for k,v in b.items() if k not in omit}
def audit_roster(loc):
 plans=read(loc/'inputs.json');rows=list(csv.DictReader((loc/'validation.csv').open()))
 oracle={(int(r['plan']),int(r['rectangle']),int(r['delta'])):r for r in rows}
 assert len(rows)==len(oracle)==41760
 for p in plans:
  assert len(p['queries'])==48
  for k,(ri,d) in enumerate(p['queries']):
   r=rows[p['id']*48+k]
   assert (int(r['plan']),int(r['rectangle']),int(r['delta']))==(p['id'],ri,d)
 # Independent raw checksum audit, including the conditional stream and stages.
 m=read(loc/'INPUT_MANIFEST.json');q=list(csv.DictReader((loc/'query_times.csv').open()));pt=list(csv.DictReader((loc/'preprocess_times.csv').open()))
 expected={}
 for s in m['strata']:
  for stream in [0,1]:
   records=[oracle[i,ri,d] for i in s['plans'] for ri,d in plans[i]['queries'] if stream==0 or oracle[i,ri,d]['beta_path']!='1']
   expected[s['id'],stream]=len(records),sum(int(r['decision']) for r in records)
 for r in q:
  count,total=expected[int(r['stratum']),int(r['stream'])]
  assert int(r['queries_per_repeat'])==count and int(r['checksum'])==total*int(r['repeats'])
 prep={}
 for s in m['strata']:
  rels=cheap=exact=0
  for i in s['plans']:
   p=plans[i];n=p['n'];R=set(map(tuple,p['edges']))
   for k in range(n):R|={(a,b) for a in range(n) for b in range(n) if (a,k) in R and (k,b) in R}
   rels+=len(R);cheap+=int(rows[i*48]['cheap_exact']);exact+=int(p['quartet_exact'])
  prep[s['id']]=rels,cheap,exact
 for r in pt:assert int(r['checksum'])==prep[int(r['stratum'])][int(r['stage'])]*int(r['repeats'])
 return dict(query_timing_rows=len(q),preprocessing_timing_rows=len(pt),query_checksum_checks=len(q),preprocessing_checksum_checks=len(pt))
def main():
 p=argparse.ArgumentParser();p.add_argument('--zig',help='Existing Zig compiler; additionally rebuild and validate all C++ queries. Never times.');a=p.parse_args()
 output=HERE/'R03_REPLAY_RESULTS.json';work=HERE/'r03-replay'
 assert not output.exists() and not work.exists(),'Use a fresh extraction; preserve completed/failed replay evidence.'
 manifest=read(HERE/'MANIFEST.json')
 for name,h in manifest['files'].items():assert sha(HERE/name)==h,name
 expected=read(HERE/'r03/EXPECTED_REGENERATION.json')
 cost=work/'cost';cost.mkdir(parents=True)
 for name in ['PROTOCOL.json','PRE_TIMING_AMENDMENT.json','benchmark.cpp','generate_inputs.py','independent_check.py','summarize.py','final_audit.py','RUN_METADATA.json','validation.csv','query_times.csv','preprocess_times.csv','timing-run.log']:
  shutil.copyfile(HERE/'r03/cost'/name,cost/name)
 run_script(cost/'generate_inputs.py')
 original=HERE/'r03/cost/recorded'
 baseline=read(original/'INPUT_MANIFEST.json')
 for name,h in baseline['files'].items():assert sha(cost/name)==h,name
 assert read(cost/'INPUT_MANIFEST.json')['strata']==baseline['strata']
 native=False
 if a.zig:
  exe=cost/('benchmark.exe' if os.name=='nt' else 'benchmark')
  cmd=[str(Path(a.zig).resolve()),'c++','-std=c++17','-O3','-DNDEBUG','benchmark.cpp','-o',exe.name]
  r=subprocess.run(cmd,cwd=cost,capture_output=True,text=True,encoding='utf-8')
  (cost/'native-build.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
  r=subprocess.run([str(exe),'validate'],cwd=cost,capture_output=True,text=True,encoding='utf-8')
  (cost/'native-validation.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,(r.stdout[-2000:],r.stderr[-2000:])
  assert sha(cost/'validation.csv')==expected['cost_unmodified_files']['validation.csv']
  native=True;print('native C++ all 41760 queries PASS; no time mode invoked',flush=True)
 run_script(cost/'independent_check.py')
 independent=read(cost/'PRE_TIMING_VALIDATION.json')
 same(independent,read(original/'PRE_TIMING_VALIDATION.json'),['sha256','python'])
 assert sha(cost/'derived_survivor_streams.json')==expected['cost_unmodified_files']['derived_survivor_streams.json']
 roster=audit_roster(cost)
 run_script(cost/'summarize.py')
 same(read(cost/'RESULTS.json'),read(original/'RESULTS.json'),['sha256'])
 assert sha(cost/'RESULTS.md')==expected['cost_unmodified_files']['RESULTS.md']
 run_script(cost/'final_audit.py')
 same(read(cost/'FINAL_AUDIT.json'),read(original/'FINAL_AUDIT.json'),['files'])
 print('all recorded timing numerical summaries and negative results PASS',flush=True)
 clock=work/'clock';clock.mkdir()
 for name in ['PROTOCOL.json','NUMERIC_PROTOCOL_ADDENDUM.json','check_clock_contract.py']:
  shutil.copyfile(HERE/'r03/clock'/name,clock/name)
 (clock/'independent').mkdir()
 shutil.copyfile(HERE/'r03/clock/independent/validate_clock_independently.py',clock/'independent/validate_clock_independently.py')
 run_script(clock/'check_clock_contract.py')
 same(read(clock/'RESULTS.json'),read(HERE/'r03/clock/recorded/RESULTS.json'),['provenance'])
 assert read(clock/'OBSERVATIONS.json')==read(HERE/'r03/clock/recorded/OBSERVATIONS.json')
 records=gzip.decompress((clock/'ALL_REPORTS.jsonl.gz').read_bytes())
 assert hashlib.sha256(records).hexdigest()==expected['clock_report_uncompressed_sha256']
 assert len(records.splitlines())==expected['clock_report_records']
 run_script(clock/'independent/validate_clock_independently.py')
 independent_clock=read(clock/'independent/VALIDATION.json')
 assert independent_clock['status']=='PASS' and not independent_clock['failures']
 same(independent_clock,read(HERE/'r03/clock/recorded/INDEPENDENT_VALIDATION.json'),['input_sha256','validator_sha256','python'])
 result=dict(status='PASS_FRESH_EXTRACTION_NEW_CORE_CHECKS_AND_RECORDED_TIMING_AUDIT',input_manifest_sha256=sha(HERE/'MANIFEST.json'),cost=dict(plans=870,finite_queries=41760,fresh_native_all_query_validation=native,python_independent_queries=independent['python_n_le_8_queries'],python_original_variable_witnesses=independent['python_feasible_original_variable_witnesses'],recorded_events=roster,all_numerical_summaries_equal=True,timing_rerun=False),clock=dict(reports=5768,uncompressed_reports_sha256=hashlib.sha256(records).hexdigest(),independent_checks=independent_clock['checks'],all_summaries_equal=True),prior_suite_rerun=False,scope='Exact stipulated clock and synthetic CPU graph calculations only. No physical experiment, GPU claim, new timing, or rerun of the unchanged older scipy-dependent suite. Optional native compile/validate regenerates correctness outcomes, not timing measurements.')
 output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
