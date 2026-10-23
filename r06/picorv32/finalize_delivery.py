"""Build transparent bounded facts and a portable file whitelist, no publication."""
from pathlib import Path
import hashlib,json,csv,shutil
HERE=Path(__file__).resolve().parent
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def main():
 out=HERE/'attempt-007';audit=json.loads((out/'AUDIT_RESULTS.json').read_text(encoding='utf-8'));rtl=json.loads((out/'RTL_RESULTS.json').read_text(encoding='utf-8'));jobs=list(csv.DictReader((out/'JOBS.csv').open(encoding='utf-8')))
 assert len(jobs)==576 and audit['source_licensed_jobs']==576
 failure=[]
 for d in sorted(HERE.glob('attempt-*')):
  a=json.loads((d/'ATTEMPT.json').read_text(encoding='utf-8'))
  if d.name!='attempt-007':failure.append(dict(attempt=d.name,status=a['status'],ledger_sha256=sha(d/'ATTEMPT.json'),graph_status='contract-unknown/not-audited',note='No failure is counted as a known graph result; unexecuted cases are not successful observations.'))
 write(HERE/'FAILED_BINDINGS.json',dict(failures=failure,original_failure_logs_and_ELF_preserved_byte_exact=True,original_protocol_sha256=sha(HERE/'PROTOCOL.json'),failed_actual_job=dict(attempt='attempt-006',job=0,status='contract-unknown',reason='Overly strict terminal-fetch validator; actual trace retained; amendment6')))
 # Preserve exact old audit/checker math with source binding.
 prov=json.loads((HERE/'CORE_PROVENANCE.json').read_text(encoding='utf-8'));prov['r05_certificate_checker.py']={'source':'r05-analysis/hopper-reference-rtl/audit_reports.py','sha256':sha(HERE/'r05_certificate_checker.py'),'use':'original-variable admission and edgewise rejection certificate checker, exact bytes'};write(HERE/'CORE_PROVENANCE.json',prov)
 example=None
 if audit['changed_decision_examples']:
  q=audit['changed_decision_examples'][0];rid=q['report'];cell=audit['cells'][rid];obs=json.loads((out/'OBSERVATIONS.json').read_text(encoding='utf-8'))[rid]
  example=dict(report_cell=cell,query=q,observation=obs,actual_source_jobs=[r for r in jobs if int(r['report'])==rid],meaning='Source-derived every-anchor-box admission but negative-cycle joint rejection. Integer weights at scale10^60 are outward-safe. Original N/D shown here are debug, excluded from auditor interface.')
 write(HERE/'NEGATIVE_CYCLE_EXAMPLE.json',example)
 zeros=[dict(report=x['report'],function=x['function'],input=x['input'],guard=x['guard'],path=x['path'],total_additional=x['total'].get('additional_joint_rejections',0),partial_additional=x['partial'].get('additional_joint_rejections',0)) for x in audit['cells'] if x['total'].get('additional_joint_rejections',0)==0 or x['partial'].get('additional_joint_rejections',0)==0]
 facts=dict(status='PRODUCER_COMPLETE_PENDING_DIFFERENT_AGENT_FRESH_GATE',upstream_commit='ef203c2b0a3fb793280f5114941416c425c5b461',unmodified_upstream_RTL=True,reports=96,jobs=576,firmware_binaries=36,independent_ISA_functional_combinations=72,queries=69888,actual_processor_core_cycles=rtl['core_cycles'],actual_reference_edges=rtl['reference_edges'],invalid_controller_controls=8,source_validator_input_mutations=4,all_invalid_contract_unknown=12,source_licensed_jobs=576,timer_model='T=N*D, c=0; actual reference edges, no driver assigned timer',total_orders=audit['total_orders'],fixed_partials=audit['fixed_partials'],groups=audit['groups'],duplicate_ram_binary_groups=audit['duplicate_ram_binary_groups'],zero_additional_cells_retained=zeros,failed_attempts=len(failure),independent_fresh_gate_complete=False,scope=audit['limitations'],limitations=['Fixed deterministic finite census, not representative firmware workload frequencies.','N is actual processor cycles under declared synchronous memory and CXXRTL scheduler boundary; all startup/result/trap cycles remain included.','Functional interpreter/algorithm check never supplies DUT cycle counts.','Admission concerns a real-log abstraction, not alternate integer N/D realizability or recovery of original N.','Every-anchor-box comparator permits separate witnesses per anchor/comparison; graph admission needs one joint original-variable witness.','Source validity and trusted guard bits are obligations supplied by producer; failure returns unknown.','Overflow guards reviewed under the bounded run domain; overflow event was not forced by simulation.','No claims of physical clock, native Hopper, silicon, FPGA, PPA, privacy or method necessity.','The fresh independent run, independent trace decode and all certificate checks remain a mandatory later gate.'],bindings={n:sha(HERE/n) for n in ['PROTOCOL.json','UPSTREAM_BINDING.json','driver.cpp','core_wrapper.v','controller.v','functional_oracle.py','audit_reports.py','replay_portable.py','CORE_PROVENANCE.json']})
 write(HERE/'PAPER_READY_FACTS.json',facts)
 t=audit['total_orders'];p=audit['fixed_partials'];den=t.get('box_admit',0);pden=p.get('box_admit',0)
 md=f'''# Bounded producer facts; independent gate pending

Actual unmodified PicoRV32 commit `{facts['upstream_commit']}` executes36 fixed
RV32I firmware binaries across72 function/input/flag combinations and576
reference-design jobs. All72 independent ISA/algorithm checks and576 actual
RTL outputs agree. The controller counts {rtl['reference_edges']} actual
reference edges and the processor executes {rtl['core_cycles']} core cycles.
Observed timer identity is T=N*D with start/reset/stop outside and c=0.

All69120 total orders: admit={t.get('admit',0)}, reject={t.get('reject',0)},
unknown={t.get('unknown',0)}, false admissions={t.get('false_admit',0)}.
Additional joint rejections beyond every-anchor boxes:
{t.get('additional_joint_rejections',0)}/{den} box admissions.
All768 fixed partials: admit={p.get('admit',0)}, reject={p.get('reject',0)},
unknown={p.get('unknown',0)}, false admissions={p.get('false_admit',0)};
additional joint rejections={p.get('additional_joint_rejections',0)}/{pden}.
Every report, tie/duplicate binary, zero-effect cell and failed attempt is
retained. Twelve invalid-control/source-validator cases return unknown.

These are producer-verified discrete-event reference-design facts. They
remain pending a different agent's fresh synthesis/execution, independent
timer-trace decode and69888 certificate checks. No publication or PDF use
is authorized by this file alone. No physical clock, native Hopper, silicon,
FPGA, PPA, performance or confidentiality conclusion follows.
'''
 (HERE/'PAPER_READY_FACTS.md').write_text(md,encoding='utf-8')
 files=[];excluded=[];portable=HERE/'portable-v1';portable.mkdir(exist_ok=False)
 for pth in sorted(HERE.rglob('*')):
  if not pth.is_file():continue
  rel=pth.relative_to(HERE).as_posix()
  if pth.name in ['PORTABLE_MANIFEST.json','PORTABLE_PACKAGE.zip'] or 'portable-v1' in pth.parts:continue
  reason=None
  if pth.suffix.lower() in ['.exe','.pdb']:reason='host build product, not distributed'
  if rel=='attempt-003/images/array_sum_O0.elf':reason='failed oversized default-runtime ELF contains local compiler debug paths; exact hash/segments kept locally, not distributed'
  if pth.name in ['CORE_CYCLES.csv','REFERENCE_RLE.csv'] and (pth.parent/(pth.name+'.gz')).exists():reason='raw duplicate of hash-bound lossless gzip'
  if '__pycache__' in pth.parts:reason='runtime cache'
  rec=dict(path=rel,bytes=pth.stat().st_size,sha256=sha(pth))
  if reason:excluded.append(dict(**rec,reason=reason))
  else:
   dest=portable/rel;dest.parent.mkdir(parents=True,exist_ok=True);data=pth.read_bytes();before=rec['sha256'];adaptations=[]
   if pth.suffix.lower() in ['.json','.log','.txt','.md','.csv','.cpp','.v','.h','.hpp','.py','.s','.ld']:
    user=str(Path.home()).encode();slashuser=str(Path.home()).replace('\\','/').encode()
    for needle in [user,slashuser]:
     if needle in data:data=data.replace(needle,b'[LOCAL_USER]');adaptations.append('local tool/cache home path replaced in portable copy only')
   dest.write_bytes(data);files.append(dict(path=rel,bytes=len(data),sha256=sha(dest),source_sha256=before,metadata_path_adaptations=adaptations))
 manifest=dict(status='PORTABLE_WHITELIST_ONLY_NO_PUBLICATION',portable_root='portable-v1',files=files,excluded_local_files=excluded,exclusion_note='Package portable-v1 only; raw failure logs/ELF and host products remain unchanged local evidence. Each portable-copy path adaptation has before/after hashes.')
 write(HERE/'PORTABLE_MANIFEST.json',manifest);write(portable/'PORTABLE_MANIFEST.json',manifest)
 print(json.dumps({k:facts[k] for k in ['status','jobs','queries','actual_reference_edges','actual_processor_core_cycles','total_orders','fixed_partials','failed_attempts']},indent=2))
if __name__=='__main__':main()
