# A finite-radius ten-coordinate Fourier interpolation lemma

Author-source appendix for C127, 2026-10-04 UTC.

Actual analytic author: OpenAI/Codex `/root/next_math_triage`, coordinated by
OpenAI/Codex root session `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`, delegated by
Dylan Roy. This is an author/coauthor contribution, not a nonauthor review.
Exact model variant/build UNKNOWN; organizational independence 0. Scientific
effect NONE. Claim `172330dc-1d1b-49f5-a651-7abe3cecd662`, Work Events748;
native pickup5974918836. No project test or finite control proves this lemma.

## 1. Exact sources and scope

The source cut is Math- commit
`bbe85e270f2c8b747f2d5d9477c86e86e323fe15`, tree
`4087029fb662c31c7239d6114b290a19fcffced5`. The complete files were read from
that native cut and matched to the cached bytes; those cached bytes were
rehashed before this derivation.

| Key | Path at the source cut | Bytes | Git blob | SHA-256 |
|---|---|---:|---|---|
| C107 | `frontiers/moving_remote_collision_20261003/PROOF.md` | 29606 | `596782786a200412a58169440b45d4f5bb36aadf` | `d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df` |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | 40261 | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` |
| SC, context only | `frontiers/spectral_cluster_closure_20260929/PROOF.md` | 25006 | `16c56821b52fd76b0be791622b9c3809eafde75a` | `e971b2cbe50a8a06b47c1219191201e0d1037c9adac23e5e3b7d2051bb70c2eb` |

C107(1), (10), (13), and its Sections4-5 supply the field convention, pin
coordinates, polynomial pin interpolant, separator/Hermite construction and
covariance-duality method. The relevant formulas and their estimates are
reproduced below. P Sections2-4 supply the same positive Fourier model and the
uniform pin-only covariance and conditional-mean interface. No cap theorem,
elder selection, full normalizer, witness-count estimate or persistence
identification is consumed by this interpolation lemma. SC Section7 motivates
the subsequent mixed-count application; no conclusion of that application is
claimed here. The main C127 argument must retain its own exact P/errata/repair,
SC, marked Kac-Rice and count-moment interfaces.

Fix a planar torus X=R^2/(L Z^2), with L>0 fixed, and the centered real Gaussian
field with covariance

    E f(z)f(w) = sum_(n in Z^2) a_n exp(2 pi i n.(z-w)/L),
    a_n = exp(-2 pi^2 |n|^2/L^2) / sum_j exp(-2 pi^2 |j|^2/L^2).

Thus every a_n is strictly positive, and the Fourier coefficients decay fast
enough for all derivative covariances used below. The field is not assumed
rotationally invariant. Directions are observation coordinates, not covariance
symmetries. All constants below may depend on L and this fixed covariance.

Choose any orthonormal frame (u,v), and put M=-ru/2, S=ru/2. Use local physical
coordinates (t,z) along (u,v) near the origin. Let 0<rho<=rho_0, with

    rho_0 <= min(1,L/32),      0<r<=rho/8,
    dist_X(x,0)>=rho.                                           (F1)

When the pin-only mean bound is used, also take r below P's fixed small-radius
threshold. The interpolation and covariance floor themselves require only
(F1). Gradients at the remote point x will be expressed in the fixed Cartesian
coordinates of the torus; an orthogonal re-expression has determinant of
absolute value one and does not affect any asserted bound.

Define a=-r/2, c=r/2 and the six EXACT finite-r pin functionals

    U_r(f) = (
      [f(a,0)+f(c,0)]/2,
      [f(c,0)-f(a,0)]/r,
      [f_t(c,0)-f_t(a,0)]/r,
      (6/r^2)[f_t(a,0)+f_t(c,0)-2(f(c,0)-f(a,0))/r],
      [f_z(a,0)+f_z(c,0)]/2,
      [f_z(c,0)-f_z(a,0)]/r ).                                (F2)

For r>0 these are an invertible transform of the two values and two full
gradients at M,S. Put

    A(f)=partial_v^2 f(0),
    V_x(f)=(A(f),f(x),partial_1 f(x),partial_2 f(x)),
    L_(r,x)(f)=(U_r(f),V_x(f)) in R^10.                       (F3)

**Lemma.** Uniformly over (F1), all x in D_rho and all frames, for every
data vector d in R^10 there is a real trigonometric polynomial phi_d with

    L_(r,x)(phi_d)=d,
    support(phi_d-hat) contained in {|n|_1<=5},
    ||phi_d-hat||_l1 <= C rho^(-9)|d|,
    ||phi_d||_H <= C rho^(-9)|d|.                             (F4)

H is the Gaussian Cameron-Martin space. Consequently

    c rho^18 I_10 <= Cov(L_(r,x) f) <= C I_10.                (F5)

Under the actual Gaussian endpoint regression Q_r at physical k=1, the target
of U_r is (b-r^3/2,-r^2,0,12,0,0). The conditional covariance S_(r,x) of V_x
and its canonical density satisfy

    c rho^18 I_4 <= S_(r,x) <= C I_4,
    p_(V_x,Q_r)(z) <= C rho^(-36)
                         exp(-c|z-mu_(r,x)|^2).              (F6)

In particular the density is at most C rho^(-36) at every target, including
(A,h,0,0). On a fixed compact birth set, |mu_(r,x)| is uniformly bounded for
small r by the separate pin-only interface of P. The conditional covariance
does not depend on the observed birth value. This lemma introduces no tilted
law or new normalizer.

## 2. Periodic separators and a uniform chart

Write omega=2 pi/L. For p in X set

    psi_p(y)=sum_(j=1)^2 [1-cos(omega(y_j-p_j))],
    S_p(y)_j=omega^(-1) sin(omega(y_j-p_j)).                  (F7)

Both are globally defined real trigonometric polynomials. psi_p has value and
first derivative zero at p. Taking minimal coordinate displacements in
[-L/2,L/2] and using 2 t^2/pi^2 <= 1-cos(t) <= t^2/2 for |t|<=pi gives

    c_L dist_X(y,p)^2 <= psi_p(y) <= C_L dist_X(y,p)^2.       (F8)

The elementary derivative bounds are |D psi_p|<=C_L dist_X(y,p) and
|D^j psi_p|<=C_L for j=2,3. Differentiating the reciprocal through order three
therefore gives

    |D^j(psi_p^(-1))(y)| <= C_L dist_X(y,p)^(-2-j),
    0<=j<=3, y!=p.                                         (F9)

For the third derivative, the term psi_p^(-2) D^3 psi_p is bounded initially
by C_L dist^(-4), which is bounded by another L-dependent constant times
dist^(-5), since the torus diameter is fixed. The other terms have the claimed
power directly. No derivative of the distance function is being taken.

For a product q=product_(i=1)^m psi_(p_i), repeated sites allowed, the Leibniz
rule and (F9) imply, on any region where all dist_X(y,p_i)>=c_0 rho,

    |D^j(q^(-1))| <= C_(L,m,c_0) rho^(-2m-j), 0<=j<=3.   (F10)

Every psi_p has frequency support |n|_1<=1 and uniformly bounded Fourier l1
norm, independently of p. Thus a product of m factors has degree at most m
and uniformly bounded l1 norm for fixed m. The same is true of each fixed
order of its derivatives, with constants depending on L,m.

On the coordinate box |y_j-p_j|<L/16, S_p is injective and its derivative and
inverse derivative are uniformly bounded. The inverse is coordinatewise
omega^(-1) arcsin(omega s_j). Its derivatives through order three are bounded
by constants depending only on L; its Lipschitz constant can be taken at most
two. These are LOCAL inverse statements. No global injectivity of S_p is used.

## 3. The stable six-observation pin interpolant

For arbitrary pin data a=(a_0,...,a_5), set

    p_a(t,z)=a_0-r^2 a_2/8+(a_1-r^2 a_3/24)t
                +(a_2/2)t^2+(a_3/6)t^3+z(a_4+a_5 t).        (F11)

Substitution in (F2) gives U_r(p_a)=a exactly. Its coefficients, and its C^3
norm on the physical ball of radius rho/3, are at most C|a| because r,rho<=1.
This local polynomial is an interpolation device; it is not itself asserted
to be periodic or to belong to H.

Here is the Hermite formula used to turn it into a periodic function. If a
C^3 function F(t,z) is defined near the segment from (0,0) to (h,0), h>0, the
polynomial

    P_F(t,z)=b_0+b_1 t+b_2 t^2+b_3 t^3+z(c_0+c_1 t)     (F12)

matches its value and both first derivatives at the two endpoints when

    b_0=F(0,0),                      b_1=F_t(0,0),
    b_2=3[F(h,0)-F(0,0)]/h^2-[2F_t(0,0)+F_t(h,0)]/h,
    b_3=[F_t(h,0)+F_t(0,0)]/h^2-2[F(h,0)-F(0,0)]/h^3,
    c_0=F_z(0,0),                   c_1=[F_z(h,0)-F_z(0,0)]/h.

The apparent inverse powers of h do not cause a bound to diverge. With
g(t)=F(t,0), integration by parts gives

    b_3=h^(-3) integral_0^h t(h-t)g'''(t)dt,
    b_2=(2h)^(-1) integral_0^h g''(t)dt-(3h/2)b_3,
    c_1=h^(-1) integral_0^h F_tz(t,0)dt.                    (F13)

Hence |b_3|<=||g'''||_infinity/6,
|b_2|<=||g''||_infinity/2+h||g'''||_infinity/4, and
|c_1|<=||F_tz||_infinity. The whole coefficient vector has norm at most
C||F||_C3 when h<=1. This argument is uniform through arbitrarily small h,
and uses no common vector-valued Rolle zero.

For the actual pin chart put

    d=S_0(ru/2),   e=d/|d|,   n a unit perpendicular to e,
    h=2|d|,       t=e.(S_0(y)+d),   z=n.S_0(y).             (F14)

The point d is nonzero. To see this quantitatively, put theta=omega r/2. Then

    d_j=(r/2)u_j sinc(theta u_j),
    |d|<=r/2,
    u.d >= (r/2)(1-theta^2/6)>0,                          (F15)

where sinc(0)=1 and theta<=pi/256 by (F1). The pin chart images are -d,d;
their coordinates in (F14) are (0,0),(h,0). The inverse image of their chart
segment is contained in the physical ball |y|<=rho/8: its chart norm is at
most |d|<=r/2<=rho/16 and the inverse Lipschitz constant is at most two.
A small open neighborhood of the segment has inverse image in |y|<rho/3.
All these points lie in the fixed sine-chart domain. Rotating chart coordinates
and translating by d preserves derivative bounds up to fixed constants.

Set q=psi_x. On |y|<rho/3, dist_X(y,x)>=2rho/3, so (F10) with m=1 gives

    ||p_a/q||_C3 <= C_L rho^(-5)|a|.                       (F16)

Compose p_a/q with the inverse chart, using (F14), to obtain F. Apply
(F12)-(F13), and let P denote the resulting polynomial written back in the
two original chart coordinates. Its coefficients are bounded by the right
side of (F16). Define

    phi_0(y)=q(y)P(S_0(y)).                                (F17)

At each pin, P(S_0) and p_a/q have the same physical value and gradient. Indeed,
their chart values and chart gradients agree by construction, and the same
invertible DS_0 and orthogonal chart change convert those gradients to physical
gradients. Multiplication by q therefore gives the value and physical gradient
of p_a. Thus U_r(phi_0)=a exactly. At x, q and its first derivative vanish,
so phi_0(x)=0 and grad phi_0(x)=0.

A polynomial of total degree three in the sine chart coordinates has frequency
support |n|_1<=3. The affine change in (F14) does not increase that degree.
Multiplication by q gives degree at most four. The chart factors and the
bounded affine coefficients have uniformly bounded Fourier l1 norms. Therefore

    ||phi_0-hat||_l1 <= C_L rho^(-5)|a|,
    |A(phi_0)| <= C_L rho^(-5)|a|.                         (F18)

The second estimate follows directly by differentiating a degree-four Fourier
polynomial twice in the unit direction v. It is a physical derivative bound,
not a chart Hessian assertion.

## 4. An exact quadratic correction for the midpoint Hessian

Define the global real trigonometric polynomial

    ell(y)=n.S_0(y).                                       (F19)

By (F14), ell(M)=ell(S)=ell(0)=0. Therefore q ell^2 and its first derivative
vanish at both pins. They also vanish at x because q=psi_x has a second-order
zero there. This correction kills the six pin observations and the remote
first jet exactly, for every finite r in (F1).

Since DS_0(0)=I and ell(0)=0, the product rule gives

    A(q ell^2)=2q(0)(n.v)^2.                              (F20)

There are no terms involving derivatives of q in (F20), because ell^2 and
its first derivatives vanish at the origin. In two dimensions, for orthonormal
(u,v) and (e,n), |n.v|=|e.u|. Equation (F15) implies

    |e.u| >= 1-theta^2/6 >= 1/2,
    2q(0)(n.v)^2 >= c_L rho^2.                            (F21)

This lower bound uses the actual finite-r chart chord and the actual physical
direction v. They are not identified with one another. Either sign of n gives
the same correction and bound; no globally continuous frame selection is needed.

For prescribed scalar alpha, put

    c_a=[alpha-A(phi_0)]/[2q(0)(n.v)^2],
    phi_P=phi_0+c_a q ell^2.                              (F22)

Then (U_r,A,f(x),grad f(x))(phi_P)=(a,alpha,0,0) exactly. By (F18)-(F21),
rho<=1 and the uniformly bounded Fourier norms of q and ell,

    ||phi_P-hat||_l1 <= C_L rho^(-7)(|a|+|alpha|).          (F23)

The added term has degree at most three, so phi_P still has degree at most
four. In particular, a=0, alpha=1 explicitly realizes a nonzero midpoint
transverse Hessian while both pin first jets and the remote first jet vanish.
This proves the required additional functional independence without appealing
to a limiting contact covariance or an unspecified perturbation remainder.

## 5. The remote first-jet dual

To prescribe remote data beta=(beta_0,beta_1,beta_2), set

    q_R=psi_M psi_S psi_0^2.                              (F24)

At either pin, q_R has value and gradient zero. At the origin, psi_0^2 has
a zero of order four, so every derivative of q_R through order three vanishes.
Consequently every smooth multiple of q_R has U_r=0 and A=0. These exact zero
statements remain true despite the small separation between the pins.

At the surviving point x, all four killed-site distances are at least c rho:

    dist_X(x,M),dist_X(x,S) >= rho-r/2 >= 15rho/16,
    dist_X(x,0)>=rho.

Equation (F10) with m=4,j<=1 yields

    |q_R^(-1)(x)|<=C_L rho^(-8),
    |grad(q_R^(-1))(x)|<=C_L rho^(-9).                     (F25)

In a physical chart centered at x, let p(y)=beta_0+beta_vec.(y-x).
Let a_R=(p/q_R)(x) and b_R=grad(p/q_R)(x), and define

    phi_R(y)=q_R(y)[a_R+b_R.S_x(y)].                       (F26)

Here S_x(x)=0 and DS_x(x)=I, so (F26) has value beta_0 and physical gradient
beta_vec at x exactly. It kills U_r,A by (F24). Equations (F25) give

    |a_R|+|b_R| <= C_L rho^(-9)|beta|,
    ||phi_R-hat||_l1 <= C_L rho^(-9)|beta|.                 (F27)

The four separator factors have degree at most four; multiplication by the
affine sine expression adds at most one. Thus phi_R has degree at most five.
No physical affine function outside its local chart is used as a global field;
the final function (F26) is genuinely periodic.

Combining (F22) and (F26) proves the exact right inverse and Fourier-norm bound
in (F4). The construction is linear in the prescribed data for each fixed
choice of geometric parameters. Its bounds hold uniformly in those parameters.

## 6. Cameron-Martin, covariance and actual conditional density

For a real trigonometric polynomial phi=sum c_n exp(2 pi i n.y/L), with
c_(-n)=conjugate(c_n), the Cameron-Martin norm is

    ||phi||_H^2 = sum_n |c_n|^2/a_n.

On the fixed set |n|_1<=5, a_min=min a_n is strictly positive. Hence
||phi||_H<=a_min^(-1/2)||phi-hat||_l1. This proves the last part of (F4).

Let t be an arbitrary nonzero real coefficient vector for the ten observations,
and choose phi_t from (F4). The covariance-representer identity and
Cauchy-Schwarz in H give

    |t|^4 = |(t.L_(r,x))(phi_t)|^2
          <= Var(t.L_(r,x) f) ||phi_t||_H^2
          <= C rho^(-18)|t|^2 Var(t.L_(r,x) f).

This is the lower bound (F5). The upper bound follows from the uniformly
bounded variances of the individual coordinates: the divided differences in
U_r have integral representations in derivatives through order three, whereas
A and the remote coordinates are raw derivatives of order at most two.
For example the fourth coordinate in (F2) equals

    (6/r^3) integral_(-r/2)^(r/2)
                  (s+r/2)(r/2-s) f_ttt(s,0) ds,

an average with a nonnegative kernel of total mass one. The other nontrivial
divided differences are ordinary averages of first or second derivatives.
The rapidly decaying fixed Fourier spectrum bounds all their variances,
uniformly over frames, r, rho and x. No torus rotational invariance is used.

Write the covariance in blocks for (U_r,V_x), and let S_(r,x) be the Schur
complement of the U_r block. For any w in R^4,

    w^T S_(r,x) w
      = min_(z in R^6) (z,w)^T Cov(U_r,V_x)(z,w)
      >= c rho^18 |w|^2.                                  (F28)

Conditioning decreases covariance, so S_(r,x)<=C I_4 as well. This is the
covariance of the canonical Gaussian regression on the actual endpoint pins,
because (F2) is an invertible transform of those observations. It is not the
covariance of a replacement field or of a witness-normalized measure.

The density formula in dimension four now gives

    p_(V_x,Q_r)(z)
      = (2pi)^(-2) det(S_(r,x))^(-1/2)
           exp[-(z-mu_(r,x))^T S_(r,x)^(-1)(z-mu_(r,x))/2]
      <= C rho^(-36) exp[-c|z-mu_(r,x)|^2].                (F29)

Indeed det(S)>=c^4 rho^72. The prefactor exponent36 uses the FOUR remaining
coordinates after the six actual pins have been conditioned on. The upper
covariance bound supplies the exponential factor with a constant independent
of rho. For bounded birth b and physical k=1, P's separate uniform pin-only
inverse covariance and the target (b-r^3/2,-r^2,0,12,0,0) bound the regression
mean uniformly. The ten-coordinate floor is not used to estimate that mean.

Equations (F4)-(F6) follow. All rank and separation bounds were established
for finite r. No passage to a limiting U_0 rank statement was substituted for
the rho-dependent calculation.

## 7. Boundary of the weighted-count application

This appendix supplies a joint density bound for the original endpoint Gaussian
law, before determinant tilting. A later marked Kac-Rice integral may retain a
field mark such as W_r 1{N_R>0}1{K<=T}, but must justify that mark through its
own Borel/finite-measure interface. The norm truncation and the deterministic
A interval must remain inside the same conditional expectation. The density
bound does not assert independence of A, the norm, the endpoint weight or the
remote Hessian. It supplies neither an extra normalizer nor a persistence mark.

In the proposed planar k=1 composition, SC(11)'s contrapositive on the typed
support and rT<=1/(4R), T>=1, gives the explicit interval

    -64R rT^2 <= A <= rT/2.

The upper bound uses the negative-definite maximum endpoint and the Hessian
Lipschitz estimate. The lower bound uses that a critical point in the Rr ball
lies in SC's Rr cylinder. This deduction requires a fixed embedded cylinder;
it is not a statement about growing R. On W_r=0 no such geometric implication
is needed for the marked estimate. Proving that marked estimate, handling its
untruncated tail, converting event mass to counted mass, and preserving the
single full normalizer are separate steps of the main argument.
