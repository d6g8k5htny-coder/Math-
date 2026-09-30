#!/usr/bin/env python3
"""Planar (d = 2) microscopic radius-tail constants for the parent kernel K(z) = exp(-|z|^2/2).

Evaluated (deterministic Gauss quadrature, standard library only; no proof, no enclosure):
  * C_* of [R] (R13): the point-intensity tail F(t) ~ C_* t^-11 of the already-formed microscopic measure, with
    C_* = (216/11) k^7 (c_m/z_0) I J_cusp; in d = 2, c_1 = 1 and c_m h_0(A_0 = 0, tau)/z_0 = [p_b(0)/z_0] p_odd(a, beta, c)
    with the exact contact regression of Math-#168 (A_0 | even pins ~ N(-b, 2); (f_xxz, f_xzz, f_zzz) | odd pins ~
    N(0, diag(2, 2, 6))), so J_cusp = int gamma(a)^11 p_odd(a, a^2/(12k), a^3/(144k^2)) da is a one-dimensional integral;
  * the whole-cluster split of [E] (E5-E6), using [E]'s exact shape constants D and J (companion, unmerged);
  * the second-order coefficient C_2/C_0, the TV coefficient kappa |C_2/C_0| and the signed constant B_sign of [Q]
    (13), (16), (19) with the aligned planar cusp density (21)-(22) (companion, unmerged);
  * control: the near-mass identity alpha_1 + 2 alpha_2 = K_0 int_S int_Z Q |Z|^-12 p_odd (the root-resolved integral
    (R11) integrated over all Z), against the merged Math-#168 values of alpha_1, alpha_2.

    python -B -S tail_constants.py            # full run, writes RESULTS.json (a few minutes)
    python -B -S tail_constants.py --check    # exact controls + replay against RESULTS.json (Python >= 3.11)
    python -B -S tail_constants.py --check --mutant NAME   # must exit 1
"""
import argparse
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('shape-integral', 'gamma-power', 'cusp-shift')
MUT = None
REPLAY_TOL = 1e-6

SQ2PI = math.sqrt(2 * math.pi)
phi = lambda t: math.exp(-t * t / 2) / SQ2PI
Phi = lambda t: 0.5 * math.erfc(-t / math.sqrt(2))
KAPPA = (2 / 13) * (11 / 13) ** 5.5

# companion constants ([E] E5, E20-E21; [Q] (12)), all recomputed exactly below where polynomial
J_OUT = Fr(1083417, 280)
def D_inner():
    return 27066286003 / 223205220 - (79298560 / 4782969) * math.log(2)

# reference values of the merged Math-#168 RESULTS.json (GH60 and MC 1e6), quoted for the control
ALPHA_GH60 = {0.5: (1.11821, 0.0347454), 1.0: (1.32906, 0.0255091), 2.0: (2.1621, 0.0169281)}
ALPHA_MC = {0.5: (1.11457, 0.034938), 1.0: (1.32721, 0.0257064), 2.0: (2.16004, 0.0173858)}
ALPHA_MC_SE1 = {0.5: 0.0856 * 0.0313439, 1.0: 0.283 * 0.00783597, 2.0: 1.69 * 0.00195899}   # s.e. of alpha_1 (J_1 s.e. times prefactor)


def require(cond, msg):
    if not cond:
        print('FAIL: ' + msg)
        sys.exit(1)


# ----------------------------------------------------------------------------- exact shape integrals
class P:
    """Univariate polynomial with Fraction coefficients."""
    def __init__(self, c):
        self.c = {k: Fr(v) for k, v in c.items() if v != 0}
    def __add__(self, o):
        c = dict(self.c)
        for k, v in o.c.items():
            c[k] = c.get(k, 0) + v
        return P(c)
    def __mul__(self, o):
        if not isinstance(o, P):
            return P({k: v * o for k, v in self.c.items()})
        c = {}
        for i, a in self.c.items():
            for j, b in o.c.items():
                c[i + j] = c.get(i + j, 0) + a * b
        return P(c)
    def __pow__(self, n):
        r = P({0: 1})
        for _ in range(n):
            r = r * self
        return r
    def integ(self, lo, hi):
        return sum((v * (Fr(hi) ** (k + 1) - Fr(lo) ** (k + 1)) / (k + 1) for k, v in self.c.items()), Fr(0))


U = P({1: 1}); ONE = P({0: 1}); B0P = ONE * 3 + U * U * (-12)
QV = {3: U * (-16), 2: B0P * 4, 1: U * B0P * B0P * 4, 0: B0P ** 3 * (-1)}   # Q(u, v) as polynomial in v with P(u) coefficients


def vint(F, lo, hi):
    tot = P({})
    for p, cu in F.items():
        tot = tot + cu * (hi ** (p + 1) + lo ** (p + 1) * (-1)) * Fr(1, p + 1)
    return tot


def shape_integral(weight_v):
    """integral_S weight(u, v) Q(u, v) du dv for weight given as dict power_of_v -> P(u); the two strips of S."""
    F = {}
    for p, cu in QV.items():
        for q, cw in weight_v.items():
            F[p + q] = F.get(p + q, P({})) + cu * cw
    lo1 = (U * U * 12 + ONE * (-3)) * Fr(1, 2); hi = ONE * 3 + U * (-6); lo2 = B0P * Fr(1, 2)
    return vint(F, lo1, hi).integ(Fr(-3, 2), Fr(-1, 2)) + vint(F, lo2, hi).integ(Fr(-1, 2), Fr(1, 2))


def exact_constants():
    I = shape_integral({0: ONE})
    U2 = shape_integral({0: U * U})
    Bsh = shape_integral({0: B0P})
    # |u| Q: negative u on (-3/2, 0), positive on (0, 1/2)
    F = {p: cu * U for p, cu in QV.items()}
    lo1 = (U * U * 12 + ONE * (-3)) * Fr(1, 2); hi = ONE * 3 + U * (-6); lo2 = B0P * Fr(1, 2)
    Uabs = -vint(F, lo1, hi).integ(Fr(-3, 2), Fr(-1, 2)) - vint(F, lo2, hi).integ(Fr(-1, 2), 0) + vint(F, lo2, hi).integ(0, Fr(1, 2))
    # eta moments: eta = u + 1/2 + v/6
    E1 = shape_integral({0: U + ONE * Fr(1, 2), 1: ONE * Fr(1, 6)}) / I
    # J = integral over S2_outer: strips 1/2<p<1: A/2<v<Ap ; 1<=p<3/2: A/2<v<3+6p, with u = -p, A = 12p^2-3 (polynomial bounds)
    Pp = P({1: 1}); A = Pp * Pp * 12 + ONE * (-3)
    Qp = {p: cu for p, cu in QV.items()}   # need Q(-p, v): substitute u -> -p
    def subst_neg(poly):
        return P({k: v * (-1) ** k for k, v in poly.c.items()})
    Qm = {p: subst_neg(cu) for p, cu in Qp.items()}
    J = vint(Qm, A * Fr(1, 2), A * Pp).integ(Fr(1, 2), 1) + vint(Qm, A * Fr(1, 2), ONE * 3 + Pp * 6).integ(1, Fr(3, 2))
    if MUT == 'shape-integral':
        I = I + 1
    return {'I': I, 'U2': U2, 'B': Bsh, 'Uabs': Uabs, 'E_eta': E1, 'J_outer': J}


# ----------------------------------------------------------------------------- quadrature
def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for m in range(2, n + 1):
                p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        p0, p1 = 1.0, x
        for m in range(2, n + 1):
            p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        xs.append(x); ws.append(2.0 / ((1 - x * x) * dp * dp))
    return xs, ws


def gl(f, lo, hi, rule):
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    return half * sum(w * f(mid + half * x) for x, w in zip(*rule))


# ----------------------------------------------------------------------------- planar contact structure (Math-#168, exact)
def m2b(b):
    m, s = -b, math.sqrt(2.0)
    t = m / s
    return (m * m + s * s) * Phi(-t) - m * s * phi(t)


def prefactor(k, b):
    """p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 . 36 k^2 m_(2,b)) = c_1 h_0(0, .)/z_0 with the odd Gaussian factored out."""
    return phi(b / math.sqrt(2)) / math.sqrt(2) / (36 * k * k * m2b(b))


def p_odd(a, beta, c):
    return math.exp(-a * a / 4 - beta * beta / 4 - c * c / 12) / ((2 * math.pi) ** 1.5 * math.sqrt(24.0))


def b0(u):
    return 3 - 12 * u * u


def Q(u, v):
    b = b0(u)
    return (4 * v * v - b * b) * (b - 4 * u * v)


def cusp_integrals(k, rule, L=14.0):
    """One-dimensional Gaussian integrals over the cusp slice beta = a^2/(12k), c = a^3/(144k^2):
    J_cusp = int gamma^11 G0, T1 = int gamma^9 (1 + 12 A^2) G0, T2 = int gamma^13 D_a G0, Tb = int |A| gamma^10 G0."""
    gpow = 10 if MUT == 'gamma-power' else 11
    def G0(a):
        cshift = 0.0 if MUT == 'cusp-shift' else a ** 3 / (144 * k * k)
        return p_odd(a, a * a / (12 * k), cshift)
    def gam(a):
        return math.sqrt(1 + (a / (12 * k)) ** 2)
    def DaG0(a):   # D_a = k d_beta + (a/4) d_c on the diagonal cusp density: -(a^2/(12 vbeta) + a^4/(576 k^2 vc)) G0, vbeta = 2, vc = 6
        return -(a * a / 24 + a ** 4 / (3456 * k * k)) * G0(a)
    Jc = gl(lambda a: gam(a) ** gpow * G0(a), -L, L, rule)
    T1 = gl(lambda a: gam(a) ** 9 * (1 + 12 * (a / (12 * k)) ** 2) * G0(a), -L, L, rule)
    T2 = gl(lambda a: gam(a) ** 13 * DaG0(a), -L, L, rule)
    Tb = gl(lambda a: abs(a / (12 * k)) * gam(a) ** 10 * G0(a), -L, L, rule)
    return {'J_cusp': Jc, 'T1': T1, 'T2': T2, 'Tb': Tb}


def near_mass(k, nu, nv, ns, na):
    """108 k^7 int_S Q(u,v) int_{Z != 0} |Z|^-12 int p_odd(a, beta(u,v,Z,a), c(u,v,Z,a)) da dZ du dv, i.e. (R11) with the
    radius indicator removed; times p_b(0)/z_0 this is the near point mass alpha_1 + 2 alpha_2.  Z = +-e^s, so
    |Z|^-12 dZ = e^{-11 s} ds; the s-window is placed at the onset of the Gaussian decay."""
    ru, rv, rs, ra = gauss_legendre(nu), gauss_legendre(nv), gauss_legendre(ns), gauss_legendre(na)
    tot = 0.0
    for (ulo, uhi, lower) in ((-1.5, -0.5, lambda u: (12 * u * u - 3) / 2), (-0.5, 0.5, lambda u: (3 - 12 * u * u) / 2)):
        def fu(u):
            b = b0(u)
            def fv(v):
                q = Q(u, v)
                c3 = 2 * k * (v - b * u)
                cands = []
                if c3 != 0:
                    cands.append(math.log(abs(c3) / 6.0) / 3.0)
                if b != 0:
                    cands.append(0.5 * math.log(k * abs(b) / 4.0))
                s_star = max(cands) if cands else 0.0
                def fs(s):
                    Zi2 = math.exp(-2 * s); Zi3 = math.exp(-3 * s)
                    acc = 0.0
                    for sign in (1.0, -1.0):
                        def fa(a):
                            return p_odd(a, a * a / (12 * k) + k * b * Zi2, a ** 3 / (144 * k * k) + (a * b / 4) * Zi2 + sign * c3 * Zi3)
                        acc += gl(fa, -14.0, 14.0, ra)
                    return math.exp(-11 * s) * acc
                return q * gl(fs, s_star - 3.0, s_star + 4.5, rs)
            return gl(fv, lower(u), 3 - 6 * u, rv)
        tot += gl(fu, ulo, uhi, ru)
    return 108 * k ** 7 * tot


# ----------------------------------------------------------------------------- assembly
def constants_table(k, b, ex, cu):
    I = float(ex['I']); U2 = float(ex['U2']); Bsh = float(ex['B']); Uabs = float(ex['Uabs'])
    D = D_inner(); J = float(ex['J_outer'])
    pf = prefactor(k, b)
    K0 = 108 * k ** 7 * pf
    C0 = (216 / 11) * k ** 7 * pf * cu['J_cusp']          # [E]'s C0: coefficient per unit shape integral
    Cstar = C0 * I                                       # [R]'s C_* = [Q]'s C_0
    C2 = K0 * (U2 * cu['T1'] + (2 * Bsh / 13) * cu['T2'])
    c = C2 / Cstar
    Bsign = (K0 / Cstar) * Uabs * cu['Tb']
    return {'prefactor_p_b0_over_z0': pf, 'K0': K0, 'C0_per_shape': C0, 'C_star': Cstar,
            'G_max_coeff': C0 * (I - D), 'G2_coeff': C0 * J, 'B2_coeff': C0 * D, 'singleton_coeff': C0 * (I - D - J),
            'C2': C2, 'C2_over_C0': c, 'tv_coefficient_kappa_c': KAPPA * c, 'B_sign': Bsign,
            'lower_bound_C2_over_C0_4587_856': 4587 / 856, 'upper_bound_B_sign_4587821_876544': 4587821 / 876544}


def controls():
    ex = exact_constants()
    require(ex['I'] == Fr(246528, 35), 'I = 246528/35')
    require(ex['U2'] == Fr(240192, 35) and ex['B'] == Fr(-428544, 7) and ex['Uabs'] == Fr(5898627, 880), 'U2, B, Uabs exact')
    require(ex['B'] == 3 * ex['I'] - 12 * ex['U2'], 'B = 3I - 12 U2')
    require(ex['E_eta'] == Fr(5771, 7062), 'E eta = 5771/7062')
    require(ex['J_outer'] == J_OUT, 'J = 1083417/280')
    require(Fr(11) * ex['U2'] / (2 * ex['I']) == Fr(4587, 856), '11 U2/(2I) = 4587/856')
    require(Fr(11) * ex['Uabs'] / (2 * ex['I']) == Fr(4587821, 876544), '11 Uabs/(2I) = 4587821/876544')
    D = D_inner()
    require(0 < D < float(ex['I']) - float(ex['J_outer']), 'D positive and I - D - J positive')
    q0 = math.sqrt(13 / 11)
    require(abs(KAPPA - (q0 ** -11 - q0 ** -13)) < 1e-15, 'kappa = q0^-11 - q0^-13')
    # planar contact structure: prefactor at b = 0 is 1/(36 k^2 sqrt(4 pi)) ... phi(0)/sqrt2/(36k^2)
    require(abs(prefactor(1.0, 0.0) - phi(0.0) / math.sqrt(2) / 36) < 1e-15, 'prefactor at b = 0, k = 1')
    # p_odd normalization
    r = gauss_legendre(64)
    z = gl(lambda a: gl(lambda be: gl(lambda c: p_odd(a, be, c), -20, 20, r), -20, 20, r), -20, 20, r)
    require(abs(z - 1.0) < 1e-10, 'p_odd normalized')
    return ex


def full_run():
    ex = controls()
    res = {'object': 'CL-C6-MICRO-TAIL-NUMERICS-20260930-v1', 'scientific_effect': 'NONE', 'certified': False,
           'dimension': 2, 'exact': {k: str(v) for k, v in ex.items()}, 'D_inner': D_inner(), 'kappa': KAPPA,
           'quadrature': {'cusp_gl': 96, 'cusp_gl_check': 48, 'cusp_range': 14.0, 'near_mass_levels': [[32, 32, 64, 32], [64, 64, 64, 32], [96, 96, 64, 32]]},
           'per_k': {}, 'table': {}, 'near_mass_identity': {}}
    r96, r48 = gauss_legendre(96), gauss_legendre(48)
    for k in (0.5, 1.0, 2.0):
        cu = cusp_integrals(k, r96)
        cu48 = cusp_integrals(k, r48)
        res['per_k'][str(k)] = {'cusp': cu, 'cusp_gl48_rel_dev': {n: abs(cu48[n] - cu[n]) / abs(cu[n]) for n in cu}}
        for b in (0.0, 1.0):
            res['table']['k=%s,b=%s' % (k, b)] = constants_table(k, b, ex, cu)
        levels = {}
        for nodes in res['quadrature']['near_mass_levels']:
            levels['x'.join(map(str, nodes))] = near_mass(k, *nodes)
        pf0, pf1 = prefactor(k, 0.0), prefactor(k, 1.0)
        top = levels['96x96x64x32']
        a1, a2 = ALPHA_GH60[k]; m1, m2 = ALPHA_MC[k]
        res['near_mass_identity']['k=%s' % k] = {
            'K0_integral_without_prefactor_by_level': levels,
            'alpha1_plus_2alpha2_b0': pf0 * top, 'alpha1_plus_2alpha2_b1': pf1 * top,
            'ref_gh60_b0': a1 + 2 * a2, 'ref_mc_b0': m1 + 2 * m2, 'ref_mc_b0_se_alpha1': ALPHA_MC_SE1[k],
            'rel_dev_vs_gh60': (pf0 * top - (a1 + 2 * a2)) / (a1 + 2 * a2), 'rel_dev_vs_mc': (pf0 * top - (m1 + 2 * m2)) / (m1 + 2 * m2)}
        print('k', k, 'C_*(b=0) = %.6g' % res['table']['k=%s,b=0.0' % k]['C_star'], 'near mass', pf0 * top, 'ref', a1 + 2 * a2, m1 + 2 * m2, flush=True)
    return res


def check_run():
    ex = controls()
    path = os.path.join(HERE, 'RESULTS.json')
    require(os.path.exists(path), 'RESULTS.json present')
    with open(path) as fh:
        ref = json.load(fh)
    r96 = gauss_legendre(96)
    for k in (0.5, 1.0, 2.0):
        cu = cusp_integrals(k, r96)
        for n in cu:
            require(abs(cu[n] - ref['per_k'][str(k)]['cusp'][n]) <= REPLAY_TOL * abs(ref['per_k'][str(k)]['cusp'][n]), 'cusp integral replay %s k=%s' % (n, k))
        t = constants_table(k, 0.0, ex, cu)
        require(abs(t['C_star'] - ref['table']['k=%s,b=0.0' % k]['C_star']) <= REPLAY_TOL * ref['table']['k=%s,b=0.0' % k]['C_star'], 'C_* replay k=%s' % k)
    nm = near_mass(1.0, 32, 32, 64, 32)
    require(abs(nm - ref['near_mass_identity']['k=1.0']['K0_integral_without_prefactor_by_level']['32x32x64x32']) <= REPLAY_TOL * nm, 'near-mass replay (low level)')
    top = ref['near_mass_identity']['k=1.0']['alpha1_plus_2alpha2_b0']
    require(abs(top - ref['near_mass_identity']['k=1.0']['ref_mc_b0']) < 3 * ref['near_mass_identity']['k=1.0']['ref_mc_b0_se_alpha1'] + 2e-3, 'near-mass identity within tolerance of the Math-#168 MC value')
    print(json.dumps({'check': 'ok', 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    if args.check:
        check_run()
        return
    res = full_run()
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote RESULTS.json')


if __name__ == '__main__':
    main()
