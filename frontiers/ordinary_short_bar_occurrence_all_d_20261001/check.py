"""Exact rational controls for C52-ALL-D (NOTE.md section 6).  Standard library only.

These check the finite identities that the general-d proof uses; they do not prove the continuum statements.

  1. pin_transform: the exact contact transformation T_r of [P] (3.1) in dimension d, |det T_r| = 12 r^-(d+3), and the
     image of the physical pin values is the target v_r of [P] (3.3).
  2. ridge_jets: for a polynomial F in (x, y_1..y_m) with grad_y F(0) = 0 and D_y^2 F(0) invertible, the transverse
     critical curve psi(x) is computed as an exact power series; g(x) = F(x, psi(x)) then satisfies
         g'(0) = F_x(0),   g''(0) = F_xx - F_xy^T (D_y^2 F)^-1 F_xy   (Schur complement),
         g'''(0) = D^3 F(0)[v, v, v],   v = (1, psi'(0)).                                   (N4), (N5)
  3. inertia: a symmetric matrix whose transverse block is negative definite has m negative eigenvalues plus the sign
     of its Schur complement (Sylvester, exact LDL^T).                                                (N6)
  4. mesh_counts: parameter and range dimensions of the three overdetermined maps of (N8), with p - q = 1.
  5. hv_rank: H -> H v from symmetric d x d matrices onto R^d has rank d for v != 0 (the symbol step of (N7)).
  6. ledger: spatial (d-1) + height 3 - pin (d+3) + determinant 2 = 1, and the lifetime Jacobian
     r dr = tau^(2/3) y^(-1/3) dy / (3 k^(2/3)) at exact cubes.

    python3 -B -S check.py"""
from fractions import Fraction as Fr
from itertools import product
import random
import sys


# ---------------------------------------------------------------------------------------------- linear algebra
def det(M):
    A = [[Fr(v) for v in row] for row in M]
    n, s = len(A), Fr(1)
    for i in range(n):
        p = next((j for j in range(i, n) if A[j][i] != 0), None)
        if p is None:
            return Fr(0)
        if p != i:
            A[i], A[p] = A[p], A[i]
            s = -s
        s *= A[i][i]
        for j in range(i + 1, n):
            f = A[j][i] / A[i][i]
            if f:
                A[j] = [a - f * b for a, b in zip(A[j], A[i])]
    return s


def rank(M):
    A = [[Fr(v) for v in row] for row in M]
    rk, cols = 0, len(A[0]) if A else 0
    for c in range(cols):
        p = next((j for j in range(rk, len(A)) if A[j][c] != 0), None)
        if p is None:
            continue
        A[rk], A[p] = A[p], A[rk]
        for j in range(len(A)):
            if j != rk and A[j][c]:
                f = A[j][c] / A[rk][c]
                A[j] = [a - f * b for a, b in zip(A[j], A[rk])]
        rk += 1
    return rk


def solve(M, b):
    n = len(M)
    A = [[Fr(v) for v in M[i]] + [Fr(b[i])] for i in range(n)]
    for i in range(n):
        p = next(j for j in range(i, n) if A[j][i] != 0)
        A[i], A[p] = A[p], A[i]
        for j in range(n):
            if j != i and A[j][i]:
                f = A[j][i] / A[i][i]
                A[j] = [a - f * c for a, c in zip(A[j], A[i])]
    return [A[i][n] / A[i][i] for i in range(n)]


def inertia(S):
    """(negatives, zeros, positives) of a symmetric rational matrix, by exact symmetric elimination with pivoting on
    the diagonal where possible (Sylvester's law of inertia)"""
    A = [[Fr(v) for v in row] for row in S]
    neg = zer = pos = 0
    while A:
        n = len(A)
        i = next((j for j in range(n) if A[j][j] != 0), None)
        if i is None:
            j = next(((a, b) for a in range(n) for b in range(n) if A[a][b] != 0), None)
            if j is None:
                zer += n
                break
            a, b = j                                   # congruence e_a -> e_a + e_b makes a diagonal entry nonzero
            for c in range(n):
                A[a][c] += A[b][c]
            for c in range(n):
                A[c][a] += A[c][b]
            continue
        p = A[i][i]
        neg, pos = neg + (p < 0), pos + (p > 0)
        rest = [j for j in range(n) if j != i]
        A = [[A[r][c] - A[r][i] * A[i][c] / p for c in rest] for r in rest]
    return neg, zer, pos


# ---------------------------------------------------------------------------------------------- 1. pin transform
def pin_transform(d, r):
    """rows of T_r acting on O_r = (f(a), f_x(a), f(c), f_x(c), f_y1(a), f_y1(c), ..., f_ym(a), f_ym(c))"""
    r = Fr(r)
    m = d - 1
    n = 4 + 2 * m
    T = [[Fr(0)] * n for _ in range(n)]
    T[0][0] = T[0][2] = Fr(1, 2)                               # (f(a) + f(c))/2
    T[1][0], T[1][2] = -1 / r, 1 / r                           # (f(c) - f(a))/r
    T[2][1], T[2][3] = -1 / r, 1 / r                           # (f_x(c) - f_x(a))/r
    s = 6 / r ** 2                                             # (6/r^2)[f_x(a) + f_x(c) - 2(f(c) - f(a))/r]
    T[3][1] = T[3][3] = s
    T[3][0], T[3][2] = 2 * s / r, -2 * s / r
    for j in range(m):
        ia, ic = 4 + 2 * j, 5 + 2 * j
        T[ia][ia] = T[ia][ic] = Fr(1, 2)
        T[ic][ia], T[ic][ic] = -1 / r, 1 / r
    return T


def pin_target(d, r, b, k):
    r, b, k = Fr(r), Fr(b), Fr(k)
    O = [b, Fr(0), b - k * r ** 3, Fr(0)] + [Fr(0)] * (2 * (d - 1))
    T = pin_transform(d, r)
    return [sum(t * o for t, o in zip(row, O)) for row in T]


def expected_target(d, r, b, k):
    r, b, k = Fr(r), Fr(b), Fr(k)
    return [b - k * r ** 3 / 2, -k * r ** 2, Fr(0), 12 * k] + [Fr(0)] * (2 * (d - 1))


def det_constant(d):
    return 12


def det_exponent(d):
    return d + 3


# ---------------------------------------------------------------------------------------------- 2. ridge jets
NS = 4                                                         # series kept mod x^NS


def s_mul(a, b):
    out = [Fr(0)] * NS
    for i, u in enumerate(a):
        if u:
            for j in range(NS - i):
                out[i + j] += u * b[j]
    return out


def s_pow(a, e):
    out = [Fr(1)] + [Fr(0)] * (NS - 1)
    for _ in range(e):
        out = s_mul(out, a)
    return out


def poly_eval_series(F, xs, ys):
    """F: dict exponent tuple (ex, ey_1..ey_m) -> coeff; xs, ys: series"""
    out = [Fr(0)] * NS
    for e, c in F.items():
        t = s_pow(xs, e[0])
        for yj, ej in zip(ys, e[1:]):
            t = s_mul(t, s_pow(yj, ej))
        out = [o + c * v for o, v in zip(out, t)]
    return out


def poly_deriv(F, i):
    out = {}
    for e, c in F.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            out[tuple(f)] = out.get(tuple(f), 0) + c * e[i]
    return out


def poly_at0(F):
    return Fr(F.get(tuple([0] * len(next(iter(F)))), 0)) if F else Fr(0)


def ridge_series(F, m):
    """psi(x) as series with grad_y F(x, psi(x)) = O(x^NS), psi(0) = 0 (requires grad_y F(0) = 0)"""
    Fy = [poly_deriv(F, 1 + j) for j in range(m)]
    J = [[poly_at0(poly_deriv(Fy[i], 1 + j)) for j in range(m)] for i in range(m)]
    xs = [Fr(0), Fr(1)] + [Fr(0)] * (NS - 2)
    psi = [[Fr(0)] * NS for _ in range(m)]
    for _ in range(NS + 1):                                    # each step fixes one more order (Jacobian error O(x))
        res = [poly_eval_series(Fy[i], xs, psi) for i in range(m)]
        for n in range(NS):
            corr = solve(J, [res[i][n] for i in range(m)])
            for j in range(m):
                psi[j][n] -= corr[j]
    res = [poly_eval_series(Fy[i], xs, psi) for i in range(m)]
    if any(any(v for v in r_) for r_ in res):
        raise ArithmeticError('ridge series did not close')
    return psi


def multilinear0(F, nvar, order, v):
    """D^order F(0)[v,...,v] = order! * sum_{|e| = order} c_e v^e"""
    fact = 1
    for i in range(2, order + 1):
        fact *= i
    tot = Fr(0)
    for e, c in F.items():
        if sum(e) == order:
            t = Fr(c)
            for vi, ei in zip(v, e):
                t *= Fr(vi) ** ei
            tot += t
    return fact * tot


def ridge_jets(F, m):
    psi = ridge_series(F, m)
    xs = [Fr(0), Fr(1)] + [Fr(0)] * (NS - 2)
    g = poly_eval_series(F, xs, psi)
    g1, g2, g3 = g[1], 2 * g[2], 6 * g[3]
    v = [Fr(1)] + [psi[j][1] for j in range(m)]
    Fx = poly_deriv(F, 0)
    Fxx = poly_at0(poly_deriv(Fx, 0))
    Fxy = [poly_at0(poly_deriv(Fx, 1 + j)) for j in range(m)]
    Fyy = [[poly_at0(poly_deriv(poly_deriv(F, 1 + i), 1 + j)) for j in range(m)] for i in range(m)]
    w = solve(Fyy, Fxy)
    schur = Fxx - sum(a * b for a, b in zip(Fxy, w))
    return {'g1': g1, 'g2': g2, 'g3': g3, 'Fx': poly_at0(Fx), 'schur': schur,
            'D2vv': multilinear0(F, m + 1, 2, v), 'D3vvv': multilinear0(F, m + 1, 3, v),
            'psi1': [psi[j][1] for j in range(m)], 'psi1_formula': [-t for t in w],
            'Fxxx': poly_at0(poly_deriv(poly_deriv(Fx, 0), 0))}


def random_ridge_poly(m, rng, contact=False):
    """random rational quartic in (x, y) with grad_y F(0) = 0 and D_y^2 F(0) negative definite; with contact=True also
    F_x(0) = F_xx(0) = 0, F_xy(0) = 0 and F_xxx(0) = 12k: the limiting contact jets (N1)"""
    nvar = m + 1
    F = {}
    for e in product(range(5), repeat=nvar):
        if 1 <= sum(e) <= 4:
            F[e] = Fr(rng.randint(-9, 9), rng.randint(1, 5))
    for j in range(m):
        e = [0] * nvar
        e[1 + j] = 1
        F[tuple(e)] = Fr(0)                                    # F_yj(0) = 0
    # D_y^2 F(0) = -(B B^T + I): coefficients of y_i y_j
    B = [[Fr(rng.randint(-3, 3)) for _ in range(m)] for _ in range(m)]
    N = [[-(sum(B[i][t] * B[j][t] for t in range(m)) + (1 if i == j else 0)) for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(i, m):
            e = [0] * nvar
            e[1 + i] += 1
            e[1 + j] += 1
            F[tuple(e)] = N[i][j] / 2 if i == j else N[i][j]
    if contact:
        k = Fr(rng.randint(1, 7), rng.randint(1, 3))
        F[(1,) + (0,) * m] = Fr(0)
        F[(2,) + (0,) * m] = Fr(0)
        F[(3,) + (0,) * m] = 2 * k                             # F_xxx(0) = 3! * 2k = 12k
        for j in range(m):
            e = [1] + [0] * m
            e[1 + j] = 1
            F[tuple(e)] = Fr(0)
        return F, k
    return F, None


# ---------------------------------------------------------------------------------------------- 4-6
def mesh_counts(d):
    """(parameter dim q, range dim p) for Z_M = (grad F(x), H F(x) v), Z_V = (grad F(x), grad F(z), F(x) - F(z)),
    Z_b = (grad F(x), F(x) - b)"""
    return {'Z_M': (d + (d - 1), 2 * d), 'Z_V': (2 * d, 2 * d + 1), 'Z_b': (d, d + 1)}


def hv_matrix(v):
    """matrix of H -> H v on independent entries H_ij, i <= j"""
    d = len(v)
    cols = [(i, j) for i in range(d) for j in range(i, d)]
    M = [[Fr(0)] * len(cols) for _ in range(d)]
    for c, (i, j) in enumerate(cols):
        M[i][c] += v[j]
        if i != j:
            M[j][c] += v[i]
    return M


def ledger_exponent(d):
    return (d - 1) + 3 - det_exponent(d) + 2


def lifetime_jacobian(tau, y, k):
    """r dr/dy at r = (tau y / k)^(1/3), returned as (r^2 / (3 y), tau^(2/3) y^(-1/3) / (3 k^(2/3))) for exact cubes"""
    def cbrt(q):
        q = Fr(q)
        for a in (q.numerator, q.denominator):
            c = round(abs(a) ** (1 / 3))
            if c ** 3 != abs(a):
                raise ValueError('not a cube')
        return Fr(round(q.numerator ** (1 / 3)), round(q.denominator ** (1 / 3)))
    tau, y, k = Fr(tau), Fr(y), Fr(k)
    r = cbrt(tau * y / k)
    lhs = r * r / (3 * y)                                      # r dr/dy, since dr/dy = r/(3y)
    rhs = cbrt(tau) ** 2 / (cbrt(y) * 3 * cbrt(k) ** 2)
    return lhs, rhs


# ---------------------------------------------------------------------------------------------- run
def run(verbose=True, seed=20261001, dims=(2, 3, 4, 5, 6)):
    rng = random.Random(seed)
    fails = 0

    def report(ok, msg):
        nonlocal fails
        fails += not ok
        if verbose:
            print(('ok    ' if ok else 'FAIL  ') + msg)

    for d in dims:
        for r in (Fr(1, 3), Fr(2, 7), Fr(5, 2)):
            D = det(pin_transform(d, r))
            report(abs(D) == det_constant(d) * r ** -det_exponent(d), 'd=%d r=%s |det T_r| = 12 r^-(d+3)' % (d, r))
            report(pin_target(d, r, Fr(-3, 4), Fr(5, 3)) == expected_target(d, r, Fr(-3, 4), Fr(5, 3)),
                   'd=%d r=%s T_r(pins) = v_r' % (d, r))
    for d in dims:
        m = d - 1
        differs = False
        for t in range(3 if d <= 4 else 1):
            F, _ = random_ridge_poly(m, rng)
            J = ridge_jets(F, m)
            differs = differs or J['g3'] != J['Fxxx']
            report(J['g1'] == J['Fx'] and J['g2'] == J['schur'] == J['D2vv'] and J['g3'] == J['D3vvv']
                   and J['psi1'] == J['psi1_formula'],
                   "d=%d ridge #%d: g' = F_x, g'' = Schur = D2F[v,v], g''' = D3F[v,v,v], psi' = -Fyy^-1 Fxy" % (d, t))
        report(differs, "d=%d falsifier: g''' differs from the raw axial F_xxx off contact" % d)
        F, k = random_ridge_poly(m, rng, contact=True)
        J = ridge_jets(F, m)
        report(J['g1'] == 0 and J['g2'] == 0 and J['g3'] == 12 * k and all(p == 0 for p in J['psi1']),
               "d=%d contact jets (N1): psi'(0) = 0, g'(0) = g''(0) = 0, g'''(0) = 12k" % d)
    for d in dims:
        m = d - 1
        for t in range(4):
            B = [[Fr(rng.randint(-4, 4)) for _ in range(m)] for _ in range(m)]
            Ayy = [[-(sum(B[i][s] * B[j][s] for s in range(m)) + (1 if i == j else 0)) for j in range(m)]
                   for i in range(m)]
            h = [Fr(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(m)]
            w = solve(Ayy, h)
            for target in (Fr(-2), Fr(3)):
                axx = target + sum(a * b for a, b in zip(h, w))   # Schur complement = target
                H = [[axx] + h] + [[h[i]] + Ayy[i] for i in range(m)]
                neg, zer, pos = inertia(H)
                exp = (m + 1, 0, 0) if target < 0 else (m, 0, 1)
                report((neg, zer, pos) == exp, 'd=%d inertia: Schur %s -> %s' % (d, target, exp))
    for d in dims:
        mc = mesh_counts(d)
        report(all(p - q == 1 for q, p in mc.values()), 'd=%d mesh counts %s, p - q = 1' % (d, mc))
        for t in range(3):
            v = [Fr(rng.randint(-3, 3)) for _ in range(d)]
            if not any(v):
                v[0] = Fr(1)
            report(rank(hv_matrix(v)) == d, 'd=%d H -> Hv onto R^d (v = %s)' % (d, [str(x) for x in v]))
        report(ledger_exponent(d) == 1, 'd=%d ledger exponent (d-1)+3-(d+3)+2 = 1' % d)
    report(mesh_counts(2) == {'Z_M': (3, 4), 'Z_V': (4, 5), 'Z_b': (2, 3)}, 'd=2 reduces to C52 (F7)-(F9) counts')
    for tau, y, k in ((Fr(1, 8), Fr(27, 64), Fr(1, 125)), (Fr(8, 27), Fr(1), Fr(64))):
        lhs, rhs = lifetime_jacobian(tau, y, k)
        report(lhs == rhs, 'lifetime Jacobian at tau=%s y=%s k=%s' % (tau, y, k))
    if verbose:
        print('check: %d failures' % fails)
    return fails


if __name__ == '__main__':
    sys.exit(1 if run() else 0)
