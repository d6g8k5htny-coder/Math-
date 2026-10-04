# Quantitative planar soft-jet transfer under the actual determinant weight

Object: C92-PLANAR-COMPACT-SOFT-JET-WEIGHTED-TRANSFER-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, acting for Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; nonauthor technical review pending.
Personal reading PENDING; organizational independence 0; scientific effect NONE.

This proves an O(r) comparison of finite measures on a bounded soft-Hessian
layer, and a determinant-weighted growing-window Taylor-failure estimate on
its r^3 probability scale. The measures keep the actual endpoint typing and
the FULL weighted normalizer. This is neither total variation of field laws
nor a persistence-identification theorem.

## 0. Exact interfaces and scope

Fix the planar torus R^2/(L Z^2), L>0 fixed, and the centered variance-one
Gaussian field with covariance

    K_L(z)=sum_{n in Z^2} exp(-|z+Ln|^2/2)
           / sum_{n in Z^2} exp(-|Ln|^2/2).

All constants may depend on L and on the stated fixed cutoffs. No uniformity
as L varies, no higher-dimensional transfer and no general-covariance claim
is made. Take birth b in a fixed nonempty compact set B0 in R, gap mark k=1,
and any orthonormal frame (u,e), including either orientation. Coordinates
(x,z) refer to the periodic lift in that frame. All assertions below are
uniform in b in B0 and in the frame, for 0<r<=r0 sufficiently small.

The parent [P] is imports/lifetime_parent_20260925/
UNIFORM_MATRIX_CAP_AND_LIFETIME.md, blob
dfed3b8d318a3ab1950957f393307733a4bef3f2, SHA256
9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7.
It is consumed with congruence erratum E1 (blob213594d6...), section9 repair
E2 (blobfe9b9ce4...), and reconciliation (blob75da2597...), not as its old
unreconciled header. [P] sections2–5 provide full positive Fourier spectrum,
exact pin coordinates, Gaussian regression moments, and the full normalizer
floor. Its topology and selection conclusions are not used here.

[R] is frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md, blob
247b3ecf80bfbe896948d5d489b2d5842a81c481, SHA256
380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a.
We use its centered-observation estimates (R2)–(R4), filtered determinant
estimate (R6), and full normalizer estimate (R10), at k=1 and compact births.
Their needed arguments are supplied below. The later full-depth review is
blob529c5264...; [P]'s nonauthor review is blobbc11369c.... Complete identities,
bytes and source paths are in SOURCE_IDENTITIES.json. The source tree ref is
e8c76a4080e8e8be3dd9f613006263be6d53bad3 in d6g8k5htny-coder/Math-.

[C91] is main229 comment5963566666, 12433 bytes, SHA256
74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa;
full nonauthor review comment5963668996, SHA256
0c472af06e13f564d44c1723b5492c6c60681000f1f00d653b2bbb5f2e992eda.
Only its C4 Taylor theorem (W4)–(W5) is used. Neither A2's proposed trap nor
any QS/maximin/pairing implication is an input to this note.

The qualitative soft-fold limit already supplies a disintegration strategy.
The new assertion here is a quantitative, polynomial-weighted L1 rate for
the actual finite-jet measure and the corresponding rare-layer failure bound.
Uniform C4 moments under the full tilted law alone are already in [P].

## 1. Measures and theorem

Put M=(-r/2,0), S=(r/2,0). Let Q_r be the continuous Gaussian regression law
at f(M)=b, f(S)=b-r^3, grad f(M)=grad f(S)=0. Define

    W_r=|det H_M det H_S| 1{H_M negative definite, index(H_S)=1},
    Z_r=E_{Q_r} W_r,       Q_r^W=(W_r/Z_r) Q_r,
    A=f_zz(0), t=(gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)),
    lambda=-A/r, |t|=|gamma|+|B1|+|C3|,
    N=1+max_{|alpha|<=4} sup_torus |D^alpha f|.

The index counts strictly negative eigenvalues; W_r is zero on singular
endpoints. Take a fixed 0<Lambda<infinity and let D_Lambda=[-Lambda,Lambda]
times R^3. Lambda is not allowed to grow with r in this theorem. On this
space define the finite measure

    mu_r(E)=r^(-5) E_{Q_r}[W_r 1{(lambda,t) in E}].             (J1)

Thus the restriction to the soft layer is part of E's domain. It is not a
renormalization of Q_r. No pin density or factor12 is included in mu_r.

Let U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0), v_0=(b,0,0,12,0,0).
Write rho_0(a,t) for the JOINT density of (A,t) conditional on U_0=v_0.
Set h_+=max(h,0), and

    w_lambda(t)=(6lambda+3B1-gamma^2/4)_+
                   (6lambda-3B1+gamma^2/4)_+,
    g_0(lambda,t)=rho_0(0,t) w_lambda(t),
    m_Lambda=integral_{D_Lambda} g_0,
    z_0=36 E[A^2 1{A<0} | U_0=v_0].                         (J2)

In particular rho_0(0,t) includes the marginal density of A at0. Replacing
it by the normalized conditional density of t given A=0 loses a factor.
The parameters b and frame in rho_0, m_Lambda and z_0 are suppressed, not
averaged out.

**Theorem J.** After choosing a common r0>0, mu_r has a density g_r, and for
every fixed finite q>=0 there is C_{Lambda,q}<infinity such that

    integral_{D_Lambda} (1+|t|)^q |g_r-g_0| <= C_{Lambda,q} r. (J3)

Here weighted total variation means precisely this L1 expression, without
an implicit factor1/2. Uniformly over the fixed parameters,

    0<m_*<=m_Lambda<=m^*<infinity,  0<z_*<=z_0<=z^*<infinity,
    z_r=Z_r/r^2,  |z_r-z_0|<=Cr,  z_r>=z_*/2.             (J4)

For the finite measure eta_r(E)=r^(-3)Q_r^W((lambda,t) in E),

    eta_r=mu_r/z_r,
    integral_{D_Lambda}(1+|t|)^q |g_r/z_r-g_0/z_0|<=C r,
    Q_r^W(|lambda|<=Lambda)
          =r^3 m_Lambda/z_0+O(r^4).                      (J5)

All constants in (J3)–(J5) may depend on L, B0, Lambda and q; none is claimed
numerically evaluated. This is a local finite measure on D_Lambda, not a
probability density on all lambda. The limiting density is zero for
lambda<=0, although the finite-r measure was restricted symmetrically.

For the Taylor statement put

    F_r(X,zeta)=(f(rX,r zeta)-b)/r^3,
    G=2X^3-3X/2-1/2+(gamma/2)(X^2-1/4)zeta
          -(lambda/2)zeta^2+(B1/2)X zeta^2+(C3/6)zeta^3,
    E_r=F_r-G,    K0=167/192, K1=635/384, K2=115/48.

Let |E_r|_j denote the maximum of all exact-order-j coordinate derivative
suprema on |X|,|zeta|<=w. For any finite p>=1, deterministic epsilon>0,
w>=1 with 2rw<=L/4, and j=0,1,2,

    Q_r^W(|lambda|<=Lambda, |E_r|_j>epsilon)
      <= C_{Lambda,p} r^3 (K_j r w^(4-j)/epsilon)^p.        (J6)

The statement holds pointwise in deterministic epsilon,w, so they may be
chosen as functions of r. If w=r^(-beta), epsilon=r^eta with beta,eta>=0
and 4beta+eta<1, a union over the three derivative orders gives

    Q_r^W(|lambda|<=Lambda, max_{0<=j<=2}|E_r|_j>r^eta)
      <= C_{Lambda,p} r^[3+p(1-4beta-eta)] = o(r^3).        (J7)

Constants depend on p; this does not assert an exponential tail or permit
p to grow with r. By (J5) the conditional failure probability given the
soft layer is O(r^[p(1-4beta-eta)]). Random jet-dependent tolerances require
additional inverse-margin estimates and are not covered by (J6)–(J7).

## 2. Uniform Gaussian facts at the actual ten observations

Use the exact centered observations, with a=-r/2 and c=r/2,

    U_r=((f(a)+f(c))/2, (f(c)-f(a))/r,
          (f_x(c)-f_x(a))/r,
          (6/r^2)[f_x(a)+f_x(c)-2(f(c)-f(a))/r],
          (f_z(a)+f_z(c))/2, (f_z(c)-f_z(a))/r).

Their target is v_r=(b-r^3/2,-r^2,0,12,0,0). For r>0 this is an invertible
linear change of the six original pin observations. At r=0 it has the
continuous extension U_0 above. Append (A,t) and write V_r=(U_r,A,t).
At contact its ten entries are precisely the ten distinct planar derivative
functionals through order3. There is no duplicated functional.

The periodized covariance has positive Fourier coefficients a_n for every
n in Z^2, with sum sqrt(a_n)(1+|n|)^s finite for every finite s. If a real
linear combination of those ten contact jets has variance zero, its
Fourier multiplier P(2pi i n/L) vanishes for every n. P is a polynomial
of degree at most3, expressed in the chosen frame. A polynomial vanishing
on all integer lattice points is zero: fix the second coordinate and use
the univariate polynomial zero theorem in the first, then apply it to each
coefficient polynomial in the second. Rotation of coordinates is an
invertible polynomial substitution, so all ten coefficients are zero.
Consequently Gamma_0=Cov(V_0) is positive definite in every frame.

The frame space O(2) is compact, Gamma_0 is continuous there, and therefore
its smallest eigenvalue has a positive minimum and its largest a finite
maximum. Centered differences give V_r-V_0=O(r^2) in every finite L^p;
the appended entries are unchanged. In particular the fourth row is
f_xxx(0)+(r^2/40)f_xxxxx(0)+O(r^4). Fourier summability controls these
estimates, as well as their cross-covariances with any fixed derivative of
the field, uniformly over position and frame. Thus, after reducing r0,

    cI<=Gamma_r<=CI,   Gamma_r-Gamma_0=O(r^2),
    Gamma_r^(-1)-Gamma_0^(-1)=O(r^2).                     (J8)

This is full-spectrum positivity plus continuity, not a numerical grid or
a finite-mode test. The same estimates hold for the U-block. Schur
complement formulas then imply that (A,t)|U_r=v_r has a uniformly positive
four-dimensional covariance, bounded mean, and covariance/mean differences
O(r^2) from contact. The mean assertion uses compact b and
v_r-v_0=O(r^2). Let its joint density be rho_r(a,t).

For |lambda|<=Lambda, Gaussian interpolation yields

    rho_r(-r lambda,t)<=C_Lambda exp(-c|t|^2),
    |rho_r(-r lambda,t)-rho_0(0,t)|
       <=C_Lambda r(1+|t|)^2 exp(-c|t|^2).              (J9)

For completeness, interpolate the conditional covariance and mean on their
straight segment. Uniform ellipticity persists on the segment. Differentiating
the Gaussian density gives that density times a polynomial of degree at most2
in (a,t), with coefficients O(r^2). The means are bounded, so every density
on the segment is bounded by C exp(-c|(a,t)|^2) after reducing c. The remaining
shift from a=0 to a=-r lambda is of size at most rLambda; its derivative is
density times an affine polynomial, again with a common Gaussian majorant in
t. Integration of both derivatives proves (J9), retaining r rather than r^2
because of the soft-coordinate shift. The l1 norm |t| is equivalent to the
Euclidean norm used in this calculation.

We will also need the field law conditional on V_r=(v_r,-r lambda,t), not
an independent replacement of its jets. The exact Gaussian regression has
mean Cov(f,V_r)Gamma_r^(-1)(v_r,-r lambda,t). Uniform bounds on four position
derivatives of this covariance, (J8) and compact b imply that its C4 norm
is at most C_Lambda(1+|t|). The centered residual has C4 moments of every
finite order uniformly in r and frame. One direct proof conditions the
real Fourier coefficients: each centered conditional coefficient has variance
no larger than its original variance. Minkowski's inequality and
sum sqrt(a_n)(1+|n|)^4<infinity bound the L^p norm of the sum of derivative
suprema. Independence among residual coefficients is not required. The
series converges in C4 in these L^p norms. Therefore for any finite p>=1,

    E[N^p | U_r=v_r,A=-r lambda,t]
              <=C_{Lambda,p}(1+|t|)^p.                (J10)

These formulas define continuous regression versions for every finite target.
Under them the pin and midpoint observations hold almost surely: each
conditioned linear observation has its specified mean and zero residual
variance. No independence between N and t, or between N and endpoint
Hessians, is being assumed. Smoothness follows from the same Fourier
summability. All disintegrations below use these versions.

## 3. Keep the actual typed determinant, including its boundary

At the two pins the cubic Hessians are

    L_M=[[-6,-gamma/2],[-gamma/2,-lambda-B1/2]],
    L_S=[[ 6, gamma/2],[ gamma/2,-lambda+B1/2]].         (J11)

Since k=1, D^2 F_r=H/r. Apply [C91] at w=1, reducing r0 so 2r<=L/4.
The N in this note dominates its C4 bound. Each entry of H_i/r-L_i has
absolute value at most (115/48)rN, hence

    ||H_i/r-L_i||_op <= (115/24)rN, i=M,S.             (J12)

There is no assumption that the eigenvalues of L_i stay away from zero.
For a symmetric 2 by 2 matrix put

    F_j(H)=|det H|1{index(H)=j}, zero on singular H.

For symmetric X,Y the filtered determinant satisfies

    |F_j(X)-F_j(Y)|<=2 max(||X||,||Y||)||X-Y||.         (J13)

If both indices equal j, use the determinant difference bound and
|| |a|-|b| ||<=|a-b|. If neither contributes, the assertion is immediate.
If only one contributes, the segment reaches a singular matrix; apply the
determinant difference bound between the contributing endpoint and that
matrix. The segment's norm and length are bounded by the endpoint maximum
and the full difference respectively. The determinant difference bound follows
by telescoping its two columns and Hadamard's inequality. Singular endpoints
are included. The inertia indicator itself is discontinuous; (J13) makes
no Lipschitz assertion about that indicator.

The pivots -6 and +6 in (J11) give exactly

    F_2(L_M)=(6lambda+3B1-gamma^2/4)_+,
    F_1(L_S)=(6lambda-3B1+gamma^2/4)_+.                (J14)

Thus their product is w_lambda for all signed lambda and all t, including
typing edges. If lambda<=0, both factors cannot be strictly positive because
their sum before taking positive parts is 12lambda, so the product vanishes.

Define D_r=W_r/r^4. Positive scalar rescaling preserves inertia, and the
determinant of a 2 by 2 matrix scales quadratically. Therefore exactly

    D_r=F_2(H_M/r)F_1(H_S/r).                         (J15)

Let D=1+Lambda+|t| and T=C(D+rN) bound the four endpoint/model operator norms.
Each filtered determinant is at most T^2. By (J12)–(J13) and the product
difference inequality,

    |D_r-w_lambda|<=C rN(D+rN)^3,
    D_r<=C(D+rN)^4.                                  (J16)

Taking the further conditional expectations in (J10), using r<=1, proves

    |E[D_r | U_r=v_r,A=-r lambda,t]-w_lambda(t)|
                    <=C_Lambda r(1+|t|)^4,
    E[D_r N^p | U_r=v_r,A=-r lambda,t]
                    <=C_{Lambda,p}(1+|t|)^(p+4).      (J17)

For the first line expand rN(D+rN)^3 and use moments through order4.
For the second, (D+rN)^4<=8(D^4+(rN)^4) and use orders p and p+4.
This step preserves the actual weight rather than replacing it by its limit.

## 4. Disintegration, density rate and full normalization

The change of variable A=-r lambda has absolute Jacobian r. Combining this
with W_r=r^4 D_r proves the exact density identity

    g_r(lambda,t)=rho_r(-r lambda,t)
                      E[D_r | U_r=v_r,A=-r lambda,t]. (J18)

Indeed the numerator in (J1) is r^5 times the integral of the right side.
Tonelli applies to these nonnegative integrands. Equations (J9) and (J17)
also prove finiteness of all the polynomial-weighted integrals used here.

Subtract g_0 by first comparing the conditional determinants, then comparing
the densities. On D_Lambda, w_lambda<=C_Lambda(1+|t|)^4. Thus (J9), (J17)
and (J18) give the integrable pointwise bound

    |g_r-g_0|<=C_Lambda r(1+|t|)^6 exp(-c|t|^2).        (J19)

Integration against (1+|t|)^q proves (J3), for every fixed finite q. Gaussian
integrability here is explicit and uniform; no differentiation of a weak
limit or unproved exchange of limits is involved.

For any lambda in (0,Lambda), the weight at t=0 is 36lambda^2>0. The joint
Gaussian density is strictly positive, so integration over a small open box
around lambda=Lambda/2,t=0 gives m_Lambda>0. On one fixed such box the
Gaussian means and eigenvalues range over a compact set; the density has a
positive uniform lower bound. Shrinking the box once keeps w_lambda bounded
below there. This proves a uniform m_*>0. The upper bound follows from the
Gaussian majorant. The same compact-parameter argument applied to the
nondegenerate conditional Gaussian A on a fixed negative interval gives a
uniform positive lower bound for z_0 in (J2), with a finite upper bound.

The full normalizer estimate is [R](R10), specialized to k=1 and b in B0:
|Z_r/r^2-z_0|<=Cr. To spell out its interface, under the centered common
regression coupling the transverse A at the pins differs by O(rT) from
contact, with all moments of T uniformly finite. Congruence by
diag(r^(-1/2),1) transforms each actual Hessian to
[[alpha_i,sqrt(r) beta_i],[sqrt(r) beta_i,A_i]],
where alpha_i=+-6+O(rT), beta_i=O(T). Removing the sqrt(r) off-diagonal
changes a filtered determinant by at most r beta_i^2, including at singular
A_i: the determinant is affine in r, and an inertia change crosses its zero.
Then (J13) bounds the remaining diagonal comparison by CrT^2. The reference
product is 36 A^2 1{A<0}; multiplying and using the uniform moments gives
the stated O(r) expectation estimate. This is the corrected inverse-square-
root congruence from E1; no false O(sqrt(r)) loss is inserted. Decrease r0
so z_r>=z_*/2. This establishes (J4) for the FULL Z_r.

Now exactly r^(-3)Q_r^W(E)=mu_r(E)/z_r. By adding and subtracting g_0/z_r,
using (J3), |1/z_r-1/z_0|<=Cr and the finite weighted integral of g_0,
we obtain (J5). In particular the unnormalized soft-layer mass is
r^5 m_Lambda+O(r^6); division by the full r^2 z_r gives r^3, not r^5
and not a conditional normalizer restricted to the layer.

## 5. Weighted failures on growing windows

[C91] gives |E_r|_j<=K_j N r w^(4-j) for every C4 field obeying the pins
and the stated geometric window restriction. Thus

    1{|E_r|_j>epsilon}
                <=(K_j r w^(4-j)/epsilon)^p N^p.

Multiply by the actual D_r in (J18), integrate rho_r(-r lambda,t), and use
(J9),(J17). This yields

    r^(-5) E_{Q_r}[W_r 1{|lambda|<=Lambda}
                           1{|E_r|_j>epsilon}]
                <=C_{Lambda,p}(K_j r w^(4-j)/epsilon)^p. (J20)

Division by Z_r>=r^2 z_*/2 proves (J6). For beta,eta in (J7), beta<1 ensures
2rw<=L/4 eventually; 4beta+eta<1 ensures the smallest exponent among
1-(4-j)beta-eta is positive. A union bound proves (J7), and the lower
soft-layer mass in (J5) proves its conditional version. All events and
derivative suprema are measurable on C4. QED.

## 6. What this result can and cannot supply downstream

For any measurable jet event in D_Lambda, (J3) controls the actual weighted
mass by the model mass with O(r) error after r^5 rescaling, uniformly even
for r-dependent events. More generally it controls measurable observables
bounded by a fixed multiple of (1+|t|)^q. This includes discontinuous typing
or fixed-margin cutoffs in these jets. It does not control observables with
unbounded inverse typing margins merely because the jet weight vanishes at
the boundary.

The Taylor statement controls field errors jointly with the soft layer under
the actual determinant weight. To infer pairing loss still requires a valid
deterministic decision certificate, window containment and quantitative
integration of any jet-dependent margins. Unbounded lambda tails, all-mark
uniformity, shrinking collisions, intermediate/remote/coarea composition and
the equality of critical-pair and persistence coefficients are not closed by
this note. No whole-field total-variation convergence, global probability
normalization of w_lambda rho_0(0,t), evaluated numerical constants, new
theorem-level status, human review or organizational independence is claimed.

Exact rational controls for matrices, Jacobians, pin scalings and negative
mutants can test transcription and algebra. The analytic proof above, and
its substantive nonauthor review, are necessary for the Gaussian density
and moment assertions; a finite list of tests cannot establish them.
