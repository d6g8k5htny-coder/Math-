# Actual fold admission for smooth Gaussian fields with dense smooth support

Author proposal, 17 October 2026. Mathematical authors: OpenAI/Codex
smooth_full_support_universality_20261017 and root (mechanism coauthor).
Status: AUTHOR PROPOSAL, not an independently reviewed or adopted theorem.
This is a new admission theorem for an explicit class of actual infinite
Gaussian laws. It consumes, rather than republishes as new, the existing
conditional structural theorem ST and its deterministic elder-transfer lemma.
The exact consumed files and their full read extents are in INPUT_MANIFEST.json.
All output is local. There is no Lean, numerical field realization, new
scientific acceptance, point-process assertion, or homology-degree extension.

## 1. The law, theorem and distinction from the previous conditional result

Fix a connected compact boundaryless smooth manifold X, a smooth Riemannian
metric g, and a fixed dimension d >= 1. Write V = vol_g(X). Choose deterministic
real functions phi_j in C-infinity(X), j >= 1, such that their real linear span
is dense in the usual C-infinity topology. Choose strictly positive a_j with

    A_q = sum_j a_j ||phi_j||_Cq < infinity, for every integer q >= 0.       (1)

The norms can be the increasing norms sum_{h<=q} sup_X |nabla^h f|_g;
coordinate norms from a finite atlas are equivalent. Let Z_j be independent
standard real Gaussians and define the actual law by

    F = sum_j a_j Z_j phi_j.                                             (2)

Neither stationarity, constant variance, isotropy, parity, a flat metric, nor
a distinguished global frame is required. The independent Gaussian law and
the full dense support are substantive hypotheses. The covariance is the
actual smooth kernel K(p,q) = sum_j a_j^2 phi_j(p) phi_j(q).

**Admission theorem (subject to the explicit classical imports in Section 12).**
Every law (2) satisfying (1) and the dense-span condition supplies all five
interfaces COUNT, CONTACT, SELECT, ENVELOPE and FAR of ST. In particular the
expected finite ordinary superlevel-H0 elder-bar measure, per volume, has the
canonical finite nonnegative Borel density representative nu defined below,
with

    nu(ell) ~ C_F,g ell^(-1/3),
    E N_bar((0,t]) / V ~ (3/2) C_F,g t^(2/3),                  t -> 0+,    (3)

and 0 < C_F,g < infinity. The essential class is excluded. The coefficient
is the exact local covariance functional (25), or equivalently (27).
The same leading coefficient holds for the ordered maximum/index-(d-1)
candidate-pair density. No selected-density continuity is asserted.

All constants in the proof belong to this one fixed law, metric and dimension.
The class genuinely allows changes in covariance, geometry and dimension;
it asserts admission separately for each member. It does not give constants
uniform over all such changes, degenerating spectra, varying metrics, or
unbounded dimensions. It does not give a small-lifetime numerical window.
For d=1 no transverse block is present; the argument uses the one-dimensional
version of ST's elder lemma and remains valid.

ST alone did not prove full jet rank, conditional remote genericity, or field
admission on arbitrary manifolds. The new content here is proving those facts
for (2) from the dense smooth span, together with same-law infinite Gaussian
regression and finite-block incidence at literal conditioned targets. The
previous exact periodized-Gaussian adapter IG is a model for some arguments,
not a premise asserting this broader admission.

## 2. Nonemptiness, smoothness, moments and full smooth support

The hypotheses are nonempty on every such X. A direct dense system can be
built as follows. Choose finitely many coordinate cubes U_i covering X,
coordinates z_i with image (-pi,pi)^d, a smooth partition of unity rho_i with
compact support in U_i, and smooth cutoffs chi_i supported in U_i and equal
to one on supp rho_i. Include the globally extended smooth functions

    chi_i cos(n.z_i), chi_i sin(n.z_i), n in Z^d,

and optionally the constant 1, in a countable list. For any smooth f,
rho_i f in these coordinates extends by zero to a smooth periodic function.
Repeated integration by parts makes its Fourier coefficients decrease faster
than every polynomial. Its Fourier partial sums converge in every Cq norm.
Multiplying those sums by chi_i and summing i converges to sum_i rho_i f = f
in C-infinity. This proves dense real span. The only manifold construction
used is the named smooth finite partition/cutoff fact, not an unproved
spectral completeness claim. Fourier coefficient decay proves the required
smooth convergence directly. No Laplace eigenfunction claim is needed.

For any such list one explicit choice is

    a_j = 2^(-j) / (1 + max_{0<=q<=j} ||phi_j||_Cq).                      (4)

For a fixed q, the finitely many j<q are harmless, and each j>=q term of
(1) is at most 2^(-j). Thus (4) meets every summability requirement and
has a_j>0. One may vary the positive weights and the dense list.

Let B_q = sum_j a_j |Z_j| ||phi_j||_Cq. Its expectation is finite, so B_q
is finite almost surely. Intersect over integer q. Uniform absolute
convergence of all derivative series proves that (2) is a smooth field,
and ||F||_Cq <= B_q. For p>=1, Minkowski gives

    ||B_q||_Lp <= A_q ||Z_1||_Lp < infinity.                            (5)

Lower positive moments follow from the p=1 bound or larger moments.
Thus every Cq norm has all finite positive moments. Differentiating the
covariance termwise is justified: the required products of summable
nonnegative derivative bounds are summable. This also proves that K is
smooth on X times X. The smooth random element is Borel as an almost sure
C-infinity limit; define it arbitrarily on the null complement.

For completeness, its topological support is all of C-infinity(X). A basic
neighborhood of h contains a Cq ball of radius epsilon. Choose a finite
linear combination h_N of the phi_j with ||h-h_N||_Cq < epsilon/3. Increase
N, adding zero coefficients, until E||sum_{j>N} a_j Z_j phi_j||_Cq is less
than epsilon/6. By Markov the tail has Cq norm < epsilon/3 with positive
probability. Independently, the first N Gaussian coefficients fall in a
small neighborhood of the coefficients of h_N/a_j with positive probability,
giving prefix error < epsilon/3. Their intersection is positive. This
support proof uses no assertion that the infinite standard coefficient
sequence belongs to unweighted l2; it does not.

## 3. Dense smooth span proves all needed finite minors

We first prove a finite-dimensional lemma. Let L_1,...,L_m be continuous
linear functionals on C-infinity(X) that are linearly independent. Then the
matrix with columns (a_j L_i phi_j)_i has row rank m, and some finite set
of columns already has row rank m. Indeed, if its column span were proper,
a nonzero c in R^m would annihilate all columns. Since a_j>0 and the span
of phi_j is dense, sum_i c_i L_i would vanish on all smooth functions,
contradicting independence. A spanning subset of R^m has a finite basis.
Consequently

    Cov(LF) = sum_j (a_j L phi_j)(a_j L phi_j)^T > 0.                    (6)

For the local rows used here independence is proved, not postulated.
At finitely many distinct sites take disjoint coordinate neighborhoods
and cutoffs equal to one near each site. A polynomial of degree at most
s in a neighborhood, multiplied by its cutoff, realizes any prescribed
s-jet at that site while killing all jets at the other sites. Coordinate
jets and covariant scalar derivatives up to a finite order differ by an
invertible triangular transformation. In a normal chart, the particular
third axial derivative along a geodesic and parallel frames is its third
Taylor coefficient when the gradient is zero; independence in any case
also follows from the triangular jet transformation. Thus independent
components of finitely many jets at distinct sites are independent
continuous distributions on C-infinity(X).

Fix a unit u at x and an orthonormal frame (u,v_1,...,v_{d-1}). Precisely
the following maps therefore have full row rank for the actual field and
for a suitable finite coefficient block:

1. grad F(p), and (grad F(p),grad F(q)) for p!=q.
2. O_pq = (F(p),grad F(p),F(q),grad F(q)), 2d+2 rows.
3. U_0 = (F,F_u,F_uu,F_uuu,(F_vi,F_uvi)_i) at x, 2d+2 rows.
4. U_0 enlarged by the (d-1)d/2 independent symmetric entries of
   A = Hess F restricted to u-perp. No axial-column entry is duplicated.
5. U_0 together with (F(p),grad F(p)), p!=x.
6. U_0 together with both first jets at p,q, where x,p,q are distinct.

Items 3-4 are independent subsets of the full third jet at x; items 5-6
join disjoint-site jets. This is also a proof of the needed conditional
remote ranks. If the block matrix (U_0,J) is surjective, then J restricted
to ker U_0 is surjective: lift (0,y) for any y. Therefore the free
coefficient directions after the exact contact pin still realize every
listed remote first jet, even though the pinned contact coordinates
have zero conditional variance. The conditional covariance of A is
positive on all its independent symmetric entries by item 4.

There is no claim of a uniform finite block over colliding site tuples.
On any compact separated tuple domain, continuity and a finite cover
let us take the union of finitely many witnessing column sets. That
one finite block has the required rank throughout that domain. Full
covariance eigenvalues have positive floors on such compact domains.
For U_0 and the enlarged contact map, compactness of the orthonormal
frame bundle gives a uniform floor. Frames may be handled in finitely
many local trivializations; a global perpendicular frame is unnecessary.

For fixed x,u the remote domains can be exhausted by dist(x,p)>=1/n,
and dist(x,p),dist(x,q),dist(p,q)>=1/n. A finite block exists for each
nonempty compact domain. Countably many blocks and covers are enough
for the conditional arguments below. A single finite block working
arbitrarily close to the contact is neither assumed nor needed.

## 4. Exact contact observations and same-law Gaussian regression

Choose r_0 below a uniform short-geodesic scale, to be decreased later.
For 0<r<=r_0 put M=exp_x(-ru/2), S=exp_x(ru/2); transport the displayed
frame parallel along the geodesic. Write h_M,h_S for endpoint values,
g_uM,g_uS for axial derivatives and g_iM,g_iS for transverse derivatives.
The literal observations are

    U_r = ((h_M+h_S)/2, (h_S-h_M)/r, (g_uS-g_uM)/r,
       (6/r^2)(g_uM+g_uS-2(h_S-h_M)/r),
       ((g_iM+g_iS)/2,(g_iS-g_iM)/r)_i).                              (7)

Their exact target for heights b,b-kr^3 and zero gradients is

    v_r = (b-kr^3/2,-kr^2,0,12k,(0,0)_i), k>0;
    v_0 = (b,0,0,12k,(0,0)_i).                                       (8)

The transform from O_MS has absolute determinant 12 r^(-(d+3)).
The contact rows in Section 3 are exactly the r=0 extension. Integral
finite-difference identities for a one-dimensional restriction and its
parallel transverse derivatives show

    |U_r f| <= C ||f||_C3,
    |(U_r-U_0)f| <= C r ||f||_C4.                                    (9)

Constants are uniform over the compact frame bundle. The fourth row
is a bounded weighted average of the third axial derivative (its
constant-third-derivative value is that derivative); the other divided
rows are averages of derivatives of order at most two. These integral
identities avoid divergent separate bounds on the summands of (7).

Set Sigma_r=Cov(U_r F) and c_r(z)=Cov(F(z),U_r F). Equations (5),(9)
and the covariance series give uniform Sigma_r -> Sigma_0 and
c_r -> c_0 in global Cq for each fixed q. For the latter, apply the
row difference to the smooth covariance in its observation variable,
then differentiate its field variable; (1) supplies every mixed bound.
The contact rank and compactness yield, after shrinking r_0,

    lambda I <= Sigma_r <= Lambda I, 0<=r<=r_0.                       (10)

On one underlying copy of the actual infinite field define

    F_r(z) = F(z)+c_r(z) Sigma_r^(-1)(v_r-U_r F).                       (11)

The observation of this field is exactly v_r. The residual
R_r=F-c_r Sigma_r^-1 U_rF is Gaussian and uncorrelated with U_rF,
hence independent. Independence for a countable dense evaluation set
and continuity proves independence of the entire smooth field.
Thus (11) is the genuine Gaussian conditional law Q_r at every target,
not a pin event with positive probability. It is jointly Borel in
parameters using local frame charts and the explicit formula.

Its residual has full support in exactly the smooth kernel of U_r.
Indeed H_r:f -> f-c_r Sigma_r^-1 U_r f is a continuous linear map on
C-infinity, U_r H_r=0, and H_r f=f whenever U_r f=0. Since F has full
smooth support, every relatively open nonempty subset of ker U_r has
positive H_r F probability: take a point in that subset and its nonempty
open preimage under H_r. The support is contained in the closed kernel,
so it is precisely ker U_r. Translating by c_r Sigma_r^-1 v gives full
support on the affine fiber U_r f=v. This support observation alone
is not used to apply finite incidence; the original finite independent
coefficient blocks and their residual Gaussian coordinates are constructed
separately in Sections 6-7.

At fixed marks and frame, F_r converges to F_0 globally in C4, almost
surely and in every finite Lp norm of C4. The same holds along convergent
parameter sequences. Uniform deterministic bounds on c_r Sigma_r^-1,
combined with (9), give for every q

    ||F_r||_Cq <= ||F||_Cq + C_q ||F||_C3 + C_q(|b|+k).                (12)

The constants are uniform in small r,x,u and all b,k; the random part
has every finite moment. This proves the mean bound for growing targets
as well as compact-mark coupling. It does not require any boundedness
of the infinite raw coefficient sequence or finite-dimensional norm
equivalence for that sequence. The conditional mean is exactly
c_r Sigma_r^-1 v_r; its Cq norm is at most C_q(|b|+k).

## 5. CONTACT, positivity and all-mark ENVELOPE

Under Q_r the exact endpoint gradients vanish. The physical Hessians
in the parallel frames have form

    H_i = [ r alpha_i   r beta_i^T ; r beta_i   A_i ], i=M,S.          (13)

The axial-column average along the geodesic is zero because the endpoint
gradient components agree. The fundamental theorem of calculus bounds
alpha_i,beta_i by C||F_r||_C3. Global C4 convergence and (8) give
alpha_M -> -6k, alpha_S -> 6k, bounded beta_i, and A_i -> A_0.
The exact polynomial identity is

    det H_i / r = alpha_i det A_i - r beta_i^T adj(A_i) beta_i.        (14)

For d=1 the second term is absent and det A=1. The correct inertia
congruence rescales by diag(r^(-1/2),I). Therefore with

    W_r = |det H_M det H_S| 1{H_M<0} 1{index H_S=d-1},
    V_r = W_r/r^2,

one has almost surely

    V_r -> V_0 = 36k^2 (det A_0)^2 1{A_0<0},
    V_r <= C(1+||F_r||_C3)^(2d).                                    (15)

If A_0 is nonsingular and not negative definite the maximum mark fails;
if A_0 is singular the limiting determinant vanishes. Hence no cone-boundary
null assertion is needed for this weighted limit. Section 3 in fact proves
that A_0 has full conditional Gaussian density on Sym(u-perp), at every
literal target. Its mean may depend on b,k. For k>0 the negative-definite
open cone has positive probability and the determinant is nonzero there.
Thus z_0=E_Q0 V_0 is finite and strictly positive. For d=1 it is 36k^2.
Dominated convergence using (12) proves E_Qr V_r -> z_0. Density
convergence pi_r(v_r)->pi_0(v_0) follows from (8),(10).
This discharges CONTACT.

For every b in R,k>0, (12) implies the uniform moment bound
E_Qr V_r <= C(1+|b|+k)^(2d). Moreover the first and fourth entries of
v_r are b-kr^3/2 and 12k. On the bounded r interval this linear map
of (b,k) has a uniformly bounded inverse on its image, so
|v_r|^2 >= c(b^2+k^2). Equation (10) gives the all-mark bound

    12 pi_r(v_r) E_Qr V_r
       <= H(b,k) = C(1+|b|+k)^(2d) exp[-c(b^2+k^2)].                 (16)

The integral of k^(-2/3)H over SX times R times (0,infinity) is finite:
SX has finite volume, k^-2/3 is integrable at zero, and Gaussian tails
beat the polynomial. This supplies ENVELOPE, with one common r_0.
It uses neither inverse curvature moments nor an inverse normalizer.

## 6. COUNT: actual all-Borel Rice and unconditional genericity

Here we prove the finite-incidence reduction for this infinite law.
For a compact site or separated pair domain choose a finite block B of
original independent coefficients whose gradients (or first jets) have
the ranks proved in Section 3. Split F=F_B+T. The complement T is an
independent smooth Gaussian tail. The block keeps its original weights;
there is no truncation approximation or variance renormalization.

Fix a smooth tail realization. In a point chart choose d invertible
coefficient columns in the gradient matrix and split block coordinates
as (a,eta). On a neighborhood with the same minor, the exact equation
for a critical point solves

    a(p,eta)=-B(p)^(-1)[grad T(p)+D(p)eta].                           (17)

The map (p,eta)->(a(p,eta),eta) is smooth between equal-dimensional
spaces. At a zero its derivative is singular exactly when the physical
Hessian is singular; moving-frame derivative terms vanish when the
gradient is zero. Equal-dimensional smooth Sard makes its critical
values Lebesgue-null in coefficient space. The finite Gaussian block
has a density. A finite/countable minor and chart cover, followed by
integration over T, proves that F is Morse almost surely before using
Rice. Compactness then makes its critical set finite.

For the pair-gradient equation use 2d invertible block columns. Its
incidence projection has absolute Jacobian
|det H_p det H_q|/|det B(p,q)| in orthonormal volume coordinates.
Coordinate versions have the matching Riemannian volume factors.
The weighted equal-dimensional area formula applied to this map and
the finite Gaussian density yields, for every nonnegative Borel mark
w of (p,q,F), the root-counting identity on that minor chart.
Partition overlapping chart/minor neighborhoods into disjoint Borel
pieces. Exhaust unbounded coefficient domains by relatively compact
ones, so only local Lipschitzness of the smooth projection is needed.
Integrate eta and T and sum by Tonelli. Exhaust the off-diagonal pair
space by separated compact domains. The result is the extended identity

    E sum_{p!=q, grad F(p)=grad F(q)=0} w(p,q,F)
      = integral_{p!=q} p_(grad F(p),grad F(q))(0)
           E[|det H_p det H_q| w | both gradients=0]
           dvol(p)dvol(q).                                           (18)

The determinant appears once. Neither finiteness nor a conditional
Morse assertion is a premise of this all-Borel identity.

We specify why the kernels in (18) agree with (11) even at zero, not
merely almost every target. In the finite-tail calculation, linear
coefficient change of variables defines the fiber integral at every
gradient target: the selected coefficient minor is invertible and its
Gaussian density is everywhere positive. The tail receives the Bayes
density equal to the block observation density at target-minus-tail,
divided by the full observation density. Given that tail, the block
has its exact affine Gaussian conditional law. Their integrated field
law at each target is the Gaussian regression law: its characteristic
function for any finite evaluation vector is the ordinary finite joint
Gaussian conditional characteristic function, obtained by completing
the finite observation square. This calculation is valid at every
target. Countably many evaluations identify Borel laws on smooth
functions: derivatives are measurable limits of value difference quotients
at a countable set of chart points, and each Cq seminorm is a supremum
of derivative magnitudes over countably many chart points. Rational finite
linear combinations from Section 2 give a countable dense set and hence
a countable norm-ball basis. Thus the smooth Borel sigma-field is generated
by countably many value evaluations, and the law is the same whole-field
kernel. Arbitrary Borel
marks were present in the area formula from the start; continuity of
such marks on a null fiber is never presumed.

On each separated compact domain, first-jet covariance floors and
conditional Hessian moments make the unmarked integral finite. The
conditional two-height Gaussian density given both gradients is
nondegenerate by Section 3 item 2. In (18) the tie mark F(p)=F(q)
therefore has zero integral after height disintegration. Countable
annulus exhaustion proves distinct critical values almost surely.
The analogous point identity and compact gradient covariance floor
also give finite expected total critical-point count.

For clarity, the everywhere Borel actual elder selector can be defined
intrinsically. Fix a countable dense set and a countable basis of small
connected geodesic balls with compact closures. Connection in {f>c}
is equivalent to a finite chain of such balls with all minima of f
on their closures > c. This is a countable Borel test. For a point p,
take the supremum over rational c<f(p) at which it connects by this
test to a dense point of value >f(p), with empty supremum -infinity.
Call the result D_f(p). On the open Morse/distinct-critical-values locus
set sigma(p,q,f)=1 exactly when p is a maximum, q has index d-1,
D_f(p)=f(q)<f(p), and D_f(p) is finite; elsewhere set it to zero.
All these tests are Borel, as in ST Section 2.

The named classical Morse level/handle facts and elementary H0 elder
linear algebra imply once-counting: a maximum creates one component;
an index-(d-1) critical point either merges two or creates no H0 change;
at a merger the lower maximum label dies. Distinct values ensure one
critical point per event. The global maximum yields the one essential
class. The rational supremum recovers the exact closed merger level.
The same argument in d=1 uses minima and intervals on a connected
closed one-manifold. Thus every finite ordinary H0 elder bar is counted
once by sigma, with no unordered-pair factor 1/2.

Apply (18) to the type/selector mark and disintegrate both heights
using the canonical Gaussian kernels. This gives the exact density
representative for ell>0

    nu(ell)=V^(-1) integral_{p!=q} integral_R
       p_O(b,0,b-ell,0) E_Q[W_pq sigma(p,q,F)] db dvol(p)dvol(q).        (19)

It is initially nonnegative Borel; its finiteness and local integrability
follow from the near and far bounds below. This supplies COUNT for the
same versions used in CONTACT, not independently chosen fibers.

## 7. Fixed-target conditional remote genericity

Fix a literal x,u,b,k with k>0 and condition on U_0 F=v_0. This law has
a forced degenerate critical point at x and is not globally Morse.
We prove its precise off-contact genericity independently of the
unconditional result. For each compact domain away from x, or pair
domain separated from x and the diagonal, take a finite block B with
the joint contact/remote ranks of Section 3. The block contact covariance
Sigma_B is positive. For F=F_B+T, under the canonical contact law the
tail distribution is exactly

    dmu_tail,v(t)/dmu_tail(t)
       = p_(U_0 F_B)(v_0-U_0 t)/p_(U_0 F)(v_0).                       (20)

The denominator is positive and the density integrates to one by
Gaussian convolution. This is an actual fixed-target Bayes identity.
The conditional tail remains smooth since it is absolutely continuous
with respect to the original smooth tail law.

Given T=t, let L_B be the contact matrix in the standard finite block
coordinates. The conditional block coefficients are

    xi_B = L_B^T (L_B L_B^T)^(-1)(v_0-U_0 t) + P_B z,
    P_B = I-L_B^T (L_B L_B^T)^(-1)L_B.                                (21)

Choose an orthonormal basis of ker L_B. The free coordinates of P_B z
in that basis are independent standard Gaussians, for every literal
target and every smooth tail. The deterministic mean in (21) need
not vanish. Joint rank implies that these free directions realize
arbitrary remote first jets; this is exactly the restricted-kernel
linear algebra proved in Section 3.

For the one-point residual gradient, repeat (17) in the free coordinates.
Smooth Sard proves that all critical points in the compact domain are
Morse, for almost every conditional block vector. Integrate (20) and
exhaust X minus {x} by countably many compact domains. Thus every
other critical point is Morse under this fixed contact law.

All residual covariance floors needed for the following Rice estimates
hold only on the particular separated compact domain. Additional finite
Gaussian regression there and (12) bound the conditional Hessian moments,
so the local unmarked expectations are finite. No floor as a site approaches
x or another site is used.

The same residual one-point area formula has a nondegenerate conditional
height given residual gradient, since the residual first-jet map is
surjective. The mark F(p)=b has zero expectation on each domain, so
no other critical value equals b. The residual two-point area formula
has a nondegenerate two-height law given both gradients; the tie mark
F(p)=F(q) has zero expectation on each separated domain. Exhaustion
proves pairwise distinct off-contact critical values. Covariance floors
are only used on the separated domains, where they are available.
Different domains may use different finite blocks; each conclusion
is a property of the same canonical whole-field Q_0, so their countable
intersection is still probability one. No conclusion about all literal
targets simultaneously has been drawn.

The conditional A_0 is invertible almost surely, by its full Gaussian
density (or is empty in d=1). Its transverse implicit ridge exists near
x. The reduced function has first and second derivatives zero at x
and third derivative 12k>0. Its reduced derivative is positive at every
sufficiently small nonzero axial coordinate, since its Taylor expansion
is 6k s^2 + o(s^2). Thus x is the only critical point in a neighborhood.
This isolation does not require A_0<0, only invertibility. The remaining
critical set is contained in a compact set away from x and all its
points are isolated Morse points. It is therefore finite: an infinite
subset of a compact set would have an accumulation point which is also
critical and hence would fail isolation. Its critical values have
finite positive gaps from b and one another.

This proves exactly the contact-global genericity premise of ST's
deterministic elder theorem, for each fixed specified target. It is
not an invocation of unconditional Morse genericity, and it does not
assert Morse behavior at the forced contact itself.

## 8. Actual SELECT through the deterministic elder argument

Use the coupling (11) at fixed parameters. On V_0>0, A_0<0, k>0,
and Section 7 holds almost surely. Thus F_r -> F_0 globally in C4,
with exact endpoint value/gradient pins, a single local cubic contact,
and finitely many other Morse critical branches with distinct heights
separated from b. These are the actual hypotheses of ST Section 4.

To identify its topological content, in a small fixed cylinder a unique
transverse ridge h_r(s) exists, and the reduced derivative has positive
second derivative. The exact critical pins give its only two zeros
at s=+-r/2. The left zero is the maximum, the right zero is the
index-(d-1) point. A left cylinder cut at the right zero has left and
side boundaries strictly below the death level, while its right face
is at most the death level by transverse concavity. The newborn
component is enclosed at every intermediate level. The positive ridge
beyond the right zero reaches a fixed point with height greater than b,
so that branch is older. The closed death-level path through the right
zero reaches that older branch. No earlier remote detour can escape
the cylinder. Persisting other critical branches and the compact
gradient floor make F_r globally Morse with distinct critical values
eventually. Consequently sigma(M,S,F_r)=1 eventually. This is the
actual deterministic elder transfer, rather than candidate identification.
For d=1 the side boundary is absent and the same left interval/right
cut/older ridge argument applies. The argument does not impose a false
height barrier on the entire boundary of a symmetric fold box.

On V_0=0, V_r(1-sigma)->0 regardless of the selector, by (15).
On V_0>0 it vanishes eventually. The moment domination (12),(15)
then gives

    E_Qr[V_r(1-sigma)] -> 0,
    E_Qr[V_r sigma] -> z_0>0.                                        (22)

This supplies SELECT. It also gives the normalized weighted selector
probability tending to one at each fixed mark, but no all-mark inverse
normalizer, rate, or common samplewise physical chart is required.
If desired, compact-mark uniformity follows by convergent-parameter
couplings and a subsequence argument applied to the single limiting
parameter's probability-one genericity event. This extra uniformity
is qualitative and is not needed for (3).

## 9. FAR and finite lifetime representatives

On dist(p,q)>=r_0, the value/gradient covariance O_pq has a positive
floor and finite upper bound, by rank, compactness and continuity.
The actual same-field Gaussian regression at target (b,0,b-ell,0)
has conditional C2 moments bounded by a polynomial in 1+|b| when
ell belongs to a fixed compact interval. In particular for 0<ell<=1,
its density is bounded by C exp(-c b^2), and hence

    integral_R p_O(b,0,b-ell,0)
           E_Q[|det H_p det H_q|] db <= C,
    0 <= nu_far(ell) <= C,                         0<ell<=1.         (23)

This is a direct density bound for the complement of (19). It proves
FAR without differentiating a cumulative estimate or trying to bound
remote bars conditional on a failed local event. The same argument
works on every fixed compact positive-lifetime band.

In the near band (16) controls the canonical integrand. For a fixed
ell>0, k=ell/r^3 cannot approach zero as r<=r_0; Gaussian decay at
large k dominates every power as r->0. Thus that near integral is finite
for every ell>0 and locally bounded on every compact positive-lifetime
interval. This proves the stated finite Borel representative and
local integrability in (19).

## 10. Actual geometry cancellation and positive local coefficient

The short-pair midpoint coordinates (x,h) map to
(exp_x(-h/2),exp_x(h/2)). Their natural volume Jacobian J(x,h) is smooth,
positive, has J(x,0)=1, and is even in h. Its derivative at h=0 is
(a,b)->(a-b/2,a+b/2), absolute determinant one. Pair swapping is
h->-h and preserves both measures. Compactness gives uniformly
J(x,ru)=1+O(r^2) and a common bound. Therefore

    dvol(M)dvol(S)=J(x,ru) dvol(x) r^(d-1)dr d sigma_x(u).

Let B_r=12 pi_r(v_r) E_Qr[V_r sigma]. The radial ledger is

    spatial volume: r^(d-1), height change: r^3,
    observation density: r^(-(d+3)), determinant product: r^2.

Their product is r, in every fixed d>=1. The physical Hessians give
the determinant order; the literal linear observation transform gives
the contact-density order. They are not inferred from the cubic height
gap alone. Curvature changes J at finite r, with leading value one.

The direct fixed-ell substitution in (19) gives

    ell^(1/3) nu_near(ell)
      = (1/(3V)) integral_{SX,R,(0,infinity)}
          1{k>=ell/r_0^3} k^(-2/3)
          J(x,(ell/k)^(1/3)u) B_((ell/k)^(1/3)) db dk dvol(x)d sigma.   (24)

Equations (15),(22) give B_r -> 12 pi_0(v_0)z_0 and (16) dominates
the integrand. Dominated convergence and (23) yield

    C_F,g = (4/V) integral_{SX,R,(0,infinity)}
                k^(-2/3) pi_0(b,0,0,12k,0,...) z_0(b,k,x,u)
                         db dk dvol(x)d sigma_x(u).                  (25)

This is exactly ST's functional, now with all five premises actually
proved for law (2). Each integrand at k>0 is strictly positive: the
contact Gaussian density is positive and the transverse conditional
Gaussian has positive negative-cone determinant weight. Finite volume
and (16) give finiteness; integrating over any nonempty finite mark
window gives strict positivity. Candidate weight has the same limit,
so its leading coefficient agrees. The cumulative factor 3/2 follows
by integration of ell^-1/3; it does not identify the lifetime density
with the cumulative exponent 2/3.

## 11. General Gaussian jet invariant, parity boundary and falsifiability

One may express (25) without a birth integral and without a parity
hypothesis. At a fixed x,u write

    G=grad F(x), V_u=Hess F(x)(u,.), T=nabla_u^3 F(x),
    A=Hess F(x)|_(u-perp).

All components are actual covariant jets in orthonormal frames. Under
the pin G=0,V_u=0, T is the third derivative along the geodesic used
above. It is not assumed independent of A or of those pins. Integrating
b in (25) by the actual Gaussian height disintegration gives

    C_F,g = (144/V) integral_SX integral_0^infinity k^(4/3)
       p_(G,V_u,T)(0,0,12k)
       E[(det A)^2 1{A<0} | G=0,V_u=0,T=12k] dk dvol d sigma.         (26)

Substitute t=12k. Since 144*12^(-7/3)=12^(-1/3), this is

    C_F,g = (12^(-1/3)/V) integral_SX p_(G,V_u)(0,0)
       E[(T_+)^(4/3)(det A)^2 1{A<0} | G=0,V_u=0] dvol d sigma.       (27)

The conditional Gaussian is centered because (2) is centered and the
conditioning target is zero; its full joint T,A covariance is positive
by the jet-rank proof. The expectation is an exact Gaussian fractional/cone
moment of the covariance Schur complement. It remains meaningful without
stationarity or reflection symmetry. In d=1 A is empty, its determinant
and cone indicator are one, and sphere measure on S^0 counts both directions.

There is also an antipodally invariant form without an oriented positive
part. At the same point replace u by -u and keep the perpendicular frame.
The gradient axial entry changes sign; for the Hessian column its axial
entry F_uu stays the same and its transverse entries F_uvi change sign;
T changes sign; A is unchanged. The zero pin is invariant and the pin
coordinate transformation has absolute determinant one. Thus its density
at zero is unchanged and the conditional T,A law is transported to -T,A.
Changing u to -u preserves sphere area, so integrating T_+^(4/3) gives
one half of the integral with |T|^(4/3). Consequently

    C_F,g = [1/(2*12^(1/3)*V)] integral_SX p_(G,V_u)(0,0)
       E[|T|^(4/3)(det A)^2 1{A<0} | G=0,V_u=0] dvol d sigma.         (28)

The universal scalar 1/(2*12^(1/3)) is now separated from a local joint-jet
invariant. This averaging uses both ordered directions in the full sphere;
it is not an additional unordered-pair division by two. Equations (25)-(27)
remain the primary derivation and independently specify the normalization.

Only if the additional odd/even independence is separately established
can (27) be factored into p_G(0)p_Vu(0), a half-Gaussian T moment and
a transverse determinant-cone moment as in ST equation (19). That
factorization has NOT been asserted for the general nonstationary
manifold law. In particular G may correlate with V_u, and T may
correlate with A, even though every field coefficient is Gaussian.
The coefficient can vary with x,u and with the metric and covariance.

The formula has a falsifiable amplitude check: F -> aF, a>0, gives
p_(G,V_u)(0,0) -> a^(-2d) times itself, while the moment gives
 a^(4/3+2(d-1)); hence C_(aF),g=a^(-2/3)C_F,g. If the metric is
multiplied by lambda^2 with the same scalar field, its volume changes
by lambda^d, G by lambda^-1, V_u by lambda^-2, T by lambda^-3,
and A by lambda^-2. The local density product in (27) scales as
lambda^(3d-4-4(d-1))=lambda^(-d), so C scales as lambda^-d,
as required for a per-volume density; the total expected count is
metric-independent. The exponent remains -1/3 because the metric's
short-pair radial order is still d-1.

The hypotheses are not covariance-only conditions for arbitrary laws.
The already preserved amplitude-mixture counterexample F=RH, with
R>0 bounded, E R^2=1 and P(R<=s) of order s^alpha, alpha<2/3,
keeps H's covariance, smooth positive moments and Morse pairings,
but its expected short-bar count is bounded below by c t^alpha.
It violates the claimed t^(2/3) conclusion. This theorem admits the
specified Gaussian law, not every law sharing its covariance.
Likewise dropping dense support may force contact rank collapse or
zero transverse negative-cone weight. Approaching such degeneracy
need not preserve any common constants or usable asymptotic scale.

## 12. Imports, evidence boundaries and status ledger

The result is a conventional proof under these explicit imports:

* Smooth finite coordinate refinements, bump cutoffs and partitions of
  unity on compact smooth manifolds; inverse/implicit-function theorem;
  existence of a uniform short-geodesic scale and smooth parallel frames.
* Equal-dimensional smooth Sard: critical values of a smooth map between
  equal-dimensional finite-dimensional manifolds are Lebesgue-null.
* Weighted equal-dimensional Euclidean area formula for a locally Lipschitz
  map and every nonnegative Borel integrand, with multiplicity; applied
  only on compact subdomains of smooth finite-dimensional incidence maps.
* Classical Morse local form, critical-free compact level-band flow and
  isolated handle attachment for an actual smooth Morse function. ST's
  Borel elder construction and its vector-ridge deterministic elder lemma
  supply the precise H0 use; no separate stochastic selection import exists.
* Elementary finite Gaussian regression, finite joint Gaussian uniqueness,
  Tonelli, Minkowski, dominated convergence and ordinary change of variables.

The finite-jet bump interpolation, actual finite coefficient minors,
residual-rank implication, fixed-target Bayes identity, infinite-field
regression, norm bounds and all five stochastic interfaces were proved
here. No general infinite-dimensional transversality theorem, conditional
Morse theorem, or all-Borel Kac-Rice theorem is imported without proof.
The only global H0 topology imported is the stated deterministic Morse
level/handle package, as already explicit in ST.

Bounded current source checks: the [UT differential-topology notes](https://web.ma.utexas.edu/users/abhishek/files/notes/Differential%20Topology.pdf)
state smooth Sard at Theorem 1.5.1 (page 14 by one-based PDF indexing).
The [author's area/coarea preprint abstract](https://arxiv.org/abs/1305.2968) identifies the general weighted-volume
area/coarea setting. The [Stanford differential-geometry handout index](https://math.stanford.edu/~conrad/diffgeomPage/handouts.html) lists bump,
local-form and Morse handouts. These bounded checks are source pointers;
there was no new full classical-book read or proof of the imported
area formula. The required theorem statements above remain explicit
classical premises. An unsuccessful attempted secondary link resolution
in the browsing session is recorded in READ_EXTENT.json and supplies no
additional evidence.

The exact ST source is 43927 bytes, SHA256
3d952a906553d578876456539a8f0dcd64aedd45099e8394cbe9db99866ec531;
its source-bound review records the fresh incorporated-file PASS after
the preserved earlier half-moment correction. The IG source is 34629
bytes, SHA256 c8bd489ca3fbb3760f7b2d53e7385131ac5336c51ba983e00e4d540fe2f00aaa;
its actual finite-tail/conditional genericity route was read fully.
Their full actual reviews were also read. Exact copies in inputs/
are frozen; no original file was changed. This author is source-exposed,
and root supplied the dense-support mechanism. A distinct nonauthor
mathematical review of these exact new bytes is still required.

Result scope: actual expected finite H0 lifetime intensity for every
fixed member of the explicitly constructed Gaussian class on every
fixed compact connected boundaryless smooth Riemannian manifold of
dimension d>=1. No arbitrary smooth Gaussian law lacking the hypotheses
is silently admitted. No higher-singularity taxonomy theorem, Hk result,
all-mark factorial moment or Poisson limit, blind 50-model validation,
coefficient enclosure, sampler/grid correctness, Lean proof, quantitative
window, manuscript acceptance, external uptake, or scientific promotion
follows. The larger research goal remains active.
