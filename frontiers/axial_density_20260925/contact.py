"""Exact finite-pin algebra for the inner axial belt; no stochastic certification."""
from fractions import Fraction as F
from typing import Sequence

Rational = int | F


def rational(value: Rational) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError('Exact int or Fraction required; bool/float is not accepted')
    return F(value)


def radius(value: Rational) -> F:
    r = rational(value)
    if r <= 0:
        raise ValueError('r must be positive')
    return r


def hermite(r: Rational, pins: Sequence[Rational]) -> tuple[F, ...]:
    """Return H(0), H'(0), H''(0), H'''(0), L(0), L'(0).

    Pins are (g(-r/2), g'(-r/2), g(r/2), g'(r/2), h(-r/2), h(r/2)).
    H is the unique cubic Hermite interpolant and L the linear interpolant.
    """
    r = radius(r)
    if len(pins) != 6:
        raise ValueError('Exactly six observations are required')
    gm, gxm, gp, gxp, hm, hp = map(rational, pins)
    a = r / 2
    S0 = (gm + gp) / 2
    D0 = (gp - gm) / (2*a)
    S1 = (gxm + gxp) / 2
    D1 = (gxp - gxm) / (2*a)
    return (S0-a*a*D1/2, (3*D0-S1)/2, D1,
            3*(S1-D0)/(a*a), (hm+hp)/2, (hp-hm)/(2*a))


def normalized(r: Rational, u: Rational, w: Rational,
               pins: Sequence[Rational], raw_gradient: Sequence[Rational]) -> tuple[F, F]:
    """Unconditional linear normalization at (x,z)=(r*u,r^2*w).

    Subtract r^2*w*L' BEFORE conditioning: its pinned value is zero but its
    unconditioned variance is not. Omitting it invalidates the covariance limit.
    """
    r, u, w = radius(r), rational(u), rational(w)
    if len(raw_gradient) != 2:
        raise ValueError('A two-component gradient is required')
    gx, gz = map(rational, raw_gradient)
    h0, h1, h2, h3, l0, lp = hermite(r, pins)
    x = r*u
    hprime = h1 + h2*x + h3*x*x/2
    linear = l0 + lp*x
    return ((gx - hprime - r*r*w*lp) / r**3,
            (gz - linear) / r**2)


def limit_rows(u: Rational, w: Rational, Q: Rational, T: Rational, S: Rational) -> tuple[F, F]:
    """Contact rows on random jets Q=f_xxxx, T=f_xxz, S=f_zz."""
    u, w, Q, T, S = map(rational, (u,w,Q,T,S))
    offset = u*u - F(1,4)
    return (u*offset*Q/6 + u*w*T, offset*T/2 + w*S)


def density_jacobian(r: Rational) -> F:
    """Determinant for W -> raw gradient; density uses its reciprocal."""
    r = radius(r)
    return r**5
