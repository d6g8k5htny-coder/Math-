"""Exact companion for the continuum review of OA-D5-PUNCTURED-PIN-20260928-v1 (PUNCTURED_PIN_PROOF.md).

Standard library, exact rationals. It checks the finite identities on which the reviewed continuum steps rest:
  TAYLOR      (P4)/(P5): pin identities of the cubic + quartic interpolant, the 2x2 system giving u''(0) = O(r^3) and
              u'''(0) = O(r^2) (scaled solution independent of r), the leading derivative terms, and the P5 cubic model.
  FRAME       (P8)/(P9): Cauchy-Binet for the 2x3 block, |a|,|b|,|c| floors attained at p = 1/4, and the Gram floor
              9/131072 on a rational grid of p and Pythagorean (alpha, beta) including both axes; the error ratios
              r^2|p|/Delta, r|q|/Delta, r|p|q^2/Delta, r|q|^3/Delta, r|pq|/Delta, r q^2/Delta are <= r.
  MEAN        (P11): |d| >= (9 k_-/2) chi, since |p - 1| >= 3/4 on |p| <= 1/4.
  NORMALIZER  (P13)/(P14): on S_0 in [-2, -1] with errors <= k_-, H_M is negative definite, H_S indefinite, and both
              |det|/r >= 5 k_-.
  TRIANGLE    (P16)/(P17): coordinate area identity, sine at C = r sigma / ell, r^4 d^2/sigma^4 = r^6 q^2 (1+t^2)^3,
              and r d^2 = r^3 (p^2+q^2).
  REGIONS     (P19)/(P20): chi^2 in [t^2/2, t^2] and q^2/Delta^2 <= 1 in Region I; chi^2 in [1/(2r^2), 1/r^2] and
              (p^2+q^2)/Delta^2 <= 2/r^2 in Region II; the Region II spatial factor stays bounded by 2/r^2 on the axis,
              while the angle-sensitive factor q^2 (1+t^2)^3 / Delta^2 would be unbounded there; power ledger -10 + 12 = 2.
  REFLECTION  §10.1 targets: tilde b - tilde k r^3 = b; determinants and negative indices invariant under reflection.
Mutants (each must fail): wrong-a-floor, drop-minor, angle-sensitive-axis, same-sign-k, absolute-remainder.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("wrong-a-floor", "drop-minor", "angle-sensitive-axis", "same-sign-k", "absolute-remainder")
MUT = None
RS = (F(1, 10), F(1, 100), F(1, 1000))
PS = [F(k, 40) for k in range(-10, 11)]
PYTH = [(F(1), F(0)), (F(0), F(1)), (F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5)), (F(5, 13), F(-12, 13)),
        (F(-8, 17), F(-15, 17)), (F(20, 29), F(21, 29)), (F(-1), F(0))]


def poly_eval(c, x):
    return sum(ci * x ** i for i, ci in enumerate(c))


def poly_der(c):
    return [i * c[i] for i in range(1, len(c))]


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def check_taylor():
    ok = True
    for r in RS:
        for b, k, A4 in ((F(1), F(1, 2), F(3)), (F(-2), F(2), F(-5, 7))):
            H = [b, F(0), -3 * r * k, 2 * k]                               # b + k(2x^3 - 3 r x^2)
            Q = poly_mul(poly_mul([F(0), F(1)], [F(0), F(1)]), poly_mul([-r, F(1)], [-r, F(1)]))  # x^2 (x-r)^2
            g = poly_add(H, [A4 / 24 * c for c in Q])
            dg = poly_der(g)
            ok &= poly_eval(g, 0) == b and poly_eval(dg, 0) == 0          # pins at M
            ok &= poly_eval(g, r) == b - k * r ** 3 and poly_eval(dg, r) == 0
            for p in (F(1, 4), F(-1, 4), F(1, 7), F(-1, 1000)):
                lead = 6 * k * r ** 2 * p * (p - 1) + r ** 3 * A4 / 12 * p * (p - 1) * (2 * p - 1)
                ok &= poly_eval(dg, r * p) == lead
        # u = A x^2/2 + B x^3/6 + remainder: u(r) = e1 = r^5 E1, u'(r) = e2 = r^4 E2  =>  A/r^3, B/r^2 independent of r
        E1, E2 = F(2, 3), F(-5, 4)
        e1, e2 = r ** 5 * E1, r ** 4 * E2
        det = (r * r / 2) * (r * r / 2) - (r ** 3 / 6) * r
        A = ((r * r / 2) * e1 - (r ** 3 / 6) * e2) / det
        B = (-r * e1 + (r * r / 2) * e2) / det
        scale = 1 if MUT == "absolute-remainder" else r ** 3
        ok &= A / scale == 6 * E1 - 2 * E2 and B / r ** 2 == -12 * E1 + 6 * E2
        # (P5) cubic model h = h1 x + T3 x^2/2 + c3 x^3 with h(0) = h(r) = 0
        T3, c3 = F(3, 2), F(-7, 3)
        h1 = -T3 * r / 2 - c3 * r * r
        for p in (F(1, 4), F(-1, 5), F(1, 1000)):
            x = r * p
            h = h1 * x + T3 * x * x / 2 + c3 * x ** 3
            ok &= h - r * r / 2 * p * (p - 1) * T3 == c3 * r ** 3 * p * (p * p - 1)
    return ok


def abc(p):
    a = (p - 1) * (2 * p - 1) / 12
    return a, (p - 1) / 2, p - F(1, 2)


def check_frame():
    ok = True
    a4, b4, c4 = abc(F(1, 4))
    floor_a = F(1, 24) if MUT == "wrong-a-floor" else F(1, 32)
    ok &= a4 == floor_a and b4 == -F(3, 8) and c4 == -F(1, 4)
    for p in PS:
        a, b, c = abc(p)
        ok &= abs(a) >= floor_a and abs(b) >= F(3, 8) and abs(c) >= F(1, 4)
        for al, be in PYTH:
            q = F(1, 16) * be
            B = [[a * al, c * be, F(0), q / 2 * be], [F(0), b * al, be, F(0)]]
            m12, m13, m23 = a * b * al * al, a * al * be, c * be * be
            B3 = [row[:3] for row in B]
            gram3 = [[sum(x * y for x, y in zip(u, v)) for v in B3] for u in B3]
            det3 = gram3[0][0] * gram3[1][1] - gram3[0][1] * gram3[1][0]
            ok &= det3 == m12 ** 2 + m13 ** 2 + m23 ** 2
            gram = [[sum(x * y for x, y in zip(u, v)) for v in B] for u in B]
            det4 = gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]
            lower = m12 ** 2 if MUT == "drop-minor" else m12 ** 2 + m23 ** 2
            ok &= det4 >= det3 >= lower >= F(9, 131072)
    for r in RS:
        for p, q in ((F(1, 4), F(0)), (F(0), F(1, 4)), (F(1, 1000), F(-1, 7)), (F(-1, 5), F(1, 10 ** 6))):
            D2 = q * q + r * r * p * p
            for num in (r * r * abs(p), r * abs(q), r * abs(p) * q * q, r * abs(q) ** 3, r * abs(p * q), r * q * q):
                ok &= num * num <= r * r * D2
    return ok


def check_mean():
    km = F(1, 3)
    ok = True
    for p in PS:
        if p == 0:
            continue
        for q in (F(0), F(1, 9), F(-1, 5)):
            r = F(1, 100)
            D2 = q * q + r * r * p * p
            d2 = (6 * km * p * (p - 1)) ** 2 / D2
            chi2 = p * p / D2
            ok &= d2 >= (F(9, 2) * km) ** 2 * chi2
    return ok


def check_normalizer():
    ok = True
    for km, kp in ((F(1, 2), F(2)), (F(1), F(1))):
        for k in (km, kp):
            for S0 in (F(-2), F(-3, 2), F(-1)):
                for e in (-km, km):
                    fxx_M = -6 * k + e
                    detM = -6 * k * S0 + e
                    detS = 6 * k * S0 + e
                    ok &= fxx_M < 0 and detM > 0 and detS < 0
                    ok &= detM >= 5 * km and -detS >= 5 * km
    return ok


def check_triangle():
    ok = True
    for r in RS:
        for p, q in ((F(1, 5), F(1, 7)), (F(-1, 4), F(1, 100)), (F(0), F(1, 4)), (F(1, 1000), F(-1, 3))):
            A, Bp, C = (F(0), F(0)), (r, F(0)), (r * p, r * q)
            d2 = C[0] ** 2 + C[1] ** 2
            l2 = (Bp[0] - C[0]) ** 2 + (Bp[1] - C[1]) ** 2
            area2 = ((Bp[0] - A[0]) * (C[1] - A[1]) - (Bp[1] - A[1]) * (C[0] - A[0])) ** 2 / 4
            sig2 = q * q / (p * p + q * q)
            ok &= area2 == r * r * d2 * sig2 / 4                          # angle at A
            sigC2 = r * r * sig2 / l2
            ok &= area2 == d2 * l2 * sigC2 / 4                            # angle at C: sin = r sigma / ell
            t2 = (p / q) ** 2
            ok &= r ** 4 * d2 / sig2 ** 2 == r ** 6 * q * q * (1 + t2) ** 3
            ok &= r * d2 == r ** 3 * (p * p + q * q)
    return ok


def check_regions():
    ok = True
    for r in (F(1, 10), F(1, 100)):
        for p in PS:
            for q in (F(1, 4), F(1, 40), F(1, 10 ** 4), F(1, 10 ** 8), F(0)):
                if p == 0 and q == 0:
                    continue
                D2 = q * q + r * r * p * p
                chi2 = p * p / D2
                if q != 0 and q * q >= r * r * p * p:                   # Region I
                    t2 = (p / q) ** 2
                    ok &= t2 / 2 <= chi2 <= t2 and q * q <= D2
                elif q * q < r * r * p * p:                             # Region II
                    ok &= 1 / (2 * r * r) <= chi2 <= 1 / (r * r)
                    spatial = (p * p + q * q) / D2
                    if MUT == "angle-sensitive-axis" and q != 0:
                        spatial = q * q * (1 + (p / q) ** 2) ** 3 / D2
                    ok &= spatial <= 2 / (r * r)
    ok &= -2 - 3 + 3 - 2 - 6 == -10 and -10 + 12 == 2
    return ok


def check_reflection():
    ok = True
    for b, k, r in ((F(1), F(1, 2), F(1, 10)), (F(-3), F(2), F(1, 100))):
        bt = b - k * r ** 3
        kt = k if MUT == "same-sign-k" else -k
        ok &= bt - kt * r ** 3 == b and abs(kt) == k
    R = [[F(-1), F(0)], [F(0), F(1)]]
    for H in ([[F(-2), F(1, 3)], [F(1, 3), F(-1)]], [[F(1), F(2)], [F(2), F(-1)]], [[F(3), F(-1)], [F(-1), F(2)]]):
        Hr = [[sum(R[i][a] * H[a][b2] * R[j][b2] for a in range(2) for b2 in range(2)) for j in range(2)]
              for i in range(2)]
        det = H[0][0] * H[1][1] - H[0][1] ** 2
        detr = Hr[0][0] * Hr[1][1] - Hr[0][1] ** 2
        ok &= det == detr and H[0][0] + H[1][1] == Hr[0][0] + Hr[1][1]
    return ok


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"TAYLOR": check_taylor(), "FRAME": check_frame(), "MEAN": check_mean(),
              "NORMALIZER": check_normalizer(), "TRIANGLE": check_triangle(), "REGIONS": check_regions(),
              "REFLECTION": check_reflection()}
    passed = all(checks.values()) and len(checks) == 7
    print(json.dumps({"object": "CLAUDE-REVIEW-D5-PUNCTURED-PIN-CONTINUUM-20260929-v1", "checks": checks,
                      "passed": passed,
                      "scope": "exact finite identities only; the Gaussian and Kac-Rice steps are reviewed in REVIEW.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
