"""Exact companion for CL-SARD-PINNED-TRANSFER-20260929-v1 (PROOF.md). Standard library, exact rationals.

Circle trigonometric model, modes 0..K with positive rational weights (covariance Sigma = diag(w) in coefficient
coordinates, H inner product <a,b>_H = a^T Sigma^-1 b). Pins: value and derivative at x_a = theta and x_b = 2 theta,
cos theta = 3/5 (all trigonometric values rational).
  RANK        the four pin functionals are independent on trigonometric polynomials.
  CORRECTION  h = tau - sum_i (J tau)_i psi_i with dual psi_i satisfies J h = 0 exactly; the correction is linear in J tau.
  PROJECTION  Pi_P(Sigma l) lies in H_P (J annihilates it) and <h, Pi_P Sigma l>_H = l(h) for h in H_P.
  SPAN        projected point-evaluation images at further Pythagorean points span H_P (dimension 2K+1-4).
Mutants (each must fail): no-correction, unprojected, duplicate-pin.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("no-correction", "unprojected", "duplicate-pin")
MUT = None
K = 3
N = 2 * K + 1
W = [F(1)] + [F(1, 2 ** k) for k in range(1, K + 1) for _ in (0, 1)]


def angle_pow(m):
    c, s = F(1), F(0)
    for _ in range(m):
        c, s = c * F(3, 5) - s * F(4, 5), s * F(3, 5) + c * F(4, 5)
    return c, s


def eval_rows(m):
    """value and derivative functionals at x = m*theta in coefficient coordinates."""
    c1, s1 = angle_pow(m)
    cs, ss = [F(1)], [F(0)]
    for _ in range(K):
        cs.append(cs[-1] * c1 - ss[-1] * s1)
        ss.append(ss[-1] * c1 + cs[-2] * s1)
    val, der = [F(1)], [F(0)]
    for k in range(1, K + 1):
        val += [cs[k], ss[k]]
        der += [-k * ss[k], k * cs[k]]
    return val, der


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def inverse(A):
    n = len(A)
    M = [list(A[i]) + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [r[n:] for r in M]


def rank(rows):
    M = [list(r) for r in rows]
    rk = 0
    for col in range(len(M[0])):
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


def check():
    out = {}
    va, da = eval_rows(1)
    vb, db = eval_rows(2) if MUT != "duplicate-pin" else eval_rows(1)
    J = [va, da, vb, db]
    out["pin_functionals_independent"] = rank(J) == 4
    if not out["pin_functionals_independent"]:
        return out
    Jt = transpose(J)
    # dual trigonometric polynomials psi = J^T (J J^T)^-1 (columns)
    Psi = matmul(Jt, inverse(matmul(J, Jt)))
    ok = True
    for tau in ([F(j + 1, 7) for j in range(N)], [F((-1) ** j * (j + 2), 3) for j in range(N)]):
        Jtau = [sum(r[i] * tau[i] for i in range(N)) for r in J]
        corr = [sum(Psi[i][c] * Jtau[c] for c in range(4)) for i in range(N)]
        h = tau if MUT == "no-correction" else [t - c for t, c in zip(tau, corr)]
        ok &= all(sum(r[i] * h[i] for i in range(N)) == 0 for r in J)
        # linearity of the correction in J tau
        corr2 = [sum(Psi[i][c] * 2 * Jtau[c] for c in range(4)) for i in range(N)]
        ok &= all(c2 == 2 * c for c, c2 in zip(corr, corr2))
    out["corrected_approximant_satisfies_pins"] = ok
    # projection Pi_P k = k - Sigma J^T (J Sigma J^T)^-1 J k
    S = [[W[i] if i == j else F(0) for j in range(N)] for i in range(N)]
    G = inverse(matmul(matmul(J, S), Jt))
    SJt = matmul(S, Jt)

    def proj(k):
        Jk = [sum(r[i] * k[i] for i in range(N)) for r in J]
        coeff = [sum(G[a][b] * Jk[b] for b in range(4)) for a in range(4)]
        return [k[i] - sum(SJt[i][a] * coeff[a] for a in range(4)) for i in range(N)]

    ok_in = ok_rep = True
    hP = [F(0)] * N
    # an element of H_P: correct a generic vector
    tau = [F(j * j + 1, 5) for j in range(N)]
    Jtau = [sum(r[i] * tau[i] for i in range(N)) for r in J]
    hP = [t - sum(Psi[i][c] * Jtau[c] for c in range(4)) for i, t in enumerate(tau)]
    for m in (3, 4, 5):
        l, _ = eval_rows(m)
        Sl = [W[i] * l[i] for i in range(N)]
        k = Sl if MUT == "unprojected" else proj(Sl)
        ok_in &= all(sum(r[i] * k[i] for i in range(N)) == 0 for r in J)
        ok_rep &= sum(hP[i] * k[i] / W[i] for i in range(N)) == sum(l[i] * hP[i] for i in range(N))
    out["projected_images_lie_in_H_P"] = ok_in
    out["reproducing_identity_on_H_P"] = ok_rep
    imgs = [proj([W[i] * eval_rows(m)[0][i] for i in range(N)]) for m in range(3, 3 + N)]
    out["projected_point_evaluations_span_H_P"] = rank(imgs) == N - 4
    return out


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = check()
    passed = all(checks.values()) and len(checks) == 5
    print(json.dumps({"object": "CL-SARD-PINNED-TRANSFER-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite-dimensional illustrations only"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
