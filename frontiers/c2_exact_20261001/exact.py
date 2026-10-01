"""Exact derivation of c and c2 for the Gaussian kernel, d = 1, 2, 3 (NOTE.md sections 2-3).  Standard library only.

Polynomials (Poly) in (r, b, k, x1, x2) over Q, truncated at r^NR; closed-form numbers (Num)
    sum q * pi^(h/2) * sqrt(m) * theta^e,   q rational, h integer, m squarefree, e in {0, 1},
where theta = M(0, 0) is the one cone atom of d = 3 (section 3.3).  Each coefficient is returned as a Num times one
Gamma atom:  c = Num * Gamma(1/6) 12^(-1/6),  c2 = Num * Gamma(5/6) 12^(-5/6)."""
from fractions import Fraction as Fr
import itertools
import math

import pseries as P

NR = 6
VARS = ('r', 'b', 'k', 'x1', 'x2')
NV = len(VARS)
ONE = (0,) * NV
MUTANT = None


# ------------------------------------------------------------------------------------------- multivariate polynomials
class Poly:
    __slots__ = ('t',)

    def __init__(self, t=None):
        self.t = {e: c for e, c in (t or {}).items() if c}

    @staticmethod
    def var(name, power=1):
        e = [0] * NV
        e[VARS.index(name)] = power
        return Poly({tuple(e): Fr(1)})

    @staticmethod
    def const(c):
        return Poly({ONE: Fr(c)})

    def __add__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(o)
        t = dict(self.t)
        for e, c in o.t.items():
            t[e] = t.get(e, 0) + c
        return Poly(t)
    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.t.items()})

    def __sub__(self, o):
        return self + (-o if isinstance(o, Poly) else Poly.const(-o))

    def __mul__(self, o):
        if not isinstance(o, Poly):
            o = Fr(o)
            return Poly({e: c * o for e, c in self.t.items()})
        t = {}
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                if e1[0] + e2[0] > NR:
                    continue
                e = tuple(a + b for a, b in zip(e1, e2))
                t[e] = t.get(e, 0) + c1 * c2
        return Poly(t)
    __rmul__ = __mul__

    def rcoef(self, n):
        return Poly({(0,) + e[1:]: c for e, c in self.t.items() if e[0] == n})

    def degree(self, name):
        i = VARS.index(name)
        return max((e[i] for e in self.t), default=0)

    def coef_of(self, name, p):
        i = VARS.index(name)
        return Poly({e[:i] + (0,) + e[i + 1:]: c for e, c in self.t.items() if e[i] == p})

    def scalar(self):
        if set(self.t) - {ONE}:
            raise ValueError('not a constant: %r' % (self.t,))
        return self.t.get(ONE, Fr(0))

    def subs(self, name, poly):
        i = VARS.index(name)
        out, powers = Poly(), [Poly.const(1)]
        for e, c in self.t.items():
            while len(powers) <= e[i]:
                powers.append(powers[-1] * poly)
            out = out + Poly({e[:i] + (0,) + e[i + 1:]: c}) * powers[e[i]]
        return out

    def is_zero(self):
        return not self.t


def from_series(s):
    return Poly({(i,) + (0,) * (NV - 1): c for i, c in enumerate(s.c[:NR + 1]) if c})


# ------------------------------------------------------------------------------------------- closed-form numbers
def squarefree(n):
    q, m, p = 1, 1, 2
    while p * p <= n:
        while n % (p * p) == 0:
            n //= p * p
            q *= p
        if n % p == 0:
            n //= p
            m *= p
        p += 1
    return q, m * n


def sqrt_frac(x):
    x = Fr(x)
    if x <= 0:
        raise ValueError('sqrt of a non-positive rational')
    q, m = squarefree(x.numerator * x.denominator)
    return Fr(q, x.denominator), m


class Num:
    __slots__ = ('t',)

    def __init__(self, t=None):
        self.t = {k: v for k, v in (t or {}).items() if v}

    @staticmethod
    def rat(q):
        return Num({(0, 1, 0): Fr(q)})

    @staticmethod
    def sqrt(x):
        q, m = sqrt_frac(x)
        return Num({(0, m, 0): q})

    @staticmethod
    def pi_half(h):
        return Num({(h, 1, 0): Fr(1)})

    def __add__(self, o):
        t = dict(self.t)
        for k, v in o.t.items():
            t[k] = t.get(k, 0) + v
        return Num(t)

    def __neg__(self):
        return Num({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-o)

    def __eq__(self, o):
        return isinstance(o, Num) and not (self - o).t

    def __mul__(self, o):
        if not isinstance(o, Num):
            return Num({k: v * Fr(o) for k, v in self.t.items()})
        t = {}
        for (h1, m1, e1), v1 in self.t.items():
            for (h2, m2, e2), v2 in o.t.items():
                g = math.gcd(m1, m2)
                key = (h1 + h2, (m1 // g) * (m2 // g), e1 + e2)
                t[key] = t.get(key, 0) + v1 * v2 * g
        return Num(t)
    __rmul__ = __mul__

    def text(self):
        parts = []
        for (h, m, e), v in sorted(self.t.items()):
            s = str(v)
            if m != 1:
                s += ' sqrt(%d)' % m
            if h:
                s += ' pi^(%s)' % Fr(h, 2)
            if e:
                s += ' theta' + ('' if e == 1 else '^%d' % e)
            parts.append(s)
        return ' + '.join(parts) if parts else '0'


# ------------------------------------------------------------------------------------------- the kernel A_r
def forms_for(d):
    forms = {}
    for nm, sg in (('M', -1), ('S', 1)):
        for i in range(d):
            for j in range(i, d):
                be = [0] * d
                be[i] += 1
                be[j] += 1
                forms[(nm, i, j)] = P.deriv_at(tuple(be), sg, d)
    trans = []
    for i in range(1, d):
        for j in range(i, d):
            be = [0] * d
            be[i] += 1
            be[j] += 1
            forms[('T', i, j)] = {tuple(be): P.S.const(1)}
            trans.append(('T', i, j))
    return forms, trans


def matchings(lst):
    if not lst:
        yield []
        return
    f, rest = lst[0], lst[1:]
    for mm in matchings(rest):
        yield mm
    for i, y in enumerate(rest):
        for mm in matchings(rest[:i] + rest[i + 1:]):
            yield [(f, y)] + mm


def perm_sign(p):
    return -1 if sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j]) % 2 else 1


def series_pow(x, alpha):
    """(1 + x)^alpha for a Poly x without r^0 part"""
    out, term, coef = Poly.const(1), Poly.const(1), Fr(1)
    for n in range(1, NR + 1):
        coef = coef * (Fr(alpha) - (n - 1)) / n
        term = term * x
        out = out + term * coef
    return out


def series_exp(x):
    out, term = Poly.const(1), Poly.const(1)
    for n in range(1, NR + 1):
        term = term * x * Fr(1, n)
        out = out + term
    return out


def kernel_data(d):
    """A~_r(b, k) = const * [cone integral of exp(-(q0 + Q0)/2) G w] / r^2  (NOTE.md 2.3; the fixed-cone surrogate), with
       w = 1 (d = 1), da over a < 0 (d = 2), (x1 - x2) dx over x2 < x1 < 0 (d = 3; the factor pi is in const)."""
    forms, trans = forms_for(d)
    pin = P.Pinned(d, forms)
    p, nt = pin.p, len(trans)
    r, b, k = Poly.var('r'), Poly.var('b'), Poly.var('k')
    tgt = 11 if MUTANT == 'target' else 12
    v = [b - k * r * r * r * Fr(1, 2), -(k * r * r), Poly(), k * tgt] + [Poly()] * (p - 4)
    mean = {u: sum((from_series(pin.G[u][j]) * v[j] for j in range(p)), Poly()) for u in pin.names}
    hn = [u for u in pin.names if u not in trans]
    if nt:
        CTT = [[pin.C[(x, y)] for y in trans] for x in trans]
        CTTinv = P.mat_inv(CTT)
        detT = P.mat_det(CTT)
        B = {u: [sum((pin.C[(u, trans[j])] * CTTinv[j][i] for j in range(nt)), P.S()) for i in range(nt)] for u in hn}
        cp = {(u, w): from_series(pin.C[(u, w)] - sum((B[u][i] * pin.C[(trans[i], w)] for i in range(nt)), P.S()))
              for u in hn for w in hn}
        tval = {('T', 1, 1): Poly.var('x1'), ('T', 1, 2): Poly(), ('T', 2, 2): Poly.var('x2')}
        zT = [tval[nm] - mean[nm] for nm in trans]
        aff = {u: mean[u] + sum((from_series(B[u][i]) * zT[i] for i in range(nt)), Poly()) for u in hn}
    else:
        CTTinv, detT, zT = [], P.S.const(1), []
        cp = {(u, w): from_series(pin.C[(u, w)]) for u in hn for w in hn}
        aff = dict((u, mean[u]) for u in hn)
    F = Poly()          # E[det H_M det H_S | T, U_r = v_r] by Isserlis
    for pp in itertools.permutations(range(d)):
        for qq in itertools.permutations(range(d)):
            fac = [('M', min(i, pp[i]), max(i, pp[i])) for i in range(d)] + \
                  [('S', min(i, qq[i]), max(i, qq[i])) for i in range(d)]
            sg = perm_sign(pp) * perm_sign(qq)
            for mt in matchings(list(range(2 * d))):
                used = set(i for pr in mt for i in pr)
                c = Poly.const(sg)
                for (i, j) in mt:
                    c = c * cp[(fac[i], fac[j])]
                for i in range(2 * d):
                    if i not in used:
                        c = c * aff[fac[i]]
                F = F + c
    q = sum((v[i] * from_series(pin.Sinv[i][j]) * v[j] for i in range(p) for j in range(p)), Poly())
    Q = sum((zT[i] * from_series(CTTinv[i][j]) * zT[j] for i in range(nt) for j in range(nt)), Poly())
    q0, Q0 = q.rcoef(0), Q.rcoef(0)
    detS0, detT0 = pin.detS.c[0], detT.c[0]
    ratio = from_series(pin.detS) * (1 / detS0) * from_series(detT) * (1 / detT0) - Poly.const(1)
    G = series_pow(ratio, Fr(-1, 2)) * series_exp(((q - q0) + (Q - Q0)) * Fr(-1, 2)) * F
    nn = p + nt
    const = Num.rat(-12) * Num.sqrt(Fr(1, 2 ** nn)) * Num.pi_half(-nn) * Num.sqrt(Fr(1) / (detS0 * detT0))
    if d == 3:
        const = const * Num.pi_half(2)
    return {'G': G, 'q0': q0, 'Q0': Q0, 'const': const, 'p': p, 'detS0': detS0, 'detT0': detT0, 'F': F}


# ------------------------------------------------------------------------------------------- the integrations
SPHERE = {1: Num.rat(2), 2: Num.pi_half(2) * 2, 3: Num.pi_half(2) * 4}


def half_moment(j, c):
    """int_0^oo t^j e^(-c t^2) dt = Gamma((j+1)/2) c^(-(j+1)/2)/2 (c > 0 rational)"""
    if j % 2 == 0:
        g = Fr(1)
        for i in range(j // 2):
            g *= Fr(2 * i + 1, 2)
        return Num.pi_half(1) * Num.sqrt(Fr(1) / c) * (g / c ** (j // 2) / 2)
    m = (j + 1) // 2
    return Num.rat(Fr(math.factorial(m - 1)) / c ** m / 2)


def quadrant_moments(al, be, ga, nmax):
    """M(i, j) = int int_(s, t > 0) s^i t^j exp(-(al s^2 + be s t + ga t^2)) ds dt, i + j <= nmax, from
    (i)  2 al M(i+1, j) + be M(i, j+1) = i M(i-1, j) + [i = 0] H_j(ga),
    (ii) be M(i+1, j) + 2 ga M(i, j+1) = j M(i, j-1) + [j = 0] H_i(al)     (H the half-line moments),
    integration by parts in s and in t.  M(0, 0) = theta = (pi/2 - arctan(be/sqrt(D)))/sqrt(D), D = 4 al ga - be^2.
    Every M(i+1, j) with j >= 1 is reached twice (from (i, j) and from (i+1, j-1)); the two values must agree."""
    D = 4 * al * ga - be * be
    if not (D > 0 and al > 0 and ga > 0):
        raise ValueError('cone exponent not positive definite')
    M = {(0, 0): Num({(0, 1, 1): Fr(1)})}
    for n in range(nmax):
        for i in range(n + 1):
            j = n - i
            R1 = (M[(i - 1, j)] * i if i else half_moment(j, ga))
            R2 = (M[(i, j - 1)] * j if j else half_moment(i, al))
            vals = (((i + 1, j), (R1 * (2 * ga) - R2 * be) * (Fr(1) / D)),
                    ((i, j + 1), (R2 * (2 * al) - R1 * be) * (Fr(1) / D)))
            for key, val in vals:
                if key in M:
                    if not M[key] == val:
                        raise ArithmeticError('quadrant recurrence inconsistent at %r' % (key,))
                else:
                    M[key] = val
    return M, D


def gamma_ratio(a, a0):
    """Gamma(a)/Gamma(a0) for a - a0 an integer (exact)"""
    out, x = Fr(1), Fr(a0)
    while x < a:
        out *= x
        x += 1
    while x > a:
        x -= 1
        out /= x
    return out


def coefficient(d, which, data=None):
    """which = 0: c = (|S^(d-1)|/3) int db int_0^oo A_0 k^(-2/3) dk;
       which = 2: c2 = (|S^(d-1)|/3) int db f.p. int_0^oo A_2 k^(-4/3) dk  (the finite part = the subtraction of A_2(b, 0)).
    Returns (Num, Gamma atom, info)."""
    D_ = data or kernel_data(d)
    G = D_['G']
    for n in (0, 1):
        if not G.rcoef(n).is_zero():
            raise ArithmeticError('integrand does not vanish to order r^2')
    if not G.rcoef(3).is_zero():
        raise ArithmeticError('A_r has an r^1 term')
    H = G.rcoef(which + 2)
    E = (D_['q0'] + D_['Q0']) * Fr(1, 2)
    # --- k: E = ak k^2 + (k-free part)
    ak = E.coef_of('k', 2).scalar()
    if not (E.coef_of('k', 1).is_zero() and E.degree('k') == 2 and ak == 12):
        raise ArithmeticError('unexpected k-dependence of the exponent')
    a0 = Fr(1, 6) if which == 0 else Fr(5, 6)
    expo = Fr(-2, 3) if which == 0 else Fr(-4, 3)
    Hk = Poly()
    for j in range(H.degree('k') + 1):
        cj = H.coef_of('k', j)
        if cj.is_zero():
            continue
        if j % 2:
            raise ArithmeticError('odd power of k')
        # int_0^oo k^(j + expo) e^(-12 k^2) dk (finite part) = Gamma(a) 12^(-a)/2,  a = (j + expo + 1)/2
        a = (j + expo + 1) / 2
        if MUTANT == 'finite-part' and j == 0 and which == 2:
            a = a0                       # drops the subtraction of A_2(b, 0): Gamma(-1/6) replaced by Gamma(5/6)
        shift = a - a0
        Hk = Hk + cj * (gamma_ratio(a, a0) * Fr(12) ** (-int(shift)) / 2)
    katom = 'Gamma(1/6) 12^(-1/6)' if which == 0 else 'Gamma(5/6) 12^(-5/6)'
    # --- b: k-free exponent = ab b^2 + b L(x) + R(x); complete the square
    Ek = E.coef_of('k', 0)
    ab = Ek.coef_of('b', 2).scalar()
    if Ek.degree('b') != 2:
        raise ArithmeticError('exponent not quadratic in b')
    Lx, Rx = Ek.coef_of('b', 1), Ek.coef_of('b', 0)
    shifted = Hk.subs('b', Poly.var('b') - Lx * (Fr(1) / (2 * ab)))
    Hb = {}
    for e, c in shifted.t.items():
        if e[1] % 2:
            continue
        key = e[3:]
        Hb[key] = Hb.get(key, Num()) + half_moment(e[1], ab) * (2 * c)
    if not Hb:
        raise ArithmeticError('empty integrand: the r-truncation is too low')
    Ex = Rx - Lx * Lx * (Fr(1) / (4 * ab))
    total, info = Num(), {}
    if d == 1:
        if not Ex.is_zero():
            raise ArithmeticError('d = 1: residual exponent')
        for val in Hb.values():
            total = total + val
    elif d == 2:
        g = Ex.coef_of('x1', 2).scalar()
        if not (Ex.degree('x1') == 2 and Ex.coef_of('x1', 1).is_zero() and Ex.coef_of('x1', 0).is_zero()):
            raise ArithmeticError('d = 2: cone exponent')
        for key, val in Hb.items():
            total = total + val * half_moment(key[0], g) * (-1) ** key[0]       # int over a < 0
        info['gamma_a'] = g
    else:
        X1, X2 = -Poly.var('x1'), -Poly.var('x1') - Poly.var('x2')    # x1 = -s, x2 = -s - t  (s -> x1, t -> x2 slots)

        def subst(poly):
            out = Poly()
            for e, c in poly.t.items():
                term = Poly({e[:3] + (0, 0): c})
                for _ in range(e[3]):
                    term = term * X1
                for _ in range(e[4]):
                    term = term * X2
                out = out + term
            return out
        Est = subst(Ex)
        al = Est.coef_of('x1', 2).coef_of('x2', 0).scalar()
        ga = Est.coef_of('x2', 2).coef_of('x1', 0).scalar()
        be = Est.coef_of('x1', 1).coef_of('x2', 1).scalar()
        chk = Poly.var('x1', 2) * al + Poly.var('x1') * Poly.var('x2') * be + Poly.var('x2', 2) * ga
        if not (Est - chk).is_zero():
            raise ArithmeticError('d = 3: cone exponent not a quadratic form')
        nmax = max(key[0] + key[1] for key in Hb) + 2
        M, Dc = quadrant_moments(al, -be if MUTANT == 'cone-sign' else be, ga, nmax)
        for key, val in Hb.items():
            mono = subst(Poly({(0, 0, 0) + key: Fr(1)})) * Poly.var('x2')           # weight x1 - x2 = t
            for e, c in mono.t.items():
                total = total + val * M[(e[3], e[4])] * c
        info.update({'alpha': al, 'beta': be, 'gamma': ga, 'D': Dc})
    value = SPHERE[d] * Fr(1, 3) * D_['const'] * total
    return value, katom, info
