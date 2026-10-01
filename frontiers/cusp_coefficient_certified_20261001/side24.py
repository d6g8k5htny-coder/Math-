"""Lemma S: (CU.2) for the [P] torus field of side L >= 24, in particular SIDE24 (NOTE.md section 3b).  Exact rational
arithmetic only.

The [P] field of side L has covariance K_L(z) = sum_n phi(z + L n) / S_L, phi(x) = exp(-|x|^2/2), S_L = sum_n phi(L n)
(the normalization of coefficients/side24_v1; the unnormalized periodization is covered too).  In an orthonormal frame
(u, Theta) the jets entering (CU.2) are the 2d + 2 pinned coordinates (f, d_u f, d_u^2 f, d_u^3 f, grad_Theta f,
grad_Theta d_u f) and the free ones (d_u^4 f, gamma = grad_Theta d_u^2 f, A = D_Theta^2 f).  Every covariance entry is
(-1)^|b| D^(|a|+|b|) K(0) contracted with frame vectors, of total order at most 8.

S.1 (image bound).  For unit vectors v_1..v_q, D^q phi(x)[v] = phi(x) sum over partial matchings of products of
    -<v_i, v_j> and -<x, v_i>, so |D^q phi(x)[v]| <= phi(x) sum_j q! |x|^(q-2j)/(2^j j! (q-2j)!).  For q <= 8 this is at most
    T_8 |x|^8 phi(x) when |x| >= 1 (T_8 = 764 matchings of 8 points), and at most 7!! = 105 at x = 0.  For d <= 3 the shell
    max|n_i| = j has at most 27 j^3 points with |n|^2 <= 3 j^2, and consecutive shell terms shrink by at least 1/2, so
        sum_(n != 0) |n|^8 e^(-288 |n|^2) <= 2 . 27 . 81 e^(-288),     S_24 - 1 <= 2 . 27 e^(-288),     e^(-288) < 10^-125.
    L^8 e^(-L^2 |n|^2/2) decreases in L for L |n| >= 3, so the bound at L = 24 holds for every L >= 24.  Hence every entry of
    C_L - C_0 has absolute value at most E = (764 . 24^8 . 4374 + 105 . 54) 10^-125.
S.2 (sandwich).  C_0 - mu I is positive definite (exact LDL^T), so |x^T (C_L - C_0) x| <= N E |x|^2 <= eps x^T C_0 x with
    eps = N E / mu, i.e. (1 - eps) C_0 <= C_L <= (1 + eps) C_0 in every frame.
S.3 (transfer).  On the slice where 2d + 1 coordinates vanish, the (CU.2) integrand is a nonnegative function of the free
    jets, homogeneous of degree 2d - 1/4, so the slice integral at a C_0 is a^(-5/8) times the one at C_0.  The density
    sandwich [(1 - eps)/(1 + eps)]^(N/2) phi_((1-eps) C_0) <= phi_(C_L) <= [(1 + eps)/(1 - eps)]^(N/2) phi_((1+eps) C_0)
    then gives c1^(L)/c1^(ref) in [rho^-M, rho^M], rho = (1 + eps)/(1 - eps), M = N/2 + 1.  Since log rho <= 4 eps and
    e^x <= 1 + 2x on [0, 1], this is within eta = 8 M eps of 1."""
import json
import os
from fractions import Fraction as Fr
from itertools import combinations

L_MIN = 24
IMAGE_ORDER = 8        # S.1 covers contractions of total order <= IMAGE_ORDER
MU = Fr(1, 4)          # certified lower bound of the smallest eigenvalue of C_0 (S.2)

# c_(d,24) of coefficients/side24_v1/ENCLOSURE.json ("dimensions"), consumed (SOURCE_MAP.json [SIDE24-E]).
C_24 = {2: ('0.07340691930603427103', '0.07340691930603427104'),
        3: ('0.04177593184059834334', '0.04177593184059834335')}


def _dfact(n):
    """(n - 1)!! for even n >= 0: the number of perfect matchings of n points."""
    r = 1
    for k in range(n - 1, 0, -2):
        r *= k
    return r


def dK0(g):
    """D^g phi(0) for the multi-index g: prod (-1)^(g_i/2) (g_i - 1)!! if every g_i is even, else 0."""
    if any(x % 2 for x in g):
        return 0
    r = 1
    for x in g:
        r *= (-1) ** (x // 2) * _dfact(x)
    return r


def jets(d):
    """The jets of (CU.2) in the frame (u = e_1, Theta = e_2..e_d): name, multi-index, role."""
    out = []
    for k in range(5):
        out.append(('d_u^%d f' % k, (k,) + (0,) * (d - 1), 'b' if k == 0 else ('pin' if k < 4 else 'free')))
    for j in range(1, d):
        for k in range(3):
            g = [0] * d
            g[0], g[j] = k, 1
            out.append(('d_y%d d_u^%d f' % (j, k), tuple(g), 'pin' if k < 2 else 'free'))
    for j in range(1, d):
        for k in range(j, d):
            g = [0] * d
            g[j] += 1
            g[k] += 1
            out.append(('d_y%d d_y%d f' % (j, k), tuple(g), 'free'))
    return out


def cov0(d):
    """Exact covariance of the jets for phi: Cov(D^a f, D^b f) = (-1)^|b| D^(a+b) phi(0)."""
    J = jets(d)
    return [[Fr((-1) ** sum(b) * dK0(tuple(x + y for x, y in zip(a, b)))) for _, b, _ in J] for _, a, _ in J]


def max_order(d):
    J = jets(d)
    return max(sum(a) + sum(b) for _, a, _ in J for _, b, _ in J)


def ldl_positive(M):
    """True iff the symmetric rational matrix M is positive definite (exact LDL^T: every pivot > 0)."""
    n = len(M)
    A = [row[:] for row in M]
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            if f:
                for j in range(k, n):
                    A[i][j] -= f * A[k][j]
    return True


def matchings(q):
    """Number of partial matchings (involutions) of q points, by enumeration: T_q."""
    def count(pts):
        if not pts:
            return 1
        first, rest = pts[0], pts[1:]
        tot = count(rest)
        for i in range(len(rest)):
            tot += count(rest[:i] + rest[i + 1:])
        return tot
    return count(tuple(range(q)))


def exp_lower(x, K=20):
    """A lower bound of e^x for rational x > 0: the positive Taylor sum through x^K/K!."""
    s, t = Fr(0), Fr(1)
    for k in range(K + 1):
        s += t
        t = t * x / (k + 1)
    return s


def image_bound():
    """E of S.1 (exact rational) after checking its numeric premises."""
    if not exp_lower(Fr(288, 125)) > 10:                      # e^(-288) < 10^-125
        raise ValueError('e^(288/125) > 10 not certified')
    e288 = Fr(1, 10 ** 125)
    if not 2 ** 11 * e288 ** 3 < Fr(1, 2) or not 2 ** 3 * e288 ** 3 < Fr(1, 2):
        raise ValueError('shell ratio bound fails')            # e^(-864) < 10^-375
    T = matchings(IMAGE_ORDER)
    dfmax = max(_dfact(q) for q in range(0, IMAGE_ORDER + 1, 2))
    lattice = 2 * 27 * 3 ** (IMAGE_ORDER // 2)                  # sum |n|^q e^(-288|n|^2) <= 2 . 27 . 3^(q/2) e^(-288)
    norm = 2 * 27                                               # S_24 - 1 <= 2 . 27 e^(-288)
    return (T * L_MIN ** IMAGE_ORDER * lattice + dfmax * norm) * e288


def transfer(d):
    """S.2 and S.3 for dimension d: the exact constants and eta."""
    C0 = cov0(d)
    N = len(C0)
    if max_order(d) > IMAGE_ORDER:
        raise ValueError('covariance entries of order %d exceed the image bound order %d' % (max_order(d), IMAGE_ORDER))
    if not ldl_positive([[C0[i][j] - (MU if i == j else 0) for j in range(N)] for i in range(N)]):
        raise ValueError('C_0 - mu I is not positive definite')
    E = image_bound()
    eps = N * E / MU
    M = Fr(N, 2) + 1
    if not 4 * M * eps <= 1:
        raise ValueError('eps too large for the bound e^x <= 1 + 2x')
    eta = 8 * M * eps
    return {'N': N, 'E': E, 'mu': MU, 'eps': eps, 'M': M, 'eta': eta}


def lemma_r_check(d):
    """Exact regression from C_0: the conditional law of the free jets given the pins, against Lemma R.1, and the pin
    density constants det C_P = 12, (C_P^-1)_(f,f) = 3/2.  Returns a list of failures."""
    J = jets(d)
    C0 = cov0(d)
    P = [i for i, j in enumerate(J) if j[2] in ('b', 'pin')]
    F = [i for i, j in enumerate(J) if j[2] == 'free']
    CP = [[C0[i][j] for j in P] for i in P]
    n = len(P)
    # exact inverse of C_P by Gauss-Jordan
    A = [CP[i][:] + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    det = Fr(1)
    for k in range(n):
        piv = next(r for r in range(k, n) if A[r][k] != 0)
        if piv != k:
            A[k], A[piv] = A[piv], A[k]
            det = -det
        det *= A[k][k]
        p = A[k][k]
        A[k] = [x / p for x in A[k]]
        for r in range(n):
            if r != k and A[r][k] != 0:
                f = A[r][k]
                A[r] = [x - f * y for x, y in zip(A[r], A[k])]
    inv = [row[n:] for row in A]
    fails = []
    if det != 12:
        fails.append('d = %d: det C_P = %s, expected 12' % (d, det))
    if inv[0][0] != Fr(3, 2):
        fails.append('d = %d: (C_P^-1)_ff = %s, expected 3/2' % (d, inv[0][0]))
    # regression coefficients on the b coordinate (pins at 0): mean = Cov(W, P) C_P^-1 e_b b; covariance = Schur complement
    CFP = [[C0[i][j] for j in P] for i in F]
    mean_b = [sum(CFP[r][k] * inv[k][0] for k in range(n)) for r in range(len(F))]
    schur = [[C0[F[r]][F[s]] - sum(CFP[r][k] * inv[k][l] * CFP[s][l] for k in range(n) for l in range(n))
              for s in range(len(F))] for r in range(len(F))]
    names = [J[i][0] for i in F]
    m = d - 1
    exp_mean, exp_cov = {}, {}
    exp_mean['d_u^4 f'] = -3
    exp_cov[('d_u^4 f', 'd_u^4 f')] = 24
    for j in range(1, d):
        exp_mean['d_y%d d_u^2 f' % j] = 0
        exp_cov[('d_y%d d_u^2 f' % j, 'd_y%d d_u^2 f' % j)] = 2
        exp_mean['d_y%d d_y%d f' % (j, j)] = -1
        exp_cov[('d_y%d d_y%d f' % (j, j), 'd_y%d d_y%d f' % (j, j))] = 2
        for k in range(j + 1, d):
            exp_mean['d_y%d d_y%d f' % (j, k)] = 0
            exp_cov[('d_y%d d_y%d f' % (j, k), 'd_y%d d_y%d f' % (j, k))] = 1
    for r, a in enumerate(names):
        if mean_b[r] != exp_mean[a]:
            fails.append('d = %d: E[%s | b] = %s b, expected %s b' % (d, a, mean_b[r], exp_mean[a]))
        for s, b in enumerate(names):
            want = exp_cov.get((a, b), exp_cov.get((b, a), 0))
            if schur[r][s] != want:
                fails.append('d = %d: Cov(%s, %s | pins) = %s, expected %s' % (d, a, b, schur[r][s], want))
    if m != len([1 for a in names if a.endswith('d_u^2 f')]):
        fails.append('d = %d: gamma has the wrong dimension' % d)
    return fails


def enclosure_check(here):
    """Compare C_24 with the repository copy of coefficients/side24_v1/ENCLOSURE.json when it is reachable."""
    path = os.path.join(here, '..', '..', 'coefficients', 'side24_v1', 'ENCLOSURE.json')
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        dims = json.load(fh)['dimensions']
    bad = []
    for d, (lo, hi) in C_24.items():
        if (dims[str(d)]['lower'], dims[str(d)]['upper']) != (lo, hi):
            bad.append('c_(%d,24) transcription differs from ENCLOSURE.json' % d)
    return bad
