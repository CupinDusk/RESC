"""Constructive settled-clock model; exact controller/times and outward log audit."""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction
from itertools import permutations
import collections,gzip,hashlib,json
HERE=Path(__file__).resolve().parent
SCALE=10**60
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def log_bounds(v):
    assert 0<v.numerator<10**50 and 0<v.denominator<10**50
    with localcontext() as c:
        c.prec=100
        a=Decimal(v.numerator).ln()-Decimal(v.denominator).ln()
        e=Decimal('1e-90')
        lo=int(((a-e)*SCALE).to_integral_value(rounding=ROUND_FLOOR))
        hi=int(((a+e)*SCALE).to_integral_value(rounding=ROUND_CEILING))
    assert lo<=hi
    return lo,hi
def ratio_string(v):return f'{v.numerator}/{v.denominator}'
def bf(mat):
    n=len(mat);d=[0]*n;pre=[None]*n;last=None
    for turn in range(n):
        last=None
        for a in range(n):
            for b in range(n):
                if a==b:continue
                if d[b]>d[a]+mat[a][b]:
                    d[b]=d[a]+mat[a][b];pre[b]=a;last=b
        if last is None:
            assert all(d[b]-d[a]<=mat[a][b] for a in range(n) for b in range(n))
            return True,dict(potential=d)
    v=last
    for _ in range(n):v=pre[v];assert v is not None
    nodes=[v];cur=pre[v]
    while cur!=v:
        assert cur is not None and cur not in nodes
        nodes.append(cur);cur=pre[cur]
    nodes.reverse();edges=[(nodes[i],nodes[(i+1)%len(nodes)]) for i in range(len(nodes))]
    weights=[mat[a][b] for a,b in edges];assert sum(weights)<0
    return False,dict(cycle=edges,weights=weights,total=sum(weights))
def floyd(mat):
    m=[row[:] for row in mat];n=len(m)
    for k in range(n):
        for a in range(n):
            for b in range(n):m[a][b]=min(m[a][b],m[a][k]+m[k][b])
    return all(m[i][i]>=0 for i in range(n))
def matrix(bounds,delta,R,tight):
    l=[v[1 if tight else 0] for v in bounds['l']]
    u=[v[0 if tight else 1] for v in bounds['u']]
    mat=[[0 if a==b else u[b]-l[a]+delta*abs(a-b) for b in range(6)] for a in range(6)]
    for p,q in R:mat[q][p]=min(0,mat[q][p])
    return mat,l,u
def audit(bounds,delta,R):
    tight,l,u=matrix(bounds,delta[0],R,True)
    relaxed,_,_=matrix(bounds,delta[1],R,False)
    t,tc=bf(tight);r,rc=bf(relaxed)
    assert t==floyd(tight) and r==floyd(relaxed)
    assert not t or r
    beta_lower=max([Fraction(0)]+[Fraction(bounds['l'][p][0]-bounds['u'][q][1],abs(p-q)) for p,q in R])
    beta_upper=max([Fraction(0)]+[Fraction(bounds['l'][p][1]-bounds['u'][q][0],abs(p-q)) for p,q in R])
    box='admit' if beta_upper<=delta[0] else 'reject' if beta_lower>delta[1] else 'unknown'
    if t:
        theta=tc['potential']
        bias=[max(l[i]-theta[i]-delta[0]*abs(j-(i+1)) for i in range(6)) for j in range(7)]
        anchor=bias[0];bias=[b-anchor for b in bias];theta=[v+anchor for v in theta]
        assert bias[0]==0 and all(abs(bias[j]-bias[j-1])<=delta[0] for j in range(1,7))
        assert all(l[i]<=theta[i]+bias[i+1]<=u[i] for i in range(6))
        assert all(theta[p]<=theta[q] for p,q in R)
        cert=dict(theta_scaled=theta,bias_scaled=bias);status='admit'
    elif not r:cert=rc;status='reject'
    else:cert=dict(tight_rejection=tc,relaxed_potential=rc);status='unknown'
    assert not(status=='admit' and box=='reject')
    return dict(path=status,box=box,beta_lower=ratio_string(beta_lower),beta_upper=ratio_string(beta_upper),certificate=cert)
