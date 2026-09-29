"""Independent nonauthor finite checks for OA-SARD-ROBUST-CHARTS-20260929-v1 slice R3/R4 (Math-#135). Exact rationals.

MODEL    a trigonometric Gaussian field on the circle with modes 0..K and positive rational weights, in coefficient
         coordinates (covariance Sigma = diag(w)); point evaluations at x_m = m*theta with cos(theta) = 3/5, so every
         cos(k x_m), sin(k x_m) is rational (Chebyshev recursion) and {x_m} is dense (theta/pi irrational).
RKHS     (R3a) <h, Sigma l>_H = l(h) for h = Sigma a, with <Sigma a, Sigma b>_H = a^T Sigma b.
SPAN     the images Sigma l_{x_m} span the Cameron-Martin space (rank 2K+1) once m runs over 2K+1 points; fewer points
         are rank-deficient (control). Single point evaluations already suffice (note N1).
RESIDUAL (R3b)-(R3c) unnormalized: xi = l(f), h = Sigma l / v, g = f - xi h gives Cov(a(g), xi) = 0 for all a
         (checked on a basis); a degenerate l (v = 0) in a singular model must be removed.
ZEROS    (R4) a C1 function with accumulating singular zeros: regular zeros are isolated, hence countable; exact
         model F(t) = t^2 sin-free polynomial surrogate with a double zero and simple zeros.
Mutants (each must fail): wrong-residual, keep-degenerate, span-deficient.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("wrong-residual", "keep-degenerate", "span-deficient")
MUT = None
K = 3
W = [F(1)] + [F(1, 2 ** k) for k in range(1, K + 1) for _ in (0, 1)]   # weights for 1, cos x, sin x, cos 2x, ...


def trig(c, s, kmax):
    """cos(kx), sin(kx) for k = 0..kmax from cos x = c, sin x = s (exact)."""
    cs, ss = [F(1)], [F(0)]
    for _ in range(kmax):
        cs.append(cs[-1] * c - ss[-1] * s)
        ss.append(ss[-1] * c + cs[-2] * s)
    return cs, ss


def point_eval(m):
    c, s = F(1), F(0)
    for _ in range(m):                                   # x_m = m theta, cos theta = 3/5, sin theta = 4/5
        c, s = c * F(3, 5) - s * F(4, 5), s * F(3, 5) + c * F(4, 5)
    cs, ss = trig(c, s, K)
    vec = [F(1)]
    for k in range(1, K + 1):
        vec += [cs[k], ss[k]]
    return vec


def rank(rows):
    M = [list(r) for r in rows]
    rk = 0
    for col in range(len(M[0]) if M else 0):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk


def sig(v, w=W):
    return [wi * vi for wi, vi in zip(w, v)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def check():
    out = {}
    n = 2 * K + 1
    # RKHS identity: <Sigma a, Sigma l>_H = a^T Sigma l = l(Sigma a)
    ok = True
    for m in range(4):
        l = point_eval(m)
        for a in ([F(1)] + [F(0)] * (n - 1), [F(j + 1, 3) for j in range(n)]):
            h = sig(a)
            ok &= dot(a, sig(l)) == dot(l, h)
    out["R3a_rkhs_identity"] = ok
    npts = n - 1 if MUT == "span-deficient" else n
    imgs = [sig(point_eval(m)) for m in range(npts)]
    out["span_of_point_evaluation_images_is_full"] = rank(imgs) == n
    out["fewer_points_rank_deficient_control"] = rank([sig(point_eval(m)) for m in range(n - 1)]) < n
    # residual: xi = l(f), h = Sigma l / v, g = f - xi h; Cov(a(g), xi) = a^T Sigma l - (a^T h) v = 0
    ok = True
    for m in range(1, 4):
        l = point_eval(m)
        v = dot(l, sig(l))
        h = [x / v for x in sig(l)] if MUT != "wrong-residual" else sig(l)
        for j in range(n):
            a = [F(int(i == j)) for i in range(n)]
            ok &= dot(a, sig(l)) - dot(a, h) * v == 0
    out["R3c_residual_uncorrelated"] = ok
    # degenerate direction in a singular model (last weight zero): l supported on that mode has v = 0 and is removed
    Ws = W[:-1] + [F(0)]
    l_deg = [F(0)] * (n - 1) + [F(1)]
    v_deg = dot(l_deg, sig(l_deg, Ws))
    kept = [l for l in (point_eval(1), l_deg) if dot(l, sig(l, Ws)) != 0 or MUT == "keep-degenerate"]
    out["degenerate_direction_removed"] = v_deg == 0 and all(dot(l, sig(l, Ws)) != 0 for l in kept)
    # (R4) isolated regular zeros: F(t) = t^2 (t - 1)(t + 2): simple zeros at 1, -2 have F' != 0, the double zero at 0
    # has F'(0) = 0; F is C1 and the regular zeros are isolated, hence countable
    Fp = lambda t: 4 * t ** 3 + 3 * t ** 2 - 4 * t        # derivative of t^4 + t^3 - 2 t^2
    Fv = lambda t: t ** 4 + t ** 3 - 2 * t ** 2
    out["regular_zeros_have_nonzero_derivative"] = all(Fv(t) == 0 and Fp(t) != 0 for t in (F(1), F(-2))) and Fp(F(0)) == 0
    return out


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = check()
    passed = all(checks.values())
    print(json.dumps({"object": "CLAUDE-REVIEW-SARD-G-R3R4-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite illustrations only; not the Banach-space proof"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
