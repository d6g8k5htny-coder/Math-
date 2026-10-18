# Independent Gaussian smoothing admits nonGaussian fold universality

Conventional mathematical author proposal, 17 October 2026. Authors:
OpenAI/Codex nongaussian-smoothing-admission author and Root01a11cbf
(mechanism coauthor). This is a new reconstruction, pending a separate
exact-source nonauthor review. The independently frozen A4 source is not
changed. All contributors are source-exposed OpenAI agents; organizational
independence is zero. No scientific promotion is asserted.

## 1. Actual product law and conclusions

Let X be a fixed nonempty connected compact smooth manifold without
boundary, with fixed smooth Riemannian metric g and dimension d>=1.
Write V=vol_g(X). Fix an actual centered Gaussian smooth random field

    G=sum_{j>=1} a_j Z_j phi_j,                                    (1)

where Z_j are the original independent standard real Gaussians, a_j>0,
the real span of the deterministic phi_j is dense in C-infinity(X), and

    sum_j a_j ||phi_j||_Cq < infinity  for every integer q>=0.       (2)

Use increasing smooth norms from covariant derivatives or a finite
coordinate atlas. Fix independently a Borel C-infinity(X)-valued random
field W such that

    E ||W||_Cq^m < infinity  for every integer q>=0 and every m>0.   (3)

W need not be centered, Gaussian, stationary, bounded, or have any
exponential moment. A deterministic smooth W is allowed. The actual
law under consideration is the independent product construction

    F=G+W.                                                        (4)

The nonzero Gaussian component and independence are substantive
hypotheses. Constants are for this fixed decomposition, law, metric and
dimension. There is no assertion uniform as the Gaussian component
vanishes or its spectra/geometry degenerate. The theorem does not say
every smooth nonGaussian law has this decomposition.

For ordinary persistence over any fixed coefficient field K, exclude
essential intervals. If d>=2 and X is orientable, let p=0,...,d-1. If
X is not assumed orientable, the assertion here is p=0 only. In d=1
it is also p=0 only. For each of these degrees the expected finite
superlevel-Hp lifetime measure per volume has the explicitly specified
finite nonnegative Borel density representative nu_p in (12), and

    nu_p(ell) ~ C_p ell^(-1/3),
    E N_p((0,t])/V ~ (3/2) C_p t^(2/3),          ell,t ->0+,          (5)

with 0<C_p<infinity. The full actual joint-jet coefficient is

    C_p = 1/(2*12^(1/3)*V) integral_SX
        p_(D,V_u)^F(0,0)
        E_F[ |T_u|^(4/3) (det A_u)^2
             1{A_u has exactly p positive eigenvalues}
                         | D=0,V_u=0 ] dvol_g(x) d sigma_x(u).     (6)

Here D=grad F(x), V_u=Hess F(x)(u,.), T_u is the third derivative
along the unit-speed geodesic in direction u, and A_u is the Hessian
restricted to u-perp. The sphere measure is ordinary Riemannian sphere
area. In d=1 the empty A has determinant one and zero positive
eigenvalues; S^0 counts both directions. In the p=0 result A is negative
definite, except for that empty convention. The literal conditional
law in (6) is specified below. It is the actual nonGaussian joint law,
not a Gaussian Schur moment computed from F's covariance.

For oriented X,d>=2 the leading coefficients, and the limiting marked
measure below, are independent of the chosen field K: the local
topological incidence is +/-1. Global pairings and lower-order terms
can depend on K. No equality C_p=C_(d-1-p) is inferred. The centered
Gaussian transverse sign symmetry used in a prior special model is
unavailable for a general noncentered mixture.

There is also an independent-whole-copy corollary, proved in Section 12.
For independent copies of this one fixed F, the rare short-bar processes,
with n t_n^(2/3)->lambda>0, converge to an explicitly marked Poisson
random measure with degree, scaled lifetime, birth height, cubic mark,
midpoint and direction marks. This is not a within-one-field spatial
Poisson theorem or a factorial-moment assertion.

## 2. Exact consumed theorems and what is new here

GAD is the smooth dense-support Gaussian admission proof, 40231 bytes,
739 lines, SHA256
8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319.
Its full proof, full 38035-byte accepted scoped review, and finite smooth
incidence appendix were read in this session. It proves for (1)-(2):
the actual smooth law and all norm moments; finite original coefficient
minors from dense smooth span; the actual full-field Gaussian conditional
version at every literal target; all-Borel finite-incidence Rice; off-
contact conditional genericity using finite residual coefficient ranks;
and the deterministic H0 elder-transfer geometry. Its hypotheses concern
G, not F. Applying its Gaussian conditional covariance formula directly
to F would be incorrect.

HF is Main331, Higher homology: attaching obstructions and isolated-fold
unit incidence, exact 46174-byte/911-line proof SHA256
87f43e6ed94c5c63c385ecf177f68212afa5db54b24062fa008f081f47a78999,
with exact 5443-byte review SHA256
4a24a4fe3e6bdd6e380ce1436f0b07eed587a03e01dc3ad6c59c59c4fbfba5fb.
Both were read completely. HF Sections 1-7 prove a deterministic
isolated regular-fold unit incidence and Borel once-counting on a closed
oriented manifold: a same-field globally C4-convergent continuation with
a single cubic contact, nonsingular transverse Hessian, exact two pins,
and all other critical points Morse with distinct heights away from
the contact gives the exact finite Hp interval. Mixed transverse
inertia changes its degree. This is the topology imported here.

HF's probabilistic Sections 8-11 admit only its named stationary Gaussian
torus law. They do not already prove (4), arbitrary geometry, or (3)'s
polynomial-only envelope. The source also retains a documentary README
audit qualification; this author does not modify that source or claim
an integration/metadata resolution. The new work here supplies the
actual product-law kernels, every analytic interface, manifold binding,
nonGaussian joint-jet coefficient, and bounded-cluster/iid-copy passage.

The deterministic HF import uses the specific classical relative handle
boundary formula: one transverse attaching/belt intersection has
incidence +/-1 over every field. Its proof constructs the local product
flow, excludes remote connecting trajectories by a fixed-annulus positive
height cost, proves no intervening critical value, and handles C4 by
aligned smoothing and regular-level isotopy. Its arbitrary adjacent-cell
counterexamples remain exclusions when these hypotheses are absent.
No new handle theorem or whole classical-book proof is claimed here.

## 3. Smooth product law, ranks and literal kernels

By GAD, G is a Borel smooth random element and all its smooth norms have
all finite moments. Thus F in (4) is Borel smooth, with all finite norm
moments by Minkowski and (3). Independence lets us use the actual product
space P_W tensor P_G throughout. Nothing requires W's raw coefficient
representation, a density for W, or recovery of W from F.

If L is any of the finite independent jet/observation maps used below,
the Gaussian covariance Gamma_L=Cov(LG) is positive. This follows from
dense-span bump-polynomial interpolation and a finite subset of the
original Gaussian coefficient columns. Write c_L=Cov(G,LG),

    R_L=G-c_L Gamma_L^-1 LG,
    G_{L,y}=R_L+c_L Gamma_L^-1 y.                                  (7)

R_L is a smooth Gaussian field independent of LG. Its finite observation
is zero. Formula (7) is the actual Gaussian conditional law at every y,
not an assertion that the pin event has positive probability. It is
jointly Borel in sites, frames and targets in local frame charts.

Let pi_L^G denote the positive Gaussian density of LG. Then LF has the
everywhere positive convolution density

    p_L^F(v)=E_W pi_L^G(v-LW).                                    (8)

It is finite and smooth in v; every derivative of a nondegenerate
Gaussian density is bounded, so differentiation under this mixture is
justified without any W exponential moment. Dependence on bounded
site/frame parameters is continuous by dominated convergence and the
proven covariance floors. The literal whole-field conditional version
of F at LF=v is

    Q^F_(L,v)(A)= [p_L^F(v)]^-1
       E_W[ pi_L^G(v-LW)
             P_G{ W+R_L+c_L Gamma_L^-1(v-LW) in A } ].              (9)

For each v this is a probability kernel; positivity of (8) makes its
denominator legitimate. Its measurability and normalization follow from
the explicit regression and Gaussian convolution. This is not a Gaussian
law in general. Its posterior distribution of W is weighted by the
displayed likelihood. Replacing it with the unweighted W law would give
the wrong conditional field.

To verify its literal version, condition first on a fixed smooth w,
split G into a finite original coefficient block plus its independent
smooth tail, and use the block's invertible observation minor. Its tail
receives the Bayes density pi_block(v-Lw-Ltail)/pi_G(v-Lw).
The remaining finite block has its affine Gaussian conditional law.
Finite Gaussian completion of squares identifies this with (7) at
every target v-Lw. Integrating the original W law multiplies by
pi_G(v-Lw), giving (9). Equality of finite evaluation characteristic
functions, followed by countable evaluation generation of the smooth
Borel sigma-field as in GAD, identifies the whole-field law, including
all Borel marks. A continuous-mark extension or almost-every-target
argument has not been substituted for this calculation.

Formula (9) names the literal whole-field version associated with the
fixed product decomposition (4). No uniqueness of all-target versions
across different decompositions is needed or asserted. The finite-jet
density is the intrinsic continuous convolution density of F, and all
counting identities use this explicitly matched version.

On compact separated site/frame domains, all needed Gaussian covariance
floors and smooth regression coefficient bounds are uniform. W is a
translation of the field, not of those Gaussian minors, so their ranks
are unchanged. Full finite F-jet laws are mixtures of shifted full-rank
Gaussian laws; they have strictly positive densities on every full
independent jet coordinate space.

## 4. COUNT_p and original genericity, conditioning on W first

For each fixed smooth w, the actual field w+G has the same independent
finite Gaussian coefficient directions as G. Fix a smooth Gaussian tail.
At a root, solve the gradient equations for an invertible finite
Gaussian coefficient minor. The incidence projection from site and
remaining coefficients has absolute Jacobian |det Hess(w+G)| divided
by that minor determinant. Smooth finite-dimensional Sard proves Morse
behavior for almost every Gaussian block. For distinct sites the joint
first jets of G have full rank; literal height disintegration rules
out ties between critical heights. A countable separated-domain/minor
cover gives these statements for the whole field, for each fixed w.
Integrating W proves that F is Morse with distinct critical values
almost surely. Compactness makes its critical set finite.

The same finite smooth incidence proof, with an arbitrary nonnegative
Borel whole-field mark, gives the two-point identity at fixed w.
Integrating W and using (8)-(9) gives the extended actual identity

    E sum_{M!=S, grad F(M)=grad F(S)=0} h(M,S,F)
      = integral_{M!=S} p^F_(grad_M,grad_S)(0,0)
         E_QF[ |det H_M det H_S| h(M,S,F) ] dvol(M)dvol(S).          (10)

The mark was Borel before tail integration; no continuity of a global
pairing is required. Each physical Hessian determinant appears once.
Expected total critical count is finite: the one-point Gaussian
gradient density is bounded uniformly, and its conditional Hessian
moment is bounded by C(1+||w||_C2)^(d), with constants enlarged if
necessary; (3) integrates this bound. Ties need only separated local
integrals and countable exhaustion, not a collision-uniform floor.

For oriented X,d>=2, use HF Section 7's Borel selector sigma_p(F,M,S)
of the unique ordinary finite Hp interval with these exact ordered
endpoints, extended by zero off the Morse/distinct locus. Its local
constancy is for the continued critical labels in a small Morse
neighborhood, as proved using aligned regular-level isotopies. Each
critical point has at most one endpoint role. For H0 in the other
cases use GAD's intrinsic rational strict-superlevel connection
selector and standard H0 elder linear algebra. Both count each finite
interval once and exclude essential intervals. Thus

    N_p((0,t])=sum_{M!=S, gradients zero}
        sigma_p(F,M,S) 1{0<F(M)-F(S)<=t}.                           (11)

For p>0, M is a birth critical point, not generally a maximum.
An index predicate alone would count candidates rather than bars.

Disintegrate both heights in (10) using the same literal kernels.
If O_MS=(F(M),grad F(M),F(S),grad F(S)), define for ell>0

    nu_p(ell)=V^-1 integral_{M!=S} integral_R
      p^F_O(b,0,b-ell,0)
      E_QF[ |det H_M det H_S| sigma_p(F,M,S)] db dvol(M)dvol(S).     (12)

The redundant inertia conditions are included in sigma_p. This
nonnegative Borel representative is the actual expected finite-bar
density by Tonelli. Its finiteness is proved below. We have obtained
COUNT_p for the actual product law, not merely a conditional Gaussian
candidate count.

## 5. Exact near observations and the same product-space coupling

Choose a fixed short-geodesic radius r_0>0. At x,u in SX let
M=exp_x(-ru/2), S=exp_x(ru/2). Parallel-transport a perpendicular
orthonormal frame along the geodesic. The literal 2d+2 observation
rows, applied to any smooth scalar field f, are

    U_r f=((f(M)+f(S))/2, (f(S)-f(M))/r,
       (f_u(S)-f_u(M))/r,
       (6/r^2)[f_u(M)+f_u(S)-2(f(S)-f(M))/r],
       ((f_vi(M)+f_vi(S))/2,(f_vi(S)-f_vi(M))/r)_i).

Their target for the two exact critical heights b,b-kr^3 is

    v_r=(b-kr^3/2,-kr^2,0,12k,(0,0)_i), k>0,
    v_0=(b,0,0,12k,(0,0)_i).                                     (13)

The r=0 extension is U_0=(f,f_u,f_uu,f_uuu,(f_vi,f_uvi)_i).
Integral finite-difference identities give ||U_r f||<=C||f||_C3
and ||(U_r-U_0)f||<=Cr||f||_C4, uniformly on SX. The exact change
from the two first jets O_MS has absolute determinant
12 r^(-(d+3)), unchanged by the law of f. In particular

    p_O^F(b,0,b-kr^3,0)=12 r^(-(d+3)) p^F_(U_r)(v_r).              (14)

This is the specific height/observation binding used in (12).

Use G's c_r=Cov(G,U_r G), Gamma_r=Cov(U_r G), and R_r from (7).
GAD's contact rank and compactness give common covariance floors
for 0<=r<=r_0 after decreasing r_0. Smooth covariance and the row
estimates imply convergence of c_r Gamma_r^-1 in each global smooth
norm, and R_r->R_0 globally C4 almost surely and in every finite
Lp norm. On the ORIGINAL product W,G define

    F_{r,w}=w+R_r+c_r Gamma_r^-1(v_r-U_r w).                       (15)

For each fixed w, this is the exact full-field conditional law
given U_r F=v_r within that component. It has the forced pins
exactly and converges to F_{0,w} globally C4, using the same G.
For every q>=3,

    ||F_{r,w}||_Cq <= C_q(||G||_Cq+||w||_Cq+1+|b|+k),              (16)

with harmless equivalent norms and enlarged constants. The bound
includes the deterministic conditional mean, which can grow with w.
There is no Gaussian assertion about F or inverse posterior normalizer
in (16). All unnormalized expectations below use this fixed product
space and the weight pi_r^G(v_r-U_r w).

## 6. Literal conditional off-contact genericity and contact isolation

Fix x,u, b in R and k>0, and ANY smooth w, and condition G on
U_0 G=v_0-U_0 w. The Gaussian finite block whose joint rows are
U_0 and one or two remote first jets has full rank on each compact
domain separated from x and, for two sites, from its diagonal.
Surjectivity of (U_0,J_remote) implies that J_remote is surjective
on the kernel of U_0: lift (0,y). This rank is independent of the
target and of w.

Under this literal target, the finite Gaussian block/tail description
is its positive Bayes-weighted smooth tail and an affine Gaussian on
the finite coefficient kernel. In an orthonormal basis of that kernel
the remaining coordinates are independent standard Gaussians. Adding
the deterministic smooth w and conditional mean does not change the
surjective residual gradient directions. Apply the finite incidence/
Sard argument in those coordinates. For every fixed w and target,
all other critical points of F_{0,w} are Morse almost surely. Residual
first-jet density excludes critical height b; residual two-first-jet
density excludes ties among other critical heights. Countably many
separated domains give the assertions on X minus {x}. A different
finite block can be used on each domain; all describe the same kernel.

The transverse A_0 of F_{0,w} has a shifted full-rank Gaussian density
on all independent symmetric entries. It is nonsingular almost surely,
and every inertia cone has strictly positive weighted determinant-square
mass at every fixed w,b,k,x,u. No centeredness of that matrix is assumed.
At the forced contact the gradient and axial Hessian column vanish,
the axial cubic derivative is 12k, and A_0 is nonsingular. The implicit
transverse critical ridge therefore has reduced derivative
6k s^2+o(s^2)>0 at sufficiently small nonzero s. The contact is isolated.
All other critical points lie in a compact complement, so they are
finite and have distinct heights with positive gaps from b.

This proves the required conditional genericity separately from original
Morse genericity. It holds for each fixed w and contact target, with
probability one in the Gaussian residual. Fubini gives the same statement
for the original W,G product at each fixed target. There is no uncountable
simultaneous event over every w,target,frame, and none is needed.

## 7. CONTACT_p and actual SELECT_p on the manifold

Put j=d-p-1. For H0 this means j=d-1. In the parallel endpoint frames
define

    W_(p,r)=|det H_M det H_S|
       1{index H_M=j+1,index H_S=j},
    V_(p,r)=W_(p,r)/r^2.

The exact gradient pins give the Hessian axial-column average zero.
As in GAD, the physical Hessian blocks and polynomial identity are

    H_i=[r alpha_i, r beta_i^T; r beta_i,A_i],
    det H_i/r=alpha_i det A_i-r beta_i^T adj(A_i)beta_i,
    alpha_M->-6k, alpha_S->6k, A_i->A_0.                           (17)

The r^-1/2 axial congruence gives the inertia. For each fixed w and
almost every residual G,

    V_(p,r) -> V_(p,0)
       =36 k^2 (det A_0)^2 1{index A_0=j},
    V_(p,r)<=C(1+||F_{r,w}||_C3)^(2d).                            (18)

If A_0 is nonsingular with a different inertia the indicator eventually
fails; at a singular A_0 the determinant vanishes in the limit regardless
of indicator oscillations. The polynomial identity avoids any inverse
curvature moment. Every index cone has finite positive contact mass.

For oriented X,d>=2, (15) and Section 6 meet HF's deterministic theorem.
To bind its physical chart to the manifold observations, use Fermi
coordinates (s,t) around the short geodesic: the axial coordinate is
unit speed and the transverse coordinate vectors on the axis are the
parallel frame. The two pins are literally (+-r/2,0). At the contact,
the zero gradient identifies coordinate and covariant Hessians, and
the axial third derivative is the geodesic derivative 12k. The fields
converge globally C4, hence in that fixed chart. These are HF's exact
geometric inputs on the stated closed oriented manifold. Its unit
incidence gives the actual finite Hp interval at the pinned endpoints,
and sigma_p=1 eventually whenever V_(p,0)>0. There is no invocation
of negative-definite H0 concavity for a mixed transverse block.

For H0 without the orientability/d>=2 premise, GAD's deterministic
asymmetric elder enclosure applies on the negative transverse cone,
with the older outgoing arm. The side wall is absent in d=1. It gives
the same exact finite H0 pair and eventual selector. Both mechanisms
also give global eventual Morse/distinct behavior and the complete
critical list: the local two roots and the finitely many old branches.

Define the UNNORMALIZED contact/selected kernels

    Z_(p,r)=E_W[ pi_r^G(v_r-U_r W) E_G V_(p,r) ],
    Y_(p,r)=E_W[ pi_r^G(v_r-U_r W) E_G(V_(p,r) sigma_p) ].          (19)

For each fixed b,k the bound (16),(18), pi_r^G<=C, and all moments
of W,G supply an integrable product-space bound. The weight converges
pointwise, and on V_(p,0)>0 the selector is eventually one; on V_(p,0)=0
the weighted determinant vanishes. Dominated convergence proves

    Z_(p,r)->Z_(p,0)>0,
    Y_(p,r)->Z_(p,0),
    E_W[pi_r^G E_G(V_(p,r)(1-sigma_p))]->0.                       (20)

These are actual same-product-space limits, not limits under a
fictionally r-independent posterior of W. Also p^F_(U_r)(v_r)->
p^F_(U_0)(v_0)>0 by bounded Gaussian densities and continuity. Division
by that FIXED-target positive normalizer gives CONTACT_p and SELECT_p
for the canonical F kernels (9), if normalized formulations are wanted.
No global lower bound for that normalizer has been used.

## 8. ENVELOPE_p with only polynomial moments of W

Here is the all-mark estimate which cannot be obtained by asserting
Gaussianity of F. Put B=1+|b|+k and N=1+||W||_Cq with q>=4 fixed.
The exact first/fourth target entries in (13) give uniformly

    |v_r|>=c_1 B-C,   |U_r W|<=C N.

Absorb the harmless constant in C_1 N. The Gaussian covariance floor
and upper bound give

    pi_r^G(v_r-U_r W)
       <=C exp[-c(c_1 B-C_1 N)_+^2].                              (21)

From (16),(18) and the Gaussian norm moments, with m=2d,

    E_G V_(p,r)<=C(B+N)^m.

Take epsilon=c_1/(2C_1)>0. On N<=epsilon B, the exponential in (21)
is at most exp(-c'B^2) and B+N<=C B. On N>epsilon B,
B+N<=C_epsilon N; discard the density exponential and use, for any
fixed M>0,

    E[N^m 1{N>epsilon B}]
        <=(epsilon B)^(-M) E N^(m+M).

The latter moment is finite by (3), even though E exp(cN^2) may be
infinite for every c>0. Thus for EVERY fixed M>0,

    0<=12Y_(p,r)<=12Z_(p,r)
       <=C_M [B^m exp(-c'B^2)+B^(-M)]
       <=H_M(b,k):=C'_M(1+|b|+k)^(-M).                           (22)

Constants are uniform in 0<r<=r_0, x,u and the finite set of p; they
depend on the fixed Gaussian law and the chosen W moment. Choose
M>4/3, for example M=6. Directly integrating b gives

    integral_R integral_0^infinity k^(-2/3) H_M(b,k) dk db<infinity:

near k=0 use k^-2/3 integrability and M>1 for b; at large k, b
integration gives order (1+k)^(1-M), and the remaining power is
k^(1/3-M), integrable precisely when M>4/3. The sphere bundle has
finite volume. This proves ENVELOPE_p without an inverse posterior
normalizer, Gaussian tails for W, or an exponential W moment.

The same argument works with untyped determinant weight, so it also
dominates candidate and bounded extra global marks. There is no
assertion of a uniform selector radius or rate over all W realizations.

## 9. FAR_p, finite density versions, and the curved Jacobian

On dist(M,S)>=r_0, G's joint two-first-jet covariance O_MS has a
positive floor on the compact domain. For 0<ell<=1, its target
(b,0,b-ell,0) is coercive in |b|. Under the literal kernel at fixed w,
the C2 norm/Hessian determinant product moment is bounded by
C(1+|b|+||w||_C2)^(2d). The same small-N/large-N split as Section 8
therefore bounds the UNNORMALIZED height integrand by
C_M(1+|b|)^(-M), uniformly in ell in this band and in separated sites.
Integrating b and the finite pair volume gives

    0<=nu_p,far(ell)<=C,             0<ell<=1.                     (23)

An analogous finite bound holds on every compact positive-lifetime
band. This is a direct bound on (12), not differentiation of a
cumulative bound or conditioning on a failed local event.

In the unique near band the midpoint/displacement map
(x,h)->(exp_x(-h/2),exp_x(h/2)) has natural volume Jacobian J(x,h),
smooth, positive, J(x,0)=1 and J(x,-h)=J(x,h). Its derivative at
h=0 is (a,b)->(a-b/2,a+b/2), of absolute determinant one. Therefore

    dvol(M)dvol(S)=J(x,ru) r^(d-1) dr dvol(x)d sigma_x(u),
    J(x,ru)=1+O(r^2)                                               (24)

uniformly on the compact sphere bundle. Curved geometry has not been
silently treated as flat. The near fixed-ell substitution k=ell/r^3
in (12), with (14),(18), gives

    ell^(1/3) nu_p,near(ell)
      =1/(3V) integral_{SX,R,(0,infinity)}
         1{k>=ell/r_0^3} k^(-2/3)
         J(x,(ell/k)^(1/3)u) 12Y_(p,(ell/k)^(1/3))
                                      db dk dvol(x)d sigma_x(u).  (25)

The radial ledger is (d-1)+3-(d+3)+2=1: spatial polar measure,
height change, literal observation density, and physical determinant
orders. No exponent was inferred merely from the cubic height gap.

The envelope (22) makes (25) finite at each ell>0, and uniformly
bounded after multiplication by ell^(1/3), with local bounds on
positive-lifetime intervals. Together with (23), (12) is the finite
Borel density representative asserted in Section 1. Equations
(20),(22),(24) and dominated convergence give

    C_p=4/V integral_{SX,R,(0,infinity)}
              k^(-2/3) Z_(p,0)(b,k,x,u)
                                  db dk dvol(x)d sigma_x(u).       (26)

Finiteness follows from the envelope. Positivity follows because for
every smooth w and every fixed b,k>0, the Gaussian likelihood is
positive and the shifted full Gaussian transverse matrix has positive
determinant-square mass on the required open inertia cone. Integration
over W and any nonempty finite mark window is strictly positive.
The cumulative factor 3/2 follows by integration of ell^(-1/3).
No density continuity or O(1) near remainder is asserted.

## 10. The full actual joint-jet invariant and geometric half

Let D,V_u,T_u,A_u have the meanings in Section 1. The full joint
law of their independent coordinates, with optional birth height F,
is a mixture of shifted nondegenerate Gaussian densities. Use exactly
the literal mixture kernels (9) for all their pins and disintegrations.
In particular the value at D=0,V_u=0 is specified, not an arbitrary
version of a conditional expectation. Normalized moments at this
fixed pin are finite: the Gaussian likelihood is bounded, its residual
jet moment is polynomial in W's finite jet, (3) integrates it, and
the fixed pin density is strictly positive.

At the contact, U_0 F=(b,0,0,12k,0,...) pins F=b,D=0,V_u=0,T_u=12k.
By (18), integrate the actual birth height b in (26), using Tonelli
and the same full joint convolution law. This yields

    C_p=144/V integral_SX integral_0^infinity k^(4/3)
        p^F_(D,V_u,T_u)(0,0,12k)
        E_F[(det A_u)^2 1{A_u has p positive eigenvalues}
                         | D=0,V_u=0,T_u=12k]
                                  dk dvol(x)d sigma_x(u).          (27)

The change t=12k gives 144*12^(-7/3)=12^(-1/3), hence

    C_p=12^(-1/3)/V integral_SX p^F_(D,V_u)(0,0)
        E_F[(T_u)_+^(4/3) (det A_u)^2 1{A_u has p positives}
                           | D=0,V_u=0] dvol(x)d sigma_x(u).       (28)

No covariance factorization, centered conditional matrix, or independent
odd/even jets have been assumed. This is the actual joint-jet invariant
of F. Its conditional distribution is generally nonGaussian.

For the alternative absolute-value formula (6), replace u by -u.
The same field has T_-u=-T_u. The transverse subspace, determinant
square and inertia cone are unchanged. The coordinates of D,V_u
transform linearly with absolute determinant one and preserve their
zero pin. Their actual density at zero and conditional law transform
accordingly. Ordinary sphere area is antipodally invariant. Therefore
the integrals of T_+^(4/3) and (-T)_+^(4/3), with these weights, are
equal AFTER integration over the full sphere. Their sum is the
absolute-value integrand. Averaging gives precisely (6).

This half is geometric averaging over opposite directions. It does
not require F or W to be centered, the law to be invariant under
F->-F, stationarity, reflection symmetry of the law, or any jet
independence. It is not a second division of ordered birth/death
pairs. Each actual interval was already counted once in (11).

For oriented X the local coefficient is independent of K by HF's
unit incidence; (27)-(28) also show no K in its limit. But changing
A to -A is a DIFFERENT transformation from changing u to -u.
There is no general sign symmetry of the transverse conditional
mixture. Already a scalar A distributed as N(m,1), m>0, has
E[A^2 1{A>0}]>E[A^2 1{A<0}], since for a>0 its two density terms
satisfy exp(-(a-m)^2/2)>exp(-(a+m)^2/2). This rejects importing the
old centered-Gaussian cone argument into this proof. No unproved
degree-duality identity for (4) is asserted.

## 11. Genuine nonGaussian examples and exact boundaries

Let H be an admitted smooth Gaussian series independent of G, and
epsilon!=0. Then

    W(x)=epsilon[H(x)^4-E H(x)^4]                                 (29)

is an actual smooth Borel field independent of G satisfying (3).
The deterministic function E H(x)^4=3 Var(H(x))^2 is smooth by covariance
summability. Leibniz gives ||H^4||_Cq<=C_q||H||_Cq^4; all required
moments follow from H's norm moments and Holder. At any point with
sigma^2=Var H(x)>0, the centered Gaussian even moments give

    E W(x)^3=epsilon^3[10395-3*3*105+2*27] sigma^12
             =9504 epsilon^3 sigma^12 !=0.

Independence and centering make the third cumulant of F(x) the same,
since G(x)'s third cumulant is zero and mixed centered terms vanish.
Consequently F is genuinely nonGaussian. Moreover for every c>0,
E exp(c |W(x)|)=infinity: for sufficiently large |H(x)| the absolute
value is bounded below by a positive multiple of |H(x)|^4, whose
positive quartic exponent dominates the Gaussian negative quadratic
density exponent. This admitted example has NO positive pointwise
absolute exponential moment. Such a moment cannot be a hidden
hypothesis of the envelope. The simpler centered-square example
epsilon[H^2-EH^2] is admitted too; its third cumulant is
8 epsilon^3 sigma^6, and it has no exponential-square moment.

If W is an independent random spatial CONSTANT S with all moments,
then every field realization G+S has exactly G's lifetime list and
pairing in every degree: all critical heights shift by S and all
height differences and sublevel inclusions simply reparameterize.
Formula (6) agrees exactly, because all the derivative jets in that
formula are unchanged. The birth integral (27) removes the random
height convolution. This is an exact consistency control, not a
claim that nonconstant W leaves the coefficient unchanged.

Independence cannot be omitted: W=-G has every smooth norm moment
and is smooth, but F=0 has no nondegenerate contact law or positive
finite-bar coefficient. This violates independence and so is outside
the theorem. Likewise the Gaussian component must satisfy the
stated actual dense-span ranks; merely writing a degenerate finite
Gaussian noise does not suffice. The constants and asymptotic window
need not remain controlled as that component approaches zero.

The prior covariance-matched random-amplitude counterexamples still
forbid universalizing over every smooth nonGaussian field with a
chosen covariance. Actual independent Gaussian smoothing, its
nonvanishing finite ranks, product moments, conditional selection
and envelope are the mechanism proved here. Covariance alone does
not assert that decomposition or those interfaces.

## 12. Bounded-cluster estimate and degree-marked iid-copy Poisson law

For the oriented manifold case sum p=0,...,d-1 and put N_t^all equal
to the number of all ordinary finite bars of lifetime <=t. No finite
degree-d bar can be killed by a (d+1)-handle. In the H0-only case
use just N_t^all=N_(0,t), and the degree mark is the singleton 0.
Each original field is Morse with a finite critical/lifetime list
almost surely; all its positive lifetimes are then bounded away
from zero for that realization. This fact alone would not prove
a Poisson limit, so we establish the required weighted cluster bound.

At fixed contact marks and fixed smooth w, for almost every Gaussian
residual with V_(p,0)>0, Section 7 gives the actual pinned bar and
the complete critical list for all small r. The two local critical
points' unique endpoint roles are consumed by this one bar. Every
other bar in the stated degree set therefore uses two OLD critical
branches. Their limiting heights are finitely many and pairwise
distinct, so every possible nonzero gap between them has a positive
lower bound. This remains true if their global pairing changes.
There are no additional critical branches near the forced contact.

Fix 0<a<=T and k>0, and set r=(ta/k)^(1/3). The pinned lifetime
is exactly ta<=Tt. Eventually it is the ONLY bar with lifetime <=Tt.
On V_(p,0)=0 the determinant weight tends to zero regardless of other
counts. Insert the bounded Borel mark 1{N_(Tt)^all>=2} into the
once-counted identity (11)-(12). After scaling ell=ta, the near
integrand divided by t^(2/3) is bounded by a finite constant times

    a^(-1/3) k^(-2/3) H_M(b,k),       0<a<=T,

with bounded J and compact SX. This is integrable INCLUDING a down
to zero and all b,k. Its weighted pointwise limit is zero by endpoint
exhaustion just proved; Section 7's unnormalized product-space DCT
remains valid with this bounded mark. Far anchored counts contribute
only O(t) by (23). Summing the finite degree set therefore gives

    E[N_(Tt)^all 1{N_(Tt)^all>=2}]=o(t^(2/3)).                     (30)

This is not a second factorial moment estimate. There is no extra
unbounded witness count, four-site rank or same-field mixing input.

For near bars use the intrinsic midpoint x and ordered unit direction
u from birth M to death S, as in Section 5. Give each the marks

    (p,a=ell/t,b=F(M),k=ell/dist(M,S)^3,x,u).

The unique short geodesic makes these jointly Borel. Bars outside
the near band may be omitted from this marked process; their expected
number on a<=T is O(t), so their probability of affecting any finite
window tends to zero also in the independent-copy limit below.
If desired they can receive a cemetery geometry mark with the same
vanishing effect. There is no need to choose a global geodesic at
cut-locus pairs.

The first-moment contact passage with a bounded continuous test of
these marks, using (20),(22),(24), gives the limiting one-copy mean
measure after division by t^(2/3):

    d eta_p=4 a^(-1/3) k^(-2/3) Z_(p,0)(b,k,x,u)
               da db dk dvol_g(x)d sigma_x(u),   a,k>0.           (31)

It is finite on the COMPLETE mark windows 0<a<=T, not just compact
b,k restrictions; (22) supplies this tightness. Its total mass there
is (3/2)V C_p T^(2/3); its lifetime marginal is
V C_p a^(-1/3) da. There is no atom at a=0. One may add that endpoint
to the mark space with zero mass. Curvature and nonstationarity
remain in the actual Z kernel and x integral; they have not been
removed by translation invariance.

For n independent whole copies of THIS ONE fixed F, choose t_n->0
with n t_n^(2/3)->lambda in (0,infinity), and superpose their marked
short-bar measures. For a nonnegative bounded continuous process test
f supported in a finite scaled-lifetime window, write Xi_t for the
single-copy measure and h=1-exp(-f). On a field with at most one
relevant point,

    1-exp(-<f,Xi_t>)=<h,Xi_t>.

In general their difference in absolute value is at most
N_(Tt)^all 1{N_(Tt)^all>=2}, plus the negligible far count if those
bars are omitted. Equations (30)-(31) give

    E[1-exp(-<f,Xi_t>)]
       =t^(2/3) sum_p integral (1-exp(-f)) d eta_p+o(t^(2/3)).

Independence then yields the Laplace limit

    E exp(-<f,sum_{i=1}^n Xi_(t_n)^i>)
      -> exp[-lambda sum_p integral (1-exp(-f)) d eta_p].          (32)

This is the Poisson random measure with intensity
lambda sum_p delta_p tensor eta_p on the marked space. The usual
Laplace-functional characterization on its locally compact separable
mark space gives convergence in law; (22) also controls the complete
finite-lifetime windows including a=0 and unbounded b,k. Limiting
degree populations are independent Poisson restrictions. The actual
degree populations within one finite field need not be independent.
The convergence is for independent whole copies, with fixed geometry
and fixed Gaussian component, not expanding volume, same-field spatial
Poisson, or factorial-moment convergence.

## 13. Evidence, imports and remaining boundaries

All five interfaces COUNT_p, CONTACT_p, SELECT_p, ENVELOPE_p and FAR_p
have been derived for (4), under the exact deterministic topology
imports stated in Section 2. The only probabilistic moments required
of W in the proof are polynomial moments of its actual global smooth
norms. Literal kernel normalization is used for definition and
fixed-target interpretation; all estimates and limiting passages
use unnormalized likelihoods on the original product space.

Classical mathematical imports remaining are finite-dimensional
Gaussian regression/uniqueness, smooth finite-dimensional Sard and
smooth incidence counting via local inverses and ordinary change
of variables, Taylor/implicit-function calculus and short-geodesic
coordinates, the named Morse handle/relative-incidence and finite
persistence package in HF, Tonelli, Minkowski/Holder, dominated
convergence, and the elementary Laplace characterization of a Poisson
random measure. GAD and HF state and derive their precise uses;
no new infinite-dimensional transversality or Kac-Rice theorem is
silently imported. The full copies and read extents are recorded in
INPUT_MANIFEST.json. No new full primary-book reading is claimed.

The new exact finite controls check Bayes weighting, shifted conditional
means, the target coercivity/tail split, exponent integrability, the
nonGaussian third cumulant, constant-shift invariance, cone-symmetry
refusal, antipodal averaging and radial/Poisson coefficient factors.
These finite algebra controls support the proof; they are not an
infinite-field sample, numerical integral, asymptotic experiment or
independent mathematical review. No old controls are rerun.

This author unit does not qualify any numerical sampler, grid, empirical
50-model trial, coefficient enclosure, Lean theorem, same-field Poisson
or all-order factorial result. It does not remove higher-singularity,
degenerate-noise, or arbitrary-law boundaries. No source branch, Drive
record, external message or scientific-status register is changed.
The larger research objective remains ACTIVE / UNMET. A separate
exact-source nonauthor review is still required for this proposal.
