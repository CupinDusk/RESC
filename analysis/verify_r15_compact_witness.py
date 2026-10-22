"""Check a compact rendering of the existing R13 upper witness claim."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import hopper_exact_certificates as ec
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'HOPPER_R13_WORKED_ORDER_RESULTS.json').read_text())
d=F('.005134328558')
lo={a:F(ec.log_bounds(r['intervals_ns'][a][0])[1],ec.U) for a in ec.ARMS}
up={a:F(ec.log_bounds(r['intervals_ns'][a][1])[0],ec.U) for a in ec.ARMS}
P,S,B,G,A,T='PULL','PUSH_ST','PUSH_BULK','GLOBAL','PUSH_STASYNC','PULL_FLAT'
z=up[A]-lo[B];b=[F(0),d,2*d,3*d,z+2*d,z+3*d,z+4*d]
x={P:up[P],S:up[S],B:lo[B],G:up[G],A:up[A],T:lo[T]}
theta={a:x[a]-b[r['slots'][a]] for a in x}
assert b[0]==0 and all(abs(b[j]-b[j-1])<=d for j in range(1,7))
assert all(lo[a]<=x[a]<=up[a] for a in x)
assert all(theta[p]<=theta[q] for p,q in zip(r['order'],r['order'][1:]))
out=HERE/'HOPPER_R15_COMPACT_WITNESS_CHECK.json';assert not out.exists()
result={'result':'PASS_COMPACT_ORIGINAL_VARIABLE_RATIONAL_UPPER_WITNESS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_r13_result_sha256':hashlib.sha256((HERE/'HOPPER_R13_WORKED_ORDER_RESULTS.json').read_bytes()).hexdigest(),'delta':str(d),'z':str(z),'bias':[str(v) for v in b],'x':{a:str(v) for a,v in x.items()},'theta':{a:str(v) for a,v in theta.items()},'rounded_bias':[round(float(v),6) for v in b],'scope':'Alternative compact witness for the existing upper bound, not a new acquisition or revised numerical minimum. Tightened outward endpoints; every original inequality checked exactly.'}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['z','x','theta','bias']},indent=2))
