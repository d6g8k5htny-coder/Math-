"""Floating controls for CL-C2-TORUS-TRANSFER-20261001 (NOTE.md section 6; not part of the certificate).

Control 1 (reference).  The floating integrator below, applied to the exact Gaussian-kernel data of c2_exact, returns c2
inside the certified intervals of frontiers/c2_exact_20261001/RESULTS.json.

Control 0 (Lemma E, exact).  For anisotropic product kernels prod_i exp(-s_i z_i^2/2) (rational jets; not isotropic),
the exact integrand of the fixed-cone surrogate has G_0 = G_1 = G_3 = 0 and G_5 = -(k/2)(d_b G_2 - (d_b E) G_2): the
identities that A~_r = A~(r^2, b - k r^3/2, k) implies.  These are exact identities of rational polynomials.

Control 2 (falsification of Lemmas F, G, P at a measurable scale).  For the isotropic, even, normalized mixture kernels
    K_eps(z) = (1 - eps) exp(-|z|^2/2) + eps exp(-s |z|^2/2),     s = 2 or 1/2,
c2[K_eps] is computed directly: c2_exact's exact derivation with the jets of K_eps (rational), then the floating
integration in closed form (k: Gamma finite parts; b: completing the square; cone: half-line / quadrant moments).  The
certified bound of transfer.bound_core, fed with balls (phi-jet, |K_eps-jet - phi-jet|), must exceed |c2[K_eps] - c2[phi]|.
Both the bound and the difference are linear in eps for small eps; their ratio is the slack of the bound.

    python3 -B -S controls.py"""
from fractions import Fraction as Fr
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pseries as P          # noqa: E402
import exact as X            # noqa: E402
import transfer as T         # noqa: E402
from ball import B           # noqa: E402

GAUSS_RHO = P.rho_der
C2_INTERVALS = {1: ('0.2300445802661503', '0.2300445802661998'), 2: ('0.2215244106266632', '0.2215244106267110'),
                3: ('0.1612340491269447', '0.1612340491269810')}


def mix_rho(eps, s):
    def rho(g):
        v = GAUSS_RHO(g)
        return v * ((1 - eps) + eps * s ** (sum(g) // 2)) if v else 0
    return rho


def half_moment_f(j, c):
    """int_0^oo t^j e^(-c t^2) dt"""
    return math.gamma((j + 1) / 2) * c ** (-(j + 1) / 2) / 2


def quadrant_moments_f(al, be, ga, nmax):
    D = 4 * al * ga - be * be
    M = {(0, 0): (math.pi / 2 - math.atan(be / math.sqrt(D))) / math.sqrt(D)}
    for n in range(nmax):
        for i in range(n + 1):
            j = n - i
            R1 = M[(i - 1, j)] * i if i else half_moment_f(j, ga)
            R2 = M[(i, j - 1)] * j if j else half_moment_f(i, al)
            M.setdefault((i + 1, j), (R1 * 2 * ga - R2 * be) / D)
            M.setdefault((i, j + 1), (R2 * 2 * al - R1 * be) / D)
    return M


def c2_float(d, data):
    """c2 = (|S^(d-1)|/3) const int db f.p. int dk k^(-4/3) int_cone exp(-E) H w  for isotropic-kernel data of
    exact.kernel_data (rotation-reduced in d = 3), with general exponent coefficients."""
    G = data['G']
    H = G.rcoef(4)
    E = (data['q0'] + data['Q0']) * Fr(1, 2)
    ak = float(E.coef_of('k', 2).scalar())
    if not (E.coef_of("k", 1).is_zero() and E.degree("k") == 2):
        raise ArithmeticError("unexpected k-dependence of the exponent")
    # k: f.p. int_0^oo k^(j - 4/3) e^(-ak k^2) dk = Gamma((j - 1/3)/2) ak^(-(j - 1/3)/2) / 2
    Hk = {}
    for e, c in H.t.items():
        j = e[2]
        a = (j - Fr(1, 3)) / 2
        val = float(c) * math.gamma(float(a)) * ak ** (-float(a)) / 2
        key = (e[1],) + e[3:]
        Hk[key] = Hk.get(key, 0.0) + val
    Ek = E.coef_of('k', 0)
    ab = float(Ek.coef_of('b', 2).scalar())
    Lx, Rx = Ek.coef_of('b', 1), Ek.coef_of('b', 0)
    # complete the square: b -> b - Lx/(2 ab); expand (b - l)^n with l a linear form in x (floats)
    lin = {e[3:]: float(c) / (2 * ab) for e, c in Lx.t.items()}         # l(x) = sum lin[e] x^e
    Hb = {}
    for key, val in Hk.items():
        n, xe = key[0], key[1:]
        # (b - l)^n = sum_m C(n, m) b^m (-l)^(n-m); keep even m
        lpow = {(0, 0): 1.0}
        powers = [dict(lpow)]
        for _ in range(n):
            nxt = {}
            for e1, c1 in powers[-1].items():
                for e2, c2 in lin.items():
                    e = (e1[0] + e2[0], e1[1] + e2[1])
                    nxt[e] = nxt.get(e, 0.0) + c1 * c2
            powers.append(nxt)
        for m in range(0, n + 1, 2):
            bm = 2 * half_moment_f(m, ab)
            for e, c in powers[n - m].items():
                kk = (xe[0] + e[0], xe[1] + e[1])
                Hb[kk] = Hb.get(kk, 0.0) + val * math.comb(n, m) * bm * c * (-1) ** (n - m)
    Ex = Rx - Lx * Lx * (Fr(1) / (4 * Ek.coef_of('b', 2).scalar()))
    total = 0.0
    if d == 1:
        total = sum(Hb.values())
    elif d == 2:
        g = float(Ex.coef_of('x1', 2).scalar())
        for key, val in Hb.items():
            total += val * half_moment_f(key[0], g) * (-1) ** key[0]
    else:
        al = float(Ex.coef_of('x1', 2).scalar())
        ga = float(Ex.coef_of('x2', 2).scalar())
        bx = float(Ex.coef_of('x1', 1).coef_of('x2', 1).scalar())
        # x1 = -s, x2 = -s - t:  al s^2 + bx s (s + t) + ga (s + t)^2 ; weight x1 - x2 = t
        A_ = al + bx + ga
        Bt = bx + 2 * ga
        C_ = ga
        nmax = max(k[0] + k[1] for k in Hb) + 3
        M = quadrant_moments_f(A_, Bt, C_, nmax)
        for key, val in Hb.items():
            i, j = key
            # x1^i x2^j = (-s)^i (-s - t)^j
            for m in range(j + 1):
                coef = math.comb(j, m) * (-1) ** (i + j)
                total += val * coef * M[(i + m, j - m + 1)]
    nn = data['p'] + (0 if d == 1 else (1 if d == 2 else 3))
    const = -12 * (2 * math.pi) ** (-nn / 2) / math.sqrt(float(data['detS0'] * data['detT0']))
    if d == 3:
        const *= math.pi
    sphere = {1: 2, 2: 2 * math.pi, 3: 4 * math.pi}[d]
    return sphere / 3 * const * total


def aniso_rho(sv):
    def rho(g):
        v = GAUSS_RHO(g)
        if not v:
            return Fr(0)
        out = Fr(v)
        for gi, si in zip(g, sv):
            out *= si ** (gi // 2)
        return out
    return rho


def evenness_checks():
    fails = 0
    nr0 = T.NR
    T.NR = 5                                       # series exact through r^5 at pseries.R = 8
    try:
        for d in (1, 2, 3):
            for sv in ([Fr(1), Fr(3, 2), Fr(5, 4)], [Fr(2), Fr(1, 3), Fr(7, 5)]):
                D = T.kernel(d, aniso_rho(sv[:d]))
                G, E = D['G'], D['E']
                G2 = G.rcoef(2)
                rhs5 = (G2.deriv('b') - E.deriv('b') * G2) * T.Poly.var('k') * Fr(-1, 2)
                ok = G.rcoef(0).is_zero() and G.rcoef(1).is_zero() and G.rcoef(3).is_zero() and \
                    (G.rcoef(5) - rhs5).is_zero() and not G2.is_zero()
                fails += not ok
                print('Lemma E, d=%d, s=%s: G0=G1=G3=0 and G5 = -(k/2)(d_b - E_b)G2: %s'
                      % (d, [str(x) for x in sv[:d]], ok))
    finally:
        T.NR = nr0
    return fails


def run():
    fails = evenness_checks()
    out = {}
    for d in (1, 2, 3):
        P.rho_der = GAUSS_RHO
        ref = c2_float(d, X.kernel_data(d))
        lo, hi = (float(x) for x in C2_INTERVALS[d])
        ok = lo - 1e-12 <= ref <= hi + 1e-12
        fails += not ok
        print('d=%d reference c2 (floating) %.15f  in certified interval: %s' % (d, ref, ok))
        for s in (Fr(2), Fr(1, 2)):
            for eps in (Fr(1, 1000), Fr(1, 100000)):
                P.rho_der = mix_rho(eps, s)
                c2m = c2_float(d, X.kernel_data(d))
                P.rho_der = GAUSS_RHO
                mix = mix_rho(eps, s)

                def jc(g, mix=mix):
                    if sum(g) % 2:
                        return B(0)
                    v = GAUSS_RHO(g)
                    return B(v, abs(Fr(mix(g)) - v))
                bd = T.bound_core(d, T.kernel(d, jc))
                diff = abs(c2m - ref)
                ok = float(bd['eps']) >= diff
                fails += not ok
                out[(d, s, eps)] = (diff, float(bd['eps']))
                print('  s=%s eps=%s: |c2[K]-c2[phi]| = %.3e   bound = %.3e   slack %.1f   %s'
                      % (s, eps, diff, float(bd['eps']), float(bd['eps']) / diff if diff else float('inf'),
                         'ok' if ok else 'FAIL'))
    print('controls: %d failures' % fails)
    return fails


if __name__ == '__main__':
    sys.exit(1 if run() else 0)
