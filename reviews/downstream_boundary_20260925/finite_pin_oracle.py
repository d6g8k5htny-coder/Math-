"""Independent exact polynomial oracle for PR9's finite-r pin interface.

Standard library only. This checks deterministic identities, not a Gaussian
Kac-Rice theorem, a probability bound, or an independent acceptance predicate.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json

NAMES = ('r', 'x', 'y', 'b', 'k', 'a', 'q', 'c', 'd', 'u', 'v')
ZERO = (0,) * len(NAMES)


class P:
    """Sparse polynomial over Q in the fixed indeterminates NAMES."""
    def __init__(self, terms=None):
        self.terms = {m: Q(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def coerce(value):
        if isinstance(value, P):
            return value
        if type(value) is int or isinstance(value, Q):
            return P({ZERO: Q(value)})
        raise TypeError('exact polynomial, integer or Fraction required')

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in self.coerce(other).terms.items():
            out[m] = out.get(m, Q(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        out = {}
        for m, a in self.terms.items():
            for n, b in self.coerce(other).terms.items():
                key = tuple(x + y for x, y in zip(m, n))
                out[key] = out.get(key, Q(0)) + a * b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, denominator):
        if type(denominator) is not int and not isinstance(denominator, Q):
            raise TypeError('division only by an exact scalar')
        if not denominator:
            raise ZeroDivisionError
        return P({m: c / Q(denominator) for m, c in self.terms.items()})

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError('nonnegative integer exponent required')
        result = self.coerce(1)
        for _ in range(n):
            result = result * self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def diff(self, name):
        i = NAMES.index(name)
        out = {}
        for m, c in self.terms.items():
            if m[i]:
                n = list(m)
                n[i] -= 1
                out[tuple(n)] = c * m[i]
        return P(out)

    def sub(self, **values):
        result = P()
        for m, c in self.terms.items():
            term = self.coerce(c)
            for name, power in zip(NAMES, m):
                if power:
                    term *= self.coerce(values.get(name, variable(name))) ** power
            result += term
        return result

    def value(self, **values):
        out = self.sub(**values)
        if any(m != ZERO for m in out.terms):
            raise ValueError('not all required variables were specified')
        return out.terms.get(ZERO, Q(0))

    def text(self):
        if not self.terms:
            return '0'
        pieces = []
        for m, c in sorted(self.terms.items()):
            monomial = '*'.join(name if e == 1 else f'{name}^{e}'
                                for name, e in zip(NAMES, m) if e)
            pieces.append(str(c) + ('*' + monomial if monomial else ''))
        return ' + '.join(pieces)


def variable(name):
    exponents = list(ZERO)
    exponents[NAMES.index(name)] = 1
    return P({tuple(exponents): Q(1)})


r, x, y, b, k, a, q, c, d, u, v = map(variable, NAMES)


def family(mutant=None):
    """Cubic in x,y; all six original endpoint constraints hold exactly."""
    result = (b - k*r**3/2 + 2*k*x**3 - 3*k*r**2*x/2
              + a*y**2/2 + q*(x**2-r**2/4)*y/2
              + c*x*y**2/2 + d*y**3/6)
    if mutant == 'drop_axial_pin_correction':
        result += 3*k*r**2*x/2
    elif mutant == 'drop_height_offset':
        result += k*r**3/2
    elif mutant == 'drop_transverse_pin_correction':
        result += q*r**2*y/8
    elif mutant is not None:
        raise ValueError('unknown mutant')
    return result


def pin_residuals(f):
    out = {}
    for label, location, height in [('M', -r/2, b), ('S', r/2, b-k*r**3)]:
        out[label+'_height'] = f.sub(x=location, y=0) - height
        out[label+'_dx'] = f.diff('x').sub(x=location, y=0)
        out[label+'_dy'] = f.diff('y').sub(x=location, y=0)
    return out


def contact_rows():
    jx = 6*k*(u**2-Q(1,4)) + q*u*v + c*v**2/2
    jy1 = a*v
    jy2 = q*(u**2-Q(1,4))/2 + c*u*v + d*v**2/2
    h2 = a*v**2/2
    h3 = (k*(2*u**3-3*u/2-Q(1,2))
          + q*(u**2-Q(1,4))*v/2 + c*u*v**2/2 + d*v**3/6)
    return jx, jy1, jy2, h2, h3


def report():
    f = family()
    jx, jy1, jy2, h2, h3 = contact_rows()
    old_jx = 6*k*u**2 + q*u*v + c*v**2/2
    old_jy_axis = q*u**2/2
    old_h3 = 2*k*u**3 + q*u**2*v/2 + c*u*v**2/2 + d*v**3/6
    residuals = pin_residuals(f)
    scaled = {
        'dx': f.diff('x').sub(x=r*u, y=r*v) - r**2*jx,
        'dy': f.diff('y').sub(x=r*u, y=r*v) - r*jy1-r**2*jy2,
        'height': f.sub(x=r*u, y=r*v)-b-r**2*h2-r**3*h3,
    }
    if not all(p == 0 for p in [*residuals.values(), *scaled.values()]):
        raise RuntimeError('independent oracle failed its exact identities')
    return {
        'object': 'OA-FINITE-PIN-ORACLE-20260925-v1',
        'reviewed_pr9_commit': 'fb5bd52d87f25671e72b0100f59773dbd69fb646',
        'pin_residuals': {n: p.text() for n, p in residuals.items()},
        'corrected_scaled_identity_residuals': {n: p.text() for n, p in scaled.items()},
        'old_minus_corrected_contact_rows': {
            'dx': (old_jx-jx).text(),
            'axial_dy': (old_jy_axis-jy2.sub(v=0)).text(),
            'height_r3_coefficient': (old_h3-h3).text(),
        },
        'rational_example': {
            'k': '1', 'a': '-2', 'q': '0', 'c': '0', 'd': '0', 'u': '2', 'v': '0',
            'true_dx_over_r2': '45/2', 'pr9_dx_over_r2': '24',
            'true_height_minus_b_over_r3': '25/2', 'pr9_height_coefficient': '16',
        },
        'conclusion': 'PR9 displayed raw finite-r Taylor/contact formulas fail original pins; amendment required',
        'not_claimed': ['a Gaussian sample counterexample', 'refutation of the persistence theorem',
                        'a Gaussian density bound', 'full RN closure', 'scientific promotion'],
    }


if __name__ == '__main__':
    print(json.dumps(report(), indent=2, sort_keys=True))
