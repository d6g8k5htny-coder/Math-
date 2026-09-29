"""Exact scalar companions; not a Gaussian covariance or Kac-Rice verifier."""
from fractions import Fraction as F

MUTANT = None

def gradient_density_power(d: int) -> int:
    if type(d) is not int or d<2:
        raise ValueError('fixed integer dimension at least two required')
    return -(d+3) if MUTANT=='height-jacobian-in-gradient-frame' else -d

def radial_power(d: int) -> int:
    determinants=0 if MUTANT=='drop-soft-determinants' else 2
    return d-1+gradient_density_power(d)+determinants

def envelope_integral(p: F) -> F:
    p=F(p)
    if not -2<p<1:
        raise ValueError('weighted envelope requires -2<p<1')
    return 1/(p+2)+1/(1-p)

def overlap_coefficient(p: F) -> F:
    p=F(p)
    if p<=-2:
        raise ValueError('origin integral requires p>-2')
    numerator=1 if MUTANT=='lose-overlap-three' else 3
    return numerator/((p+2)*(p+5))

def moment_finite(p: F) -> bool:
    return F(p)>=-2 if MUTANT=='include-divergent-endpoint' else F(p)>-2

def inverse_cutoff(q: int, lo: F, hi: F):
    if type(q) is not int or q<0 or not F(0)<lo<hi:
        raise ValueError('nonnegative integer inverse power and 0<lo<hi required')
    if q==2:
        return {'kind':'log','ratio':hi/lo,'coefficient':F(1)}
    return (hi**(2-q)-lo**(2-q))/(2-q)

def small_cdf_coefficient(J: F, A: F) -> F:
    if J<=0 or A<=0:
        raise ValueError('positive intensity and mass required')
    return J/A if MUTANT=='lose-cdf-half' else J/(2*A)

def fold_data(delta: F, T: F, transverse: list[F]) -> dict:
    if delta<=0 or not transverse:
        raise ValueError('positive separation and nonempty transverse block required')
    detA=F(1)
    for a in transverse:detA*=a
    gradient=lambda x:[T*x*x/2-T*delta*x/2]+[F(0)]*len(transverse)
    value=lambda x:T*x**3/6-T*delta*x*x/4
    left=-T*delta*detA/2;right=T*delta*detA/2
    gap=value(delta)-value(F(0))
    if MUTANT=='reverse-height-sign':gap=-gap
    return {'gradients':(gradient(F(0)),gradient(delta)),
            'height_difference':gap,'determinants':(left,right),
            'absolute_product':abs(left*right)}

def height_width_power() -> int:
    return 6 if MUTANT=='two-height-windows-at-fixed-r' else 3

def microscopic_power(p: F) -> F:
    return F(5)+F(p)

def pair_weight(n: int) -> int:
    if type(n) is not int or n<0:
        raise ValueError('nonnegative integer count required')
    return int(n>=2) if MUTANT=='event-not-factorial-weight' else n*(n-1)
