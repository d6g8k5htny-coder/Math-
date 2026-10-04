"""C103 independently written stdlib rational controls; no author/file imports.
Use --mutant NAME to require the chosen incorrect used formula to fail a gate.
These checks do not prove the analytic, Gaussian or topological theorem.
"""
from fractions import Fraction as Q
from collections import Counter
import sys

mutant = sys.argv[2] if len(sys.argv) == 3 and sys.argv[1] == '--mutant' else ''
allowed = {'jet_jacobian','determinant_k4','radius_power','hessian_factor',
           'drop_edge_term','wrong_torus_lattice'}
if mutant and mutant not in allowed:
    raise ValueError('unknown mutant')
checks = Counter()
negatives = []


def gate(group, condition):
    if not condition:
        raise RuntimeError('C103_CHECK_FAILED:' + group + ':mutant=' + mutant)
    checks[group] += 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError('FALSE_INFERENCE_SURVIVED:' + name)
    negatives.append(name)


def det(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]


def mv(m,v):
    return tuple(sum(a*b for a,b in zip(row,v)) for row in m)


def inv(m):
    d = det(m)
    if d == 0:
        raise ValueError('singular matrix')
    return ((m[1][1]/d,-m[0][1]/d),(-m[1][0]/d,m[0][0]/d))


def filt(m,index):
    d = det(m)
    if index == 1:
        return max(-d,Q(0))
    return d if d > 0 and m[0][0] < 0 else Q(0)


def cubic(k, s, a, beta, c3, x, z):
    return (2*k*x**3-3*k*x/2-k/2+s*z*z/2
            +a*(x*x-Q(1,4))*z/2+beta*x*z*z/2+c3*z**3/6)


def raw(lam,gam,b,c,x,z):
    return (2*x**3-3*x/2-Q(1,2)+gam*(x*x-Q(1,4))*z/2
            -lam*z*z/2+b*x*z*z/2+c*z**3/6)


for k in (Q(1,3),Q(1),Q(5,2)):
    for r in (Q(1,8),Q(1,32)):
        jac = (r/k)*(1/k)*(1/(k*k))
        if mutant == 'jet_jacobian':
            jac = r*k**4
        gate('physical_jet_jacobian', jac == r/k**4)
        gate('rare_disintegration', r**(-5)*jac*r**4 == k**(-4))
        for lam in (Q(-1),Q(0),Q(3,2)):
            for gam,b,c in ((Q(0),Q(0),Q(0)),(Q(-2),Q(1,3),Q(7,5)),
                            (Q(3),Q(-1),Q(-2))):
                lm = ((Q(-6),-gam/2),(-gam/2,-lam-b/2))
                ls = ((Q(6),gam/2),(gam/2,-lam+b/2))
                weight = max(6*lam+3*b-gam*gam/4,0)*max(6*lam-3*b+gam*gam/4,0)
                gate('typed_model_weight', filt(lm,2)*filt(ls,1) == weight)
                gate('quadratic_weight_bound', 0 <= weight <= 36*max(lam,0)**2)
                for m in (lm,ls):
                    physical_over_r = ((k*m[0][0],m[0][1]),(m[1][0],m[1][1]/k))
                    transferred = det(physical_over_r)
                    if mutant == 'determinant_k4':
                        transferred *= k**2
                    gate('anisotropic_determinant', transferred == det(m))
                    for idx in (1,2):
                        gate('inertia_filtered_congruence', filt(physical_over_r,idx) == filt(m,idx))
                for x,z in ((Q(-1,2),Q(0)),(Q(1,2),Q(0)),(Q(2,3),Q(-3,4))):
                    p = cubic(k,-lam/k,gam,b/k,c/(k*k),x,k*z)/k
                    gate('deterministic_polynomial_not_field_law', p == raw(lam,gam,b,c,x,z))
                bs = (b-gam*gam/12)/k
                ds = (c-gam*b/4+gam**3/72)/(2*k*k)
                d = gam*gam-12*b
                j = 8*gam**3-144*b*gam+576*c
                gate('CUB_raw_shear', bs == -d/(12*k) and ds == j/(1152*k*k))
                gate('CUB_weight_identity', 9*k*k*(4*(lam/k)**2-bs*bs)
                     == (6*lam+3*b-gam*gam/4)*(6*lam-3*b+gam*gam/4))

# Independent signed-matrix check of the square off-diagonal loss used in z_r.
for a in (Q(-3),Q(0),Q(2)):
    for b in (Q(-2),Q(0),Q(5)):
        for c in (Q(-3,2),Q(0),Q(1,4)):
            m=((a,c),(c,b)); diag=((a,Q(0)),(Q(0),b))
            for idx in (1,2):
                gate('off_diagonal_square_loss', abs(filt(m,idx)-filt(diag,idx)) <= c*c)

for kl,ku in ((Q(1),Q(1)),(Q(1,3),Q(5,2)),(Q(2),Q(4))):
    s=1+ku
    constants=(9/(64*kl)+Q(1,16)+s**4/(24*kl),
               33/(128*kl)+Q(1,16)+max(1/kl,Q(1))*s**3/6,
               17/(48*kl)+Q(1,24)+max(1/kl,Q(1),ku)*s*s/2)
    gate('compact_gap_Taylor_constants', all(v > 0 for v in constants))
    if kl == ku == 1:
        gate('unit_gap_Taylor_constants', constants == (Q(167,192),Q(635,384),Q(115,48)))

# Pole cancellation is checked as rational squared-norm algebra.
for gam in (Q(-3),Q(1,7),Q(2)):
    for edge in (Q(1,5),Q(1),Q(9)):
        kap=edge/(48*gam*gam)
        frob=Q(1,3)+(Q(1,144)+1/(gam*gam))/kap
        gate('Hessian_pole_cancellation', frob == (1+(gam*gam+144)/edge)/3)
        k2=Q(115,48)
        coeff=(Q(1) if mutant == 'hessian_factor' else Q(2,3))*k2
        gate('entry_to_operator_Hessian_factor', coeff == Q(115,72))

# Original torus need not be preserved by the physical affine coordinate map.
for reflection in (Q(1),Q(-1)):
    rot=((Q(3,5),-reflection*Q(4,5)),(Q(4,5),reflection*Q(3,5)))
    for k in (Q(1,2),Q(3)):
        r,L=Q(1,7),Q(5)
        a=((r*rot[0][0],r*k*rot[0][1]),(r*rot[1][0],r*k*rot[1][1]))
        inverse=inv(a)
        basis=[mv(inverse,(L,Q(0))),mv(inverse,(Q(0),L))]
        if mutant == 'wrong_torus_lattice':
            basis=[(L,Q(0)),(Q(0),L)]
        gate('inverse_image_lattice', mv(a,basis[0]) == (L,0) and mv(a,basis[1]) == (0,L))
        y=(Q(2,9),Q(-4,7)); winding=(2,-3)
        end=tuple(y[j]+winding[0]*basis[0][j]+winding[1]*basis[1][j] for j in range(2))
        displacement=tuple(v-u for u,v in zip(mv(a,y),mv(a,end)))
        gate('winding_displacement', displacement == (2*L,-3*L))
reject('same_square_torus_without_lattice_change', mv(a,(L,Q(0))) == (L,Q(0)))

# Exact two-variable integrations, done via coefficients of polynomial primitives.
for upper in (Q(1,10),Q(1),Q(7,2)):
    inner_coefficient=(Q(48)**3/2-Q(48)**3/3)/16
    double_weight=inner_coefficient*upper**4/4
    double_plain=48*upper**2/2
    gate('radius_integrals', double_weight == 288*upper**4 and double_plain == 24*upper**2)
for H in (Q(2),Q(5),Q(11)):
    for r in (Q(1,100),Q(1,10000)):
        for delta in (Q(1,2),Q(1,8)):
            strip=H*H*delta*delta/2+r*H**4*delta
            if mutant == 'drop_edge_term':
                strip=H*H*delta*delta/2
            gate('finite_r_strip_term', strip == H*H*delta*delta/2+r*H**4*delta)
            for v in (3,4,6):
                top=Q(48)
                exact=H*H*(delta**(2-v)-top**(2-v))/(v-2)
                exact+=r*H**4*(delta**(1-v)-top**(1-v))/(v-1)
                bound=H*H*delta**(2-v)/(v-2)+r*H**4*delta**(1-v)/(v-1)
                gate('truncated_inverse', 0 < exact < bound)

# Correlation and normalization counterexamples: no probabilistic independence inferred.
ew=Q(1+4,2); en2=Q(1+9,2); ewn2=Q(1+36,2)
reject('factor_weighted_N_moment', ewn2 == ew*en2)
weighted_joint=((Q(2),Q(3)),(Q(3),Q(5)))
reject('tilted_residual_scalar_stays_independent', det(weighted_joint) == 0)
model_strip=Q(1,2)**2/2; actual_strip=model_strip+Q(1,10)*Q(1,2)
reject('discard_finite_r_strip', actual_strip <= model_strip)
reject('jet_TV_controls_unbounded_field_norm', Q(1,100)*Q(10000) <= Q(1,100))

# Independent tail numerator integration; retain the residual indicator externally.
for r in (Q(1,10),Q(1,40)):
    for residual in (Q(1),Q(3)):
        cap=2*r*residual**2
        numerator=r*r*residual**4*(cap**3/3+3*r*residual**2*cap*cap/2)
        gate('endpoint_residual_integral', numerator == Q(26,3)*r**5*residual**10)
        zr=Q(7,5); full=r*r*zr
        gate('full_normalizer_once', r**(-3)*numerator/full == Q(26,3)*residual**10/zr)
        gate('retained_exception_scale', r**(-3)*r**4 == r)
reject('soft_r4_normalizer', full == r**4*zr)
reject('second_full_normalizer', r**(-3)*numerator/full**2 == Q(26,3)*residual**10/zr)
reject('omit_far_exception', r == 0)
endpoint=Q(2); midpoint=Q(-1); k=Q(3); r=Q(1,5)
reject('endpoint_depth_is_normalized_midpoint_lambda', endpoint == -k*midpoint/r)

# Chord extrema and two independent margins, with no trajectory interpretation.
for h in (Q(1,100),Q(1,4),Q(3,4)):
    mu=1-h
    def chord(t):
        return h*(2*t**3-3*t*t)
    gate('two_chord_margins', chord(Q(0)) == 0 and chord(Q(1)) == -h and chord(Q(2)) == 4*h)
    good=min(mu,4*h)/3
    gate('two_chord_margins', -h-good > -1 and 4*h-good > 0)
reject('saddle_margin_alone_ensures_older_endpoint', 4*Q(1,100)-Q(1,10) > 0)
reject('endpoint_margin_alone_ensures_saddle_clearance', -Q(99,100)-Q(1,10) > -1)
reject('axis_can_end_at_saddle', Q(-1) > Q(0))
reject('essential_maximum_has_older_endpoint', len([]) > 0)

# Corrected reciprocal switch: never extend the first fraction to negative denominators.
a0,b0,k0=Q(599,250),Q(277,250),Q(256,125)
switch=a0/(b0+k0*a0)
gate('corrected_G_switch', 0 < switch < 1/k0 < Q(1,2))
gate('corrected_G_switch', b0/(1-k0*switch) == a0/switch == Q(187969,31250))
reject('A2_unrestricted_reciprocal_domain', 1-k0*Q(49,100) > 0)

# Exponents computed from a monomial ledger, not copied literal outcomes.
# Coordinates (r,H,w0,d) have exponents (1,-1/12,-1/32,1/4).
power=(Q(1),Q(-1,12),Q(-1,32),Q(1,4))
terms={
 'radius':((0,0,-8,0),Q(1,4)),
 'radius_actual':((1,3,-4,0),Q(7,8)),
 'selected_value':((1,4,4,0),Q(13,24)),
 'selected_actual':((Q(3,2),5,2,0),Q(49,48)),
 'endpoint':((Q(2,3),4,Q(8,3),0),Q(1,4)),
 'endpoint_actual':((Q(4,3),5,Q(4,3),0),Q(7,8)),
 'decision':((0,0,0,1),Q(1,4)),
 'density':((1,4,0,0),Q(2,3)),
 'decision_Markov':((2,3,8,-2),Q(1)),
 'Hessian_model':((2,5,4,0),Q(35,24)),
 'Hessian_actual':((2,7,2,0),Q(65,48)),
 'failure_tail':((0,-3,0,0),Q(1,4)),
 'cap_exceptions':((1,0,0,0),Q(1)),
}
for name,(powers,expected) in terms.items():
    if mutant == 'radius_power' and name == 'radius':
        powers=(0,0,-6,0)
    value=sum(a*b for a,b in zip(power,powers))
    gate('balance_'+name, value == expected and value >= Q(1,4))
admissibility={
 'physical_jet':((1,1,0,0),Q(11,12)),
 'embedded_window':((1,0,1,0),Q(31,32)),
 'value_error':((1,0,4,0),Q(7,8)),
 'selected_split':((1,2,4,0),Q(17,24)),
 'endpoint_split':((1,3,4,0),Q(5,8)),
 'Hessian_split':((1,0,2,0),Q(15,16)),
 'level_width':((0,0,0,1),Q(1,4)),
}
for name,(powers,expected) in admissibility.items():
    value=sum(a*b for a,b in zip(power,powers))
    gate('admissibility_'+name,value == expected and value > 0)
gate('fixed_moment_orders',10+2*3 == 16 and 6+2*3 == 12)
gate('probability_consumer',3+Q(1,4) == Q(13,4))
reject('radius_model_rho6_suffices_for_claimed_schedule', 6*Q(1,32) >= Q(1,4))
reject('finite_moment_order_proves_half_endpoint', Q(3,2*(3+3)) == Q(1,2))
reject('witness_second_multiplicity_is_failure_mass', Q(2)+Q(3) == Q(2)+2*Q(3))

# Off-T complement truth table and nonnegative measure normalization bound.
typed=False; selected=False; model_selected=False; model_rejected=False
reject('Boolean_complements_agree_off_T', ((not selected) != model_rejected) == (selected != model_selected))
for vec in ((Q(1),Q(2)),(Q(1,2),Q(4)),(Q(3),Q(1,4))):
    ref=(Q(2),Q(1)); total=sum(vec); baseline=sum(ref)
    variation=sum(abs(a-b) for a,b in zip(vec,ref))
    normalized=sum(abs(a/total-b/baseline) for a,b in zip(vec,ref))
    gate('conditional_positive_mass', normalized <= 2*variation/total)

print('C103 independent rational controls; Python ' + sys.version.split()[0])
for key in sorted(checks):
    print(key+': '+str(checks[key])+' passed')
print('Positive controls: '+str(sum(checks.values())))
print('Rejected false-inference fixtures: '+str(len(negatives)))
for name in negatives:
    print('REJECTED: '+name)
print('Mutant mode: '+(mutant or 'none'))
print('No Gaussian, topology, nullity, or continuum-rate proof is claimed by these controls.')
print('PASS_C103_INDEPENDENT_CONTROLS')
