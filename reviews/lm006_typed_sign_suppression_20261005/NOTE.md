# LM006: direct typed-weight suppression of the saddle-transverse sign event

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, session `round16-typed-sign-and-final-evidence-20261005`.
Scientific effect NONE. This is a new conditional analytic companion with
finite supporting diagnostics, not a Lean formalization or a status change.

## 1. Source and purpose

The endpoint definitions are those of Math-#315, now landed at
`99ba2dfe33ef0052694510355b0c4d811fd66441`, path
`reviews/lm006_normalizer_stability_20261005/NOTE.md`, blob
`5790aaa0332bd8e79b276be1577e4c5f3502eed6`, SHA256
`2e63518026cef54bb91757ccbdba986a0765f8a8b640240417ba30c59e2f5fd4`.
Its physical type identity and Gaussian norm moments are restated below.

The generic tilted-law packet is Math-#318, original head
`ecafa5206c528b0c662ea0bcbb26938681251aa5`, NOTE blob
`6633cdf0bfee55e2fc2046176effbf44634454b3`. Its later author comment6007838056
bounds a particular sign event by a density error plus a squared coupling
error; its separate review6008028956 does not review this new argument.
The new result uses the actual typed weight instead of comparing arbitrary
weights. It removes the density-error term from the NUMERATOR estimate.
A positive lower normalizer remains indispensable.

This is not a claim of general Gaussian-inequality novelty. It is a
source-specific improvement for one endpoint event. No concrete coupling
rate, uniform radius, field identification, or full-field event is supplied.

For v=(a_-,a_+,b_-,b_+,c_-,c_+) in R^6, define x_+=max(x,0),
x_-=max(-x,0), and, for 0<=r<=1,

 F_r(v)=[(a_-)_-(c_-)_- - r b_-^2]_+,
 G_r(v)=[r b_+^2-a_+c_+]_+,
 T_r(v)=F_r(v)G_r(v).                                    (1)

For r>0, T_r is the physical maximum/saddle-filtered Hessian determinant
product divided by r^2. Explicitly, the two Hessians are

 [[r a_-,r b_-],[r b_-,c_-]],  [[r a_+,r b_+],[r b_+,c_+]].

The first is selected to be negative definite; the second has negative
determinant. Singular boundaries have zero determinant weight. At r=0,
(1) is a continuous extension, not division by zero. The event considered
throughout is E={c_+>=0}, including its boundary. This is not a trivial
maximum-type condition: a 2x2 saddle can have c_+=0 or c_+>0.

## 2. Pointwise estimate with sharp algebraic coefficients

Put u=a_+-1 and g=c_+-c_-. Then for every v and 0<=r<=1,

 T_r(v) 1_E <= r |a_-| b_+^2 |g|
                + (1/16)|a_-| u^2 g^2.                   (2)

Proof. Off E the left side is zero and both right terms are nonnegative.
On E, if F_r=0 there is again nothing to show. Otherwise a_-<0 and c_-<0.
Write A=-a_->0, C=-c_->0 and d=c_+>=0. Then g=C+d>=0, and

 F_r<=A C,   G_r<=(r b_+^2)+ (a_+)_- d.

The latter follows from [s+t]_+<=s+t_+ when s>=0. Thus

 T_r <= r A b_+^2 C + A (a_+)_- C d.

Two elementary inequalities finish the proof:

 C<=C+d=|g|,    C d <= (C+d)^2/4,
 (a_+)_- <= (a_+-1)^2/4.                                 (3)

For the last inequality, a_+>=0 gives zero on the left. If a_+<0, multiply
by4 and subtract: (a_+-1)^2+4a_+=(a_++1)^2>=0.
Combining both factors1/4 produces1/16 in (2). No eigenvalue inverse,
density assumption, type-boundary probability or independence is used.

The two coefficients in this PARTICULAR pointwise form cannot separately
be decreased while the other term is fixed:
- v=(-A,1,0,1,-q,0), A,q>0, gives T_r=r A q, with equality in the
  first term and zero second term for r>0.
- v=(-A,-1,0,0,-q,q), A,q>0, gives T_r=A q^2, with zero first term
  and equality in the second term, for every r>=0 in the domain.

These are algebraic Hessian witnesses, not realizations of the specified
six-pin random field. Sharpness of (2) does not assert sharpness of the
subsequent expectation constants.

The shared transverse difference g is essential. The event E and maximum
type force c_- and c_+ to lie on opposite sides of zero; their product is
therefore controlled by g^2. When c_-=c_+ exactly, T_r 1_E=0 for every r.

## 3. Expectation bound before any Gaussian assumption

Let X be a measurable R^6-valued random vector on a probability space.
Use its coordinates in (1), U=X_{a_+}-1 and G=X_{c_+}-X_{c_-}. Define

 K2=E[X_{a_-}^2],             K6=E[X_{a_-}^2 X_{b_+}^4],
 g2=E[G^2],                  R44=E[U^4 G^4].

Assume these four nonnegative moments are finite. Integrating (2) and
applying Cauchy--Schwarz to each term separately gives

 N_r:=E[T_r(X) 1_E]
   <= r sqrt(K6 g2) + (1/16) sqrt(K2 R44).                (4)

This step is valid for non-Gaussian variables with arbitrary dependence.
It establishes integrability of the event-restricted weight. For a
normalized endpoint probability also assume

 0<z_r:=E T_r(X)<infinity.

Then the measure with density T_r(X)/z_r under the law of X is a probability
measure nu_r and

 nu_r(E) <= min(1,[r sqrt(K6 g2)+sqrt(K2 R44)/16]/z_r).    (5)

The numerical finite-law checks below test (4), not a Gaussian conclusion
for finite atomic variables. The normalizer cannot be omitted: a one-point
law at (-1,-1,0,0,-1/2,1/2) has T_r=1/4 and nu_r(E)=1.

## 4. Gaussian error coordinates give a quartic error contribution

Suppose U and G are each univariate Gaussian, possibly degenerate and
possibly dependent. A jointly Gaussian X is sufficient. Write

 u2=E U^2,  g2=E G^2.

For any real Gaussian H=m+sZ, s>=0, with Z standard normal,

 E H^8 = m^8+28m^6s^2+210m^4s^4+420m^2s^6+105s^8
       <=105(m^2+s^2)^4.                                 (6)

The coefficients follow by the binomial expansion, vanishing odd centered
moments and the integration-by-parts recursion E Z^(2k)=(2k-1)E Z^(2k-2).
The inequality is coefficientwise: the difference is
104m^8+392m^6s^2+420m^4s^4. Thus it includes s=0 and nonzero means.
Applying Cauchy--Schwarz once more, without assuming independence,

 R44 <= sqrt(E U^8 E G^8) <=105 u2^2 g2^2.

Consequently (4) becomes

 N_r <= r sqrt(K6 g2) + [sqrt(105 K2)/16] u2 g2.          (7)

This is the useful moment-specific form. It does not require a lower
variance bound or invertible covariance matrix. K2 and K6 may be retained
as actual mixed moments rather than replaced by coarse norm bounds.

## 5. A coupling to the contact plane and the r e + e^4 estimate

On one probability space, let Y be a measurable vector with

 Y_{a_+}=1,    Y_{c_+}=Y_{c_-}    almost surely,

and suppose e^2=E||X-Y||^2<infinity. The full LM006 contact section
Y=(-1,1,-h/2,h/2,Q,Q) satisfies these two identities; they are the only
identities of Y used in this step. Pointwise norm inequalities give

 u2<=e^2,   g2<=2e^2.

The second factor2 is the squared norm of the linear functional
v -> v_{c_+}-v_{c_-}, not an omitted independence assumption. Hence, under
the Gaussian-error-coordinate assumptions of §4,

 N_r <= sqrt(2 K6) r e + [sqrt(105 K2)/8] e^4.            (8)

Let z_r>=z_*>0 be a genuinely supplied bound. Then

 nu_r(E) <= min(1, [sqrt(2 K6) r e
                         +sqrt(105 K2)e^4/8]/z_*).       (9)

Unlike an arbitrary-weight TV transfer, (9) has no Delta=E|a-b| term.
That term was not silently set to zero: the exact numerator was bounded
directly using (1)--(3). A normalizer estimate is still required, and this
result does not control a different arbitrary weight.

For Gaussian X in R^6 with ||E X||<=M and ||Cov X||_op<=Lambda, the
predecessor's norm moment argument supplies

 K2<=M^2+6Lambda=:C2,
 K6<=E||X||^6<=32(M^6+480Lambda^3)=:C6.

The number480 is 6*8*10, the sixth radial moment of a standard6 Gaussian.
If both X,Y have the specified affine Gaussian coupling and bounds in
#315, and its independently supplied condition guarantees z_r>=z0/2>0,
one may set z_*=z0/2, K2<=C2, K6<=C6 in (9). The z_r here is the normalized
physical quantity Z_r/r^2, not Z_r itself; no extra power of r is lost.

If, in addition, e<=K r^alpha with alpha>0, one common K, and uniform C2,C6
and z_*, then

 nu_r(E) <= [sqrt(2 C6) K/z_*] r^(1+alpha)
            +[sqrt(105 C2) K^4/(8z_*)] r^(4alpha).        (10)

In particular a PROVED e=O(r) input yields O(r^2), with a smaller O(r^4)
term. This note does not prove that input for the concrete field, evaluate
a numerical radius, or infer uniformity from pointwise constants.
At e=0 the event mass is zero by (8), provided normalization is defined.

The earlier generic sign-comment bound (Delta+e^2)/z0 remains correct
at its broader arbitrary-weight scope. It is not being retracted or
relabeled. The improvement here is specific to the exact typed T_r.

## 6. Why the Gaussian moment condition must not disappear

The pointwise estimate and (4) do not require Gaussianity; the replacement
of R44 by105u2^2g2^2 does. A rare-atom example exposes the distinction.

Take fixed Y=(-1,1,0,0,-1,-1). With probability1-p let X=Y; with
probability p let X=(-1,-1,0,0,-1,1). Both atoms have T_r=1 for every
r in[0,1], so z_r=1 and nu_r(E)=p. Here K2=1, K6=0 and e^2=8p.
The purported non-Gaussian version of (8) would assert

 p <= (sqrt(105)/8)(8p)^2 = 8sqrt(105)p^2,

which fails, for example at p=1/1000. U and G are not Gaussian in this
example. It is a counterexample to removing a hypothesis, not a
counterexample to this theorem or a six-pin Gaussian-field realization.
The exact general bound (4) still holds; its second term is sqrt(p),
which is at least p. The pointwise bound (2), before Cauchy--Schwarz,
is exact on both atoms.

## 7. Reproduction, controls, and exclusions

From this directory run

    python -B -S test_typed_sign.py
    python -B -O -S test_typed_sign.py
    python -B -S typed_sign_check.py
    python -B -O -S typed_sign_check.py

The12-method test suite checks the physical identity, full pointwise
majorant, both sharpness witnesses, the two scalar inequalities, Gaussian
eighth moments, correlated/degenerate Gaussian polynomial moments,180
finite-law Cauchy bounds, a non-Gaussian counterexample, normalization,
input validation, exact failure reasons and CLI rejection.

The standalone checker reports3753 exact controls:1458 physical identities,
2187 pointwise inequalities,20 eighth-moment comparisons,81 mixed Gaussian
polynomial comparisons, and7 isolated witnesses. The mixed diagnostic uses
two affine functions of one standard normal, so it explicitly includes
perfect correlation and degeneracy. General covariance is covered by the
analytic Cauchy--Schwarz proof, not extrapolated from this finite screen.

M1 uses r^2 instead of r in the main term; M2 weakens1/16 to1/32; M3 drops
the event restriction; M4 uses15 instead of105 for the eighth moment;
M5 discards the Gaussian mean; M6 falsely applies the Gaussian conclusion
to the rare-atom law; M7 omits normalization. Each must exit1 with its
specified SIGN_FAIL reason. Unknown labels or arguments exit2. Generic
crashes are not intended mathematical rejections. These are finite
supporting diagnostics, not Lean execution or continuum certification.

Excluded: an actual-field Gaussian/conditioning/Gram construction; a new
numerical normalizer or error rate; a full-field capture/persistence event;
arbitrary endpoint event bounds; total-variation convergence; higher-d
matrix generalization; proof-library alignment; historical verdict changes.
A fresh nonauthor read must inspect (2)--(10), especially the two1/4 factors,
mean-sensitive eighth moment, dependence allowance, and the normalized
z_r. Prior #315/#318 or comment6007838056 reviews do not cover this proof.
