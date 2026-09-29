# Inverse separation of remote critical-point pairs: the missing moment boundary

Object: OA-REMOTE-INVERSE-SEPARATION-20260928-v1.
Author: OpenAI / ChatGPT. Disposition: AUTHOR-SIDE CANDIDATE; nonauthor analytic review required.
Scientific effect NONE. No existing source, review verdict or status register is changed.

## 1. Objects, conventions, and conclusions

Use the exact periodized field and full pair-pinned law of RM and RC in
SOURCE_MAP.json. Fix d>=2, torus side L, remote exclusion rho>0, compact real birth
marks b and compact positive gap marks k with k_->0. The endpoints are
M=-(r/2)u, S=(r/2)u, pinned to heights b,b-k r^3 with zero gradients. Q_r is the
original Gaussian conditional law. Keep W_r=F_d(H_M)F_(d-1)(H_S), Z_r=E_Qr W_r,
and Q_r^W=(W_r/Z_r)Q_r exactly. Here F_j is the absolute determinant on index j
(counting negative eigenvalues), zero at singular matrices. No additional
normalizer or adjacency event is inserted.

Let E be a FIXED deterministic positive-volume Borel subset of D_rho. Count all
indices of critical points in E with heights in I_r=(b-k r^3,b). All pairs below
are ordered and distinct. Let

    M_p(r)=E_Qr^W sum_{x!=x' counted in E} dist(x,x')^p, p real.       (I1)

The expectation is allowed to be infinite even though the random field has
finitely many Morse critical points almost surely. Distances are physical torus
distances. At p=0, M_0 is the second factorial moment. We always distinguish a
normalized EXPECTED PAIR MEASURE from sampling a pair after conditioning a
realized field on having two or more points.

RP proves M_0(r)~r^5 A_0 and its blown-up pair-density limit. The separate RD
manuscript addresses p>=0 only. This note fills the negative-moment boundary
without importing RD's p=1 transition or its large-separation tail claims.

**Theorem I (extended microscopic moments).** For every fixed -2<p<1,

    M_p(r)=r^(5+p) A_p+o(r^(5+p)),                              (I2)

where A_p is the positive finite contact integral in Section 2. Convergence is
uniform on the fixed compact mark/frame sets for this fixed E. There is no rate
for the little-o and no uniformity over arbitrary oscillating sets E_r.

**Theorem II (fixed-r collision and sharp inverse threshold).** For every fixed
sufficiently small r>0 there is J_r in (0,infinity) such that the expected pair
separation measure, in a neighborhood of distance zero, has a density j_r with

    j_r(delta)=delta[J_r+o(1)], delta down to zero.                (I3)

Consequently, for this fixed r, M_p(r) is finite exactly when p>-2. In particular,

    E_Qr^W sum dist(x,x')^(-q) < infinity iff q<2, q>=0.           (I4)

At any fixed small delta_0>0, let I_q(r;epsilon,delta_0) restrict that inverse
sum to epsilon<dist<=delta_0. As epsilon down to zero, at FIXED r,

    q=2: I_2 ~ J_r log(delta_0/epsilon);
    q>2: I_q ~ [J_r/(q-2)] epsilon^(2-q).                        (I5)

For p>=1, Theorem II asserts finiteness, not a new r-asymptotic. For unordered
pairs, divide j_r, J_r and all unnormalized pair moments by two.

**Theorem III (small scaled separation and compatible limits).** Under the
normalized expected ordered-pair measure, S_r=dist/r converges in probability
TV to a law S on (0,infinity). With J_0 defined in Section 5,

    J_r/r^3 -> J_0>0,
    g_S(s) ~ (J_0/A_0)s as s down to zero,
    P(S<=epsilon) ~ [J_0/(2A_0)]epsilon^2.                      (I6)

For 0<q<2,

    E[S_r^(-q)] -> E[S^(-q)]=A_(-q)/A_0<infinity,               (I7)

whereas both expectations are infinite for q>=2. The assertions in (I3),(I5)
are fixed-r limits, and the first assertion of (I6) is a subsequent r limit.
No arbitrary joint cutoff epsilon(r) follows just from these iterated limits.

These are local-separation facts within the SAME FIXED REMOTE region. They do
not extend rho to zero, change d or L with r, permit random field-selected E,
identify persistence partners, or give an event-conditioned pair law. They also
do not imply that same-index pairs have the same inverse threshold; the all-index
sum is essential for the positive leading diagonal coefficient used here.

## 2. Negative moments of the blown-up pair measure

Use RP's contact law Q_0=Law(f|U_0=v_0), with endpoint contact weight w_0 and
normalizer z_0=E_Q0 w_0>0. At remote x and unit direction e, set

    Y=(grad f(x),H_x e,f(x)), T=D^3f(x)[e,e,e],
    A=H_x restricted to e-perp.

All correlations of these variables with the endpoint contact Hessian remain
inside the same conditional expectation. Ordinary, not probability-normalized,
sphere area is denoted de. Define, for -2<p<1,

    A_p = 3*12^((p+2)/3)*k^((p+5)/3) / [4(p+2)(p+5)z_0]
        * integral_E dx integral_S de p_(Y|Q0)(0,0,b)
          E_Q0[w_0 |T|^((4-p)/3)(det A)^2 |Y=(0,0,b)].         (I8)

There is no inverse T singularity in this range: (4-p)/3>1. The contact covariance
floor, moment bounds, and full conditional support from RP make A_p finite,
continuous, and positive. At p=0 this is exactly the all-index coefficient A_0.
The formula does not assert a pure k power law: Q_0 and the integrand also depend
on k through the endpoint target f_xxx(0)=12k.

RP's exact coordinates x'=x+delta e, delta=r s, y=b-r^3 z and

    t=(y'-y)/delta^3

give the window region

    0<z<k, (z-k)/s^3<t<z/s^3.                                (I9)

After extracting r^5, the nonnegative pair-density integrand is dominated by
C s(1+|t|)^(-m) times this indicator, with m sufficiently large. Integrating z,t
gives C s min(1,s^-3). To insert dist^p, multiply by r^p s^p. The new envelope is

    C s^(p+1) for s<=1; C s^(p-2) for s>=1.                   (I10)

It is integrable precisely for -2<p<1. Thus RP's coupled determinant convergence
and dominated-convergence proof applies, including unbounded weights at s=0.
The fixed-Borel spatial indicators 1_E(x)1_E(x+rse) are handled as in RP: truncate
s,t to compact ranges, use L1 continuity of torus translations, then remove the
tails using (I10). One cannot infer this step from pointwise convergence at every
point of an arbitrary Borel boundary.

Integrating z gives the overlap (k-s^3|t|)_+. For t!=0 and p>-2, elementary
integration up to s=(k/|t|)^(1/3) gives

    integral_0^infinity s^(p+1)(k-s^3|t|)_+ ds
      = 3 k^((p+5)/3)|t|^(-(p+2)/3)/[(p+2)(p+5)].             (I11)

RP's limiting determinant product is 36t^2(det A)^2. Integrate the density of
t=-T/12 and use

    108*12^(-(4-p)/3)=(3/4)*12^((p+2)/3).

This yields exactly (I8). The exceptional t=0 is a null target; Tonelli with
|t|>eta and then eta down to zero avoids assigning a value to an undefined
zero-times-infinity expression. For delta>=eta_0>0, RC's separated bound is
O(r^6); the distance weight is bounded there even for negative p. After division
by r^(5+p) it is O(r^(1-p)) and vanishes. This proves (I2). The endpoint p=-2
cannot be decided from failure of this upper envelope alone; the next section
provides the positive lower asymptotic that resolves it.

## 3. A different collision frame when r is held fixed

Fix 0<r<=r_1, with r_1 small enough that the pins lie strictly inside the excluded
remote ball. For 0<delta<eta_0<rho/2 use the GRADIENT-ONLY pair frame

    G_delta=(grad f(x),[grad f(x+delta e)-grad f(x)]/delta),
    G_0=(grad f(x),H_x e).                                    (I12)

Its transformation from the original pair gradients has absolute determinant
Delta=delta^(-d). There is NO delta^(-3) height-coordinate Jacobian here: the
height window is retained as a field mark and no divided height observation is
included. Reusing the joint value-gradient frame's delta^(-d-3) would be wrong.

For this fixed r, the joint vector (original endpoint pins,G_delta) has a positive
covariance floor uniformly over remote x,e and small delta including delta=0.
To justify contact rank, H->H e is onto in symmetric matrices, and gradient and
Hessian evaluations at x are independent linear functionals modulo the original
value/gradient evaluations at M,S. Positive spectral weights imply that a
zero-variance linear combination annihilates every Fourier mode. As a finite
sum of derivatives of delta distributions at the three distinct sites, it is
then the zero distribution; localized smooth test functions with prescribed
jets force each coefficient to vanish. Compactness gives the fixed-r floor.
Local orthonormal charts suffice for the transverse matrix A; no global sphere
frame or arbitrary-rotation invariance is assumed.

On one unconditioned smooth Gaussian field, use the usual finite-dimensional
regression formula for these observations with the exact original targets and
G_delta=0. Integral derivative representations of the divided gradient row give
covariance convergence as delta->0; the bounded inverse and rapid Fourier
summability give convergence of the conditional fields in every fixed
L^a(C^b), with uniform moments over remote x,e. Constants in this section may
depend on this fixed r. The original pin constraints are exact throughout.

The exact gradient-pair identity and C4 Taylor remainder yield

    H_x e/delta -> -D^3 f(x)[e,e,.]/2,
    H_(x+delta e)e/delta -> +D^3 f(x)[e,e,.]/2.                  (I13)

Positive congruence by diag(delta^-1/2,I) gives the two limits diag(-T/2,A) and
diag(T/2,A). Taking absolute determinants, which are continuous even on singular
matrices and have polynomial Lipschitz bounds, gives the coupled L^a limit

    |det H_x det H_(x+delta e)|/delta^2
           -> (T^2/4)(det A)^2.                               (I14)

The endpoint weight W_r is also a product of continuous index-filtered
determinants; its change under this coupling converges with polynomial moment
control. The original denominator Z_r>0 is independent of delta and remains
unchanged. For an a priori dominating bound, the zero-gradient segment identity
gives |det H_x det H_(x+delta e)|<=C delta^2(1+||f||_C3)^(2d).

The product of height indicators tends to the SINGLE indicator
1{f(x) in I_r}. To justify this despite its discontinuity, append f(x) to G_0.
Its conditional variance is positive by the same distinct-jet rank argument,
so the endpoints of I_r have zero conditional probability. Uniform convergence
also follows by bounding the probability of being within eta of either endpoint
using the uniformly bounded conditional height density, then letting eta->0.
Moment bounds and Holder control products with the determinant weights. This
argument keeps the unconditioned-in-height frame (I12); the shrinking width is
fixed and positive during this delta limit.

## 4. Positive fixed-r diagonal coefficient and inverse divergence

Let K_r(x,x') be the all-index, height-window pair intensity under Q_r^W, so the
marked Kac-Rice identity reads

    E_Qr^W sum F(x,x') = integral F(x,x')K_r(x,x') dx dx'

on distinct remote pairs for nonnegative Borel F. This is the Gaussian formula
under Q_r weighted ONCE by W_r and divided ONCE by Z_r. Exhaustion away from the
diagonal and monotone convergence allow infinite nonnegative integrals.
The continuous-field mark extension is the same interface used in RM/RC.

Equations (I12)-(I14) and the density change give, uniformly over remote x,e for
fixed r,

    delta^(d-2)K_r(x,x+delta e) -> c_r(x,e),
    c_r(x,e) = p_(G0|Qr)(0)/(4Z_r)
          * E_Qr[W_r T^2(det A)^2 1{f(x) in I_r}|G_0=0].       (I15)

The coefficient is finite and continuous. It is strictly positive: conditional
on G_0=0 and the original endpoint pins, the independent symmetric entries of
the two endpoint Hessians and the remote transverse Hessian A, together with
remote height and T, have full joint Gaussian support. This follows by adding
the remaining independent derivative evaluations to the distinct-site jet list.
The open event of a typed maximum/saddle at the pinned endpoints, remote height
strictly inside I_r, nonsingular A, and T nonzero has positive probability. The
integrand in (I15) is positive there. No independence between these blocks is
needed.

In polar coordinates the radial power is

    (d-1) from dx' - d from the gradient density
                         +2 from the determinants = 1.       (I16)

For delta below the injectivity scale, define the radial density explicitly by

    j_r(delta)=delta^(d-1) integral_E dx integral_S de
                   1_E(x+delta e) K_r(x,x+delta e).

The convergence in (I15) is uniform for fixed r. The bounded limit and
sup_{|h|<=delta}||1_E(.+h)-1_E||_1->0 remove the translated indicator, even for
an arbitrary fixed Borel E. Therefore (I3) holds with

    J_r=integral_E dx integral_S de c_r(x,e), 0<J_r<infinity.   (I17)

In particular, for each fixed r there is delta_r>0 such that
(J_r/2)delta<=j_r(delta)<=(3J_r/2)delta on (0,delta_r), and the ratio tends to
one after division by J_r delta. At larger distances, fixed-r remote pair
covariance and Gaussian moments are bounded on separated compact sets. Thus
M_p(r) is finite iff integral_0^delta_r delta^(p+1)d delta is finite, which is
precisely p>-2. This proves (I4), including its necessity, rather than merely a
sufficient condition from an upper bound.

To obtain the constants in (I5), fix eta>0 small so j_r(delta)/(J_r delta) lies
between 1-epsilon_1 and 1+epsilon_1 for delta<eta. Integrate the power on
(epsilon,eta); the contribution from (eta,delta_0) is finite and negligible
relative to the divergent expression. First send epsilon->0, then
 epsilon_1->0. For q=2 the antiderivative is log; for q>2 it is
(delta^(2-q))/(2-q). This proves the two asymptotic equivalents in (I5).
The fixed-r constants and cutoffs are existential, not numerically evaluated.

## 5. Matching the fixed-r coefficient to the contact coefficient

Disintegrating the remote height in (I15) gives a useful equivalent form:

    c_r(x,e)=1/(4Z_r) integral_(b-k r^3)^b dh
       p_(grad f(x),H_x e,f(x)|Qr)(0,0,h)
       E_Qr[W_r T^2(det A)^2|grad f(x)=H_xe=0,f(x)=h].         (I18)

Put h=b-k r^3 theta. The joint covariance of (U_r,grad f(x),H_xe,f(x)) has a
uniform floor through r=0: it is a subvector of RP's contact collision frame,
or follows directly from distinct derivative evaluations at 0 and remote x.
The same Gaussian regression coupling as RP and RM applies uniformly in
0<=theta<=1. Under these exact extra observations, original endpoint pin
identities give W_r/r^2 -> w_0 in every fixed L^a, and Z_r/r^2 -> z_0>0.
The remote A,T and the density also converge with bounded moments; no restricted
normalizer replaces Z_r. Dominated convergence in (I18) now yields, uniformly
on the fixed compact x,e,mark sets,

    c_r(x,e)/r^3 -> c_0(x,e)
       = k/(4z_0) p_(Y|Q0)(0,0,b)
          E_Q0[w_0 T^2(det A)^2|Y=(0,0,b)].                  (I19)

Integrating defines J_0=integral_E integral_S c_0 and proves J_r/r^3->J_0>0.
This is a simultaneous contact-kernel estimate for c_r, not a statement that
(I15)'s error is uniform for every joint pair (r,delta). Those are distinct
claims, and the latter is unnecessary here.

## 6. The limiting scaled law at zero and inverse-moment convergence

RP's L1 convergence of the blown-up density, followed by its measurable
pushforward s=dist/r, gives TV convergence of the normalized pair-weighted law
of S_r to S. Define

    Psi_E(t)=integral_E dx integral_S de p_(V0|Q0)(0,0,b,t)
        E_Q0[w_0(det A)^2|V_0=(grad f,H e,f,-T/12)=(0,0,b,t)].

This nonnegative function is bounded, continuous, and decays faster than any
fixed inverse polynomial after appropriate polynomial moment factors. Its
weighted integral against t^2 is positive. The all-index limiting density is

    g_S(s)=36s/(z_0 A_0) integral_R t^2(k-s^3|t|)_+Psi_E(t)dt. (I20)

At s->0, dominate the integrand by k t^2 Psi_E(t). Then

    lim g_S(s)/s = 36k/(z_0 A_0) integral t^2 Psi_E(t)dt
                 = J_0/A_0,                                (I21)

because T=-12t converts 36t^2 to T^2/4. Integrating the positive density near
zero proves the small-separation cumulative statement in (I6). Its inverse
q-moment is finite near zero iff q<2; for q>=0 there is no inverse-moment
obstruction at infinity, since s^-q<=1 for s>=1. This proves the limiting-law
threshold, without using RD's upper-tail exponent.

For 0<q<2, apply (I2) at p=-q and at p=0:

    E[S_r^(-q)] = r^q M_(-q)(r)/M_0(r) -> A_(-q)/A_0.

The same weighted dominated-convergence argument computes E[S^(-q)] from
(I20), giving that value. TV convergence alone would not justify this step for
an unbounded inverse-distance observable. At q>=2, Section 4 proves the finite-r
expectation is already infinite, and (I21) proves the limit expectation is
infinite as well. All statements are about pair-weighted means, not probabilities
of the existence of a very close pair or a persistence-lifetime law.

## 7. Scope and review obligations

The positive diagonal coefficient, not a finite numerical fit, makes the inverse
threshold sharp. The two different collision frames must not be mixed: the
height-divided frame supplies RP's r-blow-up; the gradient-only frame supplies
the fixed-r diagonal with Jacobian delta^-d. Local curvature and polar volume
cancel the dimension in (I16). This does not assert isotropy of the torus field.

All claimed new limits keep E fixed and remote. Fixed-r divergence, normalized
contact inverse moments, and an arbitrary coupled cutoff epsilon(r) are three
different assertions; only the first two are proved here. No rate for remainders,
leading event-probability constant, same-index inverse threshold, p>=1
r-asymptotic, global pin-neighborhood bound or scientific-status promotion is
provided. RP's new coefficient/height law has an actual Anthropic discussion
review; its source remains on the original branch at author publication time.

The finite runner checks powers, moment domains, cutoff integrals, determinant
and height signs on explicit polynomial fields, and coefficients. It cannot
certify Gaussian support, uniform regression, Kac-Rice applicability, or the
Borel translation argument. Those displayed analytic steps require a new
source-bound nonauthor review. No unavailable author runner is reconstructed.
