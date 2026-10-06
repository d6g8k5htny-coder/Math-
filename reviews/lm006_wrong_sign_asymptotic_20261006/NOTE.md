# LM006: a positive leading coefficient for the actual saddle-transverse sign layer

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, `lm006-sign-asymptotic-20261006-r12`, claim main#229/6009740815.
Scientific effect NONE; organizational-independence credit 0. This is a new
additive author-side analytic proposal requiring its own nonauthor review.
It does not revise historical LM006 proof/review bytes or a scientific register.

## 1. Exact object, result, and prior-work boundary

Use P's normalized periodized Gaussian field in dimension two, side L=24,
with its original coordinate axes. Fix b=6/5, h=r/2, M=(-h,0), S=(h,0), and
condition by canonical Gaussian regression on the SIX prescribed observations

    f(M)=b, f(S)=b-r^3/6, grad f(M)=grad f(S)=0.

Write Q_r for this original pin law. No good event is additionally conditioned
on. At positive r the endpoint variables of E are exactly

    (a_-,a_+,b_-,b_+,c_-,c_+)
       =(f_xx(M)/r,f_xx(S)/r,f_xy(M)/r,f_xy(S)/r,f_yy(M),f_yy(S)).

The original physical determinant/type weight and full normalizer are

    W_r=|det H_M det H_S| 1{H_M<0,det H_S<0}, Z_r=E_Qr W_r,
    T_r=W_r/r^2, z_r=Z_r/r^2, d nu_r=(T_r/z_r) d Q_r.       (1)

N gives the exact continuous formula, including every singular boundary,

    T_r=[(a_-)_- (c_-)_- - r b_-^2]_+
        [r b_+^2-a_+ c_+]_+.                              (2)

Here x_+=max(x,0), x_-=max(-x,0). The event under investigation is ONLY

    E_r={f_yy(S)>=0}={c_+>=0},

not the maximum's sign, elder-partner failure, adjacency, capture or persistence.
All limits below mean r decreases to zero through positive radii; they stay
inside 0<r<=r_*<min(1,24) with r_* sufficiently small. No numerical r_* is given.

Define the one-dimensional spectral probability and raw frequency moments

    rho_n=exp(-2 pi^2 n^2/L^2)/sum_j exp(-2 pi^2 j^2/L^2),
    omega_n=2 pi n/L, m_j=sum_n rho_n omega_n^j,
    delta=m_4-m_2^2, s^2=m_2 delta.                       (3)

These are the EXACT torus moments, not planar substitutions. Full positive
support implies m_2>0 and delta=Var(omega_N^2)>0. All moments are finite.
Let Q, B, D be mutually independent real Gaussians with

    Q ~ N(-m_2 b,delta), B ~ N(0,s^2/4), D ~ N(0,s^2).

The variable B is one HALF of the conditioned f_xxy(0), not that derivative
itself. Define

    J(d,u)=int_0^{d_+} (d-u-t)_+ (u-t)_+ dt, u>=0,
    Gamma=E J(D,B^2), z_0=E (Q_-)^2,
    p_0(0)=exp(-(m_2 b)^2/(2 delta))/sqrt(2 pi delta).

**Theorem (new actual-field asymptotic).** For exactly the object above,

    nu_r(E_r)=C_{L,b} r^3+o(r^3),
    C_{L,b}=p_0(0) Gamma/z_0,       0<C_{L,b}<infinity.     (4)

In particular this sign probability is Theta(r^3), with a strictly positive,
explicit Gaussian-integral coefficient. The coefficient is NOT numerically
evaluated or certified by this packet. If Phi and phi are standard normal
CDF/density and a=m_2 b/sqrt(delta), the optional denominator identity is

    z_0=((m_2 b)^2+delta) Phi(a)+m_2 b sqrt(delta) phi(a).   (5)

E and N already supply endpoint convergence and the full-normalizer limit.
C (#341) already gives the cubic upper bound and an ABSTRACT Gaussian example
attaining cubic order. P sections 6–7 already contain the soft determinant /
boundary-layer mechanism. The new contribution is the product-covariance
split, exact disintegration of THIS field's sign layer, and the strictly
positive leading coefficient for this fixed physical object. It is not a new
generic Gaussian regression method or a first cubic-power argument. This note
does not use C's conditional-density lemma or global claims from P.

## 2. Exact independent line-process decomposition

P's Fourier weights factor along the original axes. Thus its covariance is

    K_L(x,y)=k(x) k(y), k(x)=sum_n rho_n exp(i omega_n x),
    k(0)=1, k''(0)=-m_2, k''''(0)=m_4.                   (6)

Set F(x)=f(x,0), H(x)=f_y(x,0), Q(x)=f_yy(x,0), before conditioning. Smooth
mean-square differentiation of (6), justified by summable spectral moments,
gives for every x,y on the line

    Cov(F(x),F(y))=k(x-y), Cov(H(x),H(y))=m_2 k(x-y),
    Cov(Q(x),Q(y))=m_4 k(x-y),
    Cov(Q(x),F(y))=-m_2 k(x-y),
    Cov(F(x),H(y))=Cov(Q(x),H(y))=0.                     (7)

Consequently the centered Gaussian process

    R(x)=Q(x)+m_2 F(x)

has covariance delta k(x-y) and is independent of the JOINT line processes
(F,H). Every finite family factors by its zero cross-covariance; this also
applies to mean-square derivatives. F and H are themselves independent.
Canonical conditioning on the four axial F observations and the two H values
therefore leaves R unchanged and independent of their conditioned lines.
This is an exact Gaussian-regression statement at every prescribed pin value,
not conditioning a zero-probability event by an informal ratio.

Under the specified pins we have exactly

    c_-=-m_2 b+R(-h), c_+=-m_2(b-r^3/6)+R(h).

Let A_r=(a_-,a_+,b_-,b_+), and put

    U_r=(c_-+c_+)/2=-m_2(b-r^3/12)+(R(-h)+R(h))/2,
    D_r=(c_+-c_-)/r=m_2 r^2/6+(R(h)-R(-h))/r.            (8)

Stationarity and evenness of k give zero covariance of the R average and
difference. They are Gaussian, so U_r and D_r are independent. Both are also
independent of A_r: the four Hessian coordinates use only F and H. Thus

    U_r independent of (A_r,D_r), D_r independent of A_r,
    U_r~N(mu_r,v_r), mu_r=-m_2(b-r^3/12),
    v_r=delta (1+k(r))/2,
    D_r~N(m_2 r^2/6, 2 delta (1-k(r))/r^2).              (9)

For sufficiently small positive r, v_r>=delta/2. These identities hold BEFORE
applying the determinant tilt. No corresponding independence under nu_r is
asserted. In particular one cannot factor expectations under nu_r as though
the tilt preserved the Gaussian process independence.

## 3. The three limiting Gaussian coordinates and the normalizer

The spectral regularity and six-jet positivity required by E are verified by
P section 2. E's original adjusted linear functionals, after imposing the same
pins, are precisely the variables used here. Its limiting conditional law is

    A_r -> (-1,1,-A/2,A/2),
    A=Law(H''(0) | H(0)=H'(0)=0).                       (10)

The axial limiting cubic pin is f_xxx(0)=2, fixed by the actual r^3/6 gap.
The H line is independent of the F line, so no additional axial pin changes A.
The H covariance in (7) gives

    Var H(0)=m_2, Var H'(0)=m_2^2,
    Var H''(0)=m_2 m_4,
    Cov(H''(0),H(0))=-m_2^2,
    Cov(H''(0),H'(0))=Cov(H(0),H'(0))=0.

Its conditional mean is zero, and its conditional variance is

    m_2 m_4-(-m_2^2)^2/m_2=m_2 delta.                   (11)

Thus B=A/2 has variance s^2/4. From k(r)=1-m_2 r^2/2+o(r^2), (9) gives
D_r -> D~N(0,s^2). The independence in (9) persists in the limit, yielding

    (A_r,D_r) -> (-1,1,-B,B,D), B independent of D.       (12)

Also U_r -> Q~N(-m_2 b,delta), independent of B,D. The raw six-pin contact law
of f_yy(0) is therefore this Q. This re-identifies the actual scalar coordinate
through (7), not a numerical replacement of its law by N(-b,2).

E gives bounded means/covariances of A_r. Formula (9) bounds the mean/variance
of D_r. Hence every fixed moment of ||(A_r,D_r)|| is uniformly finite for small
r, by its finite-dimensional Gaussian law, including singular covariance.
There is no uniform inverse for the entire six-endpoint covariance: it becomes
singular at contact. No rate for a covariance square root is assumed.

We consume the already established E/N normalizer interface, not a repeat of
its determinant/type/uniform-integrability proof:

    z_r=Z_r/r^2 -> z_0=E (Q_-)^2>0.                     (13)

The strict positivity follows from the nondegenerate Gaussian Q; finiteness
follows from its second moment. Formula (5), if used, follows by integrating
(m+sigma x)^2 on x<-m/sigma with m=-m_2 b and sigma^2=delta. This normalizer
is still the FULL normalizer in (1), not conditioned on E_r.

## 4. Exact finite-radius disintegration of the sign event

Let p_r be the density of U_r in (9). Conditional on (A_r,D_r)=(a,d), change
only the scalar integration variable by c_+=r t. Then

    c_-=r(t-d), U_r=r(t-d/2), dU_r=r dt.

On E_r, a positive maximum determinant forces c_-<0, hence 0<=t<d. When
d<=0 the entire tilted sign weight vanishes. By (2), for 0<=t<=d_+,

    T_r=r^2 Psi(a,d,t),
    Psi(a,d,t)=[(a_-)_- (d-t)-b_-^2]_+ [b_+^2-a_+ t]_+.

Therefore, EXACTLY for each sufficiently small positive r,

    N_r:=E_Qr[T_r 1_{E_r}]
      =r^3 E int_0^{(D_r)_+} Psi(A_r,D_r,t)
                              p_r(r(t-D_r/2)) dt.       (14)

Tonelli applies to nonnegative integrands. The r^3 consists of TWO factors r
from the normalized determinant factors and ONE factor r from scalar density
integration. It is not the determinant of the full six-variable scaling map,
and there is no additional pin density or adjacency factor. Type-boundary
points carry zero weight and do not affect (14).

The two laws in this expectation are the UNTILTED Gaussian laws specified in
(9). Formula (14) does not replace finite-r density by a limiting density
before integration or assume a uniform density for all endpoint coordinates.

## 5. Rigorous limit of the rescaled numerator

For small r, sup_x p_r(x)<=1/sqrt(pi delta), and p_r(x)->p_0(0) as (r,x)->(0,0).
This follows directly from the continuous mean and positive limiting variance
in (9). On each compact set of (a,d), the integrand in (14), after integration
on [0,d_+], converges uniformly to

    p_0(0) int_0^{d_+} Psi(a,d,t) dt.

Positive part is continuous, and the integration interval has bounded length
on such a compact set. No assertion of uniform convergence over all d is used.

For all real a,d and 0<=t<=d_+, the elementary envelope is

    0<=Psi(a,d,t)
      <=|a_-|(d_+-t)(b_+^2+|a_+|t).

Consequently the integral including p_r is bounded by

    (pi delta)^(-1/2) |a_-|
       [b_+^2 d_+^2/2+|a_+| d_+^3/6].                   (15)

This is a fixed polynomial-growth bound of degree five. The uniform Gaussian
moments from section 3 imply a bounded SECOND moment of that envelope.
They also make its contribution outside any growing Euclidean ball uniformly
tend to zero (for example combine Cauchy–Schwarz with a uniform second-moment
tail bound on (A_r,D_r)). Truncate with a continuous compact cutoff, apply
(12) and compact uniform convergence there, and then let the cutoff radius
increase. This proves convergence of expectations in (14), not merely
pointwise convergence or convergence in distribution:

    N_r/r^3 -> p_0(0) E int_0^{D_+}
                         (D-B^2-t)_+ (B^2-t)_+ dt
             =p_0(0) Gamma.                             (16)

Thus the actual physical numerator has the DIFFERENT power

    E_Qr[W_r 1_{E_r}]=r^2 N_r
       =p_0(0) Gamma r^5+o(r^5).                        (17)

Dividing (16) by the positive limit (13) proves (4). The proof does not require
an O(r) error for every other endpoint coordinate: its first-order random
transverse DIFFERENCE is explicit, and convergence plus bounded Gaussian
moments of A_r suffices for the leading coefficient.

## 6. Closed elementary inner integral, finiteness and strict positivity

For u>=0, J(d,u)=0 if u=0 or d<=u. If d>u>0, set

    ell=min(u,d-u), M=max(u,d-u).

The interval where both factors are positive is precisely 0<t<ell. Integrating
the quadratic, without dropping either threshold, gives

    J(d,u)=u(d-u)ell-d ell^2/2+ell^3/3
          =ell^2(3M-ell)/6.                             (18)

For example J(2,1)=1/3 and J(3,1)=5/6. Formula (18) is symmetric in u and
d-u where both are nonnegative. It is homogeneous of degree three in (d,u),
not in (d,B). It must not be extended as an unclipped polynomial to d<=u.
An optional completely explicit coefficient representation is

    Gamma=int_R int_R J(x,beta^2)
             [exp(-x^2/(2s^2))/sqrt(2 pi s^2)]
             [2 exp(-2 beta^2/s^2)/sqrt(2 pi s^2)] dx d beta. (19)

The factor 2 in the B density is required by Var(B)=s^2/4.
The degree-five envelope (15) at a=(-1,1,-B,B) proves finiteness.

For strict positivity use a fixed positive-probability rectangle, not a sampled
positive value. When

    1/2<=B<=3/4, 1<=D<=5/4, 0<=t<=1/8,

one has D-B^2-t>=5/16 and B^2-t>=1/8. Thus

    J(D,B^2)>=5/1024

throughout that rectangle, and independence gives

    Gamma >= (5/1024) P(1/2<=B<=3/4) P(1<=D<=5/4)>0.      (20)

Each Gaussian assigns positive mass to its interval since s^2>0. Together with
p_0(0)>0 and 0<z_0<infinity, this proves the strict coefficient assertion.
Equation (20) is symbolic and is NOT an outward numerical torus certificate.

## 7. Tests, assumptions that cannot be discarded, and release boundary

`sign_coefficient.py` and `test_sign_coefficient.py` use exact rational arithmetic
and the standard library. Their twelve methods check the clipped integral
against separate root-split polynomial integration, thresholds, homogeneity,
the positive rectangle, exact physical determinant/type scaling, average /
difference covariance, pin-target drift, and complete contact regression for
three FINITE PRODUCT spectra. That regression is computed from the six-by-six
pin Gram and the three-target cross-covariance, rather than inserted from the
answer. It recovers diag(delta,m_2 delta,m_2 delta) for (Q,2B,D).

Those finite spectra are diagnostic models, not the exact infinite torus.
A separate nonproduct finite spectral example has
Cov(Q+E[Y^2]F,F_xx)=E[X^2Y^2]-E[X^2]E[Y^2]=9/4, not zero. Thus positivity of
all relevant marginal variances alone cannot justify (7)'s independence.
The actual product identity (6), along the ORIGINAL torus axes, is essential.
No arbitrary orientation, nonproduct covariance, varying mark, growing period
or dimension is included in (4).

Before implementation the twelve-method suite failed with twelve assertions
identifying the missing module. Final normal and optimized runs pass all twelve.
Four isolated source corruptions (doubling (18), losing the B/2 scale, reversing
the pin drift, losing the physical r^2 multiplier) make the complete tests fail
by assertions in both modes. These are finite diagnostic controls, not a
computer proof of (16), independent mathematical review, or a Lean execution.

P supplies ONLY the model/pins/spectral positivity/regularity consumed here;
E supplies the conditional endpoint interface; N supplies the exact physical
weight/normalizer interface; C is credited prior upper-bound/sharpness work.
All immutable paths, commits and roles are in SOURCES.json. No earlier proof,
review, workflow, source manifest or scientific register is modified.

A new source-bound nonauthor mathematical read is required on the product-line
split, prescribed-pin means, independence before tilt, exact layer Jacobian,
Gaussian limit and uniform-integrability argument, and strict positivity.
General existing CI does not automatically execute this standalone checker or
formalize this new theorem. After review, an eligible separate integrator must
reconcile the actual current base and its own required checks. No author
self-merge, scientific flag change, full-program closure or claim about elder
failure/capture/persistence follows from this sign-coordinate asymptotic.
