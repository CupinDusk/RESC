"""Explicit printed-input cycle and a simple boundary path, not new data."""
from pathlib import Path
import hashlib,json,math
HERE=Path(__file__).resolve().parent
def main():
 out=HERE/'HOPPER_R9_H20_CERTIFICATE.json';assert not out.exists()
 intervals={'F':[2213.4,2226.4],'P':[2160.,2173.1],'B':[2788.5,2793.1],'A':[2792.6,2796.8]}
 slots={'F':6,'P':1,'B':3,'A':5}
 h1=math.log(intervals['F'][0]/intervals['P'][1]);h2=math.log(intervals['B'][0]/intervals['A'][1]);d=(h1+h2)/3
 bias=[0.,0.,d,2*d,2*d,2*d-h2,h1]
 x={a:math.log(intervals[a][0 if a in ['F','B'] else 1]) for a in intervals}
 theta={a:x[a]-bias[slots[a]] for a in intervals}
 steps=[abs(y-x) for x,y in zip(bias,bias[1:])]
 assert max(steps)<=d+1e-14 and max(abs(theta['F']-theta['P']),abs(theta['B']-theta['A']))<1e-14
 delta=math.log1p(.005);negative=3*delta-h1-h2;assert negative<0
 r={'result':'PASS_EXPLICIT_H20_CYCLE_AND_TIE_ATTAINING_PATH','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'intervals_ns':intervals,'positions':slots,'h1':h1,'h2':h2,'minimum_shared_budget':d,'assumed_fraction':.005,'assumed_delta':delta,'negative_cycle_sum':negative,'cycle':['b1-b6 <= -h1','b5-b3 <= -h2','b6-b5 <= delta','b3-b1 <= 2delta'],'attaining_x_logs':x,'attaining_bias_b0_to_b6':bias,'attaining_theta':theta,'maximum_adjacent_increment':max(steps),'admission_at_threshold':'Both requested comparisons hold with ties; this is one hypothetical explanation, not device state.'}
 out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r))
if __name__=='__main__':main()
