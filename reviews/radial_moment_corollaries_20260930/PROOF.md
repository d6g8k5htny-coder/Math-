# Smooth inverse-radius expansion and sharp rates for microscopic extreme marks

Object: OA-RADIAL-RATE-20260930-v1. Author: OpenAI / GPT-6 Astra Pro.
Disposition: AUTHOR-SIDE CONDITIONAL PROOF CANDIDATE; NONAUTHOR REVIEW OPEN.
Scientific effect NONE. No parent proof, register, Boolean, prize, or earlier
review is changed. This conversation authored SC/P and contributed to the
related cluster line; no independent revalidation of those premises is implied.

## 1. Exact object and scope

Fix d>=2, L>0, b real, k>0 and an orthonormal frame, under the original model
and full endpoint normalizer. This paper concerns the ALREADY-FORMED limiting
microscopic POINT intensity of [R]. First the original field radius r tends to
zero; only then does the microscopic distance threshold t tend to infinity.
No finite-r convergence rate is proved. Whole-cluster maximum selection and
its moving tie boundaries are not consumed or treated here.

Exact source identities are in SOURCES.json. [R] is PR166 RADIAL_TAIL.md at
80059a97cd8eb32d1a17a0ad9cb22cb2a0d7b337, blob0f14417ef7038b9c6f50e4b01e393a58b7b5e3a4:
R7-R13 supply the root-resolved integral, Gaussian domination and positive leading
coefficient. [SC] is PR162 PROOF.md at382c0f9ff2281f43651ddbdf2e9b36dd52e2c6bf,
blob16c56821b52fd76b0be791622b9c3809eafde75a: the nondegenerate raw Gaussian contact
jet, orthogonal spectral convention and finite nonempty microscopic measure.
[P] is imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md at
7a1cb09a9d58d179393e6d29146252f714b9c9bf, blobdfed3b8d318a3ab1950957f393307733a4bef3f2:
only the exact periodized covariance and contact conditioning, used in Section7.
Neither PR169's whole-cluster candidate, its companion-ratio addendum, nor any
numerical coefficient note is a premise. Source reviews are not reviews here.

Use [R]'s variables lambda=(a,h,O,xi), with ordered positive hard curvatures h,
normalized Haar O, and remaining cubic entries xi. Put

 A=a/(12k), gamma=sqrt(1+A^2),
 beta0=a^2/(12k), c0=a^3/(144k^2),
 A0=O diag(0,-h) O^T,
 H(h)=product h_j^3 product_(i<j)(h_j-h_i),
 G_lambda(beta,c)=h0(A0,Rot_O tau(a,beta,c,xi)),
 G0=G_lambda(beta0,c0),
 K0=108 k^7 c_m/z0.                                      (1)

Empty hard products equal1 in d=2. h0 is the actual RAW Gaussian contact density,
not an isotropic replacement; z0 is the FULL normalizer limit. Rotations act
orthogonally on complete tensor coordinates, up to fixed dimensional norm
equivalence. Let

 b0(u)=3-12u^2,
 S={-3/2<u<1/2, |b0(u)|/2<v<3-6u},
 Q(u,v)=(4v^2-b0(u)^2)(b0(u)-4uv)>0 on S.

For y=1/Z define

 g_lambda,u,v(y)=G_lambda(beta0+k b0 y^2,
                  c0+(a b0/4)y^2+2k(v-b0u)y^3).          (2)

[R, R11] says exactly that the tail F(t)=integral sum_i 1{|z_i|>t}dM is

 F(t)=K0 integral_(S,lambda) Q H
    integral_R |Z|^-12 g(1/Z)
           1{(u-AZ)^2+Z^2>t^2}dZ du dv d lambda.         (3)

The multiplicity of roots is already correct in this formula. No extra factor
for a double cluster, pin density, or endpoint normalizer is introduced.

## 2. A fixed-domain smooth even representation

**Theorem 1.** There is a smooth even function C(delta), defined for
|delta|<2/3 and with every fixed derivative bounded on |delta|<=1/3, such that

                  F(t)=t^-11 C(1/t),   t>=3.             (4)

Smoothness also holds in L1 for the underlying UNSIGNED shape/parameter measures.
The claim is C-infinity, not analyticity or convergence of an infinite Taylor
series. Consequently for every fixed N>=0 there are finite coefficients C_(2j)
with

 F(t)=sum_(j=0..N) C_(2j) t^(-11-2j)+O_N(t^(-13-2N)),
 -F'(t)=sum_(j=0..N)(11+2j)C_(2j)t^(-12-2j)
                                      +O_N(t^(-14-2N)).  (5)

C_(0)>0 is [R]'s C_star. Constants are at the fixed source parameters; no growing
dimension, volume, vanishing-gap, or parameter-uniform claim is made.

**Proof.** The reciprocal substitution in (3) gives |Z|^-12 dZ=|y|^10 dy on
both signs. For t>|u| the physical radius condition is

 (t^2-u^2)y^2+2uAy-gamma^2<0.

Set delta=1/t and y=delta w. Its two endpoints in w are

 w_plus/minus(delta)=m(delta) +/- d(delta),
 m(delta)=-uA delta/(1-u^2 delta^2),
 d(delta)=sqrt(gamma^2-u^2 delta^2)/(1-u^2 delta^2).        (6)

Thus (4) holds with

 J_delta(u,v,lambda)=d(delta) integral_(-1)^1
       [m(delta)+d(delta)x]^10
       g(delta[m(delta)+d(delta)x]) dx,
 C(delta)=K0 integral Q H J_delta du dv d lambda.         (7)

There is no moving integration boundary left. On |delta|<=delta0<2/3 the
denominator is uniformly positive and the square-root radicand is bounded
below by a positive constant, since |u|<=3/2 and gamma>=1. Each fixed derivative
of m,d is bounded by a polynomial in1+|a| with constants depending on delta0,k.

For every fixed j the nondegenerate Gaussian contact density satisfies

 sup_(beta,c) |partial_(beta,c)^j G_lambda(beta,c)|
       <= C_j exp[-c_j(|h|^2+a^2+|xi|^2)]                (8)

uniformly in O. Indeed each derivative is a polynomial times the same Gaussian;
absorb that polynomial into a weaker Gaussian exponent and then discard beta,c
from its quadratic lower bound. A bounded mean changes the constants only.
Uniform tensor norm equivalence under O supplies the displayed retained variables.
No inverse hard eigenvalue is used. This is an elementary derivative extension
of [R]'s raw Gaussian bound, not an extra stochastic assumption.

The chain rule in (7), for any fixed number of delta derivatives, now gives an
integrable majorant of the form

 C Q H (1+|a|)^M exp[-c(|h|^2+a^2+|xi|^2)],               (9)

on the bounded shape domain and x in[-1,1]. The actual shifted beta,c values
may be large: (8) is a supremum over them, not an invalid compactness assumption.
This proves differentiation under all integrals and smoothness in L1 as well
as for the total mass. The exact identities m(-delta)=-m(delta),
d(-delta)=d(delta), followed by x->-x, show J_(-delta)=J_delta. This cancellation
holds even when g(y) is not even; its cubic y^3 term is retained.

Taylor's theorem with the integrated derivative bounds proves (5), including
its differentiated remainder. It is NOT obtained by formally differentiating
an unspecified big-O estimate. C(0) is the positive source coefficient. QED.

## 3. Explicit second coefficient

Write C_0=C_(0), C_2=C_(2), to distinguish coefficients from their tail powers11,13.
Set the differential operator acting on G_lambda at fixed a,h,O,xi

                 D_a=k partial_beta+(a/4)partial_c.

The pointwise density has expansion g(y)=G0+g2 y^2+g3 y^3+O(y^4), with

                 g2=b0 D_a G0.                          (10)

There is no linear y term. Expanding the exact endpoints, or differentiating
(7), gives

 j0=(2/11)gamma^11 G0,
 j2=u^2 gamma^9(1+12A^2)G0+(2/13)b0 gamma^13 D_a G0,
                 J_delta=j0+j2 delta^2+O_L1(delta^4).    (11)

For the geometric part, write w_+=gamma-uA delta+
[u^2 gamma-u^2/(2gamma)]delta^2+O(delta^3), with the corresponding reflected
negative endpoint. Then (w_+^11-w_-^11)/11 equals
2gamma^11/11+u^2 gamma^9(1+12A^2)delta^2+O(delta^4).
The g2 term contributes2g2 gamma^13 delta^2/13. The odd g3 term first contributes
at order delta^4 after the two physical sides are summed; it is not dropped
from the all-order argument.

The necessary exact shape integrals are

 I=integral_S Q=246528/35,
 U2=integral_S u^2 Q=240192/35,
 B=integral_S b0 Q=-428544/7=3I-12U2,
 Uabs=integral_S |u|Q=5898627/880.                        (12)

They follow by integrating the polynomial Q in v and then on the strips cut
at u=-1/2 and u=0. The companion computes them in exact Fraction arithmetic.
In particular

 C_0=K0*(2I/11) integral H gamma^11 G0 d lambda,
 C_2=K0 integral H [U2 gamma^9(1+12A^2)G0
                       +(2B/13)gamma^13 D_a G0]d lambda. (13)

Both integrals are finite by (8). C_0>0. No general sign or nonzero assertion
for C_2 is made in arbitrary dimension/frame; Section7 supplies an exact
noncancellation result at a narrower source scope. No numerical evaluation of
either Gaussian integral is claimed.

## 4. Rates for the radial ratio and unsigned marks

Let P_t be point-INTENSITY sampling conditioned on physical radius R>t. Define
q=R/t>=1 and retain Y=(u,v,lambda), but FORGET sign Z. These are the root-resolved
latent coordinates of [R], not a configuration-uniform selection. Define the
finite measures with densities

 dmu0=K0 Q H j0 dY, dmu2=K0 Q H j2 dY,
 c=C_2/C_0.                                             (14)

mu0 has mass C_0 and mu2 mass C_2. The joint law of (q,Y) has the L1 expansion

 dP_t(q,Y)=11q^-12 dq dmu0(Y)/C_0
  +t^-2 [13q^-14 dq dmu2(Y)/C_0
              -11c q^-12 dq dmu0(Y)/C_0]+O_L1(t^-4).     (15)

In particular its total-variation distance to the stated independent limiting
product is O(t^-2). Projection to Y, or to the downward height
eta=u+1/2+v/6, retains this rate. This supplies an O(t^-2) TV rate for the
intensity-selected height law H_eta/I in [R, H1-H2]. No spatial-configuration
TV claim is made: the map to actual positions depends on t.

Proof: for fixed Y, the radius tail density is t^-11 K0 QH J_(1/t).
Differentiate the smooth expression already justified in Section2; at tq its
radial density times t equals

t^-11 K0 QH q^-12[11J_(1/(tq))+(1/(tq))J'_(1/(tq))].

Divide by F(t)=t^-11 C(1/t) and use the L1 Taylor estimates. The remainder is
bounded after integration by a constant times t^-4 q^-12, integrable on q>=1.
This proves (15) without differentiating a merely pointwise asymptotic. QED.

Let Pareto_11 have density11q^-12 on q>=1. For the scalar radial ratio, (15) gives

 p_t(q)=11q^-12[1+c t^-2((13/11)q^-2-1)]+O_L1(t^-4).

**Sharp scalar coefficient:**

 dTV(Law_(P_t)(R/t),Pareto_11)
       =kappa |c| t^-2+O(t^-4),
 kappa=(2/13)(11/13)^(11/2).                              (16)

The same leading coefficient holds for the supremum distance of their CDFs.
The correction changes sign only at q0=sqrt(13/11). Its positive integral is
q0^-11-q0^-13=kappa; its total integral is zero. Half its L1 norm is therefore
kappa, proving (16). The uniform CDF remainder follows from the L1 remainder;
the maximum of q^-11(1-q^-2) is also kappa. If C_2=0 the stated error is O(t^-4),
not an unjustified claim of a nonzero second-order term.

As another quantitative consequence, uniformly over q>=1,

 F(tq)/F(t)=q^-11[1+c t^-2(q^-2-1)]+O(t^-4 q^-11).        (17)

This is a source-specific second-order regular-variation statement. Generic
second-order tail theory is not claimed novel.

## 5. Retaining the sign has a different, strictly slower sharp rate

The cancellation in Section2 used both signs. Keep epsilon=sign Z and the
same Y. The two half integrals are exactly

 J_delta,epsilon=integral_0^(d+epsilon m) w^10 g(epsilon delta w)dw,
 J_delta,epsilon=j0/2+epsilon h1 delta+O_L1(delta^2),
 h1=-uA gamma^10 G0.                                    (18)

The linear term comes from the physical cutoff shift m. g'(0)=0, so no density
term cancels it. Applying the differentiated density argument to each half yields

 dTV(Law_(P_t)(epsilon,R/t,Y),
           UniformSign x Pareto_11 x mu0/C_0)
                    =B_sign t^-1+O(t^-2),
 B_sign=(K0/C_0) Uabs integral H |A|gamma^10 G0 d lambda>0. (19)

Indeed the first signed correction has density
12 epsilon h1 q^-13 K0 QH/C_0; its half-L1 norm, summed over the two signs and
integrated over q, is the displayed B_sign because integral_1^infinity12q^-13dq=1.
Finiteness follows from (8); strict positivity follows from the full positive
Gaussian density on open sets with a!=0 and positive hard spectrum. The gauge
convention for O is exactly that in [R]; (19) is a result for those retained
latent variables, not a statement that a sign alone has a nonzero marginal bias.
Marginalizing can cancel a correction, and specifically forgetting epsilon
cancels this one. Thus signed and unsigned rates must not be conflated.

## 6. A finite part for the critical eleventh moment

Let M11(t)=integral sum_i min(R_i,t)^11 dM. The prior theorem gave its leading
logarithm. There is now a finite constant L11 such that

 M11(t)=11 C_0 log t+L11-(11/2)C_2 t^-2+O(t^-4).          (20)

One exact definition is

 L11=11 integral_0^1 x^10 F(x)dx
       +11 integral_1^infinity[x^10 F(x)-C_0/x]dx.

The first integral is finite by finite total point mass. The second converges
by (5) at N=1. Tonelli gives M11(t)=11 integral_0^t x^10 F(x)dx; subtracting
its limiting finite part and integrating the controlled remainder proves (20).
No numerical value for L11 is asserted. This is again after the r limit only.

## 7. Exact positive second correction in the aligned planar periodic model

**Theorem 2.** In d=2, with the axial coordinate aligned with one of the lattice
axes of [P]'s EXACT periodized kernel, C_2>0 for every fixed L,k>0 and b real.
Consequently the radial TV and CDF errors in (16) are genuinely Theta(t^-2),
with the positive coefficient in (16); not merely an upper bound.

Proof: [P]'s kernel factors as K_L(x,z)=k_L(x)k_L(z). Let m2,m4,m6 be the even
spectral moments of the one-dimensional variance-one factor; m2>0 and the full
positive lattice spectrum gives m4-m2^2>0 and m6-m4^2/m2>0. At contact condition
on (f,fx,fxx,fxxx,fz,fxz)=(b,0,0,12k,0,0).

Even-total-order jets and odd-total-order jets are independent. For the odd
soft cubic jets (a,beta,c)=(fxxz,fxzz,fzzz), separability and reflection in each
axis give a centered DIAGONAL conditional Gaussian with variances

 va=vbeta=m2(m4-m2^2),       vc=m6-m4^2/m2.                (21)

For transparency: Cov(beta,(fx,fxxx))=(-m2^2,m2 m4) is -m2 times the first row
of Cov(fx,fxxx), so its conditional mean is -m2 fx=0 even though fxxx=12k.
a and c correlate only with fz in that odd conditioning block, with covariances
-m2^2 and -m4; their raw covariance m2 m4 is removed by that regression. Their
conditional covariance with beta vanishes by coordinate reflection. The diagonal
variances follow by subtracting these rank-one regressions. The even soft
curvature has its own strictly positive conditional density at zero and merely
multiplies this cubic Gaussian by a positive b-dependent scalar.

Therefore on the cusp

 D_a G0=-[a^2/(12vbeta)+a^4/(576k^2 vc)]G0<=0.            (22)

In (13), U2>0, B<0 and G0>0. The geometric term is strictly positive and the
second term is nonnegative. Thus C_2>0, without replacing finite L by a continuum
covariance or numerically approximating a lattice sum. The same common even
b-dependent factor cancels from c=C_2/C_0 and B_sign at this planar aligned
scope. We do not extend this diagonal regression or noncancellation assertion
to arbitrary rotations or d>=3 without a separate argument. QED.

## 8. Verification and review boundary

A: reciprocal physical cutoff, fixed-domain map, C-infinity L1 Gaussian derivative
domination, exact parity and differentiated all-order asymptotic expansion.
B: j0/j2 coefficients, all four exact shape integrals, signed/unsigned TV and CDF
constants, finite-part moment, and aligned planar regression/noncancellation.

The stdlib companion checks shape integrals, formal endpoint equations, exact
Taylor coefficients, cancellation and signed bias, independent scalar controls
and deliberately false variants. These are finite checks, not a formal proof
of any Gaussian input or differentiation under an infinite-dimensional integral.
No Lean formalization, global status change, coefficient enclosure or self-merge.

No rate for r->0, no uniform simultaneous t(r)->infinity statement, no claim
about the remote singleton population, no convergence rate for whole-cluster
maximum selectors across ties, and no spatial independence/elder pairing is
added by this packet. Sign-forgetting is part of (15), not an optional omission.
