"""Checks for the D1 chain reconciliation (D1-CHAIN-RECONCILIATION-20260928-v1).

Python standard library only. Exact rational arithmetic, except one clearly labelled numerical check of (15.2).
Run from the repository root or from this directory. Groups:

  CUSTODY  every bound source and local review record matches its Git blob, byte count and SHA256.
  LEDGER   every interface has a full-depth ACCEPT from a nonauthor provider; author-provider reviews never
           discharge; P and CAP line ranges are covered exactly; every theorem cites accepted interfaces; every
           residual item is discharged. Two synthetic negative controls must be rejected.
  MATH     the reading-rule mathematics: erratum E1 versus the displayed factor; (5.3); (6.1) and (6.2), including
           the extremal equality case; (7.3); the (7.5) split and its nonempty far branch; the cap constants and
           kappa-scaling; the embedding radius; the radial ledger and |det T_r|; (11.1)-(11.3) and the difference
           exponent; the section 12 integrals; (13.1); and (15.2), numerically.

Not an analytic proof: the reviews C1, G1, G2, G4 and RECONCILIATION.md section 6 carry the arguments.
"""
import argparse
import hashlib
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MUTANTS = ("allow-author-review", "skip-coverage", "displayed-congruence", "drop-mixed-square",
           "drop-far-branch", "embedding-radius", "difference-exponent", "gamma-24")


# ---------------------------------------------------------------------------------------------------------------
# Custody
# ---------------------------------------------------------------------------------------------------------------

def git_blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def identity_ok(rec):
    data = (ROOT / rec["path"]).read_bytes()
    ok = (len(data) == rec["bytes"] and hashlib.sha256(data).hexdigest() == rec["sha256"]
          and git_blob(data) == rec["git_blob"])
    if "lines" in rec:
        ok &= data.decode("utf-8").count("\n") == rec["lines"]
    return ok


def check_custody(ledger):
    out = {}
    for group in ("sources", "local_records"):
        for key, rec in ledger[group].items():
            out[f"{group}.{key}"] = identity_ok(rec)
    return out


# ---------------------------------------------------------------------------------------------------------------
# Ledger rules
# ---------------------------------------------------------------------------------------------------------------

def discharging(ledger, iface, mut):
    authors = set(ledger["author_providers"])
    provs = set()
    for rv in iface["reviews"]:
        prov = ledger["reviews"][rv["by"]]["provider"]
        if rv["verdict"] != "ACCEPT" or rv["depth"] != "full":
            continue
        if prov in authors and mut != "allow-author-review":
            continue
        provs.add(prov)
    return provs


def coverage_ok(ledger, mut):
    if mut == "skip-coverage":
        return True
    for src in ("P", "CAP"):
        n = ledger["sources"][src]["lines"]
        hit = [0] * (n + 1)
        for iface in ledger["interfaces"]:
            if iface["source"] == src:
                for a, b in iface["lines"]:
                    for i in range(a, b + 1):
                        hit[i] += 1
        for m in ledger["meta_ranges"].get(src, []):
            a, b = m["lines"]
            for i in range(a, b + 1):
                hit[i] += 1
        if any(h != 1 for h in hit[1:]):
            return False
    return True


def ledger_rules(ledger, mut):
    ids = {i["id"] for i in ledger["interfaces"]}
    every_discharged = all(discharging(ledger, i, mut) for i in ledger["interfaces"])
    theorems_ok = all(set(v) <= ids for v in ledger["theorems"].values())
    residual_ok = all(r["status"] == "DISCHARGED" and r["discharged_by"] and
                      all(d in ids or d.startswith("RECONCILIATION.md") for d in r["discharged_by"])
                      for r in ledger["residual_items"])
    reviews_known = all(rv["by"] in ledger["reviews"] for i in ledger["interfaces"] for rv in i["reviews"])
    return every_discharged, coverage_ok(ledger, mut), theorems_ok, residual_ok, reviews_known


def check_ledger(ledger, mut):
    out = {}
    d, c, t, r, k = ledger_rules(ledger, mut)
    out["every_interface_has_nonauthor_full_accept"] = d
    out["P_and_CAP_lines_covered_exactly_once"] = c
    out["theorems_cite_known_interfaces"] = t
    out["every_residual_item_discharged"] = r
    out["every_review_is_registered"] = k
    # Negative control 1: an interface whose only ACCEPT is by the author provider must not be discharged.
    neg = json.loads(json.dumps(ledger))
    neg["interfaces"].append({"id": "NEG", "source": "E1", "lines": "all", "component": "x", "claim": "x",
                              "reviews": [{"by": "O1", "verdict": "ACCEPT", "depth": "full"}]})
    out["author_only_interface_rejected"] = not ledger_rules(neg, mut)[0]
    # Negative control 2: removing the section 11 interface must break coverage.
    neg2 = json.loads(json.dumps(ledger))
    neg2["interfaces"] = [i for i in neg2["interfaces"] if i["id"] != "S11"]
    out["coverage_gap_rejected"] = not ledger_rules(neg2, mut)[1]
    # Provider counts: the providers that discharge each interface (reported, not asserted beyond >= 1).
    out["discharging_provider_counts"] = {i["id"]: len(discharging(ledger, i, None)) for i in ledger["interfaces"]}
    return out


# ---------------------------------------------------------------------------------------------------------------
# Exact linear algebra helpers
# ---------------------------------------------------------------------------------------------------------------

def det(A):
    n = len(A)
    M = [list(r) for r in A]
    d = F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return d


def adj(A):
    n = len(A)
    if n == 1:
        return [[F(1)]]
    C = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [r[:j] + r[j + 1:] for k, r in enumerate(A) if k != i]
            C[j][i] = (-1) ** (i + j) * det(minor)
    return C


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def solve_inv(A):
    n = len(A)
    M = [list(A[i]) + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [r[n:] for r in M]


def rational_orthogonal(rng, m):
    """Cayley transform of a random rational skew matrix: an exactly orthogonal rational matrix."""
    S = [[F(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            v = F(rng.randrange(-5, 6), rng.randrange(1, 5))
            S[i][j], S[j][i] = v, -v
    I = [[F(int(i == j)) for j in range(m)] for i in range(m)]
    IminusS = [[I[i][j] - S[i][j] for j in range(m)] for i in range(m)]
    IplusS = [[I[i][j] + S[i][j] for j in range(m)] for i in range(m)]
    return matmul(solve_inv(IminusS), IplusS)


def block(alpha, beta, A):
    m = len(A)
    return [[alpha] + list(beta)] + [[beta[i]] + list(A[i]) for i in range(m)]


# ---------------------------------------------------------------------------------------------------------------
# Mathematics
# ---------------------------------------------------------------------------------------------------------------

def check_math(mut):
    rng = random.Random(63)
    out = {}
    # E1 and (5.3): H = [[r a, r b^T],[r b, A]], r = s^2.
    ok_e1, ok_53, ok_old_singular = True, True, True
    for _ in range(90):
        m = rng.choice((1, 2, 3))
        s = F(rng.randrange(1, 30), 31)
        r = s * s
        a = F(rng.randrange(-9, 10), rng.randrange(1, 4))
        b = [F(rng.randrange(-9, 10), rng.randrange(1, 4)) for _ in range(m)]
        A = [[F(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                A[i][j] = A[j][i] = F(rng.randrange(-9, 10), rng.randrange(1, 4))
        H = block(r * a, [r * x for x in b], A)
        d = F(1) / s if mut != "displayed-congruence" else s
        D = [[d if (i == j == 0) else F(int(i == j)) for j in range(m + 1)] for i in range(m + 1)]
        K = matmul(matmul(D, H), D)
        ok_e1 &= K == block(a, [s * x for x in b], A) and det(K) == det(H) / r
        adjA = adj(A)
        quad = sum(b[i] * adjA[i][j] * b[j] for i in range(m) for j in range(m))
        ok_53 &= det(H) == r * (a * det(A) - r * quad)
        Dold = [[s if (i == j == 0) else F(int(i == j)) for j in range(m + 1)] for i in range(m + 1)]
        ok_old_singular &= matmul(matmul(Dold, H), Dold)[0][0] == r * r * a
    out["E1_congruence_scaled_matrix_and_det"] = ok_e1
    out["block_determinant_5_3"] = ok_53
    out["displayed_factor_puts_r2_alpha_in_corner"] = ok_old_singular
    # (6.1) and (6.2) on exact instances with rational spectra, plus the extremal equality case.
    ok61, ok62, eq62 = True, True, True
    c32 = F(1) if mut == "drop-mixed-square" else F(3, 2)
    for trial in range(120):
        m = rng.choice((1, 2, 3))
        Q = rational_orthogonal(rng, m)
        lam = sorted(F(rng.randrange(1, 40), rng.randrange(1, 6)) for _ in range(m))
        B = matmul(matmul(Q, [[lam[i] if i == j else F(0) for j in range(m)] for i in range(m)]), transpose(Q))
        AM = [[-x for x in row] for row in B]
        h = F(rng.randrange(1, 30), rng.randrange(1, 4))
        r = F(1, rng.randrange(2, 60))
        # maximum endpoint: alpha < 0, ||beta||^2 <= h^2/4, H_M < 0
        aM = -F(rng.randrange(1, 100), 100) * h / 2
        bM = [F(rng.randrange(-10, 11), 20) * h / 2 / m for _ in range(m)]
        HM = block(r * aM, [r * x for x in bM], AM)
        negdef = all(det([row[:k] for row in [[-x for x in rr] for rr in HM][:k]]) > 0 for k in range(1, m + 2))
        if negdef:
            ok61 &= abs(det(HM)) <= r * (h / 2) * det(B)
        # saddle endpoint: ||A_S - A_M||_F <= r h (Frobenius dominates the operator norm)
        extremal = trial % 3 == 0
        if extremal:
            AS = [[-(B[i][j] + (r * h if i == j else 0)) for j in range(m)] for i in range(m)]
            aS = h / 2
            v1 = [Q[i][0] for i in range(m)]
            bS = [h / 2 * x for x in v1]
        else:
            E = [[F(0)] * m for _ in range(m)]
            for i in range(m):
                for j in range(i, m):
                    E[i][j] = E[j][i] = F(rng.randrange(-10, 11), 10 * m * m) * r * h
            AS = [[AM[i][j] + E[i][j] for j in range(m)] for i in range(m)]
            aS = F(rng.randrange(-100, 101), 100) * h / 2
            bS = [F(rng.randrange(-10, 11), 20) * h / 2 / m for _ in range(m)]
        HS = block(r * aS, [r * x for x in bS], AS)
        bound = r * (h / 2) * (lam[0] + c32 * r * h)
        for j in range(1, m):
            bound *= lam[j] + r * h
        ok62 &= abs(det(HS)) <= bound
        if extremal:
            eq62 &= abs(det(HS)) == r * (h / 2) * (lam[0] + F(3, 2) * r * h) * math.prod(
                [lam[j] + r * h for j in range(1, m)], start=F(1))
    out["canceled_pivot_6_1"] = ok61
    out["two_soft_factors_6_2"] = ok62
    out["6_2_extremal_equality"] = eq62
    # (7.3) identity.
    ok73 = True
    for _ in range(40):
        Dc, Ec, Uc, r = (F(rng.randrange(1, 20), rng.randrange(1, 5)) for _ in range(4))
        top = Dc * r * Uc ** 2
        lhs = top ** 3 / 3 + Ec * r * Uc * top ** 2 / 2
        ok73 &= lhs == r ** 3 * (Dc ** 3 / 3 * Uc ** 6 + Ec * Dc ** 2 / 2 * Uc ** 5)
    out["depth_failure_integral_7_3"] = ok73
    # (7.5): majorant event {lam <= Dr (J+lam)^2} lies in {lam <= 4DrJ^2} or {lam > 1/(4Dr)}; far part nonempty.
    ok75, far_nonempty = True, True
    for _ in range(400):
        Dr = F(1, rng.randrange(2, 400))
        J = F(rng.randrange(10, 60), 10)
        lam = F(rng.randrange(1, 4000), rng.randrange(1, 40))
        if lam <= Dr * (J + lam) ** 2:
            near = lam <= 4 * Dr * J ** 2
            far = lam > 1 / (4 * Dr)
            ok75 &= near or (far and mut != "drop-far-branch")
        big = 1 / Dr + F(rng.randrange(0, 100))
        far_nonempty &= big <= Dr * (J + big) ** 2
    out["m1_split_7_5"] = ok75
    out["m1_far_branch_nonempty_in_majorant"] = far_nonempty
    # Cap constants and kappa-scaling (normalized kappa = 1/6: lambda > 8 r m^2, r n <= 1/20).
    u = F(2, 11) + F(2, 121)
    mu = F(48, 121)
    out["cap_constants"] = (u == F(24, 121) and (1 + F(6, 11) + F(5, 121)) / 4 == mu
                            and mu * (3 + 3 * u + u * u) == F(2554128, 1771561)
                            and F(7, 4) - F(2554128, 1771561) == F(2184415, 7086244) > F(1, 4)
                            and F(9, 32) - F(1, 6) == F(11, 96)
                            and F(22, 2) * F(20, 11) ** 2 == F(4400, 121) > F(1, 6))
    kappa = F(1, 6)
    out["cap_kappa_scaling"] = (8 * 6 * kappa / (36 * kappa ** 2) == F(4) / (3 * kappa)
                                and 6 * kappa / 20 == 3 * kappa / 10 == F(1, 20))
    # Exterior integral of (x-a)(x-c)/8 from -2r to a (r = 1): 9/32.
    xs = lambda x: x ** 3 / 3 - x / 4
    out["cap_exterior_integral_9_32"] = (xs(F(-1, 2)) - xs(F(-2))) / 8 == F(9, 32)
    # Embedding radius: D = [-2r,2r] x B(0,2r) has max squared norm 8 r^2; embedded iff 8 r^2 < L^2/4.
    ok_emb = True
    for L in (F(1), F(24), F(7, 3)):
        for num in range(1, 60):
            r = L * F(num, 200)
            embedded = 8 * r * r < L * L / 4
            claimed = (r * r < L * L / 32) if mut != "embedding-radius" else (r < L / 4)
            ok_emb &= embedded == claimed
    out["embedding_radius_L_over_4_sqrt2"] = ok_emb
    # Radial ledger: |det T_r| = 12 r^-(d+3) and exponent (d-1)+3-(d+3)+2 = 1.
    ok_T = True
    for r in (F(1, 3), F(2, 7), F(1, 11)):
        a, c = -r / 2, r / 2
        # rows of U0..U3 on (f(a), f_x(a), f(c), f_x(c))
        T = [[F(1, 2), 0, F(1, 2), 0], [-1 / r, 0, 1 / r, 0], [0, -1 / r, 0, 1 / r],
             [F(12) / r ** 3, 6 / r ** 2, -F(12) / r ** 3, 6 / r ** 2]]
        T = [[F(x) for x in row] for row in T]
        ok_T &= abs(det(T)) == 12 / r ** 4 and abs(det([[F(1, 2), F(1, 2)], [-1 / r, 1 / r]])) == 1 / r
    out["contact_jacobian_12_r_minus_d_plus_3"] = ok_T and all((d - 1) + 3 - (d + 3) + 2 == 1 for d in range(2, 12))
    # (11.1): with k = a^3 and l = k r^3, r dr/dl = 1/(3 k r) = (1/3) k^(-2/3) l^(-1/3).
    ok111 = True
    for _ in range(40):
        a = F(rng.randrange(1, 9), rng.randrange(1, 9))
        k, r = a ** 3, F(rng.randrange(1, 50), 100)
        l13 = a * r                      # l^(1/3)
        ok111 &= r / (3 * k * r * r) == F(1, 3) / (a * a) / l13
    out["pushforward_jacobian_11_1"] = ok111
    out["coefficient_factor_12_over_3_is_4"] = F(12, 3) == 4
    le, ke = F(-1, 3) + 1, F(-2, 3) - (0 if mut == "difference-exponent" else 1)
    out["difference_exponent_l_2_3_k_minus_5_3"] = (le, ke) == (F(2, 3), F(-5, 3))
    # Section 12: integral_0^t l^p = t^(p+1)/(p+1) for p > -1.
    out["section12_integrals"] = (1 / (F(-1, 3) + 1) == F(3, 2) and 1 / (F(2, 3) + 1) == F(3, 5)
                                  and all(F(q) - F(1, 3) + 1 == F(q) + F(2, 3) for q in range(-0, 5))
                                  and all(F(q) + F(2, 3) + 1 == F(q) + F(5, 3) for q in range(0, 5)))
    # (13.1): (b - k r^3/2)^2 + 144 k^2 >= (b^2 + k^2)/2 for 0 < r <= 1.
    ok131 = True
    for _ in range(500):
        b = F(rng.randrange(-400, 401), rng.randrange(1, 9))
        k = F(rng.randrange(0, 400), rng.randrange(1, 9))
        r = F(rng.randrange(1, 101), 100)
        ok131 &= (b - k * r ** 3 / 2) ** 2 + 144 * k * k >= (b * b + k * k) / 2
    out["target_coercivity_13_1"] = ok131
    # (15.2) gamma factor, numerical (float): 144 int_0^inf k^(4/3) phi_tau(12k) dk.
    ok152 = True
    for tau in (0.5, 1.0, 2.5):
        # substitute t = 12k = u^3: integrand becomes 12^(-1/3) * 3 u^6 phi_tau(u^3), smooth at 0.
        n, top = 20000, (12.0 * tau) ** (1.0 / 3.0)
        hh = top / n
        f = lambda uu: 3 * uu ** 6 * math.exp(-uu ** 6 / (2 * tau * tau)) / (tau * math.sqrt(2 * math.pi))
        simpson = f(0) + f(top) + sum((4 if i % 2 else 2) * f(i * hh) for i in range(1, n))
        val = 12 ** (-1.0 / 3.0) * simpson * hh / 3
        base = 12 if mut == "gamma-24" else 24
        closed = math.gamma(7 / 6) * tau ** (4 / 3) / (base ** (1 / 3) * math.sqrt(math.pi))
        ok152 &= abs(val - closed) <= 1e-9 * closed
    out["gamma_factor_15_2_numerical_1e-9"] = ok152
    out["coefficient_power_bookkeeping"] = 4 * 36 == 144 and F(-2, 3) + 2 == F(4, 3)
    return out


def flatten(d):
    for k, v in d.items():
        if isinstance(v, dict):
            if k != "discharging_provider_counts":
                yield from flatten(v)
        else:
            yield v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    ledger = json.loads((HERE / "LEDGER.json").read_text())
    checks = {"CUSTODY": check_custody(ledger), "LEDGER": check_ledger(ledger, mut), "MATH": check_math(mut)}
    passed = all(flatten(checks))
    print(json.dumps({"checks": checks, "object": ledger["object"], "passed": passed,
                      "scope": "custody, ledger rules and exact reading-rule identities; one numerical (15.2) check; "
                               "not an analytic proof"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
