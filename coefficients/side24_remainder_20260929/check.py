#!/usr/bin/env python3
"""Exact finite controls for OA-SIDE24-REMAINDER-20260929-v1.

These controls check the arithmetic of PROOF.md, not its continuum arguments.
No nonauthor acceptance or formal verification is asserted. Standard library only.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

MUTANTS = ('ambient-as-free', 'drop-cone-degree', 'hessian-sign',
           'omit-normalizer', 'shell-q4', 'firstvar-sign')


def exact(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('exact integer or Fraction required')
    return F(x)


def dimensions(d):
    if isinstance(d, bool) or not isinstance(d, int) or d < 2:
        raise ValueError('integer dimension d >= 2 required')
    m = d-1
    n = d+1+d*(d+1)//2
    k = 1+m*(m+1)//2
    p = F(4, 3)+2*m
    return n, k, p, k+p


def scalar_score_moments(d, curvature_sign=-1):
    n, _, _, nu = dimensions(d)
    first = (nu-n)/2
    second = (nu*(nu+2)-2*n*nu+n*n)/4+F(n,2)+curvature_sign*nu
    return first, second


def score_majorant(d):
    n, _, _, nu = dimensions(d)
    return (n*n+2*n*nu+nu*(nu+2))/4+F(n,2)+nu


def taylor_constant():
    return F(1,2)*score_majorant(3)*F(16,9)*F(3125,243)


def projected_first_variation(d):
    dimensions(d)
    # Coefficients of L^2, L^4, L^6 in the projected nearest-image jets.
    da = (F(-2), F(0), F(0))
    dm4 = (F(-12), F(6,d+2), F(0))
    dchi = (F(-90), F(90,d+2), F(-30,(d+2)*(d+4)))
    return tuple((1-F(d,2))*a+(F(d,6)-1)*b+c/9
                 for a,b,c in zip(da,dm4,dchi))


def closed_first_variation(d):
    dimensions(d)
    return (F(-d), F(d+4,d+2), F(-10,3*(d+2)*(d+4)))


def first_variation_at(d, L):
    L = exact(L)
    return sum(c*L**(2*(j+1)) for j,c in enumerate(closed_first_variation(d)))


def normalize_linear(a0, a1, s1):
    a0,a1,s1 = map(exact,(a0,a1,s1))
    return a0, a1-s1*a0, s1*s1*a0-s1*a1


def exp_bounds(x, terms):
    """Positive Taylor sum through terms, plus an exact geometric tail."""
    x = exact(x)
    if isinstance(terms,bool) or not isinstance(terms,int) or terms < 0 or x < 0:
        raise ValueError('nonnegative argument and integer truncation required')
    ratio = x/(terms+2)
    if ratio >= 1:
        raise ValueError('tail ratio must be below one')
    term = F(1)
    total = term
    for j in range(1,terms+1):
        term *= x/j
        total += term
    following = term*x/(terms+1)
    return total, total+following/(1-ratio)


def outward(x, places):
    x = exact(x)
    if isinstance(places,bool) or not isinstance(places,int) or places < 0:
        raise ValueError('nonnegative integer precision required')
    scale = 10**places
    scaled = x*scale
    a = scaled.numerator//scaled.denominator
    b = -((-scaled.numerator)//scaled.denominator)
    return F(a,scale),F(b,scale)


def q_interval(terms=100, places=260):
    """Outward interval for exp(-288): exp(-9/32) raised to 1024."""
    elo,ehi = exp_bounds(F(9,32),terms)
    lo = outward(1/ehi,places)[0]
    hi = outward(1/elo,places)[1]
    for _ in range(10):
        lo = outward(lo*lo,places)[0]
        hi = outward(hi*hi,places)[1]
    return lo,hi


def image_bounds(include_normalizer=True, deep_power=2):
    B = 76*24**6+15
    z = F(1,10**125)
    E = 1458*B*z
    normalizer = 6*1458 if include_normalizer else 0
    remainder = 541+normalizer
    return {'B':B, 'E':E, 'epsilon':60*E,
            'deep_shell_coefficient':541,
            'normalization_coefficient':normalizer,
            'remainder_coefficient':remainder,
            'rho':60*remainder*B*z**deep_power}


def remainder_bound():
    data = image_bounds()
    return 2000*data['epsilon']**2+F(29,3)*data['rho']


def correction_interval(d):
    if d not in (2,3) or isinstance(d,bool):
        raise ValueError('certified remainder only for dimensions 2 and 3')
    qlo,qhi = q_interval()
    P = first_variation_at(d,24)
    if P >= 0:
        raise ValueError('negative first variation required for this interval order')
    R = remainder_bound()
    return outward(P*qhi-R,260)[0],outward(P*qlo+R,260)[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(mutant=None):
    if mutant not in (None,*MUTANTS):
        raise ValueError('unknown mutant')
    groups = []
    for d in (2,3):
        n,k,p,nu = dimensions(d)
        n = k if mutant == 'ambient-as-free' else n
        nu = k+F(4,3) if mutant == 'drop-cone-degree' else nu
        require((nu-n)/2 == F(-1,3), 'ambient/free/homogeneity scaling mismatch')
        first,second = scalar_score_moments(d, 1 if mutant == 'hessian-sign' else -1)
        require((first,second)==(F(-1,3),F(4,9)), 'density second derivative mismatch')
    require(score_majorant(3)==F(1012,9), 'radial fourth moment / majorant mismatch')
    require(taylor_constant()<2000, 'Taylor constant exceeds allowance')
    groups.append('density-scores-and-homogeneity')
    for d in range(2,21):
        require(projected_first_variation(d)==closed_first_variation(d), 'projection/chain mismatch')
    P3 = first_variation_at(3,24)*(-1 if mutant=='firstvar-sign' else 1)
    require(P3==F(-620813376,35), 'first variation sign or coefficient mismatch')
    require(first_variation_at(2,24)==-26045568, 'planar first variation mismatch')
    groups.append('nearest-image-first-variation')
    q_upper = F(1,10**125)
    require(exp_bounds(F(288,125),20)[0]>10, 'q upper bracket unproved')
    require(exp_bounds(F(16,7),40)[1]<10, 'q lower bracket unproved')
    require(512*q_upper**3<F(1,2), 'whole-shell ratio fails')
    require(F(3,2)**9*q_upper**5<F(1,2), 'deep-shell ratio fails')
    require(746496*q_upper**2<1, 'deep-shell absorption fails')
    data = image_bounds(mutant!='omit-normalizer',4 if mutant=='shell-q4' else 2)
    require(data['remainder_coefficient']==9289, 'normalization product omitted')
    require(data['rho']==60*9289*data['B']*q_upper**2, 'deep shell starts at q^2, not q^4')
    require(normalize_linear(-1,2*(24**2-1),2)[2]==-4*24**2, 'normalization q^2 term missing')
    require(data['epsilon']<F(1,4), 'Taylor neighborhood invalid')
    groups.append('infinite-shells-and-normalization')
    R = remainder_bound()
    require(R<F(1,10**216), 'claimed remainder bound fails')
    corrections = {}
    for d in (2,3):
        lo,hi = correction_interval(d)
        require(lo<hi<0, 'sign certificate fails')
        require(abs(first_variation_at(d,24))*F(1,10**126)>R, 'coarse sign margin fails')
        corrections[str(d)]={'P_d_24':str(first_variation_at(d,24)),
                            'lower':str(int(lo*10**260))+'e-260',
                            'upper':str(int(hi*10**260))+'e-260'}
    groups.append('remainder-and-negative-sign')
    return {'object':'OA-SIDE24-REMAINDER-20260929-v1',
            'passed':True, 'groups':groups, 'mutants':list(MUTANTS),
            'scope':'finite rational controls; continuum proof and nonauthor review separate',
            'scientific_effect':'NONE', 'scientific_acceptance':False,
            'taylor_majorant':str(taylor_constant()),
            'relative_remainder_rational':str(R),
            'relative_remainder_bound':'< 1e-216 (d=2,3; L=24)',
            'correction_intervals':corrections}


def verify_sources(repo):
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'SOURCES.json').read_text(encoding='utf-8'))
    expected = {row['path'] for row in manifest['files']}|{'SOURCES.json'}
    require({p.name for p in here.iterdir()}==expected, 'packet file inventory mismatch')
    for row in manifest['files']:
        path = here/row['path']
        require(Path(row['path']).name==row['path'] and not path.is_symlink(), 'regular flat packet source required')
        data = path.read_bytes()
        require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],
                'packet source identity mismatch: '+row['path'])
    root = Path(repo).resolve()
    for row in manifest['upstream']:
        rel = Path(row['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'relative upstream path required')
        path = root/rel
        require(not path.is_symlink() and path.resolve().is_relative_to(root), 'upstream path escapes repository')
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==row['git_blob'], 'upstream Git blob mismatch: '+row['path'])
        if 'sha256' in row:
            require(hashlib.sha256(data).hexdigest()==row['sha256'], 'upstream SHA256 mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=MUTANTS)
    parser.add_argument('--verify-sources',metavar='REPOSITORY_ROOT')
    args = parser.parse_args()
    try:
        report = verify(args.mutant)
        if args.verify_sources:
            verify_sources(args.verify_sources)
            report['source_manifest_verified'] = True
        print(json.dumps(report,sort_keys=True,indent=2))
        return 0
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    sys.exit(main())
