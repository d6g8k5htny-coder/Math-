# Orthogonal spectral closure of the rare window-count law

Object: OA-SPECTRAL-CLUSTER-CLOSURE-20260929-v1.
Author: OpenAI / GPT-6 Astra Pro, 29 September 2026.
Disposition: AUTHOR-SIDE CONDITIONAL PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED.
Scientific effect NONE: no existing proof, acceptance record, global register,
Boolean or prize is changed. Shared GitHub identity is not organizational
independence. All new analytic steps below require their own review.

## 1. Model, inputs, and the claimed closure

Fix d>=2, m=d-1, torus side L>0, birth b, gap mark k>0, and an orthonormal
axial/transverse frame. Use exactly [P]'s variance-one periodized Gaussian
covariance, original endpoint observations

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0,

and endpoint regression Q_r. Let W_r=F_d(H_M)F_(d-1)(H_S), Z_r=E_Q W_r and
Q_r^W=(W_r/Z_r)Q_r. N_r counts ALL additional critical points with heights in
(b-k r^3,b), excluding the two pins. Constants below depend on these fixed
parameters, d, and L; where stated they also depend on R or rho. No uniformity
in varying dimension, volume, or unbounded/vanishing marks is claimed.

Exact source commits, paths, sizes and hashes are in SOURCES.json. The inputs are:

[P] parent Sections2-5: positive Fourier spectrum, nonsingular contact frame U_r,
its target v_r, smooth finite-jet regression, every fixed C^q moment, and
Z_r/r^2 -> z0>0. The endpoint-gradient identity gives W_r/r^2 <= C K^(2d), where
K>=1 is a fixed multiple of 1+||f||C4 bounding operator derivatives through four.

[D5] the fixed-d global first moment and height-window shell estimate

    E_W N_r <= C r^3,
    E_W N({Rr<|x|<rho}) <= C r^3(R^-2+rho^2), R>=4.       (1)

[RM,RC] for fixed rho>0, on D_rho={|x|>=rho}, with Lambda the SUM of the
index-specific normalized contact kernels,

    E_W N(D_rho)=k r^3 integral_Drho Lambda+O_rho(r^4),
    E_W (N(D_rho))_2=O_rho(r^5).                          (2)

[C6] E_W (N_r)_q<=C_q r^3 for every fixed q>=2. With (1), Stirling's identity
also gives E_W N_r^q=O_q(r^3). We use this only for moment uniform integrability
and consequences, not for the new near-event domination or mixed-event estimate.

[CUB] the exact deterministic classifier in #158, Theorem C, at its xAI-reviewed
algebraic scope. Its Gaussian sector theorem is NOT consumed. [DEEP] is credited
for the planar exclusion construction; Section3 proves the vector version here.
[RCL] the previously reviewed generic Poisson/compound-Poisson consequences.
The defective global proof in #159 is NOT a premise. This note gives an alternative
spectral-coordinate proof, not a retrospective acceptance of its shear argument.

Theorem (conditional global cluster law). There are explicitly specified finite
positive numbers a1,a2,beta_far such that, putting

    nu1=a1+beta_far, nu2=a2,

for every fixed nonnegative integer q,

    sum_(n>=1) n^q |r^-3 Q_r^W(N_r=n)-nu1*1{n=1}-nu2*1{n=2}| -> 0.  (3)

The coefficients are (17) and (22) below. Thus the full limiting nonempty count
measure is unique and supported on {1,2}. This is not a joint law of clusters
from distinct pin pairs, and not a spatial independence statement. Unscaled
Law(N_r) tends to delta_0. The zero mass must be CENTERED before multiplying
by r^-3; r^-3 Q_r^W(N_r=0) diverges.

## 2. Physical jets, residual coupling, and exact orthogonal coordinates

Let A=D_y^2 f(0) be the m-by-m midpoint transverse Hessian and T the list of
independent third derivatives at 0 EXCEPT f_xxx. Set J=(A,T). At contact,
(U_0,J) is the complete nonrepeated jet list through degree three: U_0 supplies
f, all first derivatives, f_xx, f_xyi, and f_xxx. Positive Fourier spectrum
therefore gives a positive-definite covariance. For sufficiently small r, the
joint covariance and its inverse are uniformly bounded. The conditional density
h_r(A,T) under Q_r converges locally uniformly to h_0 and obeys

    h_r(A,T)<=C exp[-c(||A||F^2+|T|^2)].                   (4)

The bounded conditional means have been absorbed by reducing c.

Take an independent copy F of the unconditioned smooth field. For each raw target
j, construct the conditional field by regression on V_r=(U_r,J):

    f_r^j=F+Cov(F,V_r)Cov(V_r)^-1((v_r,j)-V_r(F)).         (5)

All coefficient functions are bounded in C4 and converge there. Averaged contact
functionals in U_r are bounded by a constant times ||F||C3; this uses the integral
forms of the pin divided differences, not separate uncontrolled r^-p terms.
Consequently, with S=C(1+||F||C4), independent of the target j,

    K(f_r^j)<=C(S+|j|),       E S^p<infinity for every p.  (6)

The same random F can be used at all small r; no independence of the field's
internal derivatives is asserted. Disintegrating first over j and then F gives
exactly Q_r. Formula (6) is a pathwise bound under this construction.

Diagonalize -A with ORDERED eigenvalues lambda1<...<lambdam. Repeated eigenvalues
are a Lebesgue-null set. Write

    lambda1=-r s, h=(h2,...,hm)=(lambda2,...,lambdam),
    A=O diag(r s,-h2,...,-hm) O^t, O in O(m).              (7)

Rotate the complete tensor T by diag(1,O), calling its coordinates tau. This
linear tensor representation has absolute determinant one: its determinant in
absolute value is a continuous homomorphism from a compact group to the positive
reals, whose only compact subgroup is {1}. The joint coordinate Jacobian is
block triangular, so the dependence of the tensor rotation on O does not add a
factor. The field covariance is NOT assumed orthogonally invariant. The density
h_r(A,T) is always evaluated at the actual rotated raw arguments.

Specify the spectral constant without any convention ambiguity. With raw
independent upper-triangular Lebesgue coordinates dA and normalized Haar dO,

    integral g(A)dA
      = c_m integral_(l1<...<lm) integral_O(m)
           g(O diag(l)O^t) product_(i<j)(lj-li) dO dl.

The positive constant c_m is fixed exactly by

    c_m = (2*pi)^(m/2) * pi^[m(m-1)/4] / H_m,
    H_m = integral_(l1<...<lm) exp(-sum li^2/2)
                                      product_(i<j)(lj-li) dl.   (8)

This also is an explicit finite integral definition; c_1=1. To prove the change
of variables, differentiate O diag(l) O^t: the off-diagonal infinitesimal in
an ij rotation is (lj-li) times the rotation increment. Their product is the
Vandermonde; invariance of matrix Lebesgue measure leaves normalized Haar times
a constant. The Gaussian test integral fixes the constant as (8). This is a
Lebesgue-coordinate identity, not a GOE assertion about h_r.

After lambda1=-r s, the spectral Jacobian is r c_m J_r, where

    J_r=product_(j=2..m)(h_j+r s) product_(2<=i<j<=m)(h_j-h_i),
    domain: -r s<h2<...<hm.                              (9)

For m=1, h is absent, every product is 1, and there is no ordering constraint.
Haar sign choices are retained; invariant observables are unchanged by the
corresponding reflection of tau and of the soft coordinate. No arbitrary global
choice of an eigenvector is needed.

Put U=1+S+|h|+|tau|. Orthogonality gives, uniformly in O,

    K<=C(U+r|s|),
    h_r(A,T)<=C exp[-c(|h|^2+|tau|^2)].                  (10)

Unlike an unbounded shear, these coordinates genuinely preserve norm equivalence
with constants depending only on the fixed dimension.

## 3. Vector transverse exclusion, and the absorption dichotomy

Use the cylinder |x|<=Rr, |y|<=Rr, R>=1, and let K bound the operator norms of
all derivatives through four. Let lambda=lambda_min(-A). If

    rK<=k/(4R), lambda>(8RK+56RK^2/k)r,                  (11)

there are only the two pinned critical points in the cylinder.

Proof. Throughout the cylinder f_yy<=-lambda/2, since its variation from A is at
most 2RKr. Put g(x)=f_y(x,0). The pin gradients give g(-r/2)=g(r/2)=0. Applying
the scalar two-node interpolation estimate to every unit projection of g gives
||g(x)||<=KR^2r^2, also outside the pin interval. No vector-valued Rolle zero is
assumed. Likewise

    g'(x)=r^-1 integral_(-r/2)^(r/2)[g'(x)-g'(t)]dt

implies ||g'(x)||<=K(R+1/2)r. For rho=4R^2Kr^2/lambda<Rr/2, the radial derivative
f_y(x,y).y is negative on |y|=rho, because it is at most
KR^2r^2 rho-(lambda/2)rho^2. The strictly concave transverse function attains its
maximum inside that ball. Its unique critical point zeta(x) depends C3-smoothly
on x. Strong concavity gives uniqueness throughout |y|<=Rr.

On the graph, ||f_xy||<=2RKr and ||zeta'||<=4RKr/lambda<1/2. For
psi(x)=f(x,zeta(x)), differentiating f_y=0 gives

    psi'''=f_xxx+3 f_xxy[zeta']+3 f_xyy[zeta',zeta']
                                      +f_yyy[zeta',zeta',zeta'].

The terms containing zeta'' cancel because f_xy+f_yy zeta'=0. Thus
|psi'''-f_xxx|<=28RK^2r/lambda<k/2. The exact two values and two axial-gradient
pins imply f_xxx(eta,0)=12k for some eta between the pins, by Hermite interpolation
and generalized Rolle. Hence |f_xxx(x,zeta)-12k|<=2RKr<=k/2, so psi'''>=11k>0.
The strictly convex function psi' already has the two pinned zeros and cannot
have a third. All critical points in the cylinder lie on its graph. This proves
(11) in every fixed dimension.

On the typed support H_M<0, A has largest eigenvalue less than rK/2 by the
Hessian Lipschitz bound, so s<K/2. If N_R, the window count in |x|<=Rr, is positive,
(11) implies, outside the event rK>k/(4R),

    |s|<=C_R K^2<=a_R U^2+a_R r^2 |s|^2, a_R>=1.         (12)

Here K>=1, k is fixed, and (10) was used. The elementary absorption dichotomy is

    x<=a U^2+a r^2 x^2  implies
    x<=2a U^2  OR  x>=1/(2a r^2), x>=0.                 (13)

If x>2aU^2, subtracting aU^2 from (12) proves the second alternative.
On the second alternative |A|op>=r|s|>=c_R/r, hence K>=c_R/r. The first excluded
event also implies K>=c_R/r. All exceptional mass can therefore be bounded in
ORIGINAL Q_r coordinates, before any spectral rescaling. For every p,M>=0,

    E_W[K^p;exceptional] <= C E_Q[K^(p+2d);K>=c_R/r]
                         <= C_(p,M,R) r^M.              (14)

The last bound uses one higher fixed Q_r moment. The normalizer is the full
Z_r>=z_*r^2 and W_r<=Cr^2K^(2d). There is no need to posit a conditional Gaussian
tail that is uniform in an unbounded scaled target. The exceptional branch has
not been discarded; it is negligible to every fixed power of r.

## 4. One global majorant, including multiple soft eigenvalues

At each pin the axial Hessian column has norm <=rK/2 by the vector gradient
average. The TRANSVERSE part of the midpoint column in the soft eigenvector direction is
r s times that eigenvector; its endpoint transverse perturbation is bounded by
rK/2. Its axial entry at a pin is already bounded by the short axial column.
Thus the full soft column is bounded by r(|s|+K), up to a fixed harmless constant.
The axial and soft columns correspond to orthogonal coordinate directions. Hadamard therefore gives

    W_r/r^4 <= C K^(2d-2)(|s|+K)^2.                     (15)

This does not divide by any hard eigenvalue. On the regular near-occurrence
branch |s|<=2a_R U^2, (10) gives K<=C_R U^2 (r<=1), so (15)<=C_R U^(4d).
Writing v=m(m-1)/2, (9) gives |J_r|<=C_R U^(2v). Thus the density of the rescaled
NONEMPTY near measure, in spectral variables and the coupling variable F, is
bounded by

    G_R=C_R exp[-c(|h|^2+|tau|^2)]
                  U^(4d+2v) 1{|s|<=2a_R U^2}.          (16)

Indeed disintegration gives r^-3 times r from (9), times r^4 from the weight,
divided by Z_r: the prefactor is c_m r^2/Z_r, which is bounded. Integrating s in
(16) contributes only another U^2. Gaussian h,tau integration and every fixed
moment of S make G_R integrable. Multiplication by any fixed polynomial in
K, |s|, |h|, |tau| remains integrable on the regular branch. Formula (14) controls
the weighted exceptional branch as well: for a scaled-jet power, use |s|<=K/r
and choose the arbitrarily large power M in (14) to absorb that extra r^-p.

Consequences: the r^-3 near-occurrence measures are tight in all the spectral
jet variables; their tails outside increasing compact sets tend to zero uniformly
as r->0. Their occurrence-weighted K moments are O(r^3). If m>=2, the limsup of
scaled near-occurrence mass with |h2|<=eta tends to zero as eta->0, directly by
integrating G_R over that strip. The same holds near repeated hard spectra. No
inverse determinant or 1/eta bound appears. This proves the needed multiple-soft
exclusion IN MEASURE, without a pointwise assertion that two soft directions
cannot occur.

Using C6 only now, Cauchy-Schwarz also yields
E_W[N_R K^p]<=sqrt(E_W N_R^2)*sqrt(E_W[K^(2p);N_R>0])=O_(R,p)(r^3).
Thus the LOCAL derivative-weighted bound is established, not assumed. The global
analogue is not needed for the rest of this proof.

## 5. Pointwise normal form, typed-boundary control, and the near limit

Fix spectral variables s,h,O,tau with 0<h2<...<hm, and a realization of F with
finite C4 norm. In the orthonormal frame (axis, soft eigenvector, hard eigenvectors),
write coordinates (x,z,w). Conditional targets are exactly
A=diag(rs,-h) and the prescribed cubic tensor tau. With x=rX,z=rZ,w=r^2V, the pin
Taylor identities from [P] give, on each fixed bounded (X,Z,V) set,

    [f(rX,rZ,0)-b]/r^3 -> P_s,tau(X,Z) in C2,
    r^-2 grad_w f(rX,rZ,r^2V) -> -diag(h)V+Q_tau(X,Z) in C1,

where

    P_s,tau=2kX^3-3kX/2-k/2+sZ^2/2
             +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(c/6)Z^3,
    a=tau_xxz, beta=tau_xzz, c=tau_zzz.

Q_tau contains the hard-index cubic terms. For fixed positive h the hard
Hessian stays negative definite for small r. On the full physical Rr ball,
grad_w f=-diag(h)w+O(Kr^2)+O(Kr|w|). Every critical point therefore has
|w|<=C_(h,R,F,tau) r^2. The hard implicit function is unique and smooth, and
substitution into f/r^3 changes the planar potential by O(r) in C2 on fixed
sets. Its inverse-hard-eigenvalue constants are used ONLY for pointwise
convergence, never in (16).

At the endpoints the soft Hessian blocks divided by r converge to

    M_M=[[-6k,-a/2],[-a/2,s-beta/2]],
    M_S=[[ 6k, a/2],[ a/2,s+beta/2]].

A Schur complement across the fixed hard block, or the determinant expansion,
gives W_r/r^4 -> product h_j^2 * w(s,a,beta), where

    w=[-6k(s-beta/2)-a^2/4]_+ [a^2/4-6k(s+beta/2)]_+.

It is positive exactly on s<-|B|/2, B=beta-a^2/(12k), and equals
9k^2(4s^2-B^2) there. Outside this open typed domain its limiting value is zero;
on the typed boundary the determinant limit is also zero. Consequently no count
convergence is needed at a point with zero limiting weight. This is the explicit
handling of the typed boundary, not an assumed compact exclusion from it.

Within the typed domain use [CUB]'s exact classifier n(s,a,beta,c) in {0,1,2}.
Let n_R count those additional cubic critical points in X^2+Z^2<R^2 and the
strict height window. For almost every jet, all relevant roots are nondegenerate,
none has boundary height, and none lies on the observation circle. The last null
set can be checked without an informal resultant assertion: on a circle R>=1,
Z!=0 at any critical root, and the two gradient equations solve for (beta,s)
as smooth functions of (X,Z,a,c). A circle coordinate plus a,c is three parameters,
so its image in four-dimensional (s,a,beta,c) space is null. Cover by countably
many compact charts with |Z| bounded away from zero. Height boundary relations
are the nonzero polynomial threshold of [CUB]. The pins are nondegenerate and
remain EXACT, so they cannot split into new counted roots.

Choose disjoint neighborhoods of relevant zeros. C2 convergence and the inverse
function theorem preserve precisely one root in each; on the rest of the compact
set in a slightly enlarged height window the gradient is bounded away from zero.
No condition on lower-height degeneracies is necessary. Hard slaving then proves
N_R -> n_R pointwise for these fixed variables. The hard coordinates vanish on
the r spatial scale. The extra points have full index d-1.

For precision, extend the coefficient kernel by zero off ordered positive h and
the typed domain. With T=Rot_O(tau), define

    dM(s,h,O,tau) = (c_m/z0) h_0(O diag(0,-h)O^t,T)
             * product_(j=2..m) h_j^3
             * product_(2<=i<j<=m)(h_j-h_i)
             * w(s,a,beta) ds dh dO dtau.                (17)

Every angular variable remains inside this integral. On each fixed R, the
nonempty joint spectral-jet/count measure converges in full variation to
1{n_R=j}dM on j>=1. To see this, on the regular branch sum the absolute conditional
errors over the count index j: it is bounded by the weight error plus twice
the weighted probability of a count mismatch. Pointwise convergence gives zero
and (16) dominates. Cases of zero limiting weight give zero directly. On a fixed typed jet with n_R>0 and finite S, K is bounded as r->0, so the
exceptional branch is eventually absent and the regular-branch indicator is
eventually one. No part of the proposed limit is lost by that split. The
exceptional mass is o(r^3) by (14). This proves

    r^-3 Q_W(N_R=j) -> a_j^R=integral 1{n_R=j}dM, j=1,2,
    r^-3 Q_W(N_R>=3) -> 0.                               (18)

There is NO finite uncentered n=0 formula. For fixed R, the right side is a
finite measure only on nonempty counts.

## 6. Integrability at arbitrary scaled radius

For the planar classifier put D=(c-a beta/(4k)+a^3/(72k^2))/2 and
T_*=-(s-B)^2(B+2s)/(12k). It says: s>B gives n=2 below D^2=T_* and n=1 at or above;
s<=B gives n=1 strictly above that threshold and n=0 otherwise. On n>=1, x=-s>0
satisfies

    x<=2|B|+(48kD^2)^(1/3).

Indeed s>B forces x<|B|. Otherwise D^2>T_*, and if x>=2|B| then
T_*>=(x/2)^2*x/(12k)=x^3/(48k). Since w<=36k^2 x^2,

    integral_s w 1{n>=1} <=384k^2 |B|^3+2304k^3 D^2.      (19)

This is a polynomial bound in the cubic coordinates at fixed k. The remaining
factor in (17) is a nonnegative polynomial in h times a uniformly Gaussian-decaying
function of h,tau, by ORTHOGONAL norm preservation. Therefore

    a_j=integral 1{n=j}dM, j=1,2                         (20)

are finite. They are strictly positive: take the open two-point cubic sector
(s,a,beta,c)=(-3k/2,0,-2k,0), or the one-point sector (-k,0,0,2k), choose distinct
positive hard h in a compact box, and arbitrary remaining cubic entries in a
small box. Gaussian densities are positive, and the spectral/weight factors are
positive on an open set. For m=1 the empty hard products are 1.

For every fixed jet, n_R=n eventually as R->infinity. Exact-count indicators
{n_R=1} need NOT be monotone, but are bounded by 1{n>=1}; (19) supplies an
integrable majorant. Dominated convergence proves a_j^R->a_j. No inverse shear
parameter is suppressed by integrating out variables that a spatial observable
still uses.

## 7. Remote singleton coefficient and vanishing mixed event

By (1) and [RM]'s fixed-remote mean limit, for 0<rho'<rho<=s0,

    k integral_(rho'<=|x|<rho) Lambda(x) dx <= C rho^2.    (21)

Apply the shell estimate with lower scale rho' held fixed as r->0; equivalently
choose R_r=rho'/r, which is permitted because the shell constant is uniform in
R_r>=4. The kernel is nonnegative and the annulus is fixed, so its mean limit
is supplied by [RM]. Thus

    beta_far=k integral_(X\{0}) Lambda(x)dx              (22)

exists, is finite, and differs from the fixed-rho integral by O(rho^2).
It is positive by positivity on any fixed remote region of positive volume.
Corollary D of [RC] and the mean limit give
r^-3 Q_W(N_far^rho=1)->k integral_Drho Lambda and
Q_W(N_far^rho>=2)=O_rho(r^5).

Fix R and rho. To control the mixed event, first restrict the spectral jets
(s,h,tau) to a fixed compact box H, retaining all O. Under the conditional law
(5) with these targets, the covariance of (f(x),grad f(x)), |x|>=rho, has a
uniform positive lower bound. At r=0 the conditioning is the COMPLETE degree-three
jet at the origin and x is a distinct site; positive Fourier spectrum gives
full joint rank. Compactness in x, O, and the target-independent covariance,
plus continuity through r=0, proves the bound. Conditional Hessian moments are
bounded on H and on the height window. The usual unweighted Gaussian Kac-Rice
formula, integrated over the window of length k r^3, gives

    E[N_far^rho | U_r,J]<=C_(H,rho) r^3.                 (23)

On H, (15) and (6) give a uniform second moment of W_r/r^4. Conditional
Cauchy-Schwarz therefore gives

    E[(W_r/r^4)1{N_far^rho>0} | U_r,J]<=C_(H,rho) r^(3/2).

Disintegrating over H with (9), the full normalizer, and bounded density and
Vandermonde gives Q_W(spectral jets in H,N_far^rho>0)=O_(H,rho)(r^(9/2)).
In particular this bounds the compact-jet near/far intersection.
Outside H, its probability is bounded by Q_W(N_R>0,jets outside H). By (16)
and (14), its scaled limsup tends to zero as H exhausts the spectral variables.
Thus

    Q_W(N_R>0,N_far^rho>0)=o_(R,rho)(r^3).                (24)

The full mixed term has no asserted r^(9/2) rate: that rate was proved only on
a fixed compact jet box. This proof avoids conditioning on a near WITNESS whose
observation frame degenerates. It uses fixed-origin physical jets instead.

## 8. The full count limit and all polynomial weights

Write N=N_R+N_mid+N_far. For fixed R,rho, the bad events N_mid>0,
{N_R>0,N_far>0}, N_far>=2, and N_R>=3 have probabilities bounded by (1), (24),
(2), and (18), respectively. On their complement N equals either the near
count in {0,1,2} or a remote singleton, but not both. Therefore, with an absolute
constant C independent of R,rho,

    limsup |r^-3 Q(N=2)-a_2^R| <= C(R^-2+rho^2),
    limsup |r^-3 Q(N=1)-a_1^R-k integral_Drho Lambda| <= C(R^-2+rho^2),
    limsup r^-3 Q(N>=3) <= C(R^-2+rho^2).                 (25)

First r->0 at fixed R,rho, then R->infinity and rho->0, using (20)-(22).
This proves coordinate convergence to nu1=a1+beta_far and nu2=a2, and vanishing
scaled tail mass. For a fixed integer q>=0, C6 supplies E N^(q+1)<=C r^3; hence

    r^-3 E[N^q;N>M]<=C/M.

Finite-coordinate convergence plus this uniform tail proves (3). No interchange
of a nonuniform radius limit and r limit has been assumed. No finite unscaled
polynomial moment theorem alone would imply (3); the new domination and regional
sandwich are the essential ingredients.

In particular

    E N/r^3 -> nu1+2nu2,
    E (N)_2/r^3 -> 2nu2,
    E (N)_q/r^3 -> 0 for every fixed q>=3.                (26)

The positive-conditioned count converges in TV to
(nu1 delta1+nu2 delta2)/(nu1+nu2), and its size-biased version to
(nu1 delta1+2nu2 delta2)/(nu1+2nu2). The two laws are different. Their formulas
use the normalized full tilt, not a restricted normalizer.

For independent replicas with floor(t/r^3) counts, the identified compound limit
is P1+2P2, with independent P1~Pois(t nu1), P2~Pois(t nu2), as follows either by
the exact generating function or [RCL]'s proved independent-replica bound.
There is no independence claim for regions of a single field.

The sharp [RCL] Poisson comparison also now has coefficients:
optimal ordinary-Poisson TV error/r^3 -> nu2 and mean-matched error/r^3 ->2nu2,
so their ratio tends to 2 (not just liminf>=2). The canonical approximant using
the ACTUAL conditional mark law still has Theta(r^6) error. Replacing its mark
law by the identified LIMIT does not inherit that rate: without a convergence
rate for the coefficients, this replacement is only o(r^3) in one-count TV.

## 9. What is solved here, conditional on review, and what is not

The proof supplies a replacement for scaled jet tails, typed-boundary control,
nearly singular hard blocks, the near/far mixed event and the radius sandwich.
It works for every FIXED d>=2 via orthogonal spectral coordinates. It does not
require the stronger global derivative-weighted insertion estimate proposed in
#157; Section4 proves the local version as a consequence and the global law does
not need the global version. Thus that former sufficient route is bypassed, not
silently assumed true.

The local coefficients in d=2 reduce exactly to #158's alpha1,alpha2, and its
contact birth factorization remains a local statement. In higher dimensions the
Haar/stable integration may couple birth-dependent even jets to orientation;
no higher-dimensional or global birth cancellation is asserted.

No convergence rate, numerical coefficient enclosure, unbounded-mark theorem,
growing-volume limit, inter-pin-pair cluster independence, elder selection of the
extra points, or full Lean formalization is claimed. The input Gaussian and
regional sources remain conditional premises at their exact stated scopes.
Theorem (3) is a new author-side candidate, not accepted merely because finite
controls or existing formal gates pass.

Review division: A, vector exclusion, absorption, and orthogonal spectral measure;
B, integrable majorant, typed/hard-boundary handling and pointwise normal form;
C, compact-jet remote conditioning, mixed event, radius sandwich and consequences.
The prior #159 diagnosis and the distinction between that proof and this replacement
are retained in AUDIT_AND_REPAIR.md. Source preservation is mandatory.
