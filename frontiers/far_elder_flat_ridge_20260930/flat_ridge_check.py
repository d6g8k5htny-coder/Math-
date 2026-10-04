#!/usr/bin/env python3
"""Exact finite controls for PROOF.md (CL-FAR-ELDER-FLAT-RIDGE-20260930-v1).  Standard library only; exact rationals.

  F1  Lemma 1 (flat components) on an explicit two-maximum landscape f(x, y) = g(x) - y^2 with
      g'(x) = -4 (x + 1)(x - 1/10)(x - 11/10): maxima at x = -1 (height 203/150, the elder) and x = 11/10 (height
      31339/30000, the younger), saddle at x = 1/10 (height -661/30000), younger lifetime 16/15.  On the rational
      grid of spacing 1/50 in [-2, 2]^2, the grid component of the younger maximum in {f > t} at t = saddle height
      + 1/1000, and again at the death level t = saddle height itself, is taken by union-find, and (1.1)
      |grad f|^2 <= 2 K (b - f) is verified at every one of its points, with K the exact operator-norm bound of the
      Hessian diag(g''(x), -2) on the x-interval spanned by the component's grid points widened by one grid step
      (for this separable f the component is {y^2 < g(x) - t} over an x-interval, which the widened grid interval
      contains); the equality case f = b - K|x|^2/2 of (1.1) is checked exactly; mutant M1 tests all grid points
      of {f > t} (the elder's component must fail); mutant M2 replaces K by 1 (must fail); mutant M5 tests the
      factor-2 error |grad f|^2 <= K (b - f) (must fail);
  F2  the uphill-segment inequality of the proof of Lemma 1, phi(s) >= f(p) + |g| s - K s^2/2 for 0 <= s <= |g|/K,
      on the same polynomial at rational p and rational s (exact), with the same K as F1, and the monotonicity
      phi' >= |g| - K s >= 0;
  F3  the pinned near-pair cubic P(x) = b - 6k(r^2 x/4 - x^3/3 + ...) with P'(x) = 6k (x^2 - r^2/4) ([P] (3.1):
      P''' = 12k): (1.1) holds on the whole segment [-r/2, r/2] with K = 1 + 6 k r, at rational (k, r, x), so the
      flat-component lemma is consistent with the near law (no restriction there);
  F4  Lemma 3's constants: for q in B(p, r_ell), r_ell = (ell/K0)^(1/2): |grad f(q)| <= (sqrt2 + 1)(K0 ell)^(1/2)
      < 3 (K0 ell)^(1/2) and |f(q) - b| <= (1 + sqrt2 + 1/2) ell < 3 ell, checked through squares
      ((sqrt2 + 1)^2 = 3 + 2 sqrt2 < 9 since sqrt2 < 3; 1 + 1/2 + sqrt2 < 3 since 2 < (3/2)^2); mutant M3 claims
      the sharper constant 2 in the first bound (false: (sqrt2 + 1)^2 = 3 + 2 sqrt2 > 4);
  F5  the exponent ledger of section 3 by exact monomial substitution: (K0/ell)^(dN/2) (K0^(d/2) ell^(1 + d/2))^N
      = K0^(dN) ell^N for d in {2, 3, 5}, N in {1, 2, 7}; mutant M4 claims ell^(N/2);
  F6  the shell geometry: radii j rho/(2N), half-width rho/(8N): pairwise separation >= rho/(4N) between shells and
      from the origin, and >= rho/4 from every y with |y| >= rho; r_ell <= rho/(8N) once ell <= rho^2/(64 N^2)
      (K0 >= 1); exact for N = 1..6 at rational rho;
  M   semantic mutants (--mutant M1|M2|M3|M4|M5) exit 1; an unknown label exits 2.
"""
import argparse
import json
import sys
from fractions import Fraction as F

# ------------------------------------------------------------------------------------------------------------
# the landscape of F1/F2: f(x, y) = g(x) - y^2, g'(x) = -4 (x - x1)(x - x2)(x - x3)
X1, X2, X3 = F(-1), F(1, 10), F(11, 10)
S1, S2, S3 = X1 + X2 + X3, X1*X2 + X1*X3 + X2*X3, X1*X2*X3


def g(x):
    return -4*(x**4/4 - S1*x**3/3 + S2*x*x/2 - S3*x)


def gp(x):
    return -4*(x**3 - S1*x*x + S2*x - S3)


def gpp(x):
    return -4*(3*x*x - 2*S1*x + S2)


def f(x, y):
    return g(x) - y*y


def grad2(x, y):
    return gp(x)**2 + 4*y*y


def hessian_bound_interval(xlo, xhi):
    """Smallest integer K >= max(sup |g''| on [xlo, xhi], 2): the operator norm of diag(g''(x), -2).  g'' is a concave
    quadratic, so its extreme values on an interval are at the endpoints or at its vertex."""
    cands = [abs(gpp(xlo)), abs(gpp(xhi)), F(2)]
    vertex = S1/3                             # g'' = -12 x^2 + 8 S1 x - 4 S2 has its maximum at x = S1/3
    if xlo <= vertex <= xhi:
        cands.append(abs(gpp(vertex)))
    m = max(cands)
    K = 1
    while K < m:
        K += 1
    return K


def component_points(t, box, n):
    """Grid points (i, j) of the union-find component of the younger maximum in {f > t}, plus all points above t."""
    h = box*2/n
    pts = {}
    idx = 0
    for i in range(n + 1):
        x = -box + i*h
        gx = g(x)
        for j in range(n + 1):
            y = -box + j*h
            if gx - y*y > t:
                pts[(i, j)] = idx; idx += 1
    parent = list(range(idx))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a

    def union(a, c):
        ra, rc = find(a), find(c)
        if ra != rc:
            parent[ra] = rc
    for (i, j), a in pts.items():
        for (di, dj) in ((1, 0), (0, 1)):
            nb = (i + di, j + dj)
            if nb in pts:
                union(a, pts[nb])
    root_idx = (int((X3 + box)/h), int((F(0) + box)/h))
    if (root_idx[0]*h - box, root_idx[1]*h - box) != (X3, F(0)):
        raise ValueError('younger maximum is not a grid point')
    root = find(pts[root_idx])
    comp = [(i, j) for (i, j), a in pts.items() if find(a) == root]
    other = any(find(a) != root for a in pts.values())
    return pts, comp, other, h


def check_F1(mutant):
    b = g(X3)                                   # younger maximum height
    s = g(X2)                                   # saddle height (death level)
    if not (g(X1) > b > s):
        return False, 'landscape heights out of order'
    if not (gpp(X1) < 0 and gpp(X3) < 0 and gpp(X2) > 0):
        return False, 'critical point types'
    box = F(2)
    n = 200                                     # grid spacing 1/50 on [-2, 2]
    info = {}
    for label, t in (('above_death_level', s + F(1, 1000)), ('at_death_level', s)):
        pts, comp, other, h = component_points(t, box, n)
        xs = [-box + i*h for (i, j) in comp]
        xlo, xhi = min(xs) - h, max(xs) + h
        K = hessian_bound_interval(xlo, xhi)
        if mutant == 'M2':
            K = 1
        factor = 2*K
        if mutant == 'M5':
            factor = K
        tested = list(pts.keys()) if mutant == 'M1' else comp
        checked = 0
        worst = F(0)
        for (i, j) in tested:
            x, y = -box + i*h, -box + j*h
            lhs = grad2(x, y)
            rhs = factor*(b - f(x, y))
            if lhs > rhs:
                return False, 'flat-component inequality fails at (%s, %s) [%s]' % (x, y, label)
            if rhs > 0:
                worst = max(worst, lhs/rhs)
            checked += 1
        info[label] = {'K': K, 'x_interval': [str(xlo), str(xhi)], 'grid_points_above_t': len(pts),
                       'component_points': checked, 'max_ratio_|grad|^2/(2K(b-f))': str(worst.limit_denominator(10**6)),
                       'elder_component_present': other}
    # equality case of (1.1): f = b - K |x|^2 / 2 on a ball (component = the ball), |grad f|^2 = K^2 |x|^2 = 2K (b - f)
    for K in (F(1), F(7, 3), F(56)):
        for x2 in (F(1, 4), F(9), F(1, 1000)):    # |x|^2
            if K*K*x2 != 2*K*(K*x2/2):
                return False, 'equality case of (1.1) fails'
    return True, info


def check_F2(mutant):
    box = F(2)
    n = 200
    pts, comp, other, h = component_points(g(X2) + F(1, 1000), box, n)
    xs = [-box + i*h for (i, j) in comp]
    K = hessian_bound_interval(min(xs) - h, max(xs) + h)
    cnt = 0
    for (x, y) in ((F(1, 2), F(1, 10)), (F(7, 10), F(-1, 5)), (F(1), F(0)), (F(3, 10), F(1, 2))):
        gx, gy = gp(x), -2*y
        gnorm2 = gx*gx + gy*gy
        # exact rational unit direction is not available; use the segment along (gx, gy)/|g| through squares:
        # phi(s) = f(p + s e), s = sigma |g| with sigma rational: p + sigma (gx, gy); then |g| s = sigma |g|^2 rational
        for sigma in (F(1, 8*K), F(1, 4*K), F(1, 2*K), F(1, K)):       # s = sigma |g| <= |g|/K
            q = (x + sigma*gx, y + sigma*gy)
            phi = f(*q)
            lower = f(x, y) + sigma*gnorm2 - K*sigma*sigma*gnorm2/2
            if phi < lower:
                return False, 'uphill segment inequality fails'
            # directional derivative along e at q, times |g|: <grad f(q), g> >= |g|^2 - K s |g| = |g|^2 (1 - K sigma)
            dd = gp(q[0])*gx - 2*q[1]*gy
            if dd < gnorm2*(1 - K*sigma):
                return False, 'monotonicity along the segment fails'
            cnt += 1
    return True, {'segments': cnt, 'K': K}


def check_F3(mutant):
    n = 0
    for k in (F(1, 2), F(1), F(3)):
        for r in (F(1, 10), F(1, 2), F(1)):
            b = F(0)
            ell = k*r**3
            K = 1 + 6*k*r                       # sup |P''| on [-r/2, r/2] is 6 k r
            for m in range(0, 21):
                x = -r/2 + r*F(m, 20)
                # P(x) = b + 6k [ (x^3/3 - r^2 x/4) - ((-r/2)^3/3 - r^2 (-r/2)/4) ], normalised so that P(-r/2) = b
                P = b + 6*k*((x**3/3 - r*r*x/4) - ((-r/2)**3/3 - r*r*(-r/2)/4))
                Pp = 6*k*(x*x - r*r/4)
                if Pp*Pp > 2*K*(b - P):
                    return False, 'near cubic violates (1.1) at k=%s r=%s x=%s' % (k, r, x)
                n += 1
            # lifetime consistency: P(-r/2) - P(r/2) = k r^3
            Pm = b; Pr = b + 6*k*(((r/2)**3/3 - r*r*(r/2)/4) - ((-r/2)**3/3 - r*r*(-r/2)/4))
            if Pm - Pr != ell:
                return False, 'near cubic lifetime'
    return True, {'points': n}


def check_F4(mutant):
    # (sqrt2 + 1)^2 = 3 + 2 sqrt2 < 9  <=>  2 sqrt2 < 6  <=>  8 < 36 ; and > 4 <=> 2 sqrt2 > 1 <=> 8 > 1
    c = F(3)
    if mutant == 'M3':
        c = F(2)
    # is (sqrt2 + 1) < c ?  <=> sqrt2 < c - 1 <=> 2 < (c - 1)^2  (c > 1)
    if not (2 < (c - 1)**2):
        return False, 'gradient constant %s is not an upper bound for sqrt2 + 1' % c
    # 1 + 1/2 + sqrt2 < 3 <=> sqrt2 < 3/2 <=> 2 < 9/4
    if not (2 < F(9, 4)):
        return False, 'value constant'
    return True, {'gradient_constant': str(c), 'value_constant': '3'}


class Mono:
    def __init__(self, ell=F(0), K=F(0)):
        self.ell, self.K = F(ell), F(K)
    def __mul__(self, o):
        return Mono(self.ell + o.ell, self.K + o.K)
    def __pow__(self, e):
        e = F(e); return Mono(self.ell*e, self.K*e)
    def key(self):
        return (self.ell, self.K)


def check_F5(mutant):
    for d in (2, 3, 5):
        for N in (1, 2, 7):
            ell, K0 = Mono(1, 0), Mono(0, 1)
            lhs = (K0*ell**(-1))**F(d*N, 2) * ((K0**F(d, 2))*(ell**(1 + F(d, 2))))**N
            want = (F(N), F(d*N))
            if mutant == 'M4':
                want = (F(N, 2), F(d*N))
            if lhs.key() != want:
                return False, 'exponent ledger fails for d=%d N=%d: %s' % (d, N, lhs.key())
    return True, {'ledger': 'K0^(dN) ell^N'}


def check_F6(mutant):
    for rho in (F(1), F(1, 3), F(6)):
        for N in range(1, 7):
            radii = [F(j, 2*N)*rho for j in range(1, N + 1)]
            hw = rho/(8*N)
            # nearest approach between consecutive shells, and from the origin to the first shell
            gaps = [radii[0] - hw] + [(radii[j + 1] - hw) - (radii[j] + hw) for j in range(N - 1)]
            if min(gaps) < rho/(4*N):
                return False, 'shell separation'
            # from y with |y| >= rho: |y| - (radii[-1] + hw) >= rho/4
            if rho - (radii[-1] + hw) < rho/4:
                return False, 'separation from y'
            # r_ell^2 = ell/K0 <= ell <= rho^2/(64 N^2) = hw^2
            ell = rho*rho/(64*N*N)
            if ell > hw*hw:
                return False, 'ball radius exceeds the shell half-width'
    return True, {'N_range': '1..6', 'separation': 'rho/(4N) between sites, rho/4 from y'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    mutant = args.mutant
    if mutant is not None and mutant not in ('M1', 'M2', 'M3', 'M4', 'M5'):
        sys.stderr.write('unknown mutant label\n'); sys.exit(2)
    results = {}
    ok_all = True
    for name, fn in (('F1_flat_component_two_maxima', check_F1), ('F2_uphill_segment', check_F2),
                     ('F3_near_cubic_consistency', check_F3), ('F4_lemma3_constants', check_F4),
                     ('F5_exponent_ledger', check_F5), ('F6_shell_geometry', check_F6)):
        ok, info = fn(mutant)
        results[name] = {'passed': bool(ok), 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-FAR-ELDER-FLAT-RIDGE-20260930-v1', 'scientific_effect': 'NONE', 'passed': ok_all,
           'checks': results}
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
