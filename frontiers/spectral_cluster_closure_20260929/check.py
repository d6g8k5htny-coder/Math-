"""Exact finite controls for orthogonal spectral cluster closure.

Standard library only. These controls do not prove Gaussian convergence.
"""
import argparse
import json
from fractions import Fraction as F
from math import prod

MUTANTS=('drop-spectral-r','drop-soft-vandermonde','wrong-hard-power',
         'drop-far-branch','reverse-cutoff','include-zero',
         'drop-mixed-term','swap-full-normalizer')


def rat(x):
    if type(x) not in (int,F): raise ValueError('exact int/Fraction required')
    return F(x)


def absorption(x,u,r,a):
    x,u,r,a=map(rat,(x,u,r,a))
    if x<0 or u<1 or r<=0 or a<=0: raise ValueError('invalid absorption arguments')
    if x>a*u*u+a*r*r*x*x: raise ValueError('absorption premise does not hold')
    if x<=2*a*u*u: return 'near'
    if x<1/(2*a*r*r): raise ValueError('absorption conclusion failed')
    return 'far'


def vandermonde(values):
    values=list(map(rat,values))
    if any(b<=a for a,b in zip(values,values[1:])):
        raise ValueError('strictly ordered spectrum required')
    return prod((values[j]-values[i] for i in range(len(values))
                  for j in range(i+1,len(values))),start=F(1))


def spectral_factor(r,s,hard):
    r,s=map(rat,(r,s)); hard=list(map(rat,hard))
    if r<=0: raise ValueError('positive radius required')
    return r*vandermonde([-r*s]+hard)


def limit_hard_factor(hard):
    hard=list(map(rat,hard))
    if any(x<=0 for x in hard): raise ValueError('positive hard spectrum required')
    return prod((x**3 for x in hard),start=F(1))*vandermonde(hard)


def typed_weight(k,s,a,beta):
    k,s,a,beta=map(rat,(k,s,a,beta))
    if k<=0: raise ValueError('positive gap required')
    return max(F(0),-6*k*(s-beta/2)-a*a/4)*max(F(0),a*a/4-6*k*(s+beta/2))


def nonempty_intensity(law,epsilon):
    epsilon=rat(epsilon)
    if epsilon<=0 or not isinstance(law,dict) or not law:
        raise ValueError('positive scale and PMF required')
    out={}
    for n,p in law.items():
        if type(n) is not int or n<0: raise ValueError('invalid count')
        p=rat(p)
        if p<0: raise ValueError('negative probability')
        if n>0 and p>0: out[n]=p/epsilon
    if sum(map(rat,law.values()))!=1: raise ValueError('PMF must sum to one')
    return out


def reduced_third(xxx,xxy_v,xyy_vv,yyy_vvv):
    xxx,xxy_v,xyy_vv,yyy_vvv=map(rat,(xxx,xxy_v,xyy_vv,yyy_vvv))
    return xxx+3*xxy_v+3*xyy_vv+yyy_vvv


def majorant_degree(d):
    if type(d) is not int or d<2: raise ValueError('integer d>=2 required')
    return 4*d+(d-1)*(d-2)


def invalid_cutoff_bound(r,determinant,eta):
    r,determinant,eta=map(rat,(r,determinant,eta))
    if not 0<determinant<eta or r<=0: raise ValueError('invalid cutoff probe')
    return r/determinant**2<=r/eta**2


def det(matrix):
    """Exact determinant, with empty determinant equal to one."""
    a=[list(map(rat,row)) for row in matrix]; n=len(a)
    if any(len(row)!=n for row in a): raise ValueError('square matrix required')
    value=F(1)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None: return F(0)
        if pivot!=i: a[i],a[pivot]=a[pivot],a[i]; value=-value
        p=a[i][i]; value*=p
        for j in range(i+1,n):
            t=a[j][i]/p
            for k in range(i+1,n): a[j][k]-=t*a[i][k]
    return value


def require(ok,message):
    if not ok: raise ValueError(message)


def run_checks(mutant=None):
    factor=spectral_factor(F(1,10),-1,[2,4])
    if mutant=='drop-spectral-r': factor/=F(1,10)
    if mutant=='drop-soft-vandermonde': factor=F(1,10)*vandermonde([2,4])
    require(factor==F(741,500),'spectral r and soft Vandermonde')
    factor=limit_hard_factor([2,4])
    if mutant=='wrong-hard-power': factor=2**2*4**2*vandermonde([2,4])
    require(factor==1024,'hard powers include weight squared and spectral factor')
    branch=absorption(200,1,F(1,10),1)
    if mutant=='drop-far-branch': branch='near'
    require(branch=='far','exceptional absorption branch retained')
    bound=invalid_cutoff_bound(F(1,10),F(1,100),F(1,10))
    if mutant=='reverse-cutoff': bound=True
    require(not bound,'inverse cutoff direction')
    law={0:F(7,8),1:F(1,16),2:F(1,16)}
    intensity=nonempty_intensity(law,F(1,8))
    if mutant=='include-zero': intensity[0]=F(7)
    require(intensity=={1:F(1,2),2:F(1,2)},'nonempty intensity excludes zero')
    reduced=reduced_third(1,2,3,4)
    if mutant=='drop-mixed-term': reduced-=3*F(2)
    require(reduced==20,'all reduced third-derivative terms')
    ledger=1+4-2
    if mutant=='swap-full-normalizer': ledger=1+4-5
    require(ledger==3,'physical jet / two soft columns / full normalizer')
    cases=0
    for a in (F(1),F(3)):
        for u in (F(1),F(2),F(5)):
            for r in (F(1,100),F(1,10),F(1,2)):
                for x in map(F,(0,1,2,5,10,20,100,200,1000,20000)):
                    if x<=a*u*u+a*r*r*x*x:
                        branch=absorption(x,u,r,a)
                        require(x<=2*a*u*u if branch=='near' else x>=1/(2*a*r*r),
                                'absorption dichotomy grid')
                        cases+=1
    return {'passed':True,'scientific_effect':'NONE','mathematical_acceptance':False,
            'scope':'finite exact controls only','absorption_cases':cases,
            'groups':['spectral-jacobian','hard-weight','absorption','cutoff-direction',
                      'nonempty-measure','vector-third-derivative','full-normalizer']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    try: result=run_checks(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True)); return 1
    print(json.dumps(result,indent=2,sort_keys=True)); return 0


if __name__=='__main__': raise SystemExit(main())
