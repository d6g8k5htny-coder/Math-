"""Certified d = 2 coefficient c_{2,L} of (15.2) for the SIDE24 family at small periods L.

Main issue 252 item 3 and main issue 259 remaining work, item 4: interval quadrature with full angular
covariance and explicit image tails.  Standard library only.  Every reported bound is an outward
rational enclosure built with the interval class, pi, log, exp, root and Gamma(7/6) enclosures of
coefficients/side24_v1/coefficient.py, imported only after its git blob matches the pin below.

Field.  K_L(z) = q_L(z_1) q_L(z_2), q_L = theta_L / theta_L(0), theta_L(t) = sum_n exp(-(t + L n)^2 / 2).
The spectral law has independent coordinates; one coordinate has raw moments m2, m4, m6 and cumulants
k2 = m2, k4 = m4 - 3 m2^2, k6 = m6 - 15 m4 m2 + 30 m2^3.

Reduction.  For u = (cos t, sin t) put q = cos^2 t sin^2 t = (1 - cos 4t) / 8.  With the conventions of
reviews/iba1_periodic_jet_claude_20261005 (V = (f_uu, f_uw), A = f_ww):
    tau^2  = 6 k2^3 + 9 k2 k4 (1 - 2q) + (k6 - k4^2/k2)(1 - 3q)                  (linear in q)
    det V  = k2^2 (3 k2^2 + k4) + k4 (4 k2^2 + k4) q                              (linear in q)
    S      = alpha - (gamma^3 + (2 gamma + alpha) k4^2 q (1 - 4q)) / det V,     alpha = 3k2^2 + k4 - 2 k4 q,
                                                                               gamma = k2^2 + 2 k4 q
    Phi(q) = (tau^2)^(2/3) S / (8 pi^2 k2 sqrt(det V))
and c_{2,L} = Gamma(7/6) / (24^(1/3) sqrt(pi)) * int_0^{2 pi} Phi((1 - cos phi) / 8) d phi.

Quadrature.  Trapezoid rule with N nodes in phi.  If Phi is analytic on the image of the strip
|Im phi| <= a, i.e. on the filled ellipse centred 1/8 with semi-axes cosh(a)/8 and sinh(a)/8, and
|Phi| <= M there, then |error| <= 4 pi M / (e^{aN} - 1) (Trefethen and Weideman, SIAM Review 56 (2014),
Theorem 3.2).  Analyticity holds when Re tau^2 > 0 and Re det V > 0 on the ellipse; both are affine in
Re q, so the two extreme values of Re q decide it.  M is bounded on the boundary ellipse by complex
interval boxes (maximum modulus).

Usage:  python3 -B -S certified_d2.py [--mutant M1|M2|M3|M4]
A normal run prints RESULTS.json and exits 0.  Each mutant must make a check fail (exit 1):
  M1  strip half-width quadrupled beyond the verified one (the strip check fails, first at L = 4);
  M2  transverse block not conditioned on V (S = alpha);
  M3  wrong det V slope (4 k2^2 k4 + 2 k4^2);
  M4  quadrature error term dropped.
An unknown mutant label exits 2.
"""
import hashlib
import importlib.util
import json
import os
import sys
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SIDE24 = os.path.join(ROOT, 'coefficients', 'side24_v1', 'coefficient.py')
SIDE24_BLOB = 'c2d3ff339f2b9953ec08e676240cdc5edcb17a3e'
MUTANT = None


def git_blob(path):
    data = open(path, 'rb').read()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def load_side24():
    if git_blob(SIDE24) != SIDE24_BLOB:
        raise SystemExit('side24_v1/coefficient.py does not match the pinned blob')
    spec = importlib.util.spec_from_file_location('side24_coefficient', SIDE24)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


S24 = load_side24()
I, root, PI = S24.I, S24.root, S24.pi_interval()
exp_interval, exp_point = S24.exp_interval, S24.exp_point


def hull(a, b):
    return I(min(a.lo, b.lo), max(a.hi, b.hi))


def sym(t):
    return I(-t, t)


# ---------------------------------------------------------------- sin and cos on [0, pi + 1/10]

def _series(x, start, terms=60):
    """sum_k (-1)^k x^(2k+start) / (2k+start)! with the alternating-series remainder (|x| <= 4)."""
    if not (x.lo >= 0 and x.hi <= 4):
        raise ValueError('series argument out of range')
    x2 = x * x
    term = I(1) if start == 0 else x
    total = term
    for k in range(1, terms):
        term = -(term * x2) / ((2 * k + start - 1) * (2 * k + start))
        total = total + term
    rem = Q(4) ** (2 * terms + start) / Q(_fact(2 * terms + start))
    return total + sym(rem)


def _fact(n):
    out = 1
    for j in range(2, n + 1):
        out *= j
    return out


def sin_point(x):
    return _series(x, 1)


def cos_point(x):
    return _series(x, 0)


# ---------------------------------------------------------------- spectral moments, two routes

def hermite_even(j, y):
    if j == 0:
        return I(1)
    y2 = y * y
    if j == 2:
        return y2 - 1
    if j == 4:
        return y2 * y2 - 6 * y2 + 3
    if j == 6:
        return y2 * y2 * y2 - 15 * y2 * y2 + 45 * y2 - 15
    raise ValueError(j)


def gaussian_tail(x, step, j):
    """Bound on sum_{n >= 0} (x + n step)^j exp(-(x + n step)^2 / 2), for x >= 10 and x * step >= 2."""
    if not (x.lo >= 10 and (x * step).lo >= 2):
        raise ArithmeticError('tail hypotheses fail')
    # Ratio of consecutive terms: (1 + step/x)^j exp(-x step - step^2/2) <= (6/5)^6 e^(-2) < 1/2 once
    # step / x <= 1/5; for larger step / x use the cruder (1 + step/x)^j <= exp(j step / x) <= exp(j step / 10).
    ratio = (1 + step / x) ** j * exp_interval(-(x * step) - step * step / 2)
    if not ratio.hi < Q(1, 2):
        raise ArithmeticError('tail ratio is not below 1/2')
    first = x ** j * exp_interval(-(x * x) / 2)
    return 2 * first.hi


def moments_image(L):
    """Raw moments (m2, m4, m6) from the image sums theta_L^(j)(0) with an explicit tail."""
    n = 1
    while (L * (n + 1)).lo < 22:
        n += 1
    x = L * (n + 1)
    th = {}
    for j in (0, 2, 4, 6):
        s = hermite_even(j, I(0))
        for m in range(1, n + 1):
            y = L * m
            s = s + 2 * hermite_even(j, y) * exp_interval(-(y * y) / 2)
        # |He_j(y)| <= y^j for y >= 10, both tails.
        s = s + sym(2 * gaussian_tail(x, L, 6))
        th[j] = s
    q2, q4, q6 = th[2] / th[0], th[4] / th[0], th[6] / th[0]
    return -q2, q4, -q6


def moments_dual(L):
    """The same moments from the Poisson-dual spectral sum: P(X = 2 pi k / L) is proportional to
    exp(-(2 pi k / L)^2 / 2).  An independent route to the inputs."""
    h = 2 * PI / L
    n = 1
    while (h * (n + 1)).lo < 22 or (h * (n + 1) * h).lo < 2:
        n += 1
    x = h * (n + 1)
    tail = 2 * gaussian_tail(x, h, 6)
    w = {j: I(1) if j == 0 else I(0) for j in (0, 2, 4, 6)}
    for k in range(1, n + 1):
        om = h * k
        e = 2 * exp_interval(-(om * om) / 2)
        om2 = om * om
        w[0] = w[0] + e
        w[2] = w[2] + om2 * e
        w[4] = w[4] + om2 * om2 * e
        w[6] = w[6] + om2 * om2 * om2 * e
    for j in (0, 2, 4, 6):
        w[j] = w[j] + I(0, tail)
    return w[2] / w[0], w[4] / w[0], w[6] / w[0], (h, 2 * exp_interval(-(h * h) / 2) / w[0],
                                                    2 * exp_interval(-(4 * h * h) / 2) / w[0])


def cumulants(m2, m4, m6):
    return m2, m4 - 3 * m2 * m2, m6 - 15 * m4 * m2 + 30 * m2 * m2 * m2


# ---------------------------------------------------------------- the integrand

def coeffs(k):
    """Real coefficients of the affine maps tau^2(q) = t0 - t1 q and det V(q) = d0 + d1 q."""
    k2, k4, k6 = k
    bc = k6 - k4 * k4 / k2
    t0 = 6 * k2 * k2 * k2 + 9 * k2 * k4 + bc
    t1 = 18 * k2 * k4 + 3 * bc
    d0 = k2 * k2 * (3 * k2 * k2 + k4)
    d1 = k4 * (4 * k2 * k2 + k4)
    if MUTANT == 'M3':
        d1 = k4 * (4 * k2 * k2 + 2 * k4)
    return t0, t1, d0, d1


def phi_real(q, k, cf):
    k2, k4, _ = k
    t0, t1, d0, d1 = cf
    tau2 = t0 - t1 * q
    detv = d0 + d1 * q
    alpha = 3 * k2 * k2 + k4 - 2 * k4 * q
    gamma = k2 * k2 + 2 * k4 * q
    S = alpha - (gamma * gamma * gamma + (2 * gamma + alpha) * k4 * k4 * q * (1 - 4 * q)) / detv
    if MUTANT == 'M2':
        S = alpha
    return root(tau2 * tau2, 3) * S / (8 * PI * PI * k2 * root(detv, 2)), (tau2, detv, S)


class C:
    """Rectangular complex interval."""

    def __init__(self, re, im=None):
        self.re = re if isinstance(re, I) else I(re)
        self.im = I(0) if im is None else (im if isinstance(im, I) else I(im))

    def __add__(self, o):
        o = o if isinstance(o, C) else C(o)
        return C(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, C) else C(o)
        return C(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return C(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, C) else C(o)
        return C(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def abs_hi(self):
        return root(I(0, self.abs2().hi), 2).hi

    def abs_lo(self):
        a = self.abs2().lo
        return root(I(a), 2).lo if a > 0 else Q(0)


def modulus_bound(qc, k, cf):
    """Upper bound of |Phi| on the complex box qc (Re tau^2, Re det V > 0 already verified)."""
    k2, k4, _ = k
    t0, t1, d0, d1 = cf
    tau2 = C(t0) - C(t1) * qc
    detv = C(d0) + C(d1) * qc
    alpha = C(3 * k2 * k2 + k4) - C(2 * k4) * qc
    gamma = C(k2 * k2) + C(2 * k4) * qc
    num = gamma * gamma * gamma + (2 * gamma + alpha) * C(k4 * k4) * qc * (1 - 4 * qc)
    dlo = detv.abs_lo()
    if dlo <= 0:
        raise ArithmeticError('det V may vanish on the ellipse')
    s_hi = alpha.abs_hi() + num.abs_hi() / dlo
    if MUTANT == 'M2':
        s_hi = alpha.abs_hi()
    t_hi = root(I(tau2.abs_hi()), 3).hi ** 2
    return t_hi * s_hi / ((8 * PI * PI * k2).lo * root(I(dlo), 2).lo)


def strip_ok(a, cf):
    """Re tau^2 > 0 and Re det V > 0 on the filled ellipse for half-width a."""
    t0, t1, d0, d1 = cf
    ea = exp_point(Q(a))
    ch = (ea + 1 / ea) / 2
    lo_u, hi_u = (1 - ch) / 8, (1 + ch) / 8
    vals = [t0 - t1 * lo_u, t0 - t1 * hi_u, d0 + d1 * lo_u, d0 + d1 * hi_u]
    return min(v.lo for v in vals)


def boundary_bound(a, k, cf, boxes=128):
    ea = exp_point(Q(a))
    ch, sh = (ea + 1 / ea) / 2, (ea - 1 / ea) / 2
    m = Q(0)
    for i in range(boxes):
        x = I((PI * i / boxes).lo, (PI * (i + 1) / boxes).hi)
        xl, xh = I(x.lo), I(x.hi)
        cosx = I(cos_point(xh).lo, cos_point(xl).hi)
        if i == boxes - 1:
            cosx = I(-1, cosx.hi)
        sl, shh = sin_point(xl), sin_point(xh)
        sinx = I(min(sl.lo, shh.lo), max(sl.hi, shh.hi))
        if (PI / 2).hi >= x.lo and (PI / 2).lo <= x.hi:
            sinx = I(sinx.lo, 1)
        qc = C((1 - ch * cosx) / 8, sh * sinx / 8)
        m = max(m, modulus_bound(qc, k, cf))
    return m


def choose_strip(cf):
    a = Q(2)
    while strip_ok(a, cf) <= 0:
        a /= 2
        if a < Q(1, 2 ** 20):
            raise ArithmeticError('no admissible strip')
    return a / 2           # keep a margin below the largest admissible dyadic half-width


def trapezoid(k, cf, N):
    """(2 pi / N) sum_j Phi(q_j) with q_j = sin^2(pi j / N) / 4, by the symmetry q_{N-j} = q_j."""
    total = phi_real(I(0), k, cf)[0] + phi_real(I(Q(1, 4)), k, cf)[0]
    for j in range(1, N // 2):
        s = sin_point(PI * j / N)
        total = total + 2 * phi_real(s * s / 4, k, cf)[0]
    return total * 2 * PI / N


def quadrature(k, tol=Q(1, 10 ** 40), N_override=None):
    cf = coeffs(k)
    a = choose_strip(cf)
    if strip_ok(a, cf) <= 0:
        raise ArithmeticError('strip not verified')
    M = boundary_bound(a, k, cf)
    a_used = 4 * a if MUTANT == 'M1' else a
    if MUTANT == 'M1' and strip_ok(a_used, cf) <= 0:
        raise ArithmeticError('M1: strip not admissible')
    N = 8
    while True:
        err = 4 * PI.hi * M / (exp_point(a_used * N).lo - 1)
        if err < tol:
            break
        N *= 2
    if N_override:
        N = N_override
        err = 4 * PI.hi * M / (exp_point(a_used * N).lo - 1)
    T = trapezoid(k, cf, N)
    E = Q(0) if MUTANT == 'M4' else err
    return T + sym(E), {'a': a_used, 'N': N, 'M': M, 'error_bound': err}


def prefactor():
    return S24.gamma_seven_sixths() / (root(I(24), 3) * root(PI, 2))


def positivity(k, cf, pieces=64):
    """Lower bounds of tau^2, det V and S over every direction (q in [0, 1/4])."""
    t0, t1, d0, d1 = cf
    out = {'tau2': min((t0 - t1 * Q(0)).lo, (t0 - t1 * Q(1, 4)).lo),
           'detV': min((d0 + d1 * Q(0)).lo, (d0 + d1 * Q(1, 4)).lo)}
    smin = None
    stack = [(Q(j, 4 * pieces), Q(j + 1, 4 * pieces)) for j in range(pieces)]
    while stack:
        lo, hi = stack.pop()
        S = phi_real(I(lo, hi), k, cf)[1][2]
        if S.lo <= 0 and hi - lo > Q(1, 2 ** 30):
            mid = (lo + hi) / 2
            stack += [(lo, mid), (mid, hi)]
            continue
        smin = S.lo if smin is None else min(smin, S.lo)
    out['S'] = smin
    return out


# ---------------------------------------------------------------- checks and report

ENCLOSURE = os.path.join(ROOT, 'coefficients', 'side24_v1', 'ENCLOSURE.json')
ENCLOSURE_BLOB = '57af39a05e14ed0ba8ebc00a9b4aca4dffb067c7'
JET_RESULTS = os.path.join(ROOT, 'reviews', 'iba1_periodic_jet_claude_20261005', 'RESULTS.json')
JET_RESULTS_BLOB = 'c1e5849cb198c1dbd965cc04806642800ec5a012'
PERIODS = [('4', I(4)), ('3', I(3)), ('24', I(24)), ('8', I(8)), ('2pi', 2 * PI), ('2', I(2))]


def pinned_json(path, blob):
    if git_blob(path) != blob:
        raise SystemExit('pinned file does not match its blob: ' + path)
    return json.load(open(path))


def dec(x, digits=30):
    return S24.decimals(x, digits)


def sci(q, digits, up):
    """Exact rational q in scientific notation, rounded toward +infinity (up) or -infinity (down)."""
    q = Q(q)
    if q == 0:
        return '0'
    a = abs(q)
    e = 0
    while a >= Q(10) ** (e + 1):
        e += 1
    while a < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = -((-scaled.numerator) // scaled.denominator) if up else scaled.numerator // scaled.denominator
    if abs(m) >= 10 ** digits:            # rounding carried into a new decade
        m = -((-m) // 10) if up else m // 10
        e += 1
    sign = '-' if m < 0 else ''
    t = str(abs(m)).rjust(digits, '0')
    return '%s%s.%se%s%02d' % (sign, t[0], t[1:], '-' if e < 0 else '+', abs(e))


def sci_upper(q, digits=4):
    return sci(q, digits, True)


def sci_lower(q, digits=4):
    return sci(q, digits, False)


def sci_interval(x, digits=8):
    return {'lower': sci_lower(x.lo, digits), 'upper': sci_upper(x.hi, digits)}


def overlap(a, b):
    return a.lo <= b.hi and b.lo <= a.hi


def half_ulp(text):
    """Half a unit in the last printed digit of a value printed like '4.9879432666614182044e-2'."""
    mant, exp = text.split('e')
    digits = len(mant.split('.')[1])
    return Q(5, 10 ** (digits + 1)) * Q(10) ** int(exp)


def main():
    global MUTANT
    if len(sys.argv) == 3 and sys.argv[1] == '--mutant':
        if sys.argv[2] not in ('M1', 'M2', 'M3', 'M4'):
            print('unknown mutant')
            sys.exit(2)
        MUTANT = sys.argv[2]
    elif len(sys.argv) != 1:
        print(__doc__)
        sys.exit(2)

    checks = {}

    def check(name, ok):
        checks[name] = bool(ok)
        if MUTANT and not ok:          # a mutant needs only one failing check
            print(json.dumps({'mutant': MUTANT, 'failed_check': name}))
            sys.exit(1)

    pref = prefactor()
    side24_ref = S24.reference_coefficient(2)
    published = pinned_json(ENCLOSURE, ENCLOSURE_BLOB)['dimensions']['2']
    jet = pinned_json(JET_RESULTS, JET_RESULTS_BLOB)['c_2_diagnostic_small_L']
    out = {'object': 'CL-SIDE24-D2-CERTIFIED-SMALL-L-20261005-v1', 'scientific_effect': 'NONE',
           'method': 'outward rational intervals (side24_v1 library); image and Poisson-dual moment sums '
                     'with explicit tails; trapezoid rule in phi = 4 theta with the analytic-strip bound',
           'cases': {}}

    # C1: the Gaussian reference reproduces side24_v1's closed-form reference coefficient.
    kref = (I(1), I(0), I(0))
    Jref, info = quadrature(kref)
    cref = pref * Jref
    check('C1_reference_equals_side24_closed_form', overlap(cref, side24_ref)
          and cref.hi - cref.lo < Q(1, 10 ** 30))
    out['reference'] = {'c_2': dec(cref), 'side24_v1_closed_form': dec(side24_ref), 'N': info['N']}

    for name, L in PERIODS:
        m_img = moments_image(L)
        m2d, m4d, m6d, (h, p1, p2) = moments_dual(L)
        check('C3_moment_routes_agree_L%s' % name, all(overlap(a, b) for a, b in zip(m_img, (m2d, m4d, m6d))))
        m2, m4, m6 = m_img
        k = cumulants(m2, m4, m6)
        cf = coeffs(k)
        try:
            J, info = quadrature(k)
            ok = strip_ok(info['a'], cf) > 0 and info['error_bound'] < Q(1, 10 ** 40)
        except ArithmeticError:
            ok = False
        check('C4_strip_and_error_bound_L%s' % name, ok)
        if not ok:
            out['cases'][name] = {'error': 'strip or error bound not verified'}
            continue
        c2 = pref * J
        check('C8_width_L%s' % name, c2.hi - c2.lo < c2.lo / 10 ** 25)
        coarse_N = max(8, info['N'] // 4)
        Jc, _ = quadrature(k, N_override=coarse_N)
        check('C9_coarse_rule_consistent_L%s' % name, overlap(Jc, J))
        pos = positivity(k, cf)
        check('C5_positive_every_direction_L%s' % name, all(v > 0 for v in pos.values()))
        # Gram floors (Astra, main#229 6002455230): V2 >= 9 h^4 p1 p2 and Delta >= 36 h^8 p1 p2 / m2.
        V2, Dl = m4 - m2 * m2, m6 - m4 * m4 / m2
        fV, fD = 9 * h ** 4 * p1 * p2, 36 * h ** 8 * p1 * p2 / m2
        check('C7_gram_floors_L%s' % name, V2.lo >= fV.hi and Dl.lo >= fD.hi)
        if name in jet:
            v = jet[name]['N512']
            tol = half_ulp(v) + (c2.hi - c2.lo)
            check('C6_matches_iba1_diagnostic_L%s' % name, abs((c2.lo + c2.hi) / 2 - Q(v)) <= tol)
        if name == '24':
            lo, hi = Q(published['lower']), Q(published['upper'])
            check('C2_L24_inside_side24_interval', lo <= c2.lo and c2.hi <= hi)
        out['cases'][name] = {
            'c_2L': dec(c2), 'ratio_to_reference': dec(c2 / cref, 25),
            'k2': dec(k[0], 25), 'k4_over_k2sq': sci_interval(k[1] / (k[0] * k[0])),
            'k6_over_k2cu': sci_interval(k[2] / (k[0] * k[0] * k[0])),
            'strip_half_width_a': str(info['a']), 'trapezoid_nodes_N': info['N'],
            'modulus_bound_M_upper': sci_upper(info['M']), 'quadrature_error_bound_upper': sci_upper(info['error_bound'], 3),
            'coarse_rule_nodes': coarse_N,
            'min_over_directions_lower': {key: sci_lower(val, 8) for key, val in sorted(pos.items())},
            'gram_floor_margin_lower': {'V2': sci_lower(V2.lo - fV.hi, 6), 'Delta': sci_lower(Dl.lo - fD.hi, 6)}}
    out['checks'] = {key: val for key, val in sorted(checks.items())}
    out['passed'] = all(checks.values())
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if out['passed'] else 1)


if __name__ == '__main__':
    main()
