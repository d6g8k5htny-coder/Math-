"""The integrand of D in Taylor-model arithmetic over a cell of (u, w, v) = (ln tau, g^{1/3}, v):

  D = 3 A3 int du int dw int dv e^{-8u/3} w^{10} e^{-12 e^{2u} w^{12} - w^6/4} F(e^u, w^3, v),   A3 = 1/(57600 pi),
  F(tau, g, v) = sum_{sg} pre_sg * sum_{branch} sum_j q_j^{sg,branch} I_j^{sg,branch},
    s = 576 sqrt6 tau^2 g, a = 1/(576 tau^2), lam = 12 (1 + sg v), mu = sg (4 v^3 - 12 v) - 8,
    alpha = a + lam^2/(2 s^2), beta = lam mu / s^2, cst = mu^2/(2 s^2), t_c = -beta/(2 alpha), pre = exp(alpha t_c^2 - cst)/(s sqrt(2 pi)),
    branch A: t in [1 - v^2/3, 1], P_A(t, v) = [v^6/3 - (1-t) v^4 + (4/3)(1-t)^3 - Iquad(t, sg R - 8 + 12 t)] 12 (v^2 - 1 + t),
    branch B: t in [1, inf),     P_B(t, v) = [v^6/3 - (1-t) v^4 - Iquad(t, sg R - 8 + 12 t)] 12 (v^2 - 1 + t),
    R = 4 v^3 - 12 v + 12 v t, Iquad(t, chi) = 20/3 - 20 t + (8/9) chi + (52/3) t^2 - (4/3) t chi + (13/486) chi^2,
    q_j = coefficients of P(t_c + u, v) in powers of u, I_j = int_{u1}^{u2} u^j e^{-alpha u^2} du (closed form).
"""
import math
from decimal import Decimal as Dec
from fractions import Fraction as Fr
import ddcore as C
from ddcore import q, add, sub, mul, div, neg, smul, sq, ipow, iexp, isqrt, TM, TMSpace, ZERO, ONE, TWO

A3 = C.div(C.q(1), C.smul(Dec(57600), C.PI))
SERIES_TARGET = 1e-14
SERIES_AMAX = Dec('1.0')   # use the series when alpha*max(u1^2,u2^2) <= this, else the half-line difference   # relative truncation target of the moment series (the remainder bound is rigorous at any K)
SQRT6 = C.isqrt(C.q(6))
K_S = C.smul(Dec(576), SQRT6)                 # 576 sqrt 6
INV_SQRT2PI = C.recip(C.SQRT2PI)
SQRTPI_HALF = C.smul(Dec('0.5'), C.SQRTPI)

def poly_in_t(v, sg, branch, one):
    """P(t, v) as a list of TMs c[0..4] in powers of t (v a TM; `one` the constant-1 TM)."""
    v2 = v * v; v3 = v2 * v; v4 = v2 * v2; v6 = v3 * v3
    if branch == 'A':
        ph = [v6 * Fr(1, 3) - v4 + Fr(4, 3), v4 - 4, one * 4, one * Fr(-4, 3)]
    else:
        ph = [v6 * Fr(1, 3) - v4, v4, one * 0, one * 0]
    chi0 = (v3 * 4 - v * 12) * sg - 8
    chi1 = v * (12 * sg) + 12
    iq = [chi0 * Fr(8, 9) + chi0 * chi0 * Fr(13, 486) + Fr(20, 3),
          chi1 * Fr(8, 9) - chi0 * Fr(4, 3) + chi0 * chi1 * Fr(13, 243) - 20,
          chi1 * Fr(-4, 3) + chi1 * chi1 * Fr(13, 486) + Fr(52, 3),
          one * 0]
    d = [ph[i] - iq[i] for i in range(4)]
    r0 = v2 * 12 - 12
    c = [d[0] * r0, d[1] * r0 + d[0] * 12, d[2] * r0 + d[1] * 12, d[3] * r0 + d[2] * 12, d[3] * 12]
    return c

def moments_halfline(alpha, sqrt_alpha, x, nmax):
    """J_n = int_x^inf u^n e^{-alpha u^2} du, n = 0..nmax, by the recursion 2 alpha J_n = (n-1) J_{n-2} + x^{n-1} e^{-alpha x^2}
    (no cancellation: both terms are positive for x >= 0; for x < 0 the second term is at most half the first)."""
    inv2a = (alpha * 2).recip()
    e = (-(alpha * (x * x))).exp()
    J = [(sqrt_alpha * x).erfc() * (sqrt_alpha.recip() * SQRTPI_HALF)]
    if nmax >= 1:
        J.append(e * inv2a)
    xp = x
    for n in range(2, nmax + 1):
        J.append((J[n - 2] * (n - 1) + xp * e) * inv2a)
        xp = xp * x
    return J

def moments_series(alpha, u1, u2, nmax, Amax):
    """I_n = int_{u1}^{u2} u^n e^{-alpha u^2} du by the series e^{-alpha u^2} = sum (-alpha u^2)^k/k!, valid for any
    alpha, u; used when alpha u^2 <= Amax over the cell. Remainder: sum_{k>K} A^k/k! <= A^(K+1)/((K+1)! (1 - A/(K+2)))."""
    A = float(Amax)
    K = 2
    import math as _m
    while (A ** (K + 1)) / _m.factorial(K + 1) / (1 - A / (K + 2)) > SERIES_TARGET:
        K += 1
    # F_n(u) = u^{n+1} sum_{k<=K} y^k/(k! (n+2k+1)), y = -alpha u^2;  I_n = F_n(u2) - F_n(u1)
    def F_all(u):
        y = -(alpha * (u * u))
        ypow = [None, y]
        for k in range(2, K + 1): ypow.append(ypow[-1] * y)
        upow = [None, u]
        for m in range(2, nmax + 2): upow.append(upow[-1] * u)
        out = []
        for n in range(nmax + 1):
            # S_n = sum_k y^k / (k! (n + 2k + 1)) (scalar multiples and sums only), then F_n = u^{n+1} S_n (one TM product)
            acc = None; fk = 1
            for k in range(K + 1):
                if k: fk *= k
                coef = Fr(1, fk * (n + 2 * k + 1))
                term = (ypow[k] * coef) if k else coef
                acc = term if acc is None else acc + term
            out.append(upow[n + 1] * acc)
        return out
    F2 = F_all(u2); F1 = F_all(u1)
    I = [a - b for a, b in zip(F2, F1)]
    # remainder bound: |R_n| <= (|u1|^(n+1) + |u2|^(n+1)) * A^(K+1)/((K+1)! (1 - A/(K+2))) / (n + 2K + 3)
    Aq = (Amax, Amax)
    fac = Dec(_m.factorial(K + 1))
    rem_fac = C.div(C.ipow(Aq, K + 1), C.mul((fac, fac), C.sub(C.q(1), C.div(Aq, C.q(K + 2)))))
    for n in range(nmax + 1):
        b = C.add(ipow(C.iabs(u1.range()), n + 1), ipow(C.iabs(u2.range()), n + 1))
        r = C.mag(C.div(C.mul(b, rem_fac), C.q(n + 2 * K + 3)))
        I[n] = I[n].add_remainder(r)
    return I

def gauss_moments(alpha, sqrt_alpha, u1, u2, nmax, one):
    """I_n = int_{u1}^{u2} u^n e^{-alpha u^2} du, n = 0..nmax; u2 is a TM or None (= +inf)."""
    if u2 is None:
        return moments_halfline(alpha, sqrt_alpha, u1, nmax)
    ar = alpha.range()
    Amax = C.CU.multiply(ar[1], max(C.ipow(C.iabs(u1.range()), 2)[1], C.ipow(C.iabs(u2.range()), 2)[1]))
    if Amax <= SERIES_AMAX:
        return moments_series(alpha, u1, u2, nmax, Amax)
    J1 = moments_halfline(alpha, sqrt_alpha, u1, nmax)
    J2 = moments_halfline(alpha, sqrt_alpha, u2, nmax)
    return [a - b for a, b in zip(J1, J2)]

def F_tm(U, W, V, S):
    """F(e^U, W^3, V) as a TM (U, W, V TMs of the space S)."""
    tau = U.exp()
    e2u = (U * 2).exp()
    g = W * W * W
    a = (U * (-2)).exp() * Fr(1, 576)
    return F_core(tau, e2u, a, g, V, S)

def F_core(tau, e2u, a, g, V, S):
    """F(tau, g, V) with tau, e2u = tau^2, a = 1/(576 tau^2) and g given as TMs (constants for a point evaluation)."""
    one = S.const(1)
    s = e2u * g * K_S
    s_inv = s.recip()
    s2inv = s_inv * s_inv
    total = None
    v2 = V * V; v3 = v2 * V
    for sg in (1, -1):
        lam = (V * sg + 1) * 12
        mu = (v3 * 4 - V * 12) * sg - 8
        # Delta = 2 a s^2 + lam^2 > 0; alpha = Delta/(2 s^2); t_c = -lam mu/Delta; log pre = -a mu^2/Delta <= 0
        s2 = s * s
        delta = a * s2 * 2 + lam * lam
        delta_inv = delta.recip()
        alpha = delta * s2inv * Fr(1, 2)
        tc = -(lam * mu * delta_inv)
        logpre = -(a * (mu * mu) * delta_inv)
        pre = logpre.exp(ZERO) * s_inv * INV_SQRT2PI           # log pre = -a mu^2/Delta <= 0 on the cell
        sqrt_alpha = alpha.sqrt()
        t1A = one - v2 * Fr(1, 3)
        contrib = None
        for branch in ('A', 'B'):
            c = poly_in_t(V, sg, branch, one)
            # shift to powers of (t - tc): q_j = sum_i c_i C(i, j) tc^(i-j)
            tcp = [one]
            for i in range(1, 5): tcp.append(tcp[-1] * tc)
            qq = []
            for j in range(5):
                acc = None
                for i in range(j, 5):
                    term = c[i] * (tcp[i - j] * math.comb(i, j))
                    acc = term if acc is None else acc + term
                qq.append(acc)
            if branch == 'A':
                u1 = t1A - tc; u2 = one - tc
            else:
                u1 = one - tc; u2 = None
            mom = gauss_moments(alpha, sqrt_alpha, u1, u2, 4, one)
            part = None
            for j in range(5):
                term = qq[j] * mom[j]
                part = term if part is None else part + term
            contrib = part if contrib is None else contrib + part
        contrib = contrib * pre
        total = contrib if total is None else total + contrib
    return total

def weight_tm(U, W, S):
    """3 A3 e^{-8u/3} w^10 e^{-12 e^{2u} w^12 - w^6/4}."""
    e2u = (U * 2).exp()
    w2 = W * W; w6 = w2 * w2 * w2; w10 = w6 * w2 * w2; w12 = w6 * w6
    ex = (-(e2u * w12 * 12 + w6 * Fr(1, 4)) + U * Fr(-8, 3)).exp()
    return (ex * w10).scale(C.smul(Dec(3), A3))

def cell_integral(uc, hu, wc, hw, vc, hv, order):
    """enclosure of the integral of the D-integrand over the cell [uc-hu, uc+hu] x [wc-hw, wc+hw] x [vc-hv, vc+hv]."""
    S = TMSpace(3, order, [hu, hw, hv])
    U = S.var(0) + q(uc); W = S.var(1) + q(wc); V = S.var(2) + q(vc)
    T = weight_tm(U, W, S) * F_tm(U, W, V, S)
    return T.integrate(), T


def H_integrand_point(tau_iv, g_iv, vc, hv, order):
    """TM (in v only) of F(tau, g, v) on the cell [vc - hv, vc + hv] for a point (tau, g) given as intervals."""
    S = C.TM1Space(order, hv)
    tau = S.const(tau_iv)
    e2u = S.const(C.sq(tau_iv))
    a = S.const(C.div(C.q(Fr(1, 576)), C.sq(tau_iv)))
    g = S.const(g_iv)
    V = S.var(0) + q(vc)
    return F_core(tau, e2u, a, g, V, S)

def H_integrand_point_log(tau_iv, g_iv, yc, hy, side, order):
    """TM (in y only) of F(tau, g, 1 + side e^y) e^y on the cell [yc - hy, yc + hy]: the substitution v = 1 + side e^y
    (side = +1 or -1) near the point v = 1 where, for small sigma_chi, F has an integrable near-singularity ~ 1/|v - 1|."""
    S = C.TM1Space(order, hy)
    tau = S.const(tau_iv)
    e2u = S.const(C.sq(tau_iv))
    a = S.const(C.div(C.q(Fr(1, 576)), C.sq(tau_iv)))
    g = S.const(g_iv)
    Y = S.var(0) + q(yc)
    E = Y.exp()
    V = (E * side) + 1
    return F_core(tau, e2u, a, g, V, S) * E
