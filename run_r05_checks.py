"""Full saved-evidence replay; optional actual native correctness; never retimes."""
from pathlib import Path
import argparse,gzip,hashlib,json,os,runpy,shutil,subprocess,sys,traceback
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
commands=[]
def run(argv,cwd,label,expected=0):
 assert not any(str(x)=='time' for x in argv),'Performance mode prohibited'
 r=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 (cwd/(label+'.stdout.log')).write_text(r.stdout,encoding='utf-8');(cwd/(label+'.stderr.log')).write_text(r.stderr,encoding='utf-8')
 commands.append(dict(label=label,argv=[str(x) for x in argv],returncode=r.returncode))
 assert r.returncode==expected,(label,r.returncode,r.stdout[-2000:],r.stderr[-2000:])
 print(label,'PASS',flush=True)
def py(p,args=()):return [sys.executable,'-I','-S','-B','-X','utf8',str(p),*args]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--zig');ap.add_argument('--yosys',default='yosys');ap.add_argument('--yosys-python-wrapper');ap.add_argument('--include');a=ap.parse_args()
 native=bool(a.zig);assert not native or a.include
 work=HERE/'r05-replay';assert not work.exists(),'Use a fresh extraction; preserve previous attempts.'
 m=read(HERE/'MANIFEST.json')
 assert all(sha(HERE/n)==h for n,h in m['files'].items())
 base=read(HERE/'r05/BASE_BINDING.json');assert len(base['preserved_nonroot_files'])==187
 assert all(sha(HERE/n)==h for n,h in base['preserved_nonroot_files'].items())
 work.mkdir();shutil.copytree(HERE/'r05',work/'r05');shutil.copytree(HERE/'r04',work/'r04')
 provenance=read(HERE/'r05/PORTABILITY_CHANGES.json')
 compressed=[]
 for item in provenance['changes']:
  if not item['file'].endswith('TICKS_RLE.csv.gz'):continue
  p=work/item['file'];raw=gzip.decompress(p.read_bytes());assert len(raw)==item['expanded_bytes'] and hashlib.sha256(raw).hexdigest()==item['original_sha256']
  p.with_suffix('').write_bytes(raw);compressed.append(dict(file=item['file'],expanded_bytes=len(raw),expanded_sha256=hashlib.sha256(raw).hexdigest()))
 for item in provenance['byte_exact_deduplication']:
  if item['path'].startswith('r05/exact-family/independent/generator-replay/'):continue
  p=work/item['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/item['canonical'],p);assert sha(p)==item['sha256']
 rtl=work/'r05/rtl';cost=work/'r05/exact-family';producer=rtl/'attempt-002';fresh=rtl/'independent/fresh-replay'
 for n in ['validation.csv','expected_batches.csv','routing_census.csv']:shutil.copyfile(cost/n,cost/'independent'/n)
 # Save producer/fresh gzip nonidentity while restoring all identical streams.
 for n in ['TICKS_RLE.csv','SCENARIOS.csv','JOBS.csv','INVALID_CONTROLS.csv','RTL_RESULTS.json','AUDITOR_INPUTS.json','OBSERVATIONS.json','netlist.cpp']:
  if not (fresh/n).exists():shutil.copyfile(producer/n,fresh/n)
 (fresh/'vectors').mkdir(exist_ok=True)
 for p in (producer/'vectors').iterdir():
  if p.is_file() and not(fresh/'vectors'/p.name).exists():shutil.copyfile(p,fresh/'vectors'/p.name)
 native_report=dict(executed=False,historical_pe_binding_freshly_rechecked=False,timing_rerun=False)
 if native:
  actual=rtl/'independent/fresh-actual';args=['--out',str(actual),'--cxx',str(Path(a.zig).resolve()),'--zig','--include',str(Path(a.include).resolve())]
  args+=['--yosys-python-wrapper',str(Path(a.yosys_python_wrapper).resolve())] if a.yosys_python_wrapper else ['--yosys',a.yosys]
  run(py(rtl/'replay_portable.py',args),rtl,'actual-rtl')
  identical=[]
  for n in ['netlist.cpp','TICKS_RLE.csv','SCENARIOS.csv','JOBS.csv','INVALID_CONTROLS.csv','RTL_RESULTS.json','AUDITOR_INPUTS.json','OBSERVATIONS.json','vectors/INPUTS.json','vectors/vectors.txt']:
   assert (producer/n).read_bytes()==(actual/n).read_bytes(),n;identical.append(dict(file=n,sha256=sha(actual/n)))
  pa=(producer/'ALL_REPORTS.jsonl.gz').read_bytes();fa=(actual/'ALL_REPORTS.jsonl.gz').read_bytes();assert gzip.decompress(pa)==gzip.decompress(fa)
  ar=read(actual/'AUDIT_RESULTS.json');pr=read(producer/'AUDIT_RESULTS.json');assert {k:v for k,v in ar.items() if k!='bindings'}=={k:v for k,v in pr.items() if k!='bindings'}
  for n in ['ALL_REPORTS.jsonl.gz','AUDIT_RESULTS.json']:shutil.copyfile(actual/n,fresh/n)
  zig=str(Path(a.zig).resolve());ind=rtl/'independent'
  run([zig,'c++','-std=c++17','-O3','-UNDEBUG',ind/'edge_oracle.cpp','-o',ind/'edge_oracle.exe'],ind,'compile-edge-oracle')
  for label,folder in [('producer',producer),('fresh',actual)]:
   run([ind/'edge_oracle.exe',folder,ind/(label+'-FRESH_EDGE_CHECK.json')],ind,label+'-all-edges')
   assert read(ind/(label+'-FRESH_EDGE_CHECK.json'))==read(ind/'PRODUCER_EDGE_CHECK.json')
  y=[sys.executable,'-B','-X','utf8',str(Path(a.yosys_python_wrapper).resolve())] if a.yosys_python_wrapper else [a.yosys]
  inc=Path(a.include).resolve();mutants=[]
  for folder in sorted((ind/'mutants').iterdir()):
   if not folder.is_dir():continue
   d=ind/('fresh-mutant-'+folder.name);d.mkdir()
   for n in ['reference.v','mutant_harness.cpp','edge_oracle.cpp']:shutil.copyfile(folder/n,d/n)
   run(y+['-p','read_verilog reference.v; hierarchy -check -top reference_job; prep -top reference_job; check -assert; write_cxxrtl netlist.cpp'],d,'synthesis')
   run([zig,'c++','-std=c++17','-O3','-UNDEBUG','-I',inc,'-I',inc/'backends/cxxrtl/runtime','mutant_harness.cpp','-o','check.exe'],d,'compile')
   run([d/'check.exe'],d,'execute',0 if folder.name=='baseline' else 1);mutants.append(folder.name)
  assert len(mutants)==6
  cpp=cost/'fresh-native';cpp.mkdir()
  for n in ['core.hpp','benchmark.cpp','census.cpp','inputs.txt','schedule.txt']:shutil.copyfile(cost/n,cpp/n)
  for n in ['benchmark','census']:run([zig,'c++','-O3','-DNDEBUG','-std=c++17','-Wall','-Wextra',n+'.cpp','-o',n+'.exe'],cpp,'compile-'+n)
  run([cpp/'benchmark.exe','validate'],cpp,'validate-720');run([cpp/'census.exe'],cpp,'census-720')
  for n in ['validation.csv','expected_batches.csv','routing_census.csv']:assert (cpp/n).read_bytes()==(cost/n).read_bytes(),n
  native_report=dict(executed=True,reference_edges_per_trace=389022846,independent_all_edge_traces=2,mutant_baseline_and_five_semantic_mutants=mutants,all_720_cpu_queries_and_60_hashes_byte_exact=True,stream_byte_comparisons=identical,gzip=dict(producer_sha256=hashlib.sha256(pa).hexdigest(),fresh_sha256=hashlib.sha256(fa).hexdigest(),archive_byte_equal=pa==fa,expanded_byte_equal=True,expanded_sha256=hashlib.sha256(gzip.decompress(pa)).hexdigest()),historical_pe_binding_freshly_rechecked=False,timing_rerun=False)
 run(py(rtl/'independent/check_portable.py'),rtl/'independent','independent-rtl-graph')
 graph=read(rtl/'independent/GRAPH_AND_FRAMING_CHECK.json');saved=read(HERE/'r05/rtl/independent/GRAPH_AND_FRAMING_CHECK.json')
 for k in ['framing','queries','certificates','totals','per_case','per_vector_total','per_vector_partial','changed_partial_case_ids']:assert graph[k]==saved[k],k
 run(py(cost/'independent/check_portable.py'),cost/'independent','independent-cpu')
 facts=read(cost/'independent/PAPER_READY_FACTS.json');assert facts==read(HERE/'r05/exact-family/independent/PAPER_READY_FACTS.json')
 for n in ['ALL_STRATA.json','ALL_STRATA.csv','CROSSOVERS.json','GRAPH_CERTIFICATES.json','ASSIGNMENT_CHECKS.json']:assert sha(cost/'independent'/n)==sha(HERE/'r05/exact-family/independent'/n),n
 # Run inherited driver in-process so every Python child receives isolation.
 original_run=subprocess.run
 def isolated_run(argv,*args,**kwargs):
  if Path(argv[0]).resolve()==Path(sys.executable).resolve() and '-I' not in argv:argv=[argv[0],'-I','-S',*argv[1:]]
  return original_run(argv,*args,**kwargs)
 subprocess.run=isolated_run;sys.argv=[str(HERE/'run_r04_checks.py')]
 try:runpy.run_path(str(HERE/'run_r04_checks.py'),run_name='__main__')
 finally:subprocess.run=original_run
 prior=read(HERE/'R04_REPLAY_RESULTS.json');assert prior['complete_job']['raw_timing_records']==5508 and not prior['complete_job']['timing_rerun']
 result=dict(status='PASS_FRESH_R05_COMPLETE_SAVED_EVIDENCE_AND_R04_STDLIB',input_files=len(m['files']),all_prior_nonroot_files_exact=187,compressed_streams=compressed,rtl_queries=graph['queries'],rtl_framing=graph['framing'],cpu_distinct_queries=720,cpu_raw_timing_rows=2160,all_scientific_facts_exact=True,native=native_report,old_raw_timing_rows=5508,new_timing_runs=0,root_python_isolated=sys.flags.isolated,root_python_no_site=sys.flags.no_site,python_checker_children_isolated_no_site=True,legacy_scope='Full inherited R04 stdlib runner; older SciPy suite not rerun.',commands=commands)
 save(HERE/'R05_REPLAY_RESULTS.json',result);print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as error:
  p=HERE/'R05_FAILURE_PRESERVED.json'
  if not p.exists():save(p,dict(error=repr(error),traceback=traceback.format_exc(),commands=commands,new_timing_runs=0))
  raise
