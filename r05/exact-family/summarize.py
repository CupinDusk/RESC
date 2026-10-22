"""Summarize all predeclared strata without selection or retiming."""
from pathlib import Path
import csv, hashlib, json, statistics
HERE=Path(__file__).resolve().parent
def read(n):
    with (HERE/n).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
    plans=json.loads((HERE/'inputs.json').read_text(encoding='utf-8'))
    schedule=json.loads((HERE/'schedule.json').read_text(encoding='utf-8'))
    rows=read('complete_times.csv');assert len(rows)==2160
    expected={(int(r['stratum']),int(r['queries'])):int(r['expected_checksum']) for r in read('expected_batches.csv')}
    index={}
    for r in rows:
        b,s,q,p,route,reps,jobs,ns=[int(r[k]) for k in ['block','stratum','queries','position','route','repeats','jobs_per_repeat','elapsed_ns']]
        assert reps==plans[s]['repeats'] and jobs==1 and ns>0
        assert int(r['checksum'])==int(r['expected_checksum'])==(expected[s,q]*reps)%(1<<64)
        key=b,s,q,route;assert key not in index;index[key]=ns/reps
    sequence=[(r['block'],r['stratum'],r['queries'],i,route) for r in schedule for i,route in enumerate(r['routes'])]
    assert sequence==[tuple(int(r[k]) for k in ['block','stratum','queries','position','route']) for r in rows]
    result=[]
    for plan in plans:
        sid=plan['id']
        for q in [1,48,192,768]:
            vals=[[index[b,sid,q,route] for b in range(9)] for route in range(4)]
            x=dict(plan=sid,n=plan['n'],family=plan['family'],queries=q,
                medians_ns=[statistics.median(v) for v in vals],
                minima_ns=[min(v) for v in vals],maxima_ns=[max(v) for v in vals],
                quartet_faster=sum(a<b for a,b in zip(vals[3],vals[2])),
                quartet_slower=sum(a>b for a,b in zip(vals[3],vals[2])),
                quartet_ties=sum(a==b for a,b in zip(vals[3],vals[2])),
                cheap_over_quartet_paired_ratios=[a/b for a,b in zip(vals[2],vals[3])])
            result.append(x)
    summary=dict(status='ALL_2160_RECORDS_SUMMARIZED_PENDING_INDEPENDENT_AUDIT',plans=15,distinct_queries=720,
        scope='Deliberately favorable exact-family constructed study. A specialized adjacent-reversal flag could be cheaper. R04 adverse studies unchanged.',
        raw_sha256=hashlib.sha256((HERE/'complete_times.csv').read_bytes()).hexdigest(),strata=result)
    (HERE/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    with (HERE/'ALL_STRATA.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['n','family','Q','Raw_ns','Closed_ns','Cheap_ns','Quartet_ns','Q_faster','Q_slower','Q_ties','paired_ratio_median'])
        for r in result:w.writerow([r['n'],r['family'],r['queries'],*r['medians_ns'],r['quartet_faster'],r['quartet_slower'],r['quartet_ties'],statistics.median(r['cheap_over_quartet_paired_ratios'])])
    print('n family Q Raw_ns Closed_ns Cheap_ns Quartet_ns Q_faster/Q_slower/tie')
    for r in result:
        print(r['n'],r['family'],r['queries'],*[round(v,1) for v in r['medians_ns']],f"{r['quartet_faster']}/{r['quartet_slower']}/{r['quartet_ties']}")
if __name__=='__main__':main()
