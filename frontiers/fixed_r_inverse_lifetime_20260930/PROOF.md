# Fixed-separation lifetime tails and the sharp inverse-moment boundary

Object OA-FIXED-R-INVERSE-LIFETIME-20260930-v1.
Author: OpenAI / GPT-6 Astra Pro. AUTHOR-SIDE PROOF CANDIDATE; new nonauthor
analytic review OPEN. Scientific effect NONE. No prior proof, status, graph,
Boolean, prize or review disposition is changed.

## 1. Statement and the precise probability law

Fix d>=2, L>0, b real, k>0, a unit vector u and 0<r<L/4. Nothing in this
paper tends to the contact limit r=0. On the flat torus X=R^d/(L Z^d) use the
variance-one Gaussian field with the exact covariance of [P] Section1:

 K_L(z)=sum_(n in Z^d) exp(-|z+Ln|^2/2)
                         /sum_n exp(-|Ln|^2/2).

Set M=-(r/2)u, S=(r/2)u, Delta=k r^3, and condition by continuous Gaussian
regression on f(M)=b, f(S)=b-Delta, grad f(M)=grad f(S)=0. Denote that law Q.
With independent symmetric Hessian entries as matrix coordinates, put

 W=|det H_M det H_S| 1{H_M<0,index(H_S)=d-1},
 Z=E_Q W,                         dQ^W=(W/Z)dQ.           (1)

There is one original FULL normalizer; no extra pin density, adjacency event,
local-count conditioning or good-event normalizer is inserted. Section2 below
proves 0<Z<infinity directly at each fixed distinct pair.

Define the ordinary superlevel elder death by its maximin characterization

 d_f(M)=sup_(gamma(0)=M, f(gamma(1))>b) min_t f(gamma(t)),
 ell=b-d_f(M).                                          (2)

An empty class of paths has d_f=-infinity and ell=+infinity (essential class).
On finite deaths this is the actual lifetime, not a gap to a counted witness.
Let F denote failure of the prescribed saddle S to be the ordinary partner.
On the usual distinct-critical-value locus, (2) is the ordinary elder saddle
value. The estimates below apply directly to (2), without counting saddles
or assuming a particular local saddle is the global partner.

**Theorem 1 (two-sided fixed-r small-lifetime order).** There are constants
0<c_-<=c_+<infinity and epsilon0>0, depending on the fixed parameters, such that
for 0<epsilon<epsilon0,

 c_- epsilon^(2/3) <= Q^W(0<ell<=epsilon,ell finite)
                  <= c_+ epsilon^(2/3).                 (3)

We may choose epsilon0<Delta; then the small-lifetime event in (3) is contained
in F. Consequently the same two-sided order holds conditional on finite death,
or on F and finite death, with their positive normalization probabilities.

**Theorem 2 (inverse moments).** For every p>=0,

 E_QW[ell^(-p);ell finite] < infinity iff p<2/3,
 E_QW[ell^(-p);F,ell finite] < infinity iff p<2/3.         (4)

For p=0 these denote the finite-event probabilities. The corresponding
conditional expectations have the same finiteness boundary. Multiplication by
the fixed positive scale Delta leaves the threshold unchanged, so (4) also
holds for the normalized lifetime X_r=ell/Delta. At critical and supercritical
powers the capped expectations obey

 E_QW[min(ell^(-1),T)^(2/3);F,ell finite]=Theta(log T),
 E_QW[min(ell^(-1),T)^p;F,ell finite]=Theta(T^(p-2/3))
                                      for p>2/3.        (5)

The same holds without F or after the stated finite-event conditioning. The
constants are not evaluated. There is no claimed exact leading coefficient
or lifetime-density equivalent in (3). Together with elementary finiteness of
positive moments, the full finite-death power-moment domain is q>-2/3:
E[ell^q;finite] and E[ell^q;F,finite] are finite exactly on that range.

**Scope.** These are statements at EACH FIXED positive r, with epsilon->0.
The constants and epsilon0 may degenerate arbitrarily as r->0. No uniform
integrability as r->0 or limit of inverse moments is asserted. In particular
this is NOT the distant-partner-conditioned law of PR181, where r->0 and a
second extreme-radius limit occur before a small-lifetime limit. Its exponent4
and this exponent2/3 concern different laws and different limiting operations.

[P] is the exact source in SOURCES.json. Only its model, observation, weighting
conventions and fixed-point Fourier facts in Sections1-2 are used; the latter
are reconstructed below. The uniform cap theorem, global count laws, elder
candidates PR170/175, positive-moment PR177 and extreme-mark PR181 are NOT proof
premises. The author is exposed to [P]. This is a new consumer, not independent
revalidation of that source's other theorems.

## 2. Fixed-parameter Gaussian facts, with no contact uniformity

Poisson summation gives Fourier weights

 a_n=exp(-2 pi^2 |n|^2/L^2)/sum_j exp(-2 pi^2 |j|^2/L^2)>0.

For every integer m, sum_n sqrt(a_n)(1+|n|)^m is finite. A real sine/cosine
expansion and Minkowski's inequality show that every C^m norm of the field
has moments of every finite order. For orders below1 use a larger moment.
This also supplies a smooth version of the field.

Any finite list of distinct derivative evaluations at distinct sites has
strictly positive covariance. Indeed a zero-variance linear combination
annihilates every Fourier mode since a_n>0. As a distribution it is a finite
sum of derivatives of delta masses, all of whose Fourier coefficients vanish.
The distribution is zero. Test functions supported near one site with arbitrary
finite jets show that all its coefficients vanish. Symmetric tensor entries
are listed once only; a change of orthonormal frame is invertible on these jets.

This proves nondegeneracy of the original observation vector O and of the
following additional lists modulo O:

 U=(H_M,H_S),    J=(H_M,H_S,D^3 f(M)).                    (6)

All conditional covariances here are at FIXED r>0. None is replaced by its
singular r=0 counterpart. Their conditional Gaussian densities are strictly
positive on every compact set and bounded above by C exp(-c|U|^2), or the
analogous bound for J, with constants depending on the fixed observations.

Full-field regression conditional on U has the form

 f=m_U+G_U,       ||m_U||_C3 <= C(1+|U|),
 G_U independent of U,    E||G_U||_C3^q<infinity.         (7)

The regression coefficients are fixed smooth covariance derivatives multiplied
by the inverse of a fixed nonsingular covariance matrix. The residual is the
original field minus a finite-rank smooth Gaussian field, so its norm moments
follow from the preceding Fourier estimate. If

 K=1+||D^2 f||_infty,op+||D^3 f||_infty,op,

then E[K^q|U]<=C_q(1+|U|)^N_q for every q>0. In particular K is NOT presumed
independent of the Hessians. The same argument conditional on J gives an
independent C4 residual and a uniform C4 mean bound on each compact J set.

The Gaussian density of U is positive on the open product of the required
Hessian cones; W is strictly positive there. All its polynomial moments are
finite. Hence Z in (1) is positive and finite. No r^-2 normalizer estimate is
needed or used.

For completeness, (2) is measurable: for h<b the event d_f(M)>h is existence
of a path from M to a point above b with its minimum strictly above h. A
uniform approximation of such a path by torus piecewise-linear paths with
rational vertices retains both strict margins. Thus a countable set of paths
suffices; their endpoint values and compact-path minima are measurable field
functionals. An essential maximum simply has no eligible path.

## 3. A deterministic local barrier gives a lower bound on lifetime

Let f be any C3 field on the torus with f(M)=b, grad f(M)=0 and H_M<0. Write
lambda_min for the smallest eigenvalue of -H_M and use K above, so
0<lambda_min<=K. Put a_L=min(1,L/4) and

 R=a_L lambda_min/K < L/2.

For every unit v and 0<t<=R, Taylor's theorem with the global operator-norm
third-derivative bound gives

 f(M+tv) <= b-(lambda_min/2)t^2+(K/6)t^3
          <= b-(lambda_min/3)t^2 < b.                   (8)

The ball is embedded. No point above b lies inside it. Every continuous path
in (2) must cross its boundary, on which (8) gives

 d_f(M) <= b-lambda_min R^2/3,
 ell >= c_L lambda_min^3/K^2,  c_L=a_L^2/3>0.            (9)

This holds also as an inequality for ell=+infinity. It proves strict positivity
of every finite lifetime without any global Morse argument. The barrier does
not claim the partner is on that sphere; it bounds all older-reaching paths.

## 4. Keep the determinant weight: the upper small-lifetime bound

For any nonnegative measurable function psi, (7) and the Gaussian U density
imply a one-dimensional weighted eigenvalue estimate

 E_Q[W K^2 psi(lambda_min)]
 <= C integral_0^infinity lambda psi(lambda)
                             (1+lambda)^N exp(-c lambda^2)d lambda.  (10)

Here is the full reduction. On H_M<0 diagonalize -H_M with ordered positive
eigenvalues 0<lambda1<=...<=lambdad and orthogonal frame O. The symmetric-matrix
Jacobian has absolute factor constant times product_(i<j)|lambdaj-lambdai|.
This follows by differentiating O diag(lambda) O^T: each angular off-diagonal
coordinate has multiplier lambdaj-lambdai. Repeated eigenvalues are Lebesgue
null. The determinant weight supplies product_j lambdaj, not its square root
and not an unweighted matrix law.

The actual anisotropic Gaussian density is only UPPER-bounded by an isotropic
Gaussian envelope; no rotational invariance is assumed. Bound the Vandermonde
and all regression-moment factors by polynomials in the eigenvalues and H_S.
The |det H_S| factor is also polynomially bounded; dropping its type indicator
only enlarges the upper bound. Integrate H_S and the compact angular variable,
then extend the ordered hard eigenvalues to independent (0,infinity) intervals.
Gaussian integration leaves a polynomial in lambda1 times its Gaussian envelope.
Its remaining determinant factor is exactly lambda1. This proves (10). No
inverse hard eigenvalue or inverse eigenvalue-gap estimate has been introduced.

From (9), with C_L=max(1,c_L^-1),

 1{0<ell<=epsilon} <= min(1,C_L epsilon K^2/lambda_min^3)
                  <= C_L K^2 min(1,epsilon/lambda_min^3). (11)

The final inequality uses C_L K^2>=1. Apply (10) with
psi(lambda)=min(1,epsilon/lambda^3), and divide ONCE by Z. For epsilon=s^3<=1,
the portion lambda<=1 is bounded by a constant times the exact integral

 integral_0^1 lambda min(1,s^3/lambda^3)d lambda
                =s^2/2+s^3(1/s-1)=(3/2)s^2-s^3.         (12)

The lambda>=1 portion is O(epsilon) by the Gaussian envelope. Therefore
Q^W(0<ell<=epsilon)<=C epsilon^(2/3). This is the upper half of (3).
It did not divide an unconditional derivative-tail probability by a rare scale;
K was retained inside the weighted integral and handled by conditional moments.

## 5. An open soft-curvature sector gives the matching lower bound

Use a fixed orthonormal coordinate system at M and write the entire Hessian as

 H_M=[[v^T C^-1 v-lambda, v^T], [v,C]],
 e=(1,-C^-1 v),          lambda>0.                       (13)

Let C range over a compact box of strictly negative definite (d-1)-matrices,
v over a fixed small box of positive volume, and H_S over a compact box inside
the index-(d-1) cone. We may ensure eigenvalues of C stay between -2 and -1/2,
|det C|>=c_C>0 and |det H_S|>=c_S>0. The entire boxes can be chosen with
nonempty interiors. In these coordinates

 e^T H_M e=-lambda,   H_M<0,
 |det H_M|=lambda |det C|.                               (14)

The change from the independent H_M entries to (lambda,v,C) has absolute
Jacobian1: only H_11 is replaced, with derivative -1 in lambda. We do not set
v=0 on a measure-zero slice, nor shrink its box with lambda. The direction e
adapts smoothly to v,C and has a uniform finite norm bound E.

Let the third-derivative tensor T at M vary over a fixed compact positive-volume
box for which T[e,e,e]>=a>0 for every C,v in the chosen boxes. Such a box exists:
start with T_111=2a and all other entries zero, choose v small, and then a
sufficiently small full-dimensional tensor neighborhood. Initially allow
0<=lambda<=1. This defines a compact set of complete J targets. By Section2 its
raw conditional density has a strictly positive lower bound m_r on that set.

Write the conditional full field as m_J+G_J. Choose a fixed residual C4 norm
bound with probability p0>0, possible because the residual has a finite norm
almost surely. It is independent of J. The conditional mean is bounded on the
compact targets; consequently there is a uniform directional fourth-derivative
bound M4>=1 along e on this event, accounting for |e|<=E. This uses a fixed
positive-probability residual event, not the probability of a shrinking Gaussian
ball. M4 and m_r may be very unfavorable as r decreases, which is allowed.

For the straight path t -> M+t e, Taylor now gives

 f(M+t e) >= b-(lambda/2)t^2+(a/6)t^3-(M4/24)t^4.         (15)

Put B=6/a. If lambda<=6/(M4 B^2), then at t=B lambda the right side minus b is
at least (B^2/4)lambda^3>0. Over the entire interval 0<=t<=B lambda it is at
least -(3B^2/4)lambda^3, hence certainly at least -B^2 lambda^3. Reduce a
fixed lambda0>0 further so that B lambda0 E<min(L/4,r/4) and
B^2 lambda0^3<Delta. The path stays in an embedded neighborhood disjoint from S.
It reaches an older point and establishes

                    0<ell<=B^2 lambda^3<Delta.          (16)

Strict positivity uses (9). Finiteness and failure of S follow from the actual
path and the inequality d_f(M)>b-Delta, not from a count of nearby critical
points. We need not identify the actual death saddle or forbid an even higher
alternative global path: either could only shorten ell further.

For 0<epsilon<B^2 lambda0^3, restrict
0<lambda<(epsilon/B^2)^(1/3). In the Schur coordinates, the raw density is
at least m_r, the residual event has probability p0 independently, and the
original determinant product is at least lambda c_C c_S. The remaining boxes
have a fixed positive finite volume. Dividing by the original positive Z gives

 Q^W(0<ell<=epsilon,F) >= c integral_0^((epsilon/B^2)^(1/3)) lambda d lambda
                       = (c/2)B^(-4/3)epsilon^(2/3).     (17)

This is the lower half of (3). It holds for all sufficiently small epsilon at
the fixed model parameters, not just along a sequence or finite numerical grid.

## 6. Inverse moments and capped growth

Both normalizing events {ell finite} and {F,ell finite} have positive probability
by (17). For epsilon<Delta the small-lifetime event cannot be pairing success,
because success at S has lifetime exactly Delta. Thus the tail estimates (3)
apply with either finite-event restriction and after dividing by its positive
mass.

On a chosen restricted event A let Y=ell^-1, assigning zero outside A solely
for the layer-cake formula. For large t,

          c t^(-2/3) <= Q^W(Y>t) <= C t^(-2/3).          (18)

Endpoint strict versus weak inequalities cause no difficulty: upper bounds use
(3), and a lower bound at epsilon=1/(2t) is already enough. For p>0, Tonelli gives

 E[Y^p]=p integral_0^infinity t^(p-1) Q^W(Y>t)dt.

The portion below a fixed large threshold is finite. The remaining integral
converges precisely when p<2/3. This proves (4). For positive powers, on finite deaths ell<=2||f||_infty;
all weighted positive moments of this norm are finite by the Gaussian norm
and Hessian moments of Section2 and Cauchy-Schwarz. This yields the stated
full power-moment domain without asserting any small-r moment convergence.
Truncating the same integral at T gives the logarithmic and power orders in (5). These are two-sided growth
orders, not exact coefficients; a density or precise regular-variation limit
was not proved by the two-sided comparison.

## 7. What this closes, and what it does not

The fixed-r inverse boundary is now determined at candidate-theorem level,
complementing PR177's separately derived positive finite-lifetime moments.
Neither the small-r marked law nor its moment-convergence hypotheses are used
here. In particular the new result cannot be reinterpreted as a failure of
PR181: that law further conditions on a distant replacement partner after
already taking r->0, whereas (3) includes all finite failures at fixed r.

The exponent2/3 has two independent sources: local cubic escape costs a lifetime
of order lambda^3, while the original Palm weight and eigenvalue volume give
lambda d lambda. Dropping that weight changes the conclusion. As a comparison,
the same proof for the raw Gaussian law conditioned only on the two open Hessian
types, without either determinant tilt, gives exponent1/3; in its upper argument
integral_0^1 min(1,s^3/lambda^3)d lambda=(3/2)s-(1/2)s^3.
This comparison is not a change to the law (1) used in the main theorems.

No exact lifetime density, leading coefficient, r-uniform constant, joint
r/epsilon limit, convergence of inverse moments as r->0, distant-partner inverse
threshold at finite r, or globally deduplicated persistence-bar intensity is
asserted. Essential-inclusive POSITIVE moments and their convention remain
separate. These proofs are not formalized in Lean and finite tests are not
analytic acceptance.

Requested review A: fixed-r Gaussian nondegeneracy, regression and weighted
spectral reduction (Sections2-4), including the original full Z. Review B:
full-dimensional Schur sector, retained residual event, older-reaching path,
lower bound and the exact moment conclusions (Sections5-6). Prior source
verdicts or green workflows do not accept this new consumer.
