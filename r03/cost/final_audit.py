"""Post-collection audit and honest stage-cost interpretation; never reruns timing."""
from pathlib import Path
from collections import defaultdict
from statistics import median
import csv,json,hashlib,math
HERE=Path(__file__).resolve().parent
NAMES=['directBF','beta_graph','cheap_span_graph','quartet_union_graph']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stat(x):return {'median':median(x),'min':min(x),'max':max(x),'all9':x}
def main():
 result=json.loads((HERE/'RESULTS.json').read_text());frozen=json.loads((HERE/'PRE_TIMING_VALIDATION.json').read_text());assert not (HERE/'FINAL_AUDIT.json').exists()
 for name,value in frozen['sha256'].items():assert sha(HERE/name)==value,(name,'changed after pre-timing freeze')
 q=list(csv.DictReader((HERE/'query_times.csv').open()));p=list(csv.DictReader((HERE/'preprocess_times.csv').open()));qi={(int(r['block']),int(r['stratum']),int(r['stream']),int(r['route'])):r for r in q}
 groups=defaultdict(list)
 for e in result['strata']:groups[e['n']].append(e)
 aggregates=[]
 for n,entries in sorted(groups.items()):
  a={'n':n,'plans':sum(len(e['plans']) for e in entries),'finite_queries':sum(e['route_counts']['queries'] for e in entries),'domain':'all720 total orders' if n==6 else '2 geometries x5 families x3seeds','route_query_ns':{},'route_counts':{}}
  for key in ['beta_reject','cheap_graph','quartet_graph','quartet_extra_scalar']:a['route_counts'][key]=sum(e['route_counts'][key] for e in entries)
  for route,name in enumerate(NAMES):
   v=[]
   for b in range(9):
    numerator=sum(int(qi[b,e['id'],0,route]['elapsed_ns'])/int(qi[b,e['id'],0,route]['repeats']) for e in entries);den=sum(e['route_counts']['queries'] for e in entries);v.append(numerator/den)
   a['route_query_ns'][name]=stat(v)
  aggregates.append(a)
 e=result['strata'][0];assert e['family']=='all720';c=e['preprocessing_ns_per_plan']['closure']['median'];cheap=e['preprocessing_ns_per_plan']['cheap_flags']['median'];quart=e['preprocessing_ns_per_plan']['quartet_after_cheap']['median'];t=e['streams']['all'];totals={}
 for Q in [1,10,48,100,1000]:
  totals[str(Q)]={'given_closed_R':{NAMES[0]:Q*t[NAMES[0]]['median'],NAMES[1]:Q*t[NAMES[1]]['median'],NAMES[2]:cheap+Q*t[NAMES[2]]['median'],NAMES[3]:cheap+quart+Q*t[NAMES[3]]['median']},'all_routes_including_same_measured_closure':{NAMES[0]:c+Q*t[NAMES[0]]['median'],NAMES[1]:c+Q*t[NAMES[1]]['median'],NAMES[2]:c+cheap+Q*t[NAMES[2]]['median'],NAMES[3]:c+cheap+quart+Q*t[NAMES[3]]['median']}}
 faster=sum(x is not None for x in e['paired_block_incremental_crossover_Q']);data={'status':'PASS_FIXED_INPUT_SOURCE_AND_RAW_ROSTER_AUDIT_NO_TIMING_RERUN','all720':{'common_closure_ns_per_plan':c,'cheap_flag_ns_per_plan':cheap,'additional_quartet_ns_per_plan':quart,'full_setup_cheap_ns_per_plan':c+cheap,'full_setup_quartet_ns_per_plan':c+cheap+quart,'paired_blocks_quartet_query_faster':faster,'paired_blocks_quartet_query_slower_or_equal':9-faster,'actual_queries_per_plan':48,'modeled_totals_ns_per_plan':totals},'n_aggregate':aggregates,'limitations':['No stable incremental quartet runtime advantage established by overlapping run ranges and mixed paired signs. Median-stage nominal crossover75 is descriptive, not a reliable deployment threshold.','In the actual48-query/plan census, additional quartet setup exceeds the median query saving; preprocessing-inclusive nominal total is slightly worse.','Beta-survivor diagnostic has cheap median57.824ns/query and quartet58.154ns/query; it does not establish a runtime advantage.','All scaling strata with n>=8 have identical cheap-vs-quartet fallback counts. Differences in their runtime medians cannot be attributed to additional quartet pruning.','Several already-cheap-EXACT quartet preprocessing batches are only100--300ns; do not interpret their divided1--5ns values as precise individual call costs.','Common closure was measured explicitly. The timed direct BF consumes the same closed_R; a direct checker can use original ranking edges and avoid closure, but that variant was not timed.','The single-host block schedule reduces drift confounding without proving CPU-load independence, hardware representativeness or population speedup.','No H20 timing auditor, GPU, hardware behavior, physical drift or improved GPU choice was measured. Synthetic integer graph instances and existing retained H20 routing counts are distinct.'],'files':{name:sha(HERE/name) for name in ['RESULTS.json','RESULTS.md','RUN_METADATA.json','timing-run.log','query_times.csv','preprocess_times.csv','PROTOCOL.json','PRE_TIMING_AMENDMENT.json','INPUT_MANIFEST.json','PRE_TIMING_VALIDATION.json','benchmark.cpp','benchmark.exe','inputs.json','inputs.txt','schedule.json','schedule.txt','validation.csv','derived_survivor_streams.json','generate_inputs.py','independent_check.py','summarize.py','final_audit.py'] if (HERE/name).is_file()}}
 (HERE/'FINAL_AUDIT.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print(json.dumps(data['all720'],indent=2))
if __name__=='__main__':main()
