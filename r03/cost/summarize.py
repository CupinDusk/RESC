"""Audit complete timing roster; report all negatives and modeled reuse costs."""
from pathlib import Path
from collections import Counter,defaultdict
from statistics import median
import csv,hashlib,json,math,platform
HERE=Path(__file__).resolve().parent
NAMES=['directBF','beta_graph','cheap_span_graph','quartet_union_graph']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stats(x):return {'median':median(x),'min':min(x),'max':max(x),'all9':x}
def main():
 out=HERE/'RESULTS.json';assert not out.exists()
 manifest=json.loads((HERE/'INPUT_MANIFEST.json').read_text());plans=json.loads((HERE/'inputs.json').read_text());schedule=json.loads((HERE/'schedule.json').read_text());validation=list(csv.DictReader((HERE/'validation.csv').open()));rawq=list(csv.DictReader((HERE/'query_times.csv').open()));rawp=list(csv.DictReader((HERE/'preprocess_times.csv').open()))
 assert len(rawq)==51*9*4*2 and len(rawp)==51*9*3
 qindex={(int(r['block']),int(r['stratum']),int(r['stream']),int(r['route'])):r for r in rawq};pindex={(int(r['block']),int(r['stratum']),int(r['stage'])):r for r in rawp};assert len(qindex)==len(rawq) and len(pindex)==len(rawp)
 surv=json.loads((HERE/'derived_survivor_streams.json').read_text());routecounts=defaultdict(Counter)
 for r in validation:
  sid=plans[int(r['plan'])]['stratum'];routecounts[sid]['queries']+=1;routecounts[sid]['admit']+=int(r['decision']);routecounts[sid]['beta_reject']+=r['beta_path']=='1';routecounts[sid]['cheap_graph']+=r['cheap_path']=='0';routecounts[sid]['quartet_graph']+=r['quartet_path']=='0';routecounts[sid]['quartet_extra_scalar']+=r['quartet_path']=='4'
 for sch in schedule:
  b,sid=sch['block'],sch['stratum'];s=manifest['strata'][sid];assert s['id']==sid
  for stream in [0,1]:
   nr=48*len(s['plans']) if stream==0 else sum(len(surv[str(i)]) for i in s['plans']);sums=[]
   for oi,route in enumerate(sch['routes']):
    r=qindex[b,sid,stream,route];assert int(r['order_position'])==oi and int(r['repeats'])==s['query_repeats'] and int(r['queries_per_repeat'])==nr;sums.append(int(r['checksum']))
   assert len(set(sums))==1
  for oi,stage in enumerate(sch['preprocess']):
   r=pindex[b,sid,stage];assert int(r['order_position'])==oi and int(r['repeats'])==(1000 if stage==1 else 20) and int(r['plans_per_repeat'])==len(s['plans'])
 results=[]
 for s in manifest['strata']:
  sid=s['id'];entry={**s,'route_counts':dict(routecounts[sid]),'cheap_exact_plans':sum(validation[i*48]['cheap_exact']=='1' for i in s['plans']),'quartet_exact_plans':sum(plans[i]['quartet_exact'] for i in s['plans'])}
  # validation follows the original per-plan stream, exactly48 rows/plan.
  prep={}
  for stage,name in enumerate(['closure','cheap_flags','quartet_after_cheap']):
   values=[int(pindex[b,sid,stage]['elapsed_ns'])/int(pindex[b,sid,stage]['repeats'])/len(s['plans']) for b in range(9)];prep[name]=stats(values)
  entry['preprocessing_ns_per_plan']=prep;entry['streams']={}
  for stream,name in [(0,'all'),(1,'beta_survivors_diagnostic')]:
   routes={}
   for route,rname in enumerate(NAMES):
    values=[]
    for b in range(9):
     r=qindex[b,sid,stream,route];den=int(r['repeats'])*int(r['queries_per_repeat']);values.append(int(r['elapsed_ns'])/den if den else None)
    routes[rname]=stats(values) if values[0] is not None else {'undefined_empty_stream':True}
   entry['streams'][name]=routes
  allstats=entry['streams']['all'];c=allstats[NAMES[2]]['median'];q=allstats[NAMES[3]]['median'];pq=prep['quartet_after_cheap']['median'];pc=prep['cheap_flags']['median'];saving=c-q
  entry['incremental_quartet_query_saving_ns']=saving;entry['median_stage_incremental_crossover_Q']=math.floor(pq/saving)+1 if saving>0 else None
  entry['modeled_totals_ns_given_closed_R']={}
  for Q in [1,10,100,1000]:
   totals={NAMES[0]:Q*allstats[NAMES[0]]['median'],NAMES[1]:Q*allstats[NAMES[1]]['median'],NAMES[2]:pc+Q*c,NAMES[3]:pc+pq+Q*q};entry['modeled_totals_ns_given_closed_R'][str(Q)]=totals
  entry['paired_block_incremental_crossover_Q']=[]
  for b in range(9):
   def t(route):r=qindex[b,sid,0,route];return int(r['elapsed_ns'])/int(r['repeats'])/int(r['queries_per_repeat'])
   pr=pindex[b,sid,2];pp=int(pr['elapsed_ns'])/int(pr['repeats'])/len(s['plans']);diff=t(2)-t(3);entry['paired_block_incremental_crossover_Q'].append(math.floor(pp/diff)+1 if diff>0 else None)
  results.append(entry)
 globalcounts=Counter()
 for r in routecounts.values():globalcounts.update(r)
 result={'status':'PASS_COMPLETE_PROSPECTIVE_LOCAL_EXACT_SYNTHETIC_COST_STUDY','scope':'One host, synthetic exact integer log units, no timed H20 auditor or physical/GPU speedup. Complete stream primary; beta-survivor stream diagnostic. Nine blocks are repeated measures on one host, not independent systems. Preprocessing+Q totals are modeled from separately measured medians, not timed end-to-end executions. Given closed_R excludes common separately measured closure; a raw-edge direct BF alternative can avoid closure entirely. Synthetic mix weights are designed coverage, not workload prevalence.','plans':len(plans),'finite_queries':len(validation),'native_BF_Floyd_certificate_checks':len(validation),'python_integer_independent_checks':37440,'native_unknown':0,'global_route_counts':dict(globalcounts),'timing_query_rows':len(rawq),'timing_preprocess_rows':len(rawp),'strata':results,'sha256':{name:sha(HERE/name) for name in ['PROTOCOL.json','PRE_TIMING_AMENDMENT.json','INPUT_MANIFEST.json','PRE_TIMING_VALIDATION.json','benchmark.cpp','benchmark.exe','inputs.txt','schedule.txt','query_times.csv','preprocess_times.csv','validation.csv','summarize.py'] if (HERE/name).is_file()}}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 lines=['# Exact synthetic local audit implementation costs','',result['scope'],'',f"All {len(plans)} plans / {len(validation)} queries passed exact route, Floyd and BF certificate checks; Python independently checked37440 n≤8 queries. Shared beta rejects15567. Cheap+span falls back5288; quartet union5099,189 extra admissions. Unknown0 for these exact integer inputs.",'','Times below are medians ns/query; preprocessing quartets ns/plan. Crossover uses median stage differences and may fail in individual blocks. All min/max/raw values are in RESULTS.json and CSV.','', '|n|geometry|family|plans|cheap EXACT|quartet EXACT|direct|beta|cheap+span|quartet union|quartet preprocess|crossover Q|','|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
 for e in results:
  vals=e['streams']['all'];nums=[vals[n]['median'] for n in NAMES];lines.append('|'+ '|'.join(map(str,[e['n'],e['geometry'],e['family'],len(e['plans']),e['cheap_exact_plans'],e['quartet_exact_plans'],*[round(v,1) for v in nums],round(e['preprocessing_ns_per_plan']['quartet_after_cheap']['median'],1),e['median_stage_incremental_crossover_Q']]))+'|')
 (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['strata','sha256']},indent=2));print('all720:',json.dumps(results[0]))
if __name__=='__main__':main()
