#!/usr/bin/env python3
"""Exact-rational diagnostics for NOTE.md; no statistical or Lean certificate.

Radii s,t below are SQUARED radii. Masses aggregate either sign. The measure
argument in the note is not replaced by this finite enumeration.
"""
import argparse
from fractions import Fraction as F
import json

MUTANTS = {'M1':'square_completion','M2':'fourth_floor','M3':'delta_floor',
           'M4':'tau_endpoint','M5':'probability_boundary','M6':'schur_endpoint',
           'M7':'zero_atom_boundary'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def rational(*values):
    if any(type(x) is not F for x in values):
        raise TypeError('exact Fraction inputs required')

def harmonic(u, v):
    rational(u, v)
    require(u >= 0 and v >= 0 and u + v > 0, 'nonnegative weights, positive sum required')
    return u*v/(u+v)

def floors(p, r, s, t):
    """Probability-law floors from lower masses at distinct squared radii."""
    rational(p, r, s, t)
    require(p > 0 and r > 0 and p+r <= 1, 'positive probability masses required')
    require(s >= 0 and t >= 0 and s != t, 'distinct nonnegative squared radii required')
    return {'m2':p*s+r*t, 'gap':harmonic(p,r)*(s-t)**2,
            'delta':harmonic(p*s,r*t)*(s-t)**2}

def moments(law):
    """Raw even moments of a finite NONNEGATIVE measure, not necessarily mass1."""
    for squared_radius, mass in law:
        rational(squared_radius, mass)
        require(squared_radius >= 0 and mass >= 0, 'nonnegative measure required')
    return tuple(sum((mass*squared_radius**n for squared_radius,mass in law),F(0))
                 for n in (1,2,3))

def direct(m2, m4, m6, q):
    """Subtractive Schur/cumulant expressions, independent of floor formulas."""
    rational(m2,m4,m6,q)
    require(m2 > 0 and F(0) <= q <= F(1,4), 'positive second moment and physical q required')
    k4=m4-3*m2*m2; k6=m6-15*m4*m2+30*m2**3
    alpha=m4-2*k4*q; gamma=m2*m2+2*k4*q
    det=alpha*gamma-k4*k4*q*(1-4*q)
    require(det > 0, 'positive pin determinant required')
    schur=alpha-(gamma**3+(2*gamma+alpha)*k4*k4*q*(1-4*q))/det
    tau=6*m2**3+9*m2*k4*(1-2*q)+(k6-k4*k4/m2)*(1-3*q)
    return det,schur,tau

def directional(p,r,s,t,m2_upper,m4_upper):
    """Requires ACTUAL moment upper bounds; consistency checks do not certify them."""
    rational(m2_upper,m4_upper)
    f=floors(p,r,s,t); ell,g,d=f['m2'],f['gap'],f['delta']
    require(s > 0 and t > 0, 'strict Delta requires two nonzero radii')
    require(m2_upper >= ell and m4_upper >= ell*ell+g, 'inconsistent upper bounds')
    dmin=min(ell*ell*(ell*ell+g),g*(4*ell*ell+g)/4)
    dmax=max(m2_upper*m2_upper*m4_upper,
             (m4_upper-ell*ell)*(m4_upper+3*m2_upper*m2_upper)/4)
    return {'det':dmin,'schur':ell*ell*g*(2*ell*ell+g)/dmax,
            'tau':min(d,(d+9*ell*g)/4)}

def laws():
    masses=((F(1,5),F(1,3)),(F(1,2),F(1,2)),(F(1,9),F(2,9)),(F(1,8),F(3,4)))
    radii=((F(1,9),F(4,9)),(F(1),F(4)),(F(1),F(9)),(F(4),F(25)),(F(1,4),F(25,4)))
    for p,r in masses:
        for s,t in radii:
            for other in (F(0),(s+t)/2,2*t):
                yield p,r,s,t,[(s,p),(t,r),(other,1-p-r)]

def check(mutant=None):
    checks={name:True for name in MUTANTS.values()}
    count={'completion':0,'finite_laws':0,'directional_cases':0,'boundary_cases':2}
    for u in (F(1,7),F(1),F(4)):
        for v in (F(1,9),F(2),F(7)):
            for a,b,c in ((F(-3),F(2),F(1)),(F(1),F(4),F(0)),(F(1),F(4),(u+4*v)/(u+v))):
                lower=harmonic(u,v)*(a-b)**2*(2 if mutant=='M1' else 1)
                rhs=lower+(u+v)*(c-(u*a+v*b)/(u+v))**2
                checks['square_completion'] &= u*(a-c)**2+v*(b-c)**2==rhs
                count['completion']+=1
    for p,r,s,t,law in laws():
        m2,m4,m6=moments(law); f=floors(p,r,s,t)
        gap=f['gap']*(2 if mutant=='M2' else 1)
        delta=f['delta']/(s*t) if mutant=='M3' else f['delta']
        checks['fourth_floor'] &= gap <= m4-m2*m2
        checks['delta_floor'] &= delta <= m6-m4*m4/m2
        count['finite_laws']+=1
        for u2,u4 in ((m2,m4),(2*m2,2*m4)):
            df=directional(p,r,s,t,u2,u4)
            if mutant=='M4': df['tau']=max(f['delta'],(f['delta']+9*f['m2']*f['gap'])/4)
            if mutant=='M6':
                ell,g=f['m2'],f['gap']
                wrong=min(u2*u2*u4,(u4-ell*ell)*(u4+3*u2*u2)/4)
                df['schur']=ell*ell*g*(2*ell*ell+g)/wrong
            for q in (F(0),F(1,64),F(1,8),F(1,4)):
                det,schur,tau=direct(m2,m4,m6,q)
                checks['tau_endpoint'] &= df['tau']<=tau
                checks['schur_endpoint'] &= df['schur']<=schur and df['det']<=det
                count['directional_cases']+=1
    m2,m4,_=moments([(F(1),F(2))]); residual=2*(1-m2)**2
    checks['probability_boundary']=(residual==m4-m2*m2) if mutant=='M5' else (residual!=m4-m2*m2)
    m2,m4,m6=moments([(F(0),F(1,2)),(F(1),F(1,2))])
    checks['zero_atom_boundary']=(m4>m2*m2 and ((m6-m4*m4/m2>0) if mutant=='M7' else (m6-m4*m4/m2==0)))
    failed=[name for name,ok in checks.items() if not ok]
    return {'ok':not failed,'checks':checks,'failed':failed,'controls':count,
            'method':'exact finite diagnostics; not continuum or Lean proof','scientific_effect':'NONE'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant')
    args=parser.parse_args()
    if args.mutant is not None and args.mutant not in MUTANTS:
        print('unknown mutant');return 2
    result=check(args.mutant)
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0 if result['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
