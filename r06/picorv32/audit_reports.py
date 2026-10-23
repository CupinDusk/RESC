"""Public-interface-only graph census; debug truth remains separately identified."""
from pathlib import Path
from fractions import Fraction
from itertools import permutations
from collections import Counter,defaultdict
import argparse,csv,gzip,hashlib,json,copy
import audit_core as core
import exact_logs
from functional_oracle import functional
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def source_valid(j,expected):
 reasons=[]
 if j.get('controller_valid')!=1 or j.get('reason')!=0:reasons.append('controller_obligation')
 if j.get('source_valid')!=1:reasons.append('memory_or_source_obligation')
 if j.get('result_writes')!=1:reasons.append('exactly_one_result')
 if j.get('result')!=expected:reasons.append('functional_result')
 if j.get('ebreak_fetched')!=1 or j.get('lastfetch')!=28 or j.get('lastinsn')!=111:reasons.append('known_ebreak_and_prefetch_terminal')
 if not 1<=j.get('N',0)<=1000000:reasons.append('core_cycle_bound')
 if not 1<=j.get('D',0)<=2000:reasons.append('divider_bound')
 if j.get('T')!=j.get('N',0)*j.get('D',0):reasons.append('timer_identity')
 if j.get('ref_trap',0)-j.get('ref_start',0)!=j.get('T'):reasons.append('observed_interval')
 if j.get('ref_stop')!=j.get('ref_trap',0)+1:reasons.append('stop_edge')
 return not reasons,reasons
def add(c,truth,r):
 c['queries']+=1;c['true' if truth else 'false']+=1;c[r['path']]+=1;c[('true_' if truth else 'false_')+r['path']]+=1;c['box_'+r['box']]+=1;c['additional_joint_rejections']+=int(r['box']=='admit' and r['path']=='reject')
 if r['box']=='admit':c['box_admitted_true' if truth else 'box_admitted_false']+=1
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--attempt',type=Path,required=True);a=ap.parse_args();out=a.attempt
 proto=json.loads((out/'PROTOCOL.json').read_text(encoding='utf-8'));config=json.loads((out/'JOBS_CONFIG.json').read_text(encoding='utf-8'))
 # Reuse byte-exact reviewed R05 certificate checker, including original-variable witnesses.
 checker=Path(__file__).resolve().parent/'r05_certificate_checker.py'
 assert checker.exists(), 'byte-exact source-bound R05 certificate checker required'
 import r05_certificate_checker as certcheck
 rows=[{k:int(v) if k not in ['function','flag'] else v for k,v in r.items()} for r in csv.DictReader((out/'JOBS.csv').open(encoding='utf-8'))];assert len(rows)==576
 oracle=json.loads((out/'FUNCTIONAL_ORACLE.json').read_text(encoding='utf-8'))['rows'];isa={(x['function'],x['flag'],x['input']):x for x in oracle};assert len(isa)==72
 interface=[];debug=[];invariants=defaultdict(set)
 for r in rows:
  expected=functional(r['function'],proto['inputs'][r['input']]);ok,reasons=source_valid(r,expected);assert isa[r['function'],r['flag'],r['input']]['result']==expected
  invariants[r['function'],r['flag'],r['input']].add((r['N'],r['result']))
  debug.append(dict(**r,expected=expected,licensed=ok,failed_obligations=reasons))
 assert all(len(v)==1 for v in invariants.values())
 for rep in config['reports']:
  jobs=[]
  for slot in range(6):
   r=debug[rep['report']*6+slot];assert r['report']==rep['report'] and r['slot']==slot
   jobs.append(dict(slot=slot,valid=r['licensed'],timer_range=[r['T']-1,r['T']+1] if r['licensed'] else None,obligations=dict(processor_reset=True,memory_contract=r['licensed'],functional_and_ISA_check=r['licensed'],known_termination=r['licensed'],timer_reference_edges=r['licensed'],held_divider=r['licensed'],settled_guard=r['licensed'])))
  interface.append(dict(report=rep['report'],budget=rep['guard'],jobs=jobs))
 controls=[dict(id=int(r['id']),kind='actual_controller_execution',valid=False,status='contract-unknown',reason=int(r['actual_reason']),graph_audit_licensed=False) for r in csv.DictReader((out/'INVALID_CONTROLS.csv').open(encoding='utf-8'))]
 assert len(controls)==8 and [x['reason'] for x in controls]==[1,2,2,3,4,6,5,8]
 mutations=[]
 for name in proto['source_validator_controls']:
  j=copy.deepcopy(rows[0]);expected=functional(j['function'],proto['inputs'][j['input']])
  if name=='missing_result':j['result_writes']=0
  if name=='wrong_result':j['result']^=1
  if name=='early_stop_without_trap':j['ebreak_fetched']=0
  if name=='memory_contract_false':j['source_valid']=0
  ok,why=source_valid(j,expected);assert not ok
  mutations.append(dict(id=8+len(mutations),kind='validator_input_mutation_not_new_DUT_execution',name=name,valid=False,status='contract-unknown',failed_obligations=why,graph_audit_licensed=False))
 public=dict(kind='slot-range-validity abstraction only',reports=interface,invalid_controls=controls+mutations,privacy='No secrecy, cryptography or inference-resistance guarantee')
 write(out/'AUDITOR_INPUTS.json',public);write(out/'DEBUG_SOURCE_RESULTS.json',debug);write(out/'SOURCE_VALIDATOR_CONTROLS.json',mutations)
 # Graph construction below reads only the abstraction interface and public protocol budgets.
 iface=json.loads((out/'AUDITOR_INPUTS.json').read_text(encoding='utf-8'));total=Counter();partials=Counter();groups=defaultdict(Counter);cells=[];observations=[];examples=[];nq=0;certs=Counter()
 rawhash=hashlib.sha256();expanded_bytes=0
 archive=out/'ALL_REPORTS.jsonl.gz'
 with archive.open('wb') as ff,gzip.GzipFile(fileobj=ff,mode='wb',mtime=0) as stream:
  for rep,pub in zip(config['reports'],iface['reports']):
   rid=pub['report'];g=proto['guards'][pub['budget']];delta=exact_logs.bounds(Fraction(g['numerator'],g['denominator']));Ns=[debug[rid*6+i]['N'] for i in range(6)];licensed=all(j['valid'] for j in pub['jobs']);b=None
   if licensed:b={'l':[exact_logs.bounds(Fraction(j['timer_range'][0],1000)) for j in pub['jobs']],'u':[exact_logs.bounds(Fraction(j['timer_range'][1],1000)) for j in pub['jobs']]}
   stats=Counter();ps=Counter();group=('all_tie' if len(set(Ns))==1 else 'contains_ties' if len(set(Ns))<6 else 'distinct')
   queries=[('total_order',list(order),[(order[i],order[j]) for i in range(6) for j in range(i+1,6)]) for order in permutations(range(6))]+[('fixed_partial',i,[tuple(x) for x in claims]) for i,claims in enumerate(proto['queries']['fixed_partials'])]
   for kind,qid,claims in queries:
    if licensed:r=core.audit(b,delta,claims);certcheck.check_certificate(b,delta,claims,r)
    else:r=dict(path='unknown',box='unknown',certificate={'reason':'unlicensed_source'})
    truth=all(Ns[p]<=Ns[q] for p,q in claims);row=dict(report=rid,kind=kind,query=qid,claims=claims,true=truth,**r)
    data=(json.dumps(row,separators=(',',':'))+'\n').encode();stream.write(data);rawhash.update(data);expanded_bytes+=len(data);nq+=1;certs[r['path']]+=1
    target=stats if kind=='total_order' else ps;add(target,truth,r)
    if r['box']=='admit' and r['path']=='reject' and len(examples)<24 and not any(e['report']==rid for e in examples):examples.append(row)
   total.update(stats);partials.update(ps);groups[g['name']+'_total'].update(stats);groups[g['name']+'_partial'].update(ps);groups[group+'_total'].update(stats);groups[group+'_partial'].update(ps)
   cells.append(dict(**rep,tie_group=group,N=Ns,total=dict(stats),partial=dict(ps)))
   observations.append(dict(report=rid,budget=pub['budget'],timer_ranges=[j['timer_range'] for j in pub['jobs']],delta_scaled=delta,log_bounds=b))
 assert nq==69888
 binarybindings=json.loads((out/'FIRMWARE_BINDINGS.json').read_text(encoding='utf-8'));duplicates=defaultdict(list)
 for n,x in binarybindings.items():duplicates[x['ram_sha256']].append(n)
 result=dict(status='PASS_PRODUCER_ONLY_PENDING_DIFFERENT_AGENT_FRESH_EXECUTION_AND_CERTIFICATE_AUDIT',reports=96,jobs=576,queries=nq,total_orders=dict(total),fixed_partials=dict(partials),groups={k:dict(v) for k,v in groups.items()},cells=cells,certificates=dict(certs),source_licensed_jobs=sum(x['licensed'] for x in debug),source_unknown_jobs=sum(not x['licensed'] for x in debug),invalid_control_unknown=12,query_stream={'compressed_sha256':sha(archive),'expanded_sha256':rawhash.hexdigest(),'expanded_bytes':expanded_bytes},duplicate_ram_binary_groups=[v for v in duplicates.values() if len(v)>1],cycle_invariance_72_combinations_all_8_guard_path_pairs=True,changed_decision_examples=examples,numerics=exact_logs.proof_metadata(),limitations=proto['scope'])
 write(out/'OBSERVATIONS.json',observations);write(out/'AUDIT_RESULTS.json',result)
 print(json.dumps({k:result[k] for k in ['status','queries','total_orders','fixed_partials','invalid_control_unknown','source_licensed_jobs']},indent=2))
if __name__=='__main__':main()
