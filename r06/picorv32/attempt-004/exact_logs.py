"""Outward log bounds from positive rational series; no floating point/Decimal.

For 0<=z<=1/3, log((1+z)/(1-z))=2*sum z^(2j+1)/(2j+1).
After M terms the positive remainder is at most
2*z^(2M+1)/((2M+1)*(1-z*z)). Each term is enclosed by integer
floor/ceil at scale10^90 before addition. Binary range reduction makes
x/2^k lie in[1,2); log2 uses the same formula at z=1/3.
"""
from fractions import Fraction
from functools import lru_cache
SCALE=10**60
WORK=10**90
TERMS=120
def ceildiv(a,b):return -(-a//b)
@lru_cache(None)
def series(n,d):
    assert 0<=n and 3*n<=d
    if not n:return (0,0)
    nn,dd=n*n,d*d;np,dp=n,d;lo=hi=0
    for j in range(TERMS):
        a=2*WORK*np;b=(2*j+1)*dp
        lo+=a//b;hi+=ceildiv(a,b);np*=nn;dp*=dd
    hi+=ceildiv(2*WORK*np*dd,(2*TERMS+1)*dp*(dd-nn))
    return lo,hi
@lru_cache(None)
def bounds(value):
    x=Fraction(value);assert x>=1
    k=x.numerator.bit_length()-x.denominator.bit_length()
    while x<Fraction(2)**k:k-=1
    while x>=Fraction(2)**(k+1):k+=1
    assert k>=0
    y=x/Fraction(2)**k;z=(y-1)/(y+1)
    a,b=series(z.numerator,z.denominator);c,d=series(1,3)
    a+=k*c;b+=k*d;factor=WORK//SCALE
    return (a//factor,ceildiv(b,factor))
def proof_metadata():
    return dict(method='positive atanh series plus geometric tail; exact integer floor/ceil per term',terms=TERMS,work_scale=str(WORK),output_scale=str(SCALE),range='all input x>=1; binary range reduction y in[1,2), z in[0,1/3)',tail='2*z^(2M+1)/((2M+1)*(1-z^2))',boundary='tight feasible => admit; relaxed negative cycle => reject; otherwise unknown, never forced')
