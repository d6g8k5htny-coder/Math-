"""Region S (tau <= tau_s) and the tau-tail (tau >= tau_1) of the certified enclosure of D, in closed form.

Region S.  H = P + r with P(sigma_t, sigma_chi) = E[T_N(sigma_t Z1, sigma_chi Z2)] = sum_{a, b even} c_ab m_a m_b sigma_t^a sigma_chi^b
(T_N the exact Taylor polynomial of g at the origin, m_k = E|Z|^k) and, by the box bound (ddtaylor; Bt, Bc, C = C_{N+1}),
  |r| <= C E[rho^{N+1} 1_box] + E[(g~ + |T_N|) 1{|t| > Bt}] + E[(g~ + |T_N|) 1{|chi| > Bc}]
      <= C sum_k C(N+1, k) m_k m_{N+1-k} sigma_t^k sigma_chi^{N+1-k}
         + sum_terms c m_a m_b 2^{(a+1)/2} e^{-Bt^2/(4 sigma_t^2)} sigma_t^a sigma_chi^b
         + sum_terms c m_a m_b 2^{(b+1)/2} e^{-Bc^2/(4 sigma_chi^2)} sigma_t^a sigma_chi^b,
using E[|X|^p 1{|X| > B}] = sigma^p 2^{p/2} Gamma((p+1)/2, B^2/(2 sigma^2))/sqrt(pi) and Gamma(s, x) <= 2^s Gamma(s) e^{-x/2}.
With sigma_t = 12 sqrt2 tau, sigma_chi = K tau^2 g (K = 576 sqrt6), rho = c0 tau^{-5/3} g^{11/3} e^{-12 tau^2 g^4 - g^2/4} and the
measure du dw = dtau dg/(tau g):
  int_0^{tau_s} int_0^inf rho tau^alpha g^beta du dw = c0 int_0^{tau_s} tau^{alpha - 8/3} G_beta(tau) dtau,
  G_beta(tau) = int_0^inf g^{beta + 8/3} e^{-12 tau^2 g^4 - g^2/4} dg in [G_beta(0) - 12 tau^2 M_beta, G_beta(0)]
  (1 - e^{-x} <= x), G_beta(0) = 2^{p-1} Gamma(p/2) with p = beta + 11/3, M_beta = 2^{p+3} Gamma(p/2 + 2).
For the e^{-Bc^2/(4 K^2 tau^4 g^2)} factor: g^2/8 + c/(tau^4 g^2) >= 2 sqrt(c/8)/tau^2 (AM-GM), so
  int g^{p-1} e^{-g^2/4} e^{-c/(tau^4 g^2)} dg <= e^{-sqrt(c/2)/tau^2} int g^{p-1} e^{-g^2/8} dg = e^{-sqrt(c/2)/tau^2} 2^{3p/2 - 1} Gamma(p/2),
and int_0^{tau_s} tau^{alpha - 8/3} e^{-kappa/tau^2} dtau = (1/2) kappa^{(alpha - 5/3)/2} Gamma((5/3 - alpha)/2, kappa/tau_s^2)
(substitution y = kappa/tau^2), bounded with Gamma(s, x) <= x^{s-1} e^{-x} for s <= 1 (x > 0) and by the Stirling-enclosed
Gamma(s) otherwise.

Tau-tail.  |int_{tau >= tau_1} int rho H| <= int int rho E[g~] with E[g~] = sum c m_a m_b sigma_t^a sigma_chi^b and
  int_0^inf g^{p-1} e^{-12 tau^2 g^4} dg = Gamma(p/4) / (4 (12 tau^2)^{p/4}),  p = b + 11/3,
so each term gives c0 c m_a m_b (12 sqrt2)^a K^b Gamma(p/4) 12^{-p/4}/4 * tau_1^{e+1}/(-(e+1)), e = a + 3b/2 - 9/2 < -1.
"""
import math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import q, add, sub, mul, div, neg, smul, sq, ipow, iexp, iln, isqrt, ZERO, ONE, TWO
import ddbounds as B

K_CHI = smul(Dec(576), isqrt(q(6)))        # sigma_chi = K tau^2 g
K_T = smul(Dec(12), isqrt(q(2)))           # sigma_t = K_T tau
C0 = B.RHO_C0

def gam(x):
    """Gamma(x) for a positive rational x (interval)."""
    return C.igamma(q(Fr(x)))

def G_full(p):
    """int_0^inf g^{p-1} e^{-g^2/4} dg = 2^{p-1} Gamma(p/2)."""
    p = Fr(p)
    return mul(B.sigma_pow(q(2), p - 1), gam(p / 2))

def G_eighth(p):
    """int_0^inf g^{p-1} e^{-g^2/8} dg = 2^{3p/2 - 1} Gamma(p/2)."""
    p = Fr(p)
    return mul(B.sigma_pow(q(2), Fr(3, 2) * p - 1), gam(p / 2))

def tau_power_integral(alpha, tau_s):
    """int_0^{tau_s} tau^{alpha - 8/3} dtau = tau_s^{alpha - 5/3} / (alpha - 5/3), alpha > 5/3 (interval)."""
    e = Fr(alpha) - Fr(5, 3)
    assert e > 0
    return div(B.sigma_pow(tau_s, e), q(e))

def tau_exp_integral_bound(alpha, kappa, tau_s):
    """upper bound of int_0^{tau_s} tau^{alpha - 8/3} e^{-kappa/tau^2} dtau = (1/2) kappa^{(alpha-5/3)/2} Gamma((5/3 - alpha)/2, kappa/tau_s^2)."""
    alpha = Fr(alpha)
    s = (Fr(5, 3) - alpha) / 2
    x = div(kappa, sq(tau_s))
    rpow = lambda base, e: (ONE, ONE) if e == 0 else iexp(mul(q(e), iln(base)))      # base^e for rational e, base > 0
    if s <= 1:
        G = (ZERO, mul(rpow(x, s - 1), iexp(neg(x)))[1])
    else:
        G = (ZERO, gam(s)[1])
    pref = mul(q(Fr(1, 2)), rpow(kappa, (alpha - Fr(5, 3)) / 2))
    return C.CU.multiply(pref[1], G[1])

def region_S(u_lo, taylor):
    """enclosure of D_S = int_{u <= u_lo} du int dw rho H.  Returns (interval, details)."""
    tau_s = iexp(q(u_lo))
    N = taylor.N; TN = taylor.TN; Cc = taylor.C; Bt = taylor.Bt; Bc = taylor.Bc
    # ---- the polynomial part: sum over (a, b) even of c_ab m_a m_b K_T^a K^b int rho tau^{a+2b} g^b
    P_int = (ZERO, ZERO)
    for (a, b), c in TN.items():
        if a % 2 or b % 2: continue
        alpha = a + 2 * b; beta = b; p = Fr(beta) + Fr(11, 3)
        Gb0 = G_full(p); Mb = mul(B.sigma_pow(q(2), p + 3), gam(p / 2 + 2))
        # int_0^{tau_s} tau^{alpha-8/3} G_beta(tau) dtau in [I_alpha G0 - 12 M I_{alpha+2}, I_alpha G0]
        I_a = tau_power_integral(alpha, tau_s); I_a2 = tau_power_integral(alpha + 2, tau_s)
        hi_ = mul(I_a, Gb0); lo_ = sub(hi_, smul(Dec(12), mul(Mb, I_a2)))
        Gint = (lo_[0], hi_[1])
        coef = mul(mul(q(c), mul(B.absmom(a), B.absmom(b))), mul(ipow(K_T, a), ipow(K_CHI, b)))
        P_int = add(P_int, mul(coef, Gint))
    P_int = mul(C0, P_int)
    # ---- remainder: C-term
    Np = N + 1
    R_C = ZERO
    for k in range(Np + 1):
        a = k; b = Np - k; alpha = a + 2 * b; p = Fr(b) + Fr(11, 3)
        term = C.CU.multiply(C.CU.multiply(Dec(math.comb(Np, k)), C.CU.multiply(B.absmom(a)[1], B.absmom(b)[1])),
                             C.CU.multiply(C.CU.multiply(ipow(K_T, a)[1], ipow(K_CHI, b)[1]), C.CU.multiply(tau_power_integral(alpha, tau_s)[1], G_full(p)[1])))
        R_C = C.CU.add(R_C, term)
    R_C = C.CU.multiply(C.CU.multiply(Cc[1], C0[1]), R_C)
    # ---- remainder: out-of-box terms, for the term list g~ + |T_N|
    terms = list(B.SHARPER) + [(q(abs(c)), Fr(a), Fr(b)) for (a, b), c in TN.items()]
    kappa_t = div(sq(q(Bt)), smul(Dec(4), sq(K_T)))                  # Bt^2/(4 sigma_t^2) = kappa_t / tau^2
    c_chi = div(sq(q(Bc)), smul(Dec(4), sq(K_CHI)))                  # Bc^2/(4 sigma_chi^2) = c_chi / (tau^4 g^2)
    kappa_chi = isqrt(div(c_chi, q(2)))                              # e^{-sqrt(c/2)/tau^2}
    R_t = ZERO; R_chi = ZERO
    for (c, a, b) in terms:
        alpha = a + 2 * b; p = Fr(b) + Fr(11, 3)
        base = C.CU.multiply(C.CU.multiply(c[1], C.CU.multiply(B.absmom(a)[1], B.absmom(b)[1])), C.CU.multiply(B.sigma_pow(K_T, a)[1], B.sigma_pow(K_CHI, b)[1]))
        # t-out: 2^{(a+1)/2} e^{-kappa_t/tau^2} tau^alpha g^b
        tt = C.CU.multiply(C.CU.multiply(base, B.sigma_pow(q(2), (a + 1) / 2)[1]), C.CU.multiply(tau_exp_integral_bound(alpha, kappa_t, tau_s), G_full(p)[1]))
        R_t = C.CU.add(R_t, tt)
        # chi-out: 2^{(b+1)/2} e^{-c_chi/(tau^4 g^2)} tau^alpha g^b -> e^{-kappa_chi/tau^2} with the g^2/8 weight
        tc = C.CU.multiply(C.CU.multiply(base, B.sigma_pow(q(2), (b + 1) / 2)[1]), C.CU.multiply(tau_exp_integral_bound(alpha, kappa_chi, tau_s), G_eighth(p)[1]))
        R_chi = C.CU.add(R_chi, tc)
    R_t = C.CU.multiply(C0[1], R_t); R_chi = C.CU.multiply(C0[1], R_chi)
    R = C.CU.add(C.CU.add(R_C, R_t), R_chi)
    enc = (C.CD.subtract(P_int[0], R), C.CU.add(P_int[1], R))
    return enc, dict(P=P_int, R_C=R_C, R_t=R_t, R_chi=R_chi, tau_s=tau_s)

def tau_tail(u_hi):
    """upper bound of |int_{u >= u_hi} du int dw rho H|."""
    tau_1 = iexp(q(u_hi))
    tot = ZERO
    for (c, a, b) in B.SHARPER:
        p = Fr(b) + Fr(11, 3)
        e = Fr(a) + Fr(3, 2) * Fr(b) - Fr(9, 2)
        assert e + 1 < 0
        gpart = div(gam(p / 4), smul(Dec(4), B.sigma_pow(q(12), p / 4)))
        tpart = div(B.sigma_pow(tau_1, e + 1), q(-(e + 1)))
        term = C.CU.multiply(C.CU.multiply(c[1], C.CU.multiply(B.absmom(a)[1], B.absmom(b)[1])),
                             C.CU.multiply(C.CU.multiply(B.sigma_pow(K_T, a)[1], B.sigma_pow(K_CHI, b)[1]), C.CU.multiply(gpart[1], tpart[1])))
        tot = C.CU.add(tot, term)
    return C.CU.multiply(C0[1], tot)

if __name__ == '__main__':
    import sys, time
    u_lo = Dec(sys.argv[1]) if len(sys.argv) > 1 else Dec('-6.2'); u_hi = Dec(sys.argv[2]) if len(sys.argv) > 2 else Dec('16.2')
    t0 = time.time()
    tp = B.TaylorPart(11, Fr(3, 10), Fr(1))
    enc, d = region_S(u_lo, tp)
    print('region S (tau <= %s): D_S in [%s, %s]; P = [%s, %s], R_C = %s, R_t = %s, R_chi = %s [%.1fs]' % (
        d['tau_s'][1], enc[0], enc[1], d['P'][0], d['P'][1], d['R_C'], d['R_t'], d['R_chi'], time.time() - t0))
    for uh in [Dec('6.9'), Dec('11.5'), Dec('13.8'), Dec('16.2'), Dec('18.4')]:
        print('tau tail beyond u = %s (tau = %.3g): <= %s' % (uh, math.exp(float(uh)), tau_tail(uh)))
