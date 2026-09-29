"""Exact finite controls for CL-D5-DIMENSION-LIFT-20260929-v1 (frontiers/d5_dimension_lift_20260929/PROOF.md).

Python standard library only; exact rational arithmetic and exact multivariate Laurent polynomials.

  X   two soft directions: det(H)^2 ||u1^u2||^2 <= ||H u1 ^ H u2||^2 ||H||_F^(2(d-2)) for d = 2, 3, 4;
      equality on a diagonal family with the operator norm; the Cramer coefficient identity a^2 ||e^e'||^2 = ||u^e'||^2
  G   pin-ball gradient frame in d dimensions: the Gram of S -> S beta over independent entries, rank d on the whole
      (alpha, beta) sphere including alpha = 0 and beta = 0, the block-Schur lower bound, and the explicit floor
      det(B_core B_core^T) >= (9/64)^(d-1) / 2048, which is the planar 9/131072 at d = 2
  R   confluent value/gradient rank with degree-five polynomials in d variables (contact rows at the midpoint plus
      value and gradient at a witness): explicit annihilating families with determinants -|v|^(2d+2) and u^(2d+6);
      degree four fails on the axis in every d
  RO  the height row operation in d = 3 on an exactly pinned cubic: no negative power of s, S_0 and C_3 cancel,
      the s^0 part is the displayed mean plus B J
  EU  Euler identity in d = 3: 3[f(X)-f(0)] - X.grad f(X) - 2 grad f(0).X - X^T H_0 X / 2 = -(quartic part of f)
  TB  transverse block determinant: det S = eps det S' - w^T adj(S') w and (w^T adj(S') w)^2 <= |w|^4 (||S'||_F^2)^(m-2)
  N   jet-functional norms: S -> S v has Gram >= |v|^2/2 I; C -> v^T C v / 2 has norm^2 >= |v|^4/4;
      D -> D[v,v,v] / 12 has norm^2 >= |v|^6/144 (all over independent entries)
  L   radius, scale and volume ledgers for d = 2..6: pin region I, pin region II, collar, intermediate shell, the
      Jacobian exponent d+4, the Gram determinant exponent 2d+8, the exact shell inequality and the dyadic sums
  W   the pin weight max(|q|, r|p|)^(2-d): radial exponent zero (integrable), nested-ball count exponent 5

Mutants (each must exit 1): drop-frobenius-order, drop-s0-block, drop-a4-column, degree-four, row-operation-third,
euler-coefficient, adjugate-sign, one-soft-direction, flat-shell, weight-one-less-power.

These checks verify exact identities, ranks, floors and power ledgers. They do not prove the Gaussian, compactness,
regression or Kac-Rice steps, which are argued in PROOF.md.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ['drop-frobenius-order', 'drop-s0-block', 'drop-a4-column', 'degree-four', 'row-operation-third',
           'euler-coefficient', 'adjugate-sign', 'one-soft-direction', 'flat-shell', 'weight-one-less-power']


def require(ok, message):
    if not ok:
        raise AssertionError(message)


# ---------------------------------------------------------------- exact multivariate Laurent polynomials

def _mono_mul(a, b):
    d = dict(a)
    for v, e in b:
        n = d.get(v, 0) + e
        if n:
            d[v] = n
        else:
            d.pop(v, None)
    return tuple(sorted(d.items()))


class P:
    __slots__ = ('t',)

    def __init__(self, t=None):
        self.t = {m: c for m, c in (t or {}).items() if c != 0}

    @staticmethod
    def c(x):
        return P({(): F(x)})

    @staticmethod
    def v(name, e=1):
        return P({((name, e),): F(1)})

    @staticmethod
    def lift(o):
        return o if isinstance(o, P) else P.c(o)

    def __add__(self, o):
        o = P.lift(o)
        t = dict(self.t)
        for m, c in o.t.items():
            t[m] = t.get(m, 0) + c
        return P(t)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.t.items()})

    def __sub__(self, o):
        return self + (-P.lift(o))

    def __rsub__(self, o):
        return P.lift(o) - self

    def __mul__(self, o):
        o = P.lift(o)
        t = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = _mono_mul(m1, m2)
                t[m] = t.get(m, 0) + c1 * c2
        return P(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        r = P.c(1)
        for _ in range(n):
            r = r * self
        return r

    def __eq__(self, o):
        return (self - P.lift(o)).is_zero()

    def is_zero(self):
        return not self.t

    def d(self, name):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.get(name, 0)
            if e == 0:
                continue
            if e == 1:
                dm.pop(name)
            else:
                dm[name] = e - 1
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c * e
        return P(t)

    def subs(self, name, q):
        q = P.lift(q)
        r = P()
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.pop(name, 0)
            if e < 0:
                raise ValueError('negative exponent substitution')
            r = r + P({tuple(sorted(dm.items())): c}) * (q ** e)
        return r

    def coeff(self, name, e):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            if dm.pop(name, 0) == e:
                t[tuple(sorted(dm.items()))] = c
        return P(t)

    def exponents(self, name):
        return sorted({dict(m).get(name, 0) for m in self.t}) if self.t else []

    def const(self):
        if any(m for m in self.t):
            raise ValueError('polynomial is not constant: ' + repr(sorted(self.t)))
        return self.t.get((), F(0))

    def variables(self):
        return sorted({v for m in self.t for v, _ in m})

    def total_degree_terms(self, names):
        out = {}
        for m, c in self.t.items():
            dm = dict(m)
            deg = sum(dm.get(n, 0) for n in names)
            out.setdefault(deg, {})[m] = c
        return {k: P(v) for k, v in out.items()}


# ---------------------------------------------------------------- exact linear algebra

def det(M):
    n = len(M)
    A = [row[:] for row in M]
    sign = F(1)
    for i in range(n):
        p = next((r for r in range(i, n) if A[r][i] != 0), None)
        if p is None:
            return F(0)
        if p != i:
            A[i], A[p] = A[p], A[i]
            sign = -sign
        for r in range(i + 1, n):
            f = A[r][i] / A[i][i]
            if f:
                for c in range(i, n):
                    A[r][c] -= f * A[i][c]
    out = sign
    for i in range(n):
        out *= A[i][i]
    return out


def rank(M):
    A = [row[:] for row in M]
    if not A:
        return 0
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                for k in range(c, cols):
                    A[i][k] -= f * A[r][k]
        r += 1
        if r == rows:
            break
    return r


def minor(M, i, j):
    return [row[:j] + row[j + 1:] for k, row in enumerate(M) if k != i]


def adj(M):
    n = len(M)
    if n == 1:
        return [[F(1)]]
    return [[(-1) ** (i + j) * det(minor(M, j, i)) for j in range(n)] for i in range(n)]


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def transpose(M):
    return [list(col) for col in zip(*M)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def gram2(a, b):
    """||a ^ b||^2 = |a|^2 |b|^2 - (a.b)^2 (Lagrange identity)."""
    return dot(a, a) * dot(b, b) - dot(a, b) ** 2


def frob2(M):
    return sum(x * x for row in M for x in row)


def diag(entries):
    n = len(entries)
    return [[entries[i] if i == j else F(0) for j in range(n)] for i in range(n)]


def unitvec(n, i):
    return [F(1) if j == i else F(0) for j in range(n)]


def rand_frac(rng, lo=-3, hi=3, den=5):
    return F(rng.randint(lo * den, hi * den), den)


def rand_vec(rng, n, lo=-3, hi=3, den=5):
    while True:
        v = [rand_frac(rng, lo, hi, den) for _ in range(n)]
        if any(v):
            return v


def rand_sym(rng, n, lo=-3, hi=3, den=5):
    M = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            M[i][j] = M[j][i] = rand_frac(rng, lo, hi, den)
    return M


def rational_unit(rng, n):
    """A rational point of the unit sphere S^(n-1) by stereographic projection of a random rational y in R^(n-1)."""
    y = [F(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(n - 1)]
    s = dot(y, y)
    x = [2 * yi / (s + 1) for yi in y] + [(s - 1) / (s + 1)]
    require(dot(x, x) == 1, 'stereographic point is not on the sphere')
    return x


# ---------------------------------------------------------------- X: two soft directions

def check_x(mut, rng):
    out = {}
    for d in (2, 3, 4):
        order = d - 2 if mut != 'drop-frobenius-order' else max(0, d - 3)
        ok = True
        for _ in range(150):
            H = rand_sym(rng, d)
            u1 = rand_vec(rng, d)
            u2 = rand_vec(rng, d)
            lhs = det(H) ** 2 * gram2(u1, u2)
            rhs = gram2(matvec(H, u1), matvec(H, u2)) * frob2(H) ** order
            ok = ok and lhs <= rhs
        require(ok, 'two-soft-direction exterior inequality failed in d=%d' % d)
        out['det2_wedge_le_Hwedge_frobenius_power_d%d' % d] = ok
    for d in (3, 4):
        s1, s2, big = F(1, 3), F(2, 5), F(7, 2)
        H = diag([s1, s2] + [big] * (d - 2))
        e1, e2 = unitvec(d, 0), unitvec(d, 1)
        lhs = det(H) ** 2 * gram2(e1, e2)
        rhs = gram2(matvec(H, e1), matvec(H, e2)) * big ** (2 * (d - 2))
        require(lhs == rhs, 'diagonal family is not an equality case')
        out['equality_on_diagonal_family_operator_norm_d%d' % d] = True
    ok = True
    for _ in range(100):
        d = rng.choice((2, 3, 4))
        e, e2 = rand_vec(rng, d), rand_vec(rng, d)
        a, b = rand_frac(rng), rand_frac(rng)
        u = [a * e[i] + b * e2[i] for i in range(d)]
        ok = ok and a * a * gram2(e, e2) == gram2(u, e2)
    require(ok, 'Cramer coefficient identity failed')
    out['cramer_coefficient_a2_wedge_identity'] = ok
    return out


# ---------------------------------------------------------------- G: pin-ball gradient frame in d dimensions

def frame_core(p, alpha, beta, drop_s0=False, drop_a4=False):
    """Columns of the frame matrix B over the jets (A_4, T_3, S_0), rows (f_x/(r^2 Delta), grad_y f/(r Delta)).

    The C_3 block is a positive-semidefinite addition to B B^T and is omitted from the core."""
    m = len(beta)
    a = (p - 1) * (2 * p - 1) / 12
    b = (p - 1) / 2
    c = p - F(1, 2)
    cols = []
    if not drop_a4:
        cols.append([a * alpha] + [F(0)] * m)
    for j in range(m):
        col = [c * beta[j]] + [F(0)] * m
        col[1 + j] = b * alpha
        cols.append(col)
    if not drop_s0:
        for i in range(m):
            for j in range(i, m):
                col = [F(0)] * (m + 1)
                if i == j:
                    col[1 + i] = beta[i]
                else:
                    col[1 + i] = beta[j]
                    col[1 + j] = beta[i]
                cols.append(col)
    B = [[cols[k][r] for k in range(len(cols))] for r in range(m + 1)]
    return B, (a, b, c)


def check_g(mut, rng):
    out = {}
    drop_s0 = mut == 'drop-s0-block'
    drop_a4 = mut == 'drop-a4-column'
    for d in (2, 3, 4):
        m = d - 1
        floor = F(9, 64) ** m / 2048
        samples = []
        for _ in range(40):
            samples.append((F(rng.randint(-16, 16), 64), rational_unit(rng, d)))
        for p in (F(0), F(1, 4), F(-1, 4)):
            samples.append((p, [F(0)] + rational_unit(rng, m)))          # alpha = 0
            samples.append((p, [F(1)] + [F(0)] * m))                       # beta = 0
            samples.append((p, [F(-1)] + [F(0)] * m))
        ok_rank = ok_floor = ok_schur = True
        for p, ab in samples:
            alpha, beta = ab[0], ab[1:]
            B, (a, b, c) = frame_core(p, alpha, beta, drop_s0, drop_a4)
            G = matmul(B, transpose(B))
            ok_rank = ok_rank and rank(B) == d
            dg = det(G)
            b2 = dot(beta, beta)
            schur = a * a * alpha * alpha + (c * c * b2 * b2 / (2 * b * b * alpha * alpha + b2)
                                            if (2 * b * b * alpha * alpha + b2) else F(0))
            lower = schur * (b * b * alpha * alpha + b2 / 2) ** m
            ok_schur = ok_schur and dg >= lower
            ok_floor = ok_floor and dg >= floor
        require(ok_rank, 'frame rank drop in d=%d' % d)
        require(ok_schur, 'block-Schur lower bound failed in d=%d' % d)
        require(ok_floor, 'explicit Gram floor failed in d=%d' % d)
        out['frame_rank_d_on_alpha_beta_sphere_d%d' % d] = True
        out['block_schur_lower_bound_d%d' % d] = True
        out['gram_det_floor_9_64_pow_d_minus_1_over_2048_d%d' % d] = True
    out['floor_d2_equals_planar_9_over_131072'] = (F(9, 64) / 2048 == F(9, 131072))
    require(out['floor_d2_equals_planar_9_over_131072'], 'planar constant mismatch')
    # quadratic form of the Gram of S -> S beta over independent entries
    ok = True
    for _ in range(80):
        m = rng.choice((1, 2, 3))
        beta = rand_vec(rng, m)
        xi = rand_vec(rng, m)
        q = sum(xi[i] ** 2 * beta[i] ** 2 for i in range(m)) + sum(
            (xi[i] * beta[j] + xi[j] * beta[i]) ** 2 for i in range(m) for j in range(i + 1, m))
        _, _ = frame_core(F(0), F(0), beta)
        B, _ = frame_core(F(0), F(0), beta)
        Bt = transpose(B)
        # rows 1..m of B restricted to S_0 columns: the last m(m+1)/2 columns
        S_cols = [row[-(m * (m + 1) // 2):] for row in B[1:]]
        Gs = matmul(S_cols, transpose(S_cols))
        qf = dot(xi, matvec(Gs, xi))
        ok = ok and qf == q and 2 * qf >= dot(beta, beta) * dot(xi, xi)
    require(ok, 'S -> S beta Gram identity or floor failed')
    out['S_to_S_beta_gram_identity_and_half_beta2_floor'] = ok
    return out


# ---------------------------------------------------------------- R: confluent rank in d variables

def spatial(d):
    return ['x'] + ['y%d' % j for j in range(1, d)]


def contact_functionals(d):
    """Derivative multi-orders at the midpoint: f, f_x, f_xx, f_xxx, f_yj, f_xyj."""
    names = spatial(d)
    base = [(), ('x',), ('x', 'x'), ('x', 'x', 'x')]
    for j in range(1, d):
        base.append(('y%d' % j,))
        base.append(('x', 'y%d' % j))
    return names, base


def apply_functional(poly, order, names):
    q = poly
    for n in order:
        q = q.d(n)
    for n in names:
        q = q.subs(n, 0)
    return q.const()


def value_gradient_row(poly, point, names):
    row = []
    q = poly
    for n, val in zip(names, point):
        q = q.subs(n, val)
    row.append(q.const())
    for n in names:
        q = poly.d(n)
        for n2, val in zip(names, point):
            q = q.subs(n2, val)
        row.append(q.const())
    return row


def monomial(exps, names):
    p = P.c(1)
    for n, e in zip(names, exps):
        if e:
            p = p * P.v(n, e)
    return p


def check_r(mut, rng):
    out = {}
    for d in (2, 3, 4):
        m = d - 1
        names, contact = contact_functionals(d)
        contact_exps = {(0,) * d, (1,) + (0,) * m, (2,) + (0,) * m, (3,) + (0,) * m}
        for j in range(m):
            e = [0] * d
            e[1 + j] = 1
            contact_exps.add(tuple(e))
            e[0] = 1
            contact_exps.add(tuple(e))
        u = F(3, 2)
        axis = (u,) + (F(0),) * m
        for maxdeg, label in ((4, 'degree4'), (5, 'degree5')):
            exps = [e for e in itertools.product(range(maxdeg + 1), repeat=d) if sum(e) <= maxdeg and e not in contact_exps]
            rows = [value_gradient_row(monomial(e, names), axis, names) for e in exps]
            out['axis_rank_%s_d%d' % (label, d)] = rank(rows)
        require(out['axis_rank_degree5_d%d' % d] == d + 1, 'degree five does not give full witness rank on the axis')
        expected_deg4 = d + 1 if mut == 'degree-four' else d
        require(out['axis_rank_degree4_d%d' % d] == expected_deg4, 'degree-four axis rank is not d')
        # explicit axis family x^4, x^5, x^2 y_j
        fam = [monomial((4,) + (0,) * m, names), monomial((5,) + (0,) * m, names)]
        for j in range(m):
            e = [0] * d
            e[0] = 2
            e[1 + j] = 1
            fam.append(monomial(tuple(e), names))
        for q in fam:
            require(all(apply_functional(q, o, names) == 0 for o in contact), 'axis family is not contact-annihilated')
        D = det([value_gradient_row(q, axis, names) for q in fam])
        require(abs(D) == u ** (2 * d + 6), 'axis family determinant is not u^(2d+6)')
        out['axis_family_det_u_pow_2d_plus_6_d%d' % d] = True
        # explicit transverse family with v along y1: y1^2, y1^3, x y1^2, y_j y1^2 (j >= 2)
        for vmag in (F(1, 2), F(3, 4), F(2)):
            w = (F(-2, 3), vmag) + (F(0),) * (m - 1)
            y1 = P.v('y1')
            fam = [y1 ** 2, y1 ** 3, P.v('x') * y1 ** 2] + [P.v('y%d' % j) * y1 ** 2 for j in range(2, d)]
            for q in fam:
                require(all(apply_functional(q, o, names) == 0 for o in contact), 'transverse family not annihilated')
            D = det([value_gradient_row(q, w, names) for q in fam])
            require(D == -vmag ** (2 * d + 2), 'transverse family determinant is not -|v|^(2d+2)')
        out['transverse_family_det_minus_v_pow_2d_plus_2_d%d' % d] = True
        # general rational transverse direction v with a rational basis of its orthogonal complement
        ok = True
        for _ in range(12):
            v = rand_vec(rng, m)
            v2 = dot(v, v)
            ys = [P.v('y%d' % j) for j in range(1, d)]
            vy = sum((v[j] * ys[j] for j in range(m)), P.c(0))
            perp = []
            for j in range(m):
                e = unitvec(m, j)
                wj = [e[i] - v[i] * v[j] / v2 for i in range(m)]
                if any(wj) and rank(perp + [wj]) == len(perp) + 1:
                    perp.append(wj)
            require(len(perp) == m - 1, 'orthogonal complement basis has wrong size')
            fam = [vy ** 2, vy ** 3, P.v('x') * vy ** 2] + [
                sum((wj[j] * ys[j] for j in range(m)), P.c(0)) * vy ** 2 for wj in perp]
            require(all(apply_functional(q, o, names) == 0 for q in fam for o in contact), 'general family not annihilated')
            w = (F(5, 4),) + tuple(v)
            ok = ok and det([value_gradient_row(q, w, names) for q in fam]) != 0
        require(ok, 'general transverse family singular')
        out['general_transverse_direction_nonsingular_d%d' % d] = ok
    return out


# ---------------------------------------------------------------- RO: row operation on a pinned cubic, d = 3

def pinned_cubic_d3():
    x, y1, y2 = P.v('x'), P.v('y1'), P.v('y2')
    k, r, bb = P.v('k'), P.v('r'), P.v('bb')
    T = [P.v('T1'), P.v('T2')]
    S = [[P.v('S11'), P.v('S12')], [P.v('S12'), P.v('S22')]]
    C = [[P.v('C11'), P.v('C12')], [P.v('C12'), P.v('C22')]]
    Dsym = {(0, 0, 0): P.v('D111'), (0, 0, 1): P.v('D112'), (0, 1, 1): P.v('D122'), (1, 1, 1): P.v('D222')}

    def Dt(i, j, kk):
        return Dsym[tuple(sorted((i, j, kk)))]
    y = [y1, y2]
    f = bb - F(3, 2) * k * r ** 2 * x + 2 * k * x ** 3
    for j in range(2):
        f = f + F(1, 2) * T[j] * (x ** 2 - r ** 2 * F(1, 4)) * y[j]
    for i in range(2):
        for j in range(2):
            f = f + F(1, 2) * S[i][j] * y[i] * y[j] + F(1, 2) * x * C[i][j] * y[i] * y[j]
    for i in range(2):
        for j in range(2):
            for kk in range(2):
                f = f + F(1, 6) * Dt(i, j, kk) * y[i] * y[j] * y[kk]
    return f, (k, r, bb, T, S, C, Dt)


def check_ro(mut):
    out = {}
    f, (k, r, bb, T, S, C, Dt) = pinned_cubic_d3()
    names = ['x', 'y1', 'y2']
    # exact pins: f(-r/2,0) = bb + k r^3/2, f(r/2,0) = bb - k r^3/2, gradients zero
    def at(q, xv):
        return q.subs('x', xv).subs('y1', 0).subs('y2', 0)
    half = P.v('r') * F(1, 2)
    require(at(f, -half) == bb + k * r ** 3 * F(1, 2) and at(f, half) == bb - k * r ** 3 * F(1, 2), 'height pins')
    for n in names:
        require(at(f.d(n), -half).is_zero() and at(f.d(n), half).is_zero(), 'gradient pins')
    out['eight_pins_exact'] = True
    # X = s (u, v1, v2), r = eps s
    s, eps, u, v1, v2 = P.v('s'), P.v('eps'), P.v('u'), P.v('v1'), P.v('v2')
    fx, fy1, fy2 = f.d('x'), f.d('y1'), f.d('y2')

    def scale(q):
        return q.subs('x', s * u).subs('y1', s * v1).subs('y2', s * v2).subs('r', eps * s)
    inv = lambda n: P.v('s', -n)
    Z1 = scale(fx) * inv(2)
    Z2 = scale(fy1) * inv(1)
    Z3 = scale(fy2) * inv(1)
    frac = F(1, 2) if mut != 'row-operation-third' else F(1, 3)
    Z4 = (scale(f) - bb - frac * s * (v1 * scale(fy1) + v2 * scale(fy2))) * inv(3)
    de = u ** 2 - eps ** 2 * F(1, 4)
    vT = v1 * T[0] + v2 * T[1]
    vCv = C[0][0] * v1 ** 2 + 2 * C[0][1] * v1 * v2 + C[1][1] * v2 ** 2
    require(Z1 == 6 * k * de + u * vT + F(1, 2) * vCv, 'first row expansion')
    out['row1_f_x_over_s2_exact'] = True
    Sv = [S[0][0] * v1 + S[0][1] * v2, S[1][0] * v1 + S[1][1] * v2]
    Cv = [C[0][0] * v1 + C[0][1] * v2, C[1][0] * v1 + C[1][1] * v2]
    v = [v1, v2]
    Dvv = [sum((Dt(i, j, kk) * v[j] * v[kk] for j in range(2) for kk in range(2)), P.c(0)) for i in range(2)]
    for i, Zi in enumerate((Z2, Z3)):
        require(Zi == Sv[i] + F(1, 2) * s * de * T[i] + s * u * Cv[i] + F(1, 2) * s * Dvv[i], 'gradient row expansion')
    out['rows_grad_y_over_s_exact'] = True
    require(min(Z4.exponents('s')) >= 0, 'height row has a negative power of s')
    out['height_row_no_negative_power_of_s'] = True
    Z40 = Z4.coeff('s', 0)
    Dvvv = sum((Dt(i, j, kk) * v[i] * v[j] * v[kk] for i in range(2) for j in range(2) for kk in range(2)), P.c(0))
    target = k * (2 * u ** 3 - F(3, 2) * eps ** 2 * u) + F(1, 4) * de * vT - F(1, 12) * Dvvv
    require(Z40 == target, 'height row s^0 part differs from mean + B J')
    out['height_row_s0_equals_mean_plus_BJ'] = True
    require(not any(n.startswith('S') or n.startswith('C') for n in Z40.variables()), 'S_0 or C_3 survives')
    out['S0_and_C3_cancel_from_height_row'] = True
    return out


# ---------------------------------------------------------------- EU: Euler identity in d = 3

def check_eu(mut):
    names = ['x', 'y1', 'y2']
    X = [P.v(n) for n in names]
    f = P.c(0)
    coefs = {}
    for e in itertools.product(range(5), repeat=3):
        if sum(e) <= 4:
            name = 'c%d%d%d' % e
            coefs[e] = P.v(name)
            f = f + coefs[e] * monomial(e, names)
    at0 = lambda q: q.subs('x', 0).subs('y1', 0).subs('y2', 0)
    grads = [f.d(n) for n in names]
    lead = 3 if mut != 'euler-coefficient' else 2
    E = lead * (f - at0(f)) - sum((X[i] * grads[i] for i in range(3)), P.c(0))
    E = E - 2 * sum((at0(grads[i]) * X[i] for i in range(3)), P.c(0))
    H0 = [[at0(grads[i].d(names[j])) for j in range(3)] for i in range(3)]
    E = E - F(1, 2) * sum((H0[i][j] * X[i] * X[j] for i in range(3) for j in range(3)), P.c(0))
    quartic = f.total_degree_terms(names).get(4, P.c(0))
    require(E == -quartic, 'Euler identity remainder is not minus the quartic part')
    return {'euler_remainder_is_minus_quartic_part_d3': True,
            'cubic_terms_cancel': (E.total_degree_terms(names).get(3, P.c(0))).is_zero()}


# ---------------------------------------------------------------- TB: transverse block determinant

def check_tb(mut, rng):
    ok_id = ok_bd = True
    for _ in range(120):
        m = rng.choice((2, 3, 4))
        S = rand_sym(rng, m)
        eps = S[0][0]
        w = [S[i][0] for i in range(1, m)]
        Sp = [row[1:] for row in S[1:]]
        adjS = adj(Sp)
        quad = dot(w, matvec(adjS, w))
        sign = -1 if mut != 'adjugate-sign' else 1
        ok_id = ok_id and det(S) == eps * det(Sp) + sign * quad
        ok_bd = ok_bd and quad ** 2 <= dot(w, w) ** 2 * frob2(Sp) ** (m - 2)
    require(ok_id, 'block determinant identity failed')
    require(ok_bd, 'adjugate quadratic-form bound failed')
    return {'det_S_equals_eps_detSp_minus_wT_adj_w': True, 'wT_adj_w_squared_le_w4_frobenius_power': True}


# ---------------------------------------------------------------- N: jet-functional norms over independent entries

def check_n(rng):
    ok_s = ok_c = ok_d = True
    for _ in range(80):
        m = rng.choice((1, 2, 3))
        v = rand_vec(rng, m)
        v2 = dot(v, v)
        xi = rand_vec(rng, m)
        q = sum(xi[i] ** 2 * v[i] ** 2 for i in range(m)) + sum(
            (xi[i] * v[j] + xi[j] * v[i]) ** 2 for i in range(m) for j in range(i + 1, m))
        ok_s = ok_s and 2 * q >= v2 * dot(xi, xi)
        nc = sum(((1 if i == j else 2) * v[i] * v[j] / 2) ** 2 for i in range(m) for j in range(i, m))
        ok_c = ok_c and 4 * nc >= v2 ** 2
        nd = F(0)
        for i in range(m):
            for j in range(i, m):
                for kk in range(j, m):
                    mult = len(set(itertools.permutations((i, j, kk))))
                    nd += (mult * v[i] * v[j] * v[kk] / 12) ** 2
        ok_d = ok_d and 144 * nd >= v2 ** 3
    require(ok_s and ok_c and ok_d, 'jet functional norm floors failed')
    return {'S_to_Sv_gram_ge_half_v2': ok_s, 'C_functional_norm2_ge_v4_over_4': ok_c,
            'D_functional_norm2_ge_v6_over_144': ok_d}


# ---------------------------------------------------------------- L: ledgers

def check_l(mut):
    out = {}
    soft_B = 6 if mut != 'one-soft-direction' else 5
    for d in range(2, 7):
        # pin region I: Z^-1 (-2), gradient density r^-(d+1), angle-sensitive product r^6, volume r^d
        out['pin_region_I_r_exponent_d%d' % d] = -2 - (d + 1) + soft_B + d
        # collar and remaining collar strips: same ledger
        out['collar_r_exponent_d%d' % d] = -2 - (d + 1) + soft_B + d
        # pin region II, pointwise, with the weight (r|p|)^(2-d) factored out:
        # Z^-1 (-2), density prefactor r^-(d+1), angle-free product r^3 (p^2+|q|^2) <= 2 r (r|p|)^2 (+1), chi^(3d) <= r^-3d
        out['pin_region_II_pointwise_r_exponent_before_absorption_d%d' % d] = -2 - (d + 1) + 1 - 3 * d
        out['pin_region_II_absorption_power_needed_d%d' % d] = (3 - d) - (-2 - (d + 1) + 1 - 3 * d)
        out['jacobian_exponent_d_plus_4_d%d' % d] = 2 + (d - 1) + 3
        out['intermediate_gram_det_exponent_2d_plus_8_d%d' % d] = 4 + 2 * (d - 1) + 6
        # intermediate shell: r: -2 (Z) +2 (endpoint product) +3 (window) = 3; s: -(d+4) density +2 (|det H_X|) + d (volume)
        out['shell_r_exponent_d%d' % d] = -2 + 2 + 3
        out['shell_s_exponent_d%d' % d] = -(d + 4) + 2 + d
    require(all(out['pin_region_I_r_exponent_d%d' % d] == 3 for d in range(2, 7)), 'pin region I ledger is not r^3')
    require(all(out['collar_r_exponent_d%d' % d] == 3 for d in range(2, 7)), 'collar ledger is not r^3')
    require(all(out['pin_region_II_pointwise_r_exponent_before_absorption_d%d' % d] == -2 - 4 * d
                and out['pin_region_II_absorption_power_needed_d%d' % d] == 5 + 3 * d for d in range(2, 7)),
            'region II ledger')
    require(all(out['shell_r_exponent_d%d' % d] == 3 and out['shell_s_exponent_d%d' % d] == -2 for d in range(2, 7)),
            'shell ledger')
    require(out['jacobian_exponent_d_plus_4_d2'] == 6 and out['intermediate_gram_det_exponent_2d_plus_8_d2'] == 12,
            'planar exponents')
    r, s = P.v('r'), P.v('s')
    lhs = 2 * ((r * P.v('s', -1)) ** 2 + s ** 2) - (r + s ** 2) ** 2 * P.v('s', -2)
    require(lhs == (r * P.v('s', -1) - s) ** 2, 'shell inequality identity')
    out['shell_inequality_2_bracket_minus_ratio_is_square'] = True
    partial = F(0)
    ok = True
    for j in range(60):
        partial += F(1, 4 ** j)
        ok = ok and partial < F(4, 3)
    out['dyadic_partial_sums_below_4_over_3'] = ok
    rr = F(1, 2 ** 20)
    rho = F(1, 8)
    total = F(0)
    j = 0
    extra = F(0) if mut != 'flat-shell' else F(1)
    while True:
        sj = 2 ** j * 4 * rr
        if sj > rho:
            break
        total += (rr / sj) ** 2 + sj ** 2 + extra
        j += 1
    require(total <= F(4, 3) / 16 + F(4, 3) * rho ** 2, 'shell sum is not bounded by the dyadic constants')
    out['dyadic_shell_sum_bounded_by_A0_and_rho_terms'] = True
    out['shells_summed'] = j
    return out


# ---------------------------------------------------------------- W: the pin weight

def check_w(mut):
    out = {}
    shift = 2 if mut != 'weight-one-less-power' else 1
    for d in range(2, 7):
        radial = (shift - d) + (d - 2)
        out['weight_radial_exponent_d%d' % d] = radial
        require(radial > -1, 'pin weight is not integrable in d=%d' % d)
        out['nested_ball_count_exponent_d%d' % d] = 3 + 1 + (radial + 1)
        require(out['nested_ball_count_exponent_d%d' % d] == 5, 'nested-ball count is not O(r^5)')
    out['weight_d2_is_one'] = (F(0) == F(shift - 2))
    return out


def flatten(dd):
    return {k: (v if not isinstance(v, F) else str(v)) for k, v in sorted(dd.items())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', choices=MUTANTS)
    mut = ap.parse_args().mutant
    rng = random.Random(20260929)
    checks = {
        'X_two_soft_directions': flatten(check_x(mut, rng)),
        'G_pin_frame_block_gram': flatten(check_g(mut, rng)),
        'R_confluent_rank': flatten(check_r(mut, rng)),
        'RO_row_operation_d3': flatten(check_ro(mut)),
        'EU_euler_identity_d3': flatten(check_eu(mut)),
        'TB_transverse_block_determinant': flatten(check_tb(mut, rng)),
        'N_jet_functional_norms': flatten(check_n(rng)),
        'L_ledgers': flatten(check_l(mut)),
        'W_pin_weight': flatten(check_w(mut)),
    }
    result = {
        'checks': checks,
        'passed': True,
        'scientific_effect': 'NONE',
        'scope': 'exact identities, ranks, floors and power ledgers only; Gaussian, compactness, regression and '
                 'Kac-Rice steps are argued in PROOF.md',
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
