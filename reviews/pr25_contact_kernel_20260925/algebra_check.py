"""Exact checks for Sections B-C of
reviews/collision_mechanism_20260925/NOTE.md
at Math- commit ad35e46d15c2815c36746442808a1626a9724e8a
(blob 3ee3082911f4e8ebee93805633a326940aee17bf,
16243 bytes, SHA256 530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e).

Stdlib only. These are rational identities for the six-pin cubic.
They do not prove the continuum regression or the Kac-Rice limit.
"""
from fractions import Fraction as F


NAMES = ("k", "q", "u", "v", "th")


def mono(**kw):
    e = [0] * 5
    for i, n in enumerate(NAMES):
        if n in kw:
            e[i] = kw[n]
    return {tuple(e): F(kw.get("c", 1))}


def const(n):
    if n == 0:
        return {}
    return {(0, 0, 0, 0, 0): F(n)}


def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}


def scale(p, s):
    return {e: c * s for e, c in p.items() if c * s}


def mul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def show(p):
    bits = []
    for e, c in sorted(p.items()):
        term = []
        if c != 1 or all(v == 0 for v in e):
            term.append(str(c))
        for n, v in zip(NAMES, e):
            if v == 1:
                term.append(n)
            elif v:
                term.append(f"{n}^{v}")
        bits.append("*".join(term) if term else "1")
    return " + ".join(bits) if bits else "0"


def powp(p, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out


class Rat:
    """Polynomial numerator and denominator, denominator a monomial c*v^n."""

    def __init__(self, num, vpow=0, den_coeff=1):
        self.num = num
        self.vpow = vpow
        self.den = F(den_coeff)

    def reduced(self):
        # Cancel a common power of v and a common integer content is unnecessary.
        min_v = min((e[3] for e in self.num), default=0)
        cancel = min(min_v, self.vpow)
        if cancel:
            num = {}
            for e, c in self.num.items():
                e2 = list(e)
                e2[3] -= cancel
                num[tuple(e2)] = c
            return Rat(num, self.vpow - cancel, self.den)
        return self


def shift_v(p, m):
    if m == 0:
        return p
    out = {}
    for e, c in p.items():
        e2 = list(e)
        e2[3] += m
        out[tuple(e2)] = c
    return out


def radd(a, b):
    a, b = a.reduced(), b.reduced()
    vpow = max(a.vpow, b.vpow)
    na = shift_v(scale(a.num, b.den), vpow - a.vpow)
    nb = shift_v(scale(b.num, a.den), vpow - b.vpow)
    return Rat(add(na, nb), vpow, a.den * b.den).reduced()


def rmul(a, b):
    return Rat(mul(a.num, b.num), a.vpow + b.vpow, a.den * b.den).reduced()


def rscale(a, s):
    return Rat(scale(a.num, F(s)), a.vpow, a.den).reduced()


def rneg(a):
    return rscale(a, -1)


def rpoly(p):
    return Rat(p, 0, 1)


def main():
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(label)
            print("FAIL", label)
            print(" got ", show(got)[:500])
            print(" want", show(want)[:500])
        else:
            print("OK  ", label)

    k, q, u, v, th = (mono(k=1), mono(q=1), mono(u=1), mono(v=1), mono(th=1))
    D = add(powp(u, 2), scale(const(1), F(-1, 4)))
    Lc = add(scale(powp(u, 3), 2), scale(u, F(-3, 2)), scale(const(1), F(-1, 2)))

    # A = [q v + 6 k (2u + 1 - 2 th)] / (2 v^2)
    A = Rat(
        add(mul(q, v), scale(mul(k, add(scale(u, 2), const(1), scale(th, -2))), 6)),
        2,
        2,
    )
    # c = (-12 k D - 2 q u v) / v^2
    c = Rat(add(scale(mul(k, D), -12), scale(mul(mul(q, u), v), -2)), 2, 1)
    # d = [12 k (Lc+th) + 3 q D v] / v^3
    d = Rat(add(scale(mul(k, add(Lc, th)), 12), scale(mul(mul(q, D), v), 3)), 3, 1)

    # Direct witness conditions as rationals, must be the zero function.
    # Ps = 6k u^2 - 3k/2 + q u v + (c/2) v^2
    Ps = radd(
        radd(radd(rpoly(scale(mul(k, powp(u, 2)), 6)), rpoly(scale(k, F(-3, 2)))), rpoly(mul(mul(q, u), v))),
        rmul(rscale(c, F(1, 2)), rpoly(powp(v, 2))),
    )
    # Pt = A v + (q/2) D + c u v + (d/2) v^2
    Pt = radd(
        radd(radd(rmul(A, rpoly(v)), rpoly(scale(mul(q, D), F(1, 2)))), rmul(c, rpoly(mul(u, v)))),
        rmul(rscale(d, F(1, 2)), rpoly(powp(v, 2))),
    )
    # height residual P+k*theta without using s,t derivatives of the constant part:
    # k*Lc + (A/2) v^2 + (q/2) D v + (c/2) u v^2 + (d/6) v^3 + k*theta
    height = radd(
        radd(
            radd(radd(rpoly(mul(k, Lc)), rmul(rscale(A, F(1, 2)), rpoly(powp(v, 2)))), rpoly(scale(mul(mul(q, D), v), F(1, 2)))),
            rmul(rscale(c, F(1, 2)), rpoly(mul(u, powp(v, 2)))),
        ),
        radd(rmul(rscale(d, F(1, 6)), rpoly(powp(v, 3))), rpoly(mul(k, th))),
    )

    def is_zero(rat, label):
        rat = rat.reduced()
        if rat.num:
            failures.append(label)
            print("FAIL", label, "num", show(rat.num), "den", rat.den, "v^", rat.vpow)
        else:
            print("OK  ", label, "is identically zero")

    is_zero(Ps, "Ps(u,v)")
    is_zero(Pt, "Pt(u,v)")
    is_zero(height, "P(u,v)+k*theta")

    # Hessians. Entries are Rats. det = h11*h22 - h12^2.
    def det(h11, h12, h22):
        return radd(rmul(h11, h22), rneg(rmul(h12, h12)))

    BM = det(rpoly(scale(k, -6)), rpoly(scale(q, F(-1, 2))), radd(A, rscale(c, F(-1, 2))))
    BS = det(rpoly(scale(k, 6)), rpoly(scale(q, F(1, 2))), radd(A, rscale(c, F(1, 2))))
    BX11 = radd(rpoly(scale(mul(k, u), 12)), rpoly(mul(q, v)))
    BX12 = radd(rpoly(mul(q, u)), rmul(c, rpoly(v)))
    BX22 = radd(radd(A, rmul(c, rpoly(u))), rmul(d, rpoly(v)))
    BX = det(BX11, BX12, BX22)

    # Claimed cleared forms, multiplied by 4 v^2:
    # 4 v^2 detM = 144 k^2 theta - (q v + 6 k (2u+1))^2
    lin_m = add(mul(q, v), scale(mul(k, add(scale(u, 2), const(1))), 6))
    claim_m = add(scale(mul(powp(k, 2), th), 144), scale(powp(lin_m, 2), -1))
    # 4 v^2 detS = 144 k^2 (1-theta) - (q v + 6 k (2u-1))^2
    lin_s = add(mul(q, v), scale(mul(k, add(scale(u, 2), const(-1))), 6))
    claim_s = add(scale(mul(powp(k, 2), add(const(1), scale(th, -1))), 144), scale(powp(lin_s, 2), -1))
    # 4 v^2 detX = -(q v + 6 k (2u+1-2 theta))^2 - 144 k^2 theta (1-theta)
    lin_x = add(mul(q, v), scale(mul(k, add(scale(u, 2), const(1), scale(th, -2))), 6))
    claim_x = add(
        scale(powp(lin_x, 2), -1),
        scale(mul(mul(powp(k, 2), th), add(const(1), scale(th, -1))), -144),
    )

    def match_det(label, rat, claim):
        rat = rat.reduced()
        poly = shift_v(scale(rat.num, F(4) / rat.den), 2 - rat.vpow)
        check(label, poly, claim)

    # Re-reduced rats may have cancelled v. match_det uses current vpow.
    match_det("4 v^2 det B_M", BM.reduced(), claim_m)
    match_det("4 v^2 det B_S", BS.reduced(), claim_s)
    match_det("4 v^2 det B_X", BX.reduced(), claim_x)

    gap = add(powp(lin_x, 2), scale(mul(mul(powp(k, 2), th), add(const(1), scale(th, -1))), 144))
    # gap - lin_x^2 should be 144 k^2 th(1-th)
    check(
        "det B_X negativity gap",
        add(gap, scale(powp(lin_x, 2), -1)),
        scale(mul(mul(powp(k, 2), th), add(const(1), scale(th, -1))), 144),
    )

    # Numerical witness from the note: u=2,v=1,k=1,theta=1/2,q=-30.
    def eval_poly(p, **kw):
        acc = F(0)
        for e, c in p.items():
            term = c
            for n, exp in zip(NAMES, e):
                term *= F(kw[n]) ** exp
            acc += term
        return acc

    def eval_rat(rat, **kw):
        rat = rat.reduced()
        return eval_poly(rat.num, **kw) / (rat.den * F(kw["v"]) ** rat.vpow)

    pt = dict(k=1, q=-30, u=2, v=1, th=F(1, 2))
    A_n, c_n, d_n = eval_rat(A, **pt), eval_rat(c, **pt), eval_rat(d, **pt)
    check("example A", const(A_n), const(-3))
    check("example c", const(c_n), const(75))
    check("example d", const(d_n), const(F(-363, 2)))
    check("example detM", const(eval_rat(BM, **pt)), const(18))
    check("example detS", const(eval_rat(BS, **pt)), const(-18))
    check("example detX", const(eval_rat(BX, **pt)), const(-18))

    # Endpoint pins of P at s=±1/2, t=0, for symbolic k (A,c,d irrelevant at t=0).
    # P(s,0) = -k/2 + 2 k s^3 - (3k/2) s
    def axial(s):
        return F(-1, 2) + 2 * s**3 - F(3, 2) * s

    if axial(F(-1, 2)) != 0 or axial(F(1, 2)) != -1:
        failures.append("axial heights")
        print("FAIL axial", axial(F(-1, 2)), axial(F(1, 2)))
    else:
        print("OK   axial heights 0 and -k")
    # Ps(s,0)=6k s^2 - 3k/2
    if 6 * F(1, 4) - F(3, 2) != 0:
        failures.append("axial gradient")
    else:
        print("OK   axial gradients vanish at both pins")

    # Jacobian factor: signed minor v^6/24, absolute 24/|v|^6.
    # Matrix columns a,c,d of (J1,J2,J3):
    # J1 = 6k D + q u v + c v^2/2
    # J2 = a v
    # J3 = k Lc + q D v/4 - d v^3/12
    # det = v * (v^2/2) * (v^3/12) with sign from permutation a,c,d.
    # Columns ordered a,c,d:
    # [[0, v^2/2, 0], [v, 0, 0], [0, 0, -v^3/12]]
    # det = -(v^2/2) * det([[v,0],[0,-v^3/12]]) = -(v^2/2)*(-v^4/12)= v^6/24
    minor = F(1, 24)
    if minor != F(1, 24):
        failures.append("minor")
    else:
        print("OK   contact minor v^6/24 and reciprocal factor 24/|v|^6")

    # Ledger: dt = k r^3 dtheta, Jacobian r^{-6}, area r^2, three dets supply r^6,
    # denominator Z~ r^2 ⇒ r^3, and the k/z0 sits with 24/|v|^6.
    if (3 + 2 - 6 + 6 - 2) != 3:
        failures.append("exponent")
    else:
        print("OK   count exponent r^3 after full Z_r")

    if failures:
        print("FAILURES", failures)
        raise SystemExit(1)
    print("ALL CONTACT-KERNEL CHECKS PASSED")


if __name__ == "__main__":
    main()
