"""Exact finite controls; continuum claims and source acceptance are in PROOF.md.

No external dependencies, network, floating arithmetic, or source execution.
Wrong-formula modes exercise named non-implications, not process crashes.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F


def beta(q: int) -> int:
    if type(q) is not int or q < 1:
        raise ValueError('q must be a positive integer')
    return q*(q+7)//2


def theta(s: int | F, p: int) -> F:
    s=F(s)
    if type(p) is not int or not 0 < s < p:
        raise ValueError('require integer p > s > 0')
    return 1-s/p


def radial_exponent(alphas: list[F], s: int | F, p: int) -> F:
    if not alphas or any(F(x)<=0 for x in alphas):
        raise ValueError('positive ordered radial exponents are required')
    if any(F(alphas[i]) < F(alphas[i+1]) for i in range(len(alphas)-1)):
        raise ValueError('eta is increasing, so alpha must be nonincreasing')
    return 3+theta(s,p)*sum((j+2)*min(F(x),1) for j,x in enumerate(alphas,2))


def falling(n: int, j: int) -> int:
    if type(n) is not int or type(j) is not int or min(n,j)<0:
        raise ValueError('falling factorial inputs must be nonnegative integers')
    out=1
    for i in range(j):out*=n-i
    return out


def stirling(p: int, j: int) -> int:
    if type(p) is not int or type(j) is not int or min(p,j)<0:
        raise ValueError('Stirling indices must be nonnegative integers')
    row=[1]+[0]*p
    for _ in range(p):row=[0]+[k*row[k]+row[k-1] for k in range(1,p+1)]
    return row[j] if j<=p else 0


def validate(atoms: list[tuple]) -> None:
    if not atoms or sum(F(row[0]) for row in atoms)!=1:
        raise ValueError('probabilities must sum to one')
    for w,n,k,event in atoms:
        if F(w)<0 or type(n) is not int or n<0 or type(k) is not int or k<1 or type(event) is not bool:
            raise ValueError('invalid probability/count/norm/event atom')


def expect(atoms: list[tuple], p: int) -> F:
    validate(atoms)
    if type(p) is not int or p<1:raise ValueError('positive integer moment required')
    return sum((F(w)*n**p for w,n,_,_ in atoms),F(0))


def fixtures() -> list[list[tuple]]:
    ans=[]
    for j in range(12):
        counts=[0,1+j%3,2+j%4,5+j%3]
        weights=[1+j%2,2+j%3,3,4]
        total=sum(weights)
        ans.append([(F(w,total),n,1+(i+j)%4,(i+j)%3!=0 and n>0)
                    for i,(w,n) in enumerate(zip(weights,counts))])
    return ans


def holder_sides(atoms: list[tuple], s: int, p: int, t: int) -> tuple[F,F]:
    validate(atoms);theta(s,p)
    if type(s) is not int or type(t) is not int or t<0:raise ValueError('integer s,t required for exact power controls')
    a=t*(p-s)
    left=sum((F(w)*k**a*n**s for w,n,k,e in atoms if e),F(0))**p
    rare=sum((F(w)*k**(t*p) for w,n,k,e in atoms if e),F(0))
    return left,rare**(p-s)*expect(atoms,p)**s


def positive_mass_removed(atoms: list[tuple], s: int) -> F:
    validate(atoms)
    if type(s) is not int or s<0:raise ValueError('nonnegative integer weight required')
    original={};retained={}
    for w,n,_,e in atoms:
        if n>0:
            original[n]=original.get(n,F(0))+F(w)
            if not e:retained[n]=retained.get(n,F(0))+F(w)
    return sum((n**s*abs(w-retained.get(n,F(0))) for n,w in original.items()),F(0))


def spike(n: int, b: int=4) -> list[tuple]:
    if type(n) is not int or n<1 or type(b) is not int or b<1:raise ValueError('n,b must be positive integers')
    r=F(1,2**n);rare=r**(3+b)
    return [(1-r**3-rare,0,1,False),(r**3,2,1,False),(rare,n+3,1,True)]


def run_checks(mutant: str | None=None) -> dict:
    checks={}
    # Controls retain the exact mixed exponents and perturbation-scale cap.
    mixed=radial_exponent([F(1,2),F(1,4)],1,4)
    if mutant=='M1':mixed=3+theta(1,4)*(3*F(1,2)+4*F(1,4))
    checks['mixed_scale']=mixed==F(87,16)
    base=3
    if mutant=='M2':base=3*theta(1,4)
    checks['rare_radial_scale']=base+4*theta(1,4)==6
    count=0;identities=True
    for p in range(1,10):
        for n in range(21):
            low=2 if mutant=='M3' else 1
            identities &= n**p==sum(stirling(p,j)*falling(n,j) for j in range(low,p+1))
            count+=1
    checks['stirling']=bool(identities)
    holder_count=0;holder=True
    for atoms in fixtures():
        for p in range(2,7):
            for s in range(1,p):
                for t in [0,1]:
                    left,right=holder_sides(atoms,s,p,t);holder &= left<=right;holder_count+=1
    checks['holder']=bool(holder)
    no_loss=True;spike_count=0
    for n in [1,2,4,8,16,32]:
        r=F(1,2**n);atoms=spike(n)
        ratio=positive_mass_removed(atoms,1)/(r**3*(2*r)**4)
        no_loss &= ratio<=1 if mutant=='M4' else ratio==F(n+3,16)
        spike_count+=1
    checks['no_loss']=bool(no_loss)
    atoms=[(F(7,8),0,1,False),(F(1,8),2,1,False)]
    third=sum(w*falling(n,3) for w,n,_,_ in atoms)
    checks['third_factorial']=third>=F(1,8) if mutant=='M5' else third==0
    removed=positive_mass_removed([(F(1,2),0,1,False),(F(1,4),2,1,False),(F(1,4),5,2,True)],2)
    checks['positive_intensity']=removed==F(25,4)
    checks['sub_r_saturation']=radial_exponent([F(2)],1,4)==radial_exponent([F(1)],1,4)
    failed=[k for k,v in checks.items() if not v]
    return {'ok':not failed,'checks':checks,'failed':failed,'mutant':mutant,
            'stirling_cases':count,'holder_cases':holder_count,'spike_cases':spike_count,
            'scientific_acceptance':False,'continuum_proof_by_tests':False}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mutant');args=parser.parse_args()
    if args.mutant not in [None,'M1','M2','M3','M4','M5']:
        print('unknown mutant');return 2
    out=run_checks(args.mutant);print(json.dumps(out,sort_keys=True,separators=(',',':')))
    return 0 if out['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
