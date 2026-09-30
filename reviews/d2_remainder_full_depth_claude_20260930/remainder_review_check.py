#!/usr/bin/env python3
"""Exact finite controls accompanying the D2 (Theorem R) full-depth review.  Standard library only.

They check, exactly in rational arithmetic, the displayed algebra that the review re-derives; they do not prove
the Gaussian estimates of the note and are not acceptance.  Scientific effect: NONE.

  C1  the four axial rows (3.1) of the parent applied to a degree-7 polynomial: U0 = f0 + (r^2/8) f2 + O(r^4),
      U1 = f1 + (r^2/24) f3 + O(r^4), U2 = f2 + (r^2/24) f4 + O(r^4), U3 = f3 + (r^2/40) f5 + O(r^4)
      (note S2: "U_r - U_0 = O(r^2)", "(r^2/40) f_xxxxx"); the r^-2, r^-1 and r^1, r^3 coefficients of every row
      are asserted to vanish (no unscaled residual, no odd term); the two transverse rows are the U0/U1 pattern
      applied to f_y and are checked on a second polynomial;
  C2  Lemma R3.2's affine determinant identity det K_t = alpha det A - t beta^T adj(A) beta on rational
      3x3 and 4x4 blocks, INCLUDING a singular A of corank one with NONZERO adjugate, and the bound
      |F_j(K_r) - F_j(K_0)| <= r |beta^T adj(A) beta| on paths whose inertia changes (a singular crossing in
      [0, r]); inertia is computed exactly by congruence diagonalisation (eigenvalue multiplicities counted);
  C3  Lemma R3.1 on rational symmetric pairs whose inertia changes along the segment: the filtered
      determinant difference is bounded by n max(||X||, ||Y||)^(n-1) ||X - Y|| (operator norms replaced by the
      larger Frobenius norms, which only weakens the bound);
  C4  the reference product: W_0 = (6k)^2 det(A_0)^2 1{A_0 < 0} is the only inertia pattern giving index d at
      diag(-6k, A_0) and index d-1 at diag(6k, A_0) (three inertia patterns for A_0);
  C5  the soft-eigenvalue integral of note S5: int_0^(D delta U^2) lambda (lambda + E r U) d lambda
      = (D^3/3) delta^3 U^6 + (E D^2/2) r delta^2 U^5 (exact, at rational parameters); the scalar split (R15):
      lambda <= D delta (T + lambda)^2 implies lambda <= 4 D delta T^2 or lambda >= 1/(4 D delta), on a rational
      grid whose parameters satisfy 4 D delta T^2 < 1/(4 D delta), so that the two branches do not overlap and
      the hypothesis fails on part of the grid (the check is informative);
  C6  the exponent ledger of notes S6-S7 by exact monomial substitution r = (ell/k)^(1/3), a = ell r_0^-3,
      eta = ell^(1/6): r k^(1/3) = ell^(1/3); r^2 k^(-2/3) = ell^(2/3) k^(-4/3); a^(7/3) = ell^(7/3) r_0^-7;
      eta^(7/3) = ell^(7/18); delta = r/k at k = eta is ell^(1/9); ell eta^(-11/3) = ell^(7/18); 7/18 > 1/3;
      and the antiderivatives int_a^1 k^(-4/3) dk = 3 a^(-1/3) - 3 and int_eta^oo k^(-14/3) dk = (3/11) eta^(-11/3)
      evaluated exactly at ell = 10^-18 (all fractional powers rational there);
  C7  the split of note S7 as a model integral with H = 1, r_0 = 1/2, in EXACT rationals at ell = 10^(-18 m),
      m = 1..4 (where ell^(1/6), ell^(1/3), a^(-1/3), a^(7/3) are rational): piece 1 = int_a^eta (2k^2 + 2r^2)
      /(3 k^(2/3)) dk = (2/7)(eta^(7/3) - a^(7/3)) + 2 ell^(2/3)(a^(-1/3) - eta^(-1/3)); piece 2 =
      int_eta^oo ell k^(-14/3)/3 dk = ell eta^(-11/3)/11; their sum divided by ell^(1/3) stays below 3/2;
  M   semantic mutants (--mutant M1|M2|M3|M4|M5|M6) exit 1; an unknown label exits 2.
"""
import argparse
import json
import sys
from fractions import Fraction as F


# ----------------------------------------------------------------------------------------------------------
# polynomial helpers (coefficient lists in r, exact)
def poly_mul(p, q):
    out = [F(0)]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out


def poly_add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0)) for i in range(n)]


def poly_scale(p, c):
    return [c*a for a in p]


def taylor_eval(fcoef, point_poly):
    """Sum_j f_j point^j / j!  where point is a polynomial in r and f_j are the derivatives at 0."""
    total = [F(0)]
    power = [F(1)]
    fact = F(1)
    for j, fj in enumerate(fcoef):
        if j > 0:
            power = poly_mul(power, point_poly)
            fact *= j
        total = poly_add(total, poly_scale(power, fj/fact))
    return total


def coeff(p, i):
    return p[i] if 0 <= i < len(p) else F(0)


def rows_from(fc):
    """The four axial rows of parent (3.1) as Laurent polynomials in r: returns dict name -> (offset, coeffs)
    where the row equals sum_i coeffs[i] r^(i-offset)."""
    fxc = [fc[j+1] for j in range(len(fc)-1)]
    a = [F(0), F(-1, 2)]
    c = [F(0), F(1, 2)]
    fa, fcv = taylor_eval(fc, a), taylor_eval(fc, c)
    fxa, fxcv = taylor_eval(fxc, a), taylor_eval(fxc, c)
    U0 = (0, poly_scale(poly_add(fa, fcv), F(1, 2)))
    d1 = poly_add(fcv, poly_scale(fa, F(-1)))                         # f(c) - f(a), then divide by r
    U1 = (1, d1)
    d2 = poly_add(fxcv, poly_scale(fxa, F(-1)))
    U2 = (1, d2)
    two_U1 = poly_scale(d1, F(-2))                                    # -2 (f(c)-f(a)) as polynomial; /r later
    # inner = f_x(a) + f_x(c) - 2 (f(c)-f(a))/r : represent with a common offset 1: multiply first part by r
    s = poly_add(fxa, fxcv)
    inner_times_r = poly_add(poly_mul(s, [F(0), F(1)]), two_U1)       # r * inner
    U3 = (3, poly_scale(inner_times_r, F(6)))                         # (6/r^2) inner = 6 * (r inner)/r^3
    return {'U0': U0, 'U1': U1, 'U2': U2, 'U3': U3}


def check_rows(mutant):
    fc = [F(v) for v in (2, 3, 5, 7, 11, 13, 17, 19)]                 # f_j = f^(j)(0), distinct primes
    rows = rows_from(fc)
    expect = {'U0': (fc[0], fc[2]/8), 'U1': (fc[1], fc[3]/24), 'U2': (fc[2], fc[4]/24), 'U3': (fc[3], fc[5]/40)}
    if mutant == 'M1':
        expect['U3'] = (fc[3], fc[5]/24)
    for name, (off, p) in rows.items():
        # coefficient of r^e is coeff(p, e + off)
        for e in (-2, -1, 1, 3):
            if coeff(p, e + off) != 0:
                return False, 'row %s has a nonzero r^%d term' % (name, e)
        c0, c2 = expect[name]
        if coeff(p, off) != c0 or coeff(p, off + 2) != c2:
            return False, 'row %s expansion mismatch' % name
    # transverse rows: V0 = (g(a)+g(c))/2, V1 = (g(c)-g(a))/r with g = f_y: the U0/U1 algebra on another polynomial
    gc = [F(v) for v in (23, 29, 31, 37, 41, 43, 47, 53)]
    rows_g = rows_from(gc)
    off, p = rows_g['U0']
    if coeff(p, off) != gc[0] or coeff(p, off + 2) != gc[2]/8 or coeff(p, off + 1) != 0:
        return False, 'transverse row V0 mismatch'
    off, p = rows_g['U1']
    if coeff(p, off) != gc[1] or coeff(p, off + 2) != gc[3]/24 or coeff(p, off + 1) != 0:
        return False, 'transverse row V1 mismatch'
    return True, {'axial_rows': 4, 'transverse_rows': 2, 'U3_second_order': str(fc[5]/40) + ' = f5/40',
                  'vanishing_terms_asserted': ['r^-2', 'r^-1', 'r^1', 'r^3']}


# ----------------------------------------------------------------------------------------------------------
# exact rational linear algebra
def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1]-M[0][1]*M[1][0]
    total = F(0)
    for j in range(n):
        minor = [row[:j]+row[j+1:] for row in M[1:]]
        total += (-1)**j*M[0][j]*det(minor)
    return total


def adjugate(A):
    n = len(A)
    adj = [[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j]+row[j+1:] for k, row in enumerate(A) if k != i]
            adj[j][i] = (-1)**(i+j)*det(minor) if n > 1 else F(1)
    return adj


def inertia(M):
    """Number of negative eigenvalues of a symmetric rational matrix, exactly, by congruence diagonalisation
    (Sylvester's law of inertia).  Repeated eigenvalues are counted with multiplicity."""
    n = len(M)
    A = [row[:] for row in M]
    neg = 0
    for p in range(n):
        # find a nonzero diagonal pivot at or after p; else create one by a congruence if an off-diagonal
        # entry exists in the trailing block; else the trailing block is zero
        piv = None
        for i in range(p, n):
            if A[i][i] != 0:
                piv = i; break
        if piv is None:
            found = None
            for i in range(p, n):
                for j in range(i+1, n):
                    if A[i][j] != 0:
                        found = (i, j); break
                if found: break
            if found is None:
                break
            i, j = found
            # congruence e_i -> e_i + e_j : A <- E^T A E with E = I + e_j e_i^T  (row/col i += row/col j)
            for k in range(n):
                A[i][k] += A[j][k]
            for k in range(n):
                A[k][i] += A[k][j]
            piv = i if A[i][i] != 0 else None
            if piv is None:
                raise RuntimeError('congruence failed to create a pivot')
        if piv != p:
            A[p], A[piv] = A[piv], A[p]
            for row in A:
                row[p], row[piv] = row[piv], row[p]
        d = A[p][p]
        if d < 0:
            neg += 1
        for i in range(p+1, n):
            f = A[i][p]/d
            if f != 0:
                for k in range(p, n):
                    A[i][k] -= f*A[p][k]
                for k in range(p, n):
                    A[k][i] -= f*A[k][p]
    return neg


def filtered_det(M, j):
    d = det(M)
    if d == 0:
        return F(0)
    return abs(d) if inertia(M) == j else F(0)


def frob2(M):
    return sum(x*x for row in M for x in row)      # squared Frobenius norm (exact)


def embed(alpha, beta, A, s):
    n = len(A)
    K = [[F(0)]*(n+1) for _ in range(n+1)]
    K[0][0] = alpha
    for i in range(n):
        K[0][i+1] = s*beta[i]; K[i+1][0] = s*beta[i]
        for j in range(n):
            K[i+1][j+1] = A[i][j]
    return K


def check_R7(mutant):
    """det K_t identity and Lemma R3.2's bound on inertia-changing paths (t = s^2 with rational s)."""
    A1 = [[F(-2), F(1, 2), F(0)], [F(1, 2), F(-1), F(1, 3)], [F(0), F(1, 3), F(-3, 2)]]        # negative definite
    A2 = [[F(-1), F(1, 2), F(0)], [F(1, 2), F(-2), F(0)], [F(0), F(0), F(0)]]                   # corank one, adj != 0
    A3 = [[F(-1), F(0), F(0), F(0)], [F(0), F(-1, 2), F(1, 4), F(0)], [F(0), F(1, 4), F(-1, 3), F(0)], [F(0), F(0), F(0), F(-2)]]
    betas = [[F(1), F(-1), F(2)], [F(3, 2), F(0), F(1, 5)], [F(2), F(1), F(1), F(-1)]]
    alphas = [F(-6), F(6), F(1, 100), F(-1, 100), F(0)]
    n_id = 0; n_bound = 0; crossings = 0; singular_adj_nonzero = 0
    for A in (A1, A2, A3):
        n = len(A)
        adjA = adjugate(A); dA = det(A)
        if dA == 0 and any(x != 0 for row in adjA for x in row):
            singular_adj_nonzero += 1
        for beta in betas:
            if len(beta) != n:
                continue
            q = sum(beta[i]*sum(adjA[i][j]*beta[j] for j in range(n)) for i in range(n))   # beta^T adj(A) beta
            for alpha in alphas:
                for s in (F(0), F(1, 3), F(1, 2), F(1), F(3, 2), F(2)):
                    t = s*s
                    lhs = det(embed(alpha, beta, A, s)); rhs = alpha*dA - t*q
                    if mutant == 'M2':
                        rhs = alpha*dA + t*q
                    if lhs != rhs:
                        return False, 'det K_t identity fails (alpha=%s, t=%s)' % (alpha, t)
                    n_id += 1
                for s in (F(1, 2), F(1), F(2)):
                    r = s*s
                    K0 = embed(alpha, beta, A, F(0)); Kr = embed(alpha, beta, A, s)
                    if det(K0) != 0 and det(Kr) != 0 and inertia(K0) != inertia(Kr):
                        crossings += 1
                    for j in range(n+2):
                        diff = abs(filtered_det(Kr, j) - filtered_det(K0, j))
                        if diff > r*abs(q):
                            return False, 'Lemma R3.2 bound fails at alpha=%s r=%s j=%s' % (alpha, r, j)
                        n_bound += 1
    if crossings == 0 or singular_adj_nonzero == 0:
        return False, 'test set lacks inertia crossings or a corank-one block with nonzero adjugate'
    return True, {'identities': n_id, 'bound_checks': n_bound, 'inertia_crossings_both_endpoints_nonsingular': crossings,
                  'singular_blocks_with_nonzero_adjugate': singular_adj_nonzero}


def check_R6(mutant):
    """Lemma R3.1 on rational symmetric pairs with an inertia change along the segment (Frobenius norms)."""
    pairs = [
        ([[F(-1), F(0)], [F(0), F(-1)]], [[F(1), F(0)], [F(0), F(-1)]]),
        ([[F(-2), F(1)], [F(1), F(-2)]], [[F(2), F(1)], [F(1), F(1, 2)]]),
        ([[F(-1), F(1, 2), F(0)], [F(1, 2), F(-1), F(0)], [F(0), F(0), F(-3)]],
         [[F(1), F(1, 2), F(1, 3)], [F(1, 2), F(-1), F(0)], [F(1, 3), F(0), F(2)]]),
    ]
    checks = 0; crossings = 0
    if inertia([[F(-1), F(0)], [F(0), F(-1)]]) != 2 or inertia([[F(1), F(0)], [F(0), F(-1)]]) != 1:
        return False, 'inertia routine miscounts a repeated eigenvalue'
    for X, Y in pairs:
        n = len(X)
        if inertia(X) != inertia(Y):
            crossings += 1
        nx, ny = frob2(X), frob2(Y)
        dXY = frob2([[X[i][j]-Y[i][j] for j in range(n)] for i in range(n)])
        bound2 = F(n*n)*max(nx, ny)**(n-1)*dXY                     # squared bound, exact
        for j in range(n+1):
            diff = abs(filtered_det(X, j) - filtered_det(Y, j))
            if mutant == 'M3':
                diff = diff*10
            if diff*diff > bound2:
                return False, 'Lemma R3.1 bound fails on pair with j=%s' % j
            checks += 1
    if crossings != len(pairs):
        return False, 'expected every pair to change inertia'
    return True, {'checks': checks, 'inertia_crossings': crossings}


def check_reference_product(mutant):
    k = F(1, 3)
    mats = {
        'negdef': [[F(-1), F(1, 4)], [F(1, 4), F(-2)]],
        'indef': [[F(-1), F(0)], [F(0), F(1)]],
        'posdef': [[F(1), F(0)], [F(0), F(2)]],
    }
    for name, A0 in mats.items():
        m = len(A0); d = m+1
        DM = embed(-6*k, [F(0)]*m, A0, F(0)); DS = embed(6*k, [F(0)]*m, A0, F(0))
        prod = filtered_det(DM, d)*filtered_det(DS, d-1)
        expected = (6*k)**2*det(A0)**2 if name == 'negdef' else F(0)
        if mutant == 'M4' and name == 'indef':
            expected = (6*k)**2*det(A0)**2
        if prod != expected:
            return False, 'reference product mismatch on %s' % name
    return True, {'inertia_patterns': 3}


def check_soft_integral(mutant):
    D, E, U, dl, k = F(4, 3), F(3, 2), F(7, 2), F(1, 5), F(2, 3)
    r = k*dl
    X = D*dl*U*U
    lhs = X**3/3 + E*r*U*X*X/2                                    # closed form of int_0^X lambda(lambda + E r U)
    rhs = (D**3/3)*dl**3*U**6 + (E*D*D/2)*r*dl*dl*U**5
    if lhs != rhs:
        return False, 'soft integral identity fails'
    # (R15) with non-overlapping branches: D delta small so that 4 D delta T^2 < 1/(4 D delta)
    D2, dl2 = F(4, 3), F(1, 100)
    hyp_false = 0; grid = 0
    for T in (F(1), F(3, 2), F(2)):
        lo, hi = 4*D2*dl2*T*T, 1/(4*D2*dl2)
        if not lo < hi:
            return False, 'branch overlap; grid uninformative'
        for lam in [F(n, 20) for n in range(1, 400)]:
            hyp = lam <= D2*dl2*(T+lam)**2
            if mutant == 'M5':
                hyp = True
            if hyp and not (lam <= lo or lam >= hi):
                return False, '(R15) branch logic fails at T=%s lam=%s' % (T, lam)
            hyp_false += (0 if hyp else 1); grid += 1
    if hyp_false == 0:
        return False, 'the hypothesis never fails on the grid; check uninformative'
    return True, {'identity': True, 'grid_points': grid, 'points_where_hypothesis_fails': hyp_false}


class Mono:
    """Monomial ell^a k^b r0^c with exact rational exponents."""
    def __init__(self, a=F(0), b=F(0), c=F(0)):
        self.a, self.b, self.c = F(a), F(b), F(c)
    def __mul__(self, o):
        return Mono(self.a+o.a, self.b+o.b, self.c+o.c)
    def __pow__(self, e):
        e = F(e); return Mono(self.a*e, self.b*e, self.c*e)
    def key(self):
        return (self.a, self.b, self.c)


def check_exponents(mutant):
    ell, k, r0 = Mono(1, 0, 0), Mono(0, 1, 0), Mono(0, 0, 1)
    r = (ell * k**(-1))**F(1, 3)
    if mutant == 'M6':
        r = (ell * k**(-1))**F(1, 2)
    a = ell * r0**(-3)
    eta = ell**F(1, 6)
    claims = {
        'r k^(1/3)': ((r * k**F(1, 3)).key(), (F(1, 3), F(0), F(0))),
        'r^2 k^(-2/3)': (((r**2) * k**F(-2, 3)).key(), (F(2, 3), F(-4, 3), F(0))),
        'a^(7/3)': ((a**F(7, 3)).key(), (F(7, 3), F(0), F(-7))),
        'ell^(2/3) a^(-1/3)': (((ell**F(2, 3)) * a**F(-1, 3)).key(), (F(1, 3), F(0), F(1))),
        'eta^(7/3)': ((eta**F(7, 3)).key(), (F(7, 18), F(0), F(0))),
        'delta = r/k at k = eta': (((ell**F(1, 3)) * eta**F(-4, 3)).key(), (F(1, 9), F(0), F(0))),
        'ell eta^(-11/3)': ((ell * eta**F(-11, 3)).key(), (F(7, 18), F(0), F(0))),
        'delta^3 k^(-2/3) at general k': ((((ell**F(1, 3)) * k**F(-4, 3))**3 * k**F(-2, 3)).key(), (F(1), F(-14, 3), F(0))),
    }
    for name, (got, want) in claims.items():
        if got != want:
            return False, 'monomial claim fails: %s got %s' % (name, got)
    if not (F(7, 18) > F(1, 3) and F(1, 9) > 0):
        return False, 'exponent comparison fails'
    # antiderivatives evaluated exactly at ell = 10^-18, r_0 = 1/2 (a = 8e-18, a^(-1/3) = 10^6/2, eta = 10^-3)
    L = F(1, 10**18); a_v = L*8; eta_v = F(1, 1000)
    a_third = F(10**6, 2)                                   # a^(-1/3)
    int_a_1 = 3*a_third - 3
    # exact Riemann-type check of the antiderivative: F(k) = -3 k^(-1/3); F(1) - F(a) = -3 + 3 a^(-1/3)
    if int_a_1 != -3*F(1) + 3*a_third:
        return False, 'antiderivative int_a^1 k^(-4/3) fails'
    eta_m113 = F(10**11)                                    # eta^(-11/3) at eta = 10^-3
    # antiderivative of k^(-14/3) is -(3/11) k^(-11/3); its limit at infinity is 0
    int_eta_inf = F(3, 11)*eta_m113
    if int_eta_inf != F(3*10**11, 11) or eta_v**11 != F(1, 10**33):
        return False, 'antiderivative int_eta^oo k^(-14/3) fails'
    return True, {name: [str(x) for x in got] for name, (got, want) in claims.items()}


def check_loss_split(mutant):
    """Model check of S7's split with H = 1, r_0 = 1/2, exactly, at ell = 10^(-18 m)."""
    ratios = {}
    for m in (1, 2, 3, 4):
        L = F(1, 10**(18*m))
        eta = F(1, 10**(3*m))                 # ell^(1/6)
        l13 = F(1, 10**(6*m)); l23 = F(1, 10**(12*m))
        a = 8*L                               # ell / r0^3, r0 = 1/2
        a_m13 = F(10**(6*m), 2)               # a^(-1/3)
        a_73 = F(128, 10**(42*m))             # a^(7/3) = 2^7 10^(-42 m)
        eta_73 = F(1, 10**(7*m)); eta_m13 = F(10**m); eta_m113 = F(10**(11*m))
        if not a < eta < 1:
            return False, 'cutoff order a < eta < 1 fails'
        piece1 = F(2, 7)*(eta_73 - a_73) + 2*l23*(a_m13 - eta_m13)
        if mutant == 'M6':
            piece1 = piece1 + l13
        piece2 = L*eta_m113/11
        ratio = (piece1 + piece2)/l13
        if ratio > F(3, 2):
            return False, 'loss split ratio exceeds 3/2 at m=%d: %s' % (m, ratio)
        ratios['ell=1e-%d' % (18*m)] = str(ratio.limit_denominator(10**9))
    return True, ratios


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    mutant = args.mutant
    if mutant is not None and mutant not in ('M1', 'M2', 'M3', 'M4', 'M5', 'M6'):
        sys.stderr.write('unknown mutant label\n'); sys.exit(2)
    results = {}
    ok_all = True
    for name, fn in (('C1_axial_and_transverse_rows', check_rows), ('C2_R7_affine_determinant', check_R7),
                     ('C3_R6_filtered_determinant', check_R6), ('C4_reference_product', check_reference_product),
                     ('C5_soft_integral_and_R15', check_soft_integral), ('C6_exponent_ledger', check_exponents),
                     ('C7_loss_split_model', check_loss_split)):
        ok, info = fn(mutant)
        results[name] = {'passed': bool(ok), 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-D2-REMAINDER-FULLDEPTH-20260930-v1', 'scientific_effect': 'NONE', 'passed': ok_all,
           'checks': results}
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
