# C99 independent checker and exact stdout

Supporting evidence for the entire source-bound nonauthor review by OpenAI/Codex `/root/c95_fresh_review`, Dylan Roy — delegated AI review. This is not an additional mathematical review. No author or prior checker source is imported or used. Personal reading PENDING; human review NONE; organizational independence0; scientific effectNONE.

Actual Python3.12.14: normal, -O and -S each exited0 with byte-identical stdout;330 positive exact controls and21 rejected false-inference fixtures. The stdout includes the actual Python version: another runtime version changes that metadata line and is not promised byte-identical output. All arithmetic checks remain active under optimization. Finite controls do not prove Gaussian rank, topology, nullity or convergence.

First fence, final LF included: checker.py,10542 UTF-8 bytes, SHA256 `d8b03204968ff93b422c4df5ca03f93294373bdaca5f71ab644bc050cd898a0e`.
Second fence, final LF included: stdout.txt,2065 UTF-8 bytes, SHA256 `b947fc9c8b89d0c52eda3d581a05da4c2589ae260ea7ffa1957c959a83c6ef6f`.

Full review: https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5966413018

## Independent source

```python
"""Independent C99 rational controls; no author/prior checker or file imports.
Finite controls do not prove Gaussian rank, topology, nullity, or convergence.
All checks use explicit exceptions and remain active with Python optimization.
"""
from fractions import Fraction as Q
from collections import Counter
import sys

counts = Counter()
negatives = []


def check(group, condition):
    if not condition:
        raise RuntimeError("FAILED: " + group)
    counts[group] += 1


def reject(name, false_statement):
    if false_statement:
        raise RuntimeError("NEGATIVE FIXTURE DID NOT REJECT: " + name)
    negatives.append(name)


def cubic(k, th, x, z):
    s, a, beta, q = th
    return (2*k*x**3 - 3*k*x/2 - k/2 + s*z*z/2
            + a*(x*x-Q(1,4))*z/2 + beta*x*z*z/2 + q*z**3/6)


def grad(k, th, x, z):
    s, a, beta, q = th
    return (6*k*x*x-3*k/2+a*x*z+beta*z*z/2,
            s*z+a*(x*x-Q(1,4))/2+beta*x*z+q*z*z/2)


def hess(k, th, x, z):
    s, a, beta, q = th
    return (12*k*x+a*z, a*x+beta*z, s+beta*x+q*z)


def det2(h):
    x, y, z = h
    return x*z-y*y


eta = (Q(-3,2), Q(2), Q(1,3), Q(55,18))
ystar = (Q(-2,3), Q(1))
yother = (Q(1,3), Q(1))
pin_m, pin_s = (Q(-1,2), Q(0)), (Q(1,2), Q(0))
for k in (Q(1,5), Q(1,2), Q(1), Q(7,4), Q(3)):
    th = tuple(k*v for v in eta)
    for point in (pin_m, pin_s, ystar, yother, (Q(2,7), Q(-3,5))):
        check("cubic_scaling", cubic(k, th, *point) == k*cubic(Q(1), eta, *point))
        check("gradient_scaling", grad(k, th, *point) == tuple(k*v for v in grad(Q(1), eta, *point)))
        check("hessian_scaling", hess(k, th, *point) == tuple(k*v for v in hess(Q(1), eta, *point)))
    for point, value, determinant in ((pin_m,Q(0),Q(9)),
                                     (pin_s,Q(-1),Q(-9)),
                                     (ystar,Q(-1,4),Q(-9)),
                                     (yother,Q(-5,4),Q(9))):
        check("exact_roots", grad(k, th, *point) == (0,0))
        check("exact_root_heights", cubic(k, th, *point) == k*value)
        check("exact_root_determinants", det2(hess(k, th, *point)) == k*k*determinant)
    s,a,beta,q = th
    bs = beta-a*a/(12*k)
    ds = (q-a*beta/(4*k)+a**3/(72*k*k))/2
    check("scaled_shear", bs == 0 and ds == Q(3,2)*k)
    weight = 9*k*k*(4*s*s-bs*bs)
    check("weight_and_eta_jacobian", weight*k**4 == 81*k**8)
    check("generic_failure", s < -abs(bs)/2 and ds != 0
          and 12*k*ds*ds+bs**3 != 0
          and 12*k*ds*ds+(s-bs)**2*(bs+2*s) != 0
          and 12*k*ds*ds+bs**3-4*bs*s*s != 0)

# Derive the height-chain-rule cancellation on a moving critical root.
# g(k,x) = -(x-k)^2 - k/4, Y(k)=k; partial_k g(Y)=-1/4.
for k in (Q(1,4), Q(1), Q(7,3)):
    y = k
    partial_x = -2*(y-k)
    partial_k = 2*(y-k)-Q(1,4)
    check("critical_value_chain_rule", partial_x == 0 and partial_k == -Q(1,4))

# Generic linear regression map with a nonzero residual/intercept.
# This checks exact algebraic affinity, not a claim about Gaussian samples.
base = (Q(7), Q(-2), Q(3))
direction = (Q(1,2), Q(12), Q(-4))
observed = (Q(2), Q(5), Q(-1))
residual = (Q(11), Q(-8))
matrix = ((Q(2), Q(1,3), Q(-1)), (Q(-3,2), Q(5), Q(2)))
def coupled(k):
    target = tuple(b+k*d-v for b,d,v in zip(base,direction,observed))
    return tuple(r+sum(c*v for c,v in zip(row,target)) for r,row in zip(residual,matrix))
ka,kb = Q(1,3),Q(5,2)
slope = tuple((v-u)/(kb-ka) for u,v in zip(coupled(ka),coupled(kb)))
for k in (Q(1,2), Q(1), Q(2)):
    check("regression_affinity", coupled(k) == tuple(u+(k-ka)*d for u,d in zip(coupled(ka),slope)))
reject("raw_field_scaling_is_not_target_regression", coupled(Q(2)) == tuple(2*v for v in coupled(Q(1))))

# Exact L1 norm for piecewise constant signed densities on rational intervals.
def l1(pieces):
    endpoints = sorted({x for a,b,v in pieces for x in (a,b)})
    return sum((b-a)*abs(sum(v for lo,hi,v in pieces if lo < (a+b)/2 < hi))
               for a,b in zip(endpoints,endpoints[1:]))

def mass(pieces):
    return sum((b-a)*v for a,b,v in pieces)

def difference(p,q):
    return p+[(a,b,-v) for a,b,v in q]

def push_affine(p,c,d):
    if c <= 0:
        raise ValueError("positive derivative required")
    return [(c*a+d,c*b+d,v/c) for a,b,v in p]

weight_pieces = [(Q(1),Q(2),Q(1)),(Q(2),Q(3),Q(1,2))]
base_push = push_affine(weight_pieces,Q(2),Q(0))
for n in (2,4,8,16,32,64):
    delta = Q(1,n)
    moved = push_affine(weight_pieces,Q(2),2*delta)
    check("discontinuous_weight_coarea", l1(difference(moved,base_push)) == 2*delta)
    check("coarea_mass", mass(moved) == Q(3,2))
    changed = [(a,b,v+delta) for a,b,v in weight_pieces]
    moved_changed = push_affine(changed,Q(2),2*delta)
    check("weighted_pushforward_split", l1(difference(moved_changed,base_push))
          <= l1(difference(changed,weight_pieces))+l1(difference(moved,base_push)))
    c = 2*(1+delta)
    scaled = push_affine(weight_pieces,c,Q(0))
    check("derivative_denominator", mass(scaled) == mass(weight_pieces))
    check("moving_endpoints_control", l1(difference(scaled,base_push)) <= 8*delta)
reject("differentiate_count_and_ignore_jump_mass", l1(difference(push_affine(weight_pieces,2,Q(1,4)),base_push)) == 0)
reject("omit_scalar_jacobian", mass([(2*a,2*b,v) for a,b,v in weight_pieces]) == mass(weight_pieces))
reject("drop_reciprocal_count", mass(weight_pieces) == Q(2))
reject("replace_reciprocal_by_one_half", mass(weight_pieces) == Q(1))

# Smooth C1 maps can converge uniformly without derivative convergence.
# On n equal cells let T'-1 linearly trace 0,1/2,0,-1/2,0.
# The exact derivative floor is 1/2, integral increment per cell is 1/n.
# Sup|T-id|=1/(8n), but ||T#Leb-Leb||_1=int|1-T'|=1/4.
for n in (1,2,4,8,16):
    width = Q(1,4*n)
    deviations = (Q(0),Q(1,2),Q(0),Q(-1,2),Q(0))
    increments = [width*(a+b)/2 for a,b in zip(deviations,deviations[1:])]
    check("uniform_not_C1", sum(increments) == 0)
    check("uniform_not_C1", max(sum(increments[:j]) for j in range(5)) == Q(1,8*n))
    exact_tv = n*sum(abs(v) for v in increments)
    check("uniform_not_C1", exact_tv == Q(1,4))
reject("uniform_maps_alone_force_L1", exact_tv == 0)

# Weak oscillating densities: masses agree in each cell but L1 stays one.
for n in (1,2,4,8,16):
    oscillatory = [(Q(j,n),Q(2*j+1,2*n),Q(2)) for j in range(n)]
    uniform = [(Q(0),Q(1),Q(1))]
    check("weak_not_L1", mass(oscillatory) == 1 and l1(difference(oscillatory,uniform)) == 1)
reject("weak_limit_plus_mass_force_L1_without_local_L1", l1(difference(oscillatory,uniform)) == 0)

# Radial coarea at perfect-cube z avoids irrational arithmetic.
for v in (Q(1,3),Q(1,2),Q(2,3)):
    z = v**3
    for t in (Q(1,2),Q(1),Q(3,2),Q(2)):
        tau_root = t*v
        density = tau_root**2/(3*v**5)
        check("radial_density", density*(3*t*t*z) == t**4)
        check("radial_support", t**3*z == tau_root**3)
    # Reciprocal changes at t=1, so it must stay inside the integral.
    direct = (1-Q(1,2)**5)/5 + (Q(2)**5-1)/10
    pushed = ((v)**5-(v/2)**5)/(5*v**5) + ((2*v)**5-v**5)/(10*v**5)
    check("radial_reciprocal_mass", direct == pushed)
reject("radial_density_missing_factor_three", (t*t/z)*(3*t*t*z) == t**4)

for r in (Q(1,2),Q(1,4),Q(1,8)):
    z0, pi0, t, h = Q(7,3), Q(5,2), Q(3,2), r/Q(3,2)
    full_z = r*r*z0
    ar = 12*pi0*full_z/(r*r)
    check("full_normalizer", ar*r*r/full_z == 12*pi0)
    check("rare_scale", r**(-3)*r*r**4/full_z == 1/z0)
    check("h_power", r*h*r**3/h**5 == t**4)
reject("second_full_normalizer", ar*r*r/(full_z*full_z) == 12*pi0)
reject("full_normalizer_has_soft_scale_r4", full_z == r**4*z0)
reject("omit_eta_jacobian_k4", Q(2)**4 == Q(2)**8)
reject("unordered_pair_half_factor", 12*pi0/2 == 12*pi0)
reject("actual_pair_needs_rejected_reciprocal", Q(1,2) == Q(1))
reject("finite_h_death_jacobian_is_h_minus3", h**3 == h**(-3))

# Positive scalar inverse null-boundary control; roots stay fixed on rays.
z,t = Q(1,4),Q(3,2)
for kend in (Q(1,3),Q(2),Q(5)):
    tau = t**3*z*kend
    check("inverse_boundary_transfer", tau/(t**3*z) == kend and t**3*z > 0)
pin_gap = -cubic(Q(2),tuple(2*v for v in eta),*pin_s)
reject("fixed_k_pin_boundary_is_null_by_scaling", pin_gap != Q(2))
reject("zero_gap_has_positive_scalar_jacobian", Q(0) > 0)
reject("negative_affine_rescaling_preserves_older_endpoints", -Q(3) > -Q(1))

# Finite kernel mixtures verify norm contraction; cancellation is allowed.
p = [(Q(0),Q(1),Q(2)),(Q(1),Q(2),Q(1))]
q = [(Q(0),Q(2),Q(1))]
d = difference(p,q)
opposite = [(a,b,-v) for a,b,v in d]
check("kernel_variation", l1(d+opposite) <= l1(d)+l1(opposite))
reject("variation_of_integral_equals_integral_variation", l1(d+opposite) == l1(d)+l1(opposite))

# Exact positive-measure version of D18a on a three-atom partition.
for aa in range(4):
    for bb in range(4):
        for cc in range(4):
            f = (Q(aa,3),Q(bb,3),Q(cc,3))
            g = (Q(1,2),Q(2,3),Q(1,4))
            lhs = sum(abs(x-y) for x,y in zip(f,g))
            rhs = 2*abs(f[1]-g[1])+abs(sum(f)-sum(g))+2*(g[0]+g[2])
            check("global_mass_completion", lhs <= rhs)
escaping = [(Q(10),Q(11),Q(1))]
local_escape_mass = sum(max(Q(0),min(b,Q(2))-max(a,Q(1)))*v
                        for a,b,v in escaping)
check("escaping_tail_fixture", local_escape_mass == 0 and mass(escaping) == 1)
reject("local_L1_without_mass_excludes_escape", mass(escaping) == local_escape_mass)
# Signed cancellation defeats the nonnegative tail bound even with equal mass.
signed_f, signed_g = (Q(1),Q(-1),Q(0)),(Q(0),Q(0),Q(0))
reject("D18a_without_nonnegativity", sum(abs(v) for v in signed_f) <= 0)

# Field-first weighted counts, arbitrary signed test values in [-1,1].
for n in range(0,9):
    values = [Q((-1)**j*(j+1),n+1) for j in range(n)]
    total = sum(values)
    sampled = total/n if n else Q(0)
    check("field_first", abs(total-sampled) <= max(n-1,0))
    check("field_first_mass", n-(1 if n else 0) == max(n-1,0))
L, coefficient = Q(3),Q(5,7)
check("field_first_normalization", (L*L)/(L*L*coefficient) == 1/coefficient)
reject("omit_area_factor_in_occurrence", L*L*coefficient == coefficient)

print("C99 independent exact rational controls")
print("Python " + sys.version.split()[0])
for name in sorted(counts):
    print(name + ": " + str(counts[name]) + " passed")
print("Positive controls: " + str(sum(counts.values())))
print("Rejected false-inference fixtures: " + str(len(negatives)))
for name in negatives:
    print("REJECTED: " + name)
print("No Gaussian/topological/null-set/convergence theorem is certified by these finite controls.")
print("PASS_EXACT_SUPPORTING_CONTROLS")
```

## Exact actual stdout

```text
C99 independent exact rational controls
Python 3.12.14
coarea_mass: 6 passed
critical_value_chain_rule: 3 passed
cubic_scaling: 25 passed
derivative_denominator: 6 passed
discontinuous_weight_coarea: 6 passed
escaping_tail_fixture: 1 passed
exact_root_determinants: 20 passed
exact_root_heights: 20 passed
exact_roots: 20 passed
field_first: 9 passed
field_first_mass: 9 passed
field_first_normalization: 1 passed
full_normalizer: 3 passed
generic_failure: 5 passed
global_mass_completion: 64 passed
gradient_scaling: 25 passed
h_power: 3 passed
hessian_scaling: 25 passed
inverse_boundary_transfer: 3 passed
kernel_variation: 1 passed
moving_endpoints_control: 6 passed
radial_density: 12 passed
radial_reciprocal_mass: 3 passed
radial_support: 12 passed
rare_scale: 3 passed
regression_affinity: 3 passed
scaled_shear: 5 passed
uniform_not_C1: 15 passed
weak_not_L1: 5 passed
weight_and_eta_jacobian: 5 passed
weighted_pushforward_split: 6 passed
Positive controls: 330
Rejected false-inference fixtures: 21
REJECTED: raw_field_scaling_is_not_target_regression
REJECTED: differentiate_count_and_ignore_jump_mass
REJECTED: omit_scalar_jacobian
REJECTED: drop_reciprocal_count
REJECTED: replace_reciprocal_by_one_half
REJECTED: uniform_maps_alone_force_L1
REJECTED: weak_limit_plus_mass_force_L1_without_local_L1
REJECTED: radial_density_missing_factor_three
REJECTED: second_full_normalizer
REJECTED: full_normalizer_has_soft_scale_r4
REJECTED: omit_eta_jacobian_k4
REJECTED: unordered_pair_half_factor
REJECTED: actual_pair_needs_rejected_reciprocal
REJECTED: finite_h_death_jacobian_is_h_minus3
REJECTED: fixed_k_pin_boundary_is_null_by_scaling
REJECTED: zero_gap_has_positive_scalar_jacobian
REJECTED: negative_affine_rescaling_preserves_older_endpoints
REJECTED: variation_of_integral_equals_integral_variation
REJECTED: local_L1_without_mass_excludes_escape
REJECTED: D18a_without_nonnegativity
REJECTED: omit_area_factor_in_occurrence
No Gaussian/topological/null-set/convergence theorem is certified by these finite controls.
PASS_EXACT_SUPPORTING_CONTROLS
```
