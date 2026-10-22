"""Collect one prospective complete-job timing run after validation."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, platform, subprocess, time
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
    for n in ['RUN_METADATA.json','complete_times.csv','timing-run.log']:
        assert not (HERE/n).exists(),n
    manifest=json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
    assert all(sha(HERE/n)==h for n,h in manifest['files'].items())
    validation=rows(HERE/'validation.csv')
    assert len(validation)==720
    assert all(all(r[k]==r['decision']=='1' for k in ['raw_floyd','closure_floyd','cheap','quartet']) for r in validation)
    expected=rows(HERE/'expected_batches.csv');assert len(expected)==60
    audit=dict(status='PASS_BEFORE_SINGLE_COLLECTION',distinct_queries=720,expected_batches=60,
        bindings={n:sha(HERE/n) for n in ['INPUT_MANIFEST.json','validation.csv','expected_batches.csv','core.hpp','benchmark.cpp','benchmark.exe','PROTOCOL.md','run_once.py']})
    (HERE/'PRE_TIMING_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    meta=dict(status='STARTED_ONCE',start_utc=datetime.now(timezone.utc).isoformat(),platform=platform.platform(),
        python=platform.python_version(),compiler='Zig0.14.1 C++17 -O3 -DNDEBUG -Wall -Wextra',
        cpu='Intel Core i9-14900HX; live OS inventory recorded separately',
        controls='Ordinary Windows process, no affinity/priority/power/frequency/service changes. Other agent requested to defer heavy RTL tools; normal apps/PDF reviews may remain active. No machine-idle guarantee.',
        methodology='One complete warmup, nine fixed paired shuffled blocks, every declared n/family/Q/route; fresh actual preparation, shared immutable inputs and reusable scratch capacity. Parsing/validation/file output/expected checks and outer volatile consumption excluded equally.',
        source_audit_sha256=sha(HERE/'PRE_TIMING_AUDIT.json'),scope='Designed planted exact-family synthetic jobs, not a population or physical application.')
    (HERE/'RUN_METADATA.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    begin=time.perf_counter_ns()
    with (HERE/'timing-run.log').open('w',encoding='utf-8',newline='\n') as log:
        r=subprocess.run([str(HERE/'benchmark.exe'),'time'],cwd=HERE,stdout=log,stderr=subprocess.STDOUT)
    meta.update(status='COMPLETE_ONCE' if r.returncode==0 else 'FAILED_PRESERVED_NO_RETRY',
        returncode=r.returncode,end_utc=datetime.now(timezone.utc).isoformat(),wall_elapsed_ns=time.perf_counter_ns()-begin,
        records=len(rows(HERE/'complete_times.csv')),raw_timing_sha256=sha(HERE/'complete_times.csv'),log_sha256=sha(HERE/'timing-run.log'))
    (HERE/'RUN_METADATA.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    assert r.returncode==0 and meta['records']==2160
    print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
