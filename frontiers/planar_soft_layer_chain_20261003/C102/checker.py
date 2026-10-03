#!/usr/bin/env python3
"""Reviewer-authored exact finite falsification controls; no author imports.

These controls do not prove Gaussian analytic estimates or event theorems.
All mathematical comparisons below use exact rational arithmetic.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256, sha1
from itertools import product
from pathlib import Path
import json
import platform

BASE = Path(__file__).resolve().parents[1]
COUNTS = Counter()
MUTANTS = []


def check(group, condition):
    if not condition:
        raise RuntimeError("independent control failed: " + group)
    COUNTS[group] += 1


def reject(name, false_proposition):
    if false_proposition:
        raise RuntimeError("mutant was not rejected: " + name)
    MUTANTS.append(name)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def trans(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[dot(row, col) for col in trans(b)] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def subtract(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def det(a):
    x = [[F(v) for v in row] for row in a]
    d = F(1)
    for i in range(len(x)):
        pivot = next((j for j in range(i, len(x)) if x[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            x[pivot], x[i] = x[i], x[pivot]
            d = -d
        p = x[i][i]
        d *= p
        for j in range(i + 1, len(x)):
            scale = x[j][i] / p
            for k in range(i + 1, len(x)):
                x[j][k] -= scale * x[i][k]
    return d


def inverse(a):
    n = len(a)
    x = [[F(v) for v in row] + unit for row, unit in zip(a, eye(n))]
    for i in range(n):
        p = next(j for j in range(i, n) if x[j][i])
        x[i], x[p] = x[p], x[i]
        scale = x[i][i]
        x[i] = [v / scale for v in x[i]]
        for j in range(n):
            if j != i:
                scale = x[j][i]
                x[j] = [u - scale * v for u, v in zip(x[j], x[i])]
    return [row[n:] for row in x]


def d2(x):
    a, c, b = x
    return a * b - c * c


def inertia(x):
    """Independent determinant/trace classification, singular case separate."""
    determinant = d2(x)
    if determinant == 0:
        return None
    if determinant < 0:
        return 1
    return 2 if x[0] + x[2] < 0 else 0


def filtered(j, x):
    return abs(d2(x)) if inertia(x) == j else F(0)


def typed_product(m, s):
    return filtered(2, m) * filtered(1, s)


def model(lam, gamma, bjet):
    return ((F(-6), -gamma / 2, -lam - bjet / 2),
            (F(6), gamma / 2, -lam + bjet / 2))


def observations(r, degree):
    lo, hi = -r / 2, r / 2
    f = lambda x: x ** degree
    fp = lambda x: F(degree) * x ** (degree - 1) if degree else F(0)
    return [(f(lo) + f(hi)) / 2,
            (f(hi) - f(lo)) / r,
            (fp(hi) - fp(lo)) / r,
            (6 / r**2) * (fp(lo) + fp(hi) - 2 * (f(hi) - f(lo)) / r)]


def interval_union_length(intervals):
    parts = sorted((a, b) for a, b in intervals if a < b)
    if not parts:
        return F(0)
    left, right = parts[0]
    total = F(0)
    for a, b in parts[1:]:
        if a <= right:
            right = max(right, b)
        else:
            total += right - left
            left, right = a, b
    return total + right - left


proof = (BASE / "PROOF.md").read_bytes()
check("source_binding", len(proof) == 28794)
check("source_binding", sha256(proof).hexdigest() ==
      "1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628")
expected = {
    "C91": (12433, "74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa"),
    "C92": (19567, "6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a"),
    "P": (40261, "9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7"),
    "E1": (1782, "bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028"),
    "E2": (9062, "845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f"),
    "REC": (23312, "451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da"),
    "CUB": (19889, "117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0"),
}
identities = json.loads((BASE / "SOURCE_IDENTITIES.json").read_text())
check("source_binding", {i["key"] for i in identities} == set(expected))
for item in identities:
    data = (BASE / item["local_path"]).read_bytes()
    actual = len(data), sha256(data).hexdigest()
    check("source_binding", actual == expected[item["key"]])
    check("source_binding", actual == (item["bytes"], item["sha256"]))
    if "blob" in item:
        header = ("blob " + str(len(data)) + "\0").encode()
        check("source_binding", sha1(header + data).hexdigest() == item["blob"])

rs = [F(1, 32), F(1, 7), F(1, 2), F(1)]
ks = [F(1, 4), F(2, 3), F(1), F(3, 2), F(4)]
for r in rs:
    transform = [
        [F(1, 2), 0, F(1, 2), 0, 0, 0],
        [-1 / r, 0, 1 / r, 0, 0, 0],
        [0, -1 / r, 0, 1 / r, 0, 0],
        [12 / r**3, 6 / r**2, -12 / r**3, 6 / r**2, 0, 0],
        [0, 0, 0, 0, F(1, 2), F(1, 2)],
        [0, 0, 0, 0, -1 / r, 1 / r],
    ]
    check("contact_frame", abs(det(transform)) == 12 / r**5)
    for k, birth in product(ks, [F(-3), F(0), F(7, 5)]):
        pins = [birth, 0, birth - k * r**3, 0, 0, 0]
        target = [birth - k * r**3 / 2, -k * r**2, 0, 12 * k, 0, 0]
        check("contact_frame", [dot(row, pins) for row in transform] == target)
    for degree in range(11):
        u = observations(r, degree)
        h = r / 2
        exact = [h**degree if degree % 2 == 0 else F(0),
                 h**(degree - 1) if degree % 2 else F(0),
                 F(degree) * h**(degree - 2) if degree > 0 and degree % 2 == 0 else F(0),
                 F(12 * (degree - 1)) * h**(degree - 1) / r**2
                 if degree % 2 else F(0)]
        check("centered_monomials", u == exact)
    check("centered_monomials", observations(r, 3)[3] == 6)
    check("centered_monomials", observations(r, 5)[3] == 120 * r**2 / 40)
    check("centered_monomials", observations(r, 7)[3] == 5040 * r**4 / 4480)

powers = [(i, j) for i in range(4) for j in range(4 - i)]
nodes = powers
frames = [(F(1), F(0), 1), (F(0), F(1), 1),
          (F(3, 5), F(4, 5), 1), (F(3, 5), F(4, 5), -1),
          (F(-5, 13), F(12, 13), 1)]
for cs, sn, orientation in frames:
    rotated = [(cs * x + sn * y, orientation * (-sn * x + cs * y))
               for x, y in nodes]
    evaluation = [[x**a * z**b for a, b in powers] for x, z in rotated]
    check("jet_rank_witness", det(evaluation) != 0)

# Finite latent Gaussian example: actual projection algebra, not a field-law
# simulation. The analytic report handles the infinite-dimensional estimates.
v = [[F(x) for x in row] for row in
     [[1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1]]]
gamma = mm(v, trans(v))
regression = mm(trans(v), inverse(gamma))
residual = subtract(eye(4), mm(regression, v))
check("regression_algebra", mm(v, regression) == eye(3))
check("regression_algebra", residual == trans(residual))
check("regression_algebra", mm(residual, residual) == residual)
check("regression_algebra", mm(v, residual) == [[0] * 4 for _ in range(3)])
check("regression_algebra", all(0 <= residual[i][i] <= 1 for i in range(4)))
u = v[:2]
u_residual = subtract(eye(4), mm(mm(trans(u), inverse(mm(u, trans(u)))), u))
evaluation = [[F(x) for x in [1, 2, 3, 4]]]
variance = mm(mm(evaluation, u_residual), trans(evaluation))[0][0]
check("regression_algebra", variance == 16)
schur = gamma[2][2] - dot(gamma[2][:2],
                         [dot(row, gamma[2][:2]) for row in inverse([r[:2] for r in gamma[:2]])])
check("regression_algebra", schur == F(4, 3))
for k in ks:
    target = [[F(3)], [12 * k], [F(5, 7)]]
    check("regression_algebra", mm(v, mm(regression, target)) == target)
    if k != 1:
        check("regression_algebra", k**2 * variance != variance)
reject("amplitude-scaled residual retains original covariance", F(4)**2 * variance == variance)

grid = [F(-3), F(-1), F(-1, 4), F(0), F(1, 4), F(1), F(3)]
for k, a, c, b in product(ks, grid, grid, grid):
    physical = (a, c, b)
    scaled = (a / k, c, k * b)
    check("anisotropic_congruence", d2(physical) == d2(scaled))
    check("anisotropic_congruence", inertia(physical) == inertia(scaled))
for r, k in product(rs, ks):
    jac = det([[r / k, 0, 0, 0], [0, 1, 0, 0],
               [0, 0, 1 / k, 0], [0, 0, 0, 1 / k**2]])
    check("physical_jacobian", jac == r / k**4)
    check("physical_jacobian", r**(-5) * jac * r**4 == k**(-4))
for lam, a, bjet, k in product(grid, grid, grid, ks):
    m, s = model(lam, a, bjet)
    # Differentiate physical cubic directly at its two pins, then transform.
    p_m = (-6 * k, -a / 2, -lam / k - bjet / (2 * k))
    p_s = (6 * k, a / 2, -lam / k + bjet / (2 * k))
    check("cubic_endpoint", (p_m[0] / k, p_m[1], k * p_m[2]) == m)
    check("cubic_endpoint", (p_s[0] / k, p_s[1], k * p_s[2]) == s)
    check("cubic_endpoint", typed_product(p_m, p_s) == typed_product(m, s))
    hm = 6 * lam + 3 * bjet - a*a / 4
    hs = 6 * lam - 3 * bjet + a*a / 4
    w = max(hm, 0) * max(hs, 0)
    check("typed_model", w == typed_product(m, s))
    check("typed_model", 0 <= w <= 36 * max(lam, 0)**2)
    check("typed_model", w == 0 or lam > 0)

for alpha, c, a in product(grid, grid, grid):
    matrix, diagonal = (alpha, c, a), (alpha, F(0), a)
    for index in [1, 2]:
        check("offdiagonal_quadratic", abs(filtered(index, matrix) - filtered(index, diagonal)) <= c*c)
for root_r, alpha, beta, a in product([F(1, 8), F(1, 3), F(1)], grid, grid, grid):
    r = root_r**2
    h = (r * alpha, r * beta, a)
    congruent = (alpha, root_r * beta, a)
    check("full_normalizer_congruence", d2(congruent) == d2(h) / r)
    check("full_normalizer_congruence", inertia(congruent) == inertia(h))
for k, a in product(ks, grid):
    result = typed_product((-6 * k, F(0), a), (6 * k, F(0), a))
    check("full_normalizer_reference", result == (36 * k*k * a*a if a < 0 else 0))

for cutoff, delta, gamma_jet, bjet in product(
        [F(0), F(1, 8), F(1), F(8), F(64)],
        [F(1, 100), F(1, 3), F(1)], grid, grid):
    h = 1 + cutoff
    d = 3 * bjet - gamma_jet**2 / 4
    centers = [-d / 6, d / 6]
    length = interval_union_length(
        [(max(-cutoff, c - delta/24), min(cutoff, c + delta/24)) for c in centers])
    check("typing_strips", length <= delta / 6)
    left = abs(d) / 6
    right = min(cutoff, left + delta / 24)
    mass = (12 * (right**3 - left**3) - d*d * (right - left)) if right > left else F(0)
    check("typing_strips", 0 <= mass <= h * delta**2)
    check("typing_strips", max(F(0), right - left) <= delta / 24)

# This quartic perturbation vanishes with its gradient along zeta=0, has
# no midpoint jet of degree <=3, and changes each endpoint zz Hessian by -eps.
for eps in [F(1, 128), F(1, 7), F(1)]:
    lam = -eps / 2
    m, s = model(lam, F(0), F(0))
    actual_m = (m[0], m[1], m[2] - eps)
    actual_s = (s[0], s[1], s[2] - eps)
    check("outside_model_leakage", typed_product(m, s) == 0)
    check("outside_model_leakage", typed_product(actual_m, actual_s) == 9 * eps**2 > 0)
    check("outside_model_leakage", -4 * eps * F(1, 2)**2 == -eps)

for kmin, h, m, p in product([F(1, 4), F(1), F(3)],
                            [F(1), F(3), F(100)], [F(1), F(2), F(5)], [0, 1, 2, 5]):
    r = min(F(1), kmin / h)
    check("cutoff_moment_ledger", r * h / kmin <= 1)
    check("cutoff_moment_ledger", h*h*m**p + r*h**3*m**(p+7) <= (1+kmin)*h*h*m**(p+7))

for r, z, mass in product(rs, [F(1, 7), F(2)], [F(0), F(3, 5)]):
    soft_numerator = r**5 * mass
    full_z = r**2 * z
    check("normalization_ledger", r**(-3) * soft_numerator / full_z == mass / z)
for r, pi, z in product(rs, [F(1, 11), F(2)], [F(1, 7), F(3)]):
    check("candidate_ledger", (12*r**(-5)*pi) * r * r**3 * (r*r*z) == r*(12*pi*z))
for beta in [F(1, 7), F(1, 2), F(1), F(2)]:
    check("prospective_consumer", F(-1, 3) + (3 + beta) / 3 == (2 + beta) / 3)
    check("prospective_consumer", F(-2, 3) - 1 == F(-5, 3))
    check("prospective_consumer", min(beta, F(1)) <= 1)

reject("physical Jacobian omits k^-4", F(1, 5) / F(2)**4 == F(1, 5))
reject("physical Jacobian inverts k^-4", F(1, 5) / F(2)**4 == F(1, 5) * F(2)**4)
reject("extra k^4 on determinant product", typed_product((-12, 0, -F(1, 2)), (12, 0, -F(1, 2))) == F(2)**4 * 36)
reject("saddle uses absolute determinant without type", filtered(1, (-1, 0, -1)) == 1)
reject("maximum uses positive determinant without type", filtered(2, (1, 0, 1)) == 1)
reject("model uses absolute rather than positive factors", typed_product(*model(F(-1), F(0), F(0))) == 36)
reject("actual off-T weight assumed zero", typed_product((-6, 0, -F(1, 14)), (6, 0, -F(1, 14))) == 0)
reject("sqrt-r congruence replaces inverse-sqrt-r", d2((F(-3, 8), F(1, 8), F(-2))) == d2((F(-3, 2), F(1, 4), F(-2))) / F(1, 4))
reject("offdiagonal filtered determinant change discarded", filtered(1, (1, 1, 0)) == filtered(1, (1, 0, 0)))
reject("full normalizer replaced by soft r^5 scale", F(-3) + F(5) - F(5) == 0)
reject("joint density loses A marginal", F(3, 7) * F(5, 11) == F(5, 11))
reject("pin density drops factor 12", F(12) == F(1))
reject("ordered maximum/saddle population divided by two", F(12) == F(6))
reject("height transformation drops r^3", F(-5) + 1 + 2 == 1)
reject("prospective loss coefficient has k^-2/3", F(-5, 3) == F(-2, 3))
reject("prefactor permits arbitrary beta>1 error", min(F(2), F(1)) == F(2))
reject("finite-r law inferred from contact parity", F(4)**2 * variance == variance)

print("C102 reviewer independent finite controls PASS")
print("Python " + platform.python_version())
for group, count in sorted(COUNTS.items()):
    print(group + ": " + str(count))
print("exact controls: " + str(sum(COUNTS.values())))
print("rejected mutants: " + str(len(MUTANTS)))
for name in MUTANTS:
    print("REJECT " + name)
print("No author checker read/imported/executed; finite checks do not prove analytic rates.")
