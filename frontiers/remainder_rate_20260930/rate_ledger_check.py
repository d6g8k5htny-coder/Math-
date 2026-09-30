#!/usr/bin/env python3
"""Exact finite controls for PROOF.md (CL-D2-REMAINDER-RATE-20260930-v1).  Standard library only; exact rationals.

  E1  the exponent ledger of section 3: with rho = ell^theta the seven terms of (3.1)(i)-(iv) have exponents
      theta, 2 - 7 theta, 1/4, theta, 1/3 - theta, 4/3 - 5 theta, 1/3; at theta = 1/6 the minimum is 1/6; over a
      rational grid of theta in (0, 1/3) and at every breakpoint the minimum never exceeds 1/6 (optimality within
      the ledger: min(theta, 1/3 - theta) <= 1/6 identically); at rational twelfth powers ell = q^12 every term is
      <= ell^(1/6) exactly, so the assembled bound is 7 C ell^(1/6); mutant M1 claims the rate 1/4;
  E2  the barrier arithmetic of [182] section 3 (8)-(9): for rational 0 < lambda <= K, a_L <= 1 and 0 < t <= a_L
      lambda / K, (K/6) t^3 <= (lambda/6) t^2 and b - (lambda/2) t^2 + (K/6) t^3 <= b - (lambda/3) t^2 exactly; the
      solved form b - d >= c_L lambda^3 / K^2  <=>  lambda <= ((b - d) K^2 / c_L)^(1/3) at rational cubes; mutant M2
      uses the radius 2 lambda / K;
  E3  the determinant / soft-eigenvalue inequality (1.3): for rational symmetric positive definite matrices
      O diag(lambda) O^T with rational orthogonal O (Cayley transforms of rational skew-symmetric matrices),
      det <= lambda_min lambda_max^(d-1), and lambda_max <= Frobenius norm; mutant M3 uses the exponent d - 2;
  E4  the integrals of Lemma B and the cutoff ledger of [C7-K] section 4: int_rho^r0 (ell r^-6 + r^-2) dr =
      ell (rho^-5 - r0^-5)/5 + rho^-1 - r0^-1 <= ell rho^-5 / 5 + rho^-1 exactly at rationals; the second piece
      ell^(-1/3) ell^(2/3) 3 (ell/rho^3)^(-1/3) = 3 rho and the first piece ell^(-1/3) (3/5) ell k_*^(-5/3) =
      (3/5) ell^(1/4) at k_* = ell^(1/4), at rational twelfth powers.
  M   mutants (--mutant M1|M2|M3) exit 1; an unknown label exits 2.
  Scope: E1-E4 check exponent bookkeeping, the barrier's algebra and a linear-algebra inequality at rational
  points.  They do NOT test Lemma B or Lemma F' as statements about the Gaussian laws, nor the assembly's use of
  Math-#191 (R+.3) and [C7-K] section 4; those are prose only.  The controls are not acceptance.
"""
import argparse
import json
import sys
from fractions import Fraction as F


# ----------------------------------------------------------------------------------------------------- helpers

def det(A):
    n = len(A)
    M = [row[:] for row in A]
    d = F(1)
    for i in range(n):
        p = None
        for r in range(i, n):
            if M[r][i] != 0:
                p = r
                break
        if p is None:
            return F(0)
        if p != i:
            M[i], M[p] = M[p], M[i]
            d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= f * M[i][c]
    return d


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def transpose(A):
    return [list(r) for r in zip(*A)]


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(A):
    n = len(A)
    M = [row[:] + identity(n)[i] for i, row in enumerate(A)]
    for i in range(n):
        p = next(r for r in range(i, n) if M[r][i] != 0)
        M[i], M[p] = M[p], M[i]
        piv = M[i][i]
        M[i] = [x / piv for x in M[i]]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i]
                M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [row[n:] for row in M]


def cayley(S):
    """Rational orthogonal matrix (I - S)(I + S)^{-1} for rational skew-symmetric S."""
    n = len(S)
    I = identity(n)
    A = [[I[i][j] - S[i][j] for j in range(n)] for i in range(n)]
    B = [[I[i][j] + S[i][j] for j in range(n)] for i in range(n)]
    return matmul(A, inverse(B))


def is_cube(x):
    """Exact rational cube root if x is a rational cube, else None."""
    if x < 0:
        r = is_cube(-x)
        return None if r is None else -r
    n, d = x.numerator, x.denominator

    def iroot3(m):
        lo, hi = 0, 1
        while hi ** 3 <= m:
            hi *= 2
        while lo < hi:
            mid = (lo + hi) // 2
            if mid ** 3 < m:
                lo = mid + 1
            else:
                hi = mid
        return lo if lo ** 3 == m else None

    a, b = iroot3(n), iroot3(d)
    return None if a is None or b is None else F(a, b)


# ---------------------------------------------------------------------------------------------------- checks

def ledger_terms(theta, mutant):
    """Exponents of the seven terms of (3.1)(i)-(iv) with rho = ell^theta."""
    return [theta, 2 - 7 * theta, F(1, 4), theta, F(1, 3) - theta, F(4, 3) - 5 * theta, F(1, 3)]


def check_E1(mutant):
    claimed = F(1, 4) if mutant == 'M1' else F(1, 6)
    theta_star = claimed  # rho = ell^gamma is forced by the two rho-terms
    m = min(ledger_terms(theta_star, mutant))
    if m != claimed:
        return False, 'ledger minimum at theta = %s is %s, not the claimed rate %s' % (theta_star, m, claimed)
    # optimality within the ledger: the minimum never exceeds 1/6 on a rational grid and at the breakpoints
    grid = [F(i, 600) for i in range(1, 200)]
    breakpoints = [F(1, 6), F(1, 4), F(1, 8), F(2, 9), F(5, 24), F(1, 12), F(7, 30)]
    for theta in grid + breakpoints:
        if min(ledger_terms(theta, mutant)) > F(1, 6):
            return False, 'ledger minimum exceeds 1/6 at theta = %s' % theta
    # exact assembled bound at rational twelfth powers: every term <= ell^(1/6)
    checked = 0
    for q in (F(1, 2), F(1, 3), F(2, 7), F(1, 10)):
        ell = q ** 12
        rho = q ** 2                                   # ell^(1/6)
        terms = [rho, ell ** 2 / rho ** 7, q ** 3, rho, q ** 4 / rho, q ** 16 / rho ** 5, q ** 4]
        # q^3 = ell^(1/4), q^4 = ell^(1/3), q^16 = ell^(4/3)
        if ell ** 2 / rho ** 7 != q ** 10 or q ** 4 / rho != q ** 2 or q ** 16 / rho ** 5 != q ** 6:
            return False, 'monomial substitution'
        if any(t > rho for t in terms):
            return False, 'a ledger term exceeds ell^(1/6) at q = %s' % q
        if sum(terms) > 7 * rho:
            return False, 'assembled bound'
        checked += 1
    # relative form: ell^(1/6) / ell^(-1/3) = ell^(1/2)
    if F(1, 6) - (-F(1, 3)) != F(1, 2):
        return False, 'relative exponent'
    return True, {'theta': str(theta_star), 'rate': str(claimed), 'grid_points': len(grid) + len(breakpoints),
                  'twelfth_power_points': checked, 'relative_exponent': '1/2'}


def check_E2(mutant):
    cases = 0
    for L in (F(1), F(24), F(1, 2)):
        a_L = min(F(1), L / 4)
        c_L = a_L * a_L / 3
        for lam, K in ((F(1, 5), F(3)), (F(2), F(2)), (F(1, 100), F(7, 2)), (F(3, 4), F(1))):
            if not (0 < lam <= K):
                return False, 'test data'
            R = (2 * lam / K) if mutant == 'M2' else a_L * lam / K
            for frac in (F(1, 7), F(1, 2), F(9, 10), F(1)):
                t = frac * R
                if not ((K / 6) * t ** 3 <= (lam / 6) * t ** 2):
                    return False, 'cubic term not dominated at t = %s (lambda %s, K %s)' % (t, lam, K)
                b = F(5, 3)
                if not (b - (lam / 2) * t ** 2 + (K / 6) * t ** 3 <= b - (lam / 3) * t ** 2):
                    return False, 'barrier inequality (8)'
                cases += 1
            # (9): d_f <= b - lambda R^2 / 3, i.e. b - d >= c_L lambda^3 / K^2 with R = a_L lambda / K
            if mutant != 'M2' and lam * R * R / 3 != c_L * lam ** 3 / K ** 2:
                return False, 'lambda R^2 / 3 != c_L lambda^3 / K^2'
    # solved form at rational cubes: b - d >= c_L lambda^3 / K^2  <=>  lambda <= ((b - d) K^2 / c_L)^(1/3)
    a_L = F(1)
    c_L = a_L * a_L / 3
    solved = 0
    for lam, K, gap in ((F(1, 2), F(2), F(2, 3)), (F(1), F(1), F(1, 3)), (F(2), F(1), F(8, 3)), (F(3), F(3), F(1, 27))):
        lhs = gap >= c_L * lam ** 3 / K ** 2
        cube = is_cube(gap * K * K / c_L)
        if cube is None:
            return False, 'test point is not a rational cube'
        rhs = lam <= cube
        if lhs != rhs:
            return False, 'solved form of (9) fails'
        solved += 1
    return True, {'barrier_cases': cases, 'solved_form_points': solved}


def check_E3(mutant):
    exp = -2 if mutant == 'M3' else -1  # det <= lambda_min * lambda_max^(d + exp)
    skews = [
        [[F(0), F(1, 2)], [F(-1, 2), F(0)]],
        [[F(0), F(1, 3), F(-2)], [F(-1, 3), F(0), F(1, 5)], [F(2), F(-1, 5), F(0)]],
        [[F(0), F(1), F(0), F(1, 2)], [F(-1), F(0), F(1, 3), F(0)], [F(0), F(-1, 3), F(0), F(2)], [F(-1, 2), F(0), F(-2), F(0)]],
    ]
    spectra = [
        [F(1, 100), F(2)],
        [F(1, 10), F(3, 2), F(5)],
        [F(1, 7), F(1, 3), F(2), F(9, 2)],
        [F(3), F(3)],
        [F(1, 50), F(1, 50), F(4)],
    ]
    cases = 0
    for S in skews:
        n = len(S)
        O = cayley(S)
        # orthogonality, exactly
        if matmul(transpose(O), O) != identity(n):
            return False, 'Cayley transform not orthogonal'
        for lam in spectra:
            if len(lam) != n:
                continue
            D = [[lam[i] if i == j else F(0) for j in range(n)] for i in range(n)]
            A = matmul(matmul(O, D), transpose(O))
            if transpose(A) != A:
                return False, 'not symmetric'
            dA = det(A)
            prod = F(1)
            for x in lam:
                prod *= x
            if dA != prod:
                return False, 'determinant != product of eigenvalues'
            lmin, lmax = min(lam), max(lam)
            if not (dA <= lmin * lmax ** (n + exp)):
                return False, 'det <= lambda_min lambda_max^(d-1) fails (spectrum %s)' % [str(x) for x in lam]
            frob2 = sum(A[i][j] ** 2 for i in range(n) for j in range(n))
            if not (lmax ** 2 <= frob2):
                return False, 'lambda_max <= Frobenius fails'
            cases += 1
    if cases == 0:
        return False, 'no cases'
    return True, {'matrices': cases, 'sizes': [2, 3, 4]}


def check_E4(mutant):
    # Lemma B integral, exact antiderivative
    pts = 0
    for ell, rho, r0 in ((F(1, 1000), F(1, 10), F(1, 2)), (F(1, 64), F(1, 4), F(1)), (F(3, 1000), F(1, 5), F(2, 5))):
        exact = ell * (rho ** -5 - r0 ** -5) / 5 + (rho ** -1 - r0 ** -1)
        # antiderivative of ell r^-6 + r^-2 is -ell r^-5 / 5 - r^-1
        anti = lambda r: -ell * r ** -5 / 5 - r ** -1
        if anti(r0) - anti(rho) != exact:
            return False, 'antiderivative'
        if not (exact <= ell * rho ** -5 / 5 + rho ** -1):
            return False, 'integral bound'
        pts += 1
    # [C7-K] section 4 pieces at rational twelfth powers ell = q^12, rho = q^3 * s (so ell / rho^3 = (q / s)^3)
    pieces = 0
    for q, s in ((F(1, 2), F(1)), (F(1, 3), F(2)), (F(2, 5), F(3, 2))):
        ell = q ** 12
        rho = s * q ** 3
        ell13 = q ** 4      # ell^(1/3)
        ell23 = q ** 8      # ell^(2/3)
        ell14 = q ** 3      # ell^(1/4) = k_*
        # second piece: ell^(-1/3) * ell^(2/3) * 3 * (ell/rho^3)^(-1/3) = 3 rho
        cube = is_cube(ell / rho ** 3)
        if cube is None:
            return False, 'ell/rho^3 not a cube'
        second = ell23 / ell13 * 3 / cube
        if second != 3 * rho:
            return False, 'second piece != 3 rho'
        # first piece: ell^(-1/3) * (3/5) * ell * k_*^(-5/3) with k_* = ell^(1/4): k_*^(5/3) = q^5
        first = (F(3, 5) * ell / q ** 5) / ell13
        if first != F(3, 5) * ell14:
            return False, 'first piece != (3/5) ell^(1/4)'
        pieces += 1
    return True, {'integral_points': pts, 'cutoff_ledger_points': pieces}


CHECKS = [('E1_exponent_ledger', check_E1), ('E2_barrier_arithmetic', check_E2),
          ('E3_soft_eigenvalue_determinant', check_E3), ('E4_integrals_and_cutoff_ledger', check_E4)]
MUTANTS = ('M1', 'M2', 'M3')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    mutant = args.mutant
    if mutant is not None and mutant not in MUTANTS:
        sys.stderr.write('unknown mutant label\n')
        return 2
    results = {}
    ok_all = True
    for name, fn in CHECKS:
        ok, info = fn(mutant)
        results[name] = {'passed': ok, 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-D2-REMAINDER-RATE-20260930-v1', 'scientific_effect': 'NONE', 'passed': ok_all,
           'mutant': mutant, 'checks': results}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
