#!/usr/bin/env python3
"""Exact finite C127 review controls; no author checker was consumed."""
import argparse
from fractions import Fraction as Q
import json
import sys

MUTANTS = (
    'pin_offset', 'u3_scale', 'hermite_value_term', 'chord_axis',
    'remote_midpoint_power', 'remote_product_rule', 'missing_slab_square',
    'density_dimension', 'second_normalizer', 'tail_order', 'independence',
)
COUNT = 0


def check(ok, name):
    global COUNT
    COUNT += 1
    if not ok:
        raise AssertionError(name)


def eq(a, b, name):
    check(a == b, name)


def val(c, x, d=0):
    out = Q(0)
    for n in range(d, len(c)):
        factor = 1
        for k in range(d):
            factor *= n-k
        out += c[n]*factor*x**(n-d)
    return out


def integral(c, h):
    return sum((a*h**(j+1)/Q(j+1) for j, a in enumerate(c)), Q(0))


def pin_controls(mutant):
    for r in (Q(1, 8), Q(1, 64), Q(1, 512)):
        for basis in range(6):
            a = [Q(int(k == basis)) for k in range(6)]
            c = [a[0]-r*r*a[2]/(4 if mutant == 'pin_offset' else 8),
                 a[1]-r*r*a[3]/24, a[2]/2, a[3]/6]
            fm, fs = val(c, -r/2), val(c, r/2)
            gm, gs = val(c, -r/2, 1), val(c, r/2, 1)
            zm, zs = a[4]-r*a[5]/2, a[4]+r*a[5]/2
            got = [(fm+fs)/2, (fs-fm)/r, (gs-gm)/r,
                   Q(3 if mutant == 'u3_scale' else 6)/r**2 *
                   (gm+gs-2*(fs-fm)/r), (zm+zs)/2, (zs-zm)/r]
            eq(got, a, 'physical U_r basis identity')


def hermite_controls(mutant):
    for h in (Q(1), Q(1, 8), Q(1, 1024)):
        for degree in range(6):
            c = [Q(1 if i == degree else 0) for i in range(6)]
            g0, gh, d0, dh = val(c, 0), val(c, h), val(c, 0, 1), val(c, h, 1)
            b3 = (dh+d0)/h**2-(1 if mutant == 'hermite_value_term' else 2)*(gh-g0)/h**3
            b2 = 3*(gh-g0)/h**2-(2*d0+dh)/h
            b = [g0, d0, b2, b3]
            eq([val(b, 0), val(b, h), val(b, 0, 1), val(b, h, 1)],
               [g0, gh, d0, dh], 'Hermite endpoint first jets')
            g3 = [c[j+3]*(j+3)*(j+2)*(j+1) for j in range(3)]
            weighted = [Q(0)]*5
            for j, a in enumerate(g3):
                weighted[j+1] += h*a
                weighted[j+2] -= a
            eq(b3, integral(weighted, h)/h**3, 'Hermite integral cancellation')
            sup3 = sum(abs(a)*h**j for j, a in enumerate(g3))
            check(abs(b3) <= sup3/6, 'separation-uniform cubic bound')


# Trigonometric functions are represented in a polynomial ring. Relations
# cos^2+sin^2=1 need not be reduced: evaluation and actual differentiation
# enforce them at the exact rational circle points.
ZERO = (0, 0, 0, 0)


def scalar(x):
    return {} if x == 0 else {ZERO: Q(x)}


def variable(i):
    e = [0]*4
    e[i] = 1
    return {tuple(e): Q(1)}


def add(*ps):
    out = {}
    for p in ps:
        for e, a in p.items():
            out[e] = out.get(e, Q(0))+a
    return {e: a for e, a in out.items() if a}


def scale(p, k):
    return {e: a*k for e, a in p.items() if a*k}


def mul(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            k = tuple(x+y for x, y in zip(e, f))
            out[k] = out.get(k, Q(0))+a*b
    return {e: a for e, a in out.items() if a}


def power(p, n):
    out = scalar(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def deriv(p, axis):
    c, s = 2*axis, 2*axis+1
    out = {}
    for e, a in p.items():
        for source, target, sign in ((c, s, -1), (s, c, 1)):
            if e[source]:
                f = list(e)
                f[source] -= 1
                f[target] += 1
                f = tuple(f)
                out[f] = out.get(f, Q(0))+sign*a*e[source]
    return {e: a for e, a in out.items() if a}


def evaluate(p, point):
    return sum((a*point[0]**e[0]*point[1]**e[1]*point[2]**e[2]*point[3]**e[3]
                for e, a in p.items()), Q(0))


def jet(p, point):
    return [evaluate(p, point), evaluate(deriv(p, 0), point), evaluate(deriv(p, 1), point)]


def vv(p, v):
    out = Q(0)
    origin = (Q(1), Q(0), Q(1), Q(0))
    for i in range(2):
        for j in range(2):
            out += v[i]*v[j]*evaluate(deriv(deriv(p, i), j), origin)
    return out


def circle(t):
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)


def angle_multiple(z, n):
    c, s = Q(1), Q(0)
    for _ in range(abs(n)):
        c, s = c*z[0]-s*z[1], s*z[0]+c*z[1]
    return c, s if n >= 0 else -s


def psi(point):
    return add(scalar(2), *(scale(variable(i), -point[i]) for i in range(4)))


def sine_chart(point):
    return [add(scale(variable(2*j+1), point[2*j]),
                scale(variable(2*j), -point[2*j+1])) for j in range(2)]


def geometry_controls(mutant):
    origin = (Q(1), Q(0), Q(1), Q(0))
    remote = circle(Q(1, 2))+circle(Q(-1, 3))
    for tsmall, ns, u in ((Q(1, 4096), (3, 4), (Q(3, 5), Q(4, 5))),
                          (Q(1, 8192), (1, 0), (Q(1), Q(0)))):
        base = circle(tsmall)
        plus = angle_multiple(base, ns[0])+angle_multiple(base, ns[1])
        minus = tuple(a if i % 2 == 0 else -a for i, a in enumerate(plus))
        d = (plus[1], plus[3])
        norm2 = d[0]**2+d[1]**2
        v = (-u[1], u[0])
        nv = -d[1]*v[0]+d[0]*v[1]
        check(nv**2 >= norm2/4, 'actual chord/physical frame angle bound')
        if ns == (3, 4):
            check(nv**2 != norm2, 'rotated sine chord is not physical axis')
        q = psi(remote)
        ell = add(scale(variable(1), -d[1]), scale(variable(3), d[0]))
        correction = mul(q, power(ell, 2))
        response = 2*evaluate(q, origin)*(norm2 if mutant == 'chord_axis' else nv**2)
        eq(vv(correction, v), response, 'finite-r midpoint Hessian response')
        eq(jet(correction, minus)+jet(correction, plus)+jet(correction, remote),
           [Q(0)]*9, 'quadratic correction kills all three first jets')
        # These rational chart coordinates have endpoints (0,0),(1,0).
        tc = add(scalar(Q(1, 2)), scale(variable(1), d[0]/(2*norm2)),
                 scale(variable(3), d[1]/(2*norm2)))
        zc = ell
        dt = (d[0]*plus[0]/(2*norm2), d[1]*plus[2]/(2*norm2))
        dz = (-d[1]*plus[0], d[0]*plus[2])
        jacdet = dt[0]*dz[1]-dt[1]*dz[0]
        check(jacdet != 0, 'actual chart Jacobian invertible')
        qremote = mul(mul(psi(minus), psi(plus)),
                      power(psi(origin), 1 if mutant == 'remote_midpoint_power' else 2))
        qr = jet(qremote, remote)
        sx = sine_chart(remote)
        for basis in range(10):
            target = [Q(int(k == basis)) for k in range(10)]
            ends = []
            for point, data in ((minus, target[:3]), (plus, target[3:6])):
                qj = jet(q, point)
                f = data[0]/qj[0]
                gx = (data[1]*qj[0]-data[0]*qj[1])/qj[0]**2
                gy = (data[2]*qj[0]-data[0]*qj[2])/qj[0]**2
                ft = (gx*dz[1]-gy*dz[0])/jacdet
                fz = (dt[0]*gy-dt[1]*gx)/jacdet
                ends.append((f, ft, fz))
            (f0, ft0, fz0), (f1, ft1, fz1) = ends
            coeff = [f0, ft0, 3*(f1-f0)-2*ft0-ft1, ft1+ft0-2*(f1-f0)]
            hp = add(*(scale(power(tc, k), a) for k, a in enumerate(coeff)),
                     scale(zc, fz0), scale(mul(zc, tc), fz1-fz0))
            phi0 = mul(q, hp)
            phi_pin = add(phi0, scale(correction, (target[6]-vv(phi0, v))/response))
            beta = target[7:]
            ar = beta[0]/qr[0]
            br = [(beta[j+1]*qr[0]-(0 if mutant == 'remote_product_rule' else beta[0]*qr[j+1]))/qr[0]**2
                  for j in range(2)]
            phi_remote = mul(qremote, add(scalar(ar), *(scale(sx[j], br[j]) for j in range(2))))
            phi = add(phi_pin, phi_remote)
            got = jet(phi, minus)+jet(phi, plus)+[vv(phi, v)]+jet(phi, remote)
            for coord, (actual, expected) in enumerate(zip(got, target)):
                eq(actual, expected, 'periodic ten-jet dual basis %d coordinate %d' % (basis, coord))
            check(max((sum(e) for e in phi), default=0) <= 5, 'frequency degree at most five')


def ledger_controls(mutant):
    # (r,T,rho) exponents, with no numerically estimated constants.
    endpoint = (Q(4), Q(6), Q(0))
    remote_det = (Q(0), Q(2), Q(0))
    slab = (Q(1), Q(0 if mutant == 'missing_slab_square' else 2), Q(0))
    height = (Q(3), Q(0), Q(0))
    normalizer = (Q(-4 if mutant == 'second_normalizer' else -2), Q(0), Q(0))
    dim = 3 if mutant == 'density_dimension' else 4
    density = (Q(0), Q(0), -Q(18*dim, 2))
    event = tuple(sum(x[i] for x in (endpoint, remote_det, slab, height, normalizer, density)) for i in range(3))
    eq(event, (Q(6), Q(10), Q(-36)), 'correlated weighted event exponent ledger')
    schedule = Q(1, 100)
    event_power = event[0]-schedule*event[1]+schedule*event[2]
    eq(event_power, Q(277, 50), 'truncated event power')
    count_power = (3+event_power)/2
    eq(count_power, Q(427, 100), 'counted Cauchy-Schwarz power')
    m = 500 if mutant == 'tail_order' else 600
    tail_power = Q(3, 2)+Q(m, 2)*schedule
    check(tail_power >= count_power, 'tail must be smaller than counted main term')
    eq(count_power+2, Q(627, 100), 'same full Z gives raw numerator power')
    for exponent in (1-schedule,):
        check(exponent > 0, 'simultaneous cutoff conditions eventually hold')


def correlation_controls(mutant):
    previous = Q(0)
    for r in (Q(1, 4), Q(1, 16), Q(1, 64)):
        prob = r**3
        mixed = prob*prob if mutant == 'independence' else prob
        eq(mixed, prob, 'same rare event couples both witnesses')
        ratio = mixed/r**4
        check(ratio > previous, 'moments-only O(r^4) shortcut fails')
        previous = ratio
        for p in range(7):
            eq(Q(2)**p*prob/r**3, Q(2)**p, 'fixed count moments have r^3 scale')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=MUTANTS)
    args = parser.parse_args()
    mutant = args.mutant
    pin_controls(mutant)
    hermite_controls(mutant)
    geometry_controls(mutant)
    ledger_controls(mutant)
    correlation_controls(mutant)
    print(json.dumps({'result': 'PASS', 'checks': COUNT, 'mutant': mutant,
                      'arithmetic': 'exact fractions', 'python': sys.version.split()[0],
                      'analytic_proof': False}, sort_keys=True))


if __name__ == '__main__':
    main()
