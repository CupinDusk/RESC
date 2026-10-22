"""Conditional fixed-position drift audit of the existing public numeric matrix."""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,math
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ARTIFACT=HERE.parent/'artifacts/hopper-retained-v1'
ARMS=['PULL','PULL_FLAT','PUSH_ST','GLOBAL','PUSH_BULK','PUSH_STASYNC']
POS={'PULL':1,'PUSH_ST':2,'PUSH_BULK':3,'GLOBAL':4,'PUSH_STASYNC':5,'PULL_FLAT':6}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def support(L,U,p,q,delta):
    if p==q:return 0.
    return math.log(U[p]/L[q])+delta*abs(POS[p]-POS[q])

def risk(L,U,p,delta):return max(support(L,U,p,q,delta) for q in ARMS)

def bounds_for_lp(L,U,delta):
    # Variables: six latent observed log summaries x, then seven b positions.
    bounds=[(math.log(L[p]),math.log(U[p])) for p in ARMS]+[(0.,0.)]+[(None,None)]*6
    A=[];rhs=[]
    for j in range(6):
        row=[0.]*13;row[6+j+1]=1;row[6+j]=-1;A.append(row);rhs.append(delta)
        A.append([-v for v in row]);rhs.append(delta)
    return bounds,A,rhs

def contrast(p,q):
    a=[0.]*13
    if p!=q:a[ARMS.index(p)]=1;a[ARMS.index(q)]=-1;a[6+POS[p]]=-1;a[6+POS[q]]=1
    return a

def main():
    protocol=HERE/'HOPPER_ORDER_SENSITIVITY_PROTOCOL.json';spec=json.loads(protocol.read_text(encoding='utf-8'))
    matrix=ARTIFACT/'selected-summary-matrix.csv';cells=defaultdict(dict)
    with matrix.open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            key=(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))
            cells[key][r['arm']]={s:float(r[s]) for s in ['primary_ns','min_ns','mean_ns','max_ns']}
    assert len(cells)==89 and sum(map(len,cells.values()))==623
    frozen=json.loads((ARTIFACT/'recomputed-results.json').read_text(encoding='utf-8'))['primary']['cases']
    policy={(r['pattern'],8,r['launched_clusters'],r['payload_B']):r for r in frozen}
    assert len(policy)==35 and sum(r['admitted'] for r in policy.values())==19
    delta=math.log1p(.02);n_lp=n_feas=0;max_error=0.
    for key,row in sorted(cells.items()):
        for model in ['minimum_point','summary_rectangle']:
            L={p:row[p]['min_ns'] for p in ARMS};U={p:row[p]['max_ns' if model=='summary_rectangle' else 'min_ns'] for p in ARMS}
            bounds,A,rhs=bounds_for_lp(L,U,delta)
            for p in ARMS:
                a_rows=[]
                for q in ARMS:
                    if p==q:continue
                    a=contrast(p,q);lp=linprog([-v for v in a],A_ub=A,b_ub=rhs,bounds=bounds,method='highs')
                    assert lp.success,lp.message
                    err=abs(-lp.fun-support(L,U,p,q,delta));max_error=max(max_error,err);assert err<1e-9
                    n_lp+=1;a_rows.append(a)
                lp=linprog([0.]*13,A_ub=A+a_rows,b_ub=rhs+[0.]*len(a_rows),bounds=bounds,method='highs')
                predicted=all(math.log(L[p]/U[q])<=delta*abs(POS[p]-POS[q])+1e-10 for q in ARMS)
                assert lp.success==predicted,(key,p,model,lp.message);n_feas+=1
    reports={};critical=[];main={}
    for model in ['primary_point','minimum_point','mean_point','maximum_point','summary_rectangle']:
        rows=[]
        for frac in spec['grid_adjacent_multiplicative_drift']:
            delta=math.log1p(frac);allcases=[]
            for key,row in sorted(cells.items()):
                field={'primary_point':'primary_ns','minimum_point':'min_ns','mean_point':'mean_ns','maximum_point':'max_ns','summary_rectangle':'min_ns'}[model]
                L={p:row[p][field] for p in ARMS};U={p:row[p]['max_ns' if model=='summary_rectangle' else field] for p in ARMS}
                winners=[p for p in ARMS if all(support(L,U,p,q,delta)<-1e-12 for q in ARMS if q!=p)]
                possible=[p for p in ARMS if all(math.log(L[p]/U[q])<=delta*abs(POS[p]-POS[q])+1e-12 for q in ARMS)]
                assert len(winners)<=1 and possible
                costs={p:risk(L,U,p,delta) for p in ARMS};best=min(ARMS,key=lambda p:costs[p])
                flat_cert=support(L,U,'PULL_FLAT','PULL',delta)<-1e-12
                peer_cert=support(L,U,'PULL','PULL_FLAT',delta)<-1e-12
                item={'key':key,'guaranteed_unique':winners,'possible_winners':possible,'minimax_audit_arm':best,
                      'minimax_log_regret':costs[best],'flat_better_certified':flat_cert,'peer_better_certified':peer_cert}
                if key in policy:item.update({'old_policy':policy[key]['selected'],'admitted':policy[key]['admitted'],'old_policy_log_regret_bound':costs[policy[key]['selected']]})
                allcases.append(item)
                if frac==0 and model=='summary_rectangle':
                    nominal=min(ARMS,key=lambda p:row[p]['min_ns'])
                    threshold=min(math.log(L[q]/U[nominal])/abs(POS[q]-POS[nominal]) for q in ARMS if q!=nominal)
                    critical.append({'key':key,'nominal_min_arm':nominal,'critical_delta':threshold,'adjacent_fraction':math.expm1(threshold),'strictly_separated_at_zero':threshold>0})
                if key==('Nto1',8,1,32):
                    main[model+':'+str(frac)]={'flat_peer_log_support':support(L,U,'PULL_FLAT','PULL',delta),'flat_peer_ratio_upper':math.exp(support(L,U,'PULL_FLAT','PULL',delta)),
                        'critical_flat_advantage_adjacent_fraction':math.expm1(math.log(L['PULL']/U['PULL_FLAT'])/5),
                        **item}
            group={}
            for name,pred in [('all',lambda r:True),('admitted',lambda r:'old_policy' in r and r['admitted']),('unsupported',lambda r:'old_policy' in r and not r['admitted']),('test35',lambda r:'old_policy' in r)]:
                selected=[r for r in allcases if pred(r)]
                group[name]={'cells':len(selected),'guaranteed_unique_winners':sum(bool(r['guaranteed_unique']) for r in selected),
                    'possible_winner_count_histogram':{str(n):sum(len(r['possible_winners'])==n for r in selected) for n in range(1,7)},
                    'audit_minimax_regret_geometric':math.exp(sum(r['minimax_log_regret'] for r in selected)/len(selected)),
                    'audit_minimax_regret_maximum':math.exp(max(r['minimax_log_regret'] for r in selected))}
                if name!='all':group[name].update({'old_policy_regret_bound_geometric':math.exp(sum(r['old_policy_log_regret_bound'] for r in selected)/len(selected)),
                    'old_policy_regret_bound_maximum':math.exp(max(r['old_policy_log_regret_bound'] for r in selected))})
            group['peer_flat_by_pattern']={pat:{'cells':sum(r['key'][0]==pat for r in allcases),
                'flat_certified':sum(r['key'][0]==pat and r['flat_better_certified'] for r in allcases),
                'peer_certified':sum(r['key'][0]==pat and r['peer_better_certified'] for r in allcases)} for pat in ['1to1','1toN','Nto1']}
            rows.append({'adjacent_fraction':frac,'delta':delta,'groups':group,'cases':allcases})
        reports[model]=rows
    singleton=math.log(100/1);assert support({'PULL':1},{'PULL':100},'PULL','PULL',1)==0 and singleton>0
    result={'result':'PASS_CONDITIONAL_ORDER_SENSITIVITY_AUDIT','scientific_boundary':spec['scientific_boundary'],'new_native_measurements':0,
        'protocol_sha256':sha(protocol),'script_sha256':sha(Path(__file__)),'selected_matrix_sha256':sha(matrix),'existing_policy_result_sha256':sha(ARTIFACT/'recomputed-results.json'),
        'checks':{'lp_pair_support_instances':n_lp,'lp_possible_winner_feasibility_instances':n_feas,'maximum_lp_support_error':max_error,'disagreements':0,'self_contrast_control':'PASS'},
        'reports':reports,'critical_summary_rectangle_winner_thresholds':critical,'main_case':main}
    (HERE/'HOPPER_ORDER_SENSITIVITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    compact={model:[{'adjacent':r['adjacent_fraction'],'all_winners':r['groups']['all']['guaranteed_unique_winners'],
        'peer_flat':r['groups']['peer_flat_by_pattern'],'test35':r['groups']['test35']} for r in rows] for model,rows in reports.items() if model in ['minimum_point','summary_rectangle']}
    print(json.dumps({'result':result['result'],'checks':result['checks'],'selected':compact}))

if __name__=='__main__':main()
