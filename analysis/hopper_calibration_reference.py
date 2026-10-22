"""Prespecified stationary no-order controls; preserve chronological outcomes."""
from pathlib import Path
from collections import Counter
import hashlib,json,math
import numpy as np
import ordersage_secondary as old
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stats(x):
 x=np.asarray(x,dtype=float)
 return {'mean':float(x.mean()),'minimum':float(x.min()),'q05':float(np.quantile(x,.05)),'median':float(np.median(x)),'q95':float(np.quantile(x,.95)),'maximum':float(x.max())}
def reference(rng,k,m,R=10000,batch=500):
 counts={s:[] for s in ['known_center','same_calibration_fitted_center','independently_fitted_center']};ratios={s:[] for s in counts}
 def scores(x,c,order):
  z=np.take_along_axis(x-c[:,None,:],order,axis=2)
  return np.abs(np.diff(z,axis=2)).max(axis=2)
 for off in range(0,R,batch):
  n=min(batch,R-off)
  cal=rng.standard_normal((n,m,k));test=rng.standard_normal((n,m,k));ind=rng.standard_normal((n,m,k))
  co=rng.random((n,m,k)).argsort(axis=2);to=rng.random((n,m,k)).argsort(axis=2)
  fitted={'known_center':np.zeros((n,k)),'same_calibration_fitted_center':cal.mean(axis=1),'independently_fitted_center':ind.mean(axis=1)}
  for s,c in fitted.items():
   d=scores(cal,c,co).max(axis=1);ass=scores(test,c,to)
   counts[s].extend((ass>d[:,None]+1e-12).sum(axis=1).tolist());ratios[s].extend((ass.max(axis=1)/d).tolist())
 out={}
 for s,x in counts.items():
  a=np.asarray(x);anyp=float((a>0).mean())
  out[s]={'exceedances':stats(a),'exceedance_count_histogram':dict(sorted(Counter(x).items())),'probability_any_exceedance':anyp,'Monte_Carlo_SE_probability_any':math.sqrt(anyp*(1-anyp)/R),'Monte_Carlo_SE_mean_exceedances':float(a.std(ddof=1)/math.sqrt(R)),'maximum_required_to_calibration_ratio':stats(ratios[s])}
 return {'arms':k,'calibration_episodes':m,'assessment_episodes':m,'replications':R,'analytic_fixed_score_iid_reference':{'expected_exceedances':m/(m+1),'probability_any_exceedance':.5},'scenarios':out}
def worked(arms,g,delta):
 details=[]
 for task in sorted({a.removeprefix('bash -i ').removesuffix('.sh').split('.',1)[1] for a in arms}):
  pair=sorted(a for a in arms if a.removeprefix('bash -i ').removesuffix('.sh').split('.',1)[1]==task);assert len(pair)==2
  for e in g['fixed']['assessment']:
   p=next(a for a in pair if '.ufs.' in a or a.removeprefix('bash -i ').startswith('ufs.'));q=next(a for a in pair if a!=p)
   by={r['arm']:r for r in e['rows']};rp,rq=by[p],by[q]
   support=-rp['x']+rq['x']+delta*abs(rp['j']-rq['j'])
   ranges={a:[min(math.exp(r['x']) for ep in g['random']['assessment'] for r in ep['rows'] if r['arm']==a),max(math.exp(r['x']) for ep in g['random']['assessment'] for r in ep['rows'] if r['arm']==a)] for a in pair}
   details.append({'task':task,'fixed_run_num':e['run_num'],'ufs_command':p,'ext4nj_command':q,'ufs_throughput':math.exp(rp['x']),'ext4nj_throughput':math.exp(rq['x']),'ufs_original_slot':rp['j'],'ext4nj_original_slot':rq['j'],'slot_distance':abs(rp['j']-rq['j']),'point_cost_ufs':-rp['x'],'point_cost_ext4nj':-rq['x'],'frozen_delta':delta,'worst_log_ufs_over_ext4nj_cost_ratio':support,'certificate':'ufs_strictly_better' if support<0 else 'abstain','observed_random_throughput_ranges':ranges})
 assert len(details)==50
 return {'queries':details,'lexicographically_first_certified':next(d for d in details if d['certificate']=='ufs_strictly_better'),'lexicographically_first_abstained':next(d for d in details if d['certificate']=='abstain')}
def main():
 out=HERE/'HOPPER_R7_CALIBRATION_REFERENCE_RESULTS.json';assert not out.exists()
 rng=np.random.default_rng(20261021);sims={};sensitivity={};worked_ufs=None
 oldreport=json.loads((HERE/'ORDERSAGE_SECONDARY_RESULTS.json').read_text(encoding='utf-8'))
 for case,k,m in [('memcached',3,25),('npbench',3,50),('ufs',20,5)]:
  sims[case]=reference(rng,k,m)
  arms,g,rows=old.load(case);entries=[]
  for shift in range(5):
   rotated={}
   for o,v in g.items():
    full=v['calibration']+v['assessment'];n=len(full);off=(shift*n)//5;seq=full[off:]+full[:off]
    rotated[o]={'calibration':seq[:n//2],'assessment':seq[n//2:]}
   c=old.centers(arms,rotated['random']['calibration']);d=max(s for ep in rotated['random']['calibration'] for s in old.edge_scores(ep,c))
   v={o:old.coverage(v['assessment'],c,d) for o,v in rotated.items()}
   entries.append({'cyclic_shift_index':shift,'random_offset':(shift*2*m)//5,'delta':d,'coverage':v})
   if shift==0:
    assert d==oldreport['cases'][case]['effective_delta_cal']
    assert v==oldreport['cases'][case]['assessment_with_frozen_calibration_centers']
    if case=='ufs':worked_ufs=worked(arms,rotated,d)
  sensitivity[case]=entries
 result={'result':'COMPLETED_STATIONARY_REFERENCE_ALL_PRESPECIFIED_SCENARIOS_AND_SHIFTS','protocol_sha256':sha(HERE/'HOPPER_R7_JOINT_PROTOCOL.json'),'script_sha256':sha(Path(__file__)),'old_secondary_report_sha256':sha(HERE/'ORDERSAGE_SECONDARY_RESULTS.json'),'numpy_version':np.__version__,'seed':20261021,'generator':'numpy default_rng PCG64; batch500; calibration/test/independent-center standard Gaussians then independent uniform permutation keys, in that order','synthetic_process':'theta=0, independent standard Gaussian log noise by arm and episode; uniformly permuted slots; zero order effect; common noise scale1 by scale equivariance','stationary_simulations':sims,'all_five_dependent_cyclic_split_sensitivities':sensitivity,'ufs_point_queries':worked_ufs,'boundary':'Original chronological results preserved exactly. Known-center iid formulas are illustrative references, not assumptions for the observed corpora. Synthetic controls are not a significance test of actual failures, temporal variation or causal ordering. Same-center fitting is explicitly compared with known/independently fitted centers. All shifts are reported as dependent sensitivity; no preferred split replaces the primary table.'}
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'simulations':sims,'cyclic_coverage':{c:[{'shift':r['cyclic_shift_index'],'delta':r['delta'],'random_covered':r['coverage']['random']['covered_episodes'],'random_n':r['coverage']['random']['episodes']} for r in v] for c,v in sensitivity.items()},'worked_certified':worked_ufs['lexicographically_first_certified'],'worked_abstained':worked_ufs['lexicographically_first_abstained']},indent=2))
if __name__=='__main__':main()
