"""Frozen deterministic C_alg(2,24) producer. No scientific experiment."""
from fractions import Fraction as F
import argparse
import json
import os
import re
from contract import (REQUEST,SOURCES,HERE,Budget,check_request,dumps,interval,
                      pack,q,source_identity,strict_json,text)
import moment_kernel

def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def div(a,b):
    if b[0]<=0:raise ValueError('NONPOSITIVE_DENOMINATOR')
    return mul(a,(1/b[1],1/b[0]))
def power(a,n):
    if a[0]<0:raise ValueError('NEGATIVE_POWER_BASE')
    return a[0]**n,a[1]**n

def scalar_bounds(m):
    a,b,c=(m[k] for k in ('mu2','mu4','mu6'))
    if any(x[0]<=0 for x in (a,b,c)):raise ValueError('NONPOSITIVE_MOMENT')
    a2=power(a,2);beta=sub(b,a2);nu3=sub(c,div(power(b,2),a))
    if beta[0]<=0 or nu3[0]<=0:raise ValueError('NONPOSITIVE_VARIANCE_FLOOR')
    H=mul(beta,add(b,a2));D0=mul(a2,b)
    Dq=div(mul(beta,add(b,mul((F(3),F(3)),a2))),(F(4),F(4)))
    V0=nu3;Vq=div(add(nu3,mul((F(9),F(9)),mul(a,beta))),(F(4),F(4)))
    D=min(D0[0],Dq[0]),max(D0[1],Dq[1])
    V=min(V0[0],Vq[0]),max(V0[1],Vq[1])
    if D[0]<=0 or V[0]<=0:raise ValueError('NONPOSITIVE_ANGULAR_FLOOR')
    return dict(a=a,b=b,c=c,beta=beta,nu3=nu3,H=H,D0=D0,Dq=Dq,V0=V0,Vq=Vq,D=D,V=V)

def cell_order(j):
    if type(j) is not int or not 0<=j<4096:raise ValueError('GAMMA_CELL_INDEX')
    return (j,j+1) if j<2048 else (j+1,j)

def gamma_accumulate(endpoints):
    if len(endpoints)!=4097:raise ValueError('GAMMA_ENDPOINT_COUNT')
    lo=F(0);hi=F(0)
    for j in range(4096):
        l,u=cell_order(j)
        lo+=F(l,2048)**6*endpoints[l][0]
        hi+=F(u,2048)**6*endpoints[u][1]
    tail=65*endpoints[4096][1]
    return 6*lo/2048,6*hi/2048+tail,tail

def gamma_witness(budget):
    endpoints=[];values=[]
    for j in range(4097):
        budget.tick(call=True)
        w=moment_kernel.exp_negative(F(j,2048)**6,bits=96,pairs=24)
        endpoints.append(w);values.append(interval(w['result']))
    lo,hi,tail=gamma_accumulate(values)
    return {'endpoints':endpoints,'bounds':pack((lo,hi)),'tail_upper':text(tail)}

def sixth_bounds(s,gamma,pi):
    numerator=mul(mul(power(gamma,6),power(s['a'],6)),mul(power(s['H'],6),power(s['V'],4)))
    denominator=mul((F(4**6*24**2),F(4**6*24**2)),mul(power(pi,9),power(s['D'],9)))
    return div(numerator,denominator)

def root_witness(x):
    if x<0:raise ValueError('NEGATIVE_ROOT_ARGUMENT')
    den=2**96;target=x.numerator*den**6//x.denominator
    lo=0;hi=1
    while hi**6<=target:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**6<=target:lo=mid
        else:hi=mid
    lower=F(lo,den);upper=lower if lower**6==x else F(lo+1,den)
    return pack((lower,upper))

def outcome(bounds):
    lo,hi=bounds
    if not 0<lo<=hi:raise ValueError('NONPOSITIVE_COEFFICIENT')
    return 'TOLERANCE_MET' if (hi-lo)/lo<=F(1,100) else 'HOLD_TARGET_UNMET'

def certify(request,source_commit,budget=None):
    budget=Budget() if budget is None else budget
    check_request(request)
    if not isinstance(source_commit,str) or not re.fullmatch('[0-9a-f]{40}',source_commit):raise ValueError('SOURCE_COMMIT_ID')
    identity=source_identity();budget.tick()
    moments=moment_kernel.certify(request['kernel'])
    if len(dumps(moments).encode())>2000000:raise ValueError('MOMENT_CERTIFICATE_SIZE_LIMIT')
    scalars=scalar_bounds({k:interval(moments['bounds'][k]) for k in ('mu2','mu4','mu6')})
    gamma=gamma_witness(budget)
    sixth=sixth_bounds(scalars,interval(gamma['bounds']),interval(moments['pi']['interval']))
    roots=[root_witness(x) for x in sixth]
    bounds=interval(roots[0])[0],interval(roots[1])[1]
    c={'schema':'original-d2-L24-coefficient-v1','request':request,'sources':SOURCES,
       'implementation':identity,'source_commit':source_commit,'moment_certificate':moments,
       'gamma':gamma,'scalar_bounds':{k:pack(v) for k,v in scalars.items()},
       'sixth_bounds':pack(sixth),'roots':roots,'bounds':pack(bounds),
       'relative_width':text((bounds[1]-bounds[0])/bounds[0]),'outcome':outcome(bounds),
       'scientific_acceptance':False,'gamma_exp_calls':budget.calls}
    budget.tick()
    if len(dumps(c).encode())+1>8388608:raise ValueError('COEFFICIENT_CERTIFICATE_SIZE_LIMIT')
    return c

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('request');p.add_argument('--source-commit',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    budget=Budget()
    try:
        with open(a.request,'rb') as f:data=f.read(65537)
        if len(data)>65536:raise ValueError('REQUEST_SIZE_LIMIT')
        c=certify(strict_json(data),a.source_commit,budget)
        payload=dumps(c)+'\n';budget.tick()
        fd=os.open(a.output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(payload)
        print(dumps({'status':'ENCLOSED','outcome':c['outcome'],'bounds':c['bounds'],
                     'relative_width':c['relative_width'],'scientific_acceptance':False}))
        return 0 if c['outcome']=='TOLERANCE_MET' else 2
    except (ValueError,OSError,moment_kernel.KernelHold) as e:
        print(dumps({'status':'HOLD','reason':str(e),'scientific_acceptance':False}));return 2

if __name__=='__main__':raise SystemExit(main())
