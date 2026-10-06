# LM006: conditional sign-band integration and a cubic saddle-sign bound

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, session `round18-cubic-sign-band-audit-20261006`.
Scientific effect NONE. This is an additive analytic companion, not a Lean
formalization, a replacement of a historical proof, or program acceptance.

## 1. Scope, exact predecessors, and what is additional

Use the six adjusted endpoint coordinates from #301 and the exact typed
weight from #315, with the conventions of #318/#325:

    v=(a_minus,a_plus,b_minus,b_plus,c_minus,c_plus),
    T_r(v)=[(a_minus)_- (c_minus)_- - r b_minus^2]_+
           [r b_plus^2-a_plus c_plus]_+,       0<=r<=1.       (1)

Here x_+=max(x,0), x_-=max(-x,0). For physical r>0, T_r=W_r/r^2.
Let E={c_plus>=0}; this is the SADDLE transverse sign, not the sign already
forced at the maximum. Write z_r=E_Qr T_r and nu_r(E)=E_Qr[T_r 1_E]/z_r.
Qr is the original Gaussian pin law; it has no additional good-event
conditioning. No pin density or coordinate Jacobian is inserted into z_r.

The #325 moment-only estimate is of order r e+e^4, hence O(r^2) when a
valid coupling error satisfies e=O(r). We add a CONDITIONAL density bound
for the scalar c_plus after all other endpoint coordinates are specified.
Integrating the actual sign interval yields order r e^2+e^5 and hence O(r^3).
Marginal density, full density at each positive r, and bounded covariance
alone do not imply the uniform conditional-density premise.

Prior-work credit is essential: P, `UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
sections 6–7, already uses two soft determinant factors and a boundary-layer
width to produce the cubic power, including its separate scalar case. This
note is not the first cubic soft-layer argument or a new generic Gaussian
regression method. It supplies the explicit one-dimensional endpoint-band
formula, a sufficient 11-observation confluent Gram proof using a finite tenth
spectral moment, and the source-matched consequence for this particular sign
event. P's global selection and lifetime theorems are NOT premises here.
Neither #329's weaker-regularity rate nor #333's application is rewritten.

## 2. Exact deterministic band and its Lebesgue integral

Put t=c_plus, g=c_plus-c_minus, so c_minus=t-g. Hold
h=(a_minus,a_plus,b_minus,b_plus,g) fixed. On E and positive typed weight,
necessarily a_minus<0 and 0<=t<g. In particular the weight vanishes on E
when g<=0. For all real h and r in [0,1],

    T_r(h,t) 1_{t>=0}
      <= |a_minus| (g_+-t)(r b_plus^2+(a_plus)_- t)
                    1_{0<=t<=g_+}.                        (2)

Indeed the first positive part in (1) is at most
|a_minus|(g-t) on its support; the second is at most
r b_plus^2+(a_plus)_-t for t>=0. At either type boundary the determinant
weight is zero, so no boundary mass is removed in (2).

Integrating the nonnegative quadratic polynomial gives

    int_0^infty T_r(h,t) dt
      <= |a_minus| [r b_plus^2 g_+^2/2
                          +(a_plus)_- g_+^3/6].            (3)

The two coefficients are individually sharp for this envelope: with
b_minus=0 and a_plus=0 the first integral is exactly the first term; with
b_minus=b_plus=0 and a_plus<0 it is exactly the second term. These witnesses
work at positive r as well. This does not assert simultaneous sharpness of
all later Gaussian constants or sharpness for a particular field.

## 3. Conditional density is the load-bearing new hypothesis

Let X be any measurable R6-valued random vector and
H=(X_a_minus,X_a_plus,X_b_minus,X_b_plus,G), G=X_c_plus-X_c_minus.
Assume the conditional law of X_c_plus given H has a Lebesgue density
f(t|H)<=L almost everywhere for a fixed finite L. All expectations in this
section are under the SAME law of X. Disintegration and Tonelli, followed
by (3), give

 N_r:=E[T_r(X)1_E]
   <= L { (r/2) E[|X_a_minus| X_b_plus^2 G_+^2]
          +(1/6) E[|X_a_minus| (X_a_plus)_- G_+^3] }.       (4)

This holds as an extended nonnegative inequality; the following moment
assumptions make its right-hand side finite. No independence is assumed.

One cannot substitute a bound on the marginal density of X_c_plus. For a
rational counterexample, take t uniform on [0,1], g=3t/2, a_minus=a_plus=-1,
and b_minus=b_plus=0. Then T=t^2/2, so N=1/6. Inserting the marginal density
cap L=1 into the proposed right-hand side gives E[g^3]/6=9/64<1/6.
H determines t; its conditional law has no density. This example is not a
Gaussian field. Even for Gaussian variables, a nonsingular marginal can
become deterministic after conditioning on a correlated coordinate.

## 4. Explicit Gaussian-error consequence

Define U=X_a_plus-1, u2=E U^2, g2=E G^2,
K2=E X_a_minus^2, K6=E[X_a_minus^2 X_b_plus^4]. Assume K2,K6 finite and
U,G individually Gaussian, possibly noncentered, degenerate and dependent.
The elementary inequality (x)_- <= (x-1)^2/4 gives

 N_r <= L [ (sqrt(3 K6)/2) r g2
       +(105*10395)^(1/4) sqrt(K2) u2 g2^(3/2)/24 ].        (5)

Details of the moment step, without independence:

 E[|X_a_minus| X_b_plus^2 G_+^2]
      <= sqrt(K6) sqrt(E G^4) <= sqrt(3 K6) g2,
 E[|X_a_minus| U^2 |G|^3]
      <= sqrt(K2) (E U^4 G^6)^(1/2)
      <= sqrt(K2) (E U^8 E G^12)^(1/4)
      <= (105*10395)^(1/4) sqrt(K2) u2 g2^(3/2).

For any real Gaussian Z=m+sZ0, its binomial even-moment expansion implies
E Z^(2k) <= (2k-1)!! (E Z^2)^k. Coefficientwise, the ratio of the j-th
variance coefficient to the corresponding upper coefficient is
1/(2(k-j)-1)!!<=1, with (-1)!!=1. The needed constants are 3,105,10395
for orders 4,8,12. Thus (5) also covers zero variances and nonzero means.

Now assume a specified coupling to Y with Y_a_plus=1 and Y_c_plus=Y_c_minus
almost surely, and e^2=E||X-Y||^2. Then u2<=e^2 and g2<=2e^2, so

 N_r <= L [sqrt(3 K6) r e^2
             +(105*10395)^(1/4) sqrt(2 K2) e^5/12].        (6)

If 0<z_*<=z_r and e<=K_e r, and K2<=C2, K6<=C6 on a fixed interval,

 nu_r(E) <= min(1, (L/z_*) [sqrt(3 C6) K_e^2 r^3
             +(105*10395)^(1/4) sqrt(2 C2) K_e^5 r^5/12]). (7)

In particular the probability is O(r^3). The division is by the normalized
normalizer z_r=Z_r/r^2, not the physical Z_r. The estimate bounds the actual
typed numerator directly; no L1 weight error is silently set to zero.
Neither (6) nor (7) is valid from a mere second-moment error without the
stated Gaussian higher-moment and conditional-density inputs.

## 5. A uniform conditional-density bound from a confluent 11-jet frame

Work in the original centered Gaussian Hilbert space, before imposing pins.
Set F(x)=f(x,0), H_y(x)=f_y(x,0), Q(x)=f_yy(x,0). Assume on a common open
interval around zero that F is C5, H_y is C3, Q is C1 in mean square and
that the indicated derivatives are actual jointly Gaussian derivatives.
Let

 J11=(F(0),F'(0),...,F^(5)(0),
                H_y(0),...,H_y'''(0),Q'(0)).

Assume the covariance of the TWELVE-component vector (J11,Q(0)) is positive
definite. This is stronger than #301's six-pin Gram hypothesis and will be
verified for a stated spectral class in section 6. Define

    sigma0^2=Var(Q(0) | J11)>0.

This is the eleven-observation residual variance, not the variance of Q_L
conditioned only on the six contact pins used to define z0 below.

For h=r/2>0 consider the 11 observations

 O_r=(F(-h),F'(-h),F''(-h), F(h),F'(h),F''(h),
      H_y(-h),H_y'(-h),H_y(h),H_y'(h), Q(h)-Q(-h)).        (8)

These are exactly the six raw pins together with the four axial/mixed
Hessian entries and the transverse difference, up to permutation and
nonzero scaling/subtraction of known pin rows. They do NOT include Q(h)
as an extra conditioned observation. Conditioning first on the six pins
and then on H in section 3 is equivalent to conditioning on (8).

Here is an explicit invertible transformation removing the coalescing
singularity. For m=3 or 2 define the fixed 2m by 2m real matrix

 V_m[(s,ell),j] = (d^ell/dt^ell t^j)|_{t=s},
 s=-1,+1; ell=0,...,m-1; j=0,...,2m-1.                    (9)

It is invertible: a polynomial of degree <2m with all m derivatives
vanishing at both nodes would be divisible by (t-1)^m(t+1)^m, so is zero.
Use V_3 on the six F rows in (8), multiplying the ell-th observed derivative
by h^ell first. If c_j is the resulting coefficient after V_3^-1, set
R_j=j! h^-j c_j. Hilbert-space Taylor expansion gives, for ell<=2,

 h^ell F^(ell)(s h)
    = sum_{j=ell}^5 [F^(j)(0) h^j/j!] V_3[(s,ell),j]+o(h^5).

Thus R_j=F^(j)(0)+o(h^(5-j)) and all six rows converge in L2.
Apply the identical construction with m=2 to H_y and its first derivative;
the four rows converge to H_y^(j)(0), j=0,...,3. Divide the last row in (8)
by 2h to obtain convergence to Q'(0). The combined change of rows is
invertible for every h>0. Call the transformed vector R_r; then

    (R_r,Q(h)) -> (J11,Q(0)) in L2.                       (10)

The 12 by 12 covariance matrices converge. Since the limiting one is
positive definite, its 11 by 11 observation block is invertible for small r,
and the scalar Schur complement is continuous and tends to sigma0^2.
Consequently

    Var(Q(h) | O_r) >= sigma0^2/2                        (11)

on a sufficiently small fixed interval. In a jointly Gaussian family this
conditional variance does not depend on the prescribed values. The canonical
conditional density of Q(h) is therefore bounded by

    L=(pi sigma0^2)^(-1/2).                              (12)

The actual successive pin/endpoint conditionings in section 3 have precisely
this variance: their raw observations are related to O_r by the invertible
maps just described. Their means may depend on all prescribed values, but
a Gaussian density's supremum does not depend on its mean. The raw or scaled
six-endpoint covariance is not assumed uniformly invertible; several of its
eigenvalues may tend to zero. Equation (11) is a scalar residual statement
proved through the DIFFERENT rescaled observation frame R_r.

## 6. Spectral-class and source-matched fixed-field corollaries

Suppose the actual stationary covariance is

 C(z)=sum_{k in Z2} p_k exp(i nu k.z),
 p_k>0, p_-k=p_k, nu>0, sum_k p_k(1+|nu k|^10)<infinity.   (13)

The tenth moment gives the mean-square derivative regularity in section 5
by dominated convergence in the weighted spectral L2 space. The 12 derivative
symbols, after nonzero scale/phase factors, are the distinct monomials

    1,x,x^2,x^3,x^4,x^5, y,xy,x^2y,x^3y, xy^2,y^2.

A zero-variance linear combination would vanish at every integer-frequency
pair because every p_k is positive. Fixing each integer y and then each
integer x shows that such a polynomial must be identically zero. Hence the
12-jet covariance is positive definite. This verifies the extra premise,
not merely the six-pin Gram. Removing the Q(0) mode in a finite model can
leave a positive residual variance at every r>0 but make it vanish at contact;
the checker retains that countercontrol.

Use the same axial pins as #301: F(-h)=b, F(h)=b-r^3/6 and both gradient
pins zero, with b=6/5. This is k=1/6 in P's convention. The #301 pin frame
has d_r=(b-r^3/12,0,0,0,0,2); after pinning, the adjusted axial/mixed Hessian
entries are precisely the physical entries divided by r. There is no switch
of endpoint coordinates or height-gap coefficient in applying (8).

Under (13), the stronger derivative assumptions of #329 hold, so its
explicit common regression coupling gives e<=K_e r, bounded Gaussian means
and covariances, and z_r>=z0/2>0 on a sufficiently small interval. The same
marginals and coupling are used in (5)--(7). For example its moment bounds
supply C2=M^2+6Lambda and C6=32(M^6+480Lambda^3). The limiting contact
transverse Gaussian has positive variance by the 12-jet Gram, hence
z0=E(Q_L)_-^2>0. Intersect that interval with the one in (11) and r<=1.
Equation (7) proves the cubic sign bound for this spectral class.

For P's actual periodized Gaussian field, specialize d=2, L=24 and nu=2pi/24.
P sections 1--2 specify exactly

 p_k=exp(-2pi^2|k|^2/24^2) / sum_j exp(-2pi^2|j|^2/24^2).

These weights are strictly positive and have finite moments of every order;
thus (13) holds. This is a check of the actual model and pins, not an import
of P's global theorems. We obtain constants C<infinity and r_*>0 such that

  nu_r{ f_yy(S)>=0 } <= C r^3,             0<r<=r_*<24.    (14)

All constants are existence/symbolic constants, not numerical enclosures.
This statement is fixed in dimension, period, birth, direction and gap mark.
It is NOT a result about 1-p_r, the elder partner, extra critical points,
capture, persistence lifetimes, all marks, or growing windows. It does not
make the endpoint total-variation obstruction disappear. P's boundary-layer
mechanism is explicitly credited; this is its independently checkable
finite-jet/sign-coordinate refinement, not a new whole-program closure.

## 7. Cubic order is attained in an abstract Gaussian family

Let Q be standard normal and, for 0<r<=1, define

    X_r=(-1,1,-1,1,Q-3r,Q),
    Y=(-1,1,-1,1,Q,Q).

Here H is deterministic, Q|H remains
standard normal, e=3r and the relevant moments are bounded. The exact weight
is (2r-Q)_+(r-Q)_+. Its normalizer tends to E Q_-^2=1/2 by domination.
The numerator of E is

    int_0^r (2r-t)(r-t) phi(t) dt
       = r^3 int_0^1 (2-s)(1-s) phi(rs) ds.

Continuity of phi and integral_0^1(2-s)(1-s)ds=5/6 yield

    lim_{r->0} nu_r(E)/r^3=5 phi(0)/3>0.                 (15)

Thus an exponent strictly larger than 3 cannot hold for the entire abstract
Gaussian/density/coupling class. This rank-one Gaussian family is NOT claimed
to be an actual six-pin periodic field, or an actual-field lower asymptotic.
It establishes sharp order for the assumptions, not equality of any coarse
constant in (7).

## 8. Reproduction, controls, and boundaries

`python -B -S test_cubic_band.py` and its `-O` version run 12 methods.
`cubic_band.py` runs 2214 exact controls: 2160 band integrations, 40 Hermite
monomial recoveries, four conditional variances, four sharp cubic integrals
and six isolated witnesses. Its outputs are deterministic. The finite
Gaussian model uses independent coefficients of 15 explicitly defined
monomials. Exact Schur computation gives 1+h^4/4; deleting its constant Q
mode gives h^4/4, so positive-radius density alone does not supply a uniform
floor. It is not an evaluation of the infinite periodic covariance.

M1--M6 must exit1 with the respective reasons BAND_R_COEFFICIENT,
BAND_CUBIC_COEFFICIENT, HERMITE_DERIVATIVE_SCALE, GAUSSIAN_TWELFTH,
CONDITIONAL_NOT_MARGINAL, MARGINAL_DENSITY_NOT_SUFFICIENT. Unknown arguments
exit2. Numerical checks are not proofs of the continuum claims. No existing
workflow automatically runs this new checker; no Lean target is added.

General linear Gaussian conditioning is prior methodology. The primary
abstract record Majumdar--Majumdar, arXiv:1710.09285, was consulted as context,
not imported as an unread proof of (10)--(14). The finite covariance/Schur and
polynomial arguments above give the assumptions and derivation explicitly.
A fresh nonauthor review must inspect the new conditional-density step,
constants, exact pin correspondence, Gaussian moment use and exclusions.
All historical proof bytes, review dispositions and scientific flags remain
unchanged. In particular this does not repair the separate source-admission
gate or resolve missing independent formal alignment/provenance.
