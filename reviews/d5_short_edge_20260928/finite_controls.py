"""Finite rational controls for the accompanying author-side D5 note.

Not a continuum proof, Gaussian regression implementation, or gate for D5.
No archived research code is imported or executed. Python standard library only.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def det(a, b, c):
    return a * c - b * b


def check(mutant=None):
    require(F(1, 2) * F(81, 16) * F(25, 32) == F(2025, 1024), "constant product")
    require(F(2025, 1024) < 2, "coarse triangle constant")
    cases = 0
    for r, k, c, d, q in itertools.product(
        [F(1, 4), F(1, 16)], [F(1), F(6, 5)],
        [F(-2), F(0), F(3)], [F(-1), F(2)], [F(-1, 8), F(1, 9)]
    ):
        t = c * q
        a0 = r * (c - d * q) / 2
        s0 = a0 if mutant == "endpoint-label" else a0 - r * c / 2
        # These follow directly by differentiation in x = -r/2+rp, z=rq.
        fx = r*r * (-t*q/2 + c*q*q/2)
        fz = r * (a0*q + r*(-c*q/2 + d*q*q/2))
        require(fx == fz == 0, "witness stationarity")
        require(s0 == -r*d*q/2, "endpoint coordinate translation")
        dm = det(-6*k*r, -r*t/2, a0-r*c/2)
        dx = det(r*(-6*k+t*q), r*(-t/2+c*q), a0-r*c/2+r*d*q)
        ds = det(6*k*r, r*t/2, a0+r*c/2)
        require(dm == q*r*r*(3*k*d-c*c*q/4), "M determinant")
        require(dx == q*r*r*(-3*k*d-c*c*q/4+c*d*q*q/2), "X determinant")
        require(ds == r*r*(6*k*c-3*k*d*q-c*c*q*q/4), "S determinant")
        product_without_q2 = (r*r*(3*k*d-c*c*q/4)
            * r*r*(-3*k*d-c*c*q/4+c*d*q*q/2)
            * r*r*(6*k*c-3*k*d*q-c*c*q*q/4))
        soft_factor = 1 if mutant == "omit-soft-factor" else q*q
        require(dm*dx*ds == soft_factor*product_without_q2, "two soft factors")
        cases += 1
    examples = 0
    # f=a(x^3/3-rx^2/2)+b(z^3/3-dz^2/2), critical triangle.
    for a, b, r, ratio in itertools.product(
        [F(-2), F(1), F(3)], [F(-2), F(1), F(3)],
        [F(1, 4), F(1, 16)], [F(1, 4), F(1, 16), F(1, 128)]
    ):
        distance = r*ratio
        lip = 2*max(abs(a), abs(b))
        product = abs(a*b*r*distance)**3
        upper = 2*lip**6*r**4*distance**2
        if mutant == "zero-bound":
            upper = F(0)
        require(product <= upper, "critical cubic triangle example")
        examples += 1
    # Dropping critical-point constraints would be false even with L=0.
    require(2**3 > 2*0**6, "quadratic noncritical counterexample")
    return {
        "scope": "finite rational algebra/examples only; not a continuum or Gaussian proof",
        "scientific_effect": "NONE",
        "coordinate_and_determinant_cases": cases,
        "critical_cubic_triangle_examples": examples,
        "noncritical_quadratic_counterexample": True,
        "coarse_constant": "2025/1024 < 2",
        "conditional_gaussian_moment_proved": False,
        "D5_closed": False,
        "passed": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutant", choices=["endpoint-label", "omit-soft-factor", "zero-bound"])
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.mutant), sort_keys=True, indent=2))
    except ValueError as exc:
        print("REJECTED: " + str(exc), file=sys.stderr)
        sys.exit(1)
