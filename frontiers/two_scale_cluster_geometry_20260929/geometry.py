"""Exact finite controls for two-scale geometry and the limiting radial tail.

Standard library only. No Gaussian integral is numerically approximated.
Sparse polynomials have keys (power_of_u, power_of_v) and Fraction values.
"""
import argparse
from fractions import Fraction as F
import json
import math

MUTANTS = ('omit-jet-factor-two', 'omit-z-reflection', 'power-ten',
           'wrong-cusp', 'height-reversed', 'wrong-window', 'wrong-k-power',
           'half-root-jacobian')


def rational(x):
    if type(x) not in (int, F):
        raise ValueError('exact int or Fraction required')
    return F(x)


def nonnegative_integer(q):
    if type(q) is not int or q < 0:
        raise ValueError('nonnegative integer required')
    return q


def positive_k(k):
    k = rational(k)
    if k <= 0:
        raise ValueError('positive k required')
    return k


def add(p, q):
    out = dict(p)
    for powers, c in q.items():
        out[powers] = out.get(powers, F(0)) + c
    return {powers:c for powers,c in out.items() if c}


def scale(p, c):
    c = rational(c)
    return {powers:c*a for powers,a in p.items() if c*a}


def mul(p, q):
    out = {}
    for (i,j), a in p.items():
        for (k,l), b in q.items():
            powers = (i+k,j+l)
            out[powers] = out.get(powers,F(0))+a*b
    return {powers:c for powers,c in out.items() if c}


def power(p, n):
    nonnegative_integer(n)
    out = {(0,0): F(1)}
    for _ in range(n):
        out = mul(out,p)
    return out


def integrate_strip(poly, lower, upper, left, right):
    """Exact integral: u in [left,right], polynomial lower(u)<=v<=upper(u)."""
    left, right = map(rational,(left,right))
    if left > right or any(j for i,j in set(lower)|set(upper)):
        raise ValueError('ordered endpoints and univariate bounds required')
    out = {}
    for (i,j), c in poly.items():
        v_integral = add(power(upper,j+1),scale(power(lower,j+1),-1))
        out = add(out,mul({(i,0): c/F(j+1)},v_integral))
    return sum((c*(right**(i+1)-left**(i+1))/F(i+1)
                for (i,j),c in out.items()),F(0))


def shape_polynomial():
    b = {(0,0):F(3),(2,0):F(-12)}
    return mul(add({(0,2):F(4)},scale(mul(b,b),-1)),
               add(b,{(1,1):F(-4)}))


def shape_integrals(height_order=0):
    nonnegative_integer(height_order)
    b = {(0,0):F(3),(2,0):F(-12)}
    upper = {(0,0):F(3),(1,0):F(-6)}
    height = {(0,0):F(1,2),(1,0):F(1),(0,1):F(1,6)}
    poly = mul(shape_polynomial(),power(height,height_order))
    return (integrate_strip(poly,scale(b,F(-1,2)),upper,F(-3,2),F(-1,2)),
            integrate_strip(poly,scale(b,F(1,2)),upper,F(-1,2),F(1,2)))


def radial_factor(k):
    """Coefficient multiplying the remaining spectral/Gaussian cusp integral."""
    return F(216,11)*positive_k(k)**7*sum(shape_integrals())


def tail_power():
    return 2+2+3+4  # ds,dB,dD and the typed determinant weight


def height_moment(q):
    """Exact integral of eta^q H_eta(eta), without probability normalization."""
    nonnegative_integer(q)
    beta = F(math.factorial(q),1)
    for j in range(q+1):
        beta /= F(9,2)+j
    return (F(110592,7)*(1/(F(q)+F(9,2))-beta+F(1,q+1))
            +13824*(F(1,q+5)-F(2,q+4)+F(5,q+3)-F(4,q+2)))


def raw_jet(k,a,B,D):
    k = positive_k(k)
    a,B,D = map(rational,(a,B,D))
    return a*a/(12*k)+B, a**3/(144*k*k)+a*B/(4*k)+2*D


def point_map(k,u,v,z,a):
    """Recover original s,a,beta,c from one canonical stationary point."""
    k = positive_k(k)
    u,v,z,a = map(rational,(u,v,z,a))
    if z == 0:
        raise ValueError('nonzero transverse coordinate required')
    b = 3-12*u*u
    s = -k*v/z**2
    B = k*b/z**2
    D = k*(v-b*u)/z**3
    beta,c = raw_jet(k,a,B,D)
    return s,a,beta,c


def cubic_gradient(k,s,a,beta,c,X,Z):
    k = positive_k(k)
    s,a,beta,c,X,Z = map(rational,(s,a,beta,c,X,Z))
    return (6*k*X*X-F(3,2)*k+a*X*Z+beta*Z*Z/2,
            s*Z+a*(X*X-F(1,4))/2+beta*X*Z+c*Z*Z/2)


def cubic_height(k,s,a,beta,c,X,Z):
    k = positive_k(k)
    s,a,beta,c,X,Z = map(rational,(s,a,beta,c,X,Z))
    return (2*k*X**3-F(3,2)*k*X-k/2+s*Z*Z/2
            +a*(X*X-F(1,4))*Z/2+beta*X*Z*Z/2+c*Z**3/6)


def root_jacobian(k,u,v,z):
    k = positive_k(k)
    u,v,z = map(rational,(u,v,z))
    if z == 0:
        raise ValueError('nonzero transverse coordinate required')
    return 6*k**3*(12*u*u+4*u*v-3)/z**8


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run_checks(mutant=None):
    raw = raw_jet(1,6,0,0)
    if mutant == 'wrong-cusp': raw = (raw[0],F(3))
    require(raw == (F(3),F(3,2)), 'cusp raw-coordinate inverse')
    exponent = 10 if mutant == 'power-ten' else tail_power()
    require(exponent == 11,'weighted radial homogeneity')
    volume = sum(shape_integrals())
    if mutant == 'wrong-window': volume = shape_integrals()[1]
    require(volume == F(246528,35),'both typed height-window strips')
    factor = radial_factor(1)
    if mutant in ('omit-jet-factor-two','omit-z-reflection','half-root-jacobian'):
        factor /= 2
    require(factor == F(53250048,385),'raw-jet, root-Jacobian and sign factors')
    value = radial_factor(2)
    if mutant == 'wrong-k-power': value /= 2
    require(value == 128*factor,'k-to-the-seventh scaling')
    mean = height_moment(1)/height_moment(0)
    if mutant == 'height-reversed': mean = 1-mean
    require(mean == F(5771,7062),'height measured downward from birth')
    for q in range(7):
        require(sum(shape_integrals(q)) == height_moment(q),
                'independent double-integral/height-density moment comparison')
    cases = 0
    for k in (F(1,2),F(1),F(2)):
        for u in (F(-5,4),F(-1),F(-3,4),F(-1,4),F(0),F(1,4)):
            b = 3-12*u*u
            for frac in (F(1,4),F(1,2),F(3,4)):
                v = abs(b)/2+frac*(3-6*u-abs(b)/2)
                for z in (F(-3),F(-1),F(1,2),F(2)):
                    for a in (F(-2),F(0),F(6)):
                        s,a,beta,c = point_map(k,u,v,z,a)
                        X = u-a*z/(12*k)
                        require(cubic_gradient(k,s,a,beta,c,X,z)==(0,0),'stationary map')
                        eta = u+F(1,2)+v/6
                        require(0<eta<1,'open height-window map')
                        require(cubic_height(k,s,a,beta,c,X,z)==-k*eta,'stationary height')
                        require(root_jacobian(k,u,v,z)<0,'nonzero oriented root Jacobian')
                        cases += 1
    return {'passed': True, 'stationary_map_cases': cases,
            'tail_exponent': 11, 'shape_integral': str(volume),
            'radial_factor_at_k1': str(factor), 'universal_height_mean':str(mean),
            'scientific_effect':'NONE', 'mathematical_acceptance':False,
            'scope':'exact finite identities, not Gaussian or limiting-law verification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=MUTANTS)
    args = parser.parse_args()
    try:
        result = run_checks(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True))
        return 1
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0


if __name__=='__main__': raise SystemExit(main())
