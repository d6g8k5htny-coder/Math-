#!/usr/bin/env python3
"""Bounded exact author controls, not continuum or Gaussian probability proofs.

All mathematics below uses integers and fractions.  The scalar Fourier example
is deliberately finite and does not satisfy the d>=2 theorem's whole spectral
class.  It checks constants and covariance normalization, not that theorem.
No sampling, numerical quadrature, symbolic package, or external write is used.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
COUNTS = {}
REJECTED = []


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def reject(condition, label):
    """An invalid candidate must fail the same algebraic predicate as a good one."""
    require(not condition, "invalid fixture unexpectedly passed: " + label)
    REJECTED.append(label)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions")
    return sum((a * b for a, b in zip(left, right)), F(0))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def inverse(matrix):
    """Gauss-Jordan inversion over Q, with explicit nonzero-pivot checks."""
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix),
            "square matrix for exact inverse")
    rows = [[F(value) for value in row] +
            [F(int(i == j)) for j in range(size)]
            for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = next((i for i in range(col, size) if rows[i][col]), None)
        require(pivot is not None, "nonsingular exact Gram matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [entry / scale for entry in rows[col]]
        for i in range(size):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[col])]
    answer = [row[size:] for row in rows]
    require(all(dot(matrix[i], [answer[k][j] for k in range(size)]) ==
                int(i == j) for i in range(size) for j in range(size)),
            "exact inverse readback")
    return answer


def padd(left, right):
    return [F(left[i] if i < len(left) else 0) +
            F(right[i] if i < len(right) else 0)
            for i in range(max(len(left), len(right)))]


def pscale(poly, scale):
    return [F(scale) * value for value in poly]


def pmul(left, right):
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def pderivative(poly, order=1):
    result = list(poly)
    for _ in range(order):
        result = [i * result[i] for i in range(1, len(result))] or [F(0)]
    return result


def peval(poly, value):
    result = F(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def pcoefficient(poly, degree):
    return poly[degree] if degree < len(poly) else F(0)


def hermite_controls():
    # Solve the cubic interpolation problem rather than inserting its answer.
    rows = [[1, 0, 0, 0], [0, 1, 0, 0],
            [1, 1, 1, 1], [0, 1, 2, 3]]
    cubic = matvec(inverse(rows), [0, 0, -1, 0])
    require(cubic == [0, 0, -3, 2], "normalized cubic Hermite interpolant")
    remainder = pmul([0, 0, 1], pmul([-1, 1], [-1, 1]))
    require(peval(cubic, F(2)) == 4, "Hermite cubic value at 2r")
    require(peval(remainder, F(2)) == 4, "Hermite remainder product at 2r")
    require(pderivative(remainder, 4) == [24], "quartic fourth derivative")
    require(4 / F(1, 6) == 24, "Hermite escape threshold 24")
    cases = 0
    for k, quartic, r, b in product([F(1, 3), F(2), F(7, 2)],
                                    [F(-9), F(-1), F(2, 5)],
                                    [F(1, 5), F(2, 7)],
                                    [F(-3), F(4, 3)]):
        normalized = padd(pscale(cubic, k), pscale(remainder, quartic))
        # Y(x)=rb+r^4 p(x/r), exactly the scaled pin convention in SA9.
        physical = [r**(4-i) * value for i, value in enumerate(normalized)]
        physical[0] += r*b
        require(peval(physical, F(0)) == r*b, "Hermite birth pin")
        require(peval(physical, r) == r*b-k*r**4, "Hermite lower pin")
        require(peval(pderivative(physical), F(0)) == 0 and
                peval(pderivative(physical), r) == 0, "Hermite gradient pins")
        d4 = peval(pderivative(physical, 4), F(0))
        require(peval(physical, 2*r)-r*b == 4*k*r**4+r**4*d4/6,
                "exact polynomial instance of SA10")
        require((peval(physical, 2*r) <= r*b) == (d4 <= -24*k),
                "Hermite quartic threshold equivalence")
        cases += 1
    reject(4 / F(1, 6) == 12, "Hermite threshold 12 instead of 24")
    reject(peval(remainder, F(2)) / 24 == F(1, 12),
           "Hermite remainder coefficient 1/12 instead of 1/6")
    reject(peval([0, 0, 3, -2], F(1)) == -1,
           "reversed cubic Hermite sign")
    COUNTS["hermite_exact_pin_cases"] = cases


def fourier_controls():
    q = {-1: F(-1), 0: F(2), 1: F(-1)}
    square = {}
    for n, a in q.items():
        for m, b in q.items():
            square[n+m] = square.get(n+m, F(0)) + a*b
    require(square == {-2: 1, -1: -4, 0: 6, 1: -4, 2: 1},
            "Laurent expansion of (2-2cos x)^2")
    require([square[0], 2*square[1], 2*square[2]] == [6, -8, 2],
            "real Fourier fixture 6-8cos x+2cos 2x")
    require(sum(square.values()) == 0, "Fourier contact value")
    require(-sum(F(n*n)*a for n, a in square.items()) == 0,
            "Fourier contact second derivative")
    require(sum(F(n**4)*a for n, a in square.items()) == 24,
            "Fourier contact fourth derivative 24 at omega=1")

    # Coordinates are (constant, cos x, sin x, cos 2x, sin 2x).
    # K(x)=a0+2a1 cos x+2a2 cos 2x, so their variances are
    # (a0,2a1,2a1,2a2,2a2).  This fixes the source RKHS normalization.
    contact = [[1, 1, 0, 1, 0], [0, 0, 1, 0, 2],
               [0, -1, 0, -4, 0], [0, 0, -1, 0, -8]]
    fourth = [0, 1, 0, 16, 0]
    profile = [F(6), F(-8), F(0), F(2), F(0)]
    require(matvec(contact, profile) == [0, 0, 0, 0],
            "finite Fourier profile satisfies every scalar contact row")
    norm_cases = 0
    equality_cases = 0
    for a0, a1, a2 in product([F(1, 2), F(2, 3)],
                              [F(1, 3), F(3, 7)], [F(1, 7), F(2, 9)]):
        variances = [a0, 2*a1, 2*a1, 2*a2, 2*a2]
        norm = sum((c*c/v for c, v in zip(profile, variances)), F(0))
        require(norm == 36/a0+32/a1+2/a2, "finite Fourier RKHS norm")
        gram = [[sum((F(x)*y*v for x, y, v in zip(row, col, variances)),
                     F(0)) for col in contact] for row in contact]
        gram_inverse = inverse(gram)
        cross = [sum((F(x)*y*v for x, y, v in zip(row, fourth, variances)),
                     F(0)) for row in contact]
        raw_variance = sum((F(x*x)*v for x, v in zip(fourth, variances)), F(0))
        coefficients = matvec(gram_inverse, cross)
        sigma4_squared = raw_variance-dot(cross, coefficients)
        require(sigma4_squared > 0, "positive exact conditional D4 variance")
        representer = [variances[j]*(fourth[j]-sum(
            (coefficients[i]*contact[i][j] for i in range(4)), F(0)))
            for j in range(5)]
        require(representer == [24*c/norm for c in profile],
                "conditional D4 representer from exact Gram inverse")
        require(sigma4_squared*norm == 24**2,
                "conditional D4 variance times profile norm")
        for k in [F(1, 4), F(1), F(5, 2)]:
            lower_action = (24*k)**2/(2*sigma4_squared)
            template_action = k*k*norm/2
            require(lower_action == template_action,
                    "finite scalar lower-bound equality")
            equality_cases += 1
        wrong_norm = 36/a0+64/a1+4/a2
        reject(wrong_norm == norm, "missing real Fourier factor 2, spectrum " +
               "/".join(str(v) for v in [a0, a1, a2]))
        reject(raw_variance == sigma4_squared,
               "unconditioned D4 variance substituted, spectrum " +
               "/".join(str(v) for v in [a0, a1, a2]))
        norm_cases += 1
    reject(6-8+1 == 0, "cos 2x coefficient 1 instead of 2")
    COUNTS["finite_fourier_norm_and_gram_cases"] = norm_cases
    COUNTS["finite_scalar_action_equality_cases"] = equality_cases


def recovery_and_scaling_controls():
    cases = 0
    for k, epsilon in product([F(1, 7), F(1), F(9, 2)],
                              [F(1, 10), F(1, 2), F(1), F(19, 10)]):
        c = -24*k*(1+epsilon)
        gamma = c/12
        require(gamma == -2*k*(1+epsilon), "strict recovery gamma")
        require(-6*k < gamma < -2*k, "strict recovery typed/essential window")
        require(gamma-6*k < 0 < gamma+6*k, "endpoint Schur signs")
        require(36*k*k-gamma*gamma == 4*k*k*(2-epsilon)*(4+epsilon) > 0,
                "strict positive typed quartic weight")
        cases += 1
    for epsilon in [F(-1, 2), F(0), F(2), F(3)]:
        gamma = -2*(1+epsilon)
        reject(-6 < gamma < -2, "recovery epsilon outside (0,2): " + str(epsilon))
    require(-2*(1+F(0)) == -2, "epsilon zero is essential-threshold boundary")
    require(-2*(1+F(2))+6 == 0, "epsilon two has degenerate saddle Schur entry")
    # Homogeneity is checked as a quadratic-form identity, including contact
    # rows and the fourth derivative.  It is not a finite proof of the cone LDP.
    vectors = [[F(6), F(-8), F(2)], [F(1, 3), F(-2, 5), F(7)]]
    weights = [F(3, 2), F(5, 7), F(11, 3)]
    scale_cases = 0
    for vector, k in product(vectors, [F(1, 9), F(2), F(11, 4)]):
        norm = sum((w*x*x for w, x in zip(weights, vector)), F(0))
        scaled = sum((w*(k*x)**2 for w, x in zip(weights, vector)), F(0))
        require(scaled == k*k*norm, "RKHS quadratic k-scaling algebra")
        scale_cases += 1
    for k in [F(1, 9), F(2), F(11, 4)]:
        profile = [F(6), F(-8), F(0), F(2), F(0)]
        require(dot([0, 1, 0, 16, 0], [-k*x for x in profile]) == -24*k,
                "quartic threshold scales linearly with k")
    reject(F(3)**2 == F(3), "linear action k law instead of quadratic law")
    COUNTS["strict_recovery_cases"] = cases
    COUNTS["quadratic_homogeneity_cases"] = scale_cases


def quintic_controls():
    cases = 0
    fixtures = [
        ([[-2]], [3], [5], [[7]], F(11), F(13)),
        ([[-2, 1], [1, -3]], [2, -1], [3, 4],
         [[5, 2], [2, -1]], F(7), F(-11)),
        ([[-4, 1], [1, -2]], [-3, 2], [2, -5],
         [[-2, 3], [3, 4]], F(-9), F(17)),
    ]
    for index, (matrix, bvec, eta, dmat, c, e) in enumerate(fixtures):
        v = matvec(inverse(matrix), bvec)
        gamma = c/12-dot(bvec, v)/4
        correction = -dot(eta, v)/12+dot(v, matvec(dmat, v))/8
        q5 = e/120+correction
        for wscale in [F(-2), F(0), F(3, 5)]:
            # An arbitrary cubic displacement also tests the cancellation
            # needed to pass from the parabola to the actual ridge's Q1.
            y = [[F(0), F(0), -vi/2, wscale*(i+1)]
                 for i, vi in enumerate(v)]
            composed = [F(0)]
            for i in range(len(v)):
                for j in range(len(v)):
                    composed = padd(composed, pscale(pmul(y[i], y[j]),
                                                      F(matrix[i][j], 2)))
                    composed = padd(composed, pscale(pmul([0, 1], pmul(y[i], y[j])),
                                                      F(dmat[i][j], 2)))
                composed = padd(composed, pscale(pmul([0, 0, 1], y[i]), F(bvec[i], 2)))
                composed = padd(composed, pscale(pmul([0, 0, 0, 1], y[i]), F(eta[i], 6)))
            composed = padd(composed, [0, 0, 0, 0, c/24, e/120])
            require(pcoefficient(composed, 4) == gamma/2,
                    "parabola quartic coefficient gamma/2")
            require(pcoefficient(composed, 5) == q5,
                    "parabola quintic equals predecessor Q1")
            cases += 1
        c0 = 3*dot(bvec, v)
        e0 = -120*correction
        require(c0/12-dot(bvec, v)/4 == 0 and e0/120+correction == 0,
                "nonlinear contact coordinates gamma=q5=0")
        for rho, s, z in product([F(1, 3), F(2, 5)],
                                  [F(-5), F(-3)], [F(-2), F(0), F(7, 3)]):
            c_tau = c0+12*rho*rho*s
            e_tau = e0+120*rho*z
            require(c_tau/12-dot(bvec, v)/4 == rho*rho*s and
                    e_tau/120+correction == rho*z,
                    "exact tiny-gap coordinate scaling tau=rho squared")
        reject(e/120+dot(eta, v)/12+dot(v, matvec(dmat, v))/8 == q5,
               "wrong eta sign in Q1 fixture " + str(index))
        reject(e/120-dot(eta, v)/12 == q5,
               "omitted transverse D term in Q1 fixture " + str(index))
    require(12*120 == 1440, "triangular contact-coordinate Jacobian")
    COUNTS["parabola_quartic_quintic_cases"] = cases
    COUNTS["tiny_gap_coordinate_scaling_cases"] = len(fixtures)*2*2*3


def sextic_controls():
    cases = 0
    # In the scaled ridge, x^4 multiplies p(x)=s/2+z*x-a*x^2.
    # Its exact vertex, not a finite grid, decides the sign on the entire line.
    for s, a, boundary in [(F(-4), F(1, 2), F(2)),
                            (F(-9, 2), F(1), F(3)),
                            (F(-3), F(3, 2), F(3))]:
        require(boundary*boundary == -2*a*s, "exact sextic discriminant threshold")
        for z in [boundary/2, -boundary/2, boundary, -boundary,
                  3*boundary/2, -3*boundary/2]:
            poly = [s/2, z, -a]
            vertex = z/(2*a)
            maximum = peval(poly, vertex)
            require(maximum == s/2+z*z/(4*a), "quadratic vertex value")
            require((maximum <= 0) == (z*z <= -2*a*s),
                    "sextic nonpositivity iff discriminant nonpositive")
            cases += 1
        reject(boundary*boundary <= -a*s,
               "missing factor 2 in sextic cutoff, a=" + str(a))
        if a != 1:
            reject(-2*s == -2*a*s,
                   "omitted actual sixth coefficient in cutoff, a=" + str(a))
    # A small fixed scaled interval can pass while the true quadratic fails.
    poly = [F(-2), F(4), F(-1)]
    local_right = F(1, 4)
    require(peval(poly, local_right) < 0 and
            peval(pderivative(poly), -local_right) > 0 and
            peval(pderivative(poly), local_right) > 0,
            "wrong local cutoff fixture is negative on its whole interval")
    require(peval(poly, F(2)) > 0, "wrong local cutoff misses positive vertex")
    reject(peval(poly, F(2)) <= 0,
           "local scaled interval substituted for global quadratic criterion")
    reject(F(4)**2 <= -2*F(1)*F(-4),
           "typed quartic window alone substituted for sextic criterion")
    # Degenerate boundary cases are explicit; an upward quadratic never passes.
    require(peval([F(-2), F(0)], F(5)) < 0,
            "q6=0,z=0 is a quadratic boundary case")
    reject(peval([F(-2), F(1)], F(3)) <= 0, "q6=0 with nonzero fifth coefficient")
    reject(peval([F(-2), F(0), F(1)], F(2)) <= 0, "positive sixth coefficient")
    COUNTS["sextic_discriminant_cases"] = cases


class Qsqrt3:
    """An exact element a+b*sqrt(3), stored as two rational coordinates."""

    def __init__(self, rational=0, radical=0):
        self.a, self.b = F(rational), F(radical)

    @staticmethod
    def lift(value):
        return value if isinstance(value, Qsqrt3) else Qsqrt3(value)

    def __add__(self, other):
        other = self.lift(other)
        return Qsqrt3(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return Qsqrt3(-self.a, -self.b)

    def __sub__(self, other):
        return self+-self.lift(other)

    def __mul__(self, other):
        other = self.lift(other)
        return Qsqrt3(self.a*other.a+3*self.b*other.b,
                      self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        denominator = other.a*other.a-3*other.b*other.b
        require(denominator != 0, "nonzero Q(sqrt3) denominator")
        return self*Qsqrt3(other.a/denominator, -other.b/denominator)

    def __eq__(self, other):
        other = self.lift(other)
        return self.a == other.a and self.b == other.b

    def coordinates(self):
        return {"rational": str(self.a), "sqrt3": str(self.b)}


def integral_controls():
    radical = Qsqrt3(0, 1)
    require(radical*radical == 3, "Q(sqrt3) defining relation")
    # t=2*x^2 converts 2*(36-t^2)*sqrt(2t) dt to
    # (576*x^2-64*x^6) dx, with bounds 1 and sqrt(3).
    integrand = [F(0), F(0), F(576), F(0), F(0), F(0), F(-64)]
    antiderivative = [F(0)] + [value/F(i+1) for i, value in enumerate(integrand)]
    require(pderivative(antiderivative) == integrand,
            "exact polynomial antiderivative after t=2*x squared")

    def field_eval(poly, x):
        value = Qsqrt3()
        for coefficient in reversed(poly):
            value = value*x+coefficient
        return value

    integral = field_eval(antiderivative, radical)-field_eval(antiderivative, Qsqrt3(1))
    expected = Qsqrt3(F(-1280, 7), F(2304, 7))
    require(integral == expected, "I6=256*(9sqrt3-5)/7")
    # An independent endpoint form of the t-antiderivative checks the substitution.
    t_form = 2*(2*radical*(24*6-F(2, 7)*6**3)-
                Qsqrt3(2)*(24*2-F(2, 7)*2**3))
    require(t_form == integral, "independent radical endpoint antiderivative")
    weight_poly = [F(36), F(0), F(-1)]
    weight_antiderivative = [F(0)] + [value/F(i+1)
                                             for i, value in enumerate(weight_poly)]
    denominator = peval(weight_antiderivative, F(6))-peval(weight_antiderivative, F(-6))
    require(denominator == 288, "typed scalar normalizer integral 288")
    ratio = integral/denominator
    require(ratio == Qsqrt3(F(-40, 63), F(8, 7)),
            "leading ratio 8*(9sqrt3-5)/63")
    require(9*9*3 > 5*5, "positive exact radical prefactor")
    reject(integral/2 == expected, "omitted z-window factor 2 in integral")
    reject(field_eval(antiderivative, radical) == integral,
           "wrong lower integration endpoint t=0 instead of t=2")
    reject(integral/432 == ratio, "normalizer 432 instead of 288")
    COUNTS["radical_integral_and_normalizer_identities"] = 6
    return {"I6": integral.coordinates(), "typed_denominator": str(denominator),
            "leading_ratio": ratio.coordinates()}


def source_controls():
    manifest = HERE / "SOURCES.json"
    sources = json.loads(manifest.read_text())["sources"]
    require(len(sources) == 19, "exactly nineteen source identity entries")
    require(len({item["id"] for item in sources}) == 19, "distinct source identifiers")
    require(len({item["path"] for item in sources}) == 19, "distinct source paths")
    checked = []
    for source in sources:
        path = (ROOT / source["path"]).resolve()
        require(path.is_relative_to(ROOT), "source path stays inside repository")
        raw = path.read_bytes()
        prefix = source["id"] + ": "
        require(len(raw) == source["bytes"], prefix+"source byte count")
        require(hashlib.sha256(raw).hexdigest() == source["sha256"],
                prefix+"source SHA256")
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
        require(blob == source["git_blob"], prefix+"Git blob identity")
        checked.append(source["id"])
    COUNTS["source_entries_checked_bytes_sha256_git_blob"] = len(checked)
    return checked


def main():
    hermite_controls()
    fourier_controls()
    recovery_and_scaling_controls()
    quintic_controls()
    sextic_controls()
    constants = integral_controls()
    sources = source_controls()
    hashes = {"checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "sources_sha256": hashlib.sha256((HERE/"SOURCES.json").read_bytes()).hexdigest(),
              "sharp_action_sha256": hashlib.sha256((HERE/"SHARP_ACTION.md").read_bytes()).hexdigest()}
    tiny_gap = HERE / "TINY_GAP.md"
    if tiny_gap.exists():
        hashes["tiny_gap_sha256"] = hashlib.sha256(tiny_gap.read_bytes()).hexdigest()
    print(json.dumps({
        "status": "PASS",
        "scope": "Bounded finite exact author controls only. These identities and "
                 "source hashes do not certify a continuum theorem, Gaussian "
                 "probabilities, an LDP, scientific review or acceptance.",
        "arithmetic": "Python standard library; integer/Fraction and Q(sqrt3); no floating point",
        "counts": COUNTS,
        "rejected_invalid_fixtures": REJECTED,
        "radical_constants": constants,
        "source_checks": sources,
        **hashes,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
