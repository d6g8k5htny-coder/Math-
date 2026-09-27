"""Exact checks for the PR36 contact-kernel tail additions.

Subject: reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md
at ef312fed26cd406120c5b6c0a0d442f13538b408,
blob 26890787afe6b8562e275603337d7e6deda1c3e9.

Python standard library only. This file does not import the author
package. A passing run checks the rational identities behind Q1-Q4.
It does not prove finite-r uniformity, a persistence intensity, or a
global lifetime law.
"""
from fractions import Fraction as Q
from math import erf, exp, factorial, pi, sqrt
import unittest


def binom(n, k):
    return Q(factorial(n), factorial(k) * factorial(n - k))


# --- bivariate polynomials in (w, theta) ---

WPoly = dict[tuple[int, int], Q]


def w_add(*parts: WPoly) -> WPoly:
    out: WPoly = {}
    for part in parts:
        for key, coeff in part.items():
            out[key] = out.get(key, Q(0)) + coeff
    return {key: coeff for key, coeff in out.items() if coeff}


def w_scale(poly: WPoly, coeff: Q) -> WPoly:
    coeff = Q(coeff)
    return {key: coeff * value for key, value in poly.items() if coeff * value}


def w_mul(left: WPoly, right: WPoly) -> WPoly:
    out: WPoly = {}
    for (i, j), a in left.items():
        for (k, l), b in right.items():
            key = (i + k, j + l)
            out[key] = out.get(key, Q(0)) + a * b
    return {key: coeff for key, coeff in out.items() if coeff}


def w_pow(poly: WPoly, n: int) -> WPoly:
    out: WPoly = {(0, 0): Q(1)}
    for _ in range(n):
        out = w_mul(out, poly)
    return out


def w_var(index: int) -> WPoly:
    return {(1, 0): Q(1)} if index == 0 else {(0, 1): Q(1)}


def w_const(value) -> WPoly:
    value = Q(value)
    return {(0, 0): value} if value else {}


def type_polynomial() -> WPoly:
    """P = P_M P_S P_X from (1.2), built from the displayed factors."""
    w, theta = w_var(0), w_var(1)
    p_m = w_add(w_scale(theta, 4), w_scale(w_pow(w_add(w, w_const(1)), 2), -1))
    p_s = w_add(w_pow(w_add(w, w_const(-1)), 2), w_const(-4), w_scale(theta, 4))
    p_x = w_add(
        w_pow(w_add(w, w_const(1), w_scale(theta, -2)), 2),
        w_scale(w_mul(theta, w_add(w_const(1), w_scale(theta, -1))), 4),
    )
    return w_mul(w_mul(p_m, p_s), p_x)


def _integrate_w(poly: WPoly, lo: int, hi: int) -> Q:
    total = Q(0)
    for (i, j), coeff in poly.items():
        if j:
            raise AssertionError("theta should already be gone")
        total += coeff * Q(hi ** (i + 1) - lo ** (i + 1), i + 1)
    return total


def integrate_reversed(poly: WPoly) -> tuple[Q, Q]:
    """Theta-first integral on the reversed maximum/saddle region."""
    w = w_var(0)
    lower_left = w_scale(w_pow(w_add(w, w_const(1)), 2), Q(1, 4))
    lower_right = w_add(w_const(1), w_scale(w_pow(w_add(w, w_const(-1)), 2), -Q(1, 4)))
    pieces = []
    for lower, lo, hi in ((lower_left, -3, -1), (lower_right, -1, 1)):
        integrated: WPoly = {}
        for (i, j), coeff in poly.items():
            height = w_mul(
                {(i, 0): coeff / Q(j + 1)},
                w_add(w_const(1), w_scale(w_pow(lower, j + 1), -1)),
            )
            integrated = w_add(integrated, height)
        pieces.append(_integrate_w(integrated, lo, hi))
    return pieces[0], pieces[1]


def gamma_half(m: int) -> tuple[Q, int]:
    """Gamma(m/2) for positive integer m, as coeff * pi**(power/2), power in {0,1}."""
    if m % 2 == 0:
        return Q(factorial(m // 2 - 1)), 0
    n = (m - 1) // 2
    return Q(factorial(2 * n), (4**n) * factorial(n)), 1


def beta_sqrt(a: int, b: int) -> tuple[Q, Q]:
    """Integral_0^1 theta**(a/2) (1-theta)**(b/2) d theta, as rational + rational*pi."""
    cx, px = gamma_half(a + 2)
    cy, py = gamma_half(b + 2)
    cz, pz = gamma_half(a + b + 4)
    coeff = cx * cy / cz
    power = px + py - pz
    if power == 0:
        return coeff, Q(0)
    if power == 2:
        return Q(0), coeff
    raise AssertionError("unexpected pi power %s" % power)


def integrate_original(poly: WPoly) -> tuple[Q, Q]:
    """w-first integral on I_theta, then exact beta values in sqrt(theta), sqrt(1-theta)."""
    rational, pi_part = Q(0), Q(0)
    for (i, j), coeff in poly.items():
        degree = i + 1
        bracket: dict[tuple[int, int], Q] = {}
        for k in range(degree + 1):
            bracket[(0, k)] = bracket.get((0, k), Q(0)) + binom(degree, k) * Q((-1) ** k * 2**k)
            bracket[(k, 0)] = bracket.get((k, 0), Q(0)) - binom(degree, k) * Q((-1) ** degree * 2**k)
        for (s_pow, t_pow), term in bracket.items():
            piece_r, piece_pi = beta_sqrt(s_pow + 2 * j, t_pow)
            weight = coeff * term / Q(degree)
            rational += weight * piece_r
            pi_part += weight * piece_pi
    return rational, pi_part


# --- Laurent polynomials in (u, w, theta, v, k) ---

LKey = tuple[int, int, int, int, int]
LPoly = dict[LKey, Q]


def l_term(coeff, u=0, w=0, t=0, v=0, k=0) -> LPoly:
    coeff = Q(coeff)
    if not coeff:
        return {}
    return {(u, w, t, v, k): coeff}


def l_add(*parts: LPoly) -> LPoly:
    out: LPoly = {}
    for part in parts:
        for key, coeff in part.items():
            out[key] = out.get(key, Q(0)) + coeff
    return {key: coeff for key, coeff in out.items() if coeff}


def l_scale(poly: LPoly, coeff) -> LPoly:
    coeff = Q(coeff)
    return {key: coeff * value for key, value in poly.items() if coeff * value}


def l_mul(left: LPoly, right: LPoly) -> LPoly:
    out: LPoly = {}
    for k1, a in left.items():
        for k2, b in right.items():
            key = tuple(x + y for x, y in zip(k1, k2))
            out[key] = out.get(key, Q(0)) + a * b
    return {key: coeff for key, coeff in out.items() if coeff}


def l_pow(poly: LPoly, n: int) -> LPoly:
    if n < 0:
        raise ValueError("negative powers are entered as monomials")
    out = l_term(1)
    for _ in range(n):
        out = l_mul(out, poly)
    return out


def contact_symbols():
    u, w, t = l_term(1, u=1), l_term(1, w=1), l_term(1, t=1)
    v, k = l_term(1, v=1), l_term(1, k=1)
    q = l_mul(l_term(6, k=1, v=-1), l_add(w, l_scale(u, -2)))
    c = l_mul(
        l_term(12, k=1, v=-2),
        l_add(l_pow(u, 2), l_scale(l_mul(u, w), -1), l_term(Q(1, 4))),
    )
    r_poly = l_add(
        l_scale(l_pow(u, 3), -2),
        l_scale(u, -Q(3, 2)),
        l_term(-1),
        l_scale(t, 2),
        l_mul(l_term(3, w=1), l_add(l_pow(u, 2), l_term(-Q(1, 4)))),
    )
    d = l_mul(l_term(6, k=1, v=-3), r_poly)
    a_num = l_add(
        l_mul(l_term(12, k=1), u),
        l_term(6, k=1),
        l_mul(q, v),
        l_mul(l_term(-12, k=1), t),
    )
    a_hess = l_mul(a_num, l_term(Q(1, 2), v=-2))
    return u, w, t, v, k, q, c, d, r_poly, a_hess


def det2(a11, a12, a22):
    return l_add(l_mul(a11, a22), l_scale(l_pow(a12, 2), -1))


class KernelIdentities(unittest.TestCase):
    def test_region_area_is_two(self):
        left, right = integrate_reversed(w_const(1))
        self.assertEqual(left, Q(4, 3))
        self.assertEqual(right, Q(2, 3))
        self.assertEqual(left + right, 2)
        rational, pi_part = integrate_original(w_const(1))
        self.assertEqual(pi_part, 0)
        self.assertEqual(rational, 2)

    def test_beta_values(self):
        self.assertEqual(beta_sqrt(0, 0), (Q(1), Q(0)))
        self.assertEqual(beta_sqrt(1, 0), (Q(2, 3), Q(0)))
        self.assertEqual(beta_sqrt(1, 1), (Q(0), Q(1, 8)))

    def test_type_mass(self):
        poly = type_polynomial()
        degrees = [i for (i, _j) in poly if poly[(i, _j)]]
        self.assertEqual(max(degrees), 6)
        self.assertEqual(sum(coeff for (i, _j), coeff in poly.items() if i == 6), -1)
        left, right = integrate_reversed(poly)
        self.assertEqual(left, Q(77248, 945))
        self.assertEqual(right, Q(704, 135))
        total = left + right
        self.assertEqual(total, Q(27392, 315))
        rational, pi_part = integrate_original(poly)
        self.assertEqual(pi_part, 0)
        self.assertEqual(rational, Q(27392, 315))

    def test_small_gap_multiplier(self):
        # 24 * 6 * 9**3 = 104976, and 104976/36 = 2916.
        self.assertEqual(24 * 6 * 9**3, 104976)
        self.assertEqual(Q(104976, 36), 2916)
        mass = Q(27392, 315)
        self.assertEqual(2916 * mass, Q(8875008, 35))

    def test_rewritten_numerator_and_signs(self):
        u, w, t, _v, _k, _q, _c, _d, r_poly, _a = contact_symbols()
        rewritten = l_add(
            l_scale(l_pow(l_add(u, l_term(-Q(1, 2))), 3), -2),
            l_mul(l_term(3), l_mul(l_add(l_pow(u, 2), l_term(-Q(1, 4))), l_add(w, l_term(-1)))),
            l_scale(l_add(l_term(1), l_scale(t, -1)), -2),
        )
        self.assertEqual(r_poly, rewritten)

    def test_hessian_determinants_match_type_factors(self):
        u, w, t, v, k, q, c, d, _r, a_hess = contact_symbols()
        # A = 3k(w+1-2 theta)/v**2
        simplified = l_mul(l_term(3, k=1, v=-2), l_add(w, l_term(1), l_scale(t, -2)))
        self.assertEqual(a_hess, simplified)
        b_m = det2(l_term(-6, k=1), l_scale(q, Q(1, 2)), l_add(a_hess, l_scale(c, -Q(1, 2))))
        b_s = det2(l_term(6, k=1), l_scale(q, Q(1, 2)), l_add(a_hess, l_scale(c, Q(1, 2))))
        b_x = det2(
            l_add(l_mul(l_term(12, k=1), u), l_mul(q, v)),
            l_add(l_mul(q, u), l_mul(c, v)),
            l_add(a_hess, l_mul(c, u), l_mul(d, v)),
        )
        nine = l_term(9, k=2)
        p_m = l_add(l_scale(t, 4), l_scale(l_pow(l_add(w, l_term(1)), 2), -1))
        p_s = l_add(l_pow(l_add(w, l_term(-1)), 2), l_term(-4), l_scale(t, 4))
        p_x = l_add(
            l_pow(l_add(w, l_term(1), l_scale(t, -2)), 2),
            l_mul(l_term(4), l_mul(t, l_add(l_term(1), l_scale(t, -1)))),
        )
        # Clear v**2: det = ±(9k^2/v^2) P becomes v^2 det = ±9k^2 P.
        self.assertEqual(l_mul(b_m, l_pow(v, 2)), l_mul(nine, p_m))
        self.assertEqual(l_mul(b_s, l_pow(v, 2)), l_mul(l_scale(nine, -1), p_s))
        self.assertEqual(l_mul(b_x, l_pow(v, 2)), l_mul(l_scale(nine, -1), p_x))
        signed = l_mul(l_mul(b_m, b_s), b_x)
        absolute = l_mul(l_pow(l_mul(nine, l_term(1, v=-2)), 3), l_mul(l_mul(p_m, p_s), p_x))
        self.assertEqual(l_mul(signed, l_pow(v, 6)), l_mul(absolute, l_pow(v, 6)))

    def test_known_cubic_point(self):
        # PR25 sample inside the type interval: u=2,v=1,k=1,theta=1/2,w=-1.
        u, v, k, w, theta = Q(2), Q(1), Q(1), Q(-1), Q(1, 2)
        q = 6 * k * (w - 2 * u) / v
        c = 12 * k * (u * u - u * w + Q(1, 4)) / v**2
        r_num = -2 * u**3 - Q(3, 2) * u - 1 + 2 * theta + 3 * w * (u * u - Q(1, 4))
        d = 6 * k * r_num / v**3
        a_hess = 3 * k * (w + 1 - 2 * theta) / v**2
        self.assertEqual((q, c, d, a_hess), (Q(-30), Q(75), Q(-363, 2), Q(-3)))
        det_m = (-6 * k) * (a_hess - c / 2) - (q / 2) ** 2
        det_s = (6 * k) * (a_hess + c / 2) - (q / 2) ** 2
        h11 = 12 * k * u + q * v
        h12 = q * u + c * v
        h22 = a_hess + c * u + d * v
        det_x = h11 * h22 - h12**2
        self.assertEqual((det_m, det_s, det_x), (Q(18), Q(-18), Q(-18)))

    def test_left_cancellation_counterexample(self):
        u, theta, w = Q(-2), Q(1, 2), Q(-76, 45)
        # Strictly inside I_{1/2} = (-1-sqrt(2), 1-sqrt(2)).
        self.assertLess((Q(31, 45)) ** 2, 2)  # 76/45 < 1+sqrt(2)
        self.assertGreater((Q(121, 45)) ** 2, 2)  # 121/45 > sqrt(2)
        r_num = -2 * u**3 - Q(3, 2) * u - 1 + 2 * theta + 3 * w * (u * u - Q(1, 4))
        self.assertEqual(r_num, 0)
        p_m = 4 * theta - (w + 1) ** 2
        p_s = (w - 1) ** 2 - 4 * (1 - theta)
        p_x = (w + 1 - 2 * theta) ** 2 + 4 * theta * (1 - theta)
        self.assertGreater(p_m, 0)
        self.assertGreater(p_s, 0)
        self.assertGreater(p_x, 0)
        self.assertEqual(p_m * p_s * p_x, Q(255214387799, 8303765625))

    def test_gradient_identity(self):
        u, w, t, v, k, q, c, _d, _r, _a = contact_symbols()
        left = l_add(l_mul(l_mul(u, v), q), l_mul(l_scale(l_pow(v, 2), Q(1, 2)), c))
        right = l_mul(l_term(-6, k=1), l_add(l_pow(u, 2), l_term(-Q(1, 4))))
        self.assertEqual(left, right)

    def test_bargmann_fock_blocks(self):
        def deriv(n):
            if n % 2:
                return Q(0)
            half = n // 2
            return Q((-1) ** half * factorial(n), (2**half) * factorial(half))

        def cov(alpha, beta):
            sign = -1 if (beta[0] + beta[1]) % 2 else 1
            return sign * deriv(alpha[0] + beta[0]) * deriv(alpha[1] + beta[1])

        even = [(0, 0), (2, 0), (1, 1)]  # f, fxx, fxz
        odd = [(1, 0), (3, 0), (0, 1)]  # fx, fxxx, fz
        a = (0, 2)
        jets = [(2, 1), (1, 2), (0, 3)]  # q, c, d
        for left in even + [a]:
            for right in odd + jets:
                self.assertEqual(cov(left, right), 0)

        def inverse(rows):
            size = len(rows)
            aug = [list(map(Q, row)) + [Q(int(i == j)) for j in range(size)] for i, row in enumerate(rows)]
            for col in range(size):
                pivot = next(i for i in range(col, size) if aug[i][col])
                aug[col], aug[pivot] = aug[pivot], aug[col]
                scale = aug[col][col]
                aug[col] = [entry / scale for entry in aug[col]]
                for row in range(size):
                    if row != col and aug[row][col]:
                        factor = aug[row][col]
                        aug[row] = [entry - factor * other for entry, other in zip(aug[row], aug[col])]
            return [row[size:] for row in aug]

        def conditional(target, observed):
            sigma_oo = [[cov(x, y) for y in observed] for x in observed]
            sigma_to = [cov(target, y) for y in observed]
            sigma_tt = cov(target, target)
            solved = inverse(sigma_oo)
            mean_on_obs = [
                sum(sigma_to[k] * solved[k][j] for k in range(len(observed))) for j in range(len(observed))
            ]
            variance = sigma_tt - sum(sigma_to[i] * mean_on_obs[i] for i in range(len(observed)))
            return mean_on_obs, variance

        mean_a, var_a = conditional(a, even)
        self.assertEqual(mean_a, [Q(-1), Q(0), Q(0)])
        self.assertEqual(var_a, 2)
        conditional_odd = [conditional(jet, odd) for jet in jets]
        for mean, _var in conditional_odd:
            # Observation (fx, fxxx, fz) = (0, 12k, 0); only the fxxx column can shift the mean.
            self.assertEqual(mean[1], 0)
        variances = [var for _mean, var in conditional_odd]
        self.assertEqual(variances, [2, 2, 6])
        # Off-diagonal conditional covariances.
        sigma_oo = [[cov(x, y) for y in odd] for x in odd]
        solved = inverse(sigma_oo)
        cross = [[cov(jet, y) for y in odd] for jet in jets]
        gram = [[cov(left, right) for right in jets] for left in jets]
        schur = []
        for i in range(3):
            row = []
            for j in range(3):
                correction = 0
                for p in range(3):
                    for q in range(3):
                        correction += cross[i][p] * solved[p][q] * cross[j][q]
                row.append(gram[i][j] - correction)
            schur.append(row)
        self.assertEqual(schur, [[2, 0, 0], [0, 2, 0], [0, 0, 6]])

    def test_bargmann_fock_coefficient(self):
        # p_a(0) C_odd = exp(-b^2/4)/(16 sqrt(3) pi^2) when a~N(-b,2), Omega=diag(2,2,6).
        # At b=0, m2a=1, so C_L = 184896 sqrt(3)/(35 pi^2).
        self.assertEqual(2 * 2 * 6, 24)
        self.assertEqual(8875008 // 16, 554688)
        self.assertEqual(554688 // 3, 184896)
        value = 184896 * sqrt(3) / (35 * pi**2)
        self.assertAlmostEqual(value, 927.086705814, places=9)

    def test_centered_moment_recurrence(self):
        # Integration by parts: the boundary term is exactly (5.1), checked on a moderate interval.
        a, lo, hi = Q(1, 2), Q(-3, 5), Q(4, 5)
        # Compare the recurrence's algebraic step at n=4 against an independent antiderivative sample
        # by evaluating both float forms. The identity itself is the assertion on the coefficients.
        af, lf, hf = float(a), float(lo), float(hi)
        el, eh = exp(-af * lf * lf), exp(-af * hf * hf)
        m0 = sqrt(pi) / (2 * sqrt(af)) * (erf(sqrt(af) * hf) - erf(sqrt(af) * lf))
        m1 = (el - eh) / (2 * af)
        m2 = (lf * el - hf * eh) / (2 * af) + m0 / (2 * af)
        m3 = (lf**2 * el - hf**2 * eh) / (2 * af) + 2 * m1 / (2 * af)
        m4 = (lf**3 * el - hf**3 * eh) / (2 * af) + 3 * m2 / (2 * af)
        # Independent Simpson check of integral x^4 exp(-a x^2), not an enclosure.
        steps = 4000
        width = (hf - lf) / steps
        acc = 0.0
        for i in range(steps):
            for weight, point in ((1, lf + i * width), (4, lf + (i + 0.5) * width), (1, lf + (i + 1) * width)):
                acc += weight * point**4 * exp(-af * point * point)
        simpson = acc * width / 6
        self.assertAlmostEqual(m4, simpson, places=10)
        self.assertGreater(m0, 0.0)
        self.assertNotEqual(m3, 0.0)


if __name__ == "__main__":
    unittest.main()
