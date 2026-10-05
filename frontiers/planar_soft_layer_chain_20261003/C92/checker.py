#!/usr/bin/env python3
"""Independent C92 transcription/obstruction controls; not a Gaussian proof.

Standard library, exact Fractions, no author checker or source execution.
Every check is an explicit exception, so python -O retains all checks.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json

COUNTS = {}
NEGATIVE = []


def check(group, condition):
    if not condition:
        raise RuntimeError(group)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("negative control survived: " + name)
    NEGATIVE.append(name)


def add(*polys):
    out = {}
    for p in polys:
        for ij, a in p.items():
            out[ij] = out.get(ij, F(0)) + a
    return {ij: a for ij, a in out.items() if a}


def scale(p, a):
    return {ij: a * b for ij, b in p.items() if a * b}


def mul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            out[i+k, j+l] = out.get((i+k, j+l), F(0)) + a*b
    return out


def deriv(p, i, j):
    return {(k-i, l-j): a*F(factorial(k), factorial(k-i))
            * F(factorial(l), factorial(l-j))
            for (k, l), a in p.items() if k >= i and l >= j}


def ev(p, x, z):
    return sum((a*x**i*z**j for (i, j), a in p.items()), F(0))


def raw(p, r):
    return {(i, j): a*r**(i+j-3) for (i, j), a in p.items()}


def model(lam, gam, b1, c3):
    return {(3, 0): F(2), (1, 0): F(-3, 2), (0, 0): F(-1, 2),
            (2, 1): gam/2, (0, 1): -gam/8, (0, 2): -lam/2,
            (1, 2): b1/2, (0, 3): c3/6}


def filtered(a, b, c, j):
    det = a*c-b*b
    if not det:
        return F(0)
    index = 1 if det < 0 else (2 if a+c < 0 else 0)
    return abs(det) if index == j else F(0)


def determinant(a):
    a = [row[:] for row in a]
    answer = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        v = a[i][i]
        answer *= v
        for j in range(i+1, len(a)):
            q = a[j][i]/v
            for k in range(i+1, len(a)):
                a[j][k] -= q*a[i][k]
    return answer


def positive_ldl(a):
    a = [row[:] for row in a]
    for i in range(len(a)):
        if a[i][i] <= 0:
            return False
        for j in range(i+1, len(a)):
            for k in range(j, len(a)):
                a[j][k] -= a[j][i]*a[k][i]/a[i][i]
                a[k][j] = a[j][k]
    return True


# Finite rank fixtures use rational positive weights and omega=1, NOT the
# periodized covariance. They test jet bookkeeping, not all-frame ellipticity.
jets = [(0,0), (1,0), (2,0), (3,0), (0,1), (1,1),
        (0,2), (2,1), (1,2), (0,3)]
check("jet_list", len(set(jets)) == 10)
check("jet_list", set(jets) == {(i,j) for i in range(4)
                              for j in range(4-i)})
for ux, uz, ex, ez in [(F(1),F(0),F(0),F(1)),
                      (F(3,5),F(4,5),F(-4,5),F(3,5)),
                      (F(3,5),F(4,5),F(4,5),F(-3,5))]:
    gram = [[F(0) for _ in jets] for _ in jets]
    for nx, nz in product(range(-2,3), repeat=2):
        ax, az = ux*nx+uz*nz, ex*nx+ez*nz
        amps = [ax**i*az**j for i,j in jets]
        weight = F(1, (1+nx*nx+nz*nz)**6)
        for a, (i,j) in enumerate(jets):
            for b, (k,l) in enumerate(jets):
                diff = i+j-k-l
                phase = (F(0) if diff % 2 else
                         (F(1) if (diff//2) % 2 == 0 else F(-1)))
                gram[a][b] += weight*amps[a]*amps[b]*phase
    check("finite_rank_fixtures", all(isinstance(v,F)
                                    for row in gram for v in row))
    check("finite_rank_fixtures", positive_ldl(gram))
    duplicate = [row[:] for row in gram]
    duplicate[-1] = duplicate[0][:]
    for row in duplicate:
        row[-1] = row[0]
    check("duplicate_rank_negative", determinant(duplicate) == 0)

# Exact six-row transform, target, and centered cancellation.
for r in [F(1,2), F(1,4), F(1,8), F(1,16)]:
    a, c = -r/2, r/2
    tmat = [[F(1,2),0,F(1,2),0,0,0],
            [-1/r,0,1/r,0,0,0], [0,-1/r,0,1/r,0,0],
            [12/r**3,6/r**2,-12/r**3,6/r**2,0,0],
            [0,0,0,0,F(1,2),F(1,2)], [0,0,0,0,-1/r,1/r]]
    check("pin_transform", abs(determinant(tmat)) == 12/r**5)
    original = [F(2),0,F(2)-r**3,0,0,0]
    target = [F(2)-r**3/2,-r**2,0,F(12),0,0]
    check("pin_transform", [sum(x*y for x,y in zip(row,original))
                            for row in tmat] == target)
    for degree in range(10):
        p = {(degree,0): F(1)}
        obs = [ev(p,a,0),ev(deriv(p,1,0),a,0),
               ev(p,c,0),ev(deriv(p,1,0),c,0),0,0]
        row3 = sum(x*y for x,y in zip(tmat[3], obs))
        expected = ev(deriv(p,3,0),0,0)
        if degree == 5:
            expected += r*r*F(factorial(5),40)
        if degree <= 6:
            check("centered_cubic_row", row3 == expected)
    check("centered_cubic_row", r*r*F(factorial(5),40) == 3*r*r)

# Signed model weight and off-diagonal filtered cancellation, including zero.
grid = [F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2)]
for lam, gam, b1 in product(grid, repeat=3):
    dm = 6*lam+3*b1-gam*gam/4
    ds = 6*lam-3*b1+gam*gam/4
    fm = filtered(F(-6),-gam/2,-lam-b1/2,2)
    fs = filtered(F(6),gam/2,-lam+b1/2,1)
    check("signed_typed_weight", fm == max(dm,0))
    check("signed_typed_weight", fs == max(ds,0))
    if lam <= 0:
        check("nonpositive_limit", fm*fs == 0)
for a,b,c in product(grid, repeat=3):
    for j in range(3):
        check("filtered_offdiagonal", abs(filtered(a,b,c,j)
              - filtered(a,0,c,j)) <= b*b)
for ax,cz,ay,dz in product(grid, repeat=4):
    norm = max(abs(ax),abs(cz),abs(ay),abs(dz))
    diff = max(abs(ax-ay),abs(cz-dz))
    for j in range(3):
        check("diagonal_filtered_lipschitz",
              abs(filtered(ax,0,cz,j)-filtered(ay,0,dz,j))
              <= 2*norm*diff)

# Independent pin-preserving quartics test exact raw Hessian scaling and all
# mixed derivatives. Nbound is a deterministic bound on the unit local box,
# not a Gaussian sample or a global torus construction.
for r in [F(1,2),F(1,4),F(1,8)]:
    q = {(2,0):F(1),(0,0):-r*r/4}
    quartics = [mul(q,q), mul(q,{(1,1):F(1)}),
                mul(q,{(0,2):F(1)}), {(1,3):F(1)}, {(0,4):F(1)}]
    for lam,gam,b1,c3 in [(F(-1,2),F(0),F(1),F(-1)),
                            (F(0),F(2),F(-1),F(1)),
                            (F(1),F(1),F(0),F(2))]:
        base = {(i,j):v*r**(3-i-j) for (i,j),v
                in model(lam,gam,b1,c3).items()}
        f = add(base, *[scale(p,F(i+1,7)) for i,p in enumerate(quartics)])
        check("quartic_pins", ev(f,-r/2,0) == 0)
        check("quartic_pins", ev(f,r/2,0) == -r**3)
        for x in [-r/2,r/2]:
            for i,j in [(1,0),(0,1)]:
                check("quartic_pins", ev(deriv(f,i,j),x,0) == 0)
        midpoint = [ev(deriv(f,i,j),0,0)
                    for i,j in [(0,2),(2,1),(1,2),(0,3)]]
        actual_model = model(-midpoint[0]/r,*midpoint[1:])
        error = add(raw(f,r),scale(actual_model,F(-1)))
        nbound = F(1) + max(sum(abs(v) for v in deriv(f,i,j).values())
                           for i in range(5) for j in range(5-i))
        for x in [-F(1,2),F(1,2)]:
            for i,j in [(2,0),(1,1),(0,2)]:
                check("raw_hessian_scale", ev(deriv(raw(f,r),i,j),x,0)
                      == ev(deriv(f,i,j),r*x,0)/r)
        constants = [F(167,192),F(635,384),F(115,48)]
        for w in [F(1),F(2),F(4)]:
            if r*w > 1:
                continue
            for x,z in product([-w,F(0),w], repeat=2):
                for order in range(3):
                    for i in range(order+1):
                        j = order-i
                        check("quartic_derivative_bounds",
                              abs(ev(deriv(error,i,j),x,z))
                              <= constants[order]*nbound*r*w**(4-order))

# Exact radius bookkeeping and a correlated weighted Markov fixture.
for r in [F(1,2),F(1,8),F(1,32)]:
    m,z = F(7,3),F(5,2)
    numerator,normalizer = r**4*r*m, r**2*z
    check("radius_ledger", numerator/normalizer == r**3*m/z)
    check("radius_ledger", r**(-3)*numerator/normalizer == m/z)
atoms = [(F(1,2),F(1),F(1)), (F(1,3),F(3),F(4)),
         (F(1,6),F(9),F(25))]  # (mass,N,D), correlated on purpose
for p in [1,2,3,5]:
    for threshold in [F(1),F(2),F(4),F(10)]:
        left = sum(m*d for m,n,d in atoms if n > threshold)
        right = sum(m*d*n**p for m,n,d in atoms)/threshold**p
        check("weighted_markov", left <= right)
for beta,eta in [(F(0),F(0)),(F(1,8),F(1,4)),
                 (F(1,10),F(1,10)),(F(6,25),F(1,100))]:
    exps = [1-(4-j)*beta-eta for j in range(3)]
    check("window_exponents", min(exps) == 1-4*beta-eta)
    check("window_exponents", min(exps) > 0 and beta < 1)

reject("omit-positive-parts", (-6+3)*(-6-3)
       == filtered(F(-6),F(0),F(1,2),2)
          *filtered(F(6),F(0),F(3,2),1))
reject("inertia-indicator-is-Lipschitz",
       F(1) <= 2*F(1,100)*(2*F(1,100)))
reject("wrong-cubic-row-factor", F(3) == F(6))
reject("wrong-soft-radius-power", F(1,8)**5 == F(1,8)**3)
reject("drop-joint-A-marginal", F(2,3)*F(5,7) == F(5,7))
reject("normalize-by-soft-layer", F(1,8)**3 == 1)
reject("critical-window-also-o-r3", 1-4*F(1,4) > 0)
reject("weighted-Markov-by-independence",
       sum(m*d*n**2 for m,n,d in atoms)
       == sum(m*d for m,n,d in atoms)*sum(m*n**2 for m,n,d in atoms))

print(json.dumps({"object":"C92-independent-controls-v1",
                  "positive_counts":COUNTS,
                  "positive_total":sum(COUNTS.values()),
                  "rejected_mutants":NEGATIVE,
                  "mutant_total":len(NEGATIVE),
                  "scope":"exact finite controls; Gaussian assertions analytic"},
                 sort_keys=True, separators=(",", ":")))
