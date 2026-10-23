"""Bounded coefficient checker. Never imports the new coefficient producer.

Shared contract.py supplies parsing/custody only. The unchanged moment checker
supplies its established moment and exponential-witness verification.
"""
from fractions import Fraction as F
import argparse
import re
from contract import (REQUEST,SOURCES,Budget,check_request,dumps,interval,keys,
                      pack,q,source_identity,strict_json,text)
import verify_certificate as upstream

def root(w,x):
    a,b=interval(w);den=2**96
    if a<0 or b-a>F(1,den) or den%a.denominator or den%b.denominator or a**6>x or b**6<x:
        raise ValueError('INVALID_SIXTH_ROOT_WITNESS')
    return a,b

def finish(bounds,claimed_width,claimed_status):
    lower,upper=bounds
    if not 0<lower<=upper:raise ValueError('COEFFICIENT_POSITIVITY')
    width=(upper-lower)/lower
    if q(claimed_width)!=width:raise ValueError('RELATIVE_WIDTH_ASSERTION')
    target='TOLERANCE_MET' if width<=F(1,100) else 'HOLD_TARGET_UNMET'
    if claimed_status!=target:raise ValueError('FALSE_TARGET_STATUS')
    return target

def gamma_bounds(g,budget=None):
    budget=Budget() if budget is None else budget
    keys(g,('endpoints','bounds','tail_upper'))
    records=g['endpoints']
    if not isinstance(records,list) or len(records)!=4097:raise ValueError('GAMMA_ENDPOINT_COUNT')
    values=[]
    for j,w in enumerate(records):
        budget.tick(call=True)
        # A fresh original Check preserves the per-primitive 3s/100000 caps.
        # The additional outer Budget limits this whole coefficient replay.
        values.append(upstream._exp(w,F(j,2048)**6,24,upstream.Check(96)))
    lower=F(0);upper=F(0)
    for j in range(4096):
        left,right=F(j,2048)**6,F(j+1,2048)**6
        if j<2048:
            lower+=left*values[j][0];upper+=right*values[j+1][1]
        else:
            lower+=right*values[j+1][0];upper+=left*values[j][1]
    tail=65*values[-1][1]
    result=(6*lower/2048,6*upper/2048+tail)
    if interval(g['bounds'])!=result or q(g['tail_upper'])!=tail:raise ValueError('GAMMA_DARBOUX_OR_TAIL')
    if result[0]<=0:raise ValueError('GAMMA_POSITIVITY')
    return result

def _plus(a,b):return a[0]+b[0],a[1]+b[1]
def _minus(a,b):return a[0]-b[1],a[1]-b[0]
def _times(a,b):
    t=tuple(x*y for x in a for y in b);return min(t),max(t)
def _quotient(a,b):
    if b[0]<=0:raise ValueError('NONPOSITIVE_DIVISOR')
    t=tuple(x/y for x in a for y in b);return min(t),max(t)
def _p(a,n):
    if a[0]<0:raise ValueError('NEGATIVE_FACTOR')
    return a[0]**n,a[1]**n

def reconstruct_scalars(m):
    a,b,c=(interval(m['bounds'][k]) for k in ('mu2','mu4','mu6'))
    if min(a[0],b[0],c[0])<=0:raise ValueError('NONPOSITIVE_MOMENT')
    squared=_p(a,2)
    beta=_minus(b,squared);nu3=_minus(c,_quotient(_p(b,2),a))
    if min(beta[0],nu3[0])<=0:raise ValueError('NONPOSITIVE_VARIANCE_FLOOR')
    H=_times(beta,_plus(b,squared))
    D0=_times(squared,b)
    Dq=_quotient(_times(beta,_plus(b,_times((F(3),F(3)),squared))),(F(4),F(4)))
    V0=nu3
    Vq=_quotient(_plus(nu3,_times((F(9),F(9)),_times(a,beta))),(F(4),F(4)))
    D=(min(D0[0],Dq[0]),max(D0[1],Dq[1]))
    V=(min(V0[0],Vq[0]),max(V0[1],Vq[1]))
    if min(D[0],V[0])<=0:raise ValueError('NONPOSITIVE_ANGULAR_FLOOR')
    return dict(a=a,b=b,c=c,beta=beta,nu3=nu3,H=H,D0=D0,Dq=Dq,V0=V0,Vq=Vq,D=D,V=V)

def _verify(c,expected_commit,budget):
    keys(c,('schema','request','sources','implementation','source_commit','moment_certificate',
            'gamma','scalar_bounds','sixth_bounds','roots','bounds','relative_width','outcome',
            'scientific_acceptance','gamma_exp_calls'))
    if c['schema']!='original-d2-L24-coefficient-v1' or c['sources']!=SOURCES or c['scientific_acceptance'] is not False:
        raise ValueError('SOURCE_OR_SEMANTIC_IDENTITY')
    check_request(c['request'])
    if c['implementation']!=source_identity():raise ValueError('IMPLEMENTATION_SOURCE_MISMATCH')
    commit=c['source_commit']
    if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('SOURCE_COMMIT_ID')
    if expected_commit is not None and commit!=expected_commit:raise ValueError('SOURCE_COMMIT_MISMATCH')
    m=c['moment_certificate']
    if len(dumps(m).encode())>2000000:raise ValueError('MOMENT_CERTIFICATE_SIZE_LIMIT')
    if dumps(m['request'])!=dumps(REQUEST['kernel']):raise ValueError('MOMENT_REQUEST_MISMATCH')
    upstream.verify(m);budget.tick()
    s=reconstruct_scalars(m)
    if c['scalar_bounds']!={k:pack(v) for k,v in s.items()}:raise ValueError('SCALAR_BOUND_ASSERTION')
    g=gamma_bounds(c['gamma'],budget)
    pi=interval(m['pi']['interval'])
    if pi[0]<=0:raise ValueError('PI_POSITIVITY')
    # Reconstruct each positive sixth-power endpoint directly, without producer.
    sixth=[]
    for lower in (True,False):
        n=0 if lower else 1;d=1-n
        numerator=g[n]**6*s['a'][n]**6*s['H'][n]**6*s['V'][n]**4
        denominator=F(4**6*24**2)*pi[d]**9*s['D'][d]**9
        sixth.append(numerator/denominator)
    if interval(c['sixth_bounds'])!=tuple(sixth):raise ValueError('SIXTH_POWER_CONSTANT_OR_BOUND')
    roots=c['roots']
    if not isinstance(roots,list) or len(roots)!=2:raise ValueError('ROOT_COUNT')
    lower=root(roots[0],sixth[0])[0];upper=root(roots[1],sixth[1])[1]
    if not 0<lower<=upper:raise ValueError('COEFFICIENT_POSITIVITY')
    if interval(c['bounds'])!=(lower,upper):raise ValueError('FINAL_BOUND_ASSERTION')
    target=finish((lower,upper),c['relative_width'],c['outcome'])
    if type(c['gamma_exp_calls']) is not int or c['gamma_exp_calls']!=4097 or budget.calls!=4097:
        raise ValueError('GAMMA_CALL_ASSERTION')
    budget.tick()
    return {'verification':'ACCEPT_BOUNDS_ONLY','outcome':target,'bounds':c['bounds'],
            'relative_width':c['relative_width'],'scientific_acceptance':False}

def verify(c,expected_commit=None,budget=None):
    budget=Budget() if budget is None else budget
    try:
        if len(dumps(c).encode())+1>8388608:raise ValueError('COEFFICIENT_CERTIFICATE_SIZE_LIMIT')
        return _verify(c,expected_commit,budget)
    except (KeyError,TypeError,IndexError,ZeroDivisionError,OverflowError,RecursionError) as e:
        raise ValueError('MALFORMED_CERTIFICATE: '+type(e).__name__) from None

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate');p.add_argument('--expected-commit',required=True);a=p.parse_args();budget=Budget()
    try:
        with open(a.certificate,'rb') as f:data=f.read(8388609)
        if len(data)>8388608:raise ValueError('COEFFICIENT_CERTIFICATE_SIZE_LIMIT')
        result=verify(strict_json(data),a.expected_commit,budget)
        print(dumps(result));return 0
    except (ValueError,OSError) as e:
        print(dumps({'verification':'REJECT_OR_HOLD','reason':str(e),'scientific_acceptance':False}));return 1

if __name__=='__main__':raise SystemExit(main())
