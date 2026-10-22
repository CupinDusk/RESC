"""Record tool-invoked commands and exact observed return codes; no timings."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[3]
py=Path(sys.executable)
zig=ROOT/'.tools/zig-0.14.1/zig-x86_64-windows-0.14.1/zig.exe'
pre=[str(py),'-B','-X','utf8']
commands=[
 dict(name='fresh_portable_replay',argv=pre+[str(BASE/'replay_portable.py'),'--out',str(HERE/'fresh-replay'),'--yosys-python-wrapper',str(ROOT/'.tools/run_iscas_yosys.py'),'--cxx',str(zig),'--zig','--include',str(ROOT/'.tools/iscas-rtl-20261023/yowasp_yosys/share/include')],returncode=0,stage_logs='fresh-replay/PORTABLE_REPLAY.json'),
 dict(name='compile_independent_edge_oracle',argv=[str(zig),'c++','-std=c++17','-O3','-UNDEBUG',str(HERE/'edge_oracle.cpp'),'-o',str(HERE/'edge_oracle.exe')],returncode=0,observed_stdout='',observed_stderr=''),
 dict(name='producer_full_edge_expansion',argv=[str(HERE/'edge_oracle.exe'),str(BASE/'attempt-002'),str(HERE/'PRODUCER_EDGE_CHECK.json')],returncode=0,observed_stdout='PASS every decoded edge: 389022846\n'),
 dict(name='fresh_full_edge_expansion',argv=[str(HERE/'edge_oracle.exe'),str(HERE/'fresh-replay'),str(HERE/'FRESH_EDGE_CHECK.json')],returncode=0,observed_stdout='PASS every decoded edge: 389022846\n'),
 *[dict(name='independent_checks_attempt_'+str(i).zfill(3),argv=pre+[str(HERE/'independent_checks.py')],returncode=1 if i<3 else 0,combined_log='independent_checks-attempt-'+str(i).zfill(3)+'.log') for i in range(1,5)],
 dict(name='synthesized_mutants',argv=pre+[str(HERE/'run_mutants.py')],returncode=0,combined_log='mutant_run-attempt-001.log',stage_logs='mutants/*/RESULT.json'),
 dict(name='finalize_audit',argv=pre+[str(HERE/'finalize_audit.py')],returncode=0,note='Final artifact generation; only metadata/file hashing, not scientific execution')
]
(HERE/'COMMANDS.json').write_text(json.dumps(dict(commands=commands,working_directory=str(ROOT),performance_timings_collected=False,note='Recorded from actual tool calls; final checker source is snapshotted in checker-sources. Initial failed check logs remain unchanged.'),indent=2)+'\n',encoding='utf-8')
