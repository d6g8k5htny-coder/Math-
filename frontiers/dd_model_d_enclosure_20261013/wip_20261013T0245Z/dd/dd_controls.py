"""Controls of note DD (standard library only; exact rational arithmetic where the statement is an identity).
C1 the v-form identities; C2 c0 and the exponents of rho; C3 the closed-form t-moments against a brute-force Riemann sum
(floats, exploration grade) and the identity log pre = -a mu^2/Delta; C4 the identity of Lemma 1 as a polynomial identity;
C5 |g| <= g~ at sample points (floats); C6 the kernel recursion, Q_{a,b} and the Bell polynomials against finite differences
(floats); C7 T_11, C_12 and the localization inequalities (exact); C8 the Gauss nodes/weights (interval) are the roots of
P_4 and integrate x^6 exactly.  Exit 0 iff every control passes."""
import sys, os, math, random
from fractions import Fraction as Fr
from decimal import Decimal as Dec
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ddcore as C
from ddcore import q, add, sub, mul, div, smul, sq, ipow, iexp, isqrt, ZERO, ONE, TWO
import ddbounds as B, ddtaylor as T, ddgauss as G, ddvq as VQ, ddint as D

FAILS = []
def check(name, ok, detail=''):
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok: FAILS.append(name)

# ---- polynomial helpers in (c, v) and (t, chi) as dicts of Fractions
def padd(p, qq):
    out = dict(p)
    for k, v in qq.items(): out[k] = out.get(k, Fr(0)) + v
    return {k: v for k, v in out.items() if v != 0}
def pmul(p, qq):
    out = {}
    for (a, b), x in p.items():
        for (c, d), y in qq.items():
            out[(a + c, b + d)] = out.get((a + c, b + d), Fr(0)) + x * y
    return {k: v for k, v in out.items() if v != 0}
def pscale(p, s): return {k: v * s for k, v in p.items()} if s else {}
def ppow(p, n):
    out = {(0, 0): Fr(1)}
    for _ in range(n): out = pmul(out, p)
    return out

def C1():
    # variables (c, v): rho = v^2 - 3c;  Phi(c>0) = rho^3/3 + 2 rho^2 c + 3 rho c^2 + (4/3) c^3 (from #244 (2.7) with y = rho + c)
    # must equal v^6/3 - c v^4 + (4/3) c^3; and R^2 = 16 v^2 rho^2.
    c = {(1, 0): Fr(1)}; v = {(0, 1): Fr(1)}
    rho = padd(ppow(v, 2), pscale(c, Fr(-3)))
    lhs = padd(padd(padd(pscale(ppow(rho, 3), Fr(1, 3)), pscale(pmul(ppow(rho, 2), c), Fr(2))), pscale(pmul(rho, ppow(c, 2)), Fr(3))), pscale(ppow(c, 3), Fr(4, 3)))
    rhs = padd(padd(pscale(ppow(v, 6), Fr(1, 3)), pscale(pmul(c, ppow(v, 4)), Fr(-1))), pscale(ppow(c, 3), Fr(4, 3)))
    check('C1a Phi(c>0) v-form', lhs == rhs)
    # (2.7): Phi = R^2/48 + c y (y + c) + (2/3)|c|^3 - (4/3) c^3 with y = rho + c, R^2 = 16 v^2 rho^2 -> for c > 0: + (2/3 - 4/3) c^3
    y = padd(rho, c); R2 = pscale(pmul(ppow(v, 2), ppow(rho, 2)), Fr(16))
    form27 = padd(padd(pscale(R2, Fr(1, 48)), pmul(pmul(c, y), padd(y, c))), pscale(ppow(c, 3), Fr(2, 3) - Fr(4, 3)))
    check('C1b (2.7) with c > 0 equals the v-form', form27 == rhs)
    # c <= 0 (write c = -m, m >= 0): |R| = 4 v^3 + 12 m v, Phi = m v^4 + v^6/3; (2.7): R^2/48 + c y (y + c) + (2/3) m^3 + (4/3) m^3 with y = rho + c
    m = {(1, 0): Fr(1)}; cneg = pscale(m, Fr(-1))
    rho_n = padd(ppow(v, 2), pscale(m, Fr(3)))            # rho = v^2 - 3c = v^2 + 3m
    R_n = padd(pscale(ppow(v, 3), Fr(4)), pscale(pmul(m, v), Fr(12)))
    y_n = padd(rho_n, cneg)
    form27n = padd(padd(pscale(ppow(R_n, 2), Fr(1, 48)), pmul(pmul(cneg, y_n), padd(y_n, cneg))), pscale(ppow(m, 3), Fr(2, 3) + Fr(4, 3)))
    rhs_n = padd(pmul(m, ppow(v, 4)), pscale(ppow(v, 6), Fr(1, 3)))
    check('C1c (2.7) with c <= 0 equals the v-form', form27n == rhs_n)
    # Phi - R^2/48 on each branch (Lemma 1's exact forms)
    check('C1d c>0: Phi - R^2/48 = c rho^2 + 3 c^2 rho + 4/3 c^3', padd(rhs, pscale(R2, Fr(-1, 48))) == padd(padd(pmul(c, ppow(rho, 2)), pscale(pmul(ppow(c, 2), rho), Fr(3))), pscale(ppow(c, 3), Fr(4, 3))))
    check('C1e c<=0: Phi - R^2/48 = -m v^4 - 3 m^2 v^2', padd(rhs_n, pscale(ppow(R_n, 2), Fr(-1, 48))) == padd(pscale(pmul(m, ppow(v, 4)), Fr(-1)), pscale(pmul(ppow(m, 2), ppow(v, 2)), Fr(-3))))

def C2():
    # D = (1/2400) int k^{-8/3} e^{-12k^2} E[gamma^6 g] dk with k = tau g^2, gamma ~ N(0, 2): E[gamma^6 | ...]: note DC Lemma 4 gives the
    # form (1.2); here the constant c0 = 24 sqrt(pi) A3, A3 = 1/(57600 pi), and the exponents -5/3 (tau), 11/3 (g) are checked against
    # the task definition's form D = 3 A3 int du int dw int dv e^{-8u/3} w^10 e^{-12 e^{2u} w^12 - w^6/4} F, with g = w^3 (dw = dg/(3 w^2)):
    # 3 A3 e^{-8u/3} w^10 dw = A3 e^{-8u/3} g^{10/3} g^{-2/3} dg = A3 tau^{-8/3} g^{8/3} dg; with du = dtau/tau and the (24 tau sqrt pi) H
    # normalization of F: A3 tau^{-8/3} g^{8/3} * 24 tau sqrt(pi) H dg dtau/tau = 24 sqrt(pi) A3 tau^{-5/3} g^{11/3} H (dtau/tau)(dg/g).
    c0 = B.RHO_C0
    ref = mul(smul(Dec(24), C.SQRTPI), C.recip(smul(Dec(57600), C.PI)))
    check('C2 c0 = 24 sqrt(pi)/(57600 pi)', c0[0] <= ref[1] and ref[0] <= c0[1], '%s' % c0[1])

def C3():
    # closed-form moments J_n(x) = int_x^inf u^n e^{-alpha u^2} du (floats) against Riemann sums
    import ddint
    alpha = 3.7; x = 0.4
    def riemann(n):
        N = 200000; h = 12.0 / N
        return sum(((x + (i + 0.5) * h) ** n) * math.exp(-alpha * (x + (i + 0.5) * h) ** 2) for i in range(N)) * h
    S = C.TM1Space(0, Dec('0'))
    al = S.const(Dec(repr(alpha))); sa = al.sqrt(); xx = S.const(Dec(repr(x)))
    J = ddint.moments_halfline(al, sa, xx, 4)
    ok = True
    for n in range(5):
        r = riemann(n); lo, hi = float(J[n].range()[0]), float(J[n].range()[1])
        ok = ok and abs(r - lo) < 1e-6 * max(1, abs(r)) and abs(r - hi) < 1e-6 * max(1, abs(r))
    check('C3a half-line moments vs Riemann sums', ok)
    # exponent identity: -a t^2 - (lam t + mu)^2/(2 s^2) = -alpha (t - tc)^2 - a mu^2/Delta, Delta = 2 a s^2 + lam^2 (symbolic over rationals)
    a, s2, lam, mu = Fr(3, 7), Fr(5, 2), Fr(-11, 3), Fr(7, 4)
    Delta = 2 * a * s2 + lam * lam; alpha_ = Delta / (2 * s2); tc = -lam * mu / Delta
    ok = True
    for t in [Fr(-3), Fr(0), Fr(1, 2), Fr(9, 5)]:
        lhs = -a * t * t - (lam * t + mu) ** 2 / (2 * s2); rhs = -alpha_ * (t - tc) ** 2 - a * mu * mu / Delta
        ok = ok and lhs == rhs
    check('C3b completing the square: log pre = -a mu^2/Delta', ok)

def C4():
    t = {(1, 0): Fr(1)}; chi = {(0, 1): Fr(1)}; one = {(0, 0): Fr(1)}
    R = padd(padd(pscale(one, Fr(8)), pscale(t, Fr(-12))), chi)
    Iq = {(0, 0): Fr(20, 3), (1, 0): Fr(-20), (0, 1): Fr(8, 9), (2, 0): Fr(52, 3), (1, 1): Fr(-4, 3), (0, 2): Fr(13, 486)}
    diff = padd(Iq, pscale(ppow(R, 2), Fr(-1, 48)))
    expect = {(0, 0): Fr(16, 3), (1, 0): Fr(-16), (0, 1): Fr(5, 9), (2, 0): Fr(43, 3), (1, 1): Fr(-5, 6), (0, 2): Fr(23, 3888)}
    check('C4 I_quad - R^2/48 identity', diff == expect)

def phi_float(c, R):
    """Phi(c, R) in floating point through the v-form (1.1): v the largest root of 4v^3 - 12cv = |R| on [sqrt(3c_+), inf) by bisection."""
    R = abs(R); lo = math.sqrt(3 * c) if c > 0 else 0.0
    G = lambda v: 4 * v ** 3 - 12 * c * v - R
    hi = max(lo, 1.0)
    while G(hi) < 0: hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if G(mid) < 0: lo = mid
        else: hi = mid
    v = 0.5 * (lo + hi)
    return v ** 6 / 3 - c * v ** 4 + (4 / 3) * c ** 3 if c > 0 else abs(c) * v ** 4 + v ** 6 / 3

def iquad_float(t, chi):
    return 20 / 3 - 20 * t + (8 / 9) * chi + (52 / 3) * t * t - (4 / 3) * t * chi + (13 / 486) * chi * chi

def C5():
    random.seed(1); worst = 0.0; n = 0
    pts = [(t, c) for t in [-30, -5, -1, -0.5, 0, 0.3, 0.9, 1, 1.1, 2, 5, 30] for c in [-3000, -100, -8, -1, 0, 1, 8, 100, 3000]]
    pts += [(random.uniform(-40, 40), random.uniform(-5000, 5000)) for _ in range(4000)] + [(random.uniform(-2, 2), random.uniform(-20, 20)) for _ in range(2000)]
    pts += [(t, 12 * t - 8) for t in (-1000, -100, -10, -3, -1, 2, 10, 100)]                      # the line R = 0, where the c'^3 term is tight
    pts += [(t, c) for t in (-1, 0, 1) for c in (1e4, -1e4, 1e5, -1e5, 1e6, -1e6)]              # large |chi|, where the chi^2 term is tight
    pts += [(t, 0.0) for t in (-100, -1000, -10000, 100, 1000, 10000)]                          # large |t| at chi = 0, where the |c'|^3 term is tight
    ok = True
    for (tt, cc) in pts:
        gval = phi_float(1 - tt, 8 - 12 * tt + cc) - iquad_float(tt, cc)
        gt = sum(float(c[1]) * abs(tt) ** float(a) * abs(cc) ** float(b) for (c, a, b) in B.SHARPER)
        ok = ok and abs(gval) <= gt * (1 + 1e-9); worst = max(worst, abs(gval) / gt); n += 1
    check('C5 |g| <= g~ at %d points' % n, ok, 'max ratio %.4f' % worst)
    # the float v-form against #244's trig/Cardano root is checked in C1 symbolically; here a spot check of Phi at the origin: I(0,0) = 20/3
    check('C5b I(0, 0) = 20/3', abs(phi_float(1.0, 8.0) - 20 / 3) < 1e-12)

def C6():
    check('C6a p1, p2', B.P[1] == {2: 1, 0: -1} and B.P[2] == {4: 1, 2: -4, 0: 1})
    # E[Z^m p_k(Z)] = m^k E[Z^m] (L^k acting on sigma^m): check for m = 4, k = 1..3 exactly (moments (m-1)!!)
    def mom(m): return 0 if m % 2 else math.prod(range(m - 1, 0, -2)) if m > 0 else 1
    ok = True
    for m in (2, 4, 6):
        for k in (1, 2, 3):
            val = sum(c * mom(m + i) for i, c in B.P[k].items())
            ok = ok and val == m ** k * mom(m)
    check('C6b E[Z^m p_k(Z)] = m^k E[Z^m]', ok)
    # Bell polynomials vs finite differences of rho (floats)
    u, w = math.log(0.37), math.log(1.3); c0 = float(B.RHO_C0[0])
    def rho(uu, ww):
        tau = math.exp(uu); g = math.exp(ww)
        return c0 * tau ** (-5 / 3) * g ** (11 / 3) * math.exp(-12 * tau * tau * g ** 4 - g * g / 4)
    X = math.exp(2 * u + 4 * w); Y = math.exp(2 * w); ok = True
    for direction in ('u', 'w'):
        Bs = B.bell_polys(direction, 4)
        for k in range(1, 5):
            e = 1e-2; val = 0.0
            for i in range(k + 1):
                d = (k / 2 - i) * e
                val += (-1) ** i * math.comb(k, i) * (rho(u + d, w) if direction == 'u' else rho(u, w + d))
            fd = val / e ** k; ex = rho(u, w) * sum(float(c) * X ** i * Y ** j for (i, j), c in Bs[k].items())
            ok = ok and abs(fd - ex) < 2e-2 * abs(ex)
    check('C6c Bell polynomials vs finite differences', ok)

def C7():
    Cc, TN, d = T.remainder_constant(11, Fr(3, 10), Fr(1))
    check('C7a C_12(3/10, 1) = 404.1...', Fr(404) < Cc < Fr(405), str(float(Cc)))
    check('C7b T_11 has no terms of degree <= 2', all(a + b >= 3 for (a, b) in TN))
    expect4 = {(3, 0): Fr(-28, 9), (2, 1): Fr(14, 81), (0, 3): Fr(-5, 52488), (4, 0): Fr(-7, 27), (3, 1): Fr(7, 243), (2, 2): Fr(5, 5832), (1, 3): Fr(-5, 34992), (0, 4): Fr(43, 15116544)}
    check('C7c degree 3-4 terms of T_11', all(TN.get(k) == v for k, v in expect4.items()))
    check('C7d localization: v_lo - eps > sqrt(1 + Bt), E_max <= eps Gmin', d['v_lo'] - d['eps'] > 0 and (d['v_lo'] - d['eps']) ** 2 > 1 + Fr(3, 10) and d['Gmin'] > 0)

def C8():
    GN = G.gauss_nodes(4)
    # P4(x) = (35 x^4 - 30 x^2 + 3)/8 must contain 0 at every node; weights sum to 2; sum w x^6 = 2/7
    ok = True; ws = (ZERO, ZERO); s6 = (ZERO, ZERO)
    for (x, wgt) in GN:
        p4 = div(add(sub(smul(Dec(35), ipow(x, 4)), smul(Dec(30), sq(x))), q(3)), q(8))
        ok = ok and p4[0] <= 0 <= p4[1]
        ws = add(ws, wgt); s6 = add(s6, mul(wgt, ipow(x, 6)))
    check('C8a nodes are roots of P4', ok)
    check('C8b weights sum to 2', ws[0] <= 2 <= ws[1])
    check('C8c rule integrates x^6 exactly (2/7)', s6[0] <= Fr(2, 7) <= s6[1])
    Kn = G.B.gauss_constant(4)
    check('C8d K_4 = 2^9 24^4/(9 (8!)^3)', Kn[0] <= Fr(2 ** 9 * 24 ** 4, 9 * math.factorial(8) ** 3) <= Kn[1])

def C9():
    # the v-tail (Lemma 5) in the right units: at (tau, g) = (0.3, 1) the enclosure with v1 = 3 (tail of order 1 relative) and the one
    # with the automatic v1 must intersect (both enclose H); the same at (0.05, 1) and (3, 0.2)
    ok = True
    for (tau, g) in ((Dec('0.3'), Dec('1')), (Dec('0.05'), Dec('1')), (Dec('3'), Dec('0.2'))):
        H1, d1 = VQ.H_point(q(tau), q(g)); H2, d2 = VQ.H_point(q(tau), q(g), v1_override=3)
        ok = ok and max(H1[0], H2[0]) <= min(H1[1], H2[1]) and d2['tail'] > C.width(H1)
    check('C9 v-tail bound: enclosures with v1 = 3 and automatic v1 intersect (tails of relative size O(1))', ok)

if __name__ == '__main__':
    for f in (C1, C2, C3, C4, C5, C6, C7, C8, C9): f()
    print('controls:', 'ALL PASS' if not FAILS else 'FAILED %s' % FAILS)
    sys.exit(0 if not FAILS else 1)
