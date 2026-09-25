# Typed contact kernel: angular suppression, exact shape mass and the small-gap limit

**Object:** OA-KERNEL-TAIL-SMALL-GAP-20260925-v1. **Author:** OpenAI / ChatGPT.
**Disposition:** new author-side analytic derivations. Separate review required. No scientific-status promotion.

## 1. Source contract and what is newly derived

Input is the six-pin cubic contact kernel of Math- PR25 at immutable
`ad35e46d15c2815c36746442808a1626a9724e8a`,
`reviews/collision_mechanism_20260925/NOTE.md`, Section C.
The expanded attached exposition is `TRANSVERSE_CONTACT_ASYMPTOTIC.md`.
The input Gaussian contact-asymptotic theorem is not independently accepted by this note.
The results below are proved for its explicit limiting kernel. They do not, by themselves,
provide finite-r uniformity as the transverse coordinate or gap mark tends to zero.

Model: the exact variance-one normalized L-periodized Gaussian covariance,
fixed L>0 in dimension two; all orthonormal frames; birth b in a fixed compact.
The contact observations are

    U0=(f,fx,fxx,fxxx,fz,fxz)_0=(b,0,0,12k,0,0), k>0.

Write the unpinned contact derivatives as

    a=fzz(0), q=fxxz(0), c=fxzz(0), d=fzzz(0).

The original six finite-r pins must precede blow-up. In the normalized cubic,
M=(-1/2,0), S=(1/2,0), heights0,-k, and X=(u,v), v!=0,
with third height -k*theta, 0<theta<1, the exact solution is

    q=6k(w-2u)/v,
    c=12k(u^2-u*w+1/4)/v^2,
    d=(6k/v^3) R(u,w,theta),
    R=-2u^3-(3/2)u-1+2theta+3w(u^2-1/4).                (1.1)

These are the same solved jets as PR25, expressed in its type variable
w=(qv+12ku)/(6k); the Jacobian is |dq/dw|=6k/|v|.

Define positive determinant factors on the desired endpoint-type region:

    P_M=4theta-(w+1)^2,
    P_S=(w-1)^2-4(1-theta),
    P_X=(w+1-2theta)^2+4theta(1-theta),
    P=P_M P_S P_X.                                      (1.2)

The region is

    0<theta<1,
    I_theta=(-1-2sqrt(theta), 1-2sqrt(1-theta)).          (1.3)

The actual Hessian determinants are (9k^2/v^2)P_M,
-(9k^2/v^2)P_S, -(9k^2/v^2)P_X. In particular the witness is a saddle
throughout this open contact region. The unscaled density coordinate a is zero;
the scaled limit of the finite-r transverse Hessian a_r/r is generally nonzero.
Those two quantities must not be confused.

Let g(a,q,c,d) be the conditional Gaussian density given U0, and let

    m2a=E[a^2 1{a<0}|U0], z0=36k^2 m2a.

PR25's saddle kernel, after the change q to w, is exactly

    Lambda_1(u,v;b,k,E)
      = [104976 k^8/(z0 |v|^13)]
          integral_0^1 integral_(I_theta) P(w,theta)
             g(0,q(w),c(w),d(w)) dw dtheta.             (1.4)

Here E denotes the frame, not a spatial integration set. The factor104976 is
24*6*9^3. The 24k comes from height/contact density, 6k from dq/dw, and k^6
from the three determinants. Division by z0 removes two powers of k.

## 2. A proved near-axis bound for the limiting kernel

Fix a scaled annulus A0<=sqrt(u^2+v^2)<=B, 1<A0<B<infinity.
For sufficiently small |v|, |u|>=A1>1. For k in (0,kmax], uniformly in b/frames,

    0<=Lambda_1 <= C k^6 |v|^-13 exp[-c k^2/v^2].        (2.1)

The constants may depend on the fixed model, annulus, birth compact and kmax.
When k>=kmin>0 this is super-algebraically small as v tends to zero.

Proof. Positive conditional jet covariance on the compact frame set yields
uniform Gaussian decay. The even/odd decomposition proved in Section4 shows
that the odd-jet mean is k times a bounded vector. The corrected critical-gradient
identity is

    u*v*q+(v^2/2)c=-6k(u^2-1/4).

Cauchy-Schwarz therefore gives

    q^2+c^2 >= 36k^2(u^2-1/4)^2 / [v^2(u^2+v^2/4)]
              >= c0 k^2/v^2.                            (2.2)

The mean shift changes Gaussian decay by only exp(C k^2), absorbable for k<=kmax.
On (1.3), |w|<3 and 0<theta<1, so P and the type-region area are bounded.
Formula(1.4), z0=36k^2m2a and a positive lower bound on m2a prove(2.1).
This proof bounds the FULL four-jet density, not merely a marginal.

Define Lambda_1(u,0)=0. For k in a fixed compact positive interval it is a continuous
extension and its value vanishes faster than every power of |v|. We do not infer
all derivative bounds merely from a value estimate.

An explicit tail primitive is useful for certified truncation once C,c are enclosed:

    integral_0^epsilon v^-13 exp(-c/v^2) dv
      = Gamma(6,c/epsilon^2)/(2c^6)
      = [5!/(2c^6)] exp(-c/epsilon^2)
           sum_(j=0)^5 (c/epsilon^2)^j/j!.               (2.3)

For a rectangular u-range of length at most2B and both signs of v, multiply
this by4B and the envelope constant. The mathematical formula is exact;
`axis_tail_integral` evaluates it in floating point only and is not an enclosure.

## 3. Stronger suppression on the saddle side of the axis

For u>=A1>1 an exact identity is

    R=-2(u-1/2)^3+3(u^2-1/4)(w-1)-2(1-theta).           (3.1)

All three terms are nonpositive on the type support and the first is strictly
negative. Hence

    |d| >= 12k(u-1/2)^3/|v|^3,

and Gaussian decay improves(2.1) to

    Lambda_1 <= C k^6 |v|^-13
                    exp[-c k^2(u-1/2)^6/|v|^6].         (3.2)

This is a directional contact-kernel result. It must not be silently exported to
u<-1. For example u=-2, theta=1/2, w=-76/45 lies in the desired type region and
has R=0. The d-channel may then cancel, although the joint q,c bound(2.2) remains.

## 4. Parity factorization and an exact sixth-order small-gap law

A real stationary covariance satisfies K(h)=K(-h). Same-point even-total-order
and odd-total-order derivatives therefore have zero cross-covariance. Joint
Gaussianity makes the two blocks independent. This remains true in every frame;
full rotational invariance is unnecessary.

The endpoint contact constraints split into an even block (f,fxx,fxz)=(b,0,0)
and an odd block (fx,fxxx,fz)=(0,12k,0). Consequently, conditioned on U0,

    a ~ N(mu_a(b,E),sigma_a(E)^2),
    T=(q,c,d) ~ N(k*m(E),Omega(E)),
    a independent of T.                                 (4.1)

The odd covariance Omega is positive definite and independent of b,k. Define

    p_a0 = density of a at zero,
    C_odd=(2pi)^(-3/2)det(Omega)^(-1/2),
    j(u,v,w,theta)=(q,c,d)/k,
    Q_E=(j-m)^T Omega^-1(j-m)>=0.

Then(1.4) becomes the exact representation

    Lambda_1 = [2916 p_a0 C_odd/m2a] k^6 |v|^-13
        integral_0^1 integral_(I_theta) P exp[-k^2 Q_E/2] dw dtheta. (4.2)

For each fixed (u,v) with v!=0, dominated convergence as k down to zero gives

    Lambda_1 ~ C_L(b,E) k^6 |v|^-13,                     (4.3)

where the coefficient is independent of u and

    C_L(b,E) = (8875008/35) p_a0 C_odd/m2a > 0.          (4.4)

This concerns the already-defined LIMITING contact kernel. It does NOT exchange
k down to zero with the original r down to zero limit.

### Exact type-region mass

Reverse the order of integration in(1.3). The domain is the union

    -3<w<-1, (w+1)^2/4<theta<1,
    -1<w<1, 1-(w-1)^2/4<theta<1.

The total area is2. Exact polynomial integration gives

    integral_left P = 77248/945,
    integral_right P = 704/135,
    J=integral P = 27392/315.

Thus 2916 J = 8875008/35. These rational identities are checked by multiplying
three determinant factors and integrating their polynomial, not by embedding
J as an implementation answer.

### Uniformity boundary and noncommuting limits

For bounded u and 0<|v|<=1, Q_E<=C_B |v|^-6 over the compact type domain.
Because P>=0,

    exp[-C_B k^2/|v|^6]
      <= Lambda_1 / [C_L k^6 |v|^-13] <= 1.             (4.5)

The small-gap expansion is uniform when k^2/|v|^6 tends to zero, i.e.
|v| is much larger than k^(1/3). This is a sufficient regime, not an exhaustive
phase diagram. For every fixed k>0 the kernel instead tends to zero at the axis.
The fixed-v small-k coefficient grows like |v|^-13. Therefore the small-k limit
cannot be integrated through v=0 using its pointwise leading term.

For any fixed off-axis chart |v|>=eta, and beta<7, one may bound the particular
contact-kernel negative moment

    integral_0^epsilon k^-beta Lambda_1 dk <= C_eta epsilon^(7-beta)/(7-beta). (4.6)

At beta=2/3 the power is19/3. This controls THIS off-axis witness correction;
it does not establish the needed small-mark moment of the full persistence-pair
intensity, nor a global lifetime law.

### Bargmann-Fock diagnostic, not a finite-volume substitution

For the unperiodized covariance exp(-|h|^2/2), the endpoint contact law is

    a~N(-b,2),  T~N(0,diag(2,2,6)).

Here

    p_a0 C_odd = exp(-b^2/4)/(16sqrt(3)pi^2),
    m2a=(b^2+2)Phi(b/sqrt(2))+b*sqrt(2)*phi(b/sqrt(2)).

At b=0, C_L=184896sqrt(3)/(35pi^2), approximately927.086705814.
This is NOT the persistence-lifetime coefficient and is NOT the SIDE24 value.

## 5. Remove the free-Gaussian-jet quadrature analytically

For fixed theta the vector j is affine in w: j=l*w+h. Complete the square:

    Q_E=A w^2+2B w+C,
    A=l^T Omega^-1 l>0, B=l^T Omega^-1(h-m),
    Q_E=A(w-mu)^2+D, mu=-B/A, D=C-B^2/A>=0.

The polynomial P has degree6 in w. Expanding it about mu reduces its integral
to the seven centered Gaussian moments

    M_n(a;L,U)=integral_L^U x^n exp(-a*x^2)dx,
    a=k^2 A/2,
    L=lower(I_theta)-mu, U=upper(I_theta)-mu.

Their exact recurrence is

    M0=sqrt(pi)/(2sqrt(a))*[erf(sqrt(a)U)-erf(sqrt(a)L)],
    M1=[exp(-aL^2)-exp(-aU^2)]/(2a),
    Mn=[L^(n-1)exp(-aL^2)-U^(n-1)exp(-aU^2)]/(2a)
                +(n-1)M_(n-2)/(2a), n>=2.              (5.1)

Thus the two-dimensional (theta,w) quadrature in PR25 reduces exactly to a single
theta integral. The change theta=sin^2(phi) gives endpoints
-1-2sin(phi), 1-2cos(phi), avoiding endpoint square roots.

The included floating-point helper checks this recurrence on moderate test cases
against independent Simpson evaluation. Extreme tails and short intervals can lose
precision; certified finite-L computation still requires outward arithmetic and an
error enclosure. No numerical continuum certificate is claimed.

## 6. Attribution and boundaries

The parity factorization is standard Gaussian calculus; Gaussian moment integration
is classical. The new project-specific content is the exact type-region polynomial
mass, its sixth-order small-gap consequence for this pin-compatible kernel, the
one-sided |v|^-6 exponential penalty, and the source-explicit use in the annulus bridge.
No worldwide novelty is claimed.

Related primary sources: Gass–Stecconi, arXiv:2305.17586v2 (multi-point interpolation
and Kac-Rice determinant renormalization); Armentano–Azais–Leon,
arXiv:2304.07424v3 (marked expected-integral framework); Muirhead,
arXiv:1901.11336 (shrinking-height-window critical-point estimates). Those papers
provide context, not the specific conditional kernel or its acceptance.
