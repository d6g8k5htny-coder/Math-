"""Floating controls for CL-CU-CUSP-COEFFICIENT-20261001.  These are not part of the certificate.

1. d = 2 by a route that does not use the Mellin identity.  Given (a = -A, gamma, b), Y is Gaussian with
   sigma = a/sqrt6 and mean (a b - gamma^2)/4, so E|Y|^(7/4) = sigma^(7/4) M(mu/sigma), M(t) = E|Z + t|^(7/4) (Kummer
   series).  b ~ N(a/4, 1/2) under the weight, so the b-average is again of M type with variance factor 19/16.  This
   leaves a 2D integral over (a, gamma).
2. d = 3 by the same route: eigenvalues a1 > a2 of -A, the Vandermonde, gamma ~ N(0, 2 I), and the b-average with
   factor 23/20.  This leaves a 4D integral, done here by a floating product Gauss rule.
3. Math-#207's floating values and Monte Carlo runs (head 826b8be, PROOF.md section 8, remark 3) and the d = 1 value of
   Math-#214/#216.

Run: python3 -B controls.py (pure Python, a few minutes)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import gauss as G

P = 1.75
CP = 2 ** (P / 2) * math.gamma((P + 1) / 2) / math.sqrt(math.pi)


def M(t):
    """E|Z + t|^(7/4): Kummer's 1F1((1+p)/2; 1/2; t^2/2) e^(-t^2/2) series for |t| <= 26, else the asymptotic series
    t^p sum_j binom(p, 2j) (2j - 1)!! t^(-2j) through j = 4 (relative error below 1e-14 there)."""
    t = abs(t)
    if t > 26.0:
        c2 = P * (P - 1) / 2
        c4 = P * (P - 1) * (P - 2) * (P - 3) / 8
        c6 = P * (P - 1) * (P - 2) * (P - 3) * (P - 4) * (P - 5) / 48
        c8 = P * (P - 1) * (P - 2) * (P - 3) * (P - 4) * (P - 5) * (P - 6) * (P - 7) / 384
        return t ** P * (1 + c2 / t ** 2 + c4 / t ** 4 + c6 / t ** 6 + c8 / t ** 8)
    z = 0.5 * t * t
    term = 1.0
    s = 1.0
    a, b = (1 + P) / 2, 0.5
    n = 0
    while True:
        term *= (a + n) / (b + n) * z / (n + 1)
        s += term
        n += 1
        if term < 1e-17 * s and n > z:
            break
    return CP * math.exp(-z) * s


def gl(n, a, b):
    xs, ws = G.rule(n)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return [(c + h * 0.5 * (x[0] + x[1]), h * 0.5 * (w[0] + w[1])) for x, w in zip(xs, ws)]


def gamma_nodes(scale, gmax=12.0, n=16):
    """Composite nodes for gamma in [0, gmax], refined near 0 at the scale sqrt(a) of the integrand."""
    edges = [0.0]
    e = 0.25 * scale
    while e < gmax:
        edges.append(e)
        e *= 2.0
    edges.append(gmax)
    out = []
    for a, b in zip(edges, edges[1:]):
        out.extend(gl(n, a, b))
    return out


def phi2(g):
    """density of N(0, 2)"""
    return math.exp(-g * g / 4) / math.sqrt(4 * math.pi)


def control_d2():
    c = math.sqrt(6 / 19)
    tot = 0.0
    for s, ws in gl(80, 0.0, 2.7):
        a = s ** 4
        jac = 4 * s ** 3
        Eg = 0.0
        for g, wg in gamma_nodes(math.sqrt(a)):
            Eg += 2 * wg * phi2(g) * M(c * (a / 4 - g * g / a))
        tot += ws * jac * a * a * math.exp(-3 * a * a / 16) * Eg
    pref = -(192 / 7) * 2 ** 0.25 * 2 * math.pi * (2 * math.pi) ** -3 * 12 ** -0.5 * 0.5 * (19 / 16) ** (7 / 8) * 6 ** (-7 / 8)
    return pref * tot


def control_d3():
    c = math.sqrt(15 / 46)
    tot = 0.0
    s_nodes = gl(24, 0.0, 1.1) + gl(24, 1.1, 1.6) + gl(24, 1.6, 2.6)
    for s, ws in s_nodes:
        a1 = s ** 4
        for w, ww in gl(28, 0.0, 1.0):
            a2 = a1 * w ** 4
            if a2 <= 0.0:
                continue
            jac = 4 * s ** 3 * a1 * 4 * w ** 3
            g1n = gamma_nodes(math.sqrt(a1), n=10)
            g2n = gamma_nodes(math.sqrt(a2), n=10)
            Eg = 0.0
            for g1, w1 in g1n:
                p1 = w1 * 2 * phi2(g1)
                x1 = g1 * g1 / a1
                for g2, w2 in g2n:
                    Eg += p1 * w2 * 2 * phi2(g2) * M(c * (x1 + g2 * g2 / a2 - (a1 + a2) / 5))
            tot += 2 * ws * ww * jac * (a1 - a2) * (a1 * a2) ** 2 * math.exp((a1 + a2) ** 2 / 20 - (a1 * a1 + a2 * a2) / 4) * Eg
    pref = (-(192 / 7) * 2 ** 0.25 * 4 * math.pi * (2 * math.pi) ** -4 * 12 ** -0.5 * 6 ** (-7 / 8) * (2 * math.pi) ** -1.5
            * 0.5 * math.sqrt(4 * math.pi / 5) * (23 / 20) ** (7 / 8) * math.pi * 0.5)
    return pref * tot


REFERENCE = {
    'Math-#207 (826b8be) PROOF.md section 8: c1, d = 2': -0.26939883,
    'Math-#207 (826b8be) PROOF.md section 8: c1, d = 3': -0.21184835,
    'Math-#207: c1/c, d = 2': -3.669938,
    'Math-#207: c1/c, d = 3': -5.071062,
    'Math-#207: I_cand, d = 2': -0.1772744,
    'Math-#207: I_cand - c1, d = 2': 0.0921244,
    'Math-#207: I_cand, d = 3': -0.1394041,
    'Math-#207: I_cand - c1, d = 3': 0.0724443,
    'Math-#207: c, d = 2': 0.0734069193,
    'Math-#207: c, d = 3': 0.0417759318,
    'Math-#207: shipped fixed-seed Monte Carlo c1, d = 3': (-0.21163, 0.00014),
    'Math-#207: development Monte Carlo c1, d = 3 (2e8 samples)': (-0.21188, 0.00010),
    'Math-#207: referee Monte Carlo c1, d = 3 (5e8 samples)': (-0.211848, 0.000024),
    'Math-#216 table: c1, d = 1 (= Math-#214 C_1)': -0.227606,
}


def main():
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        res = json.load(fh)['values']
    def mid(p):
        return 0.5 * (float(p[0]) + float(p[1]))
    print('1. d = 2, independent 2D route (no Mellin identity):')
    c2 = control_d2()
    cert = res['d=2']['c1']
    print('   control %.15f   certified [%s, %s]   difference %.1e' % (c2, cert[0], cert[1], c2 - mid(cert)))
    print('2. d = 3, independent 4D route (no Mellin identity):')
    c3 = control_d3()
    cert = res['d=3']['c1']
    print('   control %.15f   certified [%s, %s]   difference %.1e' % (c3, cert[0], cert[1], c3 - mid(cert)))
    print('3. Floating values of the sources against the certified enclosures:')
    rows = [
        ('Math-#207 (826b8be) PROOF.md section 8: c1, d = 2', res['d=2']['c1']),
        ('Math-#207 (826b8be) PROOF.md section 8: c1, d = 3', res['d=3']['c1']),
        ('Math-#207: c, d = 2', res['d=2']['c_(d,ref)']),
        ('Math-#207: c, d = 3', res['d=3']['c_(d,ref)']),
        ('Math-#207: c1/c, d = 2', res['d=2']['c1 / c_(d,ref)']),
        ('Math-#207: c1/c, d = 3', res['d=3']['c1 / c_(d,ref)']),
        ('Math-#207: I_cand, d = 2', res['d=2']['I_cand = (3^(1/4)/2) c1']),
        ('Math-#207: I_cand - c1, d = 2', res['d=2']['I_cand - c1']),
        ('Math-#207: I_cand, d = 3', res['d=3']['I_cand = (3^(1/4)/2) c1']),
        ('Math-#207: I_cand - c1, d = 3', res['d=3']['I_cand - c1']),
        ('Math-#216 table: c1, d = 1 (= Math-#214 C_1)', res['d=1']['c1']),
    ]
    for name, cert in rows:
        v = REFERENCE[name]
        print('   %-52s %12s   certified mid %+.10f   rounded value differs by %.1e' % (name, v, mid(cert), v - mid(cert)))
    for name in ('Math-#207: shipped fixed-seed Monte Carlo c1, d = 3',
                 'Math-#207: development Monte Carlo c1, d = 3 (2e8 samples)',
                 'Math-#207: referee Monte Carlo c1, d = 3 (5e8 samples)'):
        mc, se = REFERENCE[name]
        print('   %-58s %.6f +- %.6f -> (MC - certified)/s.e. = %+.2f' % (name, mc, se, (mc - mid(res['d=3']['c1'])) / se))


if __name__ == '__main__':
    main()
