"""Exact controls of note C3-R (a rate after the l^{2/3} term): the exponent arithmetic of Theorem C3-R, in exact rationals.

The note's section 4 bounds the normalized remainder R(l) = l^{-2/3}[nu_cand - (main terms) - c3 l^{2/3}] by
    C [ l^{a_eff/3} S^{a_eff+5} + l^{a'/3} S^{5+4a'} + l^{1/3} S^3 + l^{1/3} S^9 + l^{2/3} S^4 log(1/l) + 1/S + l^{1/3} ]
for S = l^{-sigma} with 1 <= S <= S_valid, where
    a     = the localization exponent of Lemma F3-R (eta = r^a), 0 < a < a_max := 1/2 - m theta/2, theta = 1/(16(m+1))
            (the Step 5 constraint 6 kappa |P| >= 2|W| on G cap E);
    a_eff = the exponent of eta' = max(eta, eta^{2/(m-1)}) = r^{min(a, 2a/(m-1))}: a for m = 2, 3 and 2a/(m-1) for m >= 4;
    a'    = the error exponent of Lemma T1-R, 0 < a' < a'_max := (1/2) min(1, 2/(m-1))   (m >= 2; for m = 1, a' = 1);
    S_valid = c l^{-v(a)}, v(a) := (1 - 2a - m theta) / (3 (4 - 2a - m theta))   (condition (V), r^{1-2a-m theta} <= c k (1+k)^{-N},
            in the fold variable r = l^{1/3} s, k = s^{-3}, kappa = l^{-1/3} s^{-4}); also sigma <= 1/12 (kappa >= 1 on s <= S).
For m = 1 the two-eigenvalue terms are void: the F3-R error is r(1 + k^{-2}) and the T1-R error kappa^{-1}; v(a) is
replaced by v_1 := (1 - theta) / (3 (4 - theta)) and the F3-R and T1-R terms are both l^{1/3} S^9.
The rate is (4.0): delta = min(sigma, a_eff/3 - sigma (a_eff + 5), a'/3 - sigma (5 + 4a'), 1/3 - 9 sigma) for admissible
(a, a', sigma) with sigma <= min(v(a), 1/12); the terms l^{1/3} S^3 and l^{2/3} S^4 log(1/l) are dominated by l^{1/3} S^9
for sigma <= 1/12 (the log is absorbed since 2/3 - 4 sigma > 1/3 - 9 sigma), and 1/S = l^{sigma}.

Controls (every check raises AssertionError on failure; `require` is kept under -O):
  E1  the exponent arithmetic of Lemma 4 for d = 2..6: the admissibility of the theorem's stated delta(d) (every term of (4.0)
      at the stated (a, a', sigma) is >= delta(d), the caps hold), the closed-form optimum for m = 2 (a* = 23/60,
      sigma* = 23/1149 >= 1/50), the grid optima for d = 4, 5, 6 as lower bounds;
  E2  0 < v(a) < 1/3 on the admissible range 0 < a < a_max (exact endpoints, monotonicity, a grid), and 0 < v_1 < 1/3;
  E3  the exponents of the terms of (4.1), derived from the substitution r = l^{1/3} s, k = s^{-3}, kappa = l^{-1/3} s^{-4}
      applied to each error term of (1.4) and integrated against s ds up to S = l^{-sigma}, agree with the table `rate_terms`,
      with a_eff derived independently as min(a, 2a/(m-1)).
Standard library only; deterministic; stdout byte-identical under -O.  Mutants: c3r_mutants.py.
"""
import sys
from fractions import Fraction as Fr


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def theta(m):
    return Fr(1, 16 * (m + 1))


def a_max(m):
    return Fr(1, 2) - m * theta(m) / 2


def ap_max(m):
    return Fr(1, 2) * min(Fr(1), Fr(2, m - 1))


def a_eff(m, a):
    """the exponent of eta' = max(eta, eta^{2/(m-1)}) with eta = r^a < 1: a for m = 2, 3 and 2a/(m-1) for m >= 4."""
    return a if m <= 3 else 2 * a / (m - 1)


def rate_terms(m, a, ap, sigma):
    """the exponents of l in the terms of (4.1) with S = l^{-sigma} (log factors ignored), m >= 2, in the order
    [1/S, F3-R (eta' (1 + 1/k)), T1-R (kappa^{-a'}/k), Lemma K (r), the r k^{-2} and r^2 log terms (l^{1/3} S^9), T_r(0)/r]."""
    ae = a_eff(m, a)
    return [sigma, ae / 3 - sigma * (ae + 5), ap / 3 - sigma * (5 + 4 * ap), Fr(1, 3) - 3 * sigma, Fr(1, 3) - 9 * sigma, Fr(2, 3) - 4 * sigma]


def v_of(m, a):
    th = theta(m)
    return (1 - 2 * a - m * th) / (3 * (4 - 2 * a - m * th))


def v_1():
    th = theta(1)
    return (1 - th) / (3 * (4 - th))


def best_rate(m, grid=96):
    """maximize the rate over a rational grid of a in (0, a_max) and a' in (0, a'_max); sigma chosen optimally for each."""
    amax, apmax = a_max(m), ap_max(m)
    best = None
    for i in range(1, grid):
        a = amax * Fr(i, grid)
        for j in range(1, grid + 1):
            ap = apmax * Fr(j, grid) if j < grid else apmax * Fr(grid - 1, grid) + apmax * Fr(1, 2 * grid)
            # the optimal sigma for fixed (a, a'): the first term is increasing in sigma and the others decreasing, so the
            # optimum is at the smallest crossing sigma = term_j(sigma) or at the validity cap
            cap = min(v_of(m, a), Fr(1, 12))
            cands = [cap, a_eff(m, a) / (3 * (a_eff(m, a) + 6)), ap / (3 * (6 + 4 * ap)), Fr(1, 30)]
            for sigma in cands:
                if sigma <= 0 or sigma > cap:
                    continue
                val = min(rate_terms(m, a, ap, sigma))
                if best is None or val > best[0]:
                    best = (val, a, ap, sigma)
    return best


def rate_m1():
    """m = 1 (d = 2): terms l^{1/3} S^9 (F3-R: r(1 + k^{-2})), l^{1/3} S^9 (T1-R: kappa^{-1}/k), l^{1/3} S^3 (K), l^{2/3} S^4 log,
    1/S; sigma <= v_1 and sigma <= 1/12; the optimum is 1/3 - 9 sigma = sigma, sigma = 1/30."""
    v1 = v_1()
    sigma = Fr(1, 30)
    require(sigma <= min(v1, Fr(1, 12)), 'm = 1: sigma within the validity caps')
    terms = [sigma, Fr(1, 3) - 9 * sigma, Fr(1, 3) - 9 * sigma, Fr(1, 3) - 3 * sigma, Fr(2, 3) - 4 * sigma]
    return min(terms), sigma, v1


def admissible(m, a, ap, sigma, delta):
    """E1: (a, a', sigma) is admissible for Lemma 4 and every term of (4.1) has exponent >= delta."""
    require(0 < a < a_max(m), 'm = %d: 0 < a < a_max' % m)
    require(0 < ap < ap_max(m), 'm = %d: 0 < a\' < a\'_max' % m)
    require(0 < sigma <= min(v_of(m, a), Fr(1, 12)), 'm = %d: 0 < sigma <= min(v(a), 1/12)' % m)
    require(all(t >= delta for t in rate_terms(m, a, ap, sigma)), 'm = %d: every term >= delta' % m)


# ---------------------------------------------------------------- E3: the exponents derived from the fold-variable substitution
def fold(r_pow, k_pow, kappa_pow):
    """r^{r_pow} k^{k_pow} kappa^{kappa_pow} = l^{e_l} s^{e_s} under r = l^{1/3} s, k = s^{-3}, kappa = l^{-1/3} s^{-4}."""
    e_l = Fr(r_pow, 3) - Fr(kappa_pow, 3)
    e_s = Fr(r_pow) - 3 * Fr(k_pow) - 4 * Fr(kappa_pow)
    return e_l, e_s


def integrated_exponent(e_l, e_s, sigma):
    """int_0^S s * l^{e_l} s^{e_s} ds = l^{e_l} S^{e_s + 2} / (e_s + 2) with S = l^{-sigma}: the exponent of l."""
    require(e_s + 2 > 0, 'the s-integral converges at 0')
    return e_l - sigma * (e_s + 2)


def derived_terms(m, a, ap, sigma):
    """the exponents of the terms of (4.1), each from the error term's (r, k, kappa) powers; a_eff independently."""
    ae = min(a, 2 * a / (m - 1))                       # eta' = max(r^a, r^{2a/(m-1)}) for r < 1
    split = sigma                                     # 1/S
    f3 = integrated_exponent(*fold(ae, -1, 0), sigma)  # eta' (1 + 1/k): the worst part r^{a_eff} k^{-1}
    t1 = integrated_exponent(*fold(0, -1, -ap), sigma)  # E_T / k = kappa^{-a'} k^{-1}
    lk = integrated_exponent(*fold(1, 0, 0), sigma)    # Lemma K: r (1 + k)^N e^{-c k^2}, the polynomial absorbed on k <= k_G
    pt = integrated_exponent(*fold(1, -2, 0), sigma)   # the r (1 + k^{-2}) part of (F3-R): r k^{-2}
    t0 = integrated_exponent(*fold(2, 0, 0), sigma)    # E_0 = -T_r(0)/r = O(r^2 log(2/r)), the log absorbed
    return [split, f3, t1, lk, pt, t0]


def main():
    out = []
    # ---- E1, d = 2
    d2, s1, v1 = rate_m1()
    out.append('d = 2 (m = 1): delta = %s (sigma = %s; validity cap v_1 = %s)' % (d2, s1, v1))
    require(d2 == Fr(1, 30), 'd = 2: delta = 1/30')
    # ---- E1, the grid optima (lower bounds of the true optima) for d = 3..6
    grid = {}
    for m in range(2, 6):
        val, a, ap, sigma = best_rate(m)
        grid[m] = (val, a, ap, sigma)
        out.append('d = %d (m = %d): delta >= %s = %.5f at a = %s (%.4f), a\' = %s (%.4f), sigma = %s (%.5f); a_max = %s, a\'_max = %s, v(a) = %s (%.5f), theta = %s'
                   % (m + 1, m, val, float(val), a, float(a), ap, float(ap), sigma, float(sigma), a_max(m), ap_max(m), v_of(m, a), float(v_of(m, a)), theta(m)))
        require(val > 0, 'a positive rate exists for m = %d' % m)
        admissible(m, a, ap, sigma, val)
    # ---- E1, the theorem's stated values: d = 3 (closed form), d = 4 (a = 3/8), d = 5, 6 (the grid points)
    th = theta(2)
    a_star = (6 - 12 * th) / 15
    sig_star = a_star / (3 * (a_star + 6))
    require(a_star == Fr(23, 60) and sig_star == Fr(23, 1149), 'm = 2: a* = 23/60, sigma* = 23/1149')
    require(sig_star == v_of(2, a_star), 'm = 2: the crossing a/(3(a+6)) = v(a) is at a* = (6 - 12 theta)/15')
    out.append('d = 3 closed form: a* = %s, sigma* = %s = %.5f >= 1/50: %s (grid optimum %s is a lower bound)' % (a_star, sig_star, float(sig_star), sig_star >= Fr(1, 50), grid[2][0]))
    stated = {2: (Fr(1, 50), a_star, Fr(499, 1000), Fr(1, 50)),
              3: (Fr(1, 51), Fr(3, 8), Fr(499, 1000), Fr(1, 51)),
              4: (Fr(1, 70),) + grid[4][1:],
              5: (Fr(1, 89),) + grid[5][1:]}
    for m in (2, 3, 4, 5):
        delta, a, ap, sigma = stated[m]
        admissible(m, a, ap, sigma, delta)
        terms = rate_terms(m, a, ap, sigma)
        out.append('d = %d stated delta = %s admissible at (a, a\', sigma) = (%s, %s, %s): terms of (4.1) = [%s]' % (m + 1, delta, a, ap, sigma, ', '.join(str(t) for t in terms)))
    require(min(rate_terms(2, a_star, Fr(499, 1000), Fr(1, 50))) == Fr(1, 50), 'd = 3: the split term is exactly 1/50 and binding')
    require(rate_terms(3, Fr(3, 8), Fr(499, 1000), Fr(1, 51))[1] == Fr(1, 51), 'd = 4: the F3-R term equals 1/51 at a = 3/8')
    # ---- E2: 0 < v(a) < 1/3 on 0 < a < a_max; v(a) = n/(3(n+3)) with n = 1 - 2a - m theta decreasing in a, so v decreases
    for m in range(2, 6):
        amax = a_max(m)
        require(v_of(m, amax) == 0 and v_of(m, 0) == (1 - m * theta(m)) / (3 * (4 - m * theta(m))), 'm = %d: v at the endpoints' % m)
        require(0 < v_of(m, 0) < Fr(1, 12), 'm = %d: v(0) < 1/12' % m)
        prev = v_of(m, 0)
        for i in range(1, 200):
            a = amax * Fr(i, 200)
            v = v_of(m, a)
            require(0 < v < prev, 'm = %d: v decreasing and positive on the grid' % m)
            n = 1 - 2 * a - m * theta(m)
            require(v == n / (3 * (n + 3)) and 0 < n, 'm = %d: the form v = n/(3(n+3)), n > 0' % m)
            prev = v
        out.append('E2 m = %d: 0 < v(a) <= v(0) = %s < 1/12 < 1/3 on 0 < a < a_max = %s, v(a_max) = 0' % (m, v_of(m, 0), amax))
    require(0 < v_1() < Fr(1, 12), 'm = 1: 0 < v_1 < 1/12')
    out.append('E2 m = 1: v_1 = %s' % v_1())
    # ---- E3: the exponents derived from the substitution agree with the table, on every grid optimum and stated point
    pts = [grid[m] for m in grid] + [stated[m] for m in stated]
    for m in range(2, 6):
        for (_, a, ap, sigma) in [grid[m], stated[m]]:
            require(derived_terms(m, a, ap, sigma) == rate_terms(m, a, ap, sigma), 'E3 m = %d: derived exponents = table' % m)
    # a few off-optimum points too (every admissible a, a', sigma must agree since both sides are affine in each variable)
    for m in range(2, 6):
        for a in (a_max(m) / 7, a_max(m) / 2, a_max(m) * Fr(9, 10)):
            for ap in (ap_max(m) / 3, ap_max(m) * Fr(4, 5)):
                for sigma in (Fr(1, 100), Fr(1, 40)):
                    require(derived_terms(m, a, ap, sigma) == rate_terms(m, a, ap, sigma), 'E3 m = %d: derived = table off optimum' % m)
    out.append('E3: the exponents of (4.1) derived from r = l^{1/3} s, k = s^{-3}, kappa = l^{-1/3} s^{-4} agree with the table at %d points' % (len(pts) + 4 * 3 * 2 * 2))
    out.append('controls: ALL PASS')
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
