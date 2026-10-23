"""Verify the complete portable tree and replay saved research without timing."""
from pathlib import Path
import argparse,gzip,hashlib,importlib.util,json,shutil,sys
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 m=json.loads((HERE/'MANIFEST.json').read_text());actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p!=HERE/'MANIFEST.json'}
 assert actual==set(m['files'])
 for n,h in m['files'].items():assert sha(HERE/n)==h,n
 result=dict(manifest_files=len(actual),manifest_verified=True,new_performance_runs=0)
 if m['paper']=='hush':
  p=HERE/'r06/calendar';sys.path.insert(0,str(p))
  spec=importlib.util.spec_from_file_location('calendar_study',p/'study.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  mod.run(out)
  for file in (p/'attempt-002/records').iterdir():assert sha(file)==sha(out/'records'/file.name)
  for n in ['COMPLETE_RECORD_BYTES.json','OPTIMA_ALL_TIES.json','WORKED_CHANGED_PERIOD.json','TRUSTED_EXPECTED_REGISTRY.json']:
   assert json.loads((out/n).read_text())==json.loads((p/'attempt-002'/n).read_text()),n
  result.update(records_rebuilt_byte_exact=72,observer_optima_and_ties_exact=True)
 else:
  p=HERE/'r06/picorv32';b=json.loads((p/'PORTABLE_MANIFEST.json').read_text())
  # Top manifest already verifies every complete payload. Explicitly validate
  # the independently reported saved totals and timing row hashes as well.
  gate=json.loads((HERE/'r06/independent-source/SCOPE_GATE.json').read_text());assert gate['status'].startswith('PASS')
  s=HERE/'r06/specialized';summary=json.loads((s/'SUMMARY.json').read_text());assert summary['raw_records']==3240 and summary['raw_sha256']==sha(s/'complete_times.csv')
  result.update(exact_saved_picorv32_payload=True,independent_native_scope_gate_recorded=True,specialized_timing_rows_hash_bound=3240,limitation='This saved-evidence/manifest run does not rerun native RTL; actual fresh independent native execution is separately recorded for identical payload.')
 (out/'R06_REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
