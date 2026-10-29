# The global essential share at a vanishing critical-gap ratio

28 October 2026. OpenAI/Codex GPT-6 author-side proof candidate, written
by author-support agent `/root/tiny_gap_route` at `/root`'s request.
This is same-family technical work. Different-family scientific review is
pending; no scientific-status or acceptance transition is asserted.

## 1. Scope, regularity and the ordered limit

Fix `d>=2`, `L>0`, a birth height `b`, and a unit direction `u`. Write
`omega=2pi/L`. The source is the real stationary Gaussian field on the
cubic torus with covariance

    K(x)=sum_(n in Z^d) a_n exp(i omega n.x),
    a_n=a_(-n)>=0,
    a_n>0 whenever ||n||_infinity<=4,
    sum_n sqrt(a_n)(1+|n|)^6 <infinity.              (TG1)

The spectrum is fixed, and all constants may depend on it, `d,L,b,u`.
The original variance-normalized periodized Gaussian has strictly positive
Gaussian-decaying Fourier coefficients and satisfies (TG1). Finite Fourier
fields with this positive cube also satisfy (TG1). There is no assumption
of full function-space support or positivity outside the displayed cube.
The sixth-order summability and cube-four positivity are explicit stronger
hypotheses than the C4/cube-three class of the preceding critical-window
packet.

Use exactly the contact law `Q_0` of
[`CRITICAL_WINDOW.md`](../all_frame_gaussian_rates_20261028/CRITICAL_WINDOW.md),
with a fixed orthonormal coordinate frame `(x,y)` whose first vector is `u`:

    f(0)=b, grad f(0)=0,
    f_xx(0)=0, f_xy(0)=0, f_xxx(0)=0.              (TG2)

Here `y` has dimension `m=d-1`. Under this law put

    A=f_yy(0), B=f_xxy(0), c=f_xxxx(0), Delta=det A,
    gamma=c/12-B^T A^-1 B/4                     on {A<0},
    w_tau=Delta^2(36tau^2-gamma^2)_+ 1{A<0},
    z(tau)=E_Q0 w_tau,
    G={max_X f<=b},
    N(tau)=E_Q0[w_tau 1{gamma<-2tau}1_G].           (TG3)

The preceding packet proves, for each fixed `tau>0`, with the original
value/full-gradient pins, original typed determinant weight and `k=tau r`,

    lim_(r downarrow0) P_r(E_r)=p_E(tau):=N(tau)/z(tau). (TG4)

Only after taking that limit do we let `tau` tend to zero below. This note
does not exchange the limits, assert a joint `r,tau` result, or integrate
the statement into a counting intensity.

For `A<0`, the implicit function theorem gives the local transverse ridge
`y_f(x)` through zero, and `g_f(x)=f(x,y_f(x))`. Define its coefficients

    q5(f)=g_f^(5)(0)/120,
    q6(f)=g_f^(6)(0)/720.                           (TG5)

The result is

    p_E(tau)=C_E sqrt(tau)+o(sqrt(tau)),
    C_E=[8(9sqrt(3)-5)/63] M_0/D_0,
    0<D_0<infinity, 0<M_0<infinity.                 (TG6)

The constants `D_0,M_0` are defined by ordinary finite-dimensional density
integrals in Section 3. In particular (TG6) specifies the actual global
essential share, rather than inferring it from a typed or local-elder
normalizer.

## 2. Reused inputs and the fifth ridge coefficient

The typed quartic weight, its small-r contact interpretation, and the
small-`tau` scalar normalization `288tau^3` are existing results. See
`cusp_second_order_20261001/PROOF.md`, CU.2--CU.4 and Remark 8.1; the latter
also contains the local elder share `13/27`. The global indicator in (TG4)
is from the preceding critical-window packet. None of these is claimed as
a new result here.

The fifth ridge coefficient is also already present: it is exactly `Q_1`
in `elder_cusp_parity_20261002/PROOF.md`, Section 0, equation (0.1), after
renaming its transverse vector `gamma` as our `B` and its transverse
matrix `B` as our `f_xyy`. In our notation, with

    v=A^-1 B, eta=f_xxxy(0), D=f_xyy(0), e=f_xxxxx(0),

the reused formula is

    q5=e/120-eta^T v/12+D[v,v]/8.                   (TG7)

For clarity, it can be checked directly on the parabola
`y=-vx^2/2`: its fourth coefficient is
`c/24-B^T v/8=gamma/2`, and its fifth coefficient is (TG7). The actual
ridge has the same coefficients. Indeed `y_f'(0)=0`,
`y_f''(0)=-v`; the contributions of its third-order displacement to the
fifth coefficient cancel because `A(-v/2)+B/2=0`.

The differently parameterized `k^6` small-gap law in
`reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md`,
Section 4, concerns an already-defined cubic off-axis witness kernel.
That source explicitly does not exchange its limiting kernel with the
original small-r limit. It supplies neither (TG6) nor a global essential
indicator.

Under (TG1) the source Fourier series converges absolutely almost surely
in C6: the expectation of the sum of the C6 norms of its real Gaussian
Fourier summands is finite. It defines a Gaussian Radon measure on C6.
Finite Gaussian regression preserves this property, and the centered
regression residual has every C6-norm moment by the Gaussian norm theorem.
Covariance derivatives and regression profiles through the orders used
below exist in C6. For example, cross derivatives of total order at most
11 for a fifth-jet observation are controlled by
`sum a_n(1+|n|)^12<infinity`, which follows from (TG1).

Every finite jet vector used below has nonsingular covariance after the
specified contact rows are removed. A differential row relation at zero
is a polynomial in the rotated frequency coordinates. A polynomial of
total degree at most six vanishing on the seven-point grid in each
coordinate, hence on the positive cube three, is zero by successive
one-variable interpolation. Rotated differential monomials are linearly
independent. Applying this argument to the contact rows together with all
jets through order four and the pure fifth derivative proves the required
rank. The same argument applies to all fifth jets and a pure sixth jet
if desired, although no assertion that `q6!=0` is needed below.

If `f_n->f` in C6 and `A(f)<0`, one common product chart supports the
transverse ridges for all sufficiently large `n`. The implicit function
theorem gives convergence of the ridges in C5. The envelope identity

    g_f'(x)=f_x(x,y_f(x))

then gives `g_f` in C6 and convergence in C6, despite the ridge itself
being guaranteed only C5. Thus `q5,q6` are continuous functions of the
field on this open hard-block set. Their values are determined by the
finite sixth jet, by differentiating the transverse critical equation, so
they are Borel without making a global choice of ridge chart.

## 3. Explicit nonlinear contact disintegration

Let `J` contain all free derivatives of orders at most four under (TG2),
except the single entry `c=f_xxxx(0)`. Each symmetric mixed derivative is
included once. In particular `A,B,eta,D` are entries of `J`. Let `e` be the
pure fifth derivative used in (TG7). Under `Q_0`, `(J,c,e)` has an
everywhere positive nonsingular Gaussian density `rho(j,c,e)` with respect
to the usual coordinates on these derivative entries. Its marginal
`rho4(j,c)=integral rho(j,c,e) de` is also nonsingular Gaussian.

For `j` in the open domain `D_-={j:A(j)<0}`, define

    v(j)=A(j)^-1 B(j),
    t(j)=B(j)^T(-A(j))^-1 B(j)>=0,
    c0(j)=3B(j)^T A(j)^-1 B(j)=-3t(j),
    r5(j)=-eta(j)^T v(j)/12+D(j)[v(j),v(j)]/8,
    e0(j)=-120r5(j).                               (TG8)

The transformation to the actual effective quartic and fifth coefficients
is the diffeomorphism on `D_- x R^2`

    (j,gamma,q) -> (j,c0(j)+12gamma,e0(j)+120q).

Its absolute Jacobian is

    12*120=1440.                                   (TG9)

Although the lower-left derivative blocks in `j` contain inverse matrices,
the diagonal blocks are `Id,12,120`; no determinant of `A`, additional
coarea density, or independence of the nonlinear coefficients is inserted.
Equation (TG7) shows that the transformed variables are exactly
`gamma` and `q=q5`, not substitutes for those ridge coefficients.

Regress the whole field on these finite linear observations, after (TG2).
There is a deterministic affine C6-valued function `mu(j,c,e)` and a
centered Gaussian C6 residual `H`, independent of `(J,c,e)`, such that the
conditional field is

    f(j,c,e;H)=mu(j,c,e)+H,
    ||mu(j,c,e)||_C6<=C(1+|j|+|c|+|e|).            (TG10)

The covariance and law `nu(dH)` of this residual do not depend on the
conditioning values. Set

    f00(j,H)=f(j,c0(j),e0(j);H).

It has all the original contact rows and exactly `gamma=q5=0`. All the
integrals below use the same residual law `nu`. Define

    D_0=12 integral_(D_-) Delta(j)^2 rho4(j,c0(j)) dj,

    M_0=1440 integral_(D_-) Delta(j)^2 rho(j,c0(j),e0(j))
          E_nu[ sqrt((-q6(f00))_+) 1{max_X f00<=b} ] dj. (TG11)

The positive part in the second line makes the integrand defined without
a sign convention off the global-maximum event. These are the precise
meanings of the sometimes convenient formal expressions
`E[Delta^2 1{A<0}delta(gamma)]` and
`E[Delta^2 1{A<0}sqrt((-q6)_+)1_G delta(gamma)delta(q5)]`.
The density factors in (TG11) are not probabilities of zero-probability
conditioning events.

For later use, nonsingularity and the Gaussian conditional density of `e`
give constants `C,a>0` such that

    rho(j,c,e)<=C exp[-a(|j|^2+c^2)]               for every e,
    rho4(j,c)<=C exp[-a(|j|^2+c^2)].               (TG12)

The fixed nonzero mean depending on `b` is absorbed by changing `C,a`.

## 4. A uniform envelope that includes every soft transverse block

The following bounds are pathwise and make no inverse-matrix moment
assumption. Put `P=1+|v|` and `K=1+||f||_C6`. In a fixed physical coordinate
chart choose `rho_*>0` small enough, depending only on the torus and frame.
The parabola

    z_v(x)=(x,-vx^2/2), |x|<=rho_*/P

stays in that chart for every `v`. Its first derivative is bounded by a
fixed constant and its second derivative has size at most `|v|`; higher
derivatives vanish. The chain rule therefore gives

    sup |(f o z_v)^(6)| <= C K P^3.                (TG13)

The largest power is three because a term in the sixth derivative contains
at most three second derivatives of `z_v`. With (TG7) and Taylor's theorem,

    f(z_v(x))-b=gamma x^4/2+q5 x^5+R(x),
    |R(x)|<=C K P^3 |x|^6.                        (TG14)

If `max_X f<=b` and `-6tau<gamma<-2tau`, divide the lower Taylor bound by
`x^4` and take `x` with the sign of `q5`. For `a0=-gamma/2` this gives

    |q5| h <= a0+C K P^3 h^2,
                       0<h<=rho_*/P.

Choosing `h=min(rho_*/P,sqrt(a0/(C K P^3)))` yields

    |q5|<=C sqrt(tau K) P^(3/2)+C tau P.           (TG15)

This estimate tests only a path in the field, so it does not require
uniform bounds for derivatives of the actual ridge near singular `A`.

Now use the common regression (TG10), with

    -6<s<-2, 0<tau<=1,
    c_tau(j,s)=c0(j)+12tau s,
    e_tau(j,z)=e0(j)+120sqrt(tau) z,
    f_tau(j,s,z,H)=f(j,c_tau,e_tau;H),
    R_H=1+||H||_C6,
    U(j)=1+|j|+|c0(j)|.                           (TG16)

These fields have `gamma=tau s` and `q5=sqrt(tau)z` exactly. From (TG8)--(TG10),

    1+||f_tau||_C6
      <=C[R_H+U(j)P^2+sqrt(tau)|z|].             (TG17)

Indeed `|e0(j)|<=C|j|P^2` and `|c_tau-c0|<=72`.
Apply (TG15), divide by `sqrt(tau)`, and use
`sqrt(a+b)<=sqrt(a)+sqrt(b)`. Young's inequality absorbs the term
`C tau^(1/4)P^(3/2)sqrt(|z|)` into `|z|/2+C sqrt(tau)P^3`.
Consequently the global-maximum event implies the uniform envelope

    |z|<=L(j,H):=C P^3 sqrt(R_H+U(j)).             (TG18)

The constant is independent of `j,H,s,tau` in (TG16). The displayed
dependence on `P` is retained when a transverse eigenvalue tends to zero;
the next estimate controls that dependence without an eigenvalue floor.

Here is the determinant cancellation that makes (TG18) usable. Let
`lambda=lambda_min(-A)>0`. Then

    |v|^2<=t/lambda,
    Delta^2<=lambda^2 ||A||^(2m-2),
    Delta^2 |v|^3
       <=lambda^(1/2)||A||^(2m-2)t^(3/2)
       <=(1+||A||)^(2m)(1+t)^(3/2).              (TG19)

For `m=1` the exponent `2m-2` is zero; the same estimate holds. Thus

    Delta^2 P^3
       <=C(1+||A||)^(2m)(1+|c0|)^(3/2),          (TG20)

because `c0=-3t`. This is a pointwise estimate, not an appeal to an
unproved inverse moment.

Also, since `|c_tau-c0|<=72`, (TG12) gives

    rho(j,c_tau,e_tau)
       <=C exp[-a'(|j|^2+c0(j)^2)]                (TG21)

after changing constants, uniformly in `z,s,tau`. Combining (TG18)--(TG21),

    integral_(D_-) integral_R integral_C6
       Delta^2 exp[-a'(|j|^2+c0^2)]
       1{|z|<=L(j,H)} nu(dH) dz dj <infinity.     (TG22)

To verify this explicitly, integrate `z` first. The resulting factor is
`2C Delta^2 P^3 sqrt(R_H+1+|j|+|c0|)`. Bound the square root by
`sqrt(R_H)+sqrt(1+|j|+|c0|)`, use (TG20), and absorb every power of `|c0|`
into half of `exp(-a'c0^2)`. What remains is a polynomial in `|j|` times
`exp(-a'|j|^2)` and `E_nu sqrt(R_H)<infinity`. Thus (TG22) holds with
ordinary Lebesgue measure in `j`, including the full approach to singular
`A`. There is no exclusion of a soft layer.

## 5. Genericity at the additional contact, including the pinned height

For every fixed `j in D_-`, the conditional field `f00(j,H)` almost surely
has no critical point away from zero at height `b`. This assertion needs
proof under the additional conditioning; its analogue under `Q_0` alone
would not suffice.

Use the nonnegative periodic function from the preceding packet,

    q(x)=sum_i 2(1-cos(omega x_i))/omega^2.

It is strictly positive off the torus origin and vanishes to order two
there. For any point `p!=0`, multiply `q^3` by a trigonometric first-jet
basis at `p`, consisting of the constant and
`sin(omega(x_i-p_i))/omega`, `1<=i<=d`. Multiplication by `q^3` is an
invertible transformation on first jets at `p`, while each product
vanishes to order six at zero. These products therefore annihilate all
the linear observations in the regression (TG10), including the pure
fifth derivative. Their Fourier supports lie in cube four and they are
in the source RKHS by (TG1).

It follows that the residual conditional covariance of
`(f00(p),grad f00(p))` is positive definite. Otherwise a nonzero linear
functional of that first jet would annihilate every RKHS direction in
the conditioning kernel, contradicting the constructed arbitrary jets.
The covariance is continuous in `p` and independent of the conditioning
values. It has a positive common eigenvalue floor on every compact set
separated from zero.

For completeness, on such a compact set take a mesh of spacing `delta`
with at most `C delta^-d` points. On a fixed C2-norm cutoff `M`, a zero of
`(f00-b,grad f00)` implies that this `(d+1)`-vector has size at most
`C M delta` at a mesh point. Its Gaussian density there is uniformly
bounded, independently of the mean. The union bound is at most
`C_M delta^-d delta^(d+1)=C_M delta`, which tends to zero. Exhaust the
norm cutoffs and then the compact sets away from zero. This proves the
assertion. It also proves it for `dj x nu(dH)` almost every `(j,H)` by
Fubini.

Consequently on `{max f00<=b}` the origin is the unique global maximum.
There is a strict positive gap below `b` on the complement of every
neighborhood of zero. This is the only off-origin genericity needed;
no global Morse hypothesis is imposed at the deliberately degenerate
origin or elsewhere.

## 6. The all-scale sextic indicator limit

Fix `j in D_-`, `H`, `s in (-6,-2)` and `z in R`. Under (TG16),

    f_tau(j,s,z,H) -> f00(j,H) in C6.               (TG23)

This is an actual common regression coupling, since only the two finite
targets change. Take a common sufficiently small product chart with
strict transverse concavity. Section 2 gives `g_tau->g_00` in C6 there,
and their exact jets satisfy

    g_tau(0)=b, g_tau'(0)=g_tau''(0)=g_tau'''(0)=0,
    g_tau''''(0)=12tau s,
    g_tau'''''(0)=120sqrt(tau)z.                   (TG24)

Write `q6=q6(f00)`. On the base global-maximum event one has `q6<=0`:
the first possibly nonzero term after the zero fourth and fifth
coefficients is `q6 x^6`, so `q6>0` would contradict the maximum.

If `max f00>b`, C0 convergence preserves a strictly higher point, and
`1{max f_tau<=b}` tends to zero. Suppose instead that `max f00<=b` and
the uniqueness conclusion of Section 5 holds.

First let `q6<0` and

    z^2<2s q6.                                    (TG25)

Choose `epsilon>0` so small that `q6+epsilon<0` and
`z^2<2s(q6+epsilon)`. Shrink the fixed chart, then take `tau` small, so
`g_tau^(6)(x)/720<=q6+epsilon` throughout its ridge interval. Taylor's
theorem with (TG24) gives, for every `x` in that fixed interval,

    g_tau(x)-b
       <=x^4[tau s/2+sqrt(tau)z x+(q6+epsilon)x^2]. (TG26)

The bracket is strictly negative for every real `x`: its quadratic
coefficient is negative and its discriminant is negative by (TG25).
Thus the entire fixed ridge interval, including all intermediate
physical scales, lies below `b` except at zero. Transverse strict
concavity bounds the field by the ridge in a smaller product chart.
The unique base maximum supplies a strict gap outside that chart;
C0 convergence preserves it. Hence `max f_tau<=b` eventually.

Conversely, if `q6<0` and `z^2>2s q6`, the quadratic

    s/2+zt+q6 t^2

is positive at some fixed nonzero `t`. From (TG23)--(TG24), at the
microscopic point `x=sqrt(tau)t`,

    tau^-3[g_tau(sqrt(tau)t)-b]
          -> t^4[s/2+zt+q6 t^2]>0.                (TG27)

Thus the global-maximum event eventually fails. If `q6=0` and `z!=0`,
the same conclusion follows by choosing `t` such that `s/2+zt>0`.
No separate assertion that a sixth derivative has a continuous density
is required. The unaddressed case `q6=z=0` is Lebesgue null in `z`.

The discriminant boundary in the `q6<0` case consists of two `z` values
for each `(j,H,s)`, and is likewise null. Together with Section 5 this
proves, for `dj x nu(dH) x ds x dz` almost every point of the integration
domain,

    1{max f_tau<=b}
      ->1{max f00<=b}1{q6(f00)<0}
                       1{|z|<sqrt(2s q6(f00))}.   (TG28)

The proof of sufficiency used a fixed physical neighborhood and its
outside gap. Convergence of a polynomial on bounded scaled windows
alone would not establish (TG28).

## 7. Domination, the coefficient and finiteness

First record the reused normalizer with the density convention of
(TG11). Changing `c=c0(j)+12tau s` gives exactly

    z(tau)/tau^3
      =12 integral_(-6)^6 integral_(D_-)
         Delta^2(36-s^2)rho4(j,c0(j)+12tau s) dj ds.

The Gaussian bound (TG12), the bounded shift of `c0`, and
`Delta^2<=||A||^(2m)` give an integrable majorant. Dominated convergence
therefore yields

    z(tau)/tau^3 ->288D_0,
    integral_(-6)^6(36-s^2)ds=288.                (TG29)

The integral defining `D_0` is finite by the same majorant. It is strictly
positive because `rho4` is everywhere positive and `Delta^2>0` on the
nonempty open set `D_-`.

For the numerator use both changes of variables in (TG9), then scale
`gamma=tau s`, `q5=sqrt(tau)z`. Its exact representation is

    N(tau)/tau^(7/2)
      =1440 integral_(-6)^(-2) integral_(D_-) integral_R
          Delta^2(36-s^2)rho(j,c_tau(j,s),e_tau(j,z))
          E_nu[1{max f_tau(j,s,z,H)<=b}] dz dj ds. (TG30)

The factor `tau^(7/2)` is the product of the weight `tau^2`, the quartic
coordinate width `tau`, and the fifth-coordinate width `sqrt(tau)`.
The absolute Jacobian `1440` has not been folded into an unspecified
conditional density.

Regard (TG30) as one integral also over `nu(dH)`. Equations
(TG18), (TG21) and (TG22), together with the bounded interval of `s`,
provide the integrable majorant

    C Delta^2 exp[-a'(|j|^2+c0(j)^2)]
                         1{|z|<=L(j,H)}.          (TG31)

It is uniform for `0<tau<=1`. The smooth Gaussian density in (TG30)
converges pointwise to `rho(j,c0(j),e0(j))`, and (TG28) gives its
indicator limit. Thus dominated convergence applies without discarding
any transverse soft layer or large-residual tail. Integrating in `z`
and then `s` gives

    N(tau)/tau^(7/2) -> I_6 M_0,
    I_6=2 integral_2^6(36-t^2)sqrt(2t)dt
       =256(9sqrt(3)-5)/7.                        (TG32)

The square-root factor after the `z` integration is exactly
`sqrt((-q6)_+)` in (TG11). The limiting integral is finite by (TG31),
so this also proves `M_0<infinity`; it is not an assumed moment of the
sixth ridge derivative. For example the elementary antiderivative for
`I_6/2` is `sqrt(2)[24t^(3/2)-(2/7)t^(7/2)]`.

Combining (TG29) and (TG32) gives the coefficient in (TG6), since

    I_6/288=8(9sqrt(3)-5)/63.                     (TG33)

## 8. Positivity from a finite sextic Cameron-Martin template

It remains to prove `M_0>0`, including the actual sixth coefficient of
the template ridge. In the original lattice coordinates put

    s_i(x)=sin(omega x_i)/omega,
    P=Id-u u^T,
    H_*(x)=b-T|P s(x)|^2-a q(x)^3,
                                      T>0, a>0. (TG34)

This is a finite Fourier function supported in cube three, so it is in
the source RKHS. Since `q(x)>0` away from zero, it has the unique global
maximum `H_*(0)=b`. It satisfies every contact row (TG2), has
`A=-2T Id`, `B=0`, `c=0`, and `q5=0`. The pure fourth derivative along
`u` vanishes because `P s(xu)=O(x^3)`, whose squared norm starts at order
six. Its odd jets of odd total degree vanish by inversion symmetry.

The sixth coefficient must be computed on the actual ridge, rather
than on the straight line `xu`. Locally write the physical point as
`xu+V y`, where the columns of `V` are the transverse frame vectors.
The equation

    P s(xu+V phi(x))=0

has a smooth solution by the implicit function theorem. Because
`s(z)=z+O(|z|^3)`, one has `phi(x)=O(x^3)`. Along this curve the hard
penalty vanishes identically and

    q(xu+V phi(x))=x^2+O(x^4),
    H_*(xu+V phi(x))=b-a x^6+O(x^8).              (TG35)

At this curve the transverse gradient of `H_*` is solely that of
`-a q^3`. It is `O(x^5)`, since `q=O(x^2)` and `grad q=O(x)`.
The uniformly invertible negative transverse Hessian implies that the
actual ridge differs from `phi(x)` by `O(x^5)`. Taylor expansion in
the transverse variable changes the value in (TG35) by `O(x^10)`.
Consequently

    g_(H_*)(x)=b-a x^6+O(x^8),
    q6(H_*)=-a.                                   (TG36)

In particular the apparent sixth-order contribution of the sine hard
penalty on the straight line is canceled by following its transverse
zero manifold; it does not alter (TG36).

Let `j_*,c_*,e_*` be the template observations. They obey
`c_*=c0(j_*)=0` and `e_*=e0(j_*)=0`. In the source RKHS the vector

    h_*=H_*-mu(j_*,0,0)

annihilates all observations used in (TG10). It is therefore in the
Cameron-Martin space of the centered residual `H`. To see this without
a support assumption, the Gaussian regression mean is the RKHS
orthogonal projection onto the span of the observation representers;
subtracting it leaves exactly the orthogonal kernel of those rows.
All representers and `H_*` are in the source RKHS.

Every centered Gaussian Radon measure on C6 gives positive mass to each
ball about zero. One proof covers a positive-mass compact set by finitely
many sufficiently small balls, takes two independent samples in the
same ball, and uses that their difference divided by `sqrt(2)` has the
original centered Gaussian law. Cameron-Martin equivalence therefore
gives

    nu{||H-h_*||_C6<epsilon}>0                    (TG37)

for every `epsilon>0`.

There is a small C6 neighborhood of `H_*` with the following relative
property: every field in it satisfying (TG2) and `gamma=q5=0` has a
unique global maximum at zero and `q6<-a/2`. Indeed, a fixed product
chart retains strict transverse concavity. C6 ridge continuity retains
a strictly negative sixth derivative throughout a smaller fixed ridge
interval. Since the lower ridge coefficients through degree five
vanish exactly, Taylor's theorem makes its values strictly below `b`
away from zero. The template's strict gap outside this chart is
preserved by C0 closeness. This proves the relative property at all
physical scales, not just for its sixth jet.

The map `j -> mu(j,c0(j),e0(j))` is continuous near `j_*`, where the
hard block stays uniformly negative. Choose a bounded open neighborhood
`U` of `j_*` of positive finite Lebesgue measure and a fixed residual
event as in (TG37), small enough that every `f00(j,H)` with `j in U`
and `H` in that event lies in the preceding relative neighborhood.
On this product set, `Delta^2` is bounded below, `q6<-a/2`, and
`max f00<=b`. The density `rho(j,c0(j),e0(j))` is continuous and has
a positive lower bound after shrinking `U` to a relatively compact
neighborhood. The integral (TG11) is therefore strictly positive.
This proves `M_0>0` and completes the proof of (TG6).

## 9. Boundaries and exact source identities

The proof establishes an ordered critical-window limit for the stated
fixed spectrum, birth height and orientation. It gives no joint limit,
uniform rate of convergence in `r,tau`, numerical value of `C_E`, or
counting-intensity expansion. The coefficient depends on the actual
global-maximum event under a sixth-order contact law. The stronger
regularity in (TG1) is used in the parabola bound and fixed-chart sextic
continuity, and cube four is used to prove no competing critical point
at the pinned height after the fifth-contact conditioning. Neither
condition is silently inherited from the earlier C4/cube-three theorem.

The density domination, its soft-block cancellation, and C6 convergence
of the actual ridge are included above. There is no remaining unproved
inverse-moment, full-support, or scaled-window-to-global implication in
this author proof. Independent different-family scientific review is
still pending.

The following identities were read from the unchanged predecessor files
in this worktree. A blob/hash identifies bytes, not scientific acceptance.

| Source and role | Git blob | SHA256 |
|---|---|---|
| `all_frame_gaussian_rates_20261028/CRITICAL_WINDOW.md`: (TG4), original contact law and weight | `520e22f219c2a6e63f229fe20755be2188b4ab50` | `16d15a49b5c484205c85b00d10b26c173072c946ee5be7f7da2c1d3a4ce97b17` |
| `cusp_second_order_20261001/PROOF.md`: CU.2--CU.4 and Remark 8.1; existing quartic weight, normalization288, local elder13/27 | `f6df5a7356a54771b0052e42a864a140709903ad` | `cffc1b83ac364da58bd650c3c301ea1babd38e19af54f74010bdc120edce38a8` |
| `elder_cusp_parity_20261002/PROOF.md`: Section 0 (0.1), the reused `Q_1=q5` formula and polynomial `Delta^2 Q_1` | `16a1db0658918057ff741df888c13702763d9919` | `35b9c5943cf35919f2046ba194945ba759be654edf5d5ad77ba17b1f5c5377fd` |
| `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md`: Section 4, distinct cubic off-axis limiting-kernel `k^6` law; cited only | `4d03f110ac82a4d876f97d1910fe997b128c6ca9` | `5faa183452ec548ee1116dd199d250f597afc0fc6de3908b37a6fd4f0dcf8e76` |
