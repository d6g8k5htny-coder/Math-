#!/usr/bin/env python3
"""Exact finite controls for PROOF.md (CL-D2-REMAINDER-VANISHING-20260930-v1).  Standard library only; exact rationals.

  E1  axial pin identities on a quintic profile f(x) = b0 + f1 x + f2 x^2/2 + f3 x^3/6 + f4 x^4/24 + f5 x^5/120: with
      b0, f1, f2, f3 solved from the four pins f(-r/2) = b, f(r/2) = b - k r^3, f'(-r/2) = f'(r/2) = 0 one finds
      f2 = -(r^2/24) f4, f3 = 12k - (r^2/40) f5, and alpha_M = f''(-r/2)/r = -6k + (r/12) f4 - (r^2/120) f5,
      alpha_S = f''(r/2)/r = 6k + (r/12) f4 + (r^2/120) f5, alpha_M alpha_S = -36k^2 + r^2 (f4^2/144 - k f5/10)
      - r^4 f5^2/14400 -- all exact at rational (r, k, f4, f5, b); mutant M1 drops the (r^2/40) f5 term;
  E2  reflection symmetry: for a general quintic in (x, y) with fifteen free rational coefficients, the six pinned
      coefficients (c00, c10, c20, c30, c01, c11) are solved exactly at rational r and at -r from f(M) = b,
      f(S) = b - k r^3, grad f(M) = grad f(S) = 0, M = (-r/2, 0), S = (r/2, 0); the identity det H_M(-r) = det H_S(r)
      holds exactly; consequently det H_M det H_S / r^2, recovered by exact Lagrange interpolation at eleven rational r
      as the polynomial of degree <= 10 in r, has only even powers, constant term -36 k^2 A0^2 (A0 = f_yy(0) = 2 c02)
      and the recorded r^2 coefficient (the parity is forced by the symmetry: a check of the mechanism, not of the
      bookkeeping); mutant M2 applies the parity test to the single factor det H_M / r, which is not even;
  E3  the block identity det K = alpha det A - r beta^T adj(A) beta, and Haynsworth's inertia additivity
      inertia(K) = inertia(A) + inertia(alpha - r beta^T A^{-1} beta), on rational 2x2/3x3 blocks A that are negative
      definite, of index m - 1, and indefinite, with the scalar Schur complement of both signs (inertia by exact
      congruence diagonalisation); the Step 4 case split: F_d(K_M) = 0 whenever lambda_max(A_M) > 0 (A_M has a
      positive eigenvalue), and |det A| <= |lambda_max(A)| * ||A||_op^(m-1) when |lambda_max(A)| is the smallest
      absolute eigenvalue, at rational points;
  E4  the ledger of section 2 and Remark 2 by exact monomial substitution r = (ell/k)^(1/3): r^-2 (ell/r^3)^2 =
      ell^2 r^-8 (so the far-cutoff tail is ell^2 r0^-7), k^(-2/3) r^3 / k = ell k^(-8/3), ell kappa^(-5/3) = kappa^(7/3)
      = ell^(7/12) at kappa = ell^(1/4), ell^(2/3) a^(-1/3) = r0 ell^(1/3) for a = ell r0^-3, and r <= k iff ell <= k^4 at
      rational (k, r) with ell = k r^3; mutant M3 claims the loss exponent 1/3;
  E5  the layer algebra of Step 4: k^2 u^2 = C1^2 r^2 T^2 (k + T)^2 and r T^2 <= k u / C1 for u = C1 r T (1 + T/k), exactly.
  M   mutants (--mutant M1|M2|M3) exit 1; an unknown label exits 2.
"""
import argparse
import json
import sys
from fractions import Fraction as F


# ---------------------------------------------------------------------------------------------------- linear algebra
def solve(Mx, rhs):
    n = len(Mx)
    A = [list(r) + [b] for r, b in zip(Mx, rhs)]
    for col in range(n):
        piv = next((r for r in range(col, n) if A[r][col] != 0), None)
        if piv is None:
            return None
        A[col], A[piv] = A[piv], A[col]
        inv = 1/A[col][col]
        A[col] = [v*inv for v in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f*b for a, b in zip(A[r], A[col])]
    return [A[r][n] for r in range(n)]


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    total = F(0)
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in M[1:]]
        total += (-1)**j*M[0][j]*det(minor)
    return total


def adj(M):
    n = len(M)
    out = [[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for r_, row in enumerate(M) if r_ != i]
            out[j][i] = (-1)**(i+j)*det(minor) if n > 1 else F(1)
    return out


def inertia(M):
    """(negatives, zeros, positives) of a symmetric rational matrix by congruence diagonalisation."""
    n = len(M)
    A = [row[:] for row in M]
    neg = zero = pos = 0
    for i in range(n):
        if A[i][i] == 0:
            piv = next((j for j in range(i + 1, n) if A[j][j] != 0), None)
            if piv is not None:
                A[i], A[piv] = A[piv], A[i]
                for row in A:
                    row[i], row[piv] = row[piv], row[i]
            else:
                j = next((j for j in range(i + 1, n) if A[i][j] != 0), None)
                if j is None:
                    zero += 1
                    continue
                # row_i += row_j, col_i += col_j (congruence) makes the (i,i) entry 2 A[i][j] + A[j][j] = 2 A[i][j]
                for c in range(n):
                    A[i][c] += A[j][c]
                for r_ in range(n):
                    A[r_][i] += A[r_][j]
        p = A[i][i]
        if p == 0:
            zero += 1
            continue
        if p < 0:
            neg += 1
        else:
            pos += 1
        for r_ in range(i + 1, n):
            if A[r_][i] != 0:
                f = A[r_][i]/p
                for c in range(n):
                    A[r_][c] -= f*A[i][c]
                for c in range(n):
                    A[c][r_] -= f*A[c][i]
    return neg, zero, pos


# ---------------------------------------------------------------------------------------------------- E1
def check_E1(mutant):
    n = 0
    for (r, k, f4, f5, b) in ((F(1, 10), F(2), F(3), F(-7), F(1, 3)), (F(1, 3), F(1, 5), F(-11), F(13), F(0)),
                              (F(2, 7), F(4), F(1, 2), F(1, 3), F(-5))):
        f2 = -(r*r/24)*f4
        f3 = 12*k - (r*r/40)*f5
        if mutant == 'M1':
            f3 = 12*k
        # f1, b0 from the gradient and height pins
        def fx(x, f1):
            return f1 + f2*x + f3*x*x/2 + f4*x**3/6 + f5*x**4/24
        # f'(-r/2) = 0 gives f1
        f1 = -(f2*(-r/2) + f3*(r*r/4)/2 + f4*(-r/2)**3/6 + f5*(r/2)**4/24)
        if fx(r/2, f1) != 0:
            return False, 'gradient pin at S fails'
        def f(x, b0):
            return b0 + f1*x + f2*x*x/2 + f3*x**3/6 + f4*x**4/24 + f5*x**5/120
        b0 = b - (f(-r/2, F(0)))
        if f(-r/2, b0) != b or f(r/2, b0) != b - k*r**3:
            return False, 'height pins fail'
        def fxx(x):
            return f2 + f3*x + f4*x*x/2 + f5*x**3/6
        aM, aS = fxx(-r/2)/r, fxx(r/2)/r
        if aM != -6*k + (r/12)*f4 - (r*r/120)*f5 or aS != 6*k + (r/12)*f4 + (r*r/120)*f5:
            return False, 'alpha expansions'
        if aM*aS != -36*k*k + r*r*(f4*f4/144 - k*f5/10) - r**4*f5*f5/14400:
            return False, 'alpha product'
        n += 1
    return True, {'points': n, 'alpha_M': '-6k + (r/12) f4 - (r^2/120) f5', 'product': '-36k^2 + r^2 (f4^2/144 - k f5/10) - r^4 f5^2/14400'}


# ---------------------------------------------------------------------------------------------------- E2
MONOS = [(i, j) for i in range(6) for j in range(6 - i)]      # 21 monomials x^i y^j, i + j <= 5
PINNED = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1)]
FREE = [m for m in MONOS if m not in PINNED]


def d_coef(i, j, dx, dy, x, y):
    """value of d^dx_x d^dy_y (x^i y^j) at (x, y)."""
    c = F(1)
    for t in range(dx):
        if i - t <= 0:
            return F(0)
        c *= (i - t)
    for t in range(dy):
        if j - t <= 0:
            return F(0)
        c *= (j - t)
    return c*x**(i - dx)*y**(j - dy)


def pinned_poly(r, k, b, free, sign):
    """Return the full coefficient dict of the pinned quintic (sign = +1: f(S) = b - k r^3; sign = -1: b + k r^3)."""
    M = (-r/2, F(0)); S = (r/2, F(0))
    conds = [((0, 0), M, b), ((0, 0), S, b - sign*k*r**3), ((1, 0), M, F(0)), ((1, 0), S, F(0)), ((0, 1), M, F(0)), ((0, 1), S, F(0))]
    rows, rhs = [], []
    for (dx, dy), pt, val in conds:
        rows.append([d_coef(i, j, dx, dy, *pt) for (i, j) in PINNED])
        rhs.append(val - sum(free[m]*d_coef(m[0], m[1], dx, dy, *pt) for m in FREE))
    sol = solve(rows, rhs)
    coef = dict(free)
    for m, v in zip(PINNED, sol):
        coef[m] = v
    return coef


def hess(coef, x, y):
    fxx = sum(c*d_coef(i, j, 2, 0, x, y) for (i, j), c in coef.items())
    fxy = sum(c*d_coef(i, j, 1, 1, x, y) for (i, j), c in coef.items())
    fyy = sum(c*d_coef(i, j, 0, 2, x, y) for (i, j), c in coef.items())
    return fxx, fxy, fyy


def interpolate(xs, ys):
    """Coefficients (low to high) of the unique polynomial of degree < len(xs) through (xs, ys): exact Lagrange."""
    n = len(xs)
    coeffs = [F(0)]*n
    for i in range(n):
        # basis polynomial l_i
        num = [F(1)]
        denom = F(1)
        for j in range(n):
            if j != i:
                num = [F(0)] + num
                for t in range(len(num) - 1):
                    num[t] -= xs[j]*num[t + 1]
                denom *= (xs[i] - xs[j])
        for t in range(n):
            coeffs[t] += ys[i]*num[t]/denom
    return coeffs


def check_E2(mutant):
    k, b = F(3, 2), F(-1, 4)
    free = {}
    vals = [F(2), F(-1), F(1, 2), F(3), F(-2, 3), F(5), F(-1, 5), F(7, 3), F(1), F(-4), F(2, 7), F(-3, 2), F(4, 5), F(-1, 7), F(6)]
    for m, v in zip(FREE, vals):
        free[m] = v
    sign = 1
    def dets(r):
        coef = pinned_poly(r, k, b, free, sign)
        fxxM, fxyM, fyyM = hess(coef, -r/2, F(0))
        fxxS, fxyS, fyyS = hess(coef, r/2, F(0))
        return fxxM*fyyM - fxyM*fxyM, fxxS*fyyS - fxyS*fxyS
    # the reflection symmetry: the pinned family at -r has M and S exchanged, so det H_M(-r) = det H_S(r)
    for r in (F(1, 10), F(3, 7), F(1)):
        dMm, dSm = dets(-r)
        dMp, dSp = dets(r)
        if dMm != dSp or dSm != dMp:
            return False, 'reflection identity det H_M(-r) = det H_S(r) fails'
    def value(r):
        dM, dS = dets(r)
        if mutant == 'M2':
            return dM/r                       # a single endpoint: NOT even in r
        return dM*dS/(r*r)
    xs = [F(n, 10) for n in range(1, 12)]        # eleven rational r values
    ys = [value(r) for r in xs]
    poly = interpolate(xs, ys)
    # verify at a twelfth value that the degree-10 interpolant is the polynomial (degree <= 10 in r)
    r12 = F(13, 10)
    if sum(c*r12**t for t, c in enumerate(poly)) != value(r12):
        return False, 'not a polynomial of degree <= 10 in r'
    odd = [t for t in range(1, 11, 2) if poly[t] != 0]
    if odd:
        return False, 'odd powers present: %s' % odd
    A0 = 2*free[(0, 2)]
    if poly[0] != -36*k*k*A0*A0:
        return False, 'constant term is not -36 k^2 A0^2'
    c02, c12, c21, c22, c31, c40, c50 = (free[(0, 2)], free[(1, 2)], free[(2, 1)], free[(2, 2)], free[(3, 1)], free[(4, 0)], free[(5, 0)])
    r2 = (16*c02**2*c40**2 - 48*c02**2*c50*k - 8*c02*c21**2*c40 + 24*c02*c21*c31*k - 72*c02*c22*k*k
          + 36*c12**2*k*k - 12*c12*c21**2*k + c21**4)
    if poly[2] != r2:
        return False, 'r^2 coefficient differs from the displayed polynomial'
    return True, {'reflection_identity': 'det H_M(-r) = det H_S(r) at 3 rational r', 'degrees_present': [t for t in range(11) if poly[t] != 0],
                  'constant': str(poly[0]), 'r2_coefficient': str(poly[2])}


# ---------------------------------------------------------------------------------------------------- E3
def block(alpha, beta, A, r):
    n = len(A) + 1
    K = [[F(0)]*n for _ in range(n)]
    K[0][0] = alpha
    for i in range(len(A)):
        K[0][i+1] = K[i+1][0] = r*beta[i]      # sqrt(r) beta entries squared give r; with r rational we use t = r directly
        for j in range(len(A)):
            K[i+1][j+1] = A[i][j]
    return K


def check_E3(mutant):
    # Use K_t with entries t*beta in place of sqrt(t) beta: det = alpha det A - t^2 beta^T adj(A) beta.  To test the
    # displayed identity with parameter r we take t^2 = r, i.e. entries sqrt(r) beta: choose r a rational square.
    cases = 0
    A_list = [
        [[F(-2), F(1, 2)], [F(1, 2), F(-3)]],                                    # negative definite
        [[F(-2), F(0)], [F(0), F(1)]],                                            # index m-1 = 1
        [[F(-3), F(1), F(0)], [F(1), F(-2), F(1, 2)], [F(0), F(1, 2), F(-4)]],    # negative definite 3x3
        [[F(-3), F(1), F(0)], [F(1), F(2), F(1, 2)], [F(0), F(1, 2), F(-4)]],     # indefinite 3x3
    ]
    for A in A_list:
        m = len(A)
        adjA = adj(A); dA = det(A)
        for beta in ([F(1), F(-2)] if m == 2 else [F(1), F(-2), F(1, 3)], [F(0)]*m):
            for alpha in (F(-5), F(-1, 10), F(1, 10), F(5)):
                for s in (F(1, 2), F(2)):        # sqrt(r) = s, r = s^2
                    r = s*s
                    n = m + 1
                    K = [[F(0)]*n for _ in range(n)]
                    K[0][0] = alpha
                    for i in range(m):
                        K[0][i+1] = K[i+1][0] = s*beta[i]
                        for j in range(m):
                            K[i+1][j+1] = A[i][j]
                    q = sum(beta[i]*sum(adjA[i][j]*beta[j] for j in range(m)) for i in range(m))
                    if det(K) != alpha*dA - r*q:
                        return False, 'block determinant identity'
                    if dA != 0:
                        sigma = alpha - r*q/dA                       # alpha - r beta^T A^{-1} beta  (A^{-1} = adj/det)
                        negK = inertia(K)[0]
                        negA = inertia(A)[0]
                        if negK != negA + (1 if sigma < 0 else 0):
                            return False, 'Haynsworth inertia additivity fails'
                    cases += 1
    # good-event inequalities: A_S negative definite and alpha_S > 0 give sigma_S > 0
    A = A_list[0]; adjA = adj(A); dA = det(A)
    for beta in ([F(1), F(-2)], [F(3), F(1, 7)]):
        q = sum(beta[i]*sum(adjA[i][j]*beta[j] for j in range(2)) for i in range(2))
        for alpha in (F(1, 100), F(3)):
            for r in (F(1, 10), F(1)):
                if not (alpha - r*q/dA > 0):
                    return False, 'sigma_S > 0 fails'
    # sigma_M < 0 under the margins: alpha_M <= -5k, r beta^T(-A)^{-1}beta <= 2rT^2/u <= 2k/C1
    k, T, C1, r = F(1), F(4), F(100), F(1, 1000)
    u = C1*r*T*(1 + T/k)
    if not (2*r*T*T/u <= 2*k/C1 and -5*k + 2*k/C1 < 0):
        return False, 'sigma_M margin'
    # Step 4, second layer: A_M with a positive eigenvalue => K_M has a positive eigenvalue => F_d(K_M) = 0
    layer2 = 0
    for A in ([[F(-2), F(0)], [F(0), F(1, 50)]], [[F(-3), F(1)], [F(1), F(1, 10)]], [[F(-3), F(1), F(0)], [F(1), F(1, 20), F(1, 2)], [F(0), F(1, 2), F(-4)]]):
        m = len(A)
        if inertia(A)[2] == 0:
            return False, 'test matrix has no positive eigenvalue'
        for alpha in (F(-5), F(-1, 10)):
            for s_ in (F(1, 2), F(1, 10)):
                beta = [F(1)]*m
                n = m + 1
                K = [[F(0)]*n for _ in range(n)]
                K[0][0] = alpha
                for i in range(m):
                    K[0][i+1] = K[i+1][0] = s_*beta[i]
                    for j in range(m):
                        K[i+1][j+1] = A[i][j]
                if inertia(K)[2] == 0:               # K negative semidefinite would give index d
                    return False, 'K_M negative definite although A_M has a positive eigenvalue'
                layer2 += 1
    # Step 4, third layer: |det A| <= |lambda_max(A)| ||A||_op^(m-1) when lambda_max is the eigenvalue of least modulus:
    # diagonal examples, exact
    for diag in ([F(-3), F(-1, 100)], [F(-5), F(-2), F(1, 1000)], [F(-4), F(-3), F(-1, 10)]):
        A = [[F(0)]*len(diag) for _ in diag]
        for i, dv in enumerate(diag):
            A[i][i] = dv
        lam_max = max(diag)
        opnorm = max(abs(v) for v in diag)
        if not (abs(det(A)) <= abs(lam_max)*opnorm**(len(diag) - 1)):
            return False, 'layer determinant bound'
    return True, {'cases': cases, 'positive_eigenvalue_cases': layer2}


# ---------------------------------------------------------------------------------------------------- E4
class Mono:
    def __init__(self, ell=F(0), k=F(0), r0=F(0)):
        self.e = (F(ell), F(k), F(r0))
    def __mul__(self, o):
        return Mono(*[a + b for a, b in zip(self.e, o.e)])
    def __pow__(self, p):
        p = F(p); return Mono(*[a*p for a in self.e])


def check_E4(mutant):
    ell, k, r0 = Mono(1, 0, 0), Mono(0, 1, 0), Mono(0, 0, 1)
    r = (ell*k**(-1))**F(1, 3)
    a = ell*r0**(-3)
    kappa = ell**F(1, 4)
    rr = Mono(0, 0, 1)                                    # a separation variable, reusing the third slot
    claims = {
        'r^-2 (ell/r^3)^2 = ell^2 r^-8': (((rr**(-2))*(ell*rr**(-3))**2).e, (F(2), F(0), F(-8))),
        'k^-2/3 r^2': ((k**F(-2, 3)*r**2).e, (F(2, 3), F(-4, 3), F(0))),
        'k^-2/3 r^3/k': ((k**F(-2, 3)*r**3*k**(-1)).e, (F(1), F(-8, 3), F(0))),
        'ell^2/3 a^-1/3': (((ell**F(2, 3))*a**F(-1, 3)).e, (F(1, 3), F(0), F(1))),
        'ell kappa^-5/3': ((ell*kappa**F(-5, 3)).e, (F(7, 12), F(0), F(0))),
        'kappa^7/3': ((kappa**F(7, 3)).e, (F(7, 12), F(0), F(0))),
        'a^7/3 ell^-1/3': ((a**F(7, 3)*ell**F(-1, 3)).e, (F(2), F(0), F(-7))),
    }
    for name, (got, want) in claims.items():
        if got != want:
            return False, 'monomial claim fails: %s got %s' % (name, got)
    # absolute loss exponent: ell^(7/12) scaled -> ell^(7/12 - 1/3) = ell^(1/4)
    loss = F(7, 12) - F(1, 3)
    if mutant == 'M3':
        loss = F(1, 3)
    if loss != F(1, 4):
        return False, 'loss exponent'
    # r <= k  <=>  ell <= k^4, with r = (ell/k)^(1/3) computed exactly where ell/k is a rational cube
    for (K, rv) in ((F(1, 10), F(1, 10)), (F(1, 10), F(1, 5)), (F(1, 2), F(1, 4)), (F(1, 16), F(1, 8))):
        L = K*rv**3                                        # ell = k r^3, so r = (ell/k)^(1/3) exactly
        if (rv <= K) != (L <= K**4):
            return False, 'threshold r <= k <=> ell <= k^4 fails'
    return True, {name: [str(x) for x in got] for name, (got, want) in claims.items()}


# ---------------------------------------------------------------------------------------------------- E5
def check_E5(mutant):
    for (k, T, C1, r) in ((F(1, 3), F(5), F(50), F(1, 100)), (F(4), F(2), F(10), F(1, 7)), (F(1, 100), F(30), F(1000), F(1, 10**6))):
        u = C1*r*T*(1 + T/k)
        if k*k*u*u != C1*C1*r*r*T*T*(k + T)**2:
            return False, 'k^2 u^2 identity'
        if not (r*T*T <= k*u/C1):
            return False, 'rT^2 <= ku/C1'
    return True, {'identity': 'k^2 u^2 = C1^2 r^2 T^2 (k+T)^2', 'inequality': 'r T^2 <= k u / C1'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    mutant = args.mutant
    if mutant is not None and mutant not in ('M1', 'M2', 'M3'):
        sys.stderr.write('unknown mutant label\n'); sys.exit(2)
    results = {}
    ok_all = True
    for name, fn in (('E1_axial_pins_quintic', check_E1), ('E2_parity_pinned_quintic_2d', check_E2), ('E3_block_and_inertia', check_E3),
                     ('E4_ledger', check_E4), ('E5_layer_algebra', check_E5)):
        ok, info = fn(mutant)
        results[name] = {'passed': bool(ok), 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-D2-REMAINDER-VANISHING-20260930-v1', 'scientific_effect': 'NONE', 'passed': ok_all, 'checks': results}
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
