#!/usr/bin/env python3
"""A3 (d >= 3) exact controls, standard library only (fractions). Author-side; not a proof of the analytic claims.

Z1  Schur/inertia identity: for H = [[A, B^T], [B, D]] with D symmetric negative definite,
      (v, w)^T H (v, w) = v^T (A - B^T D^-1 B) v + (w + D^-1 B v)^T D (w + D^-1 B v)        (exact),
    and Sylvester: inertia(H) = inertia(A - B^T D^-1 B) + (0, m) negatives (sign counts on random rational H).
Z2  Fibre bounds for z-quadratic fibres g = g0 + p.z + z^T D z / 2, D <= -Lam I (checked exactly):
      0 <= G - g0 = -p^T D^-1 p / 2 <= |p|^2/(2 Lam),   |zeta|^2 = p^T D^-2 p <= |p|^2/Lam^2,
      g(z) <= G - Lam |z - zeta|^2 / 2 at random rational z.
Z3  Interior maximum and hard drop: if |p| < Lam eps / 2 then on |z| = eps, p.z - Lam eps^2/2 < 0 (so the max is
    interior) and G - Lam (eps - |zeta|)^2 / 2 <= G - Lam eps^2 / 8;  Lam eps^2 > 8 gives a drop > 1.
Z4  Schur C2 bound: B^T (I/Lam + D^-1) B is positive semidefinite, hence ||B^T D^-1 B|| <= ||B||^2/Lam.
Mutants: --mutant Z2 (constant 1/(4 Lam)), --mutant Z3 (drop Lam eps^2/4), --mutant Z4 (bound ||B||^2/(2 Lam)) exit 1.
"""
import json
import sys
from fractions import Fraction as Fr

MUT = None
if len(sys.argv) > 1:
    if len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in ('Z2', 'Z3', 'Z4'):
        MUT = sys.argv[2]
    else:
        print(json.dumps({'error': 'unknown arguments'}))
        sys.exit(2)


class Lcg:
    """deterministic rational generator (no random module state dependence across versions)"""
    def __init__(self, seed):
        self.s = seed

    def nxt(self):
        self.s = (6364136223846793005 * self.s + 1442695040888963407) % (1 << 64)
        return self.s >> 11

    def fr(self, lo, hi, den=97):
        n = self.nxt() % (den * (hi - lo) + 1)
        return Fr(lo) + Fr(n, den)


def mat_mul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def transpose(X):
    return [list(r) for r in zip(*X)]


def inv(X):
    n = len(X)
    if n == 1:
        return [[1 / X[0][0]]]
    a, b, c, d = X[0][0], X[0][1], X[1][0], X[1][1]
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def quad(v, X, w=None):
    w = v if w is None else w
    return sum(v[i] * X[i][j] * w[j] for i in range(len(v)) for j in range(len(w)))


def sym_signs(X):
    """exact (n_pos, n_neg, n_zero) of a symmetric matrix of size <= 4 via Gaussian elimination (Sylvester)"""
    M = [list(r) for r in X]
    n = len(M); pos = neg = zero = 0
    idx = list(range(n))
    while idx:
        piv = next((i for i in idx if M[i][i] != 0), None)
        if piv is None:
            # find an off-diagonal nonzero and rotate (i, j) -> i + j
            pair = next(((i, j) for i in idx for j in idx if i < j and M[i][j] != 0), None)
            if pair is None:
                zero += len(idx); break
            i, j = pair
            for k in range(n):
                M[i][k] += M[j][k]
            for k in range(n):
                M[k][i] += M[k][j]
            continue
        p = M[piv][piv]
        if p > 0: pos += 1
        else: neg += 1
        idx.remove(piv)
        for i in idx:
            f = M[i][piv] / p
            for k in range(n):
                M[i][k] -= f * M[piv][k]
        for i in idx:
            M[piv][i] = Fr(0); M[i][piv] = Fr(0)
    return pos, neg, zero


def neg_def_with(D, lam):
    """D <= -lam I exactly (size 1 or 2)"""
    E = [[D[i][j] + (lam if i == j else 0) for j in range(len(D))] for i in range(len(D))]
    if len(D) == 1:
        return E[0][0] <= 0
    return E[0][0] <= 0 and E[1][1] <= 0 and E[0][0] * E[1][1] - E[0][1] * E[1][0] >= 0


def psd2(X):
    if len(X) == 1:
        return X[0][0] >= 0
    return X[0][0] >= 0 and X[1][1] >= 0 and X[0][0] * X[1][1] - X[0][1] * X[1][0] >= 0


def main():
    rng = Lcg(20261003)
    fails, n = [], dict(Z1=0, Z2=0, Z3=0, Z4=0)
    for trial in range(1200):
        m = 1 + trial % 2
        # A (2x2 sym), B (m x 2), D (m x m sym neg def)
        a11, a22, a12 = rng.fr(-5, 5), rng.fr(-5, 5), rng.fr(-5, 5)
        A = [[a11, a12], [a12, a22]]
        B = [[rng.fr(-4, 4) for _ in range(2)] for _ in range(m)]
        lam = rng.fr(1, 30)
        if m == 1:
            D = [[-lam - rng.fr(0, 10)]]
        else:
            t = rng.fr(-3, 3)
            d1, d2 = -lam - rng.fr(0, 10) - abs(t), -lam - rng.fr(0, 10) - abs(t)
            D = [[d1, t], [t, d2]]
        if not neg_def_with(D, lam):
            fails.append(('setup', trial)); continue
        Di = inv(D)
        S = [[A[i][j] - quad([B[k][i] for k in range(m)], Di, [B[k][j] for k in range(m)]) for j in range(2)] for i in range(2)]
        # Z1 identity at random (v, w)
        v = [rng.fr(-3, 3), rng.fr(-3, 3)]
        wv = [rng.fr(-3, 3) for _ in range(m)]
        H = [[A[0][0], A[0][1]] + [B[k][0] for k in range(m)], [A[1][0], A[1][1]] + [B[k][1] for k in range(m)]]
        for k in range(m):
            H.append([B[k][0], B[k][1]] + [D[k][j] for j in range(m)])
        vw = v + wv
        lhs = quad(vw, H)
        Bv = [sum(B[k][j] * v[j] for j in range(2)) for k in range(m)]
        shift = [wv[k] + sum(Di[k][j] * Bv[j] for j in range(m)) for k in range(m)]
        rhs = quad(v, S) + quad(shift, D)
        n['Z1'] += 1
        if lhs != rhs:
            fails.append(('Z1', trial))
        sH, sS = sym_signs(H), sym_signs(S)
        n['Z1'] += 1
        if not (sH[0] == sS[0] and sH[1] == sS[1] + m and sH[2] == sS[2]):
            fails.append(('Z1-inertia', trial, sH, sS))
        # Z2 fibre bounds for g = g0 + p.z + z^T D z / 2
        p = [rng.fr(-6, 6) for _ in range(m)]
        zeta = [-sum(Di[k][j] * p[j] for j in range(m)) for k in range(m)]
        gain = -quad(p, Di) / 2                       # G - g0
        p2 = sum(x * x for x in p)
        const = Fr(1, 4) if MUT == 'Z2' else Fr(1, 2)
        n['Z2'] += 1
        if not (0 <= gain <= const * p2 / lam):
            fails.append(('Z2-gain', trial))
        z2 = sum(x * x for x in zeta)
        n['Z2'] += 1
        if not z2 * lam * lam <= p2:
            fails.append(('Z2-zeta', trial))
        z = [rng.fr(-2, 2) for _ in range(m)]
        gz = sum(p[k] * z[k] for k in range(m)) + quad(z, D) / 2
        G = gain
        dz2 = sum((z[k] - zeta[k]) ** 2 for k in range(m))
        n['Z2'] += 1
        if not gz <= G - lam * dz2 / 2:
            fails.append(('Z2-drop', trial))
        # Z3 interior maximum and hard drop.  eps with 4|p|^2 < lam^2 eps^2 (i.e. |p| < lam eps/2); every third trial
        # takes D = -lam I and eps just above 2|p|/lam, the extreme case of the drop bound.
        extreme = trial % 3 == 0
        if extreme:
            D = [[(-lam if i == j else Fr(0)) for j in range(m)] for i in range(m)]
            Di = inv(D)
            zeta = [-sum(Di[k][j] * p[j] for j in range(m)) for k in range(m)]
            G = -quad(p, Di) / 2
            z2 = sum(x * x for x in zeta)
        lo = 2 * (abs(p[0]) + (abs(p[1]) if m == 2 else 0)) / lam      # >= 2|p|/lam
        eps = lo * (1 + Fr(1, 997)) + (Fr(1, 97) if not extreme else Fr(0)) + (rng.fr(0, 2) if not extreme else Fr(0))
        if eps == 0:
            eps = Fr(1, 97)
        n['Z3'] += 1
        if not 4 * p2 < lam * lam * eps * eps:
            fails.append(('Z3-interior', trial))
        den = 4 if MUT == 'Z3' else 8
        pts = []
        if m == 1:
            pts = [[eps], [-eps]]
        else:
            for tq in (Fr(0), Fr(1, 3), Fr(-2, 5), Fr(7, 4), Fr(-5, 2)):
                pts.append([eps * (1 - tq * tq) / (1 + tq * tq), eps * 2 * tq / (1 + tq * tq)])
            if extreme and p2 > 0:                    # include the boundary point closest to zeta (rational only if aligned)
                pts.append([eps if p[0] >= 0 else -eps, Fr(0)])
        for zb in pts:
            gzb = sum(p[k] * zb[k] for k in range(m)) + quad(zb, D) / 2
            n['Z3'] += 1
            if not gzb <= G - lam * eps * eps / den:
                fails.append(('Z3-drop', trial)); break
        n['Z3'] += 1
        e8 = Fr(8) / lam + Fr(1, 1000)                 # eps^2 with lam eps^2 > 8
        if not -lam * e8 / 8 < -1:
            fails.append(('Z3-depth', trial))
        # Z4 Schur C2 bound: B^T (I/lam + D^-1) B >= 0  =>  ||B^T D^-1 B|| <= ||B||^2/lam
        factor = Fr(1, 2) if MUT == 'Z4' else Fr(1)
        Mtmp = [[(factor / lam if i == j else 0) + Di[i][j] for j in range(m)] for i in range(m)]
        Q = [[quad([B[k][i] for k in range(m)], Mtmp, [B[k][j] for k in range(m)]) for j in range(2)] for i in range(2)]
        n['Z4'] += 1
        if not psd2(Q):
            fails.append(('Z4', trial))
    out = {'object': 'A3 d>=3 hard-fibre reduction (author-side exact controls)', 'counts': n,
           'mutant': MUT, 'all_pass': not fails, 'failures': [str(f) for f in fails[:8]], 'scientific_effect': 'NONE'}
    print(json.dumps(out, sort_keys=True))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
