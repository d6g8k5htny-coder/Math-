#!/usr/bin/env python3
"""Exact finite controls for tilted endpoint-law transfer; stdlib only.

This is finite arithmetic, not Lean execution or a continuum Gaussian proof.
"""
from fractions import Fraction as F
import argparse,itertools,json,sys


def exact(x):
 if type(x) not in (int,F): raise TypeError('exact int/Fraction required')
 return F(x)


def inputs(p,a):
 p=tuple(map(exact,p)); a=tuple(map(exact,a))
 if not p or len(p)!=len(a) or sum(p)!=1 or any(x<0 for x in p):
  raise ValueError('probability vector/weight shape invalid')
 if any(q>0 and w<0 for q,w in zip(p,a)): raise ValueError('negative weight on positive mass')
 z=sum(q*w for q,w in zip(p,a))
 if z<=0: raise ValueError('normalizer must be positive')
 return p,a,z


def tilt(p,a):
 p,a,z=inputs(p,a)
 return tuple(q*w/z for q,w in zip(p,a))


def density_data(p,a,b):
 p,a,z=inputs(p,a); _,b,z0=inputs(p,b)
 alpha=tilt(p,a); beta=tilt(p,b)
 delta=sum(q*abs(v-w) for q,v,w in zip(p,a,b))
 tv=sum(abs(v-w) for v,w in zip(alpha,beta))/2
 return dict(z=z,z0=z0,delta=delta,alpha=alpha,beta=beta,tv=tv)


def locations(x,y,n):
 x=tuple(map(exact,x)); y=tuple(map(exact,y))
 if len(x)!=n or len(y)!=n: raise ValueError('location shape invalid')
 return x,y


def bl_bound(p,a,b,x,y):
 d=density_data(p,a,b); x,y=locations(x,y,len(d['beta']))
 return 2*d['delta']/d['z0']+sum(q*abs(v-w) for q,v,w in zip(d['beta'],x,y))


def padded_budget(p,a,b,x,y,t):
 t=exact(t)
 if t<=0: raise ValueError('positive padding required')
 d=density_data(p,a,b); x,y=locations(x,y,len(d['beta']))
 return d['delta']/d['z0']+sum(q for q,v,w in zip(d['beta'],x,y) if abs(v-w)>t)


def pushforward(p,a,x):
 alpha=tilt(p,a); x,_=locations(x,x,len(alpha)); out={}
 for q,v in zip(alpha,x): out[v]=out.get(v,F(0))+q
 return out


def discrete_tv(p,q):
 return sum(abs(p.get(k,F(0))-q.get(k,F(0))) for k in p.keys()|q.keys())/2


def gaussian_diagonal_fourth(mu,lam):
 mu=tuple(map(exact,mu)); lam=tuple(map(exact,lam))
 if not mu or len(mu)!=len(lam) or any(x<0 for x in lam): raise ValueError('invalid Gaussian parameters')
 m2=sum(x*x for x in mu); tr=sum(lam); e2=m2+tr
 fourth=m2*m2+2*m2*tr+4*sum(x*x*t for x,t in zip(mu,lam))+tr*tr+2*sum(t*t for t in lam)
 return fourth,e2


def need(ok,reason):
 if not ok: raise ValueError(reason)


def controls(mutant=None):
 count=0
 p=(F(1,4),F(1,4),F(1,2)); ws=[a for a in itertools.product((0,1,2),repeat=3) if any(a)]
 for a,b in itertools.product(ws,repeat=2):
  d=density_data(p,a,b); need(d['tv']<=d['delta']/d['z0'],'REFERENCE_TV_BOUND'); count+=1
 # Minimal exact witnesses, each isolates one omitted/incorrect operation.
 p=(F(1,2),F(1,2)); a=(F(2),F(2))
 masses=tuple(q*w for q,w in zip(p,a)) if mutant=='M1' else tilt(p,a)
 need(sum(masses)==1,'NORMALIZED_MASS'); count+=1
 a,b=(F(2),F(0)),(F(0),F(2)); d=density_data(p,a,b)
 delta=abs(sum(q*(v-w) for q,v,w in zip(p,a,b))) if mutant=='M2' else d['delta']
 need(d['tv']<=delta/d['z0'],'ABSOLUTE_NOT_SIGNED_ERROR'); count+=1
 p=(F(1),); a=b=(F(1),); x=(F(1,8),); y=(F(0),)
 bd=0 if mutant=='M3' else bl_bound(p,a,b,x,y)
 need(F(1,8)<=bd,'MOVEMENT_TERM'); count+=1
 p=(F(1,16),F(15,16)); a=b=(F(16),F(0)); x=(F(1),F(0)); y=(F(0),F(0))
 bd=F(1,16) if mutant=='M4' else padded_budget(p,a,b,x,y,F(1,2))
 need(1<=bd,'TILTED_TAIL'); count+=1
 # A={x<=0}; both deterministic points are within t of each other and straddle 0.
 x,y=(F(1,8),),(F(-1,8),); p=a=b=(F(1),)
 bd=padded_budget(p,a,b,x,y,F(1,2))+(0 if mutant=='M5' else 1)
 need(1<=bd,'BOUNDARY_MARGIN'); count+=1
 m4,e2=gaussian_diagonal_fourth((0,),(1,))
 need(m4<=(1 if mutant=='M6' else 3)*e2*e2,'GAUSSIAN_FOURTH'); count+=1
 for n in (2,4,8,16,32):
  x=(F(1,n),); y=(F(0),)
  tv=discrete_tv(pushforward(p,a,x),pushforward(p,b,y))
  need(tv<=(F(1,n) if mutant=='M7' else 1),'TV_NOT_BL'); count+=1
 return {'controls':count,'scope':'finite exact controls, not continuum proof or Lean','scientific_effect':'NONE'}


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--mutant',choices=['M'+str(n) for n in range(1,8)])
 args=parser.parse_args()
 try: result=controls(args.mutant)
 except (ValueError,TypeError) as exc:
  print('TILT_FAIL: '+str(exc),file=sys.stderr); return 1
 print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': sys.exit(main())
