"""Recompute the published policy metrics from the selected numeric matrix.

Run: python -B -X utf8 reanalyze.py
Requires Python 3.12 and NumPy. No GPU, original repository, network, compiler,
account or historical launcher is used.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,json,math
import numpy as np

HERE=Path(__file__).resolve().parent
ARMS=['PULL','PULL_FLAT','PUSH_ST','GLOBAL','PUSH_BULK','PUSH_STASYNC']


def feature(key):return [1,key[1]-1,key[3]/32768,(key[1]-1)*key[3]/32768]


def stats(rs):
    return {'cells':len(rs),'geometric_regret':math.exp(sum(math.log(r['regret']) for r in rs)/len(rs)),
            'maximum_regret':max(r['regret'] for r in rs),'winners':sum(r['selected']==r['oracle'] for r in rs)}


def main():
    cells=defaultdict(dict);metadata={}
    with (HERE/'selected-summary-matrix.csv').open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            key=(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))
            cells[key][r['arm']]={s:float(r[s]) for s in ['primary_ns','min_ns','mean_ns','max_ns']}
            metadata[key]=r
    assert len(cells)==89 and all(len(v)==7 for v in cells.values())
    groups=defaultdict(list)
    for k in cells:groups[(k[0],k[2])].append(k)
    output={}
    for label,summary in [('primary','primary_ns'),('raw_minimum','min_ns'),('raw_mean','mean_ns'),('raw_maximum','max_ns')]:
        predictions=[];fits=[];baseline_predictions=defaultdict(list)
        for (pattern,ncl),keys in sorted(groups.items()):
            train=[k for k in keys if k[1] in [2,4]];test=sorted([k for k in keys if k[1]==8],key=lambda k:k[3])
            x=np.asarray([feature(k) for k in train]);admitted=bool(len(train)>=4 and np.linalg.matrix_rank(x)==4)
            coefs={a:np.linalg.lstsq(x,np.asarray([cells[k][a][summary] for k in train]),rcond=None)[0] for a in ARMS} if admitted else {}
            fits.append({'pattern':pattern,'launched_clusters':ncl,'train_cells':len(train),'admitted':admitted,
                         'coefficients':{a:c.tolist() for a,c in coefs.items()}})
            constant=min(ARMS,key=lambda a:sum(math.log(cells[k][a][summary]) for k in train)/len(train))
            winners=Counter(min(ARMS,key=lambda a:cells[k][a][summary]) for k in train)
            majority=max(ARMS,key=lambda a:winners[a])
            for k in test:
                selected=min(ARMS,key=lambda a:np.dot(feature(k),coefs[a])) if admitted else 'PULL_FLAT'
                oracle=min(ARMS,key=lambda a:cells[k][a][summary])
                row={'pattern':pattern,'launched_clusters':ncl,'payload_B':k[3],'admitted':admitted,'selected':selected,'oracle':oracle,
                     'regret':cells[k][selected][summary]/cells[k][oracle][summary]}
                predictions.append(row)
                neighbor=min([t for t in train if t[1]==4],key=lambda t:(abs(math.log2(t[3]/k[3])),t[3]))
                nearest=min(ARMS,key=lambda a:cells[neighbor][a][summary])
                for policy,choice in [('constant',constant),('majority',majority),('nearest_c4',nearest),
                                      ('model_or_nearest_c4',selected if admitted else nearest)]:
                    baseline_predictions[policy].append({**row,'selected':choice,'regret':cells[k][choice][summary]/cells[k][oracle][summary]})
        def split(rs):
            return {'all':stats(rs),'admitted':stats([r for r in rs if r['admitted']]),
                    'unsupported':stats([r for r in rs if not r['admitted']])}
        output[label]={'model_or_flat':split(predictions),'baselines':{p:split(rs) for p,rs in baseline_predictions.items()},
                       'fits':fits,'cases':predictions}
    assert output['primary']['model_or_flat']['admitted']['winners']==17
    assert abs(output['primary']['model_or_flat']['admitted']['geometric_regret']-1.0043178222330102)<1e-12
    assert abs(output['primary']['model_or_flat']['all']['geometric_regret']-1.082678792437052)<1e-12
    assert abs(output['primary']['baselines']['nearest_c4']['admitted']['geometric_regret']-1.0717541430413777)<1e-12
    print(json.dumps({k:v['model_or_flat'] for k,v in output.items()}))
    census=Counter(int(r['repetitions_from_sweep_script']) for r in metadata.values())
    triplets=[]
    for b in sorted({k[3] for k in cells if k[0]=='Nto1' and k[2]==1}):
        k2=('Nto1',2,1,b);k8=('Nto1',8,1,b)
        if k2 not in cells or k8 not in cells:continue
        nominal={a:cells[k8][a]['primary_ns']/cells[k2][a]['primary_ns'] for a in ['PULL','PULL_FLAT']}
        def factor(k):
            m=metadata[k];i=int(m['nominal_iterations']);return i/(i+int(m['additional_timed_warmup_rounds']))
        triplets.append({'payload_B':b,'nominal_C8_over_C2':nominal,
                         'actual_round_C8_over_C2':{a:r*factor(k8)/factor(k2) for a,r in nominal.items()}})
    assert census=={5:49,3:40},census
    output['corpus_audit']={'repetition_count_to_cells':dict(census),'fan_in_triplets':triplets}
    (HERE/'recomputed-results.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
