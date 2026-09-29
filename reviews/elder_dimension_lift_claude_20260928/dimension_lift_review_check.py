"""Independent nonauthor checks for OA-ELDER-DIMENSION-LIFT-20260928-v1 (Math- PR 125).

Python standard library only. Written from the manuscript, not from the author's lift.py/test_lift.py.
Groups (exact rational arithmetic unless marked NUMERIC):

  CHART     the Schur shear S^T A S = diag(sigma, D); the full raw chart (sigma,v,D,tau) -> (a,v,D,T) has
            Jacobian determinant exactly one (forward-mode dual numbers over Fractions, d = 3, 4); the xxx
            coordinate decouples; rational-orthogonal rotated lattices are unisolvent for degree <= 3.
  PHYSICAL  end to end on actual physical cubic fields in d = 3, 4, 5: build f from chart data and the
            2(d+1) pins, verify the pins, shear it, recover (sigma, D, tau) exactly, and check the planar
            normal form (A17) with zero remainder, the endpoint blocks (A20), the Schur/determinant/inertia
            identities (A21)-(A22), the gradient-pin average behind (A24) and |H u| = O(r).
  QUARTIC   physical quartic fields with pins re-solved through the 2(d+1)-row contact frame: the frame is
            nonsingular, (A17)'s remainder is O(r) (exact values on a grid at r = 1/8 ... 1/64), and
            H_i u = O(r).
  SADDLES   NUMERIC (floats): on the quartic fields the two extra critical points exist near (rP+-, r^2 W*),
            have index d-1 and window heights, w/r^2 -> -D^{-1} Q(p) at rate O(r), and the planar
            restriction's critical point is not a full critical point.
  PATH      the polygonal path (A19) and saddle data (A18), recomputed from the polynomial class.
  LEDGER    jet counts, the r * r^4 / r^2 = r^3 ledger, the density change of variables (A6) and the
            inverse-moment threshold 5/3 (A6a).

Mutants (each must make the checks fail): raw-a-in-plane, shear-sign, drop-transverse-pin-term,
no-cross-schur, planar-point-is-critical, stable-scale-r, density-dr, threshold-two-thirds, weight-2d.
This is not an analytic proof of the Gaussian covariance floor, conditional C^4 bounds or inverse-function
estimates; those are reviewed in REVIEW.md.
"""
import argparse
import json
import math
import random
import sys
from fractions import Fraction as F
from itertools import product
from math import comb, factorial

MUTANTS = ("raw-a-in-plane", "shear-sign", "drop-transverse-pin-term", "no-cross-schur",
           "planar-point-is-critical", "stable-scale-r", "density-dr", "threshold-two-thirds", "weight-2d")
MUT = None


# ---------------------------------------------------------------------------------------------------------------
# Polynomials: dict {exponent tuple: coefficient}
# ---------------------------------------------------------------------------------------------------------------

def padd(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}


def pscale(p, s):
    return {e: c * s for e, c in p.items() if c * s}


def pmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def pconst(c, n):
    return {(0,) * n: c} if c else {}


def pvar(i, n, c=1):
    return {tuple(int(j == i) for j in range(n)): c}


def pcompose(p, subs, n_out):
    """p(subs[0], ..., subs[n-1]) where each subs[i] is a polynomial in n_out variables."""
    out = {}
    cache = {}
    for e, c in p.items():
        term = pconst(c, n_out)
        for i, power in enumerate(e):
            if power:
                key = (i, power)
                if key not in cache:
                    acc = pconst(1, n_out)
                    for _ in range(power):
                        acc = pmul(acc, subs[i])
                    cache[key] = acc
                term = pmul(term, cache[key])
        out = padd(out, term)
    return out


def pdiff(p, i):
    out = {}
    for e, c in p.items():
        if e[i]:
            e2 = list(e)
            e2[i] -= 1
            out[tuple(e2)] = out.get(tuple(e2), 0) + c * e[i]
    return {e: c for e, c in out.items() if c}


def peval(p, pt):
    total = 0
    for e, c in p.items():
        term = c
        for x, k in zip(pt, e):
            if k:
                term *= x ** k
        total += term
    return total


def pderiv_at0(p, alpha):
    """partial^alpha p (0)."""
    return p.get(tuple(alpha), 0) * math.prod(factorial(a) for a in alpha)


def from_jets(jets, n):
    """Polynomial sum_alpha jets[alpha] x^alpha / alpha!."""
    return {e: F(c) / math.prod(factorial(a) for a in e) for e, c in jets.items() if c}


def multi(n, deg):
    return [e for e in product(range(deg + 1), repeat=n) if sum(e) == deg]


def unit(n, i):
    return tuple(int(j == i) for j in range(n))


def eplus(*es):
    return tuple(map(sum, zip(*es)))


# ---------------------------------------------------------------------------------------------------------------
# Small exact linear algebra
# ---------------------------------------------------------------------------------------------------------------

def solve(A, b):
    n = len(A)
    W = [list(map(F, row)) + [F(b[i])] for i, row in enumerate(A)]
    for j in range(n):
        p = next(i for i in range(j, n) if W[i][j] != 0)
        W[j], W[p] = W[p], W[j]
        piv = W[j][j]
        W[j] = [x / piv for x in W[j]]
        for i in range(n):
            if i != j and W[i][j] != 0:
                f = W[i][j]
                W[i] = [x - f * y for x, y in zip(W[i], W[j])]
    return [row[-1] for row in W]


def det(A):
    n = len(A)
    W = [list(row) for row in A]
    out = 1
    for j in range(n):
        p = next((i for i in range(j, n) if W[i][j] != 0), None)
        if p is None:
            return 0 * out
        if p != j:
            W[j], W[p] = W[p], W[j]
            out = -out
        out = out * W[j][j]
        for i in range(j + 1, n):
            f = W[i][j] / W[j][j]
            for k in range(j, n):
                W[i][k] = W[i][k] - f * W[j][k]
    return out


def inertia(A):
    """(negatives, positives, zeros) of a symmetric Fraction matrix via symmetric pivoting (Sylvester)."""
    n = len(A)
    W = [list(map(F, row)) for row in A]
    idx = list(range(n))
    neg = pos = 0
    while idx:
        j = next((i for i in idx if W[i][i] != 0), None)
        if j is None:
            # 2x2 pivot on a nonzero off-diagonal entry
            pair = next(((i, l) for i in idx for l in idx if i < l and W[i][l] != 0), None)
            if pair is None:
                return neg, pos, len(idx)
            i, l = pair
            neg += 1
            pos += 1
            blk = [[W[i][i], W[i][l]], [W[l][i], W[l][l]]]
            dB = blk[0][0] * blk[1][1] - blk[0][1] * blk[1][0]
            inv = [[blk[1][1] / dB, -blk[0][1] / dB], [-blk[1][0] / dB, blk[0][0] / dB]]
            rest = [m for m in idx if m not in (i, l)]
            for a in rest:
                for b in rest:
                    ca = [W[a][i], W[a][l]]
                    cb = [W[i][b], W[l][b]]
                    W[a][b] -= sum(ca[s] * inv[s][t] * cb[t] for s in range(2) for t in range(2))
            idx = rest
            continue
        piv = W[j][j]
        neg += piv < 0
        pos += piv > 0
        rest = [m for m in idx if m != j]
        for a in rest:
            for b in rest:
                W[a][b] -= W[a][j] * W[j][b] / piv
        idx = rest
    return neg, pos, 0


def rank(rows):
    W = [list(map(F, r)) for r in rows]
    h = 0
    ncol = len(W[0]) if W else 0
    for j in range(ncol):
        p = next((i for i in range(h, len(W)) if W[i][j] != 0), None)
        if p is None:
            continue
        W[h], W[p] = W[p], W[h]
        for i in range(h + 1, len(W)):
            f = W[i][j] / W[h][j]
            if f:
                W[i] = [x - f * y for x, y in zip(W[i], W[h])]
        h += 1
    return h


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


# ---------------------------------------------------------------------------------------------------------------
# Dual numbers over Fractions (forward-mode derivatives for the chart Jacobian)
# ---------------------------------------------------------------------------------------------------------------

class Dual:
    __slots__ = ("v", "g")

    def __init__(self, v, g=None):
        self.v = F(v)
        self.g = g or {}

    @staticmethod
    def lift(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, o):
        o = Dual.lift(o)
        g = dict(self.g)
        for k, c in o.g.items():
            g[k] = g.get(k, 0) + c
        return Dual(self.v + o.v, g)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.v, {k: -c for k, c in self.g.items()})

    def __sub__(self, o):
        return self + (-Dual.lift(o))

    def __rsub__(self, o):
        return Dual.lift(o) - self

    def __mul__(self, o):
        o = Dual.lift(o)
        g = {k: c * o.v for k, c in self.g.items()}
        for k, c in o.g.items():
            g[k] = g.get(k, 0) + c * self.v
        return Dual(self.v * o.v, g)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Dual.lift(o)
        inv = Dual(1 / o.v, {k: -c / (o.v * o.v) for k, c in o.g.items()})
        return self * inv

    def __rtruediv__(self, o):
        return Dual.lift(o) / self

    def __ne__(self, o):
        return self.v != Dual.lift(o).v

    def __eq__(self, o):
        return self.v == Dual.lift(o).v

    def __hash__(self):
        return hash(self.v)


# ---------------------------------------------------------------------------------------------------------------
# The chart
# ---------------------------------------------------------------------------------------------------------------

def rat(rng, lo, hi, steps=1000):
    """A random rational in [lo, hi] on a grid of `steps` intervals (lo, hi may be Fractions)."""
    lo, hi = F(lo), F(hi)
    return lo + (hi - lo) * F(rng.randint(0, steps), steps)


def sample_chart(d, rng, r, k, eps=F(1, 100)):
    """Chart data (sigma, v, D, tau) inside the manuscript's rare set; variables ordered (x, z, w_1..w_n)."""
    n = d - 2
    D = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = -1 + rat(rng, -1 / 10, 1 / 10)
        for j in range(i):
            D[i][j] = D[j][i] = rat(rng, -1 / (10 * n), 1 / (10 * n))
    v = [rat(rng, -1 / (20 * n), 1 / (20 * n)) for _ in range(n)]
    sigma = r * (F(-3, 2) * k + rat(rng, -eps, eps) * k)
    tau = {}
    for e in multi(d, 3):
        tau[e] = rat(rng, -eps, eps) * k
    xz, x, z = unit(d, 0), unit(d, 0), unit(d, 1)
    tau[eplus(x, x, x)] = 12 * k          # cubic model: pins force f_xxx = 12k exactly
    tau[eplus(x, z, z)] = -2 * k + rat(rng, -eps, eps) * k
    return sigma, v, D, tau


def shear_subs(d, q, sign=-1):
    """Substitution (x, z, w) -> (x, z, w + sign*q z) as polynomials in d variables."""
    subs = [pvar(0, d), pvar(1, d)]
    for j in range(d - 2):
        subs.append(padd(pvar(j + 2, d), pvar(1, d, sign * q[j])))
    return subs


def build_physical_cubic(d, sigma, v, D, tau, r, k, b):
    """Physical cubic f(x, y) with the 2(d+1) pins, transverse Hessian A = [[a, v^T], [v, D]] and physical third
    derivatives T obtained from tau through the inverse shear y_w = w - q z, i.e. w = y_w + q y_z."""
    n = d - 2
    q = solve(D, v) if n else []
    a = sigma + sum(vi * qi for vi, qi in zip(v, q))
    cubic_tilde = from_jets({e: c for e, c in tau.items()}, d)
    cubic_phys = pcompose(cubic_tilde, shear_subs(d, q, sign=+1), d)
    T = {e: pderiv_at0(cubic_phys, e) for e in multi(d, 3)}
    x = unit(d, 0)
    jets = dict(T)
    # transverse Hessian over y = (z, w)
    A = [[a] + list(v)] + [[v[i]] + list(D[i]) for i in range(n)]
    for i in range(d - 1):
        for j in range(d - 1):
            jets[eplus(unit(d, i + 1), unit(d, j + 1))] = A[i][j]
    # pin-determined lower order jets (exact for cubic fields)
    jets[(0,) * d] = b - k * r ** 3 / 2
    jets[x] = -F(3, 2) * k * r ** 2
    for j in range(1, d):
        jets[unit(d, j)] = -r * r / 8 * T[eplus(x, x, unit(d, j))]
        jets[eplus(x, unit(d, j))] = F(0)
    jets[eplus(x, x)] = F(0)
    return from_jets(jets, d), A, T, q, a


def hessian_at(p, pt, d):
    return [[peval(pdiff(pdiff(p, i), j), pt) for j in range(d)] for i in range(d)]


def gradient_at(p, pt, d):
    return [peval(pdiff(p, i), pt) for i in range(d)]


def planar_normal_form(k, s, a3, beta, c3):
    """(A17) polynomial in (X, Z)."""
    X, Z = pvar(0, 2), pvar(1, 2)
    lin = F(0) if MUT == "drop-transverse-pin-term" else F(1, 4)
    terms = [pscale(pmul(pmul(X, X), X), 2 * k), pscale(X, -F(3, 2) * k), pconst(-k / 2, 2),
             pscale(pmul(Z, Z), s / 2),
             pscale(pmul(padd(pmul(X, X), pconst(-lin, 2)), Z), a3 / 2),
             pscale(pmul(X, pmul(Z, Z)), beta / 2), pscale(pmul(Z, pmul(Z, Z)), c3 / 6)]
    return padd(*terms)


def scaled_plane(ftilde, d, r, b):
    """F_r(X, Z) = [tilde f(rX, rZ, 0) - b] / r^3."""
    subs = [pvar(0, 2, r), pvar(1, 2, r)] + [{} for _ in range(d - 2)]
    return pscale(padd(pcompose(ftilde, subs, 2), pconst(-b, 2)), 1 / r ** 3)


# ---------------------------------------------------------------------------------------------------------------
# CHART group
# ---------------------------------------------------------------------------------------------------------------

def check_chart():
    out = {}
    rng = random.Random(125001)
    ok_cancel = True
    for n in (1, 2, 3, 4):
        for _ in range(3):
            d = n + 2
            sigma, v, D, _ = sample_chart(d, rng, F(1, 16), F(1))
            q = solve(D, v)
            a = sigma + sum(x * y for x, y in zip(v, q))
            A = [[a] + list(v)] + [[v[i]] + list(D[i]) for i in range(n)]
            sgn = 1 if MUT == "shear-sign" else -1
            S = [[F(int(i == j)) for j in range(n + 1)] for i in range(n + 1)]
            for i in range(n):
                S[i + 1][0] = sgn * q[i]
            B = matmul(transpose(S), matmul(A, S))
            want = [[sigma] + [F(0)] * n] + [[F(0)] + list(D[i]) for i in range(n)]
            ok_cancel &= B == want and det(S) == 1 and det(A) == sigma * det(D)
    out["schur_shear_cancels_and_det_A_equals_sigma_det_D_n1to4"] = ok_cancel

    # Full raw-chart Jacobian with dual numbers.
    ok_jac = True
    for d in (3, 4):
        n = d - 2
        sigma, v, D, tau = sample_chart(d, rng, F(1, 16), F(1))
        names = ["sigma"] + [f"v{i}" for i in range(n)] + [f"D{i}{j}" for i in range(n) for j in range(i, n)]
        cubic_labels = [e for e in multi(d, 3) if e != eplus(unit(d, 0), unit(d, 0), unit(d, 0))]
        names += [f"tau{e}" for e in cubic_labels]
        sd = Dual(sigma, {"sigma": F(1)})
        vd = [Dual(v[i], {f"v{i}": F(1)}) for i in range(n)]
        Dd = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Dd[i][j] = Dd[j][i] = Dual(D[i][j], {f"D{i}{j}": F(1)})
        td = {e: Dual(tau[e], {f"tau{e}": F(1)}) for e in cubic_labels}
        # q = D^{-1} v with duals (Gauss-Jordan)
        W = [list(Dd[i]) + [vd[i]] for i in range(n)]
        for j in range(n):
            piv = W[j][j]
            W[j] = [x / piv for x in W[j]]
            for i in range(n):
                if i != j:
                    f = W[i][j]
                    W[i] = [x - f * y for x, y in zip(W[i], W[j])]
        qd = [W[i][-1] for i in range(n)]
        ad = sd + sum((vd[i] * qd[i] for i in range(n)), Dual(0))
        # T = substitution w -> w + q z applied to tau (dual coefficients).
        cub = {e: td[e] / math.prod(factorial(x) for x in e) for e in cubic_labels}
        subs = [pvar(0, d), pvar(1, d)] + [padd(pvar(j + 2, d), {unit(d, 1): qd[j]}) for j in range(n)]
        phys = {}
        for e, c in cub.items():
            term = {(0,) * d: c}
            for i, power in enumerate(e):
                for _ in range(power):
                    new = {}
                    for e1, c1 in term.items():
                        for e2, c2 in subs[i].items():
                            key = tuple(s + t for s, t in zip(e1, e2))
                            new[key] = new.get(key, Dual(0)) + c1 * c2
                    term = new
            for key, c in term.items():
                phys[key] = phys.get(key, Dual(0)) + c
        Td = {e: phys.get(e, Dual(0)) * math.prod(factorial(x) for x in e) for e in cubic_labels}
        outputs = [ad] + vd + [Dd[i][j] for i in range(n) for j in range(i, n)] + [Td[e] for e in cubic_labels]
        J = [[o.g.get(nm, F(0)) for nm in names] for o in outputs]
        ok_jac &= len(J) == len(names) and det(J) == 1
        # xxx decouples: no output depends on it and it is not an input (it is pinned in U_0).
    out["raw_chart_full_jacobian_is_one_d3_d4"] = ok_jac

    # Rotated-lattice unisolvence for degree <= 3 (Cayley rational orthogonal frames).
    ok_uni = True
    for d in (2, 3):
        labels = [e for deg in range(4) for e in multi(d, deg)]
        for s in ((F(1, 2),), (F(1, 3), F(2, 5), F(-1, 7))):
            K = [[F(0)] * d for _ in range(d)]
            idx = 0
            for i in range(d):
                for j in range(i + 1, d):
                    K[i][j] = s[idx % len(s)]
                    K[j][i] = -K[i][j]
                    idx += 1
            I = [[F(int(i == j)) for j in range(d)] for i in range(d)]
            IpK = [[I[i][j] + K[i][j] for j in range(d)] for i in range(d)]
            ImK = [[I[i][j] - K[i][j] for j in range(d)] for i in range(d)]
            # R = (I - K)^{-1}(I + K)
            cols = [solve(ImK, [IpK[i][j] for i in range(d)]) for j in range(d)]
            R = transpose(cols)
            ok_uni &= matmul(transpose(R), R) == I
            pts = [[sum(R[i][j] * p[j] for j in range(d)) for i in range(d)] for p in product(range(4), repeat=d)]
            rows = [[math.prod(x ** a for x, a in zip(pt, e)) for e in labels] for pt in pts]
            ok_uni &= rank(rows) == len(labels) == comb(d + 3, 3)
    out["rotated_lattice_unisolvence_degree3"] = ok_uni
    return out


# ---------------------------------------------------------------------------------------------------------------
# PHYSICAL group (exact cubic fields)
# ---------------------------------------------------------------------------------------------------------------

def check_physical():
    out = {}
    rng = random.Random(125002)
    k, b = F(6, 5), F(1, 3)
    res = {key: True for key in ("pins", "shear_recovers_sigma_D_tau", "normal_form_A17_exact", "endpoint_blocks_A20",
                                 "schur_det_inertia_A21_A22", "gradient_pin_average_A24", "Hu_order_r",
                                 "weight_order_r4")}
    for d in (3, 4, 5):
        n = d - 2
        for r in (F(1, 8), F(1, 32)):
            sigma, v, D, tau = sample_chart(d, rng, r, k)
            f, A, T, q, a = build_physical_cubic(d, sigma, v, D, tau, r, k, b)
            M = [-r / 2] + [F(0)] * (d - 1)
            S = [r / 2] + [F(0)] * (d - 1)
            res["pins"] &= (peval(f, M) == b and peval(f, S) == b - k * r ** 3
                            and all(g == 0 for g in gradient_at(f, M, d) + gradient_at(f, S, d)))
            ft = pcompose(f, shear_subs(d, q, sign=+1 if MUT == "shear-sign" else -1), d)
            Ht0 = hessian_at(ft, [F(0)] * d, d)
            rec = (Ht0[1][1] == sigma and all(Ht0[1][j + 2] == 0 for j in range(n))
                   and all(Ht0[i + 2][j + 2] == D[i][j] for i in range(n) for j in range(n))
                   and all(pderiv_at0(ft, e) == tau[e] for e in multi(d, 3)))
            res["shear_recovers_sigma_D_tau"] &= rec
            # (A17): exact for cubic fields.
            s_coef = (a if MUT == "raw-a-in-plane" else Ht0[1][1]) / r
            x, z = unit(d, 0), unit(d, 1)
            a3, beta, c3 = pderiv_at0(ft, eplus(x, x, z)), pderiv_at0(ft, eplus(x, z, z)), pderiv_at0(ft, eplus(z, z, z))
            Fr = scaled_plane(ft, d, r, b)
            res["normal_form_A17_exact"] &= Fr == planar_normal_form(k, s_coef, a3, beta, c3)
            # Endpoint blocks in the (x, z; w) shear frame.
            P = planar_normal_form(k, Ht0[1][1] / r, a3, beta, c3)
            dets = []
            for sgn, pt in ((-1, M), (1, S)):
                H = hessian_at(ft, pt, d)
                Xs = F(sgn, 2)
                Pi = [[peval(pdiff(pdiff(P, i), j), [Xs, F(0)]) for j in range(2)] for i in range(2)]
                soft = [[H[i][j] for j in range(2)] for i in range(2)]
                C = [[H[i][j + 2] for j in range(n)] for i in range(2)]
                Di = [[H[i + 2][j + 2] for j in range(n)] for i in range(n)]
                ok20 = soft == [[r * Pi[i][j] for j in range(2)] for i in range(2)]
                xxw = [pderiv_at0(ft, eplus(x, x, unit(d, j + 2))) for j in range(n)]
                xzw = [pderiv_at0(ft, eplus(x, z, unit(d, j + 2))) for j in range(n)]
                ok20 &= C == [[sgn * r / 2 * c for c in xxw], [sgn * r / 2 * c for c in xzw]]
                ok20 &= all(Di[i][j] == D[i][j] + sgn * r / 2 * pderiv_at0(ft, eplus(x, unit(d, i + 2), unit(d, j + 2)))
                            for i in range(n) for j in range(n))
                res["endpoint_blocks_A20"] &= ok20
                # Schur complement K_i = soft - C D_i^{-1} C^T
                DinvCT = transpose([solve(Di, [C[i][j] for j in range(n)]) for i in range(2)])
                corr = matmul(C, DinvCT)
                if MUT == "no-cross-schur":
                    corr = [[F(0)] * 2 for _ in range(2)]
                K = [[soft[i][j] - corr[i][j] for j in range(2)] for i in range(2)]
                Hphys = hessian_at(f, pt, d)
                ok22 = det(Hphys) == det(H) == det(Di) * det(K)
                negD, _, _ = inertia(Di)
                negK, posK, zK = inertia(K)
                negH, posH, zH = inertia(Hphys)
                ok22 &= negD == n and zK == 0 and zH == 0 and negH == negD + negK
                ok22 &= (negH == d) if sgn < 0 else (negH == d - 1)
                # K/r - P_i = O(r): exact size check against the explicit bound |C|^2 |D_i^{-1}| / r
                ok22 &= max(abs(K[i][j] / r - Pi[i][j]) for i in range(2) for j in range(2)) <= r * k
                res["schur_det_inertia_A21_A22"] &= ok22
                dets.append(abs(det(Hphys)))
                # H_i u = O(r): H(0) u = 0 exactly by pins, so H_i u = sgn (r/2) (f_xxx, f_xxy...).
                Hu = [Hphys[i][0] for i in range(d)]
                third = [pderiv_at0(f, eplus(x, x, unit(d, i))) for i in range(d)]
                res["Hu_order_r"] &= Hu == [sgn * r / 2 * c for c in third]
            res["weight_order_r4"] &= (dets[0] * dets[1] / r ** (8 if MUT == "weight-2d" else 4)) > F(1, 1000)
            # Gradient-pin average: r * int_{-1/2}^{1/2} H(t r u) u dt = grad f(S) - grad f(M) = 0.
            t = pvar(0, 1)
            line = [pscale(t, r)] + [{} for _ in range(d - 1)]
            avg = []
            for i in range(d):
                col = pcompose(pdiff(pdiff(f, i), 0), line, 1)
                prim = {(e[0] + 1,): c / (e[0] + 1) for e, c in col.items()}
                avg.append(r * (peval(prim, [F(1, 2)]) - peval(prim, [F(-1, 2)])))
            res["gradient_pin_average_A24"] &= all(v_ == 0 for v_ in avg)
    out.update(res)
    return out


# ---------------------------------------------------------------------------------------------------------------
# QUARTIC group: pins re-solved through the contact frame, O(r) remainder
# ---------------------------------------------------------------------------------------------------------------

def build_quartic(d, rng, r, k, b, sigma, v, D, tau, quartic):
    """Physical quartic field: free jets (transverse Hessian, third derivatives except xxx) from the chart, a fixed
    quartic part, and the 2(d+1) U_0 jets (f, f_x, f_xx, f_xxx, f_y, f_xy) solved from the pins."""
    n = d - 2
    q = solve(D, v) if n else []
    a = sigma + sum(vi * qi for vi, qi in zip(v, q))
    x = unit(d, 0)
    tau_free = {e: c for e, c in tau.items() if e != eplus(x, x, x)}
    cubic_phys = pcompose(from_jets(tau_free, d), shear_subs(d, q, sign=+1), d)
    base = padd(cubic_phys, quartic)
    A = [[a] + list(v)] + [[v[i]] + list(D[i]) for i in range(n)]
    for i in range(d - 1):
        for j in range(i, d - 1):
            e = eplus(unit(d, i + 1), unit(d, j + 1))
            base = padd(base, {e: A[i][j] / math.prod(factorial(t) for t in e)})
    U0 = [(0,) * d, x, eplus(x, x), eplus(x, x, x)]
    for j in range(1, d):
        U0 += [unit(d, j), eplus(x, unit(d, j))]
    basis = [from_jets({e: 1}, d) for e in U0]
    M = [-r / 2] + [F(0)] * (d - 1)
    S = [r / 2] + [F(0)] * (d - 1)
    rows, rhs = [], []
    for pt, val in ((M, b), (S, b - k * r ** 3)):
        rows.append([peval(p, pt) for p in basis])
        rhs.append(val - peval(base, pt))
    for pt in (M, S):
        for i in range(d):
            rows.append([peval(pdiff(p, i), pt) for p in basis])
            rhs.append(-peval(pdiff(base, i), pt))
    frame_det = det(rows)
    coeffs = solve(rows, rhs)
    f = padd(base, *[pscale(p, c) for p, c in zip(basis, coeffs)])
    return f, q, frame_det


def random_quartic(d, rng, size):
    return {e: rat(rng, -size, size) for e in multi(d, 4)}


def check_quartic():
    out = {}
    rng = random.Random(125003)
    k, b = F(6, 5), F(1, 3)
    ok_frame = ok_pins = True
    rates = {}
    hu_rates = {}
    grid = [F(i, 4) for i in range(-8, 9)]
    for d in (3, 4):
        quartic = random_quartic(d, rng, F(1, 2))
        base_rng_state = rng.getstate()
        errs, hus = [], []
        for r in (F(1, 8), F(1, 16), F(1, 32), F(1, 64)):
            rng.setstate(base_rng_state)
            sigma, v, D, tau = sample_chart(d, rng, r, k)
            f, q, frame_det = build_quartic(d, rng, r, k, b, sigma, v, D, tau, quartic)
            ok_frame &= frame_det != 0
            M = [-r / 2] + [F(0)] * (d - 1)
            S = [r / 2] + [F(0)] * (d - 1)
            ok_pins &= (peval(f, M) == b and peval(f, S) == b - k * r ** 3
                        and all(g == 0 for g in gradient_at(f, M, d) + gradient_at(f, S, d)))
            ft = pcompose(f, shear_subs(d, q), d)
            x, z = unit(d, 0), unit(d, 1)
            s_coef = hessian_at(ft, [F(0)] * d, d)[1][1] / r
            P = planar_normal_form(k, s_coef, pderiv_at0(ft, eplus(x, x, z)), pderiv_at0(ft, eplus(x, z, z)),
                                   pderiv_at0(ft, eplus(z, z, z)))
            Fr = scaled_plane(ft, d, r, b)
            diff = padd(Fr, pscale(P, -1))
            errs.append(max(abs(peval(diff, [X, Z])) for X in grid for Z in grid if X * X + Z * Z <= 9))
            Hs = hessian_at(f, S, d)
            hus.append(max(abs(Hs[i][0]) for i in range(d)))
        rates[d] = [float(errs[i] / errs[i + 1]) for i in range(3)]
        hu_rates[d] = [float(hus[i] / hus[i + 1]) for i in range(3)]
    out["contact_frame_nonsingular"] = ok_frame
    out["pins_exact_after_solve"] = ok_pins
    out["A17_remainder_halves_with_r"] = all(1.6 < x_ < 2.4 for rs in rates.values() for x_ in rs)
    out["Hu_halves_with_r"] = all(1.6 < x_ < 2.4 for rs in hu_rates.values() for x_ in rs)
    out["_rates"] = {"A17_remainder": {str(d_): [round(x_, 4) for x_ in v_] for d_, v_ in rates.items()},
                     "H_S_u": {str(d_): [round(x_, 4) for x_ in v_] for d_, v_ in hu_rates.items()}}
    return out


# ---------------------------------------------------------------------------------------------------------------
# SADDLES group (NUMERIC)
# ---------------------------------------------------------------------------------------------------------------

def to_float_poly(p):
    return {e: float(c) for e, c in p.items()}


def fl_eval(p, pt):
    return sum(c * math.prod(x ** k_ for x, k_ in zip(pt, e)) for e, c in p.items())


def lin_solve_float(A, b):
    n = len(A)
    W = [list(A[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        p = max(range(j, n), key=lambda i: abs(W[i][j]))
        W[j], W[p] = W[p], W[j]
        for i in range(n):
            if i != j:
                f = W[i][j] / W[j][j]
                W[i] = [x - f * y for x, y in zip(W[i], W[j])]
    return [W[i][-1] / W[i][i] for i in range(n)]


def float_inertia(A):
    n = len(A)
    W = [list(r) for r in A]
    neg = 0
    for j in range(n):
        piv = W[j][j]
        if piv == 0:
            return None
        neg += piv < 0
        for i in range(j + 1, n):
            f = W[i][j] / piv
            for l in range(j, n):
                W[i][l] -= f * W[j][l]
    return neg


def newton(grad, hess, x0, steps=60):
    x = list(x0)
    for _ in range(steps):
        g = [fl_eval(p, x) for p in grad]
        H = [[fl_eval(p, x) for p in row] for row in hess]
        dx = lin_solve_float(H, [-t for t in g])
        x = [a + b for a, b in zip(x, dx)]
        if max(abs(t) for t in dx) < 1e-15:
            break
    return x


def check_saddles():
    out = {}
    rng = random.Random(125004)
    k, b = F(6, 5), F(1, 3)
    ok_exist = ok_index = ok_height = ok_distinct = ok_not_planar = True
    conv = {}
    for d in (3, 4):
        n = d - 2
        quartic = random_quartic(d, rng, F(1, 2))
        state = rng.getstate()
        errs = []
        for r in (F(1, 16), F(1, 32), F(1, 64), F(1, 128)):
            rng.setstate(state)
            sigma, v, D, tau = sample_chart(d, rng, r, k)
            f, q, _ = build_quartic(d, rng, r, k, b, sigma, v, D, tau, quartic)
            ft = pcompose(f, shear_subs(d, q), d)
            x, z = unit(d, 0), unit(d, 1)
            s_coef = hessian_at(ft, [F(0)] * d, d)[1][1] / r
            P = planar_normal_form(k, s_coef, pderiv_at0(ft, eplus(x, x, z)), pderiv_at0(ft, eplus(x, z, z)),
                                   pderiv_at0(ft, eplus(z, z, z)))
            Pf = to_float_poly(P)
            gP = [to_float_poly(pdiff(P, i)) for i in range(2)]
            hP = [[to_float_poly(pdiff(pdiff(P, i), j)) for j in range(2)] for i in range(2)]
            ftf = to_float_poly(ft)
            g = [to_float_poly(pdiff(ft, i)) for i in range(d)]
            h = [[to_float_poly(pdiff(pdiff(ft, i), j)) for j in range(d)] for i in range(d)]
            # stable quadratic Q(X, Z) of (A28) from the actual sheared third derivatives
            Qs = []
            for j in range(n):
                wj = unit(d, j + 2)
                t_xx, t_xz, t_zz = (pderiv_at0(ft, eplus(x, x, wj)), pderiv_at0(ft, eplus(x, z, wj)),
                                    pderiv_at0(ft, eplus(z, z, wj)))
                Qs.append((float(t_xx), float(t_xz), float(t_zz)))
            Df = [[float(D[i][j]) for j in range(n)] for i in range(n)]
            rf = float(r)
            pts = []
            for sgnZ in (1, -1):
                p = newton(gP, hP, [-0.75, sgnZ * math.sqrt(15 / 8)])
                Qp = [t0 / 2 * (p[0] ** 2 - 0.25) + t1 * p[0] * p[1] + t2 / 2 * p[1] ** 2 for (t0, t1, t2) in Qs]
                Wstar = lin_solve_float(Df, [-t for t in Qp])
                # the planar restriction's critical point is not a full critical point
                grad_w_planar = [fl_eval(g[j + 2], [rf * p[0], rf * p[1]] + [0.0] * n) / rf ** 2 for j in range(n)]
                if MUT == "planar-point-is-critical":
                    ok_not_planar &= max(abs(t) for t in grad_w_planar) < 1e-12
                else:
                    ok_not_planar &= max(abs(t) for t in grad_w_planar) > 1e-4
                scale_w = rf if MUT == "stable-scale-r" else rf ** 2
                x0 = [rf * p[0], rf * p[1]] + [rf ** 2 * t for t in Wstar]
                sol = newton(g, h, x0)
                gn = max(abs(fl_eval(gi, sol)) for gi in g)
                ok_exist &= gn < 1e-15 and math.dist(sol[:2], x0[:2]) < 8 * rf ** 2  # O(r) shift in scaled units
                H = [[fl_eval(hij, sol) for hij in row] for row in h]
                ok_index &= float_inertia(H) == d - 1
                height = fl_eval(ftf, sol)
                ok_height &= float(b) - float(k) * rf ** 3 < height < float(b)
                Wn = [t / scale_w for t in sol[2:]]
                errs.append(max(abs(a_ - b_) for a_, b_ in zip(Wn, Wstar)) / rf)
                pts.append(sol)
            ok_distinct &= math.dist(pts[0], pts[1]) > 0.5 * rf and all(
                math.dist(pp, [s_ * rf / 2] + [0.0] * (d - 1)) > 0.5 * rf for pp in pts for s_ in (-1, 1))
        conv[d] = errs
    # |w/r^2 - W*| = O(r): the normalized error |w/r^2 - W*| / r stays within a factor 2 over r = 1/16 ... 1/128,
    # separately for the + and - saddle (entries alternate + / - per r).
    ratios = {d_: [max(e[i::2]) / min(e[i::2]) for i in (0, 1)] for d_, e in conv.items()}
    out["two_extra_critical_points_exist"] = ok_exist
    out["index_d_minus_1"] = ok_index
    out["heights_inside_window"] = ok_height
    out["distinct_from_each_other_and_pins"] = ok_distinct
    out["planar_critical_point_not_full_critical"] = ok_not_planar
    out["stable_displacement_W_converges_at_rate_r"] = all(x_ < 2 for rs in ratios.values() for x_ in rs)
    out["_ratios"] = {str(d_): [round(x_, 4) for x_ in rs] for d_, rs in ratios.items()}
    return out


# ---------------------------------------------------------------------------------------------------------------
# PATH and LEDGER groups
# ---------------------------------------------------------------------------------------------------------------

def check_path():
    k = F(1)
    G = planar_normal_form(k, F(-3, 2), F(0), F(-2), F(0))
    t = pvar(0, 1)
    segs = [((F(-1, 2), F(0)), (F(-3, 4), F(0))), ((F(-3, 4), F(0)), (F(-3, 4), F(9, 4))),
            ((F(-3, 4), F(9, 4)), (F(-1), F(9, 4)))]
    want = [{(2,): F(-3, 16), (3,): F(-1, 32)}, {(0,): F(-7, 32)},
            {(0,): F(-7, 32), (1,): F(51, 64), (2,): F(-9, 32), (3,): F(-1, 32)}]
    ok = True
    for (p0, p1), w in zip(segs, want):
        line = [padd(pconst(p0[i], 1), pscale(t, p1[i] - p0[i])) for i in range(2)]
        ok &= pcompose(G, line, 1) == w
        ok &= max(p0[0] ** 2 + p0[1] ** 2, p1[0] ** 2 + p1[1] ** 2) <= F(97, 16) < 9
    d3 = {(0,): F(51, 64), (1,): F(-9, 16), (2,): F(-3, 32)}
    ok &= min(peval(d3, [F(i, 64)]) for i in range(65)) >= F(9, 64) and peval(d3, [F(1)]) == F(9, 64)
    ok &= F(-7, 32) - F(1, 64) > F(-1, 4) and F(17, 64) - F(1, 64) == F(1, 4)
    ok &= peval(G, [F(-1, 2), F(0)]) == 0 and peval(G, [F(1, 2), F(0)]) == -1
    # extra saddles of G
    Z2 = F(15, 8)
    gx = pdiff(G, 0)
    ok &= peval(gx, [F(-3, 4), F(0)]) + (-Z2) == 0  # G_X = 6X^2 - 3/2 - Z^2 at X=-3/4 vanishes iff Z^2 = 15/8
    ok &= F(3, 2) + 2 * F(-3, 4) == 0                # G_Z = -Z(3/2 + 2X) vanishes at X = -3/4
    ok &= 2 * F(-3, 4) ** 3 - F(3, 2) * F(-3, 4) - F(1, 2) - (F(3, 4) + F(-3, 4)) * Z2 == F(-7, 32)
    ok &= 12 * F(-3, 4) * 0 - 4 * Z2 == F(-15, 2)     # det [[-9, -2Z], [-2Z, 0]] = -4 Z^2
    ok &= F(9, 16) + Z2 < 9
    hm = [[peval(pdiff(pdiff(G, i), j), [F(-1, 2), F(0)]) for j in range(2)] for i in range(2)]
    hs = [[peval(pdiff(pdiff(G, i), j), [F(1, 2), F(0)]) for j in range(2)] for i in range(2)]
    ok &= hm == [[-6, 0], [0, F(-1, 2)]] and hs == [[6, 0], [0, F(-5, 2)]]
    return {"path_segments_margins_and_saddle_data": ok}


def check_ledger():
    out = {}
    ok = True
    for d in range(2, 13):
        m = d - 1
        U = 2 * (d + 1)
        J = m * (m + 1) // 2 + comb(d + 2, 3) - 1
        ok &= U + J == comb(d + 3, 3)
    out["jet_count_U0_plus_J_is_binom_d3_3"] = ok
    rare, weight, norm = 1, (2 * 4 if MUT == "weight-2d" else 4), 2
    out["ledger_r_r4_over_r2_is_r3_all_d"] = rare + weight - norm == 3
    # ell = k r^3 at fixed k: r dr = (1/3) ell^(-1/3) k^(-2/3) d ell; times (1 - p) ~ r^3 = ell/k.
    r_exp = F(1, 3)  # r = ell^(1/3) k^(-1/3)
    jac_exp_ell = r_exp - 1
    jac_exp_k = -r_exp
    measure_ell = (0 if MUT == "density-dr" else r_exp) + jac_exp_ell
    measure_k = (0 if MUT == "density-dr" else -r_exp) + jac_exp_k
    loss_ell, loss_k = measure_ell + 1, measure_k - 1
    out["density_loss_ell_2_3_k_minus_5_3"] = (measure_ell, measure_k, loss_ell, loss_k) == (
        F(-1, 3), F(-2, 3), F(2, 3), F(-5, 3))
    threshold = F(2, 3) if MUT == "threshold-two-thirds" else loss_ell + 1
    ok_t = threshold == F(5, 3)
    for p in (F(1), F(3, 2), F(8, 5)):
        ok_t &= (loss_ell - p) > -1   # integrable at 0
    for p in (F(5, 3), F(2)):
        ok_t &= (loss_ell - p) <= -1  # not integrable at 0 (log at 5/3)
    out["inverse_moment_threshold_5_3"] = ok_t
    return out


def flatten(d):
    for k_, v_ in d.items():
        if k_.startswith("_"):
            continue
        if isinstance(v_, dict):
            yield from flatten(v_)
        else:
            yield v_


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"CHART": check_chart(), "PHYSICAL": check_physical(), "QUARTIC": check_quartic(),
              "SADDLES": check_saddles(), "PATH": check_path(), "LEDGER": check_ledger()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-ELDER-DIMENSION-LIFT-20260928-v1", "checks": checks,
                      "passed": passed,
                      "scope": "exact chart/field identities and one labelled numerical saddle group; "
                               "not an analytic proof"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
