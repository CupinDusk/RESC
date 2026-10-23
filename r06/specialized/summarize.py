"""After sole collection, retain absolute cell times and all paired block ratios."""
from pathlib import Path
from statistics import median
import csv,hashlib,json
HERE=Path(__file__).resolve().parent
NAMES=['Raw','Closed','Cheap','Quartet','Specialized','Specialized+Quartet']
def main():
    assert not (HERE/'SUMMARY.json').exists() and not (HERE/'ALL_STRATA.csv').exists()
    meta=json.loads((HERE/'RUN_METADATA.json').read_text());assert meta['status']=='COMPLETE_ONCE'
    with (HERE/'complete_times.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==3240
    plans=json.loads((HERE/'inputs.json').read_text());by={};seen=set()
    for r in rows:
        x={k:int(v) for k,v in r.items()};key=(x['block'],x['stratum'],x['queries'],x['route'])
        assert key not in seen;seen.add(key);assert x['checksum']==x['expected_checksum']
        p=plans[x['stratum']];assert x['repeats']==p['repeats'] and x['jobs_per_repeat']==1
        by[key]=x
    strata=[];paired=[]
    for p in plans:
        for q in [1,48,192,768]:
            item={'stratum':p['id'],'n':p['n'],'family':p['family'],'queries':q,'routes':{}}
            for route,name in enumerate(NAMES):
                times=[by[b,p['id'],q,route]['elapsed_ns']/p['repeats'] for b in range(9)]
                item['routes'][name]={'complete_ns_all_9_blocks':times,'median_complete_ns':median(times),
                    'min_complete_ns':min(times),'max_complete_ns':max(times),
                    'median_complete_ns_per_query_including_preparation':median(times)/q}
            for b in range(9):
                values={name:by[b,p['id'],q,route]['elapsed_ns']/p['repeats'] for route,name in enumerate(NAMES)}
                for numerator,denominator in [('Cheap','Specialized'),('Quartet','Specialized'),('Specialized','Specialized+Quartet'),('Cheap','Quartet')]:
                    paired.append({'block':b,'stratum':p['id'],'n':p['n'],'family':p['family'],'queries':q,
                        'numerator':numerator,'denominator':denominator,'numerator_complete_ns':values[numerator],
                        'denominator_complete_ns':values[denominator],'ratio':values[numerator]/values[denominator]})
            strata.append(item)
    assert len(strata)==60 and len(paired)==2160
    with (HERE/'PAIRED_ROWS.csv').open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(paired[0]));w.writeheader();w.writerows(paired)
    flat=[]
    for s in strata:
        for route,data in s['routes'].items():flat.append({k:s[k] for k in ['stratum','n','family','queries']}|{'route':route}|{k:v for k,v in data.items() if not isinstance(v,list)})
    with (HERE/'ALL_STRATA.csv').open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    result={'scope':'One ordinary Windows collection on the same deliberately designed fixed R05 synthetic family. No representative distribution, stable crossover or machine-isolation claim.',
        'raw_records':3240,'strata':strata,'paired_rows':2160,'per_query_boundary':'Complete preparation-inclusive job divided by Q; no separately measured query kernel.',
        'old_R05':'Preserved prior once-only evidence, not called repeated reproduction.',
        'raw_sha256':hashlib.sha256((HERE/'complete_times.csv').read_bytes()).hexdigest()}
    (HERE/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'strata':60,'absolute_route_cells':360,'paired_rows':2160,'timed_rows':3240}))
if __name__=='__main__':main()
