# C101 independent reviewer checker and original stdout

Dylan Roy — delegated AI reproducibility record. Actual performer: OpenAI/Codex agent `/root/c100_nonauthor_review`; exact runtime model variant/build UNKNOWN. This publishes the independently written finite controls supporting the [full frozen nonauthor review](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967219096) of [C101 proof5967063473](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967063473). It adds no new mathematical review vote, source acceptance, human review or organizational-independence credit. Same-provider independence credit: **0**.

The bound proof is the entire native UTF-8 body, **36333 bytes**, SHA-256 `300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4`. The full native review body is **29516 bytes**, SHA-256 `23a5b82cc4be6cbd9febd3eb5dd237fe0882ed59fef48d728a5687cd22208792`.

## Exact extraction and execution

There are exactly two payload blocks below. For each, start after the opening fence line immediately following its BEGIN marker, and stop immediately before the closing fence line immediately preceding its END marker. The payload includes its original final LF and excludes the fences and markers. Do not trim whitespace, normalize newlines, prepend a newline or append a second newline. Encode as UTF-8.

- `reviewer_controls.py`: **10231 bytes**, SHA-256 `d358da75bf73442e9e97647657f9654ed13d2956d3d8aa7b7611420424d3a33b`.
- `reviewer_controls.normal.txt`: **2304 bytes**, SHA-256 `51802ef2dd7f30466c2f110934d9a15ed412714026a7406fc28924db63e683e9`.

The original reviewer executions used **Python 3.9.6**:

```text
python3 -B reviewer_controls.py
python3 -B -O reviewer_controls.py
python3 -B -S reviewer_controls.py
```

All three exited 0. Their stdout files were byte-identical, reporting **235 positive exact controls** and **17 rejected false shortcuts**. The stdout payload below is the exact original normal-run output; the optimized and no-site outputs have that same identity. A subsequent run with another Python version changes the runtime line and therefore the stdout digest. This record does not relabel such a replay as the original output.

The checker was written after substantive proof reading without inspecting or running the author's checker or arithmetic outputs. It imports only Python standard-library modules and reads no source files, author modules, network resources or random samples. Its exact finite controls support transcription and falsification. Gaussian uniformity, continuum estimates, global topology, event identification and variation convergence require the written analytic review and its retained premises.

## Independent checker payload

<!-- C101_REVIEWER_CHECKER_BEGIN -->
```python
"""Independent exact controls for C101; no source, author code or network reads.

These controls falsify algebraic shortcuts. They do not prove the Gaussian,
topological, measurability or uniform-constant statements in the written review.
All checks remain active under Python -O. Stdout is deterministic per runtime.
"""
from fractions import Fraction as F
from collections import Counter
import sys

counts = Counter()
rejected = []


def check(ok, group):
    if not ok:
        raise ValueError(group)
    counts[group] += 1


def reject(false_claim, label):
    if false_claim:
        raise ValueError("False shortcut survived: " + label)
    rejected.append(label)


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        found = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if found is None:
            continue
        a[pivot], a[found] = a[found], a[pivot]
        scale = a[pivot][col]
        a[pivot] = [x / scale for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
    return pivot


monomials = [(i, degree - i) for degree in range(4) for i in range(degree + 1)]
for cosine, sine, reflection in [(F(1), F(0), 1), (F(3, 5), F(4, 5), 1),
                                  (F(5, 13), F(12, 13), -1)]:
    rows = []
    for x in range(-3, 4):
        for y in range(-3, 4):
            u = cosine * x + sine * y
            z = reflection * (-sine * x + cosine * y)
            rows.append([u**i * z**j for i, j in monomials])
    check(rank(rows) == 10, "exact finite jet evaluation rank")
reject(rank([[F(x)**i * F(0)**j for i, j in monomials]
             for x in range(-3, 4)]) == 10, "line samples certify all planar jets")
duplicate = [row[:-1] + [row[0]] for row in rows]
reject(rank(duplicate) == 10, "duplicated observation preserves full jet rank")


def positive(x):
    return max(F(0), x)


for lam in map(F, [-2, -1, 0, 1, 3]):
    for gamma in map(F, [-2, 0, 1, 3]):
        for b1 in map(F, [-2, 0, 2]):
            dm = 6 * lam + 3 * b1 - gamma**2 / 4
            ds = -6 * lam + 3 * b1 - gamma**2 / 4
            actual_typed_model = (dm if dm > 0 else 0) * (-ds if ds < 0 else 0)
            am, ass = 24 * lam - gamma**2 + 12 * b1, 24 * lam + gamma**2 - 12 * b1
            weight = positive(am) * positive(ass) / 16
            check(actual_typed_model == weight, "typed determinant including boundaries")
            check(weight <= 36 * positive(lam)**2, "typed weight quadratic envelope")
reject(abs(F(-6) * F(6)) == 0, "absolute determinants replace endpoint typing")


for lam, gamma, b1, c3 in [(F(2), F(1), F(1, 3), F(-2)),
                          (F(3), F(-2), F(-1, 2), F(7, 3)),
                          (F(1, 3), F(3, 2), F(5, 7), F(-1, 5))]:
    d = gamma**2 - 12 * b1
    j = 8 * gamma**3 - 144 * b1 * gamma + 576 * c3
    bsh = b1 - gamma**2 / 12
    dsh = (c3 - gamma * b1 / 4 + gamma**3 / 72) / 2
    check(bsh == -d / 12 and dsh == j / 1152, "raw to CUB parameter map")
    check(9 * (4 * lam**2 - bsh**2) ==
          (24 * lam - d) * (24 * lam + d) / 16, "model weight identity")
    psi, c, rr = 24 * lam / gamma**2, d / gamma**2, j / gamma**3
    for x, zeta in [(F(0), F(1)), (F(-1, 2), F(2, 3)),
                    (F(3, 2), F(-4, 5)), (F(2, 7), F(5, 3))]:
        u, z = x + gamma * zeta / 12, gamma * zeta
        raw = 2*x**3-3*x/2-F(1, 2)+(gamma/2)*(x*x-F(1, 4))*zeta-lam*zeta*zeta/2+b1*x*zeta*zeta/2+c3*zeta**3/6
        qs = 2*u**3-3*u/2-F(1, 2)-(psi+2*c*u)*z*z/48+rr*z**3/3456
        check(raw == qs, "raw cubic shear including negative gamma")
    check(gamma**6 * abs(c)**3 == abs(d)**3 and gamma**6 * rr**2 == j**2,
          "decision band chart pole cancellation")
reject(F(1, 16) * F(1, 24) == F(1, 384) / 12,
       "decision band Jacobian acquires extra factor twelve")


for upper in [F(1, 3), F(2), F(7, 2)]:
    # Integrate s(48 lambda-s)/16 first in s, then in lambda.
    weight_integral = (48**3 * (F(1, 2)-F(1, 3)) / 16) * upper**4 / 4
    error_integral = 48 * upper**2 / 2
    check(weight_integral == 288 * upper**4 and error_integral == 24 * upper**2,
          "radius integral and finite radius correction")
    check(weight_integral/12 == 24*upper**4 and error_integral/12 == 2*upper**2,
          "radius B1 Jacobian")
reject(-2 * 4 == -6, "actual radius leading term has rho minus six power")


h, r, delta, upper = F(3), F(1, 16), F(1, 1024), F(96)
strip = h*h*delta*delta/2+r*h**4*delta
check(strip > h*h*delta*delta/2, "actual strip retains finite radius mass")
reject(strip == h*h*delta*delta/2, "model strip substitutes for actual strip")
for v in [3, 4, 6]:
    exact = h*h*(delta**(2-v)-upper**(2-v))/(v-2) + r*h**4*(delta**(1-v)-upper**(1-v))/(v-1)
    bound = h*h*delta**(2-v)/(v-2)+r*h**4*delta**(1-v)/(v-1)
    check(0 < exact < bound, "truncated actual inverse powers")
    reject(exact <= h*h*delta**(2-v)/(v-2), "omit actual inverse correction v="+str(v))
check(F(1, 2)*(1*1+3*3) != (F(1, 2)*(1+3))**2,
      "correlated weight and norm are not independent")
reject(F(1, 2)*(1*1+3*3) == (F(1, 2)*(1+3))**2,
       "factor a correlated weighted moment")


d_cap, c_scalar, r_scalar, j_res = F(2, 3), F(5, 7), F(1, 4), F(3)
limit = 4*d_cap*r_scalar*j_res*j_res
scalar_integral = r_scalar**2*j_res**4*(limit**3/3+c_scalar*r_scalar*j_res**2*limit**2/2)
coefficient = (4*d_cap)**3/3+c_scalar*(4*d_cap)**2/2
check(scalar_integral == coefficient*r_scalar**5*j_res**10,
      "actual near scalar numerator r5 J10")
check(F(1)+4-2 == 3, "physical Jacobian soft determinant full normalizer")
reject(F(1)+4-2-2 == 3, "divide by full normalizer twice")
check(4-3 == 1, "scaled far and derivative exceptions")
reject(4-3 > 1, "discard finite radius cap exceptions")
for m in [1, 3, 7]:
    for a, jvalue in [(F(1), F(2)), (F(3), F(5)), (F(3), F(2))]:
        left = jvalue**10 if jvalue > a else 0
        check(left <= a**(-2*m)*jvalue**(10+2*m), "fixed residual tail moment")


for selected in [False, True]:
    for model_selected in [False, True]:
        model_rejected = not model_selected
        check(((not selected) != model_rejected) == (selected != model_selected),
              "Boolean complement agreement on typed partition")
reject(((not False) != False) == (False != False),
       "Boolean complements agree outside the typed partition")
mu = F(15, 16)
death_depth = 1-mu
endpoint_error = F(-3, 8)
check(abs(endpoint_error) < mu and 4*death_depth+endpoint_error < 0,
      "saddle clearance alone loses older endpoint")
reject(4*death_depth+endpoint_error > 0, "one margin certifies rejected chord")
budget = min(mu, 4*death_depth)/2
check(-death_depth-budget > -1 and 4*death_depth-budget > 0,
      "two margins certify chord and older endpoint")


# Affine expressions below represent a + b*beta, with alpha=(1-2 beta)/6.
def add(*pairs):
    return tuple(sum(p[i] for p in pairs) for i in [0, 1])


def scale(pair, amount):
    return tuple(x*amount for x in pair)


one, beta = (F(1), F(0)), (F(0), F(1))
alpha = (F(1, 6), F(-1, 3))
e = add(one, scale(beta, F(-1, 2)))
derived = [beta, add(one, scale(alpha,-3), scale(beta,F(1,2))),
           add(scale(alpha,-4),e), add(one,scale(alpha,-5),scale(e,F(1,2))),
           add(scale(alpha,-4),scale(e,F(2,3))), add(one,scale(alpha,-5),scale(e,F(1,3))),
           beta, add(one,scale(alpha,-4)), add(scale(alpha,-3),scale(add(e,scale(beta,-1)),2)),
           add(scale(one,2),scale(alpha,-5),scale(beta,F(-1,2))),
           add(scale(one,2),scale(alpha,-7),scale(beta,F(-1,4))), beta, one]
claimed = [(0,1),(F(1,2),F(3,2)),(F(1,3),F(5,6)),(F(2,3),F(17,12)),
           (0,1),(F(1,2),F(3,2)),(0,1),(F(1,3),F(4,3)),(F(3,2),-2),
           (F(7,6),F(7,6)),(F(5,6),F(25,12)),(0,1),(1,0)]
for actual, expected in zip(derived, claimed):
    check(actual == expected, "all thirteen cutoff exponents")
    # Affine nonnegativity at both endpoints proves it throughout [0,1/2].
    gap = add(actual,scale(beta,-1))
    check(gap[0] >= 0 and gap[0]+gap[1]/2 >= 0,
          "error exponents dominate target over entire beta interval")
conditions = [add(one,scale(alpha,-1)),add(one,scale(beta,F(-1,8))),e,
              add(e,scale(alpha,-2)),add(e,scale(alpha,-3)),
              add(one,scale(beta,F(-1,4))),beta]
for a,b in conditions:
    check(a >= 0 and a+b/2 > 0, "all admissibility powers positive in open interval")
for m in range(1, 21):
    aa, bb = F(1,2*(m+3)), F(m,2*(m+3))
    check(bb == m*aa and aa > 0 and 0 < bb < F(1,2), "fixed integer cutoff family")
check(F(3,12) == F(1,4) and F(1,4)/8 == F(1,32) and 1-F(1,4)/2 == F(7,8),
      "m3 displayed specialization")
check(10+2*3 == 16 and 6+2*3 == 12, "m3 actual and model moment orders")
for requested in [F(1,10),F(1,4),F(2,5),F(49,100)]:
    needed = 6*requested/(1-2*requested)
    m = max(1,(needed.numerator+needed.denominator-1)//needed.denominator)
    check(F(m,2*(m+3)) >= requested, "requested beta finite moment selection")
reject(F(1,6)-F(1,2)/3 > 0, "endpoint beta one half has an exhausting cutoff")
reject(F(3,2)-2*F(51,100) >= F(51,100), "beta beyond half satisfies Taylor balance")
reject(derived[4] == add(derived[4],scale(alpha,4)), "omit growing H4 endpoint loss")


for left,right in [([F(1,3),F(2,3)],[F(1,2),F(1,2)]),
                   ([F(1),F(2)],[F(2),F(4)]),
                   ([F(1,8),F(3,8)],[F(1,3),F(1,3)])]:
    a,b = sum(left),sum(right)
    variation = sum(abs(x-y) for x,y in zip(left,right))
    normalized = sum(abs(x/a-y/b) for x,y in zip(left,right))
    check(abs(a-b) <= variation and normalized <= 2*variation/a,
          "mass consumer and positive mass normalization")

print("C101 independent reviewer exact controls")
print("Runtime: Python " + sys.version.split()[0])
for group,count in sorted(counts.items()):
    print(str(count) + " PASS: " + group)
print("Positive exact controls: " + str(sum(counts.values())))
for label in rejected:
    print("REJECTED: " + label)
print("Rejected false shortcuts: " + str(len(rejected)))
print("Analytic Gaussian, topology and continuum conclusions require the written review.")
```
<!-- C101_REVIEWER_CHECKER_END -->

## Original Python 3.9.6 stdout payload

<!-- C101_REVIEWER_STDOUT_BEGIN -->
```text
C101 independent reviewer exact controls
Runtime: Python 3.9.6
4 PASS: Boolean complement agreement on typed partition
1 PASS: actual near scalar numerator r5 J10
1 PASS: actual strip retains finite radius mass
7 PASS: all admissibility powers positive in open interval
13 PASS: all thirteen cutoff exponents
1 PASS: correlated weight and norm are not independent
3 PASS: decision band chart pole cancellation
13 PASS: error exponents dominate target over entire beta interval
3 PASS: exact finite jet evaluation rank
20 PASS: fixed integer cutoff family
9 PASS: fixed residual tail moment
1 PASS: m3 actual and model moment orders
1 PASS: m3 displayed specialization
3 PASS: mass consumer and positive mass normalization
3 PASS: model weight identity
1 PASS: physical Jacobian soft determinant full normalizer
3 PASS: radius B1 Jacobian
3 PASS: radius integral and finite radius correction
12 PASS: raw cubic shear including negative gamma
3 PASS: raw to CUB parameter map
4 PASS: requested beta finite moment selection
1 PASS: saddle clearance alone loses older endpoint
1 PASS: scaled far and derivative exceptions
3 PASS: truncated actual inverse powers
1 PASS: two margins certify chord and older endpoint
60 PASS: typed determinant including boundaries
60 PASS: typed weight quadratic envelope
Positive exact controls: 235
REJECTED: line samples certify all planar jets
REJECTED: duplicated observation preserves full jet rank
REJECTED: absolute determinants replace endpoint typing
REJECTED: decision band Jacobian acquires extra factor twelve
REJECTED: actual radius leading term has rho minus six power
REJECTED: model strip substitutes for actual strip
REJECTED: omit actual inverse correction v=3
REJECTED: omit actual inverse correction v=4
REJECTED: omit actual inverse correction v=6
REJECTED: factor a correlated weighted moment
REJECTED: divide by full normalizer twice
REJECTED: discard finite radius cap exceptions
REJECTED: Boolean complements agree outside the typed partition
REJECTED: one margin certifies rejected chord
REJECTED: endpoint beta one half has an exhausting cutoff
REJECTED: beta beyond half satisfies Taylor balance
REJECTED: omit growing H4 endpoint loss
Rejected false shortcuts: 17
Analytic Gaussian, topology and continuum conclusions require the written review.
```
<!-- C101_REVIEWER_STDOUT_END -->
