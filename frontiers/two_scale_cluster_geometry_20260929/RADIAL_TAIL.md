# An eleven-power microscopic radius tail and its universal extreme-height law

Object: OA-TWO-SCALE-CLUSTER-GEOMETRY-20260929-R1.
Author: OpenAI / GPT-6 Astra Pro, foreground recovery, 29 September 2026 (Central).
Disposition: AUTHOR-SIDE CONDITIONAL PROOF; NONAUTHOR REVIEW REQUIRED.
Scientific effect NONE. No scientific-status transition or numerical Gaussian
coefficient is asserted. This is an analytic calculation for the explicit
limiting MICROSCOPIC measure M of TWO_SCALE_LAW.md (M1), not for the entire
finite-r global field or its remote singleton component.

## 1. Which radius and which sampling law?

Use the exact source conventions and fixed d,L,b,k,frame of TWO_SCALE_LAW.md.
For each additional root (X_i,Z_i) of the unsheared planar cubic, its physical
rescaled position is

    v_i=X_i e_axis+Z_i e_soft(O),        R_i=|v_i|.

Define the finite point-intensity measure by integrating the sum over these roots
against M. Its tail mass is

    F(t)=integral sum_i 1{R_i>t} dM.                         (R1)

This is point-intensity sampling: a cluster with two qualifying points contributes
two, not one. Every assertion below is a statement about the limiting microscopic
measure. In an application to the Gaussian field, r->0 is taken before t->infinity.
No finite-r uniform spatial moment or rate is inferred.

**Theorem R.** There is an explicit finite positive C_star such that

    F(t) ~ C_star t^-11.                                    (R2)

For p>=0 the microscopic intensity moment integral sum_i R_i^p dM is finite
exactly when p<11. The same threshold holds for the maximum radius of a nonempty
cluster under its normalized limiting law. At the boundary, the capped intensity
moment satisfies

    integral sum_i min(R_i,t)^11 dM ~ 11 C_star log t.        (R3)

A full formula for C_star is given in (R13). No numerical evaluation of its
Gaussian integral is claimed.

## 2. Resolve one stationary point by an exact change of variables

Retain the canonical shear invariants of CUB:

    u=X+aZ/(12k), B=beta-a^2/(12k),
    D=(c-a beta/(4k)+a^3/(72k^2))/2, x=-s>0.

At fixed a the inverse raw-jet map is

    beta=a^2/(12k)+B,
    c=a^3/(144k^2)+aB/(4k)+2D,
    |d(beta,c)/d(B,D)|=2.                                (R4)

The factor 2 is essential. This is a change in the JET coordinates, separate
from the determinant-one spatial shear. The remaining third-jet entries, denoted
xi, are unchanged.

Let

    b0(u)=3-12u^2,       v=xZ^2/k.

For an extra root, the canonical conic and line give the inverse parametrization

    x=kv/Z^2,
    B=k b0(u)/Z^2,
    D=k(v-b0(u)u)/Z^3,       Z!=0.                        (R5)

Conversely, every parameter in the region defined below with Z!=0 gives a strict
window root at (X,Z)=(u-aZ/(12k),Z). The normalized DOWNWARD height is

    eta=-P/k=u+1/2+v/6.                                   (R6)

Typed endpoints require v>|b0(u)|/2. The open height window requires 0<eta<1.
Combining these gives precisely the bounded region

    D_shape={ -3/2<u<1/2, |b0(u)|/2<v<3-6u }.              (R7)

For completeness, the lower height inequality v>-6u-3 is automatic on R7:
for -1/2<=u<1/2 its right side is nonpositive; for -3/2<u<-1/2, subtracting it
from |b0|/2 gives 6(u+1/2)^2>=0. The upper height inequality and v>|b0|/2 are
compatible exactly on the displayed u interval. Boundaries are excluded.

An explicit determinant computation gives the ORIENTED Jacobian

    det d(x,B,D)/d(v,u,Z)
       =6k^3(12u^2+4uv-3)/Z^8
       =-6k^3[b0(u)-4uv]/Z^8.                             (R8)

On R7 both b0(u)-4uv and 4v^2-b0(u)^2 are strictly positive. The first is also
the saddle determinant sign from CUB; it can be checked directly: for u<-1/2,
use v>|b0|/2, and for u>=0 use v<3-6u, giving a lower bound
12(u-1/2)^2, with the remaining interval -1/2<=u<0 immediate. The second follows
from v>|b0|/2. Thus the Jacobian is nonzero in the open region.

For each fixed (x,B,D) in the typed domain there are at most two extra window
roots. The usual change of variables with multiplicity is legitimate here:
cover R7 times (R minus {0}) by countably many neighborhoods where R5 is a
diffeomorphism, make them disjoint measurably, apply the ordinary change of
variables to each, and sum the resulting nonnegative integrals. The multiplicity
is exactly the number of counted roots, rather than an omitted or extra factor
of two. Degenerate/boundary jets are algebraically null and not in the strict
window. This justifies applying R5 to a point-intensity sum.

Define

    Q(u,v)=[4v^2-b0(u)^2][b0(u)-4uv].                      (R9)

The endpoint weight is w=9k^4[4v^2-b0(u)^2]/Z^4. Combining this with the absolute
Jacobian R8 and the raw-jet Jacobian 2 of R4 gives exactly

    w ds d beta dc =108 k^7 Q(u,v)|Z|^-12 du dv dZ,         (R10)

in the point-counted integral, with a and all other spectral/tensor variables
retained. This identity incorporates the root multiplicity through the map,
not by an additional constant. The two signs of Z will be integrated next.

## 3. Tail scaling, domination and the complete coefficient

Let h,O,xi be the remaining variables of M, and let tau(a,beta,c,xi) denote the
full rotated cubic tensor in those coordinates. Its raw contact Gaussian density
remains evaluated at

    h0(A0,Rot_O(tau)),      A0=O diag(0,-h)O^t.

It is NOT replaced by an isotropic density. Combining M1 and R10 gives the exact
representation of F(t) as the integral over R7 and Z!=0 of

    (108 k^7 c_m/z0) Q(u,v) H(h) |Z|^-12
    h0(A0,Rot_O tau(a, a^2/(12k)+k b0/Z^2,
           a^3/(144k^2)+a b0/(4 Z^2)+2k(v-b0 u)/Z^3, xi))
    *1{ (u-aZ/(12k))^2+Z^2 > t^2 },                     (R11)

with measure du dv dZ da dxi dh dO, ordered positive h, and the empty-product
conventions for d=2. The coefficient a b0/(4Z^2) in c includes the k cancellation
in aB/(4k). Formula R11 is often where confusing the spatial and jet Jacobians,
or integrating out a before testing the actual radius, gives a wrong exponent
or coefficient.

Put Z=t z and gamma(a)=sqrt(1+(a/(12k))^2). Then |Z|^-12 dZ=t^-11 |z|^-12 dz.
At each fixed nonzero z the raw jet tends to the cusp slice

    beta_cusp=a^2/(12k),         c_cusp=a^3/(144k^2),

and the radius indicator tends almost everywhere to 1{gamma(a)|z|>1}.
For t>=3 and |u|<=3/2, the indicator in R11 implies

    |z|>1/[2gamma(a)]

by the triangle inequality t<|u|+gamma|Z|. Orthogonal norm equivalence and SC's
Gaussian density bound imply, uniformly in t,z,u,v,O,

    h0(A0,Rot_O tau(a,beta,c,xi))
                   <= C exp[-c(|h|^2+a^2+|xi|^2)].

Dropping beta and c from this upper bound is legitimate; it never introduces
an inverse hard eigenvalue. Integration in z over |z|>1/(2gamma) costs at most
a constant times gamma^11. Q is bounded on the bounded region R7, H(h) is a
nonnegative polynomial, and Gaussian integration in h,a,xi dominates gamma^11.
Dominated convergence therefore applies to t^11 F(t).

Let

    J_cusp=integral H(h) gamma(a)^11
       h0(A0,Rot_O tau(a,a^2/(12k),a^3/(144k^2),xi))
                                      da dxi dh dO.       (R12)

This is finite by the same majorant and positive by positivity of the Gaussian
density and H on open sets. Integrating both signs of z gives
integral_(gamma|z|>1)|z|^-12 dz=2 gamma^11/11. Finally,

    I_shape=integral_Dshape Q(u,v) du dv=246528/35,

    C_star=(216/11) k^7 (c_m/z0) I_shape J_cusp
          =(53250048/385) k^7 (c_m/z0) J_cusp.             (R13)

For an exact check of I_shape, integrate v first using

    (4b0/3)v^3 -4u v^4 -b0^3 v +2u b0^2 v^2.

The strips -3/2<u<-1/2 and -1/2<u<1/2 contribute, respectively,
231744/35 and 2112/5. Their sum is 246528/35. These are exact rational polynomial
integrals, not quadrature estimates. The factors in R13 are: 9 from the weight,
6 from the stationary-point Jacobian, 2 from dc/dD, and 2/11 from both radius
signs and the tail integral.

This proves R2 in every fixed d>=2 under the source interface. The exponent 11
is dimension-independent here because the hard directions affect only the
finite integral J_cusp; the soft jet weights are s,B of degree -2, D of degree -3,
and endpoint weight of degree -4, for total 2+2+3+4=11. This explanatory homogeneity
is not substituted for the dominated-convergence proof.

For p>0, Tonelli gives the moment identity integral R^p=p integral_0^infinity
t^(p-1)F(t)dt. Finite total point mass handles t<=1 and R2 handles infinity.
This proves the threshold in Theorem R and the boundary formula R3. If R_max
is the maximum radius of a nonempty cluster, its unnormalized tail lies between
F(t)/2 and F(t), since there are at most two points. Its normalized law therefore
has the same exact moment threshold, although no exact maximum-tail coefficient
is claimed. QED.

## 4. A universal law for an intensity-selected far local point

Normalize the point-intensity measure restricted to R_i>t. For that selected
point retain its canonical shape variables (u,v), downward height eta, radial
ratio q=R_i/t, sign epsilon=sign Z, and the remaining variables (a,h,O,xi).

**Theorem H (extreme local marks).** As t->infinity, the joint law converges
weakly to the product of:

1. shape density Q(u,v)/I_shape on R7;
2. a Pareto radial ratio q>=1 with density 11q^-12;
3. a symmetric sign epsilon in {-1,1};
4. the parameter measure with density H(h) gamma(a)^11 times the cusp Gaussian
   in R12, divided by J_cusp.

In particular eta=u+1/2+v/6 is independent of the limiting radial ratio and the
remaining parameter measure. Its probability density on 0<e<1 is H_eta(e)/I_shape,
where

    H_eta(e)=(110592/7)[e^(7/2)-(1-e)^(7/2)+1]
                      +13824[e^4-2e^3+5e^2-4e].          (H1)

This density, unlike the amplitude C_star or orientation law, is independent of
d,L,b,k and the fixed axial frame. It is a universality statement only for the
intensity-selected LARGE-RADIUS tail of the limiting microscopic process.
The full local height law and the global height law are not asserted universal.

**Proof.** Apply the dominated-convergence argument of Section 3 with any bounded
continuous function of the listed variables. In the limit use the radial change
q=gamma(a)|z|. The measure |z|^-12 dz becomes gamma(a)^11 q^-12 dq on each sign,
and the threshold is q>1. The limiting Gaussian depends only on (a,h,O,xi), while
Q depends only on (u,v). Division by R13 gives exactly the four factors above.
No claim of spatial independence in the original field is involved.

To obtain H1, substitute v=6e-6u-3, with dv=6de. Conditions R7 become

    -1/2-sqrt(e) < u < 1/2-sqrt(1-e),    0<e<1.

Thus an explicitly nonnegative integral form of H_eta is

    H_eta(e)=6 integral_(-1/2-sqrt(e))^(1/2-sqrt(1-e))
                                  Q(u,6e-6u-3) du.       (H2)

Expanding this polynomial integral yields H1. This also proves its positivity
on (0,1), despite cancellations in the closed form. Its mass and first two
moments, computed exactly either from H1 or directly on R7, are

    integral_0^1 H_eta(e)de=I_shape,
    E eta=5771/7062,
    E eta^2=2440/3531.                                   (H3)

For integer j>=0 a reproducible rational formula before dividing by I_shape is

    integral e^j H_eta(e) de
      =(110592/7)[1/(j+9/2)-B(j+1,9/2)+1/(j+1)]
          +13824[1/(j+5)-2/(j+4)+5/(j+3)-4/(j+2)],        (H4)

with B(j+1,9/2)=j!/product_(l=0..j)(9/2+l). No special-function numeric library
is needed to check these moments. Seven such moments are checked independently
against exact double polynomial integration on R7. QED.

## 5. Evidence boundary and useful falsifiers

The finite companion independently checks the oriented root Jacobian, the inverse
raw-jet map and its factor 2, stationary heights and gradients at 648 rational
parameter choices, the two exact shape integrals, H4 versus direct integration,
and the k^7/radius-power ledgers. Eight explicit false variants must fail.
These controls do not prove the Gaussian bound, change-of-variables multiplicity,
weak convergence or domination; those are the written analytic obligations above.

The result would fail if the contact slice lost full positive Gaussian density,
if the physical radius were incorrectly replaced by |Z| before retaining a,
or if the invariant density were assumed isotropic rather than kept under Haar.
A finite-r spatial-moment convergence claim, a global tail including remote
singletons, an ordinary configuration-selected version of H1, or a numerical
Gaussian value of C_star would require new work and is not supplied here.
