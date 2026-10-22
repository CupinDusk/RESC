"""Candidate-dependent reanchoring against an independently constrained box LP."""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,math
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
MATRIX=HERE.parent/'artifacts/hopper-retained-v1/selected-summary-matrix.csv'
ARMS=['PULL','PULL_FLAT','PUSH_ST','GLOBAL','PUSH_BULK','PUSH_STASYNC']
POS={'PULL':1,'PUSH_ST':2,'PUSH_BULK':3,'GLOBAL':4,'PUSH_STASYNC':5,'PULL_FLAT':6}
GRID=[0,.005,.01,.02,.05,.10]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def expression(p,q):
    a=[0.]*12
    if p!=q:
        a[ARMS.index(p)]=1;a[ARMS.index(q)]=-1
        a[6+ARMS.index(p)]=-1;a[6+ARMS.index(q)]=1
    return a
def path(L,U,p,q,d):return 0. if p==q else math.log(U[p]/L[q])+d*abs(POS[p]-POS[q])
def box(L,U,p,q,d,a):return 0. if p==q else math.log(U[p]/L[q])+d*(abs(POS[p]-a)+abs(POS[q]-a))
def main():
    out=HERE/'HOPPER_R6_ANCHOR_RESULTS.json';assert not out.exists()
    cells=defaultdict(dict)
    with MATRIX.open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            cells[(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))][r['arm']]={k:float(r[k]) for k in ['min_ns','max_ns']}
    assert len(cells)==89
    npair=nfeas=0;maxerr=0.;reports=[]
    for f in GRID:
        d=math.log1p(f);counts={a:0 for a in range(7)};pathunique=centerunique=0
        for key,row in sorted(cells.items()):
            L={p:row[p]['min_ns'] for p in ARMS};U={p:row[p]['max_ns'] for p in ARMS}
            for a in counts:
                counts[a]+=any(all(box(L,U,p,q,d,a)<-1e-12 for q in ARMS if q!=p) for p in ARMS)
            pu=cu=False
            for p in ARMS:
                assert all(abs(box(L,U,p,q,d,POS[p])-path(L,U,p,q,d))<1e-12 for q in ARMS)
                possible=all(math.log(L[p]/U[q])<=d*abs(POS[p]-POS[q])+1e-12 for q in ARMS if q!=p)
                unique=all(path(L,U,p,q,d)<-1e-12 for q in ARMS if q!=p)
                centered=all(box(L,U,p,q,d,POS[p])<-1e-12 for q in ARMS if q!=p)
                assert unique==centered;pu|=unique;cu|=centered
                if f==.02:
                    bounds=[(math.log(L[q]),math.log(U[q])) for q in ARMS]+[(-d*abs(POS[q]-POS[p]),d*abs(POS[q]-POS[p])) for q in ARMS]
                    cons=[]
                    for q in ARMS:
                        if p==q:continue
                        a=expression(p,q);lp=linprog([-v for v in a],bounds=bounds,method='highs');assert lp.success
                        err=abs(-lp.fun-path(L,U,p,q,d));maxerr=max(maxerr,err);assert err<1e-9
                        cons.append(a);npair+=1
                    lp=linprog([0.]*12,A_ub=cons,b_ub=[0.]*5,bounds=bounds,method='highs')
                    assert lp.success==possible,(key,p,lp.message);nfeas+=1
            pathunique+=pu;centerunique+=cu
        reports.append({'adjacent_fraction':f,'path_unique_count':pathunique,'candidate_centered_unique_count':centerunique,'common_anchor_unique_counts':counts})
    L={'S':913.8,'P':962.6};U={'S':916.5,'P':965.0};d=math.log1p(.02)
    fixture={'S_interval':[L['S'],U['S']],'P_interval':[L['P'],U['P']],'positions':[2,1],
      'path_ratio_upper':U['S']/L['P']*math.exp(d),'box_anchor0_ratio_upper':U['S']/L['P']*math.exp(3*d),
      'box_anchor1_ratio_upper':U['S']/L['P']*math.exp(d)}
    result={'result':'PASS_CANDIDATE_CENTERED_BOX_EQUALS_PATH_QUERY_OUTPUTS','protocol_sha256':sha(HERE/'HOPPER_R6_ANCHOR_PROTOCOL.json'),
      'script_sha256':sha(Path(__file__)),'matrix_sha256':sha(MATRIX),'new_native_measurements':0,
      'checks':{'candidate_centered_pair_LPs':npair,'simultaneous_winner_LPs':nfeas,'maximum_support_error':maxerr,'disagreements':0},
      'all_common_anchor_reports':reports,'worked_reanchoring_example':fixture,
      'scope':'Query-dependent boxes have the same candidate-wise path observations, not the same joint set. Original floor0 comparisons remain numerically valid but anchor-dependent; not inherent superiority over reanchored interval baselines.'}
    assert npair==2670 and nfeas==534
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
