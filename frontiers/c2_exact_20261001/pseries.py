"""Exact truncated power series in the separation r, and the pinned two-point structure (NOTE.md section 2).

Field: centred Gaussian on R^d with covariance K(z) = exp(-|z|^2/2), so Cov(d^a f(0), d^b f(0)) = (-1)^|b| d^(a+b) K(0),
d^g K(0) = prod_i (-1)^(g_i/2) (g_i - 1)!! for even g and 0 otherwise.  Points M = -r e1/2, S = +r e1/2.

Every quantity is a linear form in the jets at 0 whose coefficients are power series in r:
    d^beta f(x e1) = sum_j x^j/j! d^(beta + j e1) f(0),   x = -+ r/2.
A Series keeps the coefficients of r^0..r^R exactly (Fractions).  The pin rows divide by r, r and r^3; each division is
exact (the low coefficients vanish identically, which `shift` asserts), and costs at most three orders, so every derived
series is exact through r^(R - 3) = r^7.  The certificate needs r^6 (exact.NR)."""
from fractions import Fraction as Fr

R = 10


class S:
    """a power series c_0 + c_1 r + ... + c_R r^R over Q (higher orders dropped)"""
    __slots__ = ('c',)

    def __init__(self, c=None):
        c = list(c or [])
        self.c = (c + [Fr(0)] * (R + 1))[:R + 1]

    @staticmethod
    def const(x):
        return S([Fr(x)])

    def __add__(self, o):
        if not isinstance(o, S):
            o = S.const(o)
        return S([a + b for a, b in zip(self.c, o.c)])
    __radd__ = __add__

    def __neg__(self):
        return S([-a for a in self.c])

    def __sub__(self, o):
        return self + (-o if isinstance(o, S) else S.const(-o))

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, S):
            return S([a * o for a in self.c])
        out = [Fr(0)] * (R + 1)
        for i, a in enumerate(self.c):
            if a:
                for j in range(R + 1 - i):
                    if o.c[j]:
                        out[i + j] += a * o.c[j]
        return S(out)
    __rmul__ = __mul__

    def inv(self):
        a0 = self.c[0]
        if a0 == 0:
            raise ZeroDivisionError('series with zero constant term')
        out = [Fr(0)] * (R + 1)
        out[0] = 1 / a0
        for n in range(1, R + 1):
            out[n] = -sum(self.c[k] * out[n - k] for k in range(1, n + 1)) / a0
        return S(out)

    def is_zero(self):
        return not any(self.c)


def dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def rho_der(g):
    """d^g K(0) for K = exp(-|z|^2/2)"""
    if any(x % 2 for x in g):
        return 0
    out = 1
    for x in g:
        out *= (-1) ** (x // 2) * dfact(x - 1)
    return out


def cov(u, w):
    """Cov of two linear forms (dict jet -> S)"""
    tot = S()
    for a, sa in u.items():
        for b, sb in w.items():
            v = rho_der(tuple(x + y for x, y in zip(a, b)))
            if v:
                tot = tot + sa * sb * ((-1) ** sum(b) * v)
    return tot


def deriv_at(beta, sign, d):
    """d^beta f at x = sign r/2 along e1, as jets: sum_(j <= R) (sign/2)^j r^j/j! d^(beta + j e1) f(0)"""
    out = {}
    fact = 1
    for j in range(R + 1):
        if j:
            fact *= j
        c = [Fr(0)] * (R + 1)
        c[j] = Fr(sign, 2) ** j / fact
        out[(beta[0] + j,) + tuple(beta[1:])] = S(c)
    return out


def lin(*terms):
    """sum of coef * form"""
    out = {}
    for coef, form in terms:
        for g, s in form.items():
            out[g] = out.get(g, S()) + s * coef
    return {g: s for g, s in out.items() if not s.is_zero()}


def shift(form, p):
    """divide by r^p; the coefficients of r^0..r^(p-1) must vanish identically"""
    out = {}
    for g, s in form.items():
        if any(x != 0 for x in s.c[:p]):
            raise ArithmeticError('inexact division by r^%d at jet %r' % (p, g))
        out[g] = S(s.c[p:])
    return out


def pin_rows(d):
    """The symmetric pin vector U_r of [R] section 2 (Math-#216 c2_check.py Pinned.pin_rows):
        (f(M) + f(S))/2,  (f(S) - f(M))/r,  (f_x(S) - f_x(M))/r,  6/r^2 (f_x(M) + f_x(S) - 2 (f(S) - f(M))/r),
        and for each transverse direction y: (f_y(M) + f_y(S))/2, (f_y(S) - f_y(M))/r.
    Target v_r = (b - k r^3/2, -k r^2, 0, 12 k, 0, ..., 0)."""
    e0 = (0,) * d
    ex = (1,) + (0,) * (d - 1)
    fa, fc = deriv_at(e0, -1, d), deriv_at(e0, 1, d)
    fxa, fxc = deriv_at(ex, -1, d), deriv_at(ex, 1, d)
    rows = [lin((Fr(1, 2), fa), (Fr(1, 2), fc)),
            shift(lin((1, fc), (-1, fa)), 1),
            shift(lin((1, fxc), (-1, fxa)), 1)]
    num = lin((1, fxa), (1, fxc), (-2, shift(lin((1, fc), (-1, fa)), 1)))
    rows.append({g: s * 6 for g, s in shift(num, 2).items()})
    for t in range(1, d):
        ey = tuple(1 if i == t else 0 for i in range(d))
        ya, yc = deriv_at(ey, -1, d), deriv_at(ey, 1, d)
        rows += [lin((Fr(1, 2), ya), (Fr(1, 2), yc)), shift(lin((1, yc), (-1, ya)), 1)]
    return rows


def mat_inv(M):
    """inverse of a square matrix of series whose r^0 part is invertible (Gauss-Jordan over Q[[r]])"""
    n = len(M)
    A = [row[:] + [S.const(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c].c[0] != 0)
        A[c], A[p] = A[p], A[c]
        iv = A[c][c].inv()
        A[c] = [x * iv for x in A[c]]
        for i in range(n):
            if i != c and not A[i][c].is_zero():
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]


def mat_det(M):
    n = len(M)
    A = [row[:] for row in M]
    det = S.const(1)
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c].c[0] != 0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            det = -det
        det = det * A[c][c]
        iv = A[c][c].inv()
        for i in range(c + 1, n):
            if not A[i][c].is_zero():
                f = A[i][c] * iv
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return det


class Pinned:
    """conditional law of linear forms given U_r: mean G v (G[u][j] series), covariance C[(u, w)] (series)"""

    def __init__(self, d, forms):
        self.d = d
        self.rows = pin_rows(d)
        p = len(self.rows)
        self.p = p
        Sm = [[cov(a, b) for b in self.rows] for a in self.rows]
        self.Sinv = mat_inv(Sm)
        self.detS = mat_det(Sm)
        self.names = list(forms)
        CF = {u: [cov(forms[u], row) for row in self.rows] for u in self.names}
        self.G = {u: [sum((CF[u][q] * self.Sinv[q][j] for q in range(p)), S()) for j in range(p)] for u in self.names}
        self.C = {}
        for i, u in enumerate(self.names):
            for w in self.names[i:]:
                val = cov(forms[u], forms[w]) - sum((self.G[u][q] * CF[w][q] for q in range(p)), S())
                self.C[(u, w)] = self.C[(w, u)] = val
