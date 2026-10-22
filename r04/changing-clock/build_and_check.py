"""Guard-attaining changing-clock interface: specified model, never GPU data.

The outward graph auditor is an unchanged local copy of the R03 own research
functions. Its provenance is recorded; independent validation uses no imports
from either auditor. Run in a fresh directory only.
"""
from pathlib import Path
from fractions import Fraction
from itertools import permutations
from collections import Counter
import gzip, hashlib, importlib.util, json

HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(v): return f'{v.numerator}/{v.denominator}'

def main():
    protocol_path=HERE/'PROTOCOL.json'
    protocol=json.loads(protocol_path.read_text(encoding='utf-8'))
    for name in ['OBSERVATIONS.json','RESULTS.json','ALL_REPORTS.jsonl.gz']:
        assert not (HERE/name).exists(),name
    core_path=HERE/'audit_core.py'
    spec=importlib.util.spec_from_file_location('own_outward_core',core_path)
    core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
    guard=Fraction(protocol['ratio_guard']);delta=core.log_bounds(guard)
    reference=Fraction(protocol['reference_multiplier'])
    paths={
      'rising':[reference*guard**j for j in range(1,7)],
      'falling':[reference/guard**j for j in range(1,7)],
      'alternating':[reference*guard if j%2 else reference for j in range(1,7)]}
    invalid=[Fraction(v) for v in [10000,10060,10000,10000,10000,10000]]
    bad_edges=[j for j,(a,b) in enumerate(zip([reference]+invalid[:-1],invalid),1)
      if max(a/b,b/a)>guard]
    assert bad_edges==[2,3]
    observations=[];reports=[];total=Counter();edge_count=0;tight_edges=0
    for vector_id,counts in enumerate(protocol['cycle_count_vectors']):
      for path_name,path in paths.items():
        previous=reference
        for multiplier in path:
          actual=max(multiplier/previous,previous/multiplier)
          assert actual==guard
          previous=multiplier;edge_count+=1;tight_edges+=1
        durations=[Fraction(n)*reference/m for n,m in zip(counts,path)]
        low=[Fraction(t.numerator//t.denominator-1) for t in durations]
        high=[Fraction(-(-t.numerator//t.denominator)+1) for t in durations]
        assert all(0<l<t<u for l,t,u in zip(low,durations,high))
        bounds=dict(l=[core.log_bounds(v) for v in low],u=[core.log_bounds(v) for v in high])
        case_id=len(observations)
        ob=dict(case_id=case_id,vector_id=vector_id,path_name=path_name,cycles=counts,
          multipliers=[ratio(v) for v in path],durations=[ratio(v) for v in durations],
          lower=[ratio(v) for v in low],upper=[ratio(v) for v in high],log_scaled_bounds=bounds)
        stats=Counter()
        for order in permutations(range(6)):
          claims=[(order[i],order[j]) for i in range(6) for j in range(i+1,6)]
          result=core.audit(bounds,delta,claims)
          truth=all(counts[a]<=counts[b] for a,b in claims)
          assert not truth or result['path']=='admit',(vector_id,path_name,order,result)
          row=dict(case_id=case_id,kind='total_order',order=list(order),true=truth,**result)
          reports.append(row);stats['reports']+=1;stats[result['path']]+=1
          stats['true']+=truth;stats['false_admit']+=int(not truth and result['path']=='admit')
          stats['box_'+result['box']]+=1
          stats['box_admit_path_reject']+=int(result['box']=='admit' and result['path']=='reject')
        claims=[(0,5),(4,1)];res=core.audit(bounds,delta,claims)
        truth=all(counts[a]<=counts[b] for a,b in claims)
        assert not truth or res['path']=='admit'
        reports.append(dict(case_id=case_id,kind='fixed_partial',claims=claims,true=truth,**res))
        ob['total_order_summary']=dict(stats);ob['fixed_partial']=reports[-1]
        observations.append(ob);total.update(stats)
    with gzip.open(HERE/'ALL_REPORTS.jsonl.gz','wt',encoding='utf-8',newline='\n') as out:
      for row in reports:out.write(json.dumps(row,separators=(',',':'))+'\n')
    (HERE/'OBSERVATIONS.json').write_text(json.dumps(observations,indent=2)+'\n',encoding='utf-8')
    result=dict(status='PASS_SPECIFIED_CHANGING_CLOCK_INTERFACE',scale=str(core.SCALE),
      delta_scaled_enclosure=delta,legal_cases=len(observations),reports=len(reports),
      total_order_summary=dict(total),guard_checks=edge_count,guard_attaining_edges=tight_edges,
      contract_negative_control=dict(multipliers=[ratio(v) for v in invalid],bad_edges=bad_edges,
        vectors=8,reports_per_vector=721,contract_unknown=8*721,
        rule='Guard fails before numerical audit; no admit/reject conclusion is licensed.'),
      positive_certificates=sum(r['path']=='admit' for r in reports),
      negative_certificates=sum(r['path']=='reject' for r in reports),
      numeric_unknown=sum(r['path']=='unknown' for r in reports),
      provenance={p.name:sha(p) for p in [protocol_path,core_path,Path(__file__),HERE/'OBSERVATIONS.json',HERE/'ALL_REPORTS.jsonl.gz']},
      scope=protocol['scope'])
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
