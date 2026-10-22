"""Bind final audit files and verify producer evidence has not changed."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((HERE/'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
assert all(sha(BASE/n)==h for n,h in source['files'].items())
old=BASE.parents[1]/'r04-analysis/hopper-end-to-end'
assert all(sha(old/n)==h for n,h in source['baseline'].items())
audit=json.loads((HERE/'INDEPENDENT_AUDIT.json').read_text(encoding='utf-8'))
facts=json.loads((HERE/'PAPER_READY_FACTS.json').read_text(encoding='utf-8'))
assert audit['status']==facts['status']=='PASS'
assert all(x['status']=='PASS' for x in audit['checks'])
assert facts['plans']==15 and facts['distinct_queries']==720 and facts['raw_timing_rows']==2160
assert facts['timed_logical_work']['queries_per_route']==3487104
assert facts['timed_logical_work']['complete_jobs_per_route']==13824
assert len(json.loads((HERE/'ALL_STRATA.json').read_text(encoding='utf-8')))==60
assert sum(line.startswith('| ') and not line.startswith('| n ') for line in (HERE/'PAPER_READY_FACTS.md').read_text(encoding='utf-8').splitlines())==30
files={str(p.relative_to(HERE)).replace('\\','/'):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
result=dict(status='PASS',created_utc=datetime.now(timezone.utc).isoformat(),checks=26,
    role='Author-side independent validation; not blind review',performance_rerun=False,
    toolchain=dict(python=platform.python_version(),python_flags='-B -X utf8',zig_verified_version='0.14.1',cxx_flags='-O3 -DNDEBUG -std=c++17 -Wall -Wextra'),
    source_manifest_sha256=sha(HERE/'SOURCE_MANIFEST.json'),
    prospective_plan_sha256=sha(BASE.parents[1]/'R05_HOPPER_PROSPECTIVE_RESPONSE_PLAN.md'),
    retained_failures=['FAILURE_PRESERVED.json','BUILD_AND_EXECUTION.md'],
    limitations=audit['limitations'],files=files)
(HERE/'MANIFEST.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('PASS final audit manifest:',len(files),'files; producer evidence and R04 source bindings unchanged.')
