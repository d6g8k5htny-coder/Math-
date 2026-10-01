"""The integrands of CL-CU-CUSP-COEFFICIENT-20261001, written once against an operations object:
RealOps (sharp real intervals, for the quadrature sums) and CplxOps (complex boxes, for the Bernstein-ellipse bounds).

d = 2 (NOTE.md section 3).  With omega = u^4 and
    H(omega) = (1 + i omega)^(-1/2) (1 - i omega/3 + 19 omega^2/36)^(-5/8),
let R = Re log H and I = Im log H.  Then
    R/omega^2 = -(1/4) L(omega^2) - (5/16) q L(omega^2 q),        q = 7/6 + 361 omega^2/1296,
    I/omega   = -(1/2) A(omega) + (5/8) A(omega/v)/v,              v = 3 + 19 omega^2/12,
and
    g2(u) = (1 - Re H)/omega^2 = -E1(R) (R/omega^2) + e^R Sinc(I/2)^2 (I/omega)^2/2.
Moreover J = 4 C0 int_0^oo g2(u) du with C0 = (3/16)^(-5/8).

d = 3 (NOTE.md section 4).  With a1 = s^4 >= a2 = a1 v^4 the transverse eigenvalue moduli and omega = t^4/a1:
    Rt = -(1/4)(L(t^8) + v^8 L(t^8 v^8)) - 23 a1^2 v^8/240,         R = t^8 Rt,
    It =  (1/2)(A(t^4) + v^4 A(t^4 v^4)) - a1^2 v^4 (1 + v^4)/20,   I = t^4 It,
    Gt = -E1(R) Rt + e^R Sinc(I/2)^2 It^2/2,
    f3(s, v, t) = s^20 v^4 (1 - v^4) exp(-s^8 (2 v^8 - v^4 + 2)/10) Gt.
Moreover T3 = 64 int_0^oo ds int_0^1 dv int_0^oo dt f3."""
from fractions import Fraction as Fr
from ia import dn, up, add, sub, neg, mul, div, sqr, pw, from_frac
import elem as EL
import cx as CX

_CONST = {}
MUTANT = None          # 'phase-sign' flips the sign of the a1^2 phase term of f3 (certificate.py mutants)


def _c(q):
    q = Fr(q)
    r = _CONST.get(q)
    if r is None:
        r = from_frac(q)
        _CONST[q] = r
    return r


class RealOps:
    @staticmethod
    def c(q):
        return _c(q)
    add = staticmethod(add)
    sub = staticmethod(sub)
    mul = staticmethod(mul)
    div = staticmethod(div)
    neg = staticmethod(neg)
    sq = staticmethod(sqr)
    pw = staticmethod(pw)
    exp = staticmethod(EL.exp_iv)
    E1 = staticmethod(EL.E1_iv)
    L = staticmethod(EL.L_iv)
    A = staticmethod(EL.A_iv)
    Sinc = staticmethod(EL.Sinc_iv)


class CplxOps:
    @staticmethod
    def c(q):
        return (_c(q), (0.0, 0.0))
    add = staticmethod(CX.cadd)
    sub = staticmethod(CX.csub)
    mul = staticmethod(CX.cmul)
    div = staticmethod(CX.cdiv)

    @staticmethod
    def neg(z):
        return (neg(z[0]), neg(z[1]))

    @staticmethod
    def sq(z):
        return CX.cmul(z, z)
    pw = staticmethod(CX.cpow)
    exp = staticmethod(CX.cexp)
    E1 = staticmethod(CX.E1c)
    L = staticmethod(CX.Lc)
    A = staticmethod(CX.Ac)
    Sinc = staticmethod(CX.Sincc)


def _G(o, R, I, Rt, It):
    t1 = o.neg(o.mul(o.E1(R), Rt))
    t2 = o.mul(o.mul(o.exp(R), o.sq(o.Sinc(o.mul(o.c(Fr(1, 2)), I)))), o.mul(o.c(Fr(1, 2)), o.sq(It)))
    return o.add(t1, t2)


def g2(o, u):
    w = o.pw(u, 4)
    w2 = o.pw(u, 8)
    q = o.add(o.c(Fr(7, 6)), o.mul(o.c(Fr(361, 1296)), w2))
    Rt = o.neg(o.add(o.mul(o.c(Fr(1, 4)), o.L(w2)), o.mul(o.mul(o.c(Fr(5, 16)), q), o.L(o.mul(w2, q)))))
    v = o.add(o.c(3), o.mul(o.c(Fr(19, 12)), w2))
    It = o.sub(o.mul(o.c(Fr(5, 8)), o.div(o.A(o.div(w, v)), v)), o.mul(o.c(Fr(1, 2)), o.A(w)))
    return _G(o, o.mul(w2, Rt), o.mul(w, It), Rt, It)


def f3(o, s, v, t):
    s4 = o.pw(s, 4)
    s8 = o.pw(s, 8)
    v4 = o.pw(v, 4)
    v8 = o.pw(v, 8)
    t4 = o.pw(t, 4)
    t8 = o.pw(t, 8)
    Rt = o.neg(o.add(o.mul(o.c(Fr(1, 4)), o.add(o.L(t8), o.mul(v8, o.L(o.mul(t8, v8))))),
                     o.mul(o.c(Fr(23, 240)), o.mul(s8, v8))))
    ph = o.mul(o.c(Fr(1, 20)), o.mul(o.mul(s8, v4), o.add(o.c(1), v4)))
    half = o.mul(o.c(Fr(1, 2)), o.add(o.A(t4), o.mul(v4, o.A(o.mul(t4, v4)))))
    It = o.add(half, ph) if MUTANT == 'phase-sign' else o.sub(half, ph)
    G = _G(o, o.mul(t8, Rt), o.mul(t4, It), Rt, It)
    E = o.mul(o.c(Fr(1, 10)), o.add(o.sub(o.mul(o.c(2), v8), v4), o.c(2)))
    wgt = o.mul(o.mul(o.pw(s, 20), o.mul(v4, o.sub(o.c(1), v4))), o.exp(o.neg(o.mul(s8, E))))
    return o.mul(wgt, G)


# ---------------------------------------------------------------- direct bounds for the Bernstein ellipses
# On the real axis Re H = (H + H*)/2 with H*(w) = conj(H(conj w)), so the analytic continuation of g2 is
# D(u) = (1 - (H(w) + H*(w))/2)/w^2, w = u^4, with principal powers.  It is analytic wherever no base of a principal
# power meets the closed half-line (-oo, 0] and w != 0.  For a real exponent, |z^a| = |z|^a, hence
#     |D(u)| <= (1 + (|H(w)| + |H*(w)|)/2)/|w|^2.
# A box passes _off_cut when it cannot meet (-oo, 0].  When every box covering an ellipse passes, D is analytic on
# the ellipse and equals the integrand there (both are analytic and agree on the real panel).  The same holds for the
# d = 3 direct form.

def _off_cut(z):
    return z[0][0] > 0.0 or z[1][0] > 0.0 or z[1][1] < 0.0


def _pow_abs_up(z, a):
    """Upper bound of |z|^a over a box, a real; requires |z| > 0 when a < 0."""
    lo, hi = CX.cabs_dn(z), CX.cabs_up(z)
    if a < 0:
        if not lo > 0.0:
            raise ZeroDivisionError('modulus may vanish')
        return EL.exp_iv(mul(_c(Fr(a)), EL.log_iv((lo, lo))))[1]
    return EL.exp_iv(mul(_c(Fr(a)), EL.log_iv((hi, hi))))[1]


def g2_bound_direct(u):
    """Upper bound of |D(u)| over the complex box u (raises if the branch conditions cannot be certified)."""
    w = CX.cpow(u, 4)
    iw = CX.cmul(((0.0, 0.0), (1.0, 1.0)), w)
    one = ((1.0, 1.0), (0.0, 0.0))
    w2 = CX.cpow(u, 8)
    quad = CX.cscal(_c(Fr(19, 36)), w2)
    third = CX.cscal(_c(Fr(1, 3)), iw)
    bases_h = (CX.cadd(one, iw), CX.cadd(CX.csub(one, third), quad))
    bases_hs = (CX.csub(one, iw), CX.cadd(CX.cadd(one, third), quad))
    for b in bases_h + bases_hs:
        if not _off_cut(b):
            raise ValueError('branch condition not certified')
    habs = up(_pow_abs_up(bases_h[0], -0.5) * _pow_abs_up(bases_h[1], -0.625))
    hsabs = up(_pow_abs_up(bases_hs[0], -0.5) * _pow_abs_up(bases_hs[1], -0.625))
    num = up(1.0 + up(0.5 * up(habs + hsabs)))
    wmin = CX.cabs_dn(w)
    if not wmin > 0.0:
        raise ZeroDivisionError('w may vanish')
    return up(num / dn(wmin * wmin))


def f3_bound_direct(s, v, t):
    """Upper bound of the modulus of the d = 3 integrand's direct continuation over complex boxes (s, v, t):
    f3 = wgt (1 - (Phi + Phi*)/2)/t^8,
    Phi = (1 - i t^4)^(-1/2) (1 - i t^4 v^4)^(-1/2) exp(-i t^4 c1 - t^8 c2),
    c1 = a1^2 v^4 (1 + v^4)/20, c2 = 23 a1^2 v^8/240, a1 = s^4, and Phi* takes i -> -i."""
    one = ((1.0, 1.0), (0.0, 0.0))
    ii = ((0.0, 0.0), (1.0, 1.0))
    s4, s8 = CX.cpow(s, 4), CX.cpow(s, 8)
    v4, v8 = CX.cpow(v, 4), CX.cpow(v, 8)
    t4, t8 = CX.cpow(t, 4), CX.cpow(t, 8)
    c1 = CX.cscal(_c(Fr(1, 20)), CX.cmul(CX.cmul(s8, v4), CX.cadd(one, v4)))
    c2 = CX.cscal(_c(Fr(23, 240)), CX.cmul(s8, v8))
    it4 = CX.cmul(ii, t4)
    it4v4 = CX.cmul(it4, v4)
    total = 0.0
    for sign in (1, -1):
        b1 = CX.csub(one, it4) if sign == 1 else CX.cadd(one, it4)
        b2 = CX.csub(one, it4v4) if sign == 1 else CX.cadd(one, it4v4)
        for b in (b1, b2):
            if not _off_cut(b):
                raise ValueError('branch condition not certified')
        ex = CX.csub(CX.cscal((-float(sign), -float(sign)), CX.cmul(it4, c1)), CX.cmul(t8, c2))
        mod = up(up(_pow_abs_up(b1, -0.5) * _pow_abs_up(b2, -0.5)) * EL.exp_iv(ex[0])[1])
        total = up(total + mod)
    num = up(1.0 + up(0.5 * total))
    tmin = CX.cabs_dn(t4)
    if not tmin > 0.0:
        raise ZeroDivisionError('t may vanish')
    G = up(num / dn(tmin * tmin))
    E = CX.cscal(_c(Fr(1, 10)), CX.cadd(CX.csub(CX.cscal((2.0, 2.0), v8), v4), CX.cscal((2.0, 2.0), one)))
    wgt = CX.cmul(CX.cmul(CX.cpow(s, 20), CX.cmul(v4, CX.csub(one, v4))), CX.cexp(CX.cscal((-1.0, -1.0), CX.cmul(s8, E))))
    return up(CX.cabs_up(wgt) * G)
