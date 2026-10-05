"""Exact finite controls, not proofs of Gaussian or persistence hypotheses.

All probabilities and scalar inputs must be integers or Fractions. Marks are
arbitrary hashable labels in a finite model. Total variation means half the L1
distance between probability measures, equivalently the supremum over events.
"""

from collections import defaultdict
from fractions import Fraction


def _rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError("exact integer or Fraction required")
    return Fraction(value)


def _integer(value, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("integer required")
    if positive and value <= 0:
        raise ValueError("positive integer required")
    return value


def _probabilities(law):
    weights = {label: _rational(p) for label, p in law.items()}
    if any(p < 0 for p in weights.values()) or sum(weights.values()) != 1:
        raise ValueError("probabilities must be nonnegative and sum to one")
    return weights


def count_statistics(law):
    """Statistics of a finite distribution of a nonnegative integer count."""
    for k in law:
        if _integer(k) < 0:
            raise ValueError("count must be nonnegative")
    weights = _probabilities(law)
    mean = sum((p * k for k, p in weights.items()), Fraction(0))
    occurrence = sum((p for k, p in weights.items() if k > 0), Fraction(0))
    excess = sum((p * max(k - 1, 0) for k, p in weights.items()), Fraction(0))
    multi_mass = sum((p * k for k, p in weights.items() if k >= 2), Fraction(0))
    factorial = sum((p * k * (k - 1) for k, p in weights.items()), Fraction(0))
    multi_probability = sum((p for k, p in weights.items() if k >= 2), Fraction(0))
    return {"mean": mean, "occurrence": occurrence, "excess": excess,
            "multi_mass": multi_mass, "second_factorial": factorial,
            "conditional_multi": multi_probability / occurrence if occurrence else None}


def total_variation(left, right):
    """Exact TV of finite probability measures, with missing atoms given mass 0."""
    left, right = _probabilities(left), _probabilities(right)
    return sum((abs(left.get(label, 0) - right.get(label, 0))
                for label in set(left) | set(right)), Fraction(0)) / 2


def mark_statistics(fields):
    """Compare intensity sampling with field-first uniform-bar sampling.

    Each input is (field probability, sequence of that field's bar marks).
    Repeated marks retain their bar multiplicity. A zero occurrence probability
    produces None for normalized laws rather than inventing a conditional law.
    """
    rows = []
    counts = defaultdict(Fraction)
    for probability, marks in fields:
        p = _rational(probability)
        if not isinstance(marks, (tuple, list)):
            raise ValueError("marks must be a finite tuple or list")
        marks = tuple(marks)
        try:
            for label in marks:
                hash(label)
        except TypeError as exc:
            raise ValueError("marks must be hashable") from exc
        if p < 0:
            raise ValueError("negative field probability")
        rows.append((p, marks))
        counts[len(marks)] += p
    summary = count_statistics(counts)
    m, p, e = summary["mean"], summary["occurrence"], summary["excess"]
    if not p:
        return dict(summary, field_first=None, intensity=None, excess_law=None,
                    tv=None, tv_bound=None)
    intensity, field, defect = (defaultdict(Fraction) for _ in range(3))
    for probability, marks in rows:
        k = len(marks)
        if not k or not probability:
            continue
        for label in marks:
            intensity[label] += probability
            field[label] += probability / k
            defect[label] += probability * (k - 1) / k
    intensity = {label: value / m for label, value in intensity.items() if value}
    field = {label: value / p for label, value in field.items() if value}
    defect = {label: value / e for label, value in defect.items() if value} if e else None
    return dict(summary, field_first=field, intensity=intensity, excess_law=defect,
                tv=total_variation(field, intensity), tv_bound=e / m)


def radial_pushforward(amplitude, radial_power, gap_power=3):
    """A r^a dr under ell=k r^q: (prefactor, k-power, ell-power).

    Fractional powers remain symbolic; no floating evaluation is substituted.
    """
    amplitude = _rational(amplitude)
    a, q = _integer(radial_power), _integer(gap_power, positive=True)
    order = Fraction(a + 1, q)
    return amplitude / q, -order, order - 1


def radial_cumulative(amplitude, radial_power, gap_power=3):
    """Integral from zero of A r^a dr, requiring a > -1."""
    amplitude = _rational(amplitude)
    a, q = _integer(radial_power), _integer(gap_power, positive=True)
    if a <= -1:
        raise ValueError("radial measure is not integrable at zero")
    order = Fraction(a + 1, q)
    return amplitude / (a + 1), -order, order


def radial_density_at_r(amplitude, radial_power, kappa, r, gap_power=3):
    """Evaluate A r^a / (d ell / dr) in exact rational arithmetic."""
    amplitude = _rational(amplitude)
    a, q = _integer(radial_power), _integer(gap_power, positive=True)
    kappa, r = _rational(kappa), _rational(r)
    if kappa <= 0 or r <= 0:
        raise ValueError("positive gap coefficient and separation required")
    return amplitude * r ** a / (q * kappa * r ** (q - 1))


def fold_jet(a, r, x):
    """(g,g',g'',g''') for g=a(x^3/3-r^2 x/4), a,r>0.

    g' is strictly convex since g'''=2a>0. The left endpoint is a longitudinal
    maximum and the right endpoint a longitudinal minimum. Adding negative
    transverse quadratic directions gives the local max/saddle model only;
    this finite calculation does not identify an actual persistence pairing.
    """
    a, r, x = _rational(a), _rational(r), _rational(x)
    if a <= 0 or r <= 0:
        raise ValueError("positive cubic coefficient and separation required")
    return (a * (x ** 3 / 3 - r ** 2 * x / 4),
            a * (x ** 2 - r ** 2 / 4), 2 * a * x, 2 * a)


def curved_ridge_third(k, r, q, x):
    """Raw f_xxx versus reduced g''' for a polynomial with a curved ridge.

    f=-kr^3/2+2kx^3-3kr^2*x/2-(z-q(x^2-r^2/4))^2/2.
    Differentiate its bivariate coefficients directly, then use the implicit
    ridge tangent v=-f_xz/f_zz. This checks the derivative correction omitted by
    the false substitution g'''=f_xxx away from the contact point.
    """
    k, r, q, x = map(_rational, (k, r, q, x))
    if k <= 0 or r <= 0:
        raise ValueError("positive gap coefficient and separation required")
    coefficients = {(0, 0): -k * r ** 3 / 2 - q ** 2 * r ** 4 / 32,
                    (3, 0): 2 * k, (1, 0): -3 * k * r ** 2 / 2,
                    (0, 2): Fraction(-1, 2), (2, 1): q,
                    (0, 1): -q * r ** 2 / 4, (4, 0): -q ** 2 / 2,
                    (2, 0): q ** 2 * r ** 2 / 4}
    z = q * (x ** 2 - r ** 2 / 4)

    def derivative(dx, dz):
        answer = Fraction(0)
        for (i, j), coefficient in coefficients.items():
            if i < dx or j < dz:
                continue
            factor = 1
            for step in range(dx):
                factor *= i - step
            for step in range(dz):
                factor *= j - step
            answer += coefficient * factor * x ** (i - dx) * z ** (j - dz)
        return answer

    raw = derivative(3, 0)
    v = -derivative(1, 1) / derivative(0, 2)
    reduced = raw + 3 * derivative(2, 1) * v + 3 * derivative(1, 2) * v ** 2 + derivative(0, 3) * v ** 3
    return raw, reduced
