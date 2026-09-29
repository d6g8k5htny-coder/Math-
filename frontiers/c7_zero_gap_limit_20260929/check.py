#!/usr/bin/env python3
"""Exact ledger controls, not a proof of the C7 zero-gap continuum limit.

Standard library only. Positive output makes no scientific acceptance claim.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

MUTANTS = ('wrong-radial-power', 'missing-gap-jacobian', 'drop-k-plus-r',
           'apply-K2-outside-domain', 'boundary-only', 'unordered-half',
           'wrong-moment-threshold', 'swap-intensity-probability')


def exact(value):
    if isinstance(value,bool) or not isinstance(value,(int,F)):
        raise TypeError('an exact integer or Fraction is required')
    return F(value)


def require(condition,message):
    if not condition:
        raise ValueError(message)


def pushforward_exponents():
    # (1/3) ell^(-1/3) k^(-2/3) |dk/dr|, k=ell/r^3.
    return F(1,3)*3, F(-1,3)+F(-2,3)+1, -3*F(-2,3)-4


def radial_ledger(d):
    if isinstance(d,bool) or not isinstance(d,int) or d<2:
        raise ValueError('fixed integer dimension d >= 2 required')
    spatial=d-1
    pin=-(d+3)
    weight=2
    return spatial+pin+weight+3, spatial+pin+weight


def ordered_height_jacobian():
    # det d(b,b-ell)/d(b,ell)=-1; the two critical types are distinct roles.
    return abs(F(1)*F(-1)-F(0)*F(1))


def parent_pin_prefactor():
    return 12


def radial_bound(r,k):
    r,k=exact(r),exact(k)
    require(0<r<=1 and k>0,'need 0 < r <= 1 and k > 0')
    return r/k if k>=r else (1+k/r)**2


def barrier_drop(curvature,perturbation,radius):
    a,eta,R=map(exact,(curvature,perturbation,radius))
    require(a>eta>=0 and R>0,'positive residual concavity and radius required')
    return (a-eta)*R**2/2


def barrier_excludes_gap(curvature,perturbation,radius,separation,gap):
    R,sep,ell=map(exact,(radius,separation,gap))
    require(sep>0 and 0<R<sep/2 and ell>0,'strictly separated positive ball and gap required')
    return ell<barrier_drop(curvature,perturbation,R)


def typed_diagonal_weight(maximum,saddle):
    a=tuple(map(exact,maximum))
    b=tuple(map(exact,saddle))
    require(len(a)==len(b)>=2,'two same-dimensional Hessian diagonals required')
    if not all(x<0 for x in a) or sum(x<0 for x in b)!=len(b)-1 or any(x==0 for x in b):
        return F(0)
    out=F(1)
    for x in a+b:
        out*=x
    return abs(out)


def normalized_tv(current,limit):
    a,b=tuple(map(exact,current)),tuple(map(exact,limit))
    require(len(a)==len(b)>0 and all(x>=0 for x in a+b),'equal nonempty nonnegative measures required')
    A,B=sum(a),sum(b)
    require(A>0 and B>0,'both masses must be positive')
    tv=sum(abs(x/A-y/B) for x,y in zip(a,b))/2
    l1=sum(abs(x-y) for x,y in zip(a,b))
    return tv,l1/B


def moment_case(q):
    q=exact(q)
    return 'finite' if q>-1 else 'logarithmic' if q==-1 else 'power-divergent'


def moment_coefficient(q):
    q=exact(q)
    require(q>-1,'power integral from zero requires q > -1')
    return 1/(q+1)


def sampling_ledger():
    candidate=F(-1,3)
    rejected=F(0)
    return rejected-candidate,(rejected+1)-(candidate+1),(candidate+1)/(rejected+1)


def verify_identity(root,row):
    root=Path(root).resolve()
    name=row['path']
    require(isinstance(name,str),'source path must be a string')
    rel=Path(name)
    require(not rel.is_absolute() and '..' not in rel.parts and bool(rel.parts),'relative source path required')
    path=root/rel
    require(path.resolve().is_relative_to(root),'source escapes root')
    for j in range(1,len(rel.parts)+1):
        require(not root.joinpath(*rel.parts[:j]).is_symlink(),'symlink source path rejected')
    data=path.read_bytes()
    require('sha256' in row or 'git_blob' in row,'at least one content identity required')
    if 'bytes' in row:
        require(len(data)==row['bytes'],'source length mismatch: '+name)
    if 'sha256' in row:
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'source SHA256 mismatch: '+name)
    if 'git_blob' in row:
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==row['git_blob'],'source Git blob mismatch: '+name)


def verify_sources(repository):
    here=Path(__file__).resolve().parent
    manifest=json.loads((here/'SOURCES.json').read_text(encoding='utf-8'))
    names=[row['path'] for row in manifest['files']]
    require(len(names)==len(set(names)),'duplicate packet identity')
    require(all(Path(p).name==p for p in names),'flat packet inventory required')
    require({p.name for p in here.iterdir()}==set(names)|{'SOURCES.json'},'packet inventory mismatch')
    for row in manifest['files']:
        verify_identity(here,row)
    for row in manifest['upstream']:
        verify_identity(repository,row)


def verify(mutant=None):
    require(mutant in (None,*MUTANTS),'unknown semantic variant')
    coeff,ell_power,r_power=pushforward_exponents()
    if mutant=='wrong-radial-power':
        r_power=F(-1)
    require((coeff,ell_power,r_power)==(1,0,-2),'lifetime-to-radius coarea mismatch')
    for d in range(2,13):
        marked,unmarked=radial_ledger(d)
        if mutant=='missing-gap-jacobian':
            unmarked=marked
        require(marked==1 and unmarked==-2,'gap Jacobian missing in radial ledger')
    pair_jac=ordered_height_jacobian()*(F(1,2) if mutant=='unordered-half' else 1)
    require(pair_jac==1 and parent_pin_prefactor()==12,'ordered pair normalization mismatch')
    for r in (F(1,100),F(1,7),F(1,2),F(1)):
        for k in (r/100,r/2,r,2*r,F(5)):
            bound=radial_bound(r,k)
            if mutant=='drop-k-plus-r' and k<r:
                bound=r**-2
            if mutant=='apply-K2-outside-domain':
                bound=r/k
            require(0<bound<=4,'uniform radial domination fails')
    drop=barrier_drop(2,F(1,2),F(1,3))
    if mutant=='boundary-only':
        drop=F(2)*F(1,3)**2/2  # ignores the C2 perturbation / residual concavity
    require(drop==F(1,12),'stable local concavity barrier mismatch')
    require(barrier_excludes_gap(2,F(1,2),F(1,3),1,F(1,24)),'barrier test failed')
    for d in range(2,8):
        require(typed_diagonal_weight([-1]*d,[1]+[-1]*(d-1))==1,'positive type example failed')
    for a,b in (([1,2,0],[2,3,4]),([0,1],[1,0]),([2,4],[1,2])):
        tv,bound=normalized_tv(a,b)
        require(tv<=bound,'normalized measure TV inequality failed')
    threshold=F(-2,3) if mutant=='wrong-moment-threshold' else F(-1)
    require(threshold==-1 and moment_case(F(-3,4))=='finite','rejected/individual moment thresholds conflated')
    sample=sampling_ledger()
    if mutant=='swap-intensity-probability':
        sample=(F(3),sample[1],sample[2])
    require(sample==(F(1,3),F(1,3),F(2,3)),'intensity sampling and fixed-radius Palm law conflated')
    return {'object':'OA-C7-ZERO-GAP-LIMIT-20260929-v1',
            'passed':True,'scientific_acceptance':False,'scientific_effect':'NONE',
            'scope':'exact finite ledgers only; regression, barrier topology and dominated convergence require analytic review',
            'groups':['coarea','ordered-normalization','radial-domination','concavity-barrier',
                      'typed-open-set-example','normalization-TV','moment-threshold','sampling-exponents'],
            'radial_power':str(r_power),'scalar_branch_bound':4,
            'positive_limit':'B_(d,L), explicit equal-height integral; not numerically evaluated',
            'rejected_moment_threshold':'q > -1',
            'density_sampling_exponent':str(sample[0]),
            'cumulative_sampling_exponent':str(sample[1]),
            'cumulative_sampling_multiplier':str(sample[2]),
            'claimed_convergence_rate':None,
            'mutants':list(MUTANTS)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=MUTANTS)
    parser.add_argument('--verify-sources',metavar='REPOSITORY_ROOT')
    args=parser.parse_args()
    try:
        report=verify(args.mutant)
        if args.verify_sources:
            verify_sources(args.verify_sources)
            report['source_manifest_verified']=True
        print(json.dumps(report,indent=2,sort_keys=True))
        return 0
    except (TypeError,ValueError,KeyError,OSError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    sys.exit(main())
