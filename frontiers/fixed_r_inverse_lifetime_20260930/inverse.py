"""Exact controls for the fixed-separation inverse-lifetime theorem candidate.

Finite rational checks only: this does not simulate a conditioned Gaussian field
or certify the infinite-dimensional support argument. Standard library only.
"""
import argparse
from fractions import Fraction as F
import json

MUTANTS=('lose-determinant-weight','wrong-cubic-power','wrong-soft-direction',
         'admit-critical-inverse','drop-endpoint-margin','unconditional-tail-shortcut')
_MUTANT=None


def rat(x):
    if type(x) not in (int,F):raise TypeError('integer or Fraction required')
    return F(x)


def determinant(matrix):
    n=len(matrix)
    if any(len(row)!=n for row in matrix):raise ValueError('square matrix required')
    a=[[rat(x) for x in row] for row in matrix];out=F(1)
    for j in range(n):
        i=next((i for i in range(j,n) if a[i][j]),None)
        if i is None:return F(0)
        if i!=j:a[j],a[i]=a[i],a[j];out=-out
        pivot=a[j][j];out*=pivot
        for i in range(j+1,n):
            q=a[i][j]/pivot
            for k in range(j+1,n):a[i][k]-=q*a[j][k]
    return out


def inverse(matrix):
    n=len(matrix)
    if any(len(row)!=n for row in matrix):raise ValueError('square matrix required')
    a=[[rat(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        i=next((i for i in range(j,n) if a[i][j]),None)
        if i is None:raise ValueError('singular matrix')
        a[j],a[i]=a[i],a[j];p=a[j][j];a[j]=[x/p for x in a[j]]
        for i in range(n):
            if i!=j:
                q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]


def soft_chart(C,v,lam):
    lam=rat(lam);C=[[rat(x) for x in row] for row in C];v=list(map(rat,v));n=len(C)
    if not n or len(v)!=n or any(len(row)!=n for row in C) or lam<=0:
        raise ValueError('positive soft curvature and a nonempty square hard block required')
    if any(C[i][j]!=C[j][i] for i in range(n) for j in range(n)):
        raise ValueError('hard block must be symmetric')
    if any((-1)**j*determinant([row[:j] for row in C[:j]])<=0 for j in range(1,n+1)):
        raise ValueError('hard block must be strictly negative definite')
    inv=inverse(C);cv=[sum((inv[i][j]*v[j] for j in range(n)),F(0)) for i in range(n)]
    top=sum((x*y for x,y in zip(v,cv)),F(0))-lam
    H=[[top]+v]+[[v[i]]+C[i] for i in range(n)]
    e=[F(1)]+[-x for x in cv]
    if _MUTANT=='wrong-soft-direction':e=[F(1)]+cv
    return H,e


def barrier(L,lam,K):
    L,lam,K=map(rat,(L,lam,K))
    if L<=0 or not 0<lam<=K or K<1:raise ValueError('positive length and 0<lambda<=K, K>=1 required')
    a=min(F(1),L/4);R=a*lam/K
    return R,lam*R*R/3


def path_constants(a,M):
    """B=6/a, admissible lambda ceiling, loss bound C and endpoint-gain coefficient."""
    a,M=map(rat,(a,M))
    if a<=0 or M<0:raise ValueError('positive cubic lower bound and nonnegative fourth bound required')
    B=6/a;cut=min(F(1),6/(M*B*B)) if M else F(1)
    return B,cut,B*B,F(0) if _MUTANT=='drop-endpoint-margin' else B*B/4


def cubic_gap(lam,g):
    lam,g=map(rat,(lam,g))
    if lam<=0 or g<=0:raise ValueError('positive lambda and cubic required')
    return 2*lam**(2 if _MUTANT=='wrong-cubic-power' else 3)/(3*g*g)


def upper_split(s):
    """Integral_0^1 lambda min(1,s^3/lambda^3)d lambda, 0<s<=1."""
    s=rat(s)
    if not 0<s<=1:raise ValueError('0<s<=1 required')
    if _MUTANT=='unconditional-tail-shortcut':return s
    return F(3,2)*s*s-s**3


def tail_exponent(beta=1):
    beta=rat(beta)
    if beta<0:raise ValueError('nonnegative determinant power required')
    return (1+(0 if _MUTANT=='lose-determinant-weight' else beta))/3


def inverse_finite(p):
    p=rat(p)
    if p<0:raise ValueError('nonnegative inverse power required')
    return p<=F(2,3) if _MUTANT=='admit-critical-inverse' else p<F(2,3)


def critical_model():
    """For density 2lambda and lifetime lambda^3, cap T=s^-3: 1-2log(s)."""
    return F(1),F(-2)


def cap_model(s,three_p):
    """Rational scalar-model capped inverse moment when 3p is an integer !=2."""
    s=rat(s)
    if not 0<s<=1 or type(three_p) is not int or three_p<0 or three_p==2:
        raise ValueError('0<s<=1 and integer 3p>=0, 3p!=2 required')
    n=2-three_p
    return s**n+2*(1-s**n)/n


def check():
    def need(ok,msg):
        if not ok:raise ValueError(msg)
    need(tail_exponent(1)==F(2,3),'retain original maximum determinant weight')
    need(cubic_gap(F(1,10),F(2))==F(1,6000),'cubic lifetime scale')
    H,e=soft_chart([[F(-2)]],[F(1,3)],F(1,10))
    q=sum((e[i]*H[i][j]*e[j] for i in range(2) for j in range(2)),F(0))
    need(q==-F(1,10),'correct Schur soft direction')
    need(not inverse_finite(F(2,3)),'critical inverse moment diverges')
    need(path_constants(1,4)[3]==9,'strict endpoint above birth')
    need(upper_split(F(1,10))==F(7,500),'retain weighted near-zero eigenvalue integral')
    cases=0
    for a in (F(1,2),F(1),F(2)):
        for M in (F(0),F(1),F(4),F(20)):
            B,ceiling,C,gain=path_constants(a,M)
            for frac in (F(1,10),F(1,2),F(1)):
                lam=ceiling*frac
                endpoint=-lam*(B*lam)**2/2+a*(B*lam)**3/6-M*(B*lam)**4/24
                need(endpoint>=gain*lam**3>0,'Taylor endpoint')
                for j in range(17):
                    t=B*lam*F(j,16)
                    lower=-lam*t*t/2+a*t**3/6-M*t**4/24
                    need(lower>=-C*lam**3,'Taylor path stays above lower barrier')
                cases+=1
    return {'passed':True,'mathematical_acceptance':False,'scientific_effect':'NONE',
            'scope':'finite rational Taylor, Schur and integral controls only',
            'path_parameter_cases':cases,'path_grid_checks':17*cases,
            'fixed_r_small_lifetime_exponent':'2/3','inverse_moment_threshold':'2/3',
            'unweighted_comparison_exponent':'1/3',
            'critical_capped_growth':'Theta(log T)',
            'supercritical_capped_growth':'Theta(T^(p-2/3))',
            'uniform_in_pin_separation':False,'extreme_partner_conditioning':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args();global _MUTANT;_MUTANT=args.mutant
    try:ans=check()
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True));raise SystemExit(1)
    print(json.dumps(ans,indent=2,sort_keys=True))

if __name__=='__main__':main()
