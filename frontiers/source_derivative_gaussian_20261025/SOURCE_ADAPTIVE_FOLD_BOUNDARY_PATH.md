# Constructed ridge, scalar barriers and an attained rectangle path

Continue the original formal goal by composing the qualified constructed ridge
with the scalar companion, then deriving the minimal ambient data for the
existing elder-boundary theorem. Add only AdaptiveFoldBoundaryPath.lean. The
preflight is /workspace/scratch/ridge-barrier-join-preflight/REPORT.md; proposed
signatures there guide implementation, while this committed contract binds scope.

Use literal V : Real x Real -> Real, G=Vy V, H=Vx V and actual fderiv coordinate
partials from AdaptiveFoldTransverseRidge. J=[-3/2,3/2]. Structural inputs are C4 V
on open O containing J x [-R,R], R,c>0, M0,M1,M2>=0, Gy<=-c, strict opposite G
boundary signs, |G(x,0)|<=M0, |Gx|<=M1 and all FOUR ordered coordinate entries
of D2G bounded by M2 throughout the rectangle. Also |Hy|<=M1, axial
D2H[ex,ex]>=A, and the OTHER THREE ordered entries of D2H bounded by M2.
Both ordered mixed entries must be explicit; assume no unproved symmetry or norm
identity. All estimates concern actual literal derivatives and the rectangle,
not a chosen ridge or desired profile/barrier.

Set s=M1/c, t=(M2/c)(1+s)^2 and E=M2(2s+s^2)+M1*t. Assume 1+E<=A.
The two literal gradient pins are G(+-1/2,0)=H(+-1/2,0)=0, and the literal
potential gap V(-1/2,0)-V(1/2,0)=1/6. These are input pins, not a preexisting
ridge or scalar certificate. Equivalent finite Prop bundles may collect inputs.

Required analytic public theorem exists_transverse_ridge_scalar_barrier:
construct U,z from these inputs, return open U containing J, C2 z, actual unique
interior G-zero graph with graph in O, z(+-1/2)=0, structural ridge bounds,
actual profileSlopeSecond>=1 on J and ScalarBarrier(profileSlope V z,
profileSlopeFirst V z,profile V z). Reuse the exact qualified constructor and
profile jets. Prove the finite coordinate error bound
|profileSlopeSecond-D2H[ex,ex]|<=M2(2|z'|+|z'|^2)+M1|z''|<=E,
then call scalarBarrier_of_secondDerivative unchanged. Do not replace structural
estimates by the desired profile curvature as a premise. Full endpoint
derivatives come from the existing open collar. No supplied ridge/regularity/
barrier/elder certificate is a premise of the public constructor.

Required geometric public theorem exists_transverse_ridge_boundary_path:
add M0/c<=R and 1<=(c/2)(R-M0/c)^2. Obtain ONE witness from the analytic
constructor and retain it throughout the result, rather than selecting separate
incompatible ridges. Put M=(-1/2,0), S=(1/2,0), P=(3/2,z(3/2)), m=V M,
d=V S, D=[-3/2,1/2] x [-R,R]. Return the analytic result for this same z plus:
- literal vertical loss V(x,y)<=V(x,z x)-(c/2)(y-z x)^2 on the rectangle;
- D closed, M in D (interior if convenient), d<m, V M=m and V P>=m+1/4;
- V<=m throughout D and V<=d throughout frontier D;
- an explicit Path M P with V>=d everywhere and midpoint equal S.
The path is the ridge graph at x(t)=-1/2+2t, not an assumed path/certificate.
Derive the frontier bound from the left arm, right root and vertical drop.
Strict unique maximizers/frontier-equality refinements, H0/torus transport, ODE
capture and source probability/count/density/Parent A/B Lean inhabitants are
outside this minimal slice. Do not reprove existing Cap, scalar comparison,
H0 or elder-boundary theorems. Do not import their full umbrella packages.

A disjoint scratch-only helper may prove the new scalar vertical quadratic-loss
lemma from actual slice derivatives and concavity. Integrate needed bodies once
with exact frozen lineage; final public theorem constructs the ridge internally.
Root owns lakefile/manifests/commits/publication. Producer owns only the one new
module and its scratch evidence. No full Mathlib import, admissions, custom
axioms, native_decide or implemented_by. Allowed axioms: propext,
Classical.choice, Quot.sound. Reuse completed32-module/25-input qualifications.

Controls: actual V=x^3/3-x/4-4y^2 at R=1,c=8,M0=M1=M2=0,A=2 must
instantiate the full constructed boundary/path theorem and recover the zero
ridge, boundary bound, actual path and normalized pins/gap. A substantive
negative control drops only the vertical-drop budget: V=x^3/3-x/4-y^2/100,
R=1,c=1/50,other bounds zero,A=2 satisfies the analytic structure, but at
(-1/2,1) its frontier value exceeds d. Record the actual counterexample and
an expected mathematical False rejection, not a missing-name/API failure.
New-only strict compile, exactly one named own-module kernel replay after final
source, exhaustive classified inventory/axiom coverage and controls; preserve
all failures, source/object identities, commands/exits and honest timing limits.
Separate provider-distinct scientific review stays pending without erasing any
completed mathematical evidence. Scientific effect NONE.
