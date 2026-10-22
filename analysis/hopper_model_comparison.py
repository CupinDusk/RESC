"""Matched bias-model, simultaneous-feasibility and misspecification audit."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,math,statistics
from scipy.optimize import linprog
from hopper_order_sensitivity import ARMS,POS,bounds_for_lp,contrast,support
HERE=Path(__file__).resolve().parent;ARTIFACT=HERE.parent/'artifacts/hopper-retained-v1'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pair(L,U,p,q,delta,model,gamma=0.):
    if p==q:return 0.
    distance=POS[p]+POS[q] if model=='independent_marginals' else abs(POS[p]-POS[q])
    return math.log(U[p]/L[q])+delta*distance+(2*gamma if model=='path_plus_arm_residual' else 0.)
def possible(L,U,p,delta,model,gamma=0.):
    if model=='linear_slope':
        low,high=-delta,delta
        for q in ARMS:
            if q==p:continue
            slope=math.log(L[p]/U[q])/(POS[p]-POS[q])
            if POS[p]>POS[q]:low=max(low,slope)
            else:high=min(high,slope)
        return low<=high+1e-12
    return all(math.log(L[p]/U[q])<=delta*(POS[p]+POS[q] if model=='independent_marginals' else abs(POS[p]-POS[q]))+(2*gamma if model=='path_plus_arm_residual' else 0.)+1e-12 for q in ARMS if q!=p)

def lp_problem(L,U,delta,model,gamma):
    n=6
    if model=='linear_slope':
        bounds=[(math.log(L[p]),math.log(U[p])) for p in ARMS]+[(-delta,delta)]
        A=[];rhs=[]
        def expression(p,q):
            a=[0.]*7
            if p!=q:a[ARMS.index(p)]=1;a[ARMS.index(q)]=-1;a[6]=POS[q]-POS[p]
            return a
    elif model=='independent_marginals':
        bounds=[(math.log(L[p]),math.log(U[p])) for p in ARMS]+[(-POS[p]*delta,POS[p]*delta) for p in ARMS]
        A=[];rhs=[]
        def expression(p,q):
            a=[0.]*12
            if p!=q:a[ARMS.index(p)]=1;a[ARMS.index(q)]=-1;a[6+ARMS.index(p)]=-1;a[6+ARMS.index(q)]=1
            return a
    else:
        bounds,A,rhs=bounds_for_lp(L,U,delta)
        bounds=bounds+[(-gamma,gamma)]*6;A=[r+[0.]*6 for r in A]
        def expression(p,q):
            a=contrast(p,q)+[0.]*6
            if p!=q:a[13+ARMS.index(p)]=-1;a[13+ARMS.index(q)]=1
            return a
    return bounds,A,rhs,expression

def gm(values):return math.exp(sum(values)/len(values))
def main():
    protocol=HERE/'HOPPER_R5_MODEL_PROTOCOL.json';spec=json.loads(protocol.read_text(encoding='utf-8'))
    matrix=ARTIFACT/'selected-summary-matrix.csv';frozenpath=ARTIFACT/'recomputed-results.json';cells=defaultdict(dict)
    with matrix.open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            key=(r['pattern'],int(r['C']),int(r['launched_clusters']),int(r['payload_B']))
            cells[key][r['arm']]={k:float(r[k]) for k in ['min_ns','max_ns','primary_ns']}
    frozen=json.loads(frozenpath.read_text(encoding='utf-8'))['primary']['cases']
    policy={(r['pattern'],8,r['launched_clusters'],r['payload_B']):r for r in frozen};assert len(cells)==89 and len(policy)==35
    n_pair=n_feas=0;maxerr=0.
    for key,row in sorted(cells.items()):
        L={p:row[p]['min_ns'] for p in ARMS};U={p:row[p]['max_ns'] for p in ARMS};delta=math.log1p(.02);gamma=math.log1p(.005)
        for model in ['linear_slope','independent_marginals','path_plus_arm_residual']:
            bounds,A,rhs,expr=lp_problem(L,U,delta,model,gamma)
            for p in ARMS:
                candidates=[]
                for q in ARMS:
                    if p==q:continue
                    a=expr(p,q);lp=linprog([-v for v in a],A_ub=A or None,b_ub=rhs or None,bounds=bounds,method='highs')
                    assert lp.success,lp.message
                    error=abs(-lp.fun-pair(L,U,p,q,delta,model,gamma));maxerr=max(maxerr,error);assert error<1e-9
                    candidates.append(a);n_pair+=1
                lp=linprog([0.]*len(bounds),A_ub=A+candidates,b_ub=rhs+[0.]*len(candidates),bounds=bounds,method='highs')
                assert lp.success==possible(L,U,p,delta,model,gamma),(key,p,model,lp.message);n_feas+=1
    reports=[];radii=[];residual_radii=[]
    for f in spec['declared_grids']['adjacent_fractions']:
        delta=math.log1p(f)
        for model,g_values in [('linear_slope',[0]),('shared_path',[0]),('independent_marginals',[0]),('path_plus_arm_residual',spec['declared_grids']['arm_residual_upper_fractions'])]:
            for frac in g_values:
                gamma=math.log1p(frac);cases=[]
                for key,row in sorted(cells.items()):
                    L={p:row[p]['min_ns'] for p in ARMS};U={p:row[p]['max_ns'] for p in ARMS}
                    risks={p:max(pair(L,U,p,q,delta,model,gamma) for q in ARMS) for p in ARMS}
                    unique=[p for p in ARMS if all(pair(L,U,p,q,delta,model,gamma)<-1e-12 for q in ARMS if q!=p)]
                    possible_set=[p for p in ARMS if possible(L,U,p,delta,model,gamma)];assert possible_set
                    item={'key':key,'guaranteed_unique':unique,'possible_winners':possible_set,'minimax_audit_arm':min(ARMS,key=lambda p:risks[p]),'log_regrets':risks}
                    if key in policy:item.update({'old_policy':policy[key]['selected'],'admitted':policy[key]['admitted'],'old_policy_log_regret':risks[policy[key]['selected']]})
                    cases.append(item)
                groups={}
                for name,pred in [('all',lambda r:True),('C8',lambda r:r['key'][1]==8),('admitted19',lambda r:r.get('admitted',False)),('all35',lambda r:'old_policy' in r)]:
                    group=[r for r in cases if pred(r)]
                    s={'cells':len(group),'unique_count':sum(bool(r['guaranteed_unique']) for r in group),'possible_count_histogram':dict(Counter(len(r['possible_winners']) for r in group))}
                    if name in ['admitted19','all35']:s.update({'old_policy_geometric_ratio_bound':gm([r['old_policy_log_regret'] for r in group]),'old_policy_max_ratio_bound':math.exp(max(r['old_policy_log_regret'] for r in group))})
                    groups[name]=s
                reports.append({'model':model,'adjacent_fraction':f,'arm_residual_upper_fraction':frac,'groups':groups,'cases':cases})
    for key,row in sorted(cells.items()):
        L={p:row[p]['min_ns'] for p in ARMS};U={p:row[p]['max_ns'] for p in ARMS};p=min(ARMS,key=lambda p:L[p])
        rival=min((q for q in ARMS if q!=p),key=lambda q:math.log(L[q]/U[p])/abs(POS[p]-POS[q]))
        delta_star=math.log(L[rival]/U[p])/abs(POS[p]-POS[rival])
        radii.append({'key':key,'nominal_winner':p,'limiting_rival':rival,'critical_log_slope':delta_star,'adjacent_fraction_radius':math.expm1(delta_star)})
        d=math.log1p(.02);rival=max((q for q in ARMS if q!=p),key=lambda q:pair(L,U,p,q,d,'shared_path'))
        gamma_star=-.5*pair(L,U,p,rival,d,'shared_path')
        residual_radii.append({'key':key,'nominal_winner':p,'limiting_rival':rival,'residual_log_radius_at_adjacent2pct':gamma_star,'residual_upper_fraction_radius':math.expm1(gamma_star)})
    comparisons=[]
    for f in spec['declared_grids']['adjacent_fractions']:
        models={r['model']:r for r in reports if r['adjacent_fraction']==f and r['arm_residual_upper_fraction']==0}
        linear=models['linear_slope']['cases'];path=models['shared_path']['cases'];box=models['independent_marginals']['cases'];different=[];correlation_unique=[]
        for a,b,c in zip(linear,path,box):
            assert a['key']==b['key']==c['key'] and a['log_regrets']==b['log_regrets'] and a['guaranteed_unique']==b['guaranteed_unique']
            assert set(a['possible_winners'])<=set(b['possible_winners'])<=set(c['possible_winners'])
            assert all(b['log_regrets'][p]<=c['log_regrets'][p]+1e-12 for p in ARMS)
            if a['possible_winners']!=b['possible_winners']:different.append({'key':a['key'],'linear':a['possible_winners'],'path':b['possible_winners']})
            if b['guaranteed_unique'] and not c['guaranteed_unique']:correlation_unique.append({'key':b['key'],'winner':b['guaranteed_unique'][0]})
        comparisons.append({'adjacent_fraction':f,'same_linear_path_pair_support_and_regret':True,'different_linear_path_possible_sets':different,'path_unique_box_ambiguous':correlation_unique})
    # Controlled three-arm geometry: pair supports agree, common feasibility differs.
    pos=[1,2,3];x=[0.,.01,0.];delta=.01;p=1
    low=max([-delta]+[(x[p]-x[q])/(pos[p]-pos[q]) for q in [0]])
    high=min([delta]+[(x[p]-x[q])/(pos[p]-pos[q]) for q in [2]])
    cone=[-delta*abs(j-pos[p])+delta*pos[p] for j in pos];theta=[a-b for a,b in zip(x,cone)]
    assert low>high and theta[p]<=min(theta)+1e-12
    # Controlled model violation: one unmodelled residual defeats a path-only guarantee.
    logs={p:(0. if p=='PULL' else .03 if p=='PULL_FLAT' else 1.) for p in ARMS};d=.002;gamma=.011
    assert all(logs['PULL']-logs[q]+d*abs(POS['PULL']-POS[q])<0 for q in ARMS if q!='PULL')
    biases={p:d*POS[p] for p in ARMS};residual={p:(-gamma if p=='PULL' else gamma if p=='PULL_FLAT' else 0.) for p in ARMS}
    theta2={p:logs[p]-biases[p]-residual[p] for p in ARMS};assert theta2['PULL']>theta2['PULL_FLAT']
    fixtures={'linear_path_equal_pair_support_not_equal_possible_winner':{'positions':pos,'log_observed_costs':x,'delta':delta,'candidate_index':p,'slope_interval':[low,high],'linear_possible':False,'path_possible':True,'attaining_cone_bias':cone,'attaining_theta':theta},
              'arm_residual_violation':{'log_observed_costs':logs,'delta':d,'gamma':gamma,'bias':biases,'arm_residual':residual,'attaining_theta':theta2,'path_only_guaranteed':'PULL','actual_better_in_constructed_misspecification':'PULL_FLAT'}}
    positive=sorted((r for r in radii if r['critical_log_slope']>0),key=lambda r:(r['critical_log_slope'],r['key']))
    residualpositive=sorted((r for r in residual_radii if r['residual_log_radius_at_adjacent2pct']>0),key=lambda r:(r['residual_log_radius_at_adjacent2pct'],r['key']))
    summaries={'adjacent_positive':{'n':len(positive),'min':positive[0]['adjacent_fraction_radius'],'median':statistics.median(r['adjacent_fraction_radius'] for r in positive),'max':positive[-1]['adjacent_fraction_radius'],'three_smallest':positive[:3],'three_largest':positive[-3:]},
               'residual_positive_at_adjacent2pct':{'n':len(residualpositive),'min':residualpositive[0]['residual_upper_fraction_radius'],'median':statistics.median(r['residual_upper_fraction_radius'] for r in residualpositive),'max':residualpositive[-1]['residual_upper_fraction_radius'],'counts_at_or_below_declared_residual':{str(f):sum(r['residual_upper_fraction_radius']<=f for r in residualpositive) for f in spec['declared_grids']['arm_residual_upper_fractions']},'three_smallest':residualpositive[:3],'three_largest':residualpositive[-3:]}}
    out={'result':'PASS_HOPPER_MATCHED_MODEL_COMPARISON','protocol_sha256':sha(protocol),'script_sha256':sha(Path(__file__)),'selected_matrix_sha256':sha(matrix),'frozen_original_choices_sha256':sha(frozenpath),
         'new_native_measurements':0,'checks':{'pair_support_LPs':n_pair,'winner_feasibility_LPs':n_feas,'maximum_support_error':maxerr,'disagreements':0},'reports':reports,'model_comparisons':comparisons,'winner_radii':radii,'residual_radii':residual_radii,'radius_summary':summaries,'controlled_mathematical_fixtures':fixtures,'scientific_boundary':spec['scientific_boundary']}
    (HERE/'HOPPER_R5_MODEL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    compact=[{'model':r['model'],'f':r['adjacent_fraction'],'g':r['arm_residual_upper_fraction'],'groups':r['groups']} for r in reports if r['model']!='path_plus_arm_residual' or r['adjacent_fraction']==.02]
    print(json.dumps({'result':out['result'],'checks':out['checks'],'comparisons':[{k:(len(v) if isinstance(v,list) else v) for k,v in r.items()} for r in comparisons],'reports':compact,'radius_summary':summaries}))
if __name__=='__main__':main()
