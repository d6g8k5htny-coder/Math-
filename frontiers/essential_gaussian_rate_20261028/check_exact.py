#!/usr/bin/env python3
"""Exact finite template controls; not a continuum or Gaussian probability proof."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


class Interval:
    """Closed rational intervals, with outward enclosure by exact arithmetic."""

    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        require(self.lo <= self.hi, 'interval endpoints')

    @staticmethod
    def lift(value):
        return value if isinstance(value, Interval) else Interval(value)

    def __add__(self, other):
        other = self.lift(other)
        return Interval(self.lo+other.lo, self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        other = self.lift(other)
        values = [a*b for a in [self.lo, self.hi]
                  for b in [other.lo, other.hi]]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def reciprocal(self):
        require(not self.lo <= 0 <= self.hi, 'interval division excludes zero')
        return Interval(1/self.hi, 1/self.lo)

    def __truediv__(self, other):
        return self * self.lift(other).reciprocal()

    def __rtruediv__(self, other):
        return self.lift(other) * self.reciprocal()

    def __pow__(self, power):
        require(isinstance(power, int) and power >= 0, 'nonnegative integer power')
        result = Interval(1)
        for _ in range(power):
            result = result*self
        return result


def alternating_trig(tau, sine, terms=10):
    """Alternating Taylor enclosure; 0<tau<=1 ensures decreasing terms."""
    require(0 < tau <= 1, 'Taylor fixture range')
    offset = 1 if sine else 0
    partial = sum((-1)**j*tau**(2*j+offset)/factorial(2*j+offset)
                  for j in range(terms))
    next_term = (-1)**terms*tau**(2*terms+offset)/factorial(2*terms+offset)
    return Interval(min(partial, partial+next_term),
                    max(partial, partial+next_term))


def parameters(c, s, tau):
    v = 1-c
    beta = s*(8+tau**4/v**2)/c
    gamma = 8*v/c+tau**4*(1+2*c)/(v*c)
    return v, beta, gamma


counts = {}
pin_cases = 0
negative_cases = 0
circle_fixtures = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)),
                   (F(12, 13), F(5, 13)), (F(15, 17), F(8, 17))]
for (c, s), tau in product(circle_fixtures, [F(1, 8), F(1, 4), F(3, 8)]):
    require(c*c+s*s == 1, 'exact unit circle')
    v, beta, gamma = parameters(c, s, tau)
    q = 8*v-beta*s+gamma
    first_q = 8*s-beta*c
    second_q = 8*c+beta*s
    value = v*q
    first = s*q+v*first_q
    second = c*q+2*s*first_q+v*second_q
    require(value == tau**4, 'exact lower value pin')
    require(first == 0, 'exact lower derivative pin')
    target_second = 8*v/c+tau**4*(1-2*c-2*c*c)/(v*c)
    require(second == target_second, 'exact lower second derivative')

    # Independent trigonometric expansion: constant, cos1, cos2, sin1, sin2.
    coeff = [12+gamma, -(16+gamma), F(4), -beta, beta/2]
    cos2, sin2 = 2*c*c-1, 2*s*c
    fourier_value = coeff[0]+coeff[1]*c+coeff[2]*cos2+coeff[3]*s+coeff[4]*sin2
    fourier_first = -coeff[1]*s-2*coeff[2]*sin2+coeff[3]*c+2*coeff[4]*cos2
    fourier_second = -coeff[1]*c-4*coeff[2]*cos2-coeff[3]*s-4*coeff[4]*sin2
    require(fourier_value == value, 'Fourier value identity')
    require(fourier_first == first, 'Fourier first derivative identity')
    require(fourier_second == second, 'Fourier second derivative identity')
    require(coeff[0]+coeff[1]+coeff[2] == 0, 'birth value pin')
    require(coeff[3]+2*coeff[4] == 0, 'birth derivative pin')
    require(-coeff[1]-4*coeff[2] == gamma, 'birth second derivative')

    require(v*(8*v+beta*s+gamma) != tau**4,
            'wrong sine sign must break lower value pin')
    require(v*(8*v-beta*s) != tau**4,
            'omitting positive gamma must break lower value pin')
    negative_cases += 2
    pin_cases += 1
counts['rational_circle_pin_and_fourier_cases'] = pin_cases
counts['wrong_template_counterexamples'] = negative_cases

enclosures = []
for tau in [F(1, 8), F(1, 16), F(1, 32)]:
    c = alternating_trig(tau, sine=False)
    s = alternating_trig(tau, sine=True)
    v, beta, gamma = parameters(c, s, tau)
    require(v.lo > 0 and c.lo > 0, 'positive denominator enclosures')
    require(gamma.lo > 0, 'positive gamma enclosure')
    discriminant = (8+gamma)**2-64-beta**2
    require(discriminant.lo > 0, 'strict positive trigonometric bracket')
    second = 8*v/c+tau**4*(1-2*c-2*c*c)/(v*c)
    require(second.hi < 0, 'strict axial minimum of field at lower pin')
    gamma_ratio, beta_ratio, second_ratio = gamma/tau**2, beta/tau, second/tau**2
    require(gamma_ratio.lo >= 9 and gamma_ratio.hi <= 11,
            'birth curvature ratio enclosure')
    require(beta_ratio.lo >= 11 and beta_ratio.hi <= 13,
            'sine coefficient ratio enclosure')
    require(second_ratio.lo >= -3 and second_ratio.hi <= -1,
            'lower curvature ratio enclosure')
    enclosures.append({'tau': str(tau), 'gamma_over_tau2': [9, 11],
                       'beta_over_tau': [11, 13], 'second_over_tau2': [-3, -1],
                       'positive_bracket_certified': True})
counts['rational_taylor_enclosure_cases'] = len(enclosures)

norm_cases = 0
for a0, a1, a2 in product([F(1, 2), F(2, 3)],
                           [F(1, 3), F(3, 7)], [F(1, 7), F(2, 9)]):
    constant, cosine1, cosine2 = F(12), F(-16), F(4)
    direct = constant**2/a0+cosine1**2/(2*a1)+cosine2**2/(2*a2)
    require(direct == 144/a0+128/a1+8/a2, 'leading Fourier RKHS norm identity')
    norm_cases += 1
counts['leading_rkhs_norm_cases'] = norm_cases

source_checks = []
for source in json.loads((HERE / 'SOURCES.json').read_text())['sources']:
    raw = (ROOT / source['path']).read_bytes()
    require(len(raw) == source['bytes'], 'source bytes: ' + source['id'])
    require(hashlib.sha256(raw).hexdigest() == source['sha256'],
            'source digest: ' + source['id'])
    require(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
            == source['git_blob'], 'source blob: ' + source['id'])
    source_checks.append(source['id'])

print(json.dumps({
    'status': 'PASS',
    'scope': 'Finite rational author-side template identities and Taylor '
             'enclosures only; no continuum, probability or scientific acceptance.',
    'counts': counts,
    'source_checks': source_checks,
    'proof_sha256': hashlib.sha256((HERE / 'PROOF.md').read_bytes()).hexdigest(),
    'sources_sha256': hashlib.sha256((HERE / 'SOURCES.json').read_bytes()).hexdigest(),
    'certified_finite_enclosures': enclosures,
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2, sort_keys=True))
