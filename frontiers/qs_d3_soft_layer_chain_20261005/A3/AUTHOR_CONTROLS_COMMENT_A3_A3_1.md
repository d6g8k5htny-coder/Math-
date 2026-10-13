## QS addenda A3 and A3.1: author controls, exact executables and stdout

This publishes the two standard-library control scripts that A3 ([5970263575](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5970263575)) and A3.1 ([5971014231](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971014231)) cite, so anyone can replay them. Until now they existed only in the author's workspace and the project archive. Nothing in either addendum changes. These are author-side controls of finite algebra and a combinatorial analogue. They do not prove the analytic statements.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude, author of QS, A2, A3 and A3.1 (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** Each file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line. A final newline is included, so the byte counts below include it. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.**
- `python3 -B -S <file>`: exit 0, with exactly the stdout shown.
- `python3 -B -S -O <file>`: byte-identical output, since no `assert` is used.
- `python3 -B -S <file> --bogus`: exit 2.

The outputs were produced with Python 3.11.15. The scripts use only `json`, `sys`, `fractions` and `heapq`.

### a3d_exact.py

- **Cited in** A3 (5970263575) §5.
- **File:** 9052 bytes, SHA-256 `f8a640475bdda971d493754ef2f949b3fea2d6ac691a81c9f6c21a13b7fc0f93`.
- **Stdout:** 211 bytes, SHA-256 `d5773800b4959eb43a81919e67bced96c4672ba3cdad5f011da173e007e7fb76`.
- **Mutants:** `--mutant Z2`, `--mutant Z3` and `--mutant Z4` each exit 1.

```python
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
```

Expected stdout:

```json
{"all_pass": true, "counts": {"Z1": 2400, "Z2": 3600, "Z3": 6800, "Z4": 1200}, "failures": [], "mutant": null, "object": "A3 d>=3 hard-fibre reduction (author-side exact controls)", "scientific_effect": "NONE"}
```

### a31_exact.py

- **Cited in** A3.1 (5971014231) §8.
- **File:** 16855 bytes, SHA-256 `644f0b7b6ce10111ac177e4bfab3b1fc52ccf034857b2b32900f218af5d5b23d`.
- **Stdout:** 208 bytes, SHA-256 `a826b2659853edfa86ffe895db5849cdea3d50da4d3c999915d8995b1761331c`.
- **Mutants:** `--mutant N1`, `F1`, `R1`, `C1` and `H1` each exit 1.

```python
#!/usr/bin/env python3
"""QS addendum A3.1: author-side exact controls (standard library only; fractions and integers).

These are checks of finite algebra and of a combinatorial analogue. They do not prove the analytic statements.

N1  Pin types (Lemma N_d).  In J-scaled planar coordinates the reduced Hessian at S is diag(2, -2) + E with ||E|| <= 2/5,
    and at M it is -2 I + E with ||E|| < 1.  For a hard block D <= -Lam I and any coupling B, the full Hessian
    H = [[A, B^T], [B, D]] with Schur complement A - B^T D^-1 B equal to that reduced Hessian has inertia (1, m + 1, 0) at S
    and (0, m + 2, 0) at M (exact Gaussian elimination).  Extreme cases ||E|| = 2/5 and ||E|| = 1 - 1/97 are included.
F1  FL.1' bookkeeping (d = 3, one hard direction).
    (a) The exponents ex(i, j, L) = i + j + 3L/2 - 3 of the degree <= 4 monomials x^i y1^j y'^l (|l| = L) are < 1 exactly
        for {L = 0, i + j <= 3}, {L = 1, i + j <= 2} and {L = 2, i + j = 0} (enumeration).
    (b) For a random rational quartic f with exact transverse pins along the hard direction (solved symbolically in
        s = r^(1/2)) and the eigenframe condition d_1 d_h f(0) = 0, the eta-linear and eta^2 parts of
        F = (f(rX, rk zeta, r^(3/2) eta) - b)/(k r^3) satisfy, as Laurent polynomials in s:
            [eta^1] F - s a(X, zeta) = O(s^3),   a = (gamma_h/(2k))(X^2 - 1/4) + d_u d_1 d_h f(0) X zeta + (k/2) d_1^2 d_h f(0) zeta^2,
            [eta^2] F + lambda_2/(2k) = O(s^2),   [eta^3] F = O(s^3),   [eta^4] F = O(s^6).
R1  Raw radii.  With sqrt(24 lam~) = t rational, the raw image (X, zeta) = (u - Z/12, Z/gamma) of
        W_E = [-5/4, 3/2] x [-30/sqrt(psi), 30/sqrt(psi)]  has max |(X, zeta)| <= 3/2 + (5/2)(|gamma| + 12)/t,
        W_R = [-5/2, 3/2] x [-34/sqrt(psi), 34/sqrt(psi)]  has max |(X, zeta)| <= 5/2 + (17/6)(|gamma| + 12)/t,
    where sqrt(psi) = t/|gamma| (exact, at the parallelogram vertices).
C1  Barrel constants.  With v^2 = lambda_2/k, eps = 4/v, Lam = v^2 - delta and 0 <= delta < v^2/2:
        Lam eps^2 > 8   and   Lam eps/2 > v = sqrt(lambda_2/k)   (exact; delta up to v^2/2 - 1/10^6).
H1  Discrete analogue of C96's lemma on periodic grids (d = 2, 3, 4; distinct integer heights; 2d-neighbour torus graph):
    for every local maximum, the superlevel union-find death with the elder rule occurs at height equal to the bottleneck
    maximin to a strictly higher vertex (over all torus paths), and the global maximum has no higher vertex.
Mutants (each exits 1): --mutant N1 (S threshold 2), F1 (drop the -1/4), R1 (17/6 -> 2), C1 (eps = 2/v), H1 (younger rule).
Unknown arguments exit 2.
"""
import json
import sys
from fractions import Fraction as Fr

MUTANTS = ('N1', 'F1', 'R1', 'C1', 'H1')
MUT = None
if len(sys.argv) > 1:
    if len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in MUTANTS:
        MUT = sys.argv[2]
    else:
        print(json.dumps({'error': 'unknown arguments'}))
        sys.exit(2)


class Lcg:
    """deterministic generator (independent of the random module)"""
    def __init__(self, seed):
        self.s = seed

    def nxt(self):
        self.s = (6364136223846793005 * self.s + 1442695040888963407) % (1 << 64)
        return self.s >> 11

    def fr(self, lo, hi, den=97):
        n = self.nxt() % (den * (hi - lo) + 1)
        return Fr(lo) + Fr(n, den)

    def below(self, n):
        return self.nxt() % n


# ----------------------------------------------------------------------------------------------- exact linear algebra
def sym_signs(X):
    """exact (n_pos, n_neg, n_zero) of a symmetric rational matrix (congruence by Gaussian elimination)"""
    M = [list(r) for r in X]
    n = len(M)
    pos = neg = zero = 0
    idx = list(range(n))
    while idx:
        piv = next((i for i in idx if M[i][i] != 0), None)
        if piv is None:
            pair = next(((i, j) for i in idx for j in idx if i < j and M[i][j] != 0), None)
            if pair is None:
                zero += len(idx)
                break
            i, j = pair
            for k in range(n):
                M[i][k] += M[j][k]
            for k in range(n):
                M[k][i] += M[k][j]
            continue
        p = M[piv][piv]
        if p > 0:
            pos += 1
        else:
            neg += 1
        idx.remove(piv)
        for i in idx:
            f = M[i][piv] / p
            for k in range(n):
                M[i][k] -= f * M[piv][k]
        for i in idx:
            M[piv][i] = Fr(0)
            M[i][piv] = Fr(0)
    return pos, neg, zero


def inv(X):
    """inverse of a 1x1 or 2x2 rational matrix"""
    if len(X) == 1:
        return [[1 / X[0][0]]]
    a, b, c, d = X[0][0], X[0][1], X[1][0], X[1][1]
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def opnorm_le(E, bound, strict=False):
    """exact test of ||E|| <= bound (or < bound) for a symmetric 2x2 rational E:
    ||E|| = |tr/2| + sqrt(((a - c)/2)^2 + b^2)"""
    a, b, c = E[0][0], E[0][1], E[1][1]
    room = bound - abs(a + c) / 2
    rad2 = ((a - c) / 2) ** 2 + b * b
    if strict:
        return room > 0 and rad2 < room * room
    return room >= 0 and rad2 <= room * room


def check_N1(rng, fails, n):
    thr_S = Fr(2) if MUT == 'N1' else Fr(2, 5)
    for trial in range(600):
        m = 1 + trial % 2
        lam = rng.fr(1, 20)
        if m == 1:
            D = [[-lam - rng.fr(0, 6)]]
        else:
            t = rng.fr(-2, 2)
            D = [[-lam - abs(t) - rng.fr(0, 6), t], [t, -lam - abs(t) - rng.fr(0, 6)]]
        B = [[rng.fr(-4, 4) for _ in range(2)] for _ in range(m)]
        Di = inv(D)
        BtDiB = [[sum(B[k][i] * Di[k][l] * B[l][j] for k in range(m) for l in range(m)) for j in range(2)] for i in range(2)]
        for site in ('S', 'M'):
            # E with ||E|| <= thr (S) or < 1 (M); every fifth trial is an extreme case
            if site == 'S':
                if trial % 5 == 0:
                    E = [[-thr_S, Fr(0)], [Fr(0), thr_S]]
                else:
                    while True:
                        E0 = [[rng.fr(-1, 1), None], [None, rng.fr(-1, 1)]]
                        E0[0][1] = E0[1][0] = rng.fr(-1, 1)
                        if opnorm_le(E0, thr_S):
                            E = E0
                            break
                base = [[Fr(2), Fr(0)], [Fr(0), Fr(-2)]]
                want = (1, m + 1, 0)
            else:
                if trial % 5 == 0:
                    E = [[1 - Fr(1, 97), Fr(0)], [Fr(0), Fr(1, 3)]]
                else:
                    while True:
                        E0 = [[rng.fr(-1, 1), None], [None, rng.fr(-1, 1)]]
                        E0[0][1] = E0[1][0] = rng.fr(-1, 1)
                        if opnorm_le(E0, Fr(1), strict=True):
                            E = E0
                            break
                base = [[Fr(-2), Fr(0)], [Fr(0), Fr(-2)]]
                want = (0, m + 2, 0)
            red = [[base[i][j] + E[i][j] for j in range(2)] for i in range(2)]
            A = [[red[i][j] + BtDiB[i][j] for j in range(2)] for i in range(2)]
            H = [[A[0][0], A[0][1]] + [B[k][0] for k in range(m)],
                 [A[1][0], A[1][1]] + [B[k][1] for k in range(m)]]
            for k in range(m):
                H.append([B[k][0], B[k][1]] + [D[k][l] for l in range(m)])
            n['N1'] += 1
            # reduced inertia (Weyl) and full inertia (Haynsworth)
            if sym_signs(red) != (want[0], 2 - want[0], 0) or sym_signs(H) != want:
                fails.append(('N1', site, trial, sym_signs(red), sym_signs(H)))


# ----------------------------------------------------------------------------------- Laurent polynomials in s = r^(1/2)
def lp_add(p, q, c=Fr(1)):
    out = dict(p)
    for e, v in q.items():
        out[e] = out.get(e, Fr(0)) + c * v
    return {e: v for e, v in out.items() if v != 0}


def lp_mono(c, e):
    return {e: Fr(c)} if c != 0 else {}


def lp_min_power(p):
    return min(p) if p else None


def check_F1(rng, fails, n):
    # (a) exponent enumeration
    low = set()
    for i in range(5):
        for j in range(5):
            for L in range(5):
                if i + j + L <= 4:
                    ex = Fr(i + j) + Fr(3 * L, 2) - 3
                    if ex < 1:
                        low.add((i, j, L))
    expect = {(i, j, 0) for i in range(4) for j in range(4) if i + j <= 3}
    expect |= {(i, j, 1) for i in range(3) for j in range(3) if i + j <= 2}
    expect |= {(0, 0, 2)}
    n['F1'] += 1
    if low != expect:
        fails.append(('F1-enumeration', sorted(low ^ expect)))
    # (b) symbolic pins along the hard direction, d = 3
    for trial in range(300):
        k = rng.fr(1, 5) / 2
        lam2 = rng.fr(1, 9)
        c = {}
        for a in range(5):
            for b_ in range(5):
                for l in range(5):
                    if a + b_ + l <= 4:
                        c[(a, b_, l)] = rng.fr(-3, 3)
        c[(0, 1, 1)] = Fr(0)               # eigenframe: d_1 d_h f(0) = 0
        c[(0, 0, 2)] = -lam2 / 2           # d_h^2 f(0) = -lambda_2
        # transverse pins along the hard direction: psi_h(x) = sum_a c[a,0,1] x^a vanishes at x = +-r/2, r = s^2.
        # Unknowns c001, c101; with rest(x) = sum_{a >= 2} c[a,0,1] x^a:
        #   c001 = -(rest(-r/2) + rest(r/2))/2,   c101 = (rest(-r/2) - rest(r/2))/r     (Laurent polynomials in s)
        rest_m, rest_p = {}, {}
        for a in range(2, 4 + 1):
            if (a, 0, 1) in c:
                rest_m = lp_add(rest_m, lp_mono(c[(a, 0, 1)] * Fr(-1, 2) ** a, 2 * a))
                rest_p = lp_add(rest_p, lp_mono(c[(a, 0, 1)] * Fr(1, 2) ** a, 2 * a))
        c001 = {e: -v / 2 for e, v in lp_add(rest_m, rest_p).items()}
        c101 = {e - 2: v for e, v in lp_add(rest_m, rest_p, Fr(-1)).items()}
        # [eta^1] F: coefficient of X^a zeta^b eta is c[a,b,1] k^(b-1) s^(2a+2b-3)
        lin = {}
        for (a, b_, l), v in c.items():
            if l != 1:
                continue
            if (a, b_) == (0, 0):
                coef = {e - 3: w / k for e, w in c001.items()}
            elif (a, b_) == (1, 0):
                coef = {e - 1: w / k for e, w in c101.items()}
            else:
                coef = lp_mono(v * k ** (b_ - 1), 2 * a + 2 * b_ - 3)
            lin[(a, b_)] = lp_add(lin.get((a, b_), {}), coef)
        gam_h = 2 * c[(2, 0, 1)]                       # d_u^2 d_h f(0)
        b11 = c[(1, 1, 1)]                             # d_u d_1 d_h f(0)
        c21 = 2 * c[(0, 2, 1)]                         # d_1^2 d_h f(0)
        quarter = Fr(0) if MUT == 'F1' else Fr(1, 4)
        a_poly = {(2, 0): gam_h / (2 * k), (0, 0): -quarter * gam_h / (2 * k), (1, 1): b11, (0, 2): k * c21 / 2}
        for key in set(lin) | set(a_poly):
            diff = lp_add(lin.get(key, {}), lp_mono(a_poly.get(key, Fr(0)), 1), Fr(-1))
            n['F1'] += 1
            mp = lp_min_power(diff)
            if mp is not None and mp < 3:
                fails.append(('F1-linear', trial, key, mp))
                break
        # [eta^2], [eta^3], [eta^4]
        for l, need in ((2, 2), (3, 3), (4, 6)):
            for (a, b_, ll), v in c.items():
                if ll != l:
                    continue
                coef = lp_mono(v * k ** (b_ - 1), 2 * a + 2 * b_ + 3 * l - 6)
                if (l, a, b_) == (2, 0, 0):
                    coef = lp_add(coef, lp_mono(lam2 / (2 * k), 0))      # [eta^2] F + lambda_2/(2k)
                n['F1'] += 1
                mp = lp_min_power(coef)
                if mp is not None and mp < need:
                    fails.append(('F1-eta%d' % l, trial, (a, b_), mp))


# ------------------------------------------------------------------------------------------------------------ raw radii
def check_R1(rng, fails, n):
    cR = Fr(2) if MUT == 'R1' else Fr(17, 6)
    for trial in range(800):
        t = rng.fr(1, 60) / 7                 # t = sqrt(24 lam~)
        gam = rng.fr(-40, 40) / 3
        if gam == 0:
            gam = Fr(1, 3)
        for (u0, u1, zc, c0, cc) in ((Fr(-5, 4), Fr(3, 2), Fr(30), Fr(3, 2), Fr(5, 2)),
                                     (Fr(-5, 2), Fr(3, 2), Fr(34), Fr(5, 2), cR)):
            Zm = zc * abs(gam) / t            # zc / sqrt(psi), sqrt(psi) = t/|gamma|
            bound = c0 + cc * (abs(gam) + 12) / t
            worst = max((u - Z / 12) ** 2 + (Z / gam) ** 2 for u in (u0, u1) for Z in (-Zm, Zm))
            n['R1'] += 1
            if not worst <= bound * bound:
                fails.append(('R1', trial, str(u0)))


# ------------------------------------------------------------------------------------------------------ barrel constants
def check_C1(rng, fails, n):
    fac = 2 if MUT == 'C1' else 4
    for trial in range(800):
        v = rng.fr(1, 40) / 9
        if trial % 4 == 0:
            delta = v * v / 2 - Fr(1, 10 ** 6)
        else:
            delta = rng.fr(0, 1) * (v * v / 2) * Fr(999, 1000)
        eps = Fr(fac) / v
        Lam = v * v - delta
        n['C1'] += 1
        if not (Lam * eps * eps > 8 and Lam * eps / 2 > v):
            fails.append(('C1', trial))


# ----------------------------------------------------------------------- discrete analogue of C96 (periodic grids, d = 2..4)
def grid_neighbours(nn, d):
    N = nn ** d
    nb = []
    for v in range(N):
        coords = []
        x = v
        for _ in range(d):
            coords.append(x % nn)
            x //= nn
        lst = []
        for ax in range(d):
            for st in (-1, 1):
                cc = list(coords)
                cc[ax] = (cc[ax] + st) % nn
                w = 0
                for q in reversed(cc):
                    w = w * nn + q
                lst.append(w)
        nb.append(sorted(set(lst)))
    return nb


def elder_deaths(h, nb, younger=False):
    """superlevel H0 by union-find; returns {birth vertex: death vertex or None}"""
    N = len(h)
    order = sorted(range(N), key=lambda v: -h[v])
    parent = list(range(N))
    root_max = list(range(N))                 # vertex of the maximum of the component (its birth)
    added = [False] * N
    death = {}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for v in order:
        added[v] = True
        roots = sorted({find(w) for w in nb[v] if added[w]}, key=lambda r: -h[root_max[r]])
        if not roots:
            death[v] = None                   # a new class is born at v (a local maximum)
            continue
        keep = roots[-1] if younger else roots[0]
        for r in roots:
            if r != keep:
                death[root_max[r]] = v        # the class of root_max[r] dies at v
                parent[r] = keep
        parent[v] = keep
    return death


def bottleneck(h, nb, M):
    """max over paths from M to a vertex higher than M of the path minimum (widest path); None if none"""
    import heapq
    best = {M: h[M]}
    heap = [(-h[M], M)]
    done = set()
    while heap:
        nv, v = heapq.heappop(heap)
        val = -nv
        if v in done:
            continue
        done.add(v)
        if h[v] > h[M]:
            return val
        for w in nb[v]:
            cand = min(val, h[w])
            if cand > best.get(w, -1):
                best[w] = cand
                heapq.heappush(heap, (-cand, w))
    return None


def check_H1(rng, fails, n):
    for (d, nn, reps) in ((2, 9, 30), (3, 6, 20), (4, 5, 8)):
        nb = grid_neighbours(nn, d)
        N = nn ** d
        for rep in range(reps):
            perm = list(range(N))
            for i in range(N - 1, 0, -1):             # Fisher-Yates with the LCG
                j = rng.below(i + 1)
                perm[i], perm[j] = perm[j], perm[i]
            h = perm
            death = elder_deaths(h, nb, younger=(MUT == 'H1'))
            maxima = [v for v in range(N) if all(h[v] > h[w] for w in nb[v])]
            for M in maxima:
                D = bottleneck(h, nb, M)
                dv = death.get(M)
                n['H1'] += 1
                if D is None:
                    if dv is not None or h[M] != N - 1:
                        fails.append(('H1-global', d, rep, M))
                elif dv is None or h[dv] != D:
                    fails.append(('H1', d, rep, M, D, None if dv is None else h[dv]))


def main():
    rng = Lcg(20261003 + 31)
    fails = []
    n = {k: 0 for k in MUTANTS}
    check_N1(rng, fails, n)
    check_F1(rng, fails, n)
    check_R1(rng, fails, n)
    check_C1(rng, fails, n)
    check_H1(rng, fails, n)
    out = {'object': 'QS addendum A3.1 author-side exact controls', 'counts': n, 'mutant': MUT,
           'all_pass': not fails, 'failures': [str(f) for f in fails[:8]], 'scientific_effect': 'NONE'}
    print(json.dumps(out, sort_keys=True))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
```

Expected stdout:

```json
{"all_pass": true, "counts": {"C1": 800, "F1": 6001, "H1": 1671, "N1": 1200, "R1": 1600}, "failures": [], "mutant": null, "object": "QS addendum A3.1 author-side exact controls", "scientific_effect": "NONE"}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_