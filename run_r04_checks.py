"""Fresh-extraction R04 exact evidence replay; standard library; never retimes."""
from pathlib import Path
import argparse,gzip,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def same(a,b,omit=()):
 assert {k:v for k,v in a.items() if k not in omit}=={k:v for k,v in b.items() if k not in omit}
def run(p,args=()):
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(p),*args],cwd=p.parent,capture_output=True,text=True,encoding='utf-8')
 (p.parent/(p.stem+'.replay.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 assert r.returncode==0,(p,r.returncode,r.stdout[-2000:],r.stderr[-2000:])
 print(p.name,'PASS',flush=True)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--zig',help='Existing compiler; correctness rebuild only, no timings.');args=parser.parse_args()
 work=HERE/'r04-replay';out=HERE/'R04_REPLAY_RESULTS.json'
 assert not work.exists() and not out.exists(),'Use a fresh extraction; preserve prior completed/failed attempts.'
 manifest=read(HERE/'MANIFEST.json')
 for name,h in manifest['files'].items():assert sha(HERE/name)==h,name
 expected=read(HERE/'r04/EXPECTED_REGENERATION.json')
 work.mkdir();shutil.copytree(HERE/'r03',work/'r03')
 clock=work/'r04/changing-clock';shutil.copytree(HERE/'r04/changing-clock',clock)
 for name in ['OBSERVATIONS.json','RESULTS.json','ALL_REPORTS.jsonl.gz']:(clock/name).unlink()
 run(clock/'build_and_check.py')
 original=HERE/'r04/changing-clock'
 same(read(clock/'RESULTS.json'),read(original/'RESULTS.json'),['provenance'])
 assert sha(clock/'OBSERVATIONS.json')==sha(original/'OBSERVATIONS.json')
 raw=gzip.decompress((clock/'ALL_REPORTS.jsonl.gz').read_bytes())
 assert raw==gzip.decompress((original/'ALL_REPORTS.jsonl.gz').read_bytes())
 assert hashlib.sha256(raw).hexdigest()==expected['clock_uncompressed_sha256'] and len(raw.splitlines())==17304
 # Check the serialized public evidence independently, rather than substituting
 # regenerated gzip-header hashes into the retained original result claims.
 shutil.copyfile(original/'RESULTS.json',clock/'RESULTS.json')
 shutil.copyfile(original/'ALL_REPORTS.jsonl.gz',clock/'ALL_REPORTS.jsonl.gz')
 run(clock/'independent/replay_changing_clock.py',['--output','FRESH_VALIDATION.json'])
 validation=read(clock/'independent/FRESH_VALIDATION.json')
 assert validation['status']=='PASS' and not validation['failures']
 same(validation,read(original/'independent/VALIDATION.json'),['validator_sha256','python'])
 job=work/'r04/complete-job';shutil.copytree(HERE/'r04/complete-job',job)
 # Public portable source preparation is exercised separately; historical files
 # remain fixed and feed the original pre-timing/input binding checks.
 prep=work/'r04/preparation';prep.mkdir()
 for n in ['prepare.py','PROTOCOL.json','benchmark.cpp']:shutil.copyfile(job/n,prep/n)
 text=(prep/'prepare.py').read_text().replace("HERE.parents[1]/'r03-analysis/hopper-cost'","HERE.parents[1]/'r03/cost'")
 (prep/'prepare.py').write_text(text,encoding='utf-8')
 run(prep/'prepare.py')
 for n in ['inputs.json','inputs.txt','core.hpp','schedule.json','schedule.txt']:assert sha(prep/n)==sha(job/n),n
 run(job/'independent/replay_complete.py',['--zig',str(Path(args.zig).resolve())] if args.zig else [])
 audit=read(job/'independent/INDEPENDENT_AUDIT.json')
 saved=read(HERE/'r04/complete-job/independent/INDEPENDENT_AUDIT.json')
 for n in ['census','strata','input_bounds','reporting_correction','timing_log_audit']:
  assert audit[n]==saved[n],n
 assert audit['raw_records_audited']==5508 and audit['distinct_queries']==41760 and audit['new_timing_runs']==0
 (job/'RESULTS.json').unlink();(job/'RESULTS.md').unlink()
 run(job/'summarize.py')
 same(read(job/'RESULTS.json'),read(HERE/'r04/complete-job/RESULTS.json'))
 assert sha(job/'RESULTS.md')==sha(HERE/'r04/complete-job/RESULTS.md')
 result=dict(status='PASS_FRESH_EXTRACTION_R04_SAVED_EVIDENCE_AND_CLOCK_REGENERATION',input_manifest_sha256=sha(HERE/'MANIFEST.json'),clock=dict(reports=17304,positive_certificates=6360,negative_certificates=10944,separate_contract_unknown=5768,log_bounds=289,uncompressed_report_sha256=hashlib.sha256(raw).hexdigest(),independent_status=validation['status'],checks=validation['checks']),complete_job=dict(plans=870,distinct_queries=41760,raw_timing_records=5508,scaling_strata=50,all_summary_values_equal=True,all_seed_order_and_hash_checks=True,fresh_native_all_query_validation=bool(args.zig),historical_pe_binding_freshly_rechecked=False,timing_rerun=False),prior_suite_rerun=False,scope='Exact specified clock and recorded synthetic CPU job evidence. Default audits retained independent graph CSV; optional existing compiler freshly rebuilds both all-query correctness paths. No new timings, GPU/RTL/physical acquisition, or prior SciPy suite run.')
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
