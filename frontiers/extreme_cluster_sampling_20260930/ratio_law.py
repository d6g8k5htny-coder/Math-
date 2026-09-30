"""Universal extreme-doublet shape: exact rational controls and a float simulator.

The density is for the already-formed limiting microscopic extreme doublet,
not finite-r field samples. sample_doublet uses ordinary floating-point random
numbers for experimentation; it is not an exact-real or interval sampler.
"""
from fractions import Fraction as F
from math import comb, sqrt
import random
import extremes as e


def _unit(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise TypeError('integer or Fraction required')
    x=F(x)
    if not 0<=x<=1: raise ValueError('unit interval required')
    return x


def coordinates(rho,z):
    """Continuous square extension of the outer root's (u,v); interior is typed."""
    rho,z=_unit(rho),_unit(z)
    den=2*rho*z+rho+1
    p=(2*rho*z*z+2*rho*z+rho+2*z+1)/(2*den)
    ell=(1+2*rho*z/(1+rho))/2
    return -p,(12*p*p-3)*ell


def acceptance(rho,z):
    rho,z=_unit(rho),_unit(z)
    return ((rho*z+1)**4*(rho*z+rho+1)**7 /
            ((rho+1)**5*(2*rho*z+rho+1)**9))


def density(rho,z):
    """Unnormalized positive density Q(u,v)|d(u,v)/d(rho,z)|; integral is J."""
    rho,z=_unit(rho),_unit(z)
    return 165888*rho*z**7*(z+1)**4*acceptance(rho,z)


def heights(rho,z):
    """Downward heights of outer and companion roots, respectively."""
    rho,z=_unit(rho),_unit(z)
    den=(rho+1)*(2*rho*z+rho+1)
    outer=z*z*(rho*z+1)*(rho*z+2*rho+1)/den
    inner=rho**3*z*z*(z+1)*(rho*z+rho+2)/den
    return outer,inner


def z_normalizer():
    return sum((F(comb(4,j),8+j) for j in range(5)),F(0))


def small_ratio_constant():
    """CDF coefficient P(rho<epsilon | extreme doublet) ~ C epsilon^2."""
    return F(82944)*z_normalizer()/e.outer_double_mass()


def proposal_mean():
    """Mean number of ideal-real proposals in the proved rejection algorithm."""
    return small_ratio_constant()


def endpoint_density():
    """Normalized marginal density at rho=1-, as rational + coefficient*log(2)."""
    J=e.outer_double_mass()
    return F(2571669,2240)/J,-F(81,8)/J


def small_ratio_height_mean():
    return (sum((F(comb(4,j),10+j) for j in range(5)),F(0)) /
            z_normalizer())


def sample_doublet(rng=None,max_trials=100000):
    """Simulate the universal extreme-doublet scalar marks (ordinary floats).

    Seeding random.Random makes this reproducible. No Gaussian orientation,
    amplitude, finite-r field, or Pareto overall scale is simulated here.
    Numerical roundoff is not enclosed; the ideal-real algorithm is proved
    in COMPANION_RATIO.md. A bounded trial budget fails explicitly.
    """
    if isinstance(max_trials,bool) or not isinstance(max_trials,int) or max_trials<1:
        raise ValueError('positive integer trial budget required')
    rng=random.Random() if rng is None else rng
    # Exact mixture weights C(4,j)/(8+j), multiplied by3960; sum=6401.
    weights=(495,1760,2376,1440,330)
    for trial in range(1,max_trials+1):
        ticket=rng.randrange(6401)
        for j,weight in enumerate(weights):
            if ticket<weight:break
            ticket-=weight
        u,v=rng.random(),rng.random()
        if not 0<u<1 or not 0<v<1:continue
        rho=sqrt(u); z=v**(1/(8+j))
        if not 0<rho<1 or not 0<z<1:continue
        a=((rho*z+1)**4*(rho*z+rho+1)**7 /
           ((rho+1)**5*(2*rho*z+rho+1)**9))
        if rng.random()>=a:continue
        den=(rho+1)*(2*rho*z+rho+1)
        return {'radius_ratio':rho,'shape_coordinate':z,
                'height_maximum':z*z*(rho*z+1)*(rho*z+2*rho+1)/den,
                'height_companion':rho**3*z*z*(z+1)*(rho*z+rho+2)/den,
                'proposals':trial}
    raise RuntimeError('extreme-doublet rejection sampler exhausted its trial budget')
