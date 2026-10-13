## QS addendum A3.2: author controls, exact executable and stdout

This publishes the standard-library control script that [A3.2 (5971639141)](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971639141) cites, so anyone can replay it. It checks finite algebra only; it does not prove the lemma.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction and run.** The extraction rule is the same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189).
- `python3 -B -S a32_exact.py`: exit 0, with exactly the stdout below.
- `-O` mode: byte-identical output.
- `--mutant W1`, `W3`, `W4` and `W4r`: each exits 1.
- An unknown argument: exit 2.

The output was produced with Python 3.11.15.

### a32_exact.py

- **File:** 9804 bytes, SHA-256 `52d908650a321cafec5271530789a293b253fd55f21611620e4de8bd3c41bf65`.
- **Stdout:** 353 bytes, SHA-256 `f2f5d0aecd9980e6d782f3ac6d8bbe2ec1d9c03197f38dfc71ca68e57022400f`.

```python
#!/usr/bin/env python3
"""QS addendum A3.2: author-side exact controls for Lemma WF (standard library only; exact rationals).

W1  Chart determinant: for the affine chart Psi(u, Z, eta) = Phi(u - Z/12, Z/gamma, eta),
    Phi(X, zeta, eta) = r X u + r k zeta e1 + r^(3/2) sum eta_i e_i (orthonormal frame; r = s^2 so r^(3/2) = s^3),
    and any symmetric H (the physical Hessian at a pin), g's Hessian D2g = L^T H L/(k r^3) satisfies
        det H = k^(d-2) gamma^2 r^2 det D2g     and     inertia(H) = inertia(D2g)        (d = 3, 4).
W2  Schur: det D2g = det g_hh * det Sigma, Sigma = g_xx - g_xh g_hh^-1 g_hx, and inertia(D2g) = inertia(g_hh) +
    inertia(Sigma) (Haynsworth), for random rational blocks with g_hh negative definite.
W3  Conventions: gamma^4 (psi^2 - c^2) = a_M a_S with psi = 24 lam~/gamma^2, c = 1 - 12 k B/gamma^2,
    a_M a_S = (24 lam~)^2 - (gamma^2 - 12 k B)^2; 144 kappa_M kappa_S = (psi^2 - c^2)/16; and with SC's variables
    (lam~ = -k s, a = gamma, beta = B, B_SC = beta - a^2/(12k)), a_M a_S/16 = 9 k^2 (4 s^2 - B_SC^2).
W4  Theta ranges: det(Q - E)/det Q in [(1 - delta/L0)^m, (1 + delta/L0)^m] for diagonal Q >= L0 I and ||E||_F <= delta
    (m = 1, 2); det(J D2G J)/det(J D2P J) in [(1 - eps/2)^2, (1 + eps/2)^2] for J D2P J = diag(2, -2) or -2I and
    ||E~||_F <= eps < 2.
Mutants: --mutant W1 (r^3 in place of r^2), W3 (12kB -> 6kB), W4 (hard range narrowed to delta/(2 L0)),
W4r (reduced upper end (1 + 0.3536 eps)^2); each exits 1.  W4 also checks the operator-norm extremes that attain
both ends of the reduced range: E~ = eps diag(1, -1), eps diag(-1, 1) at S and -eps I, +eps I at M.
"""
import json
import sys
from fractions import Fraction as Fr

MUT = None
if len(sys.argv) > 1:
    if len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in ('W1', 'W3', 'W4', 'W4r'):
        MUT = sys.argv[2]
    else:
        print(json.dumps({'error': 'unknown arguments'}))
        sys.exit(2)

fails, counts = [], {}


def ok(label, cond, info=None):
    counts[label] = counts.get(label, 0) + 1
    if not cond:
        fails.append((label, info))


seed = 20261003 + 32


def rnd(lo, hi, den=97):
    global seed
    seed = (6364136223846793005 * seed + 1442695040888963407) % (1 << 64)
    return Fr(lo) + Fr((seed >> 11) % (den * (hi - lo) + 1), den)


def det(M):
    M = [list(r) for r in M]
    n = len(M)
    d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return d


def inertia(X):
    M = [list(r) for r in X]
    m = len(M)
    pos = neg = zero = 0
    rest = list(range(m))
    while rest:
        piv = next((i for i in rest if M[i][i] != 0), None)
        if piv is None:
            pair = next(((i, j) for i in rest for j in rest if i < j and M[i][j] != 0), None)
            if pair is None:
                zero += len(rest)
                break
            i, j = pair
            for k in range(m):
                M[i][k] += M[j][k]
            for k in range(m):
                M[k][i] += M[k][j]
            continue
        p = M[piv][piv]
        pos += p > 0
        neg += p < 0
        rest.remove(piv)
        for i in rest:
            f = M[i][piv] / p
            if f:
                for k in range(m):
                    M[i][k] -= f * M[piv][k]
        for i in rest:
            M[piv][i] = M[i][piv] = Fr(0)
    return pos, neg, zero


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def T(A):
    return [list(r) for r in zip(*A)]


def inv(A):
    n = len(A)
    Aug = [list(A[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if Aug[r][c] != 0)
        Aug[c], Aug[p] = Aug[p], Aug[c]
        pv = Aug[c][c]
        Aug[c] = [x / pv for x in Aug[c]]
        for r in range(n):
            if r != c and Aug[r][c] != 0:
                f = Aug[r][c]
                Aug[r] = [x - f * y for x, y in zip(Aug[r], Aug[c])]
    return [row[n:] for row in Aug]


def rand_sym(n, lo=-5, hi=5):
    S = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            S[i][j] = S[j][i] = rnd(lo, hi)
    return S


# ---------------------------------------------------------------- W1 chart determinant
for trial in range(300):
    d = 3 + trial % 2
    s = rnd(1, 3) / 7                        # r = s^2
    r = s * s
    k = rnd(1, 4) / 3
    gam = rnd(-6, 6) / 5
    if gam == 0:
        gam = Fr(1, 5)
    # L = D Psi in the orthonormal frame (u, e1, e2, ...): columns d/du, d/dZ, d/deta_i
    L = [[Fr(0)] * d for _ in range(d)]
    L[0][0] = r                               # d/du: r u
    L[0][1] = -r / 12                         # d/dZ: X-part
    L[1][1] = r * k / gam                     # d/dZ: zeta-part
    for i in range(2, d):
        L[i][i] = s ** 3                      # r^(3/2)
    H = rand_sym(d)
    D2g = [[x / (k * r ** 3) for x in row] for row in matmul(matmul(T(L), H), L)]
    pw = 3 if MUT == 'W1' else 2
    ok('W1-det', det(H) == k ** (d - 2) * gam ** 2 * r ** pw * det(D2g), (d, trial))
    ok('W1-inertia', inertia(H) == inertia(D2g))

# ---------------------------------------------------------------- W2 Schur determinant and inertia
for trial in range(400):
    m = 1 + trial % 2
    A = rand_sym(2)
    B = [[rnd(-4, 4) for _ in range(2)] for _ in range(m)]
    lam = rnd(1, 9)
    if m == 1:
        Dh = [[-lam - rnd(0, 5)]]
    else:
        t = rnd(-2, 2)
        Dh = [[-lam - abs(t) - rnd(0, 5), t], [t, -lam - abs(t) - rnd(0, 5)]]
    full = [A[0] + [B[k][0] for k in range(m)], A[1] + [B[k][1] for k in range(m)]]
    for k in range(m):
        full.append([B[k][0], B[k][1]] + Dh[k])
    Di = inv(Dh)
    Sig = [[A[i][j] - sum(B[p][i] * Di[p][q] * B[q][j] for p in range(m) for q in range(m)) for j in range(2)] for i in range(2)]
    ok('W2-det', det(full) == det(Dh) * det(Sig))
    iS, iD, iF = inertia(Sig), inertia(Dh), inertia(full)
    ok('W2-inertia', iF == tuple(a + b for a, b in zip(iS, iD)))

# ---------------------------------------------------------------- W3 conventions
c12 = 6 if MUT == 'W3' else 12
for trial in range(500):
    k = rnd(1, 5) / 3
    lt = rnd(1, 9) / 4
    gam = rnd(-6, 6) / 5
    if gam == 0:
        gam = Fr(2, 5)
    Bj = rnd(-4, 4) / 3
    psi = 24 * lt / gam ** 2
    c = 1 - c12 * k * Bj / gam ** 2
    aMaS = (24 * lt) ** 2 - (gam ** 2 - 12 * k * Bj) ** 2
    ok('W3-psi-c', gam ** 4 * (psi ** 2 - c ** 2) == aMaS)
    kS, kM = (psi + c) / 48, (psi - c) / 48
    ok('W3-kappa', 144 * kM * kS == (psi ** 2 - c ** 2) / 16)
    s_sc = -lt / k                            # lam~ = -k s
    Bsc = Bj - gam ** 2 / (12 * k)            # beta = B, a = gamma
    ok('W3-SC', aMaS / 16 == 9 * k ** 2 * (4 * s_sc ** 2 - Bsc ** 2))

# ---------------------------------------------------------------- W4 Theta ranges
half = Fr(1, 2) if MUT == 'W4' else Fr(1)          # mutant: a range that is too narrow by the factor 1/2


def hard_ok(ratio, delta, L0, m):
    return (1 - half * delta / L0) ** m <= ratio <= (1 + half * delta / L0) ** m


for trial in range(600):
    m = 1 + trial % 2
    L0 = rnd(1, 9)
    q = [L0 + rnd(0, 5) for _ in range(m)]
    delta = L0 * rnd(0, 1) * Fr(9, 10)
    if trial % 6 == 0:                               # extreme: smallest eigenvalue L0, E = delta e1 e1^T
        q[0] = L0
        E = [[delta if (i == 0 and j == 0) else Fr(0) for j in range(m)] for i in range(m)]
    else:
        E = rand_sym(m, -3, 3)
        fro2 = sum(x * x for row in E for x in row)
        if fro2 == 0:
            continue
        ub = Fr(1)
        while ub * ub < fro2:
            ub *= 2
        E = [[delta / ub * x for x in row] for row in E]   # ||E||_F <= delta
    Q = [[q[i] if i == j else Fr(0) for j in range(m)] for i in range(m)]
    ratio = det([[Q[i][j] - E[i][j] for j in range(m)] for i in range(m)]) / det(Q)
    ok('W4-hard', hard_ok(ratio, delta, L0, m), (trial, m))
    eps = rnd(0, 1) * Fr(19, 10)
    Et = rand_sym(2, -3, 3)
    fro2 = sum(x * x for row in Et for x in row)
    if fro2 == 0:
        continue
    ub = Fr(1)
    while ub * ub < fro2:
        ub *= 2
    Et = [[eps / ub * x for x in row] for row in Et]
    up = Fr(3536, 10000) if MUT == 'W4r' else Fr(1, 2)
    for base in ([[Fr(2), Fr(0)], [Fr(0), Fr(-2)]], [[Fr(-2), Fr(0)], [Fr(0), Fr(-2)]]):
        rr = det([[base[i][j] + Et[i][j] for j in range(2)] for i in range(2)]) / det(base)
        ok('W4-reduced', (1 - eps / 2) ** 2 <= rr <= (1 + up * eps) ** 2)
    # operator-norm extremes (diagonal, operator norm exactly eps): they attain both ends of the range
    for base, ext in (([[Fr(2), Fr(0)], [Fr(0), Fr(-2)]], ((1, -1), (-1, 1))),
                      ([[Fr(-2), Fr(0)], [Fr(0), Fr(-2)]], ((-1, -1), (1, 1)))):
        vals = []
        for sg in ext:
            Ex = [[sg[0] * eps, Fr(0)], [Fr(0), sg[1] * eps]]
            rr = det([[base[i][j] + Ex[i][j] for j in range(2)] for i in range(2)]) / det(base)
            ok('W4-extreme', (1 - eps / 2) ** 2 <= rr <= (1 + up * eps) ** 2)
            vals.append(rr)
        ok('W4-attained', sorted(vals) == sorted([(1 - eps / 2) ** 2, (1 + eps / 2) ** 2]))

out = {'object': 'QS addendum A3.2 author-side exact controls (Lemma WF)', 'counts': counts, 'mutant': MUT,
       'all_pass': not fails, 'failures': [str(f) for f in fails[:6]], 'scientific_effect': 'NONE'}
print(json.dumps(out, sort_keys=True))
sys.exit(0 if not fails else 1)
```

Expected stdout:

```json
{"all_pass": true, "counts": {"W1-det": 300, "W1-inertia": 300, "W2-det": 400, "W2-inertia": 400, "W3-SC": 500, "W3-kappa": 500, "W3-psi-c": 500, "W4-attained": 1198, "W4-extreme": 2396, "W4-hard": 599, "W4-reduced": 1198}, "failures": [], "mutant": null, "object": "QS addendum A3.2 author-side exact controls (Lemma WF)", "scientific_effect": "NONE"}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_