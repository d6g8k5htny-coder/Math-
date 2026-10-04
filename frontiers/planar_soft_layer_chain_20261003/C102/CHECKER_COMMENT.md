# C102 independent nonauthor controls — exact executable and design

OpenAI/Codex `/root/c99_custody_audit`, acting for Dylan Roy — delegated AI work. Companion to [full substantive scoped review](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967434317). Same-provider/source-exposed nonauthor reviewer; independence credit 0; human review NONE; personal reading PENDING. Root and `reader_surface_audit` are author-side. These are reviewer-authored finite controls, not analytic proof substitutes. No C102 author checker implementation, separate author control design or author execution output was read/imported/run.

Bound proof: [comment5967305153](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967305153), 28794 bytes, SHA256 `1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628`. Reviewer design/script frozen before first run at 2026-10-03T08:49:04.613029+00:00. Python3.11.16 normal `-B -S` and optimized `-B -S -O` both exited 0: **19176 exact checks / 18 rejected mutants**, identical stdout and empty stderr. No code repair or rerun beyond these two modes. Counts include repeated rational fixtures and identity checks.

Extraction rule: each payload is the exact content of the single fenced block between its matching BEGIN/END markers. Exclude the marker and fence lines, preserve every payload byte including its final LF. Each payload length/hash is published below. The source manifest intentionally retains its original bytes. Place the checker in `review/` beside the packet `PROOF.md`, `SOURCE_IDENTITIES.json` and seven `sources/*.md` files. The normal stdout below is also the exact optimized stdout. This publication changes no register, proof, source or governing status. Root owns separate delivery/release.

## Exact DESIGN.txt

UTF-8 bytes: 3898; SHA256 `cee0d0f7bc87f66383e2e85fbd62f700c73742af7bda195637e9a069b5e5f7e8`.

<!-- BEGIN C102 DESIGN.txt EXACT UTF8 -->
```text
C102 independent review design — frozen before any author-checker exposure

Reviewer: OpenAI/Codex /root/c99_custody_audit, acting for Dylan Roy as delegated AI.
Target: PROOF.md, 28794 UTF-8 bytes, SHA256
1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628.
Source set: the seven original snapshots C91, C92, P, E1, E2, REC, CUB
listed in ../SOURCE_IDENTITIES.json, all byte/hash checked against their
recorded identities and available predecessor copies before this design.

Exposure and role
- This reviewer read the seven original sources and the frozen proof.
- No C102 authorship, proof suggestion, draft edit, or author-checker exposure.
- Root01a0bbb5 and reader_surface_audit are author-side, excluded from the
  nonauthor verdict. This reviewer is source-exposed and same-provider:
  organizational/provider independence credit 0; human review NONE.
- C101 exposure was custody extraction/replay of author controls, not review;
  C101 is not a source of C102 and no C101 argument is consumed here.

Private source-preparation checklist (no proof contribution)
1. Original covariance and continuous regression: P §§2–4 and C92 J1–J2;
   positive spectrum, ten-jet rank, compact frame/mark uniformity, bounded
   conditional targets; no amplitude identification of different gap laws.
2. Physical rather than normalized jet density: CUB G1/G6/G10 and C92 J3;
   include the A marginal and all anisotropic coordinate Jacobians.
3. Determinants/types: C91 endpoint Taylor control; CUB coordinate convention;
   preserve inertia, zero filtered determinants on singular matrices, and
   actual correlated conditional remainders rather than independent samples.
4. FULL normalizer: P §5 read with E1 and REC W1; distinguish its r² scale
   from the soft numerator's r⁵ scale; justify a positive compact floor and
   the new quantitative rate separately from the source's qualitative limit.
5. Candidate population: E2 disintegration and P §§10–12; retain factor 12,
   ordinary circle measure, ordered roles, height Jacobian and full Z.
   Prospective event/rate inputs must remain explicitly conditional.

Independent falsification-control plan
A. Exact rational six-observation transform, target, determinant, centered
   monomial expansion, and finite polynomial-rank witnesses in several frames.
B. Exact finite Gaussian projection/Schur-complement algebra, target-independent
   residual covariance, and rejection of amplitude scaling for k != 1.
C. Physical jet Jacobian r/k⁴; direct Hessian differentiation of the cubic;
   anisotropic congruence, determinants and inertia on signed/singular grids.
D. Filtered determinant off-diagonal c² bound, corrected E1 congruence, full
   normalizer reference product, and absence of an extra soft restriction.
E. Positive-part product bound, exact typing-strip lengths and polynomial
   integrals, plus an explicit endpoint-preserving quartic fixture with actual
   positive weight outside the model typed set.
F. Cutoff/moment exponents, one common-radius admissibility condition, normalized
   measure powers, candidate prefactor, ordered-pair factor and prospective
   lifetime-loss powers. Deliberately wrong Jacobian, determinant, typing,
   full-normalizer and population conventions must be rejected.

Analytic review remains separate from finite controls
The report must independently audit all six lemmas, including infinite Fourier
summability, uniform covariance derivatives, actual conditional C⁴ moments,
Gaussian interpolation, the cutoff-independent radius, absolute strip estimates,
full Z floor/rate and pin-density/prefactor rates. Finite rational controls cannot
prove these analytic statements or discharge a new event/tail theorem.

No author checker or output is needed for this review; controls will not import
or execute either. No source/proof edits, external writes or register changes.
```
<!-- END C102 DESIGN.txt EXACT UTF8 -->

## Exact independent_controls.py

UTF-8 bytes: 14039; SHA256 `5004c0220e86337a8e91dce65c8da99240349ef029d23d219340d75da1399822`.

<!-- BEGIN C102 independent_controls.py EXACT UTF8 -->
```python
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
```
<!-- END C102 independent_controls.py EXACT UTF8 -->

## Exact controls.normal.stdout

UTF-8 bytes: 1461; SHA256 `d9cc859ae2244785d1fd7bc201f30e3458199877cb785fcbb69a8df3db331173`.

<!-- BEGIN C102 controls.normal.stdout EXACT UTF8 -->
```text
C102 reviewer independent finite controls PASS
Python 3.11.16
anisotropic_congruence: 3430
candidate_ledger: 16
centered_monomials: 56
contact_frame: 64
cubic_endpoint: 5145
cutoff_moment_ledger: 216
full_normalizer_congruence: 2058
full_normalizer_reference: 35
jet_rank_witness: 5
normalization_ledger: 16
offdiagonal_quadratic: 686
outside_model_leakage: 9
physical_jacobian: 40
prospective_consumer: 12
regression_algebra: 16
source_binding: 22
typed_model: 5145
typing_strips: 2205
exact controls: 19176
rejected mutants: 18
REJECT amplitude-scaled residual retains original covariance
REJECT physical Jacobian omits k^-4
REJECT physical Jacobian inverts k^-4
REJECT extra k^4 on determinant product
REJECT saddle uses absolute determinant without type
REJECT maximum uses positive determinant without type
REJECT model uses absolute rather than positive factors
REJECT actual off-T weight assumed zero
REJECT sqrt-r congruence replaces inverse-sqrt-r
REJECT offdiagonal filtered determinant change discarded
REJECT full normalizer replaced by soft r^5 scale
REJECT joint density loses A marginal
REJECT pin density drops factor 12
REJECT ordered maximum/saddle population divided by two
REJECT height transformation drops r^3
REJECT prospective loss coefficient has k^-2/3
REJECT prefactor permits arbitrary beta>1 error
REJECT finite-r law inferred from contact parity
No author checker read/imported/executed; finite checks do not prove analytic rates.
```
<!-- END C102 controls.normal.stdout EXACT UTF8 -->

## Exact CONTROLS_FREEZE.json

UTF-8 bytes: 548; SHA256 `af4b4ba2d317e8b977bfcbc27c3e055a1ed433e6059390191fadb29767f61146`.

<!-- BEGIN C102 CONTROLS_FREEZE.json EXACT UTF8 -->
```json
{
  "frozen_at_utc": "2026-10-03T08:49:04.613029+00:00",
  "reviewer": "/root/c99_custody_audit",
  "proof_sha256": "1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628",
  "author_checker_exposed": false,
  "author_outputs_exposed": false,
  "files": {
    "DESIGN.txt": {
      "bytes": 3898,
      "sha256": "cee0d0f7bc87f66383e2e85fbd62f700c73742af7bda195637e9a069b5e5f7e8"
    },
    "independent_controls.py": {
      "bytes": 14039,
      "sha256": "5004c0220e86337a8e91dce65c8da99240349ef029d23d219340d75da1399822"
    }
  }
}
```
<!-- END C102 CONTROLS_FREEZE.json EXACT UTF8 -->

## Exact CONTROL_RUNS.json

UTF-8 bytes: 1348; SHA256 `1fcb4208b1512d3e56c2593017dd10efade5d97f148bfa3be055250719577cbe`.

<!-- BEGIN C102 CONTROL_RUNS.json EXACT UTF8 -->
```json
{
  "python": "3.11.16 (main, Sep  1 2026, 14:08:22) [Clang 22.1.3 ]",
  "executable": "/Users/dylanroy/Documents/Codex/2026-09-19/connect-research-repository/work/venv/bin/python3.11",
  "runs": [
    {
      "mode": "normal",
      "command": [
        "/Users/dylanroy/Documents/Codex/2026-09-19/connect-research-repository/work/venv/bin/python3.11",
        "-B",
        "-S",
        "work/continuation102/review/independent_controls.py"
      ],
      "exit_code": 0,
      "elapsed_seconds": 0.15053562493994832,
      "stdout_bytes": 1461,
      "stdout_sha256": "d9cc859ae2244785d1fd7bc201f30e3458199877cb785fcbb69a8df3db331173",
      "stderr_bytes": 0,
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "mode": "optimized",
      "command": [
        "/Users/dylanroy/Documents/Codex/2026-09-19/connect-research-repository/work/venv/bin/python3.11",
        "-B",
        "-S",
        "-O",
        "work/continuation102/review/independent_controls.py"
      ],
      "exit_code": 0,
      "elapsed_seconds": 0.15269574988633394,
      "stdout_bytes": 1461,
      "stdout_sha256": "d9cc859ae2244785d1fd7bc201f30e3458199877cb785fcbb69a8df3db331173",
      "stderr_bytes": 0,
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  ]
}
```
<!-- END C102 CONTROL_RUNS.json EXACT UTF8 -->

## Exact SOURCE_IDENTITIES.json

UTF-8 bytes: 3585; SHA256 `a2c5f89fdd516a92c1a7be11273b53f72e41abcf2168f7f52e0daba314ebf70d`.

<!-- BEGIN C102 SOURCE_IDENTITIES.json EXACT UTF8 -->
```json
[
  {
    "key": "C91",
    "local_path": "sources/C91.md",
    "copied_from": "work/continuation98/sources/C91_PROOF.md",
    "bytes": 12433,
    "sha256": "74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa",
    "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963566666",
    "comment_id": 5963566666,
    "extraction": "Exact UTF-8 body"
  },
  {
    "key": "C92",
    "local_path": "sources/C92.md",
    "copied_from": "work/continuation98/sources/C92_PROOF.md",
    "bytes": 19567,
    "sha256": "6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a",
    "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963825788",
    "comment_id": 5963825788,
    "extraction": "Exact UTF-8 body"
  },
  {
    "blob": "dfed3b8d318a3ab1950957f393307733a4bef3f2",
    "bytes": 40261,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "P",
    "local_path": "sources/P.md",
    "path": "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
    "sha256": "9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
    "copied_from": "work/continuation99/sources/P.md"
  },
  {
    "blob": "213594d6ca6a86fb938110f4d166d9ce275a02d0",
    "bytes": 1782,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "E1",
    "local_path": "sources/E1.md",
    "path": "imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
    "sha256": "bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
    "copied_from": "work/continuation99/sources/E1.md"
  },
  {
    "blob": "fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a",
    "bytes": 9062,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "E2",
    "local_path": "sources/E2.md",
    "path": "reviews/d1_section9_borel_repair_20260925/REPAIR.md",
    "sha256": "845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_section9_borel_repair_20260925/REPAIR.md",
    "copied_from": "work/continuation99/sources/E2.md"
  },
  {
    "blob": "75da2597971510f843f8d90c743950cb8c177342",
    "bytes": 23312,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "REC",
    "local_path": "sources/REC.md",
    "path": "reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
    "sha256": "451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
    "copied_from": "work/continuation99/sources/REC.md"
  },
  {
    "blob": "bb446d08db8a944537a743ad550b88c1c2ad5758",
    "bytes": 19889,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "CUB",
    "local_path": "sources/CUB.md",
    "path": "frontiers/planar_cubic_cluster_20260929/PROOF.md",
    "sha256": "117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/frontiers/planar_cubic_cluster_20260929/PROOF.md",
    "copied_from": "work/continuation99/sources/CUB.md"
  }
]
```
<!-- END C102 SOURCE_IDENTITIES.json EXACT UTF8 -->
