"""Rigorous bounds for the outer Gauss-Legendre rule in (u, w) = (ln tau, ln g):

  D_M = int du int dw rho(u, w) H(u, w),  rho = 24 sqrt(pi) A3 tau^{-5/3} g^{11/3} exp(-12 tau^2 g^4 - g^2/4),
  H(u, w) = E[g(sigma_t Z1, sigma_chi Z2)],  sigma_t = 12 sqrt2 tau, sigma_chi = 576 sqrt6 tau^2 g,  g := I - I_quad.

Derivatives of H fall on the Gaussian kernels: with L = d/d(ln sigma), L^k N_sigma(x) = N_sigma(x) p_k(z), z = x/sigma,
p_0 = 1, p_{k+1} = (z^2 - 1) p_k - z p_k'; d/du = L1 + 2 L2, d/dw = L2.  So d_u^a d_w^b H = E[g Q_{a,b}(Z1, Z2)] with
Q_{a,b} = sum_j C(a, j) 2^{a-j} p_j(Z1) p_{a-j+b}(Z2), and |E[g Q]| <= E[|g~| |Q|] for any pointwise bound |g| <= g~.

Two pointwise bounds of |g| are used: the "sharper" polynomial bound from #244 (2.7) everywhere, and on the box
|t| <= Bt, |chi| <= Bc the exact Taylor polynomial T_N plus C_{N+1} rho^{N+1} (ddtaylor); for a cell the minimum of the
resulting moment bounds is taken.  All moments are Gaussian absolute moments E|Z|^p = 2^{p/2} Gamma((p+1)/2)/sqrt(pi)
(exact for integer p, Stirling-enclosed Gamma otherwise) and incomplete ones through an upper bound of Gamma(a, x).

Derivatives of rho: rho = c0 exp(phi), phi = -5u/3 + 11w/3 - 12 X - Y/4 with X = e^{2u+4w}, Y = e^{2w}; the k-th derivative is
exp(phi) times the complete Bell polynomial of phi's derivatives, which are affine in (X, Y); the Bell polynomial is formed
exactly as a polynomial in (X, Y) and then evaluated on the cell's (X, Y) ranges.

Remainder of the tensor n-point Gauss rule on [uc - hu, uc + hu] x [wc - hw, wc + hw]:
  |E| <= K_n [ hu^{2n+1} sup|d_u^{2n}(rho H)| (2 hw) + hw^{2n+1} sup|d_w^{2n}(rho H)| (2 hu) ],
  K_n = 2^{2n+1} (n!)^4 / ((2n+1) ((2n)!)^3)   (the 1-D Gauss error constant for an interval of half-width h, with (2h)^{2n+1}).
"""
import math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import require, q, add, sub, mul, div, neg, smul, sq, ipow, iexp, iln, isqrt, ZERO, ONE, TWO

# ---------------------------------------------------------------- kernel polynomials p_k (exact integer coefficients)
def _p_next(p):
    out = {}
    for k, c in p.items():
        out[k + 2] = out.get(k + 2, 0) + c
        out[k] = out.get(k, 0) - c
        if k > 0: out[k] = out.get(k, 0) - k * c
    return {k: v for k, v in out.items() if v != 0}
P = [{0: 1}]
for _ in range(10): P.append(_p_next(P[-1]))
require(P[1] == {2: 1, 0: -1} and P[2] == {4: 1, 2: -4, 0: 1})

def kernel_abs(a, b):
    """absolute-monomial bound of Q_{a,b}: dict {(i, j): coef >= 0} with |Q_{a,b}| <= sum coef |Z1|^i |Z2|^j."""
    out = {}
    for j in range(a + 1):
        c = math.comb(a, j) * 2 ** (a - j)
        for i1, c1 in P[j].items():
            for i2, c2 in P[a - j + b].items():
                out[(i1, i2)] = out.get((i1, i2), 0) + c * abs(c1) * abs(c2)
    return out

def kernel_signed(a, b):
    """signed polynomial Q_{a,b} as {(i, j): coef}."""
    out = {}
    for j in range(a + 1):
        c = math.comb(a, j) * 2 ** (a - j)
        for i1, c1 in P[j].items():
            for i2, c2 in P[a - j + b].items():
                out[(i1, i2)] = out.get((i1, i2), 0) + c * c1 * c2
    return {k: v for k, v in out.items() if v != 0}

# ---------------------------------------------------------------- Gaussian moments
_ABSMOM = {}
def absmom(p):
    """E|Z|^p for Z ~ N(0,1), p a nonnegative Fraction; integer p exact."""
    p = Fr(p)
    if p in _ABSMOM: return _ABSMOM[p]
    if p.denominator == 1:
        n = p.numerator
        if n % 2 == 0:
            r = q(math.prod(range(n - 1, 0, -2)) if n > 0 else 1)
        else:
            # E|Z|^n = 2^{(n+1)/2} ((n-1)/2)! / sqrt(2 pi)
            r = div(q(2 ** ((n + 1) // 2) * math.factorial((n - 1) // 2)), C.SQRT2PI)
    else:
        r = div(mul(iexp(mul(q(p / 2), iln(q(2)))), C.igamma(q((p + 1) / 2))), C.SQRTPI)
    _ABSMOM[p] = r
    return r

def momZ(n):
    """E[Z^n] (signed): 0 for odd n."""
    return q(0) if n % 2 else absmom(n)

def upper_incomplete_gamma_bound(a, x):
    """interval x > 0, a Fraction > 0: an upper bound of Gamma(a, x) = int_x^inf s^{a-1} e^{-s} ds:
       a <= 1: Gamma(a, x) <= x^{a-1} e^{-x};  a > 1: Gamma(a, x) <= x^{a-1} e^{-x} * x/(x - a + 1) for x > a - 1,
       else the complete Gamma(a)."""
    a = Fr(a)
    xa1 = iexp(mul(q(a - 1), iln(x)))
    base = mul(xa1, iexp(neg(x)))
    if a <= 1:
        return (ZERO, base[1])
    if x[0] > a - 1:
        f = div(x, sub(x, q(a - 1)))
        return (ZERO, mul(base, f)[1])
    return (ZERO, C.igamma(q(a))[1])

def absmom_out(p, B, sigma):
    """upper bound of E[|X|^p 1{|X| > B}] for X ~ N(0, sigma^2): sigma^p 2^{p/2} Gamma((p+1)/2, B^2/(2 sigma^2)) / sqrt(pi)."""
    p = Fr(p)
    # increasing in sigma (= sigma^p E[|Z|^p 1{|Z| > B/sigma}]): the upper end of the sigma range is used
    sh = sigma[1]
    if sh <= 0: return (ZERO, ZERO)
    sigma = (sh, sh)
    x = div(sq(q(B)), smul(TWO, sq(sigma)))
    G = upper_incomplete_gamma_bound((p + 1) / 2, x)
    return (ZERO, div(mul(mul(iexp(mul(q(p), iln(sigma))), iexp(mul(q(p / 2), iln(q(2))))), G), C.SQRTPI)[1])

def absmom_in(p, B, sigma):
    """upper bound of E[|X|^p 1{|X| <= B}] <= min(sigma^p E|Z|^p, B^p)."""
    p = Fr(p)
    full = mul(iexp(mul(q(p), iln(sigma))), absmom(p)) if sigma[0] > 0 else (ZERO, ZERO)
    Bp = iexp(mul(q(p), iln(q(B))))
    return (ZERO, min(full[1], Bp[1]))

# ---------------------------------------------------------------- the sharper pointwise bound |g| <= sum c |t|^a |chi|^b
def sharper_terms():
    """terms (c, a, b) with c an interval, a, b Fractions:  |g| <= sum c |t|^a |chi|^b  everywhere, from
         g = I - I_quad = (Phi - R^2/48) - (I_quad - R^2/48),   R = 8 - 12 t + chi,  c' = 1 - t,
         I_quad - R^2/48 = 16/3 - 16 t + (5/9) chi + (43/3) t^2 - (5/6) t chi + (23/3888) chi^2        (exact),
         |Phi - R^2/48| <= |c'| rho_R^2 + 3 c'^2 rho_R + (4/3)|c'|^3,  rho_R := (R^2/16)^{1/3}       (Lemma: v-form),
       where, in the v-form (|R| = 4 v^3 - 12 c' v, v >= sqrt(3 c'_+)):
         c' > 0: with rho := v^2 - 3c' >= 0, Phi - R^2/48 = c' rho^2 + 3 c'^2 rho + (4/3) c'^3 and R^2 = 16 (rho + 3c') rho^2 >= 16 rho^3,
                 so 0 <= rho <= rho_R;
         c' <= 0: Phi - R^2/48 = -|c'| v^4 - 3 c'^2 v^2 and R^2 = 16 v^2 (v^2 + 3|c'|)^2 >= 16 v^6, so v^2 <= rho_R.
       Then |c'| <= 1 + |t|,  rho_R <= (8^{2/3} + (12|t|)^{2/3} + |chi|^{2/3}) / 16^{1/3}  (subadditivity of x^{2/3}),
       rho_R^2 = |R|^{4/3}/16^{2/3} <= 3^{1/3} (8^{4/3} + (12|t|)^{4/3} + |chi|^{4/3}) / 16^{2/3}  (power mean, p = 4/3)."""
    T = []
    def add_term(c, a, b): T.append((q(c) if not isinstance(c, tuple) else c, Fr(a), Fr(b)))
    add_term(Fr(23, 3888), 0, 2); add_term(Fr(5, 9), 0, 1); add_term(Fr(5, 6), 1, 1); add_term(Fr(16, 3), 0, 0); add_term(16, 1, 0); add_term(Fr(43, 3), 2, 0)
    for k, ck in enumerate([1, 3, 3, 1]): add_term(Fr(4, 3) * ck, k, 0)        # (4/3)|c'|^3 <= (4/3)(1 + |t|)^3
    c13 = C.fpow(q(16), Fr(-1, 3)); c23 = C.fpow(q(16), Fr(-2, 3)); three13 = C.fpow(q(3), Fr(1, 3))
    r23 = [(mul(C.fpow(q(8), Fr(2, 3)), c13), 0, 0), (mul(C.fpow(q(12), Fr(2, 3)), c13), Fr(2, 3), 0), (c13, 0, Fr(2, 3))]
    r43 = [(mul(mul(three13, C.fpow(q(8), Fr(4, 3))), c23), 0, 0), (mul(mul(three13, C.fpow(q(12), Fr(4, 3))), c23), Fr(4, 3), 0), (mul(three13, c23), 0, Fr(4, 3))]
    for (ct, a) in ((1, 0), (2, 1), (1, 2)):          # 3 c'^2 rho_R <= 3 (1 + 2|t| + t^2) rho_R
        for (c, pa, pb) in r23: add_term(smul(Dec(3 * ct), c), Fr(a) + pa, pb)
    for (ct, a) in ((1, 0), (1, 1)):                  # |c'| rho_R^2 <= (1 + |t|) rho_R^2
        for (c, pa, pb) in r43: add_term(c, Fr(a) + pa, pb)
    return T
SHARPER = sharper_terms()

def sigma_pow(sigma, p):
    """sigma^p for an interval sigma >= 0 and a nonnegative rational p (lower end 0 when sigma's lower end is 0)."""
    p = Fr(p)
    if p == 0: return (ONE, ONE)
    if p < 0: return C.recip(sigma_pow(sigma, -p))
    if p.denominator == 1: return ipow(sigma, p.numerator)
    if sigma[0] <= 0:
        if sigma[1] <= 0: return (ZERO, ZERO)
        return (ZERO, iexp(mul(q(p), iln((sigma[1], sigma[1]))))[1])
    return iexp(mul(q(p), iln(sigma)))

def Egtilde_terms(st, sc):
    """E[g~] term by term: list of (c m_a m_b st^a sc^b as an upper bound Decimal, a, b) for st, sc intervals (upper ends used)."""
    out = []
    for (c, a, b) in SHARPER:
        v = C.CU.multiply(C.CU.multiply(c[1], absmom(a)[1]), C.CU.multiply(absmom(b)[1], C.CU.multiply(sigma_pow(st, a)[1], sigma_pow(sc, b)[1])))
        out.append((v, a, b))
    return out

def vtail_bound(st, sc, v1):
    """upper bound of |E[g 1{v >= v1}]| at a point (sigma_t, sigma_chi) (intervals), for the v-tail of the v-quadrature:
       v >= v1 implies |t| >= T1 := v1^2/6 - 1 or |chi| >= X1 := 2 v1^3 - 8 - 12 T1   (v1 >= 3):
         if |t| < T1 then 3c' = 3(1 - t) <= 3(1 + T1) = v1^2/2, so for c' > 0: |R| = 4v(v^2 - 3c') >= 4 v1 (v1^2 - v1^2/2) = 2 v1^3,
         and for c' <= 0: |R| = 4v^3 + 12|c'|v >= 4 v1^3; then |chi| >= |R| - 8 - 12|t| >= 2 v1^3 - 8 - 12 T1.
       So |E[g 1{v>=v1}]| <= E[g~ 1{|t| >= T1}] + E[g~ 1{|chi| >= X1}], each term by the incomplete absolute moments."""
    v1 = Fr(v1)
    require(v1 >= 3)
    T1 = v1 * v1 / 6 - 1; X1 = 2 * v1 ** 3 - 8 - 12 * T1
    require(T1 > 0 and X1 > 0)
    tot = ZERO
    for (c, a, b) in SHARPER:
        ma = absmom(a)[1]; mb = absmom(b)[1]
        t1 = C.CU.multiply(absmom_out(a, T1, st)[1], C.CU.multiply(sigma_pow(sc, b)[1], mb))
        t2 = C.CU.multiply(C.CU.multiply(sigma_pow(st, a)[1], ma), absmom_out(b, X1, sc)[1])
        tot = C.CU.add(tot, C.CU.multiply(c[1], C.CU.add(t1, t2)))
    return tot

def EgQ_plain(st, sc, Qabs, cache=None):
    """upper bound of E[|g| |Q|] with the sharper bound; st, sc intervals (cell ranges of sigma_t, sigma_chi)."""
    if cache is None: cache = {}
    tot = ZERO
    for (c, a, b) in SHARPER:
        ka = ('st', a); kb = ('sc', b)
        if ka not in cache: cache[ka] = sigma_pow(st, a)
        if kb not in cache: cache[kb] = sigma_pow(sc, b)
        sa = cache[ka][1]; sb = cache[kb][1]
        for (i, j), qc in Qabs.items():
            term = C.CU.multiply(C.CU.multiply(c[1], Dec(qc)), C.CU.multiply(C.CU.multiply(sa, absmom(a + i)[1]), C.CU.multiply(sb, absmom(b + j)[1])))
            tot = C.CU.add(tot, term)
    return tot

class TaylorPart:
    """the box part: T_N (exact), C_{N+1}, Bt, Bc, from ddtaylor."""
    def __init__(self, N, Bt, Bc):
        import ddtaylor
        Cc, TN, d = ddtaylor.remainder_constant(N, Bt, Bc)
        self.N = N; self.Bt = Fr(Bt); self.Bc = Fr(Bc); self.TN = TN; self.C = q(Cc); self.details = d
        self.supT = q(sum(abs(c) * self.Bt ** a * self.Bc ** b for (a, b), c in TN.items()))
    def EgQ_box(self, st, sc, Qsigned, Qabs, cache=None):
        """upper bound of |E[g Q]| via T_N: |E[T_N Q]| + E[|T_N||Q| 1_out] + C E[rho^{N+1} |Q| 1_box] + E[g~|Q| 1_out].
        cache: a dict for per-cell memoization of the sigma-dependent moment factors (same st, sc)."""
        if cache is None: cache = {}
        def out_t(p):      # E[|t|^p 1{|t| > Bt}] upper bound
            k = ('ot', p)
            if k not in cache: cache[k] = absmom_out(p, self.Bt, st)[1]
            return cache[k]
        def out_c(p):
            k = ('oc', p)
            if k not in cache: cache[k] = absmom_out(p, self.Bc, sc)[1]
            return cache[k]
        def st_p(p):       # sigma_t^p as interval
            k = ('st', p)
            if k not in cache: cache[k] = sigma_pow(st, p)
            return cache[k]
        def sc_p(p):
            k = ('sc', p)
            if k not in cache: cache[k] = sigma_pow(sc, p)
            return cache[k]
        def rpow(sig, i):      # sigma^{-i} upper bound (i = 0: 1); needs sigma > 0 when i > 0
            if i == 0: return ONE
            return ipow(C.recip(sig), i)[1]
        exact = (ZERO, ZERO)
        for (a, b), c in self.TN.items():
            for (i, j), qc in Qsigned.items():
                m1 = momZ(a + i); m2 = momZ(b + j)
                if m1 == (ZERO, ZERO) or m2 == (ZERO, ZERO): continue
                exact = add(exact, mul(mul(q(c * qc), mul(st_p(a), sc_p(b))), mul(m1, m2)))
        tot = C.mag(exact)
        Bt = q(self.Bt); Bc = q(self.Bc)
        Np = self.N + 1
        for (i, j), qc in Qabs.items():
            qq = Dec(qc)
            rst_i = rpow(st, i); rsc_j = rpow(sc, j)
            # E[|T_N||Q| 1_out] <= sum |c| (E[|t|^{a+i} 1{|t|>Bt}] st^{-i} sc^b E|Z2|^{b+j} + st^a E|Z1|^{a+i} E[|chi|^{b+j} 1{|chi|>Bc}] sc^{-j})
            for (a, b), c in self.TN.items():
                t1 = C.CU.multiply(C.CU.multiply(out_t(a + i), rst_i), C.CU.multiply(sc_p(b)[1], absmom(b + j)[1]))
                t2 = C.CU.multiply(C.CU.multiply(st_p(a)[1], absmom(a + i)[1]), C.CU.multiply(out_c(b + j), rsc_j))
                tot = C.CU.add(tot, C.CU.multiply(C.CU.multiply(q(abs(c))[1], qq), C.CU.add(t1, t2)))
            # C E[rho^{N+1} |Q| 1_box] <= C sum_k C(N+1,k) E[|t|^k |Z1|^i 1_box] E[|chi|^{N+1-k} |Z2|^j 1_box], each factor by min(full, B^p absmom)
            for k in range(Np + 1):
                f1 = min(C.CU.multiply(st_p(k)[1], absmom(k + i)[1]), C.CU.multiply(ipow(Bt, k)[1], absmom(i)[1]))
                f2 = min(C.CU.multiply(sc_p(Np - k)[1], absmom(Np - k + j)[1]), C.CU.multiply(ipow(Bc, Np - k)[1], absmom(j)[1]))
                tot = C.CU.add(tot, C.CU.multiply(C.CU.multiply(C.CU.multiply(self.C[1], Dec(math.comb(Np, k))), qq), C.CU.multiply(f1, f2)))
            # E[g~ |Q| 1_out]
            for (c, a, b) in SHARPER:
                t1 = C.CU.multiply(C.CU.multiply(out_t(a + i), rst_i), C.CU.multiply(sc_p(b)[1], absmom(b + j)[1]))
                t2 = C.CU.multiply(C.CU.multiply(st_p(a)[1], absmom(a + i)[1]), C.CU.multiply(out_c(b + j), rsc_j))
                tot = C.CU.add(tot, C.CU.multiply(C.CU.multiply(c[1], qq), C.CU.add(t1, t2)))
        return tot

def EgQ_bound(st, sc, a, b, taylor=None, cache=None):
    """upper bound of |d_u^a d_w^b H| on a cell with sigma ranges st, sc (intervals)."""
    Qabs = kernel_abs(a, b)
    plain = EgQ_plain(st, sc, Qabs, cache)
    if taylor is None: return plain
    box = taylor.EgQ_box(st, sc, kernel_signed(a, b), Qabs, cache)
    return min(plain, box)

# ---------------------------------------------------------------- derivatives of rho = c0 exp(phi)
RHO_C0 = mul(smul(Dec(24), C.SQRTPI), C.div(q(1), smul(Dec(57600), C.PI)))   # 24 sqrt(pi) A3

def _bell_poly(derivs, k):
    """complete Bell polynomial B_k(x_1..x_k) with x_j polynomials in (X, Y) (dicts {(i, j): Fraction}); exact."""
    import ddtaylor as TT
    Bs = [{(0, 0): Fr(1)}]
    for n in range(k):
        # B_{n+1} = sum_{j=0}^{n} C(n, j) B_{n-j} x_{j+1}
        acc = {}
        for j in range(n + 1):
            acc = TT.padd(acc, TT.pscale(TT.pmul(Bs[n - j], derivs[j + 1]), Fr(math.comb(n, j))))
        Bs.append(acc)
    return Bs

# phi_u^(j): j=1: -5/3 - 24 X; j>=2: -12 2^j X.   phi_w^(j): j=1: 11/3 - 48 X - Y/2; j>=2: -12 4^j X - 2^{j-2} Y.
def _phi_u_derivs(K):
    d = {1: {(0, 0): Fr(-5, 3), (1, 0): Fr(-24)}}
    for j in range(2, K + 1): d[j] = {(1, 0): Fr(-12 * 2 ** j)}
    return d
def _phi_w_derivs(K):
    d = {1: {(0, 0): Fr(11, 3), (1, 0): Fr(-48), (0, 1): Fr(-1, 2)}}
    for j in range(2, K + 1): d[j] = {(1, 0): Fr(-12 * 4 ** j), (0, 1): -Fr(2) ** (j - 2)}
    return d
_BELL_CACHE = {}
def bell_polys(direction, K):
    key = (direction, K)
    if key not in _BELL_CACHE:
        derivs = _phi_u_derivs(K) if direction == 'u' else _phi_w_derivs(K)
        _BELL_CACHE[key] = _bell_poly(derivs, K)
    return _BELL_CACHE[key]

def poly_eval_XY(p, X, Y):
    """evaluate a polynomial {(i, j): Fraction} at intervals X, Y (Horner in X, then Y)."""
    tot = (ZERO, ZERO)
    # group by power of Y
    byj = {}
    for (i, j), c in p.items(): byj.setdefault(j, {})[i] = c
    for j, pi in byj.items():
        imax = max(pi)
        acc = q(pi.get(imax, Fr(0)))
        for i in range(imax - 1, -1, -1):
            acc = add(mul(acc, X), q(pi.get(i, Fr(0))))
        tot = add(tot, mul(acc, ipow(Y, j)))
    return tot

def rho_cell(u_iv, w_iv):
    """interval of rho over the cell, and of X, Y."""
    X = iexp(add(smul(TWO, u_iv), smul(Dec(4), w_iv)))
    Y = iexp(smul(TWO, w_iv))
    phi = add(add(smul(Dec(Fr(-5, 3).numerator), div(u_iv, q(3))), smul(Dec(11), div(w_iv, q(3)))), neg(add(smul(Dec(12), X), div(Y, q(4)))))
    rho = mul(RHO_C0, iexp(phi))
    return rho, X, Y

def _sup_unimodal(iv, i, lam):
    """upper bound of sup_{x in iv} e^{-lam x} x^i for an interval iv = [a, b] of x >= 0 (lam > 0 Decimal, i >= 0 int):
    the function increases up to x* = i/lam and decreases after, so the sup is at x*, or at the endpoint nearest to x*."""
    a, b = iv
    if i == 0:
        return iexp((C.CD.multiply(-lam, a), C.CU.multiply(-lam, a)))[1]
    xs = Fr(i) / Fr(lam)                              # the exact maximizer i/lam (lam a short decimal)
    if a <= xs <= b:
        # the exact maximum e^{-i} (i/lam)^i, as an interval
        return mul(iexp(q(-i)), ipow(q(xs), i))[1]
    x = q(a) if xs < a else q(b)
    return mul(iexp(smul(-lam, x)), ipow(x, i))[1]

def rho_deriv_bounds(u_iv, w_iv, K, direction, msplit=2):
    """list over k = 0..K of upper bounds of sup_cell |d^k rho| in the given direction, with
       d^k rho = c0 e^{-5u/3 + 11w/3} e^{-12X - Y/4} B_k(X, Y),  B_k the exact Bell polynomial in (X, Y),
    bounded on each of msplit x msplit sub-cells by c0 sup(e^{-5u/3 + 11w/3}) sum_{ij} |b_ij| sup(e^{-12X} X^i) sup(e^{-Y/4} Y^j)
    (each factor's sup over the sub-cell's X-range or Y-range, which are intervals; the sups of the unimodal functions
    e^{-lam x} x^i are explicit).  The maximum over the sub-cells is returned."""
    Bs = bell_polys(direction, K)
    best = [ZERO] * (K + 1)
    du = C.CU.subtract(u_iv[1], u_iv[0]); dw = C.CU.subtract(w_iv[1], w_iv[0])
    for iu in range(msplit):
        ulo = C.CD.add(u_iv[0], C.CD.multiply(du, C.CD.divide(Dec(iu), Dec(msplit))))
        uhi = C.CU.add(u_iv[0], C.CU.multiply(du, C.CU.divide(Dec(iu + 1), Dec(msplit))))
        if iu == msplit - 1: uhi = max(uhi, u_iv[1])
        for iw in range(msplit):
            wlo = C.CD.add(w_iv[0], C.CD.multiply(dw, C.CD.divide(Dec(iw), Dec(msplit))))
            whi = C.CU.add(w_iv[0], C.CU.multiply(dw, C.CU.divide(Dec(iw + 1), Dec(msplit))))
            if iw == msplit - 1: whi = max(whi, w_iv[1])
            X = iexp(add(smul(TWO, (ulo, uhi)), smul(Dec(4), (wlo, whi))))
            Y = iexp(smul(TWO, (wlo, whi)))
            ex = C.CU.divide(C.CU.add(C.CU.multiply(Dec(-5), ulo), C.CU.multiply(Dec(11), whi)), Dec(3))     # sup of (-5u + 11w)/3
            pre = C.CU.multiply(RHO_C0[1], iexp((ex, ex))[1])
            supX = {}; supY = {}
            for k in range(K + 1):
                tot = ZERO
                for (i, j), c in Bs[k].items():
                    if i not in supX: supX[i] = _sup_unimodal(X, i, Dec(12))
                    if j not in supY: supY[j] = _sup_unimodal(Y, j, Dec('0.25'))
                    tot = C.CU.add(tot, C.CU.multiply(C.CU.multiply(q(abs(c))[1], supX[i]), supY[j]))
                val = C.CU.multiply(pre, tot)
                if val > best[k]: best[k] = val
    return best

def gauss_constant(n):
    return q(Fr(2 ** (2 * n + 1) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 3))

def cell_remainder(uc, hu, wc, hw, n, taylor=None):
    """upper bound of the tensor n-point Gauss remainder on the cell (centre uc, wc; half-widths hu, hw; Decimals)."""
    K = 2 * n
    u_iv = (C.CD.subtract(uc, hu), C.CU.add(uc, hu)); w_iv = (C.CD.subtract(wc, hw), C.CU.add(wc, hw))
    tau = iexp(u_iv); g = iexp(w_iv)
    st = smul(Dec(12), mul(isqrt(q(2)), tau)); sc = mul(smul(Dec(576), isqrt(q(6))), mul(sq(tau), g))
    cache = {}
    Hu = [EgQ_bound(st, sc, a, 0, taylor, cache) for a in range(K + 1)]
    Hw = [EgQ_bound(st, sc, 0, b, taylor, cache) for b in range(K + 1)]
    Ru = rho_deriv_bounds(u_iv, w_iv, K, 'u'); Rw = rho_deriv_bounds(u_iv, w_iv, K, 'w')
    Bu = ZERO; Bw = ZERO
    for i in range(K + 1):
        Bu = C.CU.add(Bu, C.CU.multiply(C.CU.multiply(Dec(math.comb(K, i)), Ru[i]), Hu[K - i]))
        Bw = C.CU.add(Bw, C.CU.multiply(C.CU.multiply(Dec(math.comb(K, i)), Rw[i]), Hw[K - i]))
    Kn = gauss_constant(n)[1]
    hu_p = ipow(q(hu), K + 1)[1]; hw_p = ipow(q(hw), K + 1)[1]
    Eu = C.CU.multiply(Kn, C.CU.multiply(C.CU.multiply(hu_p, Bu), C.CU.multiply(TWO, hw)))
    Ew = C.CU.multiply(Kn, C.CU.multiply(C.CU.multiply(hw_p, Bw), C.CU.multiply(TWO, hu)))
    return C.CU.add(Eu, Ew), Eu, Ew

def H_sup(st, sc, taylor=None):
    """upper bound of sup |H| over sigma ranges st, sc (intervals; sc may start at 0)."""
    return EgQ_bound(st, sc, 0, 0, taylor, {})
