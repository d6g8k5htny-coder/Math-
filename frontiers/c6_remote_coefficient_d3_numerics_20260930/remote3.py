#!/usr/bin/env python3
"""Numerical evaluation of the remote contact kernel Lambda_j(x; b, k, u) of [RM] (13) in dimension d = 3 for the
continuum kernel K(x) = exp(-|x|^2/2): its far-field value (exact shifted-GOE quadrature), the correlation-hole
constant c_hole = integral (Lambda - Lambda_inf) d^3x (Monte Carlo with common random numbers), and the resulting
torus integral k integral_X Lambda dx = k (L^3 Lambda_inf + c_hole) entering nu(1) = a_1 + k integral Lambda
([SC] (22), [CL] (1.4)).  Standard library only.  Not a proof, not an enclosure.

    python -B -S remote3.py            # full run, writes RESULTS.json (about 40 minutes)
    python -B -S remote3.py --check    # exact controls + replay of a small subset against RESULTS.json
    python -B -S remote3.py --check --mutant NAME   # must exit 1

Conventions ([RM] section 2, (4), (10), (13)).  Coordinates x = (x1, y, z), x1 along the pin axis u.
U_0 = (f, f_x, f_xx, f_xxx, f_y, f_z, f_xy, f_xz)(0) = (b, 0, 0, 12k, 0, 0, 0, 0); A_0 = (f_yy, f_yz, f_zz)(0);
Y_x = (f_x, f_y, f_z, f)(x) = (0, 0, 0, b); H_x = the six Hessian entries at x.
w_0 = 36 k^2 (det A_0)^2 1{A_0 negative definite}; z_0 = E[w_0 | U_0] = 36 k^2 m_(3,b) (Math-#184 Lemma 2).
Lambda_j(x) = p_(Y_x | U_0)(0, b) E[w_0 F_j(H_x) | U_0, Y_x] / z_0, F_j(H) = |det H| 1{index H = j}, j = 0..3.
Cov(d^alpha f(s), d^beta f(t)) = (-1)^|alpha| d^(alpha+beta) K(t - s); d^n exp(-t^2/2) = (-1)^n He_n(t) exp(-t^2/2).
Lambda depends on (x1, r), r = sqrt(y^2 + z^2), by rotation invariance about the axis; the spatial integrals use
cylindrical midpoint rules with weight 2 pi r.
"""
import argparse
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr
from math import erf, exp, factorial, gamma, pi, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('hermite-sign', 'det-abs', 'weight-indicator')
RULES = (20, 16, 16)               # nested Gauss-Legendre nodes for the A_0 cone quadrature (5120 nodes)
MUT = None
REPLAY_TOL = 1e-9
D = 3
Z3 = (0, 0, 0)


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'what': msg, 'mutant': MUT}))
        sys.exit(1)


# ----------------------------------------------------------------------------- kernel and covariances
def hermite(n, t):
    """Probabilists' Hermite polynomial He_n(t)."""
    if n == 0:
        return 1.0
    h0, h1 = 1.0, t
    for m in range(1, n):
        h0, h1 = h1, t * h1 - m * h0
    return h1


def kernel_derivative(gam, y):
    """d^gam K(y), K(y) = exp(-|y|^2/2): prod_i (-1)^gam_i He_gam_i(y_i) exp(-y_i^2/2)."""
    v = 1.0
    for g, yi in zip(gam, y):
        sign = (-1) ** g
        if MUT == 'hermite-sign':
            sign = 1.0
        v *= sign * hermite(g, yi) * exp(-yi * yi / 2)
    return v


def cov(al, s, be, t):
    return (-1) ** sum(al) * kernel_derivative(tuple(a + b for a, b in zip(al, be)), [ti - si for si, ti in zip(s, t)])


def unit(i, n=1):
    v = [0] * D
    v[i] = n
    return tuple(v)


def add(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(D))


OBS0 = [Z3, unit(0), unit(0, 2), unit(0, 3), unit(1), unit(2), add(unit(0), unit(1)), add(unit(0), unit(2))]
A0J = [add(unit(1), unit(1)), add(unit(1), unit(2)), add(unit(2), unit(2))]
OBSX = [unit(0), unit(1), unit(2), Z3]
HXJ = [add(unit(i), unit(j)) for i in range(3) for j in range(i, 3)]   # xx xy xz yy yz zz


def v0(b, k):
    return [b, 0.0, 0.0, 12 * k, 0.0, 0.0, 0.0, 0.0]


# ----------------------------------------------------------------------------- exact one-site table (rational)
def c_even(n):
    if n % 2:
        return Fr(0)
    v = Fr(1)
    for j in range(1, n, 2):
        v *= j
    return v * (-1) ** (n // 2)


def cov_point_exact(al, be):
    v = Fr((-1) ** sum(al))
    for a, b in zip(al, be):
        v *= c_even(a + b)
    return v


def mat_inv(M):
    n = len(M)
    A = [row[:] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def exact_contact_law():
    """A_0 | U_0 exactly: mean coefficients and conditional covariance (must be -b I + GOE(2, 1))."""
    Soo = [[cov_point_exact(a, b) for b in OBS0] for a in OBS0]
    Sto = [[cov_point_exact(a, b) for b in OBS0] for a in A0J]
    Stt = [[cov_point_exact(a, b) for b in A0J] for a in A0J]
    inv = mat_inv(Soo)
    reg = [[sum(Sto[i][k] * inv[k][j] for k in range(8)) for j in range(8)] for i in range(3)]
    cc = [[Stt[i][j] - sum(reg[i][k] * Sto[j][k] for k in range(8)) for j in range(3)] for i in range(3)]
    return reg, cc


# ----------------------------------------------------------------------------- linear algebra (floats)
def cholesky(S):
    n = len(S)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = S[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError('not positive definite')
                L[i][i] = sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def solve(L, b):
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def n_negative3(m):
    d1 = m[0][0]
    d2 = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    d3 = det3(m)
    seq = [1.0, d1, d2, d3]
    return sum(1 for i in range(3) if seq[i] * seq[i + 1] < 0)


# ----------------------------------------------------------------------------- quadrature and special functions
def phi(t):
    return exp(-t * t / 2) / sqrt(2 * pi)


def Phi(t):
    return 0.5 * (1 + erf(t / sqrt(2)))


def phi2(t):
    return phi(t / sqrt(2)) / sqrt(2)


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
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def gl(f, lo, hi, rule):
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    return half * sum(w * f(mid + half * x) for x, w in zip(*rule))


def c_m(m):
    """[SC] (8) spectral constant through Mehta's integral."""
    return pi ** (m * (m - 1) / 4) * factorial(m) * gamma(1.5) ** m / math.prod(gamma(1 + j / 2) for j in range(1, m + 1))


def goe_functional(m, b, weight_fn, n=40, L=14.0):
    """sum over sign patterns: E[weight_fn(eigs) 1{index j}] for A = -b I + GOE_m(2, 1), j = number of negative
    eigenvalues, by the ordered eigenvalue density c_m (2 pi)^(-m(m-1)/4) prod phi2(l_i + b) Vandermonde."""
    rule = gauss_legendre(n)
    pref = c_m(m) * (2 * pi) ** (-m * (m - 1) / 4)
    out = [0.0] * (m + 1)
    xs, ws = rule

    def rec(prev, depth, acc, nneg):
        if depth == m:
            out[nneg] += acc * weight_fn(prev)
            return
        last = prev[-1] if prev else None
        for (lo, hi, neg) in (((last if last is not None else -L - abs(b)), 0.0, 1), (max(0.0, last if last is not None else 0.0), L + abs(b), 0)):
            if hi <= lo:
                continue
            mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
            for xg, wg in zip(xs, ws):
                l = mid + half * xg
                v = phi2(l + b) * half * wg
                for pp in prev:
                    v *= (l - pp)
                rec(prev + [l], depth + 1, acc * v, nneg + neg)
    rec([], 0, pref, 0)
    return out


def m3(b, n=40):
    """m_(3,b) = E[(det A)^2 1{A negative definite}], A = -b I_2 + GOE_2(2, 1) (Math-#184 Lemma 2 / closed form at b = 0)."""
    return goe_functional(2, b, lambda l: (l[0] * l[1]) ** 2, n)[2]


def far_field(b, n=40):
    """Lambda_inf_j(b) = phi(b) (2 pi)^(-3/2) E[|det(-b I + G_3)| 1{index j}]: the decoupled far-field kernel."""
    E = goe_functional(3, b, lambda l: abs(l[0] * l[1] * l[2]), n)
    pref = phi(b) * (2 * pi) ** (-1.5)
    return {'E_absdet_index': E, 'lambda_j': [pref * e for e in E], 'lambda': pref * sum(E)}


def R3(b):
    """Math-#184's dimension factor R_3(b) = N_3(b) m_(2,b) / m_(3,b), quoted for the assembly (conditional on #184)."""
    mu, s = -b, sqrt(2)
    t = mu / s
    m2 = (mu * mu + s * s) * Phi(-t) - mu * s * phi(t)
    rule = gauss_legendre(200)
    N3 = sqrt(pi / 2) * gl(lambda a: (-a) ** 3 * phi2(a + b), -40.0, 0.0, rule)
    return N3 * m2 / m3(b)


# ----------------------------------------------------------------------------- conditioning at a point
class Conditioning:
    """Conditional law of T = (A_0, H_x) given U_0 = v_0, Y_x = (0, b), and the density p_(Y_x | U_0)(0, b)."""

    def __init__(self, x, b, k):
        obs = [(a, Z3) for a in OBS0] + [(a, x) for a in OBSX]
        vals = v0(b, k) + [0.0, 0.0, 0.0, b]
        tg = [(a, Z3) for a in A0J] + [(a, x) for a in HXJ]
        Soo = [[cov(a, s, c, t) for (c, t) in obs] for (a, s) in obs]
        Sto = [[cov(a, s, c, t) for (c, t) in obs] for (a, s) in tg]
        Stt = [[cov(a, s, c, t) for (c, t) in tg] for (a, s) in tg]
        L = cholesky(Soo)
        W = [solve(L, row) for row in Sto]
        self.mu = [sum(W[i][j] * vals[j] for j in range(len(vals))) for i in range(len(tg))]
        cc = [[Stt[i][j] - sum(W[i][l] * Sto[j][l] for l in range(len(vals))) for j in range(len(tg))] for i in range(len(tg))]
        self.cov = cc
        SAA = [r[:3] for r in cc[:3]]
        SHA = [r[:3] for r in cc[3:]]
        SHH = [r[3:] for r in cc[3:]]
        self.covA = SAA
        self.LA = cholesky(SAA)
        Bt = [solve(self.LA, [SHA[i][j] for j in range(3)]) for i in range(6)]      # rows: Sigma_HA Sigma_AA^-1
        self.B = Bt
        SHgA = [[SHH[i][j] - sum(Bt[i][l] * SHA[j][l] for l in range(3)) for j in range(6)] for i in range(6)]
        self.LH = cholesky(SHgA)
        self.rules = RULES
        n0 = len(OBS0)
        S00 = [r[:n0] for r in Soo[:n0]]
        Sy0 = [r[:n0] for r in Soo[n0:]]
        Syy = [r[n0:] for r in Soo[n0:]]
        L0 = cholesky(S00)
        Wy = [solve(L0, row) for row in Sy0]
        muy = [sum(Wy[i][j] * vals[j] for j in range(n0)) for i in range(4)]
        cy = [[Syy[i][j] - sum(Wy[i][l] * Sy0[j][l] for l in range(n0)) for j in range(4)] for i in range(4)]
        Ly = cholesky(cy)
        dy = [vals[n0 + i] - muy[i] for i in range(4)]
        q = solve(Ly, dy)
        q2 = sum(dy[i] * q[i] for i in range(4))
        logdet = 2 * sum(math.log(Ly[i][i]) for i in range(4))
        self.density = exp(-0.5 * q2 - 0.5 * logdet - 2 * math.log(2 * pi))
        self.k = k

    def cone_nodes(self, rules=None):
        """Nodes of the nested Gauss-Legendre cone quadrature for the A_0 integral: (A_0 entries, weight, H-mean)."""
        rules = rules or self.rules
        na, nc, ne = rules
        mu, k = self.mu, self.k
        muA, muH = mu[:3], mu[3:]
        LA, B, SA = self.LA, self.B, self.covA
        logdetA = 2 * sum(math.log(LA[i][i]) for i in range(3))
        m_a = 0.5 * (muA[0] + muA[2])
        s_a = sqrt(max(0.25 * (SA[0][0] + SA[2][2] + 2 * SA[0][2]), 1e-300))
        a_lo = min(m_a - 7 * s_a, -1e-9)
        a_hi = min(0.0, m_a + 7 * s_a)
        nodes = []
        if a_hi <= a_lo:
            return nodes
        ra, rc, re = gauss_legendre(na), gauss_legendre(nc), gauss_legendre(ne)
        mid_a, half_a = 0.5 * (a_lo + a_hi), 0.5 * (a_hi - a_lo)
        for xa, wa in zip(*ra):
            a = mid_a + half_a * xa
            half_c = -a
            for xc, wc in zip(*rc):
                c = half_c * xc
                half_e = sqrt(max(a * a - c * c, 0.0))
                for xe, we in zip(*re):
                    e = half_e * xe
                    A = [a + c, e, a - c]
                    d = [A[i] - muA[i] for i in range(3)]
                    q = solve(LA, d)
                    q2 = sum(d[i] * q[i] for i in range(3))
                    dens = exp(-0.5 * q2 - 0.5 * logdetA - 1.5 * math.log(2 * pi))
                    detA = a * a - c * c - e * e
                    if MUT == 'weight-indicator':
                        detA = detA + 0.5 * (c * c + e * e)
                    w = 2.0 * (half_a * wa) * (half_c * wc) * (half_e * we) * detA * detA * dens
                    if w <= 0.0:
                        continue
                    mH = [muH[i] + sum(B[i][j] * d[j] for j in range(3)) for i in range(6)]
                    nodes.append((w, mH))
        return nodes

    def weighted(self, zs, rules=None):
        """E[w_0 F_j(H_x) | U_0, Y_x] = 36 k^2 integral_(A_0 neg. def.) (det A_0)^2 p(A_0) E[F_j(H_x) | A_0] dA_0.

        The A_0 integral is the nested Gauss-Legendre cone quadrature of cone_nodes (Jacobian 2; the cone is a < 0,
        c^2 + e^2 < a^2 in (a, c, e) = ((a11 + a22)/2, (a11 - a22)/2, a12); the integrand (a^2 - c^2 - e^2)^2 vanishes to
        second order on the cone boundary).  E[F_j(H_x) | A_0] is Monte Carlo on the supplied 6-dim standard normals zs
        (common random numbers across x), H_x | A_0 being Gaussian with mean affine in A_0 and fixed covariance; the
        sample budget len(zs) is allocated to the nodes in proportion to their weights (at least one sample per node),
        so the effective sample size is the whole budget."""
        if rules is None:
            if getattr(self, '_nodes', None) is None:
                self._nodes = self.cone_nodes()
            nodes = self._nodes
        else:
            nodes = self.cone_nodes(rules)
        if not nodes:
            return [0.0] * 4
        total_w = sum(w for w, _ in nodes)
        N = len(zs)
        LH, k = self.LH, self.k
        acc = [0.0] * 4
        pos = 0
        for w, mH in nodes:
            n = max(1, int(round(N * w / total_w)))
            block = zs[pos:pos + n]
            pos += n
            if not block:
                # budget exhausted by rounding: reuse the first samples (deterministic, tiny weights only)
                block = zs[:n]
            part = [0.0] * 4
            for z in block:
                t = [mH[i] + sum(LH[i][j] * z[j] for j in range(i + 1)) for i in range(6)]
                H = [[t[0], t[1], t[2]], [t[1], t[3], t[4]], [t[2], t[4], t[5]]]
                dH = det3(H)
                part[n_negative3(H)] += (dH if MUT == 'det-abs' else abs(dH))
            for j in range(4):
                acc[j] += w * part[j] / len(block)
        return [36 * k * k * v for v in acc]


def standard_normals(n, seed, dim=6):
    rng = random.Random(seed)
    return [[rng.gauss(0.0, 1.0) for _ in range(dim)] for _ in range(n)]


def lambda_at(x, b, k, zs, z0):
    c = Conditioning(x, b, k)
    E = c.weighted(zs)
    lam_j = [c.density * e / z0 for e in E]
    return {'x': list(x), 'density': c.density, 'lambda_j': lam_j, 'lambda': sum(lam_j)}


# ----------------------------------------------------------------------------- spatial integrals
def hole_integral(b, k, zbatches, z0, Rc=6.0, h=0.4, x_far=(10.0, 0.0, 0.0)):
    """c_hole_j = integral (Lambda_j - Lambda_j(x_far)) d^3x over the cylinder |x1| <= Rc, r <= Rc, by the midpoint rule in
    (x1, r) with weight 2 pi r, estimated with common random numbers per batch; the far point is decoupled to 1e-16, so
    Lambda(x_far) = Lambda_inf.  zbatches is a list of independent sample arrays; batch means give the standard error."""
    n1 = int(round(2 * Rc / h))
    nr = int(round(Rc / h))
    h1, hr = 2 * Rc / n1, Rc / nr
    far = Conditioning(x_far, b, k)
    batches = len(zbatches)
    far_b = [far.weighted(zs) for zs in zbatches]
    tot_b = [[0.0] * 4 for _ in range(batches)]
    skipped = 0
    for i in range(n1):
        x1 = -Rc + (i + 0.5) * h1
        for j in range(nr):
            r = (j + 0.5) * hr
            vol = 2 * pi * r * h1 * hr
            try:
                c = Conditioning((x1, r, 0.0), b, k)
            except ValueError:
                skipped += 1
                continue
            for bi, zs in enumerate(zbatches):
                E = c.weighted(zs)
                for q in range(4):
                    tot_b[bi][q] += vol * (c.density * E[q] - far.density * far_b[bi][q]) / z0
    means = [sum(tot_b[bi][q] for bi in range(batches)) / batches for q in range(4)]
    ses = [sqrt(sum((tot_b[bi][q] - means[q]) ** 2 for bi in range(batches)) / (batches - 1) / batches) for q in range(4)]
    tot = [sum(tot_b[bi]) for bi in range(batches)]
    mean_t = sum(tot) / batches
    se_t = sqrt(sum((t - mean_t) ** 2 for t in tot) / (batches - 1) / batches)
    return {'hole_j': means, 'hole_j_se': ses, 'hole': mean_t, 'hole_se': se_t,
            'grid': {'Rc': Rc, 'h1': h1, 'hr': hr, 'points': n1 * nr, 'skipped_near_pin': skipped},
            'far_point': list(x_far), 'far_weighted_mc': [sum(far_b[bi][q] for bi in range(batches)) / batches for q in range(4)],
            'samples_per_batch': len(zbatches[0]), 'batches': batches}


def ray_profile(b, k, zs, z0, lam_inf):
    rays = {'axis': (1.0, 0.0), 'transverse': (0.0, 1.0), 'diag45': (1 / sqrt(2), 1 / sqrt(2))}
    out = {}
    for name, (c1, cr) in rays.items():
        rows = []
        for rho in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0):
            x = (c1 * rho, cr * rho, 0.0)
            try:
                res = lambda_at(x, b, k, zs, z0)
                rows.append({'rho': rho, 'lambda': res['lambda'], 'ratio_to_far': res['lambda'] / lam_inf, 'lambda_j': res['lambda_j']})
            except ValueError:
                rows.append({'rho': rho, 'lambda': None})
        out[name] = rows
    return out


# ----------------------------------------------------------------------------- planar inputs (Math-#168) and assembly
def planar_alphas():
    path = os.path.join(HERE, '..', 'c6_cluster_coefficients_numerics_20260930', 'RESULTS.json')
    with open(path) as fh:
        return json.load(fh)['prefactor']


def controls(zs):
    reg, cc = exact_contact_law()
    require(all(reg[i][0] == (Fr(-1) if i in (0, 2) else Fr(0)) for i in range(3)) and all(reg[i][j] == 0 for i in range(3) for j in range(1, 8)),
            'A_0 | U_0 has mean -b I (exact)')
    require(cc == [[Fr(2), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(2)]], 'A_0 | U_0 is GOE(2, 1) (exact)')
    require(abs(c_m(2) - pi) < 1e-13, 'c_2 = pi')
    m30 = m3(0.0)
    require(abs(m30 - (7 - 4 * sqrt(2)) / 2) < 1e-10, 'm_(3,0) = (7 - 4 sqrt2)/2')
    ff0 = far_field(0.0)
    E = ff0['E_absdet_index']
    require(abs(E[0] - E[3]) < 1e-10 and abs(E[1] - E[2]) < 1e-10, 'index symmetry j <-> 3 - j at b = 0')
    tot = goe_functional(3, 0.0, lambda l: 1.0)
    require(abs(sum(tot) - 1) < 1e-9, 'eigenvalue density normalizes to 1')
    # decoupled far point: density equals phi(b) (2 pi)^(-3/2) and the weighted expectation equals z_0 E[|det| 1{j}]
    out = {'m_3_0': m30, 'E_absdet_index_b0': E, 'far_field_b0': ff0['lambda'], 'far_field_b1': far_field(1.0)['lambda']}
    for b in (0.0, 1.0):
        c = Conditioning((10.0, 0.0, 0.0), b, 1.0)
        require(abs(c.density - phi(b) * (2 * pi) ** (-1.5)) < 1e-12, 'far density decouples b = %r' % b)
        z0 = 36 * m3(b)
        Emc = c.weighted(zs)
        Eq = far_field(b)['E_absdet_index']
        out['far_mc_over_quadrature_b%s' % b] = [Emc[j] / (z0 * Eq[j]) for j in range(4)]
    # E|det G_3| at b = 0 (the level-0 factor) and the level-integrated far field: integral_b Lambda_inf_j(b) db is the
    # density of index-j critical points of the unconditioned field, whose classical closed forms in this normalization
    # (unit Gaussian kernel: sigma_0 = 1, per-component sigma_1 = 1, sigma_2^2 = 15) are (29 sqrt3 - 18 sqrt2)/(72 pi^2)
    # for maxima and minima and (29 sqrt3 + 18 sqrt2)/(72 pi^2) for each saddle index (Bardeen-Bond-Kaiser-Szalay 1986)
    out['E_absdet_G3_quadrature'] = sum(goe_functional(3, 0.0, lambda l: abs(l[0] * l[1] * l[2])))
    rule = gauss_legendre(60)
    dens = [gl(lambda bb: far_field(bb, n=24)['lambda_j'][j], -8.0, 8.0, rule) for j in range(4)]
    out['critical_point_density_by_index'] = dens
    out['closed_form_extrema'] = (29 * sqrt(3) - 18 * sqrt(2)) / (72 * pi ** 2)
    out['closed_form_saddles'] = (29 * sqrt(3) + 18 * sqrt(2)) / (72 * pi ** 2)
    require(abs(dens[0] - out['closed_form_extrema']) < 1e-9 and abs(dens[3] - out['closed_form_extrema']) < 1e-9,
            'level-integrated far field: extrema density (29 sqrt3 - 18 sqrt2)/(72 pi^2)')
    require(abs(dens[1] - out['closed_form_saddles']) < 1e-9 and abs(dens[2] - out['closed_form_saddles']) < 1e-9,
            'level-integrated far field: saddle density (29 sqrt3 + 18 sqrt2)/(72 pi^2)')
    return out


def full_run(fast=False):
    nb = 4
    per_batch = 3000 if fast else 40000
    zbatches = [standard_normals(per_batch, 2026 + i) for i in range(nb)]
    zs = [z for zb in zbatches for z in zb]
    res = {'schema': 1, 'object': 'CL-C6-REMOTE-COEFF-D3-NUMERICS-20260930-v1', 'scientific_effect': 'NONE', 'certified': False,
           'kernel': 'exp(-|x|^2/2), continuum, d = 3', 'mutant': MUT, 'python_requirement': '>= 3.11',
           'samples_per_batch': per_batch, 'batches': nb, 'rules': list(RULES), 'seeds': [2026 + i for i in range(nb)]}
    res['controls'] = controls(zs)
    res['far_field'] = {str(b): far_field(b) for b in (0.0, 1.0)}
    res['z0'] = {}
    res['hole'] = {}
    res['ray_profiles'] = {}
    res['remote_total'] = {}
    res['R_3'] = {str(b): R3(b) for b in (0.0, 1.0)}
    alphas = planar_alphas()
    res['assembled_nu'] = {}
    # grid and cutoff study at k = 1, b = 0 with two batches (same noise level as the difference estimator)
    z00 = 36 * m3(0.0)
    res['grid_convergence'] = {'k=1.0,b=0.0': {
        'hole_h=0.6,Rc=6': hole_integral(0.0, 1.0, zbatches[:2], z00, h=0.6 if not fast else 0.9),
        'hole_h=0.3,Rc=6': hole_integral(0.0, 1.0, zbatches[:2], z00, h=0.3 if not fast else 0.9),
        'hole_h=0.4,Rc=5': hole_integral(0.0, 1.0, zbatches[:2], z00, Rc=5.0, h=0.4 if not fast else 0.9)}}
    for k in (0.5, 1.0, 2.0):
        for b in (0.0, 1.0):
            key = 'k=%s,b=%s' % (k, b)
            z0 = 36 * k * k * m3(b)
            res['z0'][key] = z0
            lam_inf = res['far_field'][str(b)]['lambda']
            H = hole_integral(b, k, zbatches, z0, h=0.6 if fast else 0.4)
            res['hole'][key] = H
            if k == 1.0:
                res['ray_profiles'][key] = ray_profile(b, k, zs, z0, lam_inf)
            res['remote_total'][key] = {'L=%d' % L: {'approx_L3_lambda_inf_plus_hole': L ** 3 * lam_inf + H['hole'], 'se': H['hole_se']} for L in (12, 24)}
            kstr = {0.5: 'k=1/2', 1.0: 'k=1', 2.0: 'k=2'}[k]
            a1 = alphas['%s,b=%d' % (kstr, int(b))]['alpha1_gh60'] * res['R_3'][str(b)]
            a2 = alphas['%s,b=%d' % (kstr, int(b))]['alpha2_gh60'] * res['R_3'][str(b)]
            res['assembled_nu'][key] = {'a1_d3': a1, 'a2_d3': a2,
                                        'nu1_L': {'L=%d' % L: a1 + k * (L ** 3 * lam_inf + H['hole']) for L in (12, 24)},
                                        'nu2_over_nu1_L': {'L=%d' % L: a2 / (a1 + k * (L ** 3 * lam_inf + H['hole'])) for L in (12, 24)},
                                        'note': 'a_j^(3) = R_3(b) alpha_j^(2) (Math-#184, unmerged, conditional); alpha from Math-#168 GH60 (floating)'}
    return res


def check_run():
    zs = standard_normals(40000, 2026)
    ctl = controls(zs)
    path = os.path.join(HERE, 'RESULTS.json')
    require(os.path.exists(path), 'RESULTS.json present')
    with open(path) as fh:
        ref = json.load(fh)
    for b in (0.0, 1.0):
        require(abs(far_field(b)['lambda'] - ref['far_field'][str(b)]['lambda']) < 1e-12, 'far-field replay b = %r' % b)
        require(abs(R3(b) - ref['R_3'][str(b)]) < 1e-9, 'R_3 replay b = %r' % b)
    for j in range(3):
        r = ctl['far_mc_over_quadrature_b0.0'][j]
        require(0.9 < r < 1.1, 'far-point Monte Carlo within 10%% of z_0 E|det|1{j}, j = %d' % j)
    # replay one kernel point per (k = 1, b) with the stored sample (same seeds and lengths as the full run)
    zfull = [z for i in range(ref['batches']) for z in standard_normals(ref['samples_per_batch'], ref['seeds'][i])]
    for key, prof in ref['ray_profiles'].items():
        b = float(key.split('b=')[1])
        z0 = ref['z0'][key]
        # the transverse ray is blind to a sign error in the odd derivatives (it is the y -> -y reflection), so the
        # axis and the diagonal ray, where the ramp 2 k x1^3 breaks that symmetry, are replayed as well
        for name, idx, direction in (('transverse', 3, (0.0, 1.0)), ('diag45', 4, (1 / sqrt(2), 1 / sqrt(2))), ('axis', 5, (1.0, 0.0))):
            row = prof[name][idx]
            res = lambda_at((direction[0] * row['rho'], direction[1] * row['rho'], 0.0), b, 1.0, zfull, z0)
            require(abs(res['lambda'] - row['lambda']) <= REPLAY_TOL * max(abs(row['lambda']), 1e-9), '%s replay %s' % (name, key))
    print(json.dumps({'check': 'ok', 'far_field_b0': ctl['far_field_b0'], 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--fast', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    if args.check:
        check_run()
        return
    res = full_run(fast=args.fast)
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote RESULTS.json')


if __name__ == '__main__':
    main()
