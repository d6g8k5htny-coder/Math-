# Extreme whole-cluster sampling: exact maximum/minimum tails and the anchored doublet law

Object: OA-EXTREME-CLUSTER-SAMPLING-20260930-v1.
Author: OpenAI / GPT-6 Astra Pro. Foreground continuation authorized by Dylan.
Disposition: AUTHOR-SIDE CONDITIONAL PROOF CANDIDATE; NONAUTHOR REVIEW OPEN.
Scientific effect NONE. No earlier proof, review, global register, Boolean,
prize or integration disposition is changed. Same-provider/source exposure is
not organizational independence. Finite checks below are not analytic acceptance.

## 1. Exact object and source boundary

Fix d>=2, L>0, b in R, k>0 and one axial/transverse orthonormal frame. This
paper concerns the ALREADY-FORMED limiting microscopic cubic measure M, not
the full finite-r Gaussian field and not its remote singleton component.
The limit that forms M is taken BEFORE the radius t tends to infinity.

Sources and their complete identities are in SOURCES.json:

[R] PR166 RADIAL_TAIL.md, exact head80059a97cd8eb32d1a17a0ad9cb22cb2a0d7b337,
blob0f14417ef7038b9c6f50e4b01e393a58b7b5e3a4, 12533 bytes. Consume the exact
root-parametrized integral R4-R12, its Gaussian majorant, the point tail R13,
and the height moment identities H3-H4. Its separate reviews B/C bind these
unchanged bytes. This paper adds a once-per-cluster selector; R does NOT already
claim the coefficient of the maximum or an ordinary cluster-selected H1 law.

[M] PR166 TWO_SCALE_LAW.md at the same head, bloba32fd5f7d941bbe1fe943df045b1e0fbec8d691c,
17139 bytes: only the definition M1-M2 of the explicit microscopic measure and
its embedding in the fixed original frame. The new two-scale convergence theorem
of that file is NOT a premise of the calculation here.

[SC] PR162 PROOF.md at382c0f9ff2281f43651ddbdf2e9b36dd52e2c6bf,
blob16c56821b52fd76b0be791622b9c3809eafde75a: the explicit Gaussian/spectral M,
its finite nonempty mass, and the contact-density bound. This conversation
AUTHORED SC; citing it does not independently revalidate its parent premises.

[CUB] PR158 PROOF.md atbfcc67dc8957b3ed1fbb789e5a0305e98d7359c8,
blobbb446d08db8a944537a743ad550b88c1c2ad5758: the exact deterministic cubic
classifier only. Its Gaussian-sector statement is not consumed. This conversation
authored CUB. R and M are also OpenAI-authored, in a separate active lane.

All Gaussian conditions remain conditional on those exact sources. No whole
review disposition is inferred from these source-local uses.

For theta=(s,h,O,tau), the hard curvatures satisfy 0<h2<...<h_(d-1), O has
normalized Haar measure, and tau is the complete rotated cubic tensor except
f_xxx. Its three soft entries are a,beta,c. Let

  A0=O diag(0,-h2,...,-h_(d-1)) O^T,
  H(h)=product h_j^3 product_(2<=i<j<=d-1)(h_j-h_i),
  B=beta-a^2/(12k),  w=9k^2(4s^2-B^2) on s<-|B|/2,
  dM=(c_m/z0) h0(A0,Rot_O tau) H(h) w ds dh dO dtau.       (E1)

The weight is zero off that typed domain. Empty hard products are one in d=2.
h0 is the actual RAW contact Gaussian density; no isotropy assumption is made.
z0 is the limit of the FULL endpoint normalizer divided by r^2. M need not be
finite on all jets. Its restriction to n(theta)>0 is finite, with total mass
A_micro=a1+a2>0, and n belongs to {0,1,2} almost everywhere.

The unsheared cubic and its physical limiting root position are

  P(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2+(a/2)(X^2-1/4)Z
                         +(beta/2)XZ^2+(c/6)Z^3,
  z_i=X_i e_axis+Z_i e_soft(O),  R_i=|z_i|,
  eta_i=-P(X_i,Z_i)/k in (0,1).                           (E2)

Only additional strict-window roots are included, not the pins. Every such
root has full limiting index d-1. Define R_max on nonempty configurations;
on doublets also define R_min. Let

  F(t)=integral sum_i 1{R_i>t} dM,
  G(t)=M(n>0,R_max>t),
  G2(t)=M(n=2,R_max>t),  B2(t)=M(n=2,R_min>t).             (E3)

F is a POINT intensity. G is a CLUSTER tail. Exactly, for every t,

  F(t)=G(t)+B2(t).                                       (E4)

This elementary multiplicity identity is the distinction missing from a
naive transfer of the point-selected law to whole clusters.

## 2. Main constants and results

Let J_cusp and gamma(a) be the positive finite integral and physical-shear
factor from R12:

  gamma(a)=sqrt(1+(a/(12k))^2),
  J_cusp=integral H(h) gamma(a)^11
    h0(A0,Rot_O tau(a,a^2/(12k),a^3/(144k^2),xi)) da dxi dh dO.

Set

  C0=(216/11) k^7 (c_m/z0) J_cusp,
  I=246528/35,
  J=1083417/280,
  D=27066286003/223205220-(79298560/4782969) log(2),
  I_max=I-D.                                            (E5)

Here D is a universal scalar shape integral, NOT a hard Hessian or the cubic
coefficient called D in CUB/R. In Sections3-4 the latter is written D_cub.

**Theorem 1 (whole-cluster tail coefficients).** All the constants multiplying
C0 below are strictly positive, and

  F(t) ~ C0 I t^-11,              [the prior R result]
  G(t) ~ C0 (I-D) t^-11,
  G2(t) ~ C0 J t^-11,
  B2(t) ~ C0 D t^-11,
  M(n=1,R_max>t) ~ C0 (I-D-J) t^-11.                     (E6)

In particular the maximum/point coefficient ratio is the exact universal number

  theta_star=(I-D)/I
    =1545114756173/1572181042176
                         +(10841600/4605999147)log(2).    (E7)

This ratio is NOT asserted to be a temporal extremal index of the original
field. There is no stationary sequence of pin pairs or mixing assertion here.

Under the ordinary microscopic cluster probability law
pi=A_micro^-1 1{n>0}dM, conditioning on R_max>t gives

  P_pi(n=2 | R_max>t) -> J/(I-D),
  P_pi(K_t=2 | R_max>t) -> D/(I-D),
  E_pi[K_t | R_max>t] -> I/(I-D),                         (E8)

where K_t is the number of points above threshold t. A double cluster need
not have both of its points above the threshold. Exact rational/logarithmic
interval certificates, not numerical Gaussian integration, give

  0.984415773209943375 < theta_star < 0.984415773209943376,
  0.558034234065747870 < J/(I-D) < 0.558034234065747871,
  0.015830939745347846 < D/(I-D) < 0.015830939745347847.     (E9)

**Theorem 2 (anchored extreme configuration).** Section6 specifies the full
weak limit of a cluster under pi(. | R_max>t), with its positions divided by t,
its original normalized heights, and its maximum-radius root distinguished.
The radial ratio has Pareto exponent11 and is independent of its anchored shape,
sign and cusp parameters. The limiting doublet is antipodal, has radius ratio
rho in (0,1), and its farther saddle has strictly GREATER downward height eta,
i.e. it lies lower in the height window. Shape/count/height/radius-ratio laws
are universal for these fixed-parameter microscopic extremes; the orientation
and tail amplitude generally retain model dependence.

Theorems1-2 are new consumers, not part of R's already reviewed point theorem.

## 3. Companion-root involution and the once-per-cluster shape domain

Use R's shear invariants

  u=X+aZ/(12k),  x=-s>0,
  b0(u)=3-12u^2,  v=xZ^2/k,
  B=k b0(u)/Z^2,  D_cub=k(v-b0(u)u)/Z^3.                  (E10)

A strict typed window root is parametrized exactly by Z!=0 and

  S={-3/2<u<1/2, |b0(u)|/2<v<3-6u},
  eta=u+1/2+v/6,
  Q(u,v)=[4v^2-b0(u)^2][b0(u)-4uv]>0.                    (E11)

The letter S denotes this bounded SHAPE region, not the conditioned saddle.

Put b=b0(u) temporarily and define

  L=4v^2-8buv+b^2,
  t_c=(4v^2-b^2)/L,
  u_c=[2bv-u(4v^2+b^2)]/L,  v_c=v t_c^2.                 (E12)

Off L=0, (u_c,v_c,t_c Z) is the other extra stationary root. Its membership
in S determines whether it is also counted. Thus n=2 exactly when (u_c,v_c)
is in S. L=0 is the degree-drop locus: the second root in this parametrization
is at infinity rather than a finite second point. It is an algebraic null set.
No contribution is assigned to a fictitious point there.

Proof of E12. At Z'=tZ the stationary line and conic reduce to

  b u'+(v-bu)t=v,       12(u')^2+b t^2=3.

When b!=0, substitute u'=(v-(v-bu)t)/b. The resulting quadratic has one root
1; its other root is the ratio of its constant to its leading coefficient:

  t_c=(12v^2-3b^2)/(12(v-bu)^2+b^3)
      =(4v^2-b^2)/(4v^2-8buv+b^2).

Substitution gives u_c and then v_c. At b=0 the direct equations give the
same formula wherever L!=0; the b=0 slice is null in any case. Since the
construction swaps the two roots, applying it twice returns the original
(u,v), with t_c t_cc=1. Direct useful identities are

  b0(u_c)=b t_c^2,
  v_c-b0(u_c)u_c=(v-bu)t_c^3.                             (E13)

These preserve the same x,B,D_cub under E10 with Z'=t_cZ.

### 3.1 Explicit doublet and anchor domains

For doublets b<0. Write p=-u, A=12p^2-3=-b>0. Define

  V_+(p)=[36p^2-12p-3+3 sqrt((2p-1)^3(18p+7))]/4,
  L_p=A/2, U_p=3+6p.

Up to boundary null sets, the doublet region splits into

  S2_outer:
     1/2<p<1,       L_p<v<A p;
     1<=p<3/2,      L_p<v<U_p;

  S2_inner:
     1/2<p<1,       A p<v<V_+(p).                        (E14)

The notation outer/inner refers to the larger/smaller ABSOLUTE Z coordinate.
The anchor domain for all nonempty configurations is

  S_star=S minus S2_inner.                               (E15)

Equal-|Z| doublets on v=A p may be counted with weight1/2 per root; this curve
has zero shape measure. This convention is not imposed on finite-t physical
radii, whose exact ordering is retained in the convergence proof.

Proof of the partition. CUB gives n=2 iff v<-b and
12(v-bu)^2<(v+b)^2(2v-b). Inside S, b>=0 cannot meet v<-b.
For b<0, u=-p with 1/2<p<3/2. The difference of the two sides factors as

  (v-A)^2(2v+A)-12(v-Ap)^2=(U_p-v) H_p(v),
  H_p(v)=-2v^2+(36p^2-12p-3)v-72p^3+36p^2+18p-9.

H_p is concave quadratic with upper root V_+. Its lower root is below L_p
because H_p(L_p)=9(2p-1)^3(2p+1)>0. If p<1,
H_p(A)=18(p-1)(2p-1)^2(2p+1)<0 and A<U_p, so the counted
interval is (L_p,V_+). If p>=1, U_p<=A and
H_p(U_p)=36(p-1)(2p+1)^2>=0, so the interval is (L_p,U_p).

Both counted roots are on the negative branch of the hyperbola. The stationary
line minus that strictly concave branch is strictly convex and is negative
at Z=0 (its line intercept is -v/A<-1/2). If it has two zeros, zero lies strictly
between them: a strictly convex function with two zeros is positive outside
their interval. Hence t_c<0 on doublets. Since 4v^2-b^2>0, L<0 there. Consequently

  |t_c|>1 iff v>b u=A p,
  |t_c|<1 iff v<A p.                                    (E16)

For p<1, H_p(Ap)=-9(p-1)(2p-1)^3(2p+1)^2>0, so
L_p<Ap<V_+. For p>=1, Ap-U_p=3(p-1)(2p+1)^2>=0. These
observations prove E14. Thus S_star contains exactly one asymptotic maximum
anchor per cluster, apart from the harmless tie curve.

### 3.2 Height ordering and the intensity-change identity

On a doublet put ell=v/A (>1/2). A direct substitution in E12 gives

 eta_c-eta=2(ell-p)(4p ell-1)^3/(4ell^2-8p ell+1)^2.      (E17)

Here p>1/2 and 4p ell>1. The outer anchor has ell<p by E16, so
eta_c<eta. The equal-height case is the equal-|Z| curve and is null.

Let T(u,v)=(u_c,v_c). On the open doublet region, the root-parametrized measure
in R10 is invariant under swapping the roots. Since Z'=t_c(u,v)Z, its Jacobian
is |det DT| |t_c|. Equating the two expressions for the same jet-volume weight
therefore gives

  Q(T(u,v)) |det DT(u,v)| = Q(u,v)|t_c|^11.                (E18)

This can also be checked by differentiating E12. It is a finite-dimensional
change-of-variables identity, not an assumed stationarity or temporal Palm law.
It implies the useful normalization

  integral_(S2_outer) Q |t_c|^11 du dv
                 = integral_(S2_inner) Q du dv = D.      (E19)

## 4. Exact shape integrals, including the logarithmic correction

The old point integral is I=integral_S Q=246528/35. Integrating first in v
on u=-p, with A=12p^2-3, uses the polynomial primitive

  P0(p,v)=4p v^4-(4A/3)v^3-2p A^2 v^2+A^3 v.             (E20)

The two polynomial strips of S2_outer give exactly

 integral_(1/2)^1 [P0(p,Ap)-P0(p,A/2)]dp =596217/1120,
 integral_1^(3/2)[P0(p,3+6p)-P0(p,A/2)]dp=3737451/1120.

Their sum is J=1083417/280. The inner strip gives

 D=integral_(1/2)^1[P0(p,V_+(p))-P0(p,Ap)]dp.              (E21)

To evaluate E21 without quadrature, first put
q0=sqrt((18p+7)/(2p-1)), then y=(q0-3)/(q0+3). In reverse orientation,
y runs from1/4 to1 and

  p(y)=(4y^2+y+4)/(18y),
  A(y)=8(1-y)^2(2y+1)(y+2)/(27y^2),
  V_+(p(y))=4(1-y)^2(y+2)/(9y^2),
  -p'(y)=(2/9)(y^-2-1).                                 (E22)

Every term of [P0(p(y),V_+(p(y)))-P0(p(y),A(y)p(y))](-p'(y))
is a Laurent polynomial. Integration term by term gives precisely D in E5.
For a monomial coefficient c_j y^j, its contribution is

 c_j[1-4^(-(j+1))]/(j+1), j!=-1;
 2c_(-1)log2, j=-1.                                     (E23)

The executable certificate retains this full Laurent polynomial, not a fitted
integral. It independently reproduces its values by exact polynomial interpolation
of the original v-integrand. In particular the logarithmic coefficient is
-79298560/4782969, not zero. The constant D is positive because E21 integrates
Q>0 over a nonempty open set. I-D-J is positive because the single-root shape
sector is also nonempty and open.

For later height moments define D_j=integral_(S2_inner) eta^j Q du dv. An explicit
primitive for the same rationalization is

 P_j(p,v)=sum_(ell=0..j) binom(j,ell)(1/2-p)^(j-ell)/6^ell
  *[16p v^(ell+4)/(ell+4)-4A v^(ell+3)/(ell+3)
       -4p A^2 v^(ell+2)/(ell+2)+A^3 v^(ell+1)/(ell+1)].  (E24)

E22-E23 then give

 D_0=27066286003/223205220-(79298560/4782969)log2,
 D_1=1259212131941593/15982386572880
                                  -(3186360320/387420489)log2,
 D_2=72706616008642669/1315122095139840
                                  -(15686696960/3486784401)log2. (E25)

For certified decimal bounds use log2=2 sum_(j>=0)3^(-(2j+1))/(2j+1).
After N terms the omitted positive remainder is bounded above by

  2*3^(-(2N+1))/[(2N+1)(1-1/9)].                          (E26)

All interval endpoints are rational. The code uses60 terms, propagates coefficient
signs and positive divisions, and rounds the displayed lower/upper decimals
OUTWARD. No floating-point quadrature is used to establish E9 or E25.

## 5. Proof of the maximum and minimum tails

R's exact root-resolved integral is, with the physical radius retained,

  (108 k^7 c_m/z0) Q(u,v) H(h) |Z|^-12
   h0(A0,Rot_O tau(a,a^2/(12k)+k b0/Z^2,
           a^3/(144k^2)+a b0/(4Z^2)+2k(v-b0u)/Z^3,xi))
       du dv dZ da dxi dh dO.                            (E27)

It counts a cluster once for each of its qualifying roots. For G(t), multiply
by 1{R_i>t} times the indicator that this root has the greatest ACTUAL physical
radius, dividing by the number of ties if necessary. The sum over roots is
exactly 1{R_max>t}. This is a Borel operation on a finite configuration and
introduces no extra determinant or normalizer.

Put Z=t z. For almost every shape, off the algebraic exceptional sets L=0,
eta_c in{0,1} and |t_c|=1, the actual maximum indicator tends to 1_(S_star).
Indeed, R_i/t->gamma(a)|z| and R_c/t->gamma(a)|t_c z| if a counted companion
exists. The bounded u and u_c offsets disappear, but a is NOT integrated away:
its gamma factor remains inside the radius condition.

The dominating argument is exactly the source R11-R12 argument with one more
factor between0 and1. For t>=3, |u|<=3/2 and R_i>t imply
|z|>1/(2gamma(a)). Orthogonal Gaussian norm equivalence bounds the density by
C exp[-c(|h|^2+a^2+|xi|^2)]. The z-integral of |z|^-12 over that set costs
only C gamma(a)^11; S is bounded, H(h) is polynomial, and the resulting
Gaussian integral is finite. Thus dominated convergence applies, including
the unbounded a and hard/tensor coordinates. No inverse hard eigenvalue enters.

The limiting z-integral on either sign, with the radius condition retained,
is gamma(a)^11/11. Both signs, the source factors108 and the cusp integral
yield C0. The shape integral is I_max=integral_(S_star)Q=I-D, proving
G(t)~C0(I-D)t^-11. Multiplying by 1{n=2} gives shape S2_outer and coefficient
C0 J for G2. E4 and the known point tail then give the B2 coefficient C0 D.
Subtract G2 from G to get the singleton coefficient. This proves E6, and all
ratios E7-E9 follow since the denominators have strictly positive limits.

There is no assumption that the seed root's |Z| ordering equals physical
radius ordering at finite t. It need only agree almost everywhere in the limit;
the exact physical selector was used before taking that limit.

Moment consequences: under the appropriate normalized nonempty/doublet measure,
R_max and R_min both have moment threshold11. For R_min the doublet condition is
understood. The capped unnormalized moments have exact boundary coefficients

 integral_(n>0) min(R_max,t)^11 dM ~11 C0(I-D)log t,
 integral_(n=2) min(R_min,t)^11 dM ~11 C0 D log t.          (E28)

These follow from Tonelli and E6. They are not uniform finite-r spatial moments.

## 6. Full anchored extreme law and its universal consequences

Distinguish the actual maximum-radius root, using any Borel tie rule. Under
pi(. | R_max>t), retain its seed shape(u,v), q=R_max/t, sign epsilon=sign Z,
and remaining parameters(a,h,O,xi). The limiting joint probability is the product
of

  Q(u,v)1_(S_star)/I_max du dv;
  11q^-12 dq on q>1;
  the uniform sign law on{-1,1};
  H(h)gamma(a)^11 h0(A0,Rot_O tau_cusp)/J_cusp da dxi dh dO. (E29)

Proof: insert a bounded continuous function of these variables into E27 with
the exact maximum selector. The same majorant works. The limiting change
q=gamma(a)|z| produces gamma(a)^11 q^-12 dq, so normalization by the maximum
coefficient gives E29. The maps and the selector are continuous off the
already excluded null curves. This proves weak convergence, not total variation
of spatial laws. No uniformity in escaping model parameters is asserted.

Let

  e_*(a,O)=[-a e_axis/(12k)+e_soft(O)]/gamma(a).

If the selected shape is a singleton, the limiting marked configuration is
one point at epsilon q e_* with height eta=u+1/2+v/6. If it is a doublet,
put rho=|t_c|<1, eta_c=u_c+1/2+v_c/6. The full configuration, in positions
divided by the threshold t, is

  {(epsilon q e_*, eta, d-1),
   (-epsilon q rho e_*, eta_c, d-1)}.                     (E30)

E17 proves eta_c<eta on the doublet sector. Thus its farther point is deeper,
and the two extreme positions are antipodal. This is a SECOND limit of the
microscopic geometry, not a claim that finite-r critical points lie on one line.

The scalar q is independent of shape and remaining parameters. In particular,
conditional on a doublet, rho and the two heights are independent of q. From E19,

  E[rho^11 | limiting extreme cluster is double]=D/J.      (E31)

For a given rho, a Pareto(11) q has probability rho^11 of making q rho>1.
Combining E31 with P(n=2)=J/I_max gives D/I_max in E8 once more. This reconciles
the two-point-cluster frequency with the much smaller double-exceedance frequency.

### 6.1 The maximum anchor's height is not the old intensity-selected height

Let H_eta(e) be R's nonnegative height numerator (H1-H2), with integral I.
The height density for the maximum anchor is instead

 [H_eta(e)-6 integral_(1/2)^1 Q(-p,6(e+p-1/2))
       1{A(p)p<6(e+p-1/2)<V_+(p)} dp]/I_max,  0<e<1.     (E32)

The bracket is nonnegative: it subtracts exactly the nonmaximal-root subset
from the full point-shape intensity. From the old point moments and E25,

  E eta_max = [I*(5771/7062)-D_1]/(I-D),
  E eta_max^2 = [I*(2440/3531)-D_2]/(I-D).                 (E33)

Certified enclosures are

  0.819586988784918536 < E eta_max < 0.819586988784918537,
  0.694438469047655310 < E eta_max^2 < 0.694438469047655311.

Hence the configuration-selected anchor law is genuinely different from the
point-intensity height law. E29/E32 are universal in fixed d,L,b,k,frame; the
cusp parameter distribution, directions and C0 generally are not universal.

## 7. Deliberately independent replicas: an identified maximum law

Take independent configurations C_1,...,C_n with the ALREADY-FORMED microscopic
probability law pi. This is an explicitly imposed independence, not a property
of different pin pairs in the original Gaussian field. Put

  a_n=[n C0(I-D)/A_micro]^(1/11).

For every x>0, E6 gives

 P(max_(i<=n) R_max(C_i) <= a_n x)
   =[1-P_pi(R_max>a_n x)]^n -> exp(-x^-11).               (E34)

This is the standard iid extreme-value consequence with the newly identified
cluster coefficient. Normalizing by the POINT tail coefficient instead gives
exp(-theta_star x^-11); it is not the same normalization. No new coefficient
convergence rate, simultaneous n/r limit, within-field Poisson assertion or
stationary-sequence extremal-index theorem follows from E34.

## 8. Review obligations and nonclaims

A: E10-E19, companion involution, strict-window partition, tie/degree-drop
boundaries, exact Jacobian/multiplicity and the height ordering.
B: E20-E26 and E33, the rationalized Laurent integral, all logarithmic constants,
certified rational intervals and the independent finite integration controls.
C: E27-E34, actual physical maximum selection, domination, full anchored weak
law, the differing sampling measures, min/max/exceedance coefficients and iid
scope. These are not waived by tests or parent review acceptance.

No global scientific-status change, numerical evaluation of J_cusp, finite-r
uniform spatial tail/moment, new elder-pairing law, dependence theorem across pin
pairs, growing-volume theorem, or Lean formalization is claimed. Counterexamples
to shortcuts: F counts both above-threshold roots whereas G counts the cluster
once; replacing G by F sets theta_star=1 incorrectly. Omitting the maximum
selector and summing over roots gives the prior point-intensity height law, not
E32. Uniformly choosing one root inside each uniformly selected cluster is yet
another sampling convention and must not be identified with point intensity. Dropping log2 from E21 changes a positive exact shape integral. A single
1/r rescaling still cannot retain the remote singleton population.
