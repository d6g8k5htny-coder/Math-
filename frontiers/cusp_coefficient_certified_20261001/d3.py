"""The d = 3 integral T3 of CL-CU-CUSP-COEFFICIENT-20261001 (NOTE.md section 4):

    T3 = 64 int_0^oo ds int_0^oo dt int_0^1 dv f3(s, v, t)   (cusp.f3).

Order of integration.  v is innermost: for fixed real (s, t), f3 is analytic in v on the ellipses used.  The outer
variables (s, t) run over boxes S x T with t <= T_MAX.  The tail t > T_MAX is done separately (tail_integral).

Box enclosure (Lemma B of NOTE.md).  Let Q = Q_S Q_T Q_V be the tensor Gauss-Legendre rule (Q_V composite over the
v-panels).  Then
    |I - Q| <= |(I_S - Q_S) I_T I_V f| + |Q_S (I_T - Q_T) I_V f| + |Q_S Q_T (I_V - Q_V) f|.
Each term takes the one-dimensional bound of gauss.error_bound in its own direction:
- for s and t, the bound uses sup |I_V f| on the ellipse in that direction, with the other outer variable real;
- for v, it uses sup |f| on each v-ellipse, with s and t real.
The sums of positive weights are |S| and |T|.  Each sup is taken over complex boxes: ellipse slabs times real
sub-intervals of the other variables.  For each (sub-interval, panel) one representation of f is used on every slab,
the safe form (cusp.f3 with CplxOps) or the direct form (cusp.f3_bound_direct).  Its success on every slab certifies
that it is analytic there, so it equals f on the ellipse."""
import math
from fractions import Fraction as Fr
from ia import dn, up, add, sub, mul, div, scal, from_frac
import gauss as G
import cusp as CU
import cx as CX
import elem as EL

R, C = CU.RealOps, CU.CplxOps
ZERO = (0.0, 0.0)
FAIL = (ValueError, ZeroDivisionError, OverflowError)

S_EDGES = (0.0, 0.6, 0.9, 1.1, 1.25, 1.4, 1.55, 1.7, 1.9, 2.1, 2.35, 2.6, 3.0)
T_EDGES = (0.0, 0.4, 0.7, 0.9, 1.0, 1.1, 1.3, 1.6, 2.0, 2.6, 3.4, 4.5, 6.0, 8.0, 11.0, 15.0)
V_EDGES = (0.0, 0.35, 0.55, 0.65, 0.75, 0.85, 0.93, 1.0)
T_MAX = T_EDGES[-1]
S_MAX = S_EDGES[-1]
RHOS = (3.0, 2.2, 1.7, 1.4, 1.2)
SLABS = 8
NMAX = 48


def _sub(a, b, k):
    return [(a + (b - a) * j / k, a + (b - a) * (j + 1) / k) for j in range(k)]


def _merge(pts, top):
    out = [pts[0]]
    for x in pts[1:]:
        if x - out[-1] >= 0.02:
            out.append(x)
        elif x == top:
            out[-1] = top
    return tuple(out)


def s_edges(tb):
    """s-panel edges for an outer box with t <= tb.  For large t the integrand contains e^(-(23/240) s^8 v^8 t^8), and
    for complex s with arg s > pi/16 that factor grows once |s| > 1.3/t.  So extra edges c/tb are added below 2,
    and the s-ellipses near the origin shrink with 1/t."""
    pts = sorted(set(S_EDGES) | {c / tb for c in (0.5, 0.8, 1.1, 1.5, 2.0, 2.8) if c / tb < 2.0})
    return _merge(pts, S_EDGES[-1])


def v_edges(tb):
    """v-panel edges for an outer box with t <= tb.  For large t the integrand has branch points at |v| = 1/t, about
    0.38/t from the real axis, so extra edges c/tb are added below 0.9.  Edges closer than 0.02 are merged, keeping the
    first."""
    pts = sorted(set(V_EDGES) | {c / tb for c in (0.3, 0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0) if c / tb < 0.9})
    out = [pts[0]]
    for x in pts[1:]:
        if x - out[-1] >= 0.02 or x == 1.0:
            if x == 1.0 and 1.0 - out[-1] < 0.02:
                out[-1] = 1.0
            else:
                out.append(x)
    return tuple(out)


def _bnd(form, s, v, t):
    if form == 'safe':
        return CX.cabs_up(CU.f3(C, s, v, t))
    return CU.f3_bound_direct(s, v, t)


def _forms(t_lo):
    """Representation order: the direct form first for t >= 1 (tighter there), the safe form first below."""
    return ('direct', 'safe') if t_lo >= 1.0 else ('safe', 'direct')


def _sup_over_slabs(slabs, mk, t_lo):
    """max over the slabs of one representation (the first that succeeds on every slab); None if neither does."""
    for form in _forms(t_lo):
        try:
            m = 0.0
            for sl in slabs:
                m = max(m, _bnd(form, *mk(sl)))
            return m
        except FAIL:
            continue
    return None


GOOD_N = 16


def _search(h, tol, M_of):
    """Try rho in RHOS (descending); M_of(rho) returns sup |f| on that ellipse or None.  Stop at the first rho giving an
    admissible n <= GOOD_N, else return the smallest admissible (n, err, rho) found.  Deterministic."""
    best = None
    for rho in RHOS:
        M = M_of(rho)
        if M is None:
            continue
        for n in range(4, NMAX + 1):
            e = G.error_bound(n, rho, M, h)
            if e <= tol:
                if best is None or (n, e) < (best[0], best[1]):
                    best = (n, e, rho)
                break
        if best is not None and best[0] <= GOOD_N:
            break
    if best is None:
        raise RuntimeError('no admissible Gauss-Legendre rule')
    return best


def _v_rules(S, T, tol_v):
    """Per v-panel: (n, err, rho) for the inner rule, with sup over s in S, t in T (real sub-intervals) and v on the
    ellipse."""
    rules = []
    ve = v_edges(T[1])
    for (va, vb) in zip(ve, ve[1:]):
        def M_of(rho, va=va, vb=vb):
            slabs = G.ellipse_slabs(va, vb, rho, SLABS)
            M = 0.0
            for si in _sub(S[0], S[1], 2):
                for ti in _sub(T[0], T[1], 2):
                    m = _sup_over_slabs(slabs, lambda sl: ((si, ZERO), sl, (ti, ZERO)), ti[0])
                    if m is None:
                        return None
                    M = max(M, m)
            return M
        rules.append(_search(0.5 * (vb - va), tol_v, M_of))
    return rules


def _int_v_bound(s_box, t_box):
    """Upper bound of int_0^1 |f3(s, v, t)| dv over complex s_box, t_box (one of them real), by v-panels.  For each
    v sub-interval one representation is used (the first that succeeds)."""
    tot = 0.0
    ve = v_edges(max(t_box[0][1], 1e-300))
    for (va, vb) in zip(ve, ve[1:]):
        for vi in _sub(va, vb, 2):
            m = None
            for form in _forms(t_box[0][0]):
                try:
                    m = _bnd(form, s_box, (vi, ZERO), t_box)
                    break
                except FAIL:
                    continue
            if m is None:
                raise ValueError('no bound')
            tot = up(tot + up(m * up(vi[1] - vi[0])))
    return tot


def _outer_rule(a, b, tol, other, which):
    """Rule in the outer direction `which` ('s' or 't') on [a, b], with the other outer variable real over `other`."""
    def M_of(rho):
        slabs = G.ellipse_slabs(a, b, rho, SLABS)
        try:
            M = 0.0
            for oi in _sub(other[0], other[1], 2):
                for sl in slabs:
                    if which == 's':
                        M = max(M, _int_v_bound(sl, (oi, ZERO)))
                    else:
                        M = max(M, _int_v_bound((oi, ZERO), sl))
            return M
        except FAIL:
            return None
    return _search(0.5 * (b - a), tol, M_of)


def box(S, T, tol):
    """Certified enclosure of int_S int_T int_0^1 f3, with the rule data.  Boxes whose crude enclosure is below
    tol/10 use it directly."""
    cr = crude(S, T)
    if cr is not None and cr[1] <= tol / 10.0:
        return cr, {'crude': True, 'err': cr[1]}
    lenS, lenT = S[1] - S[0], T[1] - T[0]
    ve = v_edges(T[1])
    tol_v = tol / (3.0 * lenS * lenT * (len(ve) - 1))
    vr = _v_rules(S, T, tol_v)
    ns, es, rs = _outer_rule(S[0], S[1], tol / (3.0 * lenT), T, 's')
    nt, et, rt = _outer_rule(T[0], T[1], tol / (3.0 * lenS), S, 't')
    xs, ws = G.panel(ns, S[0], S[1])
    xt, wt = G.panel(nt, T[0], T[1])
    vpanels = []
    for (va, vb), (nv, ev, rv) in zip(zip(ve, ve[1:]), vr):
        vpanels.append(G.panel(nv, va, vb))
    Q = (0.0, 0.0)
    for x1, w1 in zip(xs, ws):
        for x2, w2 in zip(xt, wt):
            inner = (0.0, 0.0)
            for xv, wv in vpanels:
                for x3, w3 in zip(xv, wv):
                    inner = add(inner, mul(w3, CU.f3(R, x1, x3, x2)))
            Q = add(Q, mul(mul(w1, w2), inner))
    err_v = sum(e for (_, e, _) in vr)
    err = up(up(es * lenT * (1 + 1e-12)) + up(et * lenS * (1 + 1e-12)) + up(err_v * lenS * lenT * (1 + 1e-12)))
    return (dn(Q[0] - err), up(Q[1] + err)), {'ns': ns, 'nt': nt, 'nv': [r[0] for r in vr],
                                              'rho_s': rs, 'rho_t': rt, 'err': err}


def boxes():
    out = []
    for (ta, tb) in zip(T_EDGES, T_EDGES[1:]):
        se = s_edges(tb)
        out.extend(((sa, sb), (ta, tb)) for (sa, sb) in zip(se, se[1:]))
    return out


def crude(S, T):
    """0 <= int_box f3 <= sum over 2 x 2 x 4 sub-boxes of volume * sup f3, since f3 >= 0: the weight is nonnegative
    and 1 - Re Phi >= 0 because |Phi| <= 1.  Each sup is the upper end of one real interval evaluation of f3 over the
    sub-box."""
    hi = 0.0
    try:
        for si in _sub(S[0], S[1], 2):
            for ti in _sub(T[0], T[1], 2):
                for vi in _sub(0.0, 1.0, 4):
                    val = CU.f3(R, si, vi, ti)
                    vol = up(up(up(si[1] - si[0]) * up(ti[1] - ti[0])) * up(vi[1] - vi[0]))
                    hi = up(hi + up(max(0.0, val[1]) * vol))
    except FAIL:
        return None
    return (0.0, hi)


# ---------------------------------------------------------------- tails t > T_MAX and s > S_MAX
def tail_t():
    """int_0^oo ds int_0^1 dv int_(T_MAX)^oo dt f3, for real (s, v) (without the factor 64 of T3).

    Here f3 = wgt (1 - Re Phi) t^-8, and on the real axis |Phi| <= |1 - i t^4|^(-1/2) <= t^-2.  So the t-integral is
    wgt (T^-7/7 + theta T^-9/9) with |theta| <= 1.  The s-integral is exact:
        int_0^oo s^20 e^(-s^8 E) ds = Gamma(21/8)/(8 E^(21/8)),   E(v) = (2 v^8 - v^4 + 2)/10 >= 3/16.
    This leaves Gamma(21/8)/8 int_0^1 v^4 (1 - v^4) E(v)^(-21/8) dv.  That integral is enclosed by interval evaluation
    on 20000 cells; the result is multiplied by T^-7/7 < 4e-10."""
    import consts as K
    n = 20000
    tot = (0.0, 0.0)
    for j in range(n):
        V = (j / n, (j + 1) / n)
        v4 = mul(mul(V, V), mul(V, V))
        v4 = (max(0.0, v4[0]), v4[1])
        poly = mul(v4, sub((1.0, 1.0), v4))
        E = scal(0.1, add(sub(scal(2.0, mul(v4, v4)), v4), (2.0, 2.0)))
        E = (max(E[0], 0.1874999), E[1])
        val = mul(poly, EL.exp_iv(mul(from_frac(Fr(-21, 8)), EL.log_iv(E))))
        tot = add(tot, mul(val, (dn(V[1] - V[0]), up(V[1] - V[0]))))
    W = mul(div(K.gamma(Fr(21, 8)), (8.0, 8.0)), tot)
    T = T_MAX
    main = div((1.0, 1.0), (7.0 * T ** 7, 7.0 * T ** 7))
    e = up(1.0 / (9.0 * T ** 9) * (1 + 1e-12))
    return mul(W, (dn(main[0] - e), up(main[1] + e)))


def tail_s_bound():
    """Bound of int_(S_MAX)^oo ds int_0^1 dv int_0^oo dt f3 >= 0 (without the factor 64; NOTE.md section 4).

    Here 1 - Re Phi <= omega^2 E[Y^2]/2 and <= 2, so Gt <= min(E[Y^2]/(2 a1^2), 2 t^-8).  With
    E[Y^2] <= a1^6/50 + 3 a1^4 + 3 a1^2 and a1 = s^4 >= 81, int Gt dt <= a1^4 + 2/7 <= 2 s^16.  Hence the s-integrand
    is at most s^20 e^(-3 s^8/16) (1/4) 2 s^16 <= e^(-s^8/10)/2 for s >= 3 (s^36 <= e^(0.0875 s^8)), and
    int_3^oo e^(-s^8/10)/2 ds <= e^(-656.1)/(1.6 * 3^7) < 1e-280."""
    if S_MAX != 3.0:
        raise ValueError('the s-tail bound is proved for S_MAX = 3 only')
    return 1e-280
