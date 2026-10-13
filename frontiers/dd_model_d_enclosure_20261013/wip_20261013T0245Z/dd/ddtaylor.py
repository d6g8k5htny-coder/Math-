"""Exact rational Taylor polynomial of g(t, chi) = I(t, chi) - I_quad(t, chi) at the origin, I = Phi(1 - t, 8 - 12 t + chi),
through the root-free parametrization Phi = v^6/3 - c' v^4 + (4/3) c'^3 (c' = 1 - t > 0 near the origin), where v is the largest
root of G(t, chi, v) = 4 v^3 - 12 (1 - t) v - R = 0, R = 8 - 12 t + chi, v(0, 0) = 2, G_v(0, 0, 2) = 36.
Also a rigorous bound |g - T_N| <= C_{N+1} rho^{N+1} on the box |t|, |chi| <= B (rho = |t| + |chi|), from
  (i) the exact polynomial G(v_p) = O(rho^{N+1}) and the mean-value inequality |v - v_p| <= |G(v_p)| / min G_v,
  (ii) the finite Taylor expansion of the degree-6 polynomial Phi~(t, v) in v - v_p,
  (iii) the exact degree > N part of Phi~(t, v_p) - I_quad.
Python standard library (fractions); polynomials in (t, chi) as dicts {(a, b): Fraction}.
"""
from fractions import Fraction as Fr
import math

def padd(p, q_):
    out = dict(p)
    for k, v in q_.items():
        out[k] = out.get(k, Fr(0)) + v
    return {k: v for k, v in out.items() if v != 0}

def pscale(p, c):
    return {k: v * c for k, v in p.items()} if c != 0 else {}

def pmul(p, q_, N=None):
    out = {}
    for (a, b), x in p.items():
        for (c, d), y in q_.items():
            if N is not None and a + b + c + d > N: continue
            k = (a + c, b + d)
            out[k] = out.get(k, Fr(0)) + x * y
    return {k: v for k, v in out.items() if v != 0}

def ppow(p, n, N=None):
    out = {(0, 0): Fr(1)}
    for _ in range(n): out = pmul(out, p, N)
    return out

def ptrunc(p, N):
    return {k: v for k, v in p.items() if k[0] + k[1] <= N}

def pdeg_ge(p, N):
    return {k: v for k, v in p.items() if k[0] + k[1] >= N}

T = {(1, 0): Fr(1)}; CHI = {(0, 1): Fr(1)}; ONE = {(0, 0): Fr(1)}
CP = padd(ONE, pscale(T, Fr(-1)))                      # c' = 1 - t
RR = padd(padd(pscale(ONE, Fr(8)), pscale(T, Fr(-12))), CHI)   # R = 8 - 12 t + chi

def G_of(v, N=None):
    """G(t, chi, v) = 4 v^3 - 12 c' v - R as a polynomial (v a polynomial in (t, chi))."""
    return padd(padd(pscale(ppow(v, 3, N), Fr(4)), pscale(pmul(CP, v, N), Fr(-12))), pscale(RR, Fr(-1)))

def root_taylor(N):
    """Taylor polynomial v_p of degree N of the root v(t, chi) at (0, 0), by Newton iteration on truncated polynomials
    starting from v = 2; each step doubles the number of correct orders, so ceil(log2(N+1)) + 1 steps suffice; verified by
    checking that G(v_p) has no terms of degree <= N."""
    v = {(0, 0): Fr(2)}
    steps = max(1, math.ceil(math.log2(N + 1))) + 1
    for _ in range(steps):
        G = G_of(v, N)
        Gp = padd(pscale(ppow(v, 2, N), Fr(12)), pscale(CP, Fr(-12)))   # 12 v^2 - 12 c'
        # 1/Gp as a truncated series: Gp = c0 + d, 1/Gp = (1/c0) sum (-d/c0)^k
        c0 = Gp.get((0, 0), Fr(0)); d = {k: val for k, val in Gp.items() if k != (0, 0)}
        inv = {}; term = {(0, 0): Fr(1) / c0}
        for k in range(N + 1):
            inv = padd(inv, term)
            term = ptrunc(pmul(term, pscale(d, Fr(-1) / c0), N), N)
        v = ptrunc(padd(v, pscale(pmul(G, inv, N), Fr(-1))), N)
    assert ptrunc(G_of(v, N), N) == {}, 'root Taylor polynomial not exact to degree %d' % N
    return v

def phi_tilde(v, N=None):
    """Phi~(t, v) = v^6/3 - c' v^4 + (4/3) c'^3 as a polynomial in (t, chi) (c' > 0 branch)."""
    v2 = pmul(v, v, N); v4 = pmul(v2, v2, N); v6 = pmul(v4, v2, N)
    return padd(padd(pscale(v6, Fr(1, 3)), pscale(pmul(CP, v4, N), Fr(-1))), pscale(ppow(CP, 3, N), Fr(4, 3)))

IQUAD = {(0, 0): Fr(20, 3), (1, 0): Fr(-20), (0, 1): Fr(8, 9), (2, 0): Fr(52, 3), (1, 1): Fr(-4, 3), (0, 2): Fr(13, 486)}

def g_taylor(N):
    """T_N: the degree-N Taylor polynomial of g at the origin (exact), and the full exact polynomial Phi~(t, v_p) - I_quad."""
    vp = root_taylor(N)
    full = padd(phi_tilde(vp), pscale(IQUAD, Fr(-1)))     # exact polynomial, degree up to 6N
    TN = ptrunc(full, N)
    return vp, TN, full

def box_sup(p, Bt, Bc=None, min_deg=0):
    """bound of |p(t, chi)| / rho^{min_deg} on the box |t| <= Bt, |chi| <= Bc (rho = |t| + |chi|): for a term |c| |t|^a |chi|^b
    with a + b >= min_deg write |t|^a |chi|^b <= rho^{min_deg} * (|t|^a |chi|^b / rho^{min_deg}) and bound the second factor by
    Bt^{a'} Bc^{b'} with (a', b') = (a, b) minus min_deg units taken from whichever exponent is larger first (any split is valid,
    since |t|, |chi| <= rho)."""
    if Bc is None: Bc = Bt
    Bt = Fr(Bt); Bc = Fr(Bc); tot = Fr(0)
    for (a, b), c in p.items():
        if a + b < min_deg: continue
        aa, bb, m = a, b, min_deg
        while m > 0:
            if aa >= bb and aa > 0: aa -= 1
            elif bb > 0: bb -= 1
            else: aa -= 1
            m -= 1
        tot += abs(c) * Bt ** aa * Bc ** bb
    return tot

def remainder_constant(N, Bt, Bc=None):
    """C_{N+1} with |g - T_N| <= C_{N+1} rho^{N+1} on the box |t|, |chi| <= B, B < 2/3 (then c' > 0 and R > 0 on the box).
    Returns (C, details).  Steps:
      G(v_p) =: E(t, chi) is an exact polynomial with no terms of degree <= N: |E| <= K_G rho^{N+1}, K_G = box_sup(E, B, N+1).
      v_p's range on the box: v_p in [v_lo, v_hi]; G is increasing in v for v > sqrt(c') and sqrt(3 c') <= v_p - eps needed:
      G_v = 12 v^2 - 12 c' >= 12 (v_lo - eps)^2 - 12 (1 + B) =: Gmin > 0, then |v - v_p| <= K_G rho^{N+1} / Gmin =: e rho^{N+1}
      (the root is the largest: the largest root exceeds sqrt(3 c') and G is increasing there; v_p - eps > sqrt(3(1+B)) is checked).
      |Phi~(t, v_p + d) - Phi~(t, v_p)| <= sum_{k=1}^{6} sup|d_v^k Phi~| |d|^k / k!  with |d| <= e rho^{N+1} <= e (2B)^{N+1}.
      |Phi~(t, v_p) - I_quad - T_N| = |degree > N part| <= box_sup(full, B, N+1) rho^{N+1}."""
    if Bc is None: Bc = Bt
    Bt = Fr(Bt); Bc = Fr(Bc); B = Bt
    assert Bt < Fr(2, 3) and Bc < 8 * (1 - Fr(3, 2) * Bt), 'the box must stay inside c\' > 0 and R > 0'
    vp, TN, full = g_taylor(N)
    E = G_of(vp)
    assert ptrunc(E, N) == {}
    K_G = box_sup(E, Bt, Bc, N + 1)                 # |E| <= K_G rho^{N+1} on the box
    E_max = box_sup(E, Bt, Bc, 0)                   # |E| <= E_max on the box (uniform)
    v0 = vp[(0, 0)]
    vdev = box_sup({k: v for k, v in vp.items() if k != (0, 0)}, Bt, Bc)
    v_lo = v0 - vdev; v_hi = v0 + vdev
    rho_max = Bt + Bc
    cmax = 1 + Bt
    # Localization of the largest root v of G(t, chi, .) near v_p (on the box, c' > 0 and v >= sqrt(3c') > sqrt(c'), and G is
    # increasing on [sqrt(c'), inf)): with Gmin := min G_v on [v_p - eps, inf) > 0 and eps >= E_max / Gmin,
    #   E >= 0: G(v_p - eps) <= E - Gmin eps <= 0 <= G(v_p), so the root lies in [v_p - eps, v_p];
    #   E <  0: G(v_p + eps) >= E + Gmin eps >= 0 > G(v_p), so the root lies in [v_p, v_p + eps];
    # in both cases |v - v_p| <= |E| / Gmin <= (K_G / Gmin) rho^{N+1}.  Gmin = 12 (v_lo - eps)^2 - 12 c_max needs v_lo - eps > sqrt(c_max).
    # eps is found by iteration and then verified.
    def up(x, scale=10 ** 8):       # round a Fraction up to a multiple of 1/scale (keeps the rationals small)
        return Fr(math.ceil(x * scale), scale)
    E_max = up(E_max); K_G = up(K_G)
    eps = Fr(0)
    for _ in range(12):
        assert v_lo - eps > 0 and (v_lo - eps) ** 2 > cmax, 'v_p - eps must exceed sqrt(c_max)'
        Gmin = 12 * (v_lo - eps) ** 2 - 12 * cmax
        eps = up(E_max / Gmin)
    eps = up(eps * Fr(21, 20))       # a margin above the (approximate) fixed point, then verified
    assert v_lo - eps > 0 and (v_lo - eps) ** 2 > cmax, 'v_p - eps must exceed sqrt(c_max)'
    Gmin = 12 * (v_lo - eps) ** 2 - 12 * cmax
    assert E_max / Gmin <= eps, 'eps not self-consistent'
    e = K_G / Gmin
    # derivatives of Phi~ in v: Phi~ = v^6/3 - c' v^4 + (4/3) c'^3
    vmax = v_hi + eps
    dPhi = {1: 2 * vmax ** 5 + 4 * cmax * vmax ** 3, 2: 10 * vmax ** 4 + 12 * cmax * vmax ** 2, 3: 40 * vmax ** 3 + 24 * cmax * vmax,
            4: 120 * vmax ** 2 + 24 * cmax, 5: 240 * vmax, 6: Fr(240)}
    C_root = Fr(0)
    for k in range(1, 7):
        # |d| <= eps and |d| <= e rho^{N+1}, so |d|^k <= eps^{k-1} e rho^{N+1}
        C_root += dPhi[k] * e * eps ** (k - 1) / math.factorial(k)
    C_poly = box_sup(full, Bt, Bc, N + 1)
    C = C_root + C_poly
    details = dict(K_G=K_G, Gmin=Gmin, e=e, eps=eps, v_lo=v_lo, v_hi=v_hi, C_root=C_root, C_poly=C_poly, N=N, Bt=Bt, Bc=Bc)
    return C, TN, details

if __name__ == '__main__':
    import sys, time
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    Bt = Fr(sys.argv[2]) if len(sys.argv) > 2 else Fr(3, 5)
    Bc = Fr(sys.argv[3]) if len(sys.argv) > 3 else Bt
    t0 = time.time()
    C, TN, d = remainder_constant(N, Bt, Bc)
    print('N=%d Bt=%s Bc=%s: C_{N+1} = %.6g (root part %.3g, poly part %.3g); e = %.3g, eps = %.3g, v_p range [%.4f, %.4f]  [%.1fs]' % (
        N, Bt, Bc, float(C), float(d['C_root']), float(d['C_poly']), float(d['e']), float(d['eps']), float(d['v_lo']), float(d['v_hi']), time.time() - t0))
    for deg in range(N + 1):
        terms = sorted((k, v) for k, v in TN.items() if k[0] + k[1] == deg)
        if terms: print('degree', deg, ':', [(k, str(v)) for k, v in terms])
