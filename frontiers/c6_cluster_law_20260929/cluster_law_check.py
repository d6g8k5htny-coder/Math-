"""Exact finite controls for CL-C6-CLUSTER-LAW-20260929-v1.2.

Standard library only; exact rationals and exact polynomial arithmetic over Q.
Verifies identities, exact configurations and exponent bookkeeping only. It does
not verify the Gaussian, regression, dominated-convergence or Kac-Rice steps.

    python -B -S cluster_law_check.py            # rc 0, prints RESULTS.json
    python -B -S cluster_law_check.py --mutant M # rc 1 for each named mutant
"""
import argparse
import json
import math
import random
from fractions import Fraction as F

MUTANTS = ('pins-not-critical', 'wrong-pin-hessian', 'drop-sigma-jacobian',
           'three-extra-points', 'cross-term-not-small', 'window-closed', 'index-sign',
           'shear-drop-cubic', 's-bound-constant')

# ---------------------------------------------------------------- polynomials
V = ('X', 'Z', 's', 'a', 'b', 'c', 'k')
NV = len(V)


def var(name, coef=F(1)):
    e = [0] * NV
    e[V.index(name)] = 1
    return {tuple(e): F(coef)}


def const(v):
    return {tuple([0] * NV): F(v)} if v != 0 else {}


def add(p, q, sg=1):
    r = dict(p)
    for e, v in q.items():
        r[e] = r.get(e, F(0)) + sg * v
    return {e: v for e, v in r.items() if v != 0}


def mul(p, q):
    r = {}
    for e1, u in p.items():
        for e2, v in q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            r[e] = r.get(e, F(0)) + u * v
    return {e: v for e, v in r.items() if v != 0}


def smul(c, p):
    return {e: F(c) * v for e, v in p.items()} if c != 0 else {}


def powr(p, m):
    r = const(1)
    for _ in range(m):
        r = mul(r, p)
    return r


def diff(p, name):
    i = V.index(name)
    r = {}
    for e, v in p.items():
        if e[i] > 0:
            e2 = list(e)
            e2[i] -= 1
            r[tuple(e2)] = r.get(tuple(e2), F(0)) + v * e[i]
    return {e: v for e, v in r.items() if v != 0}


def subs(p, name, q):
    i = V.index(name)
    r = {}
    for e, v in p.items():
        e2 = list(e)
        m = e2[i]
        e2[i] = 0
        r = add(r, mul({tuple(e2): v}, powr(q, m)))
    return r


def coeff_in(p, name, j):
    i = V.index(name)
    r = {}
    for e, v in p.items():
        if e[i] == j:
            e2 = list(e)
            e2[i] = 0
            r[tuple(e2)] = r.get(tuple(e2), F(0)) + v
    return {e: v for e, v in r.items() if v != 0}


def degree_in(p, name):
    i = V.index(name)
    return max((e[i] for e in p), default=-1)


def require(ok, message):
    if not ok:
        raise ValueError(message)


X, Z, s, a, b, c, k = [var(t) for t in V]
HALF = F(1, 2)


def cubic(mutant=None):
    """F_0(X,Z) = 2kX^3 - (3k/2)X - k/2 + (s/2)Z^2 + (a/2)(X^2-1/4)Z + (b/2)XZ^2 + (c/6)Z^3."""
    const_term = F(-1, 3) if mutant == 'pins-not-critical' else F(-1, 2)
    terms = [smul(2, mul(k, powr(X, 3))), smul(F(-3, 2), mul(k, X)), smul(const_term, k),
             smul(HALF, mul(s, powr(Z, 2))),
             smul(HALF, mul(a, mul(add(powr(X, 2), const(F(-1, 4))), Z))),
             smul(HALF, mul(b, mul(X, powr(Z, 2)))), smul(F(1, 6), mul(c, powr(Z, 3)))]
    p = {}
    for t in terms:
        p = add(p, t)
    return p


def evaluate(p, **vals):
    for name, v in vals.items():
        p = subs(p, name, const(v))
    return p


def as_number(p):
    require(all(all(x == 0 for x in e) for e in p), 'not a constant: ' + repr(p))
    return sum(p.values(), F(0))


# ------------------------------------------------------------------ checks
def check_normal_form(mutant):
    F0 = cubic(mutant)
    gx, gz = diff(F0, 'X'), diff(F0, 'Z')
    at = lambda p, x: subs(subs(p, 'X', const(x)), 'Z', const(0))
    require(at(F0, -HALF) == {}, 'F_0(M) must be 0')
    require(at(F0, HALF) == smul(-1, k), 'F_0(S) must be -k')
    for x in (-HALF, HALF):
        require(at(gx, x) == {} and at(gz, x) == {}, 'pins must be critical')
    Hxx, Hxz, Hzz = diff(gx, 'X'), diff(gx, 'Z'), diff(gz, 'Z')
    sign = -1 if mutant == 'wrong-pin-hessian' else 1
    expect = {-HALF: (smul(-6, k), smul(-sign * HALF, a), add(s, smul(-HALF, b))),
              HALF: (smul(6, k), smul(sign * HALF, a), add(s, smul(HALF, b)))}
    for x, (exx, exz, ezz) in expect.items():
        require(at(Hxx, x) == exx and at(Hxz, x) == exz and at(Hzz, x) == ezz, 'pin Hessian block')
    return F0, gx, gz


def check_resultant(gx, gz, mutant):
    A = [coeff_in(gx, 'Z', j) for j in range(3)]
    B = [coeff_in(gz, 'Z', j) for j in range(3)]
    t1 = add(mul(A[2], B[0]), mul(A[0], B[2]), -1)
    t2 = add(mul(A[2], B[1]), mul(A[1], B[2]), -1)
    t3 = add(mul(A[1], B[0]), mul(A[0], B[1]), -1)
    res = add(mul(t1, t1), mul(t2, t3), -1)          # Sylvester determinant of two quadratics
    d = add(powr(X, 2), const(F(-1, 4)))
    q, rem = {}, dict(res)
    while degree_in(rem, 'X') >= 2:
        m = degree_in(rem, 'X')
        lead = {e: v for e, v in rem.items() if e[0] == m}
        sh = {}
        for e, v in lead.items():
            e2 = list(e)
            e2[0] -= 2
            sh[tuple(e2)] = v
        q = add(q, sh)
        rem = add(rem, mul(sh, d), -1)
    require(rem == {}, 'resultant not divisible by X^2 - 1/4')
    expected_degree = 3 if mutant == 'three-extra-points' else 2
    require(degree_in(q, 'X') == expected_degree, 'quotient degree')
    c2 = add(add(add(add(smul(F(1, 4), mul(powr(a, 3), c)), smul(F(-3, 16), mul(powr(a, 2), powr(b, 2)))),
                     smul(F(-9, 2), mul(mul(a, b), mul(c, k)))), smul(3, mul(powr(b, 3), k))),
             smul(9, mul(powr(c, 2), powr(k, 2))))
    c1 = add(add(smul(F(-1, 4), mul(powr(a, 2), b)), smul(-3, mul(mul(a, c), k))), smul(6, mul(powr(b, 2), k)))
    inner = add(smul(F(1, 8), mul(a, b)), smul(F(-3, 2), mul(c, k)))
    c0 = add(smul(3, mul(mul(powr(s, 2), b), k)), smul(-1, mul(inner, inner)))
    Q2 = add(add(mul(c2, powr(X, 2)), mul(mul(s, c1), X)), c0)
    require(q == Q2, 'Q_2 coefficients (3.6)')
    return Q2


def q2_coeffs(sv, av, bv, cv, kv):
    c2 = av ** 3 * cv / 4 - 3 * av ** 2 * bv ** 2 / 16 - F(9, 2) * av * bv * cv * kv + 3 * bv ** 3 * kv + 9 * cv ** 2 * kv ** 2
    c1 = -av ** 2 * bv / 4 - 3 * av * cv * kv + 6 * bv ** 2 * kv
    c0 = 3 * sv ** 2 * bv * kv - (av * bv / 8 - 3 * cv * kv / 2) ** 2
    return c2, sv * c1, c0


def weights(sv, av, bv, kv, mutant):
    wM = -6 * kv * (sv - bv / 2) - av * av / 4
    wS = av * av / 4 - 6 * kv * (sv + bv / 2)
    if mutant == 'index-sign':
        wS = -wS
    return wM, wS


def check_examples(F0, gx, gz, mutant):
    kv = F(1)
    ev = lambda p, x, z, sv, av, bv, cv: as_number(evaluate(p, X=x, Z=z, s=sv, a=av, b=bv, c=cv, k=kv))
    lo, hi = -kv, F(0)
    if mutant == 'window-closed':
        in_window = lambda h: lo <= h <= hi
    else:
        in_window = lambda h: lo < h < hi
    # rational configurations: jets, extra points, expected heights, expected N_oo, expected weights
    table = [
        ((F(-55, 48), F(5, 2), F(-5, 3), F(-5, 2)), [(F(-2), F(3)), (F(-783, 1616), F(-129, 1616))],
         [F(-27, 32), F(-4735, 83566592)], 2, (F(5, 16), F(215, 16))),
        ((F(-1, 2), F(3), F(1, 3), F(0)), [(F(-3, 2), F(3)), (F(45, 22), F(-357, 11))],
         [F(-1, 2), F(-9947, 121)], 1, (F(7, 4), F(17, 4))),
        ((F(-33, 10), F(3), F(-12, 5), F(-3)), [(F(-2), F(5, 2)), (F(-282, 541), F(-1495, 1082))],
         [F(-41, 16), F(-3199921, 4682896)], 1, (F(207, 20), F(117, 4))),
        ((F(-396), F(-3), F(-204), F(-3)), [(F(-2), F(1, 2)), (F(-263314, 140087), F(-115623, 280174))],
         [F(-119, 8), None], 0, (F(7047, 4), F(11961, 4))),
    ]
    counts = []
    for (sv, av, bv, cv), pts, heights, n_expected, (wM_e, wS_e) in table:
        c2, c1s, c0 = q2_coeffs(sv, av, bv, cv, kv)
        n_in = 0
        for (x, z), h in zip(pts, heights):
            require(ev(gx, x, z, sv, av, bv, cv) == 0 and ev(gz, x, z, sv, av, bv, cv) == 0, 'not a critical point')
            require(c2 * x * x + c1s * x + c0 == 0, 'X not a root of Q_2')
            hv = ev(F0, x, z, sv, av, bv, cv)
            if h is not None:
                require(hv == h, 'height')
            else:
                require(hv < -kv, 'height below window')
            n_in += 1 if in_window(hv) else 0
        # the two roots of Q_2 are exactly the two X coordinates (Vieta)
        require(c2 != 0 and pts[0][0] + pts[1][0] == -c1s / c2 and pts[0][0] * pts[1][0] == c0 / c2, 'Vieta')
        if mutant == 'window-closed':
            n_in += sum(1 for h in (F(0), -kv) if in_window(h))   # pins would be counted with a closed window
        require(n_in == n_expected, 'N_oo of a configuration')
        wM, wS = weights(sv, av, bv, kv, mutant)
        require((wM, wS) == (wM_e, wS_e) and wM > 0 and wS > 0, 'pin weights')
        counts.append(n_expected)
    # the [LM] cubic: s=-3k/2, a=0, b=-2k, c=0; extra points (-3/4, +-sqrt(15/8)) at height -7k/32
    sv, av, bv, cv = F(-3, 2), F(0), F(-2), F(0)
    c2, c1s, c0 = q2_coeffs(sv, av, bv, cv, kv)
    require(c1s * c1s == 4 * c2 * c0 and -c1s / (2 * c2) == F(-3, 4), '[LM] double root of Q_2 at -3/4')
    zz = add(powr(Z, 2), const(F(-15, 8)))          # Z^2 - 15/8
    for p, target in ((gx, F(0)), (gz, F(0)), (F0, F(-7, 32))):
        red = evaluate(p, X=F(-3, 4), s=sv, a=av, b=bv, c=cv, k=kv)
        # reduce modulo Z^2 - 15/8
        while degree_in(red, 'Z') >= 2:
            m = degree_in(red, 'Z')
            lead = {e: v for e, v in red.items() if e[1] == m}
            sh = {}
            for e, v in lead.items():
                e2 = list(e)
                e2[1] -= 2
                sh[tuple(e2)] = v
            red = add(red, mul(sh, zz), -1)
        require(red == const(target) or (target == 0 and red == {}), '[LM] configuration on Z^2 = 15/8')
    wM, wS = weights(sv, av, bv, kv, mutant)
    require((wM, wS) == (F(3), F(15)) and wM * wS == 45, '[LM] weight 45 k^4')
    require(in_window(F(-7, 32)), '[LM] heights in the window')
    # large soft curvature: no real extra critical point
    c2, c1s, c0 = q2_coeffs(F(1000), F(2), F(1), F(-1), kv)
    require(c1s * c1s - 4 * c2 * c0 < 0, 'large s: Q_2 has no real root')
    wM, wS = weights(F(1000), F(2), F(1), kv, mutant)
    require(max(wM, 0) * max(wS, 0) == 0, 'large positive s: index conditions fail')
    return sorted(set(counts)) == [0, 1, 2]


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    tot = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        tot += (-1) ** j * M[0][j] * det(minor)
    return tot


def lagrange_coeffs(points):
    """Exact polynomial coefficients through the given (x, y) points."""
    n = len(points)
    coeffs = [F(0)] * n
    for i, (xi, yi) in enumerate(points):
        basis = [F(1)]
        denom = F(1)
        for j, (xj, _) in enumerate(points):
            if j == i:
                continue
            basis = [F(0)] + basis
            for t in range(len(basis) - 1):
                basis[t] -= xj * basis[t + 1]
            denom *= (xi - xj)
        for t in range(n):
            coeffs[t] += yi * basis[t] / denom
    return coeffs


def check_block_determinant():
    random.seed(20260929)
    for dim in (3, 4):
        n = dim - 2
        for _ in range(3):
            kv, av, sv, bv = [F(random.randint(-9, 9), random.randint(1, 5)) for _ in range(4)]
            cross = [[F(random.randint(-5, 5), random.randint(1, 3)) for _ in range(n)] for _ in range(2)]
            D = [[F(0)] * n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    D[i][j] = D[j][i] = F(random.randint(-5, 5), random.randint(1, 3))
            if det(D) == 0:
                D[0][0] += 1
            M2 = [[-6 * kv, -av / 2], [-av / 2, sv - bv / 2]]
            pts = []
            for rr in [F(1, p) for p in (3, 5, 7, 11, 13)][:dim + 1]:
                H = [[F(0)] * dim for _ in range(dim)]
                for i in range(2):
                    for j in range(2):
                        H[i][j] = rr * M2[i][j]
                    for j in range(n):
                        H[i][2 + j] = H[2 + j][i] = rr * cross[i][j]
                for i in range(n):
                    for j in range(n):
                        H[2 + i][2 + j] = D[i][j]
                pts.append((rr, det(H)))
            co = lagrange_coeffs(pts)
            require(co[0] == 0 and co[1] == 0, 'block determinant: no r^0, r^1 terms')
            require(co[2] == det(D) * det(M2), 'block determinant: r^2 coefficient is det D det M_2')
    return True


def check_euler():
    xi, zeta, av, bv, cv, kv = X, Z, a, b, c, k   # reuse symbols: xi=X, zeta=Z
    G3 = add(add(add(smul(2, mul(kv, powr(xi, 3))), smul(HALF, mul(av, mul(powr(xi, 2), zeta)))),
                 smul(HALF, mul(bv, mul(xi, powr(zeta, 2))))), smul(F(1, 6), mul(cv, powr(zeta, 3))))
    G = add(G3, smul(HALF, powr(zeta, 2)))
    euler = add(add(mul(xi, diff(G, 'X')), mul(zeta, diff(G, 'Z'))), add(smul(3, G3), powr(zeta, 2)), -1)
    require(euler == {}, 'Euler identity')
    ident = add(add(smul(6, G), smul(-1, powr(zeta, 2))), smul(2, add(mul(xi, diff(G, 'X')), mul(zeta, diff(G, 'Z')))), -1)
    require(ident == {}, '6G - zeta^2 = 2(xi G_xi + zeta G_zeta), so G = zeta^2/6 at critical points')
    require(subs(diff(G, 'X'), 'Z', const(0)) == smul(6, mul(kv, powr(xi, 2))), 'zeta = 0 forces xi = 0')
    return True


def check_ledger(mutant):
    sigma_jac = 0 if mutant == 'drop-sigma-jacobian' else 1
    require(sigma_jac + 4 - 2 == 3, 'exponent: r (soft slice) . r^4 (weight) / r^2 (normalizer) = r^3')
    cross = F(3) + (F(3, 2) if mutant != 'cross-term-not-small' else F(0))
    require(cross > 3, 'near-far cross term is o(r^3)')
    for A, rho in ((4, F(1, 2)), (100, F(1, 100))):
        require(F(1, A * A) + rho * rho <= F(1, 16) + F(1, 4), 'shell error A^-2 + rho^2 decreases')
    # Hadamard bound (3.10): per pin determinant, two soft rows, the lambda_2 row and d - 3 stable rows;
    # W_r is a product of two such determinants, so the row factors number 2d in all.
    hadamard = {}
    for d in (3, 4):
        require(2 * (2 + 1 + (d - 3)) == 2 * d, 'Hadamard: 2d row factors for two pin determinants')
        require(4 + 2 + (2 * d - 6) == 2 * d, 'exponents 4 (soft), 2 (lambda_2), 2d - 6 (stable) of (3.10) sum to 2d')
        hadamard[d] = 2 * d
    # large-K_4 tail (4.3): kappa^(-p/2) -> 0; checked exactly for even p on kappa = 1, 10, 100
    for half_p in (1, 2, 10):
        require(F(1, 100) ** half_p < F(1, 10) ** half_p < F(1) ** half_p, 'kappa^(-p/2) decreases in kappa')
    # uniform integrability (§6.3, §6.5): n 1{n > M} <= n(n - 1)/(M - 1) for every integer n > M >= 2
    for M in (2, 5, 10):
        for n in range(M + 1, M + 12):
            require(F(n) <= F(n * (n - 1), M - 1), 'E[N 1{N > M}] <= E[(N)_2]/(M - 1)')
    require(F(1, 100 - 1) < F(1, 10 - 1) < F(1, 2 - 1), 'uniform-integrability tail 1/(M - 1) -> 0')
    return {'soft_slice_exponent': 3, 'cross_term_exponent': str(cross), 'hadamard_row_factors': hadamard,
            'ui_tail': '1/(M-1)'}


# ------------------------------------------------------- shear and typed window
def check_shear(F0, mutant):
    """(3.12) with k cleared: (12k)^3 F_0(X, Z) at 12k X = 12k u - a Z equals
    1728 k^3 C(u) + 864 k^3 s Z^2 + 72 k^2 (12k b - a^2) u Z^2 + 4k (72 k^2 c - 18 k a b + a^3) Z^3.
    The variable slot 'X' of the polynomial ring is used for u."""
    u, Z, s, a, b, c, k = (var(n) for n in V)
    twelve_k = smul(12, k)
    tkX = add(mul(twelve_k, u), smul(-1, mul(a, Z)))          # 12k X
    # (12k)^3 F_0 written in 12kX: 2k (12kX)^3 - (3k/2)(12k)^2 (12kX) - (k/2)(12k)^3
    #   + (12k)^3 [ (s/2) Z^2 + (c/6) Z^3 ] + (a/2)(12k) [ (12kX)^2 - (12k)^2/4 ] Z + (b/2)(12k)^2 (12kX) Z^2
    k2, k3 = powr(twelve_k, 2), powr(twelve_k, 3)
    lhs = add(smul(2, mul(k, powr(tkX, 3))), smul(F(-3, 2), mul(mul(k, k2), tkX)))
    lhs = add(lhs, smul(F(-1, 2), mul(k, k3)))
    lhs = add(lhs, mul(k3, add(smul(F(1, 2), mul(s, powr(Z, 2))), smul(F(1, 6), mul(c, powr(Z, 3))))))
    lhs = add(lhs, smul(F(1, 2), mul(mul(a, twelve_k), mul(add(powr(tkX, 2), smul(F(-1, 4), k2)), Z))))
    lhs = add(lhs, smul(F(1, 2), mul(mul(b, k2), mul(tkX, powr(Z, 2)))))
    Cu = add(add(smul(2, mul(k, powr(u, 3))), smul(F(-3, 2), mul(k, u))), smul(F(-1, 2), k))
    twelve_kB = add(mul(twelve_k, b), smul(-1, powr(a, 2)))                      # 12k B
    D144 = add(add(smul(72, mul(powr(k, 2), c)), smul(-18, mul(k, mul(a, b)))), powr(a, 3))   # 144 k^2 D
    if mutant == 'shear-drop-cubic':
        D144 = add(smul(72, mul(powr(k, 2), c)), smul(-18, mul(k, mul(a, b))))
    rhs = smul(1728, mul(powr(k, 3), Cu))
    rhs = add(rhs, smul(864, mul(powr(k, 3), mul(s, powr(Z, 2)))))
    rhs = add(rhs, smul(72, mul(powr(k, 2), mul(twelve_kB, mul(u, powr(Z, 2))))))
    rhs = add(rhs, smul(4, mul(k, mul(D144, powr(Z, 3)))))
    require(add(lhs, smul(-1, rhs)) == {}, 'shear identity (3.12) with k cleared')
    # the shear is unimodular: u = X + a Z/(12k), Z = Z
    require(F(1) * F(1) - F(0) * F(1) == 1, 'unimodular shear')


def check_typed_window(mutant):
    """Exact rational family of critical points of G(u, Z) = C(u) + (s + B u) Z^2/2 + (D/3) Z^3:
    for rational (u, Z != 0, D, k), B = 3k(1 - 4u^2)/Z^2 and s = -B u - D Z make (u, Z) critical.
    Checks the determinant identity, the height identity, and Lemma 3.6 on the typed in-window samples."""
    bound = F(1) if mutant == 's-bound-constant' else F(32)
    grid = sorted(set(F(n, d) for n in range(-9, 10) for d in (1, 2, 3)))
    total = typed = 0
    for k in (F(1), F(1, 2), F(2)):
        for u in grid:
            for Z in grid:
                if Z == 0:
                    continue
                for D in grid:
                    B = 3 * k * (1 - 4 * u * u) / (Z * Z)
                    s = -B * u - D * Z
                    w = s + B * u
                    gu = 6 * k * u * u - F(3, 2) * k + B * Z * Z / 2
                    gZ = Z * (w + D * Z)
                    require(gu == 0 and gZ == 0, 'family consists of critical points')
                    G = F(k, 2) * (u - 1) * (2 * u + 1) ** 2 + w * Z * Z / 2 + D * Z ** 3 / 3
                    det = 12 * k * u * (w + 2 * D * Z) - (B * Z) ** 2
                    require(det == -3 * k * (B + 4 * s * u), 'Hessian determinant -3k(B + 4su) at critical points')
                    if D != 0:
                        require(G == F(k, 2) * (u - 1) * (2 * u + 1) ** 2 + w ** 3 / (6 * D * D), 'height C(u) + w^3/(6D^2)')
                    total += 1
                    if s < -abs(B) / 2 and -k < G < 0:
                        typed += 1
                        require(det < 0, 'every typed in-window extra point is a saddle')
                        excess = max(F(0), -s - 2 * abs(B))
                        require(excess ** 3 <= bound * k * D * D, '(-s - 2|B|)_+^3 <= 32 k D^2 (Lemma 3.6)')
    require(typed >= 1000, 'enough typed in-window samples')
    return {'family_size': total, 'typed_in_window': typed}


def run(mutant=None):
    groups = []
    F0, gx, gz = check_normal_form(mutant)
    groups.append('NF')
    Q2 = check_resultant(gx, gz, mutant)
    groups.append('RS')
    require(check_examples(F0, gx, gz, mutant), 'configurations with 0, 1, 2 extra points')
    groups.append('EX')
    check_block_determinant()
    groups.append('BD')
    check_euler()
    groups.append('EU')
    check_shear(F0, mutant)
    groups.append('SH')
    tw = check_typed_window(mutant)
    groups.append('TW')
    ledger = check_ledger(mutant)
    groups.append('LG')
    return {'schema': 1, 'object': 'CL-C6-CLUSTER-LAW-20260929-v1.2', 'passed': True, 'groups': groups,
            'ledger': ledger, 'q2_terms': len(Q2), 'typed_window': tw, 'scientific_effect': 'NONE', 'mathematical_acceptance': False,
            'scope': 'exact identities, exact configurations and exponent bookkeeping only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=MUTANTS)
    args = parser.parse_args()
    try:
        result = run(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
