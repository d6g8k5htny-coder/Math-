"""C99 author controls: exact finite algebra, not a continuum proof.

stdlib only; no assert (normal and -O perform the same tests).
Authors of this checker: OpenAI/Codex root01a0adb2.
It is withheld from the fresh reviewer until their own implementation.
"""
from fractions import Fraction as F
from collections import Counter
import json
import sys

counts = Counter()
negative = []

def check(group, condition):
    if not condition:
        raise RuntimeError("failed control: " + group)
    counts[group] += 1

def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("false inference accepted: " + name)
    negative.append(name)

def poly(k, eta):
    s, a, beta, q = (k * e for e in eta)
    return {(3,0):2*k, (1,0):-3*k/2, (0,0):-k/2,
            (0,2):s/2, (2,1):a/2, (0,1):-a/8,
            (1,2):beta/2, (0,3):q/6}

def derivative(p, axis):
    out = {}
    for ij, value in p.items():
        exponent = ij[axis]
        if exponent:
            new = list(ij)
            new[axis] -= 1
            out[tuple(new)] = value*exponent
    return out

def evaluate(p, x, z):
    return sum((value*x**i*z**j for (i,j),value in p.items()), F(0))

def jet(p, x, z):
    dx, dz = derivative(p,0), derivative(p,1)
    return (evaluate(p,x,z), evaluate(dx,x,z), evaluate(dz,x,z),
            evaluate(derivative(dx,0),x,z),
            evaluate(derivative(dx,1),x,z),
            evaluate(derivative(dz,1),x,z))

def target(b, r, k, eta):
    s,a,beta,q = eta
    return (b-k*r**3/2,-k*r**2,F(0),12*k,F(0),F(0),
            r*k*s,k*a,k*beta,k*q)

etas = [(F(-2),F(1),F(1,2),F(3)),
        (F(-1),F(0),F(0),F(6)),
        (F(-5,3),F(-2),F(7,5),F(-4,3))]
ks = [F(1,3),F(1),F(5,2)]
for eta in etas:
    p1 = poly(F(1),eta)
    for k in ks:
        pk = poly(k,eta)
        for x,z in [(F(-1,2),F(0)),(F(1,2),F(0)),
                    (F(2,3),F(-1,4)),(F(-3,7),F(5,6))]:
            for value, base in zip(jet(pk,x,z),jet(p1,x,z)):
                check("cubic_two_jet_scaling",value==k*base)
        check("exact_pin_M",jet(pk,F(-1,2),F(0))[:3]==(F(0),F(0),F(0)))
        check("exact_pin_S",jet(pk,F(1,2),F(0))[:3]==(-k,F(0),F(0)))
        s,a,beta,q = eta
        b1 = beta-a*a/12
        bscaled = k*beta-(k*a)**2/(12*k)
        w1 = 9*(4*s*s-b1*b1)
        wk = 9*k*k*(4*(k*s)**2-bscaled*bscaled)
        check("shear_B_scaling",bscaled==k*b1)
        check("determinant_k4",wk==k**4*w1)
        check("jet_and_weight_k8",k**4*wk==k**8*w1)

for eta in etas:
    for r in [F(1,5),F(1,16)]:
        b,ka,kb,k = F(7,3),F(1,2),F(3),F(7,4)
        ta,tb,tk = target(b,r,ka,eta),target(b,r,kb,eta),target(b,r,k,eta)
        for va,vb,vk in zip(ta,tb,tk):
            slope=(vb-va)/(kb-ka)
            check("exact_affine_target",vk==va+(k-ka)*slope)

for h in [F(1,8),F(1,31)]:
    for t in [F(2,3),F(3,2)]:
        r=t*h
        # Candidate radial r dr, rare r^3, dr=h dt.
        check("radial_h5",r*r**3*h/h**5==t**4)
        for z0 in [F(2),F(7,3)]:
            Z=r*r*z0
            check("rare_r3",r*r**4/Z==r**3/z0)
            pi=F(5,7)
            A=12*pi*Z/(r*r)
            check("one_full_Z",A*(r*r/Z)==12*pi)
        z=F(2,5)
        k=F(7,4)
        tau=t**3*k*z
        check("inverse_k",tau/(t**3*z)==k)
        check("k_coarea",F(1)/(t**3*z)*(t**3*z)==1)
        check("t_coarea",t**4/(3*t*t*z)==t*t/(3*z))
        for area in [F(9),F(24**2)]:
            C=F(4,7)
            p=area*C*h**5
            check("field_first_area",area*h**5*C/p==1)

# Exact nonempty model fixture: k=1,s=-1,B=0,q=6.
# Extra window saddle Y=(-1/2,1/3), height -1/54; the other
# extra critical point is below the pinned window and cannot be
# dropped without inspecting inertia/membership separately.
p=poly(F(1),(F(-1),F(0),F(0),F(6)))
Y=(F(-1,2),F(1,3))
value,px,pz,hxx,hxz,hzz=jet(p,*Y)
check("actual_model_fixture",(value,px,pz)==(F(-1,54),F(0),F(0)))
check("window_fixture_saddle",hxx*hzz-hxz*hxz<0)
for k in ks:
    pk=poly(k,(F(-1),F(0),F(0),F(6)))
    check("critical_branch_height",jet(pk,*Y)[0]==-k/F(54))
    check("positive_lifetime_slope",k>0 and F(1,54)>0)

# Reconstruct ROOTS R4's published below-window fixture from the
# original cubic, not its source-author checker. This catches actual
# omission from the reciprocal, which a window-only fixture cannot.
pbelow=poly(F(1),(F(-39,16),F(0),F(-3),F(3,2)))
root_data=[]
for point,height,det in [((F(-5,8),F(3,4)),F(-53,512),F(-297,32)),
                         ((F(-37,24),F(-35,12)),F(-11125,4608),F(-1155,32))]:
    v,gx,gz,xx,xz,zz=jet(pbelow,*point)
    check("all_root_fixture",(v,gx,gz)==(height,F(0),F(0)))
    check("all_root_inertia",xx*zz-xz*xz==det and det<0)
    distance2=(point[0]+F(1,2))**2+point[1]**2
    gap2=v*v/(distance2**3)
    root_data.append((v,distance2,gap2))
below_height,distance2,gap2=root_data[1]
check("below_window_membership",below_height<-1 and F(1,4)<distance2<16
      and F(1,10000)<gap2<4)
check("below_window_exact_distance",distance2==F(5525,576))
check("below_window_exact_gap",gap2==F(71289,10793861))
full_rejected_count=1+int(F(1,4)<distance2<16 and F(1,10000)<gap2<4)
window_only_count=1+int(-1<below_height<0)
check("full_reciprocal_count",full_rejected_count==2 and window_only_count==1)

# A finite histogram model permits an exact pushforward TV split,
# with discontinuous reciprocal-like weights. Integrate piecewise
# constant densities on their common endpoint refinement.
def density_intervals(edges, values, slope, shift=F(0)):
    return [(slope*a+shift,slope*b+shift,v/slope)
            for a,b,v in zip(edges,edges[1:],values)]

def l1(intervals_a, intervals_b):
    edges=sorted({x for intervals in (intervals_a,intervals_b)
                  for a,b,v in intervals for x in (a,b)})
    answer=F(0)
    for a,b in zip(edges,edges[1:]):
        mid=(a+b)/2
        da=sum(v for lo,hi,v in intervals_a if lo<mid<hi)
        db=sum(v for lo,hi,v in intervals_b if lo<mid<hi)
        answer+=(b-a)*abs(da-db)
    return answer

edges=[F(1),F(3,2),F(2)]
base=[F(1),F(1,2)]
reference=density_intervals(edges,base,F(3,5))
map_errors=[]
for n in [2,4,8,16,32,64]:
    eps=F(1,n)
    altered=[base[0]+eps,base[1]+eps/2]
    moved=density_intervals(edges,base,F(3,5)+eps,eps)
    changed=density_intervals(edges,altered,F(3,5)+eps,eps)
    joint=l1(density_intervals(edges,altered,F(1)),
             density_intervals(edges,base,F(1)))
    check("TV_contraction",l1(changed,moved)==joint)
    check("weighted_TV_split",l1(changed,reference)<=joint+l1(moved,reference))
    map_errors.append(l1(moved,reference))
check("C1_map_errors_decrease",all(a>b for a,b in zip(map_errors,map_errors[1:])))

# Whole positive-axis global-L1 inequality on exact three-cell masses.
for left in [F(0),F(1,7),F(3,5)]:
    for center in [F(1,4),F(1),F(8,5)]:
        for right in [F(0),F(2,9),F(6,5)]:
            actual=[left,center,right]
            limit=[F(1,6),F(2,3),F(1,6)]
            total_error=sum(abs(a-b) for a,b in zip(actual,limit))
            local=abs(center-limit[1])
            mass=abs(sum(actual)-sum(limit))
            check("global_L1_mass_bound",total_error<=2*local+mass+2*(limit[0]+limit[2]))

for n in range(1,9):
    for weight in [F(1),F(1,2),F(-3,7)]:
        check("once_counted_reciprocal",sum(weight/n for _ in range(n))==weight)
    # Measure-level excess, allowing an arbitrary indicator test.
    for hits in range(n+1):
        check("field_first_excess",0<=F(hits)-F(hits,n)<=n-1)

# Negative false-inference fixtures.
reject("omit_jet_k4",F(2)**4*F(2)**4==F(2)**4)
reject("second_full_Z",12*F(5,7)/F(11,3)==12*F(5,7))
reject("missing_death_height_h3",F(1,8)**3==1)
reject("missing_once_count_reciprocal",F(1)+F(1)==1)
reject("universal_reciprocal_half",F(1)==F(1,2))
reject("omit_below_window_candidates",full_rejected_count==window_only_count)
reject("freeze_inverse_k",F(3,2)/F(3,4)==F(1))
# A spatial remainder e_r(k)=r sin(k/r) has amplitude<=r, but
# derivative in k is cos(k/r), equal1 at k=0. One cannot infer
# C1 from small spatial amplitude without G6's affine family.
remainder_at_zero=F(0)
parameter_derivative_at_zero=F(1)
reject("spatial_C0_implies_parameter_C1",parameter_derivative_at_zero==remainder_at_zero)
# The pinned saddle gap is exactly k for EVERY eta. On k=k_-
# its endpoint membership is equality everywhere, not a null eta-set.
pinned_gaps=[-jet(poly(F(1),eta),F(1,2),F(0))[0] for eta in etas]
reject("fixed_k_endpoint_slice_is_null",any(gap!=1 for gap in pinned_gaps))
# In the abstract joint plane the null boundary k=eta, eta in[1,2],
# projects to tau=k over the entire interval[1,2].
projected_boundary_length=F(2)-F(1)
reject("boundaries_project_to_null_tau",projected_boundary_length==0)
# a_n=indicator{|k-1/n|<1/(3n)} tends to0 a.e. at fixed k,
# but a_n(k_n)=1 for the moving inverse k_n=1/n.
moving_inverse_values=[]
for n in [2,4,8,16]:
    kn=F(1,n)
    moving_inverse_values.append(int(abs(kn-F(1,n))<F(1,3*n)))
reject("pointwise_density_after_moving_inverse",moving_inverse_values[-1]==0)
# Model lifetime support lies below C0^3*k_+; choose C0=1,k_+=2.
model_support_upper=F(1)**3*F(2)
J_outside=(F(3),F(4))
reject("positive_on_every_compact_J",J_outside[0]<model_support_upper)
# Same scalar lifetime tau=1, differing second mark locations0and1:
# marginals agree, but joint point masses are mutually singular.
scalar_marginal_difference=F(0)
joint_difference=abs(F(1)-F(0))+abs(F(0)-F(1))
reject("all_marks_TV_from_scalar_TV",joint_difference==scalar_marginal_difference)

# Oscillating nonnegative AC unit-mass densities: n exact alternating
# cells, value 2 then0. Their distribution functions differ from uniform
# by <=1/(2n), but their L1 distance is exactly1 for every n.
oscillations=[]
for n in [1,2,4,8,16,32]:
    e=[F(i,2*n) for i in range(2*n+1)]
    v=[F(2) if i%2==0 else F(0) for i in range(2*n)]
    oscillatory=density_intervals(e,v,F(1))
    uniform=[(F(0),F(1),F(1))]
    error=l1(oscillatory,uniform)
    check("weak_not_L1_fixture",error==1)
    check("oscillatory_unit_mass",sum((b-a)*val for a,b,val in oscillatory)==1)
    oscillations.append(error)
reject("weak_AC_equal_mass_implies_L1",oscillations[-1]==0)

# Escape near0 is invisible on every fixed positive compact: density
# n on (0,1/n) has mass1, local limit0. The total-mass premise cannot
# be omitted from D18a.
reject("local_L1_alone_implies_global",F(1)==0)

print(json.dumps({"object":"C99 author finite controls v1",
                  "controls":dict(sorted(counts.items())),
                  "total_controls":sum(counts.values()),
                  "rejected_false_inferences":negative,
                  "map_error_sequence":[str(x) for x in map_errors],
                  "scope":"Finite algebra and counterexamples only; no proof of analytic imports or continuum L1 theorem."},
                 indent=2,sort_keys=True))
