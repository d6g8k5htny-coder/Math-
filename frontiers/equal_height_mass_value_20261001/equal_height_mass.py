#!/usr/bin/env python3
"""Controls and the far-field coefficient of Theorem Z's equal-height mass (CL-EQUAL-HEIGHT-MASS-20261001-v1).
Standard library only; deterministic (exact rationals where exact, fixed Gauss-Legendre quadrature otherwise).

For the stationary field on R^d with covariance exp(-|z|^2/2) and d = 2, 3, the height densities (per unit volume
and unit height) of critical points of index j are

    rho_j(b) = phi(b) (2 pi)^(-d/2) E[ |det(G - b I)| 1{index(G - b I) = j} ],

where, given f = b and grad f = 0, the Hessian is H = -b I + G with G centred, Var G_ii = 2, Cov(G_ii, G_jj) = 0
(i != j), Var G_ij = 1, i.e. G has density proportional to exp(-tr G^2 / 4) (a scaled GOE).  The far-field
coefficient of the equal-height mass B_{d,L} of [Z] (Z3) is

    beta_d = int rho_d(b) rho_{d-1}(b) db                 (maxima against index-(d-1) saddles).

  Q1  the conditional law of the Hessian (exact rationals, Hermite moments of the Gaussian kernel): given f and
      grad f, the full covariance of the Hessian entries is the scaled-GOE pattern (Var f_ii = 2, Var f_ij = 1, every
      other pair 0) and E[f_ii | f = b] = -b, E[f_ij | f = b] = 0, in d = 2 and d = 3;
  Q2  the scaled-GOE normalisation: the quadrature of int |Vandermonde| exp(-sum lambda^2/4) over ordered eigenvalues,
      times d!, equals Mehta's closed form 8 sqrt(2 pi) (d = 2) and 8 (2 pi)^(3/2) 3/sqrt(pi) = 48 sqrt(2) pi (d = 3);
  Q3  the total densities against closed forms: d = 2, n_max = 1/(2 pi sqrt 3), n_sad = 1/(pi sqrt 3); d = 3 (Bardeen,
      Bond, Kaiser and Szalay 1986, with R*^3 = 27/(15 sqrt 15)), n_max = (29 - 6 sqrt 6)/(5^(3/2) 8 pi^2 R*^3) and
      n_sad = (29 + 6 sqrt 6)/(5^(3/2) 8 pi^2 R*^3), to 1e-8 relative;
  Q4  beta_2 and beta_3 at two quadrature resolutions (agreement to 1e-8 relative), and 24^3 beta_3.
  M   mutants (--mutant M1|M2|M3) exit 1: M1 uses the unconditioned diagonal variance 3 (weight exp(-lambda^2/6)),
      M2 drops the Vandermonde factor, M3 counts index-d points as the saddles; an unknown label exits 2.
  Scope: these are numerical controls of the one-point densities and of beta_d.  They do not test Proposition V
  (the volume law), the near-field correction gamma_d (see gamma_explore.py, exploration only) or Theorem Z.
"""
import argparse
import json
import math
import sys
from fractions import Fraction as F

# ------------------------------------------------------------------------------------------ Q1: exact moments

def kap(n):
    """E-moment structure of exp(-z^2/2): d^n/dz^n at 0 is 0 (n odd) or (-1)^(n/2) (n-1)!! (n even)."""
    if n % 2:
        return F(0)
    out = 1
    for t in range(n - 1, 0, -2):
        out *= t
    return F((-1) ** (n // 2) * out)


def cov(a, b):
    out = F((-1) ** sum(b))
    for x, y in zip(a, b):
        out *= kap(x + y)
    return out


def solve(M, v):
    n = len(M)
    A = [row[:] + [v[i]] for i, row in enumerate(M)]
    for i in range(n):
        p = next(r for r in range(i, n) if A[r][i] != 0)
        A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i and A[r][i] != 0:
                fct = A[r][i] / A[i][i]
                A[r] = [x - fct * y for x, y in zip(A[r], A[i])]
    return [A[i][n] / A[i][i] for i in range(n)]


def check_Q1(d):
    e = lambda *ks: tuple(sum(1 for k in ks if k == t) for t in range(d))
    obs = [tuple([0] * d)] + [e(t) for t in range(d)]
    hes = [e(i, j) for i in range(d) for j in range(i, d)]
    C = [[cov(a, b) for b in obs] for a in obs]
    out = {}
    for h in hes:
        for g in hes:
            x = solve(C, [cov(o, g) for o in obs])
            out[(h, g)] = cov(h, g) - sum(xi * cov(h, o) for xi, o in zip(x, obs))
    reg = {h: solve(C, [cov(o, h) for o in obs])[0] for h in hes}
    # the full conditional covariance must be the scaled-GOE pattern: Var f_ii = 2, Var f_ij = 1 (i < j), all other
    # pairs 0 (this is what makes the density proportional to exp(-tr G^2/4)); regression on f: -1 on f_ii, 0 on f_ij
    for h in hes:
        for g in hes:
            if h == g:
                want = F(2) if max(h) == 2 else F(1)
            else:
                want = F(0)
            if out[(h, g)] != want:
                return False
        if reg[h] != (F(-1) if max(h) == 2 else F(0)):
            return False
    return True

# ------------------------------------------------------------------------- quadrature over ordered eigenvalues

def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


class Quad:
    def __init__(self, n, mutant):
        self.gx, self.gw = gauss_legendre(n)
        self.var = 3.0 if mutant == 'M1' else 2.0          # diagonal variance of G (M1: unconditioned)
        self.vdm = mutant != 'M2'
        self.A = 12.0

    def nodes(self, a, b):
        h, c = (b - a) / 2, (a + b) / 2
        return [(c + h * x, h * w) for x, w in zip(self.gx, self.gw)]

    def wt(self, x):
        return math.exp(-x * x / (2 * self.var))

    def vd(self, *ls):
        if not self.vdm:
            return 1.0
        out = 1.0
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                out *= ls[j] - ls[i]
        return out

    def ordered_integral(self, d, region, integrand):
        """int over lambda_1 < ... < lambda_d with the per-coordinate ranges given by region(level, previous)."""
        A = self.A
        if d == 2:
            tot = 0.0
            lo2, hi2 = region['top']
            for l2, w2 in self.nodes(lo2, hi2):
                lo1, hi1 = region['low'](l2)
                s = 0.0
                for l1, w1 in self.nodes(lo1, hi1):
                    s += w1 * integrand(l1, l2) * self.vd(l1, l2) * self.wt(l1)
                tot += w2 * s * self.wt(l2)
            return tot
        tot = 0.0
        lo3, hi3 = region['top']
        for l3, w3 in self.nodes(lo3, hi3):
            lo2, hi2 = region['mid'](l3)
            s2 = 0.0
            for l2, w2 in self.nodes(lo2, hi2):
                lo1, hi1 = region['low'](l2)
                s1 = 0.0
                for l1, w1 in self.nodes(lo1, hi1):
                    s1 += w1 * integrand(l1, l2, l3) * self.vd(l1, l2, l3) * self.wt(l1)
                s2 += w2 * s1 * self.wt(l2)
            tot += w3 * s2 * self.wt(l3)
        return tot

    def normaliser(self, d):
        A = self.A
        if d == 2:
            reg = {'top': (-A, A), 'low': lambda l2: (-A, l2)}
        else:
            reg = {'top': (-A, A), 'mid': lambda l3: (-A, l3), 'low': lambda l2: (-A, l2)}
        return math.factorial(d) * self.ordered_integral(d, reg, lambda *ls: 1.0)

    def expectations(self, d, b, Z, mutant):
        """E|det(G - b)| 1{index d} and 1{index d-1} (M3: index d counted for both)."""
        A = self.A
        prod = lambda *ls: abs(math.prod(l - b for l in ls))
        if d == 2:
            rmax = {'top': (-A, b), 'low': lambda l2: (-A, l2)}
            rsad = {'top': (b, A), 'low': lambda l2: (-A, b)}
        else:
            rmax = {'top': (-A, b), 'mid': lambda l3: (-A, l3), 'low': lambda l2: (-A, l2)}
            rsad = {'top': (b, A), 'mid': lambda l3: (-A, b), 'low': lambda l2: (-A, l2)}
        emax = math.factorial(d) * self.ordered_integral(d, rmax, prod) / Z
        esad = emax if mutant == 'M3' else math.factorial(d) * self.ordered_integral(d, rsad, prod) / Z
        return emax, esad


def mehta(d):
    return 8 * math.sqrt(2 * math.pi) if d == 2 else 8 * (2 * math.pi) ** 1.5 * 3 / math.sqrt(math.pi)


def closed_densities(d):
    if d == 2:
        return 1 / (2 * math.pi * math.sqrt(3)), 1 / (math.pi * math.sqrt(3))
    rs3 = 27 / (15 * math.sqrt(15))
    den = 5 ** 1.5 * 8 * math.pi ** 2 * rs3
    return (29 - 6 * math.sqrt(6)) / den, (29 + 6 * math.sqrt(6)) / den


def densities_and_beta(d, n, nb, mutant):
    q = Quad(n, mutant)
    Z = q.normaliser(d)                                    # quadrature-consistent; Q2 compares it with Mehta
    bx, bw = gauss_legendre(nb)
    nm = ns = beta = 0.0
    for x, w in zip(bx, bw):
        b, wb = 7.0 * x, 7.0 * w
        em, es = q.expectations(d, b, Z, mutant)
        pref = math.exp(-b * b / 2) / math.sqrt(2 * math.pi) * (2 * math.pi) ** (-d / 2)
        nm += wb * pref * em
        ns += wb * pref * es
        beta += wb * pref * em * pref * es
    return nm, ns, beta, Z


def sig(x, k=10):
    return float('%.*g' % (k, x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    mut = args.mutant
    checks, ok_all = {}, True
    q1 = check_Q1(2) and check_Q1(3)
    checks['Q1_conditional_hessian_law'] = {'passed': q1, 'info': 'scaled GOE: Var f_ii = 2, Var f_ij = 1, all other pairs 0; E[f_ii | f = b] = -b'}
    ok_all &= q1
    vals = {}
    for d in (2, 3):
        hi = densities_and_beta(d, 48, 56, mut)
        lo = densities_and_beta(d, 40, 48, mut)
        vals[d] = (hi, lo)
    q2 = all(abs(vals[d][0][3] - mehta(d)) <= 1e-8 * mehta(d) for d in (2, 3))
    checks['Q2_scaled_GOE_normalisation'] = {'passed': q2, 'info': {str(d): sig(vals[d][0][3]) for d in (2, 3)}}
    ok_all &= q2
    q3 = True
    info3 = {}
    for d in (2, 3):
        cm, cs = closed_densities(d)
        nm, ns = vals[d][0][0], vals[d][0][1]
        info3[str(d)] = {'n_max': sig(nm), 'n_max_closed': sig(cm), 'n_sad': sig(ns), 'n_sad_closed': sig(cs)}
        q3 &= abs(nm - cm) <= 1e-8 * cm and abs(ns - cs) <= 1e-8 * cs
    checks['Q3_total_densities_closed_forms'] = {'passed': q3, 'info': info3}
    ok_all &= q3
    q4 = all(abs(vals[d][0][2] - vals[d][1][2]) <= 1e-8 * abs(vals[d][0][2]) for d in (2, 3))
    checks['Q4_beta_two_resolutions'] = {'passed': q4, 'info': {'beta_2': sig(vals[2][0][2]), 'beta_3': sig(vals[3][0][2]),
                                                                  '24^3 beta_3': sig(24 ** 3 * vals[3][0][2], 8)}}
    ok_all &= q4
    out = {'object': 'CL-EQUAL-HEIGHT-MASS-20261001-v1', 'scientific_effect': 'NONE', 'passed': bool(ok_all),
           'mutant': mut, 'checks': checks}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
