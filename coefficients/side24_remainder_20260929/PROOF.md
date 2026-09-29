# SIDE24: a second-order remainder and the sign of the finite-size correction

Object: **OA-SIDE24-REMAINDER-20260929-v1**.
Author: OpenAI / GPT-6 Astra Pro, foreground session, 29 September 2026.
Disposition: **AUTHOR-SIDE ANALYTIC CANDIDATE; non-OpenAI review required**.
Scientific effect: **NONE**. No existing proof bytes, review dispositions, registers,
claims, premises, prizes, or `lemma_closed` flags are changed. No self-merge.

## 1. Exact object and results

Let c_(d,L) mean exactly the coefficient expression (15.2) of the reconciled
UNIFORM-MATRIX-CAP-LIFETIME parent, with its exact variance-one covariance

    K_L(x) = [sum_(n in Z^d) exp(-|x+Ln|^2/2)] /
             [sum_(n in Z^d) exp(-|Ln|^2/2)].

Let c_(d,ref) be the same expression evaluated on the Euclidean covariance
exp(-|x|^2/2). It is a local reference expression, not an infinite-volume
persistence theorem. All source identities and the parent's complete reading-rule
set are in SOURCES.json, bound to Math- main e1ca400b3414e5a7bec13b91bc4f1e5293df32be.
Interpreting this expression as the persistence asymptotic constant still consumes
that parent with its amendments; this note does not independently revalidate it.

**Theorem R (candidate).** For d = 2 and d = 3, put z = exp(-288). Then

    |c_(d,24)/c_(d,ref) - 1 - P_d(24) z| < 10^(-216),       (R1)

where

    P_d(L) = -10 L^6/[3(d+2)(d+4)] + (d+4)L^4/(d+2) - d L^2,
    P_2(24) = -26045568,
    P_3(24) = -620813376/35.                                (R2)

In particular c_(d,24) < c_(d,ref) for both dimensions. Section 7 supplies an
explicit rational bound, rather than an unspecified constant in a big-O term.
RESULTS.json encloses both full relative corrections by outward rational endpoints.
The existing coefficient intervals in coefficients/side24_v1 are left unchanged.
No finite-radius persistence error bound, RN/24-jet result, or theorem-status fold
follows from (R1).

**Proposition V.** Formula P_d(L) in (R2) is the first normalized nearest-image
variation of the same coefficient expression for every fixed integer d >= 2.
Only d = 2,3 receive the numerical remainder (R1); no dimension-uniform estimate
is asserted. At d = 3 the polynomial agrees with Claude's reviewed first-variation
packet (Math-#144). We rederive it in Section 5, so that unmerged packet is a
comparison source, not an unverified runtime dependency.

## 2. A fixed-subspace Gaussian integral removes moving cone boundaries

For each axis u choose any orthonormal frame. Write m=d-1, G=grad f,
t=partial_u^3 f, H=Hess f, V=Hu, and A for the transverse m by m Hessian block.
Use the full covariance C of X=(G,t,svec H); svec uses sqrt(2) times off-diagonal
entries and diagonal entries unchanged. The ambient dimension and the free
subspace dimension after pinning G=0 and V=0 are

    n = d+1+d(d+1)/2,             k = 1+m(m+1)/2.

Denote that fixed linear subspace by E. On E use the nonnegative weight

    h(t,A) = |t|^(4/3) det(A)^2 1{A negative definite},
    p = degree(h) = 4/3 + 2m,    nu = k+p.

The function h is measurable, bounded on the unit sphere, and positively
homogeneous. It is not differentiated. Define

    F_u(C) = integral_E h(x) phi_C(x) dx_E.                 (R3)

Because the stationary covariance is even, the odd block (G,t) is independent
of H. Disintegration on the pinned coordinates therefore shows

    F_u(C) = 2^(-m/2) M_(4/3) p_G(0) p_V(0)
                         tau_u^(4/3) D_u,                 (R4)

where M_(4/3)=E|N(0,1)|^(4/3)>0 is independent of C,
tau_u^2=Var(t|G=0), and D_u=E[det(A)^2 1{A<0}|V=0].
The factor 2^(-m/2) comes from pinning sqrt(2)H_(uj) rather than H_(uj).
It cancels in all ratios and derivatives of ratios. Thus the parent's (15.2)
is a positive constant times the angular integral of (R3).

This representation uses the FULL covariance of the periodic jet. The periodic
field need not be rotationally invariant. In particular its coefficient is NOT
claimed to depend only on three isotropic moment scalars. Changing the transverse
frame is an orthogonal coordinate change preserving h, so no globally continuous
choice of transverse frame is required.

## 3. Explicit second-order covariance bound

Here is a general calculation for (R3). Let C_0 be positive definite, Delta
symmetric, C_s=C_0+s Delta for 0<=s<=1, and

    e = ||C_0^(-1/2) Delta C_0^(-1/2)|| <= 1/4.

At a point x in E put B=C_s^(-1/2) Delta C_s^(-1/2),
y=C_s^(-1/2)x, and R^2=|y|^2. Differentiation of the ambient Gaussian density gives

    (log phi)'  = -tr(B)/2 + y^T B y/2,
    (log phi)'' =  tr(B^2)/2 - y^T B^2 y.                  (R5)

The negative sign in the second quadratic term matters. The covariance sandwich
implies ||B|| <= e/(1-e). Therefore

    |phi''| <= [e/(1-e)]^2 phi
               [(n+R^2)^2/4+n/2+R^2].                    (R6)

All differentiations under the E integral are justified directly by a uniform
Gaussian majorant times a polynomial on this compact positive-definite path.
The cone indicator causes no difficulty because it is a fixed part of h.

Under the probability measure proportional to h(x)phi_(C_s)(x)dx_E, R^2 has a
chi-square radial distribution with parameter nu=k+p (not necessarily an integer).
Indeed C_s^(-1/2) maps E linearly onto a k-dimensional subspace; its constant
Jacobian and the angular part of the homogeneous weight cancel on normalizing.
The radial density is proportional to R^(k+p-1)exp(-R^2/2). Integration by parts
then gives E R^2=nu and E R^4=nu(nu+2). Consequently

    |F_u''(C_s)| <= K(n,nu) [e/(1-e)]^2 F_u(C_s),
    K(n,nu) = [n^2+2n nu+nu(nu+2)]/4+n/2+nu.              (R7)

For d=2: (n,k,p,nu)=(6,2,10/3,16/3).
For d=3: (n,k,p,nu)=(10,4,16/3,28/3), and K=1012/9.
The latter bounds the former term by term. Comparing the determinant and inverse
quadratic form in the density, followed by scaling on E, gives

    F_u(C_s)/F_u(C_0)
        <= (1-e)^(-n/2)(1+e)^(nu/2)
        <= (4/3)^5(5/4)^(14/3) <= (5/3)^5 = 3125/243.

Taylor's integral remainder and (1-e)^(-2)<=16/9 now give, for d=2,3,

    |F_u(C_0+Delta)-F_u(C_0)-DF_u(C_0)[Delta]|/F_u(C_0)
       <= (1/2)(1012/9)(16/9)(3125/243) e^2 <= 2000 e^2.  (R8)

The first derivative formula similarly implies, for ANY symmetric R_0,

    |DF_u(C_0)[R_0]|/F_u(C_0)
       <= [(n+nu)/2] ||C_0^(-1/2) R_0 C_0^(-1/2)||
       <= (29/3) ||C_0^(-1/2) R_0 C_0^(-1/2)||.           (R9)

As an independent normalization check, F_u(a C_0)/F_u(C_0)
=a^((k+p-n)/2)=a^(-1/3). The score expectations in (R5) consequently give
first derivative -1/3 and second derivative 4/9 at a=1, exactly as the checker
verifies. Confusing the ambient dimension n with the free dimension k fails this
check. These estimates hold uniformly in u and hence pass to the positive angular
integral defining the coefficient.

## 4. Uniform covariance comparison and reference floor

We use the elementary derivative and reference-matrix bounds of side24_v1
Sections 2-3, recording the constants here. For q<=6 mixed unit directional
derivatives of phi(x)=exp(-|x|^2/2), at |x|>=1,

    |D^q phi(x)| <= 76 |x|^6 exp(-|x|^2/2),
    |D^q phi(0)| <= 15.

The largest coefficient sum is 1+15+45+15=76 at q=6. Let

    B_0=76*24^6+15=14523826191,    z=exp(-288).

For d<=3, grouping lattice points by j=|n|_infinity gives at most 27j^3 points
and |n|^6<=27j^6. The successive ratio in sum j^9 z^(j^2) is at most
512 z^3<1/2. Thus

    sum_(n!=0) |n|^6 z^(|n|^2) <= 1458 z,
    S-1 = sum_(n!=0) z^(|n|^2) <= 1458 z.

A positive rational Taylor sum through degree 20 proves exp(288/125)>10,
so z<10^(-125). Including the exact variance normalization gives, for every
unit directional jet contraction through order six,

    |J_24-J_ref| <= 1458 B_0 z < E,
    E=1458 B_0*10^(-125)=21175738586478*10^(-125).           (R10)

For the full svec covariance, each entry difference is <=2E, the dimension
is <=10, and therefore ||C_24-C_0||<=20E. The reference Hessian covariance
has eigenvalues d+2 on trace and 2 on traceless coordinates. The only nontrivial
odd block is [[1,-3],[-3,15]]; subtracting I/3 gives positive first principal
minor 2/3 and determinant 7/9. The remaining gradient variances are 1. Hence
C_0>=I/3, and uniformly in all frames

    e <= 60E =: e_0 < 1/4.                                (R11)

## 5. First normalized image variation: every fixed dimension

The angular coefficient functional is O(d)-invariant, and the reference jet is
isotropic. Its derivative at that jet is consequently an invariant LINEAR
functional and sees precisely the Haar projection of a perturbation. This is
only a first-derivative assertion; it is not a replacement of the anisotropic
coefficient by its isotropized value at second order.

For a uniform v on S^(d-1), E v_i^2=1/d, E v_i^4=3/[d(d+2)], and
E v_i^6=15/[d(d+2)(d+4)]. These follow by factoring a standard Gaussian into
independent radius and uniform direction and using its second, fourth and sixth
moments. Apply the Hermite identities to the 2d nearest images +/-Le_i and
subtract their normalizer contribution 2d z times the reference jet. The
projected spectral variations, per unit z=exp(-L^2/2), are

    da   = -2L^2,
    dm4  = 6L^4/(d+2)-12L^2,
    dchi = -30L^6/[(d+2)(d+4)]+90L^4/(d+2)-90L^2.          (R12)

The reference isotropic moments are (a,m4,chi)=(1,3,15). Along an isotropic
family, finite Gaussian conditioning gives

    p_G proportional to a^(-d/2),
    p_V proportional to m4^(-d/2),
    tau^2=chi-m4^2/a=(a chi-m4^2)/a,
    D_u proportional to m4^(d-1).

For completeness, Cov(V)=diag(m4,m4/3,...,m4/3). The transverse Hessian
conditional on V=0 has covariance m4/3 times its reference covariance:
conditioning on H_uu subtracts m4/9 from every diagonal-diagonal covariance,
leaving (m4/3)[(2/3)delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk].
The cone determinant-square moment scales as m4^m. Therefore

    Phi proportional to a^(-d/2-2/3) m4^(d/2-1)(a chi-m4^2)^(2/3),
    d log Phi = (1-d/2)da+(d/6-1)dm4+dchi/9                 (R13)

at the reference. Substitution of (R12) gives exactly (R2). The checker derives
the polynomial by both (R12)-(R13) and the closed expression, for d=2,...,20;
the displayed rational algebra itself proves it for every fixed integer d>=2.

## 6. Deep images AND the normalization product

Fix any directional contraction of order <=6 and write its unnormalized
numerator as a_0+a_1+a_2, where a_1 is the nearest-image contribution and a_2
contains the remaining images. Write the denominator as 1+s_1+s_2, with
s_1=2d z<=6z. Its first normalized variation is b_1=a_1-s_1 a_0. Exactly,

    J_24-J_ref-b_1
       = [a_2-s_2 a_0-b_1(s_1+s_2)]/(1+s_1+s_2).          (R14)

The last product MUST be retained. Even in one dimension, division by
1+2z+O(z^4) produces a quadratic term. For example the second covariance
derivative is -1+2L^2 z-4L^2 z^2+O(z^3), not its linear part plus O(z^4).
This clarification does not change the first variation accepted in Math-#144.

For the deep images define T_6=sum_(|n|^2>=2)|n|^6 z^(|n|^2). In dimension 3,
the j=1 shell has 20 non-nearest points, each with |n|^6<=27 and |n|^2>=2;
its contribution is <=540z^2. For j>=2 the successive ratio is bounded by
(3/2)^9 z^5<1/2, so the remaining contribution is at most

    729 * 2 * 2^9 z^4 = 746496 z^4 < z^2.

Thus T_6<541 z^2. The same bound holds in dimension 2 by embedding Z^2 in Z^3.
It follows that |a_2-s_2 a_0|<=B_0 T_6 and |b_1|<=6B_0 z. Combining (R14)
with S-1<=1458z gives the explicit contraction bound

    |J_24-J_ref-J_24^(1)| < (541+6*1458) B_0 z^2
                          =9289 B_0 z^2.                  (R15)

Here J_24^(1) includes the nearest-image normalizer subtraction; it is not just
the raw six-image numerator. By the same full-matrix and reference-floor
conversion as (R11), its covariance remainder R_0 satisfies

    ||C_0^(-1/2) R_0 C_0^(-1/2)||
          < 60*9289 B_0*10^(-250) =: rho_0.               (R16)

## 7. Combine the bounds and determine the sign

Use Taylor's formula (R8) with the FULL exact Delta=C_24-C_0, then split its
linear term into the nearest normalized variation and R_0. Equations (R9),
(R11), (R16), and the first variation (R2) give

    |c_(d,24)/c_(d,ref)-1-P_d(24)z|
        < 2000 e_0^2+(29/3)rho_0 = R_rat,

    R_rat = [2000(87480 B_0)^2+580*9289 B_0]10^(-250)
          < 10^(-216).                                    (R17)

All constants in (R17) are explicit integers/rationals and checked without
floating point. This proves the candidate (R1). The weaker lower bound
z>10^(-126) follows from exp(16/7)<10, proved by a positive Taylor polynomial
through degree 40 plus its geometric tail. Both |P_2(24)|10^(-126) and
|P_3(24)|10^(-126) exceed R_rat, so both full relative corrections are negative.

For tighter displayed rational intervals the checker encloses exp(9/32) by
its degree-100 positive Taylor sum and an exact geometric remainder, takes
reciprocals, and squares ten times, rounding outwards on a 10^(-260) rational
grid. Since 1024*(9/32)=288, this encloses z. Multiplication by the NEGATIVE
P_d reverses endpoints; subtraction/addition of R_rat then encloses the full
relative correction. No floating-point comparison supplies proof evidence.

## 8. Verification, interpretation, and review request

Local test-first evidence: all 11 tests failed at the intended missing-
implementation assertion before check.py existed. After implementation, the
11 tests pass. Replays in normal and optimized Python and six semantic
mutants are recorded separately; RESULTS.json is deterministic output.
Finite controls check the rational ledgers and analytic calibrations only.
They do not prove differentiation under the integral, radial disintegration,
angular invariance, or the infinite lattice estimate; those are the arguments
above and are the nonauthor review obligations.

Primary external reconnaissance: Voigtlaender's generalized Price theorem
supports covariance smoothness for Gaussian pairings with tempered distributions,
which includes polynomially growing weights supported on a linear subspace.
The explicit constants here are derived directly and are not attributed to that
paper. Full bibliographic details and the unsuccessful Consensus request are in
RECONNAISSANCE.md. No novelty claim is made.

Requested non-OpenAI review slices:
A. Fixed-subspace representation (R3)-(R4), radial moments and Taylor bound (R5)-(R9).
B. Haar first-variation projection versus the FULL anisotropic second-order bound.
C. Deep-shell and normalization ledger (R14)-(R17), outward intervals and sign.
The parent remains an imported source, not something this author has independently
re-reviewed. Same GitHub account as the other lanes; zero organizational-
independence credit. No status transition or merge is requested before review.
