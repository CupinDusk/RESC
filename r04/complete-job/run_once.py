"""Audit frozen inputs/old decisions, then collect exactly one scheduled run."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,platform,subprocess,time
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'r03-analysis/hopper-cost'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
  with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
  for name in ['RUN_METADATA.json','complete_times.csv','timing-run.log']:
    assert not(HERE/name).exists(),name
  manifest=json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
  assert all(sha(HERE/name)==h for name,h in manifest['files'].items())
  old=rows(OLD/'validation.csv');new=rows(HERE/'validation.csv')
  def key(r):return tuple(int(r[n]) for n in ['plan','rectangle','delta'])
  a={key(r):int(r['decision']) for r in old};b={key(r):int(r['decision']) for r in new}
  assert len(old)==len(new)==len(a)==41760 and a==b
  assert all(all(r[k]==r['decision'] for k in ['raw_floyd','closure_floyd','cheap','quartet']) for r in new)
  audit=dict(status='PASS_BEFORE_TIMING',queries=41760,all_previous_decisions_preserved=True,
    original_validation_sha256=sha(OLD/'validation.csv'),new_validation_sha256=sha(HERE/'validation.csv'),
    expected_batches_sha256=sha(HERE/'expected_batches.csv'),input_manifest_sha256=sha(HERE/'INPUT_MANIFEST.json'),
    benchmark_source_sha256=sha(HERE/'benchmark.cpp'),core_sha256=sha(HERE/'core.hpp'),
    executable_sha256=sha(HERE/'benchmark.exe'),protocol_sha256=sha(HERE/'PROTOCOL.json'))
  (HERE/'PRE_TIMING_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
  metadata=dict(status='STARTED_ONCE',start_utc=datetime.now(timezone.utc).isoformat(),
    platform=platform.platform(),python=platform.python_version(),compiler='Zig0.14.1 Clang19.1.7 C++17 -O3 -DNDEBUG -Wall -Wextra',
    command=['benchmark.exe','time'],cpu='Intel Core i9-14900HX (previously verified on this same host)',
    controls='No affinity, priority, power, frequency, service or remote changes; one ordinary Windows process.',
    methodology='Exactly one complete untimed warmup; nine predeclared paired blocks, fresh route-specific ranking setup per job. Preloaded immutable inputs/common scratch capacity; parsing/validation/file writing excluded equally. Boolean decision hashes consumed; not certificate-service timing.',
    pre_timing_audit_sha256=sha(HERE/'PRE_TIMING_AUDIT.json'))
  (HERE/'RUN_METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
  start=time.perf_counter_ns()
  with(HERE/'timing-run.log').open('w',encoding='utf-8',newline='\n') as log:
    result=subprocess.run([str(HERE/'benchmark.exe'),'time'],cwd=HERE,stdout=log,stderr=subprocess.STDOUT,check=False)
  metadata.update(status='COMPLETE_ONCE' if result.returncode==0 else 'FAILED_PRESERVED_NO_RETRY',
    returncode=result.returncode,end_utc=datetime.now(timezone.utc).isoformat(),wall_elapsed_ns=time.perf_counter_ns()-start,
    complete_records=len(rows(HERE/'complete_times.csv')),
    raw_timing_sha256=sha(HERE/'complete_times.csv'),log_sha256=sha(HERE/'timing-run.log'))
  (HERE/'RUN_METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
  assert result.returncode==0 and metadata['complete_records']==9*51*3*4
  print(json.dumps(metadata,indent=2))
if __name__=='__main__':main()
