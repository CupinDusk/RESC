"""Prespecified secondary assessment of published, independently acquired data.

Only local pinned CSV inputs are read. No third-party code or remote job is run.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,math,statistics
HERE=Path(__file__).resolve().parent
INPUT=HERE/'external-ordersage-inputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def episode_key(r):return tuple(r[k] for k in ['run_uuid','hostname','run_num','order_type'])
def load(case):
    tests=read(INPUT/(case+'_tests.csv'));runs=read(INPUT/(case+'_runs.csv'))
    metadata={episode_key(r):r for r in runs};assert len(metadata)==len(runs)
    groups=defaultdict(list);field='exp_command' if case=='memcached' else 'test_command'
    commands=sorted({r[field] for r in tests})
    for r in tests:
        assert r['completion_status']=='Success'
        y=float(r['result']);assert math.isfinite(y) and y>0
        groups[episode_key(r)].append({'arm':r[field],'j':int(r['order_number']),'x':math.log(y)})
    assert set(groups)==set(metadata)
    ordergroups={}
    for order in ['fixed','random']:
        keys=sorted((k for k in groups if k[3]==order),key=lambda k:(int(k[2]),metadata[k]['time_start'],k[0]))
        assert keys and len(keys)%2==0
        eps=[]
        for k in keys:
            rows=sorted(groups[k],key=lambda r:r['j'])
            assert len(rows)==len(commands) and {r['arm'] for r in rows}==set(commands)
            assert [r['j'] for r in rows]==list(range(len(commands)))
            eps.append({'run_num':int(k[2]),'rows':rows})
        if order=='fixed':assert len({tuple(r['arm'] for r in e['rows']) for e in eps})==1
        ordergroups[order]={'calibration':eps[:len(eps)//2],'assessment':eps[len(eps)//2:]}
    assert sum(len(v[t]) for v in ordergroups.values() for t in v)==len(groups)
    return commands,ordergroups,len(tests)
def centers(commands,episodes):
    return {a:statistics.mean(r['x'] for e in episodes for r in e['rows'] if r['arm']==a) for a in commands}
def edge_scores(e,c):
    z=[r['x']-c[r['arm']] for r in e['rows']]
    return [abs(b-a) for a,b in zip(z,z[1:])]
def coverage(episodes,c,delta):
    entries=[(e['run_num'],edge_scores(e,c)) for e in episodes]
    scores=[max(s) for n,s in entries]
    return {'episodes':len(entries),'covered_episodes':sum(s<=delta+1e-12 for s in scores),
      'adjacent_constraints':sum(len(s) for n,s in entries),'violated_adjacent_constraints':sum(v>delta+1e-12 for n,s in entries for v in s),
      'maximum_required_delta':max(scores),'maximum_to_calibration_ratio':max(scores)/delta if delta else None,
      'episode_scores':[{'run_num':n,'required_delta':max(s),'covered':max(s)<=delta+1e-12} for n,s in entries]}
def unique_pair(rows,arms,delta,model):
    byarm={r['arm']:r for r in rows};ok=[]
    for a in arms:
        p=byarm[a];q=byarm[next(b for b in arms if b!=a)]
        # uFS result is throughput; cost is -log(result).
        penalty=0 if model=='naive' else delta*(p['j']+q['j']) if model=='floor0_box' else delta*abs(p['j']-q['j'])
        support=-p['x']+q['x']+penalty
        if support<0:ok.append(a)
    assert len(ok)<=1
    return ok[0] if ok else None
def rankings(commands,groups,delta):
    pairs=defaultdict(list)
    for a in commands:
        stem=a.removeprefix('bash -i ').removesuffix('.sh');fs,task=stem.split('.',1)
        assert fs in ['ufs','ext4nj'];pairs[task].append(a)
    assert len(pairs)==10 and all(len(v)==2 for v in pairs.values())
    ref=groups['random']['assessment'];fixed=groups['fixed']['assessment']
    reports={m:Counter() for m in ['naive','path','floor0_box','candidate_centered_box']};details=[]
    for task,arms in sorted(pairs.items()):
        ranges={a:[min(-r['x'] for e in ref for r in e['rows'] if r['arm']==a),max(-r['x'] for e in ref for r in e['rows'] if r['arm']==a)] for a in arms}
        refwinner=next((a for a in arms if ranges[a][1]<ranges[next(b for b in arms if b!=a)][0]),None)
        decisions=[]
        for e in fixed:
            choices={m:unique_pair(e['rows'],arms,delta,m) for m in reports}
            assert choices['path']==choices['candidate_centered_box']
            for model,choice in choices.items():
                outcome='abstain' if choice is None else 'unique_reference_ambiguous' if refwinner is None else 'unique_agrees' if choice==refwinner else 'unique_contradicts'
                reports[model][outcome]+=1
            decisions.append({'run_num':e['run_num'],'choices':choices})
        a,b=sorted(arms)
        fixedgaps=[next(-r['x'] for r in e['rows'] if r['arm']==a)-next(-r['x'] for r in e['rows'] if r['arm']==b) for e in fixed]
        randomgap=statistics.mean(next(-r['x'] for r in e['rows'] if r['arm']==a)-next(-r['x'] for r in e['rows'] if r['arm']==b) for e in ref)
        details.append({'task':task,'arms':arms,'heldout_random_observed_cost_ranges':ranges,'reference_separated_winner':refwinner,
          'gap_arm_order':[a,b],'heldout_fixed_mean_cost_gap':statistics.mean(fixedgaps),'heldout_random_mean_cost_gap':randomgap,'decisions':decisions})
    labels=['abstain','unique_reference_ambiguous','unique_agrees','unique_contradicts']
    return {'tasks':len(pairs),'fixed_assessment_episodes':len(fixed),'queries':len(pairs)*len(fixed),
      'random_reference_episodes':len(ref),'reference_separated_tasks':sum(d['reference_separated_winner'] is not None for d in details),
      'cross_tabs':{m:{k:c[k] for k in labels} for m,c in reports.items()},'details':details}
def main():
    out=HERE/'ORDERSAGE_SECONDARY_RESULTS.json';assert not out.exists()
    spec=json.loads((HERE/'ORDERSAGE_SECONDARY_PROTOCOL.json').read_text(encoding='utf-8'))
    manifest=json.loads((INPUT/'MANIFEST.json').read_text(encoding='utf-8'))
    for f in manifest['files']:assert sha(INPUT/f['alias'])==f['sha256']
    cases={}
    for case in ['memcached','npbench','ufs']:
        arms,g,n=load(case);c=centers(arms,g['random']['calibration'])
        delta=max(v for e in g['random']['calibration'] for v in edge_scores(e,c));assert delta>0
        ref=centers(arms,g['random']['assessment'])
        result={'commands':len(arms),'rows':n,'calibration_episodes_per_type':{o:len(v['calibration']) for o,v in g.items()},
          'assessment_episodes_per_type':{o:len(v['assessment']) for o,v in g.items()},'effective_delta_cal':delta,
          'exp_delta_minus1':math.expm1(delta),'assessment_with_frozen_calibration_centers':{o:coverage(v['assessment'],c,delta) for o,v in g.items()},
          'descriptive_assessment_with_heldout_random_reference_centers':{o:coverage(v['assessment'],ref,delta) for o,v in g.items()}}
        if case=='ufs':result['matched_pair_assessment']=rankings(arms,g,delta)
        cases[case]=result
    result={'result':'COMPLETED_PRESPECIFIED_SECONDARY_ASSESSMENT_ALL_CASES','protocol_sha256':sha(HERE/'ORDERSAGE_SECONDARY_PROTOCOL.json'),
      'script_sha256':sha(Path(__file__)),'input_manifest_sha256':sha(INPUT/'MANIFEST.json'),'cases':cases,
      'new_acquisitions':0,'hopper_calibration':False,'source_of_measurements':'independent published OrderSage corpus',
      'scientific_boundary':spec['comparison_boundary']}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    brief={k:{'rows':v['rows'],'delta':v['effective_delta_cal'],'calibration_episodes':v['calibration_episodes_per_type'],
      'coverage':{o:{x:c[x] for x in ['episodes','covered_episodes','violated_adjacent_constraints','maximum_to_calibration_ratio']} for o,c in v['assessment_with_frozen_calibration_centers'].items()}} for k,v in cases.items()}
    brief['ufs_pair_counts']=cases['ufs']['matched_pair_assessment']['cross_tabs']
    print(json.dumps(brief,indent=2))
if __name__=='__main__':main()
