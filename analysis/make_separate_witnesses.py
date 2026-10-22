from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent
source=HERE.parent/'expected/HOPPER_R18_EXPOSITION_RESULTS.json'
d=json.loads(source.read_text())['two_clause']; old=d['rational_upper_original_variable_witness']
positions=d['positions'];x={a:F(v) for a,v in old['x'].items()};delta=F(7,100)
out={'source':'expected/HOPPER_R18_EXPOSITION_RESULTS.json','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'declared_delta':str(delta),'positions':positions,'x':{a:str(v) for a,v in x.items()},
 'scope':'Posthoc exposition of an existing rectangle. Each separate path is a mathematical witness; no physical GPU bias inferred.',
 'endpoint_membership':'x is byte-identical to the existing outward-tightened R18 rational witness; no new endpoint sampling.',
 'separate_witnesses':{}}
for name,b,claim in [('P_le_F',[F(0)]*7,('P','F')),('A_le_S',[F(0),F(0),F(0),delta,2*delta,3*delta,3*delta],('A','S'))]:
 theta={a:x[a]-b[j] for a,j in positions.items()}
 assert b[0]==0 and all(abs(b[j]-b[j-1])<=delta for j in range(1,7))
 assert theta[claim[0]]<=theta[claim[1]]
 assert any(theta[p]>theta[q] for p,q in d['R'])
 out['separate_witnesses'][name]={'b':[str(v) for v in b],'b_float':[float(v) for v in b],
  'theta':{a:str(v) for a,v in theta.items()},'theta_float':{a:float(v) for a,v in theta.items()},
  'claim':list(claim),'claim_margin':str(theta[claim[1]]-theta[claim[0]]),
  'claim_margin_float':float(theta[claim[1]]-theta[claim[0]]),
  'both_claims':{p+'_le_'+q:theta[p]<=theta[q] for p,q in d['R']}}
out['joint_rejection']={'cycle':['P','S','A','F','P'],
 'upper_weight_at_delta':d['cycle_upper_at_delta'],'upper_weight_float':d['cycle_upper_approx'],
 'every_anchor_box_admits':True,'shared_path_admits':False,'beta':d['beta_approx'],
 'minimum_bracket':d['minimum_bracket_approx'],'restricted_cost':8,'free_cost':2,'sharp_factor':4}
assert F(out['joint_rejection']['upper_weight_at_delta'])<0
out['result']='PASS_EXACT_RATIONAL_ADJACENT_BOUNDS_AND_EACH_SEPARATE_CLAIM_JOINT_NEGATIVE_CYCLE'
(HERE/'SEPARATE_PATH_WITNESSES.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
print(json.dumps({'result':out['result'],'path':str(HERE/'SEPARATE_PATH_WITNESSES.json')},indent=2))
